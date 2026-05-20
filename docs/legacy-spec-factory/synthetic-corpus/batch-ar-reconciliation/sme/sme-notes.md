# SME Notes

Reviewer: Daniel Wu  
Role: Finance Operations SME  
Review Date: 2026-05-20

## Confirmed Business Meaning

- The batch is triggered nightly by scheduler through a submitted job, not by
  an interactive menu.
- The `ARCTRL` record is the restart/checkpoint control point for this batch.
- `RESTARTFL = 'Y'` means operations are resuming after an interrupted run.
- The exception report is reviewed the next morning by Finance before any
  write-off or manual correction decision is taken.
- A non-zero reconciliation difference is not auto-posted away; it becomes an
  exception item for review.

## Operational Notes

- Normal cut-off is before downstream consolidation starts at 06:00.
- If the batch fails mid-run, ops may rerun after correcting source data; the
  checkpoint record prevents the wrong run-date context from being used.

## Open Questions For Later Expansion

- This compact fixture does not yet show a separate GL-posting follow-on step.
- A later blocked sibling could test what happens when restart flag meaning is
  undocumented or conflicts with runtime evidence.
