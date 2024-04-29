---
title: String Functions
summary: Learn about the string functions in TiDB.
---

# String Functions

TiDB supports most of the [string functions](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html) available in MySQL 5.7, some of the [string functions](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html) available in MySQL 8.0, and some of the [functions](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009) available in Oracle 21.

<CustomContent platform="tidb">

For comparisons between functions and syntax of Oracle and TiDB, see [Comparisons between Functions and Syntax of Oracle and TiDB](/oracle-functions-to-tidb.md).

</CustomContent>

## Supported functions

| Name                                                                                                                                          | Description                                                                                                                               |
|:----------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| [`ASCII()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ascii)                                                     | Return numeric value of left-most character                                                                                               |
| [`BIN()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bin)                                                         | Return a string containing binary representation of a number                                                                              |
| [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bit-length)                                           | Return length of argument in bits                                                                                                         |
| [`CHAR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char)                                                       | Return the character for each integer passed                                                                                              |
| [`CHAR_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char-length)                                         | Return number of characters in argument                                                                                                   |
| [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_character-length)                               | Synonym for `CHAR_LENGTH()`                                                                                                               |
| [`CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat)                                                   | Return concatenated string                                                                                                                |
| [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat-ws)                                             | Return concatenate with separator                                                                                                         |
| [`ELT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_elt)                                                         | Return string at index number                                                                                                             |
| [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set)                                           | Return a string such that for every bit set in the value bits, you get an on string and for every unset bit, you get an off string        |
| [`FIELD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_field)                                                     | Return the index (position) of the first argument in the subsequent arguments                                                             |
| [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_find-in-set)                                         | Return the index position of the first argument within the second argument                                                                |
| [`FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_format)                                                   | Return a number formatted to specified number of decimal places                                                                           |
| [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_from-base64)                                         | Decode to a base-64 string and return result                                                                                              |
| [`HEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_hex)                                                         | Return a hexadecimal representation of a decimal or string value                                                                          |
| [`INSERT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_insert)                                                   | Insert a substring at the specified position up to the specified number of characters                                                     |
| [`INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_instr)                                                     | Return the index of the first occurrence of substring                                                                                     |
| [`LCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lcase)                                                     | Synonym for `LOWER()`                                                                                                                     |
| [`LEFT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_left)                                                       | Return the leftmost number of characters as specified                                                                                     |
| [`LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_length)                                                   | Return the length of a string in bytes                                                                                                    |
| [`LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like)                                              | Simple pattern matching                                                                                                                   |
| [`LOCATE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_locate)                                                   | Return the position of the first occurrence of substring                                                                                  |
| [`LOWER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lower)                                                     | Return the argument in lowercase                                                                                                          |
| [`LPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lpad)                                                       | Return the string argument, left-padded with the specified string                                                                         |
| [`LTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ltrim)                                                     | Remove leading spaces                                                                                                                     |
| [`MAKE_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_make-set)                                               | Return a set of comma-separated strings that have the corresponding bit in bits set                                                       |
| [`MID()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_mid)                                                         | Return a substring starting from the specified position                                                                                   |
| [`NOT LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)                                      | Negation of simple pattern matching                                                                                                       |
| [`NOT REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp)                                                       | Negation of `REGEXP`                                                                                                                      |
| [`OCT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct)                                                         | Return a string containing octal representation of a number                                                                               |
| [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_octet-length)                                       | Synonym for `LENGTH()`                                                                                                                    |
| [`ORD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord)                                                         | Return character code for leftmost character of the argument                                                                              |
| [`POSITION()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_position)                                               | Synonym for `LOCATE()`                                                                                                                    |
| [`QUOTE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote)                                                     | Escape the argument for use in an SQL statement                                                                                           |
| [`REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)                                                               | Pattern matching using regular expressions                                                                                                |
| [`REGEXP_INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-instr) | Return the starting index of the substring that matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)) |
| [`REGEXP_LIKE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-like) | Whether the string matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)) |
| [`REGEXP_REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-replace) | Replace substrings that match the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)) |
| [`REGEXP_SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-substr) | Return the substring that matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)) |
| [`REPEAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_repeat)                                                   | Repeat a string the specified number of times                                                                                             |
| [`REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_replace)                                                 | Replace occurrences of a specified string                                                                                                 |
| [`REVERSE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse)                                                 | Reverse the characters in a string                                                                                                        |
| [`RIGHT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right)                                                     | Return the specified rightmost number of characters                                                                                       |
| [`RLIKE`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)                                                                | Synonym for `REGEXP`                                                                                                                      |
| [`RPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rpad)                                                       | Append string the specified number of times                                                                                               |
| [`RTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rtrim)                                                     | Remove trailing spaces                                                                                                                    |
| [`SPACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_space)                                                     | Return a string of the specified number of spaces                                                                                         |
| [`STRCMP()`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp)                                        | Compare two strings                                                                                                                       |
| [`SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substr)                                                   | Return the substring as specified                                                                                                         |
| [`SUBSTRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring)                                             | Return the substring as specified                                                                                                         |
| [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring-index)                                 | Return a substring from a string before the specified number of occurrences of the delimiter                                              |
| [`TO_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_to-base64)                                             | Return the argument converted to a base-64 string                                                                                         |
| [`TRANSLATE()`](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRANSLATE.html#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690) | Replace all occurrences of characters by other characters in a string. It does not treat empty strings as `NULL` as Oracle does.              |
| [`TRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_trim)                                                       | Remove leading and trailing spaces                                                                                                        |
| [`UCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ucase)                                                     | Synonym for `UPPER()`                                                                                                                     |
| [`UNHEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_unhex)                                                     | Return a string containing hex representation of a number                                                                                 |
| [`UPPER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_upper)                                                     | Convert to uppercase                                                                                                                      |
| [`WEIGHT_STRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_weight-string) | Return the weight string for the input string |

## Unsupported functions

* `LOAD_FILE()`
* `MATCH()`
* `SOUNDEX()`

## Regular expression compatibility with MySQL

The following sections describe the regular expression compatibility with MySQL.

### Syntax compatibility

MySQL implements regular expression using International Components for Unicode (ICU), and TiDB uses RE2. To learn the syntax differences between the two libraries, you can refer to the [ICU documentation](https://unicode-org.github.io/icu/userguide/) and [RE2 Syntax](https://github.com/google/re2/wiki/Syntax).

### `match_type` compatibility

The value options of `match_type` between TiDB and MySQL are:

- Value options in TiDB are `"c"`, `"i"`, `"m"`, and `"s"`, and value options in MySQL are `"c"`, `"i"`, `"m"`, `"n"`, and `"u"`.
- The `"s"` in TiDB corresponds to `"n"` in MySQL. When `"s"` is set in TiDB, the `.` character also matches line terminators (`\n`).

    For example, the `SELECT REGEXP_LIKE(a, b, "n") FROM t1` in MySQL is the same as the `SELECT REGEXP_LIKE(a, b, "s") FROM t1` in TiDB.

- TiDB does not support `"u"`, which means Unix-only line endings in MySQL.

### Data type compatibility

The difference between TiDB and MySQL support for the binary string type:

- MySQL does not support binary strings in regular expression functions since 8.0.22. For more details, refer to [MySQL documentation](https://dev.mysql.com/doc/refman/8.0/en/regexp.html). But in practice, regular functions can work in MySQL when all parameters or return types are binary strings. Otherwise, an error will be reported.
- Currently, TiDB prohibits using binary strings and an error will be reported under any circumstances.

### Other compatibility

- The behavior of replacing empty strings in TiDB is different from MySQL. Taking `REGEXP_REPLACE("", "^$", "123")` as an example:

    - MySQL does not replace the empty string and returns `""` as the result.
    - TiDB replaces the empty string and returns `"123"` as the result.

- The keyword used for capturing groups in TiDB is different from MySQL. MySQL uses `$` as the keyword, while TiDB uses `\\` as the keyword. In addition, TiDB only supports capturing groups numbered from `0` to `9`.

    For example, the following SQL statement returns `ab` in TiDB:

    ```sql
    SELECT REGEXP_REPLACE('abcd','(.*)(.{2})$','\\1') AS s;
    ```
