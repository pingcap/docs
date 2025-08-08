---
title: Manage Table Schemas of Tables to Be Migrated Using TiDB Data Migration
summary: DM で移行するテーブルのスキーマを管理する方法を学習します。
---

# TiDB データ移行を使用して移行するテーブルのテーブルスキーマを管理する {#manage-table-schemas-of-tables-to-be-migrated-using-tidb-data-migration}

このドキュメントでは、 [dmctl](/dm/dmctl-introduction.md)使用して移行中に DM でテーブルのスキーマを管理する方法について説明します。

DMが増分レプリケーションを実行する際、まず上流のbinlogを読み取り、SQL文を作成して下流で実行します。ただし、上流のbinlogには完全なテーブルスキーマは含まれていません。SQL文を生成するために、DMは移行対象のテーブルのスキーマ情報を内部的に保持します。これを内部テーブルスキーマと呼びます。

特別な状況に対処したり、テーブル スキーマの不一致によって発生する移行の中断を処理したりするために、DM は内部テーブル スキーマを取得、変更、および削除する`binlog-schema`コマンドを提供します。

## 実施原則 {#implementation-principles}

内部テーブル スキーマは次のソースから取得されます。

-   完全データ移行（ `task-mode=all` ）では、移行タスクはダンプ/ロード/同期の3段階（完全エクスポート、完全インポート、増分レプリケーション）を経ます。ダンプ段階では、DMはデータとともにテーブルスキーマ情報をエクスポートし、下流の対応するテーブルを自動的に作成します。同期段階では、このテーブルスキーマが増分レプリケーションの開始テーブルスキーマとして使用されます。
-   同期ステージでは、DM が`ALTER TABLE`などの DDL ステートメントを処理するときに、同時に内部テーブル スキーマを更新します。
-   タスクが増分移行（ `task-mode=incremental` ）の場合、下流のデータベースで移行対象のテーブルの作成が完了していると、DMは下流のデータベースからテーブルスキーマ情報を取得します。この動作はDMのバージョンによって異なります。

増分レプリケーションでは、スキーマのメンテナンスが複雑になります。データレプリケーション全体を通して、以下の4つのテーブルスキーマが関係します。これらのスキーマは、互いに整合性が取れている場合もあれば、不整合になっている場合もあります。

![schema](/media/dm/operate-schema.png)

-   現在の時点のアップストリーム テーブル スキーマ`schema-U`として識別されます。
-   現在DMで消費されているbinlogイベントのテーブルスキーマ（ `schema-B`で識別）。このスキーマは、過去の時点のアップストリームテーブルスキーマに対応しています。
-   現在 DM (スキーマ トラッカーコンポーネント) で管理されているテーブル スキーマ`schema-I`として識別されます。
-   ダウンストリーム TiDB クラスター内のテーブル スキーマ`schema-D`として識別)。

ほとんどの場合、前述の 4 つのテーブル スキーマは一貫しています。

上流データベースがテーブルスキーマを変更するDDL操作を実行すると、 `schema-U`変更されます。このDDL操作を内部スキーマトラッカーコンポーネントと下流TiDBクラスタに適用することで、DMは`schema-I`と`schema-D`順序正しく更新し、 `schema-U`との整合性を維持します。これにより、DMは`schema-B`テーブルスキーマに対応するbinlogイベントを正常に処理できます。つまり、DDL操作`schema-B`正常に移行された後も、 `schema-U` `schema-I`および`schema-D`整合性を維持します。

不整合が発生する可能性がある次の状況に注意してください。

-   [楽観的モードシャーディングDDLサポート](/dm/feature-shard-merge-optimistic.md)を有効にした移行中に、下流テーブルの`schema-D` 、上流の一部のシャードテーブルの`schema-B`および`schema-I`と不整合になる可能性があります。このような場合でも、DM は`schema-I`と`schema-B`整合性を維持し、DML に対応するbinlogイベントを正常に解析できるようにします。

-   下流テーブルに上流テーブルよりも多くの列がある場合、 `schema-D` `schema-B`および`schema-I`と不整合になる可能性があります。完全なデータ移行（ `task-mode=all` ）では、DMが自動的に不整合を処理します。増分移行（ `task-mode=incremental` ）では、タスクが初めて開始され、内部スキーマ情報がまだないため、DMは自動的に下流スキーマ（ `schema-D` ）を読み取り、 `schema-I`更新します（この動作はDMのバージョンによって異なります）。その後、DMが`schema-I`使用して`schema-B`のbinlogを解析すると、 `Column count doesn't match value count`エラーが報告されます。詳細については、 [より多くの列を持つ下流の TiDB テーブルにデータを移行する](/migrate-with-more-columns-downstream.md)を参照してください。

