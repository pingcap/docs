---
title: RTRIM
summary: 指定したトリム文字列に含まれる任意の文字を、文字列の右側からすべて削除します。
---

# RTRIM

指定したトリム文字列に含まれる任意の文字を、文字列の右側からすべて削除します。

関連情報:

- [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md)
- [LTRIM](/tidb-cloud-lake/sql/ltrim.md)

## 構文 {#syntax}

```sql
RTRIM(<string>, <trim_string>)
```

## 例 {#examples}

```sql
SELECT RTRIM('datalakexx', 'x'), RTRIM('datalakexx', 'xy');

┌──────────────────────────────────────────────────────┐
│ rtrim('datalakexx', 'x') │ rtrim('datalakexx', 'xy') │
├──────────────────────────┼───────────────────────────┤
│ datalake                 │ datalake                  │
└──────────────────────────────────────────────────────┘
```