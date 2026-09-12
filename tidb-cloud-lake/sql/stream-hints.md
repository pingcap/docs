---
title: WITH Stream Hints
summary: 使用 hints 指定各种 stream 配置选项，以控制 stream 的处理方式。
---

# WITH Stream Hints

使用 hints 指定各种 stream 配置选项，以控制 stream 的处理方式。

另请参阅：[WITH CONSUME](/tidb-cloud-lake/sql/with-consume.md)

## 语法 {#syntax}

```sql
SELECT ...
FROM <stream_name> WITH (<hint1> = <value1>[, <hint2> = <value2>, ...])
```

下表列出了可用的 hints，包括它们的说明以及用于优化 stream 处理的推荐用法：

| Hint             | 说明                                                                                                                                                                               |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `CONSUME`        | 指定此查询是否会消费该 stream。默认值为 `False`。                                                                                                                |
| `MAX_BATCH_SIZE` | 定义从 stream 中每批处理的最大行数。<br/>- 如果未指定，则会处理 stream 中的所有行。<br/>- 不允许在同一事务中对同一个 stream 修改 `MAX_BATCH_SIZE`，否则会报错。<br/>- 对于存在大量变更积压的 stream，例如长时间未被消费的 stream，不建议设置 `MAX_BATCH_SIZE` 或使用较小的值，因为这可能会降低捕获效率。 |

## 示例 {#examples}

在演示之前，先创建一个表，在其上定义一个 stream，并插入两行数据。

```sql
CREATE TABLE t1(a int);
CREATE STREAM s ON TABLE t1;
INSERT INTO t1 values(1);
INSERT INTO t1 values(2);
```

以下示例展示了在查询 stream 时，`MAX_BATCH_SIZE` hint 如何影响每批处理的行数。将 `MAX_BATCH_SIZE` 设置为 1 时，每批只包含一行；将其设置为 2 时，则会在单个批次中处理这两行。

```sql
SELECT * FROM s WITH (CONSUME = FALSE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 1
   change$action: INSERT
change$is_update: false
   change$row_id: de75bebeeb6b4a54bfe05d4d14c83757000000

SELECT * FROM s WITH (CONSUME = FALSE, MAX_BATCH_SIZE = 2);

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│        a        │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│               2 │ INSERT        │ false            │ d2c02e411db84d269dc9f6e32d8444bc000000 │
│               1 │ INSERT        │ false            │ de75bebeeb6b4a54bfe05d4d14c83757000000 │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

以下示例展示了在查询 stream 时，`CONSUME` hint 的工作方式。将 `CONSUME = TRUE` 且 `MAX_BATCH_SIZE = 1` 时，每次查询都会从 stream 中消费一行。

```sql
SELECT * FROM s WITH (CONSUME = TRUE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 1
   change$action: INSERT
change$is_update: false
   change$row_id: de75bebeeb6b4a54bfe05d4d14c83757000000

SELECT * FROM s WITH (CONSUME = TRUE, MAX_BATCH_SIZE = 1);

-[ RECORD 1 ]-----------------------------------
               a: 2
   change$action: INSERT
change$is_update: false
   change$row_id: d2c02e411db84d269dc9f6e32d8444bc000000
```