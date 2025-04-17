---
title: String Functions
summary: Learn about the string functions in TiDB.
---

# String Functions

TiDB supports most of the [string functions](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html) available in MySQL 8.0, and some of the [functions](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009) available in Oracle 21.

<CustomContent platform="tidb">

For comparisons between functions and syntax of Oracle and TiDB, see [Comparisons between Functions and Syntax of Oracle and TiDB](/oracle-functions-to-tidb.md).

</CustomContent>

## Supported functions

### [`ASCII()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ascii)

The `ASCII(str)` function is used to get the ASCII value of the leftmost character in the given argument. The argument can be either a string or a number.

- If the argument is not empty, the function returns the ASCII value of the leftmost character.
- If the argument is an empty string, the function returns `0`.
- If the argument is `NULL`, the function returns `NULL`.

> **Note:**
>
> `ASCII(str)` only works for characters represented using 8 bits of binary digits (one byte).

Example:

```sql
SELECT ASCII('A'), ASCII('TiDB'), ASCII(23);
```

Output:

```sql
+------------+---------------+-----------+
| ASCII('A') | ASCII('TiDB') | ASCII(23) |
+------------+---------------+-----------+
|         65 |            84 |        50 |
+------------+---------------+-----------+
```

### [`BIN()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bin)

The `BIN()` function is used to convert the given argument into a string representation of its binary value. The argument can be either a string or a number.

- If the argument is a positive number, the function returns a string representation of its binary value.
- If the argument is a negative number, the function converts the absolute value of the argument to its binary representation, inverts each bit of the binary value (changing `0` to `1` and `1` to `0`), and then adds `1` to the inverted value.
- If the argument is a string containing only digits, the function returns the result according to those digits. For example, the results for `"123"` and `123` are the same.
- If the argument is a string and its first character is not a digit (such as `"q123"`), the function returns `0`.
- If the argument is a string that consists of digits and non-digits, the function returns the result according to the consecutive digits at the beginning of the argument. For example, the results for `"123q123"` and `123` are the same, but `BIN('123q123')` generates a warning like `Truncated incorrect INTEGER value: '123q123'`.
- If the argument is `NULL`, the function returns `NULL`.

Example 1:

```sql
SELECT BIN(123), BIN('123q123');
```

Output 1:

```sql
+----------+----------------+
| BIN(123) | BIN('123q123') |
+----------+----------------+
| 1111011  | 1111011        |
+----------+----------------+
```

Example 2:

```sql
SELECT BIN(-7);
```

Output 2:

```sql
+------------------------------------------------------------------+
| BIN(-7)                                                          |
+------------------------------------------------------------------+
| 1111111111111111111111111111111111111111111111111111111111111001 |
+------------------------------------------------------------------+
```

### [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bit-length)

The `BIT_LENGTH()` function is used to return the length of a given argument in bits.

Examples:

```sql
SELECT BIT_LENGTH("TiDB");

+--------------------+
| BIT_LENGTH("TiDB") |
+--------------------+
|                 32 |
+--------------------+
```

8 bits per character x 4 characters = 32 bits

```sql
SELECT BIT_LENGTH("PingCAP 123");

+---------------------------+
| BIT_LENGTH("PingCAP 123") |
+---------------------------+
|                        88 |
+---------------------------+
```

8 bits per character (space is counted because it is a non-alphanumeric character) x 11 characters = 88 bits

```sql
SELECT CustomerName, BIT_LENGTH(CustomerName) AS BitLengthOfName FROM Customers;

+--------------------+-----------------+
| CustomerName       | BitLengthOfName |
+--------------------+-----------------+
| Albert Einstein    |             120 |
| Robert Oppenheimer |             144 |
+--------------------+-----------------+
```

> **Note:**
>
> The preceding example operates under the assumption that there is a database with a table named `Customers` and a column inside the table named `CustomerName`.

### [`CHAR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char)

The `CHAR()` function is used to get the corresponding character of a specific ASCII value. It performs the opposite operation of `ASCII()`, which returns the ASCII value of a specific character. If multiple arguments are supplied, the function works on all arguments and are then concatenated together.

Examples:

```sql
SELECT CHAR(65);

+------------+
|  CHAR(65)  |
+------------+
|          A |
+------------+
```

```sql
SELECT CHAR(84);

+------------+
|  CHAR(84)  |
+------------+
|          T |
+------------+
```

The `CHAR()` function can also be used to get the corresponding character of ASCII values that extend beyond the standard ASCII range (`0` - `127`).

```sql
/*For extended ASCII: */

SELECT CHAR(128);

+------------+
|  CHAR(128) |
+------------+
|       0x80 |
+------------+
```

The `CHAR()` function can also get the corresponding character value of a unicode value.

```sql
/* For Unicode: */

--skip-binary-as-hex

SELECT CHAR(50089);

+--------------+
|  CHAR(50089) |
+--------------+
|            é |
+--------------+
```

```sql
SELECT CHAR(65,66,67);
```

```
+----------------+
| CHAR(65,66,67) |
+----------------+
| ABC            |
+----------------+
1 row in set (0.00 sec)
```

### [`CHAR_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char-length)

The `CHAR_LENGTH()` function is used to get the total number of characters in a given argument as an integer.

Examples:

```sql
SELECT CHAR_LENGTH("TiDB") AS LengthOfString;

+----------------+
| LengthOfString |
+----------------+
|              4 |
+----------------+
```

```sql
SELECT CustomerName, CHAR_LENGTH(CustomerName) AS LengthOfName FROM Customers;

+--------------------+--------------+
| CustomerName       | LengthOfName |
+--------------------+--------------+
| Albert Einstein    |           15 |
| Robert Oppenheimer |           18 |
+--------------------+--------------+
```

> **Note:**
>
> The preceding example operates under the assumption that there is a database with a table named `Customers` and a column inside the table named `CustomerName`.

### [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_character-length)

The `CHARACTER_LENGTH()` function is the same as the `CHAR_LENGTH()` function. Both functions can be used synonymously because they generate the same output.

### [`CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat)

The `CONCAT()` function concatenates one or more arguments into a single string.

Syntax:

```sql
CONCAT(str1,str2,...)
```

`str1, str2, ...` is a list of arguments to be concatenated. Each argument can be a string or a number.

Example:

```sql
SELECT CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE);
```

Output:

```sql
+---------------------------------------------+
| CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE) |
+---------------------------------------------+
| TiDB Server-11                              |
+---------------------------------------------+
```

If any of the arguments is `NULL`, `CONCAT()` returns `NULL`.

Example:

```sql
SELECT CONCAT('TiDB', NULL, 'Server');
```

Output:

```sql
+--------------------------------+
| CONCAT('TiDB', NULL, 'Server') |
+--------------------------------+
| NULL                           |
+--------------------------------+
```

In addition to the `CONCAT()` function, you can concatenate strings by placing them adjacent to each other as in the following example. Note that this method does not support numeric types.

```sql
SELECT 'Ti' 'DB' ' ' 'Server';
```

Output:

```sql
+-------------+
| Ti          |
+-------------+
| TiDB Server |
+-------------+
```

### [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat-ws)

