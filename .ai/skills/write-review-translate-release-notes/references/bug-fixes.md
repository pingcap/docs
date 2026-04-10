# Bug fixes

Rules for the `## Bug fixes` / `## 错误修复` section. The cross-cutting rules in SKILL.md (no trailing period, user perspective, inline-code conventions, and entry suffix) also apply here.

The section structure is identical to Improvements: use `+` for component groups and `-` for entries, with tools nested one level deeper under `+ Tools`. See [improvements.md](improvements.md) for the structure skeleton.

## Contents

- English style rules and templates
- Handling non-deterministic failures (`might` vs `potential`)
- Chinese style rules and templates
- Anti-patterns for both languages

## English style rules

Lead with a fix verb phrase. Use the following accepted patterns, which are listed roughly by frequency in published v6.1+ notes:

- `Fix the issue that [subject] [verb phrase]` (dominant modern pattern)
- `Fix the issue of [noun phrase] that occurs when/during [condition]` (result-first phrasing)
- `Fix the issue of [noun phrase]` (noun-centric, no trigger clause)
- `Fix the [incorrect/inaccurate] [noun]` (standalone, for example, `Fix the incorrect error message ...`)
- `Fix a [rare/potential] issue that [description]` (rare or non-deterministic bugs)
- `Fix the potential/occasional [panic/crash] that occurs when [condition]` (specific crash scenarios)
- `Fix the panic issue caused by [X]` (panic identified by cause)

A complete entry should include three elements: the trigger condition (when it happens), the observed impact (what the user sees), and optionally a workaround.

Wrap exact error messages in backticks: `Fix the issue that TiDB Lightning reports` `` `no database selected` `` `during data import`.

### Handling non-deterministic failures

Both `might` and `potential` are acceptable. Use them as follows:

- Use `might` as an inline modal verb: `Fix the issue that TiDB might crash when ...`
- Use `potential` as an adjective before a noun: `Fix the potential panic that occurs when ...`
- Do not use `may` or `could`.

### English examples (from v7.5.0 and v8.1.0)

```
- Fix the issue that executing SQL statements containing tables with multi-valued indexes might return the `Can't find a proper physical plan for this query` error [#49438](...) @[qw4990](https://github.com/qw4990)
- Fix the issue that automatic statistics collection gets stuck after an OOM error occurs [#51993](...) @[hi-rustin](https://github.com/hi-rustin)
- Fix the issue that after using BR to restore a table that has no statistics, the statistics health of that table is still 100% [#29769](...) @[winoros](https://github.com/winoros)
- Fix the issue that TiDB might crash when `tidb_mem_quota_analyze` is enabled and the memory used by updating statistics exceeds the limit [#52601](...) @[hawkingrei](https://github.com/hawkingrei)
- Fix the incorrect error message displayed when an invalid default value is specified for a column [#51592](...) @[danqixu](https://github.com/danqixu)
- Fix a rare issue that special event timing might cause the data loss in log backup [#16739](...) @[YuJuncen](https://github.com/YuJuncen)
- Fix the panic issue caused by `GetAdditionalInfo` [#8079](...) @[HuSharp](https://github.com/HuSharp)
- Fix the issue that inactive Write Ahead Logs (WALs) in RocksDB might corrupt data [#16705](...) @[Connor1996](https://github.com/Connor1996)
- Fix the issue that the MySQL compression protocol cannot handle large loads of data (>=16M) [#47152](...) [#47157](...) [#47161](...) @[dveeden](https://github.com/dveeden)
```

### English anti-patterns

| Incorrect | Correct |
|-----------|---------|
| `Fixed the issue that ...` (past tense) | `Fix the issue that ...` (imperative) |
| `Fixes an issue where ...` | `Fix the issue that ...` |
| `Fix the issue where ...` | `Fix the issue that ...` (use `that`, not `where`) |
| `Fix the issue that ... may ...` | Use `might` or `potential` |
| Entry ends with `.` | Remove the period |
| `Fix nil pointer panic in getRegionFromTS` (internal function name) | Rewrite to user-observable behavior: `Fix the potential panic that occurs when fetching region information during a Stale Read` |
| `The issue of X causing Y is fixed` | `Fix the issue that X causes Y` |

## Chinese style rules

Lead with `修复` for most entries. The standard templates are:

- `修复 [X] 的问题` (most common)
- `修复 [X] 可能 [崩溃/panic/卡住/报错] 的问题` (non-deterministic failures)
- `修复 [X] 导致 [Y] 的问题` (cause-effect issues)
- `禁止 [X]` (used when the fix introduces a restriction rather than a repair; rare)

Close the description clause with `的问题`. Use `可能` for non-deterministic failures, consistent with the English use of `might`. Do not add `。` at the end.

### Chinese examples (from v7.5.0 and v8.1.0)

```
- 修复 Sort 算子在落盘过程中可能导致 TiDB 崩溃的问题 [#47538](...) @[windtalker](https://github.com/windtalker)
- 修复 HashJoin 算子 Probe 时无法复用 chunk 的问题 [#48082](...) @[wshwsh12](https://github.com/wshwsh12)
- 修复 `COALESCE()` 函数对于 `DATE` 类型参数返回结果类型不正确的问题 [#46475](...) @[xzhangxian1008](https://github.com/xzhangxian1008)
- 修复 `client-go` 中 `batch-client` panic 的问题 [#47691](...) @[crazycs520](https://github.com/crazycs520)
- 修复 MySQL 压缩协议无法处理超大负载数据 (>= 16M) 的问题 [#47152](...) [#47157](...) [#47161](...) @[dveeden](https://github.com/dveeden)
- 禁止非整型聚簇索引进行 split table 操作 [#47350](...) @[tangenta](https://github.com/tangenta)
- 修复采用自适应同步部署模式 (DR Auto-Sync) 的集群在 Placement Rule 的配置较复杂时，`canSync` 和 `hasMajority` 可能计算错误的问题 [#7201](...) @[disksing](https://github.com/disksing)
```

### Chinese anti-patterns

| Incorrect | Correct |
|-----------|---------|
| `修复了 ...` (with `了`) | `修复 ...` (remove `了`) |
| Entry ends with `。` | Remove `。` |
| `修复 ... 的 bug` | `修复 ... 的问题` |
| `解决了 ...` | `修复 ...` |
