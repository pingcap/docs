---
name: write-update-tidb-docs
description: Write new TiDB documentation or update existing TiDB documentation from code changes, engineering notes, PRs, issues, design docs, rough drafts, existing docs, or short feature descriptions. Use when R&D engineers need user-facing docs in pingcap/docs or pingcap/docs-cn.
---

# Write or Update TiDB Docs

Use this skill to turn engineering context into user-facing TiDB documentation
in `pingcap/docs` or `pingcap/docs-cn`. Inputs can be code diffs, PRs, issues,
design notes, release notes, rough Markdown, existing docs, or a few sentences
from an R&D engineer.

## Defaults

- Inspect first, confirm when uncertain, then edit.
- Prefer updating existing docs. Write a new page only when the change introduces
  a distinct user task, feature, reference area, integration, or troubleshooting
  workflow that does not fit cleanly in an existing page.
- Documentation must justify its maintenance cost. Not every code change needs a
  doc update.
- If the user asks about local changes without naming files, run `git status -u`.
  If there are no uncommitted changes and the user clearly wants the latest local
  change, inspect `git show --name-status` and targeted diffs.
- For broad changes, group work by documentation area, such as guides, reference
  docs, release notes, examples, overview pages, and TOC updates. Use subagents
  or parallel analysis when available, but review the final result holistically.
- For substantial new docs or vague inputs, switch to co-authoring mode: gather
  context, agree on structure, draft section by section, and test whether the doc
  answers likely reader questions.

## Load context progressively

Always read:

- `.ai/shared/repo-conventions.md`
- `.ai/shared/writing-style.md`

Read only when relevant:

- `.ai/shared/translation-rules.md` and `.ai/shared/translation-terms.md` when
  the target is `docs-cn`, or the task involves English-to-Chinese translation
  or Chinese documentation updates.
- `resources/doc-templates/<template>.md` after choosing the doc type:
    - `template-new-feature.md`
    - `template-task.md`
    - `template-concept.md`
    - `template-reference.md`
    - `template-troubleshooting.md`
- `resources/terms.md` when terminology is uncertain.

Before drafting, inspect nearby docs, related overview/reference pages, TOC
entries, existing terminology, linked issues or PRs, and relevant code changes.
Prefer existing structure and wording in the same documentation area.

## Workflow

### 1. Plan with 5W1H

- **Who**: target readers, role, technical level, and prior knowledge.
- **What**: primary information versus secondary details.
- **Why**: user goal and product value, not only implementation change.
- **When**: use cases, feature status, applicable versions, and scenarios.
- **Where**: target repo, target file, TOC location, and whether to update or
  write a page.
- **How**: steps, SQL, commands, APIs, examples, expected output, limitations,
  compatibility, validation, and follow-up docs.

When facts are missing, derive what you can from code, tests, config names,
release notes, nearby docs, and issue or PR context. Ask focused questions only
for facts that cannot be verified locally and would change the documentation.

For substantial docs, ask the user to dump context in any form that is efficient:
notes, issue links, PR links, design docs, team decisions, rejected alternatives,
timeline constraints, stakeholder concerns, or rough bullets. Track what is
known, what is assumed, and what still needs confirmation.

### 2. Triage documentation impact

Prioritize tasks:

- **Critical**: breaking changes, changed defaults, compatibility changes,
  security-relevant behavior, user-facing errors, or new/changed public APIs.
- **Important**: new features, configuration options, workflows, SQL behavior,
  limitations, performance guidance, examples, or required TOC/index updates.
- **Nice to have**: minor clarifications or comments for non-obvious logic that
  users or contributors are likely to need.

Skip or consolidate docs that only:

- duplicate generated references, schemas, or existing docs without user context
- describe obvious internal implementation details
- document temporary workarounds or behavior expected to disappear soon
- repeat the same information in multiple places

### 3. Find the target doc and TOC placement

Before deciding whether to update an existing doc or write a new page, inspect
the relevant TOC file. TOC placement is often the fastest way to find the right
existing page, neighboring docs, and navigation category.

Use `rg` to search TOC files by feature name, command, component, or likely path:

```bash
rg -n "<keyword>|<path>" TOC*.md
```

TOC file purposes in `pingcap/docs`:

