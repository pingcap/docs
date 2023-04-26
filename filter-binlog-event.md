---
title: Filter Binlog Events
summary: Learn how to filter binlog events when migrating data.
---

# Binlogイベントのフィルタリング {#filter-binlog-events}

このドキュメントでは、DM を使用して継続的な増分データ レプリケーションを実行するときに、 binlogイベントをフィルター処理する方法について説明します。詳細なレプリケーション手順については、シナリオごとに次のドキュメントを参照してください。

-   [小さなデータセットの MySQL を TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットの MySQL を TiDB に移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## コンフィグレーション {#configuration}

binlogイベント フィルターを使用するには、以下に示すように、DM のタスク構成ファイルに`filter`を追加します。

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

-   `schema-pattern` / `table-pattern` : スキーマまたはテーブルに一致するフィルター

-   `events` : binlogイベントをフィルタリングします。サポートされているイベントを次の表に示します。

    | イベント        | カテゴリー | 説明                  |
    | ----------- | ----- | ------------------- |
    | 全て          |       | すべてのイベントを含む         |
    | すべてのdml     |       | すべての DML イベントを含む    |
    | すべての ddl    |       | すべての DDL イベントを含む    |
    | なし          |       | イベントを含まない           |
    | なし          |       | すべての DDL イベントを除外します |
    | dml なし      |       | すべての DML イベントを除外します |
    | 入れる         | DML   | DML イベントの挿入         |
    | アップデート      | DML   | DML イベントの更新         |
    | 消去          | DML   | DML イベントの削除         |
    | データベースを作成する | DDL   | データベース イベントの作成      |
    | データベースをドロップ | DDL   | データベースのドロップ イベント    |
    | テーブルを作成     | DDL   | テーブル イベントの作成        |
    | インデックスを作成   | DDL   | インデックス イベントの作成      |
    | ドロップテーブル    | DDL   | テーブルドロップイベント        |
    | テーブルを切り捨てる  | DDL   | テーブル イベントの切り捨て      |
    | テーブルの名前を変更  | DDL   | テーブルイベントの名前変更       |
    | ドロップ インデックス | DDL   | ドロップ インデックス イベント    |
    | 他の机         | DDL   | テーブル変更イベント          |

-   `sql-pattern` : 指定された DDL SQL ステートメントをフィルター処理します。一致ルールは、正規表現の使用をサポートしています。

-   `action` : `Do`または`Ignore`

    -   `Do` : 許可リスト。次の 2 つの条件のいずれかを満たす場合、 binlogイベントはレプリケートされます。

        -   イベントはルール設定と一致します。
        -   sql-pattern が指定されており、イベントの SQL ステートメントが sql-pattern オプションのいずれかに一致します。

    -   `Ignore` : ブロック リスト。次の 2 つの条件のいずれかを満たす場合、 binlogイベントは除外されます。

        -   イベントはルール設定と一致します。
        -   sql-pattern が指定されており、イベントの SQL ステートメントが sql-pattern オプションのいずれかに一致します。

    `Do`と`Ignore`両方が構成されている場合、 `Ignore` `Do`よりも優先度が高くなります。つまり、 `Ignore`と`Do`の両方の条件を満たすイベントが除外されます。

## アプリケーション シナリオ {#application-scenarios}

このセクションでは、 binlogイベント フィルターのアプリケーション シナリオについて説明します。

### すべてのシャーディング削除操作を除外します {#filter-out-all-sharding-deletion-operations}

すべての削除操作を除外するには、以下に示すように`filter-table-rule`と`filter-schema-rule`を構成します。

```
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

### シャードされたスキーマとテーブルの DML 操作のみを移行する {#migrate-only-dml-operations-of-sharded-schemas-and-tables}

DML ステートメントのみをレプリケートするには、以下に示すように 2 つの`Binlog event filter rule`を構成します。

```
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

### TiDB でサポートされていない SQL ステートメントを除外する {#filter-out-sql-statements-not-supported-by-tidb}

TiDB でサポートされていない SQL ステートメントを除外するには、以下に示すように`filter-procedure-rule`を構成します。

```
filters:
  filter-procedure-rule:
    schema-pattern: "*"
    sql-pattern: [".*\\s+DROP\\s+PROCEDURE", ".*\\s+CREATE\\s+PROCEDURE", "ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

> **警告：**
>
> 移行する必要のあるデータを除外しないようにするには、グローバル フィルタリング ルールをできるだけ厳密に構成します。

## こちらもご覧ください {#see-also}

[SQL 式を使用してBinlogイベントをフィルタリングする](/filter-dml-event.md)
