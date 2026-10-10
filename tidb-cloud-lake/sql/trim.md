---
title: TRIM
summary: 文字列の先頭、末尾、または両側から、空白、特定の文字、または部分文字列を削除します。
---

# TRIM

文字列の先頭、末尾、または両側から、空白、特定の文字、または部分文字列を削除します。

関連情報: [TRIM_BOTH](/tidb-cloud-lake/sql/trim-both.md)

## 構文 {#syntax}

```sql
-- Remove all occurrences of the specified trim string from the beginning, end, or both sides of the string
TRIM({ BOTH | LEADING | TRAILING } <trim_string> FROM <string>)

-- Remove all leading and trailing occurrences of any character present in the specified trim string
TRIM(<string>, <trim_string>)

-- Trim spaces from both sides
TRIM(<string>)
```

## 例 {#examples}

この例では、文字列 `'xxxdatalakexxx'` の先頭と末尾の両方から、指定した文字のすべての出現を削除します。

```sql
SELECT TRIM(BOTH 'xxx' FROM 'xxxdatalakexxx'), TRIM(BOTH 'xx' FROM 'xxxdatalakexxx'), TRIM(BOTH 'x' FROM 'xxxdatalakexxx');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(BOTH 'xxx' FROM 'xxxdatalakexxx') │ TRIM(BOTH 'xx' FROM 'xxxdatalakexxx') │ TRIM(BOTH 'x' FROM 'xxxdatalakexxx') │
├────────────────────────────────────────┼───────────────────────────────────────┼──────────────────────────────────────┤
│ datalake                               │ xdatalakex                            │ datalake                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

この例では、入力文字列 `'xxxdatalake'` の先頭から、指定した文字のすべての出現を削除します。

```sql
SELECT TRIM(LEADING 'xxx' FROM 'xxxdatalake'), TRIM(LEADING 'xx' FROM 'xxxdatalake'), TRIM(LEADING 'x' FROM 'xxxdatalake');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(LEADING 'xxx' FROM 'xxxdatalake') │ TRIM(LEADING 'xx' FROM 'xxxdatalake') │ TRIM(LEADING 'x' FROM 'xxxdatalake') │
├────────────────────────────────────────┼───────────────────────────────────────┼──────────────────────────────────────┤
│ datalake                               │ xdatalake                             │ datalake                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

この例では、入力文字列 `'datalakexxx'` の末尾から、指定した文字のすべての出現を削除します。

```sql
SELECT TRIM(TRAILING 'xxx' FROM 'datalakexxx' ), TRIM(TRAILING 'xx' FROM 'datalakexxx' ), TRIM(TRAILING 'x' FROM 'datalakexxx' );

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(TRAILING 'xxx' FROM 'datalakexxx') │ TRIM(TRAILING 'xx' FROM 'datalakexxx') │ TRIM(TRAILING 'x' FROM 'datalakexxx') │
├─────────────────────────────────────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│ datalake                                │ datalakex                              │ datalake                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

この例では、trim string 内の各文字を個別に扱い、入力文字列の先頭と末尾の両方から一致する文字を削除します。

```sql
SELECT TRIM('xxxdatalakexxx', 'xyz'), TRIM('xxxdatalakexxx', 'xy'), TRIM('xxxdatalakexxx', 'x');

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim('xxxdatalakexxx', 'xyz') │ trim('xxxdatalakexxx', 'xy') │ trim('xxxdatalakexxx', 'x') │
├───────────────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ datalake                      │ datalake                     │ datalake                    │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

この例では、先頭および末尾の空白を削除します。

```sql
SELECT TRIM('   datalake   '), TRIM('   datalake'), TRIM('datalake   ');

┌────────────────────────────────────────────────────────────────────┐
│ TRIM('   datalake   ') │ TRIM('   datalake') │ TRIM('datalake   ') │
├────────────────────────┼─────────────────────┼─────────────────────┤
│ datalake               │ datalake            │ datalake            │
└────────────────────────────────────────────────────────────────────┘
```