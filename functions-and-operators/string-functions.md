---
title: String Functions
summary: 了解 TiDB 中的字符串函数。
---

# String Functions {#string-functions}

TiDB 支持大部分 [string functions](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html) 在 MySQL 8.0 中提供的函数，以及部分 [functions](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009) 在 Oracle 21 中的实现。

<CustomContent platform="tidb">

关于 Oracle 和 TiDB 之间函数和语法的对比，请参见 [Comparisons between Functions and Syntax of Oracle and TiDB](/oracle-functions-to-tidb.md)。

</CustomContent>

## 支持的函数 {#supported-functions}

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ascii"><code>ASCII()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ascii-code-ascii-code-a}

`ASCII(str)` 函数用于获取给定参数中最左边字符的 ASCII 值。参数可以是字符串或数字。

-   如果参数不为空，返回最左字符的 ASCII 值。
-   如果参数为空字符串，返回 `0`。
-   如果参数为 `NULL`，返回 `NULL`。

> **Note:**
>
> `ASCII(str)` 仅适用于用 8 位二进制数字（1 字节）表示的字符。

示例：

```sql
SELECT ASCII('A'), ASCII('TiDB'), ASCII(23);
```

输出：

```sql
+------------+---------------+-----------+
| ASCII('A') | ASCII('TiDB') | ASCII(23) |
+------------+---------------+-----------+
|         65 |            84 |        50 |
+------------+---------------+-----------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bin"><code>BIN()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-bin-code-bin-code-a}

`BIN()` 函数用于将给定参数转换为其二进制值的字符串表示。参数可以是字符串或数字。

-   如果参数为正数，返回其二进制值的字符串表示。
-   如果参数为负数，先取绝对值转换为二进制，然后逐位取反（`0` 变 `1`，`1` 变 `0`），再加 `1`。
-   如果参数是只包含数字的字符串，返回结果与数字相同。例如，`"123"` 和 `123` 的结果相同。
-   如果参数是字符串且第一个字符不是数字（如 `"q123"`），返回 `0`。
-   如果参数是包含数字和非数字字符的字符串，返回从开头连续数字部分的结果。例如，`"123q123"` 和 `123` 的结果相同，但 `BIN('123q123')` 会产生类似 `Truncated incorrect INTEGER value: '123q123'` 的警告。
-   如果参数为 `NULL`，返回 `NULL`。

示例 1：

```sql
SELECT BIN(123), BIN('123q123');
```

输出 1：

```sql
+----------+----------------+
| BIN(123) | BIN('123q123') |
+----------+----------------+
| 1111011  | 1111011        |
+----------+----------------+
```

示例 2：

```sql
SELECT BIN(-7);
```

输出 2：

```sql
+------------------------------------------------------------------+
| BIN(-7)                                                          |
+------------------------------------------------------------------+
| 1111111111111111111111111111111111111111111111111111111111111001 |
+------------------------------------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bit-length"><code>BIT_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-bit-length-code-bit-length-code-a}

`BIT_LENGTH()` 函数用于返回给定参数的长度（以位为单位）。

示例：

```sql
SELECT BIT_LENGTH("TiDB");

+--------------------+
| BIT_LENGTH("TiDB") |
+--------------------+
|                 32 |
+--------------------+
```

每个字符 8 位 x 4 个字符 = 32 位

```sql
SELECT BIT_LENGTH("PingCAP 123");

+---------------------------+
| BIT_LENGTH("PingCAP 123") |
+---------------------------+
|                        88 |
+---------------------------+
```

每个字符 8 位（空格也算在内，因为它是非字母数字字符） x 11 个字符 = 88 位

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
> 上述示例假设存在一个名为 `Customers` 的数据库表，且表中有一个名为 `CustomerName` 的列。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char"><code>CHAR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-char-code-char-code-a}

`CHAR()` 函数用于获取对应 ASCII 值的字符。它与 `ASCII()` 相反，后者返回字符的 ASCII 值。如果提供多个参数，函数会对所有参数进行操作，然后连接成一个字符串。

示例：

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

`CHAR()` 也可以用来获取超出标准 ASCII 范围（`0` - `127`）的 ASCII 值对应的字符。

```sql
/*扩展 ASCII: */

SELECT CHAR(128);

+------------+
|  CHAR(128) |
+------------+
|       0x80 |
+------------+
```

`CHAR()` 还可以获取 Unicode 值对应的字符。

```sql
/* Unicode: */

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

    +----------------+
    | CHAR(65,66,67) |
    +----------------+
    | ABC            |
    +----------------+
    1 行结果（0.00 秒）

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char-length"><code>CHAR_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-char-length-code-char-length-code-a}

`CHAR_LENGTH()` 函数用于获取给定参数的字符总数，返回值为整数。

示例：

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
> 上述示例假设存在一个名为 `Customers` 的数据库表，且表中有一个名为 `CustomerName` 的列。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_character-length"><code>CHARACTER_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-character-length-code-character-length-code-a}

`CHARACTER_LENGTH()` 与 `CHAR_LENGTH()` 功能相同，两者可以互用，因为它们产生相同的输出。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat"><code>CONCAT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-concat-code-concat-code-a}

`CONCAT()` 函数将一个或多个参数连接成一个字符串。

语法：

```sql
CONCAT(str1,str2,...)
```

`str1, str2, ...` 是待连接的参数列表。每个参数可以是字符串或数字。

示例：

```sql
SELECT CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE);
```

输出：

```sql
+---------------------------------------------+
| CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE) |
+---------------------------------------------+
| TiDB Server-11                              |
+---------------------------------------------+
```

如果任何参数为 `NULL`，`CONCAT()` 返回 `NULL`。

示例：

```sql
SELECT CONCAT('TiDB', NULL, 'Server');
```

输出：

```sql
+--------------------------------+
| CONCAT('TiDB', NULL, 'Server') |
+--------------------------------+
| NULL                           |
+--------------------------------+
```

除了 `CONCAT()` 函数外，还可以通过将字符串相邻放置的方式进行连接，如下例所示。注意此方法不支持数字类型。

```sql
SELECT 'Ti' 'DB' ' ' 'Server';
```

输出：

```sql
+-------------+
| Ti          |
+-------------+
| TiDB Server |
+-------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat-ws"><code>CONCAT_WS()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-concat-ws-code-concat-ws-code-a}

