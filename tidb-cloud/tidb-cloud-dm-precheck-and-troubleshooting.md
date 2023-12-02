---
title: Precheck Errors, Migration Errors, and Alerts for Data Migration
summary: Learn how to resolve precheck errors, migration errors, and alerts when using Data Migration.
---

# データ移行の事前チェック エラー、移行エラー、およびアラート {#precheck-errors-migration-errors-and-alerts-for-data-migration}

このドキュメントでは、 [データ移行を使用してデータを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)場合に事前チェック エラーを解決し、移行エラーをトラブルシューティングし、アラートを購読する方法について説明します。

## 事前チェックエラーと解決策 {#precheck-errors-and-solutions}

このセクションでは、データ移行時の事前チェック エラーと対応する解決策について説明します。これらのエラーは、 [データ移行を使用してデータを移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を実行すると**[事前チェック]**ページに表示されます。

解決策は上流のデータベースによって異なります。

### エラー メッセージ: mysql server_id が 0 より大きいかどうかを確認してください {#error-message-check-whether-mysql-server-id-has-been-greater-than-0}

-   Amazon Aurora MySQL または Amazon RDS: `server_id`がデフォルトで設定されています。設定する必要はありません。完全データ移行と増分データ移行の両方をサポートするには、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   MySQL: MySQL に`server_id`設定するには、 [レプリケーションソースコンフィグレーションの設定](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-masterbaseconfig.html)を参照してください。

### エラー メッセージ: mysql binlogが有効かどうかを確認してください {#error-message-check-whether-mysql-binlog-is-enabled}

-   Amazon Aurora MySQL: [Amazon Aurora MySQL 互換クラスターのバイナリログを有効にするにはどうすればよいですか?](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)を参照してください。完全データ移行と増分データ移行の両方をサポートするには、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   Amazon RDS: [MySQL バイナリ ロギングの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。
-   Google Cloud SQL for MySQL: Google は、MySQL マスター データベースのポイントインタイム リカバリを通じてバイナリ ロギングを可能にします。 [ポイントインタイムリカバリを有効にする](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr#enablingpitr)を参照してください。
-   MySQL: [レプリケーションソースコンフィグレーションの設定](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-masterbaseconfig.html)を参照してください。

### エラー メッセージ: mysql binlog_format が ROW であるかどうかを確認してください {#error-message-check-whether-mysql-binlog-format-is-row}

-   Amazon Aurora MySQL: [Amazon Aurora MySQL 互換クラスターのバイナリログを有効にするにはどうすればよいですか?](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)を参照してください。完全データ移行と増分データ移行の両方をサポートするには、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   Amazon RDS: [MySQL バイナリ ロギングの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。
-   MySQL: `set global binlog_format=ROW;`を実行します。 [バイナリログ形式の設定](https://dev.mysql.com/doc/refman/8.0/en/binary-log-setting.html)を参照してください。

### エラー メッセージ: mysql binlog_row_image が FULL かどうかを確認してください {#error-message-check-whether-mysql-binlog-row-image-is-full}

-   Amazon Aurora MySQL: `binlog_row_image`は構成できません。この事前チェック項目は失敗しません。完全データ移行と増分データ移行の両方をサポートするには、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   Amazon RDS: このプロセスは`binlog_format`パラメーターの設定と似ています。唯一の違いは、変更する必要があるパラメーターが`binlog_format`ではなく`binlog_row_image`であることです。 [MySQL バイナリ ロギングの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。
-   MySQL: `set global binlog_row_image = FULL;` 。 [バイナリログのオプションと変数](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_row_image)を参照してください。

### エラー メッセージ: 移行されたデータベースが binlog_do_db/binlog_ignore_db にあるかどうかを確認してください {#error-message-check-whether-migrated-dbs-are-in-binlog-do-db-binlog-ignore-db}

アップストリーム データベースでbinlog が有効になっていることを確認してください。 [mysql binlog が有効になっているかどうかを確認する](#error-message-check-whether-mysql-binlog-is-enabled)を参照してください。その後、表示されるメッセージに従って問題を解決します。

-   メッセージが`These dbs xxx are not in binlog_do_db xxx`に似ている場合は、移行するすべてのデータベースがリストに含まれていることを確認してください。 [--binlog-do-db=db_name](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_binlog-do-db)を参照してください。
-   メッセージが`These dbs xxx are in binlog_ignore_db xxx`に似ている場合は、移行するすべてのデータベースが無視リストに含まれていないことを確認してください。 [--binlog-ignore-db=db_name](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_binlog-ignore-db)を参照してください。

Amazon Aurora MySQL の場合、この事前チェック項目は失敗しません。完全データ移行と増分データ移行の両方をサポートするには、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。

Amazon RDS の場合、パラメータ`replicate-do-db` 、 `replicate-do-table` 、 `replicate-ignore-db` 、および`replicate-ignore-table`を変更する必要があります。 [MySQL バイナリ ロギングの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。

### エラー メッセージ: 同時接続数がデータベースの最大接続制限を超えているかどうかを確認してください {#error-message-check-if-connection-concurrency-exceeds-database-s-maximum-connection-limit}

上流データベースでエラーが発生した場合は、次のように`max_connections`を設定します。

-   Amazon Aurora MySQL: プロセスは`binlog_format`の設定と似ています。唯一の違いは、変更するパラメーターが`binlog_format`ではなく`max_connections`であることです。 [Amazon Aurora MySQL 互換クラスターのバイナリログを有効にするにはどうすればよいですか?](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)を参照してください。
-   Amazon RDS: プロセスは`binlog_format`の設定と似ています。唯一の違いは、変更するパラメーターが`binlog_format`ではなく`max_connections`であることです。 [MySQL バイナリ ロギングの構成](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)を参照してください。
-   MySQL: ドキュメント[最大接続数](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_connections)に従って`max_connections`を設定します。

TiDB Cloudクラスターでエラーが発生した場合は、ドキュメント[最大接続数](https://docs.pingcap.com/tidb/stable/system-variables#max_connections)に従って`max_connections`を設定します。

## 移行エラーと解決策 {#migration-errors-and-solutions}

このセクションでは、移行中に発生する可能性のある問題と解決策について説明します。これらのエラー メッセージは、 **[移行ジョブの詳細]**ページに表示されます。

### エラー メッセージ: 「移行に必要なバイナリ ログは、ソース データベースに存在しません。移行が成功するために、バイナリ ログ ファイルが十分な期間保持されていることを確認してください。」 {#error-message-the-required-binary-log-for-migration-no-longer-exists-on-the-source-database-please-make-sure-binary-log-files-are-kept-for-long-enough-time-for-migration-to-succeed}

このエラーは、移行するバイナリログがクリーンアップされており、新しいタスクを作成することによってのみ復元できることを意味します。

増分移行に必要なバイナリログが存在することを確認してください。バイナリログの期間を延長するには、 `expire_logs_days`を設定することをお勧めします。移行ジョブで必要な場合は、バイナリログのクリーンアップに`purge binary log`を使用しないでください。

### エラー メッセージ:「指定されたパラメーターを使用してソース データベースに接続できませんでした。ソース データベースが起動しており、指定されたパラメーターを使用して接続できることを確認してください。」 {#error-message-failed-to-connect-to-the-source-database-using-given-parameters-please-make-sure-the-source-database-is-up-and-can-be-connected-using-the-given-parameters}

このエラーは、ソース データベースへの接続が失敗したことを意味します。ソース データベースが起動されており、指定されたパラメータを使用して接続できるかどうかを確認します。ソース データベースが使用可能であることを確認した後、 **[再起動]**をクリックしてタスクの回復を試みることができます。

### 移行タスクが中断され、「ドライバー: 接続が正しくありません」または「接続が無効です」というエラーが発生します。 {#the-migration-task-is-interrupted-and-contains-the-error-driver-bad-connection-or-invalid-connection}

このエラーは、ダウンストリーム TiDB クラスターへの接続が失敗したことを意味します。ダウンストリーム TiDB クラスターが正常な状態 ( `Available`と`Modifying`を含む) であり、ジョブで指定されたユーザー名とパスワードで接続できるかどうかを確認します。ダウンストリーム TiDB クラスターが使用可能であることを確認したら、 **[再起動]**をクリックしてタスクの再開を試みることができます。

### エラー メッセージ: 「指定されたユーザーとパスワードを使用して TiDB クラスターに接続できませんでした。TiDBクラスタが起動しており、指定されたユーザーとパスワードを使用して接続できることを確認してください。」 {#error-message-failed-to-connect-to-the-tidb-cluster-using-the-given-user-and-password-please-make-sure-tidb-cluster-is-up-and-can-be-connected-to-using-the-given-user-and-password}

TiDB クラスターへの接続に失敗しました。 TiDB クラスターが正常な状態 ( `Available`と`Modifying`を含む) であるかどうかを確認することをお勧めします。ジョブで指定されたユーザー名とパスワードを使用して接続できます。 TiDB クラスターが使用可能であることを確認したら、 **「再起動」**をクリックしてタスクの再開を試みることができます。

### エラー メッセージ:「TiDB クラスターstorageが十分ではありません。TiKV のノードstorageを増やしてください。」 {#error-message-tidb-cluster-storage-is-not-enough-please-increase-the-node-storage-of-tikv}

TiDB クラスターのstorageが不足しています。 [TiKV ノードのstorageを増やす](/tidb-cloud/scale-tidb-cluster.md#change-storage)し、 **[再起動]**をクリックしてタスクを再開することをお勧めします。

### エラー メッセージ:「ソース データベースに接続できませんでした。データベースが利用可能か、または最大接続数に達しているかを確認してください。」 {#error-message-failed-to-connect-to-the-source-database-please-check-whether-the-database-is-available-or-the-maximum-connections-have-been-reached}

ソースデータベースへの接続に失敗しました。ソースデータベースが起動しているか、データベース接続数が上限に達していないか、ジョブで指定したパラメータを使用して接続できるかを確認することをお勧めします。ソース データベースが使用可能であることを確認したら、 **[再起動]**をクリックしてジョブを再開できます。

## アラート {#alerts}

TiDB Cloudアラート電子メールを購読すると、アラートが発生したときにすぐに通知を受けることができます。

データ移行に関するアラートは次のとおりです。

-   「データのエクスポート中にデータ移行ジョブでエラーが発生しました」

    推奨されるアクション: データ移行ページのエラー メッセージを確認し、ヘルプについては[移行エラーと解決策](#migration-errors-and-solutions)を参照してください。

-   「データのインポート中にデータ移行ジョブでエラーが発生しました」

    推奨されるアクション: データ移行ページのエラー メッセージを確認し、ヘルプについては[移行エラーと解決策](#migration-errors-and-solutions)を参照してください。

-   「増分データ移行中にデータ移行ジョブでエラーが発生しました」

    推奨されるアクション: データ移行ページのエラー メッセージを確認し、ヘルプについては[移行エラーと解決策](#migration-errors-and-solutions)を参照してください。

-   「増分移行中にデータ移行ジョブが 6 時間以上一時停止されました」

    推奨されるアクション: データ移行ジョブを再開するか、このアラートを無視してください。

-   「レプリケーションの遅延が 10 分を超えており、20 分以上増加し続けています」

    -   推奨される処置: [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)に連絡して助けを求めてください。

これらのアラートに対処するためにサポートが必要な場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

アラート電子メールを購読する方法の詳細については、 [TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)を参照してください。

## こちらも参照 {#see-also}

-   [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
