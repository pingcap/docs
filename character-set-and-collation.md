---
title: Character Set and Collation
summary: Learn about the supported character sets and collations in TiDB.
---

# 文字セットと照合 {#character-set-and-collation}

このドキュメントでは、TiDBでサポートされている文字セットと照合を紹介します。

## コンセプト {#concepts}

文字セットは、記号とエンコーディングのセットです。 TiDBのデフォルトの文字セットはutf8mb4で、MySQL8.0以降のデフォルトと一致します。

照合順序は、文字セット内の文字を比較するための一連のルール、および文字の並べ替え順序です。たとえば、バイナリ照合順序では、 `A`と`a`は等しいと比較されません。

{{< copyable "" >}}

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_bin;
SELECT 'A' = 'a';
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
SELECT 'A' = 'a';
```

```sql
mysql> SELECT 'A' = 'a';
+-----------+
| 'A' = 'a' |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)

mysql> SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT 'A' = 'a';
+-----------+
| 'A' = 'a' |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
```

TiDBは、デフォルトでバイナリ照合順序を使用します。これは、デフォルトで大文字と小文字を区別しない照合順序を使用するMySQLとは異なります。

## TiDBでサポートされている文字セットと照合 {#character-sets-and-collations-supported-by-tidb}

現在、TiDBは次の文字セットをサポートしています。

{{< copyable "" >}}

```sql
SHOW CHARACTER SET;
```

```sql
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| ascii   | US ASCII                            | ascii_bin         |      1 |
| binary  | binary                              | binary            |      1 |
| gbk     | Chinese Internal Code Specification | gbk_bin           |      2 |
| latin1  | Latin1                              | latin1_bin        |      1 |
| utf8    | UTF-8 Unicode                       | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode                       | utf8mb4_bin       |      4 |
+---------+-------------------------------------+-------------------+--------+
6 rows in set (0.00 sec)
```

TiDBは、次の照合をサポートしています。

```sql
mysql> show collation;
+-------------+---------+------+---------+----------+---------+
| Collation   | Charset | Id   | Default | Compiled | Sortlen |
+-------------+---------+------+---------+----------+---------+
| utf8mb4_bin | utf8mb4 |   46 | Yes     | Yes      |       1 |
| latin1_bin  | latin1  |   47 | Yes     | Yes      |       1 |
| binary      | binary  |   63 | Yes     | Yes      |       1 |
| ascii_bin   | ascii   |   65 | Yes     | Yes      |       1 |
| utf8_bin    | utf8    |   83 | Yes     | Yes      |       1 |
| gbk_bin     | gbk     |   87 | Yes     | Yes      |       1 |
+-------------+---------+------+---------+----------+---------+
6 rows in set (0.00 sec)
```

> **警告：**
>
> TiDBは、latin1をutf8のサブセットとして誤って扱います。これにより、latin1エンコーディングとutf8エンコーディングで異なる文字を格納するときに予期しない動作が発生する可能性があります。 utf8mb4文字セットに強くお勧めします。詳細については、 [TiDB＃18955](https://github.com/pingcap/tidb/issues/18955)を参照してください。

> **ノート：**
>
> TiDBのデフォルトの照合（接尾辞`_bin`のバイナリ照合）は[MySQLのデフォルトの照合](https://dev.mysql.com/doc/refman/8.0/en/charset-charsets.html) （通常は接尾辞`_general_ci`の一般的な照合）とは異なります。これにより、明示的な文字セットを指定しているが、選択される暗黙的なデフォルトの照合順序に依存している場合に、互換性のない動作が発生する可能性があります。

次のステートメントを使用して、文字セットに対応する照合（ [照合のための新しいフレームワーク](#new-framework-for-collations)の下）を表示できます。

{{< copyable "" >}}

```sql
SHOW COLLATION WHERE Charset = 'utf8mb4';
```

```sql
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 |  224 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
3 rows in set (0.00 sec)
```

GBK文字セットのTiDBサポートの詳細については、 [GBK](/character-set-gbk.md)を参照してください。

## <code>utf8mb4</code>の<code>utf8</code>とutf8mb4 {#code-utf8-code-and-code-utf8mb4-code-in-tidb}

MySQLでは、文字セット`utf8`は最大3バイトに制限されています。これは、Basic Multilingual Plane（BMP）に文字を格納するには十分ですが、絵文字などの文字を格納するには十分ではありません。このため、代わりに文字セット`utf8mb4`を使用することをお勧めします。

デフォルトでは、TiDBで作成されたデータをMySQLで安全に復元できるように、TiDBは`utf8`に同じ3バイトの制限を提供します。これは、TiDB構成ファイルの値を`check-mb4-value-in-utf8`から`FALSE`に変更することで無効にできます。

以下は、4バイトの絵文字をテーブルに挿入するときのデフォルトの動作を示しています。 `INSERT`ステートメントは`utf8`文字セットでは失敗しますが、 `utf8mb4`では成功します。

```sql
mysql> CREATE TABLE utf8_test (
    ->  c char(1) NOT NULL
    -> ) CHARACTER SET utf8;
