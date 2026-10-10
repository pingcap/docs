---
title: TRIM_LEADING
summary: 指定したトリム文字列のすべての出現を文字列の先頭から削除します。
---

# TRIM_LEADING

指定したトリム文字列のすべての出現を文字列の先頭から削除します。

関連情報:

- [LTRIM](/tidb-cloud-lake/sql/ltrim.md)
- [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md)

## 構文 {#syntax}

```sql
TRIM_LEADING(<string>, <trim_string>)
```

## 例 {#examples}

```sql
SELECT TRIM_LEADING('xxdatalake', 'xxx'), TRIM_LEADING('xxdatalake', 'xx'), TRIM_LEADING('xxdatalake', 'x');

┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim_leading('xxdatalake', 'xxx') │ trim_leading('xxdatalake', 'xx') │ trim_leading('xxdatalake', 'x') │
├───────────────────────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ xxdatalake                        │ datalake                         │ datalake                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```