`binlog-schema`コマンドを実行して、DM で管理されている`schema-I`テーブル スキーマを取得、変更、または削除できます。

> **注記：**
>
> `binlog-schema`コマンドは DM v6.0 以降のバージョンでのみサポートされます。それ以前のバージョンでは、 `operate-schema`コマンドを使用する必要があります。

## 指示 {#command}

```bash
help binlog-schema
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

> **注記：**
>
> -   データ移行中にテーブル スキーマが変更される可能性があるため、予測可能なテーブル スキーマを取得するには、現在、データ移行タスクが`Paused`状態にある場合にのみ`binlog-schema`コマンドを使用できます。
> -   誤った取り扱いによるデータ損失を避けるため、スキーマを変更する前に、まずテーブル スキーマを取得してバックアップすること**を強くお勧めします**。

## パラメータ {#parameters}

-   `delete` : テーブル スキーマを削除します。
-   `list` : テーブル スキーマを一覧表示します。
-   `update` : テーブル スキーマを更新します。
-   `-s`または`--source` :
    -   必須。
    -   操作が適用される MySQL ソースを指定します。

## 使用例 {#usage-example}

### テーブルスキーマを取得する {#get-the-table-schema}

テーブル スキーマを取得するには、コマンド`binlog-schema list`実行します。

```bash
help binlog-schema list
```

    show table schema structure

    Usage:
      dmctl binlog-schema list <task-name> <database> <table> [flags]

    Flags:
      -h, --help   help for list

    Global Flags:
      -s, --source strings   MySQL Source ID.

`db_single`タスク内の`mysql-replica-01` MySQL ソースに対応する`` `db_single`.`t1` ``テーブルのテーブル スキーマを取得する場合は、次のコマンドを実行します。

```bash
binlog-schema list -s mysql-replica-01 task_single db_single t1
```

    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "CREATE TABLE `t1` ( `c1` int NOT NULL, `c2` int DEFAULT NULL, PRIMARY KEY (`c1`)) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin",
                "source": "mysql-replica-01",
                "worker": "127.0.0.1:8262"
            }
        ]
    }

### テーブルスキーマを更新する {#update-the-table-schema}

テーブル スキーマを更新するには、 `binlog-schema update`コマンドを実行します。

```bash
help binlog-schema update
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

`db_single`タスクで`mysql-replica-01` MySQL ソースに対応する`` `db_single`.`t1` ``テーブルのテーブルスキーマを次のように設定する場合:

```sql
CREATE TABLE `t1` (
    `c1` int NOT NULL,
    `c2` bigint DEFAULT NULL,
    PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin
```

上記の`CREATE TABLE`ステートメントをファイルとして保存し (たとえば、 `db_single.t1-schema.sql` )、次のコマンドを実行します。

```bash
operate-schema set -s mysql-replica-01 task_single -d db_single -t t1 db_single.t1-schema.sql
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

### テーブルスキーマを削除する {#delete-the-table-schema}

テーブル スキーマを削除するには、 `binlog-schema delete`コマンドを実行します。

```bash
help binlog-schema delete
```

    delete table schema structure

    Usage:
      dmctl binlog-schema delete <task-name> <database> <table> [flags]

    Flags:
      -h, --help   help for delete

    Global Flags:
      -s, --source strings   MySQL Source ID.

> **注記：**
>
> DM で管理されているテーブル スキーマが削除された後、このテーブルに関連する DDL/DML ステートメントをダウンストリームに移行する必要がある場合、DM は次の 3 つのソースからテーブル スキーマを順番に取得しようとします。
>
> -   チェックポイントテーブルの`table_info`フィールド
> -   楽観的シャーディングDDLのメタ情報
> -   下流TiDBの対応するテーブル

`db_single`タスク内の`mysql-replica-01` MySQL ソースに対応する`` `db_single`.`t1` ``テーブルのテーブル スキーマを削除する場合は、次のコマンドを実行します。

```bash
binlog-schema delete -s mysql-replica-01 task_single db_single t1
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
