---
title: Filter Binlog Events
summary: Learn how to filter binlog events when migrating data.
---

# Binlogイベントのフィルタリング {#filter-binlog-events}

このドキュメントでは、DM を使用して継続的な増分データ レプリケーションを実行するときに、binlogイベントをフィルタリングする方法について説明します。レプリケーション手順の詳細については、シナリオごとに次のドキュメントを参照してください。

-   [小規模なデータセットを MySQL から TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットを MySQL から TiDB に移行する](/migrate-large-mysql-to-tidb.md)
-   [小規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
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

-   `events` :binlogイベントをフィルタリングします。サポートされているイベントを次の表に示します。

    | イベント         | カテゴリー | 説明                  |
    | ------------ | ----- | ------------------- |
    | 全て           |       | すべてのイベントが含まれます      |
    | すべてのDML      |       | すべての DML イベントが含まれます |
    | すべての ddl     |       | すべての DDL イベントが含まれます |
    | なし           |       | イベントは含まれません         |
    | なし           |       | すべての DDL イベントを除外します |
    | なし           |       | すべての DML イベントを除外します |
    | 入れる          | DML   | DML イベントの挿入         |
    | アップデート       | DML   | DML イベントの更新         |
    | 消去           | DML   | DMLイベントの削除          |
    | データベースを作成する  | DDL   | データベースイベントの作成       |
    | データベースを削除する  | DDL   | データベースドロップイベント      |
    | テーブルを作成する    | DDL   | テーブルイベントの作成         |
    | インデックスを作成する  | DDL   | インデックスイベントの作成       |
    | ドロップテーブル     | DDL   | ドロップテーブルイベント        |
    | テーブルを切り捨てる   | DDL   | テーブルの切り捨てイベント       |
    | テーブルの名前を変更する | DDL   | テーブル名の変更イベント        |
    | インデックスを削除    | DDL   | インデックスイベントのドロップ     |
    | 他の机          | DDL   | テーブル変更イベント          |

-   `sql-pattern` : 指定された DDL SQL ステートメントをフィルターします。一致ルールでは正規表現の使用がサポートされています。

-   `action` ： `Do`または`Ignore`

    -   `Do` : 許可リスト。次の 2 つの条件のいずれかを満たしている場合、 binlogイベントはレプリケートされます。

        -   イベントはルール設定と一致します。
        -   sql-pattern が指定されており、イベントの SQL ステートメントがいずれかの sql-pattern オプションと一致します。

    -   `Ignore` : ブロックリスト。次の 2 つの条件のいずれかを満たす場合、 binlogイベントはフィルターで除外されます。

        -   イベントはルール設定と一致します。
        -   sql-pattern が指定されており、イベントの SQL ステートメントがいずれかの sql-pattern オプションと一致します。

    `Do`と`Ignore`両方が設定されている場合は、 `Ignore` `Do`よりも優先されます。つまり、 `Ignore`と`Do`の両方の条件を満たすイベントが除外されます。

## アプリケーションシナリオ {#application-scenarios}

このセクションでは、 binlogイベント フィルターの適用シナリオについて説明します。

### すべてのシャーディング削除操作をフィルターで除外する {#filter-out-all-sharding-deletion-operations}

すべての削除操作をフィルターで除外するには、以下に示すように`filter-table-rule`と`filter-schema-rule`を構成します。

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

### シャード化されたスキーマとテーブルの DML 操作のみを移行する {#migrate-only-dml-operations-of-sharded-schemas-and-tables}

DML ステートメントのみをレプリケートするには、以下に示すように 2 つの`Binlog event filter rule`を構成します。

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

### TiDB でサポートされていない SQL ステートメントをフィルターで除外する {#filter-out-sql-statements-not-supported-by-tidb}

TiDB でサポートされていない SQL ステートメントを除外するには、以下に示すように`filter-procedure-rule`を構成します。

    filters:
      filter-procedure-rule:
        schema-pattern: "*"
        sql-pattern: [".*\\s+DROP\\s+PROCEDURE", ".*\\s+CREATE\\s+PROCEDURE", "ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
        action: Ignore

> **警告：**
>
> 移行する必要があるデータがフィルタリングされないようにするため、グローバル フィルタリング ルールをできるだけ厳密に構成します。

## こちらも参照 {#see-also}

[SQL式を使用したBinlogイベントのフィルタリング](/filter-dml-event.md)
