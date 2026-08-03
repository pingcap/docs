---
title: SQL Statement Overview
summary: TiDBでサポートされているSQL文について学びましょう。
---

# SQL Statement Overview {#sql-statement-overview}

TiDBは、ISO/IEC SQL標準に準拠することを目的としたSQL文を使用しており、必要に応じてMySQL用の拡張機能やTiDB固有の文が追加されています。

## スキーマ管理／データ定義文（DDL） {#schema-management--data-definition-statements-ddl}

| SQLステートメント                                                                         | 説明                                                   |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)                | データベースを変更します。                                        |
| [`ALTER SEQUENCE`](/sql-statements/sql-statement-alter-sequence.md)                | シーケンスを変更します。                                         |
| [`ALTER TABLE ... ADD COLUMN`](/sql-statements/sql-statement-add-column.md)        | 既存のテーブルに列を追加します。                                     |
| [`ALTER TABLE ... ADD INDEX`](/sql-statements/sql-statement-add-index.md)          | 既存のテーブルにインデックスを追加します。                                |
| [`ALTER TABLE ... ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)      | インデックス定義を変更します。                                      |
| [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)  | 列の定義を変更します。                                          |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)  | テーブルをコンパクトにします。                                      |
| [`ALTER TABLE ... DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)      | テーブルから列を削除します。                                       |
| [`ALTER TABLE ... MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)  | 列定義を変更します。                                           |
| [`ALTER TABLE ... RENAME INDEX`](/sql-statements/sql-statement-rename-index.md)    | インデックスの名前を変更します。                                     |
| [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)                      | テーブル定義を変更します。                                        |
| [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)              | 新しいデータベースを作成します。                                     |
| [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md)                    | テーブルに新しいインデックスを作成します。                                |
| [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)              | 新しいシーケンスオブジェクトを作成します。                                |
| [`CREATE TABLE LIKE`](/sql-statements/sql-statement-create-table-like.md)          | 既存のテーブルの定義をコピーしますが、データは一切コピーしません。                    |
| [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)                    | 新しいテーブルを作成します。                                       |
| [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md)                      | 新しいビューを作成します。                                        |
| [`DROP DATABASE`](/sql-statements/sql-statement-drop-database.md)                  | 既存のデータベースを削除します。                                     |
| [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)                        | テーブルからインデックスを削除します。                                  |
| [`DROP SEQUENCE`](/sql-statements/sql-statement-drop-sequence.md)                  | シーケンスオブジェクトを破棄します。                                   |
| [`DROP TABLE`](/sql-statements/sql-statement-drop-table.md)                        | 既存のテーブルを削除します。                                       |
| [`DROP VIEW`](/sql-statements/sql-statement-drop-view.md)                          | 既存のビューを削除します。                                        |
| [`RENAME TABLE`](/sql-statements/sql-statement-rename-table.md)                    | テーブルの名前を変更します。                                       |
| [`SHOW COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)          | テーブルの列を表示します。                                        |
| [`SHOW CREATE DATABASE`](/sql-statements/sql-statement-show-create-database.md)    | データベースの作成ステートメントを表示します。                              |
| [`SHOW CREATE SEQUENCE`](/sql-statements/sql-statement-show-create-sequence.md)    | シーケンスのCREATE文を表示します。                                 |
| [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)          | テーブルの作成ステートメントを表示します。                                |
| [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md)                | 現在のユーザーが権限を持つデータベースの一覧を表示します。                        |
| [`SHOW FIELDS FROM`](/sql-statements/sql-statement-show-fields-from.md)            | テーブルの列を表示します。                                        |
| [`SHOW INDEXES`](/sql-statements/sql-statement-show-indexes.md)                    | テーブルのインデックスを表示します。                                   |
| [`SHOW SCHEMAS`](/sql-statements/sql-statement-show-schemas.md)                    | `SHOW DATABASES`のエイリアス。現在のユーザーが権限を持つデータベースの一覧を表示します。 |
| [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md) | テーブルの次の行IDを表示します。                                    |
| [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)        | TiDB内のテーブルのリージョン情報を表示します。                            |
| [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md)          | TiDB内のテーブルに関する様々な統計情報を表示します。                         |
| [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md)                      | データベース内のテーブルを表示します。                                  |
| [`TRUNCATE`](/sql-statements/sql-statement-truncate.md)                            | テーブル内のすべてのデータを切り捨てます。                                |

