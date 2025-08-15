---
title: Manage Queries That Consume More Resources Than Expected (Runaway Queries)
summary: Introduces how to control and degrade queries with excessive resource consumption (Runaway Queries) through resource management capabilities.
---

# Manage Queries That Consume More Resources Than Expected (Runaway Queries)

A runaway query is a query that consumes more time or resources than expected. The term **runaway queries** is used in the following to describe the feature of managing the runaway query.

- Starting from v7.2.0, the resource control feature introduces the management of runaway queries. You can set criteria for a resource group to identify runaway queries and automatically take actions to prevent them from exhausting resources and affecting other queries. You can manage runaway queries for a resource group by including the `QUERY_LIMIT` field in [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) or [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md).
- Starting from v7.3.0, the resource control feature introduces manual management of runaway watches, enabling quick identification of runaway queries for a given SQL statement or Digest. You can execute the statement [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) to manually manage the runaway queries watch list in the resource group.

For more information about the resource control feature, see [Use Resource Control to Achieve Resource Group Limitation and Flow Control](/tidb-resource-control-ru-groups.md).

## `QUERY_LIMIT` parameters

If a query exceeds any of the following limits, it is identified as a runaway query:

- `EXEC_ELAPSED`: checks whether the query execution time exceeds the limit. This rule applies to read and write DML statements.
- `PROCESSED_KEYS`: checks whether the number of keys processed by the Coprocessor exceeds the limit. This rule only applies to read statements.
- `RU`: checks whether the total number of read and write RUs consumed by the statement exceeds the limit. This rule only applies to read statements.

Supported operations (`ACTION`):

- `DRYRUN`: no action is taken. The records are appended for the runaway queries. This is mainly used to observe whether the condition setting is reasonable.
- `COOLDOWN`: the execution priority of the query is lowered to the lowest level. The query continues to execute with the lowest priority and does not occupy resources of other operations.
- `KILL`: the identified query is automatically terminated and reports an error `Query execution was interrupted, identified as runaway query`.
- `SWITCH_GROUP`: introduced in v8.4.0, this parameter switches the identified query to the specified resource group for continued execution. After this query completes, subsequent SQL statements are executed in the original resource group. If the specified resource group does not exist, the query remains in the original resource group.

To avoid too many concurrent runaway queries that exhaust system resources, the resource control feature introduces a quick identification mechanism, which can quickly identify and isolate runaway queries. You can use this feature through the `WATCH` clause. When a query is identified as a runaway query, this mechanism extracts the matching feature (defined by the parameter after `WATCH`) of the query. In the next period of time (defined by `DURATION`), the matching feature of the runaway query is added to the watch list, and the TiDB instance matches queries with the watch list. The matching queries are directly marked as runaway queries and isolated according to the corresponding action, instead of waiting for them to be identified by conditions. The `KILL` operation terminates the query and reports an error `Quarantined and interrupted because of being in runaway watch list`.

There are three methods for `WATCH` to match for quick identification:

- `EXACT` indicates that only SQL statements with exactly the same SQL text are quickly identified.
- `SIMILAR` indicates all SQL statements with the same pattern are matched by SQL Digest, and the literal values are ignored.
- `PLAN` indicates all SQL statements with the same pattern are matched by Plan Digest.

The `DURATION` option in `WATCH` indicates the duration of the identification item, which is infinite by default.

After a watch item is added, neither the matching feature nor the `ACTION` is changed or deleted whenever the `QUERY_LIMIT` configuration is changed or deleted.

You can use `QUERY WATCH REMOVE` to remove a watch item, or use `QUERY WATCH REMOVE RESOURCE GROUP` (New in v9.0.0) to remove all watch items of a specific resource group in a batch.

The parameters of `QUERY_LIMIT` are as follows:

| Parameter          | Description            | Note                                  |
|---------------|--------------|--------------------------------------|
| `EXEC_ELAPSED`  | When the query execution time exceeds this value, it is identified as a runaway query | EXEC_ELAPSED =`60s` means the query is identified as a runaway query if it takes more than 60 seconds to execute. |
| `PROCESSED_KEYS` | When the number of keys processed by the Coprocessor exceeds this value, the query is identified as a runaway query | `PROCESSED_KEYS = 1000` means the query is identified as a runaway query if the number of keys processed by the Coprocessor exceeds 1000. |
| `RU`  | When the total number of read and write RUs consumed by the query exceeds this value, this query is identified as a runaway query | `RU = 1000` means the query is identified as a runaway query if the total number of read and write RUs consumed by the query exceeds 1000. |
| `ACTION`    | Action taken when a runaway query is identified | The optional values are `DRYRUN`, `COOLDOWN`, `KILL`, and `SWITCH_GROUP`. |
| `WATCH`   | Quickly match the identified runaway query. If the same or similar query is encountered again within a certain period of time, the corresponding action is performed immediately. | Optional. For example, `WATCH=SIMILAR DURATION '60s'`, `WATCH=EXACT DURATION '1m'`, and `WATCH=PLAN`. |

