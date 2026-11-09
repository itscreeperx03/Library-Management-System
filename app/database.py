import sqlite3
import os
from datetime import datetime, timedelta

from flask import current_app, has_app_context

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'library.db')

def get_db_connection(db_path=None):
    """Establish and return a database connection with foreign key enforcement and row factory."""
    if db_path:
        path = db_path
    elif has_app_context() and current_app.config.get('DATABASE'):
        path = current_app.config['DATABASE']
    else:
        path = DB_PATH

    conn = sqlite3.connect(path, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=None):
    """Initialize all schema tables and apply default seed data if database is fresh."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        member_type TEXT NOT NULL CHECK(member_type IN ('Student', 'Faculty', 'Guest')),
        status TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active', 'Suspended', 'Expired')),
        max_books INTEGER NOT NULL DEFAULT 3,
        loan_period_days INTEGER NOT NULL DEFAULT 14,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isbn TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL,
        tier TEXT NOT NULL DEFAULT 'Standard' CHECK(tier IN ('Standard', 'Course Reserve', 'Rare/Reference')),
        publisher TEXT,
        publication_year INTEGER,
        total_copies INTEGER NOT NULL DEFAULT 1,
        available_copies INTEGER NOT NULL DEFAULT 1,
        shelf_location TEXT,
        replacement_cost REAL NOT NULL DEFAULT 50.0,
        cover_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS borrow_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE RESTRICT,
        member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE RESTRICT,
        issue_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        renewals_count INTEGER DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'Active' CHECK(status IN ('Active', 'Returned', 'Overdue', 'Lost')),
        return_condition TEXT DEFAULT 'Normal' CHECK(return_condition IN ('Normal', 'Minor Damage', 'Severe Damage', 'Lost')),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS fines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        borrow_record_id INTEGER NOT NULL REFERENCES borrow_records(id) ON DELETE CASCADE,
        member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
        days_overdue INTEGER NOT NULL DEFAULT 0,
        base_rate REAL NOT NULL DEFAULT 0.0,
        tier_multiplier REAL NOT NULL DEFAULT 1.0,
        overdue_fine REAL NOT NULL DEFAULT 0.0,
        damage_fine REAL NOT NULL DEFAULT 0.0,
        replacement_fee REAL NOT NULL DEFAULT 0.0,
        total_fine REAL NOT NULL DEFAULT 0.0,
        rule_applied TEXT NOT NULL,
        paid_status TEXT NOT NULL DEFAULT 'Unpaid' CHECK(paid_status IN ('Unpaid', 'Paid', 'Waived')),
        paid_date TEXT,
        payment_method TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
        member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
        status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Fulfilled', 'Cancelled')),
        reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notified_at TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS system_settings (
        setting_key TEXT PRIMARY KEY,
        setting_value TEXT NOT NULL,
        description TEXT
    );
    """)

    conn.commit()

    # Check if seed data is needed
    cursor.execute("SELECT COUNT(*) as count FROM members")
    if cursor.fetchone()['count'] == 0:
        seed_initial_data(conn)

    conn.close()