The `CONCAT_WS()` function is a form of [`CONCAT()`](#concat) with a separator, which returns a string concatenated by the specified separator.

Syntax:

```sql
CONCAT_WS(separator,str1,str2,...)
```

- `separator`: the first argument is the separator, which concatenates the remaining arguments that are not `NULL`.
- `str1, str2, ...`: a list of arguments to be concatenated. Each argument can be a string or a number.

Example:

```sql
SELECT CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD');
```

Output:

```sql
+---------------------------------------------+
| CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD') |
+---------------------------------------------+
| TiDB Server,TiKV,PD                         |
+---------------------------------------------+
```

- If the separator is an empty string, `CONCAT_WS()` is equivalent to `CONCAT()` and returns the concatenated string of the remaining arguments.

    Example:

    ```sql
    SELECT CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD');
    ```

    Output:

    ```sql
    +--------------------------------------------+
    | CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD') |
    +--------------------------------------------+
    | TiDB ServerTiKVPD                          |
    +--------------------------------------------+
    ```

- If the separator is `NULL`, `CONCAT_WS()` returns `NULL`.

    Example:

    ```sql
    SELECT CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD');
    ```

    Output:

    ```sql
    +----------------------------------------------+
    | CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD') |
    +----------------------------------------------+
    | NULL                                         |
    +----------------------------------------------+
    ```

- If only one of the arguments to be concatenated is not `NULL`, `CONCAT_WS()` returns that argument.

    Example:

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL);
    ```

    Output:

    ```sql
    +-------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL) |
    +-------------------------------------+
    | TiDB Server                         |
    +-------------------------------------+
    ```

- If there are `NULL` arguments to be concatenated, `CONCAT_WS()` skips these `NULL` arguments.

    Example:

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL, 'PD');
    ```

    Output:

    ```sql
    +-------------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL, 'PD') |
    +-------------------------------------------+
    | TiDB Server,PD                            |
    +-------------------------------------------+
    ```

- If there are empty strings to be concatenated, `CONCAT_WS()` does not skip empty strings.

    Example:

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', '', 'PD');
    ```

    Output:

    ```sql
    +-----------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', '', 'PD') |
    +-----------------------------------------+
    | TiDB Server,,PD                         |
    +-----------------------------------------+
    ```

### [`ELT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_elt)

The `ELT()` function returns the element at the index number.

```sql
SELECT ELT(3, 'This', 'is', 'TiDB');
```

```sql
+------------------------------+
| ELT(3, 'This', 'is', 'TiDB') |
+------------------------------+
| TiDB                         |
+------------------------------+
1 row in set (0.00 sec)
```

The preceding example returns the third element, which is `'TiDB'`.

### [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set)

The `EXPORT_SET()` function returns a string that consists of a specified number (`number_of_bits`) of `on`/`off` values, optionally separated by `separator`. These values are based on whether the corresponding bit in the `bits` argument is `1`, where the first value corresponds to the rightmost (lowest) bit of `bits`.

Syntax:

```sql
EXPORT_SET(bits, on, off, [separator[, number_of_bits]])
```

- `bits`: an integer representing the bit value.
- `on`: the string to be returned if the corresponding bit is `1`.
- `off`: the string to be returned if the corresponding bit is `0`.
- `separator` (optional): the separator character in the result string.
- `number_of_bits` (optional): the number of bits to be processed. If it is not set, `64` (the max size of bits) is used by default, which means that `bits` is treated as an unsigned 64-bit integer.

Examples:

In the following example, `number_of_bits` is set to `5`, resulting in 5 values, separated by `|`. Because only 3 bits are given, the other bits are considered unset. Therefore, setting `number_of_bits` to either `101` or `00101` results in the same output.

```sql
SELECT EXPORT_SET(b'101',"ON",'off','|',5);
```

```sql
+-------------------------------------+
| EXPORT_SET(b'101',"ON",'off','|',5) |
+-------------------------------------+
| ON|off|ON|off|off                   |
+-------------------------------------+
1 row in set (0.00 sec)
```

In the following example, `bits` is set to `00001111`, `on` is set to `x`, and `off` is set to `_`. This causes the function to return `____` for the `0` bits and `xxxx` for the `1` bits. Therefore, when processing with the bits in `00001111` from right to left, the function returns `xxxx____`.

```sql
SELECT EXPORT_SET(b'00001111', 'x', '_', '', 8);
```

```sql
+------------------------------------------+
| EXPORT_SET(b'00001111', 'x', '_', '', 8) |
+------------------------------------------+
| xxxx____                                 |
+------------------------------------------+
1 row in set (0.00 sec)
```

In the following example, `bits` is set to `00001111`, `on` is set to `x`, and `off` is set to `_`. This causes the function to return `x` for each `1` bit and `_` for each `0` bit. Therefore, when processing with the bits in `01010101` from right to left, the function returns `x_x_x_x_`.

```sql
SELECT EXPORT_SET(b'01010101', 'x', '_', '', 8);
```

```sql
+------------------------------------------+
| EXPORT_SET(b'01010101', 'x', '_', '', 8) |
+------------------------------------------+
| x_x_x_x_                                 |
+------------------------------------------+
1 row in set (0.00 sec)
```

### [`FIELD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_field)

Return the index (position) of the first argument in the subsequent arguments.

In the following example, the first argument of `FIELD()` is `needle`, and it matches the second argument in the following list, so the function returns `2`.

```sql
SELECT FIELD('needle', 'A', 'needle', 'in', 'a', 'haystack');
+-------------------------------------------------------+
| FIELD('needle', 'A', 'needle', 'in', 'a', 'haystack') |
+-------------------------------------------------------+
|                                                     2 |
+-------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_find-in-set)

Return the index position of the first argument within the second argument.

This function is often used with the [`SET`](/data-type-string.md#set-type) data type.

In the following example, `Go` is the fourth element in the set `COBOL,BASIC,Rust,Go,Java,Fortran`, so the function returns `4`.

```sql
SELECT FIND_IN_SET('Go', 'COBOL,BASIC,Rust,Go,Java,Fortran');
+-------------------------------------------------------+
| FIND_IN_SET('Go', 'COBOL,BASIC,Rust,Go,Java,Fortran') |
+-------------------------------------------------------+
|                                                     4 |
+-------------------------------------------------------+
1 row in set (0.00 sec)
```

### [`FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_format)

The `FORMAT(X,D[,locale])` function is used to format the number `X` to a format similar to `"#,###,###. ##"`, rounded to `D` decimal places, and return the result as a string.

Arguments:

- `X`: the number to be formatted. It can be a direct numeric value, a numeric string, or a number in scientific notation.
- `D`: the number of decimal places for the returned value. The function rounds the number `X` to `D` decimal places. If `D` is greater than the actual number of decimal places in `X`, the result is padded with zeros to the corresponding length.
- `[locale]`: specifies a locale setting to be used for grouping between decimal points, thousands separators, and separators for resultant numbers. A valid locale value is the same as the valid value of the [`lc_time_names`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_lc_time_names) system variable. If not specified or the region setting is `NULL`, the `'en_US'` region setting is used by default. This argument is optional.

Behaviors:

- If the first argument is a string and contains only numbers, the function returns a result based on that numeric value. For example, `FORMAT('12.34', 1)` and `FORMAT(12.34, 1)` return the same result.
- If the first argument is a number represented in scientific notation (using `E/e`), the function returns the result based on that number. For example, `FORMAT('1E2', 3)` returns `100.000`.
- If the first argument is a string starting with non-numeric characters, the function returns zero and a warning `(Code 1292)`. For example, `FORMAT('q12.36', 5)` returns `0.00000`, but also includes a warning `Warning (Code 1292): Truncated incorrect DOUBLE value: 'q12.36'`.
- If the first argument is a string mixing numbers and non-numbers, the function returns a result based on the consecutive numeric part at the beginning of the argument, and also includes a warning `(Code 1292)`. For example, `FORMAT('12.36q56.78', 1)` returns the same numeric result as `FORMAT('12.36', 1)`, but includes a warning `Warning (Code 1292): Truncated incorrect DOUBLE value: '12.36q56.78'`.
- If the second argument is zero or a negative number, the function truncates the decimal part and returns an integer.
- If any of the arguments is `NULL`, the function returns `NULL`.

Examples:

The following examples show how to format the number 12.36 to different decimal places:

```sql
mysql> SELECT FORMAT(12.36, 1);
+------------------+
| FORMAT(12.36, 1) |
+------------------+
| 12.4             |
+------------------+
```