Query OK, 0 rows affected (0.09 sec)

mysql> CREATE TABLE utf8m4_test (
    ->  c char(1) NOT NULL
    -> ) CHARACTER SET utf8mb4;
Query OK, 0 rows affected (0.09 sec)

mysql> INSERT INTO utf8_test VALUES ('😉');
ERROR 1366 (HY000): incorrect utf8 value f09f9889(😉) for column c
mysql> INSERT INTO utf8m4_test VALUES ('😉');
Query OK, 1 row affected (0.02 sec)

mysql> SELECT char_length(c), length(c), c FROM utf8_test;
Empty set (0.01 sec)

mysql> SELECT char_length(c), length(c), c FROM utf8m4_test;
+----------------+-----------+------+
| char_length(c) | length(c) | c    |
+----------------+-----------+------+
|              1 |         4 | 😉     |
+----------------+-----------+------+
1 row in set (0.00 sec)
```

## 異なるレイヤーでの文字セットと照合順序 {#character-set-and-collation-in-different-layers}

文字セットと照合順序は、異なるレイヤーで設定できます。

### データベースの文字セットと照合順序 {#database-character-set-and-collation}

各データベースには、文字セットと照合順序があります。次のステートメントを使用して、データベースの文字セットと照合順序を指定できます。

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

ここでは、 `DATABASE`を`SCHEMA`に置き換えることができます。

異なるデータベースは、異なる文字セットと照合を使用できます。 `character_set_database`と`collation_database`を使用して、現在のデータベースの文字セットと照合順序を確認します。

{{< copyable "" >}}

```sql
CREATE SCHEMA test1 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "" >}}

```sql
USE test1;
```

```sql
Database changed
```

{{< copyable "" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```sql
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8mb4                  | utf8mb4_general_ci   |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

{{< copyable "" >}}

```sql
CREATE SCHEMA test2 CHARACTER SET latin1 COLLATE latin1_bin;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "" >}}

```sql
USE test2;
```

```sql
Database changed
```

{{< copyable "" >}}

```sql
SELECT @@character_set_database, @@collation_database;
```

```sql
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| latin1                   | latin1_bin           |
+--------------------------|----------------------+
1 row in set (0.00 sec)
```

`INFORMATION_SCHEMA`の2つの値も確認できます。

{{< copyable "" >}}

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

### テーブルの文字セットと照合順序 {#table-character-set-and-collation}

次のステートメントを使用して、テーブルの文字セットと照合順序を指定できます。

```sql
CREATE TABLE tbl_name (column_list)
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]]

ALTER TABLE tbl_name
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]
```

例えば：

{{< copyable "" >}}

```sql
CREATE TABLE t1(a int) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

テーブルの文字セットと照合順序が指定されていない場合、データベースの文字セットと照合順序がデフォルト値として使用されます。

### カラムの文字セットと照合順序 {#column-character-set-and-collation}

次のステートメントを使用して、列の文字セットと照合順序を指定できます。

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

列の文字セットと照合順序が指定されていない場合は、テーブルの文字セットと照合順序がデフォルト値として使用されます。

### 文字列文字セットと照合順序 {#string-character-sets-and-collation}

各文字列は、文字セットと照合順序に対応しています。文字列を使用する場合、次のオプションを使用できます。

{{< copyable "" >}}

```sql
[_charset_name]'string' [COLLATE collation_name]
```

例：

{{< copyable "" >}}

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

ルール：

-   ルール1： `CHARACTER SET charset_name`と`COLLATE collation_name`を指定すると、 `charset_name`文字セットと`collation_name`照合順序が直接使用されます。
-   ルール2： `CHARACTER SET charset_name`を指定し、 `COLLATE collation_name`を指定しない場合、 `charset_name`文字セットとデフォルトの`charset_name`の照合順序が使用されます。
-   ルール3： `CHARACTER SET charset_name`も`COLLATE collation_name`も指定しない場合、システム変数`character_set_connection`と`collation_connection`によって指定された文字セットと照合順序が使用されます。

### クライアント接続の文字セットと照合順序 {#client-connection-character-set-and-collation}

-   サーバーの文字セットと照合順序は、 `character_set_server`と`collation_server`のシステム変数の値です。

-   デフォルトデータベースの文字セットと照合順序は、 `character_set_database`と`collation_database`のシステム変数の値です。

`character_set_connection`と`collation_connection`を使用して、各接続の文字セットと照合順序を指定できます。 `character_set_client`変数は、クライアントの文字セットを設定するためのものです。

結果を返す前に、 `character_set_results`システム変数は、サーバーが結果のメタデータを含むクエリ結果をクライアントに返す文字セットを示します。

次のステートメントを使用して、クライアントに関連する文字セットと照合順序を設定できます。

-   `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES`は、クライアントがSQLステートメントをサーバーに送信するために使用する文字セットを示します。 `SET NAMES utf8mb4`は、クライアントからのすべての要求がutf8mb4を使用し、サーバーからの結果も使用することを示します。

    `SET NAMES 'charset_name'`ステートメントは、次のステートメントの組み合わせと同等です。

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE`はオプションです。存在しない場合は、 `charset_name`のデフォルトの照合順序を使用して`collation_connection`を設定します。

