---
title: REGEXP_SPLIT_TO_ARRAY
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.756"/>

Splits a string using a regular expression pattern and returns the segments as an array.

## Syntax

```sql
REGEXP_SPLIT_TO_ARRAY(string, pattern [, flags text])
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

### Basic Splitting
```sql
SELECT REGEXP_SPLIT_TO_ARRAY('apple,orange,banana', ',');
┌───────────────────────────────────────────┐
│ ["apple","orange","banana"]               │
└───────────────────────────────────────────┘
```

### Complex Delimiters
```sql
SELECT REGEXP_SPLIT_TO_ARRAY('2023-01-01T14:30:00', '[-T:]');
┌───────────────────────────────────────────────────────┐
│ ["2023","01","01","14","30","00"]                     │
└───────────────────────────────────────────────────────┘
```

### Handling Empty Elements
```sql
SELECT REGEXP_SPLIT_TO_ARRAY('a,,b,,,c', ',+');
┌───────────────────────────────────┐
│ ["a","b","c"]                     │
└───────────────────────────────────┘
```

### With flag text 

```sql
SELECT regexp_split_to_array('One_Two_Three', '[_-]', 'i')

╭─────────────────────────────────────────────────────╮
│ ['One','Two','Three']                               │
╰─────────────────────────────────────────────────────╯

```


## See Also

- [SPLIT](split.md): For simple string splitting
- [REGEXP_SPLIT_TO_TABLE](regexp-split-table.md): split string to table

