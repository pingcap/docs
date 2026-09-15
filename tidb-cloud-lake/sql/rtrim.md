---
title: RTRIM
summary: 从字符串右侧移除指定 trim 字符串中出现的所有字符。
---

# RTRIM

从字符串右侧移除指定 trim 字符串中出现的所有字符。

另请参阅：

- [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md)
- [LTRIM](/tidb-cloud-lake/sql/ltrim.md)

## 语法 {#syntax}

```sql
RTRIM(<string>, <trim_string>)
```

## 示例 {#examples}

```sql
SELECT RTRIM('datalakexx', 'x'), RTRIM('datalakexx', 'xy');

┌──────────────────────────────────────────────────────┐
│ rtrim('datalakexx', 'x') │ rtrim('datalakexx', 'xy') │
├──────────────────────────┼───────────────────────────┤
│ datalake                 │ datalake                  │
└──────────────────────────────────────────────────────┘
```