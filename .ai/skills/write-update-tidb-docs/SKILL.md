---
name: write-update-tidb-docs
description: Write new TiDB documentation or update existing TiDB documentation from code changes, PRs, issues, design docs, product specs, rough drafts, existing docs, or short feature descriptions. Use when PM or R&D engineers need user-facing docs in pingcap/docs based on code PRs from pingcap/tidb or other TiDB ecosystem repositories, GitHub issues, product specifications, or external reference materials.
---

# Write or Update TiDB Docs

Use this skill when PM or R&D engineers provide engineering or product context
and need it turned into user-facing TiDB documentation in `pingcap/docs`.

**Role**: Act as a senior documentation engineer who understands both the
technical implementation and the user's information needs. Evaluate not just
*what* to write, but *where* it belongs, *how* it connects to existing content,
and *what style* fits the surrounding documentation.

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
| Verbal description | Short sentences describing the feature or change |

Multiple input types can be combined. The more context provided, the fewer
questions needed.

## Defaults

- Inspect first, confirm when uncertain, then edit.
- Prefer updating existing docs. Write a new page only when the change introduces
  a distinct user task, feature, reference area, integration, or troubleshooting
  workflow that does not fit cleanly in an existing page.
- Documentation must justify its maintenance cost. Not every code change needs a
  doc update.
- English documentation in `pingcap/docs` is the primary output. Do not write
  Chinese docs directly. If Chinese docs are also needed, finish the English doc
  first, then use the `create-or-update-zh-translation-pr` skill.
- If the user asks about local changes without naming files, run `git status -u`.
  If there are no uncommitted changes and the user clearly wants the latest local
  change, inspect `git show --name-status` and targeted diffs.

## Load context progressively

Always read first:

- `.ai/shared/repo-conventions.md`
- `.ai/shared/writing-style.md`

Read when relevant:

- `.ai/shared/translation-rules.md` and `.ai/shared/translation-terms.md`when the task involves English-to-Chinese translation or Chinese documentation.
- `resources/doc-templates/<template>.md` after choosing the doc type (see the create-new-doc reference).
- `resources/terms.md` when terminology is uncertain.

Before drafting, inspect nearby docs, related overview/reference pages, TOC
entries, existing terminology, linked issues or PRs, and relevant code changes.
Prefer existing structure and wording in the same documentation area.

## Workflow overview

### Phase 1: Analyze the input

**When the input is a code PR URL or reference:**

1. Fetch the PR metadata and diff:

   ```bash
   gh pr view <PR-URL> --json title,body,labels,baseRefName,headRefName,files
   gh pr diff <PR-URL>
   ```

2. Read the PR description, linked issues, and any design doc references.

3. Scan the diff for documentation-relevant changes:

   | Code pattern | Likely doc impact |
   | --- | --- |
   | New/changed `SysVar` / `DefValue` | Update `system-variables.md` |
   | New/changed config struct / `toml` tag | Update `*-configuration-file.md` |
   | New/changed command-line flag | Update `command-line-flags-for-*-configuration.md` |
   | New SQL statement or grammar change | New or updated `sql-statements/sql-statement-*.md` |
   | New built-in function | Update `functions-and-operators/` docs |
   | New `INFORMATION_SCHEMA` table | New doc under `information-schema/` |
   | New metrics or alert rules | Update `grafana-*.md` or monitoring docs |
   | New feature flag or experimental gate | New feature doc or update existing |
   | Changed default or compatibility | Update relevant docs + possibly release notes |
   | New API endpoint | Update or create API reference |

4. If the code diff is large, focus on user-facing changes (exported APIs,
   config, SQL grammar, error messages, system variables) and skip internal
   refactors.

**When the input is a product spec, issue, or design doc:**

1. Identify the user-facing changes: what can users now do, configure, or observe
   that they could not before?
2. Identify the affected components: which TiDB component(s) does this touch?
3. Determine version scope: which versions will include this change?
4. Note any constraints, limitations, or compatibility concerns mentioned.

**When the input is rough notes or verbal description:**

1. Extract the key user-facing facts.
2. Identify what information is missing and ask focused questions.
3. Derive what you can from code, tests, config names, existing docs, and
   related issues/PRs.

### Phase 2: Map to docs branch

| Source target branch | Docs target branch | Notes |
| --- | --- | --- |
| `master` | `master` | Default for new development |
| `release-X.Y` | `release-X.Y` (if it exists) | Version-specific behavior |
| Any, but user-facing across versions | `master` + cherry-pick labels | Use `needs-cherry-pick-release-X.Y` |
| TiDB Cloud content (`/tidb-cloud/`) | `release-8.5` | Cloud docs branch |
| AI content (`/ai/`) | `release-8.5` | AI docs branch |

When in doubt, target `master` and let the user decide about cherry-picks.

### Phase 3: Plan with 5W1H

- **Who**: target readers, role, technical level, prior knowledge.
- **What**: primary information vs. secondary details.
- **Why**: user goal and product value, not only implementation change.
- **When**: use cases, feature status, applicable versions, scenarios.
- **Where**: target repo, target file(s), TOC location.
- **How**: steps, SQL, commands, APIs, examples, expected output, limitations,
  compatibility, validation.

