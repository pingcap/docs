---
title: Manage Table Schemas of Tables to Be Migrated Using TiDB Data Migration
summary: DM で移行するテーブルのスキーマを管理する方法を学習します。
---

# TiDB データ移行を使用して移行するテーブルのテーブル スキーマを管理する {#manage-table-schemas-of-tables-to-be-migrated-using-tidb-data-migration}

このドキュメントでは、 [dmctl](/dm/dmctl-introduction.md)を使用して移行中に DM でテーブルのスキーマを管理する方法について説明します。

DM が増分レプリケーションを実行する場合、最初にアップストリームbinlogを読み取り、次に SQL 文を作成してダウンストリームで実行します。ただし、アップストリームbinlogには完全なテーブル スキーマは含まれていません。SQL 文を生成するために、DM は移行するテーブルのスキーマ情報を内部的に保持します。これを内部テーブル スキーマと呼びます。

特別な状況に対処するため、またはテーブル スキーマの不一致によって発生する移行の中断を処理するために、DM は内部テーブル スキーマを取得、変更、および削除するための`binlog-schema`コマンドを提供します。

## 実施原則 {#implementation-principles}

内部テーブル スキーマは次のソースから取得されます。

-   完全なデータ移行（ `task-mode=all` ）の場合、移行タスクは、ダンプ/ロード/同期（完全なエクスポート、完全なインポート、増分レプリケーション）の3つの段階を経ます。ダンプ段階では、DMはデータとともにテーブルスキーマ情報をエクスポートし、下流に対応するテーブルを自動的に作成します。同期段階では、このテーブルスキーマが増分レプリケーションの開始テーブルスキームとして使用されます。
-   同期ステージでは、DM が`ALTER TABLE`などの DDL ステートメントを処理するときに、同時に内部テーブル スキーマを更新します。
-   タスクが増分移行（ `task-mode=incremental` ）であり、ダウンストリームが移行対象のテーブルの作成を完了している場合、DM はダウンストリーム データベースからテーブル スキーマ情報を取得します。この動作は DM のバージョンによって異なります。

増分レプリケーションの場合、スキーマのメンテナンスは複雑です。データ レプリケーション全体にわたって、次の 4 つのテーブル スキーマが関係します。これらのスキーマは、互いに一貫している場合も、一貫していない場合もあります。

![schema](/media/dm/operate-schema.png)

-   現時点でのアップストリーム テーブル スキーマ`schema-U`として識別されます。
-   現在 DM によって消費されているbinlogイベントのテーブル スキーマ`schema-B`として識別)。このスキーマは、履歴時点のアップストリーム テーブル スキーマに対応します。
-   現在 DM (スキーマ トラッカーコンポーネント) で管理されているテーブル スキーマ`schema-I`として識別されます。
-   ダウンストリーム TiDB クラスター内のテーブル スキーマ ( `schema-D`として識別されます)。

ほとんどの場合、前述の 4 つのテーブル スキーマは一貫しています。

上流データベースがテーブルスキーマを変更する DDL 操作を実行すると、 `schema-U`変更されます。内部スキーマトラッカーコンポーネントと下流 TiDB クラスターに DDL 操作を適用することで、 DM は`schema-I`と`schema-D`を順序どおりに更新し、 `schema-U`との一貫性を保ちます。したがって、 DM は`schema-B`テーブルスキーマに対応するbinlogイベントを正常に消費できます。つまり、 DDL 操作が正常に移行された後も、 `schema-U` 、 `schema-B` 、 `schema-I` 、および`schema-D`一貫性を保ちます。

不整合が発生する可能性がある次の状況に注意してください。

-   [楽観的モード シャーディング DDL サポート](/dm/feature-shard-merge-optimistic.md)を有効にして移行すると、ダウンストリーム テーブルの`schema-D` 、一部のアップストリーム シャード テーブルの`schema-B`および`schema-I`と一致しなくなる可能性があります。このような場合でも、DM は`schema-I`と`schema-B`一貫性を保ち、DML に対応するbinlogイベントを正常に解析できるようにします。

-   ダウンストリーム テーブルにアップストリーム テーブルよりも多くの列がある場合、 `schema-D` `schema-B`および`schema-I`と矛盾する可能性があります。フル データ移行 ( `task-mode=all` ) では、 DM は矛盾を自動的に処理します。増分移行 ( `task-mode=incremental` ) では、タスクが初めて開始され、内部スキーマ情報がまだないため、 DM はダウンストリーム スキーマ ( `schema-D` ) を自動的に読み取り、 `schema-I`を更新します (この動作は DM のバージョンによって異なります)。その後、 DM が`schema-I`を使用して`schema-B`のbinlogを解析すると、 `Column count doesn't match value count`エラーが報告されます。詳細については、 [より多くの列を持つ下流の TiDB テーブルにデータを移行する](/migrate-with-more-columns-downstream.md)を参照してください。

`binlog-schema`コマンドを実行して、DM で管理されている`schema-I`テーブル スキーマを取得、変更、または削除できます。

> **注記：**
>
> `binlog-schema`コマンドは DM v6.0 以降のバージョンでのみサポートされます。それより前のバージョンでは、 `operate-schema`コマンドを使用する必要があります。

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
> -   誤った取り扱いによるデータ損失を避けるため、スキーマを変更する前に、まずテーブル スキーマを取得してバックアップすることを**強くお勧めします**。

## パラメーター {#parameters}

-   `delete` : テーブル スキーマを削除します。
-   `list` : テーブル スキーマを一覧表示します。
-   `update` : テーブル スキーマを更新します。
-   `-s`または`--source` :
    -   必須。
    -   操作が適用される MySQL ソースを指定します。

## 使用例 {#usage-example}

### テーブルスキーマを取得する {#get-the-table-schema}

テーブル スキーマを取得するには、コマンド`binlog-schema list`を実行します。

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

`db_single`タスクの`mysql-replica-01` MySQL ソースに対応する`` `db_single`.`t1` ``テーブルのテーブル スキーマを取得する場合は、次のコマンドを実行します。

```bash
binlog-schema list -s mysql-replica-01 task_single db_single t1
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

`db_single`タスク内の`mysql-replica-01` MySQL ソースに対応する`` `db_single`.`t1` ``テーブルのテーブル スキーマを次のように設定する場合:

```sql
CREATE TABLE `t1` (
    `c1` int(11) NOT NULL,
    `c2` bigint(11) DEFAULT NULL,
    PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin
```

上記の`CREATE TABLE`ステートメントをファイル (たとえば、 `db_single.t1-schema.sql` ) として保存し、次のコマンドを実行します。

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
