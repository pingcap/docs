# Repo Conventions

This file captures the repository-specific rules that agents should follow in `pingcap/docs`.

## Repository scope

- `pingcap/docs` stores the English TiDB documentation source.
- `pingcap/docs-cn` stores the Chinese documentation source.
- This repository is the source for the English TiDB documentation published on the PingCAP documentation website.
- TiDB documentation and TiDB Cloud documentation do not always follow the same maintenance model. Do not assume they use the same branch, scope, or publication rules.

## Repository versions and branches

- The `master` branch tracks the latest development version of TiDB documentation.
- Published TiDB documentation is maintained in the corresponding `release-<version>` branches.
- Archived documentation is no longer maintained and should not receive normal documentation updates.
- By default, target `master` unless the change clearly belongs to a maintained release branch.
- Preserve branch intent. Do not treat release-branch behavior as the default development behavior, and do not move dev-only content into release branches.

## Choosing affected versions

Follow the repository's affected-version model when proposing or reviewing changes.

- By default, affected versions should be `master` only for documentation enhancements, missing-content additions, wording fixes, refactors within a topic, and general corrections that are not tied to a specific released behavior.
- Choose the affected release branch or branches together with `master` when the change involves version-specific behavior, compatibility changes, changed default values, changed system variable behavior, display fixes, or broken-link fixes in published docs.
- If a change applies to multiple maintained versions, prefer the latest applicable branch and use cherry-pick labels instead of opening parallel PRs by default.
- If most of the change can be cherry-picked but some branches require different wording or follow-up edits, account for version-specific follow-up work and the relevant reminder labels.

## Cherry-pick and branch-follow-up conventions

- Use the repository's cherry-pick label workflow instead of inventing a custom multi-branch process.
- If a change applies only to one documentation version, use that branch directly and do not add unnecessary cherry-pick labels.
- If a change applies to multiple documentation versions, prefer a single PR on the latest applicable branch and rely on cherry-pick labels for the remaining maintained versions.
- If branch-specific differences are expected, flag that clearly so reviewers know follow-up edits are required in the cherry-picked PRs.

## Repository layout and navigation

- Use the existing repository structure and nearby documents as the primary guide for where new content should live.
- New navigable documents usually require a matching update in the appropriate `TOC.md` file.
- When a document is added, removed, moved, or renamed, check whether related TOC files, aliases, links, and cross-document references also need updates.
- Reuse existing document patterns in the same area before introducing a new structure.

## TiDB Cloud conventions

- In this repository, TiDB Cloud documentation is maintained in the `release-8.5` branch for content reuse.
- To contribute to TiDB Cloud documentation, make sure the PR is based on `release-8.5`.
- Use `TOC-tidb-cloud.md` and `TOC-tidb-cloud-*.md` to understand which documents are TiDB Cloud-only and which TiDB documents are reused by TiDB Cloud.
- If a path in `TOC-tidb-cloud.md` or `TOC-tidb-cloud-*.md` starts with `/tidb-cloud/`, it is TiDB Cloud-only content.
- If a path in `TOC-tidb-cloud.md` or `TOC-tidb-cloud-*.md` does not start with `/tidb-cloud/`, it is reused from TiDB documentation.
- Be careful with `CustomContent` tags such as `<CustomContent platform="tidb">` and `<CustomContent platform="tidb-cloud">`. Do not change, remove, or expand them casually, because they control platform-specific rendering behavior.
- When editing shared TiDB and TiDB Cloud content, verify whether the change applies to both platforms or only one.

## Contribution model

- New documents should follow the templates in `resources/doc-templates/` when applicable.
- Keep PR descriptions compatible with `.github/pull_request_template.md`.
- Keep changes scoped to the requested task. Do not broaden a focused doc update into unrelated cleanup.
- Prefer existing repository workflows, labels, and conventions over ad hoc alternatives.
- When contributing diagrams, follow the existing diagram-style guidance rather than introducing a new visual style.

## File naming rules

- Use file names that briefly describe the document content, for example, `destroy-tidb-cluster.md`.
- Keep file names concise and general. Avoid overly specific wording that might require frequent renaming and cause unnecessary URL changes.
- Except for special files such as `TOC.md`, `CONTRIBUTING.md`, and `README.md`, use lowercase letters only in file names.
- If a file name contains multiple English words, separate them with hyphens (`-`).
- Do not use underscores (`_`) in file names.
- Use lowercase file extensions only.
- Markdown files must use the `.md` extension.

## Content boundaries

- Preserve product behavior, version numbers, links, anchors, file intent, and branch intent unless the task explicitly requires changing them.
- Do not silently change technical meaning while improving wording.
- Avoid changing commands, code samples, UI strings, configuration names, API fields, JSON, EBNF content, or generated helper files unless the task directly requires it or they are factually wrong.
- When editing syntax-related content, be careful not to break EBNF or other structured source formats.
- Keep cross-repo translation traceability when work maps between `docs` and `docs-cn`.
- When a translation-related task maps content across repositories, preserve the source PR relationship, terminology intent, and affected-file mapping.

## Front matter and document metadata

- Preserve existing front matter structure unless the task requires a metadata change.
- When front matter is present, keep `title`, `summary`, `aliases`, and other metadata aligned with the document content.
- If a file is moved or renamed, check whether `aliases` should be updated to preserve inbound links.
- Do not add or remove metadata fields casually. Follow existing patterns in nearby documents.

## Linking and cross-document consistency

- Preserve repository-relative absolute links when that is the repository convention.
- When editing a document that summarizes or references other docs, check whether those related docs also need updates.
- If a term, version statement, feature behavior, workflow, or compatibility note changes in one place, check nearby overview, task, reference, and release-note content for possible follow-up updates.
- When changing headings, verify whether anchors, intra-repo links, TOC entries, or external references might be affected.

## Validation habits

Use existing repository checks instead of inventing new ones.

- `./scripts/markdownlint <files>` for Markdown formatting
- `./scripts/verify-links.sh` for link validation when links, anchors, moved files, or renamed files are involved
- targeted repository scripts when the task touches glossary terms, keywords, anchor conflicts, or other specialized checks

If a full check is too expensive for the task, validate the files you changed and any directly affected TOC or link targets.

## Existing helpers

Look for established scripts and workflows before automating from scratch.

Use them as references for expected behavior, even when local credentials, permissions, or secrets prevent direct execution.

## Agent behavior in this repository

- Read the shared guidance in `.ai/shared/` before making non-trivial changes.
- Use a matching skill in `.ai/skills/` when the task is workflow-specific.
- Prefer minimal, targeted edits over broad rewrites.
- Reuse existing wording, terminology, and document structure when they are already correct.
- When unsure, check nearby docs, templates, and repository patterns before introducing a new approach.
