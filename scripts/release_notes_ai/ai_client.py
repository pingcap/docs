from __future__ import annotations

import dataclasses
from functools import lru_cache
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Any

from .constants import (
    BUG_FIXES_REFERENCE,
    GENERATION_PROMPT_TEMPLATE,
    IMPROVEMENTS_REFERENCE,
)
from .models import GeneratedNote, RowContext


class AIClient:
    def __init__(self, command: str, model: str | None, timeout: int):
        self.command = shlex.split(command)
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str, expected_links: list[str], contributors: list[str]) -> GeneratedNote:
        result, errors = self._run_and_validate(prompt, expected_links, contributors)
        if result:
            return result

        repair_prompt = build_repair_prompt(prompt, errors)
        result, repair_errors = self._run_and_validate(repair_prompt, expected_links, contributors)
        if result:
            return result
        raise ValueError("; ".join(repair_errors))

    def _run_and_validate(
        self, prompt: str, expected_links: list[str], contributors: list[str]
    ) -> tuple[GeneratedNote | None, list[str]]:
        output = self._run(prompt)
        try:
            data = extract_json_object(output)
        except ValueError as exc:
            return None, [str(exc)]
        return validate_ai_response(data, expected_links, contributors)

    def _run(self, prompt: str) -> str:
        command = list(self.command)
        if not command:
            raise ValueError("AI command is empty. Pass a command with --ai-command.")
        if not is_executable_available(command[0]):
            raise FileNotFoundError(
                f"AI command executable not found: {command[0]!r}. "
                "Install it or pass a custom command with --ai-command."
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path: Path | None = None
            if self._is_codex_exec(command):
                if self.model:
                    command.extend(["-m", self.model])
                temp_path = Path(temp_dir)
                schema_path = temp_path / "ai-output-schema.json"
                output_path = temp_path / "ai-output.txt"
                schema_path.write_text(json.dumps(ai_output_schema()), encoding="utf-8")
                output_path.touch()
                command.extend(["--output-schema", str(schema_path)])
                command.extend(["--output-last-message", str(output_path)])

            completed = subprocess.run(
                command,
                input=prompt,
                text=True,
                capture_output=True,
                timeout=self.timeout,
                check=False,
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    "AI command failed with exit code "
                    f"{completed.returncode}: {summarize_process_output(completed)}"
                )
            if output_path and output_path.exists():
                last_message = output_path.read_text(encoding="utf-8").strip()
                if last_message:
                    return last_message
            return completed.stdout.strip()

    @staticmethod
    def _is_codex_exec(command: list[str]) -> bool:
        if not command:
            return False
        executable = Path(command[0]).name
        return executable == "codex" and "exec" in command[1:]


def is_executable_available(executable: str) -> bool:
    if os.sep in executable or (os.altsep and os.altsep in executable):
        return Path(executable).exists()
    return shutil.which(executable) is not None


def ai_output_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["type", "release_note", "needs_review", "reason"],
        "properties": {
            "type": {"type": "string", "enum": ["improvement", "bug_fix"]},
            "release_note": {"type": "string"},
            "needs_review": {"type": "boolean"},
            "reason": {"type": "string"},
        },
    }


def summarize_process_output(completed: subprocess.CompletedProcess[str]) -> str:
    parts = []
    if completed.stderr.strip():
        parts.append("stderr:\n" + tail_output(completed.stderr))
    if completed.stdout.strip():
        parts.append("stdout:\n" + tail_output(completed.stdout))
    return "\n\n".join(parts) or "no output"


def tail_output(text: str, max_lines: int = 40, max_chars: int = 4000) -> str:
    tail = "\n".join(text.strip().splitlines()[-max_lines:])
    if len(tail) > max_chars:
        tail = "...[truncated]\n" + tail[-max_chars:]
    return tail


