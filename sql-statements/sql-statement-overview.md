---
title: SQL Statement Overview
summary: TiDB でサポートされている SQL ステートメントについて学習します。
---

# SQL ステートメントの概要 {#sql-statement-overview}

TiDB は、必要に応じて MySQL および TiDB 固有のステートメントの拡張機能を使用して、ISO/IEC SQL 標準に準拠することを目的とした SQL ステートメントを使用します。

## スキーマ管理 / データ定義ステートメント (DDL) {#schema-management-data-definition-statements-ddl}

| SQL文                                                                               | 説明                                                    |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)                | データベースを変更します。                                         |
| [`ALTER SEQUENCE`](/sql-statements/sql-statement-alter-sequence.md)                | シーケンスを変更します。                                          |
| [`ALTER TABLE ... ADD COLUMN`](/sql-statements/sql-statement-add-column.md)        | 既存のテーブルに列を追加します。                                      |
| [`ALTER TABLE ... ADD INDEX`](/sql-statements/sql-statement-add-index.md)          | 既存のテーブルにインデックスを追加します。                                 |
| [`ALTER TABLE ... ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)      | インデックス定義を変更します。                                       |
| [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)  | 列の定義を変更します。                                           |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)  | テーブルを圧縮します。                                           |
| [`ALTER TABLE ... DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)      | テーブルから列を削除します。                                        |
| [`ALTER TABLE ... MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)  | 列定義を変更します。                                            |
| [`ALTER TABLE ... RENAME INDEX`](/sql-statements/sql-statement-rename-index.md)    | インデックスの名前を変更します。                                      |
| [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)                      | テーブル定義を変更します。                                         |
| [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)              | 新しいデータベースを作成します。                                      |
| [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md)                    | テーブルに新しいインデックスを作成します。                                 |
| [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)              | 新しいシーケンス オブジェクトを作成します。                                |
| [`CREATE TABLE LIKE`](/sql-statements/sql-statement-create-table-like.md)          | データをコピーせずに、既存のテーブルの定義をコピーします。                         |
| [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)                    | 新しいテーブルを作成します。                                        |
| [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md)                      | 新しいビューを作成します。                                         |
| [`DROP DATABASE`](/sql-statements/sql-statement-drop-database.md)                  | 既存のデータベースを削除します。                                      |
| [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)                        | テーブルからインデックスを削除します。                                   |
| [`DROP SEQUENCE`](/sql-statements/sql-statement-drop-sequence.md)                  | シーケンス オブジェクトを削除します。                                   |
| [`DROP TABLE`](/sql-statements/sql-statement-drop-table.md)                        | 既存のテーブルを削除します。                                        |
| [`DROP VIEW`](/sql-statements/sql-statement-drop-view.md)                          | 既存のビューを削除します。                                         |
| [`RENAME TABLE`](/sql-statements/sql-statement-rename-table.md)                    | テーブルの名前を変更します。                                        |
| [`SHOW COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)          | テーブルの列を表示します。                                         |
| [`SHOW CREATE DATABASE`](/sql-statements/sql-statement-show-create-database.md)    | データベースの CREATE ステートメントを表示します。                         |
| [`SHOW CREATE SEQUENCE`](/sql-statements/sql-statement-show-create-sequence.md)    | シーケンスの CREATE ステートメントを表示します。                          |
| [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)          | テーブルの CREATE ステートメントを表示します。                           |
| [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md)                | 現在のユーザーが権限を持つデータベースのリストを表示します。                        |
| [`SHOW FIELDS FROM`](/sql-statements/sql-statement-show-fields-from.md)            | テーブルの列を表示します。                                         |
| [`SHOW INDEXES`](/sql-statements/sql-statement-show-indexes.md)                    | テーブルのインデックスを表示します。                                    |
| [`SHOW SCHEMAS`](/sql-statements/sql-statement-show-schemas.md)                    | `SHOW DATABASES`のエイリアス。現在のユーザーが権限を持つデータベースのリストを表示します。 |
| [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md) | テーブルの次の行 ID を表示します。                                   |
| [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)        | TiDB 内のテーブルのリージョン情報を表示します。                            |
| [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md)          | TiDB 内のテーブルに関するさまざまな統計を表示します。                         |
| [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md)                      | データベース内のテーブルを表示します。                                   |
| [`TRUNCATE`](/sql-statements/sql-statement-truncate.md)                            | テーブルからすべてのデータを切り捨てます。                                 |

