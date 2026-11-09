# Software Requirements Specification (SRS)
## Library Management System (LMS)
**Document Standard:** IEEE Std 830-1998  
**Project Model:** Iterative Waterfall Model  
**Version:** 1.0.0  
**Date:** November 2026  
**Status:** Approved Baseline  

---

## Table of Contents
1. [Introduction](#1-introduction)
   - 1.1 Purpose
   - 1.2 Document Conventions
   - 1.3 Intended Audience and Reading Suggestions
   - 1.4 Product Scope
   - 1.5 References
2. [Overall Description](#2-overall-description)
   - 2.1 Product Perspective
   - 2.2 Product Functions
   - 2.3 User Classes and Characteristics
   - 2.4 Operating Environment
   - 2.5 Design and Implementation Constraints
   - 2.6 User Documentation
   - 2.7 Assumptions and Dependencies
3. [External Interface Requirements](#3-external-interface-requirements)
   - 3.1 User Interfaces
   - 3.2 Hardware Interfaces
   - 3.3 Software Interfaces
   - 3.4 Communications Interfaces
4. [System Features & Functional Requirements](#4-system-features--functional-requirements)
   - 4.1 Module 1: Authentication & Access Control (FR-01 to FR-03)
   - 4.2 Module 2: Member Management (FR-04 to FR-07)
   - 4.3 Module 3: Catalog & Inventory Management (FR-08 to FR-12)
   - 4.4 Module 4: Circulation & Loan Engine (FR-13 to FR-17)
   - 4.5 Module 5: Fine Assessment & Penalties Engine (FR-18 to FR-22)
   - 4.6 Module 6: Reservations & Queue Management (FR-23 to FR-25)
   - 4.7 Module 7: Reporting, Analytics & Administration (FR-26 to FR-28)
5. [Non-Functional Requirements](#5-non-functional-requirements)
   - 5.1 Performance Requirements
   - 5.2 Safety & Data Integrity Requirements
   - 5.3 Security Requirements
   - 5.4 Software Quality Attributes (Usability, Reliability, Availability, Maintainability)
6. [Requirements Traceability Matrix (RTM)](#6-requirements-traceability-matrix-rtm)
7. [Appendix: Glossary & Terminology](#7-appendix-glossary--terminology)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) defines the complete software requirements for the **Library Management System (LMS)** web application. Designed strictly according to the **IEEE Std 830-1998** standard, this document serves as the authoritative technical and functional contract between academic stakeholders, project managers, systems analysts, software architects, software developers, and quality assurance testers throughout the project lifecycle under the **Iterative Waterfall Model**.

### 1.2 Document Conventions
- **Requirement Identifiers:** All functional requirements follow the prefix `FR-[Module]-[Number]`.
- **Non-Functional Identifiers:** All non-functional requirements follow the prefix `NFR-[Category]-[Number]`.
- **Prioritization Schema:** Every requirement is categorized following the MoSCoW prioritization model:
  - **[M] Must Have:** Mandatory requirement essential for minimum viable system operation.
  - **[S] Should Have:** High-priority feature that significantly enhances operational capability.
  - **[C] Could Have:** Desirable feature implemented if time and resources permit.
  - **[W] Won't Have (This Iteration):** Deferred to future incremental iterations.
- **Font & Formatting:** Keywords such as *SHALL*, *MUST*, *REQUIRED*, *SHOULD*, and *MAY* are to be interpreted as described in IETF RFC 2119.

### 1.3 Intended Audience and Reading Suggestions
- **Academic Evaluators & Examiners:** Sections 2, 4, 5, and 6 provide evidence of rigorous software engineering methodology.
- **Project Manager & Scrum Master:** Sections 1.4, 2.5, and 6 establish baseline scope, milestones, and traceability.
- **Systems Analyst & System Architect:** Sections 2, 3, and 4 provide structural definitions for DFD, UML, and ERD mapping.
- **Developers:** Section 4 dictates exact input, processing, and output specifications for each transaction.
- **QA Testers:** Sections 4 and 5 supply the acceptance criteria for black-box and white-box test suite development.

### 1.4 Product Scope
The Library Management System (LMS) is a modern web-based enterprise application engineered to automate the complete operational lifecycle of an academic institutional library. The system replaces obsolete manual registers with a unified, high-integrity digital platform.

Key functional capabilities include:
1. Multi-role role-based access control (Admin, Librarian, Student, Faculty, Guest).
2. Comprehensive bibliographic cataloging with Dewey Decimal/shelf-location tracking and item tiering (Standard, Course Reserve, Rare/Reference).
3. Real-time circulation management supporting checkout, return, auto-renewals, and inventory reservation hold queues.
4. An automated, multi-parameter decision-table-driven fine assessment engine factoring in borrower category, overdue duration, item tier, physical return damage, and repeat default history.
5. Digital fee settlement, receipt issuance, fine waivers, and borrower eligibility sanctions.
6. Management dashboards delivering overdue delinquencies, inventory velocity, circulation trends, and dynamic institutional policy configuration.

### 1.5 References
1. IEEE Std 830-1998: *IEEE Recommended Practice for Software Requirements Specifications*.
2. Albrecht, A.J., & Gaffney, J.E. (1983): *Software Function, Source Lines of Code, and Development Effort Prediction*. IEEE Transactions on Software Engineering.
3. Pressman, R.S., & Maxim, B.R. (2020): *Software Engineering: A Practitioner's Approach* (9th ed.). McGraw-Hill.
4. Sommerville, I. (2016): *Software Engineering* (10th ed.). Pearson.
5. Syllabus Guidelines: *Minor Projects in Software Engineering*, Academic Curriculum Document 2026.

---

## 2. Overall Description

### 2.1 Product Perspective
The Library Management System is a self-contained, three-tier web application operating in an intranet/extranet environment. It interfaces directly with an ACID-compliant relational database (`SQLite 3` in Write-Ahead-Logging mode for atomic, thread-safe circulation transactions, upgradable to `MySQL/PostgreSQL`).

```
+--------------------------------------------------------------------------+
|                        PRESENTATION TIER (CLIENT)                        |
|   HTML5 / CSS3 (Modern Glassmorphic UI) / Vanilla JavaScript / Chart.js  |
+--------------------------------------------------------------------------+
                                    │  HTTPS / REST / Form Data
                                    ▼
+--------------------------------------------------------------------------+
|                       APPLICATION TIER (SERVER)                          |
|   Python Web Engine (Flask/WSGI)                                         |
|   ├── Authentication & Role Middleware                                   |
|   ├── Catalog Service                                                    |
|   ├── Circulation Transaction Engine                                     |
|   ├── Decision-Table Fine Engine                                         |
|   └── Analytics & Report Generator                                       |
+--------------------------------------------------------------------------+
                                    │  SQLite3 Foreign-Key Enforced DB-API
                                    ▼
+--------------------------------------------------------------------------+
|                           DATA TIER (STORAGE)                            |
|   Relational Tables: members, books, borrow_records, fines,              |
|                      reservations, system_settings                       |
+--------------------------------------------------------------------------+
```

### 2.2 Product Functions
1. **Cataloging & Inventory:** Catalog books by ISBN, title, author, category, item tier, total copies, and shelf location.
2. **Member Administration:** Register, categorize, activate, and suspend members across Student, Faculty, and Guest tiers with custom borrowing limits.
3. **Circulation Workflow:** Handle book checkouts, due date calculation, check-ins, physical condition grading, and renewals.
4. **Automated Fine & Penalty Calculation:** Apply mathematical fine logic based on an exhaustive 16+ rule Decision Table covering grace periods, member rates, tier multipliers, damage surcharges, and statutory caps.
5. **Reservation Queue:** Enable members to place holds on out-of-stock titles and notify them when returned.
6. **Institutional Auditing & Reporting:** Produce printable receipts, overdue summaries, circulation statistics, and revenue accounting.

### 2.3 User Classes and Characteristics

| User Class | Technical Expertise | System Rights & Responsibilities | Frequency of Use |
| :--- | :--- | :--- | :--- |
| **System Administrator (Admin)** | High | Full read/write/delete access. Manages staff accounts, system settings, database backup/restore, policy configuration, and audit logs. | Daily administrative check |
| **Librarian / Circulation Desk** | Medium | Front-desk operations: check-in, check-out, condition inspection, fee collection, waiver authorization, and inventory audits. | Continuous daily operation |
| **Faculty Member** | Low to Medium | View catalog, borrow up to 8 books for 30 days, place reservations, view personal borrowing history and fee status. | 2–4 times per week |
| **Student Member** | Medium | Search catalog, borrow up to 4 books for 14 days, reserve titles, track personal due dates, view fines. | Daily to weekly |
| **Guest / External Scholar** | Low to Medium | Search catalog, borrow up to 2 books for 7 days (deposit secured), restricted access to Course Reserve items. | Occasional / Weekly |

### 2.4 Operating Environment
- **Server Platform:** Python 3.10+, Flask 3.x, Werkzeug WSGI.
- **Operating Systems:** Microsoft Windows 10/11, Windows Server 2022, Ubuntu Linux 22.04 LTS.
- **Database Engine:** SQLite 3.37+ with Foreign Key constraints enabled (`PRAGMA foreign_keys = ON`) and Write-Ahead Logging (`PRAGMA journal_mode = WAL`).
- **Client Browsers:** Google Chrome 110+, Mozilla Firefox 110+, Microsoft Edge 110+, Apple Safari 16+. Responsive across desktop (>= 1280px) and mobile viewport (>= 375px).

### 2.5 Design and Implementation Constraints
1. **Relational Integrity:** Strict foreign key integrity must be enforced on delete/update cascading rules (`ON DELETE RESTRICT` for active loans).
2. **Zero-Loss Auditability:** Deleting active circulation or unpaid fine records is strictly prohibited at the database schema level.
3. **Deterministic Fines:** Fine calculations must be 100% deterministic, deriving fines from persisted loan dates, return dates, member tiers, and damage conditions using the formal decision table.
4. **Statutory Caps:** Fine accumulators must never exceed the member category caps ($20 Student, $30 Faculty, $50 Guest), except in book replacement cases.
5. **Lightweight Deployment:** The system must run smoothly without external cloud infrastructure dependencies, self-hosting all assets locally.

### 2.6 User Documentation
The application package includes:
- Comprehensive User Manual (`docs/USER_MANUAL.md`) with role-based operational procedures.
- Viva Voce technical defence guide covering algorithm complexity, decision table derivation, and Function Point metrics.
- Inline contextual help tooltips and interactive error alerts across all forms.

### 2.7 Assumptions and Dependencies
- **System Clocks:** Server system time is synchronized via NTP, as all loan and overdue calculations depend on `datetime.now()`.
- **Currency:** Calculations are denominated in USD standard currency format with two decimal places.
- **Physical Handover:** Book condition inspection occurs physically at the circulation desk during check-in.

---

## 3. External Interface Requirements

### 3.1 User Interfaces
- **Layout Architecture:** Glassmorphism UI styled with modern CSS variables, CSS Grid, and Flexbox. High-contrast typography and clear visual cues.
- **Navigation Structure:** Top sticky navigation bar displaying active module links, search input, member profile pill, and dynamic badge notifications for overdue loans.
- **Operational Screens:**
  1. *Dashboard:* High-level KPI metric cards (Active Loans, Overdue Items, Total Books, Pending Fines) and circulation activity stream.
  2. *Catalog Management:* Real-time filterable book grid with cover thumbnails, available copy badges, tier indicators, and modal editing forms.
  3. *Circulation Desk:* Instant two-field issue/return terminal with auto-complete member code and ISBN lookup.
  4. *Fines & Fee Settlement Terminal:* Detailed breakdown modal showing base fine, multiplier, damage assessment, cap adjustment, and payment recording.
  5. *Member Registry:* Card-based member overview with tier tags, borrowing statistics, and suspension toggles.
  6. *Reports & Analytics:* Exportable tabular overdue reports and interactive Chart.js circulation breakdown graphs.

### 3.2 Hardware Interfaces
- No proprietary hardware is mandated.
- Compatible with standard USB/Bluetooth optical barcode scanners operating in keyboard-wedge mode (auto-entering ISBN/Member Code followed by Return key).
- Standard A4/thermal receipt printers for circulation receipts.

### 3.3 Software Interfaces
- **Python Standard Library:** `sqlite3`, `datetime`, `os`, `json`, `math`, `csv`.
- **Web Framework:** Flask microframework providing routing, session handling, and Jinja2 templating.
- **Visualization Library:** Chart.js 4.4 CDN / embedded for circulation analytics.
- **External Mock Payment Gateway:** REST-based payment webhook simulation returning payment verification tokens.

### 3.4 Communications Interfaces
- HTTPS over TLS 1.3 for secure encrypted transport in production.
- Standard HTTP 1.1 / HTTP/2 for local intranet operations.
- Application data interchange via JSON payloads and `multipart/form-data`.

---

## 4. System Features & Functional Requirements

### 4.1 Module 1: Authentication & Access Control

#### `FR-AUTH-01` User Login & Session Management [M]
- **Description:** Authenticate users against stored credentials and issue a role-scoped cryptographic session.
- **Inputs:** Username/Email (string), Password (string), Selected Role.
- **Processing:**
  1. Verify non-empty credentials.
  2. Query database for user account matching username.
  3. Validate password hash using secure salted SHA-256 or bcrypt.
  4. If valid, initialize session containing `user_id`, `role`, and `login_timestamp`.
  5. Reject invalid attempts with generic error: "Invalid username or password".
- **Outputs:** Redirect to Dashboard with active session cookie; error banner on failure.

#### `FR-AUTH-02` Role-Based Route Authorization [M]
- **Description:** Enforce strict access control ensuring users only execute actions permitted by their role.
- **Inputs:** Active session role, Target URL endpoint, HTTP Method.
- **Processing:**
  1. Intercept request via route decorator (`@role_required`).
  2. Check if current role matches endpoint permissions:
     - Admin: Full access (`/admin/*`, `/settings/*`, `/catalog/*`, `/circulation/*`, `/fines/*`).
     - Librarian: Circulation, Catalog, Fines, Reservations (`/catalog/*`, `/circulation/*`, `/fines/*`).
     - Student/Faculty/Guest: Self-service catalog, self loan view, reservations (`/catalog/view`, `/my-account`).
  3. Return HTTP 403 Forbidden if unauthorized.
- **Outputs:** Allowed page rendering or HTTP 403 Access Denied.

#### `FR-AUTH-03` User Logout & Session Invalidation [M]
- **Description:** Terminate user session and purge session tokens.
- **Inputs:** User logout action trigger.
- **Processing:** Clear server session dictionary, expire client cookie, redirect to login page.
- **Outputs:** Login screen with flash confirmation "You have been logged out safely."

---

### 4.2 Module 2: Member Management

#### `FR-MEM-01` Member Registration & Code Generation [M]
- **Description:** Register new library patrons with automatic unique Member Code assignment.
- **Inputs:** Full Name, Email, Phone, Member Category (`Student`, `Faculty`, `Guest`).
- **Processing:**
  1. Validate email format and ensure uniqueness across database.
  2. Generate unique alphanumeric Member Code (`MEM-STU-XXX`, `MEM-FAC-XXX`, `MEM-GST-XXX`).
  3. Assign policy limits based on category:
     - Student: Max 4 books, 14 days loan period.
     - Faculty: Max 8 books, 30 days loan period.
     - Guest: Max 2 books, 7 days loan period.
  4. Set account status to `Active`.
  5. Persist record to `members` table.
- **Outputs:** Success toast notification, new member card displayed in directory.

#### `FR-MEM-02` Member Eligibility & Delinquency Verification [M]
- **Description:** Verify borrower standing prior to granting any new loan.
- **Inputs:** `member_id` (integer).
- **Processing:**
  1. Fetch member status: If `Suspended` or `Expired`, immediately deny checkout.
  2. Count currently checked-out books (`borrow_records` where `status = 'Active'`). If active count >= `max_books`, deny checkout.
  3. Query outstanding unpaid fines for member: If sum(`total_fine`) > $0.00, deny checkout and flag delinquency.
  4. Check for any currently overdue books held by member: If any exist, deny checkout.
- **Outputs:** Boolean flag `is_eligible`, along with detailed refusal reason if ineligible.

#### `FR-MEM-03` Member Suspension & Account Re-activation [S]
- **Description:** Automatically or manually suspend borrowing privileges upon policy breach or fine settlement.
- **Inputs:** `member_id`, action (`Suspend` | `Reactivate`), reason note.
- **Processing:**
  1. When member incurs fine exceeding statutory threshold or has book overdue > 21 days, trigger auto-suspension (`status = 'Suspended'`).
  2. When all delinquent books are checked in and all unpaid fines are settled in full, automatically restore `status = 'Active'`.
  3. Provide Admin override to manually toggle status.
- **Outputs:** Updated database record, status badge change, audit log entry.

#### `FR-MEM-04` Member Directory Filtering & History Inspection [S]
- **Description:** Allow librarians to view and search patron records and examine complete circulation history.
- **Inputs:** Search keyword (Name, Code, Email), Member Category filter, Status filter.
- **Processing:** Execute parameterized SQL search with `LIKE` clauses; join `borrow_records` and `fines` to compute lifetime borrowing volume and outstanding liability.
- **Outputs:** Paginated list of member records with live loan metrics.

---

### 4.3 Module 3: Catalog & Inventory Management

#### `FR-CAT-01` Bibliographic Item Ingestion [M]
- **Description:** Add new book titles and initialize copy inventory.
- **Inputs:** ISBN (13-digit), Title, Author, Category, Item Tier (`Standard`, `Course Reserve`, `Rare/Reference`), Publisher, Publication Year, Total Copies, Shelf Location, Replacement Cost ($), Cover URL.
- **Processing:**
  1. Validate ISBN-10 or ISBN-13 format. Check uniqueness of ISBN.
  2. Validate Total Copies >= 1, Replacement Cost > 0.
  3. Set `available_copies = total_copies`.
  4. Insert record into `books` table.
- **Outputs:** Book added confirmation; item immediately visible in catalog.

#### `FR-CAT-02` Catalog Modification & Copy Replenishment [M]
- **Description:** Update book bibliographic details or alter inventory copy count.
- **Inputs:** `book_id`, updated fields, added/removed copy delta.
- **Processing:**
  1. Verify book existence.
  2. If total copies is adjusted, verify `new_total_copies >= (total_copies - available_copies)` to prevent reducing below loaned count.
  3. Update `available_copies` proportionally.
  4. Save updates into `books`.
- **Outputs:** Updated catalog record.

#### `FR-CAT-03` Multi-Facet Catalog Search [M]
- **Description:** Enable patrons and staff to search the collection across multiple simultaneous parameters.
- **Inputs:** Keyword query, Category filter, Tier filter, Availability toggle (`Available only` / `All`).
- **Processing:**
  1. Construct parameterized SQL query:
     `SELECT * FROM books WHERE (title LIKE ? OR author LIKE ? OR isbn LIKE ?) AND category = ? ...`
  2. Return matched book records ordered by title.
- **Outputs:** Responsive card/table view displaying real-time availability badges.

#### `FR-CAT-04` Tier Classification Management [S]
- **Description:** Classify books into policy tiers governing checkout eligibility and fine multipliers.
- **Inputs:** `book_id`, `tier` (`Standard`, `Course Reserve`, `Rare/Reference`).
- **Processing:**
  1. Standard: Standard loan duration, 1x fine multiplier.
  2. Course Reserve: High-demand textbook; max loan period shortened to 3 days, 2x fine multiplier.
  3. Rare/Reference: In-library use or faculty-only short loan; 3x fine multiplier, strict condition checks.
- **Outputs:** Tier badge updated; circulation policies dynamically adjust.

#### `FR-CAT-05` Deletion & Weeding Protection [M]
- **Description:** Protect bibliographic records from accidental deletion when active transactions exist.
- **Inputs:** `book_id` delete request.
- **Processing:**
  1. Query `borrow_records` for active or overdue loans referencing `book_id`.
  2. If active records exist, abort deletion with error: "Cannot delete book with active loans".
  3. If no active loans exist, execute deletion or mark as archived/weeded.
- **Outputs:** Deletion confirmation or integrity error message.

---

### 4.4 Module 4: Circulation & Loan Engine

#### `FR-CIRC-01` Issue Book Transaction (Checkout) [M]
- **Description:** Check out a book copy to an eligible member.
- **Inputs:** `member_code` or `member_id`, `isbn` or `book_id`.
- **Processing:**
  1. Validate member existence and check eligibility via `FR-MEM-02`.
  2. Validate book existence. Check `available_copies > 0`.
  3. Check if member already has an active loan for this exact book title. If yes, reject.
  4. If book tier is `Rare/Reference`, verify member category is `Faculty` or Librarian administrative override is provided.
  5. Check `reservations` queue for this book: If pending reservation belongs to another member, reject checkout.
  6. Calculate `issue_date = CURRENT_DATE`.
  7. Compute `due_date = issue_date + member.loan_period_days` (adjusted to 3 days if book tier is `Course Reserve`).
  8. Begin DB transaction:
     - Insert record into `borrow_records (book_id, member_id, issue_date, due_date, status='Active')`.
     - Decrement `books.available_copies` by 1.
  9. Commit transaction.
- **Outputs:** Loan created receipt displaying Member Name, Book Title, Issue Date, Due Date.

#### `FR-CIRC-02` Return Book Transaction (Check-In) [M]
- **Description:** Process the physical return of a borrowed book, calculate overdues, inspect physical condition, and assess fines.
- **Inputs:** `borrow_record_id`, Return Date (defaults to `CURRENT_DATE`), Book Physical Condition (`Normal`, `Minor Damage`, `Severe Damage`, `Lost`), Optional Notes.
- **Processing:**
  1. Fetch active `borrow_record`. If already returned, reject.
  2. Calculate `days_overdue = max(0, return_date - due_date)`.
  3. Execute Decision Table Fine Engine (`FR-FINE-01`) passing:
     - Member Category
     - Days Overdue
     - Book Tier
     - Book Physical Condition
     - Member Default History
  4. Begin DB transaction:
     - Update `borrow_records` with `return_date`, `status = ('Returned' or 'Lost')`, `return_condition = condition`.
     - Increment `books.available_copies` by 1 (unless condition is `Lost`).
     - If calculated fine > 0, insert record into `fines` table with complete breakdown.
     - If book condition is `Lost`, deduct 1 from `books.total_copies`.
     - Check `reservations` queue: if pending reservations exist, mark oldest reservation as `Fulfilled` and flag notification.
  5. Commit transaction.
- **Outputs:** Return confirmation modal displaying overdue days, fine breakdown (if any), and printable return receipt.

#### `FR-CIRC-03` Loan Renewal [M]
- **Description:** Extend the loan period of an active checkout if policy conditions are met.
- **Inputs:** `borrow_record_id`.
- **Processing:**
  1. Fetch active loan. Ensure `status = 'Active'`.
  2. Verify current date <= `due_date` (cannot renew an already overdue book).
  3. Verify `renewals_count < system_settings.max_renewals_allowed` (default 2).
  4. Verify no pending reservations exist for this book in `reservations` table.
  5. Verify member has no other delinquent books or outstanding unpaid fines.
  6. Calculate `new_due_date = due_date + member.loan_period_days`.
  7. Increment `renewals_count` by 1.
  8. Update `borrow_records`.
- **Outputs:** Renewal confirmation banner with extended due date.

#### `FR-CIRC-04` Automated Overdue Batch Detection [S]
- **Description:** Daily automated background task to detect loans exceeding due date and update loan statuses.
- **Inputs:** System trigger / application startup / daily schedule.
- **Processing:**
  1. Query all `borrow_records` where `status = 'Active'` and `due_date < CURRENT_DATE`.
  2. Update status to `Overdue`.
  3. If `days_overdue > 21`, flag member for immediate borrowing suspension.
- **Outputs:** Batch status count log (e.g., "4 loans flagged as Overdue").

#### `FR-CIRC-05` Circulation Receipt Generation [S]
- **Description:** Generate standardized digital and printable proof of checkout or return.
- **Inputs:** `borrow_record_id`.
- **Processing:** Compile transaction receipt containing Transaction ID, Member Code, Member Name, ISBN, Title, Issue Date, Due Date, Return Date, Fine Incurred, and Cashier/Librarian ID.
- **Outputs:** Clean, printable HTML/PDF receipt dialog.

---

### 4.5 Module 5: Fine Assessment & Penalties Engine

#### `FR-FINE-01` Formal Decision Table Execution Engine [M]
- **Description:** Implement the formal 16-rule decision table to calculate accurate, unalterable overdue and damage assessments.
- **Inputs:** Member Category (`Student` | `Faculty` | `Guest`), Days Overdue ($D \ge 0$), Book Tier (`Standard` | `Course Reserve` | `Rare/Reference`), Physical Condition (`Normal` | `Minor Damage` | `Severe Damage` | `Lost`), Member Repeat Default History (`Yes` | `No`).
- **Processing:**
  1. **Grace Period Evaluation:** If $0 \le D \le 2$, base overdue charge is $0.00.
  2. **Base Daily Rate ($R_B$):**
     - Student: $0.50 / day.
     - Faculty: $0.20 / day.
     - Guest: $1.00 / day.
  3. **Tier Multiplier ($M_T$):**
     - Standard: $1.0\times$.
     - Course Reserve: $2.0\times$.
     - Rare/Reference: $3.0\times$.
  4. **Overdue Subtotal ($F_{overdue}$):**
     - If $D > 2$: $F_{overdue} = D \times R_B \times M_T$.
     - If repeat defaulter is `Yes` and $D > 7$: Add 20% surcharge to $F_{overdue}$.
  5. **Statutory Overdue Cap Application:**
     - Student Cap: $\min(F_{overdue}, \$20.00)$.
     - Faculty Cap: $\min(F_{overdue}, \$30.00)$.
     - Guest Cap: $\min(F_{overdue}, \$50.00)$.
  6. **Physical Damage Penalty ($F_{damage}$):**
     - Normal: $\$0.00$.
     - Minor Damage (torn pages, markings, water spots): $\$5.00$.
     - Severe Damage (broken spine, missing pages): $\$15.00$.
  7. **Lost Book Assessment ($F_{lost}$):**
     - If condition is `Lost`: $F_{overdue} = 0$, $F_{damage} = 0$, and assessment becomes:
       $$F_{total} = \text{Replacement Cost} + \$10.00\text{ (Admin Fee)}$$
       *(Statutory fine caps DO NOT apply to lost book replacement costs).*
  8. **Total Fine Assessment:**
     $$F_{total} = \min(F_{overdue}, \text{Cap}) + F_{damage} + F_{lost}$$
  9. Identify matching Decision Table Rule Identifier (e.g., `Rule R4`).
- **Outputs:** Calculated record: `base_rate`, `tier_multiplier`, `overdue_fine`, `damage_fine`, `replacement_fee`, `total_fine`, `rule_applied`.

#### `FR-FINE-02` Fine Payment & Cashier Reconciliation [M]
- **Description:** Record cash, card, or mock online payment against outstanding fine records.
- **Inputs:** `fine_id`, Amount Paid, Payment Method (`Cash`, `Card`, `Campus Wallet`), Reference Note.
- **Processing:**
  1. Validate `fine_id` and ensure `paid_status = 'Unpaid'`.
  2. Verify amount paid matches `total_fine` (full settlement).
  3. Update `fines`:
     - `paid_status = 'Paid'`
     - `paid_date = CURRENT_TIMESTAMP`
     - `payment_method = method`
  4. Check if member has any other unpaid fines. If none and no overdue books, restore `members.status = 'Active'`.
- **Outputs:** Payment receipt, updated member standing.

#### `FR-FINE-03` Administrative Fine Waiver [S]
- **Description:** Allow authorized Librarians/Admins to waive fines under medical or institutional hardship circumstances.
- **Inputs:** `fine_id`, Waiver Reason, Approving Admin Credentials.
- **Processing:**
  1. Validate user has `Admin` or `Librarian` privileges.
  2. Record waiver note in `fines` table.
  3. Update `paid_status = 'Waived'`, `paid_date = CURRENT_TIMESTAMP`.
  4. Write entry to audit log.
- **Outputs:** Fine marked as waived; member balance cleared.

#### `FR-FINE-04` Automated Account Suspension Enforcement [M]
- **Description:** Automatically update member account status to `Suspended` whenever fine conditions warrant.
- **Inputs:** Triggered upon fine creation or daily audit.
- **Processing:**
  - If member total unpaid fines > $10.00 OR overdue loan > 21 days OR unreturned book marked `Lost`, set `members.status = 'Suspended'`.
- **Outputs:** Account status updated in database; borrower barred from subsequent checkouts.

---

### 4.6 Module 6: Reservations & Queue Management

#### `FR-RES-01` Place Book Reservation (Hold) [M]
- **Description:** Allow a patron to reserve a book title when all copies are currently checked out.
- **Inputs:** `book_id`, `member_id`.
- **Processing:**
  1. Verify book has `available_copies == 0`. (If copies are on the shelf, reservations are disallowed; patron is directed to checkout).
  2. Check if member already has an active reservation or loan for this book. If so, reject.
  3. Verify member account is in good standing (`status == 'Active'`).
  4. Insert record into `reservations (book_id, member_id, status='Pending', reserved_at=CURRENT_TIMESTAMP)`.
- **Outputs:** Reservation confirmation with queue position (e.g., "Reserved at position #1").

#### `FR-RES-02` Reservation Fulfillment on Return [M]
- **Description:** Automatically assign returned books to the first waiting patron in the reservation queue.
- **Inputs:** Triggered during `FR-CIRC-02` (Book Return).
- **Processing:**
  1. When book is returned, query `reservations` for oldest `Pending` record for `book_id` ordered by `reserved_at ASC`.
  2. If reservation exists:
     - Mark reservation as `Fulfilled`.
     - Set `notified_at = CURRENT_TIMESTAMP`.
     - Keep book in held status for patron for 48 hours.
- **Outputs:** Librarian alert: "Book held for Member Aarav Sharma (Reservation #3)".

#### `FR-RES-03` Reservation Cancellation & Expiry [S]
- **Description:** Cancel an existing hold request either by patron action or after 48-hour pickup window lapse.
- **Inputs:** `reservation_id`, Cancellation Reason (`User Cancelled` | `Pickup Expired`).
- **Processing:**
  1. Update `reservations.status = 'Cancelled'`.
  2. If book was held on shelf, release copy back to general availability (`available_copies += 1`) or allocate to next reservation in queue.
- **Outputs:** Reservation cancelled confirmation.

---

### 4.7 Module 7: Reporting, Analytics & Administration

#### `FR-REP-01` Overdue & Delinquency Report [M]
- **Description:** Produce real-time reporting of all unreturned books currently exceeding their due dates.
- **Inputs:** Filter criteria (Overdue Days > X, Member Category, Department).
- **Processing:**
  1. Execute joined query across `borrow_records`, `members`, and `books`.
  2. Calculate days overdue, accrued estimated fine, and contact phone/email for each record.
- **Outputs:** Tabular report exportable to CSV or formatted print layout.

#### `FR-REP-02` Circulation Velocity & Category Analytics [S]
- **Description:** Generate visual charts and metrics displaying most-borrowed categories, monthly circulation trends, and fine revenues.
- **Inputs:** Date range selection (Last 7 Days, Last 30 Days, Year-to-Date).
- **Processing:**
  1. Aggregate loan volumes grouped by book category.
  2. Aggregate fine collections grouped by payment method and member type.
  3. Format data arrays into JSON for Chart.js rendering.
- **Outputs:** Interactive doughnut and bar charts on Admin Dashboard.

#### `FR-REP-03` Dynamic System Policy Configuration [S]
- **Description:** Allow Administrator to dynamically calibrate fine rates, grace periods, and borrowing caps without code changes.
- **Inputs:** Key-value pairs for `grace_period_days`, `student_daily_rate`, `faculty_daily_rate`, `student_max_fine_cap`, etc.
- **Processing:**
  1. Validate numeric input values (ensure rates >= 0, caps >= 5).
  2. Update key-value rows in `system_settings` table.
  3. Reload cached in-memory policy configuration.
- **Outputs:** Policy update confirmation toast; immediate runtime application across all subsequent checkout/return events.

#### `FR-REP-04` Database Integrity Check & Seed Data Reset [S]
- **Description:** Administrative tool to verify database foreign-key integrity, create automated database backups, or reseed realistic demonstration data.
- **Inputs:** Admin authentication credentials, Action (`Integrity Check`, `Create Backup`, `Seed Demo Data`).
- **Processing:**
  1. Run `PRAGMA foreign_key_check`.
  2. Copy `library.db` to timestamped backup directory.
  3. If seed requested, execute `seed_initial_data()` from `database.py`.
- **Outputs:** Operational diagnostic summary report.

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
- **`NFR-PERF-01` Response Time:** Catalog search and transaction processing queries must return results within **under 500 milliseconds** for a database size of up to 100,000 records.
- **`NFR-PERF-02` Concurrency:** The system must comfortably handle **50 simultaneous active user sessions** without database lock contention or thread starvation by leveraging SQLite's WAL (Write-Ahead Logging) mode.
- **`NFR-PERF-03` Page Load Budget:** Initial web application page load time must not exceed **1.2 seconds** over standard campus broadband (10 Mbps+), with total page asset payload kept below 1.5 MB.
- **`NFR-PERF-04` Database Query Optimization:** All frequently filtered database columns (`members.member_code`, `books.isbn`, `borrow_records.status`, `borrow_records.due_date`) must be indexed to ensure $O(\log n)$ search efficiency.

### 5.2 Safety & Data Integrity Requirements
- **`NFR-SAFE-01` ACID Compliance:** All circulation transactions involving multi-table operations (decrementing copy count, inserting borrow record, updating member quota) must be encapsulated in atomic database transactions (`BEGIN TRANSACTION ... COMMIT`).
- **`NFR-SAFE-02` Foreign Key Enforcement:** The database engine must strictly enforce foreign key constraints (`PRAGMA foreign_keys = ON`), preventing orphan loan or fine records.
- **`NFR-SAFE-03` Zero-Deletion of Financial History:** Fine records must never be physically purged; status transitions must be limited to `Unpaid -> Paid` or `Unpaid -> Waived` with timestamped cashier attribution.

### 5.3 Security Requirements
- **`NFR-SEC-01` Injection Prevention:** All SQL interactions must exclusively utilize parameterized queries (`cursor.execute(sql, (param1, param2))`). Dynamic string interpolation in SQL statements is strictly prohibited.
- **`NFR-SEC-02` Cross-Site Scripting (XSS) Sanitization:** All user inputs rendered in HTML templates must be auto-escaped using Jinja2 engine defaults.
- **`NFR-SEC-03` Session Integrity:** Session identifiers must be stored in HTTP-only, SameSite-restricted cookies signed with a cryptographically random 256-bit secret key.
- **`NFR-SEC-04` Privilege Separation:** Direct URL manipulation by a low-privilege user attempting to access admin endpoints (`/admin`, `/settings`) must be blocked by server middleware with an audit warning logged.

### 5.4 Software Quality Attributes
- **`NFR-QUAL-01` Usability:** The user interface must achieve a **System Usability Scale (SUS) score of >= 80**. Desk librarians must be able to complete a standard book checkout transaction in **fewer than 4 keypresses / clicks**.
- **`NFR-QUAL-02` Availability:** The application must maintain an operational uptime of **99.5%** during institutional operational hours (08:00 to 22:00 daily).
- **`NFR-QUAL-03` Reliability & MTBF:** Mean Time Between Failures (MTBF) must exceed **720 operational hours** (30 days continuous operation) with Mean Time to Recovery (MTTR) under 15 minutes.
- **`NFR-QUAL-04` Maintainability:** The software codebase must adhere strictly to PEP 8 standards, maintain clean modular separation between database access, business calculation engines, and presentation templates, and achieve cyclomatic complexity $V(G) \le 10$ across all functional methods.
- **`NFR-QUAL-05` Portability:** The entire system must execute seamlessly on Windows, macOS, and Linux platforms with zero binary recompilation requirements, using standard Python 3.10+ environments.

---

## 6. Requirements Traceability Matrix (RTM)

The following matrix verifies that every functional requirement is mapped to its architectural component, database entities, decision table rule, and test verification suite:

| Req ID | Requirement Title | Architectural Module | Database Tables Involved | Associated Rule / Spec | Test Case Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-AUTH-01** | User Login & Authentication | `auth_service.py` | `users` | IEEE 830 Sec 3.1 | `TC-AUTH-01` |
| **FR-AUTH-02** | Role-Based Authorization | `middleware.py` | `users` | IEEE 830 Sec 3.1 | `TC-AUTH-02` |
| **FR-MEM-01** | Member Registration | `member_service.py` | `members` | IEEE 830 Sec 4.2 | `TC-MEM-01` |
| **FR-MEM-02** | Delinquency Verification | `circulation_service.py`| `members`, `fines` | Decision Table C5 | `TC-CIRC-04` |
| **FR-MEM-03** | Member Suspension | `member_service.py` | `members` | Decision Table A4 | `TC-MEM-03` |
| **FR-CAT-01** | Book Catalog Ingestion | `catalog_service.py` | `books` | IEEE 830 Sec 4.3 | `TC-CAT-01` |
| **FR-CAT-03** | Catalog Multi-Search | `catalog_service.py` | `books` | IEEE 830 Sec 4.3 | `TC-CAT-03` |
| **FR-CAT-04** | Book Tier Classification | `catalog_service.py` | `books` | Decision Table C3 | `TC-CAT-04` |
| **FR-CIRC-01**| Issue Book Transaction | `circulation_service.py`| `borrow_records`, `books`| IEEE 830 Sec 4.4 | `TC-CIRC-01` |
| **FR-CIRC-02**| Return Book Processing | `circulation_service.py`| `borrow_records`, `books`| IEEE 830 Sec 4.4 | `TC-CIRC-02` |
| **FR-CIRC-03**| Loan Renewal | `circulation_service.py`| `borrow_records` | IEEE 830 Sec 4.4 | `TC-CIRC-03` |
| **FR-FINE-01**| Decision Table Fines Engine | `fine_engine.py` | `fines`, `system_settings`| Rules R1 to R16 | `TC-FINE-01..16`|
| **FR-FINE-02**| Fine Payment & Receipt | `fine_engine.py` | `fines`, `members` | IEEE 830 Sec 4.5 | `TC-FINE-17` |
| **FR-FINE-03**| Administrative Waiver | `fine_engine.py` | `fines` | IEEE 830 Sec 4.5 | `TC-FINE-18` |
| **FR-RES-01** | Place Book Reservation | `reservation_service.py`| `reservations` | IEEE 830 Sec 4.6 | `TC-RES-01` |
| **FR-RES-02** | Reservation Fulfillment | `reservation_service.py`| `reservations`, `books` | IEEE 830 Sec 4.6 | `TC-RES-02` |
| **FR-REP-01** | Overdue Delinquency Report | `report_service.py` | `borrow_records`, `fines`| IEEE 830 Sec 4.7 | `TC-REP-01` |
| **FR-REP-03** | Dynamic System Settings | `settings_service.py` | `system_settings` | IEEE 830 Sec 4.7 | `TC-SET-01` |

---

## 7. Appendix: Glossary & Terminology

- **ACID:** Atomicity, Consistency, Isolation, Durability — set of properties of database transactions.
- **AFP:** Adjusted Function Points — metric of software functional size adjusted for environmental characteristics.
- **Course Reserve:** Core academic textbooks placed on high-demand loan rules with shortened checkout durations and increased fine rates.
- **Decision Table:** A tabular software engineering method for specifying complex logical business rules and combinations of inputs with resulting actions.
- **Grace Period:** A statutory initial window (default 2 calendar days) following the loan due date during which the borrower can return an overdue item without incurring financial fines.
- **IFPUG:** International Function Point Users Group — the standard governing body for functional software measurement.
- **ISBN:** International Standard Book Number — a 10 or 13-digit commercial book identifier.
- **RTM:** Requirements Traceability Matrix — a cross-referencing document mapping requirements to downstream design, code, and test cases.
- **VAF:** Value Adjustment Factor — derived from the 14 General System Characteristics in Function Point analysis.
- **WAL:** Write-Ahead Logging — an SQLite journaling mode providing high concurrent reader-writer throughput.