-   `SET CHARACTER SET 'charset_name'`

    `SET NAMES`と同様に、 `SET NAMES 'charset_name'`ステートメントは次のステートメントの組み合わせと同等です。

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET charset_connection = @@charset_database;
    SET collation_connection = @@collation_database;
    ```

## 文字セットと照合の選択の優先順位 {#selection-priorities-of-character-sets-and-collations}

文字列&gt;カラム&gt;テーブル&gt;データベース&gt;サーバー

## 文字セットと照合順序の選択に関する一般的な規則 {#general-rules-on-selecting-character-sets-and-collation}

-   ルール1： `CHARACTER SET charset_name`と`COLLATE collation_name`を指定すると、 `charset_name`文字セットと`collation_name`照合順序が直接使用されます。
-   ルール2： `CHARACTER SET charset_name`を指定し、 `COLLATE collation_name`を指定しない場合、 `charset_name`文字セットとデフォルトの`charset_name`の照合順序が使用されます。
-   ルール3： `CHARACTER SET charset_name`も`COLLATE collation_name`も指定しない場合、より高い最適化レベルの文字セットと照合順序が使用されます。

## 文字の妥当性チェック {#validity-check-of-characters}

指定された文字セットが`utf8`または`utf8mb4`の場合、TiDBは有効な`utf8`文字のみをサポートします。無効な文字の場合、TiDBは`incorrect utf8 value`エラーを報告します。このTiDBの文字の有効性チェックは、 MySQL 5.7 8.0と互換性がありますが、MySQL5.7以前のバージョンとは互換性がありません。

このエラー報告を無効にするには、 `set @@tidb_skip_utf8_check=1;`を使用して文字チェックをスキップします。

> **ノート：**
>
> 文字チェックをスキップすると、TiDBはアプリケーションによって書き込まれた不正なUTF-8文字の検出に失敗し、 `ANALYZE`の実行時にデコードエラーが発生し、その他の不明なエンコードの問題が発生する可能性があります。アプリケーションが書き込まれた文字列の有効性を保証できない場合は、文字チェックをスキップすることはお勧めしません。

## 照合サポートフレームワーク {#collation-support-framework}

照合順序の構文サポートとセマンティックサポートは、 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)の構成項目の影響を受けます。構文サポートとセマンティックサポートは異なります。前者は、TiDBが照合を解析および設定できることを示しています。後者は、文字列を比較するときにTiDBが照合を正しく使用できることを示しています。

v4.0より前では、TiDBは[照合のための古いフレームワーク](#old-framework-for-collations)のみを提供します。このフレームワークでは、TiDBはほとんどのMySQL照合の構文解析をサポートしていますが、意味的にはすべての照合をバイナリ照合として受け取ります。

v4.0以降、TiDBは[照合のための新しいフレームワーク](#new-framework-for-collations)をサポートします。このフレームワークでは、TiDBはさまざまな照合を意味的に解析し、文字列を比較するときに照合を厳密に追跡します。

### 照合のための古いフレームワーク {#old-framework-for-collations}

v4.0より前では、TiDBでほとんどのMySQL照合を指定でき、これらの照合はデフォルトの照合に従って処理されます。つまり、バイト順序によって文字の順序が決まります。 MySQLとは異なり、TiDBは文字の末尾のスペースを処理しないため、次の動作の違いが発生します。

{{< copyable "" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
Query OK, 0 rows affected
INSERT INTO t VALUES ('A');
Query OK, 1 row affected
INSERT INTO t VALUES ('a');
Query OK, 1 row affected # In TiDB, it is successfully executed. In MySQL, because utf8mb4_general_ci is case-insensitive, the `Duplicate entry 'a'` error is reported.
INSERT INTO t1 VALUES ('a ');
Query OK, 1 row affected # In TiDB, it is successfully executed. In MySQL, because comparison is performed after the spaces are filled in, the `Duplicate entry 'a '` error is returned.
```

### 照合のための新しいフレームワーク {#new-framework-for-collations}

