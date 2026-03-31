# AI Collaboration Guide

This directory stores repo-local guidance for AI agents working in `pingcap/docs`.

## Structure

- `.ai/shared/`: reusable repo policy, writing guidance, and translation guidance
- `.ai/skills/`: workflow-specific instructions for recurring tasks in this repo

## Shared guidance

Read only the files that apply to the task:

- `.ai/shared/repo-conventions.md`: repository scope, branch rules, file naming, TOC expectations, TiDB Cloud boundaries, and validation habits
- `.ai/shared/writing-style.md`: document structure, wording, formatting, headings, front matter, and repo-compatible writing style
- `.ai/shared/translation-rules.md`: EN -> ZH translation constraints, traceability, structure preservation, and workflow expectations
- `.ai/shared/translation-terms.md`: quick terminology reference for frequent translation terms

Use `resources/terms.md` when terminology is uncertain or not covered by the quick reference.

## Current skills

- `.ai/skills/review-doc-pr/`: review documentation PRs and Markdown diffs for factual accuracy, user usefulness, completeness, version fit, related-doc impact, links, and style
- `.ai/skills/create-or-update-zh-translation-pr/`: create a new docs translation PR or update an existing one by combining repo-local scripts with minimal-edit translation rules and incremental source-diff handling
- `.ai/skills/writing-doc-summaries/`: write or update the `summary` front matter field in a document following the repo's 115-145 character SEO-friendly sentence rules

The translation skill includes bundled scripts under `.ai/skills/create-or-update-zh-translation-pr/scripts/` for:

- preparing structured translation inputs from a source PR
- preparing structured translation inputs from either a full source PR or an update commit range
- creating or reusing the translation branch
- applying high-confidence deterministic updates before AI editing
- committing, pushing, and creating or updating the PR with `gh`

## How to use it

Use progressive loading so the task stays grounded but efficient:

1. Start with the relevant shared guidance.
2. Load a skill only when the task matches that workflow.
3. If the selected skill includes bundled scripts, prefer the scripts over retyping ad hoc commands.
4. Validate the files you changed with the repo's existing checks when practical.

Keep the task grounded in the existing repository rules, templates, scripts, and workflows.
