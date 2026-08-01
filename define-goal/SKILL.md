---
name: define-goal
description: Turn a fuzzy, consequential, or long-running intention into a confirmed, evidence-backed, cross-harness goal brief saved under docs/goals with a dated filename and ready for another agent to execute through the built-in /goal mode in Codex or Claude Code. Also accept or verify a completed goal in a fresh session and close it automatically after an independent acceptance pass. Use when the user invokes $define-goal or /define-goal, asks to define or clarify a goal, 写目标、目标任务书、goal prompt, 验收目标、结项, or wants an agent to work autonomously toward a verifiable outcome. Do not use for ordinary implementation whose outcome and checks are already clear, or to start execution unless the user explicitly asks.
disable-model-invocation: true
---

# Define Goal

Turn intent into an approved contract that a long-running agent can execute and
verify honestly. Conduct the session in the user's language and preserve
established domain terms.

## Operating boundary

- Define the goal; do not implement it during the definition workflow.
- Assume the defining agent and executing agent may be different. Make the goal
  document self-contained, repository-relative, and independent of harness,
  chat history, scratchpads, or current goal-tool state.
- Use read-only inspection to discover facts. Do not ask the user for facts that
  can be checked safely in the authorized environment.
- Treat facts, inferences, assumptions, preferences, and decisions as distinct
  categories.
- Do not write the goal document until the user confirms the material decisions.
  A user who explicitly requests a non-interactive best-effort brief authorizes
  reasonable defaults, but label each material default and its cost of being
  wrong.
- Do not start, replace, clear, or resume a runtime goal unless the user
  explicitly asks. Goal definition alone is not permission to begin execution.
- Protect pre-existing working-tree state. Do not modify or clean it during
  definition, and do not describe every out-of-scope or frozen path as an
  existing worktree change. If an existing change overlaps the goal and its
  ownership cannot be established, make that a stop condition.
- Never read or print secrets, credential files, cookies, tokens, or
  environment-variable values.

## Workflow

### 1. Establish the object

Restate:

- the intended outcome;
- the artifact, system, repository, environment, or decision involved;
- the target repository and any handoff or access boundary;
- why the result matters;
- what this definition session must resolve.

Do not bind the goal to Codex, Claude Code, or another harness unless the user
explicitly requires a harness-specific capability. Host choice is normally an
execution concern, not part of the goal.

If a goal-state tool is available, read the current state first. Flag a
conflicting active goal; never replace it silently.

### 2. Inspect before asking

When a repository or working environment is available, inspect only what is
needed to ground the goal:

- governing `AGENTS.md` or `CLAUDE.md` files;
- relevant README, specifications, plans, schemas, and design artifacts;
- package scripts, test configuration, CI jobs, and existing validators;
- affected module boundaries and `git status`;
- cheap, safe baseline commands that materially affect the completion contract.

Prefer existing specification-bearing files and validators over prose copied
into the brief. Verify command existence before naming a command as evidence.
Do not install dependencies or run a broad or expensive suite merely to define
the goal.

If the environment cannot be inspected, mark claims as unverified and make
environment discovery the first execution step. Never disguise a guessed
command or baseline as observed fact. Even when inspection succeeds, record the
source and observation date and require the future executor to revalidate
drift-prone facts before changing anything.

When `git status` is available, distinguish:

- modified or untracked items that already exist and must not be cleaned or
  overwritten;
- paths that are merely outside the approved scope;
- paths that the goal explicitly freezes.

Record only the first category as pre-existing worktree state. If it is empty,
say so explicitly while still requiring the executor to recheck. If an existing
change overlaps the approved scope, require the executor to preserve its
unrelated portions; stop when ownership cannot be determined safely.

### 3. Classify and map the goal

Read [references/goal-patterns.md](references/goal-patterns.md) before the
interview. Classify the work as:

- **execution**: completion can be shown by a changed state and checks;
- **exploration**: completion is a decision or answer supported by reproducible
  evidence;
- **mixed**: exploration must resolve a named decision before bounded execution.

Build a private decision map ordered by dependency, impact, reversibility, and
cost of being wrong. Track known facts, assumptions, preferences, accepted
decisions, rejected alternatives, and open questions.

### 4. Resolve only material decisions

