# Create New TiDB Documentation

Self-contained workflow for creating a new documentation page in `pingcap/docs`. Follow these steps sequentially if the [write-update-tidb-docs](/.agents/skills/write-update-tidb-docs/SKILL.md) skill has determined that a new page is needed.

## Confirm the decision to create

This is a final sanity re-check of the create-vs-update decision already made in the Step 4 (the authoritative decision point) of the [write-update-tidb-docs](/.agents/skills/write-update-tidb-docs/SKILL.md) skill — not a second, independent decision. If any criterion below fails, switch to `ref-update-existing-doc.md`.

A new page is justified when all of these are true:

- The content does not fit cleanly as a section of an existing page.
- There is enough substance for ≥3 meaningful sections.
- The content has standalone discoverability value (users might search for it directly).

Typical triggers: new feature with its own scenarios/config/limitations, new SQL statement, new `INFORMATION_SCHEMA` table, new integration/tool, new troubleshooting workflow.

Do **not** create a new page if:

- The content can be a section in an existing page without making it too long.
- The content would be too thin (fewer than ~3 sections).
- Similar content already exists and could be expanded instead.

## 1. Choose doc type and template

| Doc type | User question it answers | Template to read |
| --- | --- | --- |
| New feature | "What is this? Why use it? How?" | `resources/doc-templates/template-new-feature.md` |
| Task | "How do I do X step by step?" | `resources/doc-templates/template-task.md` |
| Concept | "What is X and how does it work?" | `resources/doc-templates/template-concept.md` |
| Reference | "What are the params/syntax/options?" | `resources/doc-templates/template-reference.md` |
| Troubleshooting | "Something is wrong, how to fix?" | `resources/doc-templates/template-troubleshooting.md` |

Read the selected template before drafting. Use it as a structural skeleton; skip sections that do not apply.

For features combining concept + usage + reference (common in TiDB), use the **new feature** template. Split into multiple pages only when content naturally exceeds ~1500 words per concern.

## 2. Choose file path and name

Look at where similar docs live:

```bash
# Find peers in the TOC
rg -n "<component>|<feature-keyword>" TOC*.md

# Check existing directory structure
ls <component-dir>/
```

**Naming rules:**

- Lowercase, hyphen-separated: `feature-name.md`
- Concise and stable: avoid version numbers or overly specific wording
- Follow existing patterns in the same area

**Placement rules:**

| Feature scope | Path |
| --- | --- |
| Component-specific (TiCDC, TiFlash, TiProxy, DM, BR) | `<component>/feature-name.md` |
| SQL statement | `sql-statements/sql-statement-<name>.md` |
| INFORMATION_SCHEMA table | `information-schema/information-schema-<name>.md` |
| Function/operator | `functions-and-operators/<category>.md` |
| Cross-component or general | Root: `feature-name.md` |

## 3. Determine TOC placement

Every navigable page needs a TOC entry.

### Which TOC file?

| Content area | TOC file |
| --- | --- |
| TiDB Self-Managed (most common) | `TOC.md` |
| AI / vector search / pytidb / MCP | `TOC-ai.md` |
| App development guides | `TOC-develop.md` |
| Best practices | `TOC-best-practices.md` |
| API docs | `TOC-api.md` |
| TiDB release notes | `TOC-tidb-releases.md` |
| TiDB Cloud general | `TOC-tidb-cloud.md` |
| TiDB Cloud tier-specific | `TOC-tidb-cloud-starter.md` / `TOC-tidb-cloud-essential.md` / `TOC-tidb-cloud-premium.md` |
| TiDB Cloud release notes | `TOC-tidb-cloud-releases.md` |

### Where in the TOC?

1. Find the relevant section: `rg -n "<keyword>" TOC.md`
2. Look at neighbors (TOC groups by component), then by complexity (overview → getting started → usage → reference → troubleshooting).
3. Place the entry adjacent to similar items at the correct nesting level.

**Format** (2-space indent per level):

