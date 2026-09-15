---
title: DIVNULL
summary: 将第一个数字除以第二个数字并返回商。如果第二个数字为 0 或 NULL，则返回 NULL。
---

# DIVNULL

将第一个数字除以第二个数字并返回商。如果第二个数字为 0 或 NULL，则返回 NULL。

另请参阅：

- [DIV](/tidb-cloud-lake/sql/div.md)
- [DIV0](/tidb-cloud-lake/sql/div0.md)

## 语法 {#syntax}

```sql
DIVNULL(<number1>, <number2>)
```

## 示例 {#examples}

```sql
SELECT
  DIVNULL(20, 6),
  DIVNULL(20, 0),
  DIVNULL(20, NULL);

┌─────────────────────────────────────────────────────────┐
│   divnull(20, 6)   │ divnull(20, 0) │ divnull(20, null) │
├────────────────────┼────────────────┼───────────────────┤
│ 3.3333333333333335 │ NULL           │ NULL              │
└─────────────────────────────────────────────────────────┘
```