---
title: String Functions
---

This page provides a comprehensive overview of String functions in Databend, organized by functionality for easy reference.

## String Concatenation and Manipulation

| Function | Description | Example |
|----------|-------------|---------|
| [CONCAT](concat.md) | Concatenates strings | `CONCAT('data', 'bend')` → `'databend'` |
| [CONCAT_WS](concat-ws.md) | Concatenates strings with a separator | `CONCAT_WS('-', 'data', 'bend')` → `'data-bend'` |
| [INSERT](insert.md) | Inserts a string at a specified position | `INSERT('databend', 5, 0, 'cloud')` → `'databcloudbend'` |
| [REPLACE](replace.md) | Replaces occurrences of a substring | `REPLACE('databend', 'bend', 'cloud')` → `'datacloud'` |
| [TRANSLATE](translate.md) | Replaces characters with their replacements | `TRANSLATE('databend', 'abn', '123')` → `'d1t12e3d'` |

## String Extraction

| Function                                        | Description                                                          | Example                                                                                |
|-------------------------------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [LEFT](left.md)                                 | Returns leftmost characters                                          | `LEFT('databend', 4)` → `'data'`                                                       |
| [RIGHT](right.md)                               | Returns rightmost characters                                         | `RIGHT('databend', 4)` → `'bend'`                                                      |
| [SUBSTR](substr.md) / [SUBSTRING](substring.md) | Extracts a substring                                                 | `SUBSTR('databend', 5, 4)` → `'bend'`                                                  |
| [MID](mid.md)                                   | Extracts a substring (alias for SUBSTRING)                           | `MID('databend', 5, 4)` → `'bend'`                                                     |
| [SPLIT](split.md)                               | Splits a string into an array                                        | `SPLIT('data,bend', ',')` → `['data', 'bend']`                                         |
| [SPLIT_PART](split-part.md)                     | Returns a specific part after splitting                              | `SPLIT_PART('data,bend', ',', 2)` → `'bend'`                                           |
| [REGEXP_SPLIT_TO_ARRAY](regexp-split-array.md)  | Split a string into an array of segments using the specified pattern | `regexp_split_to_array('apple,banana,orange', ',');` → `'['apple','banana','orange']'` |
| [REGEXP_SPLIT_TO_TABLE](regexp-split-table.md)  | Split a string into a table of segments using the specified pattern  | `regexp_split_to_table('data,bend', ',', 2)`                                           |

## String Padding and Formatting

| Function | Description | Example |
|----------|-------------|---------|
| [LPAD](lpad.md) | Left-pads a string to a length | `LPAD('bend', 8, 'data')` → `'databend'` |
| [RPAD](rpad.md) | Right-pads a string to a length | `RPAD('data', 8, 'bend')` → `'databend'` |
| [REPEAT](repeat.md) | Repeats a string n times | `REPEAT('data', 2)` → `'datadata'` |
| [SPACE](space.md) | Returns a string of spaces | `SPACE(4)` → `'    '` |
| [REVERSE](reverse.md) | Reverses a string | `REVERSE('databend')` → `'dnebtad'` |

## String Trimming

| Function | Description | Example |
|----------|-------------|---------|
| [TRIM](trim.md) | Removes leading and trailing spaces | `TRIM('  databend  ')` → `'databend'` |
| [TRIM_BOTH](trim-both.md) | Removes specified chars from both ends | `TRIM_BOTH('xxdatabendxx', 'x')` → `'databend'` |
| [TRIM_LEADING](trim-leading.md) | Removes specified chars from start | `TRIM_LEADING('xxdatabend', 'x')` → `'databend'` |
| [TRIM_TRAILING](trim-trailing.md) | Removes specified chars from end | `TRIM_TRAILING('databendxx', 'x')` → `'databend'` |
| [LTRIM](ltrim.md) | Removes leading spaces | `LTRIM('  databend')` → `'databend'` |
| [RTRIM](rtrim.md) | Removes trailing spaces | `RTRIM('databend  ')` → `'databend'` |

## String Information

