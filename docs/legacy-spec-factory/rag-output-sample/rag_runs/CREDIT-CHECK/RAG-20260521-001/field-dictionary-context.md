# Field Dictionary Context

This file shows how RAG maps legacy fields and program variables to approved
business terms. Dictionary entries are synthetic for this sample.

## Approved Dictionary Terms

| Standard field ID | Canonical name | Definition | Owner | Status |
| --- | --- | --- | --- | --- |
| `DD-CUSTOMER-NUMBER` | Customer Number | Stable customer identifier used for credit lookup. | Credit Operations | approved |
| `DD-CUSTOMER-ACCOUNT-STATUS` | Customer Account Status | Eligibility state for customer credit evaluation. | Credit Operations | approved |
| `DD-CREDIT-LIMIT-AMOUNT` | Credit Limit Amount | Maximum credit exposure configured for the customer. | Credit Operations | approved |
| `DD-CREDIT-USED-AMOUNT` | Credit Used Amount | Current consumed credit exposure. | Credit Operations | approved |
| `DD-CREDIT-AVAILABLE-AMOUNT` | Available Credit Amount | Amount currently available for order approval. | Credit Operations | approved |
| `DD-REQUESTED-ORDER-AMOUNT` | Requested Order Amount | Requested order exposure submitted for credit checking. | Order Management | approved |
| `DD-APPROVED-CREDIT-AMOUNT` | Approved Credit Amount | Amount returned by credit check as currently approvable. | Credit Operations | approved |
| `DD-CREDIT-DECISION-CODE` | Credit Decision Code | Legacy approve/deny indicator returned by credit checking. | Credit Operations | approved |

## Legacy Field Mappings

| Legacy reference | Standard field ID | Evidence | Confidence |
| --- | --- | --- | --- |
| `CUSTMAST.CUSTNO` | `DD-CUSTOMER-NUMBER` | `DDS-CREDIT-CHECK-CUSTMAST-001` | approved_dictionary |
| `CREDITVW.CUSTNO` | `DD-CUSTOMER-NUMBER` | `DDS-CREDIT-CHECK-CREDITVW-001` | approved_dictionary |
| `CREDITCHK.CustNo` | `DD-CUSTOMER-NUMBER` | `SNP-CREDIT-CHECK-002` | confirmed_from_code |
| `CREDITCHK.pCustNo` | `DD-CUSTOMER-NUMBER` | `SNP-CREDIT-CHECK-002` | confirmed_from_code |
| `CUSTMAST.STATUS` | `DD-CUSTOMER-ACCOUNT-STATUS` | `DDS-CREDIT-CHECK-CUSTMAST-001` | approved_dictionary |
| `CREDITVW.STATUS` | `DD-CUSTOMER-ACCOUNT-STATUS` | `DDS-CREDIT-CHECK-CREDITVW-001` | approved_dictionary |
| `CREDITCHK.Status` | `DD-CUSTOMER-ACCOUNT-STATUS` | `SNP-CREDIT-CHECK-003` | confirmed_from_code |
| `CUSTMAST.CRDLMT` | `DD-CREDIT-LIMIT-AMOUNT` | `DDS-CREDIT-CHECK-CUSTMAST-001` | approved_dictionary |
| `CUSTMAST.USEDAMT` | `DD-CREDIT-USED-AMOUNT` | `DDS-CREDIT-CHECK-CUSTMAST-001` | approved_dictionary |
| `CREDITVW.AVAIL_CREDIT` | `DD-CREDIT-AVAILABLE-AMOUNT` | `DDS-CREDIT-CHECK-CREDITVW-001` | approved_dictionary |
| `CREDITCHK.AvailCredit` | `DD-CREDIT-AVAILABLE-AMOUNT` | `SNP-CREDIT-CHECK-003` | confirmed_from_code |
| `CREDITCHK.ReqAmt` | `DD-REQUESTED-ORDER-AMOUNT` | `SNP-CREDIT-CHECK-002` | confirmed_from_code |
| `CREDITCHK.pReqAmt` | `DD-REQUESTED-ORDER-AMOUNT` | `SNP-CREDIT-CHECK-002` | confirmed_from_code |
| `CREDITCHK.ApprAmt` | `DD-APPROVED-CREDIT-AMOUNT` | `SNP-CREDIT-CHECK-002`, `SNP-CREDIT-CHECK-004` | confirmed_from_code |
| `CREDITCHK.pApprAmt` | `DD-APPROVED-CREDIT-AMOUNT` | `SNP-CREDIT-CHECK-002`, `SNP-CREDIT-CHECK-004` | confirmed_from_code |
| `CREDITCHK.Decision` | `DD-CREDIT-DECISION-CODE` | `SNP-CREDIT-CHECK-002`, `SNP-CREDIT-CHECK-004` | confirmed_from_code |

## Unmapped Or Operational Fields

| Legacy reference | Reason | Suggested downstream handling |
| --- | --- | --- |
| `CREDITCHK.MsgText` | Operational message text, not yet mapped to a business dictionary term. | Keep as runtime/report message evidence unless SME says message taxonomy is business-significant. |

## Dictionary Notes

- The sample maps `CREDITVW.AVAIL_CREDIT` to available credit, but the supplied
  logical file does not prove how that value is derived.
- Treat `STATUS = 'A'` as SME-confirmed meaning from `SME-CREDIT-CHECK-001`,
  not solely as a dictionary conclusion.
- Treat `Decision = 'A'` and `Decision = 'D'` as candidate legacy code values
  requiring downstream rule review before promotion.
