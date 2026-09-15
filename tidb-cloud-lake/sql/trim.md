---
title: TRIM
summary: 从字符串的开头、结尾或两侧移除空格、特定字符或子字符串。
---

# TRIM

从字符串的开头、结尾或两侧移除空格、特定字符或子字符串。

另请参阅：[TRIM_BOTH](/tidb-cloud-lake/sql/trim-both.md)

## 语法 {#syntax}

```sql
-- Remove all occurrences of the specified trim string from the beginning, end, or both sides of the string
TRIM({ BOTH | LEADING | TRAILING } <trim_string> FROM <string>)

-- Remove all leading and trailing occurrences of any character present in the specified trim string
TRIM(<string>, <trim_string>)

-- Trim spaces from both sides
TRIM(<string>)
```

## 示例 {#examples}

以下示例从字符串 `'xxxdatalakexxx'` 的开头和结尾移除指定字符的所有出现：

```sql
SELECT TRIM(BOTH 'xxx' FROM 'xxxdatalakexxx'), TRIM(BOTH 'xx' FROM 'xxxdatalakexxx'), TRIM(BOTH 'x' FROM 'xxxdatalakexxx');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(BOTH 'xxx' FROM 'xxxdatalakexxx') │ TRIM(BOTH 'xx' FROM 'xxxdatalakexxx') │ TRIM(BOTH 'x' FROM 'xxxdatalakexxx') │
├────────────────────────────────────────┼───────────────────────────────────────┼──────────────────────────────────────┤
│ datalake                               │ xdatalakex                            │ datalake                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

以下示例从输入字符串 `'xxxdatalake'` 的开头移除指定字符的所有出现：

```sql
SELECT TRIM(LEADING 'xxx' FROM 'xxxdatalake'), TRIM(LEADING 'xx' FROM 'xxxdatalake'), TRIM(LEADING 'x' FROM 'xxxdatalake');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(LEADING 'xxx' FROM 'xxxdatalake') │ TRIM(LEADING 'xx' FROM 'xxxdatalake') │ TRIM(LEADING 'x' FROM 'xxxdatalake') │
├────────────────────────────────────────┼───────────────────────────────────────┼──────────────────────────────────────┤
│ datalake                               │ xdatalake                             │ datalake                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

以下示例从输入字符串 `'datalakexxx'` 的结尾移除指定字符的所有出现：

```sql
SELECT TRIM(TRAILING 'xxx' FROM 'datalakexxx' ), TRIM(TRAILING 'xx' FROM 'datalakexxx' ), TRIM(TRAILING 'x' FROM 'datalakexxx' );

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(TRAILING 'xxx' FROM 'datalakexxx') │ TRIM(TRAILING 'xx' FROM 'datalakexxx') │ TRIM(TRAILING 'x' FROM 'datalakexxx') │
├─────────────────────────────────────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│ datalake                                │ datalakex                              │ datalake                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

以下示例将 trim 字符串中的每个字符分别处理，并从输入字符串的开头和结尾移除所有匹配字符：

```sql
SELECT TRIM('xxxdatalakexxx', 'xyz'), TRIM('xxxdatalakexxx', 'xy'), TRIM('xxxdatalakexxx', 'x');

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim('xxxdatalakexxx', 'xyz') │ trim('xxxdatalakexxx', 'xy') │ trim('xxxdatalakexxx', 'x') │
├───────────────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ datalake                      │ datalake                     │ datalake                    │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

以下示例移除前导和/或尾随空格：

```sql
SELECT TRIM('   datalake   '), TRIM('   datalake'), TRIM('datalake   ');

┌────────────────────────────────────────────────────────────────────┐
│ TRIM('   datalake   ') │ TRIM('   datalake') │ TRIM('datalake   ') │
├────────────────────────┼─────────────────────┼─────────────────────┤
│ datalake               │ datalake            │ datalake            │
└────────────────────────────────────────────────────────────────────┘
```