# Translation Rules

Use this file for EN -> ZH translation work that starts from changes in `pingcap/docs`.

## Scope

- This guidance is for mapping English docs work in `pingcap/docs` to Chinese docs work in `pingcap/docs-cn`.
- Keep the translation faithful to the source change unless the target repo or branch requires a documented difference.

## Preserve structure

Keep the following stable unless translation requires a language-only adjustment:

- heading hierarchy
- lists and numbering
- tables and column order
- code fences and info strings
- links, anchors, and repo paths
- commands, flags, API names, config keys, and version numbers
- product names and branch names

Do not invent new product behavior, prerequisites, warnings, or version claims.

## Terminology

- Use `resources/terms.md` as the source of truth for terminology.
- Use `.ai/shared/translation-terms.md` as a quick reference for high-frequency terms.
- If a term is missing or ambiguous, keep the source term until you can verify the preferred translation.

## PR traceability

When preparing a translation PR:

- reference the source English PR or file links
- preserve the intended affected versions as much as the target repo allows
- keep the PR body compatible with `.github/pull_request_template.md`
- make the relationship to the source PR explicit

## Workflow expectations

- Identify the source files and the target files before translating.
- Check whether the target branch should be `master` or a release branch.
- If a helper script is available, prefer adapting it over rewriting the workflow from scratch.
- If local automation depends on unavailable tokens or secrets, still prepare the branch, file list, PR body, and follow-up instructions so a human can finish the workflow quickly.
