---
title: SET_VAR
summary: SET_VAR 用于在单条 SQL 语句中指定优化器 hint，从而对该语句的执行计划进行更细粒度的控制。这包括。
---

# SET_VAR

SET_VAR 用于在单条 SQL 语句中指定优化器 hint，从而对该语句的执行计划进行更细粒度的控制。这包括：

> **Note:**
>
> SET_VAR 将在即将发布的版本中被弃用。建议改用 [SETTINGS 子句](/tidb-cloud-lake/sql/settings-clause.md)。

- 临时配置设置，仅在 SQL 语句执行期间生效。需要注意的是，使用 SET_VAR 指定的设置只会影响当前正在执行语句的结果，不会对整体数据库配置产生任何持久影响。有关可通过 SET_VAR 配置的可用设置列表，请参阅 [SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md)。如需了解其工作方式，请参阅以下示例：

    - [示例 1：临时设置时区](#example-1-temporarily-set-timezone)
    - [示例 2：控制 COPY INTO 的并行处理](#example-2-control-parallel-processing-for-copy-into)

- 使用标签 *deduplicate_label* 控制 [INSERT](/tidb-cloud-lake/sql/insert.md)、[UPDATE](/tidb-cloud-lake/sql/update.md) 或 [REPLACE](/tidb-cloud-lake/sql/replace.md) 操作的去重行为。对于 SQL 语句中带有 deduplicate_label 的这些操作，{{{ .lake }}} 只执行第一条语句，后续具有相同 deduplicate_label 值的语句都会被忽略，无论这些语句原本打算进行何种数据修改。请注意，一旦设置了 deduplicate_label，它将在 24 小时内持续生效。要了解 deduplicate_label 如何帮助去重，请参阅 [示例 3：设置去重标签](#example-3-set-deduplicate-label)。

另请参阅：

- [SETTINGS 子句](/tidb-cloud-lake/sql/settings-clause.md)
- [SET](/tidb-cloud-lake/sql/set.md)

## 语法 {#syntax}

```sql
/*+ SET_VAR(key=value) SET_VAR(key=value) ... */
```

- 该 hint 必须紧跟在作为 SQL 语句开头的 [SELECT](/tidb-cloud-lake/sql/select.md)、[INSERT](/tidb-cloud-lake/sql/insert.md)、[UPDATE](/tidb-cloud-lake/sql/update.md)、[REPLACE](/tidb-cloud-lake/sql/replace.md)、[MERGE](/tidb-cloud-lake/sql/merge.md)、[DELETE](/tidb-cloud-lake/sql/dml.md) 或 [COPY](/tidb-cloud-lake/sql/copy-into-table.md) (INTO) 关键字之后。
- 一个 SET_VAR 只能包含一个 Key=Value 对，这意味着你只能通过一个 SET_VAR 配置一个设置。不过，你可以使用多个 SET_VAR hint 来配置多个设置。
    - 如果多个 SET_VAR hint 包含相同的 key，则第一个 Key=Value 对会生效。
    - 如果某个 key 解析或绑定失败，则所有 hint 都会被忽略。

## 示例 {#examples}

### 示例 1：临时设置时区 {#example-1-temporarily-set-timezone}

```sql
root@localhost> SELECT TIMEZONE();

SELECT
  TIMEZONE();

┌────────────┐
│ timezone() │
│   String   │
├────────────┤
│ UTC        │
└────────────┘

1 row in 0.011 sec. Processed 1 rows, 1B (91.23 rows/s, 91B/s)

root@localhost> SELECT /*+SET_VAR(timezone='America/Toronto') */ TIMEZONE();

SELECT
  /*+SET_VAR(timezone='America/Toronto') */
  TIMEZONE();

┌─────────────────┐
│    timezone()   │
│      String     │
├─────────────────┤
│ America/Toronto │
└─────────────────┘

1 row in 0.023 sec. Processed 1 rows, 1B (43.99 rows/s, 43B/s)

root@localhost> SELECT TIMEZONE();

SELECT
  TIMEZONE();

┌────────────┐
│ timezone() │
│   String   │
├────────────┤
│ UTC        │
└────────────┘

1 row in 0.010 sec. Processed 1 rows, 1B (104.34 rows/s, 104B/s)
```

### 示例 2：控制 COPY INTO 的并行处理 {#example-2-control-parallel-processing-for-copy-into}

在 {{{ .lake }}} 中，*max_threads* 设置指定了可用于执行请求的最大线程数。默认情况下，该值通常设置为与机器上可用的 CPU 核心数一致。

使用 COPY INTO 将数据加载到 {{{ .lake }}} 时，你可以通过在 COPY INTO 命令中注入 hint 并设置 *max_threads* 参数来控制并行处理能力。例如：

```sql
COPY /*+ set_var(max_threads=6) */ INTO mytable FROM @mystage/ pattern='.*[.]parq' FILE_FORMAT=(TYPE=parquet);
```

### 示例 3：设置去重标签 {#example-3-set-deduplicate-label}

```sql
CREATE TABLE t1(a Int, b bool);
INSERT /*+ SET_VAR(deduplicate_label='datalake') */ INTO t1 (a, b) VALUES(1, false);
SELECT * FROM t1;

a|b|
-+-+
1|0|

UPDATE /*+ SET_VAR(deduplicate_label='datalake') */ t1 SET a = 20 WHERE b = false;
SELECT * FROM t1;

a|b|
-+-+
1|0|

REPLACE /*+ SET_VAR(deduplicate_label='datalake') */ INTO t1 on(a,b) VALUES(40, false);
SELECT * FROM t1;

a|b|
-+-+
1|0|

MERGE /*+ SET_VAR(deduplicate_label='datalake') */ INTO t1 using t2 on t1.a = t2.a when matched then update *;
SELECT * FROM t1;

a|b|
-+-+
1|0|
```