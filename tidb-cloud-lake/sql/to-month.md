---
title: TO_MONTH
summary: 将日期或带时间的日期（timestamp/datetime）转换为包含月份编号（1-12）的 UInt8 数字。
---

# TO_MONTH

将日期或带时间的日期（timestamp/datetime）转换为包含月份编号（1-12）的 UInt8 数字。

## 语法 {#syntax}

```sql
TO_MONTH(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<expr>`  | 日期/时间戳 |

## 别名 {#aliases}

- [MONTH](/tidb-cloud-lake/sql/month.md)

## 返回类型 {#return-type}

 `TINYINT`

## 示例 {#examples}

```sql
SELECT NOW(), TO_MONTH(NOW()), MONTH(NOW());

┌─────────────────────────────────────────────────────────────┐
│            now()           │ to_month(now()) │ month(now()) │
├────────────────────────────┼─────────────────┼──────────────┤
│ 2024-03-14 23:34:02.161291 │               3 │            3 │
└─────────────────────────────────────────────────────────────┘
```