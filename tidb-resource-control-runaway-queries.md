---
title: 管理超出预期资源消耗的查询（Runaway Queries）
summary: 介绍如何通过资源管理能力控制和降级资源消耗过多的查询（Runaway Queries）。
---

# 管理超出预期资源消耗的查询（Runaway Queries）

> **Note:**
>
> 此功能不适用于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。

Runaway query 指的是消耗时间或资源超出预期的查询。下文中使用 **runaway queries** 来描述对这类查询的管理功能。

- 从 v7.2.0 开始，资源控制功能引入了 runaway queries 管理。你可以为资源组设置判定 runaway queries 的条件，并自动采取措施，防止其耗尽资源并影响其他查询。你可以通过在 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 或 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 语句中包含 `QUERY_LIMIT` 字段来为资源组管理 runaway queries。
- 从 v7.3.0 开始，资源控制功能引入了 runaway watch 的手动管理，支持针对指定 SQL 语句或 Digest 快速识别 runaway queries。你可以执行 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) 语句，手动管理资源组中的 runaway queries watch 列表。

关于资源控制功能的更多信息，参见 [使用资源控制实现资源组限制与流控](/tidb-resource-control-ru-groups.md)。

## `QUERY_LIMIT` 参数

如果查询超出了以下任一限制，则会被判定为 runaway query：

- `EXEC_ELAPSED`：检查查询执行时间是否超出限制。该规则适用于读写 DML 语句。
- `PROCESSED_KEYS`：检查 Coprocessor 处理的 key 数量是否超出限制。该规则仅适用于读语句。
- `RU`：检查语句消耗的读写 RU 总数是否超出限制。该规则仅适用于读语句。

支持的操作（`ACTION`）：

- `DRYRUN`：不采取任何操作，仅记录 runaway queries。主要用于观察条件设置是否合理。
- `COOLDOWN`：将查询的执行优先级降至最低。查询以最低优先级继续执行，不再占用其他操作的资源。
- `KILL`：自动终止被判定的查询，并报错 `Query execution was interrupted, identified as runaway query`。
- `SWITCH_GROUP`：v8.4.0 引入，该参数将被判定的查询切换到指定资源组继续执行。该查询完成后，后续 SQL 语句仍在原资源组中执行。如果指定的资源组不存在，查询仍留在原资源组。

为避免过多并发 runaway queries 耗尽系统资源，资源控制功能引入了快速识别机制，可快速识别并隔离 runaway queries。你可以通过 `WATCH` 子句使用该功能。当查询被判定为 runaway query 时，该机制会提取查询的匹配特征（由 `WATCH` 后的参数定义）。在接下来的时间段内（由 `DURATION` 定义），runaway query 的匹配特征会被加入 watch 列表，TiDB 实例会将后续查询与 watch 列表进行匹配。匹配到的查询会被直接标记为 runaway query 并按对应操作隔离，无需等待条件再次判定。`KILL` 操作会终止查询并报错 `Quarantined and interrupted because of being in runaway watch list`。

`WATCH` 支持三种快速识别匹配方式：

- `EXACT` 表示仅对 SQL 文本完全相同的语句进行快速识别。
- `SIMILAR` 表示对 SQL Digest 相同的所有语句进行匹配，忽略字面量值。
- `PLAN` 表示对 Plan Digest 相同的所有语句进行匹配。

`WATCH` 中的 `DURATION` 选项表示识别项的持续时间，默认为无限。

添加 watch 项后，无论 `QUERY_LIMIT` 配置如何变更或删除，匹配特征和 `ACTION` 都不会被更改或删除。你可以使用 `QUERY WATCH REMOVE` 移除 watch 项。

`QUERY_LIMIT` 的参数如下：

| 参数                | 描述            | 说明                                  |
|---------------------|-----------------|---------------------------------------|
| `EXEC_ELAPSED`      | 当查询执行时间超过该值时，被判定为 runaway query | `EXEC_ELAPSED = '60s'` 表示查询执行超过 60 秒即被判定为 runaway query。 |
| `PROCESSED_KEYS`    | 当 Coprocessor 处理的 key 数量超过该值时，被判定为 runaway query | `PROCESSED_KEYS = 1000` 表示 Coprocessor 处理的 key 数量超过 1000 即被判定为 runaway query。 |
| `RU`                | 当查询消耗的读写 RU 总数超过该值时，被判定为 runaway query | `RU = 1000` 表示查询消耗的读写 RU 总数超过 1000 即被判定为 runaway query。 |
| `ACTION`            | 被判定为 runaway query 时采取的操作 | 可选值为 `DRYRUN`、`COOLDOWN`、`KILL` 和 `SWITCH_GROUP`。 |
| `WATCH`             | 快速匹配已判定的 runaway query。如果在一定时间内再次遇到相同或相似的查询，立即执行对应操作。 | 可选。例如，`WATCH=SIMILAR DURATION '60s'`、`WATCH=EXACT DURATION '1m'`、`WATCH=PLAN`。 |

