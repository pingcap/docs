---
title: Precheck Errors, Migration Errors, and Alerts for Data Migration
summary: データ移行時に発生する事前チェックエラー、移行エラー、およびアラートの解決方法を学びましょう。
---

# データ移行に関する事前チェックエラー、移行エラー、およびアラート {#precheck-errors-migration-errors-and-alerts-for-data-migration}

このドキュメントでは[データ移行を使用してデータを移行します](/tidb-cloud/migrate-from-mysql-using-data-migration.md)ときに、事前チェック エラーを解決し、移行エラーをトラブルシューティングし、アラートを購読する方法について説明します。

## 事前チェックのエラーと解決策 {#precheck-errors-and-solutions}

このセクションでは、データ移行時の事前チェック エラーと対応する解決策について説明します。これらのエラーは[データ移行を使用してデータを移行します](/tidb-cloud/migrate-from-mysql-using-data-migration.md)ときに**[事前チェック]**ページに表示されます。

解決策は、使用している上位データベースによって異なります。

### エラーメッセージ: mysql server_id が 0 より大きいかどうかを確認してください {#error-message-check-whether-mysql-server-id-has-been-greater-than-0}

-   Amazon Aurora MySQL または Amazon RDS: `server_id`はデフォルトで設定されています。設定する必要はありません。フルデータ移行と増分データ移行の両方をサポートするには、Amazon Aurora MySQL ライターインスタンスを使用していることを確認してください。
-   MySQL: MySQL 用に`server_id`を構成するには、 [レプリケーションソースコンフィグレーションの設定](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-masterbaseconfig.html)参照してください。

### エラーメッセージ: mysql binlogが有効になっているか確認してください {#error-message-check-whether-mysql-binlog-is-enabled}