## データ操作ステートメント (DML) {#data-manipulation-statements-dml}

| SQL文                                                  | 説明                                        |
| ----------------------------------------------------- | ----------------------------------------- |
| [`BATCH`](/sql-statements/sql-statement-batch.md)     | DML ステートメントを TiDB 内の複数のステートメントに分割して実行します。 |
| [`DELETE`](/sql-statements/sql-statement-delete.md)   | テーブルから行を削除します。                            |
| [`INSERT`](/sql-statements/sql-statement-insert.md)   | テーブルに新しい行を挿入します。                          |
| [`REPLACE`](/sql-statements/sql-statement-replace.md) | 既存の行を置き換えるか、新しい行を挿入します。                   |
| [`SELECT`](/sql-statements/sql-statement-select.md)   | テーブルからデータを読み取ります。                         |
| [`TABLE`](/sql-statements/sql-statement-table.md)     | テーブルから行を取得します。                            |
| [`UPDATE`](/sql-statements/sql-statement-update.md)   | テーブル内の既存の行を更新します。                         |
| [`WITH`](/sql-statements/sql-statement-with.md)       | 共通テーブル式を定義します。                            |

## トランザクション明細 {#transaction-statements}

| SQL文                                                                      | 説明                                     |
| ------------------------------------------------------------------------- | -------------------------------------- |
| [`BEGIN`](/sql-statements/sql-statement-begin.md)                         | 新しいトランザクションを開始します。                     |
| [`COMMIT`](/sql-statements/sql-statement-commit.md)                       | 現在のトランザクションをコミットします。                   |
| [`ROLLBACK`](/sql-statements/sql-statement-rollback.md)                   | 現在のトランザクションをロールバックします。                 |
| [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)                 | トランザクション内にセーブポイントを設定します。               |
| [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md)     | 現在の分離レベルを`GLOBAL`または`SESSION`単位で変更します。 |
| [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) | 新しいトランザクションを開始します。                     |

## 準備されたステートメント {#prepared-statements}

| SQL文                                                        | 説明                                    |
| ----------------------------------------------------------- | ------------------------------------- |
| [`DEALLOCATE`](/sql-statements/sql-statement-deallocate.md) | プリペアドステートメントの割り当てを解除し、関連するリソースを解放します。 |
| [`EXECUTE`](/sql-statements/sql-statement-execute.md)       | 特定のパラメータ値を使用してプリペアドステートメントを実行します。     |
| [`PREPARE`](/sql-statements/sql-statement-prepare.md)       | プレースホルダーを使用してプリペアドステートメントを作成します。      |

## 行政上の声明 {#administrative-statements}

<CustomContent platform="tidb">