## データ操作文（DML） {#data-manipulation-statements-dml}

| SQLステートメント                                            | 説明                                     |
| ----------------------------------------------------- | -------------------------------------- |
| [`BATCH`](/sql-statements/sql-statement-batch.md)     | TiDB内でDMLステートメントを複数のステートメントに分割して実行します。 |
| [`DELETE`](/sql-statements/sql-statement-delete.md)   | テーブルから行を削除します。                         |
| [`INSERT`](/sql-statements/sql-statement-insert.md)   | テーブルに新しい行を挿入します。                       |
| [`REPLACE`](/sql-statements/sql-statement-replace.md) | 既存の行を置き換えるか、新しい行を挿入します。                |
| [`SELECT`](/sql-statements/sql-statement-select.md)   | テーブルからデータを読み取ります。                      |
| [`TABLE`](/sql-statements/sql-statement-table.md)     | テーブルから行を取得します。                         |
| [`UPDATE`](/sql-statements/sql-statement-update.md)   | テーブル内の既存の行を更新します。                      |
| [`WITH`](/sql-statements/sql-statement-with.md)       | 共通テーブル式を定義します。                         |

## トランザクション書 {#transaction-statements}

| SQLステートメント                                                                | 説明                                        |
| ------------------------------------------------------------------------- | ----------------------------------------- |
| [`BEGIN`](/sql-statements/sql-statement-begin.md)                         | 新しいトランザクションを開始します。                              |
| [`COMMIT`](/sql-statements/sql-statement-commit.md)                       | 現在のトランザクションをコミットします。                      |
| [`ROLLBACK`](/sql-statements/sql-statement-rollback.md)                   | 現在のトランザクションをロールバックします。                    |
| [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)                 | トランザクション内にセーブポイントを設定します。                  |
| [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md)     | `GLOBAL`または`SESSION`に基づいて、現在の隔離レベルを変更します。 |
| [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) | 新しいトランザクションを開始します。                              |

## プリペアドステートメント {#prepared-statements}

| SQLステートメント                                                  | 説明                                 |
| ----------------------------------------------------------- | ---------------------------------- |
| [`DEALLOCATE`](/sql-statements/sql-statement-deallocate.md) | プリペアドステートメントを解除し、関連するリソースを解放します。   |
| [`EXECUTE`](/sql-statements/sql-statement-execute.md)       | 特定のパラメータ値を指定して、プリペアドステートメントを実行します。 |
| [`PREPARE`](/sql-statements/sql-statement-prepare.md)       | プレースホルダーを含むプリペアドステートメントを作成します。     |

## 管理ステートメント {#administrative-statements}

<CustomContent platform="tidb">

