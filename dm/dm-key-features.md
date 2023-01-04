---
title: Key Features of TiDB Data Migration
summary: Learn about the key features of DM and appropriate parameter configurations.
---

# TiDB データ移行の主な機能 {#key-features-of-tidb-data-migration}

このドキュメントでは、TiDB Data Migration (DM) によって提供されるデータ移行機能について説明し、適切なパラメーター構成を紹介します。

DM のバージョンが異なると、テーブル ルーティング、ブロック リストと許可リスト、binlog イベント フィルター機能でスキーマまたはテーブル名の一致ルールが異なることに注意してください。

-   DM v1.0.5 以降のバージョンでは、上記のすべての機能が[ワイルドカードマッチ](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)をサポートしています。 DM のすべてのバージョンで、ワイルドカード式に使用できる`*`は**1 つだけ**<strong>であり、最後に</strong>`*`を配置する必要があることに注意してください。
-   v1.0.5 より前の DM バージョンでは、テーブル ルーティングと binlog イベント フィルターはワイルドカードをサポートしますが、 `[...]`と`[!...]`の式はサポートしません。ブロック &amp; 許可リストは、正規表現のみをサポートしています。

単純なシナリオでのマッチングには、ワイルドカードを使用することをお勧めします。

## テーブル ルーティング {#table-routing}

テーブル ルーティング機能により、DM は上流の MySQL または MariaDB インスタンスの特定のテーブルを下流の指定されたテーブルに移行できます。

