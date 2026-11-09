# Function Point Analysis (FPA) & Effort Estimation
## Library Management System (LMS)
**Methodology Standard:** IFPUG Counting Practices Manual (CPM 4.3.1) / Albrecht Function Point Model  
**Project Special Syllabus Focus:** Function Point (FP) Count, Cost & Effort Estimation  
**Version:** 1.0.0  
**Date:** November 2026  

---

## Table of Contents
1. [Introduction to Function Point Analysis](#1-introduction-to-function-point-analysis)
   - 1.1 Objectives & Academic Significance
   - 1.2 IFPUG Architectural Foundations
2. [Data Function Types (ILF & EIF)](#2-data-function-types-ilf--eif)
   - 2.1 Internal Logical Files (ILF) Evaluation
   - 2.2 External Interface Files (EIF) Evaluation
   - 2.3 Data Functions Complexity Matrix
3. [Transactional Function Types (EI, EO & EQ)](#3-transactional-function-types-ei-eo--eq)
   - 3.1 External Inputs (EI)
   - 3.2 External Outputs (EO)
   - 3.3 External Inquiries (EQ)
   - 3.4 Transaction Functions Complexity Matrix
4. [Unadjusted Function Point (UFP) Summary](#4-unadjusted-function-point-ufp-summary)
5. [General System Characteristics (GSC) & Value Adjustment Factor (VAF)](#5-general-system-characteristics-gsc--value-adjustment-factor-vaf)
   - 5.1 The 14 GSC Evaluation Criteria
   - 5.2 Degree of Influence (DI) Rating Justifications
   - 5.3 Calculation of TDI and VAF
6. [Final Adjusted Function Point (AFP) Computation](#6-final-adjusted-function-point-afp-computation)
7. [Software Effort, Cost & Schedule Estimation (COCOMO I & Empirical Benchmarks)](#7-software-effort-cost--schedule-estimation-cocomo-i--empirical-benchmarks)
   - 7.1 FP to SLOC Translation (Language Gear Ratio)
   - 7.2 Basic COCOMO Estimation Model
   - 7.3 Academic Minor Project Team Effort & Productivity Metrics

---

## 1. Introduction to Function Point Analysis

### 1.1 Objectives & Academic Significance
**Function Point Analysis (FPA)**, initially pioneered by Allan Albrecht at IBM and formalized by the International Function Point Users Group (IFPUG), is an industry-standard synthetic software metric used to quantify the functional size of a software application strictly from the user's operational perspective.

Unlike Source Lines of Code (SLOC), which varies drastically depending on the programming language, developer seniority, and styling conventions, Function Points provide a **technology-independent measure** of the business functionality delivered by the software. FPA enables:
1. Objective project size measurement prior to writing code.
2. Rigorous development effort, cost, and schedule estimations.
3. Cross-project productivity benchmarking ($FP / \text{Person-Month}$).
4. Normalization for software defect density analysis ($\text{Defects} / FP$).

### 1.2 IFPUG Architectural Foundations
The IFPUG measurement model decomposes software requirements into five fundamental components belonging to two broad categories:

```
                               ┌────────────────────────────────────────────────────────┐
                               │            TOTAL FUNCTIONAL SYSTEM BOUNDARY            │
                               └────────────────────────────────────────────────────────┘
                                      │                                          │
                    ┌─────────────────┴─────────────────┐      ┌─────────────────┴─────────────────┐
                    ▼                                   ▼      ▼                                   ▼
        ┌───────────────────────┐           ┌───────────────────────┐                 ┌───────────────────────┐
        │  DATA FUNCTION TYPES  │           │   EXTERNAL DATA FLOW  │                 │ TRANSACTION FUNCTIONS │
        └───────────────────────┘           └───────────────────────┘                 └───────────────────────┘
        │ • Internal Logical    │           │ • External Interface  │                 │ • External Inputs     │
        │   Files (ILF)         │           │   Files (EIF)         │                 │   (EI)                │
        │   [Maintained inside] │           │   [Referenced outside]│                 │ • External Outputs    │
        └───────────────────────┘           └───────────────────────┘                 │   (EO)                │
                                                                                      │ • External Inquiries  │
                                                                                      │   (EQ)                │
                                                                                      └───────────────────────┘
```

---

## 2. Data Function Types (ILF & EIF)

Data function types represent the static user data stored and accessed by the system.

### 2.1 Internal Logical Files (ILF)
An **Internal Logical File (ILF)** is a user-identifiable group of logically related data or control information maintained within the system boundary via one or more system processes.

The complexity of an ILF depends on:
- **RET (Record Element Type):** A user-recognizable subgroup of data elements within the file.
- **DET (Data Element Type):** A unique, user-recognizable, non-repeated field.

#### ILF Complexity Thresholds (IFPUG standard):
| RET \ DET | 1 to 19 DET | 20 to 50 DET | > 50 DET |
| :--- | :---: | :---: | :---: |
| **1 RET** | Low (7) | Low (7) | Average (10) |
| **2 to 5 RET** | Low (7) | Average (10) | High (15) |
| **> 5 RET** | Average (10) | High (15) | High (15) |

#### Inventory of System ILFs:
1. **`ILF-01: Books Inventory`**
   - *Description:* Core bibliographic catalog items and copy tracking.
   - *DETs (12):* `id`, `isbn`, `title`, `author`, `category`, `tier`, `publisher`, `publication_year`, `total_copies`, `available_copies`, `shelf_location`, `replacement_cost`.
   - *RETs (1):* Bibliographic Record.
   - *Complexity:* **Low (7 FP)**.

2. **`ILF-02: Members Directory`**
   - *Description:* Patron records across Student, Faculty, and Guest tiers.
   - *DETs (9):* `id`, `member_code`, `name`, `email`, `phone`, `member_type`, `status`, `max_books`, `loan_period_days`.
   - *RETs (1):* Member Profile.
   - *Complexity:* **Low (7 FP)**.

3. **`ILF-03: Borrow Records (Circulation Ledger)`**
   - *Description:* Active and historical checkouts, renewals, and returns.
   - *DETs (10):* `id`, `book_id`, `member_id`, `issue_date`, `due_date`, `return_date`, `renewals_count`, `status`, `return_condition`, `notes`.
   - *RETs (2):* Checkout Transaction Data, Check-In Return Inspection Data.
   - *Complexity:* **Low (7 FP)**.

4. **`ILF-04: Fines & Penalties Ledger`**
   - *Description:* Persisted fine assessments, fee breakdowns, and settlement history.
   - *DETs (13):* `id`, `borrow_record_id`, `member_id`, `days_overdue`, `base_rate`, `tier_multiplier`, `overdue_fine`, `damage_fine`, `replacement_fee`, `total_fine`, `rule_applied`, `paid_status`, `payment_method`.
   - *RETs (1):* Fine Invoice Record.
   - *Complexity:* **Low (7 FP)**.

5. **`ILF-05: Book Reservations (Hold Queue)`**
   - *Description:* Queued reservation requests for titles with zero available shelf copies.
   - *DETs (5):* `id`, `book_id`, `member_id`, `status`, `reserved_at`.
   - *RETs (1):* Reservation Queue Item.
   - *Complexity:* **Low (7 FP)**.

6. **`ILF-06: System Users & Credentials`**
   - *Description:* Staff credentials, roles, and administrative authorization tokens.
   - *DETs (6):* `user_id`, `username`, `password_hash`, `role`, `is_active`, `last_login`.
   - *RETs (1):* User Account.
   - *Complexity:* **Low (7 FP)**.

7. **`ILF-07: System Policy Settings`**
   - *Description:* Dynamic institutional runtime parameters for fines, caps, and loan durations.
   - *DETs (4):* `setting_id`, `setting_key`, `setting_value`, `description`.
   - *RETs (1):* Configuration Entry.
   - *Complexity:* **Low (7 FP)**.

### 2.2 External Interface Files (EIF)
An **External Interface File (EIF)** is a user-identifiable group of logically related data referenced by the system for informational purposes, but maintained entirely by another external system.

#### EIF Complexity Thresholds (IFPUG standard):
| RET \ DET | 1 to 19 DET | 20 to 50 DET | > 50 DET |
| :--- | :---: | :---: | :---: |
| **1 RET** | Low (5) | Low (5) | Average (7) |
| **2 to 5 RET** | Low (5) | Average (7) | High (10) |
| **> 5 RET** | Average (7) | High (10) | High (10) |

#### Inventory of System EIFs:
1. **`EIF-01: Campus Notification / SMS Gateway Interface`**
   - *Description:* External notification provider API referenced to format and dispatch overdue warnings and hold fulfillment notices.
   - *DETs (6):* `recipient_phone`, `recipient_email`, `message_payload`, `channel_type`, `dispatch_status`, `gateway_reference_id`.
   - *RETs (1):* Dispatch Request Object.
   - *Complexity:* **Low (5 FP)**.

2. **`EIF-02: Payment Gateway Interface (Card / Campus Wallet)`**
   - *Description:* External financial payment processor interface for settling library fines.
   - *DETs (8):* `merchant_id`, `order_token`, `transaction_amount`, `currency`, `card_last_four`, `payment_gateway_status`, `settlement_timestamp`, `auth_code`.
   - *RETs (2):* Authorization Header, Payment Transaction Payload.
   - *Complexity:* **Low (5 FP)**.

### 2.3 Data Functions Complexity Matrix

| Code | Functional File Name | Category | RET | DET | Complexity Rating | Weight (FP) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **ILF-01** | Books Inventory | ILF | 1 | 12 | Low | 7 |
| **ILF-02** | Members Directory | ILF | 1 | 9 | Low | 7 |
| **ILF-03** | Borrow Records | ILF | 2 | 10 | Low | 7 |
| **ILF-04** | Fines & Penalties Ledger | ILF | 1 | 13 | Low | 7 |
| **ILF-05** | Book Reservations | ILF | 1 | 5 | Low | 7 |
| **ILF-06** | System Users & Credentials | ILF | 1 | 6 | Low | 7 |
| **ILF-07** | System Policy Settings | ILF | 1 | 4 | Low | 7 |
| **EIF-01** | Campus Notification Interface | EIF | 1 | 6 | Low | 5 |
| **EIF-02** | Payment Gateway Interface | EIF | 2 | 8 | Low | 5 |
| **Subtotal**| **Data Functions Total** | | | | | **59 FP** |

---

## 3. Transactional Function Types (EI, EO & EQ)

### 3.1 External Inputs (EI)
An **External Input (EI)** processes data or control information originating from outside the application boundary to maintain one or more ILFs or alter system behavior.

#### EI Complexity Thresholds:
| FTR \ DET | 1 to 4 DET | 5 to 15 DET | > 15 DET |
| :--- | :---: | :---: | :---: |
| **0 to 1 FTR** | Low (3) | Low (3) | Average (4) |
| **2 FTR** | Low (3) | Average (4) | High (6) |
| **> 2 FTR** | Average (4) | High (6) | High (6) |

#### Inventory of External Inputs:
- **`EI-01: Ingest New Book`:** Add new catalog entry. FTR=1 (`books`), DET=11. $\implies$ **Low (3 FP)**.
- **`EI-02: Edit Book / Adjust Stock`:** Modify book metadata or inventory. FTR=1 (`books`), DET=10. $\implies$ **Low (3 FP)**.
- **`EI-03: Register New Member`:** Create patron profile. FTR=1 (`members`), DET=7. $\implies$ **Low (3 FP)**.
- **`EI-04: Update Member Standing`:** Modify member status / suspension. FTR=1 (`members`), DET=4. $\implies$ **Low (3 FP)**.
- **`EI-05: Issue Book Loan (Checkout)`:** Create checkout record, verify member eligibility, decrement copy count. FTR=3 (`books`, `members`, `borrow_records`), DET=6. $\implies$ **High (6 FP)**.
- **`EI-06: Return Book & Assess Condition`:** Process check-in, update copy status, trigger decision table fine calculation, update reservation hold. FTR=4 (`borrow_records`, `books`, `fines`, `reservations`), DET=7. $\implies$ **High (6 FP)**.
- **`EI-07: Renew Book Loan`:** Validate policy limits, extend due date. FTR=2 (`borrow_records`, `system_settings`), DET=4. $\implies$ **Low (3 FP)**.
- **`EI-08: Record Fine Settlement (Payment)`:** Record fee settlement, update cashier note, restore member status. FTR=2 (`fines`, `members`), DET=5. $\implies$ **Average (4 FP)**.
- **`EI-09: Waive Fine Administrative Action`:** Mark fine as waived with justification. FTR=2 (`fines`, `members`), DET=4. $\implies$ **Low (3 FP)**.
- **`EI-10: Place Book Hold (Reservation)`:** Queue hold request for unstocked item. FTR=3 (`reservations`, `books`, `members`), DET=4. $\implies$ **Average (4 FP)**.
- **`EI-11: Cancel Hold Request`:** Revoke hold and update queue. FTR=2 (`reservations`, `books`), DET=3. $\implies$ **Low (3 FP)**.
- **`EI-12: Update System Policy Settings`:** Dynamically alter fine rates and caps. FTR=1 (`system_settings`), DET=4. $\implies$ **Low (3 FP)**.

**EI Subtotal:** $3 + 3 + 3 + 3 + 6 + 6 + 3 + 4 + 3 + 4 + 3 + 3 = \mathbf{44\text{ FP}}$.

---

### 3.2 External Outputs (EO)
An **External Output (EO)** generates user-directed output containing derived or calculated data, maintaining internal control conditions or presenting processed information.

#### EO Complexity Thresholds:
| FTR \ DET | 1 to 5 DET | 6 to 19 DET | > 19 DET |
| :--- | :---: | :---: | :---: |
| **0 to 1 FTR** | Low (4) | Low (4) | Average (5) |
| **2 to 3 FTR** | Low (4) | Average (5) | High (7) |
| **> 3 FTR** | Average (5) | High (7) | High (7) |

#### Inventory of External Outputs:
- **`EO-01: Overdue Delinquency Summary Report`:** Scans loans, computes overdue days and estimated accrued fines, groups by department. FTR=3 (`borrow_records`, `members`, `books`), DET=10. $\implies$ **Average (5 FP)**.
- **`EO-02: Circulation Loan / Return Receipt`:** Generates printed/digital receipt with transaction ID, due date, condition assessment, and fine calculation breakdown. FTR=3 (`borrow_records`, `books`, `fines`), DET=9. $\implies$ **Average (5 FP)**.
- **`EO-03: Overdue Delinquency Notification Payload`:** Generates formatted overdue notification dispatch payload sent via external gateway. FTR=2 (`borrow_records`, `members`), DET=7. $\implies$ **Average (5 FP)**.
- **`EO-04: Circulation Analytics & Revenue Dashboard`:** Computes velocity rates, category distribution percentages, monthly loan charts, and fine revenue totals. FTR=4 (`borrow_records`, `books`, `fines`, `members`), DET=12. $\implies$ **High (7 FP)**.

**EO Subtotal:** $5 + 5 + 5 + 7 = \mathbf{22\text{ FP}}$.

---

### 3.3 External Inquiries (EQ)
An **External Inquiry (EQ)** retrieves static data from ILFs or EIFs and renders it to the user without altering system state or computing complex derived mathematical results.

#### EQ Complexity Thresholds:
| FTR \ DET | 1 to 5 DET | 6 to 19 DET | > 19 DET |
| :--- | :---: | :---: | :---: |
| **0 to 1 FTR** | Low (3) | Low (3) | Average (4) |
| **2 to 3 FTR** | Low (3) | Average (4) | High (6) |
| **> 3 FTR** | Average (4) | High (6) | High (6) |

#### Inventory of External Inquiries:
- **`EQ-01: Multi-Facet Catalog Search`:** Search collection by Title, Author, Category, or ISBN. FTR=1 (`books`), DET=8. $\implies$ **Low (3 FP)**.
- **`EQ-02: Member Profile & Loan History Query`:** Display member card, current active loans, and borrowing history. FTR=3 (`members`, `borrow_records`, `fines`), DET=12. $\implies$ **Average (4 FP)**.
- **`EQ-03: Outstanding Fine Balance Lookup`:** Patron or librarian inquiry on active unpaid invoices. FTR=2 (`fines`, `members`), DET=6. $\implies$ **Average (4 FP)**.
- **`EQ-04: Book Shelf Location & Real-Time Availability Check`:** Single-item lookup for physical shelf position and stock count. FTR=1 (`books`), DET=5. $\implies$ **Low (3 FP)**.
- **`EQ-05: Book Hold Queue Position Lookup`:** Check waiting list position for reserved title. FTR=2 (`reservations`, `books`), DET=4. $\implies$ **Low (3 FP)**.

**EQ Subtotal:** $3 + 4 + 4 + 3 + 3 = \mathbf{17\text{ FP}}$.

---

## 4. Unadjusted Function Point (UFP) Summary

Consolidating all five functional components yields the overall Unadjusted Function Point (UFP) count:

| Component Type | Count (Low) | Count (Average) | Count (High) | Weighting Matrix | Subtotal (FP) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Internal Logical Files (ILF)** | 7 | 0 | 0 | $7 \times 7$ | **49** |
| **External Interface Files (EIF)** | 2 | 0 | 0 | $2 \times 5$ | **10** |
| **External Inputs (EI)** | 8 | 2 | 2 | $(8 \times 3) + (2 \times 4) + (2 \times 6)$ | **44** |
| **External Outputs (EO)** | 0 | 3 | 1 | $(0 \times 4) + (3 \times 5) + (1 \times 7)$ | **22** |
| **External Inquiries (EQ)** | 3 | 2 | 0 | $(3 \times 3) + (2 \times 4) + (0 \times 6)$ | **17** |
| **Total Unadjusted Function Points (UFP)** | | | | | **142 UFP** |

---

## 5. General System Characteristics (GSC) & Value Adjustment Factor (VAF)

### 5.1 The 14 GSC Evaluation Criteria
The IFPUG model evaluates 14 General System Characteristics (GSCs) scored on a scale from **0 (No Influence)** to **5 (Strong / Critical Influence)** to adjust the functional size based on operational complexity:

$$\text{TDI} = \sum_{i=1}^{14} C_i \qquad (0 \le \text{TDI} \le 70)$$

$$\text{VAF} = 0.65 + (0.01 \times \text{TDI}) \qquad (0.65 \le \text{VAF} \le 1.35)$$

### 5.2 Degree of Influence (DI) Rating Justifications

| No. | General System Characteristic | Score (0–5) | Academic Engineering Justification |
| :---: | :--- | :---: | :--- |
| **1** | **Data Communications** | **3** | Operates over standard TCP/IP campus network via HTTP/HTTPS REST APIs and browser clients. |
| **2** | **Distributed Data Processing** | **2** | Client-server architecture; presentation executed on client browser, relational logic centralized on server. |
| **3** | **Performance Objectives** | **4** | Sub-500ms transaction latency required during peak student loan turnover periods. |
| **4** | **Heavily Used Configuration** | **3** | High transaction surges during semester starts and exam loan returns; server utilizes caching and connection pooling. |
| **5** | **Transaction Rate** | **3** | Continuous loan transactions, check-in scans, and catalog searches during 14 institutional operating hours. |
| **6** | **Online Data Entry** | **5** | 100% of circulation transactions, book registrations, and fee settlements occur through live online web forms. |
| **7** | **End-User Efficiency** | **4** | Designed for high desk throughput: barcode scanner auto-submit, modal receipts, and rapid single-click renewals. |
| **8** | **Online Update** | **4** | Real-time atomic database updates for inventory copies, loan statuses, and fine balances. |
| **9** | **Complex Processing** | **4** | Multi-parameter decision table fine calculation, grace period branching, damage penalties, and statutory caps. |
| **10**| **Reusability** | **3** | Cleanly architected service layer (`circulation_service`, `fine_engine`) reusable across web and headless CLI tools. |
| **11**| **Installation Ease** | **3** | Self-contained automated SQLite database initialization, automated table seeding, zero external daemon requirements. |
| **12**| **Operational Ease** | **4** | Automated overdue status transitions, receipt printing, and comprehensive error handling. |
| **13**| **Multiple Sites** | **2** | Designed for single institutional campus deployment with access across departmental library terminals. |
| **14**| **Facilitate Change** | **4** | Institutional policies (fine rates, grace periods, caps) dynamically configurable via `system_settings` table. |

### 5.3 Calculation of TDI and VAF

$$\text{Total Degree of Influence (TDI)} = 3 + 2 + 4 + 3 + 3 + 5 + 4 + 4 + 4 + 3 + 3 + 4 + 2 + 4 = \mathbf{48}$$

$$\text{Value Adjustment Factor (VAF)} = 0.65 + (0.01 \times 48) = 0.65 + 0.48 = \mathbf{1.13}$$

---

## 6. Final Adjusted Function Point (AFP) Computation

The final Adjusted Function Point (AFP) count is computed as:

$$\text{AFP} = \text{UFP} \times \text{VAF}$$

$$\text{AFP} = 142 \times 1.13 = \mathbf{160.46\text{ AFP}}$$

> **Summary:** The Library Management System delivers **160.46 Adjusted Function Points** of user-facing operational capability.

---

## 7. Software Effort, Cost & Schedule Estimation (COCOMO I & Empirical Benchmarks)

### 7.1 FP to SLOC Translation (Language Gear Ratio)
Industry empirical benchmarks compiled by QSM and Capers Jones establish standard language conversion ratios (Source Lines of Code per Function Point). For modern high-level languages:

| Language | Average SLOC / FP | Median SLOC / FP |
| :--- | :---: | :---: |
| Assembly | 320 | 300 |
| C | 128 | 120 |
| Java / C# | 55 | 53 |
| **Python 3 / Flask** | **50** | **48** |
| HTML5 / CSS3 / JavaScript | 45 | 42 |

Using the standard benchmark of **50 SLOC/FP** for Python web development:
$$\text{Estimated Application Size} = 160.46\text{ AFP} \times 50\text{ SLOC/FP} \approx \mathbf{8,023\text{ SLOC (8.02 KSLOC)}}$$

---

### 7.2 Basic COCOMO Estimation Model
Using Barry Boehm's **Basic COCOMO (Organic Mode)**, appropriate for small, stable in-house software teams with familiar requirements:

$$\text{Effort (Person-Months)} = a_b \times (\text{KSLOC})^{b_b}$$
$$\text{Development Time (Months)} = c_b \times (\text{Effort})^{d_b}$$

*Organic Coefficients:* $a_b = 2.4$, $b_b = 1.05$, $c_b = 2.5$, $d_b = 0.38$.

#### 1. Development Effort:
$$\text{Effort} = 2.4 \times (8.023)^{1.05} = 2.4 \times 8.948 \approx \mathbf{21.48\text{ Person-Months}}$$

#### 2. Nominal Development Schedule:
$$\text{Time}_{dev} = 2.5 \times (21.48)^{0.38} = 2.5 \times 3.208 \approx \mathbf{8.02\text{ Calendar Months}}$$

#### 3. Average Staffing Level:
$$\text{Average Staff} = \frac{\text{Effort}}{\text{Time}_{dev}} = \frac{21.48}{8.02} \approx \mathbf{2.68\text{ Engineers}} \approx \mathbf{3\text{ to 4 Persons}}$$

---

### 7.3 Academic Minor Project Team Effort & Productivity Metrics
In the context of the **Academic Minor Project (4-Member Student Team)** working over a structured **10-week semester timeline**:

| Metric Parameter | Formula / Input | Academic Value |
| :--- | :--- | :--- |
| **Team Size** | 4 members (PM/Analyst, Designer, Developer, Tester) | 4 students |
| **Semester Duration** | Iterative Waterfall timeline | 10 academic weeks |
| **Commitment per Member** | 8 productive hours per week | 8 hours / week |
| **Total Available Team Effort** | $4 \text{ members} \times 8 \text{ hrs/wk} \times 10 \text{ wks}$ | **320 Person-Hours** |
| **Academic Productivity Rate** | $\text{AFP} / \text{Person-Hour} = 160.46 / 320$ | **0.50 FP / Hour** |
| **Effort Distribution by Phase** | Requirements & SRS (20%) | 64 Person-Hours |
| | Architecture & DFD (20%) | 64 Person-Hours |
| | Coding & Decision Table (35%) | 112 Person-Hours |
| | Testing & Verification (15%) | 48 Person-Hours |
| | SPMP, Manuals & Viva Prep (10%) | 32 Person-Hours |

This analysis confirms that the Library Management System scope of **160.46 Function Points** is appropriately sized, mathematically sound, and rigorously achievable within the university minor project curriculum.
