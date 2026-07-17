---
name: create-or-update-zh-translation-pr
description: Create or update a zh translation PR from pingcap/docs to pingcap/docs-cn by using repo-local scripts to prepare change-unit translation inputs, apply minimal edits to the existing Chinese files, and create or update the target PR with the same branch, title, body, and label rules used in gh-util.user.js.
---

# Create or Update ZH Translation PR

Use this skill when the user asks to create a Chinese translation PR in `pingcap/docs-cn` from an English doc change in `pingcap/docs`, or when they want to sync later source-PR updates into an existing translation PR.

## Default behavior

Do not stop to ask whether to run the scripts referenced in this skill.

- `create` mode: use it when the user gives a source PR URL and wants a new translation PR.
- `update` mode: use it when the user gives an existing translation PR URL plus a source update range and wants to sync only the new source changes into that translation PR.
- Use the source PR branch name to create the target branch as `translate/<source-head-branch>`.
- In `update` mode, do not ask for the source PR URL if it can be inferred from the target translation PR body.
- Only ask the user if a decision would materially change the output and cannot be resolved from the repo, the PR metadata, or the generated translation inputs.

## Load this context first

- `.ai/shared/repo-conventions.md`
- `.ai/shared/translation-rules.md`
- `.ai/shared/translation-terms.md`
- `resources/terms.md` when terminology is uncertain

## Preconditions

- `gh auth status` succeeds.
- `jq` is available.
- A writable local clone of `docs-cn` exists.
- In that clone, `origin` points to your fork and `upstream` points to `pingcap/docs-cn`.

## Required inputs

### Create mode

Provide:

- the source PR URL
- the local `docs-cn` clone path

Example:

```text
Please create a translation PR for https://github.com/pingcap/docs/pull/22583 using /path/to/docs-cn.
```

### Update mode

Provide:

- the target translation PR URL
- the source update range
- the local `docs-cn` clone path

`source update range` can be:

- a single source commit SHA
- a source commit range in `<base>..<head>` form
- a source commit URL like `https://github.com/pingcap/docs/pull/<pr-number>/commits/<sha>`
- Prefer the full source commit URL when you have it, because it already identifies both the source PR and the exact increment to sync.

In `update` mode, infer the source PR URL in this order:

1. from the source commit URL when the input uses that form
2. from the target translation PR body line `This PR is translated from: ...`

Only ask for the source PR URL if both inference paths fail.

When the target translation PR body references multiple source PR URLs, treat that body line as fallback context only. Use the explicit update input first.

Example:

```text
Please sync https://github.com/pingcap/docs-cn/pull/12345 with source update range abc1234..def5678 using /path/to/docs-cn.
```

## Use the bundled scripts

Prefer the scripts in `.ai/skills/create-or-update-zh-translation-pr/scripts/` over retyping long commands:

- `prepare_translation_inputs.py`: fetch PR and commit metadata with `gh`, apply the `gh-util.user.js` title/body/label rules, and generate `translation-input.json` plus `translation-meta.env`
- `create_translation_branch.sh`: sync the fork base branch with upstream, create or reuse the translation branch with `gh`, and check it out locally
- `apply_translation_units.py`: apply only high-confidence deterministic updates to the target files and write a report of what still needs AI or human attention
- `create_translation_pr.sh`: stage only the target files, commit, push, create a new translation PR, or update the existing translation PR with `gh`

These scripts are the preferred path because they are deterministic and easier to reuse correctly than ad hoc shell snippets.

## Processing strategy

Do not process every changed file the same way.

- Modified Markdown files: build change units, read the existing Chinese target file, and apply the smallest necessary edits.
- Newly added Markdown files: translate in batches that respect section boundaries instead of sending the whole file at once.
- Deleted files: remove the matching target files directly. No AI is needed.
- `TOC.md` and `keywords.md`: use structure-aware updates, not generic section translation.
- Image files: copy, replace, or delete the binary files directly. Do not send image diffs to the LLM.
- `.ai` files, `tidb-cloud/` files, and `TOC-tidb-cloud-*.md` files: skip them for `docs -> docs-cn` unless the user explicitly asks otherwise.
- Large translation inputs: if the total changed source content is too large for one LLM request, split the work by file or by section batches before translating.

## Step 1. Prepare translation inputs

### Create mode

Run:

```bash
python3 .ai/skills/create-or-update-zh-translation-pr/scripts/prepare_translation_inputs.py \
  --mode create \
  --source-pr-url "<source-pr-url>" \
  --target-repo-dir "<path-to-docs-cn>"
```

### Update mode

Run:

```bash
python3 .ai/skills/create-or-update-zh-translation-pr/scripts/prepare_translation_inputs.py \
  --mode update \
  --target-translation-pr-url "<target-translation-pr-url>" \
  --source-update-range "<commit-sha-or-base..head>" \
  --target-repo-dir "<path-to-docs-cn>"
```

This script writes all intermediate artifacts into a temporary `$WORKDIR`, including:

