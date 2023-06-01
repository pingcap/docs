---
title: TiDB Data Migration Binlog Event Filter
summary: Learn how to use the binlog event filter feature of DM.
---

# TiDB データ移行Binlogイベント フィルター {#tidb-data-migration-binlog-event-filter}

TiDB Data Migration (DM) は、一部のスキーマまたはテーブルの指定されたタイプのbinlogイベントをフィルターで除外するか、のみ受信するbinlogイベント フィルター機能を提供します。たとえば、 `TRUNCATE TABLE`つまたは`INSERT`のイベントをすべてフィルターで除外できます。 binlogイベント フィルター機能は、 [ブロックリストと許可リスト](/dm/dm-block-allow-table-lists.md)機能よりも粒度が細かいです。

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

単純なシナリオでは、スキーマとテーブルを一致させるためにワイルドカードを使用することをお勧めします。ただし、次のバージョンの違いに注意してください。

-   DM v1.0.5 以降のバージョンでは、 binlogイベント フィルターは[ワイルドカードマッチ](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)サポートしますが、ワイルドカード式には`*`**つだけ**使用でき、**最後に**`*`を配置する必要があります。

-   v1.0.5 より前の DM バージョンの場合、 binlogイベント フィルターはワイルドカードをサポートしますが、 `[...]`および`[!...]`式はサポートしません。

## パラメータの説明 {#parameter-descriptions}

-   [`schema-pattern` / `table-pattern`](/dm/table-selector.md) : `schema-pattern` / `table-pattern`に一致するアップストリーム MySQL または MariaDB インスタンス テーブルのbinlogイベントまたは DDL SQL ステートメントは、以下のルールによってフィルターされます。

-   `events` :binlogイベント配列。次の表から 1 つ以上の`Event`のみを選択できます。

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

-   `sql-pattern` : 指定された DDL SQL ステートメントをフィルタリングするために使用されます。一致ルールでは正規表現の使用がサポートされています。たとえば、 `"^DROP\\s+PROCEDURE"` 。

-   `action` : 文字列 ( `Do` / `Ignore` )。以下のルールに基づいてフィルタリングするかどうかを判断します。 2 つのルールのいずれかが満たされる場合、binlogはフィルタリングされます。それ以外の場合、binlogはフィルタリングされません。

    -   `Do` : 許可リスト。binlogは、次の 2 つの条件のいずれかでフィルタリングされます。
        -   イベントのタイプはルールのリスト`event`にありません。
        -   イベントの SQL ステートメントはルールの`sql-pattern`と一致できません。
    -   `Ignore` : ブロックリスト。binlogは、次の 2 つの条件のいずれかでフィルタリングされます。
        -   イベントのタイプはルールのリスト`event`にあります。
        -   イベントの SQL ステートメントは、ルールの`sql-pattern`と照合できます。
    -   複数のルールが同じテーブルに一致する場合、ルールは順番に適用されます。ブロック リストは許可リストよりも高い優先度を持ちます。たとえば、 `Ignore`と`Do`の両方のルールが同じテーブルに適用される場合、 `Ignore`ルールが有効になります。

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

> **ノート：**
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

TiDB パーサーがサポートしていない SQL ステートメントの場合、DM はそれらを解析して`schema` / `table`の情報を取得できません。したがって、グローバル フィルタリング ルールを使用する必要があります: `schema-pattern: "*"` 。

> **ノート：**
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
