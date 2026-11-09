# System User Manual & Viva Voce Defence Dossier
## Library Management System (LMS)
**Document Standard:** IEEE Std 1063-2001 Software User Documentation  
**Version:** 1.0.0  
**Date:** November 2026  
**Audience:** Desk Librarians, Academic Patrons, System Administrators, and Viva Voce Examiners  

---

## Table of Contents
1. [System Overview & Deployment Quickstart](#1-system-overview--deployment-quickstart)
   - 1.1 Architecture & Prerequisites
   - 1.2 Starting the Application
   - 1.3 Default Demonstration Accounts & Credentials
2. [Patron User Guide (Student, Faculty & Guest)](#2-patron-user-guide-student-faculty--guest)
   - 2.1 Searching the Online Public Access Catalog (OPAC)
   - 2.2 Placing a Hold / Reservation on Out-of-Stock Books
   - 2.3 Viewing Personal Borrowing Standing & Due Dates
3. [Circulation Desk Librarian Operational Guide](#3-circulation-desk-librarian-operational-guide)
   - 3.1 Patron Registration & Quota Assignment
   - 3.2 Book Catalog Ingestion & Shelf Management
   - 3.3 Book Checkout (Issue Transaction) Workflow
   - 3.4 Book Check-In (Return Transaction) & Condition Grading
   - 3.5 Loan Renewal Processing
   - 3.6 Fee Collection, Receipts & Administrative Waivers
4. [System Administrator Guide](#4-system-administrator-guide)
   - 4.1 Dynamic Policy Settings Configuration
   - 4.2 Overdue Delinquency Audits & Data Exports
   - 4.3 Circulation Analytics Dashboard
   - 4.4 Database Integrity Verification & Reseeding
5. [Operational Troubleshooting & Edge Case Handling](#5-operational-troubleshooting--edge-case-handling)
6. [Comprehensive Academic Viva Voce Defence Guide](#6-comprehensive-academic-viva-voce-defence-guide)
   - 6.1 Process Models & Project Governance
   - 6.2 Decision Table Logic & Fine Engine Verification
   - 6.3 Function Point Analysis (FPA) & COCOMO Sizing
   - 6.4 Data Flow Diagrams (DFDs) & Software Architecture
   - 6.5 Quality Assurance, Concurrency & Database Integrity

---

## 1. System Overview & Deployment Quickstart

### 1.1 Architecture & Prerequisites
The Library Management System is a lightweight, responsive three-tier web application built with Python 3, Flask, and SQLite.

**Prerequisites:**
- Python 3.10 or higher installed.
- Standard web browser (Chrome, Firefox, Safari, or Edge).
- No external database servers or cloud dependencies required; SQLite handles transactional persistence locally in `library.db`.

### 1.2 Starting the Application
From the project root directory (`C:\Users\jatin\OneDrive\Desktop\Projects\Library Management System`):

1. **Initialize / Verify the Database:**
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```
   *This automatically builds the database tables and populates sample books, members, active loans, and fine records if fresh.*

2. **Launch the Web Application Server:**
   ```bash
   python app/main.py
   ```
   *The server initializes at `http://127.0.0.1:5000`.*

3. Open your browser and navigate to `http://127.0.0.1:5000` to access the interactive web interface.

### 1.3 Default Demonstration Accounts & Credentials
The database comes pre-seeded with representative accounts across all user classes:

| Member Code | Member Name | Category | Status | Borrowing Privileges | Seeded Test Scenario |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **`MEM-STU-101`** | Aarav Sharma | Student | Active | Max 4 books, 14 days | Active clean loans |
| **`MEM-STU-102`** | Priya Patel | Student | Active | Max 4 books, 14 days | 1 loan in 2-day Grace Period |
| **`MEM-STU-103`** | Sneha Roy | Student | Suspended | Barred from borrowing | Unpaid past fine ($9.00) |
| **`MEM-FAC-201`** | Dr. Ramesh Sundaram | Faculty | Active | Max 8 books, 30 days | Research monograph checkout |
| **`MEM-FAC-202`** | Prof. Anita Deshmukh | Faculty | Active | Max 8 books, 30 days | Overdue Course Reserve item |
| **`MEM-GST-301`** | Vikram Malhotra | Guest | Active | Max 2 books, 7 days | Standard borrowing tier |

---

## 2. Patron User Guide (Student, Faculty & Guest)

### 2.1 Searching the Online Public Access Catalog (OPAC)
Patrons can search and filter the institutional bibliographic collection without logging in:
1. Navigate to the **Catalog** tab in the main navigation bar.
2. In the search input box, type keywords matching the **Title**, **Author**, or **ISBN** (e.g., `Clean Code` or `Algorithms`).
3. Select an optional category from the dropdown (e.g., `Computer Science`, `Mathematics`, `Software Engineering`).
4. Toggle **Available Only** to view titles currently on physical shelves.
5. Review the resulting book cards:
   - Green badge indicates **Available Copies** ($> 0$).
   - Yellow/Red badge indicates **All Copies Checked Out** ($0$ available).
   - Blue/Purple badge displays the **Tier** (`Standard`, `Course Reserve`, `Rare/Reference`).
   - The card displays the exact **Physical Shelf Location** (e.g., `CS-Shelf-A2`).

### 2.2 Placing a Hold / Reservation on Out-of-Stock Books
When a desired book has 0 available copies on the shelf:
1. Locate the book card in the catalog.
2. Click the **Reserve / Place Hold** button on the card.
3. Enter your **Member Code** (e.g., `MEM-STU-101`) and submit.
4. The system validates that:
   - Your account is `Active` and has no outstanding unpaid fines.
   - You do not already have an active loan for this book.
5. Upon confirmation, the system assigns you a queue position (e.g., *Position #1 in Hold Queue*). When the book is returned to the circulation desk, it is automatically held for you for 48 hours.

### 2.3 Viewing Personal Borrowing Standing & Due Dates
1. Click the **Patron Standing** lookup button on the top navigation bar.
2. Enter your Member Code or Email address.
3. The system renders your personal dashboard:
   - List of all currently checked-out titles with **Issue Date** and **Due Date**.
   - Color-coded countdown badges:
     - **Green:** Due in $> 3$ days.
     - **Amber:** Due within 48 hours or in 2-day Grace Period.
     - **Red:** Overdue — immediate return requested.
   - Accumulated fine balance (if any) with itemized breakdown.

---

## 3. Circulation Desk Librarian Operational Guide

### 3.1 Patron Registration & Quota Assignment
1. Open the **Members** tab in the navigation bar and click **+ Register New Member**.
2. Complete the required fields:
   - **Full Name:** Patron's legal name.
   - **Email:** Institutional campus email (must be unique).
   - **Phone:** Contact phone number.
   - **Member Category:** Select `Student`, `Faculty`, or `Guest`.
3. The system automatically initializes the policy parameters:
   - `Student`: Max 4 books, 14 days loan period.
   - `Faculty`: Max 8 books, 30 days loan period.
   - `Guest`: Max 2 books, 7 days loan period.
4. Click **Create Member Profile**. The system assigns a unique sequential code (`MEM-STU-XXX`).

### 3.2 Book Catalog Ingestion & Shelf Management
1. Open the **Catalog** tab and click **+ Add New Book**.
2. Enter the bibliographic metadata:
   - **ISBN-13 / ISBN-10:** (e.g., `978-0132350884`).
   - **Title & Author:** Full book title and author names.
   - **Category:** Academic discipline.
   - **Book Tier:**
     - `Standard`: General collection ($1.0\times$ fine multiplier).
     - `Course Reserve`: High-demand syllabus textbook ($2.0\times$ fine multiplier, 3-day max loan).
     - `Rare/Reference`: Archive collection ($3.0\times$ fine multiplier).
   - **Total Copies:** Physical copy inventory acquired.
   - **Shelf Location Code:** Physical coordinate (e.g., `CS-Shelf-B2`).
   - **Replacement Cost ($):** Valuation used if patron reports the item lost.
3. Click **Save Book Entry**. The item is immediately searchable.

### 3.3 Book Checkout (Issue Transaction) Workflow
To check out a book to a patron:
1. Navigate to the **Circulation Desk** tab.
2. In the **Issue Book** panel:
   - Scan or type the patron's **Member Code** (e.g., `MEM-STU-101`).
   - Scan or type the book's **ISBN** or select from the live autocomplete list.
3. Click **Issue Loan**.
4. The system executes automated eligibility gates:
   - *Check 1:* Verifies member status is `Active` (rejects if `Suspended`).
   - *Check 2:* Verifies member has zero unpaid outstanding fines.
   - *Check 3:* Verifies active loan count is less than member's `max_books`.
   - *Check 4:* Verifies book has `available_copies > 0`.
   - *Check 5:* Verifies no other patron holds the active reservation queue head.
5. Upon successful checkout:
   - `available_copies` is atomically decremented by 1.
   - Due date is computed (`TODAY + loan_period_days`).
   - A printable checkout slip is generated containing Member Name, Title, and Due Date.

---

### 3.4 Book Check-In (Return Transaction) & Condition Grading
When a borrower returns a physical book to the circulation desk:
1. Navigate to the **Return Terminal** under the **Circulation Desk** tab.
2. Locate the active loan using the search box (search by Member Name, Member Code, or Book Title).
3. Click **Process Return** on the corresponding row.
4. **Inspect the Physical Book Condition** and select from the dropdown:
   - **`Normal`:** Acceptable wear and tear. Surcharge: **$\$0.00$**.
   - **`Minor Damage`:** Marginal pencil notes, creased pages, soiled cover. Surcharge: **$\$5.00$**.
   - **`Severe Damage`:** Broken binding, torn spine, liquid damage, missing pages. Surcharge: **$\$15.00$**.
   - **`Lost`:** Patron cannot return the item. Converts transaction to **Replacement Cost + $\$10.00$ Administrative Fee**.
5. Click **Calculate & Check-In**.
6. The system executes the **16-Rule Decision Table Fine Engine**:
   - Compares Return Date against Due Date to compute `days_overdue`.
   - Evaluates Grace Period ($0 \le D \le 2 \implies \$0.00$).
   - Calculates base daily rate $\times$ book tier multiplier $\times$ repeat defaulter surcharge.
   - Enforces statutory fine cap ($\le \$20$ Student, $\le \$30$ Faculty, $\le \$50$ Guest).
   - Adds physical damage fee or replacement cost.
   - Updates member account status (Active, Warning, or Suspended).
7. If fine $> \$0.00$, the system displays the **Fine Assessment Modal** with the exact rule applied and prompts for payment settlement.

---

### 3.5 Loan Renewal Processing
To extend a loan:
1. Under the **Circulation Desk** tab, locate the active loan.
2. Click **Renew Loan**.
3. The system verifies:
   - The book is not currently overdue ($D = 0$). Overdue loans cannot be renewed.
   - The renewal count is less than the institutional maximum ($2$ renewals).
   - No other patron has placed a pending reservation on the book.
4. If eligible, the due date is extended by the member's standard loan duration.

---

### 3.6 Fee Collection, Receipts & Administrative Waivers
When a fine is assessed or an outstanding balance is settled:
1. In the **Fine Management** dialog:
   - **Cash Settlement:** Select payment method (`Cash`, `Campus Card`, `Online`), enter amount, and click **Record Payment**.
   - **Print Receipt:** Click **Generate Official Receipt** to open the printable cashier slip containing the transaction number, date, breakdown, and cashier signature line.
   - **Administrative Waiver:** If the patron presents documented medical or compassionate hardship, an authorized Librarian can enter a waiver justification note and click **Grant Administrative Waiver**. The invoice is marked `Waived` with an audit record preserved.
2. Once all outstanding liabilities are settled, the patron's borrowing status is automatically restored to `Active`.

---

## 4. System Administrator Guide

### 4.1 Dynamic Policy Settings Configuration
Administrators can tune institutional circulation policies without code changes:
1. Open the **System Administration** tab and select **Policy Settings**.
2. Calibrate any runtime parameter:
   - `grace_period_days`: Number of days overdue without financial penalty (default `2`).
   - `student_daily_rate`: Base daily fine rate for Students (default `$0.50`).
   - `faculty_daily_rate`: Base daily fine rate for Faculty (default `$0.20`).
   - `guest_daily_rate`: Base daily fine rate for Guests (default `$1.00`).
   - `student_max_fine_cap`: Maximum overdue cap for Students (default `$20.00`).
   - `course_reserve_multiplier`: Multiplier for Reserve items (default `2.0x`).
   - `minor_damage_charge`: Fee for minor book damage (default `$5.00`).
   - `lost_processing_fee`: Administrative fee for lost book replacement (default `$10.00`).
3. Click **Update System Policies**. Changes take effect instantly across all subsequent circulation events.

### 4.2 Overdue Delinquency Audits & Data Exports
1. Navigate to the **Reports** tab.
2. Select **Overdue Delinquency Report**.
3. Filter by department, overdue threshold (e.g., $D > 7$ days), or member category.
4. Click **Export to CSV / Excel** to generate institutional audit rosters.
5. Click **Dispatch Overdue Notices** to simulate generating email/SMS notification batches.

### 4.3 Circulation Analytics Dashboard
The Admin Dashboard provides real-time business intelligence powered by Chart.js:
- **Velocity Doughnut Chart:** Breakdown of circulation volume across academic disciplines (Computer Science, Mathematics, Software Engineering, etc.).
- **Monthly Circulation Trends Bar Chart:** Monthly loan issuances vs. returns over the academic semester.
- **Financial Metric Cards:** Total fines assessed, total cash collected, total waived, and current outstanding institutional liabilities.

### 4.4 Database Integrity Verification & Reseeding
1. In the **Admin Tools** panel:
   - **Run Integrity Audit:** Executes `PRAGMA foreign_key_check` and verifies that no orphaned loan records or inconsistent inventory counts exist.
   - **Create Database Backup:** Generates a timestamped SQLite snapshot in the backup directory.
   - **Reseed Demonstration Data:** Restores initial baseline members, catalog books, active loans, and fine records for clean demonstration.

---

## 5. Operational Troubleshooting & Edge Case Handling

| Symptom / Error Message | Operational Cause | Standard Resolution Procedure |
| :--- | :--- | :--- |
| **"Member is currently Suspended"** | Patron has accrued unpaid fines exceeding policy limits or holds an item $> 21$ days overdue. | Direct patron to Fine Settlement modal; settle outstanding fee balance to automatically reactivate account. |
| **"Borrowing limit reached"** | Patron has already checked out their maximum allowed titles (Student: 4, Faculty: 8, Guest: 2). | Patron must check in an existing loaned book before borrowing a new one. |
| **"Cannot renew: Book is already overdue"** | Renewal requested after loan due date has passed. | Institutional policy prohibits renewing overdue books. Book must be returned, fine settled, and re-issued if unreserved. |
| **"Book is reserved by another patron"** | A waiting member has placed a hold on this copy. | Book cannot be checked out to a walk-in borrower; hand over copy to the patron holding the reservation queue position. |
| **"Database is locked"** | High concurrency lock contention during multi-tab operations. | SQLite Write-Ahead Logging (WAL) and 10-second timeout mitigate this; refresh the page. |

---

## 6. Comprehensive Academic Viva Voce Defence Guide

This section prepares all team members to answer examiner questions regarding software engineering principles, algorithms, sizing, and architecture:

---

### 6.1 Process Models & Project Governance

#### Q1: Why did your team choose the Iterative Waterfall model instead of a pure Waterfall or Agile/Scrum approach?
> **Answer:**  
> A **pure Waterfall model** is strictly linear; once a phase finishes, regression is forbidden. However, software engineering projects frequently encounter discovered constraints—for example, during desk testing, edge-case interactions in fine caps necessitated refining our decision logic.  
> Conversely, a **pure Scrum model** prioritizes working software over comprehensive documentation, which risks missing rigorous IEEE-standard specifications required for academic evaluation.  
> The **Iterative Waterfall model** represents the optimal synthesis: it preserves the discipline of formal milestone-gated phases (Requirements $\to$ Design $\to$ Implementation $\to$ Testing), while organizing work into four planned iterations with feedback loops that permit controlled requirement updates via formal Change Requests.

#### Q2: How did you enforce team working rules and individual accountability?
> **Answer:**  
> We instituted four strict governance mechanisms:
> 1. **Weekly 30-Minute Status Meetings:** Formally recorded *what was done*, *what is planned*, and *what is blocked*.
> 2. **Definition of Done (DoD):** A work package is complete only when coded, peer-reviewed, tested with 100% pass rate, and documented.
> 3. **Honesty with Data:** We maintained an Individual Contribution Log where each of the 4 roles logged hours and task descriptions weekly as they occurred.
> 4. **Formal Change Control:** Any scope alteration required a formal Change Request (e.g., `CR-01`, `CR-02`, `CR-03`) evaluated by the CCB and approved by the Project Manager.

---

### 6.2 Decision Table Logic & Fine Engine Verification

#### Q3: What is a Decision Table, and why is it superior to nested `if-else` statements for library fine calculations?
> **Answer:**  
> A **Decision Table** is a formal tabular specification technique representing complex combinational logic with intersecting input conditions and resulting actions.  
> Nested `if-else` blocks suffer from **combinatorial explosion**, hidden edge cases, dead code, and high cyclomatic complexity ($V(G) > 15$). A decision table guarantees:
> 1. **Completeness:** Ensures every permutation of member type, overdue tier, item rarity, damage condition, and repeat history is evaluated.
> 2. **Consistency:** Eliminates contradictory business rules.
> 3. **Direct Test Vector Mapping:** Every column in the decision table directly generates a black-box test case.

#### Q4: How did you reduce the 288 theoretical condition states to 16 canonical rules?
> **Answer:**  
> The Cartesian product of our 5 condition stubs is:
> $$|C_1| \times |C_2| \times |C_3| \times |C_4| \times |C_5| = 3 \times 4 \times 3 \times 4 \times 2 = 288 \text{ states}$$
> We applied **Formal Indifference Analysis**:
> 1. **Lost Book Invariance:** When condition is `Lost` ($C_4$), daily overdue rates, book tiers, and repeat defaulter flags become indifferent; the action is unconditionally Replacement Cost + $\$10.00$ Admin Fee.
> 2. **Grace Period Invariance:** For $0 \le D \le 2$, base overdue rate is $\$0.00$ regardless of tier or defaulter history.
> 3. **Severe Delinquency Invariance:** When $D > 21$, overdue fees hit statutory caps and account suspension is mandatory across all categories.  
> Eliminating these redundant sub-spaces yielded **16 non-overlapping, canonical rules (R1 to R16)** providing 100% domain coverage.

#### Q5: Explain the mathematical fine formula and why Lost books are uncapped.
> **Answer:**  
> For returned books:
> $$F_{total} = \min(D \times R_B \times M_T \times \text{Surcharge}, \text{Cap}) + F_{damage}$$
> - Base rates $R_B$: Student (\$0.50), Faculty (\$0.20), Guest (\$1.00).
> - Multipliers $M_T$: Standard (1.0x), Reserve (2.0x), Rare (3.0x).
> - Caps: Student (\$20), Faculty (\$30), Guest (\$50).  
> **Why Lost books are uncapped (CR-03):** Statutory fine caps exist to prevent routine late return fines from becoming punitive. However, if a patron loses a \$120 reference book, applying a \$20 cap would inflict a \$100 asset loss on the institution. Therefore, replacement valuations are strictly uncapped:
> $$F_{lost} = \text{Replacement Cost} + \$10.00\text{ (Admin Fee)}$$

---

### 6.3 Function Point Analysis (FPA) & COCOMO Sizing

#### Q6: What is Function Point Analysis, and how does it differ from SLOC?
> **Answer:**  
> **Function Point Analysis (IFPUG standard)** quantifies the functional size of software strictly from the user's operational viewpoint, based on the logical data functions (ILF, EIF) and transactional functions (EI, EO, EQ) provided.  
> Source Lines of Code (SLOC) measures implementation artifact length, which fluctuates wildly across languages (e.g., 300 SLOC in Assembly vs. 50 in Python for the same feature). Function Points provide a **technology-independent metric** that can be calculated at the requirements stage before code is written.

#### Q7: Walk us through your project's Function Point calculation.
> **Answer:**  
> 1. **Unadjusted Function Points (UFP):**
>    - 7 Internal Logical Files (ILF): Books, Members, BorrowRecords, Fines, Reservations, Users, Settings $\implies 7 \times 7 = \mathbf{49\text{ FP}}$.
>    - 2 External Interface Files (EIF): Notification Gateway, Payment Gateway $\implies 2 \times 5 = \mathbf{10\text{ FP}}$.
>    - 12 External Inputs (EI) $\implies \mathbf{44\text{ FP}}$.
>    - 4 External Outputs (EO) $\implies \mathbf{22\text{ FP}}$.
>    - 5 External Inquiries (EQ) $\implies \mathbf{17\text{ FP}}$.
>    - **Total UFP = 142 FP**.
> 2. **General System Characteristics (GSC):**
>    - Scored the 14 GSC factors based on technical complexity (online data entry = 5, performance = 4, dynamic settings = 4).
>    - Total Degree of Influence ($\text{TDI}$) = 48.
> 3. **Value Adjustment Factor (VAF):**
>    $$\text{VAF} = 0.65 + (0.01 \times 48) = \mathbf{1.13}$$
> 4. **Final Adjusted Function Points (AFP):**
>    $$\text{AFP} = 142 \times 1.13 = \mathbf{160.46\text{ AFP}}$$
> 5. **Effort & Team Feasibility:** At standard Python productivity (50 SLOC/FP), this corresponds to ~8.0 KSLOC. Under Basic COCOMO Organic mode, this validates our 10-week, 320 person-hour team allocation (~0.50 FP/hour).

---

### 6.4 Data Flow Diagrams (DFDs) & Software Architecture

#### Q8: Explain the difference between DFD Level 0, Level 1, and Level 2.
> **Answer:**  
> - **Context Level 0 DFD:** Models the entire system as a single abstract process (`0.0 Library Management System`), establishing the operational boundary and showing data flows between external entities (Student, Faculty, Librarian, Admin, Payment Gateway) and the system.
> - **Level 1 DFD:** Decomposes Process 0.0 into major functional subsystems:
>   - `1.0 User Authentication`
>   - `2.0 Catalog & Inventory Management`
>   - `3.0 Circulation & Loan Engine`
>   - `4.0 Decision-Table Fine Engine`
>   - `5.0 Reporting & Analytics`  
>   It introduces the 7 canonical data stores (`D1: Users` through `D7: SystemSettings`).
> - **Level 2 DFD:** Provides an explosive decomposition of a specific complex process (Processes 3.0 and 4.0), detailing internal steps such as verifying eligibility, checking hold queues, grading physical return condition, executing the 16 decision rules, applying caps, and updating inventory.

#### Q9: How are Data Stores in DFDs related to the database schema?
> **Answer:**  
> Data Stores in our DFD represent persistent data at rest. In our system, they map directly to relational tables:
> - `D1: Users` $\implies$ `users` table
> - `D2: Books` $\implies$ `books` table
> - `D3: Members` $\implies$ `members` table
> - `D4: BorrowRecords` $\implies$ `borrow_records` table
> - `D5: Fines` $\implies$ `fines` table
> - `D6: Reservations` $\implies$ `reservations` table
> - `D7: SystemSettings` $\implies$ `system_settings` table

---

### 6.5 Quality Assurance, Concurrency & Database Integrity

#### Q10: How does the system handle database concurrency and prevent data loss during checkout?
> **Answer:**  
> We implemented three layers of database safety:
> 1. **Write-Ahead Logging (WAL Mode):** Enabled via `PRAGMA journal_mode = WAL`. WAL separates read and write operations into distinct files, allowing concurrent readers to access the database without blocking writers.
> 2. **ACID Atomic Transactions:** Every checkout or return transaction executes inside an atomic block (`BEGIN TRANSACTION ... COMMIT`). If decrementing available copies succeeds but creating the loan record fails, the entire transaction is rolled back, preventing phantom stock counts.
> 3. **Foreign Key Integrity:** Enforced via `PRAGMA foreign_keys = ON`, utilizing `ON DELETE RESTRICT` on books and members to prevent deletion of entities with active circulation records.

#### Q11: How was Boundary Value Analysis (BVA) applied in testing?
> **Answer:**  
> Because the fine engine branches across numeric overdue boundaries, bugs typically occur at interval edges rather than in the middle. We designed test cases targeting the precise transition boundaries:
> - **Grace Period Boundary:** $D = 0$ (lower bound), $D = 2$ (upper bound $\implies \$0.00$), $D = 3$ (Tier 1 entry $\implies \$1.50$).
> - **Defaulter Surcharge Boundary:** $D = 7$ (no surcharge), $D = 8$ (Tier 2 entry $\implies +20\%$ surcharge triggers).
> - **Suspension Boundary:** $D = 21$ (warning status), $D = 22$ (Tier 3 entry $\implies$ automatic account suspension).
> - **Cap Saturation Boundary:** Student standard loan at $D = 39$ (\$19.50), $D = 40$ (exact \$20.00 cap), $D = 41$ (clamped to \$20.00 ceiling).

---
*End of Documentation Dossier — Library Management System v1.0.0*
