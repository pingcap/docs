---
title: REGEXP_SUBSTR
summary: 返回字符串 `expr` 中与模式 `pat` 指定的正则表达式匹配的子字符串；如果没有匹配项，则返回 NULL。如果 expr 或 pat 为 NULL，则返回值为 NULL。
---

# REGEXP_SUBSTR

返回字符串 `expr` 中与模式 `pat` 指定的正则表达式匹配的子字符串；如果没有匹配项，则返回 NULL。如果 expr 或 pat 为 NULL，则返回值为 NULL。

- REGEXP_SUBSTR 不支持提取捕获组（由括号 `()` 定义的子模式）。它返回整个匹配到的子字符串，而不是特定的捕获组。

```sql
SELECT REGEXP_SUBSTR('abc123', '(\w+)(\d+)');
-- Returns 'abc123' (the entire match), not 'abc' or '123'.

-- Alternative Solution: Use string functions like SUBSTRING and REGEXP_INSTR to manually extract the desired portion of the string:
SELECT SUBSTRING('abc123', 1, REGEXP_INSTR('abc123', '\d+') - 1);
-- Returns 'abc' (extracts the part before the digits).
SELECT SUBSTRING('abc123', REGEXP_INSTR('abc123', '\d+'));
-- Returns '123' (extracts the digits).
```

- REGEXP_SUBSTR 不支持 `e` 参数（在 Snowflake 中用于提取捕获组），也不支持用于指定返回哪个捕获组的 `group_num` 参数。

```sql
SELECT REGEXP_SUBSTR('abc123', '(\w+)(\d+)', 1, 1, 'e', 1);
-- Error: {{{ .lake }}} does not support the 'e' parameter or capture group extraction.

-- Alternative Solution: Use string functions like SUBSTRING and LOCATE to manually extract the desired substring, or preprocess the data with external tools (e.g., Python) to extract capture groups before querying.
SELECT SUBSTRING(
    REGEXP_SUBSTR('letters:abc,numbers:123', 'letters:[a-z]+,numbers:[0-9]+'),
    LOCATE('letters:', 'letters:abc,numbers:123') + 8,
    LOCATE(',', 'letters:abc,numbers:123') - (LOCATE('letters:', 'letters:abc,numbers:123') + 8)
);
-- Returns 'abc'
```

## 语法 {#syntax}

```sql
REGEXP_SUBSTR(<expr>, <pat[, pos[, occurrence[, match_type]]]>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|------------|-----------------------------------------------------------------------------------------------------------|
| expr       | 要匹配的字符串 expr                                                                        |
| pat        | 正则表达式                                                                                    |
| pos        | 可选。在 expr 中开始搜索的位置。如果省略，默认值为 1。                |
| occurrence | 可选。要搜索匹配项的第几次出现。如果省略，默认值为 1。                        |
| match_type | 可选。一个字符串，用于指定如何执行匹配。其含义与 REGEXP_LIKE() 中的说明相同。 |

## 返回类型 {#return-type}

`VARCHAR`

## 示例 {#examples}

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