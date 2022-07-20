---
title: Manage Table Schemas of Tables to be Migrated
summary: Learn how to manage the schema of the table to be migrated in DM.
---

# 移行するテーブルのテーブルスキーマを管理する {#manage-table-schemas-of-tables-to-be-migrated}

このドキュメントでは、 [dmctl](/dm/dmctl-introduction.md)を使用して移行中にDMでテーブルのスキーマを管理する方法について説明します。

## 実装の原則 {#implementation-principles}

DMを使用してテーブルを移行する場合、DMはテーブルスキーマに対して次の操作を実行します。

-   完全なエクスポートとインポートの場合、DMは現在の時刻のアップストリームテーブルスキーマをSQLファイルに直接エクスポートし、テーブルスキーマをダウンストリームに適用します。

-   インクリメンタルレプリケーションの場合、データリンク全体に次のテーブルスキーマが含まれます。これらは同じでも異なる場合もあります。

    ![schema](/media/dm/operate-schema.png)

    -   `schema-U`として識別される、現時点でのアップストリームテーブルスキーマ。
    -   DMによって現在消費されているbinlogイベントのテーブルスキーマ`schema-B`として識別されます。このスキーマは、履歴時のアップストリームテーブルスキーマに対応します。
    -   `schema-I`として識別されるDM（スキーマトラッカーコンポーネント）で現在維持されているテーブルスキーマ。
    -   `schema-D`として識別されるダウンストリームTiDBクラスタのテーブルスキーマ。

    ほとんどの場合、上記の4つのテーブルスキーマは同じです。

アップストリームデータベースがDDL操作を実行してテーブルスキーマを変更すると、 `schema-U`が変更されます。内部スキーマトラッカーコンポーネントとダウンストリームTiDBクラスタにDDL操作を適用することにより、DMは`schema-I`と`schema-D`を順番に更新し、 `schema-U`との整合性を維持します。したがって、DMは通常、 `schema-B`テーブルスキーマに対応するbinlogイベントを消費できます。つまり、DDL操作が正常に移行された後でも、 `schema-B` 、および`schema-U`は`schema-I`性があり`schema-D` 。

ただし、 [オプティミスティックモードシャーディングDDLサポート](/dm/feature-shard-merge-optimistic.md)を有効にして移行中に、ダウンストリームテーブルの`schema-D`が、一部のアップストリームシャードテーブルの`schema-B`および`schema-I`と一致しない場合があります。このような場合でも、DMは`schema-I`と`schema-B`の一貫性を維持して、DMLに対応するbinlogイベントを正常に解析できるようにします。

さらに、一部のシナリオ（ダウンストリームテーブルにアップストリームテーブルよりも多くの列がある場合など）では、 `schema-D`が`schema-B`および`schema-I`と矛盾する場合があります。

上記のシナリオをサポートし、スキーマの不整合によって引き起こされる他の移行の中断を処理するために、DMは、DMに保持されている`schema-I`のテーブルスキーマを取得、変更、および削除する`binlog-schema`のコマンドを提供します。

> **ノート：**
>
> `binlog-schema`コマンドは、DMv6.0以降のバージョンでのみサポートされます。以前のバージョンでは、 `operate-schema`コマンドを使用する必要があります。

## 指示 {#command}

{{< copyable "" >}}

```bash
help binlog-schema
```

```
manage or show table schema in schema tracker

Usage:
  dmctl binlog-schema [command]

Available Commands:
  delete      delete table schema structure
  list        show table schema structure
  update      update tables schema structure

Flags:
  -h, --help   help for binlog-schema

Global Flags:
  -s, --source strings   MySQL Source ID.

Use "dmctl binlog-schema [command] --help" for more information about a command.
```

> **ノート：**
>
> -   データ移行中にテーブルスキーマが変更される可能性があるため、予測可能なテーブルスキーマを取得するには、現在、データ移行タスクが`Paused`状態の場合にのみ`binlog-schema`コマンドを使用できます。
> -   誤った取り扱いによるデータの損失を避けるために、スキーマを変更する前に、まずテーブルスキーマを取得してバックアップすることを**強くお勧め**します。

