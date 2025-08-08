---
title: Filter Binlog Events
summary: データを移行するときにbinlogイベントをフィルター処理する方法を学びます。
---

# Binlogイベントをフィルタリングする {#filter-binlog-events}

このドキュメントでは、DMを使用して継続的な増分データレプリケーションを実行する際に、 binlogイベントをフィルタリングする方法について説明します。レプリケーションの詳細な手順については、シナリオごとに以下のドキュメントを参照してください。

-   [小規模データセットをMySQLからTiDBに移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模データセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模データセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## コンフィグレーション {#configuration}

binlogイベント フィルターを使用するには、以下に示すように、DM のタスク構成ファイルに`filter`追加します。

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

-   `events` : binlogイベントをフィルタリングします。サポートされているイベントは以下の表のとおりです。

    | イベント         | カテゴリ | 説明                |
    | ------------ | ---- | ----------------- |
    | 全て           |      | すべてのイベントを含む       |
    | すべてのDML      |      | すべてのDMLイベントを含む    |
    | すべてのDDL      |      | すべてのDDLイベントを含む    |
    | なし           |      | イベントは含まれません       |
    | なしDDL        |      | すべてのDDLイベントを除外します |
    | なし dml       |      | すべてのDMLイベントを除外します |
    | 入れる          | DML  | DMLイベントを挿入        |
    | アップデート       | DML  | DMLイベントの更新        |
    | 消去           | DML  | DMLイベントの削除        |
    | データベースを作成する  | DDL  | データベースイベントの作成     |
    | データベースを削除    | DDL  | データベースイベントの削除     |
    | テーブルを作成する    | DDL  | テーブルイベントの作成       |
    | インデックスを作成する  | DDL  | インデックスイベントの作成     |
    | ドロップテーブル     | DDL  | ドロップテーブルイベント      |
    | テーブルを切り捨てる   | DDL  | テーブル切り捨てイベント      |
    | テーブルの名前を変更する | DDL  | テーブル名の変更イベント      |
    | インデックスを削除    | DDL  | インデックス削除イベント      |
    | テーブルを変更する    | DDL  | テーブル変更イベント        |

-   `sql-pattern` : 指定されたDDL SQL文をフィルタリングします。マッチングルールでは正規表現の使用がサポートされています。

-   `action` ： `Do`または`Ignore`

    -   `Do` : 許可リスト。以下の2つの条件のいずれかを満たす場合、 binlogイベントは複製されます。

        -   イベントはルール設定と一致します。
        -   sql-pattern が指定されており、イベントの SQL ステートメントが sql-pattern オプションのいずれかと一致します。

    -   `Ignore` ：ブロックリスト。以下の2つの条件のいずれかを満たす場合、 binlogイベントはフィルタリングされます。

        -   イベントはルール設定と一致します。
        -   sql-pattern が指定されており、イベントの SQL ステートメントが sql-pattern オプションのいずれかと一致します。

    `Do`と`Ignore`両方が設定されている場合、 `Ignore` `Do`よりも優先されます。つまり、 `Ignore`と`Do`両方の条件を満たすイベントは除外されます。

## アプリケーションシナリオ {#application-scenarios}

このセクションでは、 binlogイベント フィルターの適用シナリオについて説明します。

### すべてのシャーディング削除操作を除外する {#filter-out-all-sharding-deletion-operations}

すべての削除操作を除外するには、次に示すように`filter-table-rule`と`filter-schema-rule`設定します。

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

### シャード化されたスキーマとテーブルのDML操作のみを移行する {#migrate-only-dml-operations-of-sharded-schemas-and-tables}

DML ステートメントのみをレプリケートするには、次に示すように`Binlog event filter rule`を 2 つ設定します。

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

### TiDB でサポートされていない SQL ステートメントを除外する {#filter-out-sql-statements-not-supported-by-tidb}

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
