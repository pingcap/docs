---
title: 字符串函数
summary: 了解 TiDB 中的字符串函数。
---

# 字符串函数 {#string-functions}

TiDB 支持 MySQL 8.0 中大多数 [字符串函数](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html)，以及部分 Oracle 21 中的 [函数](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009)。

<CustomContent platform="tidb">

关于 Oracle 与 TiDB 函数和语法的对比，参见 [Oracle 与 TiDB 函数和语法对比](/oracle-functions-to-tidb.md)。

</CustomContent>

## 支持的函数 {#supported-functions}

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ascii"><code>ASCII()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ascii-code-ascii-code-a}

`ASCII(str)` 函数用于获取给定参数最左侧字符的 ASCII 值。参数可以是字符串或数字。

-   如果参数非空，函数返回最左侧字符的 ASCII 值。
-   如果参数为空字符串，函数返回 `0`。
-   如果参数为 `NULL`，函数返回 `NULL`。

> **Note:**
>
> `ASCII(str)` 只适用于用 8 位二进制位（一个字节）表示的字符。

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

-   如果参数为正数，函数返回其二进制值的字符串表示。
-   如果参数为负数，函数将参数的绝对值转换为二进制表示，对二进制值的每一位取反（`0` 变为 `1`，`1` 变为 `0`），然后加 `1`。
-   如果参数为仅包含数字的字符串，函数根据这些数字返回结果。例如，`"123"` 和 `123` 的结果相同。
-   如果参数为字符串且首字符不是数字（如 `"q123"`），函数返回 `0`。
-   如果参数为包含数字和非数字的字符串，函数根据参数开头连续的数字部分返回结果。例如，`"123q123"` 和 `123` 的结果相同，但 `BIN('123q123')` 会产生类似 `Truncated incorrect INTEGER value: '123q123'` 的警告。
-   如果参数为 `NULL`，函数返回 `NULL`。

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

`BIT_LENGTH()` 函数用于返回给定参数的比特位长度。

示例：

```sql
SELECT BIT_LENGTH("TiDB");

+--------------------+
| BIT_LENGTH("TiDB") |
+--------------------+
|                 32 |
+--------------------+
```

每个字符 8 位 × 4 个字符 = 32 位

```sql
SELECT BIT_LENGTH("PingCAP 123");

+---------------------------+
| BIT_LENGTH("PingCAP 123") |
+---------------------------+
|                        88 |
+---------------------------+
```

每个字符 8 位（空格也计入，因为它是非字母数字字符）× 11 个字符 = 88 位

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
> 上述示例假设存在一个名为 `Customers` 的数据库表，并且表中有一个名为 `CustomerName` 的列。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char"><code>CHAR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-char-code-char-code-a}

`CHAR()` 函数用于获取指定 ASCII 值对应的字符。它与 `ASCII()` 的操作相反，`ASCII()` 返回指定字符的 ASCII 值。如果传入多个参数，函数会对所有参数分别操作并将结果拼接在一起。

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

`CHAR()` 函数也可以获取超出标准 ASCII 范围（`0` - `127`）的 ASCII 值对应的字符。

```sql
/*For extended ASCII: */

SELECT CHAR(128);

+------------+
|  CHAR(128) |
+------------+
|       0x80 |
+------------+
```

`CHAR()` 函数还可以获取 Unicode 值对应的字符。

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

    +----------------+
    | CHAR(65,66,67) |
    +----------------+
    | ABC            |
    +----------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char-length"><code>CHAR_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-char-length-code-char-length-code-a}

`CHAR_LENGTH()` 函数用于获取给定参数的字符总数，返回整数。

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
> 上述示例假设存在一个名为 `Customers` 的数据库表，并且表中有一个名为 `CustomerName` 的列。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_character-length"><code>CHARACTER_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-character-length-code-character-length-code-a}

`CHARACTER_LENGTH()` 函数与 `CHAR_LENGTH()` 函数等价。两者可以互换使用，输出结果相同。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat"><code>CONCAT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-concat-code-concat-code-a}

`CONCAT()` 函数将一个或多个参数拼接为单个字符串。

语法：

```sql
CONCAT(str1,str2,...)
```

`str1, str2, ...` 是要拼接的参数列表。每个参数可以是字符串或数字。

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

如果任一参数为 `NULL`，`CONCAT()` 返回 `NULL`。

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

除了 `CONCAT()` 函数外，还可以通过将字符串直接相邻拼接的方式实现字符串拼接，如下例所示。注意该方法不支持数值类型。

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