| SQLステートメント                                                                              | 説明                                                                      |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)              | 実行中の単一のDDLジョブのパラメータを変更します。                                              |
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)                 | DDLジョブをキャンセルします。                                                        |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの整合性をチェックします。                                              |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのチェックサムを計算します。                                                      |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)                 | テーブルからインデックスを削除します。                                                     |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)                   | DDL操作を一時停止します。                                                          |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)                 | DDL操作を再開します。                                                            |
| [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)  | DDLジョブまたはジョブクエリを表示します。                                                  |
| [`ADMIN`](/sql-statements/sql-statement-admin.md)                                       | 様々な事務作業を行う。                                                             |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md)                         | [MySQLとの互換性](/mysql-compatibility.md)のために含まれています。 TiDB では効果的な使用法がありません。 |
| [`SET &#x3C;variable>`](/sql-statements/sql-statement-set-variable.md)                  | システム変数またはユーザー変数を変更します。                                                  |
| [`SET [NAMES|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md)               | 文字セットと照合順序を設定します。                                                       |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md)                         | リージョンをより小さな領域に分割します。                                                    |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQLステートメント                                                                              | 説明                                                                      |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)              | 実行中の単一のDDLジョブのパラメータを変更します。                                              |
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)                 | DDLジョブをキャンセルします。                                                        |
| [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | テーブルまたはインデックスの整合性をチェックします。                                              |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)         | テーブルのチェックサムを計算します。                                                      |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md)                 | テーブルからインデックスを削除します。                                                     |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md)                   | DDL操作を一時停止します。                                                          |
| [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md)                 | 冗長なインデックスに基づいて一貫性を回復します。                                                |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md)                 | DDL操作を再開します。                                                            |
| [`ADMIN SHOW DDL [JOBS|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md)  | DDLジョブまたはジョブクエリを表示します。                                                  |
| [`ADMIN`](/sql-statements/sql-statement-admin.md)                                       | 様々な事務作業を行う。                                                             |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md)                         | [MySQLとの互換性](/mysql-compatibility.md)のために含まれています。 TiDB では効果的な使用法がありません。 |
| [`SET &#x3C;variable>`](/sql-statements/sql-statement-set-variable.md)                  | システム変数またはユーザー変数を変更します。                                                  |
| [`SET [NAMES|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md)               | 文字セットと照合順序を設定します。                                                       |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md)                         | リージョンをより小さな領域に分割します。                                                    |

</CustomContent>

## データのインポートとエクスポート {#data-import-and-export}

| SQLステートメント                                                                | 説明                                                                                                                       |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md) | 進行中のインポートジョブをキャンセルします。                                                                                                   |
| [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)             | TiDB Lightningの[物理インポートモード](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)を介してデータをテーブルにインポートします。 |
| [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)                 | Amazon S3またはGoogle Cloud Storageからデータをテーブルに読み込みます。                                                                       |
| [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md)     | インポートジョブのステータスを表示します。                                                                                                    |

## バックアップと復元 {#backup--restore}

| SQLステートメント                                                                  | 説明                                            |
| --------------------------------------------------------------------------- | --------------------------------------------- |
| [`BACKUP`](/sql-statements/sql-statement-backup.md)                         | TiDBクラスタの分散バックアップを実行します。                      |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)   | クラスターを特定の時点のスナップショットに復元します。                   |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | `DROP`ステートメントによって削除されたデータベースとそのデータを復元します。     |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)       | `DROP`または`TRUNCATE`操作によって削除されたテーブルとデータを復元します。 |
| [`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md)           | 削除されたテーブルとその中のデータを復元します。                      |
| [`RESTORE`](/sql-statements/sql-statement-restore.md)                       | バックアップからデータベースを復元します。                         |
| [`SHOW BACKUPS`](/sql-statements/sql-statement-show-backups.md)             | バックアップタスクを表示します。                              |
| [`SHOW RESTORES`](/sql-statements/sql-statement-show-backups.md)            | 復元タスクを表示します。                                  |

## 配置方針 {#placement-policy}

| SQLステートメント                                                                                      | 説明                            |
| ----------------------------------------------------------------------------------------------- | ----------------------------- |
| [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)             | 配置方針を変更します。                   |
| [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md)                                   | 配置ポリシーの範囲を変更します。              |
| [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md)           | 新しい配置ポリシーを作成します。              |
| [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md)               | 既存の配置ポリシーを廃止します。              |
| [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) | 配置ポリシーの`CREATE`ステートメントを表示します。 |
| [`SHOW PLACEMENT FOR`](/sql-statements/sql-statement-show-placement-for.md)                     | 特定のテーブルの配置ルールを表示します。          |
| [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md)               | 使用可能な配置ラベルを表示します。             |
| [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md)                             | 配置ルールを表示します。                  |

