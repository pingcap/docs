---
title: Key Features
summary: Learn about the key features of DM and appropriate parameter configurations.
---

# 主な機能 {#key-features}

このドキュメントでは、TiDBデータ移行（DM）によって提供されるデータ移行機能について説明し、適切なパラメーター構成を紹介します。

異なるDMバージョンの場合、テーブルルーティング、ブロックおよび許可リスト、およびbinlogイベントフィルター機能のスキーマ名またはテーブル名の異なる一致ルールに注意してください。

-   DM v1.0.5以降のバージョンでは、上記のすべての機能が[ワイルドカード一致](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)をサポートします。 DMのすべてのバージョンで、ワイルドカード式には`*`を**1つしか**含めることができず<strong>、最後に</strong>`*`を配置する必要があることに注意してください。
-   v1.0.5より前のバージョンのDMの場合、テーブルルーティングとbinlogイベントフィルターはワイルドカードをサポートしますが、 `[...]`および`[!...]`式はサポートしません。ブロック＆許可リストは正規表現のみをサポートします。

単純なシナリオでの照合には、ワイルドカードを使用することをお勧めします。

## テーブルルーティング {#table-routing}

テーブルルーティング機能により、DMはアップストリームのMySQLまたはMariaDBインスタンスの特定のテーブルをダウンストリームの指定されたテーブルに移行できます。

