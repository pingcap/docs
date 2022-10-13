---
title: Manage Table Schemas of Tables to be Migrated
summary: Learn how to manage the schema of the table to be migrated in DM.
---

# 移行するテーブルのテーブル スキーマの管理 {#manage-table-schemas-of-tables-to-be-migrated}

このドキュメントでは、 [dmctl](/dm/dmctl-introduction.md)を使用して移行中に DM でテーブルのスキーマを管理する方法について説明します。

## 実施原則 {#implementation-principles}

DM を使用してテーブルを移行する場合、DM はテーブル スキーマに対して次の操作を実行します。

-   完全なエクスポートとインポートの場合、DM は現在の上流のテーブル スキーマを SQL ファイルに直接エクスポートし、そのテーブル スキーマを下流に適用します。

-   増分レプリケーションの場合、データ リンク全体に次のテーブル スキーマが含まれます。これらは同じ場合も異なる場合もあります。

    ![schema](/media/dm/operate-schema.png)

    -   `schema-U`として識別される、現時点でのアップストリーム テーブル スキーマ。
    -   `schema-B`として識別される、現在 DM によって消費されている binlog イベントのテーブル スキーマ。このスキーマは、過去の時点での上流のテーブル スキーマに対応します。
    -   `schema-I`として識別される、現在 DM (スキーマ トラッカー コンポーネント) で維持されているテーブル スキーマ。
    -   `schema-D`として識別される、ダウンストリーム TiDB クラスター内のテーブル スキーマ。

    ほとんどの場合、上記の 4 つのテーブル スキーマは同じです。

アップストリーム データベースが DDL 操作を実行してテーブル スキーマを変更すると、 `schema-U`が変更されます。 DDL 操作を内部スキーマ トラッカー コンポーネントとダウンストリームの TiDB クラスターに適用することにより、DM は`schema-I`と`schema-D`を順番に更新して`schema-U`との一貫性を保ちます。したがって、DM は通常、 `schema-B`テーブル スキーマに対応する binlog イベントを使用できます。つまり、DDL 操作が正常に移行された後でも、 `schema-U` 、 `schema-B` 、 `schema-I` 、および`schema-D`は一貫しています。

ただし、 [オプティミスティック モード シャーディング DDL サポート](/dm/feature-shard-merge-optimistic.md)が有効になっている移行中に、ダウンストリーム テーブルの`schema-D`が、一部のアップストリーム シャード テーブルの`schema-B`および`schema-I`と一致しない場合があります。このような場合でも、DM は`schema-I`と`schema-B`の一貫性を保ち、DML に対応する binlog イベントを正常に解析できるようにします。

さらに、一部のシナリオ (下流のテーブルに上流のテーブルよりも多くの列がある場合など) では、 `schema-D`が`schema-B`および`schema-I`と一致しない場合があります。

上記のシナリオをサポートし、スキーマの不一致によって引き起こされるその他の移行の中断を処理するために、DM は、DM で維持される`schema-I`のテーブル スキーマを取得、変更、および削除するための`binlog-schema`のコマンドを提供します。

> **ノート：**
>
> `binlog-schema`コマンドは、DM v6.0 以降のバージョンでのみサポートされています。以前のバージョンでは、 `operate-schema`コマンドを使用する必要があります。

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
> -   テーブル スキーマはデータ移行中に変更される可能性があるため、予測可能なテーブル スキーマを取得するために、現在、データ移行タスクが`Paused`状態にある場合にのみ`binlog-schema`コマンドを使用できます。
> -   誤った取り扱いによるデータ損失を避けるために、スキーマを変更する前に、まずテーブル スキーマを取得してバックアップすることを**強くお勧め**します。

## パラメーター {#parameters}

-   `delete` : テーブル スキーマを削除します。
-   `list` : テーブル スキーマを一覧表示します。
-   `update` : テーブル スキーマを更新します。
-   `-s`または`--source` :
    -   必須。
    -   操作が適用される MySQL ソースを指定します。

## 使用例 {#usage-example}

### テーブル スキーマを取得する {#get-the-table-schema}

テーブル スキーマを取得するには、次の`binlog-schema list`コマンドを実行します。

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

`db_single`番目のタスクで`mysql-replica-01`番目の MySQL ソースに対応する`` `db_single`.`t1` ``番目のテーブルのテーブル スキーマを取得する場合は、次のコマンドを実行します。

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

### テーブル スキーマを更新する {#update-the-table-schema}

テーブル スキーマを更新するには、次の`binlog-schema update`コマンドを実行します。

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

`db_single`タスクで`mysql-replica-01` MySQL ソースに対応する`` `db_single`.`t1` ``テーブルのテーブル スキーマを次のように設定する場合:

```sql
CREATE TABLE `t1` (
    `c1` int(11) NOT NULL,
    `c2` bigint(11) DEFAULT NULL,
    PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin
```

上記の`CREATE TABLE`ステートメントをファイル (たとえば、 `db_single.t1-schema.sql` ) として保存し、次のコマンドを実行します。

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

### テーブル スキーマを削除する {#delete-the-table-schema}

テーブル スキーマを削除するには、次の`binlog-schema delete`コマンドを実行します。

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
> DM で保持されているテーブル スキーマが削除された後、このテーブルに関連する DDL/DML ステートメントをダウンストリームに移行する必要がある場合、DM は次の 3 つのソースから順番にテーブル スキーマを取得しようとします。
>
> -   チェックポイント テーブルの`table_info`フィールド
> -   オプティミスティック シャーディング DDL のメタ情報
> -   下流の TiDB の対応するテーブル

`db_single`タスクで`mysql-replica-01` MySQL ソースに対応する`` `db_single`.`t1` ``テーブルのテーブル スキーマを削除する場合は、次のコマンドを実行します。

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