`CONCAT_WS()` 函数是带分隔符的 [`CONCAT()`](#concat) 变体，返回由指定分隔符拼接的字符串。

语法：

```sql
CONCAT_WS(separator,str1,str2,...)
```

-   `separator`：第一个参数为分隔符，用于拼接剩余非 `NULL` 参数。
-   `str1, str2, ...`：要拼接的参数列表。每个参数可以是字符串或数字。

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

-   如果分隔符为空字符串，`CONCAT_WS()` 等价于 `CONCAT()`，返回剩余参数拼接后的字符串。

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

-   如果仅有一个待拼接参数非 `NULL`，`CONCAT_WS()` 返回该参数。

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

-   如果待拼接参数中有 `NULL`，`CONCAT_WS()` 会跳过这些 `NULL` 参数。

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

-   如果待拼接参数中有空字符串，`CONCAT_WS()` 不会跳过空字符串。

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

`ELT()` 函数返回指定索引位置的元素。

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

上述示例返回第三个元素，即 `'TiDB'`。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set"><code>EXPORT_SET()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-export-set-code-export-set-code-a}

`EXPORT_SET()` 函数返回一个由指定数量（`number_of_bits`）的 `on`/`off` 值组成的字符串，值之间可选用 `separator` 分隔。这些值基于 `bits` 参数中对应位是否为 `1`，第一个值对应 `bits` 的最右侧（最低位）。

语法：

```sql
EXPORT_SET(bits, on, off, [separator[, number_of_bits]])
```

-   `bits`：表示位值的整数。
-   `on`：对应位为 `1` 时返回的字符串。
-   `off`：对应位为 `0` 时返回的字符串。
-   `separator`（可选）：结果字符串中的分隔符。
-   `number_of_bits`（可选）：要处理的位数。如果未设置，默认使用 `64`（位最大长度），即将 `bits` 视为无符号 64 位整数。

示例：

下例中，`number_of_bits` 设置为 `5`，因此有 5 个值，用 `|` 分隔。由于只给了 3 位，其他位视为未设置。因此，`number_of_bits` 设置为 `101` 或 `00101`，输出相同。

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

下例中，`bits` 为 `00001111`，`on` 为 `x`，`off` 为 `_`，函数对 `0` 位返回 `____`，对 `1` 位返回 `xxxx`。从右到左处理 `00001111`，返回 `xxxx____`。

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

下例中，`bits` 为 `01010101`，`on` 为 `x`，`off` 为 `_`，从右到左处理，返回 `x_x_x_x_`。

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_field"><code>FIELD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-field-code-field-code-a}

返回第一个参数在后续参数中的索引（位置）。

下例中，`FIELD()` 的第一个参数为 `needle`，它与后续参数列表中的第二个参数匹配，因此函数返回 `2`。

```sql
SELECT FIELD('needle', 'A', 'needle', 'in', 'a', 'haystack');
+-------------------------------------------------------+
| FIELD('needle', 'A', 'needle', 'in', 'a', 'haystack') |
+-------------------------------------------------------+
|                                                     2 |
+-------------------------------------------------------+
1 row in set (0.00 sec)
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_find-in-set"><code>FIND_IN_SET()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-find-in-set-code-find-in-set-code-a}

返回第一个参数在第二个参数中的索引位置。

该函数常与 [`SET`](/data-type-string.md#set-type) 数据类型配合使用。

下例中，`Go` 是集合 `COBOL,BASIC,Rust,Go,Java,Fortran` 中的第四个元素，因此函数返回 `4`。

```sql
SELECT FIND_IN_SET('Go', 'COBOL,BASIC,Rust,Go,Java,Fortran');
+-------------------------------------------------------+
| FIND_IN_SET('Go', 'COBOL,BASIC,Rust,Go,Java,Fortran') |
+-------------------------------------------------------+
|                                                     4 |
+-------------------------------------------------------+
1 row in set (0.00 sec)
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_format"><code>FORMAT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-format-code-format-code-a}

`FORMAT(X,D[,locale])` 函数用于将数字 `X` 格式化为类似 `"#,###,###. ##"` 的格式，四舍五入到 `D` 位小数，并以字符串形式返回结果。

参数说明：

-   `X`：要格式化的数字。可以是直接的数值、数字字符串或科学计数法表示的数字。
-   `D`：返回值的小数位数。函数会将数字 `X` 四舍五入到 `D` 位小数。如果 `D` 大于 `X` 实际的小数位数，结果会补零到相应长度。
-   `[locale]`：指定用于小数点、千位分隔符和结果数字分隔符的区域设置。有效的区域值与 [`lc_time_names`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_lc_time_names) 系统变量的有效值相同。如果未指定或区域设置为 `NULL`，则默认使用 `'en_US'`。该参数为可选项。

行为说明：

-   如果第一个参数为仅包含数字的字符串，函数根据该数值返回结果。例如，`FORMAT('12.34', 1)` 和 `FORMAT(12.34, 1)` 返回相同结果。
-   如果第一个参数为科学计数法（带 `E/e`）表示的数字，函数根据该数值返回结果。例如，`FORMAT('1E2', 3)` 返回 `100.000`。
-   如果第一个参数为以非数字字符开头的字符串，函数返回零并产生警告 `(Code 1292)`。例如，`FORMAT('q12.36', 5)` 返回 `0.00000`，同时有警告 `Warning (Code 1292): Truncated incorrect DOUBLE value: 'q12.36'`。
-   如果第一个参数为数字和非数字混合的字符串，函数根据参数开头连续的数字部分返回结果，并产生警告 `(Code 1292)`。例如，`FORMAT('12.36q56.78', 1)` 返回与 `FORMAT('12.36', 1)` 相同的数值结果，但有警告 `Warning (Code 1292): Truncated incorrect DOUBLE value: '12.36q56.78'`。
-   如果第二个参数为零或负数，函数会截断小数部分并返回整数。
-   如果任一参数为 `NULL`，函数返回 `NULL`。

示例：

以下示例展示如何将数字 12.36 格式化为不同的小数位数：

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

-   该函数只接受一个参数，即要解码的 Base64 编码字符串。
-   如果参数为 `NULL` 或不是有效的 Base64 编码字符串，`FROM_BASE64()` 返回 `NULL`。

示例：

下例展示如何解码 Base64 编码字符串 `'SGVsbG8gVGlEQg=='`。该字符串是使用 [`TO_BASE64()`](#to_base64) 函数对 `'Hello TiDB'` 编码的结果。

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

下例展示如何解码 Base64 编码数字 `MTIzNDU2`。该字符串是对 `123456` 使用 [`TO_BASE64()`](#to_base64) 编码的结果。

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

-   如果参数为字符串，`HEX(str)` 返回 `str` 的十六进制字符串表示。函数将 `str` 中每个字符的每个字节转换为两个十六进制数字。例如，字符 `a` 在 UTF-8 或 ASCII 字符集下的二进制值为 `00111101`，十六进制为 `61`。
-   如果参数为数字，`HEX(n)` 返回 `n` 的十六进制字符串表示。函数将参数 `n` 视为 `BIGINT` 数字，等价于 `CONV(n, 10, 16)`。
-   如果参数为 `NULL`，函数返回 `NULL`。

> **Note:**
>
> 在 MySQL 客户端中，交互模式下默认启用 [`--binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) 选项，会将未知字符集的数据以 [十六进制字面量](https://dev.mysql.com/doc/refman/8.0/en/hexadecimal-literals.html) 显示。你可以使用 `--skip-binary-as-hex` 选项关闭该行为。

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

`INSERT(str, pos, len, newstr)` 函数用于将 `str` 中从位置 `pos` 开始、长度为 `len` 的子串替换为字符串 `newstr`。该函数支持多字节字符。

-   如果 `pos` 超过 `str` 的长度，函数返回原始字符串 `str`，不做修改。
-   如果 `len` 超过从 `pos` 开始剩余的字符串长度，函数会替换从 `pos` 开始的剩余部分。
-   如果任一参数为 `NULL`，函数返回 `NULL`。

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

`INSTR(str, substr)` 函数用于获取 `substr` 在 `str` 中首次出现的位置。每个参数可以是字符串或数字。该函数与 [`LOCATE(substr, str)`](#locate) 的双参数版本等价，但参数顺序相反。

> **Note:**
>
> `INSTR(str, substr)` 的大小写敏感性由 TiDB 所用的 [排序规则](/character-set-and-collation.md) 决定。二进制排序规则（后缀为 `_bin`）区分大小写，通用排序规则（后缀为 `_general_ci` 或 `_ai_ci`）不区分大小写。

-   如果任一参数为数字，函数会将数字视为字符串处理。
-   如果 `substr` 不在 `str` 中，函数返回 `0`。否则，返回 `substr` 在 `str` 中首次出现的位置。
-   如果任一参数为 `NULL`，函数返回 `NULL`。

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lcase"><code>LCASE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-lcase-code-lcase-code-a}

`LCASE(str)` 函数是 [`LOWER(str)`](#lower) 的同义词，返回参数的小写形式。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_left"><code>LEFT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-left-code-left-code-a}

`LEFT()` 函数返回字符串左侧指定数量的字符。

语法：

```sql
LEFT(`str`, `len`)
```

-   `str`：要提取字符的原始字符串。如果 `str` 包含多字节字符，函数将其视为单个码点。
-   `len`：要返回的字符长度。
    -   如果 `len` 小于等于 0，函数返回空字符串。
    -   如果 `len` 大于等于 `str` 的长度，函数返回原始 `str`。
-   如果任一参数为 `NULL`，函数返回 `NULL`。

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

`LENGTH()` 会将多字节字符计为多个字节，而 `CHAR_LENGTH()` 会将多字节字符计为一个码点。

如果参数为 `NULL`，函数返回 `NULL`。

示例：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like"><code>LIKE</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-comparison-functions-html-operator-like-code-like-code-a}

`LIKE` 运算符用于简单的字符串匹配。表达式 `expr LIKE pat [ESCAPE 'escape_char']` 返回 `1`（`TRUE`）或 `0`（`FALSE`）。如果 `expr` 或 `pat` 为 `NULL`，结果为 `NULL`。

你可以在 `LIKE` 中使用以下两个通配符：

-   `%` 匹配任意数量的字符，包括零个字符。
-   `_` 精确匹配一个字符。

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

默认转义字符为 `\`：

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

如需指定其他转义字符（如 `*`），可使用 `ESCAPE` 子句：

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

你可以使用 `LIKE` 运算符匹配数值：

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

如需显式指定排序规则（如 `utf8mb4_unicode_ci`），可使用 `COLLATE`：

```sql
SELECT '🍣🍺Sushi🍣🍺' COLLATE utf8mb4_unicode_ci LIKE '%SUSHI%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_locate"><code>LOCATE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-locate-code-locate-code-a}

`LOCATE(substr, str[, pos])` 函数用于获取字符串 `str` 中指定子串 `substr` 首次出现的位置。`pos` 参数为可选项，指定搜索的起始位置。

-   如果子串 `substr` 不在 `str` 中，函数返回 `0`。
-   如果任一参数为 `NULL`，函数返回 `NULL`。
-   该函数支持多字节字符，只有当至少一个参数为二进制字符串时才区分大小写。

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

`LOWER(str)` 函数用于将给定参数 `str` 的所有字符转换为小写。参数可以是字符串或数字。

-   如果参数为字符串，函数返回小写字符串。
-   如果参数为数字，函数返回去除前导零的数字。
-   如果参数为 `NULL`，函数返回 `NULL`。

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

`LPAD(str, len, padstr)` 函数返回用指定字符串 `padstr` 在左侧填充到长度为 `len` 的字符串。

-   如果 `len` 小于字符串 `str` 的长度，函数会将 `str` 截断为 `len` 长度。
-   如果 `len` 为负数，函数返回 `NULL`。
-   如果任一参数为 `NULL`，函数返回 `NULL`。

示例：

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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ltrim"><code>LTRIM()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ltrim-code-ltrim-code-a}

`LTRIM()` 函数用于去除给定字符串的前导空格。

如果参数为 `NULL`，该函数返回 `NULL`。

> **Note:**
>
> 该函数只会去除空格字符（U+0020），不会去除其他类似空格的字符，如制表符（U+0009）或不间断空格（U+00A0）。

示例：

下例中，`LTRIM()` 函数去除了 `'    hello'` 的前导空格，返回 `hello`。

```sql
SELECT LTRIM('    hello');
```

    +--------------------+
    | LTRIM('    hello') |
    +--------------------+
    | hello              |
    +--------------------+
    1 row in set (0.00 sec)

下例中，使用 [`CONCAT()`](#concat) 将 `LTRIM('    hello')` 的结果用 `«` 和 `»` 包裹，便于观察前导空格已被去除。

```sql
SELECT CONCAT('«',LTRIM('    hello'),'»');
```

    +------------------------------------+
    | CONCAT('«',LTRIM('    hello'),'»') |
    +------------------------------------+
    | «hello»                            |
    +------------------------------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_make-set"><code>MAKE_SET()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-make-set-code-make-set-code-a}

`MAKE_SET()` 函数根据 `bits` 参数中对应位是否为 `1`，返回由逗号分隔的字符串集合。

语法：

```sql
MAKE_SET(bits, str1, str2, ...)
```

-   `bits`：控制结果集中包含哪些后续字符串参数。如果 `bits` 为 `NULL`，函数返回 `NULL`。
-   `str1, str2, ...`：字符串列表。每个字符串从右到左分别对应 `bits` 的每一位。`str1` 对应最右侧第一位，`str2` 对应第二位，以此类推。对应位为 `1` 时，该字符串包含在结果中，否则不包含。

示例：

下例中，`bits` 参数所有位均为 `0`，函数不包含任何后续字符串，返回空字符串。

```sql
SELECT MAKE_SET(b'000','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'000','foo','bar','baz') |
    +------------------------------------+
    |                                    |
    +------------------------------------+
    1 row in set (0.00 sec)

下例中，只有最右侧第一位为 `1`，函数只返回第一个字符串 `foo`。

```sql
SELECT MAKE_SET(b'001','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'001','foo','bar','baz') |
    +------------------------------------+
    | foo                                |
    +------------------------------------+
    1 row in set (0.00 sec)

下例中，只有第二位为 `1`，函数只返回第二个字符串 `bar`。

```sql
SELECT MAKE_SET(b'010','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'010','foo','bar','baz') |
    +------------------------------------+
    | bar                                |
    +------------------------------------+
    1 row in set (0.00 sec)

下例中，只有第三位为 `1`，函数只返回第三个字符串 `baz`。

```sql
SELECT MAKE_SET(b'100','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'100','foo','bar','baz') |
    +------------------------------------+
    | baz                                |
    +------------------------------------+
    1 row in set (0.00 sec)

下例中，所有位均为 `1`，函数返回所有三个字符串，逗号分隔。

```sql
SELECT MAKE_SET(b'111','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'111','foo','bar','baz') |
    +------------------------------------+
    | foo,bar,baz                        |
    +------------------------------------+
    1 row in set (0.0002 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_mid"><code>MID()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-mid-code-mid-code-a}

`MID(str, pos[, len])` 函数返回从指定 `pos` 位置开始、长度为 `len` 的子串。

自 v8.4.0 起，TiDB 支持双参数变体 `MID(str, pos)`。如果未指定 `len`，该函数返回从指定 `pos` 位置到字符串末尾的所有字符。

如果任一参数为 `NULL`，函数返回 `NULL`。

示例：

下例中，`MID()` 返回输入字符串从第二个字符（`b`）开始，长度为 `3` 的子串。

```sql
SELECT MID('abcdef',2,3);
```

    +-------------------+
    | MID('abcdef',2,3) |
    +-------------------+
    | bcd               |
    +-------------------+
    1 row in set (0.00 sec)

下例中，`MID()` 返回输入字符串从第二个字符（`b`）开始到字符串末尾的子串。

```sql
SELECT MID('abcdef',2);
```

    +-------------------+
    | MID('abcdef',2)   |
    +-------------------+
    | bcdef             |
    +-------------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like"><code>NOT LIKE</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-comparison-functions-html-operator-not-like-code-not-like-code-a}

简单模式匹配的取反。

该函数执行 [`LIKE`](#like) 的相反操作。

示例：

下例中，`NOT LIKE` 返回 `0`（False），因为 `aaa` 匹配 `a%` 模式。

```sql
SELECT 'aaa' LIKE 'a%', 'aaa' NOT LIKE 'a%';
```

    +-----------------+---------------------+
    | 'aaa' LIKE 'a%' | 'aaa' NOT LIKE 'a%' |
    +-----------------+---------------------+
    |               1 |                   0 |
    +-----------------+---------------------+
    1 row in set (0.00 sec)

下例中，`NOT LIKE` 返回 `1`（True），因为 `aaa` 不匹配 `b%` 模式。

```sql
SELECT 'aaa' LIKE 'b%', 'aaa' NOT LIKE 'b%';
```

    +-----------------+---------------------+
    | 'aaa' LIKE 'b%' | 'aaa' NOT LIKE 'b%' |
    +-----------------+---------------------+
    |               0 |                   1 |
    +-----------------+---------------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp"><code>NOT REGEXP</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-operator-not-regexp-code-not-regexp-code-a}

[`REGEXP`](#regexp) 的取反。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct"><code>OCT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-oct-code-oct-code-a}

返回数字的 [八进制](https://en.wikipedia.org/wiki/Octal)（基数 8）表示的字符串。

示例：

下例使用 [递归公共表表达式（CTE）](/develop/dev-guide-use-common-table-expression.md#recursive-cte) 生成 0 到 20 的数字序列，然后用 `OCT()` 函数将每个数字转换为八进制表示。十进制 0 到 7 与八进制表示相同。十进制 8 到 15 分别对应八进制 10 到 17。

```sql
WITH RECURSIVE nr(n) AS (
    SELECT 0 AS n
    UNION ALL
    SELECT n+1 FROM nr WHERE n<20
)
SELECT n, OCT(n) FROM nr;
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

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_octet-length"><code>OCTET_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-octet-length-code-octet-length-code-a}

[`LENGTH()`](#length) 的同义词。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord"><code>ORD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ord-code-ord-code-a}

返回给定参数最左侧字符的字符编码。

该函数与 [`CHAR()`](#char) 类似，但方向相反。

示例：

以 `a` 和 `A` 为例，`ORD()` 对 `a` 返回 `97`，对 `A` 返回 `65`。

```sql
SELECT ORD('a'), ORD('A');
```

    +----------+----------+
    | ORD('a') | ORD('A') |
    +----------+----------+
    |       97 |       65 |
    +----------+----------+
    1 row in set (0.00 sec)

如果将 `ORD()` 得到的字符编码作为输入，可以用 `CHAR()` 函数还原原始字符。注意输出格式可能因 MySQL 客户端是否启用 `binary-as-hex` 选项而异。

```sql
SELECT CHAR(97), CHAR(65);
```

    +----------+----------+
    | CHAR(97) | CHAR(65) |
    +----------+----------+
    | a        | A        |
    +----------+----------+
    1 row in set (0.01 sec)

下例展示 `ORD()` 如何处理多字节字符。这里 `101` 和 `0x65` 都是 `e` 字符的 UTF-8 编码值，但格式不同。`50091` 和 `0xC3AB` 都表示 `ë` 字符的编码值。

```sql
SELECT ORD('e'), ORD('ë'), HEX('e'), HEX('ë');
```

    +----------+-----------+----------+-----------+
    | ORD('e') | ORD('ë')  | HEX('e') | HEX('ë')  |
    +----------+-----------+----------+-----------+
    |      101 |     50091 | 65       | C3AB      |
    +----------+-----------+----------+-----------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_position"><code>POSITION()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-position-code-position-code-a}

[`LOCATE()`](#locate) 的同义词。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote"><code>QUOTE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-quote-code-quote-code-a}

对参数进行转义，以便在 SQL 语句中使用。

如果参数为 `NULL`，函数返回 `NULL`。

示例：

如需直接显示结果而不是十六进制编码值，需要以 [`--skip-binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) 选项启动 MySQL 客户端。

下例显示 ASCII NULL 字符被转义为 `\0`，单引号字符 `'` 被转义为 `\'`：

```sql
SELECT QUOTE(0x002774657374);
```

    +-----------------------+
    | QUOTE(0x002774657374) |
    +-----------------------+
    | '\0\'test'            |
    +-----------------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp"><code>REGEXP</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-operator-regexp-code-regexp-code-a}

使用正则表达式进行模式匹配。

示例：

下例将多个字符串与两个正则表达式进行匹配。

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

    +----------+------------------+------------------------+
    | v        | starts with "Ti" | Length is 4 characters |
    +----------+------------------+------------------------+
    | TiDB     |                1 |                      1 |
    | Titanium |                1 |                      0 |
    | Tungsten |                0 |                      0 |
    | Rust     |                0 |                      1 |
    +----------+------------------+------------------------+
    4 rows in set (0.00 sec)

下例演示 `REGEXP` 不仅可用于 `SELECT` 子句，也可用于查询的 `WHERE` 子句。

```sql
SELECT
    v
FROM (
        SELECT 'TiDB' AS v
    ) AS vals
WHERE
    v REGEXP 'DB$';
```

    +------+
    | v    |
    +------+
    | TiDB |
    +------+
    1 row in set (0.01 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-instr"><code>REGEXP_INSTR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-function-regexp-instr-code-regexp-instr-code-a}

返回与正则表达式匹配的子串的起始索引（与 MySQL 部分兼容。详情参见 [正则表达式与 MySQL 的兼容性](#regular-expression-compatibility-with-mysql)）。

`REGEXP_INSTR(str, regexp, [start, [match, [ret, [match_type]]]])` 函数在正则表达式（`regexp`）匹配字符串（`str`）时，返回匹配的位置。

如果 `str` 或 `regexp` 为 `NULL`，则函数返回 `NULL`。

示例：

下例中，`^.b.$` 匹配 `abc`。

```sql
SELECT REGEXP_INSTR('abc','^.b.$');
```

    +-----------------------------+
    | REGEXP_INSTR('abc','^.b.$') |
    +-----------------------------+
    |                           1 |
    +-----------------------------+
    1 row in set (0.00 sec)

下例使用第三个参数指定字符串中不同的起始位置查找匹配。

```sql
SELECT REGEXP_INSTR('abcabc','a');
```

    +----------------------------+
    | REGEXP_INSTR('abcabc','a') |
    +----------------------------+
    |                          1 |
    +----------------------------+
    1 row in set (0.00 sec)

```sql
SELECT REGEXP_INSTR('abcabc','a',2);
```

    +------------------------------+
    | REGEXP_INSTR('abcabc','a',2) |
    +------------------------------+
    |                            4 |
    +------------------------------+
    1 row in set (0.00 sec)

下例使用第四个参数查找第二个匹配项。

```sql
SELECT REGEXP_INSTR('abcabc','a',1,2);
```

    +--------------------------------+
    | REGEXP_INSTR('abcabc','a',1,2) |
    +--------------------------------+
    |                              4 |
    +--------------------------------+
    1 row in set (0.00 sec)

下例使用第五个参数返回匹配项之后的位置，而不是匹配项本身的位置。

```sql
SELECT REGEXP_INSTR('abcabc','a',1,1,1);
```

    +----------------------------------+
    | REGEXP_INSTR('abcabc','a',1,1,1) |
    +----------------------------------+
    |                                2 |
    +----------------------------------+
    1 row in set (0.00 sec)

下例使用第六个参数添加 `i` 标志，实现不区分大小写匹配。关于正则表达式 `match_type` 的更多信息，参见 [`match_type` 兼容性](#match_type-compatibility)。

```sql
SELECT REGEXP_INSTR('abcabc','A',1,1,0,'');
```

    +-------------------------------------+
    | REGEXP_INSTR('abcabc','A',1,1,0,'') |
    +-------------------------------------+
    |                                   0 |
    +-------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT REGEXP_INSTR('abcabc','A',1,1,0,'i');
```

    +--------------------------------------+
    | REGEXP_INSTR('abcabc','A',1,1,0,'i') |
    +--------------------------------------+
    |                                    1 |
    +--------------------------------------+
    1 row in set (0.00 sec)

除了 `match_type`，[排序规则](/character-set-and-collation.md) 也会影响匹配。下例分别使用区分大小写和不区分大小写的排序规则进行演示。

```sql
SELECT REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_general_ci);
```

    +-------------------------------------------------------+
    | REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_general_ci) |
    +-------------------------------------------------------+
    |                                                     1 |
    +-------------------------------------------------------+
    1 row in set (0.01 sec)

```sql
SELECT REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_bin);
```

    +------------------------------------------------+
    | REGEXP_INSTR('abcabc','A' COLLATE utf8mb4_bin) |
    +------------------------------------------------+
    |                                              0 |
    +------------------------------------------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-like"><code>REGEXP_LIKE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-function-regexp-like-code-regexp-like-code-a}

判断字符串是否匹配正则表达式（与 MySQL 部分兼容。详情参见 [正则表达式与 MySQL 的兼容性](#regular-expression-compatibility-with-mysql)）。

`REGEXP_LIKE(str, regex, [match_type])` 函数用于测试正则表达式是否匹配字符串。可选的 `match_type` 用于改变匹配行为。

示例：

下例显示 `^a` 匹配 `abc`。

```sql
SELECT REGEXP_LIKE('abc','^a');
```

    +-------------------------+
    | REGEXP_LIKE('abc','^a') |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.00 sec)

下例显示 `^A` 不匹配 `abc`。

```sql
SELECT REGEXP_LIKE('abc','^A');
```

    +-------------------------+
    | REGEXP_LIKE('abc','^A') |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)

下例将 `^A` 匹配 `abc`，由于加了 `i` 标志，实现了不区分大小写匹配。关于正则表达式 `match_type` 的更多信息，参见 [`match_type` 兼容性](#match_type-compatibility)。

```sql
SELECT REGEXP_LIKE('abc','^A','i');
```

    +-----------------------------+
    | REGEXP_LIKE('abc','^A','i') |
    +-----------------------------+
    |                           1 |
    +-----------------------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-replace"><code>REGEXP_REPLACE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-function-regexp-replace-code-regexp-replace-code-a}

替换匹配正则表达式的子串（与 MySQL 部分兼容。详情参见 [正则表达式与 MySQL 的兼容性](#regular-expression-compatibility-with-mysql)）。

`REGEXP_REPLACE(str, regexp, replace, [start, [match, [match_type]]])` 函数可用于基于正则表达式替换字符串。

示例：

下例将两个 o 替换为 `i`。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i');
```

    +--------------------------------------+
    | REGEXP_REPLACE('TooDB', 'o{2}', 'i') |
    +--------------------------------------+
    | TiDB                                 |
    +--------------------------------------+
    1 row in set (0.00 sec)

下例从第三个字符开始匹配，导致正则表达式不匹配，不进行替换。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i',3);
```

    +----------------------------------------+
    | REGEXP_REPLACE('TooDB', 'o{2}', 'i',3) |
    +----------------------------------------+
    | TooDB                                  |
    +----------------------------------------+
    1 row in set (0.00 sec)

下例用第五个参数设置替换第一个或第二个匹配项。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o', 'i',1,1);
```

    +---------------------------------------+
    | REGEXP_REPLACE('TooDB', 'o', 'i',1,1) |
    +---------------------------------------+
    | TioDB                                 |
    +---------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT REGEXP_REPLACE('TooDB', 'o', 'i',1,2);
```

    +---------------------------------------+
    | REGEXP_REPLACE('TooDB', 'o', 'i',1,2) |
    +---------------------------------------+
    | ToiDB                                 |
    +---------------------------------------+
    1 row in set (0.00 sec)

下例用第六个参数设置 `match_type`，实现不区分大小写匹配。关于正则表达式 `match_type` 的更多信息，参见 [`match_type` 兼容性](#match_type-compatibility)。

```sql
SELECT REGEXP_REPLACE('TooDB', 'O{2}','i',1,1);
```

    +-----------------------------------------+
    | REGEXP_REPLACE('TooDB', 'O{2}','i',1,1) |
    +-----------------------------------------+
    | TooDB                                   |
    +-----------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT REGEXP_REPLACE('TooDB', 'O{2}','i',1,1,'i');
```

    +---------------------------------------------+
    | REGEXP_REPLACE('TooDB', 'O{2}','i',1,1,'i') |
    +---------------------------------------------+
    | TiDB                                        |
    +---------------------------------------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-substr"><code>REGEXP_SUBSTR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-function-regexp-substr-code-regexp-substr-code-a}

返回匹配正则表达式的子串（与 MySQL 部分兼容。详情参见 [正则表达式与 MySQL 的兼容性](#regular-expression-compatibility-with-mysql)）。

`REGEXP_SUBSTR(str, regexp, [start, [match, [match_type]]])` 函数用于基于正则表达式获取子串。

下例使用正则表达式 `Ti.{2}` 获取字符串 `This is TiDB` 中的 `TiDB` 子串。

```sql
SELECT REGEXP_SUBSTR('This is TiDB','Ti.{2}');
```

    +----------------------------------------+
    | REGEXP_SUBSTR('This is TiDB','Ti.{2}') |
    +----------------------------------------+
    | TiDB                                   |
    +----------------------------------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_repeat"><code>REPEAT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-repeat-code-repeat-code-a}

将字符串重复指定次数。

示例：

下例使用 [递归公共表表达式（CTE）](/develop/dev-guide-use-common-table-expression.md#recursive-cte) 生成 1 到 20 的数字序列。对每个数字，将字符 `x` 重复该数字次数。

```sql
WITH RECURSIVE nr(n) AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n+1 FROM nr WHERE n<20
)
SELECT n, REPEAT('x',n) FROM nr;
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

下例演示 `REPEAT()` 可对多字符字符串操作。

```sql
SELECT REPEAT('ha',3);
```

    +----------------+
    | REPEAT('ha',3) |
    +----------------+
    | hahaha         |
    +----------------+
    1 row in set (0.00 sec)

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_replace"><code>REPLACE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-replace-code-replace-code-a}

替换指定字符串的所有出现。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse"><code>REVERSE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-reverse-code-reverse-code-a}

反转字符串中的字符顺序。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right"><code>RIGHT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-right-code-right-code-a}

返回字符串最右侧指定数量的字符。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp"><code>RLIKE</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-operator-regexp-code-rlike-code-a}

[`REGEXP`](#regexp) 的同义词。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rpad"><code>RPAD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-rpad-code-rpad-code-a}

在字符串右侧追加指定次数的字符串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rtrim"><code>RTRIM()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-rtrim-code-rtrim-code-a}

去除字符串末尾的空格。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_space"><code>SPACE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-space-code-space-code-a}

返回指定数量空格组成的字符串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp"><code>STRCMP()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-comparison-functions-html-function-strcmp-code-strcmp-code-a}

比较两个字符串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substr"><code>SUBSTR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substr-code-substr-code-a}

返回指定的子串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring"><code>SUBSTRING()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substring-code-substring-code-a}

返回指定的子串。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring-index"><code>SUBSTRING_INDEX()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substring-index-code-substring-index-code-a}

`SUBSTRING_INDEX()` 函数用于根据指定分隔符和计数，从字符串中提取子串。该函数在处理以特定分隔符分隔的数据时非常有用，如解析 CSV 数据或处理日志文件。

语法：

```sql
SUBSTRING_INDEX(str, delim, count)
```

-   `str`：要处理的字符串。
-   `delim`：字符串中的分隔符，区分大小写。
-   `count`：分隔符出现的次数。
    -   如果 `count` 为正数，函数返回从字符串左侧起分隔符出现 `count` 次之前的子串。
    -   如果 `count` 为负数，函数返回从字符串右侧起分隔符出现 `count` 次之后的子串。
    -   如果 `count` 为 `0`，函数返回空字符串。

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

`TO_BASE64()` 函数用于将给定参数转换为 base-64 编码形式的字符串，并根据当前连接的字符集和排序规则返回结果。base-64 编码字符串可通过 [`FROM_BASE64()`](#from_base64) 函数解码。

语法：

```sql
TO_BASE64(str)
```

-   如果参数不是字符串，函数会先将其转换为字符串再进行 base-64 编码。
-   如果参数为 `NULL`，函数返回 `NULL`。

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

将字符串中所有出现的字符替换为其他字符。与 Oracle 不同，空字符串不会被视为 `NULL`。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_trim"><code>TRIM()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-trim-code-trim-code-a}

去除字符串首尾的空格。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ucase"><code>UCASE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ucase-code-ucase-code-a}

`UCASE()` 函数用于将字符串转换为大写字母。该函数等价于 `UPPER()` 函数。

> **Note:**
>
> 当字符串为 null 时，`UCASE()` 函数返回 `NULL`。

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

`UNHEX()` 函数执行 `HEX()` 函数的逆操作。它将参数中的每对字符视为一个十六进制数，并将其转换为该数值对应的字符，以二进制字符串形式返回结果。

> **Note:**
>
> -   参数必须是有效的十六进制值，仅包含 `0`–`9`、`A`–`F` 或 `a`–`f`。如果参数为 `NULL` 或超出该范围，函数返回 `NULL`。
> -   在 MySQL 客户端中，交互模式下默认启用 [`--binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex) 选项，会将未知字符集的数据以 [十六进制字面量](https://dev.mysql.com/doc/refman/8.0/en/hexadecimal-literals.html) 显示。你可以使用 `--skip-binary-as-hex` 选项关闭该行为。

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

`UPPER()` 函数用于将字符串转换为大写字母。该函数等价于 `UCASE()` 函数。

> **Note:**
>
> 当字符串为 null 时，`UPPER()` 函数返回 `NULL`。

示例：

```sql
SELECT UPPER('bigdata') AS result_upper, UPPER(null) AS result_null;
```

输出：

```sql
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_weight-string"><code>WEIGHT_STRING()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-weight-string-code-weight-string-code-a}

`WEIGHT_STRING()` 函数返回输入字符串的权重字符串（二进制字符），主要用于多字符集场景下的排序和比较操作。如果参数为 `NULL`，则返回 `NULL`。语法如下：

```sql
WEIGHT_STRING(str [AS {CHAR|BINARY}(N)])
```

-   `str`：输入的字符串表达式。如果是非二进制字符串，如 `CHAR`、`VARCHAR` 或 `TEXT` 值，返回值包含字符串的排序权重。如果是二进制字符串，如 `BINARY`、`VARBINARY` 或 `BLOB` 值，返回值与输入相同。

-   `AS {CHAR|BINARY}(N)`：可选参数，用于指定输出的类型和长度。`CHAR` 表示字符类型，`BINARY` 表示二进制类型。`N` 指定输出长度，需为大于等于 1 的整数。

> **Note:**
>
> 如果 `N` 小于字符串长度，则字符串被截断。如果 `N` 大于字符串长度，`AS CHAR(N)` 会用空格补齐到指定长度，`AS BINARY(N)` 会用 `0x00` 补齐到指定长度。

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

以下章节介绍 TiDB 与 MySQL 在正则表达式方面的兼容性，包括 `REGEXP_INSTR()`、`REGEXP_LIKE()`、`REGEXP_REPLACE()` 和 `REGEXP_SUBSTR()`。

### 语法兼容性 {#syntax-compatibility}

MySQL 使用 International Components for Unicode (ICU) 实现正则表达式，TiDB 使用 RE2。你可以参考 [ICU 文档](https://unicode-org.github.io/icu/userguide/) 和 [RE2 语法](https://github.com/google/re2/wiki/Syntax) 了解两者的语法差异。

### <code>match_type</code> 兼容性 {#code-match-type-code-compatibility}

TiDB 与 MySQL 的 `match_type` 取值选项如下：

-   TiDB 支持的取值为 `"c"`、`"i"`、`"m"` 和 `"s"`，MySQL 支持的取值为 `"c"`、`"i"`、`"m"`、`"n"` 和 `"u"`。

-   TiDB 中的 `"s"` 对应 MySQL 的 `"n"`。在 TiDB 中设置 `"s"` 时，`.` 字符也会匹配换行符（`\n`）。

    例如，MySQL 中的 `SELECT REGEXP_LIKE(a, b, "n") FROM t1` 等价于 TiDB 中的 `SELECT REGEXP_LIKE(a, b, "s") FROM t1`。

-   TiDB 不支持 `"u"`，即 MySQL 中的 Unix-only 换行符。

| `match_type` | MySQL | TiDB | 描述                                   |
| :----------: | ----- | ---- | -------------------------------------- |
|       c      | Yes   | Yes  | 区分大小写匹配                         |
|       i      | Yes   | Yes  | 不区分大小写匹配                       |
|       m      | Yes   | Yes  | 多行模式                               |
|       s      | No    | Yes  | 匹配换行符，等价于 MySQL 的 `n`        |
|       n      | Yes   | No   | 匹配换行符，等价于 TiDB 的 `s`         |
|       u      | Yes   | No   | UNIX™ 换行符                           |

### 数据类型兼容性 {#data-type-compatibility}

TiDB 与 MySQL 在二进制字符串类型支持上的差异：

-   MySQL 自 8.0.22 起不支持在正则表达式函数中使用二进制字符串。详情参见 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/regexp.html)。但实际上，当所有参数或返回类型均为二进制字符串时，MySQL 的正则函数可以工作，否则会报错。
-   目前，TiDB 禁止在任何情况下使用二进制字符串，否则会报错。

### 其他兼容性 {#other-compatibility}

-   TiDB 在替换空字符串的行为与 MySQL 不同。以 `REGEXP_REPLACE("", "^$", "123")` 为例：

    -   MySQL 不会替换空字符串，结果为 `""`。
    -   TiDB 会替换空字符串，结果为 `"123"`。

-   TiDB 捕获组的关键字与 MySQL 不同。MySQL 使用 `$` 作为关键字，TiDB 使用 `\\` 作为关键字。此外，TiDB 仅支持编号为 `0` 到 `9` 的捕获组。

    例如，以下 SQL 语句在 TiDB 中返回 `ab`：

    ```sql
    SELECT REGEXP_REPLACE('abcd','(.*)(.{2})$','\\1') AS s;
    ```

### 已知问题 {#known-issues}

-   [GitHub Issue #37981](https://github.com/pingcap/tidb/issues/37981)