| SQL文                                                                                    | 説明                                                                 |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)                 | DDL ジョブをキャンセルします。                                                  |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの整合性をチェックします。                                         |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのチェックサムを計算します。                                                 |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)                 | テーブルからインデックスをクリーンアップします。                                           |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)                   | DDL 操作を一時停止します。                                                    |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)                 | DDL 操作を再開します。                                                      |
| [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)  | DDL ジョブまたはジョブ クエリを表示します。                                           |
| [`ADMIN`](/sql-statements/sql-statement-admin.md)                                       | さまざまな管理タスクを実行します。                                                  |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md)                         | [MySQL 互換性](/mysql-compatibility.md)に含まれています。TiDB では有効な使用方法はありません。 |
| [`SET &#x3C;variable>`](/sql-statements/sql-statement-set-variable.md)                  | システム変数またはユーザー変数を変更します。                                             |
| [`SET [NAMES|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md)               | 文字セットと照合順序を設定します。                                                  |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md)                         | リージョンを小さなリージョンに分割します。                                              |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL文                                                                                    | 説明                                                                 |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)                 | DDL ジョブをキャンセルします。                                                  |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの整合性をチェックします。                                         |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのチェックサムを計算します。                                                 |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)                 | テーブルからインデックスをクリーンアップします。                                           |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)                   | DDL 操作を一時停止します。                                                    |
| [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)                 | 冗長インデックスに基づいて一貫性を回復します。                                            |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)                 | DDL 操作を再開します。                                                      |
| [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)  | DDL ジョブまたはジョブ クエリを表示します。                                           |
| [`ADMIN`](/sql-statements/sql-statement-admin.md)                                       | さまざまな管理タスクを実行します。                                                  |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md)                         | [MySQL 互換性](/mysql-compatibility.md)に含まれています。TiDB では有効な使用方法はありません。 |
| [`SET &#x3C;variable>`](/sql-statements/sql-statement-set-variable.md)                  | システム変数またはユーザー変数を変更します。                                             |
| [`SET [NAMES|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md)               | 文字セットと照合順序を設定します。                                                  |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md)                         | リージョンを小さなリージョンに分割します。                                              |

</CustomContent>

## データのインポートとエクスポート {#data-import-and-export}

| SQL文                                                                      | 説明                                                                                                                         |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md) | 進行中のインポート ジョブをキャンセルします。                                                                                                    |
| [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)             | TiDB Lightningの[物理インポートモード](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)介してデータをテーブルにインポートします。 |
| [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)                 | Amazon S3 または Google Cloud Storage からテーブルにデータをロードします。                                                                      |
| [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md)     | インポート ジョブのステータスを表示します。                                                                                                     |

## バックアップと復元 {#backup-x26-restore}

| SQL文                                                                        | 説明                                            |
| --------------------------------------------------------------------------- | --------------------------------------------- |
| [`BACKUP`](/sql-statements/sql-statement-backup.md)                         | TiDB クラスターの分散バックアップを実行します。                    |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)   | クラスターを特定のスナップショットに復元します。                      |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | `DROP`ステートメントによって削除されたデータベースとそのデータを復元します。     |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)       | `DROP`または`TRUNCATE`操作によって削除されたテーブルとデータを復元します。 |
| [`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md)           | 削除されたテーブルとその上のデータを回復します。                      |
| [`RESTORE`](/sql-statements/sql-statement-restore.md)                       | バックアップからデータベースを復元します。                         |
| [`SHOW BACKUPS`](/sql-statements/sql-statement-show-backups.md)             | バックアップ タスクを表示します。                             |
| [`SHOW RESTORES`](/sql-statements/sql-statement-show-backups.md)            | 復元タスクを表示します。                                  |

## 配置ポリシー {#placement-policy}

| SQL文                                                                                            | 説明                            |
| ----------------------------------------------------------------------------------------------- | ----------------------------- |
| [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)             | 配置ポリシーを変更します。                 |
| [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md)                                   | 配置ポリシーの範囲を変更します。              |
| [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md)           | 新しい配置ポリシーを作成します。              |
| [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md)               | 既存の配置ポリシーを削除します。              |
| [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) | 配置ポリシーの`CREATE`ステートメントを表示します。 |
| [`SHOW PLACEMENT FOR`](/sql-statements/sql-statement-show-placement-for.md)                     | 特定のテーブルの配置ルールを表示します。          |
| [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)               | 使用可能な配置ラベルを表示します。             |
| [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md)                             | 配置ルールを表示します。                  |

## リソース グループ {#resource-groups}

<CustomContent platform="tidb">

| SQL文                                                                                        | 説明                                                                                        |
| ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)             | リソース グループを変更します。                                                                          |
| [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md)                 | 現在のクラスターの[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru)容量を推定して出力します。 |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)           | 新しいリソース グループを作成します。                                                                       |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)               | リソース グループを削除します。                                                                          |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)                               | ランナウェイ クエリ監視リストを管理します。                                                                    |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)                 | リソース グループを設定します。                                                                          |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | リソース グループの`CREATE`ステートメントを表示します。                                                          |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL文                                                                                        | 説明                               |
| ------------------------------------------------------------------------------------------- | -------------------------------- |
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)             | リソース グループを変更します。                 |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)           | 新しいリソース グループを作成します。              |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)               | リソース グループを削除します。                 |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)                               | ランナウェイ クエリ監視リストを管理します。           |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)                 | リソース グループを設定します。                 |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | リソース グループの`CREATE`ステートメントを表示します。 |