```sql
mysql> SELECT FORMAT(12.36, 5);
+------------------+
| FORMAT(12.36, 5) |
+------------------+
| 12.36000         |
+------------------+
```

```sql
mysql> SELECT FORMAT(12.36, 2);
+------------------+
| FORMAT(12.36, 2) |
+------------------+
| 12.36            |
+------------------+
```

### [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_from-base64)

The `FROM_BASE64()` function is used to decode a [Base64](https://datatracker.ietf.org/doc/html/rfc4648) encoded string and return the decoded result in its hexadecimal form.

- This function accepts a single argument, that is, the Base64 encoded string to be decoded.
- If the argument is `NULL` or not a valid Base64 encoded string, the `FROM_BASE64()` function returns `NULL`.

Examples:

The following example shows how to decode the Base64 encoded string `'SGVsbG8gVGlEQg=='`. This string is the result of encoding `'Hello TiDB'`, using the [`TO_BASE64()`](#to_base64) function.

```sql
mysql> SELECT TO_BASE64('Hello TiDB');
+-------------------------+
| TO_BASE64('Hello TiDB') |
+-------------------------+
| SGVsbG8gVGlEQg==        |
+-------------------------+

mysql> SELECT FROM_BASE64('SGVsbG8gVGlEQg==');
+------------------------------------------------------------------+
| FROM_BASE64('SGVsbG8gVGlEQg==')                                  |
+------------------------------------------------------------------+
| 0x48656C6C6F2054694442                                           |
+------------------------------------------------------------------+
```

```sql
mysql> SELECT CONVERT(FROM_BASE64('SGVsbG8gVGlEQg==') USING utf8mb4);
+--------------------------------------------------------+
| CONVERT(FROM_BASE64('SGVsbG8gVGlEQg==') USING utf8mb4) |
+--------------------------------------------------------+
| Hello TiDB                                             |
+--------------------------------------------------------+
```

The following example shows how to decode the Base64 encoded number `MTIzNDU2`. This string is the result of encoding `123456`, which can be done using the [`TO_BASE64()`](#to_base64) function.

```sql
mysql> SELECT FROM_BASE64('MTIzNDU2');
+--------------------------------------------------+
| FROM_BASE64('MTIzNDU2')                          |
+--------------------------------------------------+
| 0x313233343536                                   |
+--------------------------------------------------+
```

### [`HEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_hex)

The `HEX()` function is used to convert the given argument into a string representation of its hexadecimal value. The argument can be either a string or a number.

- If the argument is a string, `HEX(str)` returns a hexadecimal string representation of `str`. The function converts each byte of each character in `str` into two hexadecimal digits. For example, the character `a` in a UTF-8 or ASCII character set is represented as a binary value of `00111101`, or `61` in hexadecimal notation.
- If the argument is a number, `HEX(n)` returns a hexadecimal string representation of `n`. The function treats the argument `n` as a `BIGINT` number, equivalent to using `CONV(n, 10, 16)`.
- If the argument is `NULL`, the function returns `NULL`.

> **Note:**
>
> In the MySQL client, the [`--binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) option is enabled by default in interactive mode, causing the client to display data with an unknown character set as a [hexadecimal literal](https://dev.mysql.com/doc/refman/8.0/en/hexadecimal-literals.html). You can use the `--skip-binary-as-hex` option to disable this behavior.

Examples (with `mysql --skip-binary-as-hex`):

```sql
SELECT X'616263', HEX('abc'), UNHEX(HEX('abc')), 0x616263;
+-----------+------------+-------------------+----------+
| X'616263' | HEX('abc') | UNHEX(HEX('abc')) | 0x616263 |
+-----------+------------+-------------------+----------+
| abc       | 616263     | abc               | abc      |
+-----------+------------+-------------------+----------+
```

```sql
SELECT X'F09F8DA3', HEX('🍣'), UNHEX(HEX('🍣')), 0xF09F8DA3;
+-------------+-------------+--------------------+------------+
| X'F09F8DA3' | HEX('🍣')     | UNHEX(HEX('🍣'))     | 0xF09F8DA3 |
+-------------+-------------+--------------------+------------+
| 🍣            | F09F8DA3    | 🍣                   | 🍣           |
+-------------+-------------+--------------------+------------+
```

```sql
SELECT HEX(255), CONV(HEX(255), 16, 10);
+----------+------------------------+
| HEX(255) | CONV(HEX(255), 16, 10) |
+----------+------------------------+
| FF       | 255                    |
+----------+------------------------+
```

```sql
SELECT HEX(NULL);
+-----------+
| HEX(NULL) |
+-----------+
| NULL      |
+-----------+
```

### [`INSERT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_insert)

The `INSERT(str, pos, len, newstr)` function is used to replace a substring in `str` (that starts at position `pos` and is `len` characters long) with the string `newstr`. This function is multibyte safe.

- If `pos` exceeds the length of `str`, the function returns the original string `str` without modification.
- If `len` exceeds the remaining length of `str` from position `pos`, the function replaces the rest of the string from position `pos`.
- If any argument is `NULL`, the function returns `NULL`.

Examples:

```sql
SELECT INSERT('He likes tennis', 4, 5, 'plays');
+------------------------------------------+
| INSERT('He likes tennis', 4, 5, 'plays') |
+------------------------------------------+
| He plays tennis                          |
+------------------------------------------+
```

```sql
SELECT INSERT('He likes tennis', -1, 5, 'plays');
+-------------------------------------------+
| INSERT('He likes tennis', -1, 5, 'plays') |
+-------------------------------------------+
| He likes tennis                           |
+-------------------------------------------+
```

```sql
SELECT INSERT('He likes tennis', 4, 100, 'plays');
+--------------------------------------------+
| INSERT('He likes tennis', 4, 100, 'plays') |
+--------------------------------------------+
| He plays                                   |
+--------------------------------------------+
```

```sql
SELECT INSERT('He likes tenis', 10, 100, '🍣');
+-------------------------------------------+
| INSERT('He likes tenis', 10, 100, '🍣')     |
+-------------------------------------------+
| He likes 🍣                                 |
+-------------------------------------------+
```

```sql
SELECT INSERT('あああああああ', 2, 3, 'いいい');
+----------------------------------------------------+
| INSERT('あああああああ', 2, 3, 'いいい')           |
+----------------------------------------------------+
| あいいいあああ                                     |
+----------------------------------------------------+
```

```sql
SELECT INSERT('あああああああ', 2, 3, 'xx');
+---------------------------------------------+
| INSERT('あああああああ', 2, 3, 'xx')        |
+---------------------------------------------+
| あxxあああ                                  |
+---------------------------------------------+
```

### [`INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_instr)

The `INSTR(str, substr)` function is used to get the position of the first occurrence of `substr` in `str`. Each argument can be either a string or a number. This function is the same as the two-argument version of [`LOCATE(substr, str)`](#locate), but with the order of the arguments reversed.

> **Note:**
>
> The case sensitivity of `INSTR(str, substr)` is determined by the [collations](/character-set-and-collation.md) used in TiDB. Binary collations (with the suffix `_bin`) are case-sensitive, while general collations (with the suffix `_general_ci` or `_ai_ci`, and) are case-insensitive.

- If either argument is a number, the function treats the number as a string.
- If `substr` is not in `str`, the function returns `0`. Otherwise, it returns the position of the first occurrence of `substr` in `str`.
- If either argument is `NULL`, the function returns `NULL`.

Examples:

```sql
SELECT INSTR("pingcap.com", "tidb");

+------------------------------+
| INSTR("pingcap.com", "tidb") |
+------------------------------+
|                            0 |
+------------------------------+
```

```sql
SELECT INSTR("pingcap.com/tidb", "tidb");

+-----------------------------------+
| INSTR("pingcap.com/tidb", "tidb") |
+-----------------------------------+
|                                13 |
+-----------------------------------+
```

```sql
SELECT INSTR("pingcap.com/tidb" COLLATE utf8mb4_bin, "TiDB");

+-------------------------------------------------------+
| INSTR("pingcap.com/tidb" COLLATE utf8mb4_bin, "TiDB") |
+-------------------------------------------------------+
|                                                     0 |
+-------------------------------------------------------+
```

```sql
SELECT INSTR("pingcap.com/tidb" COLLATE utf8mb4_general_ci, "TiDB");

+--------------------------------------------------------------+
| INSTR("pingcap.com/tidb" COLLATE utf8mb4_general_ci, "TiDB") |
+--------------------------------------------------------------+
|                                                           13 |
+--------------------------------------------------------------+
```

```sql
SELECT INSTR(0123, "12");

+-------------------+
| INSTR(0123, "12") |
+-------------------+
|                 1 |
+-------------------+
```

### [`LCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lcase)

The `LCASE(str)` function is a synonym for [`LOWER(str)`](#lower), which returns the lowercase of the given argument.

### [`LEFT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_left)

The `LEFT()` function returns a specified number of characters from the left side of a string.

Syntax:

```sql
LEFT(`str`, `len`)
```

- `str`: the original string to extract characters. If `str` contains a multibyte character, the function counts it as a single code point.
- `len`: the length of characters to be returned.
    - If `len` is equal to or less than 0, the function returns an empty string.
    - If `len` is equal to or greater than the length of `str`, the function returns the original `str`.
- If any argument is `NULL`, the function returns `NULL`.

Examples:

```sql
SELECT LEFT('ABCED', 3);
+------------------+
| LEFT('ABCED', 3) |
+------------------+
| ABC              |
+------------------+

SELECT LEFT('ABCED', 6);
+------------------+
| LEFT('ABCED', 6) |
+------------------+
| ABCED            |
+------------------+
```

```sql
SELECT LEFT('ABCED', 0);
+------------------+
| LEFT('ABCED', 0) |
+------------------+
|                  |
+------------------+

SELECT LEFT('ABCED', -1);
+-------------------+
| LEFT('ABCED', -1) |
+-------------------+
|                   |
+-------------------+
```

```sql
SELECT LEFT('🍣ABC', 3);
+--------------------+
| LEFT('🍣ABC', 3)     |
+--------------------+
| 🍣AB                 |
+--------------------+
```

```sql
SELECT LEFT('ABC', NULL);
+-------------------+
| LEFT('ABC', NULL) |
+-------------------+
| NULL              |
+-------------------+

SELECT LEFT(NULL, 3);
+------------------------------+
| LEFT(NULL, 3)                |
+------------------------------+
| NULL                         |
+------------------------------+
```

### [`LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_length)

The `LENGTH()` function returns the length of a string in bytes.

`LENGTH()` counts a multibyte character as multiple bytes while `CHAR_LENGTH()` counts a multibyte character as a single code point.

If the argument is `NULL`, the function returns `NULL`.

Examples:

```sql
SELECT LENGTH('ABC');
+---------------+
| LENGTH('ABC') |
+---------------+
|             3 |
+---------------+

SELECT LENGTH('🍣ABC');
+-------------------+
| LENGTH('🍣ABC')     |
+-------------------+
|                 7 |
+-------------------+

SELECT CHAR_LENGTH('🍣ABC');
+------------------------+
| CHAR_LENGTH('🍣ABC')     |
+------------------------+
|                      4 |
+------------------------+
```

```sql
SELECT LENGTH(NULL);
+--------------+
| LENGTH(NULL) |
+--------------+
|         NULL |
+--------------+
```

### [`LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like)

The `LIKE` operator is used for simple string matching. The expression `expr LIKE pat [ESCAPE 'escape_char']` returns `1` (`TRUE`) or `0` (`FALSE`). If either `expr` or `pat` is `NULL`, the result is `NULL`.

You can use the following two wildcard parameters with `LIKE`:

- `%` matches any number of characters, including zero characters.
- `_` matches exactly one character.

The following examples use the `utf8mb4_bin` collation:

```sql
SET collation_connection='utf8mb4_bin';
SHOW VARIABLES LIKE 'collation_connection';
+----------------------+-------------+
| Variable_name        | Value       |
+----------------------+-------------+
| collation_connection | utf8mb4_bin |
+----------------------+-------------+
```

```sql
SELECT NULL LIKE '%' as result;
+--------+
| result |
+--------+
|   NULL |
+--------+
```

```sql
SELECT 'sushi!!!' LIKE 'sushi_' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

```sql
SELECT '🍣🍺sushi🍣🍺' LIKE '%sushi%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

```sql
SELECT '🍣🍺sushi🍣🍺' LIKE '%SUSHI%' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

```sql
SELECT '🍣🍺sushi🍣🍺' LIKE '%🍣%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

The default escape character is `\`:

```sql
SELECT 'sushi!!!' LIKE 'sushi\_' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

```sql
SELECT 'sushi_' LIKE 'sushi\_' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

To specify a different escape character, such as `*`, you can use the `ESCAPE` clause:

```sql
SELECT 'sushi_' LIKE 'sushi*_' ESCAPE '*' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

```sql
SELECT 'sushi!' LIKE 'sushi*_' ESCAPE '*' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

You can use the `LIKE` operator to match a numeric value:

```sql
SELECT 10 LIKE '1%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

```sql
SELECT 10000 LIKE '12%' AS result;
+--------+
| result |
+--------+
|      0 |
+--------+
```

To specify a collation explicitly, such as `utf8mb4_unicode_ci`, you can use `COLLATE`:

```sql
SELECT '🍣🍺Sushi🍣🍺' COLLATE utf8mb4_unicode_ci LIKE '%SUSHI%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

### [`LOCATE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_locate)

The `LOCATE(substr, str[, pos])` function is used to get the position of the first occurrence of a specified substring `substr` in a string `str`. The `pos` argument is optional and specifies the starting position for the search.

- If the substring `substr` is not present in `str`, the function returns `0`.
- If any argument is `NULL`, the function returns `NULL`.
- This function is multibyte safe and performs a case-sensitive search only if at least one argument is a binary string.

The following examples use the `utf8mb4_bin` collation:

```sql
SET collation_connection='utf8mb4_bin';
SHOW VARIABLES LIKE 'collation_connection';
+----------------------+-------------+
| Variable_name        | Value       |
+----------------------+-------------+
| collation_connection | utf8mb4_bin |
+----------------------+-------------+
```

```sql
SELECT LOCATE('bar', 'foobarbar');
+----------------------------+
| LOCATE('bar', 'foobarbar') |
+----------------------------+
|                          4 |
+----------------------------+
```

```sql
SELECT LOCATE('baz', 'foobarbar');
+----------------------------+
| LOCATE('baz', 'foobarbar') |
+----------------------------+
|                          0 |
+----------------------------+
```

```sql
SELECT LOCATE('bar', 'fooBARBAR');
+----------------------------+
| LOCATE('bar', 'fooBARBAR') |
+----------------------------+
|                          0 |
+----------------------------+
```

```sql
SELECT LOCATE('bar', 'foobarBAR', 100);
+---------------------------------+
| LOCATE('bar', 'foobarBAR', 100) |
+---------------------------------+
|                               0 |
+---------------------------------+
```

```sql
SELECT LOCATE('bar', 'foobarbar', 5);
+-------------------------------+
| LOCATE('bar', 'foobarbar', 5) |
+-------------------------------+
|                             7 |
+-------------------------------+
```

```sql
SELECT LOCATE('bar', NULL);
+---------------------+
| LOCATE('bar', NULL) |
+---------------------+
|                NULL |
+---------------------+
```

```sql
SELECT LOCATE('い', 'たいでぃーびー');
+----------------------------------------+
| LOCATE('い', 'たいでぃーびー')         |
+----------------------------------------+
|                                      2 |
+----------------------------------------+
```

```sql
SELECT LOCATE('い', 'たいでぃーびー', 3);
+-------------------------------------------+
| LOCATE('い', 'たいでぃーびー', 3)         |
+-------------------------------------------+
|                                         0 |
+-------------------------------------------+
```

The following examples use the `utf8mb4_unicode_ci` collation:

```sql
SET collation_connection='utf8mb4_unicode_ci';
SHOW VARIABLES LIKE 'collation_connection';
+----------------------+--------------------+
| Variable_name        | Value              |
+----------------------+--------------------+
| collation_connection | utf8mb4_unicode_ci |
+----------------------+--------------------+
```

```sql
SELECT LOCATE('い', 'たいでぃーびー', 3);
+-------------------------------------------+
| LOCATE('い', 'たいでぃーびー', 3)         |
+-------------------------------------------+
|                                         4 |
+-------------------------------------------+
```

```sql
SELECT LOCATE('🍺', '🍣🍣🍣🍺🍺');
+----------------------------------------+
| LOCATE('🍺', '🍣🍣🍣🍺🍺')            |
+----------------------------------------+
|                                      1 |
+----------------------------------------+
```

The following multibyte and binary string examples use the `utf8mb4_bin` collation:

```sql
SET collation_connection='utf8mb4_bin';
SHOW VARIABLES LIKE 'collation_connection';
+----------------------+-------------+
| Variable_name        | Value       |
+----------------------+-------------+
| collation_connection | utf8mb4_bin |
+----------------------+-------------+
```

```sql
SELECT LOCATE('🍺', '🍣🍣🍣🍺🍺');
+----------------------------------------+
| LOCATE('🍺', '🍣🍣🍣🍺🍺')                         |
+----------------------------------------+
|                                      4 |
+----------------------------------------+
```

```sql
SELECT LOCATE('b', _binary'aBcde');
+-----------------------------+
| LOCATE('b', _binary'aBcde') |
+-----------------------------+
|                           0 |
+-----------------------------+
```

```sql
SELECT LOCATE('B', _binary'aBcde');
+-----------------------------+
| LOCATE('B', _binary'aBcde') |
+-----------------------------+
|                           2 |
+-----------------------------+
```

```sql
SELECT LOCATE(_binary'b', 'aBcde');
+-----------------------------+
| LOCATE(_binary'b', 'aBcde') |
+-----------------------------+
|                           0 |
+-----------------------------+
```

```sql
SELECT LOCATE(_binary'B', 'aBcde');
+-----------------------------+
| LOCATE(_binary'B', 'aBcde') |
+-----------------------------+
|                           2 |
+-----------------------------+
```

### [`LOWER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lower)

The `LOWER(str)` function is used to convert all characters in the given argument `str` to lowercase. The argument can be either a string or a number.

- If the argument is a string, the function returns the string in lowercase.
- If the argument is a number, the function returns the number without leading zeros.
- If the argument is `NULL`, the function returns `NULL`.

Examples:

```sql
SELECT LOWER("TiDB");

+---------------+
| LOWER("TiDB") |
+---------------+
| tidb          |
+---------------+
```

```sql
SELECT LOWER(-012);

+-------------+
| LOWER(-012) |
+-------------+
| -12         |
+-------------+
```

### [`LPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lpad)

The `LPAD(str, len, padstr)` function returns the string argument, left-padded with the specified string `padstr` to a length of `len` characters.

- If `len` is less than the length of the string `str`, the function truncates the string `str` to the length of `len`.
- If `len` is a negative number, the function returns `NULL`.
- If any argument is `NULL`, the function returns `NULL`.

Examples:

```sql
SELECT LPAD('TiDB',8,'>');
+--------------------+
| LPAD('TiDB',8,'>') |
+--------------------+
| >>>>TiDB           |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT LPAD('TiDB',2,'>');
+--------------------+
| LPAD('TiDB',2,'>') |
+--------------------+
| Ti                 |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT LPAD('TiDB',-2,'>');
+---------------------+
| LPAD('TiDB',-2,'>') |
+---------------------+
| NULL                |
+---------------------+
1 row in set (0.00 sec)
```

### [`LTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ltrim)

The `LTRIM()` function removes leading spaces from a given string.

If the argument is `NULL`, this function returns `NULL`.

> **Note:**
>
> This function only removes the space character (U+0020) and does not remove other space-like characters such as tab (U+0009) or non-breaking space (U+00A0).

Examples:

In the following example, the `LTRIM()` function removes the leading spaces from `'    hello'` and returns `hello`.

```sql
SELECT LTRIM('    hello');
```

```
+--------------------+
| LTRIM('    hello') |
+--------------------+
| hello              |
+--------------------+
1 row in set (0.00 sec)
```

In the following example, [`CONCAT()`](#concat) is used to enclose the result of `LTRIM('    hello')` with `«` and `»`. This formatting makes it a bit easier to see that all leading spaces are removed.

```sql
SELECT CONCAT('«',LTRIM('    hello'),'»');
```

```
+------------------------------------+
| CONCAT('«',LTRIM('    hello'),'»') |
+------------------------------------+
| «hello»                            |
+------------------------------------+
1 row in set (0.00 sec)
```

### [`MAKE_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_make-set)

The `MAKE_SET()` function returns a set of comma-separated strings based on whether a corresponding bit in the `bits` argument is set to `1`.

Syntax:

```sql
MAKE_SET(bits, str1, str2, ...)
```

- `bits`: controls which subsequent string arguments to include in the result set. If `bits` is set to `NULL`, the function returns `NULL`.
- `str1, str2, ...`: a list of strings. Each string corresponds to a bit in the `bits` argument from right to left. `str1` corresponds to the first bit from the right, `str2` corresponds to the second bit from the right, and so on. If the corresponding bit is `1`, the string is included in the result; otherwise, it is not included.

Examples:

In the following example, because all bits are set to `0` in the `bits` argument, the function does not include any subsequent strings in the result and returns an empty string.

```sql
SELECT MAKE_SET(b'000','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'000','foo','bar','baz') |
+------------------------------------+
|                                    |
+------------------------------------+
1 row in set (0.00 sec)
```

In the following example, because only the first bit from the right is `1`, the function only returns the first string `foo`.

```sql
SELECT MAKE_SET(b'001','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'001','foo','bar','baz') |
+------------------------------------+
| foo                                |
+------------------------------------+
1 row in set (0.00 sec)
```

In the following example, because only the second bit from the right is `1`, the function only returns the second string `bar`.

```sql
SELECT MAKE_SET(b'010','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'010','foo','bar','baz') |
+------------------------------------+
| bar                                |
+------------------------------------+
1 row in set (0.00 sec)
```

In the following example, because only the third bit from the right is `1`, the function only returns the third string `baz`.

```sql
SELECT MAKE_SET(b'100','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'100','foo','bar','baz') |
+------------------------------------+
| baz                                |
+------------------------------------+
1 row in set (0.00 sec)
```

In the following example, because all bits are `1`, the function returns all three strings in a comma-separated result set.

```sql
SELECT MAKE_SET(b'111','foo','bar','baz');
```

```
+------------------------------------+
| MAKE_SET(b'111','foo','bar','baz') |
+------------------------------------+
| foo,bar,baz                        |
+------------------------------------+
1 row in set (0.0002 sec)
```

### [`MID()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_mid)

The `MID(str, pos[, len])` function returns a substring starting from the specified `pos` position with the `len` length.

Starting from v8.4.0, TiDB supports the two-argument variant `MID(str, pos)`. If `len` is not specified, this function returns all remaining characters from the specified `pos` position to the end of the string.

If any of the arguments are `NULL`, the function returns `NULL`.

Examples:

In the following example, `MID()` returns the substring of the input string starting from the second character (`b`) with a length of `3` characters.

```sql
SELECT MID('abcdef',2,3);
```

```
+-------------------+
| MID('abcdef',2,3) |
+-------------------+
| bcd               |
+-------------------+
1 row in set (0.00 sec)
```

In the following example, `MID()` returns the substring of the input string starting from the second character (`b`) to the end of the string.

```sql
SELECT MID('abcdef',2);
```

```
+-------------------+
| MID('abcdef',2)   |
+-------------------+
| bcdef             |
+-------------------+
1 row in set (0.00 sec)
```

### [`NOT LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)

Negation of simple pattern matching.

This function performs the inverse operation of [`LIKE`](#like).

Examples:

In the following example, `NOT LIKE` returns `0` (False) because `aaa` matches the `a%` pattern.

```sql
SELECT 'aaa' LIKE 'a%', 'aaa' NOT LIKE 'a%';
```

```
+-----------------+---------------------+
| 'aaa' LIKE 'a%' | 'aaa' NOT LIKE 'a%' |
+-----------------+---------------------+
|               1 |                   0 |
+-----------------+---------------------+
1 row in set (0.00 sec)
```

In the following example, `NOT LIKE` returns `1` (True) because `aaa` does not match the `b%` pattern.

```sql
SELECT 'aaa' LIKE 'b%', 'aaa' NOT LIKE 'b%';
```

```
+-----------------+---------------------+
| 'aaa' LIKE 'b%' | 'aaa' NOT LIKE 'b%' |
+-----------------+---------------------+
|               0 |                   1 |
+-----------------+---------------------+
1 row in set (0.00 sec)
```

### [`NOT REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp)

Negation of [`REGEXP`](#regexp).

### [`OCT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct)

Return a string containing [octal](https://en.wikipedia.org/wiki/Octal) (base 8) representation of a number.

Examples:

The following example generates a sequence of numbers from 0 to 20 using a [recursive common table expression (CTE)](/develop/dev-guide-use-common-table-expression.md#recursive-cte) and then uses the `OCT()` function to convert each number to its octal representation. Decimal values from 0 to 7 have identical representations in octal. Decimal numbers from 8 to 15 correspond to octal numbers from 10 to 17.

```sql
WITH RECURSIVE nr(n) AS (
    SELECT 0 AS n
    UNION ALL
    SELECT n+1 FROM nr WHERE n<20
)
SELECT n, OCT(n) FROM nr;
```

```
+------+--------+
| n    | OCT(n) |
+------+--------+
|    0 | 0      |
|    1 | 1      |
|    2 | 2      |
|    3 | 3      |
|    4 | 4      |
|    5 | 5      |
|    6 | 6      |
|    7 | 7      |
|    8 | 10     |
|    9 | 11     |
|   10 | 12     |
|   11 | 13     |
|   12 | 14     |
|   13 | 15     |
|   14 | 16     |
|   15 | 17     |
|   16 | 20     |
|   17 | 21     |
|   18 | 22     |
|   19 | 23     |
|   20 | 24     |
+------+--------+
20 rows in set (0.00 sec)
```

### [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_octet-length)

Synonym for [`LENGTH()`](#length).

### [`ORD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord)

Return the character code for the leftmost character of the given argument.

This function is similar to [`CHAR()`](#char) but works the other way around.

Examples:

Taking `a` and `A` as an example, `ORD()` returns `97` for `a` and `65` for `A`.

```sql
SELECT ORD('a'), ORD('A');
```

```
+----------+----------+
| ORD('a') | ORD('A') |
+----------+----------+
|       97 |       65 |
+----------+----------+
1 row in set (0.00 sec)
```

If you take the character code obtained from `ORD()` as input, you can get the original characters back using the `CHAR()` function. Note that the output format might vary depending on whether the `binary-as-hex` option is enabled in your MySQL client.

```sql
SELECT CHAR(97), CHAR(65);
```

```
+----------+----------+
| CHAR(97) | CHAR(65) |
+----------+----------+
| a        | A        |
+----------+----------+
1 row in set (0.01 sec)
```

The following example shows how `ORD()` handles multibyte characters. Here, both `101` and `0x65` are the UTF-8 encoded values for the `e` character, but in different formats. And both `50091` and `0xC3AB` represent the same values, but for the `ë` character.

```sql
SELECT ORD('e'), ORD('ë'), HEX('e'), HEX('ë');
```

```
+----------+-----------+----------+-----------+
| ORD('e') | ORD('ë')  | HEX('e') | HEX('ë')  |
+----------+-----------+----------+-----------+
|      101 |     50091 | 65       | C3AB      |
+----------+-----------+----------+-----------+
1 row in set (0.00 sec)
```

### [`POSITION()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_position)

Synonym for [`LOCATE()`](#locate).

### [`QUOTE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote)

Escape the argument for use in an SQL statement.

If the argument is `NULL`, the function returns `NULL`.

Example:

To display the result directly instead of showing a hexadecimal-encoded value, you need to start the MySQL client with the [`--skip-binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) option.

The following example shows that the ASCII NULL character is escaped as `\0` and the single quote character `'` is escaped as `\'`:

```sql
SELECT QUOTE(0x002774657374);
```

```
+-----------------------+
| QUOTE(0x002774657374) |
+-----------------------+
| '\0\'test'            |
+-----------------------+
1 row in set (0.00 sec)
```

### [`REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)

Pattern matching using regular expressions.

Examples:

In this example a number of strings are matched against two regular expressions.

```sql
WITH vals AS (
    SELECT 'TiDB' AS v
    UNION ALL
    SELECT 'Titanium'
    UNION ALL
    SELECT 'Tungsten'
    UNION ALL
    SELECT 'Rust'
)
SELECT
    v,
    v REGEXP '^Ti' AS 'starts with "Ti"',
    v REGEXP '^.{4}$' AS 'Length is 4 characters'
FROM
    vals;
```

```
+----------+------------------+------------------------+
| v        | starts with "Ti" | Length is 4 characters |
+----------+------------------+------------------------+
| TiDB     |                1 |                      1 |
| Titanium |                1 |                      0 |
| Tungsten |                0 |                      0 |
| Rust     |                0 |                      1 |
+----------+------------------+------------------------+
4 rows in set (0.00 sec)
```

The following example demonstrates that `REGEXP` is not limited to the `SELECT` clause. For example, you can also use it in the `WHERE` clause of the query.

```sql
SELECT
    v
FROM (
        SELECT 'TiDB' AS v
    ) AS vals
WHERE
    v REGEXP 'DB$';
```

```
+------+
| v    |
+------+
| TiDB |
+------+
1 row in set (0.01 sec)
```

### [`REGEXP_INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-instr)

Return the starting index of the substring that matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)).

The `REGEXP_INSTR(str, regexp, [start, [match, [ret, [match_type]]]])` function returns the position of the match if the regular expression (`regexp`) matches the string (`str`).

If either the `str` or `regexp` is `NULL`, then the function returns `NULL`.

Examples:

In the example below you can see that the `^.b.$` matches `abc`.

```sql
SELECT REGEXP_INSTR('abc','^.b.$');
```

```
+-----------------------------+
| REGEXP_INSTR('abc','^.b.$') |
+-----------------------------+
|                           1 |
+-----------------------------+
1 row in set (0.00 sec)
```

The following example uses the third argument to look for a match with a different start position in the string.

```sql
SELECT REGEXP_INSTR('abcabc','a');
```

```
+----------------------------+
| REGEXP_INSTR('abcabc','a') |
+----------------------------+
|                          1 |
+----------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT REGEXP_INSTR('abcabc','a',2);
```

```
+------------------------------+
| REGEXP_INSTR('abcabc','a',2) |
+------------------------------+
|                            4 |
+------------------------------+
1 row in set (0.00 sec)
```

The following example uses the 4th argument to look for the second match.

```sql
SELECT REGEXP_INSTR('abcabc','a',1,2);
```

```
+--------------------------------+
| REGEXP_INSTR('abcabc','a',1,2) |
+--------------------------------+
|                              4 |
+--------------------------------+
1 row in set (0.00 sec)
```

The following example uses the 5th argument to return the value _after_ the mach, instead of the value of the match.

```sql
SELECT REGEXP_INSTR('abcabc','a',1,1,1);
```

```
+----------------------------------+
| REGEXP_INSTR('abcabc','a',1,1,1) |
+----------------------------------+
|                                2 |
+----------------------------------+
1 row in set (0.00 sec)
```

The following example uses the 6th argument to add the `i` flag to get a case insensitive match. For more details about regular expression `match_type`, see [`match_type` compatibility](#match_type-compatibility).

```sql
SELECT REGEXP_INSTR('abcabc','A',1,1,0,'');
```

```
+-------------------------------------+
| REGEXP_INSTR('abcabc','A',1,1,0,'') |
+-------------------------------------+
|                                   0 |
+-------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT REGEXP_INSTR('abcabc','A',1,1,0,'i');
```

```
+--------------------------------------+
| REGEXP_INSTR('abcabc','A',1,1,0,'i') |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)
```

Besides `match_type`, the [collation](/character-set-and-collation.md) also influences the matching. The following example uses a case-sensitive and a case-insensitive collation to demonstrate this.

```sql
SELECT REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_general_ci);
```

```
+-------------------------------------------------------+
| REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_general_ci) |
+-------------------------------------------------------+
|                                                     1 |
+-------------------------------------------------------+
1 row in set (0.01 sec)
```

```sql
SELECT REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_bin);
```

```
+------------------------------------------------+
| REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_bin) |
+------------------------------------------------+
|                                              0 |
+------------------------------------------------+
1 row in set (0.00 sec)
```

### [`REGEXP_LIKE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-like)

Whether the string matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)).

The `REGEXP_LIKE(str, regex, [match_type])` function is used to test if a regular expression matches a string. Optionally the `match_type` can be used to change the matching behavior.

Examples:

The following example shows that `^a` matches `abc`.

```sql
SELECT REGEXP_LIKE('abc','^a');
```

```
+-------------------------+
| REGEXP_LIKE('abc','^a') |
+-------------------------+
|                       1 |
+-------------------------+
1 row in set (0.00 sec)
```

This following example shows that `^A` does not match `abc`.

```sql
SELECT REGEXP_LIKE('abc','^A');
```

```
+-------------------------+
| REGEXP_LIKE('abc','^A') |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.00 sec)
```

This example matches `^A` against `abc`, which now matches because of the `i` flag which enabled case insensitive matching. For more details about the regular expression `match_type`, see [`match_type` compatibility](#match_type-compatibility).

```sql
SELECT REGEXP_LIKE('abc','^A','i');
```

```
+-----------------------------+
| REGEXP_LIKE('abc','^A','i') |
+-----------------------------+
|                           1 |
+-----------------------------+
1 row in set (0.00 sec)
```

### [`REGEXP_REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-replace)

Replace substrings that match the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)).

The `REGEXP_REPLACE(str, regexp, replace, [start, [match, [match_type]]])` function can be used to replace strings based on regular expressions.

Examples:

In the following example, two o's are replaced by `i`.

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i');
```

```
+--------------------------------------+
| REGEXP_REPLACE('TooDB', 'o{2}', 'i') |
+--------------------------------------+
| TiDB                                 |
+--------------------------------------+
1 row in set (0.00 sec)
```

The following example starts the match at the third character, causing the regular expression not to match and not do any replacement.

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i',3);
```

```
+----------------------------------------+
| REGEXP_REPLACE('TooDB', 'o{2}', 'i',3) |
+----------------------------------------+
| TooDB                                  |
+----------------------------------------+
1 row in set (0.00 sec)
```

In the following example, the 5th argument is used to set if the first or the second match is used for the replacement.

```sql
SELECT REGEXP_REPLACE('TooDB', 'o', 'i',1,1);
```

```
+---------------------------------------+
| REGEXP_REPLACE('TooDB', 'o', 'i',1,1) |
+---------------------------------------+
| TioDB                                 |
+---------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT REGEXP_REPLACE('TooDB', 'o', 'i',1,2);
```

```
+---------------------------------------+
| REGEXP_REPLACE('TooDB', 'o', 'i',1,2) |
+---------------------------------------+
| ToiDB                                 |
+---------------------------------------+
1 row in set (0.00 sec)
```

The following example uses the 6th argument to set the `match_type` for case insensitive matching. For more details about the regular expression `match_type`, see [`match_type` compatibility](#match_type-compatibility).

```sql
SELECT REGEXP_REPLACE('TooDB', 'O{2}','i',1,1);
```

```
+-----------------------------------------+
| REGEXP_REPLACE('TooDB', 'O{2}','i',1,1) |
+-----------------------------------------+
| TooDB                                   |
+-----------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT REGEXP_REPLACE('TooDB', 'O{2}','i',1,1,'i');
```

```
+---------------------------------------------+
| REGEXP_REPLACE('TooDB', 'O{2}','i',1,1,'i') |
+---------------------------------------------+
| TiDB                                        |
+---------------------------------------------+
1 row in set (0.00 sec)
```

### [`REGEXP_SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-substr)

Return the substring that matches the regular expression (Partly compatible with MySQL. For more details, see [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)).

The `REGEXP_SUBSTR(str, regexp, [start, [match, [match_type]]])` function is used to get a substring based on a regular expression.

The following example uses the `Ti.{2}` regular expression to get the `TiDB` substring of the `This is TiDB` string.

```sql
SELECT REGEXP_SUBSTR('This is TiDB','Ti.{2}');
```

```
+----------------------------------------+
| REGEXP_SUBSTR('This is TiDB','Ti.{2}') |
+----------------------------------------+
| TiDB                                   |
+----------------------------------------+
1 row in set (0.00 sec)
```

### [`REPEAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_repeat)

Repeat a string the specified number of times.

Examples:

The following example generates a sequence of numbers from 1 to 20 using a [recursive common table expression (CTE)](/develop/dev-guide-use-common-table-expression.md#recursive-cte). For each number in the sequence, the character `x` is repeated the number of times equal to the number itself.

```sql
WITH RECURSIVE nr(n) AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n+1 FROM nr WHERE n<20
)
SELECT n, REPEAT('x',n) FROM nr;
```

```
+------+----------------------+
| n    | REPEAT('x',n)        |
+------+----------------------+
|    1 | x                    |
|    2 | xx                   |
|    3 | xxx                  |
|    4 | xxxx                 |
|    5 | xxxxx                |
|    6 | xxxxxx               |
|    7 | xxxxxxx              |
|    8 | xxxxxxxx             |
|    9 | xxxxxxxxx            |
|   10 | xxxxxxxxxx           |
|   11 | xxxxxxxxxxx          |
|   12 | xxxxxxxxxxxx         |
|   13 | xxxxxxxxxxxxx        |
|   14 | xxxxxxxxxxxxxx       |
|   15 | xxxxxxxxxxxxxxx      |
|   16 | xxxxxxxxxxxxxxxx     |
|   17 | xxxxxxxxxxxxxxxxx    |
|   18 | xxxxxxxxxxxxxxxxxx   |
|   19 | xxxxxxxxxxxxxxxxxxx  |
|   20 | xxxxxxxxxxxxxxxxxxxx |
+------+----------------------+
20 rows in set (0.01 sec)
```

The following example demonstrates that `REPEAT()` can operate on strings consisting of multiple characters.

```sql
SELECT REPEAT('ha',3);
```

```
+----------------+
| REPEAT('ha',3) |
+----------------+
| hahaha         |
+----------------+
1 row in set (0.00 sec)
```

### [`REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_replace)

Replace occurrences of a specified string.

### [`REVERSE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse)

Reverse the characters in a string.

### [`RIGHT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right)

Return the specified rightmost number of characters.

### [`RLIKE`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)

Synonym for [`REGEXP`](#regexp).

### [`RPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rpad)

Append string the specified number of times.

### [`RTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rtrim)

Remove trailing spaces.

### [`SPACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_space)

Return a string of the specified number of spaces.

### [`STRCMP()`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp)

Compare two strings.

### [`SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substr)

Return the substring as specified.

### [`SUBSTRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring)

Return the substring as specified.

### [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring-index)

The `SUBSTRING_INDEX()` function is used to extract a substring from a string based on a specified delimiter and count. This function is particularly useful when dealing with data separated by a specific delimiter, such as parsing CSV data or processing log files.

Syntax:

```sql
SUBSTRING_INDEX(str, delim, count)
```

- `str`: specifies the string to be processed.
- `delim`: specifies the delimiter in the string, which is case-sensitive.
- `count`: specifies the number of occurrences of the delimiter.
    - If `count` is a positive number, the function returns the substring before the `count` occurrences (counting from the left of the string) of the delimiter.
    - If `count` is a negative number, the function returns the substring after the `count` occurrences (counting from the right of the string) of the delimiter.
    - If `count` is `0`, the function returns an empty string.

Example 1:

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', 2);
```

Output 1:

```sql
+-----------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', 2) |
+-----------------------------------------+
| www.tidbcloud                                |
+-----------------------------------------+
```

Example 2:

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', -1);
```

Output 2:

```sql
+------------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', -1) |
+------------------------------------------+
| com                                      |
+------------------------------------------+
```

### [`TO_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_to-base64)

The `TO_BASE64()` function is used to convert the given argument to a string in the base-64 encoded form and return the result according to the character set and collation of the current connection. A base-64 encoded string can be decoded using the [`FROM_BASE64()`](#from_base64) function.

Syntax:

```sql
TO_BASE64(str)
```

- If the argument is not a string, the function converts it to a string before base-64 encoding.
- If the argument is `NULL`, the function returns `NULL`.

Example 1:

```sql
SELECT TO_BASE64('abc');
```

Output 1:

```sql
+------------------+
| TO_BASE64('abc') |
+------------------+
| YWJj             |
+------------------+
```

Example 2:

```sql
SELECT TO_BASE64(6);
```

Output 2:

```sql
+--------------+
| TO_BASE64(6) |
+--------------+
| Ng==         |
+--------------+
```

### [`TRANSLATE()`](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRANSLATE.html#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690)

Replace all occurrences of characters by other characters in a string. It does not treat empty strings as `NULL` as Oracle does.

### [`TRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_trim)

Remove leading and trailing spaces.

### [`UCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ucase)

The `UCASE()` function is used to convert a string to uppercase letters. This function is equivalent to the `UPPER()` function.

> **Note:**
>
> When the string is null, the `UCASE()` function returns `NULL`.

Example:

```sql
SELECT UCASE('bigdata') AS result_upper, UCASE(null) AS result_null;
```

Output:

```sql
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### [`UNHEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_unhex)

The `UNHEX()` function performs the reverse operation of the `HEX()` function. It treats each pair of characters in the argument as a hexadecimal number and converts it to the character represented by that number, returning the result as a binary string.

> **Note:**
>
> - The argument must be a valid hexadecimal value that contains `0`–`9`, `A`–`F`, or `a`–`f`. If the argument is `NULL` or falls outside this range, the function returns `NULL`.
> - In the MySQL client, the [`--binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) option is enabled by default in interactive mode, causing the client to display data with an unknown character set as a [hexadecimal literal](https://dev.mysql.com/doc/refman/8.0/en/hexadecimal-literals.html). You can use the `--skip-binary-as-hex` option to disable this behavior.

Example:

```sql
SELECT UNHEX('54694442');
```

Output:

```sql
+--------------------------------------+
| UNHEX('54694442')                    |
+--------------------------------------+
| 0x54694442                           |
+--------------------------------------+
```

### [`UPPER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_upper)

The `UPPER()` function is used to convert a string to uppercase letters. This function is equivalent to the `UCASE()` function.

> **Note:**
>
> When the string is null, the `UPPER()` function returns `NULL`.

Example:

```sql
SELECT UPPER('bigdata') AS result_upper, UPPER(null) AS result_null;
```

Output:

```sql
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### [`WEIGHT_STRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_weight-string)

The `WEIGHT_STRING()` function returns the weight string (binary characters) for the input string, primarily used for sorting and comparison operations in multi-character set scenarios. If the argument is `NULL`, it returns `NULL`. The syntax is as follows:

```sql
WEIGHT_STRING(str [AS {CHAR|BINARY}(N)])
```

- `str`: the input string expression. If it is a non-binary string, such as a `CHAR`, `VARCHAR`, or `TEXT` value, the return value contains the collation weights for the string. If it is a binary string, such as a `BINARY`, `VARBINARY`, or `BLOB` value, the return value is the same as the input.

- `AS {CHAR|BINARY}(N)`: optional parameters used to specify the type and length of the output. `CHAR` represents the character data type, and `BINARY` represents the binary data type. `N` specifies the output length, which is an integer greater than or equal to 1.

> **Note:**
>
> If `N` is less than the string length, the string is truncated. If `N` exceeds the string length, `AS CHAR(N)` pads the string with spaces to the specified length, and `AS BINARY(N)` pads the string with `0x00` to the specified length.

Example:

```sql
SET NAMES 'utf8mb4';
SELECT HEX(WEIGHT_STRING('ab' AS CHAR(3))) AS char_result, HEX(WEIGHT_STRING('ab' AS BINARY(3))) AS binary_result;
```

Output:

```sql
+-------------+---------------+
| char_result | binary_result |
+-------------+---------------+
| 6162        | 616200        |
+-------------+---------------+
```

## Unsupported functions

* `LOAD_FILE()`
* `MATCH()`
* `SOUNDEX()`

## Regular expression compatibility with MySQL

The following sections describe the regular expression compatibility with MySQL, including `REGEXP_INSTR()`, `REGEXP_LIKE()`, `REGEXP_REPLACE()`, and `REGEXP_SUBSTR()`.

### Syntax compatibility

MySQL implements regular expression using International Components for Unicode (ICU), and TiDB uses RE2. To learn the syntax differences between the two libraries, you can refer to the [ICU documentation](https://unicode-org.github.io/icu/userguide/) and [RE2 Syntax](https://github.com/google/re2/wiki/Syntax).

### `match_type` compatibility

The value options of `match_type` between TiDB and MySQL are:

- Value options in TiDB are `"c"`, `"i"`, `"m"`, and `"s"`, and value options in MySQL are `"c"`, `"i"`, `"m"`, `"n"`, and `"u"`.
- The `"s"` in TiDB corresponds to `"n"` in MySQL. When `"s"` is set in TiDB, the `.` character also matches line terminators (`\n`).

    For example, the `SELECT REGEXP_LIKE(a, b, "n") FROM t1` in MySQL is the same as the `SELECT REGEXP_LIKE(a, b, "s") FROM t1` in TiDB.

- TiDB does not support `"u"`, which means Unix-only line endings in MySQL.

| `match_type` | MySQL | TiDB | Description                            |
|:------------:|-------|------|----------------------------------------|
| c            | Yes   | Yes  | Case-sensitive matching                |
| i            | Yes   | Yes  | Case-insensitive matching              |
| m            | Yes   | Yes  | Multi-line mode                        |
| s            | No    | Yes  | Matches newlines, same as `n` in MySQL |
| n            | Yes   | No   | Matches newlines, same as `s` in TiDB  |
| u            | Yes   | No   | UNIX&trade; line endings               |

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

### Known issues

- [GitHub Issue #37981](https://github.com/pingcap/tidb/issues/37981)
