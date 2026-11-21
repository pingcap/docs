---
title: Configure Trigger Rules for Slow Queries
summary: Define the trigger rules for slow query logs.
---

# Configure Trigger Rules for Slow Queries

<CustomContent platform="tidb">

This document describes how to use the [`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) system variable to define the trigger rules for [slow query logs](/identify-slow-queries.md).

[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) supports multi-dimensional metric combinations. It is suitable for "targeted sampling" and "problem reproduction" of slow query logs, enabling you to filter target statements based on specific metric combinations.

For TiDB Self-Managed, the triggering behavior of slow query logs depends on the configuration of `tidb_slow_log_rules`:

- If the current session has no applicable `tidb_slow_log_rules` rule (either because this variable is not set or because none of the configured rules apply to the session), slow query logging still relies on [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) (in milliseconds).
- If the current session has any applicable `tidb_slow_log_rules` rules, slow query logging is determined by the rule matching results, and [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) is ignored.

</CustomContent>
<CustomContent platform="tidb-cloud">

In the [TiDB Cloud console](https://tidbcloud.com/), you can view slow queries on the [**Slow Query**](/tidb-cloud/tune-performance.md#slow-query) tab of the [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) page.

By default, SQL queries that take more than 300 milliseconds are considered as slow queries. To configure the trigger rules for slow queries, you can modify the [`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) system variable.

[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules) supports multi-dimensional metric combinations. It is suitable for "targeted sampling" and "problem reproduction" of slow queries, enabling you to filter target statements based on specific metric combinations.

</CustomContent>

## Examples

- Standard format (`SESSION` scope):

    ```sql
    SET SESSION tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- Invalid `SESSION` rule (`SESSION` scope does not support `Conn_ID`):

    ```sql
    SET SESSION tidb_slow_log_rules = 'Conn_ID: 12, Query_time: 0.5, Is_internal: false';
    ```

<CustomContent platform="tidb">

- Global rule (applies to all connections):

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- Global rules for specific connections (applied separately to the two connections `Conn_ID:11` and `Conn_ID:12`):

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Conn_ID: 11, Query_time: 0.5, Is_internal: false; Conn_ID: 12, Query_time: 0.6, Process_time: 0.3, DB: db1';
    ```

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

- Global rule (applies to all connections):

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

