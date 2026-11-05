---
title: BUCKET
summary: サポートされている値を、固定数のハッシュバケットのいずれかにマッピングします。
---

# BUCKET

サポートされている値を、固定数のハッシュバケットのいずれかにマッピングします。`BUCKET()` は、`0` から `bucket_count - 1` までの決定的な `UInt32` 値を返し、[`PARTITION BY`](/tidb-cloud-lake/guides/partition-by.md) および `CLUSTER BY` 式向けに設計されています。

## 構文 {#syntax}

```sql
BUCKET(<bucket_count>, <value>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|----------|-------------|
| `bucket_count` | `1` から `4294967295` までの整数です。`PARTITION BY` または `CLUSTER BY` 式では、定数リテラルである必要があります。 |
| `value` | ハッシュ化する整数、文字列、日付、またはタイムスタンプ値です。 |

いずれかの引数が `NULL` の場合、この関数は `NULL` を返します。

> **Note:**
>
> バケットの結果は値のデータ型に対して安定していますが、同じ論理値でも異なるデータ型で表現されると、異なるバケットにマッピングされる可能性があります。バケット化されたキーのデータ型は変更しないでください。

## 例 {#examples}

```sql
-- Returns an integer from 0 through 15.
SELECT BUCKET(16, 'customer-123');
```

固定のバケット数を使用して、高カーディナリティのキーをパーティション分割します。

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id));
```

分散取り込みでは、評価後のパーティション値が同じ行を同じライターにルーティングできます。

```sql
CREATE TABLE customer_events_distributed (
    customer_id BIGINT,
    event_time  TIMESTAMP
)
PARTITION BY (BUCKET(32, customer_id))
WRITE_DISTRIBUTION_MODE = 'hash';
```

`WRITE_DISTRIBUTION_MODE = 'hash'` には `PARTITION BY` 句が必要です。