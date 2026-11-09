# Formal Decision Table for Fine & Penalty Calculations
## Library Management System (LMS)
**Document Type:** Formal Specification & Algorithmic Logic Dossier  
**Project Special Syllabus Focus:** Decision Table for Fines Calculation  
**Standard:** ISO/IEC/IEEE 29119 Software Testing & Structured Logic Specification  
**Version:** 1.0.0  
**Date:** November 2026  

---

## Table of Contents
1. [Executive Summary & Theoretical Foundations](#1-executive-summary--theoretical-foundations)
   - 1.1 Decision Table Architecture in Software Engineering
   - 1.2 Mathematical Formulation of the Fine Function
2. [Condition Stubs (Input Domain Specifications)](#2-condition-stubs-input-domain-specifications)
   - 2.1 C1: Member Category
   - 2.2 C2: Days Overdue (Equivalence Partitions)
   - 2.3 C3: Book Inventory Category / Tier
   - 2.4 C4: Physical Condition of Book on Return
   - 2.5 C5: Prior Default History / Repeated Overdues
3. [Action Stubs (Output Domain Specifications)](#3-action-stubs-output-domain-specifications)
   - 3.1 A1: Base Daily Overdue Rate
   - 3.2 A2: Book Category Tier Multiplier
   - 3.3 A3: Physical Damage / Replacement Penalty
   - 3.4 A4: Member Account Status Action
   - 3.5 A5: Statutory Fine Cap Enforcement
4. [Combinatorial Analysis & Rule Reduction](#4-combinatorial-analysis--rule-reduction)
   - 4.1 Cartesian Expansion
   - 4.2 Equivalence Partitioning & Indifference Rules
5. [Master Consolidated Decision Table (Rules R1 to R16)](#5-master-consolidated-decision-table-rules-r1-to-r16)
6. [Worked Numerical Calculations & Walkthroughs (R1 to R16)](#6-worked-numerical-calculations--walkthroughs-r1-to-r16)
7. [Boundary Value Analysis (BVA) & Equivalence Partitioning Test Suite](#7-boundary-value-analysis-bva--equivalence-partitioning-test-suite)
8. [Algorithmic Implementation in Python](#8-algorithmic-implementation-in-python)

---

## 1. Executive Summary & Theoretical Foundations

### 1.1 Decision Table Architecture in Software Engineering
A **Decision Table** is a rigorous formal technique used in software engineering to model, specify, and test complex combinational business logic where system behaviors depend on multiple intersecting conditions. Compared to unwieldy nested conditional statements (`if-else if-else`), decision tables offer four decisive advantages:
1. **Completeness:** Verifies that every possible permutation of input conditions has an explicitly defined outcome.
2. **Consistency:** Guarantees that conflicting or contradictory requirements cannot coexist unnoticed.
3. **Traceability:** Maps business policy clauses directly to automated black-box test vectors.
4. **Maintainability:** Permits policy updates (such as fine rate revisions) without destabilizing underlying control flow.

A standard decision table is divided into four distinct quadrants:
```
┌──────────────────────────────────────┬──────────────────────────────────────┐
│           CONDITION STUB             │          CONDITION ENTRIES           │
│  (List of input criteria/predicates) │    (Combinations of domain values)   │
├──────────────────────────────────────┼──────────────────────────────────────┤
│            ACTION STUB               │            ACTION ENTRIES            │
│  (List of system responses/outputs)  │     (Execution flags: X, -, or val)  │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 1.2 Mathematical Formulation of the Fine Function
The total assessment fee $F_{total}$ evaluated upon book return is formulated as a piecewise multivariate function:

$$F_{total} = f(C_1, C_2, C_3, C_4, C_5)$$

Where:
$$F_{total} = 
\begin{cases} 
\text{Cost}_{replacement} + \text{Fee}_{admin} & \text{if } C_4 = \text{Lost} \\
\min\left(F_{overdue}, \text{Cap}(C_1)\right) + F_{damage}(C_4) & \text{otherwise}
\end{cases}$$

The intermediate overdue fine component $F_{overdue}$ is calculated as:
$$F_{overdue} = 
\begin{cases} 
0 & \text{if } D \le 2 \text{ (Grace Period)} \\
D \times \text{Rate}_{base}(C_1) \times \text{Multiplier}_{tier}(C_3) \times \text{Surcharge}(C_5) & \text{if } D > 2 
\end{cases}$$

Where:
- $D = \max(0, \text{ReturnDate} - \text{DueDate})$
- $\text{Surcharge}(C_5) = 1.20$ if $C_5 = \text{Yes and } D \ge 8$; otherwise $1.00$.

---

## 2. Condition Stubs (Input Domain Specifications)

### 2.1 C1: Member Category
Institutional borrowing policies differentiate between student patrons, faculty members, and external guests based on their institutional affiliation and security deposits:
- **`Student`:** Standard enrolled scholar; high inventory velocity; base daily rate $\$0.50$; statutory overdue cap $\$20.00$.
- **`Faculty`:** Academic teaching and research staff; research loan privileges; base daily rate $\$0.20$; statutory overdue cap $\$30.00$.
- **`Guest`:** External or temporary borrower; base daily rate $\$1.00$; statutory overdue cap $\$50.00$.

### 2.2 C2: Days Overdue ($D \ge 0$)
The overdue duration $D$ is partitioned into four mutually exclusive operational tiers:
- **Tier 0 (Grace Period: $0 \le D \le 2$):** Statutory courtesy buffer. Borrowers returning within 48 hours of due date incur $\$0.00$ overdue penalty.
- **Tier 1 (Short Overdue: $3 \le D \le 7$):** Routine overdue. Standard base rate applies with tier multiplier.
- **Tier 2 (Moderate Overdue: $8 \le D \le 21$):** Persistent overdue. Account flagged with formal institutional warning; default surcharge triggers if repeated defaulter.
- **Tier 3 (Severe Delinquency: $D > 21$):** Immediate borrowing suspension; account blocked; statutory fine cap saturated.

### 2.3 C3: Book Inventory Category / Tier
Circulation items are stratified by demand and rarity:
- **`Standard` (Multiplier: $1.0\times$):** General circulation collection (novels, standard monographs, general literature).
- **`Course Reserve` (Multiplier: $2.0\times$):** High-demand course textbooks, syllabi reference books, and reserve shelf items with 3-day max loan windows.
- **`Rare/Reference` (Multiplier: $3.0\times$):** Archival volumes, primary reference sets, limited editions, and non-circulating research treatises.

### 2.4 C4: Physical Condition of Book on Return
Physical item inspection takes place at the desk upon check-in:
- **`Normal`:** Acceptable wear and tear. Zero penalty ($\$0.00$).
- **`Minor Damage`:** Marginal physical defects (pencil/highlighter markings, dog-eared pages, soiled cover). Penalty: Flat **$\$5.00$**.
- **`Severe Damage`:** Substantial physical mutilation (broken binding, torn spine, liquid damage, missing pages). Penalty: Flat **$\$15.00$**.
- **`Lost`:** Item unreturned, destroyed beyond repair, or reported lost by patron. Penalty: **Full Replacement Cost of Book + $\$10.00$ Administrative Processing Fee**. (Overdue daily fees are waived and converted to replacement charge).

### 2.5 C5: Prior Default History / Repeated Overdues
Borrower credit record tracked over the academic semester:
- **`No` (Clean Standing):** Zero prior overdue occurrences; standard fine schedule.
- **`Yes` (Repeat Defaulter):** Patron has had 2 or more overdue occurrences in the current semester. A **20% punitive surcharge** is appended to overdue charges if overdue duration reaches Tier 2 ($D \ge 8$).

---

## 3. Action Stubs (Output Domain Specifications)

### 3.1 A1: Base Daily Overdue Rate Applied
- **`$0.00`:** Applied during Grace Period ($D \le 2$) or Lost book status.
- **`$0.50`:** Standard Student base daily rate.
- **`$0.20`:** Concessionary Faculty base daily rate.
- **`$1.00`:** Full Guest base daily rate.

### 3.2 A2: Book Category Tier Multiplier
- **`1.0x`:** Standard general collection multiplier.
- **`2.0x`:** Course Reserve high-demand multiplier.
- **`3.0x`:** Rare/Reference collection multiplier.

### 3.3 A3: Physical Damage / Replacement Penalty Assessed
- **`$0.00`:** Book returned in Normal condition.
- **`$5.00`:** Minor damage surcharge added to invoice.
- **`$15.00`:** Severe damage surcharge added to invoice.
- **`Replacement Cost + $10.00 Fee`:** Invoiced for unrecoverable/lost items.

### 3.4 A4: Member Account Status Action
- **`Normal`:** Account remains active; borrower may check out subsequent titles.
- **`Warning`:** Delinquency notification issued via email/portal; borrowing permitted if fines under threshold.
- **`Suspended`:** Borrowing privileges immediately revoked; account locked until invoice is paid in full.

### 3.5 A5: Statutory Fine Cap Applied
- **`Max $20.00`:** Hard ceiling for Student overdue fines.
- **`Max $30.00`:** Hard ceiling for Faculty overdue fines.
- **`Max $50.00`:** Hard ceiling for Guest overdue fines.
- **`Uncapped (N/A)`:** Replacement fees and administrative surcharges are never subject to overdue caps.

---

## 4. Combinatorial Analysis & Rule Reduction

### 4.1 Cartesian Expansion
The total possible combinations of all conditions equals:
$$N = |C_1| \times |C_2| \times |C_3| \times |C_4| \times |C_5| = 3 \times 4 \times 3 \times 4 \times 2 = 288 \text{ theoretical rules}$$

### 4.2 Equivalence Partitioning & Indifference Rules
In formal software engineering, 288 rules contain substantial redundancy. Using **Indifference Analysis** (where specific condition combinations produce identical actions regardless of other values), we compress the space into **16 canonical, non-overlapping rules (R1 to R16)** that completely cover the operational domain:
1. **Lost Item Principle (Indifference to C2, C3, C5):** When $C_4 = \text{Lost}$, overdue daily calculation is bypassed in favor of full replacement cost + administrative fee.
2. **Grace Period Principle (Indifference to C3, C5):** When $C_2 = \text{Grace } (0 \le D \le 2)$, base overdue fee is $\$0.00$, irrespective of book tier or repeat defaulter history.
3. **Severe Delinquency Principle ($D > 21$):** Regardless of member type, any item overdue for more than 21 days results in automatic account suspension and overdue cap activation.

---

## 5. Master Consolidated Decision Table (Rules R1 to R16)

The following table specifies all 16 canonical business logic rules governing library circulation returns:

| Stubs | Rule Elements | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 | R12 | R13 | R14 | R15 | R16 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | Member Category | Stu | Stu | Stu | Stu | Stu | Stu | Fac | Fac | Fac | Fac | Gst | Gst | Gst | Any | Any | Any |
| **C2** | Days Overdue ($D$) | 0-2 | 3-7 | 3-7 | 8-21 | 8-21 | >21 | 0-2 | 3-7 | 8-21 | >21 | 0-2 | 3-7 | 8-21 | >21 | Any | Any |
| **C3** | Book Tier | Std | Std | Res | Std | Res | Any | Any | Res | Ref | Std | Std | Std | Ref | Any | Any | Any |
| **C4** | Physical Condition | Norm | Norm | Norm | MinD | SevD | Norm | Norm | Norm | MinD | Norm | Norm | SevD | Norm | Any | Lost | Lost |
| **C5** | Repeat Defaulter | No | No | No | No | Yes | No | No | No | Yes | No | No | No | Yes | Any | No | Yes |
| **A1** | Base Daily Rate | $0.00 | $0.50 | $0.50 | $0.50 | $0.50 | $0.50 | $0.00 | $0.20 | $0.20 | $0.20 | $0.00 | $1.00 | $1.00 | Rate | $0.00 | $0.00 |
| **A2** | Tier Multiplier | 1x | 1x | 2x | 1x | 2x | 1x | 1x | 2x | 3x | 1x | 1x | 1x | 3x | Multi | N/A | N/A |
| **A3** | Damage Penalty | $0 | $0 | $0 | $5 | $15 | $0 | $0 | $0 | $5 | $0 | $0 | $15 | $0 | Cond | Rep+$10 | Rep+$10 |
| **A4** | Account Status Action | Norm | Norm | Warn | Warn | Susp | Susp | Norm | Norm | Warn | Susp | Norm | Susp | Susp | Susp | Susp | Susp |
| **A5** | Fine Cap Applied | $20 | $20 | $20 | $20 | $20 | $20 | $30 | $30 | $30 | $30 | $50 | $50 | $50 | Cap | None | None |

*Legend:*  
- **Stu:** Student | **Fac:** Faculty | **Gst:** Guest  
- **Std:** Standard (1x) | **Res:** Course Reserve (2x) | **Ref:** Rare/Reference (3x)  
- **Norm:** Normal ($0) | **MinD:** Minor Damage ($5) | **SevD:** Severe Damage ($15) | **Lost:** Replacement Cost + $10 Fee  
- **Rep+$10:** Full book replacement cost + $10 administrative fee  
- **Norm / Warn / Susp:** Normal (Active) / Warning Notice / Borrowing Suspended  

---

## 6. Worked Numerical Calculations & Walkthroughs (R1 to R16)

To ensure zero ambiguity during coding and testing, the following section provides concrete, step-by-step arithmetic traces for every rule in the master decision table.

---

### Rule R1: Student — Grace Period Return
- **Scenario:** Student returns a Standard book 2 days late in perfect condition. No prior defaults.
- **Inputs:** $C_1 = \text{Student}$, $D = 2$, $C_3 = \text{Standard}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - $D \le 2 \implies \text{Grace Period activated}$.
  - Overdue Fine $F_{overdue} = \$0.00$.
  - Damage Fine $F_{damage} = \$0.00$.
  - Total Fine $F_{total} = \$0.00 + \$0.00 = \mathbf{\$0.00}$.
- **Account Action:** Status remains `Normal`. No warning issued.

---

### Rule R2: Student — Tier 1 Overdue (Standard Book)
- **Scenario:** Student returns a Standard book 5 days late in normal condition.
- **Inputs:** $C_1 = \text{Student}$, $D = 5$, $C_3 = \text{Standard}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - $D = 5$ (Tier 1: $3 \le D \le 7$). Base rate $= \$0.50$, Multiplier $= 1.0\times$.
  - $F_{overdue} = 5 \times \$0.50 \times 1.0 = \$2.50$.
  - Cap check: $\min(\$2.50, \$20.00) = \$2.50$.
  - Damage Fine $F_{damage} = \$0.00$.
  - Total Fine $F_{total} = \$2.50 + \$0.00 = \mathbf{\$2.50}$.
- **Account Action:** Status remains `Normal`. Receipt generated.

---

### Rule R3: Student — Tier 1 Overdue (Course Reserve Book)
- **Scenario:** Student returns high-demand Course Reserve book 4 days late in normal condition.
- **Inputs:** $C_1 = \text{Student}$, $D = 4$, $C_3 = \text{Course Reserve}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - $D = 4$. Base rate $= \$0.50$, Course Reserve Multiplier $= 2.0\times$.
  - $F_{overdue} = 4 \times \$0.50 \times 2.0 = \$4.00$.
  - Cap check: $\min(\$4.00, \$20.00) = \$4.00$.
  - Total Fine $F_{total} = \mathbf{\$4.00}$.
- **Account Action:** Status flagged with `Warning` (due to high-demand reserve holding delay).

---

### Rule R4: Student — Tier 2 Overdue with Minor Damage
- **Scenario:** Student returns Standard book 10 days late with torn and dog-eared pages.
- **Inputs:** $C_1 = \text{Student}$, $D = 10$, $C_3 = \text{Standard}$, $C_4 = \text{Minor Damage}$, $C_5 = \text{No}$.
- **Calculation:**
  - $D = 10$ (Tier 2: $8 \le D \le 21$). Base rate $= \$0.50$, Multiplier $= 1.0\times$.
  - $F_{overdue} = 10 \times \$0.50 \times 1.0 = \$5.00$.
  - Cap check: $\min(\$5.00, \$20.00) = \$5.00$.
  - Damage Penalty $F_{damage} = \$5.00$ (Minor Damage schedule).
  - Total Fine $F_{total} = \$5.00 + \$5.00 = \mathbf{\$10.00}$.
- **Account Action:** Account issued `Warning`. Borrowing held until $\$10.00$ is cleared.

---

### Rule R5: Student — Tier 2 Overdue + Course Reserve + Severe Damage + Repeat Defaulter
- **Scenario:** Chronic defaulter student returns Course Reserve textbook 15 days late with broken spine and missing pages.
- **Inputs:** $C_1 = \text{Student}$, $D = 15$, $C_3 = \text{Course Reserve}$, $C_4 = \text{Severe Damage}$, $C_5 = \text{Yes}$.
- **Calculation:**
  - $D = 15$. Base rate $= \$0.50$, Multiplier $= 2.0\times$.
  - Subtotal overdue $= 15 \times \$0.50 \times 2.0 = \$15.00$.
  - Repeat Defaulter Surcharge in Tier 2 ($+20\%$):
    $$F_{overdue} = \$15.00 \times 1.20 = \$18.00$$
  - Cap check: $\min(\$18.00, \$20.00) = \$18.00$.
  - Severe Damage Penalty: $F_{damage} = \$15.00$.
  - Total Fine $F_{total} = \$18.00 + \$15.00 = \mathbf{\$33.00}$.
- **Account Action:** Immediate borrowing `Suspended`. Mandatory referral to Head Librarian.

---

### Rule R6: Student — Tier 3 Severe Delinquency (Fine Cap Enforced)
- **Scenario:** Student returns book 55 days overdue in clean condition.
- **Inputs:** $C_1 = \text{Student}$, $D = 55$, $C_3 = \text{Standard}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - Theoretical overdue charge $= 55 \times \$0.50 \times 1.0 = \$27.50$.
  - Statutory Student Fine Cap $= \$20.00$.
  - Capped Overdue Fine $= \min(\$27.50, \$20.00) = \mathbf{\$20.00}$.
  - Damage Fine $= \$0.00$.
  - Total Fine $F_{total} = \mathbf{\$20.00}$.
- **Account Action:** Immediate `Suspended` status due to delinquency exceeding 21 days.

---

### Rule R7: Faculty — Grace Period Return
- **Scenario:** Faculty member returns research monograph 1 day after the 30-day term.
- **Inputs:** $C_1 = \text{Faculty}$, $D = 1$, $C_3 = \text{Standard}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - $D \le 2 \implies \text{Grace Period activated}$.
  - Total Fine $F_{total} = \mathbf{\$0.00}$.
- **Account Action:** Account status `Normal`.

---

### Rule R8: Faculty — Tier 1 Overdue (Course Reserve)
- **Scenario:** Faculty member retains reserve teaching manual 6 days late.
- **Inputs:** $C_1 = \text{Faculty}$, $D = 6$, $C_3 = \text{Course Reserve}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - $D = 6$. Base rate $= \$0.20$, Multiplier $= 2.0\times$.
  - Overdue Fine $= 6 \times \$0.20 \times 2.0 = \mathbf{\$2.40}$.
  - Cap check: $\min(\$2.40, \$30.00) = \$2.40$.
  - Total Fine $F_{total} = \mathbf{\$2.40}$.
- **Account Action:** Account status `Normal`. Courtesy email notice.

---

### Rule R9: Faculty — Tier 2 Overdue (Rare/Reference) + Minor Damage + Repeat Defaulter
- **Scenario:** Faculty member returns rare archive reference 12 days late with marginal ink annotation; has prior overdue history.
- **Inputs:** $C_1 = \text{Faculty}$, $D = 12$, $C_3 = \text{Rare/Reference}$, $C_4 = \text{Minor Damage}$, $C_5 = \text{Yes}$.
- **Calculation:**
  - $D = 12$. Base rate $= \$0.20$, Rare/Ref Multiplier $= 3.0\times$.
  - Subtotal overdue $= 12 \times \$0.20 \times 3.0 = \$7.20$.
  - Repeat Defaulter surcharge in Tier 2 ($+20\%$):
    $$F_{overdue} = \$7.20 \times 1.20 = \$8.64$$
  - Cap check: $\min(\$8.64, \$30.00) = \$8.64$.
  - Damage Penalty $F_{damage} = \$5.00$ (Minor Damage).
  - Total Fine $F_{total} = \$8.64 + \$5.00 = \mathbf{\$13.64}$.
- **Account Action:** Account issued `Warning`.

---

### Rule R10: Faculty — Tier 3 Severe Delinquency (Fine Cap Enforced)
- **Scenario:** Faculty member returns rare archive volume 70 days overdue in normal condition.
- **Inputs:** $C_1 = \text{Faculty}$, $D = 70$, $C_3 = \text{Rare/Reference}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - Theoretical overdue $= 70 \times \$0.20 \times 3.0 = \$42.00$.
  - Statutory Faculty Fine Cap $= \$30.00$.
  - Capped Overdue Fine $= \min(\$42.00, \$30.00) = \mathbf{\$30.00}$.
  - Total Fine $F_{total} = \mathbf{\$30.00}$.
- **Account Action:** Account borrowing privileges `Suspended` ($D > 21$).

---

### Rule R11: Guest — Grace Period Return
- **Scenario:** External visiting guest scholar returns general collection item 2 days overdue.
- **Inputs:** $C_1 = \text{Guest}$, $D = 2$, $C_3 = \text{Standard}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - $D \le 2 \implies \text{Grace Period activated}$.
  - Total Fine $F_{total} = \mathbf{\$0.00}$.
- **Account Action:** Account status `Normal`.

---

### Rule R12: Guest — Tier 1 Overdue with Severe Damage
- **Scenario:** Guest returns book 5 days overdue with severe water damage and binding separation.
- **Inputs:** $C_1 = \text{Guest}$, $D = 5$, $C_3 = \text{Standard}$, $C_4 = \text{Severe Damage}$, $C_5 = \text{No}$.
- **Calculation:**
  - $D = 5$. Base rate $= \$1.00$, Multiplier $= 1.0\times$.
  - $F_{overdue} = 5 \times \$1.00 \times 1.0 = \$5.00$.
  - Damage Penalty $F_{damage} = \$15.00$ (Severe Damage).
  - Total Fine $F_{total} = \$5.00 + \$15.00 = \mathbf{\$20.00}$.
- **Account Action:** Account `Suspended` due to severe damage assessment pending payment.

---

### Rule R13: Guest — Tier 2 Overdue (Rare/Reference) + Repeat Defaulter
- **Scenario:** Visiting researcher returns reference folio 10 days late; has repeated past overdue infractions.
- **Inputs:** $C_1 = \text{Guest}$, $D = 10$, $C_3 = \text{Rare/Reference}$, $C_4 = \text{Normal}$, $C_5 = \text{Yes}$.
- **Calculation:**
  - $D = 10$. Base rate $= \$1.00$, Rare/Ref Multiplier $= 3.0\times$.
  - Subtotal overdue $= 10 \times \$1.00 \times 3.0 = \$30.00$.
  - Repeat Defaulter Surcharge in Tier 2 ($+20\%$):
    $$F_{overdue} = \$30.00 \times 1.20 = \$36.00$$
  - Cap check: $\min(\$36.00, \$50.00) = \$36.00$.
  - Damage Penalty $F_{damage} = \$0.00$.
  - Total Fine $F_{total} = \mathbf{\$36.00}$.
- **Account Action:** Account immediately `Suspended`. Security deposit attached.

---

### Rule R14: Guest — Tier 3 Severe Delinquency (Fine Cap Enforced)
- **Scenario:** Guest returns book 60 days overdue in normal condition.
- **Inputs:** $C_1 = \text{Guest}$, $D = 60$, $C_3 = \text{Standard}$, $C_4 = \text{Normal}$, $C_5 = \text{No}$.
- **Calculation:**
  - Theoretical overdue $= 60 \times \$1.00 \times 1.0 = \$60.00$.
  - Statutory Guest Fine Cap $= \$50.00$.
  - Capped Overdue Fine $= \min(\$60.00, \$50.00) = \mathbf{\$50.00}$.
  - Total Fine $F_{total} = \mathbf{\$50.00}$.
- **Account Action:** Account `Suspended`. Library access badge deactivated.

---

### Rule R15: Any Member — Lost Book (Clean Standing)
- **Scenario:** Student patron admits losing a textbook whose replacement cost in catalog is $\$45.00$.
- **Inputs:** $C_1 = \text{Student}$, $D = 14$, $C_3 = \text{Standard}$, $C_4 = \text{Lost}$, $C_5 = \text{No}$.
- **Calculation:**
  - $C_4 = \text{Lost} \implies$ Overdue daily calculation is superseded.
  - Replacement Cost $= \$45.00$.
  - Administrative Processing Fee $= \$10.00$.
  - Overdue Cap Applicability: **Uncapped** (Caps do not apply to lost book replacement).
  - Total Fine $F_{total} = \$45.00 + \$10.00 = \mathbf{\$55.00}$.
- **Account Action:** Account `Suspended` until replacement cost is settled; inventory copy marked as Lost.

---

### Rule R16: Any Member — Lost Book + Repeat Defaulter
- **Scenario:** Defaulter faculty member reports a rare reference book (replacement cost $\$120.00$) as lost.
- **Inputs:** $C_1 = \text{Faculty}$, $D = 30$, $C_3 = \text{Rare/Reference}$, $C_4 = \text{Lost}$, $C_5 = \text{Yes}$.
- **Calculation:**
  - $C_4 = \text{Lost} \implies$ Replacement fee schedule applies.
  - Replacement Cost $= \$120.00$.
  - Administrative Fee $= \$10.00$.
  - Repeat defaulter lost penalty: Additional institutional review flagged.
  - Total Fine $F_{total} = \$120.00 + \$10.00 = \mathbf{\$130.00}$.
- **Account Action:** Account immediately `Suspended`; dean of faculty notified.

---

## 7. Boundary Value Analysis (BVA) & Equivalence Partitioning Test Suite

In accordance with IEEE 29119 testing standards, the following boundary test vectors verify that edge transitions around grace periods, overdue tier transitions, and statutory cap limits are strictly respected:

| Test ID | Condition Tested | Member Type | Days Overdue ($D$) | Book Tier | Condition | Repeat? | Expected Overdue ($) | Expected Total ($) | Verification Rule |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **BVA-01** | Due date today | Student | 0 | Standard | Normal | No | $0.00 | $0.00 | R1 (Grace lower bound) |
| **BVA-02** | Grace upper limit | Student | 2 | Course Reserve| Normal | No | $0.00 | $0.00 | R1 (Grace upper bound) |
| **BVA-03** | Tier 1 entry boundary | Student | 3 | Standard | Normal | No | $1.50 | $1.50 | R2 ($3 \times 0.50 \times 1$) |
| **BVA-04** | Tier 1 upper boundary | Student | 7 | Course Reserve| Normal | No | $7.00 | $7.00 | R3 ($7 \times 0.50 \times 2$) |
| **BVA-05** | Tier 2 entry boundary | Student | 8 | Standard | Normal | Yes | $4.80 | $4.80 | R4 ($8 \times 0.50 \times 1 \times 1.2$) |
| **BVA-06** | Student cap exactly reached| Student | 40 | Standard | Normal | No | $20.00 | $20.00 | R6 (Exact cap saturation) |
| **BVA-07** | Student cap boundary - 1 | Student | 39 | Standard | Normal | No | $19.50 | $19.50 | R2 ($39 \times 0.50$) |
| **BVA-08** | Student cap exceeded | Student | 41 | Standard | Normal | No | $20.00 | $20.00 | R6 (Hard ceiling clamp) |
| **BVA-09** | Faculty cap reached | Faculty | 150 | Standard | Normal | No | $30.00 | $30.00 | R10 ($150 \times 0.20 \to \$30$) |
| **BVA-10** | Tier 3 suspension threshold | Guest | 22 | Standard | Normal | No | $22.00 | $22.00 | R14 (Suspension trigger) |
| **BVA-11** | Lost book unencumbered | Student | 100 | Standard | Lost ($50)| No | $0.00 | $60.00 | R15 ($50 cost + $10 fee) |

---

## 8. Algorithmic Implementation in Python

The business rules established above are directly implemented in production as a deterministic, pure function:

```python
"""
Decision-Table-Driven Fine & Penalty Calculation Engine
Adhering to IEEE 830 and LMS Specification v1.0.0
"""
from typing import Dict, Any

def calculate_fine(
    member_type: str,
    days_overdue: int,
    book_tier: str = 'Standard',
    condition: str = 'Normal',
    repeat_defaulter: bool = False,
    replacement_cost: float = 50.0
) -> Dict[str, Any]:
    """
    Executes the 16-Rule Decision Table to assess library circulation fines.
    
    Returns:
        dict containing:
            - base_rate (float)
            - tier_multiplier (float)
            - overdue_fine (float)
            - damage_fine (float)
            - replacement_fee (float)
            - total_fine (float)
            - rule_applied (str)
            - account_action (str)
    """
    days_overdue = max(0, days_overdue)
    
    # Policy Parameter Dictionaries
    BASE_RATES = {'Student': 0.50, 'Faculty': 0.20, 'Guest': 1.00}
    FINE_CAPS = {'Student': 20.00, 'Faculty': 30.00, 'Guest': 50.00}
    TIER_MULTIPLIERS = {'Standard': 1.0, 'Course Reserve': 2.0, 'Rare/Reference': 3.0}
    DAMAGE_FEES = {'Normal': 0.0, 'Minor Damage': 5.0, 'Severe Damage': 15.0}
    ADMIN_LOST_FEE = 10.00

    base_rate = BASE_RATES.get(member_type, 0.50)
    tier_multiplier = TIER_MULTIPLIERS.get(book_tier, 1.0)
    fine_cap = FINE_CAPS.get(member_type, 20.00)

    # 1. Condition C4: Lost Book Rule Handling (Rules R15 & R16)
    if condition == 'Lost':
        total_fine = round(replacement_cost + ADMIN_LOST_FEE, 2)
        rule = 'Rule R16: Lost Book (Repeat Defaulter)' if repeat_defaulter else 'Rule R15: Lost Book Assessment'
        return {
            'base_rate': 0.0,
            'tier_multiplier': 1.0,
            'overdue_fine': 0.0,
            'damage_fine': 0.0,
            'replacement_fee': total_fine,
            'total_fine': total_fine,
            'rule_applied': rule,
            'account_action': 'Suspended'
        }

    # 2. Condition C2: Grace Period (0 <= D <= 2) (Rules R1, R7, R11)
    if days_overdue <= 2:
        damage_fine = DAMAGE_FEES.get(condition, 0.0)
        account_action = 'Suspended' if condition == 'Severe Damage' else 'Normal'
        rule_num = 'R1' if member_type == 'Student' else ('R7' if member_type == 'Faculty' else 'R11')
        return {
            'base_rate': 0.0,
            'tier_multiplier': tier_multiplier,
            'overdue_fine': 0.0,
            'damage_fine': damage_fine,
            'replacement_fee': 0.0,
            'total_fine': damage_fine,
            'rule_applied': f"Rule {rule_num}: Grace Period Return ({member_type})",
            'account_action': account_action
        }

    # 3. Calculate Overdue Fine with Multipliers and Defaulter Surcharge
    raw_overdue = days_overdue * base_rate * tier_multiplier
    
    # Repeat defaulter + Tier 2 (D >= 8) -> 20% surcharge
    if repeat_defaulter and days_overdue >= 8:
        raw_overdue *= 1.20

    # 4. Enforce Statutory Overdue Cap
    capped_overdue = round(min(raw_overdue, fine_cap), 2)
    damage_fine = DAMAGE_FEES.get(condition, 0.0)
    total_fine = round(capped_overdue + damage_fine, 2)

    # 5. Determine Account Action & Specific Rule Mapping
    if days_overdue > 21 or condition == 'Severe Damage' or total_fine >= fine_cap:
        account_action = 'Suspended'
    elif days_overdue >= 8 or condition == 'Minor Damage' or book_tier == 'Course Reserve':
        account_action = 'Warning'
    else:
        account_action = 'Normal'

    # Synthesize Applied Rule Label
    if days_overdue > 21:
        rule_applied = f"Rule R6/R10/R14: Delinquency Cap Reached ({member_type})"
    elif repeat_defaulter and days_overdue >= 8:
        rule_applied = f"Rule R5/R9/R13: Defaulter Surcharge ({member_type})"
    elif damage_fine > 0:
        rule_applied = f"Rule R4/R12: Overdue + {condition} Assessment"
    elif book_tier == 'Course Reserve':
        rule_applied = f"Rule R3/R8: Course Reserve Tier 1 ({member_type})"
    else:
        rule_applied = f"Rule R2: Standard Tier 1 ({member_type})"

    return {
        'base_rate': base_rate,
        'tier_multiplier': tier_multiplier,
        'overdue_fine': capped_overdue,
        'damage_fine': damage_fine,
        'replacement_fee': 0.0,
        'total_fine': total_fine,
        'rule_applied': rule_applied,
        'account_action': account_action
    }
```
