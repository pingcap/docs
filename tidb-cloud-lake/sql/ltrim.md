---
title: LTRIM
summary: 指定されたトリム文字列に含まれる任意の文字を、文字列の左側からすべて削除します。
---

# LTRIM

指定されたトリム文字列に含まれる任意の文字を、文字列の左側からすべて削除します。

関連情報:

- [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md)
- [RTRIM](/tidb-cloud-lake/sql/rtrim.md)

## 構文 {#syntax}

```sql
LTRIM(<string>, <trim_string>)
```

## 例 {#examples}

```sql
SELECT LTRIM('xxdatalake', 'xx'), LTRIM('xxdatalake', 'xy');

┌───────────────────────────────────────────────────────┐
│ ltrim('xxdatalake', 'xx') │ ltrim('xxdatalake', 'xy') │
├───────────────────────────┼───────────────────────────┤
│ datalake                  │ datalake                  │
└───────────────────────────────────────────────────────┘
```