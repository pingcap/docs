---
title: TiDB Data Migration Binlog Event Filter
summary: DM のbinlogイベント フィルター機能の使用方法を学習します。
---

# TiDB データ移行Binlogイベントフィルター {#tidb-data-migration-binlog-event-filter}

TiDB Data Migration (DM) は、特定のスキーマまたはテーブルについて、エラーをフィルタリング、ブロック、報告したり、特定の種類のbinlogイベントのみを受信したりするためのbinlogイベントフィルタ機能を提供します。例えば、 `TRUNCATE TABLE`または`INSERT`イベントすべてをフィルタリングできます。binlogイベントフィルタ機能は、 [ブロックリストと許可リスト](/dm/dm-block-allow-table-lists.md)機能よりもきめ細かな制御が可能です。

## binlogイベントフィルターを構成する {#configure-the-binlog-event-filter}

タスク構成ファイルに次の構成を追加します。

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    ​table-pattern: "t_*"
    ​events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    ​action: Ignore
```

DM v2.0.2以降では、ソース設定ファイルでbinlogイベントフィルターを設定できます。詳細については、 [上流データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)参照してください。

一致するスキーマとテーブルにワイルドカードを使用する場合は、次の点に注意してください。

-   `schema-pattern`と`table-pattern` 、 `*` 、 `?` 、 `[]`を含むワイルドカードのみをサポートします。ワイルドカード一致では`*`記号は1つだけ使用でき、末尾に配置する必要があります。例えば、 `table-pattern: "t_*"`の場合、 `"t_*"` `t_`で始まるすべてのテーブルを示します。詳細は[ワイルドカードマッチング](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)参照してください。

-   `sql-pattern`正規表現のみをサポートします。

## パラメータの説明 {#parameter-descriptions}

-   [`schema-pattern` / `table-pattern`](/dm/table-selector.md) : `schema-pattern` `table-pattern`一致するアップストリーム MySQL または MariaDB インスタンス テーブルのbinlogイベントまたは DDL SQL ステートメントは、以下のルールによってフィルター処理されます。

-   `events` : binlogイベント配列。次の表から1つ以上の`Event`のみを選択できます。

    | イベント                         | タイプ       | 説明                                                                                         |
    | ---------------------------- | --------- | ------------------------------------------------------------------------------------------ |
    | `all`                        |           | 以下のすべてのイベントが含まれます                                                                          |
    | `all dml`                    |           | 以下のすべてのDMLイベントが含まれます                                                                       |
    | `all ddl`                    |           | 以下のすべてのDDLイベントが含まれます                                                                       |
    | `incompatible ddl changes`   |           | 互換性のないすべての DDL イベントが含まれます。「互換性のない DDL」とは、データ損失を引き起こす可能性のある DDL 操作を意味します。                   |
    | `none`                       |           | 以下のイベントは含まれません                                                                             |
    | `none ddl`                   |           | 以下の DDL イベントは含まれません                                                                        |
    | `none dml`                   |           | 以下のDMLイベントは含まれません                                                                          |
    | `insert`                     | DML       | `INSERT` DMLイベント                                                                           |
    | `update`                     | DML       | `UPDATE` DMLイベント                                                                           |
    | `delete`                     | DML       | `DELETE` DMLイベント                                                                           |
    | `create database`            | DDL       | 第`CREATE DATABASE` DDLイベント                                                                 |
    | `drop database`              | 互換性のないDDL | 第`DROP DATABASE` DDLイベント                                                                   |
    | `create table`               | DDL       | 第`CREATE TABLE` DDLイベント                                                                    |
    | `create index`               | DDL       | 第`CREATE INDEX` DDLイベント                                                                    |
    | `drop table`                 | 互換性のないDDL | 第`DROP TABLE` DDLイベント                                                                      |
    | `truncate table`             | 互換性のないDDL | 第`TRUNCATE TABLE` DDLイベント                                                                  |
    | `rename table`               | 互換性のないDDL | 第`RENAME TABLE` DDLイベント                                                                    |
    | `drop index`                 | 互換性のないDDL | 第`DROP INDEX` DDLイベント                                                                      |
    | `alter table`                | DDL       | 第`ALTER TABLE` DDLイベント                                                                     |
    | `value range decrease`       | 互換性のないDDL | 列フィールドの値の範囲を減らすDDL文（例えば、 `VARCHAR(20)`を`VARCHAR(10)`に変更する`ALTER TABLE MODIFY COLUMN`文）     |
    | `precision decrease`         | 互換性のないDDL | 列フィールドの精度を下げるDDL文（例えば、 `Decimal(10, 2)`を`Decimal(10, 1)`に変更する`ALTER TABLE MODIFY COLUMN`文） |
    | `modify column`              | 互換性のないDDL | 列フィールドの型を変更するDDL文（ `INT`を`VARCHAR`に変更する`ALTER TABLE MODIFY COLUMN`文など）                     |
    | `rename column`              | 互換性のないDDL | 列の名前を変更するDDL文（ `ALTER TABLE RENAME COLUMN`文など）                                             |
    | `rename index`               | 互換性のないDDL | インデックス名を変更するDDL文（ `ALTER TABLE RENAME INDEX`文など）                                           |
    | `drop column`                | 互換性のないDDL | テーブルから列を削除するDDL文（ `ALTER TABLE DROP COLUMN`文など）                                            |
    | `drop index`                 | 互換性のないDDL | テーブルのインデックスを削除するDDL文`ALTER TABLE DROP INDEX`文など）                                           |
    | `truncate table partition`   | 互換性のないDDL | 指定されたパーティションからすべてのデータを削除するDDL文（ `ALTER TABLE TRUNCATE PARTITION`文など）                       |
    | `drop primary key`           | 互換性のないDDL | 主キーを削除するDDL文`ALTER TABLE DROP PRIMARY KEY`文など）                                             |
    | `drop unique key`            | 互換性のないDDL | `ALTER TABLE DROP UNIQUE KEY`文のような、一意のキーを削除する DDL 文                                        |
    | `modify default value`       | 互換性のないDDL | 列のデフォルト値を変更するDDL文（ `ALTER TABLE CHANGE DEFAULT`文など）                                        |
    | `modify constraint`          | 互換性のないDDL | 制約を変更するDDL文`ALTER TABLE ADD CONSTRAINT`文など）                                                |
    | `modify columns order`       | 互換性のないDDL | 列の順序を変更するDDL文（ `ALTER TABLE CHANGE AFTER`文など）                                              |
    | `modify charset`             | 互換性のないDDL | 列の文字セットを変更するDDL文（ `ALTER TABLE MODIFY CHARSET`文など）                                         |
    | `modify collation`           | 互換性のないDDL | 列の照合順序を変更するDDL文（ `ALTER TABLE MODIFY COLLATE`文など）                                          |
    | `remove auto increment`      | 互換性のないDDL | 自動増分キーを削除するDDL文                                                                            |
    | `modify storage engine`      | 互換性のないDDL | テーブルstorageエンジンを変更するDDL文（ `ALTER TABLE ENGINE = MyISAM`文など）                                |
    | `reorganize table partition` | 互換性のないDDL | テーブル内のパーティションを再編成するDDL文`ALTER TABLE REORGANIZE PARTITION`文など）                              |
    | `rebuild table partition`    | 互換性のないDDL | テーブルパーティションを再構築するDDL文（ `ALTER TABLE REBUILD PARTITION`文など）                                 |
    | `exchange table partition`   | 互換性のないDDL | 2つのテーブル間でパーティションを交換するDDL文（ `ALTER TABLE EXCHANGE PARTITION`文など）                            |
    | `coalesce table partition`   | 互換性のないDDL | テーブル内のパーティションの数を減らすDDL文（ `ALTER COALESCE PARTITION`文など）                                    |

-   `sql-pattern` : 指定されたDDL SQL文をフィルタリングするために使用されます。一致ルールでは正規表現がサポートされています。例： `"^DROP\\s+PROCEDURE"` 。

-   `action` ：文字列（ `Do` / `Ignore` / `Error` ）。ルールに基づいて、以下のように判定します。

    -   `Do` : 許可リスト。binlogは次の2つの条件のいずれかでフィルタリングされます。
        -   イベントのタイプがルールの`event`のリストにありません。
        -   イベントの SQL ステートメントはルールの`sql-pattern`に一致しません。
    -   `Ignore` : ブロックリスト。binlogは次の2つの条件のいずれかでフィルタリングされます。
        -   イベントのタイプはルールの`event`のリストにあります。
        -   イベントの SQL 文は、ルールの`sql-pattern`つに一致できます。
    -   `Error` : エラーリスト。binlogは、以下のいずれかの条件でエラーを報告します。
        -   イベントのタイプはルールの`event`のリストにあります。
        -   イベントの SQL 文は、ルールの`sql-pattern`つに一致できます。
    -   複数のルールが同じテーブルに一致する場合、ルールは順番に適用されます。ブロックリストはエラーリストよりも優先度が高く、エラーリストは許可リストよりも優先度が高くなります。例：
        -   ルール`Ignore`と`Error`両方が同じテーブルに適用された場合、ルール`Ignore`有効になります。
        -   ルール`Error`と`Do`両方が同じテーブルに適用された場合、ルール`Error`有効になります。

## 使用例 {#usage-examples}

このセクションでは、シャーディング (シャードされたスキーマとテーブル) のシナリオでの使用例を示します。

### すべてのシャーディング削除操作をフィルタリングする {#filter-all-sharding-deletion-operations}

すべての削除操作をフィルタリングするには、次の 2 つのフィルタリング ルールを構成します。

-   `filter-table-rule` 、 `test_*` . `t_*`パターンに一致するすべてのテーブルの`TRUNCATE TABLE` 、 `DROP TABLE` 、および`DELETE STATEMENT`操作を除外します。
-   `filter-schema-rule` `test_*`パターンに一致するすべてのスキーマの`DROP DATABASE`操作を除外します。

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

### シャーディングDMLステートメントのみを移行する {#only-migrate-sharding-dml-statements}

シャーディング DML ステートメントのみを移行するには、次の 2 つのフィルタリング ルールを構成します。

-   `do-table-rule` 、 `test_*` . `t_*`パターンに一致するすべてのテーブルの`CREATE TABLE` 、 `INSERT` 、 `UPDATE` 、および`DELETE`ステートメントのみを移行します。
-   `do-schema-rule` 、 `test_*`パターンに一致するすべてのスキーマの`CREATE DATABASE`のステートメントのみを移行します。

> **注記：**
>
> `CREATE DATABASE/TABLE`ステートメントが移行される理由は、スキーマとテーブルが作成された後にのみ DML ステートメントを移行できるためです。

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

### TiDBがサポートしていないSQL文を除外する {#filter-out-the-sql-statements-that-tidb-does-not-support}

TiDB がサポートしていない`PROCEDURE`ステートメントを除外するには、次の`filter-procedure-rule`構成します。

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

`filter-procedure-rule` `test_*` . `t_*`パターンに一致するすべてのテーブルの`^CREATE\\s+PROCEDURE`と`^DROP\\s+PROCEDURE`ステートメントを除外します。

### TiDBパーサーがサポートしていないSQL文を除外する {#filter-out-the-sql-statements-that-the-tidb-parser-does-not-support}

TiDBパーサーがサポートしていないSQL文については、DMは解析できず、 `schema` / `table`情報を取得できません。そのため、グローバルフィルタリングルール`schema-pattern: "*"`使用する必要があります。

> **注記：**
>
> 移行する必要があるデータがフィルタリングされないようにするには、グローバル フィルタリング ルールをできるだけ厳密に構成する必要があります。

TiDB パーサー (特定のバージョン) がサポートしていない`PARTITION`ステートメントを除外するには、次のフィルタリング ルールを構成します。

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

### 一部のDDL文のエラーを報告する {#report-errors-on-some-ddl-statements}

DM が TiDB に複製する前に、一部のアップストリーム操作によって生成された DDL ステートメントのエラーをブロックして報告する必要がある場合は、次の設定を使用できます。

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "truncate table partition"]
    action: Error
```