- `translation-input.json`
- `translation-body.md`
- `translation-labels.txt`
- `target-files.txt`
- `translation-meta.env`

Script behavior in `update` mode:

- Do not block on the source PR having `translation/done`. That label only prevents duplicate `create` flows.
- If the source update input is a commit URL, extract the source PR URL from it before looking at the target translation PR body.
- If the target translation PR body contains multiple source PR URLs, use it only as fallback metadata, not as the primary selector for the update scope.

`translation-input.json` is a change-unit mapping, not just a section dump. It includes:

- `mode`
- `source_pr`
- `source_update`
- `target_translation_pr` in update mode
- `source_file`
- `target_file_path`
- `status`
- `processing_strategy`
- `patch`
- `changes[].action`
- `changes[].section_path`
- `changes[].old_source_excerpt`
- `changes[].new_source_excerpt`
- `changes[].source_section_excerpt`
- `changes[].target_section_excerpt`

## Step 2. Create or reuse the translation branch

Run:

```bash
bash .ai/skills/create-or-update-zh-translation-pr/scripts/create_translation_branch.sh \
  "$WORKDIR/translation-meta.env"
```

This script uses `gh` for the remote branch operations and then prepares the local `docs-cn` worktree on the translation branch.

- If the remote branch does not exist, it creates it from the synced upstream base branch.
- If the remote branch already exists, it reuses it instead of failing.
- Run this step before editing translated files so branch setup does not interfere with local modifications.

## Step 3. Apply deterministic updates first

Run:

```bash
python3 .ai/skills/create-or-update-zh-translation-pr/scripts/apply_translation_units.py \
  --meta-env "$WORKDIR/translation-meta.env" \
  --write
```

This script is intentionally conservative. It should only auto-apply changes when it can verify them locally, such as:

- literal block replacements inside the matched target section
- code, SQL, path, shortcode, and command insertions anchored by unchanged nearby literals
- token replacements like backticked identifiers or stable paths inside an already matched section

It writes `translation-apply-report.json` into `$WORKDIR`.

- If a change is not clearly safe, the script leaves it untouched and records it as pending.
- Do not try to force the script to handle natural-language paragraph rewrites. Leave those for the next step.

## Step 4. Apply the remaining translation as minimal edits

Use `translation-input.json` as the source of truth for what changed, but do not treat it as the only context. For each target file:

1. Read the existing Chinese target file in `docs-cn`.
2. Read the change units for that file from `translation-input.json`.
3. Reuse the existing Chinese wording wherever it is still correct.
4. Translate only the new or changed source content.
5. Make the smallest necessary edits to the existing Chinese file instead of re-translating the whole section.

When applying a change unit:

- Prefer updating the exact sentence, list item, code block, or short paragraph that corresponds to the English change.
- Use `section_path`, `source_section_excerpt`, and `target_section_excerpt` together to locate the right place.
- Preserve unchanged Chinese content around the edit.
- If the target section cannot be matched exactly, search the target file for the closest translated paragraph before rewriting anything larger.
- For small source diffs, unchanged target lines should remain byte-for-byte identical whenever possible.
- If your draft introduces a much larger target diff than the source change warrants, fall back to a narrower edit or keep the original Chinese unchanged.
- Prefer deterministic replacements for obvious literal changes such as link text, config names, file paths, or short option names.

### Special cases

- `TOC.md`: match lines by link target and nearby context, then translate only the visible link text when needed.
- `keywords.md`: match and update only the affected letter blocks under `TabsPanel`, not the full file.
- Added Markdown files: translate in section-sized batches, typically around 200 lines or less per request.
- Deleted files: delete the target file and stage the deletion later.
- Added or modified images: copy the binary file to the same target path.
- Deleted images: remove the matching target file.

Start from the deterministic script output:

1. Read `translation-apply-report.json`.
2. Focus only on the pending changes.
3. Reuse any deterministic edits that were already applied correctly.
4. Translate only the remaining new or changed source content.

## Step 5. Create or update the translation PR

Run this only after the translated target files are ready:

```bash
bash .ai/skills/create-or-update-zh-translation-pr/scripts/create_translation_pr.sh \
  "$WORKDIR/translation-meta.env"
```

- In `create` mode, this creates a new translation PR.
- In `update` mode, this commits and pushes the new translation changes to the existing translation branch and updates the existing translation PR metadata.
- In `update` mode, preserve existing related-source references in the target translation PR body unless the current sync explicitly needs to replace them.
- In `update` mode, stage only the files listed in `target-files.txt` and do not widen the update to unrelated local changes.

This script intentionally stages only the files listed in `target-files.txt`.

## Output expectations

When you finish the task, report the following information:

- The mode you used
- The source PR URL
- The source update range in update mode
- The generated `translation-input.json` path
- The generated `translation-apply-report.json` path
- The translated target files
- The created or updated PR URL
- Any terminology or branch issues that still need human review
