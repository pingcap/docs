---
title: String Functions
summary: TiDB の文字列関数について学習します。
---

# 文字列関数 {#string-functions}

TiDB は、MySQL 8.0 で利用可能な[文字列関数](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html)ほとんどと、Oracle 21 で利用可能な[関数](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009)の一部をサポートしています。

<CustomContent platform="tidb">

Oracle と TiDB の関数と構文の比較については、 [Oracle と TiDB の機能と構文の比較](/oracle-functions-to-tidb.md)参照してください。

</CustomContent>

## サポートされている関数 {#supported-functions}

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ascii"><code>ASCII()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ascii-code-ascii-code-a}

`ASCII(str)`関数は、指定された引数の左端の文字のASCII値を取得するために使用されます。引数は文字列または数値のいずれかです。

-   引数が空でない場合、関数は左端の文字の ASCII 値を返します。
-   引数が空の文字列の場合、関数は`0`返します。
-   引数が`NULL`場合、関数は`NULL`返します。

> **注記：**
>
> `ASCII(str)` 、8 ビットの 2 進数 (1 バイト) を使用して表される文字に対してのみ機能します。

例：

```sql
SELECT ASCII('A'), ASCII('TiDB'), ASCII(23);
```

出力：

```sql
+------------+---------------+-----------+
| ASCII('A') | ASCII('TiDB') | ASCII(23) |
+------------+---------------+-----------+
|         65 |            84 |        50 |
+------------+---------------+-----------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bin"><code>BIN()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-bin-code-bin-code-a}

`BIN()`関数は、指定された引数をそのバイナリ値の文字列表現に変換します。引数は文字列または数値のいずれかです。

-   引数が正の数の場合、関数はそのバイナリ値の文字列表現を返します。
-   引数が負の数の場合、関数は引数の絶対値をそのバイナリ表現に変換し、バイナリ値の各ビットを反転（ `0`を`1`に、 `1`を`0`に変更）してから、反転した値に`1`加算します。
-   引数が数字のみを含む文字列の場合、関数はその数字に応じた結果を返します。例えば、 `"123"`と`123`結果は同じになります。
-   引数が文字列で、その最初の文字が数字ではない場合 ( `"q123"`など)、関数は`0`返します。
-   引数が数字と非数字を含む文字列の場合、関数は引数の先頭の連続する数字に基づいて結果を返します。例えば、 `"123q123"`と`123`結果は同じですが、 `BIN('123q123')`は`Truncated incorrect INTEGER value: '123q123'`ような警告が表示されます。
-   引数が`NULL`場合、関数は`NULL`返します。

例1:

```sql
SELECT BIN(123), BIN('123q123');
```

出力1:

```sql
+----------+----------------+
| BIN(123) | BIN('123q123') |
+----------+----------------+
| 1111011  | 1111011        |
+----------+----------------+
```

例2:

```sql
SELECT BIN(-7);
```

出力2:

```sql
+------------------------------------------------------------------+
| BIN(-7)                                                          |
+------------------------------------------------------------------+
| 1111111111111111111111111111111111111111111111111111111111111001 |
+------------------------------------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bit-length"><code>BIT_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-bit-length-code-bit-length-code-a}

`BIT_LENGTH()`関数は、指定された引数の長さをビット単位で返すために使用されます。

例:

```sql
SELECT BIT_LENGTH("TiDB");

+--------------------+
| BIT_LENGTH("TiDB") |
+--------------------+
|                 32 |
+--------------------+
```

1文字あたり8ビット×4文字＝32ビット

```sql
SELECT BIT_LENGTH("PingCAP 123");

+---------------------------+
| BIT_LENGTH("PingCAP 123") |
+---------------------------+
|                        88 |
+---------------------------+
```

1文字あたり8ビット（スペースは英数字ではないためカウントされます）×11文字 = 88ビット

```sql
SELECT CustomerName, BIT_LENGTH(CustomerName) AS BitLengthOfName FROM Customers;

+--------------------+-----------------+
| CustomerName       | BitLengthOfName |
+--------------------+-----------------+
| Albert Einstein    |             120 |
| Robert Oppenheimer |             144 |
+--------------------+-----------------+
```

> **注記：**
>
> 上記の例は、 `Customers`という名前のテーブルと、テーブル内に`CustomerName`名前の列を持つデータベースが存在するという前提で動作します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char"><code>CHAR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-char-code-char-code-a}

`CHAR()`関数は、特定のASCII値に対応する文字を取得するために使用されます。これは、特定の文字のASCII値を返す`ASCII()`の逆の操作を行います。複数の引数が指定された場合、この関数はすべての引数に対して処理を行い、それらを連結します。

例:

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

`CHAR()`関数は、標準の ASCII 範囲 ( `0` - `127` ) を超える ASCII 値の対応する文字を取得するためにも使用できます。

```sql
/*For extended ASCII: */

SELECT CHAR(128);

+------------+
|  CHAR(128) |
+------------+
|       0x80 |
+------------+
```

`CHAR()`関数は、Unicode 値に対応する文字値を取得することもできます。

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

`CHAR_LENGTH()`関数は、指定された引数内の文字の合計数を整数として取得するために使用されます。

例:

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

> **注記：**
>
> 上記の例は、 `Customers`という名前のテーブルと、テーブル内に`CustomerName`名前の列を持つデータベースが存在するという前提で動作します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_character-length"><code>CHARACTER_LENGTH()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-character-length-code-character-length-code-a}

関数`CHARACTER_LENGTH()`関数`CHAR_LENGTH()`と同じです。どちらの関数も同じ出力を生成するため、同義語として使用できます。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat"><code>CONCAT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-concat-code-concat-code-a}

`CONCAT()`関数は、1 つ以上の引数を 1 つの文字列に連結します。

構文：

```sql
CONCAT(str1,str2,...)
```

`str1, str2, ...`は連結される引数のリストです。各引数は文字列または数値です。

