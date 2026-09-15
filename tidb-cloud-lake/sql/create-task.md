---
title: CREATE TASK
summary: CREATE TASK 语句用于定义一个新任务，该任务按调度周期或基于 dag 的任务图来执行指定的 SQL 语句。
---

# CREATE TASK

CREATE TASK 语句用于定义一个新任务，该任务按调度周期或基于 dag 的任务图来执行指定的 SQL 语句。

**NOTICE:** 此功能仅在 {{{ .lake }}} 中开箱即用。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
 WAREHOUSE = <string>
 SCHEDULE = { <num> MINUTE | <num> SECOND | USING CRON <expr> <time_zone> }
 [ AFTER <string>
 [ WHEN <boolean_expr> ]
 [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
 [ ERROR_INTEGRATION = <string> ]
 [ COMMENT = '<string_literal>' ]
 [ <session_parameter> = <value> [ , <session_parameter> = <value> ... ] ]
AS
{ <sql_statement>
| BEGIN
    <sql_statement>;
    [ <sql_statement>; ... ]
  END;
}
```

将多个 SQL 语句包装在 `BEGIN ... END;` 块中，以便任务按顺序将它们作为脚本执行。

| 参数 | 描述 |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IF NOT EXISTS                                    | 可选。如果指定，只有在不存在同名任务时才会创建该任务。 |
| name                                             | 任务名称。这是必填字段。 |
| WAREHOUSE                                        | 必填。指定任务使用的虚拟计算集群。 |
| SCHEDULE                                         | 必填。定义任务的运行调度。可以按分钟指定，也可以结合时区使用 CRON 表达式指定。 |
| SUSPEND_TASK_AFTER_NUM_FAILURES                  | 可选。任务在连续失败达到该次数后会被自动挂起。 |
| AFTER                                            | 必须在此任务启动前完成的前置任务列表。 |
| WHEN boolean_expr                                | 任务运行前必须满足的条件。 |
| [ERROR_INTEGRATION](/tidb-cloud-lake/sql/notification.md) | 可选。用于任务错误通知的通知集成名称，并应用特定的 [任务错误载荷](/tidb-cloud-lake/sql/task-error-notification-payload.md) |
| COMMENT                                          | 可选。作为任务注释或描述的字符串字面量。 |
| session_parameter                                | 可选。指定任务运行期间使用的会话参数。注意，在 CREATE TASK 语句中，会话参数必须放在所有其他任务参数之后。 |
| sql                                              | 任务将执行的 SQL 语句。可以是单条语句，也可以是包装在 `BEGIN ... END;` 中的脚本。这是必填字段。 |

### 使用说明 {#usage-notes}

- 独立任务或任务 DAG 中的根任务必须定义调度；否则，该任务只会在使用 EXECUTE TASK 手动执行时运行。
- 任务 DAG 中的子任务不能指定调度。
- 创建任务后，必须先执行 ALTER TASK … RESUME，任务才会根据任务定义中指定的参数开始运行。
- 当 Condition 时，仅支持 `<boolean_expression>` 的一个子集。

    以下内容可在任务的 WHEN 子句中使用：

    - 支持在 SQL 表达式中使用 [STREAM_STATUS](/tidb-cloud-lake/sql/stream-status.md) 进行求值。该函数用于指示指定 stream 是否包含变更跟踪数据。你可以在启动当前运行前，使用该函数判断指定 stream 是否包含变更数据。如果结果为 FALSE，则任务不会运行。
    - 布尔运算符，例如 AND、OR、NOT 等。
    - 数值、字符串和布尔类型之间的类型转换。
    - 比较运算符，例如等于、不等于、大于、小于等。

> **Note:**
>
> 警告：在任务中使用 STREAM_STATUS 时，引用 stream 必须包含数据库名（例如，`STREAM_STATUS('mydb.stream_name')`）。

- 多个任务如果消费同一个表 stream 中的变更数据，将会获取不同的增量数据。当某个任务使用 DML 语句消费 stream 中的变更数据时，stream 会推进偏移量。这样一来，这些变更数据将不再可供下一个任务消费。目前，我们建议仅由单个任务消费一个 stream 中的变更数据。你可以为同一张表创建多个 stream，并由不同任务分别消费。
- 任务在每次执行时不会重试；每次执行都是串行的。脚本中的每条 SQL 都会逐条执行，不会并行执行。这可以确保任务执行的顺序和依赖关系得到维护。
- 基于间隔的任务会严格遵循固定的间隔点。这意味着，如果当前任务的执行时间超过间隔单位，则下一个任务会立即执行；否则，下一个任务会等待直到下一个间隔点触发。例如，如果某个任务定义为 1 秒间隔，而一次任务执行耗时 1.5 秒，则下一个任务会立即执行。如果一次任务执行耗时 0.5 秒，则下一个任务会等待直到下一个 1 秒间隔开始。
- 虽然可以在创建任务时指定会话参数，但你也可以稍后使用 ALTER TASK 语句修改它们。例如：

  ```sql
  ALTER TASK simple_task SET
      enable_query_result_cache = 1,
      query_result_cache_min_execute_secs = 5;
  ```

### 关于 Cron 表达式的重要说明 {#important-notes-on-cron-expressions}

- `SCHEDULE` 参数中使用的 cron 表达式必须**恰好包含 6 个字段**。
- 这些字段分别表示：
  1. **秒** (0-59)
  2. **分** (0-59)
  3. **小时** (0-23)
  4. **每月第几天** (1-31)
  5. **月份** (1-12 或 JAN-DEC)
  6. **星期几** (0-6，其中 0 表示星期日，或 SUN-SAT)

#### Cron 表达式示例 {#example-cron-expressions}

- **太平洋时间每天上午 9:00:00：**
    - `USING CRON '0 0 9 * * *' 'America/Los_Angeles'`

- **每分钟：**
    - `USING CRON '0 * * * * *' 'UTC'`
    - 这表示任务会在每分钟开始时运行一次。

- **每小时的第 15 分钟：**
    - `USING CRON '0 15 * * * *' 'UTC'`
    - 这表示任务会在每小时过 15 分钟时运行一次。

- **每周一中午 12:00:00：**
    - `USING CRON '0 0 12 * * 1' 'UTC'`
    - 这表示任务会在每周一中午运行一次。

- **每月第一天的午夜：**
    - `USING CRON '0 0 0 1 * *' 'UTC'`
    - 这表示任务会在每个月第一天的午夜运行。

- **每个工作日上午 8:30:00：**
    - `USING CRON '0 30 8 * * 1-5' 'UTC'`
    - 这表示任务会在每个工作日（周一到周五）上午 8:30 运行。

## 使用示例 {#usage-examples}

### CRON 调度 {#cron-schedule}

```sql
CREATE TASK my_daily_task
 WAREHOUSE = 'compute_wh'
 SCHEDULE = USING CRON '0 0 9 * * *' 'America/Los_Angeles'
 COMMENT = 'Daily summary task'
AS
 INSERT INTO summary_table SELECT * FROM source_table;
```

在此示例中，创建了一个名为 `my_daily_task` 的任务。它使用 **compute_wh** warehouse 来运行一条 SQL 语句，将 `source_table` 中的数据插入到 `summary_table`。该任务使用 **CRON expression** 进行调度，在**太平洋时间每天上午 9 点**执行。

### 多条语句 {#multiple-statements}

```sql
CREATE TASK IF NOT EXISTS nightly_refresh
 WAREHOUSE = 'etl'
 SCHEDULE = USING CRON '0 0 2 * * *' 'UTC'
AS
BEGIN
    DELETE FROM staging.events WHERE event_time < DATEADD(DAY, -1, CURRENT_TIMESTAMP());
    INSERT INTO mart.events SELECT * FROM staging.events;
END;
```

此示例创建了一个名为 `nightly_refresh` 的任务，用于执行包含多条语句的脚本。该脚本被包装在 `BEGIN ... END;` 中，因此每次任务执行时，都会先运行 DELETE，再运行 INSERT。

### 动态 SQL（EXECUTE IMMEDIATE） {#dynamic-sql-execute-immediate}

```sql
CREATE OR REPLACE TASK log_ingestion
  WAREHOUSE = 'default'
  SCHEDULE = 1 MINUTE
AS
EXECUTE IMMEDIATE $$
BEGIN
    LET path := CONCAT('@mylog/', DATE_FORMAT(CURRENT_DATE - INTERVAL 3 DAY, '%m/%d/'));

    LET sql := CONCAT(
        'COPY INTO logs.web_logs FROM ', path,
        ' PATTERN = ''.*[.]gz'' FILE_FORMAT = (type = NDJSON compression = AUTO) MAX_FILES = 10000'
    );

    EXECUTE IMMEDIATE :sql;
END;
$$;
```

此示例创建了一个每分钟运行一次的任务。它会动态计算 **3 天前**的 stage 路径（例如，`@mylog/12/15/`），构造一条 `COPY INTO` 语句，并通过 `EXECUTE IMMEDIATE` 执行它。

### 自动挂起 {#automatic-suspension}

```sql
CREATE TASK IF NOT EXISTS mytask
 WAREHOUSE = 'system'
 SCHEDULE = 2 MINUTE
 SUSPEND_TASK_AFTER_NUM_FAILURES = 3
AS
 INSERT INTO compaction_test.test VALUES((1));
```

此示例创建了一个名为 `mytask` 的任务（如果它尚不存在）。该任务被分配到 **system** warehouse，并被调度为**每 2 分钟**运行一次。如果它**连续失败三次**，将会被**自动挂起**。该任务会向 `compaction_test.test` 表执行 INSERT 操作。

### 秒级调度 {#second-level-scheduling}

```sql
CREATE TASK IF NOT EXISTS daily_sales_summary
 WAREHOUSE = 'analytics'
 SCHEDULE = 30 SECOND
AS
 SELECT sales_date, SUM(amount) AS daily_total
 FROM sales_data
 GROUP BY sales_date;
```

在此示例中，创建了一个名为 `daily_sales_summary` 的任务，并使用**秒级调度**。它被设置为**每 30 秒**运行一次。该任务使用 **analytics** warehouse，并通过聚合 `sales_data` 表中的数据来计算每日销售汇总。

### 任务依赖 {#task-dependencies}

```sql
CREATE TASK IF NOT EXISTS process_orders
 WAREHOUSE = 'etl'
 AFTER task1
AS
 INSERT INTO data_warehouse.orders SELECT * FROM staging.orders;
```

在此示例中，创建了一个名为 `process_orders` 的任务，并将其定义为在 **task1** 和 **task2** **成功完成之后**运行。这对于在任务的**有向无环图（DAG）**中创建**依赖关系**非常有用。该任务使用 **etl** 计算集群，并将数据从暂存区传输到数据仓库。

> 提示：使用 AFLTER 参数时，无需设置 SCHEDULE 参数。

### 条件执行 {#conditional-execution}

```sql
CREATE TASK IF NOT EXISTS hourly_data_cleanup
 WAREHOUSE = 'maintenance'
 SCHEDULE = USING CRON '0 0 9 * * *' 'America/Los_Angeles'
 WHEN STREAM_STATUS('db1.change_stream') = TRUE
AS
 DELETE FROM archived_data
 WHERE archived_date < DATEADD(HOUR, -24, CURRENT_TIMESTAMP());

```

在此示例中，创建了一个名为 `hourly_data_cleanup` 的任务。它使用 **maintenance** 计算集群，并被调度为**每小时**运行一次。该任务会删除 `archived_data` 表中超过 24 小时的数据。该任务仅会在**满足条件时**运行，即使用 **STREAM_STATUS** 函数检查 `db1.change_stream` 是否包含变更数据。

### 错误集成 {#error-integration}

```sql
CREATE TASK IF NOT EXISTS mytask
 WAREHOUSE = 'mywh'
 SCHEDULE = 30 SECOND
 ERROR_INTEGRATION = 'myerror'
AS
 BEGIN
    BEGIN;
    INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
    DELETE FROM mytable WHERE ts < DATEADD(MINUTE, -5, CURRENT_TIMESTAMP());
    COMMIT;
 END;
```

在此示例中，创建了一个名为 `mytask` 的任务。它使用 **mywh** 计算集群，并被调度为**每 30 秒**运行一次。该任务执行一个 **BEGIN 块**，其中包含一条 INSERT 语句和一条 DELETE 语句。在两条语句都执行后，任务会提交事务。当任务失败时，它将触发名为 **myerror** 的**错误集成**。

### 会话参数 {#session-parameters}

```sql
CREATE TASK IF NOT EXISTS cache_enabled_task
 WAREHOUSE = 'analytics'
 SCHEDULE = 5 MINUTE
 COMMENT = 'Task with query result cache enabled'
 enable_query_result_cache = 1,
 query_result_cache_min_execute_secs = 5
AS
 SELECT SUM(amount) AS total_sales
 FROM sales_data
 WHERE transaction_date >= DATEADD(DAY, -7, CURRENT_DATE())
 GROUP BY product_category;
```

在此示例中，创建了一个名为 `cache_enabled_task` 的任务，并配置了用于启用查询结果缓存的**会话参数**。该任务被调度为**每 5 分钟**运行一次，并使用 **analytics** 计算集群。会话参数 **`enable_query_result_cache = 1`** 和 **`query_result_cache_min_execute_secs = 5`** 被指定在**所有其他任务参数之后**，从而为执行时间至少为 5 秒的查询启用查询结果缓存。如果底层数据没有变化，这可以在后续执行相同任务时**提升性能**。

### 查看任务运行历史 {#view-task-run-history}

使用 `TASK_HISTORY()` 表函数查看任务何时运行以及如何运行：

```sql
SELECT *
FROM TASK_HISTORY(
  TASK_NAME   => 'daily_sales_summary',
  RESULT_LIMIT => 20
)
ORDER BY scheduled_time DESC;
```

有关所有可用选项，请参见 [TASK HISTORY](/tidb-cloud-lake/sql/table-functions.md)，包括按时间范围或 DAG 中的根任务 ID 进行过滤。