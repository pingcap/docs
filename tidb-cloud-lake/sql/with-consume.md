---
title: WITH CONSUME
summary: 在 SELECT 查询中消费 stream 中的数据。
---

# WITH CONSUME

在 SELECT 查询中消费 stream 中的数据。

另请参阅：[WITH Stream Hints](/tidb-cloud-lake/sql/stream-hints.md)

## 语法 {#syntax}

```sql
SELECT ...
FROM <stream_name> WITH CONSUME [ AS <alias> ]
[ WHERE <conditions> ]
```

> **注意：**
>
> 只要查询成功执行，`WITH CONSUME` 子句就会消费该 stream 捕获的所有数据，即使通过 `WHERE` 条件只查询了其中一部分数据也是如此。

## 示例 {#examples}

假设有一个名为 `s` 的 stream，它捕获了以下数据：

```sql
SELECT * FROM s;

┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│        a        │   change$action  │              change$row_id             │ change$is_update │
├─────────────────┼──────────────────┼────────────────────────────────────────┼──────────────────┤
│               3 │ INSERT           │ 4942372d864147e98188f3b486ec18d2000000 │ false            │
│               1 │ DELETE           │ 3df95ad8552e4967a704e1c7209d3dff000000 │ false            │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

如果现在使用 `WITH CONSUME` 查询该 stream，将得到以下结果：

```sql
SELECT
  a
FROM
  s WITH CONSUME AS ss
WHERE
  ss.change$action = 'INSERT';

┌─────────────────┐
│        a        │
├─────────────────┤
│               3 │
└─────────────────┘
```

此时该 stream 已为空，因为上述查询已经消费了 stream 中当时存在的所有数据。

```sql
-- empty results
SELECT * FROM s;
```