> **ノート：**
>
> -   1 つのテーブルに対して複数の異なるルーティング ルールを構成することはサポートされていません。
> -   スキーマの一致ルールは、 [パラメータ構成](#parameter-configuration)の`rule-2`に示すように、移行`CREATE/DROP SCHEMA xx`に使用される個別に構成する必要があります。

### パラメータ構成 {#parameter-configuration}

```yaml
routes:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
    # extract-table, extract-schema, and extract-source are optional and are required only when you need to extract information about sharded tables, sharded schemas, and source datatabase information.
    extract-table:
      table-regexp: "t_(.*)"
      target-column: "c_table"
    extract-schema:
      schema-regexp: "test_(.*)"
      target-column: "c_schema"
    extract-source:
      source-regexp: "(.*)"
      target-column: "c_source"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

### パラメータの説明 {#parameter-explanation}

-   DM は、 [テーブル セレクターによって提供される`schema-pattern` / <code>table-pattern</code>ルール](/dm/table-selector.md)に一致する上流の MySQL または MariaDB インスタンス テーブルを下流の`target-schema` / `target-table`に移行します。
-   `schema-pattern`ルールに一致するシャード テーブルの場合、DM は`table-pattern`を使用してテーブル名を抽出し`extract-table` 。 `table-regexp`正規表現、 `extract-schema`を使用したスキーマ名。 `schema-regexp`正規表現、および`extract-source`を使用したソース情報。 `source-regexp`正規表現。次に、DM は、抽出された情報を下流のマージされたテーブルの対応する`target-column`に書き込みます。

### 使用例 {#usage-examples}

このセクションでは、さまざまなシナリオでの使用例を示します。

#### シャードされたスキーマとテーブルをマージする {#merge-sharded-schemas-and-tables}

シャードされたスキーマとテーブルのシナリオで、 `test_{1,2,3...}`を移行すると仮定します。 `test`への 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`のテーブル。ダウンストリーム TiDB インスタンスの`t`テーブル。

アップストリーム インスタンスをダウンストリームに移行するには`test` . `t`では、次のルーティング ルールを作成する必要があります。

-   `rule-1`は、 `schema-pattern: "test_*"`と`table-pattern: "t_*"`に一致するテーブルの DML または DDL ステートメントをダウンストリーム`test`に移行するために使用されます。 `t` .
-   `rule-2`は、 `CREATE/DROP SCHEMA xx`などの`schema-pattern: "test_*"`に一致するスキーマの DDL ステートメントを移行するために使用されます。

> **ノート：**
>
> -   ダウンストリーム`schema: test`が既に存在し、削除しない場合は、 `rule-2`を省略できます。
> -   ダウンストリーム`schema: test`が存在せず、 `rule-1`のみが構成されている場合、移行中に`schema test doesn't exist`エラーが報告されます。

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

#### テーブル、スキーマ、およびソース情報を抽出し、マージされたテーブルに書き込みます {#extract-table-schema-and-source-information-and-write-into-the-merged-table}

シャードされたスキーマとテーブルのシナリオで、 `test_{1,2,3...}`を移行すると仮定します。 `test`への 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`のテーブル。ダウンストリーム TiDB インスタンスの`t`テーブル。同時に、シャードされたテーブルのソース情報を抽出し、それをダウンストリームのマージされたテーブルに書き込みたいと考えています。

アップストリーム インスタンスをダウンストリームに移行するには`test` . `t`では、前のセクション[シャードされたスキーマとテーブルをマージする](#merge-sharded-schemas-and-tables)と同様のルーティング ルールを作成する必要があります。さらに、 `extract-table` 、 `extract-schema` 、および`extract-source`構成を追加する必要があります。

-   `extract-table` : `schema-pattern`と`table-pattern`に一致するシャード テーブルの場合、DM は`table-regexp`を使用してシャード テーブル名を抽出し、マージされたテーブルの`target-column` 、つまり`c_table`列に`t_`の部分を除いた名前サフィックスを書き込みます。
-   `extract-schema` : `schema-pattern`と`table-pattern`に一致するシャード スキーマの場合、DM は`schema-regexp`を使用してシャード スキーマ名を抽出し、マージされたテーブルの`target-column` 、つまり`c_schema`列に`test_`の部分を除いた名前サフィックスを書き込みます。
-   `extract-source` : `schema-pattern`と`table-pattern`が一致するシャード テーブルの場合、DM はソース インスタンス情報をマージされたテーブルの`target-column` 、つまり`c_source`列に書き込みます。

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
    extract-table:
      table-regexp: "t_(.*)"
      target-column: "c_table"
    extract-schema:
      schema-regexp: "test_(.*)"
      target-column: "c_schema"
    extract-source:
      source-regexp: "(.*)"
      target-column: "c_source"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

アップストリームのシャード テーブルのソース情報をダウンストリームのマージされたテーブルに抽出する**には、移行を開始する前に、ダウンストリームでマージされたテーブルを手動で作成する必要があります**。結合されたテーブルには、ソース情報の指定に使用される 3 つの`target-columns` ( `c_table` 、 `c_schema` 、および`c_source` ) が含まれている必要があります。さらに、これらの列<strong>は最後の列であり、<a href="/data-type-string.md">文字列型</a>である必要があります</strong>。

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

アップストリームに次の 2 つのデータ ソースがあるとします。

データ ソース`mysql-01` :

```sql
mysql> select * from test_11.t_1;
+---+
| a |
+---+
| 1 |
+---+
mysql> select * from test_11.t_2;
+---+
| a |
+---+
| 2 |
+---+
mysql> select * from test_12.t_1;
+---+
| a |
+---+
| 3 |
+---+
```

データ ソース`mysql-02` :

```sql
mysql> select * from test_13.t_3;
+---+
| a |
+---+
| 4 |
+---+
```

DM を使用して移行した後、マージされたテーブルのデータは次のようになります。

```sql
mysql> select * from test.t;
+---+---------+----------+----------+
| a | c_table | c_schema | c_source |
+---+---------+----------+----------+
| 1 | 1       | 11       | mysql-01 |
| 2 | 2       | 11       | mysql-01 |
| 3 | 1       | 12       | mysql-01 |
| 4 | 3       | 13       | mysql-02 |
+---+---------+----------+----------+
```

##### マージされたテーブルを作成する間違った例 {#incorrect-examples-of-creating-merged-tables}

> **ノート：**
>
> 以下のいずれかのエラーが発生した場合、シャード テーブルおよびスキーマのソース情報がマージ テーブルに書き込まれない可能性があります。

-   最後の 3 列に`c-table`はありません。

```sql
CREATE TABLE `test`.`t` (
    c_table varchar(10) DEFAULT NULL,
    a int(11) PRIMARY KEY,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

-   `c-source`は存在しません:

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
);
```

-   `c_schema`は文字列型ではありません:

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema int(11) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL,
);
```

#### シャードされたスキーマをマージする {#merge-sharded-schemas}

シャード スキーマのシナリオで、 `test_{1,2,3...}`を移行すると仮定します。 2 つのアップストリーム MySQL インスタンスの`t_{1,2,3...}`のテーブルから`test` .ダウンストリームの TiDB インスタンスに`t_{1,2,3...}`のテーブル。

アップストリーム スキーマをダウンストリームに移行するには`test` . `t_[1,2,3]`では、ルーティング ルールを 1 つだけ作成する必要があります。

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

#### 不適切なテーブル ルーティング {#incorrect-table-routing}

次の 2 つのルーティング ルールが構成されていると仮定し`test_1_bak` 。 `t_1_bak`が`rule-1`と`rule-2`の両方に一致する場合、テーブル ルーティング構成が数の制限に違反しているため、エラーが報告されます。

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_1_bak"
    table-pattern: "t_1_bak"
    target-schema: "test"
    target-table: "t_bak"
```

## テーブル リストのブロックと許可 {#block-and-allow-table-lists}

アップストリーム データベース インスタンス テーブルのブロック リストと許可リストのフィルタリング ルールは、MySQL の replication-rules-db/tables に似ており、一部のデータベースまたは一部のテーブルのすべての操作をフィルタリングまたは移行するために使用できます。

### パラメータ構成 {#parameter-configuration}

```yaml
block-allow-list:             # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  rule-1:
    do-dbs: ["test*"]         # Starting with characters other than "~" indicates that it is a wildcard;
                              # v1.0.5 or later versions support the regular expression rules.
    do-tables:
    - db-name: "test[123]"    # Matches test1, test2, and test3.
      tbl-name: "t[1-5]"      # Matches t1, t2, t3, t4, and t5.
    - db-name: "test"
      tbl-name: "t"
  rule-2:
    do-dbs: ["~^test.*"]      # Starting with "~" indicates that it is a regular expression.
    ignore-dbs: ["mysql"]
    do-tables:
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "test"
      tbl-name: "t"
    ignore-tables:
    - db-name: "test"
      tbl-name: "log"
```

### パラメータの説明 {#parameter-explanation}

-   `do-dbs` : スキーマのリストの移行を許可します。MySQL の[`replicate-do-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-db)と同様です。
-   `ignore-dbs` : 移行するスキーマのブロック リスト。MySQL の[`replicate-ignore-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-db)に似ています。
-   `do-tables` : MySQL の[`replicate-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-table)と同様に、テーブルのリストの移行を許可します。 `db-name`と`tbl-name`の両方を指定する必要があります
-   `ignore-tables` : 移行するテーブルのブロック リスト。MySQL の[`replicate-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-table)に似ています。 `db-name`と`tbl-name`の両方を指定する必要があります

上記のパラメーターの値が`~`文字で始まる場合、この値の後続の文字は[正規表現](https://golang.org/pkg/regexp/syntax/#hdr-syntax)として扱われます。このパラメーターを使用して、スキーマまたはテーブル名を一致させることができます。

### フィルタリングプロセス {#filtering-process}

`do-dbs`と`ignore-dbs`に対応するフィルタリング ルールは、MySQL の[データベース レベルのレプリケーションおよびバイナリ ログ オプションの評価](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html)に似ています。 `do-tables`と`ignore-tables`に対応するフィルタリング ルールは、MySQL の[テーブル レベルのレプリケーション オプションの評価](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-table-options.html)に似ています。

> **ノート：**
>
> DM と MySQL では、許可リストとブロック リストのフィルタリング ルールは次の点で異なります。
>
> -   MySQL では、 [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-do-table)と[`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table)はワイルドカード文字をサポートしています。 DM では、一部のパラメーター値は、 `~`文字で始まる正規表現を直接サポートしています。
> -   DM は現在、 `ROW`形式のバイナリログのみをサポートしており、 `STATEMENT`または`MIXED`形式のバイナリログはサポートしていません。したがって、DM のフィルタリング ルールは、MySQL の`ROW`形式のフィルタリング ルールに対応します。
> -   MySQL は、ステートメントの`USE`セクションで明示的に指定されたデータベース名によってのみ DDL ステートメントを決定します。 DM は、最初に DDL ステートメントのデータベース名セクションに基づいてステートメントを決定します。 DDL ステートメントにそのようなセクションが含まれていない場合、DM は`USE`セクションによってステートメントを判別します。判別する SQL ステートメントが`USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`であるとします。 `replicate-do-db=test_db_1`は MySQL で構成され、 `do-dbs: ["test_db_1"]`は DM で構成されます。次に、このルールは DM にのみ適用され、MySQL には適用されません。

