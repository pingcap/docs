---
name: write-update-tidb-docs
description: Write new TiDB documentation or update existing TiDB documentation from code changes, PRs, issues, design docs, product specs, rough drafts, existing docs, or short feature descriptions. Use when PM or R&D engineers need user-facing docs in pingcap/docs based on code PRs from pingcap/tidb or other TiDB ecosystem repositories, GitHub issues, product specifications, or external reference materials.
---

# Write or Update TiDB Docs

Act as a senior documentation engineer. Turn engineering or product context into
user-facing TiDB documentation in `pingcap/docs`.

## Quick start

1. Read this file to analyze the input and decide the action type.
2. Load one reference file based on your decision:
   - **Creating** a new page → read `ref-create-new-doc.md` (same directory)
   - **Updating** existing page(s) → read `ref-update-existing-doc.md` (same directory)
3. Follow that reference file's workflow end-to-end.

## Accepted inputs

| Input type | Examples |
| --- | --- |
| Code PR | `pingcap/tidb` PR link, diff, or reference |
| GitHub issue | Feature request, bug report, design discussion |
| Product spec | Feature specification, product requirement document |
| Design doc | Technical design, RFC, architecture proposal |
| External reference | Blog post, conference talk notes, user feedback |
| Rough notes | Bullets, chat messages, informal descriptions |
| Existing docs | Current doc page that needs improvement |

Multiple inputs can be combined. More context = fewer questions needed.

## Defaults

- Inspect first, confirm when uncertain, then edit.
- Prefer updating existing docs over creating new pages.
- Not every code change needs a doc update. Documentation must justify its
  maintenance cost.
- English in `pingcap/docs` is the primary output. For Chinese docs, finish
  English first, then use the `create-or-update-zh-translation-pr` skill.
- If the user asks about local changes without naming files, start with
  `git status -u` or `git show --name-status`.

## Step 1: Load shared context

Always read before making any doc changes:

- `.ai/shared/repo-conventions.md`
- `.ai/shared/writing-style.md`

Read only when relevant:

- `.ai/shared/translation-rules.md` — when translation is involved
- `resources/terms.md` — when terminology is uncertain

## Step 2: Analyze the input

### From a code PR

```bash
gh pr view <PR-URL> --json title,body,labels,baseRefName,headRefName,files
gh pr diff <PR-URL>
```

Scan for documentation-relevant patterns:

| Code pattern | Likely doc impact |
| --- | --- |
| New/changed `SysVar` / `DefValue` | `system-variables.md` |
| New/changed config field / `toml` tag | `*-configuration-file.md` |
| New/changed command-line flag | `command-line-flags-for-*-configuration.md` |
| New SQL statement or grammar change | `sql-statements/sql-statement-*.md` |
| New built-in function | `functions-and-operators/` |
| New `INFORMATION_SCHEMA` table | `information-schema/` |
| New feature flag or experimental gate | Feature doc (new or existing) |
| Changed default or compatibility | Relevant docs + possibly release notes |

Focus on user-facing changes. Skip internal refactors that do not affect behavior.

### From a product spec, issue, or design doc

Extract:

1. What can users now do, configure, or observe that they could not before?
2. Which components are affected?
3. Which versions will include this?
4. Any constraints, limitations, or compatibility concerns?

### From rough notes or verbal description

Extract key user-facing facts. Ask focused questions only for facts that cannot
be derived from code, tests, or existing docs.

## Step 3: Determine the target branch

| Source context | Docs target branch |
| --- | --- |
| New development (default) | `master` |
| Version-specific behavior | `release-X.Y` + `master` |
| Cross-version change | `master` + `needs-cherry-pick-release-X.Y` labels |
| `/tidb-cloud/` content | `release-8.5` |
| `/ai/` content | `release-8.5` |

When in doubt, target `master`.

## Step 4: Decide — create new page or update existing

Ask these questions:

1. Does this change have a natural home in an existing page?
2. Would adding it to an existing page make that page too long or dilute its
   focus?
3. Does it introduce a distinct user task or feature that needs standalone
   discoverability?
4. Is there enough substance for a standalone page (≥3 meaningful sections)?

| Answer | Action |
| --- | --- |
| Fits in existing page(s) | → Load `ref-update-existing-doc.md` |
| Needs a new standalone page | → Load `ref-create-new-doc.md` |
| New page + related updates to existing pages | → Load both; start with `ref-create-new-doc.md` |

Then follow the loaded reference file's workflow from start to finish.

## Shared gotchas

These apply to both creating and updating:

- The `/tidb-cloud/` and `/ai/` folders live only in `release-8.5`. Update
  English only; Chinese is AI-translated weekly.
- Do not change `CustomContent` blocks without understanding platform-specific
  rendering.
- Do not silently broaden scope from a targeted fix into cross-file rewrites.
- Preserve code samples, commands, SQL, config names, API fields, JSON, EBNF,
  and UI strings unless the task requires changing them or they are clearly wrong.

## Coordinating with other skills

| Need | Skill |
| --- | --- |
| Chinese translation | `create-or-update-zh-translation-pr` |
| Release notes | `write-review-translate-release-notes` |
| Doc PR review | `review-doc-pr` |
| Front matter `summary` | `writing-doc-summaries` |

Flag these to the user instead of silently switching.

## Output format

**Plan (before editing):**

```
Target: <branch/path>
Source: <PR URL, issue, spec, or description>
Action: <create new page | update existing | both>
Doc type: <task | concept | reference | new feature | troubleshooting>
Outline: <heading list>
Related updates: <TOC, links, overview, release notes>
Open questions: <facts needing confirmation>
```

**Completion report:**

```
Changed files:
- <path>: <what changed>

Source: <link or description>

Validation:
- <check>: <result>

Follow-up:
- <translation, release notes, or other needs>
```
