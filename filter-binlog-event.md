---
title: Filter Binlog Events
summary: データを移行するときにbinlogイベントをフィルター処理する方法を学びます。
---

# Binlogイベントをフィルタリングする {#filter-binlog-events}

このドキュメントでは、DMを使用して継続的な増分データレプリケーションを実行する際に、 binlogイベントをフィルタリングする方法について説明します。レプリケーションの詳細な手順については、シナリオごとに以下のドキュメントを参照してください。

- [小規模データセットをMySQLからTiDBに移行する](/migrate-small-mysql-to-tidb.md)
- [大規模データセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)
- [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)
- [大規模データセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## 設定 {#configuration}

binlogイベントフィルターを使用するには、以下に示すように、DM のタスク設定ファイルに`filters`フィールドを追加します。

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    action: Ignore
```

- `schema-pattern` / `table-pattern` : 一致するスキーマまたはテーブルをフィルターします

- `events` : binlogイベントをフィルタリングします。サポートされているイベントは以下の表のとおりです。

    | イベント         | カテゴリ | 説明                |
    | ------------ | ---- | ----------------- |
    | all           |      | すべてのイベントを含む       |
    | all dml      |      | すべてのDMLイベントを含む    |
    | all ddl      |      | すべてのDDLイベントを含む    |
    | none           |      | イベントは含まれません       |
    | none ddl        |      | すべてのDDLイベントを除外します |
    | none dml       |      | すべてのDMLイベントを除外します |
    | insert          | DML  | DMLイベントを挿入        |
    | update       | DML  | DMLイベントの更新        |
    | delete           | DML  | DMLイベントの削除        |
    | create database  | DDL  | データベースイベントの作成     |
    | drop database    | DDL  | データベースイベントの削除     |
    | create table    | DDL  | テーブルイベントの作成       |
    | create index  | DDL  | インデックスイベントの作成     |
    | drop table     | DDL  | ドロップテーブルイベント      |
    | truncate table   | DDL  | テーブル切り捨てイベント      |
    | rename table | DDL  | テーブル名の変更イベント      |
    | drop index    | DDL  | インデックス削除イベント      |
    | alter table    | DDL  | テーブル変更イベント        |

- `sql-pattern` : 指定されたDDL SQL文をフィルタリングします。マッチングルールでは正規表現の使用がサポートされています。

- `action` ： `Do`または`Ignore`

    - `Do` : 許可リスト。以下の2つの条件のいずれかを満たす場合、 binlogイベントは複製されます。

        - イベントはルール設定と一致します。
        - sql-pattern が指定されており、イベントの SQL文が sql-pattern オプションのいずれかと一致します。

    - `Ignore` ：ブロックリスト。以下の2つの条件のいずれかを満たす場合、 binlogイベントはフィルタリングされます。

        - イベントはルール設定と一致します。
        - sql-pattern が指定されており、イベントの SQL文が sql-pattern オプションのいずれかと一致します。

    `Do`と`Ignore`両方が設定されている場合、 `Ignore`の方が`Do`よりも優先されます。つまり、 `Ignore`と`Do`両方の条件を満たすイベントは除外されます。

## アプリケーションシナリオ {#application-scenarios}

このセクションでは、 binlogイベントフィルターの適用シナリオについて説明します。

### すべてのシャーディング削除操作を除外する {#filter-out-all-sharding-deletion-operations}

すべての削除操作を除外するには、次に示すように`filter-table-rule`と`filter-schema-rule`を設定します。

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

### シャーディングされたスキーマとテーブルのDML操作のみを移行する {#migrate-only-dml-operations-of-sharded-schemas-and-tables}

DML文のみをレプリケートするには、次に示すように`Binlog event filter rule`を 2つ設定します。

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

### TiDB がサポートしていない SQL 文、または DM が解析できない SQL 文を処理する {#handle-sql-statements-that-tidb-does-not-support-or-that-dm-cannot-parse}

`CREATE PROCEDURE`、`DROP PROCEDURE`、または `ALTER PROCEDURE` に対してフィルターを設定する必要はありません。DM はこれらのステートメントを自動的にスキップします。

MySQL でパーティションを追加または削除すると、DM は通常その変更を TiDB にレプリケートします。DM と TiDB の両方がサポートするパーティション操作にはフィルターは不要です。テーブルのパーティションタイプに対して TiDB がどの操作をサポートしているかを確認するには、[パーティション管理](/partitioned-table.md#partition-management) を参照してください。

`ADD PARTITION` または `DROP PARTITION` を使用する `ALTER TABLE` ステートメントに対して DM が解析エラーを報告し、そのパーティション変更を TiDB にレプリケートする必要がない場合は、以下のルールを使用してそのステートメントをスキップできます。DM で解析エラーが発生しても、必ずしも TiDB がその操作をサポートしていないことを意味するわけではありません。

DM がステートメントを解析できない場合、特定のスキーマまたはテーブルを対象とするフィルターを適用できません。この場合、`schema-pattern: "*"` を指定し、`table-pattern` を指定しないグローバルフィルタリングルールが必要です。このルールは、移行タスク内のすべてのテーブルに対する一致ステートメントに適用されます。

> **Warning:**
>
> 移行する必要があるデータがフィルタリングされないようにするには、グローバルフィルタリングルールをできるだけ厳密に構成します。
>
> 次のパターンは文字列リテラルを含む SQL テキストに一致するため、意図せず他の DDL ステートメントをフィルタリングしてしまう可能性があります。たとえば、デフォルト値に `ADD PARTITION` を含む `ALTER TABLE ... ADD COLUMN` ステートメントもスキップされる可能性があります。このルールを使用する前に、レプリケートする必要がある DDL ステートメントにこれらのパターンが一致しないことを確認してください。

```
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

## 参照 {#see-also}

[SQL 式を使用してBinlogイベントをフィルタリングする](/filter-dml-event.md)
