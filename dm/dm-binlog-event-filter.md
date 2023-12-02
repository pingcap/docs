---
title: TiDB Data Migration Binlog Event Filter
summary: Learn how to use the binlog event filter feature of DM.
---

# TiDB データ移行Binlogイベント フィルター {#tidb-data-migration-binlog-event-filter}

TiDB Data Migration (DM) は、エラーをフィルタリングしてブロックし、レポートしたり、一部のスキーマまたはテーブルの指定されたタイプのbinlogイベントのみを受信したりするためのbinlogイベント フィルター機能を提供します。たとえば、 `TRUNCATE TABLE`つまたは`INSERT`のイベントをすべてフィルターで除外できます。 binlogイベント フィルター機能は、 [ブロックリストと許可リスト](/dm/dm-block-allow-table-lists.md)機能よりも粒度が細かいです。

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

DM v2.0.2 以降、ソース構成ファイルでbinlogイベント フィルターを構成できます。詳細は[アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

スキーマとテーブルの一致にワイルドカードを使用する場合は、次の点に注意してください。

-   `schema-pattern`と`table-pattern` 、 `*` 、 `?` 、および`[]`を含むワイルドカードのみをサポートします。ワイルドカード一致では`*`シンボルは 1 つだけ使用でき、最後になければなりません。たとえば、 `table-pattern: "t_*"`では、 `"t_*"` `t_`で始まるすべてのテーブルを示します。詳細は[ワイルドカードマッチング](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)参照してください。

-   `sql-pattern`は正規表現のみをサポートします。

## パラメータの説明 {#parameter-descriptions}

-   [`schema-pattern` / `table-pattern`](/dm/table-selector.md) : `schema-pattern` / `table-pattern`に一致するアップストリーム MySQL または MariaDB インスタンス テーブルのbinlogイベントまたは DDL SQL ステートメントは、以下のルールによってフィルターされます。

-   `events` :binlogイベント配列。次の表から 1 つ以上の`Event`のみを選択できます。

    | イベント                         | タイプ        | 説明                                                                                                      |
    | ---------------------------- | ---------- | ------------------------------------------------------------------------------------------------------- |
    | `all`                        |            | 以下のすべてのイベントが含まれます                                                                                       |
    | `all dml`                    |            | 以下のすべての DML イベントが含まれます                                                                                  |
    | `all ddl`                    |            | 以下のすべての DDL イベントが含まれます                                                                                  |
    | `incompatible ddl changes`   |            | すべての互換性のない DDL イベントが含まれます。「互換性のない DDL」とは、データ損失を引き起こす可能性のある DDL 操作を意味します。                                |
    | `none`                       |            | 以下のイベントは含まれません                                                                                          |
    | `none ddl`                   |            | 以下の DDL イベントは含まれません                                                                                     |
    | `none dml`                   |            | 以下の DML イベントは含まれません                                                                                     |
    | `insert`                     | DML        | `INSERT` DML イベント                                                                                       |
    | `update`                     | DML        | `UPDATE` DML イベント                                                                                       |
    | `delete`                     | DML        | `DELETE` DML イベント                                                                                       |
    | `create database`            | DDL        | `CREATE DATABASE` DDL イベント                                                                              |
    | `drop database`              | 互換性のない DDL | `DROP DATABASE` DDL イベント                                                                                |
    | `create table`               | DDL        | `CREATE TABLE` DDL イベント                                                                                 |
    | `create index`               | DDL        | `CREATE INDEX` DDL イベント                                                                                 |
    | `drop table`                 | 互換性のない DDL | `DROP TABLE` DDL イベント                                                                                   |
    | `truncate table`             | 互換性のない DDL | `TRUNCATE TABLE` DDL イベント                                                                               |
    | `rename table`               | 互換性のない DDL | `RENAME TABLE` DDL イベント                                                                                 |
    | `drop index`                 | 互換性のない DDL | `DROP INDEX` DDL イベント                                                                                   |
    | `alter table`                | DDL        | `ALTER TABLE` DDL イベント                                                                                  |
    | `value range decrease`       | 互換性のない DDL | 列フィールドの値の範囲を減らす DDL ステートメント ( `VARCHAR(20)`を`VARCHAR(10)`に変更する`ALTER TABLE MODIFY COLUMN`ステートメントなど)     |
    | `precision decrease`         | 互換性のない DDL | 列フィールドの精度を下げる DDL ステートメント ( `Decimal(10, 2)`を`Decimal(10, 1)`に変更する`ALTER TABLE MODIFY COLUMN`ステートメントなど) |
    | `modify column`              | 互換性のない DDL | 列フィールドの型を変更する DDL ステートメント ( `INT`を`VARCHAR`に変更する`ALTER TABLE MODIFY COLUMN`ステートメントなど)                   |
    | `rename column`              | 互換性のない DDL | 列の名前を変更する DDL ステートメント ( `ALTER TABLE RENAME COLUMN`ステートメントなど)                                           |
    | `rename index`               | 互換性のない DDL | インデックス名を変更する DDL ステートメント ( `ALTER TABLE RENAME INDEX`ステートメントなど)                                         |
    | `drop column`                | 互換性のない DDL | `ALTER TABLE DROP COLUMN`ステートメントなど、テーブルから列を削除する DDL ステートメント                                             |
    | `drop index`                 | 互換性のない DDL | `ALTER TABLE DROP INDEX`ステートメントなど、テーブル内のインデックスを削除する DDL ステートメント                                         |
    | `truncate table partition`   | 互換性のない DDL | 指定されたパーティションからすべてのデータを削除する DDL ステートメント ( `ALTER TABLE TRUNCATE PARTITION`ステートメントなど)                     |
    | `drop primary key`           | 互換性のない DDL | 主キーを削除する DDL ステートメント ( `ALTER TABLE DROP PRIMARY KEY`ステートメントなど)                                         |
    | `drop unique key`            | 互換性のない DDL | 一意のキーを削除する DDL ステートメント ( `ALTER TABLE DROP UNIQUE KEY`ステートメントなど)                                        |
    | `modify default value`       | 互換性のない DDL | 列のデフォルト値を変更する DDL ステートメント ( `ALTER TABLE CHANGE DEFAULT`ステートメントなど)                                      |
    | `modify constraint`          | 互換性のない DDL | 制約を変更する DDL ステートメント ( `ALTER TABLE ADD CONSTRAINT`ステートメントなど)                                            |
    | `modify columns order`       | 互換性のない DDL | 列の順序を変更する DDL ステートメント ( `ALTER TABLE CHANGE AFTER`ステートメントなど)                                            |
    | `modify charset`             | 互換性のない DDL | `ALTER TABLE MODIFY CHARSET`ステートメントなど、列の文字セットを変更する DDL ステートメント                                          |
    | `modify collation`           | 互換性のない DDL | 列の照合順序を変更する DDL ステートメント ( `ALTER TABLE MODIFY COLLATE`ステートメントなど)                                        |
    | `remove auto increment`      | 互換性のない DDL | 自動増分キーを削除する DDL ステートメント                                                                                 |
    | `modify storage engine`      | 互換性のない DDL | テーブルstorageエンジンを変更する DDL ステートメント ( `ALTER TABLE ENGINE = MyISAM`ステートメントなど)                              |
    | `reorganize table partition` | 互換性のない DDL | `ALTER TABLE REORGANIZE PARTITION`ステートメントなど、テーブル内のパーティションを再編成する DDL ステートメント                             |
    | `rebuild table partition`    | 互換性のない DDL | テーブル パーティションを再構築する DDL ステートメント ( `ALTER TABLE REBUILD PARTITION`ステートメントなど)                              |
    | `exchange table partition`   | 互換性のない DDL | 2 つのテーブル間のパーティションを交換する DDL ステートメント ( `ALTER TABLE EXCHANGE PARTITION`ステートメントなど)                         |
    | `coalesce table partition`   | 互換性のない DDL | テーブル内のパーティションの数を減らす DDL ステートメント ( `ALTER COALESCE PARTITION`ステートメントなど)                                  |

-   `sql-pattern` : 指定された DDL SQL ステートメントをフィルタリングするために使用されます。一致ルールでは正規表現の使用がサポートされています。たとえば、 `"^DROP\\s+PROCEDURE"` 。

-   `action` : 文字列 ( `Do` / `Ignore` / `Error` )。ルールに基づき、以下のように判断します。

    -   `Do` : 許可リスト。binlogは、次の 2 つの条件のいずれかでフィルタリングされます。
        -   イベントのタイプはルールのリスト`event`にありません。
        -   イベントの SQL ステートメントはルールの`sql-pattern`と一致できません。
    -   `Ignore` : ブロックリスト。binlogは、次の 2 つの条件のいずれかでフィルタリングされます。
        -   イベントのタイプはルールのリスト`event`にあります。
        -   イベントの SQL ステートメントは、ルールの`sql-pattern`と照合できます。
    -   `Error` : エラーリスト。 binlog は、次の 2 つの条件のいずれかでエラーを報告します。
        -   イベントのタイプはルールのリスト`event`にあります。
        -   イベントの SQL ステートメントは、ルールの`sql-pattern`と照合できます。
    -   複数のルールが同じテーブルに一致する場合、ルールは順番に適用されます。ブロック リストはエラー リストよりも優先度が高く、エラー リストは許可リストよりも優先度が高くなります。例えば：
        -   `Ignore`と`Error`両方のルールが同じテーブルに適用される場合、 `Ignore`ルールが有効になります。
        -   `Error`と`Do`両方のルールが同じテーブルに適用される場合、 `Error`ルールが有効になります。

## 使用例 {#usage-examples}

このセクションでは、シャーディング (シャードされたスキーマとテーブル) のシナリオでの使用例を示します。

### すべてのシャーディング削除操作をフィルタリングする {#filter-all-sharding-deletion-operations}

すべての削除操作をフィルターで除外するには、次の 2 つのフィルター ルールを構成します。

-   `filter-table-rule` `test_*`に一致するすべてのテーブルの`TRUNCATE TABLE` 、 `DROP TABLE` 、および`DELETE STATEMENT`操作を除外します。 `t_*`パターン。
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

### シャーディング DML ステートメントのみを移行する {#only-migrate-sharding-dml-statements}

シャーディング DML ステートメントのみを移行するには、次の 2 つのフィルタリング ルールを構成します。

-   `do-table-rule` `test_*`に一致するすべてのテーブルの`CREATE TABLE` 、 `INSERT` 、 `UPDATE` 、および`DELETE`ステートメントのみを移行します。 `t_*`パターン。
-   `do-schema-rule`パターン`test_*`に一致するすべてのスキーマのステートメント`CREATE DATABASE`のみを移行します。

> **注記：**
>
> `CREATE DATABASE/TABLE`ステートメントが移行される理由は、DML ステートメントはスキーマとテーブルの作成後にのみ移行できるためです。

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

### TiDB がサポートしていない SQL ステートメントをフィルタリングして除外します。 {#filter-out-the-sql-statements-that-tidb-does-not-support}

TiDB がサポートしていない`PROCEDURE`ステートメントをフィルタリングして除外するには、次の`filter-procedure-rule`を構成します。

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

`filter-procedure-rule` `test_*`に一致するすべてのテーブルの`^CREATE\\s+PROCEDURE`および`^DROP\\s+PROCEDURE`ステートメントを除外します。 `t_*`パターン。

### TiDB パーサーがサポートしていない SQL ステートメントをフィルターで除外します。 {#filter-out-the-sql-statements-that-the-tidb-parser-does-not-support}

TiDB パーサーがサポートしていない SQL ステートメントの場合、DM はそれらを解析して`schema` / `table`の情報を取得できません。したがって、グローバル フィルタリング ルール`schema-pattern: "*"`を使用する必要があります。

> **注記：**
>
> 移行する必要があるデータがフィルターで除外されないようにするには、グローバル フィルター ルールをできるだけ厳密に構成する必要があります。

TiDB パーサー (一部のバージョン) がサポートしていない`PARTITION`ステートメントをフィルターで除外するには、次のフィルター ルールを構成します。

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

### 一部の DDL ステートメントのエラーを報告する {#report-errors-on-some-ddl-statements}

DM が TiDB に DDL ステートメントをレプリケートする前に、一部のアップストリーム操作によって生成された DDL ステートメントのエラーをブロックして報告する必要がある場合は、次の設定を使用できます。

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "truncate table partition"]
    action: Error
```