- Global rules for specific connections (applied separately to the two connections `Conn_ID:11` and `Conn_ID:12`):

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Conn_ID: 11, Query_time: 0.5, Is_internal: false; Conn_ID: 12, Query_time: 0.6, Process_time: 0.3, DB: db1';
    ```

</CustomContent>

## Unified rule syntax and type constraints

- Rule capacity and separation: each supported scope can contain a maximum of 10 rules. Rules are separated by `;`.
- Condition format: each condition uses the format `field_name:value`. Multiple conditions within a single rule are separated by `,`.
- Field names are case-insensitive. Underscores and other characters in field names are preserved.

<CustomContent platform="tidb">

TiDB Self-Managed supports both `SESSION` and `GLOBAL` rules for `tidb_slow_log_rules`. A single session can have up to 20 active rules across the two scopes. `SESSION` rules do not support `Conn_ID`; only `GLOBAL` rules support this field.

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

TiDB Cloud Dedicated supports both `SESSION` and `GLOBAL` rules for `tidb_slow_log_rules`. A single session can have up to 20 active rules across the two scopes. `SESSION` rules do not support `Conn_ID`; only `GLOBAL` rules support this field.

</CustomContent>

<CustomContent platform="tidb-cloud" plan="essential,premium">

TiDB Cloud Essential and TiDB Cloud Premium support only `SESSION` rules for `tidb_slow_log_rules`. Therefore, `Conn_ID`, which is available only in `GLOBAL` rules, is not supported.

</CustomContent>

- Matching semantics:
    - Numeric fields except `Conn_ID` are matched using `>=`. `Conn_ID`, string fields, and boolean fields are matched using equality (`=`).
    - Matching for `DB` and `Resource_group` is case-insensitive.
    - Explicit operators such as `>`, `<`, and `!=` are not supported.

Type constraints are as follows:

- Numeric types (`int64`, `uint64`, `float64`) require values greater than or equal to `0`. Negative values result in a parsing error.
    - `int64`: the maximum value is `2^63-1`.
    - `uint64`: the maximum value is `2^64-1`.
    - `float64`: values must be finite and non-negative. The maximum value is approximately `1.79e308`. `NaN` and infinite values such as `Inf` and `-Inf` are invalid and result in an error.
- `bool`: supports `true`/`false`, `1`/`0`, and `t`/`f` (case-insensitive).
- `string`: currently does not support strings containing the separators `,` (condition separator) or `;` (rule separator), even with quotes (single or double). Escaping is not supported.
- Duplicate fields: if the same field is specified multiple times in a single rule, the last occurrence takes effect.

## Supported fields

The fields in the following table follow the general matching and type rules described in [Unified rule syntax and type constraints](#unified-rule-syntax-and-type-constraints), unless otherwise noted.

| Field name | Type | Unit | Description |
| --- | --- | --- | --- |
| `Conn_ID` | `uint` | count | The connection ID (session ID). This field uses exact matching. For example, `Conn_ID:3` matches only logs whose session ID is `3`. This field is supported only in `GLOBAL` rules. |
| `Session_alias` | `string` | none | The alias of the current session. |
| `DB` | `string` | none | The current database. Matching is case-insensitive. |
| `Exec_retry_count` | `uint` | count | The retry times of this statement. This field is usually for pessimistic transactions in which the statement is retried when the lock fails. |
| `Query_time` | `float` | second | The execution time of a statement. |
| `Parse_time` | `float` | second | The parsing time for the statement. |
| `Compile_time` | `float` | second | The duration of the query optimization. |
| `Rewrite_time` | `float` | second | The time consumed for rewriting the query of this statement. |
| `Optimize_time` | `float` | second | The time consumed for optimizing the execution plan. |
| `Wait_TS` | `float` | second | The waiting time of the statement to get transaction timestamps. |
| `Is_internal` | `bool` | none | Whether a SQL statement is internal to TiDB. `true` indicates that the statement is executed internally in TiDB, and `false` indicates that the statement is executed by the user. |
| `Digest` | `string` | none | The fingerprint of the SQL statement. |
| `Plan_digest` | `string` | none | The digest of the execution plan. |
| `Num_cop_tasks` | `int` | count | The number of Coprocessor tasks sent by this statement. |
| `Mem_max` | `int` | bytes | The maximum memory space used during the execution period of a SQL statement. |
| `Disk_max` | `int` | bytes | The maximum disk space used during the execution period of a SQL statement. |
| `Write_sql_response_total` | `float` | second | The time consumed for sending the results back to the client by this statement. |
| `Succ` | `bool` | none | Whether a statement is executed successfully. |
| `Resource_group` | `string` | none | The resource group that the statement is bound to. Matching is case-insensitive. |
| `KV_total` | `float` | second | The time spent on all the RPC requests to TiKV or TiFlash by this statement. |
| `PD_total` | `float` | second | The time spent on all the RPC requests to PD by this statement. |
| `Process_time` | `float` | second | The total processing time of a SQL statement in TiKV. Because data is sent to TiKV concurrently, this value might exceed `Query_time`. |
| `Backoff_time` | `float` | second | The waiting time before retrying when a statement encounters errors that require a retry. Common errors include lock conflicts, Region splits, and busy TiKV servers. |
| `Total_keys` | `uint` | count | The number of keys that Coprocessor has scanned. |
| `Process_keys` | `uint` | count | The number of keys that Coprocessor has processed. Compared with `Total_keys`, `Process_keys` does not include old versions of MVCC. A large difference between `Process_keys` and `Total_keys` indicates that many old versions exist. |
| `cop_mvcc_read_amplification` | `float` | ratio | The MVCC read amplification ratio, calculated as `Total_keys / Process_keys`. |
| `Prewrite_time` | `float` | second | The duration of the first phase (prewrite) of the two-phase transaction commit. |
| `Commit_time` | `float` | second | The duration of the second phase (commit) of the two-phase transaction commit. |
| `Write_keys` | `uint` | count | The count of keys that the transaction writes to the Write CF in TiKV. |
| `Write_size` | `uint` | bytes | The total size of the keys or values to be written when the transaction commits. |
| `Prewrite_region` | `uint` | count | The number of TiKV Regions involved in the first phase (prewrite) of the two-phase transaction commit. Each Region triggers a remote procedure call. |

## Effective behavior and matching order

- Setting `tidb_slow_log_rules` overwrites the existing rules in the specified scope instead of appending new rules.
- Setting `tidb_slow_log_rules` to an empty string clears the rules in the specified scope.
- Multiple rules are combined with `OR`, while multiple field conditions within a single rule are combined with `AND`.
- If you still want to use SQL execution time as a condition for writing slow query logs, use `Query_time` in the rule and note that the unit is seconds.

<CustomContent platform="tidb">

TiDB Self-Managed supports both `SESSION` and `GLOBAL` rules for `tidb_slow_log_rules`.

- If the current session has any applicable rules, such as `SESSION` rules, `GLOBAL` rules for the current `Conn_ID`, or generic `GLOBAL` rules without `Conn_ID`, slow query log output is determined by the rule matching results, and `tidb_slow_log_threshold` is ignored.
- If the current session has no applicable rules, for example, when both `SESSION` and `GLOBAL` rules are empty or only `GLOBAL` rules that do not match the current `Conn_ID` are configured, slow query logging still depends on `tidb_slow_log_threshold`. The unit of `tidb_slow_log_threshold` is milliseconds.
- TiDB matches `SESSION` rules first. If none matches, TiDB then matches `GLOBAL` rules for the current `Conn_ID`, followed by generic `GLOBAL` rules without `Conn_ID`.
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` and `SELECT @@SESSION.tidb_slow_log_rules` return the `SESSION` rule text, or an empty string if unset. `SELECT @@GLOBAL.tidb_slow_log_rules` returns the `GLOBAL` rule text.

