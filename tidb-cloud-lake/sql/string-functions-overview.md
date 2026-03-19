---
title: String Functions
summary: This page provides a comprehensive overview of String functions in Databend, organized by functionality for easy reference.
---

# String Functions

This page provides a comprehensive overview of String functions in Databend, organized by functionality for easy reference.

## String Concatenation and Manipulation

| Function | Description | Example |
|----------|-------------|---------|
| [CONCAT](/tidb-cloud-lake/sql/concat.md) | Concatenates strings | `CONCAT('data', 'bend')` → `'databend'` |
| [CONCAT_WS](/tidb-cloud-lake/sql/concat-ws.md) | Concatenates strings with a separator | `CONCAT_WS('-', 'data', 'bend')` → `'data-bend'` |
| [INSERT](/tidb-cloud-lake/sql/insert.md) | Inserts a string at a specified position | `INSERT('databend', 5, 0, 'cloud')` → `'databcloudbend'` |
| [REPLACE](/tidb-cloud-lake/sql/replace.md) | Replaces occurrences of a substring | `REPLACE('databend', 'bend', 'cloud')` → `'datacloud'` |
| [TRANSLATE](/tidb-cloud-lake/sql/translate.md) | Replaces characters with their replacements | `TRANSLATE('databend', 'abn', '123')` → `'d1t12e3d'` |

## String Extraction

| Function                                        | Description                                                          | Example                                                                                |
|-------------------------------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| [LEFT](/tidb-cloud-lake/sql/left.md)                                 | Returns leftmost characters                                          | `LEFT('databend', 4)` → `'data'`                                                       |
| [RIGHT](/tidb-cloud-lake/sql/right.md)                               | Returns rightmost characters                                         | `RIGHT('databend', 4)` → `'bend'`                                                      |
| [SUBSTR](/tidb-cloud-lake/sql/substr.md) / [SUBSTRING](/tidb-cloud-lake/sql/substring.md) | Extracts a substring                                                 | `SUBSTR('databend', 5, 4)` → `'bend'`                                                  |
| [MID](/tidb-cloud-lake/sql/mid.md)                                   | Extracts a substring (alias for SUBSTRING)                           | `MID('databend', 5, 4)` → `'bend'`                                                     |
| [SPLIT](/tidb-cloud-lake/sql/split.md)                               | Splits a string into an array                                        | `SPLIT('data,bend', ',')` → `['data', 'bend']`                                         |
| [SPLIT_PART](/tidb-cloud-lake/sql/split-part.md)                     | Returns a specific part after splitting                              | `SPLIT_PART('data,bend', ',', 2)` → `'bend'`                                           |
| [REGEXP_SPLIT_TO_ARRAY](/tidb-cloud-lake/sql/regexp-split-array.md)  | Split a string into an array of segments using the specified pattern | `regexp_split_to_array('apple,banana,orange', ',');` → `'['apple','banana','orange']'` |
| [REGEXP_SPLIT_TO_TABLE](/tidb-cloud-lake/sql/regexp-split-table.md)  | Split a string into a table of segments using the specified pattern  | `regexp_split_to_table('data,bend', ',', 2)`                                           |

## String Padding and Formatting

| Function | Description | Example |
|----------|-------------|---------|
| [LPAD](/tidb-cloud-lake/sql/lpad.md) | Left-pads a string to a length | `LPAD('bend', 8, 'data')` → `'databend'` |
| [RPAD](/tidb-cloud-lake/sql/rpad.md) | Right-pads a string to a length | `RPAD('data', 8, 'bend')` → `'databend'` |
| [REPEAT](/tidb-cloud-lake/sql/repeat.md) | Repeats a string n times | `REPEAT('data', 2)` → `'datadata'` |
| [SPACE](/tidb-cloud-lake/sql/space.md) | Returns a string of spaces | `SPACE(4)` → `'    '` |
| [REVERSE](/tidb-cloud-lake/sql/reverse.md) | Reverses a string | `REVERSE('databend')` → `'dnebtad'` |

## String Trimming

| Function | Description | Example |
|----------|-------------|---------|
| [TRIM](/tidb-cloud-lake/sql/trim.md) | Removes leading and trailing spaces | `TRIM('  databend  ')` → `'databend'` |
| [TRIM_BOTH](/tidb-cloud-lake/sql/trim-both.md) | Removes specified chars from both ends | `TRIM_BOTH('xxdatabendxx', 'x')` → `'databend'` |
| [TRIM_LEADING](/tidb-cloud-lake/sql/trim-leading.md) | Removes specified chars from start | `TRIM_LEADING('xxdatabend', 'x')` → `'databend'` |
| [TRIM_TRAILING](/tidb-cloud-lake/sql/trim-trailing.md) | Removes specified chars from end | `TRIM_TRAILING('databendxx', 'x')` → `'databend'` |
| [LTRIM](/tidb-cloud-lake/sql/ltrim.md) | Removes leading spaces | `LTRIM('  databend')` → `'databend'` |
| [RTRIM](/tidb-cloud-lake/sql/rtrim.md) | Removes trailing spaces | `RTRIM('databend  ')` → `'databend'` |

## String Information

