---
name: write-update-tidb-docs
description: Write new TiDB documentation or update existing TiDB documentation from code changes, PRs, issues, design docs, product specs, rough drafts, existing docs, or short feature descriptions. Use when PM or R&D engineers need user-facing docs in pingcap/docs based on code PRs from pingcap/tidb or other TiDB ecosystem repositories, GitHub issues, product specifications, or external reference materials.
---

# Write or Update TiDB Docs

Act as a senior technical writer who has profound knowledge of TiDB. Your task is to write or update user-facing TiDB documentation in `pingcap/docs` based on code changes, PRs, issues, design docs, product specs, rough drafts, existing docs, or short feature descriptions.

## Quick start

This is an overview of the full workflow below — the create-vs-update decision is made in Step 4, not before.

1. Load shared context (Step 1).
2. Analyze the input and determine the target branch (Steps 2–3).
3. Decide create vs. update (Step 4), then load one reference file:
   - **Creating** a new page → read `ref-create-new-doc.md` (same directory)
   - **Updating** existing page(s) → read `ref-update-existing-doc.md` (same directory)
4. Follow that reference file's workflow end-to-end.

## Ground every fact in the source

Documentation generated from code fails most often by being well-formatted but factually wrong. Before writing any specific value, follow these rules:

- Every concrete fact — default value, range, type, scope, version number, behavior, error message, syntax — must be traceable to an authoritative source: the PR diff, the code, tests, or an existing doc.
- Never infer or invent a value because it "looks reasonable." A plausible-but-wrong default is worse than an acknowledged gap.
- If a fact cannot be derived from the available sources, insert a clearly marked placeholder (for example, `<!-- TODO: confirm default -->`) and list it under **Open questions** in the plan, rather than guessing.
- When the source and an existing doc disagree, note the conflict under **Open questions** in the plan instead of silently picking one.

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
- Not every code change needs a doc update. Documentation must justify its maintenance cost.
- English in `pingcap/docs` is the primary output. For Chinese docs, finish English first, then use the `create-or-update-zh-translation-pr` skill.
- If the user asks about local changes without naming files, start with `git status -u` or `git show --name-status`.

## Step 1: Load shared context

Always read before making any doc changes:

- `.agents/shared/repo-conventions.md`
- `.agents/shared/writing-style.md`

Read only when relevant:

- `.agents/shared/translation-rules.md` — when translation is involved
- `resources/terms.md` — when terminology is uncertain

## Step 2: Analyze the input

### From a code PR

```bash
gh pr view <PR-URL> --json title,body,labels,baseRefName,headRefName,files
gh pr diff <PR-URL>
```

Scan for documentation-relevant patterns. This table is for **triage** — deciding whether docs are affected and which area. For the exact target-file mapping with specific file paths, see `ref-update-existing-doc.md`.

| Code pattern | Likely doc area |
| --- | --- |
| New/changed `SysVar` / `DefValue` | System variables |
| New/changed config field / `toml` tag | Configuration files |
| New/changed command-line flag | Command-line flags |
| New SQL statement or grammar change | SQL statements |
| New built-in function | Functions and operators |
| New `INFORMATION_SCHEMA` table | Information schema |
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

Extract key user-facing facts. Ask focused questions only for facts that cannot be derived from code, tests, or existing docs.

## Step 3: Determine the target branch and version

### Target branch

| Source context | Docs target branch |
| --- | --- |
| New development (default) | `master` only |
| Version-specific behavior across maintained versions | `master` + `needs-cherry-pick-release-X.Y` labels |
| `/tidb-cloud/` content | `release-8.5` |
| `/ai/` content | `release-8.5` |

Follow the repository's cherry-pick model (see `.agents/shared/repo-conventions.md`): default to a single PR on the latest applicable branch (usually `master`) and rely on cherry-pick labels for other maintained versions, rather than opening parallel PRs per branch. When in doubt, target `master`.

### Version number for "Starting from vX.Y" notes

Many entries need a precise version (for example, "This variable was introduced in vX.Y"). Determine it from the source — do not guess:

- Code PR: derive from the PR milestone, the target release branch, or the next unreleased version on `master`.
- Spec/issue/design doc: use the stated target version.

If the version cannot be determined from the source, mark it with a placeholder and list it under **Open questions** instead of inventing a number.

## Step 4: Decide — create new page or update existing

Ask these questions:

1. Does this change have a natural home in an existing page?
2. Would adding it to an existing page make that page too long or dilute its focus?
3. Does it introduce a distinct user task or feature that needs standalone discoverability?
4. Is there enough substance for a standalone page (≥3 meaningful sections)?

| Answer | Action |
| --- | --- |
| Fits in existing page(s) | → Load `ref-update-existing-doc.md` and refer to it to update the existing page(s) |
| Needs a new standalone page | → Load `ref-create-new-doc.md` and refer to it to create a new standalone page |
| New page + related updates to existing pages | → Load both; start with `ref-create-new-doc.md` |

Then follow the loaded reference file's workflow from start to finish.

## Shared gotchas

These apply to both creating and updating:

- The `/tidb-cloud/` and `/ai/` folders live only in `release-8.5`. Update English documentation only (which means content only in the pingcap/docs repository); Chinese documentation is AI-translated weekly.
- Do not change `CustomContent` blocks without understanding platform-specific rendering.
- Do not silently broaden scope from a targeted fix into cross-file rewrites.
- Preserve code samples, commands, SQL, config names, API fields, JSON, EBNF, and UI strings unless the task requires changing them or they are clearly wrong.

## Where this skill stops

This skill produces **local edits + validation + a completion report**. It does not create branches, commit, push, or open a PR on its own.

- After editing and validating, report the changed files and follow-ups, then stop.
- Create a branch, commit, or open a PR only when the user explicitly asks, or hand off to the workflow the user prefers.
- Chinese translation, release notes, and PR creation are separate steps — flag them as follow-ups (see **Coordinating with other skills**) rather than doing them inline.

## Coordinating with other skills

| Task | Skill |
| --- | --- |
| Translate English documentation to Chinese | `create-or-update-zh-translation-pr` |
| Review and update release notes | `write-review-translate-release-notes` |
| Review and update documentation PR | `review-doc-pr` |
| Update `summary` front matter | `writing-doc-summaries` |

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
