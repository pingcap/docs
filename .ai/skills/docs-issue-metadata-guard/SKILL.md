---
name: docs-issue-metadata-guard
description: Use when creating or editing GitHub issues in pingcap/docs so issue templates, required fields, scope boundaries, and labels stay consistent with repository workflow. Trigger on tasks involving issue creation, error reports, change requests, questions, label selection, or searching for existing issues before filing a new one.
---

# Docs Issue Metadata Guard

## Overview

Use this skill for `pingcap/docs` GitHub issue metadata work.
The goal is to preserve issue-template structure, scope discipline, and searchable issue descriptions.

Before creating or editing an issue, read the matching file under `.github/ISSUE_TEMPLATE/`.

This repository has three issue templates and disables blank issues (`blank_issues_enabled: false` in `config.yml`). Every new issue must use one of the templates.

## Issue Templates

| Template | File | Use when |
|---|---|---|
| Error Report | `error-report.md` | Typos, grammatical errors, terminology misuse, ambiguity, broken formatting, incorrect code samples, wrong links |
| Change Request | `change-request.md` | Suggesting new content, restructuring, adding missing information, improving existing documentation |
| Question | `question.md` | Usage questions about documentation that are not answered in existing docs or discussions |

## Scope Boundary

All three templates include the same scope reminder:

> This repository is ONLY used to solve issues related to DOCS.

Enforce this boundary:

- Do not file product bug reports, feature requests, or technical support questions in this repository.
- Redirect product issues to the appropriate repository under `github.com/pingcap/`.
- Redirect technical support questions to the TiDB community channels (Discord, Slack).
- If an issue mixes a doc problem with a product problem, separate them: file the doc part here and note where the product part should go.

## Workflow

1. Write issue titles and descriptions in English.
2. Search existing issues first before filing a new one.
   - Check open and closed issues for duplicates or related discussions.
   - If an existing issue covers the same problem, comment on it instead of creating a new one.
3. Choose the correct issue template based on the issue type.
   - Do not write the body from scratch. Start from the matching template.
   - The repository disables blank issues, but `gh issue create` does not enforce this — the agent must self-enforce template usage.
4. When using `gh issue create`:
   - Use `--template "Error Report"`, `--template "Change Request"`, or `--template "Question"` to select the template (the `-T` / `--template` flag for `gh issue create` takes a template **name**, not a file path).
   - Alternatively, copy the template body (everything below the YAML front matter `---` block) into a local file and use `--body-file <local-file>`. The YAML front matter (`name:` and `about:`) is GitHub metadata and does not appear in the issue body.
   - Always add `--label` flags explicitly — `gh issue create` does not auto-apply labels from templates.
5. Fill in all template fields with concrete information.

### Error Report

Fill in both required fields:

- **What is the URL/path of the document related to this issue?** — provide the published doc URL or the repository file path. Do not leave this blank.
- **How would you like to improve it?** — describe the specific error and the expected correction. Include the current incorrect text and the proposed fix when possible.

### Change Request

Fill in all three sections:

- **Describe what you find is inappropriate or missing in the existing docs.** — be specific about which document, section, or topic is affected.
- **Describe your suggestion or addition.** — explain what should be changed or added and why it helps users.
- **Provide some reference materials (such as documents and websites) if you could.** — link to product PRs, release notes, related docs, or external references that support the request. Write "N/A" if no references are available; do not delete the section.

### Question

Before filing:

- Search existing Stack Overflow questions, Google results, and open/closed GitHub issues as the template instructs.
- Read the relevant docs in `pingcap/docs` and `pingcap/docs-cn`.

Then describe the question clearly, including what you searched and why the existing documentation did not answer it.

## Editing Existing Issues

1. Fetch the current title, body, and labels first.
2. Patch only the intended sections and preserve untouched sections, metadata, and still-valid context.
3. Do not rewrite the issue body from scratch.
4. Preserve the template structure: keep the headings and numbered prompts intact.

## Preserving Template Structure

- Keep the hidden HTML comment block (scope reminder and community links) unchanged.
- Keep the template heading (`## Error Report`, `## Change Request`, or `## Question`) unchanged.
- Keep the numbered prompts or instruction text in each template unchanged.
- Do not merge, reorder, or rename template sections.

## Labels

- Apply labels explicitly when creating or editing issues.
- For issues created with `gh issue create`, add labels via `-l` flag since the CLI does not auto-apply template labels.
- For existing issues, use `gh issue edit` to update labels.
- Label taxonomy in this repository:
  - **Type labels**: `type/bug`, `type/enhancement`, `type/feature-request`, `type/question`, `type/refactor`. Pick the one that matches the issue intent.
  - **Area labels**: `area/*` labels identify the documentation area (e.g. `area/tidb-cloud`, `area/planner`, `area/br`, `area/ticdc`, `area/dm`, `area/tidb-lightning`, `area/deploy-upgrade-maintain`, `area/security`, `area/general`). Add at least one when the issue clearly targets a specific area.
  - **Priority labels**: `priority/P1`, `priority/P2`. Use when the issue affects published documentation accuracy or user-facing correctness.
  - **Workflow labels**: `good first issue`, `help wanted` for community contribution signaling.
- If label permissions are missing, add a comment with `Suggested labels: ...` so maintainers can apply them.

## File-based Editing

- Materialize the intended issue body in a local Markdown file.
- For new issues, review that file against the matching issue template before calling `gh`.
- For existing issues, diff the patched body against the current issue body before calling `gh`.

## Quick Checks

- The issue title and body are in English.
- The issue uses one of the three available templates (Error Report, Change Request, or Question) — blank issues are not allowed.
- The issue stays within the docs-only scope and does not mix in product bugs or feature requests.
- All template fields are filled in with concrete information, not generic placeholders.
- The template headings, numbered prompts, and HTML comments are preserved.
- Existing issue edits preserve untouched sections and metadata outside the intended patch.
- The issue carries appropriate labels, or a `Suggested labels: ...` comment is present when label permissions are missing.
