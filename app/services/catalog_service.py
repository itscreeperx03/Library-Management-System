"""
catalog_service.py
==================
Catalog inventory and book management service.
"""

from typing import List, Dict, Any, Optional, Tuple
from app.database import get_db_connection

class CatalogService:
    @staticmethod
    def get_all_books(search: str = None, category: str = None, tier: str = None,
                      available_only: bool = False, db_path: str = None) -> List[Dict[str, Any]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if search:
            term = f"%{search.strip()}%"
            query += " AND (title LIKE ? OR author LIKE ? OR isbn LIKE ? OR category LIKE ?)"
            params.extend([term, term, term, term])

        if category and category != 'All':
            query += " AND category = ?"
            params.append(category)

        if tier and tier != 'All':
            query += " AND tier = ?"
            params.append(tier)

        if available_only:
            query += " AND available_copies > 0"

        query += " ORDER BY title ASC"
        cursor.execute(query, params)
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return books

    @staticmethod
    def get_book_by_id(book_id: int, db_path: str = None) -> Optional[Dict[str, Any]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_book_by_isbn(isbn: str, db_path: str = None) -> Optional[Dict[str, Any]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn.strip(),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create_book(book_data: Dict[str, Any], db_path: str = None) -> Dict[str, Any]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        total_copies = int(book_data.get('total_copies', 1))
        available_copies = int(book_data.get('available_copies', total_copies))
        replacement_cost = float(book_data.get('replacement_cost', 50.0))

        cursor.execute("""
            INSERT INTO books (isbn, title, author, category, tier, publisher, publication_year,
                               total_copies, available_copies, shelf_location, replacement_cost, cover_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            book_data['isbn'].strip(),
            book_data['title'].strip(),
            book_data['author'].strip(),
            book_data.get('category', 'General').strip(),
            book_data.get('tier', 'Standard').strip(),
            book_data.get('publisher', '').strip(),
            int(book_data.get('publication_year', 2024)),
            total_copies,
            available_copies,
            book_data.get('shelf_location', 'General Shelf').strip(),
            replacement_cost,
            book_data.get('cover_url', '').strip()
        ))
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return CatalogService.get_book_by_id(book_id, db_path)

    @staticmethod
    def update_book(book_id: int, book_data: Dict[str, Any], db_path: str = None) -> Optional[Dict[str, Any]]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE books
            SET isbn = ?, title = ?, author = ?, category = ?, tier = ?,
                publisher = ?, publication_year = ?, total_copies = ?,
                shelf_location = ?, replacement_cost = ?, cover_url = ?
            WHERE id = ?
        """, (
            book_data['isbn'].strip(),
            book_data['title'].strip(),
            book_data['author'].strip(),
            book_data.get('category', 'General').strip(),
            book_data.get('tier', 'Standard').strip(),
            book_data.get('publisher', '').strip(),
            int(book_data.get('publication_year', 2024)),
            int(book_data.get('total_copies', 1)),
            book_data.get('shelf_location', '').strip(),
            float(book_data.get('replacement_cost', 50.0)),
            book_data.get('cover_url', '').strip(),
            book_id
        ))
        conn.commit()
        conn.close()
        return CatalogService.get_book_by_id(book_id, db_path)

    @staticmethod
    def delete_book(book_id: int, db_path: str = None) -> Tuple[bool, str]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        # Check for active loans
        cursor.execute("SELECT COUNT(*) as active_count FROM borrow_records WHERE book_id = ? AND status = 'Active'", (book_id,))
        row = cursor.fetchone()
        if row and row['active_count'] > 0:
            conn.close()
            return False, f"Cannot delete book: {row['active_count']} active loans exist."

        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        return True, "Book successfully removed from catalog."

    @staticmethod
    def get_categories(db_path: str = None) -> List[str]:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM books ORDER BY category ASC")
        categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        return categories
