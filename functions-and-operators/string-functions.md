---
title: String Functions
summary: Learn about the string functions in TiDB.
---

# 文字列関数 {#string-functions}

TiDB は、 MySQL 5.7で使用可能な[文字列関数](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html)のほとんど、MySQL 8.0 で使用可能な[文字列関数](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html)の一部、Oracle 21 で使用可能な[関数](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlqr/SQL-Functions.html#GUID-93EC62F8-415D-4A7E-B050-5D5B2C127009)の一部をサポートします。

<CustomContent platform="tidb">

Oracle と TiDB の関数と構文の比較については、 [OracleとTiDBの機能と構文の比較](/oracle-functions-to-tidb.md)を参照してください。

</CustomContent>

## サポートされている関数 {#supported-functions}

| 名前                                                                                                                                            | 説明                                                                                                                                     |
| :-------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| [`ASCII()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ascii)                                                     | 左端の文字の数値を返す                                                                                                                            |
| [`BIN()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bin)                                                         | 数値のバイナリ表現を含む文字列を返します。                                                                                                                  |
| [`BIT_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_bit-length)                                           | 引数の長さをビット単位で返します                                                                                                                       |
| [`CHAR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char)                                                       | 渡された各整数の文字を返します                                                                                                                        |
| [`CHAR_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_char-length)                                         | 引数の文字数を返す                                                                                                                              |
| [`CHARACTER_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_character-length)                               | `CHAR_LENGTH()`の同義語                                                                                                                    |
| [`CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat)                                                   | 連結された文字列を返す                                                                                                                            |
| [`CONCAT_WS()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat-ws)                                             | セパレータを使用して連結して返す                                                                                                                       |
| [`ELT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_elt)                                                         | インデックス番号の文字列を返す                                                                                                                        |
| [`EXPORT_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_export-set)                                           | 値ビットに設定されているすべてのビットに対して on 文字列を取得し、未設定のすべてのビットに対して off 文字列を取得するような文字列を返します。                                                            |
| [`FIELD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_field)                                                     | 後続の引数の最初の引数のインデックス (位置) を返します。                                                                                                         |
| [`FIND_IN_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_find-in-set)                                         | 2 番目の引数内の最初の引数のインデックス位置を返します。                                                                                                          |
| [`FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_format)                                                   | 指定された小数点以下の桁数にフォーマットされた数値を返します                                                                                                         |
| [`FROM_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_from-base64)                                         | Base-64 文字列にデコードして結果を返す                                                                                                                |
| [`HEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_hex)                                                         | 10 進数または文字列値の 16 進数表現を返します。                                                                                                            |
| [`INSERT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_insert)                                                   | 指定された位置に指定された文字数までの部分文字列を挿入します                                                                                                         |
| [`INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_instr)                                                     | 最初に出現した部分文字列のインデックスを返します。                                                                                                              |
| [`LCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lcase)                                                     | `LOWER()`の同義語                                                                                                                          |
| [`LEFT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_left)                                                       | 指定されたとおりに左端の文字数を返します                                                                                                                   |
| [`LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_length)                                                   | 文字列の長さをバイト単位で返します                                                                                                                      |
| [`LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like)                                              | 簡単なパターンマッチング                                                                                                                           |
| [`LOCATE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_locate)                                                   | 部分文字列が最初に出現する位置を返します。                                                                                                                  |
| [`LOWER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lower)                                                     | 引数を小文字で返します                                                                                                                            |
| [`LPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_lpad)                                                       | 指定された文字列で左詰めされた文字列引数を返します。                                                                                                             |
| [`LTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ltrim)                                                     | 先頭のスペースを削除する                                                                                                                           |
| [`MAKE_SET()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_make-set)                                               | ビットセット内の対応するビットを持つコンマ区切りの文字列のセットを返します。                                                                                                 |
| [`MID()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_mid)                                                         | 指定された位置から始まる部分文字列を返します                                                                                                                 |
| [`NOT LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like)                                      | 単純なパターンマッチングの否定                                                                                                                        |
| [`NOT REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp)                                                       | `REGEXP`の否定                                                                                                                            |
| [`OCT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_oct)                                                         | 数値の 8 進表現を含む文字列を返します。                                                                                                                  |
| [`OCTET_LENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_octet-length)                                       | `LENGTH()`の同義語                                                                                                                         |
| [`ORD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ord)                                                         | 引数の左端の文字の文字コードを返す                                                                                                                      |
| [`POSITION()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_position)                                               | `LOCATE()`の同義語                                                                                                                         |
| [`QUOTE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_quote)                                                     | SQL ステートメントで使用する引数をエスケープする                                                                                                             |
| [`REGEXP`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)                                                               | 正規表現を使用したパターン マッチング                                                                                                                    |
| [`REGEXP_INSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-instr)                                                 | 正規表現に一致する部分文字列の開始インデックスを返します (MySQL と部分的に互換性があります。詳細については、 [MySQL との正規表現の互換性](#regular-expression-compatibility-with-mysql)を参照してください)。 |
| [`REGEXP_LIKE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-like)                                                   | 文字列が正規表現と一致するかどうか (MySQL と部分的に互換性があります。詳細については[MySQL との正規表現の互換性](#regular-expression-compatibility-with-mysql)を参照してください)               |
| [`REGEXP_REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-replace)                                             | 正規表現に一致する部分文字列を置換します (MySQL と部分的に互換性があります。詳細については、 [MySQL との正規表現の互換性](#regular-expression-compatibility-with-mysql)を参照してください)。         |
| [`REGEXP_SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#function_regexp-substr)                                               | 正規表現に一致する部分文字列を返します (MySQL と部分的に互換性があります。詳細については、 [MySQL との正規表現の互換性](#regular-expression-compatibility-with-mysql)を参照してください)。          |
| [`REPEAT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_repeat)                                                   | 指定された回数だけ文字列を繰り返します                                                                                                                    |
| [`REPLACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_replace)                                                 | 指定された文字列の出現箇所を置換します                                                                                                                    |
| [`REVERSE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_reverse)                                                 | 文字列内の文字を反転する                                                                                                                           |
| [`RIGHT()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_right)                                                     | 指定された右端の文字数を返します                                                                                                                       |
| [`RLIKE`](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp)                                                                | `REGEXP`の同義語                                                                                                                           |
| [`RPAD()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rpad)                                                       | 指定された回数だけ文字列を追加します                                                                                                                     |
| [`RTRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_rtrim)                                                     | 末尾のスペースを削除する                                                                                                                           |
| [`SPACE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_space)                                                     | 指定された数のスペースを含む文字列を返します。                                                                                                                |
| [`STRCMP()`](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp)                                        | 2 つの文字列を比較する                                                                                                                           |
| [`SUBSTR()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substr)                                                   | 指定された部分文字列を返します                                                                                                                        |
| [`SUBSTRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring)                                             | 指定された部分文字列を返します                                                                                                                        |
| [`SUBSTRING_INDEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_substring-index)                                 | 区切り文字が指定された回数出現する前の文字列から部分文字列を返します。                                                                                                    |
| [`TO_BASE64()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_to-base64)                                             | Base-64 文字列に変換された引数を返します                                                                                                               |
| [`TRANSLATE()`](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/TRANSLATE.html#GUID-80F85ACB-092C-4CC7-91F6-B3A585E3A690) | 文字列内のすべての文字を他の文字に置き換えます。 Oracle のように空の文字列を`NULL`として扱いません。                                                                              |
| [`TRIM()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_trim)                                                       | 先頭と末尾のスペースを削除する                                                                                                                        |
| [`UCASE()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_ucase)                                                     | `UPPER()`の同義語                                                                                                                          |
| [`UNHEX()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_unhex)                                                     | 数値の 16 進表現を含む文字列を返します。                                                                                                                 |
| [`UPPER()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_upper)                                                     | 大文字に変換する                                                                                                                               |
| [`WEIGHT_STRING()`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_weight-string)                                     | 入力文字列の重み文字列を返します。                                                                                                                      |

## サポートされていない関数 {#unsupported-functions}

-   `LOAD_FILE()`
-   `MATCH()`
-   `SOUNDEX()`

## MySQL との正規表現の互換性 {#regular-expression-compatibility-with-mysql}

次のセクションでは、MySQL との正規表現の互換性について説明します。

### 構文の互換性 {#syntax-compatibility}

MySQL は International Components for Unicode (ICU) を使用して正規表現を実装し、TiDB は RE2 を使用します。 2 つのライブラリの構文の違いについては、 [ICUの文書](https://unicode-org.github.io/icu/userguide/)と[RE2 の構文](https://github.com/google/re2/wiki/Syntax)を参照してください。

### <code>match_type</code>互換性 {#code-match-type-code-compatibility}

TiDB と MySQL の間の`match_type`の値オプションは次のとおりです。

-   TiDB の値のオプションは`"c"` 、 `"i"` 、 `"m"` 、および`"s"`であり、MySQL の値のオプションは`"c"` 、 `"i"` 、 `"m"` 、 `"n"` 、および`"u"`です。

-   TiDB の`"s"` MySQL の`"n"`に対応します。 TiDB で`"s"`が設定されている場合、 `.`文字は行終了文字 ( `\n` ) にも一致します。

    たとえば、MySQL の`SELECT REGEXP_LIKE(a, b, "n") FROM t1` TiDB の`SELECT REGEXP_LIKE(a, b, "s") FROM t1`と同じです。

-   TiDB は、MySQL での Unix 専用の行末を意味する`"u"`サポートしていません。

### データ型の互換性 {#data-type-compatibility}

TiDB と MySQL のバイナリ文字列タイプのサポートの違いは次のとおりです。

-   MySQL は 8.0.22 以降、正規表現関数でバイナリ文字列をサポートしません。詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/regexp.html)を参照してください。ただし、実際には、すべてのパラメータまたは戻り値の型がバイナリ文字列の場合、通常の関数はMySQL で動作します。それ以外の場合は、エラーが報告されます。
-   現在、TiDB ではバイナリ文字列の使用が禁止されており、いかなる状況でもエラーが報告されます。

### その他の互換性 {#other-compatibility}

空の文字列の置換における TiDB サポートと MySQL サポートの違い:

以下では`REGEXP_REPLACE("", "^$", "123")`を例にします。

-   MySQL は空の文字列を置き換えず、結果として`""`を返します。
-   TiDB は空の文字列を置き換え、結果として`"123"`を返します。
