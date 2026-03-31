---
name: writing-doc-summaries
description: Writes or updates the front matter `summary` field in pingcap/docs and pingcap/docs-cn Markdown files. The summary is an SEO-friendly sentence of 115-145 characters. Use when a document is missing a summary, when a reviewer or CI check flags a low-quality summary, or when an existing summary is outdated, inaccurate, or the wrong length.
---

# Writing Doc Summaries

Write or improve the `summary` field in the YAML front matter of Markdown files in `pingcap/docs` and `pingcap/docs-cn`.

## Front matter example

```yaml
---
title: Back up and Restore Data Using Dumpling and TiDB Lightning
summary: Learn how to use Dumpling and TiDB Lightning to back up and restore full data of TiDB.
---
```

## Summary rules

1. **Length**: 115-145 characters including spaces.
2. **Opening verb**: Start with an SEO-friendly verb phrase (see table below) that tells the reader what they will get from this document. Never start with the document title, a product name alone, or a noun phrase.
3. **Perspective**: Reader-focused — tell them what they will learn or do.
4. **No special leading characters**: Do not start with `>`, `*`, `#`, `-`, or `[`.
5. **YAML quoting**: Wrap the value in double quotes if it contains `:` or other YAML special characters.
6. **No redundancy**: Do not repeat the document title word-for-word. Rephrase to add value.
7. **Language**: Match the document body language. Chinese body → Chinese summary.
8. **Self-contained**: Must be understandable without the title or body — it may appear as a standalone search snippet.
9. **Accuracy**: Must match the actual scope of the document. Do not promise content the document does not deliver.
10. **Tone**: Conversational but professional. No marketing language.

## Structure formula

For most document types, a reliable pattern is:

**[Action/Topic] + [Object] + [Outcome/Value]**

| Part | What it covers | Example |
|---|---|---|
| Action/Topic | Opening verb phrase | `Learn how to configure` |
| Object | What the document is about | `TLS encryption between TiDB components` |
| Outcome/Value | What the reader gains or achieves | `to secure data in transit and meet compliance requirements` |

Full example: `Learn how to configure TLS encryption between TiDB components to secure data in transit and meet compliance requirements.`

**Exceptions:**

- **SQL statement reference**: Use fixed template — `An overview of the usage of <STATEMENT> for the TiDB database`. No outcome clause needed.
- **Focused task docs**: Omit the outcome clause if the action and object already imply it and the sentence meets minimum length.

## Opening verb guidance

Scan a few existing summaries in the same subdirectory first to match local conventions.

### Preferred patterns

| Document type | Preferred opening |
|---|---|
| Concept / overview | Learn what, Learn how X works, Learn about, Introduce the concept of |
| Feature introduction | Introduce, Introduce the, Learn about |
| Task / procedure | Learn how to |
| Quick start | Learn how to quickly get started with |
| Configuration | Learn all the configuration options for, Learn how to configure |
| Troubleshooting | Learn how to troubleshoot, Learn how to diagnose |
| SQL statement reference | An overview of the usage of `<STATEMENT>` for the TiDB database |
| Release notes | Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB `<version>` |

### Patterns to avoid

- Starting with the product name alone: `TiDB ...`, `TiKV ...`
- `This document`, `This guide`, `This article`, `This page`
- `Explains`, `Describes` (use `Learn` or `An overview of` instead)
- `The reference for`, `The usage of`
- Repeating the document title word-for-word

## Before and after

**Before** (vague, filler opening, no outcome):

```yaml
summary: This document explains the auto-tune feature of Backup & Restore.
```

**After** (reader-focused, specific, includes outcome):
```yaml
summary: Learn how the BR auto-tune feature automatically limits backup resource usage to reduce impact on online TiDB cluster performance.
```

**Before** (generic, no user intent):
```yaml
summary: An introduction to metadata lock in TiDB.
```

**After** (introduces concept and explains why it matters):
```yaml
summary: Introduce the concept, principles, and implementation of metadata lock in TiDB, and learn how it prevents DDL and DML conflicts.
```

## Workflow

1. **Read** the target Markdown file fully. Note the title, opening paragraph, main sections, scope, and any existing `summary`.

2. **Draft** 2-3 candidate sentences using the structure formula and the opening-verb table.

3. **Validate** each candidate:
   - Count characters. Must be 115-145.
   - Confirm opening verb fits the document type.
   - Confirm it does not promise content the document lacks.
   - Confirm language matches the document body.
   - If it contains `:`, confirm the value is wrapped in double quotes.

4. **If validation fails** → revise and re-validate. Repeat until all checks pass.

5. **Apply** the best candidate:
   - If front matter exists, update the `summary` line in place.
   - If front matter is missing, add it at the top:
     ```yaml
     ---
     title: <existing H1 text, in title case>
     summary: <new summary>
     ---
     ```
   - Preserve all other front matter fields. Do not change the document body.

6. **Final check**: Re-count characters one more time after editing. Confirm `title` matches the H1. Confirm no special leading character without wrapping quotes.

## Output expectations

- Apply the change directly using the Edit tool.
- Report the final summary text and its character count.
- If the existing summary is already acceptable, say so and explain why.
- Prefer a full rewrite over minor edits when the existing summary is structurally weak.
- Do not rewrite or reformat any other part of the document.

## Gut check

Before applying: **would this make a TiDB user want to click through from search results?** If not, rewrite.