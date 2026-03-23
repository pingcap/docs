# Repository Agents Guide

This repository is the source for the English TiDB documentation maintained in `pingcap/docs`.

Use this file as the entrypoint for agent work in this repository.

## Working approach

Before making changes:

1. Use `.ai/AI-README.md` as the map of the repo-local AI guidance.
2. Read the relevant shared guidance in `.ai/shared/`.
3. Use a matching skill in `.ai/skills/` when the task is workflow-specific.
4. Keep edits minimal and scoped to the requested task.
5. Reuse existing wording, structure, and terminology unless there is a clear reason to change them.

When rules conflict, follow this priority order:

1. Direct user instructions
2. Repository rules in this file
3. Task-specific instructions in the selected skill
4. Shared guidance in `.ai/shared/`
5. General writing preferences

## Start here

Read `.ai/AI-README.md` first when you need the current layout of repo-local AI guidance.

Then read the shared guidance in `.ai/shared/` before making changes:

- `.ai/AI-README.md`
- `.ai/shared/repo-conventions.md`
- `.ai/shared/writing-style.md`
- `.ai/shared/translation-rules.md` when the task involves EN -> ZH translation
- `.ai/shared/translation-terms.md` when the task involves terminology decisions for translation

Use `resources/terms.md` when additional product terminology context is needed.

## Use the repo skills

Use the workflow-specific skills in `.ai/skills/` when they match the task:

- `review-doc-pr`: review Markdown diffs, doc PRs, wording, structure, factual accuracy, and possible cross-file impact
- `create-or-update-zh-translation-pr`: create or update an EN -> ZH translation PR that maps an English docs change or incremental source update to `pingcap/docs-cn`, using the bundled scripts in `.ai/skills/create-or-update-zh-translation-pr/scripts/` when applicable

If no existing skill matches the task, follow this file plus the shared guidance and keep the change narrowly scoped.

## Repository expectations

- Prefer the existing templates in `resources/doc-templates/` when creating new documents or reshaping existing ones.
- Preserve the repository's Markdown, heading, list, link, and front matter conventions.
- Use lowercase file names and separate words with hyphens, for example, `x-y-z.md`, unless the existing file path already follows a different required pattern.
- Reuse existing approved terminology and phrasing whenever possible.
- Prefer consistency with surrounding documents over stylistic rewrites.
- Respect the repository's version and branch rules, including release branches and TiDB Cloud branch constraints.
- Prefer existing scripts, workflows, and repository patterns over ad hoc reinvention.
- When a selected skill includes bundled scripts, prefer those scripts over rewriting the same workflow inline.

## Content guardrails

- Do not change technical meaning unless the task explicitly requires it.
- Do not silently rewrite commands, code samples, configuration names, API fields, UI strings, or JSON unless they are part of the requested task or are clearly incorrect.
- Do not expand the scope from a local fix into a broad rewrite unless the user asks for that.
- Do not introduce new terminology when an established term already exists in the repository or shared terminology references.
- When editing translated-content workflows, preserve existing English source intent and terminology rather than paraphrasing freely.

## Translation-related guardrails

When the task involves translation or translation review:

- Follow `.ai/shared/translation-rules.md` and `.ai/shared/translation-terms.md`.
- For translation PR creation or update workflows, prefer the script-backed process in `.ai/skills/create-or-update-zh-translation-pr/`.
- Prefer updating the existing translation with the smallest necessary change instead of retranslating entire sections.
- Preserve structure, headings, lists, code blocks, links, and note/admonition semantics.
- Reuse existing translated terminology when it is still correct.
- Flag terminology uncertainty explicitly instead of guessing.

## Validation

When the task changes Markdown, run relevant checks when practical:

- `./scripts/markdownlint <files>`
- `./scripts/verify-links.sh` for link-sensitive changes

If a full-repo check is too expensive for the task, validate only the files you changed.

## Commit and PR boundaries

- Do not commit, push, create branches, or open PRs unless the user explicitly asks for it.
- Before any write action that affects Git history or GitHub state, make sure the requested scope is clear.
- When reporting completed work, summarize changed files, key decisions, and any issues that still need human review.

## Scope discipline

Keep changes scoped to the requested task and avoid mutating unrelated files.

When a requested change might affect other docs, note the possible cross-file impact and only update additional files when the user asks or the selected skill explicitly requires it.