> **ノート：**
>
> -   1つのテーブルに複数の異なるルーティングルールを設定することはサポートされていません。
> -   スキーマの一致ルールは個別に構成する必要があります。これは、 [パラメータ設定](#parameter-configuration)つのうち`rule-2`に示すように、 `CREATE/DROP SCHEMA xx`を移行するために使用されます。

### パラメータ設定 {#parameter-configuration}

```yaml
routes:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

### パラメータの説明 {#parameter-explanation}

DMは、 [テーブルセレクターによって提供される`schema-pattern` / <code>table-pattern</code>ルール](/dm/table-selector.md)に一致するアップストリームのMySQLまたはMariaDBインスタンステーブルをダウンストリームの`target-schema`に移行し`target-table` 。

### 使用例 {#usage-examples}

このセクションでは、さまざまなシナリオでの使用例を示します。

#### シャーディングされたスキーマとテーブルをマージする {#merge-sharded-schemas-and-tables}

シャーディングされたスキーマとテーブルのシナリオで、 `test_{1,2,3...}`を移行するとします。 `test`への2つのアップストリームMySQLインスタンスの`t_{1,2,3...}`のテーブル。ダウンストリームTiDBインスタンスの`t`テーブル。

アップストリームインスタンスをダウンストリームに移行するには`test` 。 `t` 、次のルーティングルールを作成する必要があります。

-   `rule-1`は、 `schema-pattern: "test_*"`と`table-pattern: "t_*"`に一致するテーブルのDMLまたはDDLステートメントをダウンストリーム`test`に移行するために使用されます。 `t` 。
-   `rule-2`は、 `CREATE/DROP SCHEMA xx`などの`schema-pattern: "test_*"`に一致するスキーマのDDLステートメントを移行するために使用されます。

> **ノート：**
>
> -   ダウンストリーム`schema: test`がすでに存在し、削除しない場合は、 `rule-2`を省略できます。
> -   ダウンストリーム`schema: test`が存在せず、 `rule-1`だけが構成されている場合、移行中に`schema test doesn't exist`エラーが報告されます。

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

#### シャーディングされたスキーマをマージする {#merge-sharded-schemas}

シャーディングされたスキーマのシナリオで、 `test_{1,2,3...}`を移行するとします。 `test`への2つのアップストリームMySQLインスタンスの`t_{1,2,3...}`のテーブル。ダウンストリームTiDBインスタンスの`t_{1,2,3...}`のテーブル。

アップストリームスキーマをダウンストリーム`test`に移行するには。 `t_[1,2,3]` 、必要なルーティングルールは1つだけです。

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

#### 正しくないテーブルルーティング {#incorrect-table-routing}

次の2つのルーティングルールが構成されていると仮定し`test_1_bak` 。 `t_1_bak`は`rule-1`と`rule-2`の両方に一致します。テーブルルーティング構成が数の制限に違反しているため、エラーが報告されます。

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

## テーブルリストをブロックして許可する {#block-and-allow-table-lists}

アップストリームデータベースインスタンステーブルのブロックおよび許可リストフィルタリングルールは、MySQLレプリケーションルール-db /テーブルに似ています。これは、一部のデータベースまたは一部のテーブルのすべての操作をフィルタリングまたは移行するためにのみ使用できます。

### パラメータ設定 {#parameter-configuration}

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

-   `do-dbs` ：MySQLの[`replicate-do-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-db)と同様に、スキーマのリストを移行できるようにします
-   `ignore-dbs` ：MySQLの[`replicate-ignore-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-db)と同様に、移行するスキーマのブロックリスト
-   `do-tables` ：MySQLの[`replicate-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-table)と同様に、テーブルのリストを移行できるようにします。 `db-name`と`tbl-name`の両方を指定する必要があります
-   `ignore-tables` ：MySQLの[`replicate-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-table)と同様に、移行するテーブルのブロックリスト。 `db-name`と`tbl-name`の両方を指定する必要があります

上記のパラメータの値が`~`文字で始まる場合、この値の後続の文字は[正規表現](https://golang.org/pkg/regexp/syntax/#hdr-syntax)として扱われます。このパラメーターを使用して、スキーマ名またはテーブル名を照合できます。

### フィルタリングプロセス {#filtering-process}

`do-dbs`と`ignore-dbs`に対応するフィルタリングルールは、MySQLの[データベースレベルのレプリケーションとバイナリロギングオプションの評価](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html)に似ています。 `do-tables`と`ignore-tables`に対応するフィルタリングルールは、MySQLの[テーブルレベルのレプリケーションオプションの評価](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-table-options.html)に似ています。

> **ノート：**
>
> DMとMySQLでは、許可リストとブロックリストのフィルタリングルールは次の点で異なります。
>
> -   MySQLでは、 [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-do-table)と[`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table)はワイルドカード文字をサポートしています。 DMでは、一部のパラメーター値は、 `~`文字で始まる正規表現を直接サポートします。
> -   DMは現在、 `ROW`形式のbinlogのみをサポートしており、 `STATEMENT`または`MIXED`形式のbinlogはサポートしていません。したがって、DMのフィルタリングルールは、MySQLの`ROW`形式のフィルタリングルールに対応しています。
> -   MySQLは、ステートメントの`USE`セクションで明示的に指定されたデータベース名によってのみDDLステートメントを決定します。 DMは、最初にDDLステートメントのデータベース名セクションに基づいてステートメントを決定します。 DDLステートメントにそのようなセクションが含まれていない場合、DMは`USE`セクションによってステートメントを決定します。決定されるSQLステートメントが`USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`であると仮定します。 `replicate-do-db=test_db_1`はMySQLで構成され、 `do-dbs: ["test_db_1"]`はDMで構成されます。その場合、このルールはDMにのみ適用され、MySQLには適用されません。

フィルタリングプロセスは次のとおりです。

1.  スキーマレベルでのフィルター：

    -   `do-dbs`が空でない場合は、一致するスキーマが`do-dbs`に存在するかどうかを判断します。

        -   はいの場合は、引き続きテーブルレベルでフィルタリングします。
        -   そうでない場合は、フィルター`test` 。 `t` 。

    -   `do-dbs`が空で、 `ignore-dbs`が空でない場合は、一致したスキーマが`ignore-dbs`で終了するかどうかを判断します。

        -   はいの場合、フィルター`test` 。 `t` 。
        -   そうでない場合は、引き続きテーブルレベルでフィルタリングします。

    -   `do-dbs`と`ignore-dbs`の両方が空の場合は、テーブルレベルでフィルタリングを続行します。

2.  テーブルレベルでのフィルタリング：

    1.  `do-tables`が空でない場合は、一致するテーブルが`do-tables`に存在するかどうかを判断します。

        -   はいの場合、 `test`を移行します。 `t` 。
        -   そうでない場合は、フィルター`test` 。 `t` 。

    2.  `ignore-tables`が空でない場合は、一致するテーブルが`ignore-tables`に存在するかどうかを判断します。

        -   はいの場合、フィルター`test` 。 `t` 。
        -   そうでない場合は、 `test`を移行します。 `t` 。

    3.  `do-tables`と`ignore-tables`の両方が空の場合は、 `test`を移行します。 `t` 。

> **ノート：**
>
> スキーマ`test`をフィルタリングする必要があるかどうかを判断するには、スキーマレベルでフィルタリングするだけで済みます。

### 使用例 {#usage-example}

アップストリームのMySQLインスタンスに次のテーブルが含まれていると想定します。

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

`bw-rule`のルールを使用した後：

| テーブル                             | フィルタリングするかどうか | なぜフィルタリングするのか                                                                                                                                      |
| :------------------------------- | :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| `logs` 。 `messages_2016`         | はい            | スキーマ`logs`はどの`do-dbs`とも一致しません。                                                                                                                     |
| `logs` 。 `messages_2017`         | はい            | スキーマ`logs`はどの`do-dbs`とも一致しません。                                                                                                                     |
| `logs` 。 `messages_2018`         | はい            | スキーマ`logs`はどの`do-dbs`とも一致しません。                                                                                                                     |
| `forum_backup_2016` 。 `messages` | はい            | スキーマ`forum_backup_2016`はどの`do-dbs`とも一致しません。                                                                                                        |
| `forum_backup_2017` 。 `messages` | はい            | スキーマ`forum_backup_2017`はどの`do-dbs`とも一致しません。                                                                                                        |
| `forum` 。 `users`                | はい            | <li>スキーマ`forum`は`do-dbs`と一致し、テーブルレベルでフィルタリングを続行します。<br/> 2.スキーマとテーブルが`do-tables`と`ignore-tables`のいずれにも一致せず、 `do-tables`が空ではありません。</li>             |
| `forum` 。 `messages`             | いいえ           | <li>スキーマ`forum`は`do-dbs`と一致し、テーブルレベルでフィルタリングを続行します。<br/> 2.表`messages`は`do-tables`の`db-name: "~^forum.*",tbl-name: "messages"`にあります。</li>          |
| `forum_backup_2018` 。 `messages` | いいえ           | <li>スキーマ`forum_backup_2018`は`do-dbs`と一致し、テーブルレベルでフィルタリングを続行します。<br/> 2.スキーマとテーブルは`do-tables`と一致し`db-name: "~^forum.*",tbl-name: "messages"` 。</li> |

## Binlogイベントフィルター {#binlog-event-filter}

Binlogイベントフィルターは、ブロックおよび許可リストのフィルタリングルールよりもきめ細かいフィルタリングルールです。 `INSERT`や`TRUNCATE TABLE`などのステートメントを使用して、移行またはフィルターで除外する必要がある`schema/table`のbinlogイベントを指定できます。

> **ノート：**
>
> -   同じテーブルが複数のルールに一致する場合、これらのルールが順番に適用され、ブロックリストが許可リストよりも優先されます。これは、 `Ignore`と`Do`の両方のルールがテーブルに適用される場合、 `Ignore`のルールが有効になることを意味します。
> -   DM v2.0.2以降では、ソース構成ファイルでbinlogイベントフィルターを構成できます。詳細については、 [アップストリームデータベースConfiguration / コンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

### パラメータ設定 {#parameter-configuration}

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

-   [`schema-pattern` / <code>table-pattern</code>](/dm/table-selector.md) ： `schema-pattern`に一致するアップストリームMySQLまたはMariaDBインスタンステーブルの`table-pattern`イベントまたはDDL SQLステートメントは、以下のルールによってフィルタリングされます。

-   `events` ：binlogイベント配列。次の表から1つ以上の`Event`を選択することしかできません。

    | イベント              | タイプ | 説明                        |
    | ----------------- | --- | ------------------------- |
    | `all`             |     | 以下のすべてのイベントが含まれます         |
    | `all dml`         |     | 以下のすべてのDMLイベントが含まれます      |
    | `all ddl`         |     | 以下のすべてのDDLイベントが含まれます      |
    | `none`            |     | 以下のイベントは含まれていません          |
    | `none ddl`        |     | 以下のDDLイベントは含まれていません       |
    | `none dml`        |     | 以下のDMLイベントは含まれていません       |
    | `insert`          | DML | `INSERT`のDMLイベント          |
    | `update`          | DML | `UPDATE`のDMLイベント          |
    | `delete`          | DML | `DELETE`のDMLイベント          |
    | `create database` | DDL | `CREATE DATABASE`のDDLイベント |
    | `drop database`   | DDL | `DROP DATABASE`のDDLイベント   |
    | `create table`    | DDL | `CREATE TABLE`のDDLイベント    |
    | `create index`    | DDL | `CREATE INDEX`のDDLイベント    |
    | `drop table`      | DDL | `DROP TABLE`のDDLイベント      |
    | `truncate table`  | DDL | `TRUNCATE TABLE`のDDLイベント  |
    | `rename table`    | DDL | `RENAME TABLE`のDDLイベント    |
    | `drop index`      | DDL | `DROP INDEX`のDDLイベント      |
    | `alter table`     | DDL | `ALTER TABLE`のDDLイベント     |

-   `sql-pattern` ：指定されたDDLSQLステートメントをフィルタリングするために使用されます。マッチングルールは、正規表現の使用をサポートしています。たとえば、 `"^DROP\\s+PROCEDURE"` 。

-   `action` ：文字`Ignore` `Do` 。以下のルールに基づいて、フィルタリングするかどうかを判断します。 2つのルールのいずれかが満たされると、binlogがフィルタリングされます。それ以外の場合、binlogはフィルタリングされません。

    -   `Do` ：許可リスト。 binlogは、次の2つの条件のいずれかでフィルタリングされます。
        -   イベントのタイプは、ルールの`event`リストに含まれていません。
        -   イベントのSQLステートメントは、ルールの`sql-pattern`と一致することはできません。
    -   `Ignore` ：ブロックリスト。 binlogは、次の2つの条件のいずれかでフィルタリングされます。
        -   イベントのタイプは、ルールの`event`リストにあります。
        -   イベントのSQLステートメントは、ルールの`sql-pattern`つと一致させることができます。

### 使用例 {#usage-examples}

このセクションでは、シャーディング（シャーディングされたスキーマとテーブル）のシナリオでの使用例を示します。

#### すべてのシャーディング削除操作をフィルタリングする {#filter-all-sharding-deletion-operations}

すべての削除操作を除外するには、次の2つのフィルタリングルールを構成します。

-   `filter-table-rule`は、 `drop table` `truncate table`および`delete statement`の操作を除外し`test_*` 。 `t_*`パターン。
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

#### シャーディングDMLステートメントのみを移行する {#only-migrate-sharding-dml-statements}

シャーディングDMLステートメントのみを移行するには、次の2つのフィルタリングルールを構成します。

-   `do-table-rule`は、 `insert`に一致するすべてのテーブルの`create table` 、および`update` `test_*`のみを移行し`delete` 。 `t_*`パターン。
-   `do-schema-rule`は、 `test_*`パターンに一致するすべてのスキーマの`create database`ステートメントのみを移行します。

> **ノート：**
>
> `create database/table`ステートメントがマイグレーションされる理由は、スキーマとテーブルが作成された後にのみDMLステートメントをマイグレーションできるためです。

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

#### TiDBがサポートしていないSQLステートメントを除外します {#filter-out-the-sql-statements-that-tidb-does-not-support}

TiDBがサポートしていない`PROCEDURE`のステートメントを除外するには、次の`filter-procedure-rule`を構成します。

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

`filter-procedure-rule`は、 `test_*`に一致するすべてのテーブルの`^CREATE\\s+PROCEDURE`および`^DROP\\s+PROCEDURE`ステートメントを除外します。 `t_*`パターン。

#### TiDBパーサーがサポートしていないSQLステートメントを除外します {#filter-out-the-sql-statements-that-the-tidb-parser-does-not-support}

`table`パーサーがサポートしていないSQLステートメントの場合、DMはそれらを解析して`schema`情報を取得できません。したがって、グローバルフィルタリングルールを使用する必要があります： `schema-pattern: "*"` 。

> **ノート：**
>
> 移行する必要のあるデータが除外されないようにするには、グローバルフィルタリングルールをできるだけ厳密に構成する必要があります。

（一部のバージョンの）TiDBパーサーがサポートしていない`PARTITION`のステートメントをフィルターで除外するには、次のフィルター規則を構成します。

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

## オンラインDDLツール {#online-ddl-tools}

MySQLエコシステムでは、gh-ostやpt-oscなどのツールが広く使用されています。 DMは、不要な中間データの移行を回避するために、これらのツールのサポートを提供します。

### 制限 {#restrictions}

-   DMはgh-ostとpt-oscのみをサポートします。
-   `online-ddl`が有効になっている場合、インクリメンタルレプリケーションに対応するチェックポイントはオンラインDDL実行のプロセスにあるべきではありません。たとえば、アップストリームオンラインDDL操作がbinlogの`position-A`で開始し、 `position-B`で終了する場合、増分レプリケーションの開始点は`position-A`より前または`position-B`より後である必要があります。そうしないと、エラーが発生します。詳しくは[FAQ](/dm/dm-faq.md#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-online-ddl-scheme-gh-ost-is-set)をご覧ください。

### パラメータ設定 {#parameter-configuration}

<SimpleTab>
<div label="v2.0.5 and later">

v2.0.5以降のバージョンでは、 `task`の構成ファイルの`online-ddl`の構成アイテムを使用する必要があります。

-   アップストリームのMySQL/MariaDBが（同時に）gh-ostまたはpt-oscツールを使用する場合は、タスク構成ファイルで`online-ddl`から`true`に設定します。

```yml
online-ddl: true
```

> **ノート：**
>
> v2.0.5以降、 `online-ddl-scheme`は非推奨になっているため、 `online-ddl-scheme`ではなく`online-ddl`を使用する必要があります。つまり、設定`online-ddl: true`は`online-ddl-scheme`を上書きし、設定`online-ddl-scheme: "pt"`または`online-ddl-scheme: "gh-ost"`は`online-ddl: true`に変換されます。

</div>

<div label="earlier than v2.0.5">

v2.0.5（v2.0.5を含まない）より前では、 `task`構成ファイルの`online-ddl-scheme`構成項目を使用する必要があります。

-   アップストリームのMySQL/MariaDBがgh-ostツールを使用する場合は、タスク構成ファイルで設定します。

```yml
online-ddl-scheme: "gh-ost"
```

-   アップストリームのMySQL/MariaDBがptツールを使用する場合は、タスク構成ファイルで設定します。

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>

## シャードマージ {#shard-merge}

DMは、アップストリームのMySQL / MariaDBシャードテーブルのDMLデータとDDLデータのマージ、およびマージされたデータのダウンストリームTiDBテーブルへの移行をサポートしています。

### 制限 {#restrictions}

現在、シャードマージ機能は限られたシナリオでのみサポートされています。詳細については、 [ペシミスティックモードでのDDL使用制限のシャーディング](/dm/feature-shard-merge-pessimistic.md#restrictions)と[オプティミスティックモードでのDDL使用制限のシャーディング](/dm/feature-shard-merge-optimistic.md#restrictions)を参照してください。

### パラメータ設定 {#parameter-configuration}

タスク構成ファイルで`shard-mode`から`pessimistic`を設定します。

```
shard-mode: "pessimistic" # The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic" mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
```

### シャーディングDDLロックを手動で処理する {#handle-sharding-ddl-locks-manually}

いくつかの異常なシナリオでは、 [シャーディングDDLロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)にする必要があります。
