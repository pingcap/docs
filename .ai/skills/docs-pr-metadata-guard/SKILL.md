---
name: docs-pr-metadata-guard
description: Use when creating or editing pull requests in pingcap/docs so the PR template sections, version checkboxes, related-link fields, HTML comments, and description structure stay intact. Trigger on tasks involving PR creation, PR body updates, version selection, cherry-pick label decisions, or translating a PR from docs-cn.
---

# Docs PR Metadata Guard

Use this skill for `pingcap/docs` GitHub pull request metadata work. The goal is to preserve the repository-required PR description structure while editing only the mutable fields.

Before changing a PR body, read `.github/pull_request_template.md`.

## Workflow

1. Write PR titles and descriptions in English.
2. For a new PR, start from `.github/pull_request_template.md` instead of writing the body from scratch.
   - Copy the template into a local Markdown file and fill in the mutable fields.
   - Submit with `gh pr create --body-file <local-file>`, or use `gh pr create -T .github/pull_request_template.md` to let `gh` load the template as the starting body text (the `-T` / `--template` flag for `gh pr create` takes a file path).
   - Review the local file against the template before calling `gh`.
3. Fill in the required sections with concrete information.
   - **What is changed, added or deleted? (Required)**: describe what changed and why in clear, specific language. Do not leave this blank or fill it with a generic placeholder.
   - **Which TiDB version(s) do your changes apply to? (Required)**: check at least one version checkbox. Follow the affected-version rules in `.ai/shared/repo-conventions.md`:
     - Default to `master` only for general improvements, wording fixes, missing-content additions, and corrections not tied to a specific released behavior.
     - Check the affected release branch(es) together with `master` when the change involves version-specific behavior, compatibility changes, changed defaults, or fixes in published docs.
   - **What is the related PR or file link(s)?**: fill in the translation source link under `This PR is translated from:` when the PR is a translation from `docs-cn`. Fill in other reference links such as product PRs, issues, or related doc PRs under `Other reference link(s):`.
   - **AI agent involvement**: when this section is present in the template, keep it intact. Check its checkbox only when the changes were primarily made by an AI agent on behalf of the PR author; otherwise leave it unchecked.
   - **Do your changes match any of the following descriptions?**: check all that apply. If the change needs different wording on another branch, check `Need modification after applied to another branch` and comment `/label version-specific-changes-required`.
4. Choose the correct base branch.
   - Default to `master` for most documentation PRs.
   - Use `release-8.5` for TiDB Cloud documentation changes (see `.ai/shared/repo-conventions.md` for TiDB Cloud conventions).
   - Use a specific `release-X.Y` branch when the change is scoped to a single published version and does not apply to `master`.
5. For an existing PR, update only the mutable sections.
   - Safe targets: the description text under "What is changed, added or deleted?", the version checkboxes, the related-link fields, and the description checkboxes.
   - Do not rename headings, reorder sections, or rewrite the template wholesale.
6. Preserve hidden HTML comments exactly.
   - Keep `<!--Tell us what you did and why.-->` unchanged.
   - Keep `<!-- Fill in "x" in [] to tick the checkbox below.-->` unchanged.
   - Keep `<!--Reference link(s) will help reviewers review your PR quickly.-->` unchanged.
   - Keep `<!-- If yes, please comment "/label version-specific-changes-required" below to trigger the bot to add the label. -->` unchanged.
   - Do not delete or rewrite any template comment that explains contributor behavior or bot behavior.
7. Preserve the "Tips for choosing the affected version(s)" guidance block.
   - The bold tips paragraph and the `CONTRIBUTING.md` link between the version heading and the checkboxes are part of the template structure. Do not delete, rewrite, or move them.
8. Handle the first-time contributors' checklist correctly.
   - If the contributor is not a first-time contributor, remove the entire "First-time contributors' checklist" section as the template instructs.
   - If the contributor is a first-time contributor, keep the section and check the CLA checkbox after signing.
9. Prefer file-based edits for GitHub metadata.
   - Materialize the intended PR body into a local Markdown file.
   - Review that file against the PR template before calling `gh`.
10. After any PR body update, re-read the PR to verify the structure is intact.

## Version checkbox rules

The version checkboxes in the PR template follow a specific order from newest to oldest. When filling them in:

- Do not add or remove version lines. The template defines the canonical list.
- Do not reorder the version lines.
- Check only the versions where the change should apply.
- If a version is not in the template list, do not invent a new checkbox line.

## Cherry-pick and label conventions

- When a change applies to multiple versions, prefer a single PR on the latest applicable branch and use cherry-pick labels for remaining maintained versions.
- Cherry-pick labels follow the pattern `needs-cherry-pick-release-X.Y` (e.g. `needs-cherry-pick-release-8.5`, `needs-cherry-pick-release-7.5`). There is also `needs-cherry-pick-master` for cherry-picks to master.
- If branch-specific wording differences are expected, check `Need modification after applied to another branch` and add the `requires-version-specific-changes` label so cherry-pick reviewers know follow-up edits are required.
- Use the repository's cherry-pick label workflow. Do not invent a custom multi-branch process.
- Common non-cherry-pick labels for PRs:
    - `type/bugfix`, `type/enhancement`, `type/refactor`, `type/compatibility-or-feature-change` for change type.
    - `area/*` labels (e.g. `area/tidb-cloud`, `area/planner`, `area/br`) for the documentation area.
    - `translation/from-docs-cn` when the PR is translated from a `docs-cn` PR.
    - `translation/welcome` to invite community translation; `translation/no-need` when translation is not needed.

## Quick checks

- The PR body contains the "What is changed, added or deleted? (Required)" heading with a non-empty description below it.
- At least one version checkbox is checked under "Which TiDB version(s) do your changes apply to? (Required)".
- The version checkbox section preserves the template's canonical version list and order.
- The "Tips for choosing the affected version(s)" paragraph and the `CONTRIBUTING.md` link are present between the version heading and the checkboxes.
- The related-link fields (`This PR is translated from:` and `Other reference link(s):`) are present, even if left at their default values.
- The `AI agent involvement` section is present when defined by the template, and its checkbox accurately reflects whether an AI agent primarily made the changes on the PR author's behalf.
- The "Do your changes match any of the following descriptions?" section is present with its checkboxes intact.
- The first-time contributors' checklist is either correctly filled in or removed entirely as instructed.
- The base branch matches the change scope: `master` by default, `release-8.5` for TiDB Cloud, or a specific `release-X.Y` for version-scoped fixes.
