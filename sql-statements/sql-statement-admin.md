---
title: ADMIN | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるADMINの使用方法の概要。
---

# 管理者 {#admin}

このステートメントは、TiDB のステータスを表示したり、TiDB 内のテーブルのデータをチェックしたりするために使用される TiDB 拡張構文です。このドキュメントでは、次の`ADMIN`関連のステートメントを紹介します。

-   [`ADMIN RELOAD`](#admin-reload-statement)
-   [`ADMIN PLUGINS`](#admin-plugins-related-statement)
-   [`ADMIN ... BINDINGS`](#admin-bindings-related-statement)
-   [`ADMIN REPAIR`](#admin-repair-statement)
-   [`ADMIN SHOW NEXT_ROW_ID`](#admin-show-next_row_id-statement)
-   [`ADMIN SHOW SLOW`](#admin-show-slow-statement)

## DDL関連の声明 {#ddl-related-statement}

<CustomContent platform="tidb-cloud">

| 声明                                                                                      | 説明                             |
| --------------------------------------------------------------------------------------- | ------------------------------ |
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)            | 現在実行中のDDLジョブをキャンセルします。         |
| [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)              | 現在実行中のDDLジョブを一時停止します。          |
| [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)            | 一時停止していたDDLジョブを再開します。          |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのすべての行とインデックスのCRC64を計算します。 |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの一貫性をチェックします。     |
| [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)      | 現在実行中または最近完了したDDLジョブの詳細を表示します。 |

</CustomContent>

<CustomContent platform="tidb">

| 声明                                                                                      | 説明                             |
| --------------------------------------------------------------------------------------- | ------------------------------ |
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)            | 現在実行中のDDLジョブをキャンセルします。         |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのすべての行とインデックスのCRC64を計算します。 |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの一貫性をチェックします。     |
| [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)      | 現在実行中または最近完了したDDLジョブの詳細を表示します。 |

</CustomContent>

## <code>ADMIN RELOAD</code>ステートメント {#code-admin-reload-code-statement}

```sql
ADMIN RELOAD expr_pushdown_blacklist;
```

上記のステートメントは、式によってプッシュされたブロックリストを再読み込みするために使用されます。

```sql
ADMIN RELOAD opt_rule_blacklist;
```

上記のステートメントは、ロジック最適化ルールのブロックリストを再読み込みするために使用されます。

## <code>ADMIN PLUGINS</code>関連の声明 {#code-admin-plugins-code-related-statement}

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

```sql
ADMIN PLUGINS ENABLE plugin_name [, plugin_name] ...;
```

上記の記述は`plugin_name`プラグインを有効にするために使用されます。

```sql
ADMIN PLUGINS DISABLE plugin_name [, plugin_name] ...;
```

上記のステートメントは`plugin_name`プラグインを無効にするために使用されます。

## <code>ADMIN BINDINGS</code>関連のステートメント {#code-admin-bindings-code-related-statement}

```sql
ADMIN FLUSH BINDINGS;
```

上記のステートメントは、SQLプランのバインディング情報を永続化するために使用されます。

```sql
ADMIN CAPTURE BINDINGS;
```

上記のステートメントは、複数回出現する`SELECT`ステートメントから SQL プランのバインディングを生成できます。

```sql
ADMIN EVOLVE BINDINGS;
```

自動バインディング機能が有効になると、SQL プランのバインディング情報の更新は`bind-info-leave`ごと（デフォルト値は`3s` ）にトリガーされます。上記のステートメントは、この更新を事前にトリガーするために使用されます。

```sql
ADMIN RELOAD BINDINGS;
```

上記のステートメントは、SQLプランのバインディング情報を再読み込みするために使用されます。

## <code>ADMIN REPAIR</code>声明 {#code-admin-repair-code-statement}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB の記述はTiDB Cloudには適用されません。

</CustomContent>

極端なケースで、保存されたテーブルのメタデータを信頼できない方法で上書きするには、 `ADMIN REPAIR TABLE`を使用します。

```sql
ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT;
```

<CustomContent platform="tidb">

ここで「信頼できない」とは、元のテーブルのメタデータが`CREATE TABLE STATEMENT`操作でカバーできることを手動で確認する必要があることを意味します。この`REPAIR`ステートメントを使用するには、 [`repair-mode`](/tidb-configuration-file.md#repair-mode)構成項目を有効にし、修復対象のテーブルが[`repair-table-list`](/tidb-configuration-file.md#repair-table-list)にリストされていることを確認してください。

</CustomContent>

## <code>ADMIN SHOW NEXT_ROW_ID</code>ステートメント {#code-admin-show-next-row-id-code-statement}

```sql
ADMIN SHOW t NEXT_ROW_ID;
```

上記のステートメントは、テーブルの特定の列の詳細を表示するために使用されます。出力は[SHOW TABLE NEXT_ROW_ID](/sql-statements/sql-statement-show-table-next-rowid.md)と同じです。

## <code>ADMIN SHOW SLOW</code>ステートメント {#code-admin-show-slow-code-statement}

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

```sql
ADMIN SHOW SLOW RECENT N;
```

```sql
ADMIN SHOW SLOW TOP [INTERNAL | ALL] N;
```

<CustomContent platform="tidb">

詳細については、 [`ADMIN SHOW SLOW`コマンド](/identify-slow-queries.md#admin-show-slow-command)を参照してください。

</CustomContent>

## あらすじ {#synopsis}

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 
        'SHOW' ( 
            'DDL' ( 
                'JOBS' Int64Num? WhereClauseOptional 
                | 'JOB' 'QUERIES' (NumList | AdminStmtLimitOpt)
            )? 
            | TableName 'NEXT_ROW_ID' 
            | 'SLOW' AdminShowSlow 
            | 'BDR' 'ROLE'
        ) 
        | 'CHECK' ( 
            'TABLE' TableNameList 
            | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? 
        ) 
        | 'RECOVER' 'INDEX' TableName Identifier 
        | 'CLEANUP' ( 
            'INDEX' TableName Identifier 
            | 'TABLE' 'LOCK' TableNameList ) 
        | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList 
        | ( 'CANCEL' | 'PAUSE' | 'RESUME' ) 'DDL' 'JOBS' NumList
        | 'RELOAD' (
            'EXPR_PUSHDOWN_BLACKLIST' 
            | 'OPT_RULE_BLACKLIST' 
            | 'BINDINGS'
            | 'STATS_EXTENDED'
            | 'STATISTICS'
        ) 
        | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList 
        | 'REPAIR' 'TABLE' TableName CreateTableStmt 
        | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS'
        | 'FLUSH' ('SESSION' | 'INSTANCE') 'PLAN_CACHE'
        | 'SET' 'BDR' 'ROLE' ( 'PRIMARY' | 'SECONDARY' )
        | 'UNSET' 'BDR' 'ROLE'
    )

NumList ::=
    Int64Num ( ',' Int64Num )*

AdminStmtLimitOpt ::=
    'LIMIT' LengthNum
|    'LIMIT' LengthNum ',' LengthNum
|    'LIMIT' LengthNum 'OFFSET' LengthNum

TableNameList ::=
    TableName ( ',' TableName )*
```

## 例 {#examples}

現在実行中の DDL ジョブ キューで完了した最新の 10 件の DDL ジョブを表示するには、次のコマンドを実行します。 `NUM`が指定されていない場合、デフォルトでは完了した最新の 10 件の DDL ジョブのみが表示されます。

```sql
ADMIN SHOW DDL JOBS;
```

    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
    | 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
    | 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
    | 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
    | 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
    | 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
    | 39     | test    | t1         | add column    | public               | 32        | 37       | 0         | 2019-01-10 12:32:55.42 +0800 CST  | 2019-01-10 12:32:56.24 +0800 CST  | synced        |
    | 38     | test    | t1         | create table  | public               | 32        | 37       | 0         | 2019-01-10 12:32:41.956 +0800 CST | 2019-01-10 12:32:43.956 +0800 CST | synced        |
    | 36     | test    |            | drop table    | none                 | 32        | 34       | 0         | 2019-01-10 11:29:59.982 +0800 CST | 2019-01-10 11:30:00.45 +0800  CST | synced        |
    | 35     | test    |            | create table  | public               | 32        | 34       | 0         | 2019-01-10 11:29:40.741 +0800 CST | 2019-01-10 11:29:41.682 +0800 CST | synced        |
    | 33     | test    |            | create schema | public               | 32        | 0        | 0         | 2019-01-10 11:29:22.813 +0800 CST | 2019-01-10 11:29:23.954 +0800 CST | synced        |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+

現在実行中のDDLジョブキューで完了した最新の5件のDDLジョブを表示するには、次のコマンドを実行します。

```sql
ADMIN SHOW DDL JOBS 5;
```

    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
    | 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
    | 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
    | 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
    | 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
    | 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+

テーブルの特定の列の詳細を表示するには、次のコマンドを実行します。出力は[SHOW TABLE NEXT_ROW_ID](/sql-statements/sql-statement-show-table-next-rowid.md)と同じです。

```sql
ADMIN SHOW t NEXT_ROW_ID;
```

```sql
+---------+------------+-------------+--------------------+----------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID | ID_TYPE        |
+---------+------------+-------------+--------------------+----------------+
| test    | t          | _tidb_rowid |                101 | _TIDB_ROWID    |
| test    | t          | _tidb_rowid |                  1 | AUTO_INCREMENT |
+---------+------------+-------------+--------------------+----------------+
2 rows in set (0.01 sec)
```

テストデータベース内の未完了のDDLジョブを表示するには、次のコマンドを実行します。結果には、実行中のDDLジョブと、完了したが失敗した直近5件のDDLジョブが含まれます。

```sql
ADMIN SHOW DDL JOBS 5 WHERE state != 'synced' AND db_name = 'test';
```

    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
    | 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+

-   `JOB_ID` : 各 DDL 操作は 1 つの DDL ジョブに対応します。 `JOB_ID`はグローバルに一意です。
-   `DB_NAME` : DDL操作が実行されるデータベースの名前。
-   `TABLE_NAME` : DDL操作が実行されるテーブルの名前。
-   `JOB_TYPE` : DDL操作のタイプ。
-   `SCHEMA_STATE` : スキーマの現在の状態。 `JOB_TYPE`が`add index`の場合、インデックスの状態です。 `JOB_TYPE`が`add column`の場合、列の状態です。 `JOB_TYPE`が`create table`の場合、テーブルの状態です。一般的な状態には以下が含まれます。
    -   `none` : 存在しないことを示します。 `drop`または`create`操作が失敗してロールバックされると、通常は`none`状態になります。
    -   `delete only` 、 `write only` 、 `delete reorganization` 、 `write reorganization` ：これら4つの状態は中間状態です。中間状態からの変換が非常に速いため、これらの状態は通常の操作では表示されません。 `write reorganization`状態は`add index`操作でのみ表示され、これはインデックスデータが追加されていることを意味します。
    -   `public` : 存在していて使用可能であることを示します。 `create table`や`add index/column`のような操作が完了すると、通常は`public`の状態になります。これは、作成されたテーブル/列/インデックスを正常に読み書きできるようになったことを意味します。
-   `SCHEMA_ID` : DDL操作が実行されるデータベースのID。
-   `TABLE_ID` : DDL操作が実行されるテーブルのID。
-   `ROW_COUNT` : `add index`操作を実行した際に追加されたデータ行の数。
-   `START_TIME` : DDL操作の開始時刻。
-   `END_TIME` : DDL 操作の終了時刻。
-   `STATE` : DDL操作の状態。一般的な状態には以下が含まれます。
    -   `none` : これは、操作タスクが DDL ジョブ キューに入れられたものの、前のタスクの完了を待っているため、まだ実行されていないことを示します。別の理由としては、ドロップ操作の実行後に`none`状態になるものの、すぐに`synced`状態に更新されることが考えられます。これは、すべての TiDB インスタンスがこの状態に同期されたことを意味します。
    -   `running` : これは、操作が実行されていることを示します。
    -   `synced` : これは、操作が正常に実行され、すべての TiDB インスタンスがこの状態に同期されたことを示します。
    -   `rollback done` : 操作が失敗し、ロールバックが完了したことを示します。
    -   `rollingback` : 操作が失敗し、ロールバックされていることを示します。
    -   `cancelling` : これは、操作がキャンセルされていることを示します。この状態は、 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルした場合にのみ発生します。
    -   `paused` : 操作が一時停止されていることを示します。この状態は[`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)コマンドを使用して DDL ジョブを一時停止した場合にのみ表示されます。ADMIN [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)コマンドを使用して DDL ジョブを再開できます。

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。
