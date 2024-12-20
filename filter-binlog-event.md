---
title: Filter Binlog Events
summary: データを移行するときにbinlogイベントをフィルター処理する方法を学びます。
---

# Binlogイベントをフィルタリングする {#filter-binlog-events}

このドキュメントでは、DM を使用して継続的な増分データ レプリケーションを実行するときに、 binlogイベントをフィルター処理する方法について説明します。詳細なレプリケーション手順については、シナリオ別に次のドキュメントを参照してください。

-   [小規模データセットを MySQL から TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模データセットの MySQL シャードを TiDB に移行してマージする](/migrate-large-mysql-shards-to-tidb.md)

## コンフィグレーション {#configuration}

binlogイベント フィルターを使用するには、次に示すように、DM のタスク構成ファイルに`filter`を追加します。

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

-   `schema-pattern` / `table-pattern` : 一致するスキーマまたはテーブルをフィルターします

-   `events` : binlogイベントをフィルタリングします。サポートされているイベントは以下の表に示されています。

    | イベント        | カテゴリ   | 説明                |
    | ----------- | ------ | ----------------- |
    | 全て          |        | すべてのイベントを含む       |
    | すべてのDML     |        | すべてのDMLイベントを含む    |
    | すべてのDDL     |        | すべてのDDLイベントを含む    |
    | なし          |        | イベントは含まれません       |
    | なし          |        | すべてのDDLイベントを除外します |
    | なし dml      |        | すべてのDMLイベントを除外します |
    | 入れる         | DMML の | DMLイベントを挿入        |
    | アップデート      | DMML の | DMLイベントの更新        |
    | 消去          | DMML の | DMLイベントの削除        |
    | データベースを作成する | DDL    | データベースイベントの作成     |
    | データベースを削除   | DDL    | データベースイベントの削除     |
    | テーブルを作成する   | DDL    | テーブルイベントの作成       |
    | インデックスを作成   | DDL    | インデックスイベントの作成     |
    | ドロップテーブル    | DDL    | テーブルドロップイベント      |
    | テーブルを切り捨てる  | DDL    | テーブル切り捨てイベント      |
    | テーブル名の変更    | DDL    | テーブル名の変更イベント      |
    | インデックスを削除   | DDL    | インデックス削除イベント      |
    | テーブルを変更する   | DDL    | テーブル変更イベント        |

-   `sql-pattern` : 指定された DDL SQL ステートメントをフィルタリングします。一致ルールは正規表現の使用をサポートします。

-   `action` : `Do`または`Ignore`

    -   `Do` : 許可リスト。次の 2 つの条件のいずれかを満たす場合、 binlogイベントが複製されます。

        -   イベントはルール設定と一致します。
        -   sql-pattern が指定されており、イベントの SQL ステートメントが sql-pattern オプションのいずれかと一致します。

    -   `Ignore` : ブロック リスト。次の 2 つの条件のいずれかを満たす場合、 binlogイベントはフィルター処理されます。

        -   イベントはルール設定と一致します。
        -   sql-pattern が指定されており、イベントの SQL ステートメントが sql-pattern オプションのいずれかと一致します。

    `Do`と`Ignore`両方が設定されている場合、 `Ignore` `Do`よりも優先されます。つまり、 `Ignore`と`Do`両方の条件を満たすイベントは除外されます。

## アプリケーションシナリオ {#application-scenarios}

このセクションでは、 binlogイベント フィルターのアプリケーション シナリオについて説明します。

### すべてのシャーディング削除操作を除外する {#filter-out-all-sharding-deletion-operations}

すべての削除操作を除外するには、以下に示すように`filter-table-rule`と`filter-schema-rule`設定します。

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

### シャードされたスキーマとテーブルのDML操作のみを移行する {#migrate-only-dml-operations-of-sharded-schemas-and-tables}

DML ステートメントのみをレプリケートするには、次に示すように 2 つの`Binlog event filter rule`を設定します。

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

### TiDBでサポートされていないSQL文を除外する {#filter-out-sql-statements-not-supported-by-tidb}

TiDB でサポートされていない SQL ステートメントを除外するには、以下に示すように`filter-procedure-rule`設定します。

    filters:
      filter-procedure-rule:
        schema-pattern: "*"
        sql-pattern: [".*\\s+DROP\\s+PROCEDURE", ".*\\s+CREATE\\s+PROCEDURE", "ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
        action: Ignore

> **警告：**
>
> 移行する必要があるデータがフィルタリングされないようにするには、グローバル フィルタリング ルールをできるだけ厳密に構成します。

## 参照 {#see-also}

[SQL 式を使用してBinlogイベントをフィルタリングする](/filter-dml-event.md)
