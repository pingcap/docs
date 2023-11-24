---
title: Character Set and Collation
summary: Learn about the supported character sets and collations in TiDB.
---

# 文字セットと照合順序 {#character-set-and-collation}

このドキュメントでは、TiDB でサポートされる文字セットと照合順序を紹介します。

## コンセプト {#concepts}

文字セットは、記号とエンコーディングのセットです。 TiDB のデフォルトの文字セットは utf8mb4 で、MySQL 8.0 以降のデフォルトと一致します。

照合順序は、文字セット内の文字と文字の並べ替え順序を比較するための一連の規則です。たとえば、バイナリ照合順序では、 `A`と`a`は同等として比較されません。

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_bin;
SELECT 'A' = 'a';
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
SELECT 'A' = 'a';
```

```sql
SELECT 'A' = 'a';
```

```sql
+-----------+
| 'A' = 'a' |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)
```

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT 'A' = 'a';
```

```sql
+-----------+
| 'A' = 'a' |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
```

TiDB はデフォルトでバイナリ照合順序を使用します。これは、デフォルトで大文字と小文字を区別しない照合順序を使用する MySQL とは異なります。

## TiDB でサポートされる文字セットと照合順序 {#character-sets-and-collations-supported-by-tidb}

現在、TiDB は次の文字セットをサポートしています。

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

TiDB は次の照合順序をサポートしています。

```sql
SHOW COLLATION;
```

```sql
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| ascii_bin          | ascii   |   65 | Yes     | Yes      |       1 |
| binary             | binary  |   63 | Yes     | Yes      |       1 |
| gbk_bin            | gbk     |   87 |         | Yes      |       1 |
| gbk_chinese_ci     | gbk     |   28 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |   47 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |   83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |   33 |         | Yes      |       1 |
| utf8_unicode_ci    | utf8    |  192 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 |  224 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
11 rows in set (0.00 sec)
```