## パラメーター {#parameters}

-   `delete` ：テーブルスキーマを削除します。
-   `list` ：テーブルスキーマを一覧表示します。
-   `update` ：テーブルスキーマを更新します。
-   `-s`または`--source` ：
    -   必須。
    -   操作が適用されるMySQLソースを指定します。

## 使用例 {#usage-example}

### テーブルスキーマを取得する {#get-the-table-schema}

テーブルスキーマを取得するには、 `binlog-schema list`コマンドを実行します。

```bash
help binlog-schema list
```

```
show table schema structure

Usage:
  dmctl binlog-schema list <task-name> <database> <table> [flags]

Flags:
  -h, --help   help for list

Global Flags:
  -s, --source strings   MySQL Source ID.
```

`db_single`タスクの`mysql-replica-01`ソースに対応する`` `db_single`.`t1` ``テーブルのテーブルスキーマを取得する場合は、次のコマンドを実行します。

{{< copyable "" >}}

```bash
binlog-schema list -s mysql-replica-01 task_single db_single t1
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "CREATE TABLE `t1` ( `c1` int(11) NOT NULL, `c2` int(11) DEFAULT NULL, PRIMARY KEY (`c1`)) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```

### テーブルスキーマを更新します {#update-the-table-schema}

テーブルスキーマを更新するには、次の`binlog-schema update`コマンドを実行します。

{{< copyable "" >}}

```bash
help binlog-schema update
```

```
update tables schema structure

Usage:
  dmctl binlog-schema update <task-name> <database> <table> [schema-file] [flags]

Flags:
      --flush         flush the table info and checkpoint immediately (default true)
      --from-source   use the schema from upstream database as the schema of the specified tables
      --from-target   use the schema from downstream database as the schema of the specified tables
  -h, --help          help for update
      --sync          sync the table info to master to resolve shard ddl lock, only for optimistic mode now (default true)

Global Flags:
  -s, --source strings   MySQL Source ID.
```

次のように、 `db_single`のタスクで`mysql-replica-01`のMySQLソースに対応する`` `db_single`.`t1` ``のテーブルのテーブルスキーマを設定する場合：

```sql
CREATE TABLE `t1` (
    `c1` int(11) NOT NULL,
    `c2` bigint(11) DEFAULT NULL,
    PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin
```

上記の`CREATE TABLE`のステートメントをファイル（たとえば、 `db_single.t1-schema.sql` ）として保存し、次のコマンドを実行します。

{{< copyable "" >}}

```bash
operate-schema set -s mysql-replica-01 task_single -d db_single -t t1 db_single.t1-schema.sql
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```

### テーブルスキーマを削除します {#delete-the-table-schema}

テーブルスキーマを削除するには、次の`binlog-schema delete`コマンドを実行します。

```bash
help binlog-schema delete
```

```
delete table schema structure

Usage:
  dmctl binlog-schema delete <task-name> <database> <table> [flags]

Flags:
  -h, --help   help for delete

Global Flags:
  -s, --source strings   MySQL Source ID.
```

> **ノート：**
>
> DMに保持されているテーブルスキーマが削除された後、このテーブルに関連するDDL / DMLステートメントをダウンストリームに移行する必要がある場合、DMは次の3つのソースからテーブルスキーマを順番に取得しようとします。
>
> -   チェックポイントテーブルの`table_info`フィールド
> -   楽観的なシャーディングDDLのメタ情報
> -   ダウンストリームTiDBの対応するテーブル

`db_single`タスクの`mysql-replica-01`ソースに対応する`` `db_single`.`t1` ``テーブルのテーブルスキーマを削除する場合は、次のコマンドを実行します。

{{< copyable "" >}}

```bash
binlog-schema delete -s mysql-replica-01 task_single db_single t1
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```