## リソースグループ {#resource-groups}

<CustomContent platform="tidb">

| SQLステートメント                                                                                  | 説明                                                                                                 |
| ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)             | リソースグループを変更します。                                                                                    |
| [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md)                 | 現在のクラスターの[リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)容量を推定して出力します。 |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)           | 新しいリソースグループを作成します。                                                                                 |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)               | リソースグループを削除します。                                                                                    |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)                               | 暴走クエリの監視リストを管理します。                                                                                 |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)                 | リソースグループを設定します。                                                                                    |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | リソース グループの`CREATE`ステートメントを表示します。                                                                   |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQLステートメント                                                                                  | 説明                               |
| ------------------------------------------------------------------------------------------- | -------------------------------- |
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)             | リソースグループを変更します。                  |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)           | 新しいリソースグループを作成します。               |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)               | リソースグループを削除します。                  |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)                               | 暴走クエリの監視リストを管理します。               |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)                 | リソースグループを設定します。                  |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | リソース グループの`CREATE`ステートメントを表示します。 |

</CustomContent>

## ユーティリティステートメント {#utility-statements}

| SQLステートメント                                              | 説明                          |
| ------------------------------------------------------- | --------------------------- |
| [`DESC`](/sql-statements/sql-statement-desc.md)         | テーブルの構造を示す`DESCRIBE`のエイリアス。 |
| [`DESCRIBE`](/sql-statements/sql-statement-describe.md) | テーブルの構造を示します。               |
| [`DO`](/sql-statements/sql-statement-do.md)             | 式を実行しますが、結果は返しません。          |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)   | クエリの実行プランを表示します。            |
| [`TRACE`](/sql-statements/sql-statement-trace.md)       | クエリ実行に関する詳細情報を提供します。        |
| [`USE`](/sql-statements/sql-statement-use.md)           | 現在のデータベースを設定します。            |

## SHOW ステートメント {#show-statements}

<CustomContent platform="tidb">

| SQLステートメント                                                                  | 説明                                                                                                                                                                      |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md)           | 組み込み関数の一覧を表示します。                                                                                                                                                        |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | 文字セットの一覧を表示します。                                                                                                                                                         |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md)        | 照合順序を一覧表示します。                                                                                                                                                           |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md)               | 以前に実行されたステートメントのエラーを表示します。                                                                                                                                              |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md)               | [MySQLとの互換性](/mysql-compatibility.md)のために含まれています。 TiDB は、ほとんどのメトリックに対して`SHOW STATUS`の代わりにPrometheus[PrometheusとGrafana](/tidb-monitoring-framework.md)Grafanaを使用して一元的なメトリック収集を行います。 |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md)         | システム変数を表示します。                                                                                                                                                           |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)           | 以前に実行されたステートメントに関する警告と注記を表示します。                                                                                                                                         |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQLステートメント                                                                  | 説明                                                                                                                                                               |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md)           | 組み込み関数の一覧を表示します。                                                                                                                                                 |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | 文字セットの一覧を表示します。                                                                                                                                                  |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md)        | 照合順序を一覧表示します。                                                                                                                                                    |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md)               | 以前に実行されたステートメントのエラーを表示します。                                                                                                                                       |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md)               | [MySQLとの互換性](/mysql-compatibility.md)のために含まれています。 TiDB Cloudは、ほとんどのメトリクスに対して`SHOW STATUS`の代わりに、一元化されたメトリクス収集のための[監視](/tidb-cloud/monitor-tidb-cluster.md)を提供します。 |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md)         | システム変数を表示します。                                                                                                                                                    |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)           | 以前に実行されたステートメントに関する警告と注記を表示します。                                                                                                                                  |

</CustomContent>

## インスタンス管理 {#instance-management}

<CustomContent platform="tidb">