| Function | Description | Example |
|----------|-------------|---------|
| [LENGTH](/tidb-cloud-lake/sql/length.md) | Returns string length in characters | `LENGTH('databend')` → `8` |
| [CHAR_LENGTH](/tidb-cloud-lake/sql/char-length.md) / [CHARACTER_LENGTH](/tidb-cloud-lake/sql/character-length.md) | Returns string length in characters | `CHAR_LENGTH('databend')` → `8` |
| [BIT_LENGTH](/tidb-cloud-lake/sql/bit-length.md) | Returns string length in bits | `BIT_LENGTH('databend')` → `64` |
| [OCTET_LENGTH](/tidb-cloud-lake/sql/octet-length.md) | Returns string length in bytes | `OCTET_LENGTH('databend')` → `8` |
| [INSTR](/tidb-cloud-lake/sql/instr.md) | Returns position of first occurrence | `INSTR('databend', 'bend')` → `5` |
| [LOCATE](/tidb-cloud-lake/sql/locate.md) | Returns position of first occurrence | `LOCATE('bend', 'databend')` → `5` |
| [POSITION](/tidb-cloud-lake/sql/position.md) | Returns position of first occurrence | `POSITION('bend' IN 'databend')` → `5` |
| [STRCMP](/tidb-cloud-lake/sql/strcmp.md) | Compares two strings | `STRCMP('databend', 'datacloud')` → `-1` |
| [JARO_WINKLER](/tidb-cloud-lake/sql/jaro-winkler.md) | Returns similarity between strings | `JARO_WINKLER('databend', 'databand')` → `0.9619047619047619` |

## Case Conversion

| Function | Description | Example |
|----------|-------------|---------|
| [LOWER](/tidb-cloud-lake/sql/lower.md) / [LCASE](/tidb-cloud-lake/sql/lcase.md) | Converts to lowercase | `LOWER('DataBend')` → `'databend'` |
| [UPPER](/tidb-cloud-lake/sql/upper.md) / [UCASE](/tidb-cloud-lake/sql/ucase.md) | Converts to uppercase | `UPPER('databend')` → `'DATABEND'` |

## Pattern Matching

| Function | Description | Example |
|----------|-------------|---------|
| [LIKE](/tidb-cloud-lake/sql/like.md) | Pattern matching with wildcards | `'databend' LIKE 'data%'` → `true` |
| [NOT_LIKE](/tidb-cloud-lake/sql/not-like.md) | Negated LIKE | `'databend' NOT LIKE 'cloud%'` → `true` |
| [REGEXP](/tidb-cloud-lake/sql/regexp.md) / [RLIKE](/tidb-cloud-lake/sql/rlike.md) | Pattern matching with regex | `'databend' REGEXP '^data'` → `true` |
| [NOT_REGEXP](/tidb-cloud-lake/sql/not-regexp.md) / [NOT_RLIKE](/tidb-cloud-lake/sql/not-rlike.md) | Negated regex matching | `'databend' NOT REGEXP '^cloud'` → `true` |
| [REGEXP_LIKE](/tidb-cloud-lake/sql/regexp-like.md) | Returns boolean for regex match | `REGEXP_LIKE('databend', '^data')` → `true` |
| [REGEXP_INSTR](/tidb-cloud-lake/sql/regexp-instr.md) | Returns position of regex match | `REGEXP_INSTR('databend', 'bend')` → `5` |
| [REGEXP_SUBSTR](/tidb-cloud-lake/sql/regexp-substr.md) | Returns substring matching regex | `REGEXP_SUBSTR('databend', 'bend')` → `'bend'` |
| [REGEXP_REPLACE](/tidb-cloud-lake/sql/regexp-replace.md) | Replaces regex matches | `REGEXP_REPLACE('databend', 'bend', 'cloud')` → `'datacloud'` |
| [GLOB](/tidb-cloud-lake/sql/glob.md) | Unix-style pattern matching | `'databend' GLOB 'data*'` → `true` |

## Encoding and Decoding

| Function | Description | Example |
|----------|-------------|---------|
| [ASCII](/tidb-cloud-lake/sql/ascii.md) | Returns ASCII value of first character | `ASCII('D')` → `68` |
| [ORD](/tidb-cloud-lake/sql/ord.md) | Returns Unicode code point of first character | `ORD('D')` → `68` |
| [CHAR](/tidb-cloud-lake/sql/char.md) / [CHR](/tidb-cloud-lake/sql/char.md) | Returns string of characters for given Unicode code points | `CHAR(68,97,116,97)` → `'Data'` |
| [BIN](/tidb-cloud-lake/sql/bin.md) | Returns binary representation | `BIN(5)` → `'101'` |
| [OCT](/tidb-cloud-lake/sql/oct.md) | Returns octal representation | `OCT(8)` → `'10'` |
| [HEX](/tidb-cloud-lake/sql/hex.md) | Returns hexadecimal representation | `HEX('ABC')` → `'414243'` |
| [UNHEX](/tidb-cloud-lake/sql/unhex.md) | Converts hex to binary | `UNHEX('414243')` → `'ABC'` |
| [TO_BASE64](/tidb-cloud-lake/sql/to-base64.md) | Encodes to base64 | `TO_BASE64('databend')` → `'ZGF0YWJlbmQ='` |
| [FROM_BASE64](/tidb-cloud-lake/sql/from-base64.md) | Decodes from base64 | `FROM_BASE64('ZGF0YWJlbmQ=')` → `'databend'` |

## Miscellaneous

| Function | Description | Example |
|----------|-------------|---------|
| [QUOTE](/tidb-cloud-lake/sql/quote.md) | Escapes string for SQL | `QUOTE('databend')` → `'"databend"'` |
| [SOUNDEX](/tidb-cloud-lake/sql/soundex.md) | Returns soundex code | `SOUNDEX('databend')` → `'D315'` |
| [SOUNDSLIKE](/tidb-cloud-lake/sql/sounds-like.md) | Compares soundex values | `SOUNDSLIKE('databend', 'databand')` → `true` |