例：

```sql
SELECT CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE);
```

出力：

```sql
+---------------------------------------------+
| CONCAT('TiDB', ' ', 'Server', '-', 1, TRUE) |
+---------------------------------------------+
| TiDB Server-11                              |
+---------------------------------------------+
```

引数のいずれかが`NULL`の場合、 `CONCAT()` `NULL`返します。

例：

```sql
SELECT CONCAT('TiDB', NULL, 'Server');
```

出力：

```sql
+--------------------------------+
| CONCAT('TiDB', NULL, 'Server') |
+--------------------------------+
| NULL                           |
+--------------------------------+
```

`CONCAT()`関数に加えて、次の例のように文字列を隣接させて連結することもできます。ただし、この方法は数値型をサポートしていないことに注意してください。

```sql
SELECT 'Ti' 'DB' ' ' 'Server';
```

出力：

```sql
+-------------+
| Ti          |
+-------------+
| TiDB Server |
+-------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat-ws"><code>CONCAT_WS()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-concat-ws-code-concat-ws-code-a}

`CONCAT_WS()`関数は、セパレーター付きの[`CONCAT()`](#concat)の形式で、指定されたセパレーターで連結された文字列を返します。

構文：

```sql
CONCAT_WS(separator,str1,str2,...)
```

-   `separator` : 最初の引数はセパレーターであり、 `NULL`以外の残りの引数を連結します。
-   `str1, str2, ...` : 連結する引数のリスト。各引数は文字列または数値です。

例：

```sql
SELECT CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD');
```

出力：

```sql
+---------------------------------------------+
| CONCAT_WS(',', 'TiDB Server', 'TiKV', 'PD') |
+---------------------------------------------+
| TiDB Server,TiKV,PD                         |
+---------------------------------------------+
```

-   セパレータが空の文字列の場合、 `CONCAT_WS()` `CONCAT()`に相当し、残りの引数の連結された文字列を返します。

    例：

    ```sql
    SELECT CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD');
    ```

    出力：

    ```sql
    +--------------------------------------------+
    | CONCAT_WS('', 'TiDB Server', 'TiKV', 'PD') |
    +--------------------------------------------+
    | TiDB ServerTiKVPD                          |
    +--------------------------------------------+
    ```

-   区切り文字が`NULL`の場合、 `CONCAT_WS()` `NULL`返します。

    例：

    ```sql
    SELECT CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD');
    ```

    出力：

    ```sql
    +----------------------------------------------+
    | CONCAT_WS(NULL, 'TiDB Server', 'TiKV', 'PD') |
    +----------------------------------------------+
    | NULL                                         |
    +----------------------------------------------+
    ```

-   連結される引数の 1 つだけが`NULL`でない場合、 `CONCAT_WS()`その引数を返します。

    例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL);
    ```

    出力：

    ```sql
    +-------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL) |
    +-------------------------------------+
    | TiDB Server                         |
    +-------------------------------------+
    ```