Ask one load-bearing decision point per turn. A decision is load-bearing when a
different answer would materially change the outcome, scope, authority,
acceptance standard, or stop conditions. Do not batch load-bearing decisions.

For each decision point provide:

- the question;
- a recommended answer in one sentence;
- the main reason in one sentence;
- the strongest tradeoff or counterargument in one sentence;
- the basis labeled as verified fact, inference, or judgment.

Ask about outcomes, priorities, risk tolerance, scope, authority, acceptance
judgment, and stop conditions. Do not ask the user to choose technical details
that the executor can decide safely inside the accepted goal.

Decide long-tail, non-load-bearing points on the user's behalf. For each such
default, record one sentence of reasoning and the cost of being wrong, then put
all defaults in an "Agent-decided defaults (change before approval)" list for
the owner to flip in one pass. Do not interrupt the interview for these points.

After five resolved decisions, or at a major dependency boundary, summarize
accepted decisions and remaining high-impact branches. Stop interviewing once
the goal is actionable; do not optimize low-impact preferences indefinitely.

### 5. Pass the goal quality gate

The draft must answer all of these:

1. What concrete state will be true when done?
2. What evidence will prove that state?
3. What binary or quantitative threshold defines success?
4. What is explicitly in scope and out of scope?
5. What files, systems, people, money, permissions, or external actions may the
   executor affect?
6. Which tempting shortcuts would satisfy the metric while violating the
   intent?
7. Which priorities govern tradeoffs?
8. What mismatch, failure count, budget, or uncertainty must stop execution?
9. How will progress survive a resumed session without changing the approved
   contract?
10. Could a fresh agent in another harness execute this document without access
    to the definition conversation?
11. Does every known fact support a decision, acceptance item, or stop
    condition, and have facts an executor can see at a glance in the repository
    been removed?

Reject activity goals such as "make progress", "keep investigating", or
"improve X". Replace decorative precision with the most honest observable
validator. For exploration, measure evidence quality and the decision enabled,
not arbitrary source or conclusion counts.

Keep the brief's length proportional to its risk and coordination burden. Keep
a small goal to one page when that is enough to remain self-contained.

### 6. Confirm the contract

Present a concise decision register containing:

- the proposed one-sentence goal;
- accepted decisions and reasons;
- agent-decided defaults, each with its reason and cost of being wrong;
- material assumptions and their consequences;
- rejected alternatives;
- deferred or deliberately open questions;
- the proposed completion evidence and stop conditions.

Ask for explicit confirmation. A clear instruction to save or start the
presented contract counts as confirmation when no high-impact branch remains.

### 7. Write the goal brief

After confirmation:

1. Create `docs/goals/` if needed.
2. Choose `docs/goals/YYYY-MM-DD-<short-slug>.md` using the user's local date.
3. Never overwrite an existing goal. Revise an existing file only when the user
   explicitly asks to amend that goal, and preserve the reason for the amendment.
4. Fill [assets/goal-template.md](assets/goal-template.md). Keep its ordinary
   Markdown headings and replace every `<<PLACEHOLDER>>`. Do not add hidden
   schema comments or harness-specific runtime metadata.
5. Fill `<<PREEXISTING_WORKTREE_STATE_OR_NONE>>` with the concrete modified or
   untracked items observed before definition, or state that none were observed.
   Do not use this field for every out-of-scope or frozen path.
6. Only six sections are required: 目标陈述, 范围与权限, 执行前复核, 完成契约,
   停止、升级与续跑, and 跨 Harness 交接. Every other template section is
   optional — keep it only when it earns its place, and delete the entire
   section otherwise. For example, keep "Related Goals" only when another goal
   has an ordering dependency, overlapping path, or explicit handoff condition.
7. Treat evidence requirements as mandatory and the proposed steps and order as
   advisory. If execution takes another route, require one sentence explaining
   the deviation in the progress file and all originally required evidence.
8. Keep the brief self-contained. Cite observed commands, files, dates, or
   sources next to the claims they support.
9. Separate definition-time observations from execution-time facts. Require the
   receiving agent to reread repository instructions, recheck the working tree,
   and rerun material baselines before mutation.
10. Put one portable built-in `/goal` launch command in the final section. Point
   it at the document instead of pasting a long brief into the command. The same
   document and command must be usable when definition and execution happen in
   different supported harnesses.