| SQLステートメント                                                              | 説明                                                                                                                                                                      |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md)     | インスタンスを変更します。                                                                                                                                                           |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md)         | [MySQLとの互換性](/mysql-compatibility.md)のために含まれています。 TiDB は、ほとんどのメトリックに対して`SHOW STATUS`の代わりにPrometheus[PrometheusとGrafana](/tidb-monitoring-framework.md)Grafanaを使用して一元的なメトリック収集を行います。 |
| [`KILL`](/sql-statements/sql-statement-kill.md)                         | 現在の TiDB クラスタ内の任意の TiDB インスタンスの接続を切断します。                                                                                                                                |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)           | TiDBの各種コンポーネントの設定を表示します。                                                                                                                                                |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md)         | 利用可能なストレージエンジンを表示します。                                                                                                                                                 |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md)         | インストールされているプラ​​グインを表示します。                                                                                                                                               |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | 同じ TiDBサーバーに接続されている現在のセッションを表示します。                                                                                                                                      |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md)       | [MySQLとの互換性](/mysql-compatibility.md)のために含まれています。現時点では、空の結果のみが返されます。                                                                                                    |
| [`SHUTDOWN`](/sql-statements/sql-statement-shutdown.md)                 | クライアントに接続されているTiDBインスタンスを停止します。TiDBクラスタ全体を停止するわけではありません。                                                                                                                |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQLステートメント                                                              | 説明                                                                                                                                                               |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md)     | インスタンスを変更します。                                                                                                                                                    |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md)         | [MySQLとの互換性](/mysql-compatibility.md)のために含まれています。 TiDB Cloudは、ほとんどのメトリクスに対して`SHOW STATUS`の代わりに、一元化されたメトリクス収集のための[監視](/tidb-cloud/monitor-tidb-cluster.md)を提供します。 |
| [`KILL`](/sql-statements/sql-statement-kill.md)                         | 現在の TiDB クラスタ内の任意の TiDB インスタンスの接続を切断します。                                                                                                                         |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md)         | 利用可能なストレージエンジンを表示します。                                                                                                                                          |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md)         | インストールされているプラ​​グインを表示します。                                                                                                                                        |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | 同じ TiDBサーバーに接続されている現在のセッションを表示します。                                                                                                                               |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md)       | クエリプロファイルを表示します。 [MySQLとの互換性](/mysql-compatibility.md)のために含まれています。現在は空の結果のみを返します。                                                                                |

</CustomContent>

## ロックステートメント {#locking-statements}

| SQLステートメント                                                                        | 説明                                 |
| --------------------------------------------------------------------------------- | ---------------------------------- |
| [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)                       | テーブルまたはパーティションの統計情報をロックします。        |
| [`LOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)   | 現在のセッションのテーブルをロックします。              |
| [`UNLOCK STATS`](/sql-statements/sql-statement-unlock-stats.md)                   | テーブルまたはパーティションの統計情報へのアクセス権限を解放します。 |
| [`UNLOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) | テーブルのロックを解除します。                    |

## アカウント管理／データ制御言語 {#account-management--data-control-language}

| SQLステートメント                                                                       | 説明                             |
| -------------------------------------------------------------------------------- | ------------------------------ |
| [`ALTER USER`](/sql-statements/sql-statement-alter-user.md)                      | ユーザーを変更します。                    |
| [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)                    | 役割を作成します。                      |
| [`CREATE USER`](/sql-statements/sql-statement-create-user.md)                    | 新しいユーザーを作成します。                 |
| [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)                        | 既存の役割を削除します。                   |
| [`DROP USER`](/sql-statements/sql-statement-drop-user.md)                        | 既存のユーザーを削除します。                 |
| [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)          | 権限テーブルから、メモリ上の権限コピーを再読み込みします。  |
| [`GRANT &#x3C;privileges>`](/sql-statements/sql-statement-grant-privileges.md)   | 権限を付与します。                      |
| [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)               | 役割を付与します。                      |
| [`RENAME USER`](/sql-statements/sql-statement-rename-user.md)                    | 既存のユーザー名を変更します。                |
| [`REVOKE &#x3C;privileges>`](/sql-statements/sql-statement-revoke-privileges.md) | 権限を取り消します。                     |
| [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)             | 役割を取り消します。                     |
| [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)          | デフォルトの役割を設定します。                |
| [`SET PASSWORD`](/sql-statements/sql-statement-set-password.md)                  | パスワードを変更します。                   |
| [`SET ROLE`](/sql-statements/sql-statement-set-role.md)                          | 現在のセッションでロールを有効にします。           |
| [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md)          | ユーザーに対する`CREATE`ステートメントを表示します。 |
| [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md)                    | ユーザーに関連付けられている権限を表示します。        |
| [`SHOW PRIVILEGES`](/sql-statements/sql-statement-show-privileges.md)            | 利用可能な権限を表示します。                 |