-   Amazon Aurora MySQL: [Amazon Aurora MySQL互換クラスターでバイナリログを有効にするにはどうすればよいですか？](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)を参照してください。完全データ移行と増分データ移行の両方をサポートするには、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   Amazon RDS: [MySQLバイナリログの設定](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)参照してください。
-   Google Cloud SQL for MySQL: Google は、MySQL マスター データベースのポイントインタイムリカバリを通じてバイナリ ロギングを可能にします。 [特定時点へのリカバリを有効にする](https://cloud.google.com/sql/docs/mysql/backup-recovery/pitr#enablingpitr)参照してください。
-   MySQL: [レプリケーションソースコンフィグレーションの設定](https://dev.mysql.com/doc/refman/8.0/en/replication-howto-masterbaseconfig.html)参照してください。

### エラーメッセージ: mysql binlog_format が ROW かどうか確認してください {#error-message-check-whether-mysql-binlog-format-is-row}

-   Amazon Aurora MySQL: [Amazon Aurora MySQL互換クラスターでバイナリログを有効にするにはどうすればよいですか？](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)を参照してください。完全データ移行と増分データ移行の両方をサポートするには、Amazon Aurora MySQL ライター インスタンスを使用していることを確認してください。
-   Amazon RDS: [MySQLバイナリログの設定](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html)参照してください。
-   MySQL: `set global binlog_format=ROW;`を実行します。 [バイナリログフォーマットの設定](https://dev.mysql.com/doc/refman/8.0/en/binary-log-setting.html)参照してください。

### エラーメッセージ: mysql binlog_row_image が満杯かどうか確認してください {#error-message-check-whether-mysql-binlog-row-image-is-full}

-   Amazon Aurora MySQL: `binlog_row_image`は設定できません。この事前チェック項目は、設定変更の対象外です。完全データ移行と増分データ移行の両方をサポートするために、Amazon Aurora MySQL ライターインスタンスを使用していることを確認してください。
-   Amazon RDS: 手順は`binlog_format`パラメータの設定と似ています。唯一の違いは、変更する必要のあるパラメータが`binlog_row_image`ではなく`binlog_format`であることです。MySQL [MySQLバイナリログの設定](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
-   MySQL: `set global binlog_row_image = FULL;` 。 [バイナリログのオプションと変数](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_row_image)参照してください。

### エラーメッセージ: 移行されたデータベースが binlog_do_db/binlog_ignore_db に含まれているかどうかを確認してください {#error-message-check-whether-migrated-dbs-are-in-binlog-do-db-binlog-ignore-db}

アップストリーム データベースでbinlogが有効になっていることを確認してください。 [MySQLのbinlogが有効になっているか確認してください。](#error-message-check-whether-mysql-binlog-is-enabled)その後、表示されるメッセージに従って問題を解決します。

-   メッセージが`These dbs xxx are not in binlog_do_db xxx`に似ている場合は、移行したいすべてのデータベースがリストに含まれていることを確認してください。-- [--binlog-do-db=db_name](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_binlog-do-db)を参照してください。
-   メッセージが`These dbs xxx are in binlog_ignore_db xxx`に似ている場合は、移行したいすべてのデータベースが無視リストに含まれていないことを確認してください。-- [--binlog-ignore-db=db_name](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_binlog-ignore-db)を参照してください。

Amazon Aurora MySQL の場合、この事前チェック項目はエラーになりません。完全データ移行と増分データ移行の両方をサポートするために、Amazon Aurora MySQL ライターインスタンスを使用していることを確認してください。

Amazon RDS の場合、次のパラメータを変更する必要があります: `replicate-do-db` 、 `replicate-do-table` 、 `replicate-ignore-db` 、および`replicate-ignore-table` 。MySQL [MySQLバイナリログの設定](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).

### エラーメッセージ：接続同時接続数がデータベースの最大接続制限を超えていないか確認してください。 {#error-message-check-if-connection-concurrency-exceeds-database-s-maximum-connection-limit}

上流のデータベースでエラーが発生した場合は、 `max_connections`を次のように設定してください。

-   Amazon Aurora MySQL: このプロセスは、 `binlog_format`の設定と似ています。唯一の違いは、変更するパラメータが`max_connections`ではなく`binlog_format`であることです。 [Amazon Aurora MySQL互換クラスターでバイナリログを有効にするにはどうすればよいですか？](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls)参照してください。
-   Amazon RDS: 手順は`binlog_format`の設定と似ています。唯一の違いは、変更するパラメータが`max_connections`ではなく`binlog_format` } であることです。MySQL [MySQLバイナリログの設定](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.MySQL.BinaryFormat.html).
-   MySQL: ドキュメント[最大接続数](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_connections)に従って`max_connections`を設定します。

TiDB Cloudクラスターでエラーが発生した場合は、ドキュメントの[最大接続数](https://docs.pingcap.com/tidb/stable/system-variables#max_connections)に従って`max_connections`を設定します。

## 移行エラーとその解決策 {#migration-errors-and-solutions}

このセクションでは、移行中に発生する可能性のある問題とその解決策について説明します。これらのエラーメッセージは、**移行ジョブの詳細**ページに表示されます。

### エラーメッセージ：「移行に必要なバイナリログがソースデータベースに存在しません。移行が成功するためには、バイナリログファイルが十分な期間保持されていることを確認してください。」 {#error-message-the-required-binary-log-for-migration-no-longer-exists-on-the-source-database-please-make-sure-binary-log-files-are-kept-for-long-enough-time-for-migration-to-succeed}

このエラーは、移行対象のバイナリログが既にクリーンアップされており、新しいタスクを作成することによってのみ復元できることを意味します。

増分移行に必要なバイナリログが存在することを確認してください。バイナリログの保存期間を延長するために、 `expire_logs_days`を設定することをお勧めします。移行ジョブでバイナリログのクリーンアップが必要な場合は、 `purge binary log`を使用してバイナリログをクリーンアップしないでください。

### エラーメッセージ：「指定されたパラメータを使用してソースデータベースに接続できませんでした。ソースデータベースが稼働しており、指定されたパラメータを使用して接続できることを確認してください。」 {#error-message-failed-to-connect-to-the-source-database-using-given-parameters-please-make-sure-the-source-database-is-up-and-can-be-connected-using-the-given-parameters}

このエラーは、ソースデータベースへの接続に失敗したことを意味します。ソースデータベースが起動しており、指定されたパラメータを使用して接続できるかどうかを確認してください。ソースデータベースが利用可能であることを確認したら、 **「再起動」**をクリックしてタスクの復旧を試みてください。

### 移行タスクが中断され、「ドライバー: 接続不良」または「無効な接続」というエラーが含まれています。 {#the-migration-task-is-interrupted-and-contains-the-error-driver-bad-connection-or-invalid-connection}

このエラーは、ダウンストリームの TiDB クラスタへの接続に失敗したことを意味します。ダウンストリームの TiDB クラスタが正常な状態（ `Available`および`Modifying`を含む）であり、ジョブで指定されたユーザー名とパスワードで接続できるかどうかを確認してください。ダウンストリームの TiDB クラスタが利用可能であることを確認したら、 **[再起動]**をクリックしてタスクを再開してみてください。

### エラーメッセージ：「指定されたユーザー名とパスワードを使用してTiDBクラスタに接続できませんでした。TiDBクラスタが起動しており、指定されたユーザー名とパスワードで接続できることを確認してください。」 {#error-message-failed-to-connect-to-the-tidb-cluster-using-the-given-user-and-password-please-make-sure-tidb-cluster-is-up-and-can-be-connected-to-using-the-given-user-and-password}

TiDB クラスターへの接続に失敗しました。TiDB クラスターが正常な状態（ `Available`および`Modifying`を含む）であるかどうかを確認することをお勧めします。ジョブで指定されたユーザー名とパスワードを使用して接続できます。TiDB クラスターが利用可能であることを確認したら、 **[再起動]**をクリックしてタスクを再開してみてください。

### エラーメッセージ：「TiDBクラスタのstorageが不足しています。TiKVのノードstorageを増やしてください。」 {#error-message-tidb-cluster-storage-is-not-enough-please-increase-the-node-storage-of-tikv}

TiDB クラスターのstorageが不足しています。 [TiKVノードのstorageを増やす](/tidb-cloud/scale-tidb-cluster.md#change-storage)から、 **「再起動」**をクリックしてタスクを再開することをお勧めします。

### エラーメッセージ：「ソースデータベースへの接続に失敗しました。データベースが利用可能か、または最大接続数に達していないかを確認してください。」 {#error-message-failed-to-connect-to-the-source-database-please-check-whether-the-database-is-available-or-the-maximum-connections-have-been-reached}

ソースデータベースへの接続に失敗しました。ソースデータベースが起動しているか、データベース接続数が上限に達していないか、ジョブで指定されたパラメータを使用して接続できるかを確認してください。ソースデータベースが利用可能であることを確認したら、 **「再起動」**をクリックしてジョブを再開してください。

### エラーメッセージ：「エラー 1273: 新しい照合順序が有効になっている場合、サポートされていない照合順序です: &#39;utf8mb4_0900_ai_ci&#39;」 {#error-message-error-1273-unsupported-collation-when-new-collation-is-enabled-utf8mb4-0900-ai-ci}

ダウンストリームのTiDBクラスタでスキーマを作成できませんでした。このエラーは、アップストリームのMySQLで使用されている照合順序がTiDBクラスタでサポートされていないことを意味します。

この問題を解決するには、 [サポートされている照合順序](/character-set-and-collation.md#character-sets-and-collations-supported-by-tidb)に基づいて TiDB クラスターにスキーマを作成し、 **[再起動]**をクリックしてタスクを再開します。

### エラーメッセージ：「LOCK TABLES ... アクセスが拒否されました」 {#error-message-lock-tables-access-denied}

ソース データベース ユーザーに`LOCK TABLES`権限がないため、データの完全なエクスポートが失敗します。このエラーは通常、マネージド MySQL サービス (Amazon RDS、 Aurora、ApsaraDB RDS for MySQL、Azure Database for MySQL、Google Cloud SQL など) から移行する場合に発生します。これらのサービスでは、クラウド プロバイダーによって`FLUSH TABLES WITH READ LOCK` (FTWRL) が許可されていません。このシナリオでは、DM はデフォルトの`consistency=auto`モードを使用し、完全なエクスポート中にデータの一貫性を確保するために`LOCK TABLES`にフォールバックします。この操作には`LOCK TABLES`権限が必要です。

> **注記：**
>
> このエラーは`RELOAD`権限がないなど、他の理由で FTWRL が利用できない場合にも、自己管理型の MySQL インスタンスで発生する可能性があります。

この問題を解決するには、移行元のMySQLデータベースで、移行ユーザーに`LOCK TABLES`権限を付与してください。

```sql
GRANT LOCK TABLES ON *.* TO 'dm_source_user'@'%';
```

その後、 **「再起動」**をクリックしてタスクを再開してください。

## アラート {#alerts}

TiDB Cloudのアラートメールを購読すると、アラートが発生した際にタイムリーに通知を受け取ることができます。

データ移行に関するアラートは以下のとおりです。

-   データ移行ジョブで、データエクスポート中にエラーが発生しました。

    推奨されるアクション: データ移行ページでエラー メッセージを確認し、[移行エラーとその解決策](#migration-errors-and-solutions)でヘルプを参照してください。

-   データ移行ジョブのデータインポート中にエラーが発生しました

    推奨されるアクション: データ移行ページでエラー メッセージを確認し、[移行エラーとその解決策](#migration-errors-and-solutions)でヘルプを参照してください。

-   「増分データ移行中にデータ移行ジョブでエラーが発生しました」

    推奨されるアクション: データ移行ページでエラー メッセージを確認し、[移行エラーとその解決策](#migration-errors-and-solutions)でヘルプを参照してください。

-   「増分移行中にデータ移行ジョブが6時間以上一時停止されました」

    推奨される対処法：データ移行ジョブを再開するか、このアラートを無視してください。

-   「レプリケーション遅延が10分を超え、20分以上経過してもなお増加し続けている」

    -   推奨されるアクション: [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

これらのアラートへの対応についてサポートが必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

アラート電子メールを購読する方法の詳細については、 [TiDB Cloudの組み込みアラート機能](/tidb-cloud/monitor-built-in-alerting.md)を参照してください。

## 関連項目 {#see-also}

-   [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
