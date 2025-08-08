---
title: Character Set and Collation
summary: TiDB でサポートされている文字セットと照合順序について学習します。
---

# 文字セットと照合順序 {#character-set-and-collation}

このドキュメントでは、TiDB でサポートされている文字セットと照合順序について説明します。

## 概念 {#concepts}

文字セットとは、記号とエンコーディングの集合です。TiDBのデフォルトの文字セットは`utf8mb4`で、これはMySQL 8.0以降のデフォルトの文字セットと一致します。

照合順序とは、文字セット内の文字を比較するための規則と、文字の並び順のことです。例えば、バイナリ照合順序では、 `A`と`a`等しいとみなされません。

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

次の例は、異なるUnicode照合順序がドイツ語の`ß`と`ss`どのように比較するかを示しています。より厳密なUnicode照合順序のみがこれらを同等とみなし、 `1` （つまりTRUE）を返すことがわかります。

```sql
SELECT
  'ss' COLLATE utf8mb4_general_ci = 'ß',
  'ss' COLLATE utf8mb4_unicode_ci = 'ß',
  'ss' COLLATE utf8mb4_0900_ai_ci = 'ß',
  'ss' COLLATE utf8mb4_0900_bin = 'ß'
\G
```

    *************************** 1. row ***************************
    'ss' COLLATE utf8mb4_general_ci = 'ß': 0
    'ss' COLLATE utf8mb4_unicode_ci = 'ß': 1
    'ss' COLLATE utf8mb4_0900_ai_ci = 'ß': 1
      'ss' COLLATE utf8mb4_0900_bin = 'ß': 0
    1 row in set (0.01 sec)

### 文字セットと照合順序の命名 {#character-set-and-collation-naming}

文字セットには、 `<character_set>_<collation_properties>`形式で命名された複数の照合順序を設定できます。例えば、 `utf8mb4`文字セットには`utf8mb4_bin`という照合順序があり、これは`utf8mb4`バイナリ照合順序です。複数の照合順序プロパティをアンダースコア ( `_` ) で区切って名前に含めることができます。

次の表は、一般的な照合順序プロパティと意味を示しています。

| 照合プロパティ       | 意味                                    |
| ------------- | ------------------------------------- |
| `_bin`        | バイナリ                                  |
| `_ci`         | 大文字と小文字を区別しない                         |
| `_ai_ci`      | アクセント、大文字と小文字を区別しない                   |
| `_0900_bin`   | Unicode UCA 9.0.0、バイナリ                |
| `_unicode_ci` | （古い）Unicode UCA照合順序、大文字と小文字を区別しない     |
| `_general_ci` | Unicode照合順序はそれほど厳密ではなく、大文字と小文字を区別しません |