TiDB 4.0では、照合のための完全なフレームワークが導入されています。この新しいフレームワークは、意味論的な照合の解析をサポートし、クラスタが最初に初期化されるときに新しいフレームワークを有効にするかどうかを決定する`new_collations_enabled_on_first_bootstrap`の構成項目を導入します。新しいフレームワークを有効にするには、 `new_collations_enabled_on_first_bootstrap`を`true`に設定します。詳細については、 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)を参照してください。構成項目を有効にした後でクラスタを初期化すると、 `mysql`の`new_collation_enabled`変数を使用して新しい照合順序が有効になっているかどうかを確認できます。 `tidb`テーブル：

{{< copyable "" >}}

```sql
SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME='new_collation_enabled';
```

```sql
+----------------+
| VARIABLE_VALUE |
+----------------+
| True           |
+----------------+
1 row in set (0.00 sec)
```

新しいフレームワークでは、 `utf8mb4_general_ci`はMySQLと互換性のある`utf8_general_ci` 、および`utf8mb4_unicode_ci`の`gbk_bin`を`gbk_chinese_ci`し`utf8_unicode_ci` 。

`utf8_general_ci` 、および`utf8mb4_general_ci`の`utf8mb4_unicode_ci` `gbk_chinese_ci`が使用されている場合、文字列の比較では大文字と小文字が区別されず、アクセントも区別され`utf8_unicode_ci`ん。同時に、TiDBは照合の`PADDING`の動作も修正します。

{{< copyable "" >}}

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
Query OK, 0 rows affected (0.00 sec)
INSERT INTO t VALUES ('A');
Query OK, 1 row affected (0.00 sec)
INSERT INTO t VALUES ('a');
ERROR 1062 (23000): Duplicate entry 'a' for key 'PRIMARY' # TiDB is compatible with the case-insensitive collation of MySQL.
INSERT INTO t VALUES ('a ');
ERROR 1062 (23000): Duplicate entry 'a ' for key 'PRIMARY' # TiDB modifies the `PADDING` behavior to be compatible with MySQL.
```

> **ノート：**
>
> TiDBでのパディングの実装は、MySQLでの実装とは異なります。 MySQLでは、パディングはスペースを埋めることによって実装されます。 TiDBでは、パディングは最後のスペースを切り取って実装されます。 2つのアプローチは、ほとんどの場合同じです。唯一の例外は、文字列の末尾にスペース（0x20）未満の文字が含まれている場合です。たとえば、TiDBでの`'a' < 'a\t'`の結果は`1`ですが、MySQLでは`'a' < 'a\t'`は`'a ' < 'a\t'`に相当し、結果は`0`です。

## 式の照合の強制力の値 {#coercibility-values-of-collations-in-expressions}

式に異なる照合の複数の句が含まれる場合は、計算で使用される照合順序を推測する必要があります。ルールは次のとおりです。

-   明示的な`COLLATE`節の強制力の値は`0`です。
-   2つの文字列の照合に互換性がない場合、照合が異なる2つの文字列の連結の強制力の値は`1`です。
-   列`CAST()` 、または`CONVERT()`の照合順序には、 `BINARY()`の強制力値があり`2` 。
-   システム定数（ `USER ()`または`VERSION ()`によって返される文字列）の強制力の値は`3`です。
-   定数の強制力の値は`4`です。
-   数値または中間変数の強制力の値は`5`です。
-   `NULL`または`NULL`から派生した式の強制力の値は、 `6`です。

照合を推測する場合、TiDBは、より低い強制力の値を持つ式の照合順序を使用することを好みます。 2つの句の強制力の値が同じである場合、照合順序は次の優先順位に従って決定されます。

バイナリ&gt;utf8mb4_bin&gt;（utf8mb4_general_ci = utf8mb4_unicode_ci）&gt; utf8_bin&gt;（utf8_general_ci = utf8_unicode_ci）&gt; latin1_bin&gt; ascii_bin

TiDBは照合順序を推測できず、次の状況でエラーを報告します。

-   2つの句の照合が異なり、両方の句の強制力の値が`0`である場合。
-   2つの句の照合に互換性がなく、返される式のタイプが`String`の場合。

## <code>COLLATE</code>句 {#code-collate-code-clause}

TiDBは、式の照合順序を指定するための`COLLATE`句の使用をサポートしています。この式の強制力の値は`0`であり、これが最も優先度が高くなります。次の例を参照してください。

{{< copyable "" >}}

```sql
SELECT 'a' = _utf8mb4 'A' collate utf8mb4_general_ci;
```

```sql
+-----------------------------------------------+
| 'a' = _utf8mb4 'A' collate utf8mb4_general_ci |
+-----------------------------------------------+
|                                             1 |
+-----------------------------------------------+
1 row in set (0.00 sec)
```

詳細については、 [接続文字セットと照合](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html)を参照してください。
