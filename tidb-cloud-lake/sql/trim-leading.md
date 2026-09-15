---
title: TRIM_LEADING
summary: 从字符串开头移除所有指定的修剪字符串。
---

# TRIM_LEADING

从字符串开头移除所有指定的修剪字符串。

另请参阅：

- [LTRIM](/tidb-cloud-lake/sql/ltrim.md)
- [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md)

## 语法 {#syntax}

```sql
TRIM_LEADING(<string>, <trim_string>)
```

## 示例 {#examples}

```sql
SELECT TRIM_LEADING('xxdatalake', 'xxx'), TRIM_LEADING('xxdatalake', 'xx'), TRIM_LEADING('xxdatalake', 'x');

┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_leading('xxdatalake', 'xxx') │ trim_leading('xxdatalake', 'xx') │ trim_leading('xxdatalake', 'x') │
├───────────────────────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ xxdatalake                        │ datalake                         │ datalake                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```