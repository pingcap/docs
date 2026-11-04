---
title: BUCKET
summary: 将受支持的值映射到固定数量的哈希桶之一。
---

# BUCKET

将受支持的值映射到固定数量的哈希桶之一。`BUCKET()` 会返回一个确定性的 `UInt32` 值，范围为 `0` 到 `bucket_count - 1`，并且专为 [`PARTITION BY`](/tidb-cloud-lake/guides/partition-by.md) 和 `CLUSTER BY` 表达式而设计。

## 语法 {#syntax}

```sql
BUCKET(<bucket_count>, <value>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|----------|-------------|
| `bucket_count` | 取值范围为 `1` 到 `4294967295` 的整数型。在 `PARTITION BY` 或 `CLUSTER BY` 表达式中，它必须是一个常量字面量。 |
| `value` | 要进行哈希计算的整数型、字符串、日期或时间戳值。 |

当任一参数为 `NULL` 时，该函数返回 `NULL`。

> **Note:**
>
> 对于某个值的数据类型而言，bucket 结果是稳定的；但同一个逻辑值如果使用不同的数据类型表示，可能会映射到不同的 bucket。请避免更改已进行 bucket 处理的键的数据类型。

## 示例 {#examples}

```sql
-- Returns an integer from 0 through 15.
SELECT BUCKET(16, 'customer-123');
```

使用固定的 bucket 数量对高基数键进行分区：

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id));
```

对于分布式写入，具有相同分区计算值的行可以被路由到同一个 writer：

```sql
CREATE TABLE customer_events_distributed (
    customer_id BIGINT,
    event_time  TIMESTAMP
)
PARTITION BY (BUCKET(32, customer_id))
WRITE_DISTRIBUTION_MODE = 'hash';
```

`WRITE_DISTRIBUTION_MODE = 'hash'` 需要 `PARTITION BY` 子句。