def seed_initial_data(conn):
    """Seed sample realistic books, members, active loans, and fine scenarios for presentation."""
    cursor = conn.cursor()

    # 1. System Settings
    settings = [
        ('grace_period_days', '2', 'Number of overdue days without fine penalty'),
        ('student_daily_rate', '0.50', 'Base fine per day for Student members ($)'),
        ('faculty_daily_rate', '0.20', 'Base fine per day for Faculty members ($)'),
        ('guest_daily_rate', '1.00', 'Base fine per day for Guest members ($)'),
        ('course_reserve_multiplier', '2.0', 'Fine multiplier for Course Reserve items'),
        ('rare_reference_multiplier', '3.0', 'Fine multiplier for Rare or Reference items'),
        ('student_max_fine_cap', '20.0', 'Maximum overdue fine capped for Students ($)'),
        ('faculty_max_fine_cap', '30.0', 'Maximum overdue fine capped for Faculty ($)'),
        ('guest_max_fine_cap', '50.0', 'Maximum overdue fine capped for Guests ($)'),
        ('minor_damage_charge', '5.0', 'Damage fee for minor physical damage ($)'),
        ('severe_damage_charge', '15.0', 'Damage fee for severe physical damage ($)'),
        ('lost_processing_fee', '10.0', 'Administrative processing fee for lost books ($)'),
        ('max_renewals_allowed', '2', 'Maximum number of times a book can be renewed')
    ]
    cursor.executemany("INSERT OR REPLACE INTO system_settings (setting_key, setting_value, description) VALUES (?, ?, ?)", settings)

    # 2. Members
    members = [
        ('MEM-STU-101', 'Aarav Sharma', 'aarav.sharma@campus.edu', '+91 98765 43210', 'Student', 'Active', 4, 14),
        ('MEM-STU-102', 'Priya Patel', 'priya.patel@campus.edu', '+91 98765 43211', 'Student', 'Active', 4, 14),
        ('MEM-FAC-201', 'Dr. Ramesh Sundaram', 'r.sundaram@campus.edu', '+91 98765 43212', 'Faculty', 'Active', 8, 30),
        ('MEM-FAC-202', 'Prof. Anita Deshmukh', 'a.deshmukh@campus.edu', '+91 98765 43213', 'Faculty', 'Active', 8, 30),
        ('MEM-GST-301', 'Vikram Malhotra', 'vikram.m@external.org', '+91 98765 43214', 'Guest', 'Active', 2, 7),
        ('MEM-STU-103', 'Sneha Roy', 'sneha.roy@campus.edu', '+91 98765 43215', 'Student', 'Suspended', 4, 14),
    ]
    cursor.executemany("""
        INSERT INTO members (member_code, name, email, phone, member_type, status, max_books, loan_period_days)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, members)

    # 3. Books
    books = [
        ('978-0134685991', 'Effective Java (3rd Edition)', 'Joshua Bloch', 'Computer Science', 'Standard', 'Addison-Wesley', 2018, 5, 3, 'CS-Shelf-A1', 45.0, 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300'),
        ('978-0132350884', 'Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', 'Computer Science', 'Standard', 'Prentice Hall', 2008, 4, 2, 'CS-Shelf-A2', 40.0, 'https://images.unsplash.com/photo-1532012164546-f432f2e3777f?w=300'),
        ('978-0262033848', 'Introduction to Algorithms (CLRS)', 'Thomas H. Cormen et al.', 'Algorithms', 'Course Reserve', 'MIT Press', 2009, 3, 1, 'CS-Reserve-B1', 95.0, 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300'),
        ('978-0321125217', 'Domain-Driven Design: Tackling Complexity', 'Eric Evans', 'Software Engineering', 'Standard', 'Addison-Wesley', 2003, 3, 3, 'CS-Shelf-B2', 55.0, 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=300'),
        ('978-0201616224', 'The Pragmatic Programmer: 20th Anniversary Edition', 'David Thomas, Andrew Hunt', 'Software Engineering', 'Standard', 'Addison-Wesley', 2019, 4, 2, 'CS-Shelf-C1', 50.0, 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=300'),
        ('978-0070131439', 'Principles of Mathematical Analysis', 'Walter Rudin', 'Mathematics', 'Rare/Reference', 'McGraw-Hill', 1976, 2, 1, 'MATH-Ref-R1', 120.0, 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=300'),
        ('978-0131103627', 'The C Programming Language (ANSI C)', 'Brian W. Kernighan, Dennis Ritchie', 'Computer Science', 'Rare/Reference', 'Prentice Hall', 1988, 2, 2, 'CS-Ref-R2', 65.0, 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=300'),
        ('978-0321751041', 'The Art of Computer Programming, Vol 1', 'Donald E. Knuth', 'Computer Science', 'Rare/Reference', 'Addison-Wesley', 2011, 1, 0, 'CS-Rare-Vault', 180.0, 'https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=300'),
        ('978-1449331818', 'Learning Python (5th Edition)', 'Mark Lutz', 'Computer Science', 'Standard', "O'Reilly Media", 2013, 6, 5, 'CS-Shelf-D3', 60.0, 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=300'),
        ('978-0134494166', 'Clean Architecture', 'Robert C. Martin', 'Software Engineering', 'Course Reserve', 'Prentice Hall', 2017, 3, 2, 'CS-Reserve-B2', 45.0, 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=300')
    ]
    cursor.executemany("""
        INSERT INTO books (isbn, title, author, category, tier, publisher, publication_year, total_copies, available_copies, shelf_location, replacement_cost, cover_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, books)

    # 4. Realistic Borrow Records & Fines (Demonstrating grace, overdue, damage, and lost rules)
    today = datetime.now()
    records = [
        # Record 1: Normal active loan (Due in 7 days)
        (1, 1, (today - timedelta(days=7)).strftime('%Y-%m-%d'), (today + timedelta(days=7)).strftime('%Y-%m-%d'), None, 0, 'Active', 'Normal', 'Current active loan'),
        # Record 2: Grace period overdue (Due 2 days ago -> Overdue status, within 2 days grace)
        (2, 2, (today - timedelta(days=16)).strftime('%Y-%m-%d'), (today - timedelta(days=2)).strftime('%Y-%m-%d'), None, 0, 'Overdue', 'Normal', 'Within 2-day grace period'),
        # Record 3: Returned on time
        (3, 3, (today - timedelta(days=20)).strftime('%Y-%m-%d'), (today - timedelta(days=5)).strftime('%Y-%m-%d'), (today - timedelta(days=6)).strftime('%Y-%m-%d'), 0, 'Returned', 'Normal', 'Returned cleanly on time'),
        # Record 4: Severely overdue loan (Student overdue by 12 days, Standard book)
        (4, 1, (today - timedelta(days=26)).strftime('%Y-%m-%d'), (today - timedelta(days=12)).strftime('%Y-%m-%d'), None, 0, 'Overdue', 'Normal', 'Overdue 12 days - Student rate applies'),
        # Record 5: Faculty overdue on Course Reserve book (Overdue by 5 days)
        (3, 4, (today - timedelta(days=35)).strftime('%Y-%m-%d'), (today - timedelta(days=5)).strftime('%Y-%m-%d'), None, 1, 'Overdue', 'Normal', 'Course Reserve 2x multiplier'),
        # Record 6: Checked out Knuth (all copies checked out, so available=0)
        (8, 5, (today - timedelta(days=10)).strftime('%Y-%m-%d'), (today - timedelta(days=3)).strftime('%Y-%m-%d'), None, 0, 'Overdue', 'Normal', 'Rare reference vault copy')
    ]

    cursor.executemany("""
        INSERT INTO borrow_records (book_id, member_id, issue_date, due_date, return_date, renewals_count, status, return_condition, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    # 5. Seed historical fine for demonstration
    # Record 7: Past returned with overdue and minor damage
    cursor.execute("""
        INSERT INTO borrow_records (book_id, member_id, issue_date, due_date, return_date, renewals_count, status, return_condition, notes)
        VALUES (5, 6, ?, ?, ?, 0, 'Returned', 'Minor Damage', 'Returned with spine wear and 8 days overdue')
    """, (
        (today - timedelta(days=30)).strftime('%Y-%m-%d'),
        (today - timedelta(days=16)).strftime('%Y-%m-%d'),
        (today - timedelta(days=8)).strftime('%Y-%m-%d')
    ))
    past_record_id = cursor.lastrowid

    # Add fine record: 8 days overdue (Tier 2 student = $0.50 * 8 = $4.00) + Minor Damage ($5.00) = $9.00
    cursor.execute("""
        INSERT INTO fines (borrow_record_id, member_id, days_overdue, base_rate, tier_multiplier, overdue_fine, damage_fine, replacement_fee, total_fine, rule_applied, paid_status, created_at)
        VALUES (?, 6, 8, 0.50, 1.0, 4.00, 5.00, 0.0, 9.00, 'Rule R4: Student Overdue (Tier 2) + Minor Damage', 'Unpaid', ?)
    """, (past_record_id, (today - timedelta(days=8)).strftime('%Y-%m-%d %H:%M:%S')))

    # 6. Reservation for the out-of-stock Knuth book (Book ID 8)
    cursor.execute("""
        INSERT INTO reservations (book_id, member_id, status)
        VALUES (8, 2, 'Pending')
    """)

    conn.commit()