> **警告：**
>
> TiDB は、latin1 を utf8 のサブセットとして誤って扱います。これにより、latin1 エンコーディングと utf8 エンコーディングの間で異なる文字を保存すると、予期しない動作が発生する可能性があります。 utf8mb4 文字セットを強く推奨します。詳細については[TiDB #18955](https://github.com/pingcap/tidb/issues/18955)参照してください。
>
> 述語に`LIKE 'prefix%'`などの文字列接頭辞の`LIKE`含まれており、ターゲット列が非バイナリ照合順序(接尾辞が`_bin`で終わらない) に設定されている場合、オプティマイザは現在、この述語を範囲スキャンに変換できません。代わりに、フルスキャンが実行されます。その結果、このような SQL クエリは予期しないリソースの消費につながる可能性があります。

> **注記：**
>
> TiDB のデフォルトの照合順序 (サフィックス`_bin`が付くバイナリ照合順序) は、 [MySQL のデフォルトの照合順序](https://dev.mysql.com/doc/refman/8.0/en/charset-charsets.html) (通常はサフィックス`_general_ci`が付く一般照合順序) とは異なります。これにより、明示的な文字セットを指定しているが、暗黙的なデフォルト照合順序の選択に依存している場合、互換性のない動作が発生する可能性があります。

次のステートメントを使用すると、文字セットに対応する照合順序 ( [照合順序の新しいフレームワーク](#new-framework-for-collations)の下) を表示できます。

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

TiDB による GBK 文字セットのサポートの詳細については、 [GBK](/character-set-gbk.md)を参照してください。

## TiDB の<code>utf8</code>と<code>utf8mb4</code> {#code-utf8-code-and-code-utf8mb4-code-in-tidb}

MySQL では、文字セット`utf8`は最大 3 バイトに制限されています。これは、Basic Multilingual Plane (BMP) に文字を保存するには十分ですが、絵文字などの文字を保存するには十分ではありません。この場合、代わりに文字セット`utf8mb4`を使用することをお勧めします。

デフォルトでは、TiDB は文字セット`utf8`を最大 3 バイトに制限し、TiDB で作成されたデータを MySQL で安全に復元できるようにします。システム変数[`tidb_check_mb4_value_in_utf8`](/system-variables.md#tidb_check_mb4_value_in_utf8)の値を`OFF`に変更することで無効にできます。

以下は、表に 4 バイトの絵文字を挿入するときのデフォルトの動作を示しています。 `INSERT`ステートメントは`utf8`文字セットでは失敗しますが、 `utf8mb4`では成功します。

```sql
CREATE TABLE utf8_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

```sql
CREATE TABLE utf8m4_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8mb4;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

```sql
INSERT INTO utf8_test VALUES ('😉');
```

```sql
ERROR 1366 (HY000): incorrect utf8 value f09f9889(😉) for column c
```

```sql
INSERT INTO utf8m4_test VALUES ('😉');
```

```sql
Query OK, 1 row affected (0.02 sec)
```

```sql
SELECT char_length(c), length(c), c FROM utf8_test;
```

```sql
Empty set (0.01 sec)
```

```sql
SELECT char_length(c), length(c), c FROM utf8m4_test;
```

```sql
+----------------+-----------+------+
| char_length(c) | length(c) | c    |
+----------------+-----------+------+
|              1 |         4 | 😉     |
+----------------+-----------+------+
1 row in set (0.00 sec)
```

## 異なるレイヤーの文字セットと照合順序 {#character-set-and-collation-in-different-layers}

文字セットと照合順序は異なるレイヤーで設定できます。

### データベースの文字セットと照合順序 {#database-character-set-and-collation}

各データベースには文字セットと照合順序があります。次のステートメントを使用して、データベースの文字セットと照合順序を指定できます。

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

ここで`DATABASE` `SCHEMA`に置き換えることができます。

データベースが異なれば、異なる文字セットと照合順序を使用できます。現在のデータベースの文字セットと照合順序を確認するには、 `character_set_database`と`collation_database`を使用します。

```sql
CREATE SCHEMA test1 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

```sql
USE test1;
```

```sql
Database changed
```

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

```sql
CREATE SCHEMA test2 CHARACTER SET latin1 COLLATE latin1_bin;
```

```sql
Query OK, 0 rows affected (0.09 sec)
```

```sql
USE test2;
```

```sql
Database changed
```

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

`INFORMATION_SCHEMA`には 2 つの値も表示されます。

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

```sql
CREATE TABLE t1(a int) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

テーブルの文字セットと照合順序が指定されていない場合は、データベースの文字セットと照合順序がデフォルト値として使用されます。

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

### 文字列の文字セットと照合順序 {#string-character-sets-and-collation}

各文字列は文字セットと照合順序に対応します。文字列を使用する場合は、次のオプションを使用できます。

```sql
[_charset_name]'string' [COLLATE collation_name]
```

例：

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

ルール:

-   ルール 1: `CHARACTER SET charset_name`と`COLLATE collation_name`を指定すると、 `charset_name`文字セットと`collation_name`照合順序が直接使用されます。
-   ルール 2: `CHARACTER SET charset_name`を指定して`COLLATE collation_name`指定しない場合、 `charset_name`文字セットとデフォルトの照合順序`charset_name`が使用されます。
-   規則 3: `CHARACTER SET charset_name`も`COLLATE collation_name`指定しない場合、システム変数`character_set_connection`と`collation_connection`で指定された文字セットと照合順序が使用されます。

### クライアント接続の文字セットと照合順序 {#client-connection-character-set-and-collation}

-   サーバーの文字セットと照合順序は、システム変数`character_set_server`および`collation_server`の値です。

-   デフォルトのデータベースの文字セットと照合順序は、システム変数`character_set_database`および`collation_database`の値です。

`character_set_connection`と`collation_connection`を使用して、各接続の文字セットと照合順序を指定できます。 `character_set_client`変数はクライアントの文字セットを設定します。

結果を返す前に、 `character_set_results`システム変数は、サーバーが結果のメタデータを含むクエリ結果をクライアントに返す文字セットを示します。

次のステートメントを使用して、クライアントに関連する文字セットと照合順序を設定できます。

-   `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES`クライアントが SQL ステートメントをサーバーに送信するために使用する文字セットを示します。 `SET NAMES utf8mb4`クライアントからのすべてのリクエストとサーバーからの結果が utf8mb4 を使用することを示します。

    `SET NAMES 'charset_name'`ステートメントは、次のステートメントの組み合わせと同等です。

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE`はオプションであり、存在しない場合は、 `charset_name`のデフォルトの照合順序が`collation_connection`の設定に使用されます。

-   `SET CHARACTER SET 'charset_name'`

    `SET NAMES`と同様に、 `SET NAMES 'charset_name'`ステートメントは次のステートメントの組み合わせと同等です。

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET charset_connection = @@charset_database;
    SET collation_connection = @@collation_database;
    ```

## 文字セットと照合順序の選択優先順位 {#selection-priorities-of-character-sets-and-collations}

文字列 &gt;カラム&gt; テーブル &gt; データベース &gt; サーバー

## 文字セットと照合順序の選択に関する一般規則 {#general-rules-on-selecting-character-sets-and-collation}

-   ルール 1: `CHARACTER SET charset_name`と`COLLATE collation_name`を指定すると、 `charset_name`文字セットと`collation_name`照合順序が直接使用されます。
-   ルール 2: `CHARACTER SET charset_name`を指定し、 `COLLATE collation_name`指定しない場合は、 `charset_name`文字セットとデフォルトの照合順序`charset_name`が使用されます。
-   ルール 3: `CHARACTER SET charset_name`も`COLLATE collation_name`指定しない場合、より高い最適化レベルの文字セットと照合順序が使用されます。

## 文字の妥当性チェック {#validity-check-of-characters}

指定された文字セットが`utf8`または`utf8mb4`の場合、TiDB は有効な`utf8`文字のみをサポートします。無効な文字の場合、TiDB は`incorrect utf8 value`エラーを報告します。 TiDB のこの文字の有効性チェックは MySQL 8.0 と互換性がありますが、 MySQL 5.7以前のバージョンとは互換性がありません。

このエラー報告を無効にするには、 `set @@tidb_skip_utf8_check=1;`使用して文字チェックをスキップします。

> **注記：**
>
> 文字チェックがスキップされると、TiDB はアプリケーションによって書き込まれた不正な UTF-8 文字の検出に失敗し、 `ANALYZE`の実行時にデコード エラーが発生し、その他の不明なエンコードの問題が発生する可能性があります。アプリケーションが書き込まれた文字列の正当性を保証できない場合は、文字チェックをスキップすることはお勧めできません。

## 照合サポートフレームワーク {#collation-support-framework}

<CustomContent platform="tidb">

照合照合順序の構文サポートとセマンティック サポートは、 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)構成項目の影響を受けます。構文サポートとセマンティック サポートは異なります。前者は、TiDB が解析および照合順序の設定ができることを示します。後者は、TiDB が文字列を比較するときに照合順序を正しく使用できることを示しています。

</CustomContent>

v4.0 より前では、TiDB は[照合順序の古いフレームワーク](#old-framework-for-collations)のみを提供します。このフレームワークでは、TiDB はほとんどの MySQL 照合順序の構文解析をサポートしていますが、意味的にはすべての照合順序をバイナリ照合順序として受け取ります。

v4.0 以降、TiDB は[照合順序の新しいフレームワーク](#new-framework-for-collations)をサポートします。このフレームワークでは、TiDB はさまざまな照合順序を意味的に解析し、文字列を比較するときに照合順序に厳密に従います。

### 照合順序の古いフレームワーク {#old-framework-for-collations}

v4.0 より前では、TiDB でほとんどの MySQL 照合順序を指定でき、これらの照合順序はデフォルトの照合順序に従って処理されます。つまり、バイト順序によって文字順序が決まります。 MySQL とは異なり、TiDB は文字の末尾のスペースを処理しないため、次のような動作の違いが生じます。

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
```

```sql
Query OK, 0 rows affected
```

```sql
INSERT INTO t VALUES ('A');
```

```sql
Query OK, 1 row affected
```

```sql
INSERT INTO t VALUES ('a');
```

```sql
Query OK, 1 row affected
```

TiDB では、前述のステートメントは正常に実行されます。 MySQL では、 `utf8mb4_general_ci`は大文字と小文字が区別されないため、 `Duplicate entry 'a'`エラーが報告されます。

```sql
INSERT INTO t1 VALUES ('a ');
```

```sql
Query OK, 1 row affected
```

TiDB では、前述のステートメントは正常に実行されます。 MySQLではスペースを埋めて比較するため、 `Duplicate entry 'a '`エラーが返されます。

### 照合順序の新しいフレームワーク {#new-framework-for-collations}

TiDB v4.0 以降、照合順序のための完全なフレームワークが導入されています。

<CustomContent platform="tidb">

この新しいフレームワークは、セマンティック解析照合をサポートし、クラスターの最初の初期化時に新しいフレームワークを有効にするかどうかを決定する`new_collations_enabled_on_first_bootstrap`構成項目を導入します。新しいフレームワークを有効にするには、 `new_collations_enabled_on_first_bootstrap` ～ `true`を設定します。詳細は[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)を参照してください。構成項目が有効になった後にクラスターを初期化すると、 `mysql`の`new_collation_enabled`変数を通じて新しい照合順序が有効になっているかどうかを確認できます。 `tidb`テーブル:

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

</CustomContent>

<CustomContent platform="tidb-cloud">

この新しいフレームワークは、意味論的な照合順序の解析をサポートします。 TiDB は、クラスターが最初に初期化されるときに、デフォルトで新しいフレームワークを有効にします。

</CustomContent>

新しいフレームワークでは、TiDB は MySQL と互換性のある`utf8_general_ci` 、 `utf8mb4_general_ci` 、 `utf8_unicode_ci` 、 `utf8mb4_unicode_ci` 、 `gbk_chinese_ci` 、および`gbk_bin`照合順序をサポートします。

`utf8_general_ci` 、 `utf8mb4_general_ci` 、 `utf8_unicode_ci` 、 `utf8mb4_unicode_ci` 、および`gbk_chinese_ci`のいずれかを使用する場合、文字列比較では大文字と小文字とアクセントは区別されません。同時に、TiDB は照合順序`PADDING`動作も修正します。

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES ('A');
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
INSERT INTO t VALUES ('a');
```

```sql
ERROR 1062 (23000): Duplicate entry 'a' for key 't.PRIMARY' # TiDB is compatible with the case-insensitive collation of MySQL.
```

```sql
INSERT INTO t VALUES ('a ');
```

```sql
ERROR 1062 (23000): Duplicate entry 'a ' for key 't.PRIMARY' # TiDB modifies the `PADDING` behavior to be compatible with MySQL.
```

> **注記：**
>
> TiDB でのパディングの実装は、MySQL でのパディングの実装とは異なります。 MySQL では、パディングはスペースを埋めることによって実装されます。 TiDB では、パディングは末尾のスペースを切り取ることで実装されます。ほとんどの場合、2 つのアプローチは同じです。唯一の例外は、文字列の末尾にスペース (0x20) 未満の文字が含まれている場合です。たとえば、TiDB では`'a' < 'a\t'`の結果は`1`ですが、MySQL では`'a' < 'a\t'`は`'a ' < 'a\t'`に相当し、結果は`0`になります。

## 式内の照合順序の強制値 {#coercibility-values-of-collations-in-expressions}

式に異なる照合順序の複数の句が含まれる場合、計算で使用される照合順序を推測する必要があります。ルールは次のとおりです。

-   明示的な`COLLATE`句の強制値は`0`です。
-   2 つの文字列の照合順序に互換性がない場合、照合順序が異なる 2 つの文字列の連結の強制値は`1`です。
-   列`CAST()` 、 `CONVERT()` 、または`BINARY()`の照合順序の強制値は`2`です。
-   システム定数 ( `USER ()`または`VERSION ()`によって返される文字列) の強制値は`3`です。
-   定数の強制値は`4`です。
-   数値または中間変数の強制値は`5`です。
-   `NULL`または`NULL`から派生した式の強制値は`6`です。

照合順序を推論する場合、TiDB は強制性の値が低い式の照合照合順序を使用することを優先します。 2 つの句の強制性の値が同じ場合、照合順序は次の優先順位に従って決定されます。

バイナリ &gt; utf8mb4_bin &gt; (utf8mb4_general_ci = utf8mb4_unicode_ci) &gt; utf8_bin &gt; (utf8_general_ci = utf8_unicode_ci) &gt; latin1_bin &gt; ascii_bin

TiDB は、次の状況では照合順序を推測できず、エラーを報告します。

-   2 つの句の照合順序が異なり、両方の句の強制値が`0`である場合。
-   2 つの句の照合順序に互換性がなく、返される式の型が`String`である場合。

## <code>COLLATE</code>句 {#code-collate-code-clause}

TiDB は、 `COLLATE`句を使用して式の照合順序を指定することをサポートしています。この式の強制値は`0`で、最も高い優先順位を持ちます。次の例を参照してください。

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

詳細については、 [接続文字セットと照合順序](https://dev.mysql.com/doc/refman/5.7/en/charset-connection.html)を参照してください。
