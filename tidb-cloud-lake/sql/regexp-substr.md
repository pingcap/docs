---
title: REGEXP_SUBSTR
---

Returns the substring of the string `expr` that matches the regular expression specified by the pattern `pat`, NULL if there is no match. If expr or pat is NULL, the return value is NULL.

-  REGEXP_SUBSTR does not support extracting capture groups (subpatterns defined by parentheses `()`). It returns the entire matched substring instead of specific captured groups.

```sql
SELECT REGEXP_SUBSTR('abc123', '(\w+)(\d+)');
-- Returns 'abc123' (the entire match), not 'abc' or '123'.

-- Alternative Solution: Use string functions like SUBSTRING and REGEXP_INSTR to manually extract the desired portion of the string:
SELECT SUBSTRING('abc123', 1, REGEXP_INSTR('abc123', '\d+') - 1);
-- Returns 'abc' (extracts the part before the digits).
SELECT SUBSTRING('abc123', REGEXP_INSTR('abc123', '\d+'));
-- Returns '123' (extracts the digits).
```

- REGEXP_SUBSTR does not support the `e` parameter (used in Snowflake to extract capture groups) or the `group_num` parameter for specifying which capture group to return.

```sql
SELECT REGEXP_SUBSTR('abc123', '(\w+)(\d+)', 1, 1, 'e', 1);
-- Error: Databend does not support the 'e' parameter or capture group extraction.

-- Alternative Solution: Use string functions like SUBSTRING and LOCATE to manually extract the desired substring, or preprocess the data with external tools (e.g., Python) to extract capture groups before querying.
SELECT SUBSTRING(
    REGEXP_SUBSTR('letters:abc,numbers:123', 'letters:[a-z]+,numbers:[0-9]+'),
    LOCATE('letters:', 'letters:abc,numbers:123') + 8,
    LOCATE(',', 'letters:abc,numbers:123') - (LOCATE('letters:', 'letters:abc,numbers:123') + 8)
);
-- Returns 'abc'
```

## Syntax

```sql
REGEXP_SUBSTR(<expr>, <pat[, pos[, occurrence[, match_type]]]>)
```

## Arguments

| Arguments  | Description                                                                                               |
|------------|-----------------------------------------------------------------------------------------------------------|
| expr       | The string expr that to be matched                                                                        |
| pat        | The regular expression                                                                                    |
| pos        | Optional. The position in expr at which to start the search. If omitted, the default is 1.                |
| occurrence | Optional. Which occurrence of a match to search for. If omitted, the default is 1.                        |
| match_type | Optional. A string that specifies how to perform matching. The meaning is as described for REGEXP_LIKE(). |

## Return Type

`VARCHAR`

## Examples

```sql
SELECT REGEXP_SUBSTR('abc def ghi', '[a-z]+');
+----------------------------------------+
| REGEXP_SUBSTR('abc def ghi', '[a-z]+') |
+----------------------------------------+
| abc                                    |
+----------------------------------------+

SELECT REGEXP_SUBSTR('abc def ghi', '[a-z]+', 1, 3);
+----------------------------------------------+
| REGEXP_SUBSTR('abc def ghi', '[a-z]+', 1, 3) |
+----------------------------------------------+
| ghi                                          |
+----------------------------------------------+

SELECT REGEXP_SUBSTR('周 周周 周周周 周周周周', '周+', 2, 3);
+------------------------------------------------------------------+
| REGEXP_SUBSTR('周 周周 周周周 周周周周', '周+', 2, 3)            |
+------------------------------------------------------------------+
| 周周周周                                                         |
+------------------------------------------------------------------+

```
