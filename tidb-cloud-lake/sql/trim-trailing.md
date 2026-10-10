---
title: TRIM_TRAILING
summary: 指定したトリム文字列を文字列の末尾からすべて削除します。
---

# TRIM_TRAILING

指定したトリム文字列を文字列の末尾からすべて削除します。

関連情報:

- [RTRIM](/tidb-cloud-lake/sql/rtrim.md)
- [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md)

## 構文 {#syntax}

```sql
TRIM_TRAILING(<string>, <trim_string>)
```

## 例 {#examples}

```sql
SELECT TRIM_TRAILING('datalakexx', 'xxx'), TRIM_TRAILING('datalakexx', 'xx'), TRIM_TRAILING('datalakexx', 'x');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_trailing('datalakexx', 'xxx') │ trim_trailing('datalakexx', 'xx') │ trim_trailing('datalakexx', 'x') │
├────────────────────────────────────┼───────────────────────────────────┼──────────────────────────────────┤
│ datalakexx                         │ datalake                          │ datalake                         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```