| TOC file | Use for |
| --- | --- |
| `TOC.md` | Main TiDB Self-Managed docs |
| `TOC-ai.md` | TiDB for AI, vector search, `pytidb`, MCP, AI integrations |
| `TOC-develop.md` | Application development guides, quick starts, integrations, developer reference |
| `TOC-best-practices.md` | Best practice pages for schema, deployment, operations, and performance |
| `TOC-api.md` | API documentation navigation for TiDB Cloud and TiDB Self-Managed |
| `TOC-tidb-releases.md` | TiDB Self-Managed release notes |
| `TOC-tidb-cloud.md` | Main TiDB Cloud docs, especially Dedicated/general Cloud navigation |
| `TOC-tidb-cloud-starter.md` | TiDB Cloud Starter docs |
| `TOC-tidb-cloud-essential.md` | TiDB Cloud Essential docs |
| `TOC-tidb-cloud-premium.md` | TiDB Cloud Premium docs |
| `TOC-tidb-cloud-releases.md` | TiDB Cloud release notes and maintenance notifications |

For `docs-cn`, check the corresponding TOC files in that repository, except for
`/tidb-cloud/` and `/ai/` content. These two areas are maintained through English
source updates only; do not manually update their Chinese translations.

Common doc targets in `pingcap/docs`:

| User request mentions | Start with |
| --- | --- |
| system variable | `system-variables.md` and `system-variable-reference.md` |
| status variable | `status-variables.md` |
| TiDB config parameter | `tidb-configuration-file.md` |
| TiKV config parameter | `tikv-configuration-file.md` |
| TiFlash config parameter | `tiflash/tiflash-configuration.md` |
| PD config parameter | `pd-configuration-file.md` |
| TSO or scheduling config | `tso-configuration-file.md` or `scheduling-configuration-file.md` |
| TiDB/TiKV/PD/TiFlash command-line flag | `command-line-flags-for-*-configuration.md` or `tiflash/tiflash-command-line-flags.md` |
| TiCDC server or changefeed config | `ticdc/ticdc-server-config.md` or `ticdc/ticdc-changefeed-config.md` |
| TiProxy config | `tiproxy/tiproxy-configuration.md` |
| SQL statement | `sql-statements/sql-statement-<statement>.md` and `sql-statements/sql-statement-overview.md` |
| function or operator | `functions-and-operators/` and `functions-and-operators/functions-and-operators-overview.md` |
| data type | `data-type-*.md` and `data-type-overview.md` |
| vector type/function/index | `/ai/reference/` docs, English-only in `release-8.5` |
| `INFORMATION_SCHEMA` table | `information-schema/` |
| monitoring metric | `grafana-*.md`, `tiflash/monitor-tiflash.md`, or `ticdc/monitor-ticdc.md` |

Treat these as starting points, not final answers. Confirm placement in the
appropriate TOC and inspect nearby entries before editing.

### 4. Choose the doc type

- **New feature**: what it is, why it matters, when to use it, how to use it,
  limitations, compatibility, and related resources.
- **Task**: prerequisites, numbered steps, expected results, and troubleshooting
  tips when useful.
- **Concept**: ideas, architecture, terms, behavior, or tradeoffs users need
  before tasks.
- **Reference**: syntax, APIs, configuration, system variables, parameters,
  functions, outputs, or limits.
- **Troubleshooting**: symptoms, likely causes, checks, fixes, and prevention.
- **Developer/API doc**: interfaces, parameters, examples, return values, errors,
  compatibility, and migration impact.
- **Architecture/design doc**: components, data flow, interfaces, tradeoffs,
  scalability, security, and observability only when they affect users.
- **Existing-doc update**: change only affected sections and preserve the
  surrounding structure, tone, and technical scope.

For any update, check whether overview pages, reference pages, examples,
`TOC.md`, aliases, links, or release notes also need changes.

### 5. Write

For new feature docs, or substantial feature expansions, use this shape when
applicable:

```markdown
---
title: <same as H1>
summary: <115-145 character reader-focused summary>
---

# <same as title>

<Intro: what the feature does, why it matters, and when users should use it.>

## Usage scenarios

## Prerequisites

## Usage or procedures

### Method 1: <method name> (recommended)

### Method 2: <method name>

## Limitations

## Compatibility

## FAQ

## More resources
```