> **Note:**
>
> 如果你希望严格限制 runaway queries 到指定资源组，建议结合 `SWITCH_GROUP` 和 [`QUERY WATCH`](#query-watch-参数) 语句使用。因为 `QUERY_LIMIT` 仅在查询满足条件时才触发对应 `ACTION` 操作，在此类场景下，`SWITCH_GROUP` 可能无法及时将查询切换到目标资源组。

## 示例

1. 创建资源组 `rg1`，每秒配额 500 RU，并将执行超过 60 秒的查询定义为 runaway query，降低其优先级。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2. 修改资源组 `rg1`，将 runaway queries 直接终止，并在接下来的 10 分钟内对相同模式的查询立即标记为 runaway query。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3. 修改资源组 `rg1`，取消 runaway query 检查。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

## `QUERY WATCH` 参数

关于 `QUERY WATCH` 的语法详情，参见 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)。

参数说明如下：

- `RESOURCE GROUP` 指定资源组。该语句添加的 runaway query 匹配特征会加入该资源组的 watch 列表。该参数可省略，省略时应用于 `default` 资源组。
- `ACTION` 的含义与 `QUERY LIMIT` 相同。该参数可省略，省略时，识别后采取的操作采用资源组中 `QUERY LIMIT` 配置的 `ACTION`，且该操作不会随 `QUERY LIMIT` 配置变更而变更。如果资源组未配置 `ACTION`，则会报错。
- `QueryWatchTextOption` 参数有三种选项：`SQL DIGEST`、`PLAN DIGEST` 和 `SQL TEXT`。
    - `SQL DIGEST` 与 `SIMILAR` 相同。后续参数可为字符串、用户自定义变量或其他返回字符串结果的表达式。字符串长度需为 64，与 TiDB 中 Digest 定义一致。
    - `PLAN DIGEST` 与 `PLAN` 相同。后续参数为 Digest 字符串。
    - `SQL TEXT` 以原始字符串（`EXACT`）匹配输入 SQL，或根据后续参数解析编译为 `SQL DIGEST`（`SIMILAR`）或 `PLAN DIGEST`（`PLAN`）。

- 为默认资源组的 runaway query watch 列表添加一个匹配特征（需提前为默认资源组设置 `QUERY LIMIT`）。

    ```sql
    QUERY WATCH ADD ACTION KILL SQL TEXT EXACT TO 'select * from test.t2';
    ```

- 通过解析 SQL 为 SQL Digest，为 `rg1` 资源组的 runaway query watch 列表添加一个匹配特征。未指定 `ACTION` 时，使用 `rg1` 资源组已配置的 `ACTION` 选项。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- 通过解析 SQL 为 SQL Digest，为 `rg1` 资源组的 runaway query watch 列表添加一个匹配特征，并指定 `ACTION` 为 `SWITCH_GROUP(rg2)`。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION SWITCH_GROUP(rg2) SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- 通过 `PLAN DIGEST` 为 `rg1` 资源组的 runaway query watch 列表添加一个匹配特征，并指定 `ACTION` 为 `KILL`。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

- 通过查询 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 获取 watch 项 ID 并删除该 watch 项。

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

## 可观测性

你可以通过以下系统表和 `INFORMATION_SCHEMA` 获取更多 runaway queries 相关信息：

+ `mysql.tidb_runaway_queries` 表包含过去 7 天内所有被判定为 runaway query 的历史记录。以下为其中一行示例：

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

    字段说明：

    - `start_time` 表示被判定为 runaway query 的时间。
    - `repeats` 表示自 `start_time` 起该 runaway query 被判定的次数。
    - `match_type` 表示 runaway query 的识别方式。可选值如下：
        - `identify` 表示匹配 runaway query 条件。
        - `watch` 表示匹配 watch 列表中的快速识别规则。

+ `information_schema.runaway_watches` 表包含 runaway query 快速识别规则的记录。更多信息参见 [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md)。