## TiDB でサポートされている文字セットと照合順序 {#character-sets-and-collations-supported-by-tidb}

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
| gbk     | Chinese Internal Code Specification | gbk_chinese_ci    |      2 |
| latin1  | Latin1                              | latin1_bin        |      1 |
| utf8    | UTF-8 Unicode                       | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode                       | utf8mb4_bin       |      4 |
+---------+-------------------------------------+-------------------+--------+
6 rows in set (0.00 sec)
```

TiDB は次の照合をサポートしています。

```sql
SHOW COLLATION;
```

```sql
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
| binary             | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 | PAD SPACE     |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 | PAD SPACE     |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       8 | PAD SPACE     |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
13 rows in set (0.00 sec)
```

> **警告：**
>
> TiDBはlatin1をutf8のサブセットとして誤って扱います。そのため、latin1とutf8のエンコーディング間で異なる文字を格納すると、予期しない動作が発生する可能性があります。utf8mb4文字セットの使用を強くお勧めします。詳細は[TiDB #18955](https://github.com/pingcap/tidb/issues/18955)ご覧ください。

> **注記：**
>
> TiDBのデフォルトの照合順序（サフィックスが`_bin`であるバイナリ照合順序）は、 [MySQLのデフォルトの照合順序](https://dev.mysql.com/doc/refman/8.0/en/charset-charsets.html) （サフィックスが`_general_ci`または`_ai_ci`である一般的な照合順序）とは異なります。そのため、明示的に文字セットを指定しても暗黙的にデフォルトの照合照合順序が選択されることに依存する場合、互換性のない動作が発生する可能性があります。
>
> ただし、TiDB のデフォルトの照合順序は、クライアントの[接続照合順序](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)設定にも影響されます。例えば、MySQL 8.x クライアントでは、 `utf8mb4`文字セットの接続照合順序はデフォルトで`utf8mb4_0900_ai_ci`に設定されています。
>
> -   TiDB v7.4.0 より前では、クライアントが`utf8mb4_0900_ai_ci` [接続照合順序](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)として使用すると、TiDB は`utf8mb4_0900_ai_ci`照合順序をサポートしていないため、TiDB は TiDBサーバーのデフォルトの照合照合順序`utf8mb4_bin`使用します。
> -   v7.4.0 以降、クライアントが[接続照合順序](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)として`utf8mb4_0900_ai_ci`使用する場合、TiDB はクライアントの構成に従って、デフォルトの照合順序として`utf8mb4_0900_ai_ci`使用します。

次のステートメントを使用すると、文字セットに対応する照合順序 ( [照合のための新しいフレームワーク](#new-framework-for-collations)下) を表示できます。

```sql
SHOW COLLATION WHERE Charset = 'utf8mb4';
```

```sql
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
5 rows in set (0.001 sec)
```

GBK 文字セットの TiDB サポートの詳細については、 [GBK](/character-set-gbk.md)参照してください。

## TiDB の<code>utf8</code>と<code>utf8mb4</code> {#code-utf8-code-and-code-utf8mb4-code-in-tidb}

MySQLでは、文字セット`utf8`最大3バイトに制限されています。これは基本多言語面（BMP）の文字を格納するには十分ですが、絵文字などの文字を格納するには不十分です。新規インストールの場合は、文字セット`utf8mb4`使用し、文字セット`utf8`から移行することをお勧めします。

MySQL と TiDB の両方で、 `utf8`と`utf8mb3`同じ文字セットのエイリアスです。

TiDBはデフォルトで、文字セット`utf8`を最大3バイトに制限しています。これは、TiDBで作成されたデータがMySQLで安全に復元できることを保証するためです。システム変数[`tidb_check_mb4_value_in_utf8`](/system-variables.md#tidb_check_mb4_value_in_utf8)の値を`OFF`に変更することで、この制限を無効にすることができます。ただし、完全なUnicodeサポートと高い互換性のためには、代わりに`utf8mb4`使用することをお勧めします。

以下は、4バイトの絵文字をテーブルに挿入する際のデフォルトの動作を示しています。1 `INSERT`文は`utf8`文字セットでは失敗しますが、 `utf8mb4`の文では成功します。

```sql
CREATE TABLE utf8_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8;
```

    Query OK, 0 rows affected (0.09 sec)

```sql
CREATE TABLE utf8m4_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8mb4;
```

    Query OK, 0 rows affected (0.09 sec)

```sql
INSERT INTO utf8_test VALUES ('😉');
```

    ERROR 1366 (HY000): incorrect utf8 value f09f9889(😉) for column c

```sql
INSERT INTO utf8m4_test VALUES ('😉');
```

    Query OK, 1 row affected (0.02 sec)

```sql
SELECT char_length(c), length(c), c FROM utf8_test;
```

    Empty set (0.01 sec)

```sql
SELECT char_length(c), length(c), c FROM utf8m4_test;
```

    +----------------+-----------+------+
    | char_length(c) | length(c) | c    |
    +----------------+-----------+------+
    |              1 |         4 | 😉     |
    +----------------+-----------+------+
    1 row in set (0.00 sec)

## 異なるレイヤーでの文字セットと照合順序 {#character-set-and-collation-in-different-layers}

文字セットと照合順序は異なるレイヤーで設定できます。

### データベースの文字セットと照合順序 {#database-character-set-and-collation}

各データベースには文字セットと照合順序があります。次の文を使用して、データベースの文字セットと照合順序を指定できます。

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

ここで`DATABASE` `SCHEMA`に置き換えることができます。

データベースによって文字セットと照合順序が異なる場合があります。現在のデータベースの文字セットと照合順序を確認するには、 `character_set_database`と`collation_database`使用します。

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

`INFORMATION_SCHEMA`には次の 2 つの値も表示されます。

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

### 表の文字セットと照合順序 {#table-character-set-and-collation}

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

テーブルの文字セットと照合順序が指定されていない場合、データベースの文字セットと照合順序がデフォルト値として使用されます。照合順序を指定せずに文字セットのみを`utf8mb4`と指定した場合、照合順序はシステム変数[`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740)値によって決定されます。

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

