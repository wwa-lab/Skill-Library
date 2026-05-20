# Input: Flow Definition (Interactive Menu Example)

**Capability / Module:** Customer Inquiry (CUST-INQUIRY module)

**Business Event:** Customer service rep looks up a customer and views
recent transactions.

**Trigger:** User selects option 5 ("Customer Inquiry") from `*MENU`
object `CSRMENU` in their job menu.

**Programs in chain:**

| Order | Program | OBJ-* | Approved program-analysis |
|---|---|---|---|
| 1 | CUSTINQ  | OBJ-CUST-INQ-001 | program-analysis-OBJ-CUST-INQ-001.md ✅ |
| 2 | CUSTLKP  | OBJ-CUST-INQ-002 | program-analysis-OBJ-CUST-INQ-002.md ✅ |
| 3 | TXNHIST  | OBJ-CUST-INQ-003 | program-analysis-OBJ-CUST-INQ-003.md ✅ |

**UI surfaces:**

- `CSRMENU` (\*MENU)
- `CUSTINQD` (DSPF) — customer search panel
- `CUSTINQD2` (DSPF) — customer detail panel
- `TXNHISTD` (DSPF, with subfile) — recent transactions list

**SME contact:** Liu Wei (Customer Service Operations); confirmed flow
sequence; noted F12 returns to menu and Enter on subfile row option 5
opens transaction detail.
