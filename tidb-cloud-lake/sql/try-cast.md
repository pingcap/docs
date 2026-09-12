---
title: TRY_CAST
summary: 将一个值从一种数据类型转换为另一种数据类型。出错时返回 NULL。
---

# TRY_CAST

将一个值从一种数据类型转换为另一种数据类型。出错时返回 NULL。

另请参阅：[CAST](/tidb-cloud-lake/sql/cast.md)

## 语法 {#syntax}

```sql
TRY_CAST( <expr> AS <data_type> )
```

## 示例 {#examples}

```sql
SELECT TRY_CAST(1 AS VARCHAR);

┌───────────────────────┐
│ try_cast(1 as string) │
├───────────────────────┤
│ 1                     │
└───────────────────────┘
```