フィルタリング プロセスは次のとおりです。

1.  スキーマ レベルでフィルター処理します。

    -   `do-dbs`が空でない場合、一致するスキーマが`do-dbs`に存在するかどうかを判断します。

        -   はいの場合は、引き続きテーブル レベルでフィルタリングします。
        -   そうでない場合は、フィルタ`test`を使用します。 `t` .

    -   `do-dbs`が空で`ignore-dbs`が空でない場合、 `ignore-dbs`で一致するスキーマが存在するかどうかを判断します。

        -   はいの場合、フィルター`test` 。 `t` .
        -   そうでない場合は、引き続きテーブル レベルでフィルタリングします。

    -   `do-dbs`と`ignore-dbs`の両方が空の場合は、引き続きテーブル レベルでフィルタリングします。

2.  テーブル レベルでフィルター処理します。

    1.  `do-tables`が空でない場合、 `do-tables`に一致するテーブルが存在するかどうかを判断します。

        -   はいの場合は、移行`test`します。 `t` .
        -   そうでない場合は、フィルタ`test`を使用します。 `t` .

    2.  `ignore-tables`が空でない場合、 `ignore-tables`に一致するテーブルが存在するかどうかを判断します。

        -   はいの場合、フィルター`test` 。 `t` .
        -   そうでない場合は、移行`test`します。 `t` .

    3.  `do-tables`と`ignore-tables`の両方が空の場合は、 `test`を移行します。 `t` .

