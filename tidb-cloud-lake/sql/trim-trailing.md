---
title: TRIM_TRAILING
summary: 从字符串末尾移除所有指定 trim 字符串的出现。
---

# TRIM_TRAILING

从字符串末尾移除所有指定 trim 字符串的出现。

另请参阅：

- [RTRIM](/tidb-cloud-lake/sql/rtrim.md)
- [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md)

## 语法 {#syntax}

```sql
TRIM_TRAILING(<string>, <trim_string>)
```

## 示例 {#examples}

```sql
SELECT TRIM_TRAILING('datalakexx', 'xxx'), TRIM_TRAILING('datalakexx', 'xx'), TRIM_TRAILING('datalakexx', 'x');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_trailing('datalakexx', 'xxx') │ trim_trailing('datalakexx', 'xx') │ trim_trailing('datalakexx', 'x') │
├────────────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ datalakexx                         │ datalake                          │ datalake                         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```