-   連結する引数が`NULL`ある場合、 `CONCAT_WS()`これら`NULL`引数をスキップします。

    例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', NULL, 'PD');
    ```

    出力：

    ```sql
    +-------------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', NULL, 'PD') |
    +-------------------------------------------+
    | TiDB Server,PD                            |
    +-------------------------------------------+
    ```

-   連結する空の文字列がある場合、 `CONCAT_WS()`空の文字列をスキップしません。

    例：

    ```sql
    SELECT CONCAT_WS(',', 'TiDB Server', '', 'PD');
    ```

    出力：

    ```sql
    +-----------------------------------------+
    | CONCAT_WS(',', 'TiDB Server', '', 'PD') |
    +-----------------------------------------+
    | TiDB Server,,PD                         |
    +-----------------------------------------+
    ```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_elt"><code>ELT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-elt-code-elt-code-a}

`ELT()`関数はインデックス番号の要素を返します。

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

上記の例では、3 番目の要素である`'TiDB'`返します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set"><code>EXPORT_SET()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-export-set-code-export-set-code-a}

`EXPORT_SET()`関数は、指定された数（ `number_of_bits` ）の`on`または`off`の値（オプションで`separator`で区切られる）で構成される文字列を返します。これらの値は、 `bits`引数の対応するビットが`1`であるかどうかに基づいて決定されます。最初の値は`bits`の右端（最下位）ビットに対応します。

構文：

```sql
EXPORT_SET(bits, on, off, [separator[, number_of_bits]])
```

-   `bits` : ビット値を表す整数。
-   `on` : 対応するビットが`1`場合に返される文字列。
-   `off` : 対応するビットが`0`場合に返される文字列。
-   `separator` (オプション): 結果文字列の区切り文字。
-   `number_of_bits` （オプション）：処理するビット数。設定されていない場合は、デフォルトで`64` （最大ビット数）が使用され、 `bits`符号なし64ビット整数として扱われます。

例:

次の例では、 `number_of_bits`が`5`に設定され、 `|`で区切られた 5 つの値が生成されます。3 ビットしか指定されていないため、残りのビットは未設定とみなされます。したがって、 `number_of_bits` `101`または`00101`に設定しても同じ出力になります。

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

次の例では、 `bits`が`00001111`に、 `on`が`x`に、 `off` `_`に設定されます。これにより、関数は`0`ビットに対して`____` 、 `1`ビットに対して`xxxx`返します。したがって、 `00001111`ビットを右から左に処理すると、関数は`xxxx____`返します。

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

次の例では、 `bits`が`00001111`に、 `on`が`x`に、 `off` `_`に設定されます。これにより、関数は`1`ビットごとに`x` 、 `0`ビットごとに`_`返します。したがって、 `01010101`ビットを右から左に処理すると、関数は`x_x_x_x_`返します。

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

後続の引数の最初の引数のインデックス (位置) を返します。

次の例では、 `FIELD()`の最初の引数は`needle`であり、次のリストの 2 番目の引数と一致するため、関数は`2`返します。

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

2 番目の引数内の最初の引数のインデックス位置を返します。

この関数は、 [`SET`](/data-type-string.md#set-type)データ型でよく使用されます。

次の例では、 `Go`セット`COBOL,BASIC,Rust,Go,Java,Fortran`の 4 番目の要素なので、関数は`4`返します。

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

`FORMAT(X,D[,locale])`関数は、数値`X` `"#,###,###. ##"`と同様の形式にフォーマットし、小数点以下`D`桁に丸めて、結果を文字列として返すために使用されます。

引数:

-   `X` : 書式設定する数値。数値、数値文字列、または科学的記数法で表された数値を指定できます。
-   `D` : 返される値の小数点以下の桁数。この関数は、数値を小数点以下`X`桁から`D`桁に丸めます`X`の実際の小数点以下の桁数よりも`D`大きい場合、結果の長さに合わせて0が補われます。
-   `[locale]` : 小数点の区切り、千単位の区切り、および結果の数値の区切りに使用するロケール設定を指定します。有効なロケール値は、システム変数[`lc_time_names`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_lc_time_names)の有効な値と同じです。指定されていない場合、または地域設定が`NULL`場合、デフォルトで地域設定`'en_US'`使用されます。この引数は省略可能です。

動作:

-   最初の引数が文字列で、数値のみを含む場合、関数はその数値に基づいて結果を返します。例えば、 `FORMAT('12.34', 1)`と`FORMAT(12.34, 1)`同じ結果を返します。
-   最初の引数が科学的記数法（ `E/e`を使用）で表された数値の場合、関数はその数値に基づいて結果を返します。例えば、 `FORMAT('1E2', 3)` `100.000`返します。
-   最初の引数が数値以外の文字で始まる文字列の場合、関数は0と警告`(Code 1292)`返します。例えば、 `FORMAT('q12.36', 5)` `0.00000`返しますが、警告`Warning (Code 1292): Truncated incorrect DOUBLE value: 'q12.36'`も含まれます。
-   最初の引数が数値と非数値が混在する文字列の場合、関数は引数の先頭の連続する数値部分に基づいて結果を返しますが、警告`(Code 1292)`も表示されます。例えば、 `FORMAT('12.36q56.78', 1)` `FORMAT('12.36', 1)`と同じ数値結果を返しますが、警告`Warning (Code 1292): Truncated incorrect DOUBLE value: '12.36q56.78'`が表示されます。
-   2 番目の引数が 0 または負の数の場合、関数は小数部分を切り捨てて整数を返します。
-   引数のいずれかが`NULL`の場合、関数は`NULL`返します。

例:

次の例は、数値 12.36 をさまざまな小数点以下の桁にフォーマットする方法を示しています。

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

`FROM_BASE64()`関数は、 [ベース64](https://datatracker.ietf.org/doc/html/rfc4648)エンコードされた文字列をデコードし、デコードされた結果を 16 進形式で返すために使用されます。

-   この関数は、デコードする Base64 でエンコードされた文字列という単一の引数を受け入れます。
-   引数が`NULL`であるか、有効な Base64 エンコードされた文字列でない場合、 `FROM_BASE64()`関数は`NULL`返します。

例:

次の例は、Base64でエンコードされた文字列`'SGVsbG8gVGlEQg=='`をデコードする方法を示しています。この文字列は、 [`TO_BASE64()`](#to_base64)関数を使用して`'Hello TiDB'`エンコードした結果です。

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

次の例は、Base64でエンコードされた数値`MTIzNDU2`デコードする方法を示しています。この文字列は、 [`TO_BASE64()`](#to_base64)関数を使用してエンコードされた`123456`結果です。

```sql
mysql> SELECT FROM_BASE64('MTIzNDU2');
+--------------------------------------------------+
| FROM_BASE64('MTIzNDU2')                          |
+--------------------------------------------------+
| 0x313233343536                                   |
+--------------------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_hex"><code>HEX()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-hex-code-hex-code-a}

`HEX()`関数は、指定された引数を16進数値の文字列表現に変換します。引数は文字列または数値のいずれかです。

-   引数が文字列の場合、 `HEX(str)` `str`の16進文字列表現を返します。この関数は、 `str`の各文字の各バイトを2桁の16進数に変換します。例えば、UTF-8またはASCII文字セットの文字`a` 、2進値では`00111101` 、16進表記では`61`として表されます。
-   引数が数値の場合、 `HEX(n)` `n`の16進文字列表現を返します。この関数は引数`n`数値`BIGINT`として扱い、これは`CONV(n, 10, 16)`使用するのと同じ意味になります。
-   引数が`NULL`場合、関数は`NULL`返します。

