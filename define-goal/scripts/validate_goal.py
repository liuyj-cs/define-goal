#!/usr/bin/env python3
"""Validate a portable goal brief produced by the define-goal skill."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath


SECTION_ALIASES = {
    "goal-statement": ("目标陈述", "Goal Statement"),
    "why": ("为什么要做", "Why This Matters"),
    "current-state": ("已知事实与来源", "Known Facts and Sources"),
    "decisions": (
        "已确认决策、假设与留白",
        "Confirmed Decisions, Assumptions, and Open Items",
    ),
    "scope": ("范围与权限", "Scope and Authority"),
    "constraints": (
        "约束、优先级与防绕过",
        "Constraints, Priorities, and Anti-Cheating",
    ),
    "preflight": ("执行前复核", "Execution Preflight"),
    "evidence-plan": ("工作与取证路径", "Work and Evidence Plan"),
    "completion-contract": ("完成契约", "Completion Contract"),
    "stop-conditions": ("停止、升级与续跑", "Stop, Escalation, and Resume"),
    "handoff": ("跨 Harness 交接", "Cross-Harness Handoff"),
}
TYPE_ALIASES = {
    "execution": {"execution", "执行型"},
    "exploration": {"exploration", "探索型"},
    "mixed": {"mixed", "混合型"},
}
STATUS_VALUES = {
    "approved",
    "completed",
    "abandoned",
    "已批准",
    "已完成",
    "已废弃",
}
PLACEHOLDER_RE = re.compile(r"<<[A-Z][A-Z0-9_-]*>>")
INTERNAL_MARKER_RE = re.compile(
    r"<!--\s*(?:goal-|section:)|goal-runtime\s*:",
    flags=re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a portable docs/goals Markdown goal brief."
    )
    parser.add_argument("goal_file", type=Path)
    return parser.parse_args()


def normalized_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def masked_line(line: str) -> str:
    return "".join(character if character in "\r\n" else " " for character in line)


def mask_fenced_code(text: str) -> str:
    lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if fence_character is None:
            opening = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})", content)
            if opening:
                fence = opening.group(1)
                fence_character = fence[0]
                fence_length = len(fence)
                lines.append(masked_line(line))
                continue
            lines.append(line)
            continue

        closing = re.match(
            rf"^[ \t]{{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$",
            content,
        )
        lines.append(masked_line(line))
        if closing:
            fence_character = None
            fence_length = 0

    return "".join(lines)


def mask_inline_code(text: str) -> str:
    masked = list(text)
    for line_match in re.finditer(r"^.*$", text, flags=re.MULTILINE):
        line = line_match.group(0)
        offset = line_match.start()
        index = 0
        while index < len(line):
            if line[index] != "`":
                index += 1
                continue
            end_of_opening = index + 1
            while end_of_opening < len(line) and line[end_of_opening] == "`":
                end_of_opening += 1
            delimiter = line[index:end_of_opening]
            closing = line.find(delimiter, end_of_opening)
            if closing == -1:
                index = end_of_opening
                continue
            end = closing + len(delimiter)
            masked[offset + index : offset + end] = " " * (end - index)
            index = end
    return "".join(masked)


def h2_sections(text: str) -> list[tuple[str, int, int]]:
    text_without_fences = mask_fenced_code(text)
    matches = list(
        re.finditer(r"^##\s+(.+?)\s*$", text_without_fences, flags=re.MULTILINE)
    )
    sections: list[tuple[str, int, int]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((normalized_heading(match.group(1)), start, end))
    return sections


def section_body(text: str, aliases: tuple[str, ...]) -> tuple[str | None, int]:
    accepted = {normalized_heading(alias) for alias in aliases}
    matches = [
        text[start:end].strip()
        for heading, start, end in h2_sections(text)
        if heading in accepted
    ]
    if not matches:
        return None, 0
    return matches[0], len(matches)


def visible_metadata(text: str, labels: tuple[str, ...]) -> str | None:
    label_pattern = "|".join(re.escape(label) for label in labels)
    match = re.search(
        rf"^>\s*(?:{label_pattern})\s*[：:]\s*(.+?)\s*$",
        text,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    if not match:
        return None
    return match.group(1).replace("`", "").strip()


def canonical_goal_type(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.casefold()
    for canonical, aliases in TYPE_ALIASES.items():
        if normalized in {alias.casefold() for alias in aliases}:
            return canonical
    return None


def content_without_subheadings(body: str) -> str:
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    return "\n".join(lines)


def goal_relative_path(path: Path) -> str | None:
    parts = path.resolve().parts
    matches = [
        index
        for index in range(len(parts) - 1)
        if parts[index] == "docs" and parts[index + 1] == "goals"
    ]
    if not matches:
        return None
    return str(PurePosixPath(*parts[matches[-1] :]))


def validate(path: Path) -> list[str]:
    errors: list[str] = []

    if not path.exists():
        return [f"file does not exist: {path}"]
    if not path.is_file():
        return [f"path is not a file: {path}"]
    if path.suffix.lower() != ".md":
        errors.append("goal file must use the .md extension")

    relative_path = goal_relative_path(path)
    if relative_path is None:
        errors.append("goal file must be located under a docs/goals directory")

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return errors + ["goal file must be valid UTF-8"]

    if INTERNAL_MARKER_RE.search(text):
        errors.append(
            "goal document must not contain hidden schema markers or goal-runtime metadata"
        )

    title = re.search(r"^#\s+\S.+$", text, flags=re.MULTILINE)
    if not title:
        errors.append("missing non-empty level-one title")

    status = visible_metadata(text, ("状态", "Status"))
    if status is None or status.casefold() not in {
        value.casefold() for value in STATUS_VALUES
    }:
        errors.append(
            "visible status must be 已批准/已完成/已废弃 or "
            "Approved/Completed/Abandoned"
        )

    goal_type = canonical_goal_type(
        visible_metadata(text, ("目标类型", "Goal Type"))
    )
    if goal_type is None:
        errors.append(
            "visible goal type must be 执行型/探索型/混合型 or "
            "execution/exploration/mixed"
        )

    declared_path = visible_metadata(text, ("目标文档", "Goal Document"))
    if relative_path and declared_path != relative_path:
        errors.append(
            f"visible goal document path must equal the actual path: {relative_path}"
        )

    handoff_principle = visible_metadata(text, ("交接原则", "Handoff Principle"))
    if not handoff_principle:
        errors.append("missing visible cross-harness handoff principle")

    text_without_code = mask_inline_code(mask_fenced_code(text))
    placeholders = sorted(set(PLACEHOLDER_RE.findall(text_without_code)))
    if placeholders:
        errors.append("unresolved placeholders: " + ", ".join(placeholders))

    bodies: dict[str, str] = {}
    for name, aliases in SECTION_ALIASES.items():
        body, count = section_body(text, aliases)
        if count == 0 or body is None:
            errors.append(f"missing required section: {aliases[0]}")
            continue
        if count > 1:
            errors.append(f"duplicate required section: {aliases[0]}")
        bodies[name] = body
        if not content_without_subheadings(body):
            errors.append(f"section has no content: {aliases[0]}")

    preflight = bodies.get("preflight", "")
    preflight_items = re.findall(r"^-\s+\[[ xX]\]\s+\S", preflight, re.MULTILINE)
    if len(preflight_items) < 3:
        errors.append("execution preflight must contain at least three checklist items")

    completion = bodies.get("completion-contract", "")
    completion_items = re.findall(
        r"^-\s+\[[ xX]\]\s+\S", completion, re.MULTILINE
    )
    if len(completion_items) < 2:
        errors.append("completion contract must contain at least two checklist items")

    stop_conditions = bodies.get("stop-conditions", "")
    if not re.search(r"^\s*(?:-\s+|\d+[.)]\s+)\S", stop_conditions, re.MULTILINE):
        errors.append("stop conditions must contain at least one list item")

    handoff = bodies.get("handoff", "")
    if "harness" not in handoff.casefold():
        errors.append("cross-harness handoff section must name the harness boundary")
    if "定义会话" not in handoff and "definition session" not in handoff.casefold():
        errors.append(
            "cross-harness handoff must state that definition-session context is not required"
        )

    launch_commands = [
        line.strip() for line in handoff.splitlines() if line.strip().startswith("/goal ")
    ]
    if len(launch_commands) != 1:
        errors.append("cross-harness handoff must contain exactly one '/goal ...' command")
    else:
        command = launch_commands[0]
        if len(command) > 4000:
            errors.append("launch command exceeds the 4,000-character goal limit")
        if relative_path and relative_path not in command:
            errors.append(
                f"launch command must reference the exact goal path: {relative_path}"
            )

    return errors


def main() -> int:
    args = parse_args()
    errors = validate(args.goal_file)
    if errors:
        print(f"INVALID: {args.goal_file}")
        for error in errors:
            print(f"- {error}")
        return 1

    text = args.goal_file.read_text(encoding="utf-8")
    goal_type = canonical_goal_type(
        visible_metadata(text, ("目标类型", "Goal Type"))
    )
    status = visible_metadata(text, ("状态", "Status"))
    relative_path = goal_relative_path(args.goal_file)
    print(
        f"VALID: {relative_path} "
        f"(type={goal_type}, status={status}, cross_harness=yes)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