```markdown
- Category Name
  - [Page Title](/path/to/file.md)
  - [New Page Title](/path/to/new-file.md)
    - [Sub Page](/path/to/sub.md)
```

**TOC title**: title case, concise (3 to 7 words), match the doc H1 when feasible.

## 4. Write front matter

```yaml
---
title: <same as H1, title case>
summary: <verb-led, SEO-friendly sentence>
---
```

- `title` must match the H1 exactly, in title case, and stay within ~59 characters.
- `summary` must not start with `>`, `*`, `#`, `-`, or `[`.
- `summary` tells readers what they will learn or accomplish.
- For exact `summary` length rules and verb guidance, follow the `writing-doc-summaries` skill (target 115 to 145 characters, 45-character absolute minimum).
- SQL statement reference pages use a fixed template defined in the `writing-doc-summaries` skill that falls below 115 characters — that is expected.
- Add `aliases` only if replacing an older page URL.

## 5. Draft the document

### Writing principles

- Start with what users care about, not the internal background.
- Put conditions before instructions.
- Define jargon on first use.
- Include realistic, runnable examples.
- End with related resources or next steps.

### Structure by doc type

**New feature:**

```
# Feature Name
  Intro: what it does, why it matters, when to use it.

## Use cases

## Prerequisites (if needed)

## How to use <feature>
### Method 1: <name> (recommended)
### Method 2: <name>

## Parameter reference (if applicable)

## Limitations

## Compatibility

## FAQ (if needed)

## See also
```

**Task:**

```
# Task Title
  Intro: what this helps you accomplish.

## Prerequisites

## Step 1. <verb phrase>

## Step 2. <verb phrase>

## Step 3. <verb phrase>

## What's next
```

**Concept:**

```
# Concept Title
  Intro: what this concept is and why it matters.

## Architecture / How it works

## Key features

## Limitations (if applicable)

## What's next
```

**Reference:**

```
# Reference Title
  Intro: what this reference covers.

## Category 1
### Item / parameter

## Category 2
### Item / parameter
```

**Troubleshooting:**

```
# Troubleshoot <Problem>
  Intro: what problems this covers.

## Common causes
### Cause 1
  Symptom → Solution
### Cause 2

## Other causes
### Cause 3
```

### Co-authoring mode (for substantial docs)

When the doc is expected to exceed ~800 words or has unclear scope:

1. Propose 3 to 5 core sections. Get confirmation.
2. Start with the highest-value or most-uncertain section.
3. Draft section by section. Ask questions only when facts cannot be derived from available sources.
4. After drafting, run a reader test: predict 5 to 10 questions a real user would ask. Verify the doc answers them.
5. Ask: can anything be removed without losing value?

## 6. Handle associated updates

| Check | Action when needed |
| --- | --- |
| TOC entry | Always required |
| Overview page | Add brief mention or link (e.g., `sql-statements/sql-statement-overview.md`) |
| Related docs | Add "See also" links where users benefit |
| Release notes | Flag for the release notes skill |
| System variable page | Cross-link if the feature has variables |
| Compatibility page | Update if MySQL compat is affected |

## 7. Validate

```bash
./scripts/markdownlint <new-file> <changed-toc-file>
./scripts/verify-links.sh  # if links were added
```

Also check:

- [ ] Front matter: title matches H1; summary follows `writing-doc-summaries` length rules (115–145 chars target, ≥45 chars)
- [ ] TOC: correct file, correct level, correct indentation
- [ ] Heading levels: no skipped levels, exactly one H1
- [ ] File name: lowercase, hyphen-separated, `.md` extension
- [ ] A user finding this via search can complete their task without hidden context

## Common mistakes

- Page too thin — should have been a section in an existing page.
- TOC entry in wrong file or wrong nesting level.
- Intro describes what the doc will do instead of starting with useful info.
- Missing overview/reference page updates that help users discover the new page.
- Forgetting `aliases` when replacing an older page.
- Writing content that duplicates an existing page without adding new user value.
