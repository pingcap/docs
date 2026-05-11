# Improvements

Rules for the `## Improvements` / `## 改进提升` section. The cross-cutting rules in SKILL.md (no trailing period, user perspective, inline-code conventions, and entry suffix) also apply here.

## Contents

- Section structure and component grouping
- English style rules and opening verbs
- English examples
- Chinese style rules and opening verbs
- Chinese examples
- Common review findings

## Section structure

```markdown
## Improvements

+ TiDB

    - Entry one [#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN) @[contributor](https://github.com/contributor)
    - Entry two [#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN) @[contributor](https://github.com/contributor)

+ TiKV

    - Entry [#NNNNN](https://github.com/tikv/tikv/issues/NNNNN) @[contributor](https://github.com/contributor)

+ PD

    - Entry [#NNNNN](https://github.com/tikv/pd/issues/NNNNN) @[contributor](https://github.com/contributor)

+ TiFlash

    - Entry [#NNNNN](https://github.com/pingcap/tiflash/issues/NNNNN) @[contributor](https://github.com/contributor)

+ Tools

    + Backup & Restore (BR)

        - Entry [#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN) @[contributor](https://github.com/contributor)

    + TiCDC

        - Entry [#NNNNN](https://github.com/pingcap/tiflow/issues/NNNNN) @[contributor](https://github.com/contributor)

    + TiDB Lightning

        - Entry [#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN) @[contributor](https://github.com/contributor)
```

Component groups use `+`, and individual entries use `-`. Tools are nested one level deeper under `+ Tools`.

## English style rules

Lead with an action verb. Do not start with "This improves..." or "The X now supports...".

State the user benefit explicitly. Explain why the change matters in terms of performance, stability, or capability. For example, instead of "Not use the stale read request's `start_ts` to update `max_ts`," write "Avoid excessive commit request retrying by not using the Stale Read request's `start_ts` to update `max_ts`."

Metric claims are encouraged when sourced, such as "up to 10 times performance improvement" or "improves performance by up to 62.5%."

### Opening verbs

| Verb | When to use |
|------|-------------|
| `Support` | New capability: ```Support casting the `STRING` type to the `DOUBLE` type``` |
| `Add` | New element or mechanism: `Add a timeout mechanism for LDAP authentication` |
| `Optimize` | Algorithmic improvement: `Optimize the non-joined data in right outer join using multiple threads` |
| `Improve` | General improvement: `Improve the MySQL compatibility of ...` |
| `Avoid` | Eliminate a problem: `Avoid excessive commit request retrying by ...` |
| `Enhance` | Capability expansion |
| `Mitigate` | Risk or stability improvement |
| `Accelerate` | Speed improvement |
| `Remove` | Cleanup or deprecation |
| `Increase` | Raise a limit or capacity |

### English examples (from v7.5.0 and v8.1.0)

```
- Improve the MySQL compatibility of expression default values displayed in the output of `SHOW CREATE TABLE` [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
- Support adding multiple indexes concurrently in the ingest mode [#52596](https://github.com/pingcap/tidb/issues/52596) @[lance6716](https://github.com/lance6716)
- Add a timeout mechanism for LDAP authentication to avoid the issue of resource lock (RLock) not being released in time [#51883](https://github.com/pingcap/tidb/issues/51883) @[YangKeao](https://github.com/YangKeao)
- Avoid performing IO operations on snapshot files in Raftstore threads to improve TiKV stability [#16564](https://github.com/tikv/tikv/issues/16564) @[Connor1996](https://github.com/Connor1996)
- Significantly improve the stability of data replication in transaction conflict scenarios, with up to 10 times performance improvement [#10896](https://github.com/pingcap/tiflow/issues/10896) @[CharlesCheung96](https://github.com/CharlesCheung96)
- Improve the performance of adding indexes with `tidb_ddl_enable_fast_reorg` enabled. In internal tests, v7.5.0 improves the performance by up to 62.5% compared with v6.5.0. [#47757](https://github.com/pingcap/tidb/issues/47757) @[tangenta](https://github.com/tangenta)
```

## Chinese style rules

Lead with one of the approved opening verbs (see table below). Do not add `。` at the end.

Use a colon to introduce elaboration in compound improvements: `优化 ANALYZE 流程：引入 [...] 以......，从而......`

For performance metrics, use Chinese expressions such as `性能最高提升 62.5%`.

### Opening verbs

| Verb | When to use |
|------|-------------|
| `优化` | Algorithmic or architectural optimization |
| `提升` | Performance improvement |
| `支持` | New capability |
| `新增` | New metric, parameter, or function |
| `避免` | Eliminate a problem |
| `改进` | General improvement |
| `引入` | Introduce a new mechanism |
| `增加` | Raise a limit or capacity |

Do not start with `改善了...`. Rewrite to `优化`, `提升`, `改进`, or `支持` as appropriate.

### Chinese examples (from v7.5.0 and v8.1.0)

```
- 优化合并分区表的全局统计信息的并发模型：引入 [`tidb_enable_async_merge_global_stats`] 实现同时加载统计信息并进行合并，从而加速分区表场景下全局统计信息的生成 [#47219](...) @[hawkingrei](https://github.com/hawkingrei)
- 支持在 ingest 模式下同时添加多个索引 [#52596](...) @[lance6716](https://github.com/lance6716)
- 新增 LDAP 认证的超时机制，避免 RLock 未及时释放的问题 [#51883](...) @[YangKeao](https://github.com/YangKeao)
- 避免在 Raftstore 线程中对快照文件执行 IO 操作以提高 TiKV 稳定性 [#16564](...) @[Connor1996](https://github.com/Connor1996)
- 提升启用索引加速功能 `tidb_ddl_enable_fast_reorg` 后添加索引的性能，在内部测试中 v7.5.0 相比 v6.5.0 性能最高提升 62.5% [#47757](...) @[tangenta](https://github.com/tangenta)
```

## Common review findings

| Problem | Fix |
|---------|-----|
| Entry starts with "This improvement..." or "The X now supports..." | Rewrite to start with an action verb |
| Entry ends with `.` | Remove |
| Describes only what the code does without user benefit | Add a benefit clause (performance, stability, or capability) |
| Chinese entry starts with `改善了...` | Use `优化`, `提升`, `改进`, or `支持` |
| SQL function not in backtick ALL CAPS format with parentheses | `date()` should be `` `DATE()` `` |
| SQL keyword not in ALL CAPS backticks | `having` should be `` `HAVING` `` |
| Issue link missing | Add at least one `[#NNNNN](https://github.com/pingcap/tidb/issues/NNNNN)` |
| Contributor missing | Add `@[contributor](https://github.com/contributor)` |