</CustomContent>

## ユーティリティステートメント {#utility-statements}

| SQL文                                                    | 説明                          |
| ------------------------------------------------------- | --------------------------- |
| [`DESC`](/sql-statements/sql-statement-desc.md)         | テーブルの構造を示す`DESCRIBE`のエイリアス。 |
| [`DESCRIBE`](/sql-statements/sql-statement-describe.md) | テーブルの構造を表示します。              |
| [`DO`](/sql-statements/sql-statement-do.md)             | 式を実行しますが、結果は返しません。          |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)   | クエリの実行プランを表示します。            |
| [`TRACE`](/sql-statements/sql-statement-trace.md)       | クエリ実行に関する詳細情報を提供します。        |
| [`USE`](/sql-statements/sql-statement-use.md)           | 現在のデータベースを設定します。            |

## ステートメントを表示 {#show-statements}

<CustomContent platform="tidb">

| SQL文                                                                        | 説明                                                                                                                                                 |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md)           | 組み込み関数を一覧表示します。                                                                                                                                    |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | 文字セットを一覧表示します。                                                                                                                                     |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md)        | 照合を一覧表示します。                                                                                                                                        |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md)               | 以前に実行されたステートメントのエラーを表示します。                                                                                                                         |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md)               | [MySQLとの互換性](/mysql-compatibility.md)に含まれています。TiDB は、ほとんどのメトリックに対して`SHOW STATUS`ではなく、集中メトリック収集に[プロメテウスとグラファナ](/tidb-monitoring-framework.md)使用します。 |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md)         | システム変数を表示します。                                                                                                                                      |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)           | 以前に実行されたステートメントからの警告とメモを表示します。                                                                                                                     |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL文                                                                        | 説明                                                                                                                                                           |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md)           | 組み込み関数を一覧表示します。                                                                                                                                              |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | 文字セットを一覧表示します。                                                                                                                                               |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md)        | 照合を一覧表示します。                                                                                                                                                  |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md)               | 以前に実行されたステートメントのエラーを表示します。                                                                                                                                   |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md)               | [MySQLとの互換性](/mysql-compatibility.md)に含まれています。TiDB TiDB Cloud は、ほとんどのメトリックに対して`SHOW STATUS`ではなく、集中メトリック収集に対して[監視](/tidb-cloud/monitor-tidb-cluster.md)提供します。 |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md)         | システム変数を表示します。                                                                                                                                                |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)           | 以前に実行されたステートメントからの警告とメモを表示します。                                                                                                                               |

</CustomContent>

## インスタンス管理 {#instance-management}

<CustomContent platform="tidb">

