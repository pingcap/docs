---
title: SHOW SETTINGS
summary: "{{{ .lake }}} 提供了多种系统设置，使你能够控制 {{{ .lake }}} 的工作方式。此命令会显示可用系统设置的当前值、默认值以及设置级别。要修改某个设置，请使用 SET 或 UNSET 命令。"
---

# SHOW SETTINGS

{{{ .lake }}} 提供了多种系统设置，使你能够控制 {{{ .lake }}} 的工作方式。此命令会显示可用系统设置的当前值、默认值以及[设置级别](#setting-levels)。要修改某个设置，请使用 [SET](/tidb-cloud-lake/sql/set.md) 或 [UNSET](/tidb-cloud-lake/sql/unset.md) 命令。

- {{{ .lake }}} 的某些行为无法通过系统设置进行更改；你在使用 {{{ .lake }}} 时必须将这些行为考虑在内。例如：
    - {{{ .lake }}} 会将字符串编码为 UTF-8 字符集。
    - {{{ .lake }}} 对数组使用从 1 开始的编号约定。
- {{{ .lake }}} 将系统设置存储在系统表 [system.settings](/tidb-cloud-lake/sql/system-settings.md) 中。

## 语法 {#syntax}

```sql
SHOW SETTINGS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## 设置级别 {#setting-levels}

每个 {{{ .lake }}} 设置都具有一个级别，可以是 Global、Default 或 Session。下表说明了各个级别之间的区别：

|   级别    |   说明                                                                                                                                                                                                                                                              |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   Global   |   具有此级别的设置会写入 meta service，并影响同一租户中的所有集群。在此级别进行的更改具有全局影响，并会应用于由多个集群共享的整个数据库环境。                                                |
|   Default  |   具有此级别的设置是单个查询实例的服务默认值。在此级别进行的更改只会影响应用该默认值的查询实例。  |
|   Session  |   具有此级别的设置仅限于单个请求或会话。它们的作用域最小，仅适用于当前正在进行的特定会话或请求，从而提供按会话自定义设置的方式。                                       |

## 示例 {#examples}

> **注意：**
>
> 由于 {{{ .lake }}} 会不时修改系统设置，此示例可能不会显示最新结果。要查看 {{{ .lake }}} 中最新的系统设置，请在你的 {{{ .lake }}} 实例中执行 `SHOW SETTINGS;`。

```sql
SHOW SETTINGS LIMIT 5;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                     name                    │  value │ default │   range  │  level  │                                                                     description                                                                    │  type  │
├─────────────────────────────────────────────┼────────┼─────────┼──────────┼─────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┤
│ acquire_lock_timeout                        │ 15     │ 15      │ None     │ DEFAULT │ Sets the maximum timeout in seconds for acquire a lock.                                                                                            │ UInt64 │
│ aggregate_spilling_bytes_threshold_per_proc │ 0      │ 0       │ None     │ DEFAULT │ Sets the maximum amount of memory in bytes that an aggregator can use before spilling data to storage during query execution.                      │ UInt64 │
│ aggregate_spilling_memory_ratio             │ 0      │ 0       │ [0, 100] │ DEFAULT │ Sets the maximum memory ratio in bytes that an aggregator can use before spilling data to storage during query execution.                          │ UInt64 │
│ auto_compaction_imperfect_blocks_threshold  │ 50     │ 50      │ None     │ DEFAULT │ Threshold for triggering auto compaction. This occurs when the number of imperfect blocks in a snapshot exceeds this value after write operations. │ UInt64 │
│ collation                                   │ utf8   │ utf8    │ ["utf8"] │ DEFAULT │ Sets the character collation. Available values include "utf8".                                                                                     │ String │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```