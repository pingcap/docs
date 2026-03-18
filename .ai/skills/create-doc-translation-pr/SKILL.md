---
name: create-doc-translation-pr
description: Translate a docs pull request from pingcap/docs to pingcap/docs-cn by using repo-local scripts to prepare change-unit translation inputs, apply minimal edits to the existing Chinese files, and create the target PR with the same branch, title, body, and label rules used in gh-util.user.js.
---

# Create Doc Translation PR

Use this skill when the user asks to create a Chinese doc translation PR in `pingcap/docs-cn` according to a source language (English) doc PR in `pingcap/docs`.

## Default behavior

Do not stop to ask whether to run scripts mentioned in the skill.

- Proceed with the standard `docs -> docs-cn` flow by default.
- Use the source PR branch name to create the target branch as `translate/<source-head-branch>`.
- Use the same relative target file path unless the repo structure clearly requires a different path.
- Only ask the user if a decision would materially change the output and cannot be resolved from the repo, the PR, or the generated translation inputs.

## Load this context first

- `.ai/shared/repo-conventions.md`
- `.ai/shared/translation-rules.md`
- `.ai/shared/translation-terms.md`
- `resources/terms.md` when terminology is uncertain

## Preconditions

- `gh auth status` succeeds.
- `jq` is available.
- A writable local clone of `docs-cn` exists. Ask the user to provide the path to the clone when they don't have one.
- In that clone, `origin` points to your fork and `upstream` points to `pingcap/docs-cn`.

## Use the bundled scripts

Prefer the scripts in `.ai/skills/create-doc-translation-pr/scripts/` over retyping long commands:

- `prepare_translation_inputs.py`: fetch source PR info with `gh`, apply the `gh-util.user.js` title/body/label rules, and generate the translation inputs under `$WORKDIR`
- `create_translation_branch.sh`: sync the fork base branch with upstream, create the translation branch with `gh`, and check it out locally
- `apply_translation_units.py`: apply only high-confidence deterministic updates to the target files and write a report of what still needs AI or human attention
- `create_translation_pr.sh`: stage only the target files, commit, push, create the PR with `gh`, and add labels

These scripts are the preferred path because they are deterministic and easier to reuse correctly than inline shell snippets.

## Processing strategy

Do not process every changed file the same way.

- Modified Markdown files: build change units, read the existing Chinese target file, and apply the smallest necessary edits.
- Newly added Markdown files: translate in batches that respect section boundaries instead of sending the whole file at once.
- Deleted files: remove the matching target files directly. No AI is needed.
- `TOC.md` and `keywords.md`: use structure-aware updates, not generic section translation.
- Image files: copy, replace, or delete the binary files directly. Do not send image diffs to the LLM.
- `.ai` files, `tidb-cloud/` files, and `TOC-tidb-cloud-*.md` files: skip translation of them for `docs -> docs-cn` unless the user explicitly asks otherwise, because these docs will be translated into Chinese in another workflow.
- Large translation inputs: if the total changed source content is too large for one LLM request, split work by file or by section batches before translating.

## Step 1. Prepare translation inputs

Run:

```bash
python3 .ai/skills/create-doc-translation-pr/scripts/prepare_translation_inputs.py \
  --source-pr-url "<source-pr-url>"
  --target-repo-dir "<the path to the local clone of `docs-cn`>"
```

This script writes all intermediate artifacts into a temporary `$WORKDIR`, including:

- `translation-input.json`
- `translation-body.md`
- `translation-labels.txt`
- `target-files.txt`
- `translation-meta.env`

### What `translation-input.json` contains

This file is a change-unit mapping, not just a section dump. It includes:

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
bash .ai/skills/create-doc-translation-pr/scripts/create_translation_branch.sh \
  "$WORKDIR/translation-meta.env"
```

This script uses `gh` for the remote branch operations and then prepares the local `docs-cn` worktree on the translation branch.

- If the remote branch does not exist, it creates it from the synced upstream base branch.
- If the remote branch already exists, it reuses it instead of failing, so reruns are easier.
- Run this step before editing translated files so branch setup does not interfere with local modifications.

## Step 3. Apply deterministic updates first

Run:

```bash
python3 .ai/skills/create-doc-translation-pr/scripts/apply_translation_units.py \
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

## Step 5. Create the translation PR

Run this only after the translated target files are ready:

```bash
bash .ai/skills/create-doc-translation-pr/scripts/create_translation_pr.sh \
  "$WORKDIR/translation-meta.env"
```

This script intentionally stages only the files listed in `target-files.txt`.

## Output expectations

When you finish the task, report:

- the source PR URL
- the generated `translation-input.json` path
- the generated `translation-apply-report.json` path
- the translated target files
- the created PR URL
- any terminology or branch issues that still need human review