> **注記：**
>
> MySQLクライアントでは、インタラクティブモードではデフォルトで[`--binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex)オプションが有効になっているため、クライアントは不明な文字セットのデータを[16進数リテラル](https://dev.mysql.com/doc/refman/8.0/en/hexadecimal-literals.html)として表示します。この動作を無効にするには、 `--skip-binary-as-hex`オプションを使用します。

例（ `mysql --skip-binary-as-hex`件）:

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

`INSERT(str, pos, len, newstr)`関数は、 `str`内の部分文字列（位置`pos`から始まり、長さ`len`文字）を文字列`newstr`に置き換えるために使用されます。この関数はマルチバイトセーフです。

-   `pos` `str`の長さを超える場合、関数は変更せずに元の文字列`str`を返します。
-   `len`位置`pos`からの残りの長さ`str`を超える場合、関数は位置`pos`からの残りの文字列を置き換えます。
-   いずれかの引数が`NULL`場合、関数は`NULL`返します。

例:

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

`INSTR(str, substr)`関数は、 `str`における`substr`の最初の出現位置を取得します。各引数は文字列または数値のいずれかです。この関数は、引数が2つの[`LOCATE(substr, str)`](#locate)関数と同じですが、引数の順序が逆になっています。

> **注記：**
>
> `INSTR(str, substr)`の大文字と小文字の区別は、TiDB で使用される[照合](/character-set-and-collation.md)によって決まります。バイナリ照合順序（サフィックスが`_bin` ）では大文字と小文字が区別されますが、一般照合順序（サフィックスが`_general_ci`または`_ai_ci` ）では大文字と小文字は区別されません。

-   いずれかの引数が数値の場合、関数はその数値を文字列として扱います。
-   `substr` `str`に含まれない場合、この関数は`0`返します。そうでない場合は、 `str`における`substr`の最初の出現位置を返します。
-   いずれかの引数が`NULL`場合、関数は`NULL`返します。

例:

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

`LCASE(str)`関数は[`LOWER(str)`](#lower)の同義語で、指定された引数の小文字を返します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_left"><code>LEFT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-left-code-left-code-a}

`LEFT()`関数は、文字列の左側から指定された数の文字を返します。

構文：

```sql
LEFT(`str`, `len`)
```

-   `str` : 文字を抽出する元の文字列。2 `str`マルチバイト文字が含まれている場合、関数はそれを単一のコードポイントとしてカウントします。
-   `len` : 返される文字の長さ。
    -   `len`が 0 以下の場合、関数は空の文字列を返します。
    -   `len` `str`の長さ以上である場合、関数は元の`str`返します。
-   いずれかの引数が`NULL`場合、関数は`NULL`返します。

例:

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

`LENGTH()`関数は文字列の長さをバイト単位で返します。

`LENGTH()`マルチバイト文字を複数バイトとしてカウントし、 `CHAR_LENGTH()`マルチバイト文字を単一のコード ポイントとしてカウントします。

引数が`NULL`場合、関数は`NULL`返します。

例:

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

`LIKE`演算子は単純な文字列マッチングに使用されます。式`expr LIKE pat [ESCAPE 'escape_char']` `1` ( `TRUE` ) または`0` ( `FALSE` ) を返します。13 または`pat`いずれかが`expr` `NULL`場合、結果は`NULL`なります。

`LIKE`では次の 2 つのワイルドカード パラメータを使用できます。

-   `%` 、ゼロ文字を含む任意の数の文字に一致します。
-   `_` 1 つの文字と一致します。

次の例では、 `utf8mb4_bin`照合順序を使用しています。

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

デフォルトのエスケープ文字は`\`です。

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

`*`などの別のエスケープ文字を指定するには、 `ESCAPE`句を使用します。

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

`LIKE`演算子を使用して数値を一致させることができます。

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

`utf8mb4_unicode_ci`などの照合順序を明示的に指定するには、 `COLLATE`使用します。

```sql
SELECT '🍣🍺Sushi🍣🍺' COLLATE utf8mb4_unicode_ci LIKE '%SUSHI%' AS result;
+--------+
| result |
+--------+
|      1 |
+--------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_locate"><code>LOCATE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-locate-code-locate-code-a}

`LOCATE(substr, str[, pos])`関数は、文字列`str`内で指定された部分文字列`substr`が最初に出現する位置を取得するために使用されます。引数`pos`はオプションであり、検索の開始位置を指定します。

-   部分文字列`substr` `str`に存在しない場合、関数は`0`返します。
-   いずれかの引数が`NULL`場合、関数は`NULL`返します。
-   この関数はマルチバイトセーフであり、少なくとも 1 つの引数がバイナリ文字列である場合にのみ大文字と小文字を区別した検索を実行します。

次の例では、 `utf8mb4_bin`照合順序を使用しています。

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

次の例では、 `utf8mb4_unicode_ci`照合順序を使用しています。

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

次のマルチバイト文字列とバイナリ文字列の例では、 `utf8mb4_bin`照合順序が使用されています。

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

`LOWER(str)`関数は、指定された引数`str`のすべての文字を小文字に変換します。引数は文字列または数値のいずれかです。

-   引数が文字列の場合、関数は小文字で文字列を返します。
-   引数が数値の場合、関数は先頭のゼロを除いた数値を返します。
-   引数が`NULL`場合、関数は`NULL`返します。

例:

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

`LPAD(str, len, padstr)`関数は、指定された文字列`padstr`を左側に埋め込んで`len`文字の長さにした文字列引数を返します。

-   `len`文字列`str`の長さより短い場合、関数は文字列`str` `len`の長さに切り捨てます。
-   `len`が負の数の場合、関数は`NULL`返します。
-   いずれかの引数が`NULL`場合、関数は`NULL`返します。

例:

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

`LTRIM()`関数は、指定された文字列の先頭のスペースを削除します。

引数が`NULL`場合、この関数は`NULL`返します。

> **注記：**
>
> この関数は、スペース文字 (U+0020) のみを削除し、タブ (U+0009) やノーブレークスペース (U+00A0) などの他のスペースのような文字は削除しません。

例:

次の例では、 `LTRIM()`関数は`'    hello'`の先頭のスペースを削除し、 `hello`返します。

```sql
SELECT LTRIM('    hello');
```

    +--------------------+
    | LTRIM('    hello') |
    +--------------------+
    | hello              |
    +--------------------+
    1 row in set (0.00 sec)

次の例では、 [`CONCAT()`](#concat)を使って`LTRIM('    hello')`の結果を`«`と`»`で囲んでいます。この書式設定により、先頭のスペースがすべて削除されていることが少しわかりやすくなります。

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

`MAKE_SET()`関数は、 `bits`引数の対応するビットが`1`に設定されているかどうかに基づいて、コンマで区切られた文字列のセットを返します。

構文：

```sql
MAKE_SET(bits, str1, str2, ...)
```

-   `bits` : 結果セットに含める後続の文字列引数を制御します。2 `bits` `NULL`に設定されている場合、関数は`NULL`返します。
-   `str1, str2, ...` : 文字列のリスト。各文字列は、引数`bits`右から左へのビットに対応します。4 `str1`右から最初のビット、 `str2`右から2番目のビットに対応し、以下同様です。対応するビットが`1`場合、文字列は結果に含まれます。それ以外の場合は含まれません。

例:

次の例では、引数`bits`のすべてのビットが`0`に設定されているため、関数は結果に後続の文字列を含めず、空の文字列を返します。

```sql
SELECT MAKE_SET(b'000','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'000','foo','bar','baz') |
    +------------------------------------+
    |                                    |
    +------------------------------------+
    1 row in set (0.00 sec)

次の例では、右から最初のビットのみが`1`あるため、関数は最初の文字列`foo`のみを返します。

```sql
SELECT MAKE_SET(b'001','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'001','foo','bar','baz') |
    +------------------------------------+
    | foo                                |
    +------------------------------------+
    1 row in set (0.00 sec)

次の例では、右から 2 番目のビットのみが`1`であるため、関数は 2 番目の文字列`bar`のみを返します。

```sql
SELECT MAKE_SET(b'010','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'010','foo','bar','baz') |
    +------------------------------------+
    | bar                                |
    +------------------------------------+
    1 row in set (0.00 sec)

次の例では、右から 3 番目のビットのみが`1`であるため、関数は 3 番目の文字列`baz`のみを返します。

```sql
SELECT MAKE_SET(b'100','foo','bar','baz');
```

    +------------------------------------+
    | MAKE_SET(b'100','foo','bar','baz') |
    +------------------------------------+
    | baz                                |
    +------------------------------------+
    1 row in set (0.00 sec)

次の例では、すべてのビットが`1`あるため、関数は 3 つの文字列すべてをコンマ区切りの結果セットで返します。

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

`MID(str, pos[, len])`関数は、指定された`pos`位置から始まり、長さが`len`部分文字列を返します。

TiDB v8.4.0以降、2つの引数を持つバリアント`MID(str, pos)`がサポートされます。3 `len`指定されていない場合、この関数は指定された`pos`の位置から文字列の末尾までの残りのすべての文字を返します。

引数のいずれかが`NULL`の場合、関数は`NULL`返します。

例:

次の例では、 `MID()`入力文字列の 2 番目の文字 ( `b` ) から始まる`3`文字の長さの部分文字列を返します。

```sql
SELECT MID('abcdef',2,3);
```

    +-------------------+
    | MID('abcdef',2,3) |
    +-------------------+
    | bcd               |
    +-------------------+
    1 row in set (0.00 sec)

次の例では、 `MID()`入力文字列の 2 番目の文字 ( `b` ) から文字列の末尾までの部分文字列を返します。

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

単純なパターン マッチングの否定。

この関数は[`LIKE`](#like)の逆演算を実行します。

例:

次の例では、 `aaa` `a%`パターンと一致するため、 `NOT LIKE` `0` (False) を返します。

```sql
SELECT 'aaa' LIKE 'a%', 'aaa' NOT LIKE 'a%';
```

    +-----------------+---------------------+
    | 'aaa' LIKE 'a%' | 'aaa' NOT LIKE 'a%' |
    +-----------------+---------------------+
    |               1 |                   0 |
    +-----------------+---------------------+
    1 row in set (0.00 sec)

次の例では、 `aaa` `b%`パターンと一致しないため、 `NOT LIKE` `1` (True) を返します。

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

[`REGEXP`](#regexp)の否定。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct"><code>OCT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-oct-code-oct-code-a}

数値の[8進数](https://en.wikipedia.org/wiki/Octal) (基数 8) 表現を含む文字列を返します。

例:

次の例では、 [再帰共通テーブル式（CTE）](/develop/dev-guide-use-common-table-expression.md#recursive-cte)を使って 0 から 20 までの数値のシーケンスを生成し、関数`OCT()`を使用して各数値を 8 進数表現に変換します。0 から 7 までの 10 進数値は 8 進数でも同じ表現になります。8 から 15 までの 10 進数値は、10 から 17 までの 8 進数値に対応します。

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

[`LENGTH()`](#length)の同義語。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord"><code>ORD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ord-code-ord-code-a}

指定された引数の左端の文字の文字コードを返します。

この関数は[`CHAR()`](#char)と似ていますが、動作は逆になります。

例:

`a`と`A`例にとると、 `ORD()` `a`に対して`97`返し、 `A`に対して`65`を返します。

```sql
SELECT ORD('a'), ORD('A');
```

    +----------+----------+
    | ORD('a') | ORD('A') |
    +----------+----------+
    |       97 |       65 |
    +----------+----------+
    1 row in set (0.00 sec)

`ORD()`で取得した文字コードを入力として受け取ると、 `CHAR()`関数を使用して元の文字を復元できます。出力形式は、MySQLクライアントで`binary-as-hex`オプションが有効になっているかどうかによって異なる場合がありますのでご注意ください。

```sql
SELECT CHAR(97), CHAR(65);
```

    +----------+----------+
    | CHAR(97) | CHAR(65) |
    +----------+----------+
    | a        | A        |
    +----------+----------+
    1 row in set (0.01 sec)

次の例は、 `ORD()`マルチバイト文字をどのように処理するかを示しています。ここで、 `101`と`0x65`どちらも`e`番目の文字の UTF-8 エンコードされた値ですが、形式が異なります。また、 `50091`と`0xC3AB`どちらも`ë`番目の文字の同じ値です。

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

[`LOCATE()`](#locate)の同義語。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote"><code>QUOTE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-quote-code-quote-code-a}

SQL ステートメントで使用するために引数をエスケープします。

引数が`NULL`場合、関数は`NULL`返します。

例：

16 進数でエンコードされた値を表示する代わりに結果を直接表示するには、MySQL クライアントを[`--skip-binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex)オプションで起動する必要があります。

次の例では、ASCII NULL 文字が`\0`としてエスケープされ、一重引用符文字`'` `\'`としてエスケープされていることを示しています。

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

正規表現を使用したパターン マッチング。

例:

この例では、いくつかの文字列が 2 つの正規表現と照合されます。

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

次の例は、 `REGEXP` `SELECT`節に限定されないことを示しています。例えば、クエリの`WHERE`節でも使用できます。

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

正規表現に一致する部分文字列の開始インデックスを返します（MySQLと部分的に互換性があります。詳細については[MySQLとの正規表現の互換性](#regular-expression-compatibility-with-mysql)参照してください）。

`REGEXP_INSTR(str, regexp, [start, [match, [ret, [match_type]]]])`関数は正規表現（ `regexp` ）が文字列（ `str` ）と一致する場合、一致した位置を返します。

`str`または`regexp`いずれかが`NULL`の場合、関数は`NULL`返します。

例:

以下の例では、 `^.b.$` `abc`一致していることがわかります。

```sql
SELECT REGEXP_INSTR('abc','^.b.$');
```

    +-----------------------------+
    | REGEXP_INSTR('abc','^.b.$') |
    +-----------------------------+
    |                           1 |
    +-----------------------------+
    1 row in set (0.00 sec)

次の例では、3 番目の引数を使用して、文字列内の異なる開始位置との一致を検索します。

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

次の例では、4 番目の引数を使用して 2 番目の一致を検索します。

```sql
SELECT REGEXP_INSTR('abcabc','a',1,2);
```

    +--------------------------------+
    | REGEXP_INSTR('abcabc','a',1,2) |
    +--------------------------------+
    |                              4 |
    +--------------------------------+
    1 row in set (0.00 sec)

次の例では、5 番目の引数を使用して、一致の値ではなく、一致*後の*値を返します。

```sql
SELECT REGEXP_INSTR('abcabc','a',1,1,1);
```

    +----------------------------------+
    | REGEXP_INSTR('abcabc','a',1,1,1) |
    +----------------------------------+
    |                                2 |
    +----------------------------------+
    1 row in set (0.00 sec)

次の例では、6番目の引数にフラグ`i`を追加して、大文字と小文字を区別しない一致を取得しています。正規表現`match_type`詳細については、 [`match_type`互換性](#match_type-compatibility)参照してください。

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

`match_type`に加えて、 [照合順序](/character-set-and-collation.md)もマッチングに影響します。次の例では、大文字と小文字を区別する照合と大文字と小文字を区別しない照合順序を使用して、これを示しています。

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

文字列が正規表現に一致するかどうか（MySQLと部分的に互換性があります。詳しくは[MySQLとの正規表現の互換性](#regular-expression-compatibility-with-mysql)参照してください）。

`REGEXP_LIKE(str, regex, [match_type])`関数は、正規表現が文字列に一致するかどうかをテストするために使用されます。オプションで`match_type`を使用して、一致の動作を変更することもできます。

例:

次の例は、 `^a` `abc`一致することを示しています。

```sql
SELECT REGEXP_LIKE('abc','^a');
```

    +-------------------------+
    | REGEXP_LIKE('abc','^a') |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.00 sec)

次の例は、 `^A` `abc`一致しないことを示しています。

```sql
SELECT REGEXP_LIKE('abc','^A');
```

    +-------------------------+
    | REGEXP_LIKE('abc','^A') |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)

この例では、 `^A` `abc`に一致しますが、これは大文字と小文字を区別しない一致を有効にする`i`フラグによって一致します。正規表現`match_type`詳細については、 [`match_type`互換性](#match_type-compatibility)参照してください。

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

正規表現に一致する部分文字列を置換します（MySQLと部分的に互換性があります。詳しくは[MySQLとの正規表現の互換性](#regular-expression-compatibility-with-mysql)参照してください）。

`REGEXP_REPLACE(str, regexp, replace, [start, [match, [match_type]]])`関数は、正規表現に基づいて文字列を置換するために使用できます。

例:

次の例では、 2 つの o が`i`に置き換えられます。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i');
```

    +--------------------------------------+
    | REGEXP_REPLACE('TooDB', 'o{2}', 'i') |
    +--------------------------------------+
    | TiDB                                 |
    +--------------------------------------+
    1 row in set (0.00 sec)

次の例では、3 番目の文字から一致が開始され、正規表現は一致せず、置換も行われません。

```sql
SELECT REGEXP_REPLACE('TooDB', 'o{2}', 'i',3);
```

    +----------------------------------------+
    | REGEXP_REPLACE('TooDB', 'o{2}', 'i',3) |
    +----------------------------------------+
    | TooDB                                  |
    +----------------------------------------+
    1 row in set (0.00 sec)

次の例では、5 番目の引数を使用して、置換に最初の一致を使用するか、2 番目の一致を使用するかを設定します。

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

次の例では、6番目の引数に`match_type`設定して大文字と小文字を区別しない一致を指定しています。正規表現`match_type`詳細については、 [`match_type`互換性](#match_type-compatibility)参照してください。

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

正規表現に一致する部分文字列を返します（MySQLと部分的に互換性があります。詳しくは[MySQLとの正規表現の互換性](#regular-expression-compatibility-with-mysql)参照してください）。

`REGEXP_SUBSTR(str, regexp, [start, [match, [match_type]]])`関数は、正規表現に基づいて部分文字列を取得するために使用されます。

次の例では、正規表現`Ti.{2}`使用して、文字列`This is TiDB`のサブ文字列`TiDB`を取得します。

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

文字列を指定された回数繰り返します。

例:

次の例では、 [再帰共通テーブル式（CTE）](/develop/dev-guide-use-common-table-expression.md#recursive-cte)を使って1から20までの数字のシーケンスを生成します。シーケンス内の各数字に対して、文字`x`その数字と同じ回数繰り返されます。

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

次の例は、 `REPEAT()`複数の文字で構成される文字列に対して操作できることを示しています。

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

指定された文字列の出現を置き換えます。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse"><code>REVERSE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-reverse-code-reverse-code-a}

文字列内の文字を逆にします。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right"><code>RIGHT()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-right-code-right-code-a}

指定された右端の文字数を返します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp"><code>RLIKE</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-regexp-html-operator-regexp-code-rlike-code-a}

[`REGEXP`](#regexp)の同義語。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rpad"><code>RPAD()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-rpad-code-rpad-code-a}

指定された回数だけ文字列を追加します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rtrim"><code>RTRIM()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-rtrim-code-rtrim-code-a}

末尾のスペースを削除します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_space"><code>SPACE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-space-code-space-code-a}

指定された数のスペースを含む文字列を返します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp"><code>STRCMP()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-comparison-functions-html-function-strcmp-code-strcmp-code-a}

2 つの文字列を比較します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substr"><code>SUBSTR()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substr-code-substr-code-a}

指定されたとおりに部分文字列を返します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring"><code>SUBSTRING()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substring-code-substring-code-a}

指定されたとおりに部分文字列を返します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring-index"><code>SUBSTRING_INDEX()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-substring-index-code-substring-index-code-a}

`SUBSTRING_INDEX()`関数は、指定された区切り文字とカウントに基づいて文字列から部分文字列を抽出するために使用されます。この関数は、CSVデータの解析やログファイルの処理など、特定の区切り文字で区切られたデータを扱う場合に特に便利です。

構文：

```sql
SUBSTRING_INDEX(str, delim, count)
```

-   `str` : 処理する文字列を指定します。
-   `delim` : 文字列内の区切り文字を指定します。大文字と小文字が区別されます。
-   `count` : 区切り文字の出現回数を指定します。
    -   `count`が正の数の場合、関数は区切り文字の`count`目の出現の前の部分文字列 (文字列の左から数えて) を返します。
    -   `count`が負の数の場合、関数は区切り文字の`count`目の出現後 (文字列の右から数えて) の部分文字列を返します。
    -   `count`が`0`場合、関数は空の文字列を返します。

例1:

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', 2);
```

出力1:

```sql
+-----------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', 2) |
+-----------------------------------------+
| www.tidbcloud                                |
+-----------------------------------------+
```

例2:

```sql
SELECT SUBSTRING_INDEX('www.tidbcloud.com', '.', -1);
```

出力2:

```sql
+------------------------------------------+
| SUBSTRING_INDEX('www.tidbcloud.com', '.', -1) |
+------------------------------------------+
| com                                      |
+------------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_to-base64"><code>TO_BASE64()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-to-base64-code-to-base64-code-a}

`TO_BASE64()`関数は、指定された引数をBase64エンコードされた文字列に変換し、現在の接続の文字セットと照合順序に従って結果を返します。Base64エンコードされた文字列は、 [`FROM_BASE64()`](#from_base64)関数を使用してデコードできます。

構文：

```sql
TO_BASE64(str)
```

-   引数が文字列でない場合、関数はそれを base-64 エンコードする前に文字列に変換します。
-   引数が`NULL`場合、関数は`NULL`返します。

例1:

```sql
SELECT TO_BASE64('abc');
```

出力1:

```sql
+------------------+
| TO_BASE64('abc') |
+------------------+
| YWJj             |
+------------------+
```

例2:

```sql
SELECT TO_BASE64(6);
```

出力2:

```sql
+--------------+
| TO_BASE64(6) |
+--------------+
| Ng==         |
+--------------+
```

### <a href="https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRANSLATE.html#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690"><code>TRANSLATE()</code></a> {#a-href-https-docs-oracle-com-en-database-oracle-oracle-database-21-sqlrf-translate-html-guid-80f85acb-092c-4cc7-91f6-b3a585e3a690-code-translate-code-a}

文字列中のすべての文字を他の文字に置き換えます。Oracleのように空文字列を`NULL`として扱いません。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_trim"><code>TRIM()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-trim-code-trim-code-a}

先頭と末尾のスペースを削除します。

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ucase"><code>UCASE()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-ucase-code-ucase-code-a}

`UCASE()`関数は文字列を大文字に変換するために使用されます。この関数は`UPPER()`関数と同等です。

> **注記：**
>
> 文字列が null の場合、 `UCASE()`関数は`NULL`返します。

例：

```sql
SELECT UCASE('bigdata') AS result_upper, UCASE(null) AS result_null;
```

出力：

```sql
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_unhex"><code>UNHEX()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-unhex-code-unhex-code-a}

`UNHEX()`関数は`HEX()`関数の逆の操作を実行します。引数内の各文字ペアを16進数として扱い、その数値で表される文字に変換し、結果をバイナリ文字列として返します。

> **注記：**
>
> -   引数は`0` ～ `9` 、 `A` ～ `F` 、または`a` ～ `f`を含む有効な16進数値でなければなりません。引数が`NULL`またはこの範囲外の場合、関数は`NULL`返します。
> -   MySQLクライアントでは、インタラクティブモードではデフォルトで[`--binary-as-hex`](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html#option_mysql_binary-as-hex)オプションが有効になっているため、クライアントは不明な文字セットのデータを[16進数リテラル](https://dev.mysql.com/doc/refman/8.0/en/hexadecimal-literals.html)として表示します。この動作を無効にするには、 `--skip-binary-as-hex`オプションを使用します。

例：

```sql
SELECT UNHEX('54694442');
```

出力：

```sql
+--------------------------------------+
| UNHEX('54694442')                    |
+--------------------------------------+
| 0x54694442                           |
+--------------------------------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_upper"><code>UPPER()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-upper-code-upper-code-a}

`UPPER()`関数は文字列を大文字に変換するために使用されます。この関数は`UCASE()`関数と同等です。

> **注記：**
>
> 文字列が null の場合、 `UPPER()`関数は`NULL`返します。

例：

```sql
SELECT UPPER('bigdata') AS result_upper, UPPER(null) AS result_null;
```

出力：

```sql
+--------------+-------------+
| result_upper | result_null |
+--------------+-------------+
| BIGDATA      | NULL        |
+--------------+-------------+
```

### <a href="https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_weight-string"><code>WEIGHT_STRING()</code></a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-string-functions-html-function-weight-string-code-weight-string-code-a}

`WEIGHT_STRING()`関数は、入力文字列の重み文字列（バイナリ文字）を返します。これは主に、複数文字セットのシナリオにおけるソートや比較演算に使用されます。引数が`NULL`の場合、 `NULL`返します。構文は次のとおりです。

```sql
WEIGHT_STRING(str [AS {CHAR|BINARY}(N)])
```

-   `str` : 入力文字列式。2、4、6などの非バイナリ`VARCHAR` `CHAR`の場合、 `TEXT`値には文字列の照合順序重みが含まれ`VARBINARY` 。8、10、12などの`BINARY` `BLOB`列の場合、戻り値は入力値と同じになります。

-   `AS {CHAR|BINARY}(N)` : 出力のタイプと長さを指定するために使用されるオプションのパラメータ。2 `CHAR`文字データ型を表し、 `BINARY`バイナリ データ型を表します。6 `N`出力長を指定します。これは 1 以上の整数です。

> **注記：**
>
> `N`文字列の長さより短い場合、文字列は切り捨てられます。3 `N`文字列の長さを超える場合、 `AS CHAR(N)`指定された長さになるまで文字列にスペースを埋め込み、 `AS BINARY(N)`指定された長さになるまで文字列に`0x00`埋め込みます。

例：

```sql
SET NAMES 'utf8mb4';
SELECT HEX(WEIGHT_STRING('ab' AS CHAR(3))) AS char_result, HEX(WEIGHT_STRING('ab' AS BINARY(3))) AS binary_result;
```

出力：

```sql
+-------------+---------------+
| char_result | binary_result |
+-------------+---------------+
| 6162        | 616200        |
+-------------+---------------+
```

## サポートされていない関数 {#unsupported-functions}

-   `LOAD_FILE()`
-   `MATCH()`
-   `SOUNDEX()`

## MySQLとの正規表現の互換性 {#regular-expression-compatibility-with-mysql}

次のセクションでは、 `REGEXP_INSTR()` 、 `REGEXP_LIKE()` 、 `REGEXP_REPLACE()` 、 `REGEXP_SUBSTR()`を含む、MySQL との正規表現の互換性について説明します。

### 構文の互換性 {#syntax-compatibility}

MySQLはInternational Components for Unicode（ICU）を使用して正規表現を実装し、TiDBはRE2を使用しています。2つのライブラリの構文の違いについては、 [ICUの文書](https://unicode-org.github.io/icu/userguide/)と[RE2 構文](https://github.com/google/re2/wiki/Syntax)を参照してください。

### <code>match_type</code>互換性 {#code-match-type-code-compatibility}

TiDB と MySQL 間の`match_type`の値オプションは次のとおりです。

-   TiDB の値オプションは`"c"` 、 `"i"` 、 `"m"` 、 `"s"`であり、MySQL の値オプションは`"c"` 、 `"i"` 、 `"m"` 、 `"n"` 、 `"u"`です。

-   TiDBの`"s"` MySQLの`"n"`に相当します。TiDBで`"s"`設定されている場合、 `.`は行末文字（ `\n` ）にも一致します。

    たとえば、MySQL の`SELECT REGEXP_LIKE(a, b, "n") FROM t1` TiDB の`SELECT REGEXP_LIKE(a, b, "s") FROM t1`と同じです。

-   TiDB は、MySQL で Unix 専用の行末を意味する`"u"`サポートしていません。

| `match_type` | MySQL | TiDB | 説明                       |
| :----------: | ----- | ---- | ------------------------ |
|       c      | はい    | はい   | 大文字と小文字を区別する一致           |
|       私      | はい    | はい   | 大文字と小文字を区別しないマッチング       |
|     メートル     | はい    | はい   | 複数行モード                   |
|       s      | いいえ   | はい   | 改行に一致します。MySQLの`n`と同じです。 |
|       n      | はい    | いいえ  | 改行に一致します。TiDB の`s`と同じです。 |
|      あなた     | はい    | いいえ  | UNIX™ の行末                |

### データ型の互換性 {#data-type-compatibility}

バイナリ文字列型に対する TiDB と MySQL のサポートの違い:

-   MySQL 8.0.22以降、正規表現関数ではバイナリ文字列をサポートしていません。詳細は[MySQLドキュメント](https://dev.mysql.com/doc/refman/8.0/en/regexp.html)を参照してください。ただし、実際には、すべてのパラメータまたは戻り値の型がバイナリ文字列であれば、MySQLで正規関数は正常に動作します。それ以外の場合は、エラーが報告されます。
-   現在、TiDB ではバイナリ文字列の使用が禁止されており、どのような状況でもエラーが報告されます。

### その他の互換性 {#other-compatibility}

-   TiDBにおける空文字列の置換動作はMySQLとは異なります。1 `REGEXP_REPLACE("", "^$", "123")`例に挙げます。

    -   MySQL は空の文字列を置き換えず、結果として`""`返します。
    -   TiDB は空の文字列を置き換え、結果として`"123"`返します。

-   TiDBでグループをキャプチャするために使用するキーワードはMySQLとは異なります。MySQLではキーワードとして`$`使用しますが、TiDBでは`\\`使用します。また、TiDBは`0`から`9`までの番号のグループのみをキャプチャできます。

    たとえば、次の SQL ステートメントは TiDB に`ab`返します。

    ```sql
    SELECT REGEXP_REPLACE('abcd','(.*)(.{2})$','\\1') AS s;
    ```

### 既知の問題 {#known-issues}

-   [GitHub の問題 #37981](https://github.com/pingcap/tidb/issues/37981)
