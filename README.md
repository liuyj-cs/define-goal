# define-goal

`define-goal` turns an intention into a self-contained goal contract under
`docs/goals/`, hands execution to the host's built-in `/goal`, and can verify
and close the result from a fresh acceptance session.

## Symlink installation

Point both hosts at the same source directory. Set `DEFINE_GOAL_REPO` to this
repository's absolute path; do not copy the skill or create a custom `/goal`
skill.

```bash
DEFINE_GOAL_REPO=/absolute/path/to/DefineGoal
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$DEFINE_GOAL_REPO/define-goal" "$HOME/.agents/skills/define-goal"
ln -s "$DEFINE_GOAL_REPO/define-goal" "$HOME/.claude/skills/define-goal"
```

Codex discovers the first link and Claude Code discovers the second. Existing
links should be inspected before replacement.

## Layout

- `define-goal/SKILL.md`: definition and acceptance workflows.
- `define-goal/assets/goal-template.md`: portable Chinese goal template.
- `define-goal/references/`: evidence patterns and host adapters.
- `define-goal/scripts/validate_goal.py`: standard-library goal validator.
- `tests/`: unittest coverage and synthetic goal fixtures.

## Validation and tests

Validate one goal document:

```bash
python3 define-goal/scripts/validate_goal.py docs/goals/<goal-file>.md
```

Run the regression suite from the repository root:

```bash
python3 -m unittest discover -s tests
```
