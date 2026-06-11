# Reference: Create New TiDB Documentation

This reference covers the full workflow for creating a new documentation page in
`pingcap/docs`. Read this after the main SKILL.md has determined that a new page
is needed.

## When to create a new page

Create a new page only when the change introduces content that does not fit
cleanly in an existing page. Typical triggers:

- A distinct user-facing feature with its own usage scenarios, configuration,
  and limitations (for example, a new index type, a new SQL statement, a new
  tool mode).
- A new integration, connector, or ecosystem tool that needs a standalone guide.
- A new reference entity that follows an established pattern (for example, a new
  `INFORMATION_SCHEMA` table, a new TiCDC sink type).
- A troubleshooting workflow that is complex enough to justify its own page
  rather than a section in an existing troubleshooting doc.
- A new concept or architecture topic that supports multiple task or reference
  pages.

Do **not** create a new page when:

- The content can be added as a section or subsection of an existing page without
  making that page unreasonably long.
- The content duplicates information already available elsewhere.
- The content is too thin to justify standalone maintenance (fewer than ~3
  meaningful sections).

## Step 1: Choose the doc type and template

Match the user's information need to a doc type:

| Doc type | User need | Template |
| --- | --- | --- |
| New feature | "What is this, why should I use it, how do I use it?" | `resources/doc-templates/template-new-feature.md` |
| Task | "How do I do X step by step?" | `resources/doc-templates/template-task.md` |
| Concept | "What is X and how does it work?" | `resources/doc-templates/template-concept.md` |
| Reference | "What are the parameters, syntax, config options?" | `resources/doc-templates/template-reference.md` |
| Troubleshooting | "Something is wrong, how do I fix it?" | `resources/doc-templates/template-troubleshooting.md` |

Read the selected template before drafting. Use the template as the structural
skeleton; skip sections that do not apply rather than filling them with thin
content.

For features that combine concept, usage, and reference (common in TiDB), prefer
the **new feature** template and merge concept and reference into its sections.
Split into multiple pages only when the content naturally exceeds ~1500 words per
concern.

## Step 2: Choose the file path and name

Follow existing patterns in the same documentation area:

- Check where similar docs live by inspecting the relevant TOC file and nearby
  directory structure.
- Use lowercase, hyphen-separated names: `feature-name.md`.
- Keep names concise and stable. Avoid version numbers or overly specific wording
  that would require renaming.
- If the feature belongs to a component that has its own directory (for example,
  `ticdc/`, `tiflash/`, `tiproxy/`, `dm/`), place the file in that directory.
- If the feature is cross-component or general, place it at the repository root.

Examples:

| Feature | Good path | Why |
| --- | --- | --- |
| New TiCDC sink type | `ticdc/ticdc-sink-to-<target>.md` | Follows existing sink docs pattern |
| New SQL statement | `sql-statements/sql-statement-<name>.md` | Follows SQL statement pattern |
| New INFORMATION_SCHEMA table | `information-schema/information-schema-<name>.md` | Follows info schema pattern |
| New general feature | `<feature-name>.md` at root | Matches other root-level features |
| New TiFlash feature | `tiflash/<feature-name>.md` | Component directory |

## Step 3: Determine TOC placement

Every new navigable page requires an entry in the appropriate TOC file.

### Identify the right TOC file

| Content type | TOC file |
| --- | --- |
| TiDB Self-Managed (most common) | `TOC.md` |
| AI, vector search, pytidb, MCP | `TOC-ai.md` |
| Application development guides | `TOC-develop.md` |
| Best practices | `TOC-best-practices.md` |
| API documentation | `TOC-api.md` |
| TiDB release notes | `TOC-tidb-releases.md` |
| TiDB Cloud (Dedicated/general) | `TOC-tidb-cloud.md` |
| TiDB Cloud Starter | `TOC-tidb-cloud-starter.md` |
| TiDB Cloud Essential | `TOC-tidb-cloud-essential.md` |
| TiDB Cloud Premium | `TOC-tidb-cloud-premium.md` |
| TiDB Cloud release notes | `TOC-tidb-cloud-releases.md` |

### Find the right position

1. Search the TOC for the relevant section or category:

   ```bash
   rg -n "<keyword>|<component>" TOC.md
   ```

2. Look at the neighboring entries. TOC entries follow logical grouping:
   - Features of the same component are grouped together.
   - Related features are adjacent (for example, all sink types under
     "Create Changefeeds").
   - Difficulty generally progresses from overview → getting started → usage →
     reference → troubleshooting within each group.

