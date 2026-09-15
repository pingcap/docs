---
title: LTRIM
summary: 从字符串左侧移除指定 trim 字符串中出现的所有字符。
---

# LTRIM

从字符串左侧移除指定 trim 字符串中出现的所有字符。

另请参阅：

- [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md)
- [RTRIM](/tidb-cloud-lake/sql/rtrim.md)

## 语法 {#syntax}

```sql
LTRIM(<string>, <trim_string>)
```

## 示例 {#examples}

```sql
SELECT LTRIM('xxdatalake', 'xx'), LTRIM('xxdatalake', 'xy');

┌───────────────────────────────────────────────────────┐
│ ltrim('xxdatalake', 'xx') │ ltrim('xxdatalake', 'xy') │
├───────────────────────────┼───────────────────────────┤
│ datalake                  │ datalake                  │
└───────────────────────────────────────────────────────┘
```