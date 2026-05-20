# Forward SDLC Contract

This contract defines what the reverse chain must provide before a Java/cloud
SDLC agent can safely generate implementation artifacts.

## Required Inputs

The forward SDLC agent should receive:

- `spec.yaml`: structured source of truth following `schemas/spec.schema.yaml`
- `spec.md`: human-readable rendering of the same spec
- `traceability-matrix.md` or equivalent structured traceability data
- approved acceptance criteria
- approved or explicitly deferred open questions
- redacted sample transactions when golden master comparison is required

## Required Spec Fields

The forward chain depends on:

- capability ID and name
- approved business rules
- inputs and outputs
- data entities and legacy source mappings
- exceptions and error behavior
- acceptance criteria
- modernization decisions
- test cases or golden master expectations
- unresolved TBDs and their blocking status

## Handoff Rule

The reverse chain may hand off to forward SDLC only when:

- all business-critical rules are `approved`
- all linked evidence is present or SME-approved
- no blocking TBD remains
- data sensitivity has been reviewed
- acceptance criteria exist for every approved rule
- modernization decisions are explicitly separated from observed legacy behavior

## Forward Outputs

The forward SDLC agent may produce:

- Java service design
- API contracts
- domain model
- persistence model
- migration plan
- unit, integration, and acceptance tests
- golden master comparison harness
- deployment notes

## ID Preservation Mechanism

The forward agent must preserve spec IDs in generated implementation and tests.
Use these conventions unless the target team's engineering standards require an
approved alternative.

Java source:

```java
/**
 * @spec-id BR-CREDIT-CHECK-004
 * @evidence EV-CREDIT-CHECK-012
 */
public CreditDecision checkCredit(CreditCheckRequest request) {
    ...
}
```

JUnit:

```java
@Test
@DisplayName("BR-CREDIT-CHECK-004: blocks order when open balance exceeds credit limit")
void blocksOrderWhenOpenBalanceExceedsCreditLimit() {
    ...
}
```

Generated traceability:

```yaml
implementation_trace:
  - spec_id: BR-CREDIT-CHECK-004
    code_refs:
      - src/main/java/com/example/credit/CreditCheckService.java
    test_refs:
      - src/test/java/com/example/credit/CreditCheckServiceTest.java
```

Do not drop IDs during refactoring. If code no longer implements a rule, update
the traceability report and review status rather than silently removing the ID.