3. Position the new entry:
   - If there is a clear peer group, add the entry adjacent to similar items.
   - If it is the first of a new category, create a new section heading.
   - If it is a sub-feature, nest it under the parent feature entry.

4. Use the correct indentation level (2 spaces per TOC level). The TOC format:

   ```markdown
   - Category Name
     - [Page Title](/path/to/file.md)
     - [Another Page](/path/to/another.md)
       - [Sub Page](/path/to/sub.md)
   ```

### TOC title conventions

- Use title case for TOC entries.
- Keep TOC titles concise (typically 3–7 words).
- Match the document H1 when possible, but shorten for TOC readability.
- Do not include "TiDB" in the TOC title when the context already makes it
  clear.

## Step 4: Write front matter

Every new page needs front matter:

```yaml
---
title: <same as H1, title case, ≤59 characters>
summary: <115–145 characters, starts with a verb, SEO-friendly, reader-focused>
---
```

Rules:

- The `title` must match the H1 heading exactly.
- The `summary` must not start with special characters (`>`, `*`, `#`, `-`, `[`).
- The `summary` should tell readers what they will learn or accomplish.
- Do not add other metadata fields unless there is a specific reason (for
  example, `aliases` for a page that replaces an older URL).

## Step 5: Draft the document

### General structure principles

- Start with what users care about: what the feature does, why it matters, when
  to use it.
- Put conditions and prerequisites before instructions.
- Include realistic, runnable examples where practical.
- Define jargon on first use.
- End with related resources or next steps.

### Structure by doc type

**New feature:**

```
H1: Feature Name
  Intro paragraph (what, why, when)
H2: Usage scenarios
H2: Prerequisites (optional)
H2: Usage / Procedures
  H3: Method 1 (recommended)
  H3: Method 2
H2: Parameter reference (if applicable)
H2: Limitations
H2: Compatibility
H2: FAQ (optional)
H2: More resources
```

**Task:**

```
H1: Task Title
  Intro paragraph (what this doc helps you do)
H2: Prerequisites
H2: Step 1. <action>
H2: Step 2. <action>
H2: Step 3. <action>
H2: What's next
```

**Concept:**

```
H1: Concept Title
  Intro paragraph (what the concept is)
H2: Architecture / Key components
H2: How it works
H2: Key features / Limitations
H2: What's next
```

**Reference:**

```
H1: Reference Title
  Intro paragraph (what this reference covers)
H2: Category 1
  H3: Parameter/item
H2: Category 2
  H3: Parameter/item
```

**Troubleshooting:**

```
H1: Troubleshoot <Problem>
  Intro paragraph (what problems this doc covers)
H2: Common causes
  H3: Cause 1 (Symptom + Solution)
  H3: Cause 2
H2: Other causes
  H3: Cause 3
```

### Co-authoring mode for substantial docs

For documents expected to exceed ~800 words or with unclear scope:

1. Propose the 3–5 core sections first and get confirmation.
2. Start with the section that has the most unknowns or highest user value.
3. Draft section by section, asking focused questions only for facts that cannot
   be derived from code, tests, or existing docs.
4. After drafting, run a reader test: predict 5–10 realistic reader questions and
   verify the doc answers them.
5. Ask whether anything can be removed without losing important information.

## Step 6: Handle associated updates

Creating a new page often requires updates elsewhere:

| Check | Action |
| --- | --- |
| TOC entry added? | Required for all navigable pages |
| Overview page mentions new feature? | Add a brief entry or link if the area has an overview |
| Related docs link to new page? | Add "See also" or inline links where users would benefit |
| `sql-statement-overview.md` updated? | Required for new SQL statements |
| `functions-and-operators-overview.md` updated? | Required for new functions |
| Release notes mention the feature? | Flag for release notes skill if applicable |
| `system-variables.md` references new page? | If the feature has system variables |

## Step 7: Validate

1. Run `./scripts/markdownlint <new-file>` to catch formatting issues.
2. Run `./scripts/verify-links.sh` if the new page has links or is linked from
   other pages.
3. Verify the TOC renders correctly (correct indentation, no orphaned entries).
4. Check front matter: title matches H1, summary is 115–145 characters.
5. Mentally test: can a user who finds this page via search complete their task
   without hidden context?

## Common mistakes to avoid

- Creating a page that is too thin (only 1–2 short sections). Consider whether
  the content fits as a section in an existing page.
- Placing the TOC entry in the wrong file or nesting level.
- Using a file name that duplicates or conflicts with existing names.
- Writing an intro that describes what the document will do instead of starting
  with useful information directly.
- Skipping the overview/reference page updates that help users discover the new
  page.
- Forgetting to handle `aliases` when a new page replaces an older page.