| SQL文                                                                    | 説明                                                                                                                                                 |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md)     | インスタンスを変更します。                                                                                                                                      |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md)         | [MySQLとの互換性](/mysql-compatibility.md)に含まれています。TiDB は、ほとんどのメトリックに対して`SHOW STATUS`ではなく、集中メトリック収集に[プロメテウスとグラファナ](/tidb-monitoring-framework.md)使用します。 |
| [`KILL`](/sql-statements/sql-statement-kill.md)                         | 現在の TiDB クラスター内の任意の TiDB インスタンスの接続を切断します。                                                                                                          |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)           | TiDB のさまざまなコンポーネントの構成を表示します。                                                                                                                       |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md)         | 使用可能なstorageエンジンを表示します。                                                                                                                            |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md)         | インストールされているプラグインを表示します。                                                                                                                            |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | 同じ TiDBサーバーに接続されている現在のセッションを表示します。                                                                                                                 |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md)       | [MySQLとの互換性](/mysql-compatibility.md)に含まれています。現在は空の結果のみが返されます。                                                                                     |
| [`SHUTDOWN`](/sql-statements/sql-statement-shutdown.md)                 | TiDB クラスター全体ではなく、クライアントに接続された TiDB インスタンスを停止します。                                                                                                   |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL文                                                                    | 説明                                                                                                                                                           |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md)     | インスタンスを変更します。                                                                                                                                                |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md)         | [MySQLとの互換性](/mysql-compatibility.md)に含まれています。TiDB TiDB Cloud は、ほとんどのメトリックに対して`SHOW STATUS`ではなく、集中メトリック収集に対して[監視](/tidb-cloud/monitor-tidb-cluster.md)提供します。 |
| [`KILL`](/sql-statements/sql-statement-kill.md)                         | 現在の TiDB クラスター内の任意の TiDB インスタンスの接続を切断します。                                                                                                                    |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md)         | 使用可能なstorageエンジンを表示します。                                                                                                                                      |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md)         | インストールされているプラグインを表示します。                                                                                                                                      |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | 同じ TiDBサーバーに接続されている現在のセッションを表示します。                                                                                                                           |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md)       | クエリ プロファイルを表示します。 [MySQLとの互換性](/mysql-compatibility.md)に含まれます。現在は空の結果のみが返されます。                                                                               |

</CustomContent>

## ロックステートメント {#locking-statements}

| SQL文                                                                              | 説明                          |
| --------------------------------------------------------------------------------- | --------------------------- |
| [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)                       | テーブルまたはパーティションの統計をロックします。   |
| [`LOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)   | 現在のセッションのテーブルをロックします。       |
| [`UNLOCK STATS`](/sql-statements/sql-statement-unlock-stats.md)                   | テーブルまたはパーティションの統計をロック解除します。 |
| [`UNLOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) | テーブルのロックを解除します。             |

## アカウント管理 / データ制御言語 {#account-management-data-control-language}

| SQL文                                                                             | 説明                          |
| -------------------------------------------------------------------------------- | --------------------------- |
| [`ALTER USER`](/sql-statements/sql-statement-alter-user.md)                      | ユーザーを変更します。                 |
| [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)                    | ロールを作成します。                  |
| [`CREATE USER`](/sql-statements/sql-statement-create-user.md)                    | 新しいユーザーを作成します。              |
| [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)                        | 既存のロールを削除します。               |
| [`DROP USER`](/sql-statements/sql-statement-drop-user.md)                        | 既存のユーザーを削除します。              |
| [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)          | 権限テーブルから権限のメモリ内コピーを再ロードします。 |
| [`GRANT &#x3C;privileges>`](/sql-statements/sql-statement-grant-privileges.md)   | 権限を付与します。                   |
| [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)               | ロールを付与します。                  |
| [`RENAME USER`](/sql-statements/sql-statement-rename-user.md)                    | 既存のユーザーの名前を変更します。           |
| [`REVOKE &#x3C;privileges>`](/sql-statements/sql-statement-revoke-privileges.md) | 権限を取り消します。                  |
| [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)             | ロールを取り消します。                 |
| [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)          | デフォルトのロールを設定します。            |
| [`SET PASSWORD`](/sql-statements/sql-statement-set-password.md)                  | パスワードを変更します。                |
| [`SET ROLE`](/sql-statements/sql-statement-set-role.md)                          | 現在のセッションでロールを有効にします。        |
| [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md)          | ユーザーの`CREATE`ステートメントを表示します。 |
| [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md)                    | ユーザーに関連付けられた権限を表示します。       |
| [`SHOW PRIVILEGES`](/sql-statements/sql-statement-show-privileges.md)            | 利用可能な権限を表示します。              |