Use only sections that help users complete tasks or make decisions. When updating
an existing doc, fit new content into the existing structure unless the current
structure blocks user understanding.

For substantial new docs or major rewrites, draft section by section:

1. Propose the 3-5 core sections based on the doc type or template.
2. Start with the section that has the most unknowns; write summaries or
   conclusions last.
3. For each section, ask only the clarifying questions needed for that section,
   draft the section, then revise surgically instead of reprinting the whole doc.
4. After several small edits, ask whether anything can be removed without losing
   important information.

Writing rules that matter most:

- Start with useful information directly. Avoid internal background unless users
  need it.
- Start task docs with the most common use case or shortest path to first
  success.
- Put conditions before instructions. Tell users where to perform each action.
- Explain placeholders and include expected output for commands, SQL, or APIs
  when useful.
- Keep code examples realistic and runnable when possible. Use language IDs and
  comments only for non-obvious logic.
- Define jargon on first use.
- Preserve commands, SQL, API names, UI strings, config names, JSON fields,
  outputs, and technical meaning unless they are factually wrong or confirmed.

## TiDB docs gotchas

- Target `master` by default. Use release branches only for version-specific
  behavior, compatibility changes, broken links in published docs, explicit user
  requests, or the `/tidb-cloud/` and `/ai/` exceptions below.
- The `/tidb-cloud/` and `/ai/` folders are currently maintained only in the
  `pingcap/docs` `release-8.5` branch. For these folders, update English only.
  Do not manually update Chinese content:
    - `/tidb-cloud/` Chinese content is in `pingcap/docs`
      `i18n-zh-release-8.5` and is AI-translated weekly.
    - `/ai/` Chinese content is in `pingcap/docs-cn` and is also AI-translated
      weekly.
- New navigable pages usually require `TOC.md` updates. Renamed or replaced pages
  might need `aliases`.
- TiDB Cloud docs use special branch and rendering rules. Before changing shared
  TiDB/TiDB Cloud content, check repo guidance and any `CustomContent` blocks.
- Do not silently broaden scope from a local doc fix into cross-file rewrites.
  Note possible related updates, and only edit them when needed for correctness
  or navigation.
- Preserve code samples, commands, SQL, config names, API fields, JSON, EBNF, and
  UI strings unless the task requires changing them or they are clearly wrong.
- Front matter `title` must match the H1. English titles use title case; headings
  below H1 use sentence case.
- Summaries should be reader-focused and usually 115-145 characters. Add
  `aliases` only when replacing, renaming, or deleting an existing page.
- For `docs-cn`, preserve source meaning, structure, links, and terminology. Use
  repo translation guidance instead of free paraphrasing.

## Validation loop

1. Review against the plan: facts, user goal, doc type, scope, examples, links,
   TOC impact, version scope, and maintainability.
2. Run Markdown validation when practical:

   ```bash
   ./scripts/markdownlint <changed-files>
   ```

3. Run targeted link validation when adding or changing links, anchors, moved
   files, renamed files, aliases, or TOC entries.
4. For procedural docs, mentally or actually test the steps, sample code, SQL,
   expected output, and placeholders.
5. For substantial docs, run a reader test: predict 5-10 realistic reader
   questions, verify the doc answers them without hidden context, and fix gaps,
   ambiguities, contradictions, or unstated assumptions. Use a subagent for a
   fresh-read review when available.
6. If validation fails, fix the issue and repeat until checks pass or clearly
   report why a check could not be run.

## Output templates

When proposing a plan before editing:

```markdown
Target: <repo/path>
Change type: <update existing doc | write new page>
Doc type: <task | concept | reference | new feature | troubleshooting | other>
Outline: <short heading list>
Related updates: <TOC, aliases, links, overview/reference/release notes>
Validation: <checks to run>
Reader test: <questions the doc should answer, for substantial docs>
Open questions: <facts that need confirmation>
```

When reporting completed edits:

```markdown
Changed files:
- <path>: <what changed>

Checks:
- <command>: <result>

Notes:
- <key decisions, maintenance triggers, or unresolved engineering questions>
```
