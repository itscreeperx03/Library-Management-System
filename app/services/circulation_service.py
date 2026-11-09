"""
circulation_service.py
======================
Core circulation engine: handles checkout (issue), return, renewals, reservations,
and seamlessly triggers the FineDecisionTable engine upon book returns.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from app.database import get_db_connection
from app.services.fine_calculator import FineDecisionTable
from app.services.member_service import MemberService
from app.services.catalog_service import CatalogService

class CirculationService:
    @staticmethod
    def issue_book(book_id: int, member_id: int, due_days: int = None, notes: str = None, db_path: str = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        try:
            # 1. Validate Member
            cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
            member = cursor.fetchone()
            if not member:
                return False, "Member not found.", None
            member = dict(member)

            if member['status'] != 'Active':
                return False, f"Member account status is {member['status']}. Issue blocked.", None

            # Check unpaid fines
            cursor.execute("SELECT COALESCE(SUM(total_fine), 0.0) as unpaid FROM fines WHERE member_id = ? AND paid_status = 'Unpaid'", (member_id,))
            unpaid_fines = cursor.fetchone()['unpaid']
            if unpaid_fines > 15.0:
                return False, f"Outstanding unpaid fines (${unpaid_fines:.2f}) exceed borrowing threshold ($15.00). Settle fines first.", None

            # Check current borrowed count
            cursor.execute("SELECT COUNT(*) as count FROM borrow_records WHERE member_id = ? AND status IN ('Active', 'Overdue')", (member_id,))
            borrowed_count = cursor.fetchone()['count']
            if borrowed_count >= member['max_books']:
                return False, f"Borrow limit reached ({borrowed_count}/{member['max_books']} books).", None

            # 2. Check if already holding this book
            cursor.execute("SELECT COUNT(*) as count FROM borrow_records WHERE member_id = ? AND book_id = ? AND status IN ('Active', 'Overdue')", (member_id, book_id))
            if cursor.fetchone()['count'] > 0:
                return False, "Member already has an active loan for this book.", None

            # 3. Validate Book availability
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            book = cursor.fetchone()
            if not book:
                return False, "Book not found.", None
            book = dict(book)

            if book['available_copies'] <= 0:
                return False, "No copies currently available for checkout. Consider placing a reservation.", None

            # 4. Determine Loan Duration
            if due_days is not None and str(due_days).strip() != '':
                try:
                    loan_days = int(due_days)
                    if loan_days <= 0:
                        loan_days = member['loan_period_days']
                except (ValueError, TypeError):
                    loan_days = member['loan_period_days']
            else:
                loan_days = member['loan_period_days']

            today = datetime.now()
            issue_date = today.strftime('%Y-%m-%d')
            due_date = (today + timedelta(days=loan_days)).strftime('%Y-%m-%d')

            # 5. Decrement book stock
            cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = ?", (book_id,))

            # 6. Insert borrow record
            cursor.execute("""
                INSERT INTO borrow_records (book_id, member_id, issue_date, due_date, status, return_condition, notes)
                VALUES (?, ?, ?, ?, 'Active', 'Normal', ?)
            """, (book_id, member_id, issue_date, due_date, notes or 'Standard checkout'))
            record_id = cursor.lastrowid

            # 7. If member had a pending reservation for this book, fulfill it
            cursor.execute("""
                UPDATE reservations SET status = 'Fulfilled'
                WHERE book_id = ? AND member_id = ? AND status = 'Pending'
            """, (book_id, member_id))

            conn.commit()

            cursor.execute("""
                SELECT br.*, b.title, b.isbn, b.tier, m.name as member_name, m.member_code, m.member_type
                FROM borrow_records br
                JOIN books b ON br.book_id = b.id
                JOIN members m ON br.member_id = m.id
                WHERE br.id = ?
            """, (record_id,))
            new_record = dict(cursor.fetchone())
            return True, f"Book successfully issued. Due date is {due_date}.", new_record

        except Exception as e:
            conn.rollback()
            return False, f"Database transaction failed: {str(e)}", None
        finally:
            conn.close()

    @staticmethod
    def return_book(borrow_record_id: int, return_condition: str = 'Normal',
                    notes: str = None, return_date_str: str = None, db_path: str = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT br.*, b.id as b_id, b.title, b.tier, b.replacement_cost,
                       m.id as m_id, m.name as member_name, m.member_type, m.status as member_status
                FROM borrow_records br
                JOIN books b ON br.book_id = b.id
                JOIN members m ON br.member_id = m.id
                WHERE br.id = ?
            """, (borrow_record_id,))
            record = cursor.fetchone()

            if not record:
                return False, "Borrow record not found.", None
            record = dict(record)

            if record['status'] == 'Returned':
                return False, "Book has already been returned previously.", None

            # Compute Overdue Days
            effective_return_date = datetime.strptime(return_date_str, '%Y-%m-%d') if return_date_str else datetime.now()
            due_date = datetime.strptime(record['due_date'], '%Y-%m-%d')
            delta_days = (effective_return_date - due_date).days
            days_overdue = max(0, delta_days)

            # Evaluate Decision Table for Fines
            fine_result = FineDecisionTable.calculate(
                days_overdue=days_overdue,
                member_type=record['member_type'],
                book_tier=record['tier'],
                return_condition=return_condition,
                replacement_cost=record['replacement_cost']
            )

            actual_return_date_str = effective_return_date.strftime('%Y-%m-%d')
            final_status = 'Lost' if return_condition == 'Lost' else 'Returned'

            # Update borrow record
            cursor.execute("""
                UPDATE borrow_records
                SET return_date = ?, status = ?, return_condition = ?, notes = ?
                WHERE id = ?
            """, (actual_return_date_str, final_status, return_condition, notes or 'Returned normally', borrow_record_id))

            # Restock book if NOT lost
            if return_condition != 'Lost':
                cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = ?", (record['b_id'],))

            # Record fine if total > 0
            fine_id = None
            if fine_result.total_fine > 0:
                cursor.execute("""
                    INSERT INTO fines (borrow_record_id, member_id, days_overdue, base_rate, tier_multiplier,
                                       overdue_fine, damage_fine, replacement_fee, total_fine, rule_applied, paid_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Unpaid')
                """, (
                    borrow_record_id,
                    record['m_id'],
                    fine_result.days_overdue,
                    fine_result.base_rate,
                    fine_result.tier_multiplier,
                    fine_result.capped_overdue_fine,
                    fine_result.damage_fee,
                    fine_result.replacement_fee,
                    fine_result.total_fine,
                    f"{fine_result.rule_id}: {fine_result.rule_name}"
                ))
                fine_id = cursor.lastrowid

            # Apply account action if suspension triggered by Decision Table
            if fine_result.account_action == 'Suspended':
                cursor.execute("UPDATE members SET status = 'Suspended' WHERE id = ?", (record['m_id'],))

            conn.commit()

            response_data = {
                'borrow_record_id': borrow_record_id,
                'book_title': record['title'],
                'member_name': record['member_name'],
                'return_date': actual_return_date_str,
                'days_overdue': days_overdue,
                'return_condition': return_condition,
                'fine_id': fine_id,
                'fine_details': fine_result.to_dict()
            }
            return True, f"Return processed successfully. Rule: {fine_result.rule_id} applied.", response_data

        except Exception as e:
            conn.rollback()
            return False, f"Return operation failed: {str(e)}", None
        finally:
            conn.close()

    @staticmethod
    def renew_book(borrow_record_id: int, additional_days: int = 14, db_path: str = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT br.*, b.id as b_id, b.title, m.name as member_name
                FROM borrow_records br
                JOIN books b ON br.book_id = b.id
                JOIN members m ON br.member_id = m.id
                WHERE br.id = ?
            """, (borrow_record_id,))
            record = cursor.fetchone()
            if not record:
                return False, "Record not found.", None
            record = dict(record)

            if record['status'] != 'Active' and record['status'] != 'Overdue':
                return False, f"Cannot renew record in status: {record['status']}.", None

            if record['renewals_count'] >= 2:
                return False, "Maximum renewal limit (2 renewals) reached for this loan.", None

            # Check if pending reservation exists for this book
            cursor.execute("SELECT COUNT(*) as count FROM reservations WHERE book_id = ? AND status = 'Pending'", (record['b_id'],))
            if cursor.fetchone()['count'] > 0:
                return False, "Cannot renew: this book has an active reservation queued by another patron.", None

            # Extend due date
            current_due = datetime.strptime(record['due_date'], '%Y-%m-%d')
            new_due = (current_due + timedelta(days=additional_days)).strftime('%Y-%m-%d')

            cursor.execute("""
                UPDATE borrow_records
                SET due_date = ?, renewals_count = renewals_count + 1, status = 'Active'
                WHERE id = ?
            """, (new_due, borrow_record_id))

            conn.commit()
            return True, f"Book renewed successfully! New due date is {new_due}.", {'new_due_date': new_due, 'renewals_count': record['renewals_count'] + 1}
        finally:
            conn.close()

    @staticmethod
    def reserve_book(book_id: int, member_id: int, db_path: str = None) -> Tuple[bool, str]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            book = cursor.fetchone()
            if not book:
                return False, "Book not found."

            # Check if patron already has active reservation
            cursor.execute("SELECT COUNT(*) as count FROM reservations WHERE book_id = ? AND member_id = ? AND status = 'Pending'", (book_id, member_id))
            if cursor.fetchone()['count'] > 0:
                return False, "You already have a pending reservation for this title."

            cursor.execute("INSERT INTO reservations (book_id, member_id, status) VALUES (?, ?, 'Pending')", (book_id, member_id))
            conn.commit()
            return True, "Reservation queued successfully. You will be notified when a copy is returned."
        finally:
            conn.close()

    @staticmethod
    def get_all_loans(status_filter: str = None, member_id: int = None, db_path: str = None) -> List[Dict[str, Any]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        query = """
            SELECT br.*, b.title, b.isbn, b.author, b.tier, b.replacement_cost,
                   m.name as member_name, m.member_code, m.member_type
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            JOIN members m ON br.member_id = m.id
            WHERE 1=1
        """
        params = []

        if status_filter and status_filter != 'All':
            query += " AND br.status = ?"
            params.append(status_filter)

        if member_id:
            query += " AND br.member_id = ?"
            params.append(member_id)

        query += " ORDER BY br.id DESC"
        cursor.execute(query, params)
        loans = [dict(row) for row in cursor.fetchall()]

        # Calculate live days overdue and estimated fine for active/overdue loans
        today_str = datetime.now().strftime('%Y-%m-%d')
        today_date = datetime.strptime(today_str, '%Y-%m-%d')

        for loan in loans:
            if loan['status'] in ('Active', 'Overdue'):
                due_date = datetime.strptime(loan['due_date'], '%Y-%m-%d')
                delta = (today_date - due_date).days
                loan['current_days_overdue'] = max(0, delta)
                loan['is_overdue'] = delta > 0

                # Fine preview
                fine_preview = FineDecisionTable.calculate(
                    days_overdue=loan['current_days_overdue'],
                    member_type=loan['member_type'],
                    book_tier=loan['tier'],
                    return_condition='Normal'
                )
                loan['estimated_fine'] = fine_preview.total_fine
                loan['matched_rule'] = fine_preview.rule_id
            else:
                loan['current_days_overdue'] = 0
                loan['is_overdue'] = False
                loan['estimated_fine'] = 0.0
                loan['matched_rule'] = 'N/A'

        conn.close()
        return loans

    @staticmethod
    def get_all_fines(paid_status: str = None, db_path: str = None) -> List[Dict[str, Any]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        query = """
            SELECT f.*, m.name as member_name, m.member_code, m.member_type,
                   b.title as book_title, b.isbn
            FROM fines f
            JOIN members m ON f.member_id = m.id
            JOIN borrow_records br ON f.borrow_record_id = br.id
            JOIN books b ON br.book_id = b.id
            WHERE 1=1
        """
        params = []
        if paid_status and paid_status != 'All':
            query += " AND f.paid_status = ?"
            params.append(paid_status)

        query += " ORDER BY f.id DESC"
        cursor.execute(query, params)
        fines = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return fines

    @staticmethod
    def settle_fine(fine_id: int, payment_method: str = 'Cash', db_path: str = None) -> Tuple[bool, str]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM fines WHERE id = ?", (fine_id,))
        fine = cursor.fetchone()
        if not fine:
            conn.close()
            return False, "Fine record not found."

        if fine['paid_status'] == 'Paid':
            conn.close()
            return False, "Fine is already settled."

        paid_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            UPDATE fines
            SET paid_status = 'Paid', paid_date = ?, payment_method = ?
            WHERE id = ?
        """, (paid_date, payment_method, fine_id))

        # Check if member had suspended status and no more unpaid fines
        member_id = fine['member_id']
        cursor.execute("SELECT COUNT(*) as unpaid_count FROM fines WHERE member_id = ? AND paid_status = 'Unpaid'", (member_id,))
        if cursor.fetchone()['unpaid_count'] == 0:
            cursor.execute("UPDATE members SET status = 'Active' WHERE id = ? AND status = 'Suspended'", (member_id,))

        conn.commit()
        conn.close()
        return True, "Fine payment successfully recorded."

    @staticmethod
    def get_dashboard_stats(db_path: str = None) -> Dict[str, Any]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as total_books, SUM(total_copies) as total_volume, SUM(available_copies) as total_available FROM books")
        b_stats = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) as total_members FROM members WHERE status = 'Active'")
        m_stats = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) as active_loans FROM borrow_records WHERE status IN ('Active', 'Overdue')")
        l_stats = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) as overdue_loans FROM borrow_records WHERE status = 'Overdue' OR (status = 'Active' AND due_date < date('now'))")
        o_stats = cursor.fetchone()

        cursor.execute("SELECT COALESCE(SUM(total_fine), 0.0) as fines_collected FROM fines WHERE paid_status = 'Paid'")
        collected = cursor.fetchone()['fines_collected']

        cursor.execute("SELECT COALESCE(SUM(total_fine), 0.0) as fines_pending FROM fines WHERE paid_status = 'Unpaid'")
        pending = cursor.fetchone()['fines_pending']

        # Category breakdown
        cursor.execute("SELECT category, COUNT(*) as count FROM books GROUP BY category ORDER BY count DESC LIMIT 5")
        categories = [dict(row) for row in cursor.fetchall()]

        # Top borrowed books
        cursor.execute("""
            SELECT b.title, COUNT(br.id) as borrow_count
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            GROUP BY b.id
            ORDER BY borrow_count DESC
            LIMIT 5
        """)
        top_books = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return {
            'total_unique_titles': b_stats['total_books'] or 0,
            'total_physical_copies': b_stats['total_volume'] or 0,
            'available_copies': b_stats['total_available'] or 0,
            'active_members': m_stats['total_members'] or 0,
            'active_loans': l_stats['active_loans'] or 0,
            'overdue_loans': o_stats['overdue_loans'] or 0,
            'fines_collected': round(collected, 2),
            'fines_pending': round(pending, 2),
            'categories': categories,
            'top_books': top_books
        }
