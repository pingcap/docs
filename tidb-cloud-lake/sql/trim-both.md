---
title: TRIM_BOTH
summary: 从字符串的开头、结尾或两端移除所有指定 trim 字符串的出现。
---

# TRIM_BOTH

从字符串的开头、结尾或两端移除所有指定 trim 字符串的出现。

另请参阅：[TRIM](/tidb-cloud-lake/sql/trim.md)

## 语法 {#syntax}

```sql
TRIM_BOTH(<string>, <trim_string>)
```

## 示例 {#examples}

```sql
SELECT TRIM_BOTH('xxdatalakexx', 'xxx'), TRIM_BOTH('xxdatalakexx', 'xx'), TRIM_BOTH('xxdatalakexx', 'x');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_both('xxdatalakexx', 'xxx') │ trim_both('xxdatalakexx', 'xx') │ trim_both('xxdatalakexx', 'x') │
├──────────────────────────────────┼─────────────────────────────────┼────────────────────────────────┤
│ xxdatalakexx                     │ datalake                        │ datalake                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```