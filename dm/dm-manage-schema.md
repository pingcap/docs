---
title: Manage Table Schemas of Tables to Be Migrated Using TiDB Data Migration
summary: Learn how to manage the schema of the table to be migrated in DM.
---

# TiDB データ移行を使用して移行するテーブルのテーブル スキーマを管理する {#manage-table-schemas-of-tables-to-be-migrated-using-tidb-data-migration}

このドキュメントでは、 [dmctl](/dm/dmctl-introduction.md)使用して移行中に DM でテーブルのスキーマを管理する方法について説明します。

DM が増分レプリケーションを実行する場合、最初にアップストリームのbinlogを読み取り、次に SQL ステートメントを作成してダウンストリームで実行します。ただし、上流のbinlog には完全なテーブル スキーマが含まれていません。 SQL ステートメントを生成するために、DM は移行するテーブルのスキーマ情報を内部的に保持します。これは、内部テーブル スキーマと呼ばれます。

特別な場合に対処するため、またはテーブル スキーマの不一致による移行の中断を処理するために、DM は、内部テーブル スキーマを取得、変更、および削除するための`binlog-schema`コマンドを提供します。

## 実施原則 {#implementation-principles}

内部テーブル スキーマは、次のソースから取得されます。

-   完全なデータ移行 ( `task-mode=all` ) の場合、移行タスクは次の 3 つの段階を経ます。ダンプ/ロード/同期、つまり、完全なエクスポート、完全なインポート、および増分レプリケーションです。ダンプ ステージでは、DM はデータと共にテーブル スキーマ情報をエクスポートし、対応するテーブルをダウンストリームに自動的に作成します。同期ステージでは、このテーブル スキーマが増分レプリケーションの開始テーブル スキームとして使用されます。
-   同期段階では、DM が`ALTER TABLE`などの DDL ステートメントを処理するときに、同時に内部テーブル スキーマを更新します。
-   タスクが増分移行 ( `task-mode=incremental` ) で、ダウンストリームが移行対象のテーブルの作成を完了している場合、DM はダウンストリーム データベースからテーブル スキーマ情報を取得します。この動作は、DM のバージョンによって異なります。

増分レプリケーションの場合、スキーマのメンテナンスは複雑です。データのレプリケーション全体では、次の 4 つのテーブル スキーマが関係します。これらのスキーマは、互いに一貫しているか、または一貫していない可能性があります。

![schema](/media/dm/operate-schema.png)

-   `schema-U`として識別される、現時点でのアップストリーム テーブル スキーマ。
-   `schema-B`として識別される、現在 DM によって消費されているbinlogイベントのテーブル スキーマ。このスキーマは、過去の時点での上流のテーブル スキーマに対応します。
-   `schema-I`として識別される、DM (スキーマ トラッカーコンポーネント) で現在維持されているテーブル スキーマ。
-   `schema-D`として識別される、ダウンストリーム TiDB クラスター内のテーブル スキーマ。

ほとんどの場合、前述の 4 つのテーブル スキーマは一貫しています。

アップストリーム データベースが DDL 操作を実行してテーブル スキーマを変更すると、 `schema-U`が変更されます。 DDL 操作を内部スキーマ トラッカーコンポーネントとダウンストリームの TiDB クラスターに適用することにより、DM は`schema-I`と`schema-D`を順番に更新して`schema-U`との一貫性を保ちます。したがって、DM は通常、 `schema-B`テーブル スキーマに対応するbinlogイベントを使用できます。つまり、DDL 操作が正常に移行された後でも、 `schema-U` 、 `schema-B` 、 `schema-I` 、および`schema-D`は一貫しています。

不整合の原因となる可能性がある次の状況に注意してください。

-   [楽観的モード シャーディング DDL サポート](/dm/feature-shard-merge-optimistic.md)を有効にして移行中に、ダウンストリーム テーブルの`schema-D` 、一部のアップストリーム シャード テーブルの`schema-B`および`schema-I`と一致しない場合があります。このような場合でも、DM は`schema-I`と`schema-B`の一貫性を保ち、DML に対応するbinlogイベントを正常に解析できるようにします。

-   下流のテーブルに上流のテーブルよりも多くの列がある場合、 `schema-D` `schema-B`および`schema-I`と矛盾する可能性があります。完全なデータ移行 ( `task-mode=all` ) では、DM は不整合を自動的に処理します。増分移行 ( `task-mode=incremental` ) では、タスクが最初に開始され、内部スキーマ情報がまだないため、DM は自動的にダウンストリーム スキーマを読み取り ( `schema-D` )、更新`schema-I`します (この動作は DM のバージョンによって異なります)。その後、DM が`schema-I`使用して`schema-B`のbinlogを解析すると、 `Column count doesn't match value count`エラーが報告されます。詳しくは[より多くの列を持つ下流の TiDB テーブルにデータを移行する](/migrate-with-more-columns-downstream.md)をご参照ください。

`binlog-schema`コマンドを実行して、DM で管理されている`schema-I`テーブル スキーマを取得、変更、または削除できます。

> **ノート：**
>
> `binlog-schema`コマンドは、DM v6.0 以降のバージョンでのみサポートされています。以前のバージョンでは、 `operate-schema`コマンドを使用する必要があります。

## 指図 {#command}

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
> -   誤った取り扱いによるデータ損失を避けるために、スキーマを変更する前に、まずテーブル スキーマを取得してバックアップすることを**強くお勧めします**。

## パラメーター {#parameters}

-   `delete` : テーブル スキーマを削除します。
-   `list` : テーブル スキーマを一覧表示します。
-   `update` : テーブル スキーマを更新します。
-   `-s`または`--source` :
    -   必要。
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

`db_single`番目のタスクで`mysql-replica-01`の MySQL ソースに対応する`` `db_single`.`t1` ``のテーブルのテーブル スキーマを取得する場合は、次のコマンドを実行します。

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
> -   楽観的シャーディング DDL のメタ情報
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
