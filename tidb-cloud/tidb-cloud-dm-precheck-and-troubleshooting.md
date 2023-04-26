---
title: Precheck Errors, Migration Errors, and Alerts for Data Migration
summary: Learn how to resolve precheck errors, migration errors, and alerts when using Data Migration.
---

# データ移行の事前チェック エラー、移行エラー、アラート {#precheck-errors-migration-errors-and-alerts-for-data-migration}

このドキュメントでは、事前チェック エラーを解決[データ移行を使用してデータを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)方法、移行エラーをトラブルシューティングする方法、およびアラートをサブスクライブする方法について説明します。

## 事前チェックのエラーと解決策 {#precheck-errors-and-solutions}

このセクションでは、データ移行中の事前チェック エラーと対応する解決策について説明します。これらのエラーは、 [データ移行を使用してデータを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)場合に**[事前チェック]**ページに表示されます。

ソリューションは、上流のデータベースによって異なります。

### エラー メッセージ: mysql server_id が 0 より大きいかどうかを確認してください {#error-message-check-whether-mysql-server-id-has-been-greater-than-0}

-   Amazon Aurora MySQL または Amazon RDS: `server_id`がデフォルトで設定されています。構成する必要はありません。完全なデータ移行と増分データ移行の両方をサポートするために、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   MySQL: MySQL 用に`server_id`構成するには、 [レプリケーション ソースコンフィグレーションの設定](https://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)を参照してください。

### エラー メッセージ: mysql binlogが有効になっているかどうかを確認してください {#error-message-check-whether-mysql-binlog-is-enabled}

-   Amazon Aurora MySQL: [Amazon Aurora MySQL 互換クラスターのバイナリログを有効にする方法](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)を参照してください。完全なデータ移行と増分データ移行の両方をサポートするために、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   Amazon RDS: [MySQL バイナリ ログの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。
-   Google Cloud SQL for MySQL: Google は、MySQL マスター データベースのポイント イン タイム リカバリを通じてバイナリ ロギングを有効にします。 [ポイントインタイム リカバリを有効にする](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr#enablingpitr)を参照してください。
-   MySQL: [レプリケーション ソースコンフィグレーションの設定](https://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)を参照してください。

### エラー メッセージ: mysql binlog_format が ROW かどうかを確認してください {#error-message-check-whether-mysql-binlog-format-is-row}

-   Amazon Aurora MySQL: [Amazon Aurora MySQL 互換クラスターのバイナリログを有効にする方法](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)を参照してください。完全なデータ移行と増分データ移行の両方をサポートするために、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   Amazon RDS: [MySQL バイナリ ログの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。
-   MySQL: `set global binlog_format=ROW;`を実行します。 [バイナリログ形式の設定](https://dev.mysql.com/doc/refman/5.7/en/binary-log-setting.html)を参照してください。

### エラー メッセージ: mysql の binlog_row_image が FULL かどうかを確認してください {#error-message-check-whether-mysql-binlog-row-image-is-full}

-   Amazon Aurora MySQL: `binlog_row_image`は設定できません。それに対して、この事前チェック項目は失敗しません。完全なデータ移行と増分データ移行の両方をサポートするために、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   Amazon RDS: プロセスは`binlog_format`パラメータの設定に似ています。唯一の違いは、変更する必要があるパラメーターが`binlog_format`ではなく`binlog_row_image`であることです。 [MySQL バイナリ ログの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。
-   MySQL: `set global binlog_row_image = FULL;` . [バイナリ ログのオプションと変数](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_binlog_row_image)を参照してください。

### エラー メッセージ: 移行されたデータベースが binlog_do_db/binlog_ignore_db にあるかどうかを確認します {#error-message-check-whether-migrated-dbs-are-in-binlog-do-db-binlog-ignore-db}

アップストリーム データベースでbinlog が有効になっていることを確認します。 [mysql binlog が有効になっているかどうかを確認する](#error-message-check-whether-mysql-binlog-is-enabled)を参照してください。その後、表示されるメッセージに従って問題を解決します。

-   メッセージが`These dbs xxx are not in binlog_do_db xxx`のような場合は、移行するすべてのデータベースがリストにあることを確認してください。 [--binlog-do-db=db_name](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#option_mysqld_binlog-do-db)を参照してください。
-   メッセージが`These dbs xxx are in binlog_ignore_db xxx`のような場合は、移行するすべてのデータベースが無視リストに含まれていないことを確認してください。 [--binlog-ignore-db=db_name](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#option_mysqld_binlog-ignore-db)を参照してください。

Amazon Aurora MySQL の場合、この事前チェック項目は失敗しません。完全なデータ移行と増分データ移行の両方をサポートするために、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。

Amazon RDS の場合、次のパラメーターを変更する必要があります: `replicate-do-db` 、 `replicate-do-table` 、 `replicate-ignore-db` 、および`replicate-ignore-table` 。 [MySQL バイナリ ログの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。

### エラー メッセージ: 同時接続数がデータベースの最大接続制限を超えていないか確認してください {#error-message-check-if-connection-concurrency-exceeds-database-s-maximum-connection-limit}

アップストリームデータベースでエラーが発生した場合は、次のように`max_connections`を設定します。

-   Amazon Aurora MySQL: プロセスは`binlog_format`の設定に似ています。唯一の違いは、変更するパラメーターが`binlog_format`ではなく`max_connections`であることです。 [Amazon Aurora MySQL 互換クラスターのバイナリログを有効にする方法](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)を参照してください。
-   Amazon RDS: プロセスは`binlog_format`の設定に似ています。唯一の違いは、変更するパラメーターが`binlog_format`ではなく`max_connections`であることです。 [MySQL バイナリ ログの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。
-   MySQL: ドキュメント[最大接続数](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_max_connections)に従って`max_connections`を構成します。

TiDB Cloudクラスターでエラーが発生した場合は、ドキュメント[最大接続数](https://docs.pingcap.com/tidb/stable/system-variables#max_connections)に従って`max_connections`を設定します。

## 移行エラーと解決策 {#migration-errors-and-solutions}

このセクションでは、移行中に発生する可能性のある問題と解決策について説明します。これらのエラー メッセージは、 **[移行ジョブの詳細]**ページに表示されます。

### エラー メッセージ:「移行に必要なバイナリ ログがソース データベースに存在しません。移行が成功するまで、バイナリ ログ ファイルが十分な時間保持されていることを確認してください。」 {#error-message-the-required-binary-log-for-migration-no-longer-exists-on-the-source-database-please-make-sure-binary-log-files-are-kept-for-long-enough-time-for-migration-to-succeed}

このエラーは、移行するバイナリログがクリーンアップされており、新しいタスクを作成することによってのみ復元できることを意味します。

増分移行に必要なバイナリログが存在することを確認してください。 binlog の期間を延長するには、 `expire_logs_days`を構成することをお勧めします。一部の移行ジョブで必要な場合は、バイナリログのクリーンアップに`purge binary log`を使用しないでください。

### エラー メッセージ:「指定されたパラメーターを使用してソース データベースに接続できませんでした。ソース データベースが起動しており、指定されたパラメーターを使用して接続できることを確認してください。」 {#error-message-failed-to-connect-to-the-source-database-using-given-parameters-please-make-sure-the-source-database-is-up-and-can-be-connected-using-the-given-parameters}

このエラーは、ソース データベースへの接続が失敗したことを意味します。ソース・データベースが開始されており、指定されたパラメーターを使用して接続できるかどうかを確認してください。ソース データベースが使用可能であることを確認したら、 **[再起動]**をクリックしてタスクの回復を試みることができます。

### 移行タスクが中断され、「ドライバー: 接続が正しくありません」または「接続が無効です」というエラーが表示される {#the-migration-task-is-interrupted-and-contains-the-error-driver-bad-connection-or-invalid-connection}

このエラーは、下流の TiDB クラスターへの接続が失敗したことを意味します。ダウンストリームの TiDB クラスターが正常な状態 ( `Available`と`Modifying`を含む) であり、ジョブで指定されたユーザー名とパスワードで接続できるかどうかを確認します。ダウンストリームの TiDB クラスターが使用可能であることを確認したら、 **[再起動]**をクリックしてタスクの再開を試みることができます。

### エラー メッセージ:「指定されたユーザーとパスワードを使用して TiDB クラスターに接続できませんでした。TiDBクラスタが起動しており、指定されたユーザーとパスワードを使用して接続できることを確認してください。」 {#error-message-failed-to-connect-to-the-tidb-cluster-using-the-given-user-and-password-please-make-sure-tidb-cluster-is-up-and-can-be-connected-to-using-the-given-user-and-password}

TiDB クラスターへの接続に失敗しました。 TiDB クラスターが正常な状態であるかどうかを確認することをお勧めします ( `Available`と`Modifying`を含む)。ジョブで指定されたユーザー名とパスワードで接続できます。 TiDB クラスターが使用可能であることを確認したら、 **[再起動]**をクリックしてタスクの再開を試みることができます。

### エラー メッセージ:「TiDB クラスターstorageが不足しています。TiKV のノードstorageを増やしてください。」 {#error-message-tidb-cluster-storage-is-not-enough-please-increase-the-node-storage-of-tikv}

TiDB クラスターstorageが不足しています。 [TiKV ノードstorageを増やす](/tidb-cloud/scale-tidb-cluster.md#change-node-storage)にしてから、 **[再起動]**をクリックしてタスクを再開することをお勧めします。

### エラー メッセージ:「ソース データベースに接続できませんでした。データベースが使用可能かどうか、または最大接続数に達しているかどうかを確認してください。」 {#error-message-failed-to-connect-to-the-source-database-please-check-whether-the-database-is-available-or-the-maximum-connections-have-been-reached}

ソース データベースへの接続に失敗しました。ソースデータベースが起動しているか、データベース接続数が上限に達していないか、ジョブで指定されたパラメーターを使用して接続できるかを確認することをお勧めします。ソース データベースが使用可能であることを確認したら、 **[再起動]**をクリックしてジョブの再開を試みることができます。

## アラート {#alerts}

TiDB Cloudアラート メールを購読して、アラートが発生したときに通知を受けることができます。

以下は、データ移行に関するアラートです。

-   「データのエクスポート中にデータ移行ジョブがエラーに遭遇しました」

    推奨されるアクション: データ移行ページのエラー メッセージを確認し、ヘルプについては[移行エラーと解決策](#migration-errors-and-solutions)を参照してください。

-   「データのインポート中にデータ移行ジョブがエラーに遭遇しました」

    推奨されるアクション: データ移行ページのエラー メッセージを確認し、ヘルプについては[移行エラーと解決策](#migration-errors-and-solutions)を参照してください。

-   「増分データ移行中にデータ移行ジョブがエラーに遭遇しました」

    推奨されるアクション: データ移行ページのエラー メッセージを確認し、ヘルプについては[移行エラーと解決策](#migration-errors-and-solutions)を参照してください。

-   「増分移行中にデータ移行ジョブが 6 時間以上一時停止されました」

    推奨されるアクション: データ移行ジョブを再開するか、このアラートを無視してください。

-   「レプリケーション ラグが 10 分を超えており、静止状態が 20 分以上増加しています」

    -   推奨処置: [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)に連絡して助けを求めてください。

これらのアラートに対処するための支援が必要な場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)に連絡して相談してください。

アラート E メールをサブスクライブする方法の詳細については、 [TiDB Cloudの組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)を参照してください。

## こちらもご覧ください {#see-also}

-   [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
