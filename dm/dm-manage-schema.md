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
    -   DMによって現在消費されているbinlogイベントのテーブルスキーマ`schema-B`として識別されます。このスキーマは、過去のアップストリームテーブルスキーマに対応しています。
    -   DM（スキーマトラッカーコンポーネント）で現在維持されているテーブルスキーマ`schema-I`として識別されます。
    -   `schema-D`として識別されるダウンストリームTiDBクラスタのテーブルスキーマ。

    ほとんどの場合、上記の4つのテーブルスキーマは同じです。

アップストリームデータベースがDDL操作を実行してテーブルスキーマを変更すると、 `schema-U`が変更されます。内部スキーマトラッカーコンポーネントとダウンストリームTiDBクラスタにDDL操作を適用することにより、DMは`schema-I`と`schema-D`を順番に更新し、 `schema-U`との整合性を維持します。したがって、DMは通常、 `schema-B`テーブルスキーマに対応するbinlogイベントを消費できます。つまり、DDL操作が正常に移行された後でも、 `schema-B` 、および`schema-U`は`schema-I`性があり`schema-D` 。

ただし、 [楽観的モードシャーディングDDLサポート](/dm/feature-shard-merge-optimistic.md)を有効にして移行中に、ダウンストリームテーブルの`schema-D`が、一部のアップストリームシャードテーブルの`schema-B`および`schema-I`と一致しない場合があります。このような場合でも、DMは`schema-I`と`schema-B`の一貫性を維持して、DMLに対応するbinlogイベントを正常に解析できるようにします。

さらに、一部のシナリオ（ダウンストリームテーブルにアップストリームテーブルよりも多くの列がある場合など）では、 `schema-D`が`schema-B`および`schema-I`と矛盾する場合があります。

上記のシナリオをサポートし、スキーマの不整合によって引き起こされる他の移行の中断を処理するために、DMは、DMに保持されている`schema-I`のテーブルスキーマを取得、変更、および削除する`operate-schema`のコマンドを提供します。

## 指示 {#command}

{{< copyable "" >}}

```bash
help operate-schema
```

```
`get`/`set`/`remove` the schema for an upstream table.

Usage:
  dmctl operate-schema <operate-type> <-s source ...> <task-name | task-file> <-d database> <-t table> [schema-file] [--flush] [--sync] [flags]

Flags:
  -d, --database string   database name of the table
      --flush             flush the table info and checkpoint immediately
  -h, --help              help for operate-schema
      --sync              sync the table info to master to resolve shard ddl lock, only for optimistic mode now
  -t, --table string      table name

Global Flags:
  -s, --source strings   MySQL Source ID.
```

> **ノート：**
>
> -   データ移行中にテーブルスキーマが変更される可能性があるため、予測可能なテーブルスキーマを取得するには、現在、データ移行タスクが`Paused`状態の場合にのみ`operate-schema`コマンドを使用できます。
> -   誤った取り扱いによるデータの損失を回避するために、スキーマを変更する前に、まずテーブルスキーマを取得してバックアップすることを**強くお勧め**します。

## パラメーター {#parameters}

-   `operate-type` ：
    -   必須。
    -   スキーマに対する操作のタイプを指定します。オプションの値は、 `get` 、および`set` `remove` 。
-   `-s` ：
    -   必須。
    -   操作が適用されるMySQLソースを指定します。
-   `task-name | task-file` ：
    -   必須。
    -   タスク名またはタスクファイルのパスを指定します。
-   `-d` ：
    -   必須。
    -   テーブルが属するアップストリームデータベースの名前を指定します。
-   `-t` ：
    -   必須。
    -   テーブルに対応するアップストリームテーブルの名前を指定します。
-   `schema-file` ：
    -   操作タイプが`set`の場合に必要です。他の操作タイプの場合はオプション。
    -   設定するテーブルスキーマファイル。ファイルの内容は有効な`CREATE TABLE`ステートメントである必要があります。
-   `--flush` ：
    -   オプション。
    -   DMがタスクの再開後にスキーマをロードできるように、スキーマをチェックポイントに書き込みます。
    -   デフォルト値は`true`です。
-   `--sync` ：
    -   オプション。楽観的シャーディングDDLモードでエラーが発生した場合にのみ使用されます。
    -   このスキーマで楽観的なシャーディングメタデータを更新します。

## 使用例 {#usage-example}

### テーブルスキーマを取得する {#get-the-table-schema}

`db_single`タスクの`mysql-replica-01`ソースに対応する`` `db_single`.`t1` ``テーブルのテーブルスキーマを取得する場合は、次のコマンドを実行します。

{{< copyable "" >}}

```bash
operate-schema get -s mysql-replica-01 task_single -d db_single -t t1
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

### テーブルスキーマを設定する {#set-the-table-schema}

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

### テーブルスキーマを削除する {#delete-table-schema}

> **ノート：**
>
> DMに保持されているテーブルスキーマが削除された後、このテーブルに関連するDDL / DMLステートメントをダウンストリームに移行する必要がある場合、DMは次の3つのソースからテーブルスキーマを順番に取得しようとします。
>
> -   チェックポイントテーブルの`table_info`フィールド
> -   楽観的シャーディングDDLのメタ情報
> -   ダウンストリームTiDBの対応するテーブル

`db_single`タスクの`mysql-replica-01`ソースに対応する`` `db_single`.`t1` ``テーブルのテーブルスキーマを削除する場合は、次のコマンドを実行します。

{{< copyable "" >}}

```bash
operate-schema remove -s mysql-replica-01 task_single -d db_single -t t1
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