| Function | Description | Example |
|----------|-------------|---------|
| [LENGTH](length.md) | Returns string length in characters | `LENGTH('databend')` → `8` |
| [CHAR_LENGTH](char-length.md) / [CHARACTER_LENGTH](character-length.md) | Returns string length in characters | `CHAR_LENGTH('databend')` → `8` |
| [BIT_LENGTH](bit-length.md) | Returns string length in bits | `BIT_LENGTH('databend')` → `64` |
| [OCTET_LENGTH](octet-length.md) | Returns string length in bytes | `OCTET_LENGTH('databend')` → `8` |
| [INSTR](instr.md) | Returns position of first occurrence | `INSTR('databend', 'bend')` → `5` |
| [LOCATE](locate.md) | Returns position of first occurrence | `LOCATE('bend', 'databend')` → `5` |
| [POSITION](position.md) | Returns position of first occurrence | `POSITION('bend' IN 'databend')` → `5` |
| [STRCMP](strcmp.md) | Compares two strings | `STRCMP('databend', 'datacloud')` → `-1` |
| [JARO_WINKLER](jaro-winkler.md) | Returns similarity between strings | `JARO_WINKLER('databend', 'databand')` → `0.9619047619047619` |

## Case Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [LOWER](lower.md) / [LCASE](lcase.md) | Converts to lowercase | `LOWER('DataBend')` → `'databend'` |
| [UPPER](upper.md) / [UCASE](ucase.md) | Converts to uppercase | `UPPER('databend')` → `'DATABEND'` |

## Pattern Matching

| Function | Description | Example |
|----------|-------------|---------|
| [LIKE](like.md) | Pattern matching with wildcards | `'databend' LIKE 'data%'` → `true` |
| [NOT_LIKE](not-like.md) | Negated LIKE | `'databend' NOT LIKE 'cloud%'` → `true` |
| [REGEXP](regexp.md) / [RLIKE](rlike.md) | Pattern matching with regex | `'databend' REGEXP '^data'` → `true` |
| [NOT_REGEXP](not-regexp.md) / [NOT_RLIKE](not-rlike.md) | Negated regex matching | `'databend' NOT REGEXP '^cloud'` → `true` |
| [REGEXP_LIKE](regexp-like.md) | Returns boolean for regex match | `REGEXP_LIKE('databend', '^data')` → `true` |
| [REGEXP_INSTR](regexp-instr.md) | Returns position of regex match | `REGEXP_INSTR('databend', 'bend')` → `5` |
| [REGEXP_SUBSTR](regexp-substr.md) | Returns substring matching regex | `REGEXP_SUBSTR('databend', 'bend')` → `'bend'` |
| [REGEXP_REPLACE](regexp-replace.md) | Replaces regex matches | `REGEXP_REPLACE('databend', 'bend', 'cloud')` → `'datacloud'` |
| [GLOB](glob.md) | Unix-style pattern matching | `'databend' GLOB 'data*'` → `true` |

## Encoding and Decoding

| Function | Description | Example |
|----------|-------------|---------|
| [ASCII](ascii.md) | Returns ASCII value of first character | `ASCII('D')` → `68` |
| [ORD](ord.md) | Returns Unicode code point of first character | `ORD('D')` → `68` |
| [CHAR](char.md) / [CHR](char.md) | Returns string of characters for given Unicode code points | `CHAR(68,97,116,97)` → `'Data'` |
| [BIN](bin.md) | Returns binary representation | `BIN(5)` → `'101'` |
| [OCT](oct.md) | Returns octal representation | `OCT(8)` → `'10'` |
| [HEX](hex.md) | Returns hexadecimal representation | `HEX('ABC')` → `'414243'` |
| [UNHEX](unhex.md) | Converts hex to binary | `UNHEX('414243')` → `'ABC'` |
| [TO_BASE64](to-base64.md) | Encodes to base64 | `TO_BASE64('databend')` → `'ZGF0YWJlbmQ='` |
| [FROM_BASE64](from-base64.md) | Decodes from base64 | `FROM_BASE64('ZGF0YWJlbmQ=')` → `'databend'` |

## Miscellaneous

| Function | Description | Example |
|----------|-------------|---------|
| [QUOTE](quote.md) | Escapes string for SQL | `QUOTE('databend')` → `'"databend"'` |
| [SOUNDEX](soundex.md) | Returns soundex code | `SOUNDEX('databend')` → `'D315'` |
| [SOUNDSLIKE](soundslike.md) | Compares soundex values | `SOUNDSLIKE('databend', 'databand')` → `true` |
