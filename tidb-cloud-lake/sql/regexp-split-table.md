---
title: REGEXP_SPLIT_TO_TABLE
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.754"/>

Splits a string using a regular expression pattern and returns each segment as a table.

## Syntax

```sql
REGEXP_SPLIT_TO_TABLE(string, pattern [, flags text])
```

| Parameter    | Description                                                    |
|--------------|----------------------------------------------------------------|
| `string`     | The input string to split (VARCHAR type)                       |
| `pattern`    | Regular expression pattern used for splitting (VARCHAR type)   |
| `flags text` | A string of flags to modify the regular expression's behavior. |


**Supported `flags` Parameter:**
Provides flexible regular expression configuration options, controlling matching behavior by combining the following characters:
*   `i` (case-insensitive): Pattern matching ignores case.
*   `c` (case-sensitive): Pattern matching is case-sensitive (default behavior).
*   `n` or `m` (multi-line): Enables multi-line mode. In this mode, `^` and `$` match the beginning and end of the string, respectively, as well as the beginning and end of each line; the dot `.` does not match newline characters.
*   `s` (single-line): Enables single-line mode (also known as dot-matches-newline). In this mode, the dot `.` matches any character, including newline characters.
*   `x` (ignore-whitespace): Ignores whitespace characters in the pattern (improves pattern readability).
*   `q` (literal): Treats the `pattern` as a literal string rather than a regular expression.

## Examples

### Basic Row Generation
```sql
SELECT REGEXP_SPLIT_TO_TABLE('one,two,three', ',');
┌─────────┐
│ one     │
│ two     │
│ three   │
└─────────┘
```

### Log Parsing
```sql
SELECT REGEXP_SPLIT_TO_TABLE('ERR:404:File Not Found', ':');
┌──────────────────┐
│ ERR              │
│ 404              │
│ File Not Found   │
└──────────────────┘
```

### With flag text

```sql
SELECT regexp_split_to_table('One_Two_Three', '[_-]', 'i')

╭────────╮
│ One    │
│ Two    │
│ Three  │
╰────────╯

```

### Nested Usage

```sql
WITH data AS (
  SELECT 'id=123,name=John' AS kv_pairs
)
SELECT 
  REGEXP_SPLIT_TO_TABLE(kv_pairs, ',') AS pair
FROM data;
┌──────────────┐
│ id=123       │
│ name=John    │
└──────────────┘
```

## See Also

- [SPLIT](split.md): For simple string splitting
- [REGEXP_SPLIT_TO_ARRAY](regexp-split-array.md): split string to array