列の文字セットと照合順序が指定されていない場合、テーブルの文字セットと照合順序がデフォルト値として使用されます。照合順序を指定せずに文字セットのみを`utf8mb4`に指定した場合、照合順序はシステム変数[`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740)値によって決定されます。

### 文字列の文字セットと照合順序 {#string-character-sets-and-collation}

各文字列は文字セットと照合順序に対応しています。文字列を使用する場合、このオプションが利用可能です。

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

-   ルール 1: `CHARACTER SET charset_name`と`COLLATE collation_name`指定すると、 `charset_name`文字セットと`collation_name`照合順序が直接使用されます。
-   ルール 2: `CHARACTER SET charset_name`指定して`COLLATE collation_name`指定しない場合は、 `charset_name`文字セットとデフォルトの照合順序`charset_name`が使用されます。
-   ルール 3: `CHARACTER SET charset_name`も`COLLATE collation_name`指定しない場合は、システム変数`character_set_connection`と`collation_connection`で指定された文字セットと照合順序が使用されます。

### クライアント接続の文字セットと照合順序 {#client-connection-character-set-and-collation}

-   サーバーの文字セットと照合順序は、システム変数`character_set_server`と`collation_server`の値です。

-   デフォルト データベースの文字セットと照合順序は、システム変数`character_set_database`と`collation_database`の値です。

`character_set_connection`と`collation_connection` 、各接続の文字セットと照合順序を指定するために使用できます。5 `character_set_client` 、クライアントの文字セットを設定するための変数です。

結果を返す前に、 `character_set_results`システム変数は、結果のメタデータを含む、サーバーがクライアントにクエリ結果を返す文字セットを示します。

次のステートメントを使用して、クライアントに関連する文字セットと照合順序を設定できます。

-   `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES` 、クライアントがサーバーに SQL ステートメントを送信するために使用する文字セットを示します。2 `SET NAMES utf8mb4` 、クライアントからのすべてのリクエストとサーバーからの結果に utf8mb4 が使用されることを示します。

    `SET NAMES 'charset_name'`文は次の文の組み合わせと同等です。

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE`はオプションです。指定しない場合は、デフォルトの照合順序`charset_name`を使用して`collation_connection`設定されます。

-   `SET CHARACTER SET 'charset_name'`

    `SET NAMES`と同様に、 `SET NAMES 'charset_name'`ステートメントは次のステートメントの組み合わせと同等です。

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection=@@character_set_database;
    SET collation_connection = @@collation_database;
    ```

## 文字セットと照合順序の選択優先順位 {#selection-priorities-of-character-sets-and-collations}

文字列 &gt;カラム&gt; テーブル &gt; データベース &gt; サーバー

## 文字セットと照合順序の選択に関する一般的なルール {#general-rules-on-selecting-character-sets-and-collation}

-   ルール 1: `CHARACTER SET charset_name`と`COLLATE collation_name`指定すると、 `charset_name`文字セットと`collation_name`照合順序が直接使用されます。
-   ルール 2: `CHARACTER SET charset_name`指定し、 `COLLATE collation_name`指定しない場合は、 `charset_name`文字セットとデフォルトの照合順序`charset_name`が使用されます。
-   ルール 3: `CHARACTER SET charset_name`も`COLLATE collation_name`も指定しない場合は、最適化レベルが高い文字セットと照合順序が使用されます。

## 文字の有効性チェック {#validity-check-of-characters}

指定された文字セットが`utf8`または`utf8mb4`場合、TiDB は有効な`utf8`文字のみをサポートします。無効な文字の場合、TiDB は`incorrect utf8 value`エラーを報告します。TiDB のこの文字の有効性チェックは MySQL 8.0 と互換性がありますが、 MySQL 5.7以前のバージョンとは互換性がありません。

このエラー報告を無効にするには、 `set @@tidb_skip_utf8_check=1;`使用して文字チェックをスキップします。

> **注記：**
>
> 文字チェックを省略すると、TiDBはアプリケーションによって書き込まれた不正なUTF-8文字を検出できず、 `ANALYZE`実行時にデコードエラーが発生し、その他の未知のエンコード問題が発生する可能性があります。アプリケーションが書き込まれた文字列の有効性を保証できない場合は、文字チェックを省略することは推奨されません。

## 照合サポートフレームワーク {#collation-support-framework}

<CustomContent platform="tidb">

照合順序の構文サポートとセマンティックサポートは、 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)設定項目の影響を受けます。構文サポートとセマンティックサポートは異なります。前者は、TiDB が照合順序を解析および設定できることを示します。後者は、TiDB が文字列の比較時に照合順序を正しく使用できることを示します。

</CustomContent>

v4.0 より前のバージョンでは、 TiDB は[照合のための古いフレームワーク](#old-framework-for-collations)のみを提供していました。このフレームワークでは、 TiDB は MySQL 照合順序のほとんどを構文的に解析することをサポートしていますが、意味的にはすべての照合順序をバイナリ照合順序として扱います。

TiDBはv4.0以降、 [照合のための新しいフレームワーク](#new-framework-for-collations)サポートしています。このフレームワークでは、TiDBは異なる照合順序を意味的に解析し、文字列を比較する際には照合順序に厳密に従います。

### 照合のための古いフレームワーク {#old-framework-for-collations}

v4.0より前のバージョンでは、TiDBでMySQLのほとんどの照合順序を指定でき、これらの照合順序はデフォルトの照合順序に従って処理されます。つまり、バイト順序によって文字順序が決定されます。MySQLとは異なり、TiDBは文字末尾のスペースを処理しないため、以下の動作の違いが生じます。

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

TiDBでは、上記の文は正常に実行されます。MySQLでは、 `utf8mb4_general_ci`大文字と小文字を区別しないため、 `Duplicate entry 'a'`エラーが報告されます。

```sql
INSERT INTO t1 VALUES ('a ');
```

```sql
Query OK, 1 row affected
```

TiDBでは、上記の文は正常に実行されます。MySQLでは、スペースを埋めてから比較が行われるため、エラー`Duplicate entry 'a '`が返されます。

### 照合のための新しいフレームワーク {#new-framework-for-collations}

TiDB v4.0 以降では、照合のための完全なフレームワークが導入されています。

<CustomContent platform="tidb">

この新しいフレームワークは、照合順序の意味解析をサポートし、クラスターの初回初期化時に新しいフレームワークを有効にするかどうかを決定するための設定項目`new_collations_enabled_on_first_bootstrap`導入しました。新しいフレームワークを有効にするには、 `new_collations_enabled_on_first_bootstrap`を`true`に設定します。詳細については、 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)参照してください。

すでに初期化されている TiDB クラスターの場合、 `mysql.tidb`テーブルの`new_collation_enabled`変数を通じて新しい照合順序が有効になっているかどうかを確認できます。

> **注記：**
>
> `mysql.tidb`テーブルのクエリ結果が`new_collations_enabled_on_first_bootstrap`の値と異なる場合、 `mysql.tidb`テーブルの結果が実際の値になります。

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

この新しいフレームワークは、照合順序の意味的な解析をサポートします。TiDB は、クラスターが最初に初期化されるときに、この新しいフレームワークをデフォルトで有効にします。

</CustomContent>

新しいフレームワークでは、TiDB は MySQL と互換性のある`utf8_general_ci` 、 `utf8mb4_general_ci` 、 `utf8_unicode_ci` 、 `utf8mb4_unicode_ci` 、 `utf8mb4_0900_bin` 、 `utf8mb4_0900_ai_ci` 、 `gbk_chinese_ci` 、および`gbk_bin`照合をサポートします。

`utf8_general_ci` 、 `utf8mb4_general_ci` 、 `utf8_unicode_ci` 、 `utf8mb4_unicode_ci` 、 `utf8mb4_0900_ai_ci` 、 `gbk_chinese_ci`のいずれかが使用される場合、文字列比較は大文字と小文字を区別せず、アクセントも区別しません。同時に、TiDBは照合順序の`PADDING`動作も修正します。

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
ERROR 1062 (23000): Duplicate entry 'a' for key 't.PRIMARY' -- TiDB is compatible with the case-insensitive collation of MySQL.
```

```sql
INSERT INTO t VALUES ('a ');
```

```sql
ERROR 1062 (23000): Duplicate entry 'a ' for key 't.PRIMARY' -- TiDB modifies the `PADDING` behavior to be compatible with MySQL.
```

> **注記：**
>
> TiDBにおけるパディングの実装はMySQLとは異なります。MySQLでは、パディングはスペースを埋めることで実装されます。TiDBでは、パディングは末尾のスペースを切り取ることで実装されます。2つのアプローチはほとんどの場合同じです。唯一の例外は、文字列の末尾にスペース（0x20）未満の文字が含まれている場合です。例えば、TiDBでは`'a' < 'a\t'`の結果は`1`なりますが、MySQLでは`'a' < 'a\t'` `'a ' < 'a\t'`と同等であり、結果は`0`なります。

## 式内の照合順序の強制値 {#coercibility-values-of-collations-in-expressions}

式に異なる照合順序を持つ複数の節が含まれる場合、計算で使用される照合順序を推測する必要があります。そのルールは以下のとおりです。

-   明示的な`COLLATE`節の強制可能性値は`0`です。
-   2 つの文字列の照合順序に互換性がない場合は、異なる照合順序を持つ 2 つの文字列の連結の強制可能性値は`1`なります。
-   列の照合順序`CAST()` 、 `CONVERT()` 、または`BINARY()`の強制値は`2`です。
-   システム定数 ( `USER ()`または`VERSION ()`によって返される文字列) の強制値は`3`です。
-   定数の強制値は`4`です。
-   数値または中間変数の強制値は`5`です。
-   `NULL`または`NULL`から派生した式の強制値は`6`です。

TiDBは照合順序を推論する際に、強制性値の低い式の照合順序を優先的に使用します。2つの句の強制性値が同じ場合、以下の優先順位に従って照合順序が決定されます。

バイナリ &gt; utf8mb4_bin &gt; (utf8mb4_general_ci = utf8mb4_unicode_ci) &gt; utf8_bin &gt; (utf8_general_ci = utf8_unicode_ci) &gt; latin1_bin &gt; ascii_bin

次の状況では、TiDB は照合順序を推測できず、エラーを報告します。

-   2 つの句の照合順序が異なり、両方の句の強制可能性値が`0`場合。
-   2 つの句の照合順序に互換性がなく、返される式の型が`String`場合。

## <code>COLLATE</code>句 {#code-collate-code-clause}

TiDBは、式の照合順序を指定するために`COLLATE`句の使用をサポートしています。この式の強制値は`0` 、これが最高の優先度です。次の例をご覧ください。

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

詳細については[接続文字セットと照合順序](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html)参照してください。
