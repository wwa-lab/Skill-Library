# Input: Flow Definition (Incomplete — Negative Case)

**Capability / Module:** Order Submission (ORDER-SUBMIT module)

**Business Event:** Online order submission from website channel.

**Trigger:** API/Remote — inbound from web channel via MQ queue
`WEBORDER.IN`.

**Programs in chain (declared by inventory `relationships`):**

| Order | Program | OBJ-* | program-analysis status |
|---|---|---|---|
| 1 | WEBORDIN | OBJ-ORDER-SUBMIT-001 | program-analysis-OBJ-ORDER-SUBMIT-001.md ✅ approved |
| 2 | ORDVAL   | OBJ-ORDER-SUBMIT-002 | program-analysis-OBJ-ORDER-SUBMIT-002.md ✅ approved |
| 3 | ORDPRICE | OBJ-ORDER-SUBMIT-003 | **(missing — no program-analysis yet)** |
| 4 | ORDPERSIST | OBJ-ORDER-SUBMIT-004 | program-analysis-OBJ-ORDER-SUBMIT-004.md ✅ approved |
| 5 | WEBORDOUT | OBJ-ORDER-SUBMIT-005 | **(missing — no program-analysis yet)** |

**SME contact:** None confirmed yet for this flow.
