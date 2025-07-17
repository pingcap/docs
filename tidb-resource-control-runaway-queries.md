---
title: 管理消耗资源超出预期的查询（Runaway Queries）
summary: 介绍如何通过资源管理能力控制和降级资源消耗过多的查询（Runaway Queries）。
---

# 管理消耗资源超出预期的查询（Runaway Queries）

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

Runaway query 指的是消耗时间或资源超出预期的查询。以下将使用 **runaway queries** 一词来描述管理 runaway query 的功能。

- 从 v7.2.0 版本开始，资源控制功能引入了对 runaway queries 的管理。你可以为资源组设置条件，以识别 runaway queries，并自动采取措施防止其耗尽资源，影响其他查询。你可以在 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) 或 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) 中包含 `QUERY_LIMIT` 字段来管理 runaway queries。
- 从 v7.3.0 版本开始，资源控制功能引入了手动管理 runaway watches，支持快速识别特定 SQL 语句或 Digest 的 runaway 查询。你可以执行 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) 语句，手动管理资源组中的 runaway 查询监控列表。

关于资源控制功能的更多信息，请参见 [使用资源控制实现资源组限制和流控](/tidb-resource-control-ru-groups.md)。

## `QUERY_LIMIT` 参数

如果查询超过以下任一限制，即被识别为 runaway 查询：

- `EXEC_ELAPSED`：检查查询执行时间是否超过限制。此规则适用于读写 DML 语句。
- `PROCESSED_KEYS`：检查 Coprocessor 处理的键数量是否超过限制。此规则仅适用于读语句。
- `RU`：检查查询消耗的总读写 RUs 是否超过限制。此规则仅适用于读语句。

支持的操作（`ACTION`）：

- `DRYRUN`：不采取任何操作。将记录追加到 runaway 查询的记录中，主要用于观察条件设置是否合理。
- `COOLDOWN`：将查询的执行优先级降至最低。查询以最低优先级继续执行，不占用其他操作的资源。
- `KILL`：自动终止识别出的查询，并报告错误 `Query execution was interrupted, identified as runaway query`。
- `SWITCH_GROUP`：在 v8.4.0 版本引入，将识别出的查询切换到指定的资源组以继续执行。该查询完成后，后续 SQL 语句在原资源组中执行。如果指定的资源组不存在，查询将保持在原资源组。

为了避免大量并发 runaway 查询耗尽系统资源，资源控制功能引入了快速识别机制，可以快速识别并隔离 runaway 查询。你可以通过 `WATCH` 子句使用此功能。当查询被识别为 runaway 查询时，该机制会提取匹配的特征（由 `WATCH` 后的参数定义）。在接下来的时间段（由 `DURATION` 定义）内，匹配的 runaway 查询特征会被加入监控列表，TiDB 实例会匹配监控列表中的查询。匹配的查询会被直接标记为 runaway 查询，并根据对应的操作进行隔离，而不是等待条件识别。`KILL` 操作会终止查询并报告错误 `Quarantined and interrupted because of being in runaway watch list`。

`WATCH` 快速识别的三种匹配方式：

- `EXACT` 表示只快速识别完全相同 SQL 文本的语句。
- `SIMILAR` 表示匹配所有具有相同模式的 SQL Digest，忽略字面值。
- `PLAN` 表示匹配所有具有相同模式的 Plan Digest。

`WATCH` 中的 `DURATION` 选项表示识别项的持续时间，默认为无限。

添加监控项后，无论 `QUERY_LIMIT` 配置如何变更或删除，匹配特征和 `ACTION` 都不会被更改或删除。你可以使用 `QUERY WATCH REMOVE` 来移除监控项。

`QUERY_LIMIT` 的参数如下：

| 参数             | 描述                                                         | 备注                                                         |
|------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| `EXEC_ELAPSED`   | 当查询执行时间超过此值时，识别为 runaway 查询                     | `EXEC_ELAPSED = '60s'` 表示如果查询执行时间超过 60 秒，则识别为 runaway 查询。 |
| `PROCESSED_KEYS` | 当 Coprocessor 处理的键数量超过此值时，识别为 runaway 查询             | `PROCESSED_KEYS = 1000` 表示如果 Coprocessor 处理的键数超过 1000，则识别为 runaway 查询。 |
| `RU`             | 当查询消耗的总读写 RUs 超过此值时，识别为 runaway 查询                | `RU = 1000` 表示如果查询消耗的读写 RUs 总数超过 1000，则识别为 runaway 查询。 |
| `ACTION`         | 识别为 runaway 查询后采取的操作                                    | 可选值为 `DRYRUN`、`COOLDOWN`、`KILL` 和 `SWITCH_GROUP`。 |
| `WATCH`          | 快速匹配识别的 runaway 查询。如果在一定时间内再次遇到相同或相似的查询，则立即执行对应操作。 | 可选。例如，`WATCH=SIMILAR DURATION '60s'`、`WATCH=EXACT DURATION '1m'` 和 `WATCH=PLAN`。 |