`CONCAT_WS()` 是带分隔符的 [`CONCAT()`](#concat) 形式，返回由指定分隔符连接的字符串。

语法：

```sql
CONCAT_WS(separator,str1,str2,...)
```

-   `separator`：第一个参数为分隔符，用于连接剩余参数（不为 `NULL` 的部分）。
-   `str1, str2, ...`：待连接的参数列表。每个参数可以是字符串或数字。

示例：

```sql
SELECT CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD');
```

输出：

```sql
+---------------------------------------------+
| CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD') |
+---------------------------------------------+
| TiDB Server,TiKV,PD                         |
+---------------------------------------------+
```

-   如果分隔符为空字符串，`CONCAT_WS()` 等价于 `CONCAT()`，返回剩余参数连接的字符串。

    示例：

    ```sql
    SELECT CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD');
    ```

    输出：

    ```sql
    +--------------------------------------------+
    | CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD') |
    +--------------------------------------------+
    | TiDB ServerTiKVPD                          |
    +--------------------------------------------+
    ```

-   如果分隔符为 `NULL`，`CONCAT_WS()` 返回 `NULL`。

    示例：

    ```sql
    SELECT CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD');
    ```

    输出：

    ```sql
    +----------------------------------------------+
    | CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD') |
    +----------------------------------------------+
    | NULL                                         |
    +----------------------------------------------+
    ```

-   如果待连接的参数中只有一个不是 `NULL`，`CONCAT_WS()` 返回该参数。

    示例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL);
    ```

    输出：

    ```sql
    +-------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL) |
    +-------------------------------------+
    | TiDB Server                         |
    +-------------------------------------+
    ```

-   如果待连接的参数中存在 `NULL`，`CONCAT_WS()` 会跳过这些 `NULL`。

    示例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL, 'PD');
    ```

    输出：

    ```sql
    +-------------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL, 'PD') |
    +-------------------------------------------+
    | TiDB Server,PD                            |
    +-------------------------------------------+
    ```

-   如果待连接的字符串中有空字符串，`CONCAT_WS()` 不会跳过。

    示例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', '', 'PD');
    ```

    输出：

    ```sql
    +-----------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', '', 'PD') |
    +-----------------------------------------+
    | TiDB Server,,PD                         |
    +-----------------------------------------+
    ```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_elt"><code>ELT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-elt-code-elt-code-a}

`ELT()` 函数返回第 `index` 个元素。

```sql
SELECT ELT(3, 'This', 'is', 'TiDB');
```

```sql
+------------------------------+
| ELT(3, 'This', 'is', 'TiDB') |
+------------------------------+
| TiDB                         |
+------------------------------+
1 行结果（0.00 秒）
```

上述示例返回第三个元素，即 `'TiDB'`。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set"><code>EXPORT_SET()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-export-set-code-export-set-code-a}

`EXPORT_SET()` 函数返回由指定的 `number_of_bits` 个 `on`/`off` 值组成的字符串，值之间可用 `separator` 分隔。这些值基于 `bits` 参数中对应位是否为 `1`，第一个值对应最低位（最右边的位）。

语法：

```sql
EXPORT_SET(bits, on, off, [separator[, number_of_bits]])
```

-   `bits`：表示位值的整数。
-   `on`：当对应位为 `1` 时返回的字符串。
-   `off`：当对应位为 `0` 时返回的字符串。
-   `separator`（可选）：结果字符串中的分隔符字符。
-   `number_of_bits`（可选）：要处理的位数。如果未设置，默认使用 `64`（最大位数），即 `bits` 被视为无符号的 64 位整数。

示例：

在以下示例中，`number_of_bits` 设置为 `5`，生成 5 个值，用 `|` 分隔。由于只给出了 3 位，其他位视为未设置。因此，将 `number_of_bits` 设置为 `101` 或 `00101`，结果相同。

```sql
SELECT EXPORT_SET(b'101',"ON",'off','|',5);
```

```sql
+-------------------------------------+
| EXPORT_SET(b'101',"ON",'off','|',5) |
+-------------------------------------+
| ON|off|ON|off|off                   |
+-------------------------------------+
1 行结果（0.00 秒）
```

在以下示例中，`bits` 设置为 `00001111`，`on` 设置为 `x`，`off` 设置为 `_`。这会导致函数对 `0` 位返回 `____`，对 `1` 位返回 `xxxx`。从右到左处理 `00001111` 时，返回 `xxxx____`。

```sql
SELECT EXPORT_SET(b'00001111', 'x', '_', '', 8);
```

```sql
+------------------------------------------+
| EXPORT_SET(b'00001111', 'x', '_', '', 8) |
+------------------------------------------+
| xxxx____                                 |
+------------------------------------------+
1 行结果（0.00 秒）
```

在以下示例中，`bits` 设置为 `00001111`，`on` 设置为 `x`，`off` 设置为 `_`。这会导致每个 `1` 位返回 `x`，每个 `0` 位返回 `_`。从右到左处理 `01010101` 时，返回 `x_x_x_x_`。

```sql
SELECT EXPORT_SET(b'01010101', 'x', '_', '', 8);
```

```sql
+------------------------------------------+
| EXPORT_SET(b'01010101', 'x', '_', '', 8) |
+------------------------------------------+
| x_x_x_x_                                 |
+------------------------------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_field"><code>FIELD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-field-code-field-code-a}

返回第一个参数在后续参数中的位置（索引）。

在以下示例中，`FIELD()` 的第一个参数为 `needle`，它在列表中第二个参数中匹配，因此返回 `2`。

```sql
SELECT FIELD('needle', 'A', 'needle', 'in', 'a', 'haystack');
+-------------------------------------------------------+
| FIELD('needle', 'A', 'needle', 'in', 'a', 'haystack') |
+-------------------------------------------------------+
|                                                     2 |
+-------------------------------------------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_find-in-set"><code>FIND_IN_SET()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-find-in-set-code-find-in-set-code-a}

返回第一个参数在第二个参数中的索引位置。

此函数常用于 [`SET`](/data-type-string.md#set-type) 类型数据。

在以下示例中，`Go` 是集合 `COBOL,BASIC,Rust,Go,Java,Fortran` 中的第 4 个元素，因此返回 `4`。

```sql
SELECT FIND_IN_SET('Go', 'COBOL,BASIC,Rust,Go,Java,Fortran');
+-------------------------------------------------------+
| FIND_IN_SET('Go', 'COBOL,BASIC,Rust,Go,Java,Fortran') |
+-------------------------------------------------------+
|                                                     4 |
+-------------------------------------------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_format"><code>FORMAT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-format-code-format-code-a}

