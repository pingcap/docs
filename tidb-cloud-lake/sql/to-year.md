---
title: TO_YEAR
summary: 将日期或带时间的日期（timestamp/datetime）转换为包含年份（公元）的 UInt16 数字。
---

# TO_YEAR

将日期或带时间的日期（timestamp/datetime）转换为包含年份（公元）的 UInt16 数字。

## 语法 {#syntax}

```sql
TO_YEAR(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<expr>`  | 日期/时间戳 |

## 别名 {#aliases}

- [YEAR](/tidb-cloud-lake/sql/year.md)

## 返回类型 {#return-type}

 `SMALLINT`

## 示例 {#examples}

```sql
SELECT NOW(), TO_YEAR(NOW()), YEAR(NOW());

┌───────────────────────────────────────────────────────────┐
│            now()           │ to_year(now()) │ year(now()) │
├────────────────────────────┼────────────────┼─────────────┤
│ 2024-03-14 23:37:03.895166 │           2024 │        2024 │
└───────────────────────────────────────────────────────────┘
```