## TiCDC {#ticdc}

<CustomContent platform="tidb">

| SQLステートメント                                                                           | 説明                       |
| ------------------------------------------------------------------------------------ | ------------------------ |
| [`ADMIN [SET|SHOW|UNSET] BDR ROLE`](/sql-statements/sql-statement-admin-bdr-role.md) | BDR（ビジネス開発担当者）の役割を管理します。 |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md)          | クラスター内の最新のTSOを表示します。     |

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)は、TiDB Self-ManagedのTiDBデータをアップストリームに複製するためのツールです。TiCDCのほとんどのSQLステートメントはTiDB Cloudには適用できません。TiDB Cloudの場合は、代わりに[TiDB Cloudコンソール](https://tidbcloud.com)の[変更フィード](/tidb-cloud/changefeed-overview.md)機能を使用してデータをストリーミングできます。

| SQLステートメント                                                                  | 説明                   |
| --------------------------------------------------------------------------- | -------------------- |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md) | クラスター内の最新のTSOを表示します。 |

</CustomContent>

## 統計と計画管理 {#statistics-and-plan-management}

| SQLステートメント                                                                            | 説明                                           |
| ------------------------------------------------------------------------------------- | -------------------------------------------- |
| [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)                     | テーブルに関する統計情報を収集します。                          |
| [`CREATE BINDING`](/sql-statements/sql-statement-create-binding.md)                   | SQL文の実行プランバインディングを作成します。                     |
| [`DROP BINDING`](/sql-statements/sql-statement-drop-binding.md)                       | SQL文から実行プランのバインディングを削除します。                   |
| [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md)                           | テーブルから統計情報を削除します。                            |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                 | `EXPLAIN`と似た動作をしますが、大きな違いは、ステートメントを実行することです。 |
| [`LOAD STATS`](/sql-statements/sql-statement-load-stats.md)                           | 統計情報をTiDBにロードします。                            |
| [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md)         | 統計情報の収集タスクを表示します。                            |
| [`SHOW BINDINGS`](/sql-statements/sql-statement-show-bindings.md)                     | 作成されたSQLバインディングを表示します。                       |
| [`SHOW COLUMN_STATS_USAGE`](/sql-statements/sql-statement-show-column-stats-usage.md) | 列統計の最終使用日時と収集日時を表示します。                       |
| [`SHOW STATS_BUCKETS`](/sql-statements/sql-statement-show-stats-buckets.md)           | 統計情報にバケット情報を表示します。                           |
| [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)           | 統計データの正確性に関する推定値を示します。                       |
| [`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md)     | 統計情報にヒストグラム情報を表示します。                         |
| [`SHOW STATS_LOCKED`](/sql-statements/sql-statement-show-stats-locked.md)             | 統計情報がロックされているテーブルを表示します。                     |
| [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)                 | テーブルに含まれる行数と、そのテーブル内で変更された行数を表示します。          |
| [`SHOW STATS_TOPN`](/sql-statements/sql-statement-show-stats-topn.md)                 | 統計情報の中から上位N件の情報を表示します。                       |