> **Note:**
>
> If you want to strictly limit runaway queries to a specific resource group, it is recommended to use `SWITCH_GROUP` together with the [`QUERY WATCH`](#query-watch-parameters) statement. Because `QUERY_LIMIT` only triggers the corresponding `ACTION` operation when the query meets the criteria, `SWITCH_GROUP` might not be able to switch the query to the target resource group in a timely manner in such scenarios.

## Examples

1. Create a resource group `rg1` with a quota of 500 RUs per second, and define a runaway query as one that exceeds 60 seconds, and lower the priority of the runaway query.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2. Change the `rg1` resource group to terminate the runaway queries, and mark the queries with the same pattern as runaway queries immediately in the next 10 minutes.

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3. Change the `rg1` resource group to cancel the runaway query check.

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

## `QUERY WATCH` parameters

For more information about the synopsis of `QUERY WATCH`, see [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md).

The parameters are as follows:

- The `RESOURCE GROUP` specifies a resource group. The matching features of runaway queries added by this statement are added to the watch list of the resource group. This parameter can be omitted. If omitted, it applies to the `default` resource group.
- The meaning of `ACTION` is the same as `QUERY LIMIT`. This parameter can be omitted. If omitted, the corresponding action after identification adopts the `ACTION` configured by `QUERY LIMIT` in the resource group, and the action does not change with the `QUERY LIMIT` configuration. If there is no `ACTION` configured in the resource group, an error is reported.
- The `QueryWatchTextOption` parameter has three options: `SQL DIGEST`, `PLAN DIGEST`, and `SQL TEXT`.
    - `SQL DIGEST` is the same as that of `SIMILAR`. The following parameters accept strings, user-defined variables, or other expressions that yield string result. The string length must be 64, which is the same as the Digest definition in TiDB.
    - `PLAN DIGEST` is the same as `PLAN`. The following parameter is a Digest string.
    - `SQL TEXT` matches the input SQL as a raw string (`EXACT`), or parses and compiles it into `SQL DIGEST` (`SIMILAR`) or `PLAN DIGEST` (`PLAN`), depending on the following parameter.

- Add a matching feature to the runaway query watch list for the default resource group (you need to set `QUERY LIMIT` for the default resource group in advance).

    ```sql
    QUERY WATCH ADD ACTION KILL SQL TEXT EXACT TO 'select * from test.t2';
    ```

- Add a matching feature to the runaway query watch list for the `rg1` resource group by parsing the SQL into SQL Digest. When `ACTION` is not specified, the `ACTION` option already configured for the `rg1` resource group is used.

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- Add a matching feature to the runaway query watch list for the `rg1` resource group by parsing the SQL into SQL Digest, and specify `ACTION` as `SWITCH_GROUP(rg2)`.

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION SWITCH_GROUP(rg2) SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- Add a matching feature to the runaway query watch list for the `rg1` resource group using `PLAN DIGEST`, and specify `ACTION` as `KILL`.

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

- Get the watch item ID by querying `INFORMATION_SCHEMA.RUNAWAY_WATCHES` and delete the watch item.

    ```sql
    SELECT * from information_schema.runaway_watches ORDER BY id\G
    ```

    ```sql
    *************************** 1. row ***************************
                     ID: 1
    RESOURCE_GROUP_NAME: default
             START_TIME: 2024-09-09 03:35:31
               END_TIME: 2024-09-09 03:45:31
                  WATCH: Exact
            WATCH_TEXT: SELECT variable_name, variable_value FROM mysql.global_variables
                 SOURCE: 127.0.0.1:4000
                ACTION: Kill
                RULE: ProcessedKeys = 666(10)
    1 row in set (0.00 sec)
    ```

    ```sql
    QUERY WATCH REMOVE 1;
    ```

- <span class="version-mark">New in v9.0.0</span> Remove all watch items of a specific resource group:

    ```sql
    QUERY WATCH REMOVE RESOURCE GROUP rg1;
    ```

## Observability

You can get more information about runaway queries from the following system tables and `INFORMATION_SCHEMA`:

+ The `mysql.tidb_runaway_queries` table contains the history records of all runaway queries identified in the past 7 days. Take one of the rows as an example:

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_runaway_queries LIMIT 1\G
    *************************** 1. row ***************************
    resource_group_name: default
         start_time: 2024-09-09 17:43:42
            repeats: 2
         match_type: watch
             action: kill
         sample_sql: select sleep(2) from t
         sql_digest: 4adbc838b86c573265d4b39a3979d0a362b5f0336c91c26930c83ab187701a55
        plan_digest: 5d094f78efbce44b2923733b74e1d09233cb446318293492901c5e5d92e27dbc
        tidb_server: 127.0.0.1:4000
    ```

    Field description:

    - `start_time` indicates the time when the runaway query is identified.
    - `repeats` indicates the number of times the runaway query has been identified since `start_time`.
    - `match_type` indicates how the runaway query is identified. The value can be one of the following:
        - `identify` means that it matches the condition of the runaway query.
        - `watch` means that it matches the quick identification rule in the watch list.

+ The `information_schema.runaway_watches` table contains records of quick identification rules for runaway queries. For more information, see [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md).
