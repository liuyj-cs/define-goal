# Goal patterns

Use this reference to choose honest evidence and to run the decision interview.
Do not copy every pattern into every goal.

## Decision interview

Maintain these categories:

| Category | Meaning |
| --- | --- |
| Verified fact | Observed directly from an authorized source or command |
| Inference | Best explanation of verified facts, still falsifiable |
| Assumption | Unverified input the goal currently depends on |
| Preference | User-owned priority or risk tolerance |
| Decision | Explicitly accepted choice and its reason |
| Deferred | Deliberately left open with an execution rule |

Order questions by dependency, impact, irreversibility, and cost of being wrong.
A useful question gives a recommendation, its basis, and the strongest
counterargument. Do not turn the interview into a questionnaire.

## Evidence patterns

| Domain | Outcome evidence | Constraint evidence |
| --- | --- | --- |
| Bug | failing reproduction before, passing regression after | unaffected targeted or full suite |
| Feature | acceptance examples or user-visible behavior | compatibility, lint, typecheck, tests |
| Migration | zero remaining old call sites plus build/tests | no unsupported scope or data loss |
| Performance | metric, threshold, method, environment, repeated runs | correctness and resource guardrails |
| Reliability | failure injection and recovery evidence | alerting, rollback, no silent failure |
| Research | decision-ready findings with sources, dates, and reproduction steps | uncertainty and excluded-source disclosure |
| Operations | defined healthy state over a monitoring window | rollback trigger and change record |
| Documentation | required audience questions answered and links valid | factual review against authoritative sources |

Name exact commands only when verified. Otherwise state the property to prove
and require task 0 to discover the repository's real validator.

## Anti-cheat without overconstraint

Guard against only shortcuts that are both tempting and plausible:

- deleting, skipping, weakening, or replacing the check;
- changing the benchmark, fixture, threshold, or evaluator instead of the
  target behavior;
- mocking the behavior that is supposed to be exercised;
- suppressing an exit code or treating warnings as success;
- narrowing the input population until the metric looks good;
- claiming a command was run or a source was read without evidence.

Freeze specification-bearing files only when they truly define acceptance.
Do not ban implementation approaches merely because the goal author prefers a
particular solution.

### Reverse verification

For a candidate acceptance item, ask: "If this breaks, who or what will know?"
When the honest answer is "no one," selectively require reverse verification:
make the protected behavior fail once, preserve the red output, restore the
behavior, and preserve the green output. Use this for fragile checks whose
passing state alone could be accidental or disconnected from the requirement;
do not impose it mechanically on every goal.

## Goal seams

When related goals touch the same outcome or files, state:

- their ordering and which result unlocks the next goal;
- one unambiguous owner for every overlapping path;
- the evidence or state handed across each seam.

A seam with no receiving owner is an incident. Keep the "Related Goals"
section out of independent goals instead of filling it with decorative text.

## Stop and resume

Use bounded persistence, not endless grinding. Stop conditions written into a
goal are limited to these kinds:

- an observed baseline contradicts a material premise;
- the same validator fails three times without a new hypothesis;
- required authority, credentials, or external approval is missing — finish
  the unaffected items first, mark the affected ones unverified, then stop and
  report the gap;
- a destructive or externally visible action is needed but not authorized;
- the time, turn, cost, or source budget is exhausted;
- progress would require a substantive scope change (mechanical spillover such
  as import updates is allowed with a one-line note in the progress file).

Every execution ending must land on one of the two legal exits: every
completion item has evidence, or a documented stop condition is reached. A
rule that defines an ending outside these two exits is a defect.

Process hygiene — commit state, branch layout, file tracking status, or the
existence of a progress file — is never a precondition or stop condition. At
most it appears as one advisory line in the acceptance report.

Goal status is semantic, not hygiene: only an `已批准`/`Approved` goal may be
executed. A document in `已完成`/`已废弃` (Completed/Abandoned) state is
read-only for review and re-enters execution only after the owner explicitly
reopens it by flipping the status back to approved.

For work likely to span sessions, authorize a separate progress file such as
`docs/goals/<goal-slug>.progress.md`. The progress file records evidence,
attempts, and the next step; it must never silently amend the approved goal.

Put non-load-bearing questions in a "Pending owner decisions" (`待裁决`) area
of that progress file, record the question, impact, and temporary handling,
then keep working on unaffected parts. Stop globally only when a documented
stop condition is reached or a load-bearing premise conflicts with observed
facts.

## Cross-harness handoff

Assume the defining agent and executing agent are different unless the user
explicitly says otherwise.

- Put every material decision, assumption, scope boundary, permission, and
  completion rule in the goal document. Do not rely on chat history,
  scratchpads, memory, or active goal state.
- Use repository-relative paths and commands. Avoid harness-specific tool names
  unless the goal truly requires that capability.
- Label definition-time observations with their source and date. Require the
  executor to revalidate drift-prone facts before mutation.
- Keep the approved goal immutable across handoff. Record execution progress in
  a separate file and require owner confirmation for amendments.
- If the receiving harness lacks a required tool, install a missing common
  open-source tool when the goal's agent-decided defaults authorize it — never
  sudo or system-level changes. For anything that cannot be installed, such as
  credentials, external services, or environments, mark only the affected items
  as unverified, complete the rest, then close by reporting the gap as a
  documented stop; never fill it by inference.
