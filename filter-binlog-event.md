---
title: Filter Binlog Events
summary: Learn how to filter binlog events when migrating data.
---

# Binlogイベントをフィルタリングする {#filter-binlog-events}

このドキュメントでは、DMを使用して継続的な増分データレプリケーションを実行するときにbinlogイベントをフィルタリングする方法について説明します。詳細なレプリケーション手順については、シナリオごとに次のドキュメントを参照してください。

-   [小さなデータセットのMySQLをTiDBに移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットのMySQLをTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模なデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## Configuration / コンフィグレーション {#configuration}

binlogイベントフィルターを使用するには、以下に示すように、DMのタスク構成ファイルに`filter`を追加します。

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

-   `schema-pattern` ：スキーマまたは`table-pattern`に一致するフィルター

-   `events` ：binlogイベントをフィルタリングします。サポートされているイベントを以下の表に示します。

    | イベント         | カテゴリー | 説明                |
    | ------------ | ----- | ----------------- |
    | 全て           |       | すべてのイベントが含まれます    |
    | すべてのdml      |       | すべてのDMLイベントが含まれます |
    | すべてのddl      |       | すべてのDDLイベントが含まれます |
    | なし           |       | イベントは含まれていません     |
    | なしddl        |       | すべてのDDLイベントを除外します |
    | なしdml        |       | すべてのDMLイベントを除外します |
    | 入れる          | DML   | DMLイベントを挿入します     |
    | アップデート       | DML   | DMLイベントを更新する      |
    | 消去           | DML   | DMLイベントを削除する      |
    | データベースを作成する  | DDL   | データベースイベントの作成     |
    | データベースを削除します | DDL   | データベースイベントの削除     |
    | テーブルを作成する    | DDL   | テーブルイベントの作成       |
    | インデックスを作成する  | DDL   | インデックスイベントの作成     |
    | ドロップテーブル     | DDL   | ドロップテーブルイベント      |
    | テーブルを切り捨てます  | DDL   | テーブルイベントの切り捨て     |
    | テーブルの名前を変更   | DDL   | テーブルイベントの名前を変更    |
    | ドロップインデックス   | DDL   | ドロップインデックスイベント    |
    | 他の机          | DDL   | テーブルイベントの変更       |

-   `sql-pattern` ：指定されたDDLSQLステートメントをフィルタリングします。マッチングルールは、正規表現の使用をサポートしています。

-   `action` ： `Do`または`Ignore`

    -   `Do` ：許可リスト。次の2つの条件のいずれかを満たす場合、binlogイベントが複製されます。

        -   イベントはルール設定と一致します。
        -   sql-patternが指定されており、イベントのSQLステートメントがいずれかのsql-patternオプションと一致します。

    -   `Ignore` ：ブロックリスト。次の2つの条件のいずれかを満たす場合、binlogイベントは除外されます。

        -   イベントはルール設定と一致します。
        -   sql-patternが指定されており、イベントのSQLステートメントがいずれかのsql-patternオプションと一致します。

    `Do`と`Ignore`の両方が構成されている場合、 `Ignore`は`Do`よりも優先されます。つまり、 `Ignore`と`Do`の両方の条件を満たすイベントが除外されます。

## アプリケーションシナリオ {#application-scenarios}

このセクションでは、binlogイベントフィルターのアプリケーションシナリオについて説明します。

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

### シャーディングされたスキーマとテーブルのDML操作のみを移行します {#migrate-only-dml-operations-of-sharded-schemas-and-tables}

DMLステートメントのみを複製するには、以下に示すように2つの`Binlog event filter rule`を構成します。

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

### TiDBでサポートされていないSQLステートメントを除外する {#filter-out-sql-statements-not-supported-by-tidb}

TiDBでサポートされていないSQLステートメントを除外するには、以下に示すように`filter-procedure-rule`を構成します。

```
filters:
  filter-procedure-rule:
    schema-pattern: "*"
    sql-pattern: [".*\\s+DROP\\s+PROCEDURE", ".*\\s+CREATE\\s+PROCEDURE", "ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

> **警告：**
>
> 移行する必要のあるデータが除外されないようにするには、グローバルフィルタリングルールをできるだけ厳密に構成します。

## も参照してください {#see-also}

[SQL式を使用してBinlogイベントをフィルタリングする](/filter-dml-event.md)