## TiCDC および TiDBBinlog {#ticdc-x26-tidb-binlog}

<CustomContent platform="tidb">

| SQL文                                                                                 | 説明                                 |
| ------------------------------------------------------------------------------------ | ---------------------------------- |
| [`ADMIN [SET|SHOW|UNSET] BDR ROLE`](/sql-statements/sql-statement-admin-bdr-role.md) | BDR ロールを管理します。                     |
| [`CHANGE DRAINER`](/sql-statements/sql-statement-change-drainer.md)                  | クラスター内のDrainerのステータス情報を変更します。      |
| [`CHANGE PUMP`](/sql-statements/sql-statement-change-pump.md)                        | クラスター内のPumpのステータス情報を変更します。         |
| [`SHOW DRAINER STATUS`](/sql-statements/sql-statement-show-drainer-status.md)        | クラスター内のすべてのDrainerノードのステータスを表示します。 |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md)          | クラスター内の最新の TSO を表示します。             |
| [`SHOW PUMP STATUS`](/sql-statements/sql-statement-show-pump-status.md)              | クラスター内のすべてのPumpノードのステータス情報を表示します。  |

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> [ティCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)と[TiDBBinlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview) 、TiDB Self-Managed のアップストリームに TiDB データを複製するためのツールです。TiCDC と TiDB Binlogのほとんどの SQL ステートメントは、TiDB Cloudには適用できません。TiDB TiDB Cloudでは、代わりに[TiDB Cloudコンソール](https://tidbcloud.com)の[チェンジフィード](/tidb-cloud/changefeed-overview.md)機能を使用してデータをストリーミングできます。

| SQL文                                                                        | 説明                     |
| --------------------------------------------------------------------------- | ---------------------- |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md) | クラスター内の最新の TSO を表示します。 |

</CustomContent>

## 統計と計画管理 {#statistics-and-plan-management}

| SQL文                                                                              | 説明                                             |
| --------------------------------------------------------------------------------- | ---------------------------------------------- |
| [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)                 | テーブルに関する統計を収集します。                              |
| [`CREATE BINDING`](/sql-statements/sql-statement-create-binding.md)               | SQL ステートメントの実行プラン バインディングを作成します。               |
| [`DROP BINDING`](/sql-statements/sql-statement-drop-binding.md)                   | SQL ステートメントから実行プラン バインディングを削除します。              |
| [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md)                       | テーブルから統計を削除します。                                |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)             | `EXPLAIN`と同様に動作しますが、ステートメントを実行するという大きな違いがあります。 |
| [`LOAD STATS`](/sql-statements/sql-statement-load-stats.md)                       | 統計を TiDB に読み込みます。                              |
| [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md)     | 統計収集タスクを表示します。                                 |
| [`SHOW BINDINGS`](/sql-statements/sql-statement-show-bindings.md)                 | 作成された SQL バインディングを表示します。                       |
| [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)       | 統計がどの程度正確であると考えられるかの推定値を示します。                  |
| [`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md) | 統計のヒストグラム情報を表示します。                             |
| [`SHOW STATS_LOCKED`](/sql-statements/sql-statement-show-stats-locked.md)         | 統計がロックされているテーブルを表示します。                         |
| [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)             | テーブル内の行数と、そのテーブル内で変更された行数を表示します。               |