`FORMAT(X,D[,locale])` 函数用于将数字 `X` 格式化为类似 `"#,###,###. ##"` 的格式，四舍五入到 `D` 位小数，并以字符串形式返回。

参数：

-   `X`：待格式化的数字，可以是直接的数值、数字字符串或科学计数法表示的数字。
-   `D`：返回值的小数位数。函数会将 `X` 四舍五入到 `D` 位小数。如果 `D` 大于 `X` 实际的小数位数，则用零补齐。
-   `[locale]`：指定用于分组（千位分隔符、小数点等）的区域设置。有效的区域值与 [`lc_time_names`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_lc_time_names) 系统变量的值相同。未指定或区域设置为 `NULL` 时，默认使用 `'en_US'`。此参数为可选。

行为说明：

-   如果第一个参数为字符串且只包含数字，返回基于该数字的结果。例如，`FORMAT('12.34', 1)` 和 `FORMAT(12.34, 1)` 返回相同结果。
-   如果第一个参数为科学计数法表示的数字（用 `E/e`），返回基于该数字的结果。例如，`FORMAT('1E2', 3)` 返回 `100.000`。
-   如果第一个参数为以非数字字符开头的字符串，返回零并产生警告 `(Code 1292)`。例如，`FORMAT('q12.36', 5)` 返回 `0.00000`，同时会有警告 `Warning (Code 1292): Truncated incorrect DOUBLE value: 'q12.36'`。
-   如果第一个参数为数字和非数字字符混合的字符串，返回从开头连续数字部分的结果，并产生警告 `(Code 1292)`。例如，`FORMAT('12.36q56.78', 1)` 返回与 `FORMAT('12.36', 1)` 相同的数字结果，但会有警告 `Warning (Code 1292): Truncated incorrect DOUBLE value: '12.36q56.78'`。
-   如果第二个参数为零或负数，则截断小数部分，返回整数。
-   如果任何参数为 `NULL`，返回 `NULL`。

示例：

以下示例演示如何将数字 12.36 格式化为不同的小数位数：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_from-base64"><code>FROM_BASE64()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-from-base64-code-from-base64-code-a}

