---
title: TiDB Data Migration Binlog Event Filter
summary: Learn how to use the binlog event filter feature of DM.
---

# TiDB データ移行Binlogイベント フィルター {#tidb-data-migration-binlog-event-filter}

TiDB Data Migration (DM) は、binlogイベント フィルター機能を提供し、一部のスキーマまたはテーブルに対して、指定された種類のbinlogイベントを除外または受信します。たとえば、 `TRUNCATE TABLE`つまたは`INSERT`のイベントすべてを除外できます。 binlogイベント フィルター機能は、 [ブロックリストと許可リスト](/dm/dm-block-allow-table-lists.md)機能よりもきめ細かくなっています。

## binlogイベント フィルターを構成する {#configure-the-binlog-event-filter}

タスク構成ファイルで、次の構成を追加します。

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    ​table-pattern: "t_*"
    ​events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    ​action: Ignore
```

DM v2.0.2 以降では、ソース構成ファイルでbinlogイベント フィルターを構成できます。詳細については、 [アップストリーム データベースコンフィグレーションファイル](/dm/dm-source-configuration-file.md)を参照してください。

単純なシナリオでは、スキーマとテーブルの一致にワイルドカードを使用することをお勧めします。ただし、次のバージョンの違いに注意してください。

-   DM v1.0.5 以降のバージョンの場合、 binlogイベント フィルターは[ワイルドカードマッチ](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)サポートしますが、ワイルドカード式で指定できるのは`*`**だけ**であり、<strong>最後に</strong>`*`を配置する必要があります。

-   v1.0.5 より前のバージョンの DM の場合、 binlogイベント フィルターはワイルドカードをサポートしますが、 `[...]`と`[!...]`式はサポートしません。

## パラメータの説明 {#parameter-descriptions}

-   [`schema-pattern` / <code>table-pattern</code>](/dm/table-selector.md) : `schema-pattern` / `table-pattern`に一致する上流の MySQL または MariaDB インスタンス テーブルのbinlogイベントまたは DDL SQL ステートメントは、以下のルールによってフィルター処理されます。

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

-   `sql-pattern` : 指定された DDL SQL ステートメントをフィルタリングするために使用されます。一致ルールは、正規表現の使用をサポートしています。たとえば、 `"^DROP\\s+PROCEDURE"`です。

-   `action` : 文字列 ( `Do` / `Ignore` )。以下のルールに基づいて、フィルタリングするかどうかを判断します。 2 つのルールのいずれかが満たされる場合、binlogはフィルタリングされます。それ以外の場合、binlogはフィルタリングされません。

    -   `Do` : 許可リスト。 binlog は、次の 2 つの条件のいずれかでフィルター処理されます。
        -   イベントのタイプがルールの`event`リストにありません。
        -   イベントの SQL ステートメントは、ルールの`sql-pattern`つと一致しません。
    -   `Ignore` : ブロック リスト。 binlog は、次の 2 つの条件のいずれかでフィルター処理されます。
        -   イベントのタイプは、ルールの`event`リストにあります。
        -   イベントの SQL ステートメントは、ルールの`sql-pattern`に一致できます。
    -   複数のルールが同じテーブルに一致する場合、ルールは順番に適用されます。ブロック リストは、許可リストよりも優先度が高くなります。たとえば、 `Ignore`と`Do`の両方のルールが同じテーブルに適用される場合、 `Ignore`ルールが有効になります。

## 使用例 {#usage-examples}

このセクションでは、シャーディングのシナリオ (シャードされたスキーマとテーブル) での使用例を示します。

### すべてのシャーディング削除操作をフィルタリングする {#filter-all-sharding-deletion-operations}

すべての削除操作を除外するには、次の 2 つのフィルタリング ルールを構成します。

-   `filter-table-rule` `test_*`に一致するすべてのテーブルの`TRUNCATE TABLE` `DROP TABLE`および`DELETE STATEMENT`操作を除外します。 `t_*`パターン。
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
-   `do-schema-rule` `test_*`パターンに一致するすべてのスキーマの`CREATE DATABASE`ステートメントのみを移行します。

> **ノート：**
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

### TiDB がサポートしていない SQL ステートメントを除外する {#filter-out-the-sql-statements-that-tidb-does-not-support}

TiDB がサポートしていない`PROCEDURE`ステートメントを除外するには、次の`filter-procedure-rule`構成します。

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

`filter-procedure-rule` `test_*`に一致するすべてのテーブルの`^CREATE\\s+PROCEDURE`および`^DROP\\s+PROCEDURE`ステートメントを除外します。 `t_*`パターン。

### TiDB パーサーがサポートしていない SQL ステートメントを除外する {#filter-out-the-sql-statements-that-the-tidb-parser-does-not-support}

TiDB パーサー`table`サポートしていない SQL ステートメントの場合、DM はそれらを解析して`schema`情報を取得できません。したがって、グローバル フィルタリング ルール`schema-pattern: "*"`を使用する必要があります。

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
