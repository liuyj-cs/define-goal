from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "define-goal" / "scripts" / "validate_goal.py"
FIXTURES = Path(__file__).parent / "fixtures" / "docs" / "goals"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class GoalValidatorTests(unittest.TestCase):
    def assert_valid(self, name: str, *, status: str | None = None) -> str:
        result = run_validator(FIXTURES / name)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VALID:", result.stdout)
        if status is not None:
            self.assertIn(f"status={status}", result.stdout)
        return result.stdout

    def validate_variant(
        self, text: str, filename: str = "valid-zh.md"
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            goal_dir = Path(temporary_directory) / "docs" / "goals"
            goal_dir.mkdir(parents=True)
            path = goal_dir / filename
            path.write_text(text, encoding="utf-8")
            return run_validator(path)

    def test_current_chinese_and_english_structures_remain_valid(self) -> None:
        self.assert_valid("valid-zh.md")
        self.assert_valid("valid-en.md")

    def test_fenced_heading_does_not_split_preflight(self) -> None:
        self.assert_valid("valid-fenced-heading.md")

    def test_placeholders_in_inline_and_fenced_code_are_not_unresolved(self) -> None:
        self.assert_valid("valid-literal-placeholder.md")
        self.assert_valid("valid-fenced-heading.md")

    def test_all_six_lifecycle_status_values_are_valid_and_reported(self) -> None:
        base_zh = (FIXTURES / "valid-zh.md").read_text(encoding="utf-8")
        base_en = (FIXTURES / "valid-en.md").read_text(encoding="utf-8")
        cases = (
            (base_zh, "> 状态：已批准", "> 状态：已批准", "已批准", "valid-zh.md"),
            (base_zh, "> 状态：已批准", "> 状态：已完成", "已完成", "valid-zh.md"),
            (base_zh, "> 状态：已批准", "> 状态：已废弃", "已废弃", "valid-zh.md"),
            (base_en, "> Status: Approved", "> Status: Approved", "Approved", "valid-en.md"),
            (base_en, "> Status: Approved", "> Status: Completed", "Completed", "valid-en.md"),
            (base_en, "> Status: Approved", "> Status: Abandoned", "Abandoned", "valid-en.md"),
        )
        for source, old_line, new_line, status, filename in cases:
            with self.subTest(status=status):
                result = self.validate_variant(
                    source.replace(old_line, new_line),
                    filename,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f"status={status}", result.stdout)

    def test_completed_and_abandoned_fixtures_are_valid(self) -> None:
        self.assert_valid("valid-completed.md", status="已完成")
        self.assert_valid("valid-abandoned.md", status="已废弃")

    def test_filled_new_template_example_is_valid(self) -> None:
        self.assert_valid("valid-full-template.md", status="已批准")

    def test_minimal_goal_with_only_required_sections_is_valid(self) -> None:
        self.assert_valid("valid-minimal.md", status="已批准")

    def test_existing_error_categories_remain_rejected(self) -> None:
        base = (FIXTURES / "valid-zh.md").read_text(encoding="utf-8")
        cases = {
            "missing required section": base.replace(
                "## 范围与权限\n\n- 仅修改授权文件。\n\n", ""
            ),
            "unresolved placeholders": base.replace(
                "## 为什么要做\n", "## 为什么要做\n\n<<TODO>>\n"
            ),
            "hidden schema markers": base + "\n<!-- goal-runtime: codex -->\n",
            "exactly one '/goal ...' command": base.replace("/goal ", "/run "),
            "visible status must be": base.replace("> 状态：已批准", "> 状态：执行中"),
        }
        for expected_error, text in cases.items():
            with self.subTest(expected_error=expected_error):
                result = self.validate_variant(text)
                if os.environ.get("SHOW_VALIDATOR_OUTPUT"):
                    print(f"[{expected_error}]\n{result.stdout.rstrip()}")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(expected_error, result.stdout)


if __name__ == "__main__":
    unittest.main()
