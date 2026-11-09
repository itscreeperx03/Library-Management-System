# System Architecture & Data Flow Diagrams (DFD)
## Library Management System (LMS)
**Document Type:** Technical Architecture, Data Flow & UML Design Specification  
**Project Special Syllabus Focus:** DFD Level 0, Level 1, Level 2, UML Class & Sequence Diagrams, ERD  
**Standard:** IEEE Std 1016-2009 Software Design Descriptions  
**Version:** 1.0.0  
**Date:** November 2026  

---

## Table of Contents
1. [Architectural Overview & Structural Decomposition](#1-architectural-overview--structural-decomposition)
   - 1.1 Three-Tier Layered Architecture
   - 1.2 Module Decomposition
2. [Data Flow Diagrams (DFD)](#2-data-flow-diagrams-dfd)
   - 2.1 Context Level 0 DFD (System Boundary)
   - 2.2 Level 1 DFD (Subsystem Decomposition)
   - 2.3 Level 2 DFD (Process 3.0: Issue, Return & Fine Engine)
3. [Unified Modeling Language (UML) Class Diagram](#3-unified-modeling-language-uml-class-diagram)
   - 3.1 Class Model & Design Patterns
   - 3.2 Mermaid Class Diagram
4. [UML Dynamic Sequence Diagrams](#4-uml-dynamic-sequence-diagrams)
   - 4.1 Sequence Diagram: Book Checkout (Issue Transaction)
   - 4.2 Sequence Diagram: Book Return with Overdue Fine & Damage Assessment
5. [Entity-Relationship Diagram (ERD)](#5-entity-relationship-diagram-erd)
   - 5.1 Relational Data Schema & Integrity Constraints
   - 5.2 Mermaid Entity-Relationship Diagram

---

## 1. Architectural Overview & Structural Decomposition

### 1.1 Three-Tier Layered Architecture
The Library Management System is architected according to a decoupled **Three-Tier Architectural Pattern**, ensuring separation of concerns between presentation, domain business logic, and transactional persistence:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER (UI)                         │
│  • HTML5 Semantic Templates & CSS3 Glassmorphic Styling                │
│  • Client-side validation & Barcode keyboard-wedge handler             │
│  • Chart.js Interactive Analytics & Responsive DataTables              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST / JSON Payloads
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER (SERVER)                     │
│  • Authentication & Role-Based Access Control Middleware               │
│  • Catalog & Inventory Management Service                              │
│  • Circulation Engine (Checkout, Renewal, Reservation Queue)           │
│  • Formal 16-Rule Decision Table Fine & Penalty Assessment Engine      │
│  • Delinquency Auditor & Overdue Dispatcher                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ SQLite3 WAL-Mode DB-API
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       DATA PERSISTENCE LAYER                           │
│  • Relational Tables: members, books, borrow_records, fines,           │
│                       reservations, system_settings, users             │
│  • Foreign Key referential integrity (`ON DELETE RESTRICT/CASCADE`)   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Flow Diagrams (DFD)

Data Flow Diagrams model the movement, transformation, and storage of information through the system without imposing sequential programming order (using standard DeMarco & Yourdon notation).

### 2.1 Context Level 0 DFD (System Boundary)
The Context Diagram establishes the total system boundary, illustrating the external entities (actors and external systems) that interface directly with the centralized Library Management System.

```mermaid
flowchart TD
    Student["Student Member"]
    Faculty["Faculty Member"]
    Guest["Guest Member"]
    Librarian["Librarian / Circulation Desk"]
    Admin["System Administrator"]
    PaymentGateway["Payment Gateway (External)"]
    NotificationService["Notification Service (External)"]
    
    LMS(("0.0<br/>Library Management<br/>System"))

    %% Student Flows
    Student -->|"Search query / Reserve hold"| LMS
    LMS -->|"Catalog results / Hold confirmation"| Student
    Student -->|"Borrow / Return request"| LMS
    LMS -->|"Due date reminder / Fine notice"| Student

    %% Faculty Flows
    Faculty -->|"Course reserve request / Loan"| LMS
    LMS -->|"Extended research loan status"| Faculty

    %% Guest Flows
    Guest -->|"Deposit / Standard loan query"| LMS
    LMS -->|"Guest borrowing receipt"| Guest

    %% Librarian Flows
    Librarian -->|"Issue / Return / Condition grade"| LMS
    Librarian -->|"Record cash fee / Administrative waiver"| LMS
    LMS -->|"Circulation slips / Delinquency alerts"| Librarian

    %% Admin Flows
    Admin -->|"System policy changes / Seed reset"| LMS
    LMS -->|"Audit reports / Velocity analytics"| Admin

    %% External Systems
    LMS -->|"Fine settlement request"| PaymentGateway
    PaymentGateway -->|"Payment auth token / Status"| LMS
    LMS -->|"Overdue warning / Reservation ready payload"| NotificationService
```

---

### 2.2 Level 1 DFD (Subsystem Decomposition)
The Level 1 DFD decomposes the system into five primary functional processes, interconnected via seven canonical data stores:
- **`D1: Users`** (Staff accounts and roles)
- **`D2: Books`** (Bibliographic catalog and physical copy counts)
- **`D3: Members`** (Patron profiles, categories, and account status)
- **`D4: BorrowRecords`** (Circulation ledger: active loans, history, returns)
- **`D5: Fines`** (Invoiced fines, fee breakdowns, payment records)
- **`D6: Reservations`** (Hold queues for checked-out items)
- **`D7: SystemSettings`** (Dynamic institutional fine rates, caps, loan days)

```mermaid
flowchart TD
    subgraph ExternalEntities ["External Entities"]
        UserEntity["Patron / Staff User"]
        LibrarianEntity["Desk Librarian"]
        AdminEntity["Administrator"]
        GatewayEntity["Payment Gateway"]
    end

    subgraph Processes ["Subsystem Functional Processes"]
        P1(("1.0<br/>User Authentication<br/>& Access Control"))
        P2(("2.0<br/>Catalog & Inventory<br/>Management"))
        P3(("3.0<br/>Circulation Engine<br/>(Issue / Return)"))
        P4(("4.0<br/>Decision-Table Fine<br/>& Penalty Engine"))
        P5(("5.0<br/>Reporting, Auditing<br/>& Analytics"))
    end

    subgraph DataStores ["Data Stores"]
        D1[("D1: Users")]
        D2[("D2: Books")]
        D3[("D3: Members")]
        D4[("D4: BorrowRecords")]
        D5[("D5: Fines")]
        D6[("D6: Reservations")]
        D7[("D7: SystemSettings")]
    end

    %% Process 1.0 Flows
    UserEntity -->|"Login credentials"| P1
    P1 <-->|"Verify hash & role"| D1
    P1 -->|"Session token / Role claims"| UserEntity

    %% Process 2.0 Flows
    UserEntity -->|"Search query"| P2
    AdminEntity -->|"Add / Edit book metadata"| P2
    P2 <-->|"Query / Update catalog"| D2
    P2 -->|"Catalog search results"| UserEntity

    %% Process 3.0 Flows
    LibrarianEntity -->|"Issue loan / Return book"| P3
    P3 <-->|"Verify member status & quota"| D3
    P3 <-->|"Check stock & update copies"| D2
    P3 -->|"Create / Close loan entry"| D4
    P3 <-->|"Queue / Fulfill hold"| D6
    P3 -->|"Circulation receipt"| LibrarianEntity
    P3 -->|"Return condition & overdue days"| P4

    %% Process 4.0 Flows
    P4 <-->|"Read policy rates & caps"| D7
    P4 <-->|"Check prior default history"| D4
    P4 -->|"Persist fine assessment"| D5
    P4 -->|"Update member suspension"| D3
    GatewayEntity <-->|"Online payment reconciliation"| P4
    P4 -->|"Payment receipt & cleared status"| LibrarianEntity

    %% Process 5.0 Flows
    AdminEntity -->|"Report request parameters"| P5
    P5 <--|"Read circulation data"| D4
    P5 <--|"Read fee balances"| D5
    P5 <--|"Read catalog turnover"| D2
    P5 -->|"Delinquency report & graphs"| AdminEntity
```

---

### 2.3 Level 2 DFD (Process 3.0: Issue, Return & Fine Engine)
The Level 2 DFD provides an explosive decomposition of the mission-critical circulation and fine assessment pipeline (combining Processes 3.0 and 4.0):

```mermaid
flowchart TD
    Librarian["Desk Librarian"]
    
    subgraph P3_Decomposition ["Process 3.0 & 4.0: Detailed Circulation Pipeline"]
        P31(("3.1<br/>Verify Borrower<br/>Eligibility & Quota"))
        P32(("3.2<br/>Validate Book Stock<br/>& Hold Queue"))
        P33(("3.3<br/>Record Active Loan<br/>(Issue Transaction)"))
        P34(("3.4<br/>Inspect Return<br/>& Compute Overdue Days"))
        P41(("4.1<br/>Evaluate Decision<br/>Table Base Rates"))
        P42(("4.2<br/>Assess Damage &<br/>Lost Replacement"))
        P43(("4.3<br/>Enforce Statutory<br/>Fine Caps"))
        P35(("3.5<br/>Update Stock &<br/>Fulfill Reservations"))
        P44(("4.4<br/>Process Payment<br/>or Waiver"))
    end

    D2[("D2: Books")]
    D3[("D3: Members")]
    D4[("D4: BorrowRecords")]
    D5[("D5: Fines")]
    D6[("D6: Reservations")]
    D7[("D7: SystemSettings")]

    %% Issue Pipeline
    Librarian -->|"Issue command (MemberCode, ISBN)"| P31
    P31 <-->|"Check status, unpaid fines, active count"| D3
    P31 -->|"Eligible borrower token"| P32
    P32 <-->|"Check available copies & hold queue"| D2
    P32 <-->|"Verify next patron in queue"| D6
    P32 -->|"Stock verified"| P33
    P33 -->|"Decrement available copies"| D2
    P33 -->|"Insert active loan record"| D4
    P33 -->|"Printed checkout slip"| Librarian

    %% Return Pipeline
    Librarian -->|"Check-in (RecordID, Condition)"| P34
    P34 <-->|"Fetch loan issue & due dates"| D4
    P34 -->|"Overdue days (D) & Condition"| P41
    P41 <-->|"Fetch member rates & multipliers"| D7
    P41 <-->|"Check prior default occurrences"| D4
    P41 -->|"Raw overdue subtotal"| P42
    P42 -->|"Add damage fee or lost cost"| P43
    P43 <-->|"Apply category cap ($20/$30/$50)"| D7
    P43 -->|"Persist assessed fine record"| D5
    P43 -->|"Update status (Warning/Suspended)"| D3
    P43 -->|"Return summary to desk"| P35
    P35 -->|"Increment available copies"| D2
    P35 <-->|"Check pending holds & notify"| D6
    P35 -->|"Close loan (status='Returned')"| D4

    %% Payment Pipeline
    Librarian -->|"Settle fine (Cash/Card/Waiver)"| P44
    P44 <-->|"Update paid_status='Paid'"| D5
    P44 -->|"Reactivate member if clean"| D3
    P44 -->|"Fee receipt"| Librarian
```

---

## 3. Unified Modeling Language (UML) Class Diagram

### 3.1 Class Model & Design Patterns
The domain model applies standard Object-Oriented principles (Encapsulation, Polymorphism, Single Responsibility):
- **Inheritance / Specialization:** `Member` serves as the abstract base for `StudentMember`, `FacultyMember`, and `GuestMember`, encapsulating policy parameters (`max_books`, `loan_period_days`, `fine_cap`, `base_rate`).
- **Composition & Association:** A `BorrowRecord` associates exactly one `Member` with one `Book`. An overdue or damaged return generates a compositionally bound `Fine` entity.
- **Service Layer Pattern:** Controller methods delegate business rules to stateless singleton services (`CirculationService`, `FineEngine`).

### 3.2 Mermaid Class Diagram

```mermaid
classDiagram
    direction TB

    class User {
        +int user_id
        +string username
        +string password_hash
        +string role
        +bool is_active
        +datetime last_login
        +verifyPassword(string raw_password) bool
        +hasPermission(string route) bool
    }

    class Member {
        <<abstract>>
        +int id
        +string member_code
        +string name
        +string email
        +string phone
        +string member_type
        +string status
        +int max_books
        +int loan_period_days
        +datetime created_at
        +isEligibleToBorrow() bool
        +getActiveLoanCount() int
        +getOutstandingFineTotal() float
        +suspendAccount(string reason) void
        +reactivateAccount() void
    }

    class StudentMember {
        +float base_daily_rate = 0.50
        +float fine_cap = 20.00
        +int max_books = 4
        +int loan_period_days = 14
    }

    class FacultyMember {
        +float base_daily_rate = 0.20
        +float fine_cap = 30.00
        +int max_books = 8
        +int loan_period_days = 30
    }

    class GuestMember {
        +float base_daily_rate = 1.00
        +float fine_cap = 50.00
        +int max_books = 2
        +int loan_period_days = 7
    }

    class Book {
        +int id
        +string isbn
        +string title
        +string author
        +string category
        +string tier
        +string publisher
        +int publication_year
        +int total_copies
        +int available_copies
        +string shelf_location
        +float replacement_cost
        +string cover_url
        +isAvailable() bool
        +decrementCopy() bool
        +incrementCopy() void
        +markLost() void
    }

    class BorrowRecord {
        +int id
        +int book_id
        +int member_id
        +date issue_date
        +date due_date
        +date return_date
        +int renewals_count
        +string status
        +string return_condition
        +string notes
        +calculateDaysOverdue(date return_date) int
        +isRenewable() bool
        +renewLoan(int days) void
        +closeLoan(string condition) void
    }

    class Fine {
        +int id
        +int borrow_record_id
        +int member_id
        +int days_overdue
        +float base_rate
        +float tier_multiplier
        +float overdue_fine
        +float damage_fine
        +float replacement_fee
        +float total_fine
        +string rule_applied
        +string paid_status
        +datetime paid_date
        +string payment_method
        +markAsPaid(string method) void
        +waiveFine(string reason) void
    }

    class Reservation {
        +int id
        +int book_id
        +int member_id
        +string status
        +datetime reserved_at
        +datetime notified_at
        +fulfillHold() void
        +cancelHold() void
    }

    class SystemSetting {
        +string setting_key
        +string setting_value
        +string description
        +getValue() string
        +setValue(string val) void
    }

    class FineEngine {
        <<service>>
        +calculateFine(member, days_overdue, book_tier, condition, repeat_defaulter) FineCalculationResult
    }

    %% Relationships
    Member <|-- StudentMember
    Member <|-- FacultyMember
    Member <|-- GuestMember

    Member "1" --> "0..*" BorrowRecord : borrows
    Book "1" --> "0..*" BorrowRecord : lent via
    BorrowRecord "1" --> "0..1" Fine : incurs
    Member "1" --> "0..*" Fine : liable for
    Book "1" --> "0..*" Reservation : queued for
    Member "1" --> "0..*" Reservation : places
    FineEngine ..> Fine : instantiates
    FineEngine ..> SystemSetting : reads
```

---

## 4. UML Dynamic Sequence Diagrams

### 4.1 Sequence Diagram: Book Checkout (Issue Transaction)
This sequence captures the interaction between the Desk Librarian, the web presentation layer, the circulation business service, and database persistence during a routine checkout:

```mermaid
sequenceDiagram
    autonumber
    actor Librarian as Desk Librarian
    participant UI as Circulation Desk (Web UI)
    participant CircService as CirculationService
    participant DB as SQLite Database

    Librarian->>UI: Enter Member Code & Book ISBN
    UI->>CircService: issue_book(member_code, isbn)
    
    CircService->>DB: SELECT * FROM members WHERE member_code = ?
    DB-->>CircService: Member Profile Record
    
    Note over CircService: Verify eligibility: status == 'Active'<br/>unpaid fines == $0<br/>active loans < max_books
    
    CircService->>DB: SELECT * FROM books WHERE isbn = ?
    DB-->>CircService: Book Record
    
    Note over CircService: Check available_copies > 0<br/>Check reservation queue
    
    alt Patron Ineligible or Book Unavailable
        CircService-->>UI: Raise BusinessRuleViolation(Reason)
        UI-->>Librarian: Display Red Error Alert Modal
    else Checks Passed
        Note over CircService: Compute due_date = TODAY + loan_period_days
        CircService->>DB: BEGIN TRANSACTION
        CircService->>DB: INSERT INTO borrow_records (book_id, member_id, issue_date, due_date, status='Active')
        CircService->>DB: UPDATE books SET available_copies = available_copies - 1 WHERE id = ?
        CircService->>DB: COMMIT
        DB-->>CircService: Transaction Committed
        CircService-->>UI: Return CheckoutSuccessDTO (Receipt Data)
        UI-->>Librarian: Display Checkout Receipt & Print Dialog
    end
```

---

### 4.2 Sequence Diagram: Book Return with Overdue Fine & Damage Assessment
This sequence demonstrates the execution of the Decision Table Fine Engine when a book is checked in late with physical damage:

```mermaid
sequenceDiagram
    autonumber
    actor Librarian as Desk Librarian
    participant UI as Check-In Terminal (Web UI)
    participant CircService as CirculationService
    participant FineEngine as DecisionTableFineEngine
    participant DB as SQLite Database
    participant Gateway as Mock Payment Gateway

    Librarian->>UI: Select Active Loan, Choose Condition ('Minor Damage')
    UI->>CircService: return_book(record_id, condition='Minor Damage')
    
    CircService->>DB: SELECT * FROM borrow_records WHERE id = ?
    DB-->>CircService: Borrow Record (Due Date, Member ID, Book ID)
    
    CircService->>DB: SELECT * FROM members WHERE id = record.member_id
    DB-->>CircService: Member Record (Type='Student', Status='Active')
    
    CircService->>DB: SELECT * FROM books WHERE id = record.book_id
    DB-->>CircService: Book Record (Tier='Course Reserve', Cost=$45.00)
    
    Note over CircService: Calculate days_overdue = TODAY - due_date (e.g., 5 days)
    
    CircService->>DB: SELECT COUNT(*) FROM borrow_records WHERE member_id = ? AND status = 'Overdue'
    DB-->>CircService: Prior default count (Repeat Defaulter check)
    
    CircService->>FineEngine: calculate_fine('Student', days=5, tier='Course Reserve', cond='Minor Damage', repeat=False)
    
    Note over FineEngine: 1. Base rate: $0.50/day<br/>2. Tier Multiplier: 2.0x (Reserve)<br/>3. Raw Overdue: 5 * 0.50 * 2 = $5.00<br/>4. Statutory Cap Check: min($5, $20) = $5.00<br/>5. Damage Penalty: $5.00 (Minor Damage)<br/>6. Total Fine: $5.00 + $5.00 = $10.00<br/>7. Rule matched: Rule R4
    
    FineEngine-->>CircService: FineResult (Overdue=$5, Damage=$5, Total=$10, Rule='R4')
    
    CircService->>DB: BEGIN TRANSACTION
    CircService->>DB: UPDATE borrow_records SET return_date=TODAY, status='Returned', return_condition='Minor Damage'
    CircService->>DB: UPDATE books SET available_copies = available_copies + 1 WHERE id = ?
    CircService->>DB: INSERT INTO fines (borrow_record_id, member_id, days_overdue=5, total_fine=10.00, rule_applied='Rule R4')
    CircService->>DB: UPDATE members SET status = 'Warning' WHERE id = ?
    CircService->>DB: COMMIT
    DB-->>CircService: Transaction Committed
    
    CircService-->>UI: Return CheckInSummary (Fine Total: $10.00, Status: 'Warning')
    UI-->>Librarian: Prompt Cashier Settlement Modal
    
    opt Immediate Payment Settlement
        Librarian->>UI: Submit Payment (Method: 'Card', Amount: $10.00)
        UI->>Gateway: process_payment(amount=10.00, token)
        Gateway-->>UI: Payment Authorized (AuthCode='AUTH-9821')
        UI->>CircService: record_fine_payment(fine_id, method='Card')
        CircService->>DB: UPDATE fines SET paid_status='Paid', payment_method='Card'
        CircService->>DB: UPDATE members SET status='Active' WHERE id = ?
        DB-->>CircService: Status Restored
        CircService-->>UI: Settlement Receipt Generated
        UI-->>Librarian: Print Cleared Account Statement
    end
```

---

## 5. Entity-Relationship Diagram (ERD)

### 5.1 Relational Data Schema & Integrity Constraints
The persistence layer contains six core relational tables engineered with strict foreign key constraints:
- **`MEMBERS`**: Stores library patrons with unique email and member codes.
- **`BOOKS`**: Bibliographic entries with ISBN unique keys, available copy inventory, and catalog tiers.
- **`BORROW_RECORDS`**: M:N junction table between `MEMBERS` and `BOOKS` with loan status, issue/due dates, and return condition audit.
- **`FINES`**: 1:1 / 1:M financial ledger recording mathematical fine breakdowns linked to circulation loans.
- **`RESERVATIONS`**: Waitlist queue resolving holds on zero-stock titles.
- **`SYSTEM_SETTINGS`**: Dynamic institutional configuration key-value storage.

### 5.2 Mermaid Entity-Relationship Diagram

```mermaid
erDiagram
    MEMBERS ||--o{ BORROW_RECORDS : "initiates"
    MEMBERS ||--o{ FINES : "incurs"
    MEMBERS ||--o{ RESERVATIONS : "places"
    BOOKS ||--o{ BORROW_RECORDS : "checked_out_in"
    BOOKS ||--o{ RESERVATIONS : "held_by"
    BORROW_RECORDS ||--o| FINES : "generates"

    MEMBERS {
        int id PK "INTEGER AUTOINCREMENT"
        string member_code UK "TEXT UNIQUE NOT NULL"
        string name "TEXT NOT NULL"
        string email UK "TEXT UNIQUE NOT NULL"
        string phone "TEXT"
        string member_type "CHECK(Student, Faculty, Guest)"
        string status "CHECK(Active, Suspended, Expired)"
        int max_books "INTEGER DEFAULT 3"
        int loan_period_days "INTEGER DEFAULT 14"
        timestamp created_at "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    BOOKS {
        int id PK "INTEGER AUTOINCREMENT"
        string isbn UK "TEXT UNIQUE NOT NULL"
        string title "TEXT NOT NULL"
        string author "TEXT NOT NULL"
        string category "TEXT NOT NULL"
        string tier "CHECK(Standard, Course Reserve, Rare/Reference)"
        string publisher "TEXT"
        int publication_year "INTEGER"
        int total_copies "INTEGER DEFAULT 1"
        int available_copies "INTEGER DEFAULT 1"
        string shelf_location "TEXT"
        float replacement_cost "REAL DEFAULT 50.0"
        string cover_url "TEXT"
        timestamp created_at "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    BORROW_RECORDS {
        int id PK "INTEGER AUTOINCREMENT"
        int book_id FK "REFERENCES books(id) ON DELETE RESTRICT"
        int member_id FK "REFERENCES members(id) ON DELETE RESTRICT"
        string issue_date "TEXT NOT NULL"
        string due_date "TEXT NOT NULL"
        string return_date "TEXT"
        int renewals_count "INTEGER DEFAULT 0"
        string status "CHECK(Active, Returned, Overdue, Lost)"
        string return_condition "CHECK(Normal, Minor Damage, Severe Damage, Lost)"
        string notes "TEXT"
        timestamp created_at "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    FINES {
        int id PK "INTEGER AUTOINCREMENT"
        int borrow_record_id FK "REFERENCES borrow_records(id) ON DELETE CASCADE"
        int member_id FK "REFERENCES members(id) ON DELETE CASCADE"
        int days_overdue "INTEGER DEFAULT 0"
        float base_rate "REAL DEFAULT 0.0"
        float tier_multiplier "REAL DEFAULT 1.0"
        float overdue_fine "REAL DEFAULT 0.0"
        float damage_fine "REAL DEFAULT 0.0"
        float replacement_fee "REAL DEFAULT 0.0"
        float total_fine "REAL DEFAULT 0.0"
        string rule_applied "TEXT NOT NULL"
        string paid_status "CHECK(Unpaid, Paid, Waived)"
        string paid_date "TEXT"
        string payment_method "TEXT"
        timestamp created_at "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    RESERVATIONS {
        int id PK "INTEGER AUTOINCREMENT"
        int book_id FK "REFERENCES books(id) ON DELETE CASCADE"
        int member_id FK "REFERENCES members(id) ON DELETE CASCADE"
        string status "CHECK(Pending, Fulfilled, Cancelled)"
        timestamp reserved_at "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        timestamp notified_at "TIMESTAMP"
    }

    SYSTEM_SETTINGS {
        string setting_key PK "TEXT PRIMARY KEY"
        string setting_value "TEXT NOT NULL"
        string description "TEXT"
    }
```