Do not create `PROGRESS.md`, `BLOCKED.md`, or implementation artifacts while
defining the goal. The approved brief may authorize the future executor to
create a separate progress file when resumption needs it.

### 8. Validate and hand off

Run the validator through the host-specific skill directory. Do not assume the
target repository contains the skill source.

Claude Code:

```text
python3 "${CLAUDE_SKILL_DIR}/scripts/validate_goal.py" docs/goals/<goal-file>.md
```

Codex or another Agent Skills host:

```text
python3 <absolute-directory-containing-this-SKILL.md>/scripts/validate_goal.py docs/goals/<goal-file>.md
```

Fix all validation errors and rerun until it exits zero. Read
[references/runtime-adapters.md](references/runtime-adapters.md) before handing
off or starting the goal.

Return:

- the approved goal in one sentence;
- a clickable path to the goal document;
- the exact `/goal ...` command to run;
- validation evidence;
- a reminder to commit the approved document before execution starts, so
  acceptance can diff against that commit as its tamper-check baseline;
- any still-open, explicitly deferred issue.

If the user explicitly asks to start now and the runtime exposes goal-control
tools, check current goal state and set the validated launch objective. If the
runtime does not expose such a tool, return the command for the user to enter;
do not claim the goal started.

## Acceptance and closure mode

Enter this mode when the user invokes a request such as
`/define-goal 验收 docs/goals/<goal-file>.md`, asks to accept or verify a
completed goal, asks to close a goal, or when an executing agent spawns a
subagent for automatic acceptance after finishing a goal. Acceptance is
model-run: the owner only reads the short report. A full pass closes the goal
in the same step; the owner can ask to revert a closure afterward.

Acceptance must be performed by an agent whose context did not do the work: a
fresh session started by the owner, or a subagent the executing agent spawns
right after the Completion Contract evidence is in. A spawning executor passes
only the goal document path and relays the acceptance report verbatim, without
rewriting or summarizing it. Never grade work your own context performed; an
executor that cannot spawn a subagent hands the owner the acceptance command
instead of accepting.

In the accepting agent:

1. Read the goal document, its authorized progress file when present, current
   repository rules, and current worktree state.
2. Check that the approved contract survived execution unmodified: diff the
   goal file against its last approved commit. Only an appended closure record
   may differ. If the body changed, or no committed baseline exists, say so in
   the report instead of silently treating the current text as the approved
   contract.
3. Personally rerun every command named by the Completion Contract. Prior logs
   are context, not proof that the current state passes.
4. Derive and run two or three checks not named in the goal document. Choose
   them at acceptance time from the highest-risk boundaries, anti-cheat rules,
   and likely collateral effects.
5. If a required command cannot run, report that item as unverified and do not
   infer, guess, or close the goal.
6. If every Completion Contract item and every spot check passed, change the
   visible status to `已完成`/`Completed`, append the level-two section shown
   below, and rerun `validate_goal.py`. If anything failed or could not be
   verified, leave the status and document untouched; flipping to
   `已废弃`/`Abandoned` always requires an explicit owner decision.
7. End with a plain-language report of no more than five lines covering: pass
   or fail; what was actually delivered; unmet or unverified items; the
   independent spot checks; and whether the goal was closed, or what decision
   the owner still needs to make. Closure is one status line plus one appended
   record; revert it on request.

```markdown
## 结项记录

- 验收日期：<date>
- 结论：<completed or abandoned, with reason>
- 逐项核对与抽查摘要：<completion items and independent checks>
- 状态翻转记录：<old status -> new status, closed by the acceptance session>
```

Acceptance is the only workflow allowed to change the status of an approved
goal document. Do not alter the approved contract's scope, decisions,
constraints, or Completion Contract during closure.

## Completion gate

The definition workflow is complete only when:

- no unresolved high-impact decision remains;
- the user confirmed the contract, or explicitly authorized labeled defaults;
- exactly one approved goal document exists at the reported path;
- a document newly written by the definition workflow has visible status
  `已批准` or `Approved`;
- a fresh executor can understand it without the definition conversation;
- the document does not bind execution to the defining harness;
- `validate_goal.py` passes that exact file;
- the launch command references that file and requires completion evidence in
  the conversation.