> **ノート：**
>
> スキーマ`test`をフィルタリングする必要があるかどうかを判断するには、スキーマ レベルでフィルタリングするだけで済みます。

### 使用例 {#usage-example}

アップストリームの MySQL インスタンスに次のテーブルが含まれているとします。

```
`logs`.`messages_2016`
`logs`.`messages_2017`
`logs`.`messages_2018`
`forum`.`users`
`forum`.`messages`
`forum_backup_2016`.`messages`
`forum_backup_2017`.`messages`
`forum_backup_2018`.`messages`
```

構成は次のとおりです。

```yaml
block-allow-list:  # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  bw-rule:
    do-dbs: ["forum_backup_2018", "forum"]
    ignore-dbs: ["~^forum_backup_"]
    do-tables:
    - db-name: "logs"
      tbl-name: "~_2018$"
    - db-name: "~^forum.*"
​      tbl-name: "messages"
    ignore-tables:
    - db-name: "~.*"
​      tbl-name: "^messages.*"
```

`bw-rule`ルールを使用した後:

| テーブル                             | フィルタリングするかどうか | フィルタリングする理由                                                                                                                                                |
| :------------------------------- | :------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `logs` . `messages_2016`         | はい            | スキーマ`logs`はどの`do-dbs`とも一致しません。                                                                                                                             |
| `logs` . `messages_2017`         | はい            | スキーマ`logs`はどの`do-dbs`とも一致しません。                                                                                                                             |
| `logs` . `messages_2018`         | はい            | スキーマ`logs`はどの`do-dbs`とも一致しません。                                                                                                                             |
| `forum_backup_2016` . `messages` | はい            | スキーマ`forum_backup_2016`はどの`do-dbs`とも一致しません。                                                                                                                |
| `forum_backup_2017` . `messages` | はい            | スキーマ`forum_backup_2017`はどの`do-dbs`とも一致しません。                                                                                                                |
| `forum` . `users`                | はい            | <li>スキーマ`forum`は`do-dbs`に一致し、引き続きテーブル レベルでフィルタリングします。<br/> 2. スキーマとテーブルは`do-tables`と`ignore-tables`のいずれとも一致せず、 `do-tables`は空ではありません。</li>                  |
| `forum` . `messages`             | いいえ           | <li>スキーマ`forum`は`do-dbs`に一致し、引き続きテーブル レベルでフィルタリングします。<br/> 2. 表`messages`は`do-tables`の`db-name: "~^forum.*",tbl-name: "messages"`の中にあります。</li>             |
| `forum_backup_2018` . `messages` | いいえ           | <li>スキーマ`forum_backup_2018`は`do-dbs`に一致し、引き続きテーブル レベルでフィルタリングします。<br/> 2. スキーマとテーブルは`db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`と一致します。</li> |