</CustomContent>

<CustomContent platform="tidb-cloud" plan="dedicated">

TiDB Cloud Dedicated supports both `SESSION` and `GLOBAL` rules for `tidb_slow_log_rules`.

- If the current session has any applicable rules, such as `SESSION` rules, `GLOBAL` rules for the current `Conn_ID`, or generic `GLOBAL` rules without `Conn_ID`, slow query log output is determined by the rule matching results.
- If the current session has no applicable rules, for example, when both `SESSION` and `GLOBAL` rules are empty or only `GLOBAL` rules that do not match the current `Conn_ID` are configured, the rules for slow query logging fall back to the default one: SQL queries that take more than 300 milliseconds are considered as slow queries.
- TiDB matches `SESSION` rules first. If none matches, TiDB then matches `GLOBAL` rules for the current `Conn_ID`, followed by generic `GLOBAL` rules without `Conn_ID`.
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` and `SELECT @@SESSION.tidb_slow_log_rules` return the `SESSION` rule text, or an empty string if unset. `SELECT @@GLOBAL.tidb_slow_log_rules` returns the `GLOBAL` rule text.

</CustomContent>

<CustomContent platform="tidb-cloud" plan="essential,premium">

TiDB Cloud Essential and TiDB Cloud Premium support only `SESSION` rules for `tidb_slow_log_rules`.

- If the current session has any `SESSION` rules, slow query log output is determined by the rule matching results.
- `SHOW VARIABLES LIKE 'tidb_slow_log_rules'` and `SELECT @@SESSION.tidb_slow_log_rules` return the `SESSION` rule text, or an empty string if unset.

</CustomContent>

## Recommendations

- `tidb_slow_log_rules` is designed to replace the single-threshold approach. It supports combinations of multi-dimensional metric conditions, enabling more flexible and fine-grained control over slow query logging.

- In a well-provisioned test environment with 1 TiDB node (16 CPU cores, 48 GiB memory) and 3 TiKV nodes (each with 16 CPU cores and 48 GiB memory), repeated sysbench tests show that performance impact remains small when multi-dimensional slow query log rules generate millions of slow log entries within 30 minutes. However, when the log volume reaches tens of millions, TPS drops significantly and latency increases noticeably. Therefore, if business workload is high or CPU and memory resources are close to their limits, configure `tidb_slow_log_rules` carefully to avoid log flooding caused by overly broad rules. <CustomContent platform="tidb">If you need to limit the log output rate, use [`tidb_slow_log_max_per_sec`](/system-variables.md#tidb_slow_log_max_per_sec) to throttle it and reduce the impact on business performance.</CustomContent>