`FROM_BASE64()` 函数用于解码 [Base64](https://datatracker.ietf.org/doc/html/rfc4648) 编码的字符串，并以十六进制形式返回解码结果。

-   该函数接受一个参数，即待解码的 Base64 编码字符串。
-   如果参数为 `NULL` 或不是有效的 Base64 编码字符串，返回 `NULL`。

示例：

以下示例演示如何解码 `'SGVsbG8gVGlEQg=='`，该字符串是用 [`TO_BASE64()`](#to_base64) 编码 `'Hello TiDB'` 后的结果。

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

以下示例演示如何解码数字 `MTIzNDU2`，该字符串是用 [`TO_BASE64()`](#to_base64) 编码 `123456` 后的结果。

```sql
mysql> SELECT FROM_BASE64('MTIzNDU2');
+--------------------------------------------------+
| FROM_BASE64('MTIzNDU2')                          |
+--------------------------------------------------+
| 0x313233343536                                   |
+--------------------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_hex"><code>HEX()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-hex-code-hex-code-a}

`HEX()` 函数用于将给定参数转换为其十六进制值的字符串表示。参数可以是字符串或数字。

-   如果参数为字符串，`HEX(str)` 返回 `str` 的十六进制字符串表示。函数会将每个字符的每个字节转换为两个十六进制数字。例如，字符 `a` 在 UTF-8 或 ASCII 编码中表示为二进制值 `00111101`，十六进制为 `61`。
-   如果参数为数字，`HEX(n)` 返回 `n` 的十六进制字符串表示。函数将参数 `n` 视为 `BIGINT` 数字，等价于 `CONV(n, 10, 16)`。
-   如果参数为 `NULL`，返回 `NULL`。

> **Note:**
>
> 在 MySQL 客户端中，交互模式下默认启用 [`--binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) 选项，导致显示未知字符集的数据时以十六进制字面量显示。可以使用 `--skip-binary-as-hex` 选项禁用此行为。

示例（使用 `mysql --skip-binary-as-hex`）：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_insert"><code>INSERT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-insert-code-insert-code-a}

`INSERT(str, pos, len, newstr)` 函数用于将字符串 `str` 中，从位置 `pos` 开始，长度为 `len` 的子串替换为 `newstr`。此函数支持多字节字符。

-   如果 `pos` 超出 `str` 长度，返回原字符串 `str`。
-   如果 `len` 超出从 `pos` 开始到字符串末尾的长度，替换剩余部分。
-   如果任何参数为 `NULL`，返回 `NULL`。

示例：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_instr"><code>INSTR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-instr-code-instr-code-a}

`INSTR(str, substr)` 函数用于获取 `substr` 在 `str` 中第一次出现的位置。参数可以是字符串或数字。此函数与 `LOCATE(substr, str)` 的两参数版本相同，但参数顺序相反。

> **Note:**
>
> `INSTR(str, substr)` 的大小写敏感性由 TiDB 中使用的 [collations](/character-set-and-collation.md) 决定。二进制排序（后缀 `_bin`）区分大小写，而通用排序（后缀 `_general_ci` 或 `_ai_ci`）不区分大小写。

-   如果任一参数为数字，视为字符串处理。
-   如果 `substr` 不在 `str` 中，返回 `0`。否则返回第一次出现的位置。
-   如果任一参数为 `NULL`，返回 `NULL`。

示例：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#operator-lcase"><code>LCASE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-lcase-code-lcase-code-a}

`LCASE(str)` 是 [`LOWER(str)`](#lower) 的同义词，返回参数的全部字符的小写形式。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_left"><code>LEFT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-left-code-left-code-a}

`LEFT()` 函数返回字符串左侧的指定字符数。

语法：

```sql
LEFT(`str`, `len`)
```

-   `str`：原始字符串，用于提取字符。如果 `str` 包含多字节字符，函数会将其作为单一代码点计数。
-   `len`：返回的字符数。
    -   如果 `len` 小于或等于 0，返回空字符串。
    -   如果 `len` 大于或等于 `str` 的长度，返回原字符串 `str`。
-   如果任何参数为 `NULL`，返回 `NULL`。

示例：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_length"><code>LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-length-code-length-code-a}

`LENGTH()` 函数返回字符串的字节长度。

`LENGTH()` 统计多字节字符时会将其视为多个字节，而 `CHAR_LENGTH()` 将多字节字符视为单一代码点。

如果参数为 `NULL`，返回 `NULL`。

示例：

```sql
SELECT LENGTH('ABC');
+---------------+
| LENGTH('ABC') |
+---------------+
|             3 |
+---------------+
```

```sql
SELECT LENGTH('🍣ABC');
+-------------------+
| LENGTH('🍣ABC')     |
+-------------------+
|                 7 |
+-------------------+
```

```sql
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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator-like"><code>LIKE</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-comparison-functions-html-operator-like-code-like-code-a}

`LIKE` 操作符用于简单的字符串匹配。表达式 `expr LIKE pat [ESCAPE 'escape_char']` 返回 `1`（`TRUE`）或 `0`（`FALSE`）。如果 `expr` 或 `pat` 为 `NULL`，结果为 `NULL`。

可以使用以下两个通配符参数：

-   `%`：匹配任意字符（包括零个字符）。
-   `_`：匹配恰好一个字符。

以下示例使用 `utf8mb4_bin` 排序规则：

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

默认的转义字符为 `\`：

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

若要指定其他转义字符（如 `*`），可以使用 `ESCAPE` 子句：

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

可以用 `LIKE` 来匹配数字值：

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

也可以用 `COLLATE` 指定排序规则，例如 `utf8mb4_unicode_ci`：

```sql
SELECT '🍣🍺Sushi🍣🍺' COLLATE utf8mb4_unicode_ci LIKE '%SUSHI%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_locate"><code>LOCATE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-locate-code-locate-code-a}

`LOCATE(substr, str[, pos])` 函数用于获取 `substr` 在 `str` 中第一次出现的位置。参数 `pos` 为可选，表示从哪个位置开始搜索。

-   如果子串 `substr` 不在 `str` 中，返回 `0`。
-   如果任一参数为 `NULL`，返回 `NULL`。
-   该函数支持多字节字符，且仅在至少一个参数为二进制字符串时区分大小写。

以下示例使用 `utf8mb4_bin` 排序规则：

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

以下示例使用 `utf8mb4_unicode_ci` 排序规则：

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

以下多字节和二进制字符串示例使用 `utf8mb4_bin` 排序规则：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lower"><code>LOWER()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-lower-code-lower-code-a}

`LOWER(str)` 函数用于将参数 `str` 中的所有字符转换为小写。参数可以是字符串或数字。

-   如果参数为字符串，返回小写字符串。
-   如果参数为数字，返回去除前导零的数字。
-   如果参数为 `NULL`，返回 `NULL`。

示例：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lpad"><code>LPAD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-lpad-code-lpad-code-a}

`LPAD(str, len, padstr)` 函数返回字符串 `str`，左侧用 `padstr` 填充至长度为 `len`。

-   如果 `len` 小于 `str` 长度，截断 `str` 至 `len`。
-   如果 `len` 为负数，返回 `NULL`。
-   如果任何参数为 `NULL`，返回 `NULL`。

示例：

```sql
SELECT LPAD('TiDB',8,'>');
+--------------------+
| LPAD('TiDB',8,'>') |
+--------------------+
| >>>>TiDB           |
+--------------------+
1 行结果（0.00 秒）
```

```sql
SELECT LPAD('TiDB',2,'>');
+--------------------+
| LPAD('TiDB',2,'>') |
+--------------------+
| Ti                 |
+--------------------+
1 行结果（0.00 秒）
```

```sql
SELECT LPAD('TiDB',-2,'>');
+---------------------+
| LPAD('TiDB',-2,'>') |
+---------------------+
| NULL                |
+---------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ltrim"><code>LTRIM()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ltrim-code-ltrim-code-a}

`LTRIM()` 函数用于去除字符串左侧的空格。

如果参数为 `NULL`，返回 `NULL`。

> **Note:**
>
> 该函数只会去除空格字符（U+0020），不会去除制表符（U+0009）或不间断空格（U+00A0）等其他空白字符。

示例：

以下示例中，`LTRIM()` 去除 `'    hello'` 左侧的空格，返回 `hello`。

```sql
SELECT LTRIM('    hello');
```

    +--------------------+
    | LTRIM('    hello') |
    +--------------------+
    | hello              |
    +--------------------+
    1 行结果（0.00 秒）

以下示例中，使用 [`CONCAT()`](#concat) 将 `LTRIM('    hello')` 的结果用 `«` 和 `»` 包裹，方便观察所有左侧空格已被去除。

```sql
SELECT CONCAT('«',LTRIM('    hello'),'»');
```

    +------------------------------------+
    | CONCAT('«',LTRIM('    hello'),'»') |
    +------------------------------------+
    | «hello»                            |
    +------------------------------------+
    1 行结果（0.00 秒）

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_make-set"><code>MAKE_SET()</code></a> {#a-href-https-dev-mysql.com/doc/refman/8-0/en/string-functions-html-function-make-set-code-make-set-code-a}

`MAKE_SET()` 函数根据 `bits` 参数中对应位是否为 `1`，返回一个逗号分隔的字符串集合。

语法：

```sql
MAKE_SET(bits, str1, str2, ...)
```

-   `bits`：控制后续字符串参数的包含。若为 `NULL`，返回 `NULL`。
-   `str1, str2, ...`：字符串列表。每个字符串对应 `bits` 参数中的一位，从右到左。`str1` 对应最低位，`str2` 对应次低位，依此类推。对应位为 `1` 时，字符串包含在结果中，否则不包含。

示例：

在以下示例中，由于 `bits` 全为 `0`，函数不包含任何后续字符串，返回空字符串。

```sql
SELECT MAKE_SET(b'000','foo','bar','baz');
```

```sql
+------------------------------------+
| MAKE_SET(b'000','foo','bar','baz') |
+------------------------------------+
|                                    |
+------------------------------------+
1 行结果（0.00 秒）
```

在以下示例中，只有最低位为 `1`，函数只返回第一个字符串 `foo`。

```sql
SELECT MAKE_SET(b'001','foo','bar','baz');
```

```sql
+------------------------------------+
| MAKE_SET(b'001','foo','bar','baz') |
+------------------------------------+
| foo                                |
+------------------------------------+
1 行结果（0.00 秒）
```

在以下示例中，第二位为 `1`，函数只返回第二个字符串 `bar`。

```sql
SELECT MAKE_SET(b'010','foo','bar','baz');
```

```sql
+------------------------------------+
| MAKE_SET(b'010','foo','bar','baz') |
+------------------------------------+
| bar                                |
+------------------------------------+
1 行结果（0.00 秒）
```

在以下示例中，第三位为 `1`，函数只返回第三个字符串 `baz`。

```sql
SELECT MAKE_SET(b'100','foo','bar','baz');
```

```sql
+------------------------------------+
| MAKE_SET(b'100','foo','bar','baz') |
+------------------------------------+
| baz                                |
+------------------------------------+
1 行结果（0.00 秒）
```

在所有位都为 `1` 时，函数返回所有字符串，用逗号连接。

```sql
SELECT MAKE_SET(b'111','foo','bar','baz');
```

```sql
+------------------------------------+
| MAKE_SET(b'111','foo','bar','baz') |
+------------------------------------+
| foo,bar,baz                        |
+------------------------------------+
1 行结果（0.0002 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_mid"><code>MID()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-mid-code-mid-code-a}

`MID(str, pos[, len])` 函数返回从指定位置 `pos` 开始，长度为 `len` 的子串。

从 v8.4.0 开始，TiDB 支持两参数版本 `MID(str, pos)`。如果未指定 `len`，则返回从 `pos` 开始到字符串末尾的所有字符。

如果任何参数为 `NULL`，返回 `NULL`。

示例：

以下示例中，`MID()` 返回从第二个字符（`b`）开始，长度为 3 的子串。

```sql
SELECT MID('abcdef',2,3);
```

```sql
+-------------------+
| MID('abcdef',2,3) |
+-------------------+
| bcd               |
+-------------------+
1 行结果（0.00 秒）
```

以下示例中，`MID()` 返回从第二个字符（`b`）开始，到字符串末尾的子串。

```sql
SELECT MID('abcdef',2);
```

```sql
+-------------------+
| MID('abcdef',2)   |
+-------------------+
| bcdef             |
+-------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like"><code>NOT LIKE</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-comparison-functions-html-operator-not-like-code-not-like-code-a}

简单模式匹配的取反。

此函数执行 [`LIKE`](#like) 的逆操作。

示例：

以下示例中，`NOT LIKE` 返回 `0`（假），因为 `'aaa'` 匹配 `'a%'` 模式。

```sql
SELECT 'aaa' LIKE 'a%', 'aaa' NOT LIKE 'a%';
```

```sql
+-----------------+---------------------+
| 'aaa' LIKE 'a%' | 'aaa' NOT LIKE 'a%' |
+-----------------+---------------------+
|               1 |                   0 |
+-----------------+---------------------+
1 行结果（0.00 秒）
```

以下示例中，`NOT LIKE` 返回 `1`（真），因为 `'aaa'` 不匹配 `'b%'` 模式。

```sql
SELECT 'aaa' LIKE 'b%', 'aaa' NOT LIKE 'b%';
```

```sql
+-----------------+---------------------+
| 'aaa' LIKE 'b%' | 'aaa' NOT LIKE 'b%' |
+-----------------+---------------------+
|               0 |                   1 |
+-----------------+---------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp"><code>NOT REGEXP</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-operator-not-regexp-code-not-regexp-code-a}

`REGEXP` 的取反。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct"><code>OCT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-oct-code-oct-code-a}

返回数字的八进制（base 8）字符串。

示例：

以下示例使用递归公共表表达式（CTE）生成 0 到 20 的数字序列，然后用 `OCT()` 函数将每个数字转换为八进制表示。0 到 7 的十进制值在八进制中表示相同，8 到 15 的十进制对应八进制的 10 到 17。

```sql
WITH RECURSIVE nr(n) AS (
    SELECT 0 AS n
    UNION ALL
    SELECT n+1 FROM nr WHERE n<20
)
SELECT n, OCT(n) FROM nr;
```

输出示例：

```sql
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
20 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_octet-length"><code>OCTET_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-octet-length-code-octet-length-code-a}

`OCTET_LENGTH()` 是 [`LENGTH()`](#length) 的同义词。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord"><code>ORD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ord-code-ord-code-a}

返回参数中最左字符的字符编码。

此函数类似于 [`CHAR()`](#char)，但作用相反。

示例：

以 `a` 和 `A` 为例，`ORD()` 对 `a` 返回 `97`，对 `A` 返回 `65`。

```sql
SELECT ORD('a'), ORD('A');
```

```sql
+----------+----------+
| ORD('a') | ORD('A') |
+----------+----------+
|       97 |       65 |
+----------+----------+
1 行结果（0.00 秒）
```

如果用 `ORD()` 获取的字符编码作为输入，可以用 `CHAR()` 还原字符。注意输出格式可能会因 MySQL 客户端启用的 `binary-as-hex` 选项而不同。

```sql
SELECT CHAR(97), CHAR(65);
```

```sql
+----------+----------+
| CHAR(97) | CHAR(65) |
+----------+----------+
| a        | A        |
+----------+----------+
1 行结果（0.01 秒）
```

以下示例演示 `ORD()` 如何处理多字节字符。这里，`101` 和 `0x65` 都是字符 `e` 的 UTF-8 编码值，但格式不同。`50091` 和 `0xC3AB` 代表相同的值，但对应字符 `ë`。

```sql
SELECT ORD('e'), ORD('ë'), HEX('e'), HEX('ë');
```

```sql
+----------+-----------+----------+-----------+
| ORD('e') | ORD('ë')  | HEX('e') | HEX('ë')  |
+----------+-----------+----------+-----------+
|      101 |     50091 | 65       | C3AB      |
+----------+-----------+----------+-----------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_position"><code>POSITION()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-position-code-position-code-a}

`POSITION()` 是 [`LOCATE()`](#locate) 的同义词。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote"><code>QUOTE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-quote-code-quote-code-a}

对参数进行转义，用于在 SQL 语句中使用。

如果参数为 `NULL`，返回 `NULL`。

示例：

为了直接显示结果而不是十六进制编码值，需要在 MySQL 客户端启用 [`--skip-binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) 选项。

以下示例演示 ASCII 空字符会被转义为 `\0`，单引号字符 `'` 会被转义为 `\'`：

```sql
SELECT QUOTE(0x002774657374);
```

```sql
+-----------------------+
| QUOTE(0x002774657374) |
+-----------------------+
| '\0\'test'            |
+-----------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp"><code>REGEXP</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-operator-regexp-code-regexp-code-a}

正则表达式匹配。

示例：

在此示例中，多个字符串与两个正则表达式进行匹配。

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

```plaintext
+----------+------------------+------------------------+
| v        | starts with "Ti" | Length is 4 characters |
+----------+------------------+------------------------+
| TiDB     |                1 |                      1 |
| Titanium |                1 |                      0 |
| Tungsten |                0 |                      0 |
| Rust     |                0 |                      1 |
+----------+------------------+------------------------+
20 行结果（0.00 秒）
```

此示例演示 `REGEXP` 不仅可以在 `SELECT` 中使用，还可以在 `WHERE` 条件中。

```sql
SELECT
    v
FROM (
        SELECT 'TiDB' AS v
    ) AS vals
WHERE
    v REGEXP 'DB$';
```

```plaintext
+------+
| v    |
+------+
| TiDB |
+------+
1 行结果（0.01 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-instr"><code>REGEXP_INSTR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-function-regexp-instr-code-regexp-instr-code-a}

返回匹配正则表达式的子串的起始索引（部分兼容 MySQL。详情参见 [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)）。

`REGEXP_INSTR(str, regexp, [start, [match, [ret, [match_type]]]])` 函数在正则表达式 (`regexp`) 匹配字符串 (`str`) 时，返回匹配的位置。

如果 `str` 或 `regexp` 为 `NULL`，返回 `NULL`。

示例：

以下示例中，`^.b.$` 匹配 `abc`。

```sql
SELECT REGEXP_INSTR('abc','^.b.$');
```

```plaintext
+-----------------------------+
| REGEXP_INSTR('abc','^.b.$') |
+-----------------------------+
|                           1 |
+-----------------------------+
1 行结果（0.00 秒）
```

以下示例中，使用第三个参数在字符串中从不同位置开始查找。

```sql
SELECT REGEXP_INSTR('abcabc','a');
```

```plaintext
+----------------------------+
| REGEXP_INSTR('abcabc','a') |
+----------------------------+
|                          1 |
+----------------------------+
```

```sql
SELECT REGEXP_INSTR('abcabc','a',2);
```

```plaintext
+------------------------------+
| REGEXP_INSTR('abcabc','a',2) |
+------------------------------+
|                            4 |
+------------------------------+
```

以下示例中，使用第四个参数查找第二个匹配。

```sql
SELECT REGEXP_INSTR('abcabc','a',1,2);
```

```plaintext
+--------------------------------+
| REGEXP_INSTR('abcabc','a',1,2) |
+--------------------------------+
|                              4 |
+--------------------------------+
```

以下示例中，使用第五个参数返回匹配之后的值，而不是匹配位置。

```sql
SELECT REGEXP_INSTR('abcabc','a',1,1,1);
```

```plaintext
+----------------------------------+
| REGEXP_INSTR('abcabc','a',1,1,1) |
+----------------------------------+
|                                2 |
+----------------------------------+
```

以下示例中，使用第六个参数添加 `i` 标志，实现不区分大小写的匹配。关于 `match_type` 的更多信息，请参见 [`match_type` compatibility](#match_type-compatibility)。

```sql
SELECT REGEXP_INSTR('abcabc','A',1,1,0,'');
```

```plaintext
+-------------------------------------+
| REGEXP_INSTR('abcabc','A',1,1,0,'') |
+-------------------------------------+
|                                   0 |
+-------------------------------------+
```

```sql
SELECT REGEXP_INSTR('abcabc','A',1,1,0,'i');
```

```plaintext
+--------------------------------------+
| REGEXP_INSTR('abcabc','A',1,1,0,'i') |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
```

除了 `match_type`，排序规则（collation）也会影响匹配结果。以下示例演示区分大小写和不区分大小写的效果。

```sql
SELECT REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_general_ci);
```

```plaintext
+-------------------------------------------------------+
| REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_general_ci) |
+-------------------------------------------------------+
|                                                     1 |
+-------------------------------------------------------+
```

```sql
SELECT REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_bin);
```

```plaintext
+------------------------------------------------+
| REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_bin) |
+------------------------------------------------+
|                                              0 |
+------------------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-like"><code>REGEXP_LIKE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-function-regexp-like-code-regexp-like-code-a}

判断字符串是否匹配正则表达式（部分兼容 MySQL。详情参见 [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)）。

`REGEXP_LIKE(str, regex, [match_type])` 函数用于测试正则表达式是否匹配字符串。可选的 `match_type` 用于改变匹配行为。

示例：

以下示例中，`^a` 匹配 `abc`。

```sql
SELECT REGEXP_LIKE('abc','^a');
```

```plaintext
+-------------------------+
| REGEXP_LIKE('abc','^a') |
+-------------------------+
|                       1 |
+-------------------------+
```

以下示例中，`^A` 不匹配 `abc`。

```sql
SELECT REGEXP_LIKE('abc','^A');
```

```plaintext
+-------------------------+
| REGEXP_LIKE('abc','^A') |
+-------------------------+
|                       0 |
+-------------------------+
```

以下示例中，启用不区分大小写的匹配（`i` 标志），`^A` 可以匹配 `abc`。

```sql
SELECT REGEXP_LIKE('abc','^A','i');
```

```plaintext
+-----------------------------+
| REGEXP_LIKE('abc','^A','i') |
+-----------------------------+
|                           1 |
+-----------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-replace"><code>REGEXP_REPLACE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-function-regexp-replace-code-regexp-replace-code-a}

用正则表达式替换子串（部分兼容 MySQL。详情参见 [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)）。

`REGEXP_REPLACE(str, regexp, replace, [start, [match, [match_type]]])` 函数可用于基于正则表达式替换字符串。

示例：

以下示例中，将两个 `o` 替换为 `i`。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i');
```

```plaintext
+--------------------------------------+
| REGEXP_REPLACE('TooDB', 'o{2}', 'i') |
+--------------------------------------+
| TiDB                                 |
+--------------------------------------+
1 行结果（0.00 秒）
```

以下示例中，从第三个字符开始匹配，导致正则不匹配，不进行替换。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i',3);
```

```plaintext
+----------------------------------------+
| REGEXP_REPLACE('TooDB', 'o{2}', 'i',3) |
+----------------------------------------+
| TooDB                                  |
+----------------------------------------+
1 行结果（0.00 秒）
```

以下示例中，使用第 5 个参数设置匹配的起始位置或第一个/第二个匹配。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o', 'i',1,1);
```

```plaintext
+---------------------------------------+
| REGEXP_REPLACE('TooDB', 'o', 'i',1,1) |
+---------------------------------------+
| TioDB                                 |
+---------------------------------------+
1 行结果（0.00 秒）
```

```sql
SELECT REGEXP_REPLACE('TooDB', 'o', 'i',1,2);
```

```plaintext
+---------------------------------------+
| REGEXP_REPLACE('TooDB', 'o', 'i',1,2) |
+---------------------------------------+
| ToiDB                                 |
+---------------------------------------+
1 行结果（0.00 秒）
```

以下示例中，使用第 6 个参数设置 `match_type`，实现不区分大小写的匹配。更多关于 `match_type` 的信息，请参见 [`match_type` compatibility](#match_type-compatibility)。

```sql
SELECT REGEXP_REPLACE('TooDB', 'O{2}','i',1,1);
```

```plaintext
+-----------------------------------------+
| REGEXP_REPLACE('TooDB', 'O{2}','i',1,1) |
+-----------------------------------------+
| TooDB                                   |
+-----------------------------------------+
1 行结果（0.00 秒）
```

```sql
SELECT REGEXP_REPLACE('TooDB', 'O{2}','i',1,1,'i');
```

```plaintext
+---------------------------------------------+
| REGEXP_REPLACE('TooDB', 'O{2}','i',1,1,'i') |
+---------------------------------------------+
| TiDB                                        |
+---------------------------------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-substr"><code>REGEXP_SUBSTR()</code></a> {#a-href-https-dev-mysql.com/doc/refman/8-0/en-regexp-html-function-regexp-substr-code-regexp-substr-code-a}

返回匹配正则表达式的子串（部分兼容 MySQL。详情参见 [Regular expression compatibility with MySQL](#regular-expression-compatibility-with-mysql)）。

`REGEXP_SUBSTR(str, regexp, [start, [match, [match_type]]])` 函数用于根据正则表达式获取子串。

以下示例中，使用正则 `Ti.{2}` 获取字符串 `This is TiDB` 中的 `TiDB` 子串。

```sql
SELECT REGEXP_SUBSTR('This is TiDB','Ti.{2}');
```

```plaintext
+----------------------------------------+
| REGEXP_SUBSTR('This is TiDB','Ti.{2}') |
+----------------------------------------+
| TiDB                                   |
+----------------------------------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_repeat"><code>REPEAT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-repeat-code-repeat-code-a}

重复字符串指定次数。

示例：

以下示例使用递归公共表表达式（CTE）生成 1 到 20 的数字序列，然后对每个数字，重复字符 `x`，次数等于数字本身。

```sql
WITH RECURSIVE nr(n) AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n+1 FROM nr WHERE n<20
)
SELECT n, REPEAT('x',n) FROM nr;
```

```plaintext
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
20 行结果（0.01 秒）
```

以下示例演示 `REPEAT()` 可以作用于由多个字符组成的字符串。

```sql
SELECT REPEAT('ha',3);
```

```plaintext
+----------------+
| REPEAT('ha',3) |
+----------------+
| hahaha         |
+----------------+
1 行结果（0.00 秒）
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_replace"><code>REPLACE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-replace-code-replace-code-a}

替换指定字符串的内容。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse"><code>REVERSE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-reverse-code-reverse-code-a}

反转字符串中的字符。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right"><code>RIGHT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-right-code-right-code-a}

返回字符串右侧的指定字符数。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp"><code>RLIKE</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-operator-regexp-code-rlike-code-a}

`REGEXP` 的同义词。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rpad"><code>RPAD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-rpad-code-rpad-code-a}

在字符串后面追加指定次数的字符串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rtrim"><code>RTRIM()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-rtrim-code-rtrim-code-a}

去除字符串右侧的空格。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_space"><code>SPACE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-space-code-space-code-a}

返回由指定数量空格组成的字符串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp"><code>STRCMP()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-comparison-functions-html-function-strcmp-code-strcmp-code-a}

比较两个字符串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substr"><code>SUBSTR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substr-code-substr-code-a}

返回指定的子串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring"><code>SUBSTRING()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substring-code-substring-code-a}

返回指定的子串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring-index"><code>SUBSTRING_INDEX()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substring-index-code-substring-index-code-a}

`SUBSTRING_INDEX()` 函数用于根据指定的分隔符和计数，从字符串中提取子串。该函数在处理由特定分隔符分隔的数据（如解析 CSV 或日志文件）时非常有用。

语法：

```sql
SUBSTRING_INDEX(str, delim, count)
```

-   `str`：待处理的字符串。
-   `delim`：字符串中的分隔符，区分大小写。
-   `count`：分隔符的出现次数。
    -   若为正数，返回从左开始第 `count` 次出现的分隔符之前的子串（不包括分隔符）。
    -   若为负数，返回从右开始第 `|` count `` 次出现的分隔符之后的子串（不包括分隔符）。
    -   若为 `0`，返回空字符串。

示例 1：

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', 2);
```

输出 1：

```sql
+-----------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', 2) |
+-----------------------------------------+
| www.tidbcloud                                |
+-----------------------------------------+
```

示例 2：

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', -1);
```

输出 2：

```sql
+------------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', -1) |
+------------------------------------------+
| com                                      |
+------------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_to-base64"><code>TO_BASE64()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-to-base64-code-to-base64-code-a}

`TO_BASE64()` 函数用于将参数转换为 base-64 编码字符串，并根据当前连接的字符集和排序规则返回结果。Base64 编码的字符串可以用 [`FROM_BASE64()`](#from_base64) 进行解码。

语法：

```sql
TO_BASE64(str)
```

-   如果参数不是字符串，函数会先将其转换为字符串再进行 base-64 编码。
-   如果参数为 `NULL`，返回 `NULL`。

示例 1：

```sql
SELECT TO_BASE64('abc');
```

输出 1：

```sql
+------------------+
| TO_BASE64('abc') |
+------------------+
| YWJj             |
+------------------+
```

示例 2：

```sql
SELECT TO_BASE64(6);
```

输出 2：

```sql
+--------------+
| TO_BASE64(6) |
+--------------+
| Ng==         |
+--------------+
```

### <a href="https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRANSLATE.html#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690"><code>TRANSLATE()</code></a> {#a-href-https-docs-oracle-com-en-database-oracle-oracle-database-21-sqlrf-translate-html-guid-80f85acb-092c-4cc7-91f6-b3a585e3a690-code-translate-code-a}

将字符串中的所有字符替换为其他字符。它不会像 Oracle 那样将空字符串视为 `NULL`。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_trim"><code>TRIM()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-trim-code-trim-code-a}

去除字符串两端的空格。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ucase"><code>UCASE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ucase-code-ucase-code-a}

`UCASE()` 函数用于将字符串转换为大写字母。等同于 `UPPER()`。

> **Note:**
>
> 当字符串为 `NULL` 时，`UCASE()` 返回 `NULL`。

示例：

```sql
SELECT UCASE('bigdata') AS result_upper, UCASE(null) AS result_null;
```

输出：

```sql
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_unhex"><code>UNHEX()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-unhex-code-unhex-code-a}

`UNHEX()` 函数执行 `HEX()` 的逆操作。它将参数中的每对字符视为十六进制数，并转换为该数字对应的字符，返回二进制字符串。

> **Note:**
>
> -   参数必须是有效的十六进制值，包含 `0`–`9`、`A`–`F` 或 `a`–`f`。如果参数为 `NULL` 或超出范围，返回 `NULL`。
> -   在 MySQL 客户端中，交互模式下默认启用 [`--binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex)，导致显示未知字符集的数据时以十六进制字面量显示。可以用 `--skip-binary-as-hex` 关闭此行为。

示例：

```sql
SELECT UNHEX('54694442');
```

输出：

```sql
+--------------------------------------+
| UNHEX('54694442')                    |
+--------------------------------------+
| 0x54694442                           |
+--------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_upper"><code>UPPER()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-upper-code-upper-code-a}

`UPPER()` 函数用于将字符串转换为大写字母。等同于 `UCASE()`。

> **Note:**
>
> 当字符串为 `NULL` 时，`UPPER()` 返回 `NULL`。

示例：

```sql
SELECT UPPER('bigdata') AS result_upper, UPPER(null) AS result_null;
```

```plaintext
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_weight-string"><code>WEIGHT_STRING()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-weight-string-code-weight-string-code-a}

`WEIGHT_STRING()` 函数返回输入字符串的权重字符串（二进制字符），主要用于多字符集场景下的排序和比较操作。若参数为 `NULL`，返回 `NULL`。语法如下：

```sql
WEIGHT_STRING(str [AS {CHAR|BINARY}(N)])
```

-   `str`：输入字符串表达式。如果是非二进制字符串（如 `CHAR`、`VARCHAR` 或 `TEXT`），返回值包含字符集的权重值；如果是二进制字符串（如 `BINARY`、`VARBINARY` 或 `BLOB`），返回值与输入相同。

-   `AS {CHAR|BINARY}(N)`：可选参数，用于指定输出类型和长度。`CHAR` 表示字符类型，`BINARY` 表示二进制类型。`N` 为输出长度，为大于等于 1 的整数。

> **Note:**
>
> 如果 `N` 小于字符串长度，则会截断字符串；如果 `N` 大于字符串长度，`AS CHAR(N)` 会用空格补齐，`AS BINARY(N)` 会用 `0x00` 补齐。

示例：

```sql
SET NAMES 'utf8mb4';
SELECT HEX(WEIGHT_STRING('ab' AS CHAR(3))) AS char_result, HEX(WEIGHT_STRING('ab' AS BINARY(3))) AS binary_result;
```

输出：

```sql
+-------------+---------------+
| char_result | binary_result |
+-------------+---------------+
| 6162        | 616200        |
+-------------+---------------+
```

## 不支持的函数 {#unsupported-functions}

-   `LOAD_FILE()`
-   `MATCH()`
-   `SOUNDEX()`

## 正则表达式与 MySQL 的兼容性 {#regular-expression-compatibility-with-mysql}

以下章节介绍正则表达式在 MySQL 中的兼容性，包括 `REGEXP_INSTR()`、`REGEXP_LIKE()`、`REGEXP_REPLACE()` 和 `REGEXP_SUBSTR()`。

### 语法兼容性 {#syntax-compatibility}

MySQL 使用 ICU（International Components for Unicode）实现正则表达式，而 TiDB 使用 RE2。想了解两者的语法差异，可以参考 [ICU 文档](https://unicode-org.github.io/icu/userguide/) 和 [RE2 语法](https://github.com/google/re2/wiki/Syntax)。

### <code>match_type</code> 兼容性 {#code-match-type-code-compatibility}

TiDB 和 MySQL 中 `match_type` 的取值选项如下：

-   TiDB 中的值为 `"c"`、`"i"`、`"m"` 和 `"s"`，MySQL 中的值为 `"c"`、`"i"`、`"m"`、`"n"` 和 `"u"`。
-   TiDB 中的 `"s"` 对应 MySQL 中的 `"n"`。当在 TiDB 中设置 `"s"` 时，`.` 字符也会匹配换行符（`\n`）。

  例如，MySQL 中的 `SELECT REGEXP_LIKE(a, b, "n") FROM t1` 与 TiDB 中的 `SELECT REGEXP_LIKE(a, b, "s") FROM t1` 等价。
-   TiDB 不支持 `"u"`，意味着在 MySQL 中的 Unix-only 换行符。

| `match_type` | MySQL | TiDB | 描述                         |
| :----------: | ----- | ---- | ---------------------------- |
|       c      | 是    | 是   | 匹配区分大小写               |
|       i      | 是    | 是   | 匹配不区分大小写             |
|       m      | 是    | 是   | 多行模式                     |
|       s      | 否    | 是   | 匹配换行符，等同于 `n`（MySQL） |
|       n      | 是    | 否   | 匹配换行符，等同于 `s`（TiDB） |
|       u      | 是    | 否   | UNIX™ 换行符                |

### 数据类型兼容性 {#data-type-compatibility}

TiDB 和 MySQL 对二进制字符串类型的支持差异：

-   MySQL 从 8.0.22 版本开始，不支持在正则表达式函数中使用二进制字符串。详情请参见 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/regexp.html)。但在实际中，只要所有参数或返回类型为二进制字符串，正则函数仍可在 MySQL 中正常工作，否则会报错。
-   目前，TiDB 禁止使用二进制字符串，任何情况下都会报错。

### 其他兼容性 {#other-compatibility}

-   TiDB 中空字符串的替换行为与 MySQL 不同。例如，`REGEXP_REPLACE("", "^$", "123")`：
    -   MySQL 不会替换空字符串，结果仍为 `""`。
    -   TiDB 会替换空字符串，结果为 `"123"`。
-   TiDB 中捕获组的关键字与 MySQL 不同。MySQL 使用 `$`，而 TiDB 使用 `\\`。此外，TiDB 仅支持编号从 `0` 到 `9` 的捕获组。

  例如，以下 SQL 在 TiDB 中会返回 `ab`：

  ```sql
  SELECT REGEXP_REPLACE('abcd','(.*)(.{2})$','\\1') AS s;
  ```

### 已知问题 {#known-issues}

-   [GitHub Issue #37981](https://github.com/pingcap/tidb/issues/37981)