> **Note:**
>
> 如果你希望严格限制 runaway 查询到某个特定资源组，建议结合 [`QUERY WATCH`](#query-watch-parameters) 语句使用 `SWITCH_GROUP`。因为 `QUERY_LIMIT` 仅在查询满足条件时触发对应的 `ACTION` 操作，在此类场景中，`SWITCH_GROUP` 可能无法及时将查询切换到目标资源组。

## 示例

1. 创建一个资源组 `rg1`，配额为每秒 500 RUs，定义超时超过 60 秒的查询为 runaway 查询，并降低其优先级。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2. 将 `rg1` 资源组设置为终止 runaway 查询，并在接下来的 10 分钟内立即将匹配相同模式的查询标记为 runaway 查询。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3. 将 `rg1` 资源组设置为取消 runaway 查询检测。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

## `QUERY WATCH` 参数

关于 `QUERY WATCH` 的详细说明，请参见 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)。

参数如下：

- `RESOURCE GROUP` 指定一个资源组。由此语句添加的 runaway 查询匹配特征会加入到该资源组的监控列表中。此参数可省略，省略时适用于 `default` 资源组。
- `ACTION` 的含义与 `QUERY LIMIT` 相同。此参数可省略，省略后识别后采取的操作会采用资源组中通过 `QUERY LIMIT` 配置的 `ACTION`，且不会随 `QUERY LIMIT` 配置变化而变化。如果资源组中未配置 `ACTION`，会报错。
- `QueryWatchTextOption` 有三种选项：`SQL DIGEST`、`PLAN DIGEST` 和 `SQL TEXT`。
    - `SQL DIGEST` 与 `SIMILAR` 相同。后续参数接受字符串、用户变量或其他表达式，结果为字符串。字符串长度必须为 64，与 TiDB 中的 Digest 定义相同。
    - `PLAN DIGEST` 与 `PLAN` 相同。后续参数为 Digest 字符串。
    - `SQL TEXT` 表示将输入的 SQL 作为原始字符串（`EXACT`）匹配，或解析并编译成 `SQL DIGEST`（`SIMILAR`）或 `PLAN DIGEST`（`PLAN`），具体取决于后续参数。

- 添加匹配特征到默认资源组的 runaway 查询监控列表（需要提前为默认资源组设置 `QUERY LIMIT`）。

    ```sql
    QUERY WATCH ADD ACTION KILL SQL TEXT EXACT TO 'select * from test.t2';
    ```

- 通过解析 SQL 为 SQL Digest，将匹配特征添加到 `rg1` 资源组的 runaway 查询监控列表。当未指定 `ACTION` 时，使用 `rg1` 资源组已配置的 `ACTION`。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- 通过解析 SQL 为 SQL Digest，将匹配特征添加到 `rg1` 资源组的 runaway 查询监控列表，并将 `ACTION` 指定为 `SWITCH_GROUP(rg2)`。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION SWITCH_GROUP(rg2) SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

- 使用 `PLAN DIGEST` 将匹配特征添加到 `rg1` 资源组的 runaway 查询监控列表，并将 `ACTION` 指定为 `KILL`。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

- 通过查询 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 获取监控项 ID，并删除监控项。

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

## 可观察性

你可以通过以下系统表和 `INFORMATION_SCHEMA` 获取关于 runaway 查询的更多信息：

+ `mysql.tidb_runaway_queries` 表包含过去 7 天内所有识别的 runaway 查询的历史记录。以一行数据为例：

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

    - `start_time` 表示识别出 runaway 查询的时间。
    - `repeats` 表示自 `start_time` 以来识别出的次数。
    - `match_type` 表示识别方式。值可以是以下之一：
        - `identify` 表示符合 runaway 查询条件。
        - `watch` 表示符合监控列表中的快速识别规则。

+ `information_schema.runaway_watches` 表包含 runaway 查询的快速识别规则记录。更多信息请参见 [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md)。