### Phase 4: Decide — create new or update existing

This is the key routing decision. Ask:

1. Does this feature/change have a natural home in an existing page?
2. Is the existing page already covering this topic area?
3. Would adding this content to an existing page make it unreasonably long or
   confuse the page's current focus?
4. Does this introduce a distinct user task or feature that deserves standalone
   discoverability?

| Decision | Action |
| --- | --- |
| Content fits in existing page(s) | → Read `ref-update-existing-doc.md` and follow its workflow |
| Content needs a new standalone page | → Read `ref-create-new-doc.md` and follow its workflow |
| Both (new page + updates to related pages) | → Read both references; start with the new page, then update related |

### Phase 5: Triage priority

When multiple docs need updating, prioritize:

- **Critical**: breaking changes, changed defaults, compatibility changes,
  security-relevant behavior, user-facing errors, new/changed public APIs.
- **Important**: new features, configuration options, workflows, SQL behavior,
  limitations, performance guidance, examples, TOC updates.
- **Nice to have**: minor clarifications, comments for non-obvious logic.

Skip or consolidate docs that only duplicate generated references without user
context, describe obvious internal implementation, or document temporary behavior.

### Phase 6: Write

Follow `.ai/shared/writing-style.md` for all writing conventions. Key reminders:

- Start with useful information directly. No preamble about what the doc will do.
- Start task docs with the most common use case or shortest path to first
  success.
- Put conditions before instructions.
- Explain placeholders and include expected output for commands, SQL, or APIs.
- Keep code examples realistic and runnable when possible.
- Define jargon on first use.
- Preserve commands, SQL, API names, UI strings, config names, JSON fields,
  outputs, and technical meaning unless factually wrong or confirmed changed.

For doc-type-specific structure, see the appropriate reference file.

### Phase 7: Validate

1. Review against the plan: facts, user goal, doc type, scope, examples, links,
   TOC impact, version scope, and maintainability.
2. Run Markdown validation:

   ```bash
   ./scripts/markdownlint <changed-files>
   ```

3. Run link validation when adding or changing links, anchors, moved or renamed
   files, aliases, or TOC entries.
4. For procedural docs, mentally or actually test the steps, sample code, SQL,
   expected output, and placeholders.
5. For substantial docs, run a reader test: predict 5–10 realistic reader
   questions, verify the doc answers them without hidden context, and fix gaps.
6. If validation fails, fix the issue and repeat.

## Reference files

This skill includes two reference files for the detailed workflows:

- `ref-create-new-doc.md` — complete guidance for creating new documentation
  pages, including TOC placement, doc type selection, file naming, structure,
  front matter, and co-authoring mode.
- `ref-update-existing-doc.md` — complete guidance for updating existing pages,
  including target identification, related doc assessment, style consistency,
  cross-document impact, and common update patterns.

Load the relevant reference file after Phase 4 determines the action type.

## TiDB docs gotchas

- Target `master` by default. Use release branches only for version-specific
  behavior, compatibility changes, broken links in published docs, explicit user
  requests, or the `/tidb-cloud/` and `/ai/` exceptions.
- The `/tidb-cloud/` and `/ai/` folders are maintained only in `release-8.5`.
  Update English only. Chinese content is AI-translated weekly.
- New navigable pages always require `TOC.md` updates. Renamed or replaced pages
  might need `aliases`.
- TiDB Cloud docs use special branch and rendering rules. Check `CustomContent`
  blocks before changing shared TiDB/TiDB Cloud content.
- Do not silently broaden scope from a local fix into cross-file rewrites. Note
  related updates and only make them when needed for correctness or navigation.
- Preserve code samples, commands, SQL, config names, API fields, JSON, EBNF, and
  UI strings unless the task requires changing them or they are clearly wrong.
- For broad changes, group work by documentation area and use subagents or
  parallel analysis when available, but review the final result holistically.

## Coordinating with other skills

| Scenario | Skill to use |
| --- | --- |
| Chinese translation needed after English doc is done | `create-or-update-zh-translation-pr` |
| Code change also needs release notes | `write-review-translate-release-notes` |
| English doc PR needs review | `review-doc-pr` |
| Doc pages need `summary` front matter | `writing-doc-summaries` |

Flag these needs to the user instead of silently switching skills.

## Output templates

**When proposing a plan before editing:**

```markdown
Target: <repo/branch/path>
Source: <code PR URL, issue, spec, or other input>
Change type: <update existing doc | write new page | both>
Doc type: <task | concept | reference | new feature | troubleshooting | other>
Outline: <short heading list>
Related updates: <TOC, aliases, links, overview/reference/release notes>
Validation: <checks to run>
Reader test: <questions the doc should answer, for substantial docs>
Open questions: <facts that need confirmation>
```

**When reporting completed edits:**

```markdown
Changed files:
- <path>: <what changed>

Source: <link to the code PR, issue, or spec that motivated the change>

Checks:
- <command>: <result>

Notes:
- <key decisions, maintenance triggers, or unresolved engineering questions>
- <whether Chinese translation or release notes are also needed>
```
