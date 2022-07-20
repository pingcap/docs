---
title: String Functions
summary: Learn about the string functions in TiDB.
---

# 文字列関数 {#string-functions}

TiDBは、 MySQL 5.7で使用可能な[文字列関数](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html)のほとんどと、Oracle21で使用可能な[関数](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009)の一部をサポートします。

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                                            | 説明                                                                      |
| :-------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| [`ASCII()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ascii)                                                     | 左端の文字の数値を返します                                                           |
| [`BIN()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bin)                                                         | 数値のバイナリ表現を含む文字列を返します                                                    |
| [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bit-length)                                           | 引数の長さをビットで返します                                                          |
| [`CHAR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char)                                                       | 渡された各整数の文字を返します                                                         |
| [`CHAR_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char-length)                                         | 引数の文字数を返す                                                               |
| [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_character-length)                               | `CHAR_LENGTH()`の同義語                                                     |
| [`CONCAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat)                                                   | 連結された文字列を返す                                                             |
| [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat-ws)                                             | セパレータと連結して返す                                                            |
| [`ELT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_elt)                                                         | インデックス番号の文字列を返す                                                         |
| [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_export-set)                                           | 値ビットに設定されたすべてのビットに対してオン文字列を取得し、設定されていないすべてのビットに対してオフ文字列を取得するような文字列を返します |
| [`FIELD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_field)                                                     | 後続の引数の最初の引数のインデックス（位置）を返します                                             |
| [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_find-in-set)                                         | 2番目の引数内の最初の引数のインデックス位置を返します                                             |
| [`FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_format)                                                   | 指定した小数点以下の桁数にフォーマットされた数値を返します                                           |
| [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_from-base64)                                         | Base-64文字列にデコードし、結果を返します                                                |
| [`HEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_hex)                                                         | 10進値または文字列値の16進表現を返します                                                  |
| [`INSERT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_insert)                                                   | 指定された文字数まで、指定された位置に部分文字列を挿入します                                          |
| [`INSTR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_instr)                                                     | 部分文字列の最初の出現のインデックスを返します                                                 |
| [`LCASE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lcase)                                                     | `LOWER()`の同義語                                                           |
| [`LEFT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_left)                                                       | 指定された左端の文字数を返します                                                        |
| [`LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_length)                                                   | 文字列の長さをバイト単位で返します                                                       |
| [`LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like)                                              | シンプルなパターンマッチング                                                          |
| [`LOCATE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_locate)                                                   | 部分文字列の最初の出現位置を返します                                                      |
| [`LOWER()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lower)                                                     | 引数を小文字で返します                                                             |
| [`LPAD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_lpad)                                                       | 指定された文字列が左に埋め込まれた文字列引数を返します                                             |
| [`LTRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ltrim)                                                     | 先頭のスペースを削除します                                                           |
| [`MAKE_SET()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_make-set)                                               | 対応するビットインビットが設定されているコンマ区切りの文字列のセットを返します                                 |
| [`MID()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_mid)                                                         | 指定された位置から始まる部分文字列を返します                                                  |
| [`NOT LIKE`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like)                                      | 単純なパターンマッチングの否定                                                         |
| [`NOT REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp)                                                       | `REGEXP`の否定                                                             |
| [`OCT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_oct)                                                         | 数値の8進表現を含む文字列を返します                                                      |
| [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_octet-length)                                       | `LENGTH()`の同義語                                                          |
| [`ORD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ord)                                                         | 引数の左端の文字の文字コードを返します                                                     |
| [`POSITION()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_position)                                               | `LOCATE()`の同義語                                                          |
| [`QUOTE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_quote)                                                     | SQLステートメントで使用するために引数をエスケープします                                           |
| [`REGEXP`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                                               | 正規表現を使用したパターンマッチング                                                      |
| [`REPEAT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_repeat)                                                   | 指定された回数だけ文字列を繰り返します                                                     |
| [`REPLACE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_replace)                                                 | 指定された文字列の出現箇所を置き換えます                                                    |
| [`REVERSE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_reverse)                                                 | 文字列の文字を反転します                                                            |
| [`RIGHT()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_right)                                                     | 指定された右端の文字数を返します                                                        |
| [`RLIKE`](https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp)                                                                | `REGEXP`の同義語                                                            |
| [`RPAD()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rpad)                                                       | 指定された回数だけ文字列を追加します                                                      |
| [`RTRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rtrim)                                                     | 末尾のスペースを削除します                                                           |
| [`SPACE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_space)                                                     | 指定された数のスペースの文字列を返します                                                    |
| [`STRCMP()`](https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp)                                        | 2つの文字列を比較する                                                             |
| [`SUBSTR()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substr)                                                   | 指定されたとおりに部分文字列を返します                                                     |
| [`SUBSTRING()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring)                                             | 指定されたとおりに部分文字列を返します                                                     |
| [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring-index)                                 | 指定された区切り文字の出現回数の前の文字列から部分文字列を返します                                       |
| [`TO_BASE64()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_to-base64)                                             | Base-64文字列に変換された引数を返します                                                 |
| [`TRANSLATE()`](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRANSLATE.html#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690) | 文字列内の他の文字に出現するすべての文字を置き換えます。 Oracleのように、空の文字列を`NULL`として扱いません。           |
| [`TRIM()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_trim)                                                       | 先頭と末尾のスペースを削除します                                                        |
| [`UCASE()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ucase)                                                     | `UPPER()`の同義語                                                           |
| [`UNHEX()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_unhex)                                                     | 数値の16進表現を含む文字列を返します                                                     |
| [`UPPER()`](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_upper)                                                     | 大文字に変換する                                                                |

## サポートされていない関数 {#unsupported-functions}

-   `LOAD_FILE()`
-   `MATCH`
-   `SOUNDEX()`
-   `SOUNDS LIKE`
-   `WEIGHT_STRING()`