## Binlogイベント フィルター {#binlog-event-filter}

Binlogイベント フィルターは、ブロックおよび許可リストのフィルター処理ルールよりも細かいフィルター処理ルールです。 `INSERT`または`TRUNCATE TABLE`のようなステートメントを使用して、移行またはフィルターで除外する必要がある`schema/table`のバイナリログ イベントを指定できます。

> **ノート：**
>
> -   同じテーブルが複数のルールに一致する場合、これらのルールは順番に適用され、ブロック リストは許可リストよりも優先されます。これは、テーブルに`Ignore`と`Do`の両方のルールが適用されている場合、 `Ignore`のルールが有効になることを意味します。
> -   DM v2.0.2 以降では、ソース構成ファイルで binlog イベント フィルターを構成できます。詳細については、 [アップストリーム データベースConfiguration / コンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

### パラメータ構成 {#parameter-configuration}

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    ​table-pattern: "t_*"
    ​events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    ​action: Ignore
```

### パラメータの説明 {#parameter-explanation}

-   [`schema-pattern` / <code>table-pattern</code>](/dm/table-selector.md) : `schema-pattern` / `table-pattern`に一致する上流の MySQL または MariaDB インスタンス テーブルの binlog イベントまたは DDL SQL ステートメントは、以下のルールによってフィルター処理されます。

-   `events` : バイナリログ イベント配列。次の表から 1 つ以上の`Event`のみを選択できます。

    | イベント              | タイプ | 説明                         |
    | ----------------- | --- | -------------------------- |
    | `all`             |     | 以下のすべてのイベントが含まれます          |
    | `all dml`         |     | 以下のすべての DML イベントが含まれます     |
    | `all ddl`         |     | 以下のすべての DDL イベントが含まれます     |
    | `none`            |     | 以下のイベントは含まれません             |
    | `none ddl`        |     | 以下の DDL イベントは含まれません        |
    | `none dml`        |     | 以下の DML イベントは含まれません        |
    | `insert`          | DML | `INSERT` DML イベント          |
    | `update`          | DML | `UPDATE` DML イベント          |
    | `delete`          | DML | `DELETE` DML イベント          |
    | `create database` | DDL | `CREATE DATABASE` DDL イベント |
    | `drop database`   | DDL | `DROP DATABASE` DDL イベント   |
    | `create table`    | DDL | `CREATE TABLE` DDL イベント    |
    | `create index`    | DDL | `CREATE INDEX` DDL イベント    |
    | `drop table`      | DDL | `DROP TABLE` DDL イベント      |
    | `truncate table`  | DDL | `TRUNCATE TABLE` DDL イベント  |
    | `rename table`    | DDL | `RENAME TABLE` DDL イベント    |
    | `drop index`      | DDL | `DROP INDEX` DDL イベント      |
    | `alter table`     | DDL | `ALTER TABLE` DDL イベント     |

-   `sql-pattern` : 指定された DDL SQL ステートメントをフィルタリングするために使用されます。一致ルールは、正規表現の使用をサポートしています。たとえば、 `"^DROP\\s+PROCEDURE"`です。

-   `action` : 文字列 ( `Do` / `Ignore` )。以下のルールに基づいて、フィルタリングするかどうかを判断します。 2 つのルールのいずれかが満たされる場合、バイナリログはフィルタリングされます。それ以外の場合、バイナリログはフィルタリングされません。

    -   `Do` : 許可リスト。 binlog は、次の 2 つの条件のいずれかでフィルター処理されます。
        -   イベントのタイプがルールの`event`リストにありません。
        -   イベントの SQL ステートメントは、ルールの`sql-pattern`つと一致しません。
    -   `Ignore` : ブロック リスト。 binlog は、次の 2 つの条件のいずれかでフィルター処理されます。
        -   イベントのタイプは、ルールの`event`リストにあります。
        -   イベントの SQL ステートメントは、ルールの`sql-pattern`に一致できます。

### 使用例 {#usage-examples}

このセクションでは、シャーディングのシナリオ (シャードされたスキーマとテーブル) での使用例を示します。

#### すべてのシャーディング削除操作をフィルタリングする {#filter-all-sharding-deletion-operations}

すべての削除操作を除外するには、次の 2 つのフィルタリング ルールを構成します。

-   `filter-table-rule`は、 `drop table` `truncate table`および`delete statement`操作を除外し`test_*` 。 `t_*`パターン。
-   `filter-schema-rule`は、 `test_*`のパターンに一致するすべてのスキーマの`drop database`の操作を除外します。

```yaml
filters:
  filter-table-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  filter-schema-rule:
    schema-pattern: "test_*"
    events: ["drop database"]
    action: Ignore
```

#### シャーディング DML ステートメントのみを移行する {#only-migrate-sharding-dml-statements}

シャーディング DML ステートメントのみを移行するには、次の 2 つのフィルタリング ルールを構成します。

-   `do-table-rule`は、 `test_*`に一致するすべてのテーブルの`create table` 、 `insert` 、 `update` 、および`delete`ステートメントのみを移行します。 `t_*`パターン。
-   `do-schema-rule`は、 `test_*`パターンに一致するすべてのスキーマの`create database`ステートメントのみを移行します。

> **ノート：**
>
> `create database/table`ステートメントが移行される理由は、スキーマとテーブルが作成された後にのみ DML ステートメントを移行できるためです。

```yaml
filters:
  do-table-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["create table", "all dml"]
    action: Do
  do-schema-rule:
    schema-pattern: "test_*"
    events: ["create database"]
    action: Do
```

#### TiDB がサポートしていない SQL ステートメントを除外する {#filter-out-the-sql-statements-that-tidb-does-not-support}

TiDB がサポートしていない`PROCEDURE`ステートメントを除外するには、次の`filter-procedure-rule`を構成します。

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

`filter-procedure-rule`は、 `test_*`に一致するすべてのテーブルの`^CREATE\\s+PROCEDURE`および`^DROP\\s+PROCEDURE`ステートメントを除外します。 `t_*`パターン。

#### TiDB パーサーがサポートしていない SQL ステートメントを除外する {#filter-out-the-sql-statements-that-the-tidb-parser-does-not-support}

`table`パーサーがサポートしていない SQL ステートメントの場合、DM はそれらを解析して`schema`情報を取得できません。したがって、グローバル フィルタリング ルール`schema-pattern: "*"`を使用する必要があります。

> **ノート：**
>
> 移行する必要のあるデータを除外しないようにするには、グローバル フィルタリング ルールをできるだけ厳密に構成する必要があります。

TiDB パーサー (一部のバージョン) がサポートしていない`PARTITION`ステートメントを除外するには、次のフィルター規則を構成します。

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

## オンライン DDL ツール {#online-ddl-tools}

MySQL エコシステムでは、gh-ost や pt-osc などのツールが広く使用されています。 DM は、これらのツールをサポートして、不要な中間データの移行を回避します。

### 制限 {#restrictions}

-   DM は gh-ost と pt-osc のみをサポートします。
-   `online-ddl`が有効な場合、増分レプリケーションに対応するチェックポイントは、オンライン DDL 実行のプロセスにあってはなりません。たとえば、アップストリームのオンライン DDL 操作がバイナリログの`position-A`で開始し、 `position-B`で終了する場合、増分レプリケーションの開始点は`position-A`より前または`position-B`より後である必要があります。そうしないと、エラーが発生します。詳細は[FAQ](/dm/dm-faq.md#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-online-ddl-scheme-gh-ost-is-set)を参照してください。

### パラメータ構成 {#parameter-configuration}

<SimpleTab>
<div label="v2.0.5 and later">

v2.0.5 以降のバージョンでは、 `task`構成ファイルの`online-ddl`構成アイテムを使用する必要があります。

-   上流の MySQL/MariaDB が (同時に) gh-ost または pt-osc ツールを使用する場合は、タスク構成ファイルで`online-ddl`から`true`を設定します。

```yml
online-ddl: true
```

> **ノート：**
>
> v2.0.5 以降、 `online-ddl-scheme`は廃止されたため、 `online-ddl-scheme`の代わりに`online-ddl`を使用する必要があります。つまり、設定`online-ddl: true`は`online-ddl-scheme`を上書きし、設定`online-ddl-scheme: "pt"`または`online-ddl-scheme: "gh-ost"`は`online-ddl: true`に変換されます。

</div>

<div label="earlier than v2.0.5">

v2.0.5 より前 (v2.0.5 を除く) では、 `task`構成ファイルの`online-ddl-scheme`構成アイテムを使用する必要があります。

-   アップストリームの MySQL/MariaDB が gh-ost ツールを使用している場合は、タスク構成ファイルで設定します。

```yml
online-ddl-scheme: "gh-ost"
```

-   アップストリームの MySQL/MariaDB が pt ツールを使用している場合は、タスク構成ファイルで設定します。

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>

## シャードマージ {#shard-merge}

DM は、上流の MySQL/MariaDB シャード テーブルの DML および DDL データのマージと、マージされたデータの下流の TiDB テーブルへの移行をサポートします。

### 制限 {#restrictions}

現在、シャード マージ機能は限られたシナリオでのみサポートされています。詳細については、 [シャーディング DDL の使用悲観的モードでの制限事項](/dm/feature-shard-merge-pessimistic.md#restrictions)および[シャーディング DDL の使用法楽観的モードでの制限事項](/dm/feature-shard-merge-optimistic.md#restrictions)を参照してください。

### パラメータ構成 {#parameter-configuration}

タスク構成ファイルで`shard-mode`から`pessimistic`を設定します。

```
shard-mode: "pessimistic" # The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic" mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
```

### シャーディング DDL ロックを手動で処理する {#handle-sharding-ddl-locks-manually}

一部の異常なシナリオでは、 [シャーディング DDL ロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)する必要があります。
