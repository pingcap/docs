---
name: release-notes
description: Evaluate whether a change needs a release note. If yes, write, review, revise, or translate TiDB release note entries for the features, compatibility changes, improvements, and bug fixes sections. Use this skill when triaging PRs for release-note relevance, working with release note entries, aligning English and Chinese content, auditing `release-X.X.X.md` files, or editing files under `docs/releases/` or `docs-cn/releases/`.
---

# TiDB Release Notes

When you evaluate whether a change needs a release note, write, review, or translate a release note entry (including feature descriptions, compatibility changes, improvements, and bug fixes), use this skill to load the right references, apply the correct patterns, and produce output that matches the published format in `releases/` (`pingcap/docs` for English, `pingcap/docs-cn` for Chinese) for v6.1.0 and later.

## When to use this skill

Use this skill when the task involves any of the following:

- **Evaluating whether a change needs a release note** based on a GitHub PR, issue, or set of changes — and returning a `None(reason)` verdict when it does not
- **Writing a new feature description** for the Feature details or Features section based on a GitHub PR, issue description, or product brief
- **Writing a new entry** for the Compatibility changes, Improvements, or Bug fixes section based on a GitHub PR or issue description
- **Reviewing or revising** an existing English or Chinese release note entry or section, such as correcting the structure, tightening the description, or fixing style issues
- **Translating** an entry between English and Chinese, including updating document anchor suffixes and verifying bilingual alignment

This skill applies to the recurring sections in every `release-X.X.X.md` file: Feature details / Features, Compatibility changes, Improvements, and Bug fixes.

## Determine whether a change needs a release note

Not every PR or change warrants a release note. Before writing, determine whether the change is visible to TiDB users or operators.

### User-visible changes (write a release note)

- Bug fixes that change query results, upgrade behavior, privilege checks, error messages, or compatibility
- New features, new SQL syntax or function support, or new configuration options
- Meaningful performance improvements observable in common operations
- Behavior changes that affect upgrade paths, tooling integration, or operational workflows
- Default value changes for system variables or configuration parameters

### Internal-only changes (no release note needed)

- Test-only changes: new test cases, flaky test fixes, test infrastructure updates
- Pure refactors or internal data-structure changes with no user-observable effect
- Added or improved debug/internal logs that do not surface in user-facing interfaces
- Internal CI/CD pipeline changes or developer workflow changes
- Code comments or source-code-only documentation changes (not user-facing docs)

### Borderline cases

If a PR is mostly internal but the outcome is user-visible, write a release note that describes the outcome and omit the implementation details. If the only user-facing effect is indirect or speculative, lean toward `None(reason)`.

### Return a "no release note needed" verdict

When a change does not need a release note, return:

```
Release note is not needed: <reason>
```

Use a short reason in parentheses. Examples:

- `Release note is not needed: test-only change`
- `Release note is not needed: internal refactor, no user-visible effect`
- `Release note is not needed: flaky test fix`
- `Release note is not needed: added internal debug logging`

### Handle cherry-pick and backport PRs

Cherry-pick or backport PRs sometimes contain sparse descriptions. When evaluating one:

1. Read the backport PR first.
2. If the backport PR body omits details, follow the link to the original upstream PR and its linked issues.
3. Base the release note on the actual behavior change described in the original PR or issue, not the cherry-pick mechanics.
4. Ignore cherry-pick metadata (such as "cherry-pick from #XXXXX") in the release note text.

## Which reference to load

Load only what is necessary for the task:

| Task | Load |
|------|------|
| Feature descriptions (title line, before-after structure, GA/experimental tags, examples) | [references/feature-description.md](references/feature-description.md) |
| Compatibility changes (upgrade note block, behavior-change paragraph, system-variable table, config-parameter table, anchor suffixes) | [references/compatibility-changes.md](references/compatibility-changes.md) |
| Improvement entries (opening verbs, English and Chinese patterns, examples) | [references/improvements.md](references/improvements.md) |
| Bug-fix entries (fix templates, anti-patterns, English and Chinese patterns, examples) | [references/bug-fixes.md](references/bug-fixes.md) |
| Translation, bilingual alignment check, or auditing paired files | [references/bilingual-alignment.md](references/bilingual-alignment.md) |

