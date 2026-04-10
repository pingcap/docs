---
name: release-notes
description: Write, review, revise, and translate TiDB release notes for the Compatibility changes, Improvements, and Bug fixes sections in English and Chinese. Use this skill when working with release note entries, aligning English and Chinese content, auditing `release-X.X.X.md` files, or editing files under `docs/releases/` or `docs-cn/releases/`.
---

# TiDB Release Notes

When you write, review, or translate a release note entry, use this skill to load the right references, apply the correct patterns, and produce output that matches the published format in `releases/` (`pingcap/docs` for English, `pingcap/docs-cn` for Chinese) for v6.1.0 and later.

## When to use this skill

Use this skill when the task involves any of the following:

- **Writing a new entry** based on a GitHub PR or issue description
- **Reviewing or revising** an existing English or Chinese release note entry or section (Compatibility changes, Improvements, or Bug fixes), such as correcting the opening verb, tightening the description, or fixing style issues
- **Translating** an entry between English and Chinese, including updating document anchor suffixes and verifying bilingual alignment

This skill applies to the three recurring sections in every `release-X.X.X.md` file: Compatibility changes, Improvements, and Bug fixes.

## Which reference to load

Load only what is necessary for the task:

| Task | Load |
|------|------|
| Compatibility changes (upgrade note block, behavior-change paragraph, system-variable table, config-parameter table, anchor suffixes) | [references/compatibility-changes.md](references/compatibility-changes.md) |
| Improvement entries (opening verbs, English and Chinese patterns, examples) | [references/improvements.md](references/improvements.md) |
| Bug-fix entries (fix templates, anti-patterns, English and Chinese patterns, examples) | [references/bug-fixes.md](references/bug-fixes.md) |
| Translation, bilingual alignment check, or auditing paired files | [references/bilingual-alignment.md](references/bilingual-alignment.md) |

A Chinese-only bug-fix revision does not need the compatibility-changes file. For a full bilingual audit, load all four.

## File-level structure

### English file (`docs/releases/release-X.X.X.md`)

```markdown
---
title: TiDB X.X.X Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB X.X.X.
---

# TiDB X.X.X Release Notes

Release date: Month DD, YYYY

TiDB version: X.X.X

Quick access: [Quick start](https://docs.pingcap.com/tidb/vX.X/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/vX.X/production-deployment-using-tiup)
```

The `summary` value lists the sections actually present in the file, in the same order as the level-2 headings. For example, if the file includes New features, Compatibility changes, Improvements, and Bug fixes, the summary reads: `Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB X.X.X.` If a section is absent, omit it from the summary.

### Chinese file (`docs-cn/releases/release-X.X.X.md`)

```markdown
---
title: TiDB X.X.X Release Notes
summary: 了解 TiDB X.X.X 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB X.X.X Release Notes

发版日期：YYYY 年 M 月 D 日

TiDB 版本：X.X.X

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/vX.X/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/vX.X/production-deployment-using-tiup)
```

### Section heading mapping

| English | Chinese |
|---------|---------|
| `## Compatibility changes` | `## 兼容性变更` |
| `### Behavior changes` | `### 行为变更` |
| `### System variables` | `### 系统变量` |
| `### Configuration parameters` | `### 配置参数` |
| `## Deprecated features` | `## 废弃功能` |
| `## Improvements` | `## 改进提升` |
| `## Bug fixes` | `## 错误修复` |
| `## Performance test` | `## 性能测试` |
| `## Contributors` | `## 贡献者` |

## Rules that apply to every entry

These rules apply to both Improvements and Bug fixes in both languages. The reference files assume these conventions.

### No trailing period

Entries do not end with `.` (English) or `。` (Chinese).

### Write from the user's perspective

Describe what the user observes, not what the code does.

- Bug fixes: start from the GitHub issue description (user-facing symptoms). Avoid exposing internal function or variable names.
- Improvements: use the GitHub PR as a reference, but reframe the entry in terms of user benefit (performance, stability, or capability).
- A complete bug fix describes both the trigger condition and the observed impact. A complete improvement explains what changed and why it benefits the user.

### Inline code

Use backticks for:

- Variable names: `` `tidb_mem_quota_analyze` ``
- Config parameters: `` `raftstore.inspect-interval` ``, command-line flags: `` `--ignore-stats` ``
- SQL keywords in ALL CAPS: `` `HAVING` ``, `` `COUNT DISTINCT` ``, `` `ORDER BY` ``
- SQL functions in ALL CAPS with parentheses: `` `DATE()` ``, `` `STR_TO_DATE()` ``, `` `COUNT()` ``
- Exact error message strings: `` `Can't find a proper physical plan for this query` ``
- Operator or plan names: `` `IndexHashJoin` ``, `` `MPP` ``
- Literal values, ports, sizes: `` `8123` ``, `` `"8KiB"` ``, `` `false` ``

Do not wrap product or component names in prose (TiDB, TiKV, PD, TiFlash, TiCDC), or generic nouns such as "query," "table," or "index," unless referring to a specific named object.

### Entry suffix

Each improvement and bug-fix entry ends with issue link(s) and contributor, in the following format:

```
[#NNNNN](https://github.com/org/repo/issues/NNNNN) @[contributor](https://github.com/contributor)
```

For multiple issues in one entry: `[#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN) [#MMMMM](https://github.com/pingcap/tidb/issues/MMMMM) @[contributor](https://github.com/contributor)`

## Quick reference

### English bug-fix templates

```
- Fix the issue that [subject] [verb phrase]
- Fix the issue that [subject] might [crash/panic/get stuck/return incorrect results]
- Fix the issue of [noun phrase] that occurs when [condition]
- Fix the [incorrect/inaccurate] [noun]
- Fix a [rare/potential] issue that [description]
- Fix the potential [panic/crash] that occurs when [condition]
- Fix the panic issue caused by [X]
```

### Chinese bug-fix templates

```
- 修复 [X] 的问题
- 修复 [X] 可能 [崩溃/panic/卡住/报错/返回错误结果] 的问题
- 修复 [X] 导致 [Y] 的问题
```

### Improvement opening verbs

English: `Support`, `Add`, `Optimize`, `Improve`, `Avoid`, `Enhance`, `Mitigate`, `Accelerate`, `Remove`, `Increase`

Chinese: `支持`、`新增`、`优化`、`提升`、`避免`、`改进`、`引入`、`增加`

For verb selection guidance and examples, see [references/improvements.md](references/improvements.md).

### Compatibility change-type vocabulary

| English | Chinese |
|---------|---------|
| `Newly added` | `新增` |
| `Modified` | `修改` |
| `Deprecated` | `废弃` |
| `Deleted` | `删除` |

Component names in section headers are identical in English and Chinese: `TiDB`, `TiKV`, `PD`, `TiFlash`, `TiDB Lightning`, `BR`, `TiCDC`.
