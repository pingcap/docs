---
title: TRIM_BOTH
summary: 指定したトリム文字列のすべての出現を、文字列の先頭、末尾、または両端から削除します。
---

# TRIM_BOTH

指定したトリム文字列のすべての出現を、文字列の先頭、末尾、または両端から削除します。

関連項目: [TRIM](/tidb-cloud-lake/sql/trim.md)

## 構文 {#syntax}

```sql
TRIM_BOTH(<string>, <trim_string>)
```

## 例 {#examples}

```sql
SELECT TRIM_BOTH('xxdatalakexx', 'xxx'), TRIM_BOTH('xxdatalakexx', 'xx'), TRIM_BOTH('xxdatalakexx', 'x');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_both('xxdatalakexx', 'xxx') │ trim_both('xxdatalakexx', 'xx') │ trim_both('xxdatalakexx', 'x') │
├──────────────────────────────────┼─────────────────────────────────┼────────────────────────────────┤
│ xxdatalakexx                     │ datalake                        │ datalake                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```