---
title:  Migrate from Amazon RDS for Oracle to TiDB Cloud Using AWS DMS
summary: AWS Database Migration Service (AWS DMS) を使用して、Amazon RDS for Oracle からTiDB Cloud Starterへデータを移行する方法を学びましょう。
---

# AWS DMSを使用してAmazon RDS for OracleからTiDB Cloudに移行する {#migrate-from-amazon-rds-for-oracle-to-tidb-cloud-using-aws-dms}

このドキュメントでは、AWS Database Migration Service (AWS DMS) を使用して Amazon RDS for Oracle から[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)へデータを移行する手順を段階的に説明します。

> **ヒント：**
>
> このドキュメントの手順は、 TiDB Cloud Starterインスタンスに加えて、 TiDB Cloud Essentialインスタンスでも適用できます。

TiDB CloudとAWS DMSについてさらに詳しく知りたい場合は、以下をご覧ください。

-   [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)
-   [TiDB開発者ガイド](https://docs.pingcap.com/tidbcloud/dev-guide-overview)
-   [AWS DMS ドキュメント](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.html)

## AWS DMSを使う理由とは？ {#why-use-aws-dms}

AWS DMSは、リレーショナルデータベース、データウェアハウス、NoSQLデータベース、およびその他の種類のデータストアの移行を可能にするクラウドサービスです。

PostgreSQL、Oracle、SQL Serverなどの異種データベースからTiDB Cloudへデータを移行する場合は、AWS DMSの使用をお勧めします。

## デプロイメントアーキテクチャ {#deployment-architecture}

大まかに言うと、以下の手順に従ってください。

1.  Oracle用のAmazon RDSソースを設定します。
2.  TiDB Cloud Starterインスタンスを作成します。
3.  AWS DMSを使用してデータ移行（フルロード）を設定します。

以下の図は、高レベルのアーキテクチャを示しています。

![Architecture](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-0.png)

## 前提条件 {#prerequisites}

始める前に、以下の前提条件をお読みください。

-   [AWS DMSの前提条件](/tidb-cloud/migrate-from-mysql-using-aws-dms.md#prerequisites)
-   [AWSクラウドアカウント](https://aws.amazon.com)
-   [TiDB Cloudアカウント](https://tidbcloud.com)
-   [DBeaver](https://dbeaver.io/)

次に、AWS DMS を使用して Amazon RDS for Oracle からTiDB Cloudへデータを移行する方法を学びます。

## ステップ1. VPCを作成する {#step-1-create-a-vpc}

[AWSコンソール](https://console.aws.amazon.com/vpc/home#vpcs:)にログインし、AWS VPCを作成してください。後でこのVPC内にOracle RDSおよびDMSインスタンスを作成する必要があります。

VPC の作成方法については、 [VPCの作成](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#Create-VPC)参照してください。

![Create VPC](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-1.png)

## ステップ2. Oracle DBインスタンスを作成する {#step-2-create-an-oracle-db-instance}

先ほど作成したVPC内にOracle DBインスタンスを作成し、パスワードを控えてパブリックアクセス権限を付与してください。AWSスキーマ変換ツールを使用するには、パブリックアクセスを有効にする必要があります。なお、本番環境でパブリックアクセス権限を付与することは推奨されません。

Oracle DB インスタンスの作成方法については、「Oracle DB インスタンス[Oracle DBインスタンスを作成し、Oracle DBインスタンス上のデータベースに接続する](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.Oracle.html)。

![Create Oracle RDS](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-2.png)

## ステップ3．Oracleでテーブルデータを準備する {#step-3-prepare-the-table-data-in-oracle}

以下のスクリプトを使用して、github_events テーブルに 10,000 行のデータを作成し、データを投入します。GitHub イベントデータセットは[GHアーカイブ](https://gharchive.org/)からダウンロードできます。 10,000 行のデータが含まれています。以下の SQL スクリプトを使用して Oracle で実行します。

-   [table_schema_oracle.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_table_schema.sql)
-   [oracle_data.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_data.sql)

SQLスクリプトの実行が完了したら、Oracleのデータを確認してください。以下の例では、 [DBeaver](https://dbeaver.io/)を使用してデータを照会します。

![Oracle RDS Data](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-3.png)

## ステップ4. TiDB Cloud Starterインスタンスを作成する {#step-4-create-a-tidb-cloud-starter-instance}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。

2.  [TiDB Cloud Starterインスタンスを作成する](/tidb-cloud/tidb-cloud-quickstart.md)。

3.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Starterインスタンスの名前をクリックすると、その概要ページに移動します。

4.  右上隅にある**「接続」**をクリックします。

5.  **「パスワードを生成」**をクリックしてパスワードを生成し、生成されたパスワードをコピーしてください。

## ステップ5. AWS DMSレプリケーションインスタンスを作成する {#step-5-create-an-aws-dms-replication-instance}

1.  AWS DMS コンソールの[レプリケーションインスタンス](https://console.aws.amazon.com/dms/v2/home#replicationInstances)ページに移動し、対応するリージョンに切り替えます。

2.  VPC 内に`dms.t3.large`を使用して AWS DMS レプリケーション インスタンスを作成します。

    ![Create AWS DMS Instance](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-8.png)

> **注記：**
>
> TiDB Cloud Starterで動作する AWS DMS レプリケーション インスタンスを作成する詳細な手順については、 [AWS DMSをTiDB Cloudに接続する](/tidb-cloud/tidb-cloud-connect-aws-dms.md)を参照してください。

## ステップ6．DMSエンドポイントを作成する {#step-6-create-dms-endpoints}

1.  [AWS DMSコンソール](https://console.aws.amazon.com/dms/v2/home)で、左側のペインにある`Endpoints`メニュー項目をクリックします。

2.  OracleのソースエンドポイントとTiDBのターゲットエンドポイントを作成します。

    以下のスクリーンショットは、ソースエンドポイントの設定を示しています。

    ![Create AWS DMS Source endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-9.png)

    以下のスクリーンショットは、ターゲットエンドポイントの設定を示しています。

    ![Create AWS DMS Target endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-10.png)

> **注記：**
>
> TiDB Cloud Starter DMS エンドポイントを作成する詳細な手順については、 [AWS DMSをTiDB Cloudに接続する](/tidb-cloud/tidb-cloud-connect-aws-dms.md)参照してください。

## ステップ7．スキーマを移行する {#step-7-migrate-the-schema}

この例では、スキーマ定義が単純なため、AWS DMS がスキーマを自動的に処理します。

AWS Schema Conversion Tool を使用してスキーマを移行する場合は、 [AWS SCTのインストール](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Installing.html#CHAP_Installing.Procedure)参照してください。

詳細については、 [AWS SCTを使用してソーススキーマをターゲットデータベースに移行する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SCT.html)参照してください。

## ステップ8. データベース移行タスクを作成する {#step-8-create-a-database-migration-task}

1.  AWS DMS コンソールで、 [データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページに移動します。お住まいの地域に切り替えてください。次に、ウィンドウの右上隅にある**「タスクの作成」を**クリックします。

    ![Create task](/media/tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2.  データベース移行タスクを作成し、**選択ルール**を指定します。

    ![Create AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-11.png)

    ![AWS DMS migration task selection rules](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-12.png)

3.  タスクを作成し、開始し、タスクが完了するまで待ちます。

4.  **テーブル統計**をクリックしてテーブルを確認してください。スキーマ名は`ADMIN`です。

    ![Check AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-13.png)

## ステップ9. 下流のTiDBのデータを確認する {#step-9-check-data-in-the-downstream-tidb}

[TiDB Cloud Starterインスタンス](https://tidbcloud.com/tidbs)に接続します。そして、 `admin.github_event`テーブルのデータを確認します。次のスクリーンショットに示すように、DMSは`github_events`テーブルと10000行のデータを正常に移行しました。

![Check Data In TiDB](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-14.png)

## まとめ {#summary}

AWS DMS を使用すると、このドキュメントの例に従って、任意の上流の AWS RDS データベースからデータを正常に移行できます。

移行中に問題や障害が発生した場合は、 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home)のログ情報を確認して問題のトラブルシューティングを行ってください。

![Troubleshooting](/media/tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## 関連項目 {#see-also}

-   [AWS DMSを使用してMySQL互換データベースから移行する](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
-   [AWS DMSをTiDB Cloudに接続する](/tidb-cloud/tidb-cloud-connect-aws-dms.md)
