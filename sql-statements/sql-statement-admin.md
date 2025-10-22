---
title: ADMIN | TiDB SQL Statement Reference
summary: TiDB データベースの ADMIN の使用法の概要。
---

# 管理者 {#admin}

このステートメントはTiDBの拡張構文であり、TiDBのステータスを表示し、TiDB内のテーブルのデータを確認するために使用されます。このドキュメントでは、以下の`ADMIN`関連ステートメントについて説明します。

-   [`ADMIN RELOAD`](#admin-reload-statement)
-   [`ADMIN PLUGINS`](#admin-plugins-related-statement)
-   [`ADMIN ... BINDINGS`](#admin-bindings-related-statement)
-   [`ADMIN REPAIR`](#admin-repair-statement)
-   [`ADMIN SHOW NEXT_ROW_ID`](#admin-show-next_row_id-statement)
-   [`ADMIN SHOW SLOW`](#admin-show-slow-statement)

## DDL関連ステートメント {#ddl-related-statement}

<CustomContent platform="tidb-cloud">

| 声明                                                                                      | 説明                               |
| --------------------------------------------------------------------------------------- | -------------------------------- |
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)            | 現在実行中の DDL ジョブをキャンセルします。         |
| [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)              | 現在実行中の DDL ジョブを一時停止します。          |
| [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)            | 一時停止された DDL ジョブを再開します。           |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのすべての行とインデックスの CRC64 を計算します。 |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの一貫性をチェックします。       |
| [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)      | 現在実行中または最近完了した DDL ジョブの詳細を表示します。 |

</CustomContent>

<CustomContent platform="tidb">

| 声明                                                                                      | 説明                               |
| --------------------------------------------------------------------------------------- | -------------------------------- |
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)            | 現在実行中の DDL ジョブをキャンセルします。         |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのすべての行とインデックスの CRC64 を計算します。 |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの一貫性をチェックします。       |
| [`ADMIN SHOW DDL [JOBS|QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)      | 現在実行中または最近完了した DDL ジョブの詳細を表示します。 |

</CustomContent>

## <code>ADMIN RELOAD</code>ステートメント {#code-admin-reload-code-statement}

```sql
ADMIN RELOAD expr_pushdown_blacklist;
```

上記のステートメントは、式によってプッシュダウンされたブロックリストをリロードするために使用されます。

```sql
ADMIN RELOAD opt_rule_blacklist;
```

上記のステートメントは、ロジック最適化ルールのブロックリストを再ロードするために使用されます。

## <code>ADMIN PLUGINS</code>関連の声明 {#code-admin-plugins-code-related-statement}

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

```sql
ADMIN PLUGINS ENABLE plugin_name [, plugin_name] ...;
```

上記のステートメントは、プラグイン`plugin_name`を有効にするために使用されます。

```sql
ADMIN PLUGINS DISABLE plugin_name [, plugin_name] ...;
```

上記のステートメントは、 `plugin_name`プラグインを無効にするために使用されます。

## <code>ADMIN BINDINGS</code>関連のステートメント {#code-admin-bindings-code-related-statement}

```sql
ADMIN FLUSH BINDINGS;
```

上記のステートメントは、SQL プランのバインディング情報を保持するために使用されます。

```sql
ADMIN CAPTURE BINDINGS;
```

上記のステートメントは、複数回発生する`SELECT`ステートメントから SQL プランのバインディングを生成できます。

```sql
ADMIN EVOLVE BINDINGS;
```

自動バインディング機能を有効にすると、SQLプランのバインディング情報の更新は`bind-info-leave`回ごとにトリガーされます（デフォルト値は`3s` ）。上記のステートメントは、この更新を事前にトリガーするために使用されます。

```sql
ADMIN RELOAD BINDINGS;
```

上記のステートメントは、SQL プランのバインディング情報を再ロードするために使用されます。

## <code>ADMIN REPAIR</code>ステートメント {#code-admin-repair-code-statement}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この TiDB ステートメントはTiDB Cloudには適用されません。

</CustomContent>

極端な場合、保存されたテーブルのメタデータを信頼できない方法で上書きするには、 `ADMIN REPAIR TABLE`使用します。

```sql
ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT;
```

<CustomContent platform="tidb">

ここで「信頼できない」とは、元のテーブルのメタデータが`CREATE TABLE STATEMENT`操作でカバーされるかどうかを手動で確認する必要があることを意味します。この`REPAIR`ステートメントを使用するには、 [`repair-mode`](/tidb-configuration-file.md#repair-mode)設定項目を有効にし、修復対象のテーブルが[`repair-table-list`](/tidb-configuration-file.md#repair-table-list)リストに含まれていることを確認してください。

</CustomContent>

## <code>ADMIN SHOW NEXT_ROW_ID</code>ステートメント {#code-admin-show-next-row-id-code-statement}

```sql
ADMIN SHOW t NEXT_ROW_ID;
```

上記の文は、テーブル内の特定の列の詳細を表示するために使用されます。出力は[テーブルNEXT_ROW_IDを表示](/sql-statements/sql-statement-show-table-next-rowid.md)と同じです。

## <code>ADMIN SHOW SLOW</code>ステートメント {#code-admin-show-slow-code-statement}

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

```sql
ADMIN SHOW SLOW RECENT N;
```

```sql
ADMIN SHOW SLOW TOP [INTERNAL | ALL] N;
```

<CustomContent platform="tidb">

詳細は[`ADMIN SHOW SLOW`コマンド](/identify-slow-queries.md#admin-show-slow-command)を参照。

</CustomContent>

## 概要 {#synopsis}

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

現在実行中のDDLジョブキュー内の最新の完了済みDDLジョブ10件を表示するには、以下のコマンドを実行します。1 `NUM`指定しない場合は、デフォルトで最新の完了済みDDLジョブ10件のみが表示されます。

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

現在実行中の DDL ジョブ キュー内の最後の 5 つの完了した DDL ジョブを表示するには、次のコマンドを実行します。

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

テーブルの特定の列の詳細を表示するには、次のコマンドを実行します。出力は[テーブルNEXT_ROW_IDを表示](/sql-statements/sql-statement-show-table-next-rowid.md)と同じです。

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

次のコマンドを実行すると、テストデータベース内の未完了のDDLジョブが表示されます。結果には、実行中のDDLジョブと、完了したが失敗した最後の5つのDDLジョブが含まれます。

```sql
ADMIN SHOW DDL JOBS 5 WHERE state != 'synced' AND db_name = 'test';
```

    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
    | 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
    | 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
    +--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+

-   `JOB_ID` : 各 DDL 操作は 1 つの DDL ジョブに対応します。2 `JOB_ID`グローバルに一意です。
-   `DB_NAME` : DDL 操作が実行されるデータベースの名前。
-   `TABLE_NAME` : DDL 操作が実行されるテーブルの名前。
-   `JOB_TYPE` : DDL 操作のタイプ。
-   `SCHEMA_STATE` : スキーマの現在の状態。2 が`JOB_TYPE` `add index`場合はインデックスの状態、 `JOB_TYPE`が`add column`場合は列の状態、 `JOB_TYPE`が`create table`の場合はテーブルの状態です。一般的な状態には以下が含まれます。
    -   `none` ：存在しないことを示します。2または`drop` `create`操作が失敗してロールバックされた場合、通常は`none`状態になります。
    -   `delete only` ：これら`write reorganization` 4つの状態は中間状態です。中間状態からの変換`write only`非常に速いため、これらの状態`delete reorganization`通常の操作では見えません。8 `write reorganization`の状態は`add index`操作でのみ確認できます。これは、インデックスデータが追加されていることを意味します。
    -   `public` ：存在し使用可能であることを示します。2や`add index/column`などの操作が完了すると、通常は`public`状態になり、作成されたテーブル/列/インデックスが正常に読み書き可能になったこと`create table`意味します。
-   `SCHEMA_ID` : DDL 操作が実行されるデータベースの ID。
-   `TABLE_ID` : DDL 操作が実行されるテーブルの ID。
-   `ROW_COUNT` : `add index`操作を実行するときに追加されたデータ行の数。
-   `START_TIME` : DDL 操作の開始時刻。
-   `END_TIME` : DDL 操作の終了時刻。
-   `STATE` : DDL操作の状態。一般的な状態には以下が含まれます。
    -   `none` : 操作タスクはDDLジョブキューに入れられましたが、前のタスクの完了を待機しているため、まだ実行されていません。別の理由としては、ドロップ操作の実行後に状態`none`になりますが、すぐに状態`synced`に更新され、すべてのTiDBインスタンスがこの状態に同期されたことが考えられます。
    -   `running` : 操作が実行中であることを示します。
    -   `synced` : 操作が正常に実行され、すべての TiDB インスタンスがこの状態に同期されていることを示します。
    -   `rollback done` : 操作が失敗し、ロールバックが完了したことを示します。
    -   `rollingback` : 操作が失敗し、ロールバック中であることを示します。
    -   `cancelling` : 操作がキャンセルされていることを示します。この状態は、 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルした場合にのみ発生します。
    -   `paused` : 操作が一時停止されていることを示します。この状態は、 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)コマンドを使用して DDL ジョブを一時停止した場合にのみ表示されます。4 コマンド[`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)使用して DDL ジョブを再開できます。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