A Chinese-only bug-fix revision does not need the compatibility-changes file. For a full bilingual audit, load all five.

## File-level structure

### English file (`docs/releases/release-X.X.X.md`)

```markdown
---
title: TiDB X.X.X Release Notes
summary: Learn about the features, compatibility changes, improvements, and bug fixes in TiDB X.X.X.
---

# TiDB X.X.X Release Notes

Release date: Month DD, YYYY

TiDB version: X.X.X

Quick access: [Quick start](https://docs.pingcap.com/tidb/vX.X/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/vX.X/production-deployment-using-tiup)
```

The `summary` value lists the sections actually present in the file, in the same order as the level-2 headings. If a section is absent, omit it from the summary. Examples:

- With all sections: `Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB X.X.X.`
- Without features: `Learn about the compatibility changes, improvements, and bug fixes in TiDB X.X.X.`

### Chinese file (`docs-cn/releases/release-X.X.X.md`)

```markdown
---
title: TiDB X.X.X Release Notes
summary: 了解 TiDB X.X.X 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB X.X.X Release Notes

发版日期：YYYY 年 M 月 D 日

TiDB 版本：X.X.X

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/vX.X/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/vX.X/production-deployment-using-tiup)
```

### Section heading mapping

| English | Chinese |
|---------|---------|
| `## Feature details` | `## 功能详情` |
| `## Features` | `## 功能` |
| `### Scalability` | `### 可扩展性` |
| `### Performance` | `### 性能` |
| `### Reliability` | `### 稳定性` |
| `### Availability` | `### 可用性` |
| `### SQL` | `### SQL` |
| `### DB Operations and Observability` | `### 数据库管理与可观测性` |
| `### DB operations` | `### 数据库管理` |
| `### Observability` | `### 可观测性` |
| `### Security` | `### 安全` |
| `### Data Migration` | `### 数据迁移` |
| `## Compatibility changes` | `## 兼容性变更` |
| `### Behavior changes` | `### 行为变更` |
| `### System variables` | `### 系统变量` |
| `### Configuration parameters` | `### 配置参数` |
| `## Deprecated features` | `## 废弃功能` |
| `## Improvements` | `## 改进提升` |
| `## Bug fixes` | `## 错误修复` |
| `## Performance test` | `## 性能测试` |
| `## Contributors` | `## 贡献者` |

## Cross-cutting rules

These rules apply to all sections (Features, Compatibility changes, Improvements, and Bug fixes) in both languages. Each reference file assumes these conventions.

### Write from the user's perspective

Describe what the user observes, gains, or can do — not what the code does internally.

- Feature descriptions: explain the capability, the problem it solves, and the user benefit.
- Improvements: use the GitHub PR as a reference, but reframe the entry in terms of user benefit (performance, stability, or capability).
- Bug fixes: start from the GitHub issue description (user-facing symptoms). Avoid exposing internal function or variable names.
- A complete bug fix describes both the trigger condition and the observed impact. A complete improvement explains what changed and why it benefits the user. A complete feature description covers the before state, the after state, and the user value.

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

### Issue and PR author links

Every entry (feature, improvement, or bug fix) ends with issue link(s) and PR author link(s) on the title line:

```
[#NNNNN](https://github.com/org/repo/issues/NNNNN) @[pr_author](https://github.com/pr_author)
```

The `@` link is the **author of the PR that resolves the issue**, not the issue author. When an issue has linked PRs, find the PR author(s) from those PRs.

For multiple issues: `[#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN) [#MMMMM](https://github.com/pingcap/tidb/issues/MMMMM) @[pr_author](https://github.com/pr_author)`

### No trailing period on single-line entries

Improvement and bug-fix entries (single-line entries starting with `-`) do not end with `.` (English) or `。` (Chinese).

Feature entries follow a different convention: the title line (starting with `*`) omits the trailing period, but body paragraphs use normal sentence punctuation. See [references/feature-description.md](references/feature-description.md) for details.

### Component names

Component names are identical in English and Chinese across all sections: `TiDB`, `TiKV`, `PD`, `TiFlash`, `TiDB Lightning`, `BR`, `TiCDC`.
