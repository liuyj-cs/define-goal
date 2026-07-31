# Runtime adapters

The goal brief and workflow are portable. Host metadata, discovery, invocation,
and goal-loop behavior are not. The agent that defines the goal does not need to
be the agent that executes it.

## File responsibilities

| Artifact | Codex | Claude Code |
| --- | --- | --- |
| `SKILL.md` | Required workflow, triggering metadata | Required workflow, triggering metadata, and `/define-goal` command source |
| `agents/openai.yaml` | Optional OpenAI/Codex UI label and default prompt | Ignored; no equivalent `agents/claude.yaml` exists |
| `references/` and `assets/` | Read relative to the skill | Read relative to the skill |
| `scripts/validate_goal.py` | Run from the installed skill path | Run through `${CLAUDE_SKILL_DIR}` |

Keep the shared `SKILL.md` frontmatter limited to `name` and `description`.
Claude-specific frontmatter is unnecessary for this workflow and would weaken
portability. Do not invent a Claude metadata file merely to mirror
`agents/openai.yaml`.

Never store the defining or executing harness as goal metadata. Put
harness-specific instructions only in this adapter and the handoff response.
The goal document must contain all decisions and evidence requirements needed by
a fresh agent with repository access and no definition-session context.

## Codex

- Discover a personal skill from `$HOME/.agents/skills/define-goal/` or a
  repository skill from `.agents/skills/define-goal/`.
- Invoke this skill with `$define-goal` or select it through `/skills`.
- Invoke acceptance in a fresh, non-executing session with a request such as
  `$define-goal 验收 docs/goals/<file>.md`.
- Execute the approved brief with the built-in `/goal <objective>`.
- When goal-control tools are exposed, read current state before creating a
  goal. Create or replace a goal only after explicit user authorization.
- If the brief is long, keep the `/goal` objective short and point it at the
  checked-in `docs/goals/*.md` file.
- Codex supports a symlinked skill directory. Avoid installing the same skill
  under multiple discovery roots because duplicate names are not merged.

## Claude Code

### Discovery and invocation

- Discover a personal skill from
  `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/define-goal/SKILL.md`, or a
  repository skill from `.claude/skills/define-goal/SKILL.md`.
- The directory name supplies `/define-goal`; `name` and `description` in
  `SKILL.md` supply identification and automatic-trigger metadata.
- Invoke `/define-goal <intention>`. Because this skill does not consume an
  explicit `$ARGUMENTS` placeholder, Claude Code appends the supplied intention
  to the loaded instructions.
- Invoke acceptance in a fresh, non-executing session with
  `/define-goal 验收 docs/goals/<file>.md`.
- For enumerable decision choices during definition, use `AskUserQuestion` when
  it is available; keep each option concrete and preserve the skill's rule that
  load-bearing decisions are resolved one at a time.
- Resolve bundled resources with `${CLAUDE_SKILL_DIR}`. Do not assume the
  current repository contains a `define-goal/` source directory.
- Execute the approved brief with Claude Code's built-in `/goal <condition>`.
  Do not add a custom skill or command named `goal`; it would conflict with the
  runtime command this workflow is meant to prepare.

### Availability boundaries

- User-level discovery requires the `user` setting source. A session that
  explicitly excludes it will not load this personal skill.
- `--safe-mode` or `--disable-slash-commands` disables custom skills.
- Claude Code's `/goal` requires a trusted workspace and enabled hooks. If
  managed policy disables hooks, return the launch sentence as an ordinary
  prompt and state that automatic continuation is unavailable.
- Claude's goal evaluator judges the conversation; it does not independently
  run commands or read files. Require the executor to surface actual completion
  evidence in the transcript.
- A resumed session can retain an active goal, but the brief remains the stable
  contract and a separate progress file carries execution state.
- If a personal and project skill share the same name, follow Claude Code's
  configured precedence rather than assuming the two definitions merge.

## Acceptance access boundary

Acceptance is an ordinary invocation of this skill, not a new runtime mode or a
replacement for `/goal`. The accepting agent needs read access to the goal,
progress file, repository rules, worktree, and every local evidence source, plus
the authority needed to run all Completion Contract commands and two or three
independent spot checks. If that access is missing, report the affected checks
as unverified and do not close the goal.

## Shared launch condition

Both current hosts accept a goal objective of at most 4,000 characters. Use one
short command in the receiving harness, regardless of which harness created the
document:

```text
/goal Read and complete the approved goal in docs/goals/<file>.md. Treat that file as the complete outcome, scope, authority, constraints, and verification contract. Run its execution preflight first, then continue until every item in its Completion Contract is demonstrated with actual evidence in the execution conversation, or a documented stop condition is reached.
```

Localize the prose when useful, but preserve all five ideas: complete portable
contract, execution preflight, all completion items, evidence in the receiving
conversation, and stop conditions.

If `/goal` is unavailable, provide the same sentence as an ordinary prompt and
state that autonomous continuation is unavailable. Never represent an ordinary
prompt as an active runtime goal.
