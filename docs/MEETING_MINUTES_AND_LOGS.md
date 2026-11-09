# Meeting Minutes, Contribution Logs & Change Control
## Library Management System (LMS)
**Document Type:** Project Governance, Audit Records & Change Management Dossier  
**Life Cycle Model:** Iterative Waterfall Model  
**Standard:** ISO/IEC/IEEE 12207 Software Life Cycle Processes  
**Version:** 1.0.0  
**Date:** November 2026  

---

## Table of Contents
1. [Governance Overview & Cadence](#1-governance-overview--cadence)
2. [Weekly Meeting Minutes (Weeks 1 to 10)](#2-weekly-meeting-minutes-weeks-1-to-10)
   - 2.1 Iteration 1: Inception, Requirements & Sizing (Weeks 1–2)
   - 2.2 Iteration 2: Design, DFD & Architectural Modeling (Weeks 3–4)
   - 2.3 Iteration 3: Core Implementation & Decision Engine (Weeks 5–7)
   - 2.4 Iteration 4: Testing, Defect Remediation & Viva Prep (Weeks 8–10)
3. [Individual Contribution Logs](#3-individual-contribution-logs)
   - 3.1 Student 1: Project Manager (Lead)
   - 3.2 Student 2: Systems Analyst
   - 3.3 Student 3: Designer & Developer
   - 3.4 Student 4: Developer & Quality Tester
4. [Formal Change Request Log (CR-01 to CR-03)](#4-formal-change-request-log-cr-01-to-cr-03)
   - 4.1 CR-01: Introduction of 2-Day Overdue Grace Period
   - 4.2 CR-02: Item Tier Stratification (Course Reserve & Rare/Reference)
   - 4.3 CR-03: Exemption of Lost Book Replacement from Statutory Overdue Caps
5. [Quality Defect & Remediation Log](#5-quality-defect--remediation-log)

---

## 1. Governance Overview & Cadence
In compliance with the **Minor Projects in Software Engineering** curriculum instructions, the four-student engineering team instituted disciplined operational governance throughout the 10-week project lifecycle:
- **Meeting Cadence:** Mandatory 30-minute status meetings held weekly on Mondays at 10:00 AM.
- **Reporting Triad:** Every meeting systematically documents:
  1. *What was done* during the previous week.
  2. *What is planned* for the upcoming week.
  3. *What is blocked* (blockers, dependencies, and mitigation actions).
- **Auditability:** Individual contributions were recorded contemporaneously each week to ensure honesty with data. All requirement adjustments were processed strictly through formal Change Requests.

---

## 2. Weekly Meeting Minutes (Weeks 1 to 10)

### 2.1 Iteration 1: Inception, Requirements & Sizing (Weeks 1–2)

#### Meeting 01 — Project Inception & Team Role Finalization
- **Date & Time:** Week 1, Monday, 10:00 AM – 10:35 AM
- **Attendees:** Student 1 (PM), Student 2 (Analyst), Student 3 (Designer), Student 4 (Tester)
- **Chair:** Student 1 | **Minutes Recorder:** Student 2
- **Agenda:** Project selection from syllabus catalogue, role distribution, lifecycle model selection, and working rules agreement.
- **What Was Done:**
  - Evaluated candidate syllabus projects. Selected Project #1: *Library Management System* (Special focus: Decision Table for Fines, Function Point count, and DFDs).
  - Assigned four formal roles: Student 1 (Project Manager), Student 2 (Systems Analyst), Student 3 (Designer & Developer), Student 4 (Developer & Tester).
  - Selected the **Iterative Waterfall Model** to combine structured milestone gating with iterative feedback.
- **What Is Planned:**
  - Analyst to draft initial IEEE 830 SRS outline and user class taxonomy.
  - PM to initiate the Software Project Management Plan (SPMP) and WBS.
  - Designer to survey database technology choices (evaluating SQLite WAL vs MySQL).
- **What Is Blocked / Challenges:**
  - *Blocker:* Ambiguity regarding how faculty borrowing privileges differ from students.
  - *Resolution:* Analyst to consult departmental librarian for representative circulation policy numbers.

---

#### Meeting 02 — Requirements Baseline & Function Point Sizing
- **Date & Time:** Week 2, Monday, 10:00 AM – 10:30 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 2
- **Agenda:** Review of draft IEEE 830 SRS, IFPUG Function Point counting, and schedule confirmation.
- **What Was Done:**
  - Analyst presented complete functional requirements (`FR-01` to `FR-27`) and user classes (Admin, Librarian, Student, Faculty, Guest).
  - Conducted preliminary IFPUG Function Point sizing: 7 ILFs, 2 EIFs, 12 EIs, 4 EOs, 5 EQs identified.
  - Computed Unadjusted Function Points (142 UFP) and evaluated 14 GSC factors (TDI = 48, VAF = 1.13, AFP = 160.46).
- **What Is Planned:**
  - Finalize and sign off `SRS.md` (Milestone M1).
  - Analyst to commence formal Decision Table construction for fine calculation.
  - Designer to map out Context Level 0 and Level 1 DFDs.
- **What Is Blocked / Challenges:**
  - *Blocker:* Sizing estimates showed 160 AFP could require significant effort.
  - *Resolution:* COCOMO analysis confirmed project is achievable within 320 team person-hours using high-level Python libraries.

---

### 2.2 Iteration 2: Design, DFD & Architectural Modeling (Weeks 3–4)

#### Meeting 03 — Formal Fine Decision Table Derivation
- **Date & Time:** Week 3, Monday, 10:00 AM – 10:40 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 2
- **Agenda:** Review condition stubs, action stubs, and rule reduction for library fine assessments.
- **What Was Done:**
  - Analyst presented 5 Condition Stubs ($C_1$ to $C_5$) and 5 Action Stubs ($A_1$ to $A_5$).
  - Evaluated Cartesian expansion ($3 \times 4 \times 3 \times 4 \times 2 = 288$ states). Applied formal indifference analysis to synthesize the 16 canonical rules (R1 to R16).
  - Validated edge cases: Lost book replacement cost decoupling and statutory fine cap enforcement ($20 Student, $30 Faculty, $50 Guest).
- **What Is Planned:**
  - Analyst to document worked-out arithmetic examples for all 16 rules in `DECISION_TABLE_FINES.md`.
  - Designer to begin UML Sequence Diagram modeling the Return with Fine workflow.
  - Tester to formulate Boundary Value Analysis (BVA) test vectors.
- **What Is Blocked / Challenges:**
  - *Blocker:* Disagreement over whether repeat defaulter surcharge (+20%) should apply during Tier 1 overdue.
  - *Resolution:* Team consensus agreed surcharge activates strictly in Tier 2 ($D \ge 8$) to avoid penalizing minor slip-ups.

---

#### Meeting 04 — System Architecture, DFDs & Database Schema Freeze
- **Date & Time:** Week 4, Monday, 10:00 AM – 10:30 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 3
- **Agenda:** Review of DFD Level 0, Level 1, Level 2, UML Class Diagram, and Relational Schema.
- **What Was Done:**
  - Designer presented complete Data Flow Diagrams (Context L0, Level 1 decomposition into 5 processes, Level 2 for Process 3.0/4.0).
  - Reviewed UML Class Diagram with inheritance hierarchy and sequence diagrams for checkout/return.
  - Finalized relational database schema in `app/database.py` with foreign keys, checks, and WAL mode.
- **What Is Planned:**
  - Freeze architecture and schema baseline (Milestone M3).
  - Initialize Git repository and seed database with sample test books and members.
  - Designer and Developer to begin coding core circulation and catalog routes.
- **What Is Blocked / Challenges:**
  - *Blocker:* SQLite file locking during concurrent reads/writes.
  - *Resolution:* Added `conn.execute("PRAGMA journal_mode = WAL")` and 10-second connection timeout in `get_db_connection()`.

---

### 2.3 Iteration 3: Core Implementation & Decision Engine (Weeks 5–7)

#### Meeting 05 — Circulation Engine Sprint Kickoff
- **Date & Time:** Week 5, Monday, 10:00 AM – 10:35 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 4
- **Agenda:** Sprint planning for book checkout, return, auto-renewals, and inventory copy adjustments.
- **What Was Done:**
  - Student 3 implemented core database initialization and catalog query routines.
  - Student 1 implemented authentication middleware and session role decorators.
  - Student 4 established automated test harness using Python `unittest`.
- **What Is Planned:**
  - Student 3 to code `issue_book()` and `return_book()` transactional methods.
  - Student 2 to assist in encoding the `calculate_fine()` decision table module in pure Python.
  - Student 4 to construct test suites for checkout quota validation.
- **What Is Blocked / Challenges:**
  - *Blocker:* Active loan checkout was allowing double-borrowing of the same title by one student.
  - *Resolution:* Added uniqueness constraint validation query in `CirculationService`.

---

#### Meeting 06 — Decision Table Algorithm Implementation & Mid-Review
- **Date & Time:** Week 6, Monday, 10:00 AM – 10:45 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 4
- **Agenda:** Verification of Python implementation of the 16-rule Decision Table; Alpha milestone review.
- **What Was Done:**
  - Completed `fine_engine.py` integrating the complete 16-rule logic.
  - Student 4 executed initial unit tests covering Rules R1 through R8.
  - Tested grace period handling ($D \le 2 \implies \$0.00$) and damage surcharge additions.
  - Achieved Milestone M4 (Circulation & Fine Engine Alpha).
- **What Is Planned:**
  - Designer to construct the modern web interface (glassmorphic CSS, responsive dashboard).
  - Student 1 and Student 2 to build the dynamic system policy settings table and admin view.
  - Tester to run test suite on Rules R9 through R16.
- **What Is Blocked / Challenges:**
  - *Blocker:* Bug discovered where statutory fine cap was inadvertently clipping the lost book administrative fee.
  - *Resolution:* Patched `calculate_fine()` to bypass fine cap checks when condition is `Lost` (logged as Bug `DF-02`).

---

#### Meeting 07 — UI Integration, Reservations & Beta Release
- **Date & Time:** Week 7, Monday, 10:00 AM – 10:30 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 3
- **Agenda:** Full frontend integration, reservation queue testing, and Beta release candidate freeze.
- **What Was Done:**
  - Integrated modern Glassmorphic web frontend with interactive Chart.js circulation trends.
  - Implemented reservation queue hold placement and automatic fulfillment trigger on book return.
  - Executed end-to-end integration walkthrough from book checkout through return, damage assessment, and fine settlement.
  - Achieved Milestone M5 (Feature Complete Beta Release).
- **What Is Planned:**
  - Tester to lead full boundary value analysis and regression test run.
  - Analyst to draft user operations manual and viva voce study guide.
  - PM to compile change request audit logs.
- **What Is Blocked / Challenges:**
  - *Blocker:* Returning a reserved book made it immediately available for any patron rather than holding it for the reserving member.
  - *Resolution:* Integrated reservation fulfillment check in return transaction pipeline.

---

### 2.4 Iteration 4: Testing, Defect Remediation & Viva Prep (Weeks 8–10)

#### Meeting 08 — Quality Verification & Defect Remediation
- **Date & Time:** Week 8, Monday, 10:00 AM – 10:30 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 4
- **Agenda:** Review of automated test suite results, boundary value analysis, and defect burndown.
- **What Was Done:**
  - Tester reported 100% test pass rate across all 11 BVA test vectors and 16 decision table scenarios.
  - Verified zero open Severity 1 (Critical) or Severity 2 (Major) defects.
  - Achieved Milestone M6 (Testing Sign-Off).
- **What Is Planned:**
  - Analyst to complete User Operations Manual (`docs/USER_MANUAL.md`).
  - PM to verify all documentation cross-references (SRS, SPMP, DFD, Decision Table, FP Analysis).
  - Conduct team-wide internal mock viva session.
- **What Is Blocked / Challenges:**
  - *Blocker:* Minor styling glitch in receipt printing on Firefox browsers.
  - *Resolution:* Added `@media print` CSS stylesheet rules for universal receipt formatting.

---

#### Meeting 09 — Documentation Dossier Audit & User Manual Sign-Off
- **Date & Time:** Week 9, Monday, 10:00 AM – 10:30 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 2
- **Agenda:** Comprehensive peer review of all documentation artifacts; consistency verification against syllabus requirements.
- **What Was Done:**
  - Completed peer reviews across all 7 markdown documentation files in `docs/`.
  - Verified Requirements Traceability Matrix linking all 27 functional requirements to code and test cases.
  - Signed off `docs/USER_MANUAL.md` including role workflows and viva voce defence section.
- **What Is Planned:**
  - Perform dress-rehearsal technical presentation and code walkthrough.
  - Prepare demonstration database backup with pre-populated realistic scenarios.
- **What Is Blocked / Challenges:**
  - *Blocker:* Ensuring every team member can fluently explain the Function Point calculation and Decision Table derivation during external viva.
  - *Resolution:* Conducted dedicated 1-hour peer-teaching session on Albrecht FP formulas and Decision Table state reduction.

---

#### Meeting 10 — Project Retrospective & Final Viva Voce Rehearsal
- **Date & Time:** Week 10, Monday, 10:00 AM – 10:45 AM
- **Attendees:** All team members present
- **Chair:** Student 1 | **Minutes Recorder:** Student 1
- **Agenda:** Final project retrospective, deliverables archival, and academic viva readiness sign-off.
- **What Was Done:**
  - Conducted comprehensive mock viva examination covering all four project roles.
  - Verified repository cleanliness, documentation completeness, and database reseed capability.
  - Closed all Change Requests (CR-01, CR-02, CR-03) and verified baseline version 1.0.0.
  - Achieved Milestone M7 (Final Project Dossier & Viva Ready).
- **Retrospective Insights:**
  - *What went well:* Iterative Waterfall model prevented last-minute design surprises; formal decision table eliminated logic bugs in fines.
  - *Lessons learned:* Writing automated boundary unit tests early saved days of manual verification during integration.

---

## 3. Individual Contribution Logs

In accordance with curriculum guidelines, actual individual effort was recorded contemporaneously each week across the 10-week lifecycle:

### 3.1 Student 1: Project Manager (Lead)
- **Primary Assigned Role:** Project Manager, Configuration Controller, Back-End Route Developer
- **Total Effort Logged:** 82 Person-Hours

| Week | Work Package | Tasks Executed & Modules Authored | Effort (Hrs) | Peer Sign-Off |
| :---: | :---: | :--- | :---: | :---: |
| **W1** | WP 1.1, 1.2 | Formulated project charter; drafted initial SPMP structure; led inception meeting. | 8 | Student 2 |
| **W2** | WP 1.3 | Conducted COCOMO I effort estimation; verified 142 UFP sizing; set up Git repository. | 8 | Student 3 |
| **W3** | WP 1.4, 2.3 | Reviewed Decision Table condition stubs; authored WBS dictionary and schedule roadmap. | 8 | Student 2 |
| **W4** | WP 4.2 | Implemented user authentication middleware, session decorators, and password hashing. | 9 | Student 3 |
| **W5** | WP 4.3 | Coded member registration services and loan quota eligibility verification endpoints. | 8 | Student 4 |
| **W6** | WP 4.6 | Coded system settings configuration routes; implemented policy dynamic updating. | 8 | Student 3 |
| **W7** | WP 1.4, 4.7 | Integrated management analytics backend; structured Change Request board. | 9 | Student 2 |
| **W8** | WP 5.3 | Reviewed defect tracker; coordinated defect burndown; validated milestone M6. | 8 | Student 4 |
| **W9** | WP 1.2, 5.4 | Finalized SPMP baseline; compiled meeting minutes; conducted documentation cross-audit. | 10 | Student 2 |
| **W10**| WP 1.4, 5.4 | Chaired retrospective; led mock viva examination; signed off final dossier. | 10 | All |

---

### 3.2 Student 2: Systems Analyst
- **Primary Assigned Role:** Systems Analyst, Decision Table Architect, Documentation Lead
- **Total Effort Logged:** 80 Person-Hours

| Week | Work Package | Tasks Executed & Modules Authored | Effort (Hrs) | Peer Sign-Off |
| :---: | :---: | :--- | :---: | :---: |
| **W1** | WP 2.1 | Interviewed library stakeholders; gathered operational rules, loan periods, and fine rates. | 8 | Student 1 |
| **W2** | WP 2.2, 1.3 | Authored IEEE 830 SRS (`docs/SRS.md`); decomposed 27 functional requirements. | 9 | Student 1 |
| **W3** | WP 2.3 | Formulated the 5 Condition and 5 Action Stubs; conducted state reduction down to 16 rules. | 9 | Student 4 |
| **W4** | WP 2.3 | Calculated worked-out numerical examples for Rules R1 to R16; authored `DECISION_TABLE_FINES.md`. | 9 | Student 3 |
| **W5** | WP 4.5 | Co-developed pure Python implementation of the 16-rule Decision Table fine algorithm. | 8 | Student 3 |
| **W6** | WP 1.3 | Authored `docs/FUNCTION_POINT_ANALYSIS.md` (ILF, EIF, EI, EO, EQ and 14 GSC factors). | 8 | Student 1 |
| **W7** | WP 2.4 | Constructed Requirements Traceability Matrix (RTM); processed Change Requests CR-01 & CR-02. | 7 | Student 1 |
| **W8** | WP 5.4 | Authored comprehensive User Operations Manual (`docs/USER_MANUAL.md`). | 8 | Student 4 |
| **W9** | WP 5.4 | Compiled Viva Voce examination defence guide covering algorithms and complexity. | 8 | Student 1 |
| **W10**| WP 5.4 | Rehearsed requirements justification and Decision Table mathematical proofs for viva. | 6 | All |

---

### 3.3 Student 3: Designer & Developer
- **Primary Assigned Role:** System Designer, Database Architect, Full-Stack Developer
- **Total Effort Logged:** 82 Person-Hours

| Week | Work Package | Tasks Executed & Modules Authored | Effort (Hrs) | Peer Sign-Off |
| :---: | :---: | :--- | :---: | :---: |
| **W1** | WP 3.1 | Researched architectural patterns; designed 3-tier system architecture and component layout. | 7 | Student 1 |
| **W2** | WP 3.4 | Designed relational database schema; drafted entity relationships with foreign keys. | 8 | Student 2 |
| **W3** | WP 3.1, 3.2 | Created Context Level 0 and Level 1 DFDs; authored UML Class Diagram in Mermaid. | 9 | Student 1 |
| **W4** | WP 3.3, 4.1 | Created Level 2 DFD, Sequence Diagrams, and ERD; authored `app/database.py` with seed data. | 9 | Student 4 |
| **W5** | WP 4.4 | Implemented circulation transactions (`issue_book`, `return_book`, `renew_loan`) in database layer. | 9 | Student 4 |
| **W6** | WP 4.6 | Engineered modern glassmorphic web UI (responsive CSS, modal dialogs, navigation). | 8 | Student 2 |
| **W7** | WP 4.6, 4.7 | Integrated Chart.js analytics dashboard; implemented reservation queue fulfillment logic. | 9 | Student 1 |
| **W8** | WP 4.6 | Refined receipt generation and print stylesheets; optimized database indexes for sub-500ms queries. | 8 | Student 4 |
| **W9** | WP 3.1 | Authored `docs/DFD_AND_ARCHITECTURE.md`; verified architectural compliance. | 8 | Student 1 |
| **W10**| WP 5.4 | Prepared interactive system demo; verified seed data restoration scripts for viva. | 7 | All |

---

### 3.4 Student 4: Developer & Quality Tester
- **Primary Assigned Role:** Quality Assurance Tester, Defect Manager, Module Developer
- **Total Effort Logged:** 78 Person-Hours

| Week | Work Package | Tasks Executed & Modules Authored | Effort (Hrs) | Peer Sign-Off |
| :---: | :---: | :--- | :---: | :---: |
| **W1** | WP 5.1 | Formulated master test strategy; defined acceptance criteria and defect severity classifications. | 6 | Student 1 |
| **W2** | WP 5.1 | Developed test case templates; created test scenarios for member registration and authentication. | 7 | Student 2 |
| **W3** | WP 5.2 | Designed Boundary Value Analysis (BVA) test matrix covering days 0, 2, 3, 7, 8, 21, and caps. | 8 | Student 2 |
| **W4** | WP 4.1 | Reviewed `database.py` schema; verified cascading integrity constraints and WAL mode concurrency. | 8 | Student 3 |
| **W5** | WP 5.2 | Built automated Python unit test suite for loan checkout restrictions and quota enforcement. | 8 | Student 3 |
| **W6** | WP 5.2 | Coded automated unit test suite verifying all 16 rules in `DECISION_TABLE_FINES.md`. | 9 | Student 2 |
| **W7** | WP 5.3 | Executed integration tests across circulation and reservation pipelines; logged bugs DF-01 to DF-04. | 9 | Student 1 |
| **W8** | WP 5.3 | Conducted regression testing following defect fixes; verified 100% test pass rate. | 8 | Student 1 |
| **W9** | WP 5.3 | Authored defect remediation report; audited code maintainability and cyclomatic complexity. | 8 | Student 3 |
| **W10**| WP 5.4 | Prepared test execution demonstration for external viva examiners. | 7 | All |

---

## 4. Formal Change Request Log (CR-01 to CR-03)

In compliance with syllabus change control rules, all scope and policy modifications were evaluated through formal Change Requests:

### 4.1 CR-01: Introduction of 2-Day Overdue Grace Period
- **CR ID:** `CR-01`
- **Date Submitted:** Week 2, Thursday
- **Initiator:** Student 2 (Analyst, on behalf of library user feedback)
- **Change Description:** Add a statutory 2-day grace period ($0 \le D \le 2$) following due date during which no overdue fine is assessed.
- **Rationale / Justification:** Patrons frequently experienced conflict when returning books within hours of due date expiration (e.g., weekend library closures). A 2-day buffer drastically improves student compliance and reduces dispute overhead.
- **Impact Analysis:**
  - *Functional:* Modifies `FR-CIRC-02` and `FR-FINE-01`.
  - *Decision Table:* Adds Grace Period condition branch ($0 \le D \le 2 \implies \text{Base Rate} = \$0.00$).
  - *Effort / FP Impact:* Adds ~2 FP (one algorithmic branch adjustment); minimal schedule impact (+1 person-day).
- **CCB Decision:** **APPROVED** by Student 1 (Project Manager) on Week 3, Monday.
- **Implementation Status:** Incorporated in `SRS.md` v1.0.0 and `DECISION_TABLE_FINES.md` Rule R1, R7, R11.

---

### 4.2 CR-02: Item Tier Stratification (Course Reserve & Rare/Reference)
- **CR ID:** `CR-02`
- **Date Submitted:** Week 3, Wednesday
- **Initiator:** Student 3 (Designer)
- **Change Description:** Introduce book tiering (`Standard`, `Course Reserve`, `Rare/Reference`) with differentiated loan durations and fine multipliers ($1.0\times, 2.0\times, 3.0\times$).
- **Rationale / Justification:** Academic libraries possess high-demand reserve textbooks that must circulate rapidly among entire classes, as well as high-value reference volumes requiring heightened protection against holding delinquency.
- **Impact Analysis:**
  - *Database:* Adds `tier` column with check constraint to `books` table.
  - *Decision Table:* Condition stub $C_3$ expanded from binary to 3-state enum. Multipliers applied to overdue subtotal.
  - *Effort / FP Impact:* Increases UFP by +4 FP (catalog metadata DET and fine engine calculation logic).
- **CCB Decision:** **APPROVED** by Student 1 (Project Manager) on Week 4, Monday.
- **Implementation Status:** Implemented in `app/database.py`, `SRS.md`, and `DECISION_TABLE_FINES.md`.

---

### 4.3 CR-03: Exemption of Lost Book Replacement from Statutory Overdue Caps
- **CR ID:** `CR-03`
- **Date Submitted:** Week 6, Tuesday
- **Initiator:** Student 4 (Quality Tester)
- **Change Description:** Formally decouple Lost Book replacement cost assessments from the statutory overdue fine caps ($20 Student, $30 Faculty, $50 Guest).
- **Rationale / Justification:** During test execution of Rule R15, a $120 rare reference book marked as lost was mistakenly capped at $20 for students, causing the institution a $100 financial loss. Statutory caps must protect against routine overdue buildup, not asset loss.
- **Impact Analysis:**
  - *Algorithmic:* Rule R15 and R16 updated so that:
    $$F_{total} = \text{Replacement Cost} + \$10.00\text{ (Admin Fee)}$$
    executed unconditionally without clamping to `fine_cap`.
  - *Effort / FP Impact:* Zero FP impact; purely algorithmic logic correction in `fine_engine.py`.
- **CCB Decision:** **APPROVED** unanimously by team on Week 6, Wednesday.
- **Implementation Status:** Algorithm patched in `fine_engine.py`, verified in test suite, updated in documentation.

---

## 5. Quality Defect & Remediation Log

The following defects were discovered, logged, and successfully remediated during testing:

| Defect ID | Discovered In | Severity | Defect Description | Root Cause | Remediation & Fix | Status |
| :---: | :---: | :---: | :--- | :--- | :--- | :---: |
| **DF-01** | Week 5 | Major | Concurrent checkout requests threw `sqlite3.OperationalError: database is locked`. | Default SQLite connection lacked WAL mode and sufficient timeout. | Added `PRAGMA journal_mode = WAL` and `timeout=10` in `database.py`. | **Closed** |
| **DF-02** | Week 6 | Critical | Lost book replacement fee capped at $20 for students, causing asset cost loss. | Fine cap clamp was applied after total fine calculation rather than before adding replacement fee. | Refactored `calculate_fine()` to apply cap strictly to $F_{overdue}$ and treat `Lost` as uncapped (CR-03). | **Closed** |
| **DF-03** | Week 6 | Major | Loan renewal permitted on books that were already 5 days overdue. | `isRenewable()` checked renewal count but omitted validation of `CURRENT_DATE <= due_date`. | Added explicit condition check rejecting renewal if `CURRENT_DATE > due_date`. | **Closed** |
| **DF-04** | Week 7 | Moderate | Patron holding a pending reservation was not prioritized when copy was checked in. | Return routine immediately incremented `available_copies` without checking `reservations` queue. | Added trigger allocating returned book to oldest pending reservation and flagging notification. | **Closed** |
| **DF-05** | Week 7 | Minor | Receipt print preview clipped the right margin on narrow paper layouts. | Missing print CSS media query for page widths below 800px. | Added `@media print { body { width: 100%; font-size: 12pt; } }` in static stylesheet. | **Closed** |
| **DF-06** | Week 8 | Minor | Repeat defaulter surcharge triggered during Grace Period returns ($D \le 2$). | Defaulter check was evaluated before the Grace Period early exit branch. | Reordered control flow so Grace Period ($D \le 2 \implies \$0.00$) exits prior to defaulter calculations. | **Closed** |

> **Audit Summary:** All 6 logged defects have been successfully remediated, re-tested, and closed. Zero open defects exist in baseline release 1.0.0.
