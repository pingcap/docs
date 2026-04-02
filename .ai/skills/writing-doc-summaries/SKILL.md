---
name: writing-doc-summaries
description: Writes or updates the front matter `summary` field in pingcap/docs and pingcap/docs-cn Markdown files. The summary targets 115-145 characters, with a 45-character absolute minimum. Use when a document is missing a summary, when a reviewer or CI check flags a low-quality summary, or when an existing summary is outdated, inaccurate, or the wrong length.
---

# Writing Doc Summaries

Write or improve the `summary` field in the YAML front matter of Markdown files in `pingcap/docs` and `pingcap/docs-cn`.

## Front matter example

```yaml
---
title: Performance Analysis and Tuning
summary: Learn how to optimize database system based on database time and how to utilize the TiDB Performance Overview dashboard for performance analysis and tuning.
---
```

## Summary rules

1. **Length**: Target 115-145 characters including spaces; 45 characters is the absolute minimum.
2. **Opening verb**: Start with an SEO-friendly verb phrase (see [Opening verb guidance](#opening-verb-guidance)) that tells the reader what they will get from this document. Never start with the document title, a product name alone, or a noun phrase.
3. **Perspective**: Reader-focused — tell them what they will learn or do.
4. **No special leading characters**: Do not start with `>`, `*`, `#`, `-`, or `[`. If the summary must begin with a special character, wrap the entire value in quotation marks.
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

- **SQL statement reference**: Use fixed template — `An overview of the usage of <STATEMENT> for the TiDB database`. No outcome clause needed. This template falls below the 115-character target; the 45-character absolute minimum still applies.
- **Focused task docs**: Omit the outcome clause if the action and object already imply it and the sentence meets minimum length.

## Opening verb guidance

Scan a few existing summaries in the same subdirectory first to match local conventions.

### Preferred patterns

| Document type | Preferred opening (English) | Preferred opening (Chinese) |
|---|---|---|
| Concept / overview | Learn what, Learn how X works, Learn about, Introduce the concept of | 介绍 X 的概念、了解 X 的原理、本文介绍 |
| Feature introduction | Introduce, Introduce the, Learn about | 介绍、了解 |
| Task / procedure | Learn how to | 了解如何、学习如何 |
| Quick start | Learn how to quickly get started with | 了解如何快速上手 |
| Configuration | Learn all the configuration options for, Learn how to configure | 介绍 X 的配置、了解 X 的配置项 |
| Troubleshooting | Learn how to troubleshoot, Learn how to diagnose | 了解如何定位和处理 X、介绍 X 的排查思路 |
| SQL statement reference | An overview of the usage of `<STATEMENT>` for the TiDB database | TiDB 数据库中 `<STATEMENT>` 的使用概况 |
| Release notes | Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB `<version>` | 了解 TiDB `<version>` 版本的新功能、兼容性变更、改进提升，以及错误修复 |

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
summary: Learn about the concept, principles, and implementation of metadata lock in TiDB, and understand how it prevents DDL and DML conflicts.
```

**Before** (filler opening, no outcome):

```yaml
summary: 本文介绍了 TiDB 的元数据锁功能。
```

**After** (reader-focused, includes concept and value):

```yaml
summary: 介绍 TiDB 元数据锁的概念、原理和实现，了解它如何防止 DDL 与 DML 操作之间的冲突。
```

**Before** (generic, no user intent):

```yaml
summary: BR 自动调节功能说明。
```

**After** (specific, includes outcome):

```yaml
summary: 了解 BR 自动调节功能如何自动限制备份资源用量，从而降低对 TiDB 在线集群性能的影响。
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