def build_generation_prompt(
    row_context: RowContext,
    expected_links: list[str],
    contributors: list[str],
) -> str:
    prompt_template = load_prompt_template(GENERATION_PROMPT_TEMPLATE)
    improvements_reference = load_reference_file(IMPROVEMENTS_REFERENCE)
    bug_fixes_reference = load_reference_file(BUG_FIXES_REFERENCE)
    context = {
        "row_number": row_context.row_number,
        "component": row_context.component,
        "raw_component_from_excel": row_context.raw_component,
        "issue_type_from_excel": row_context.issue_type,
        "pr_title_from_excel": row_context.pr_title,
        "formatted_release_note_from_excel": row_context.formatted_release_note,
        "expected_links": expected_links,
        "contributors": contributors,
        "issues": [dataclasses.asdict(issue) for issue in row_context.issues],
        "pull_requests": [dataclasses.asdict(pull) for pull in row_context.pulls],
    }
    return render_prompt_template(
        prompt_template,
        {
            "EXPECTED_LINKS": json.dumps(expected_links, ensure_ascii=False, indent=2),
            "CONTRIBUTORS": json.dumps(contributors, ensure_ascii=False, indent=2),
            "ROW_CONTEXT": json.dumps(context, ensure_ascii=False, indent=2),
            "IMPROVEMENTS_REFERENCE": improvements_reference,
            "BUG_FIXES_REFERENCE": bug_fixes_reference,
        },
    )


def build_repair_prompt(original_prompt: str, errors: list[str]) -> str:
    return textwrap.dedent(
        f"""
        Your previous answer did not satisfy the required JSON schema or release-note rules.

        Validation errors:
        {json.dumps(errors, ensure_ascii=False, indent=2)}

        Rewrite the answer. Return only the corrected JSON object.

        Original task:
        {original_prompt}
        """
    ).strip()


def render_prompt_template(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template.strip()


@lru_cache(maxsize=None)
def load_prompt_template(path: Path) -> str:
    try:
        return strip_prompt_template_heading(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Cannot find release-note prompt template: {path}. "
            "Make sure scripts/release_notes_ai/prompts/generation.md exists."
        ) from exc


def strip_prompt_template_heading(template: str) -> str:
    lines = template.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        if lines and not lines[0].strip():
            lines = lines[1:]
    return "\n".join(lines)


@lru_cache(maxsize=None)
def load_reference_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Cannot find release-note reference file: {path}. "
            "Make sure the repo-local write-review-translate-release-notes skill is present."
        ) from exc


def extract_json_object(output: str) -> dict[str, Any]:
    output = output.strip()
    if not output:
        raise ValueError("AI command returned no output")
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        candidates = extract_json_object_candidates(output)
        if not candidates:
            raise ValueError("AI output did not contain a JSON object") from None
        required_keys = {"type", "release_note", "needs_review", "reason"}
        data = next(
            (candidate for candidate in candidates if required_keys <= candidate.keys()),
            candidates[0],
        )
    if not isinstance(data, dict):
        raise ValueError("AI output JSON is not an object")
    return data


def extract_json_object_candidates(output: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    candidates: list[dict[str, Any]] = []
    for index, char in enumerate(output):
        if char != "{":
            continue
        try:
            data, _end = decoder.raw_decode(output[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            candidates.append(data)
    return candidates


def validate_ai_response(
    data: dict[str, Any],
    expected_links: list[str],
    contributors: list[str],
) -> tuple[GeneratedNote | None, list[str]]:
    errors: list[str] = []
    note_type = data.get("type")
    release_note = data.get("release_note")
    needs_review = data.get("needs_review")
    reason = data.get("reason")

    if note_type not in {"improvement", "bug_fix"}:
        errors.append('type must be "improvement" or "bug_fix"')
    if not isinstance(release_note, str) or not release_note.startswith("- "):
        errors.append('release_note must be a string that starts with "- "')
    if isinstance(release_note, str) and release_note.rstrip().endswith("."):
        errors.append("release_note must not end with a period")
    if not isinstance(needs_review, bool):
        errors.append("needs_review must be a boolean")
    if not isinstance(reason, str):
        errors.append("reason must be a string")

    if isinstance(release_note, str):
        for link in expected_links:
            if link and link not in release_note:
                errors.append(f"release_note is missing expected link: {link}")
        for contributor in contributors:
            expected = f"@[{contributor}](https://github.com/{contributor})"
            if contributor and expected not in release_note:
                errors.append(f"release_note is missing contributor: {contributor}")

    if errors:
        return None, errors
    return (
        GeneratedNote(
            note_type=str(note_type),
            release_note=str(release_note).strip(),
            needs_review=bool(needs_review),
            reason=str(reason).strip(),
        ),
        [],
    )
