---
title:  Migrate from Amazon RDS for Oracle to TiDB Cloud Using AWS DMS
summary: AWS Database Migration Service (AWS DMS) を使用して、Amazon RDS for Oracle からTiDB Cloud Serverless にデータを移行する方法を学びます。
---

# AWS DMS を使用して Amazon RDS for Oracle からTiDB Cloudに移行する {#migrate-from-amazon-rds-for-oracle-to-tidb-cloud-using-aws-dms}

このドキュメントでは、AWS Database Migration Service (AWS DMS) を使用して Amazon RDS for Oracle から[TiDB Cloudサーバーレス](https://tidbcloud.com/clusters/create-cluster)にデータを移行する方法の例を段階的に説明します。

TiDB Cloudと AWS DMS について詳しく知りたい場合は、以下を参照してください。

-   [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)
-   [TiDB 開発者ガイド](https://docs.pingcap.com/tidbcloud/dev-guide-overview)
-   [AWS DMS ドキュメント](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.html)

## AWS DMS を使用する理由 {#why-use-aws-dms}

AWS DMS は、リレーショナル データベース、データ ウェアハウス、NoSQL データベース、その他の種類のデータ ストアの移行を可能にするクラウド サービスです。

PostgreSQL、Oracle、SQL Server などの異種データベースからTiDB Cloudにデータを移行する場合は、AWS DMS を使用することをお勧めします。

## デプロイメントアーキテクチャ {#deployment-architecture}

大まかに言うと、次の手順に従います。

1.  ソース Amazon RDS for Oracle をセットアップします。
2.  ターゲット[TiDB Cloudサーバーレス](https://tidbcloud.com/project/clusters/create-cluster)を設定します。
3.  AWS DMS を使用してデータ移行 (フルロード) を設定します。

次の図は、高レベルのアーキテクチャを示しています。

![Architecture](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-0.png)

## 前提条件 {#prerequisites}

始める前に次の前提条件をお読みください。

-   [AWS DMS の前提条件](/tidb-cloud/migrate-from-mysql-using-aws-dms.md#prerequisites)
-   [AWSクラウドアカウント](https://aws.amazon.com)
-   [TiDB Cloudアカウント](https://tidbcloud.com)
-   [DBeaver](https://dbeaver.io/)

次に、AWS DMS を使用して Amazon RDS for Oracle からTiDB Cloudにデータを移行する方法を学習します。

## ステップ1. VPCを作成する {#step-1-create-a-vpc}

[AWSコンソール](https://console.aws.amazon.com/vpc/home#vpcs:)にログインし、AWS VPC を作成します。この VPC に、後で Oracle RDS と DMS インスタンスを作成する必要があります。

VPC を作成する方法については、 [VPCの作成](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#Create-VPC)参照してください。

![Create VPC](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-1.png)

## ステップ2. Oracle DBインスタンスを作成する {#step-2-create-an-oracle-db-instance}

先ほど作成したVPCにOracle DBインスタンスを作成し、パスワードを記憶してパブリックアクセスを許可してください。AWS Schema Conversion Toolを使用するには、パブリックアクセスを有効にする必要があります。本番環境ではパブリックアクセスを許可することは推奨されませんのでご注意ください。

Oracle DB インスタンスを作成する方法については、 [Oracle DBインスタンスを作成し、Oracle DBインスタンス上のデータベースに接続する](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.Oracle.html)参照してください。

![Create Oracle RDS](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-2.png)

## ステップ3. Oracleでテーブルデータを準備する {#step-3-prepare-the-table-data-in-oracle}

以下のスクリプトを使用して、github_events テーブルに10,000行のデータを作成し、入力します。github イベントデータセットは[GHアーカイブ](https://gharchive.org/)からダウンロードできます。データセットには10,000行のデータが含まれています。Oracle で実行するには、以下のSQLスクリプトを使用してください。

-   [テーブルスキーマOracle.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_table_schema.sql)
-   [oracle_data.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_data.sql)

SQLスクリプトの実行が完了したら、Oracleでデータを確認します。次の例では、 [DBeaver](https://dbeaver.io/)使用してデータをクエリしています。

![Oracle RDS Data](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-3.png)

## ステップ4. TiDB Cloud Serverlessクラスターを作成する {#step-4-create-a-tidb-cloud-serverless-cluster}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/project/clusters)にログインします。

2.  [TiDB Cloud Serverless クラスターを作成する](/tidb-cloud/tidb-cloud-quickstart.md) 。

3.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲット クラスター名をクリックして概要ページに移動します。

4.  右上隅の**[接続]**をクリックします。

5.  **「パスワードの生成」**をクリックしてパスワードを生成し、生成されたパスワードをコピーします。

## ステップ5. AWS DMSレプリケーションインスタンスを作成する {#step-5-create-an-aws-dms-replication-instance}

1.  AWS DMS コンソールの[レプリケーションインスタンス](https://console.aws.amazon.com/dms/v2/home#replicationInstances)ページに移動し、対応するリージョンに切り替えます。

2.  VPC に`dms.t3.large`の AWS DMS レプリケーションインスタンスを作成します。

    ![Create AWS DMS Instance](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-8.png)

> **注記：**
>
> TiDB Cloud Serverless と連携する AWS DMS レプリケーションインスタンスを作成する詳細な手順については、 [AWS DMS をTiDB Cloudクラスターに接続する](/tidb-cloud/tidb-cloud-connect-aws-dms.md)参照してください。

## ステップ6. DMSエンドポイントを作成する {#step-6-create-dms-endpoints}

1.  [AWS DMSコンソール](https://console.aws.amazon.com/dms/v2/home)で、左側のペインの`Endpoints`メニュー項目をクリックします。

2.  Oracle ソース エンドポイントと TiDB ターゲット エンドポイントを作成します。

    次のスクリーンショットは、ソース エンドポイントの構成を示しています。

    ![Create AWS DMS Source endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-9.png)

    次のスクリーンショットは、ターゲット エンドポイントの構成を示しています。

    ![Create AWS DMS Target endpoint](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-10.png)

> **注記：**
>
> TiDB Cloud Serverless DMS エンドポイントを作成する詳細な手順については、 [AWS DMS をTiDB Cloudクラスターに接続する](/tidb-cloud/tidb-cloud-connect-aws-dms.md)参照してください。

## ステップ7. スキーマを移行する {#step-7-migrate-the-schema}

この例では、スキーマ定義が単純なので、AWS DMS が自動的にスキーマを処理します。

AWS スキーマ変換ツールを使用してスキーマを移行する場合は、 [AWS SCT のインストール](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Installing.html#CHAP_Installing.Procedure)参照してください。

詳細については[AWS SCT を使用してソーススキーマをターゲットデータベースに移行する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SCT.html)参照してください。

## ステップ8. データベース移行タスクを作成する {#step-8-create-a-database-migration-task}

1.  AWS DMS コンソールで[データ移行タスク](https://console.aws.amazon.com/dms/v2/home#tasks)ページ目に移動し、リージョンを切り替えます。次に、ウィンドウの右上隅にある**「タスクの作成」**をクリックします。

    ![Create task](/media/tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2.  データベース移行タスクを作成し、**選択ルール**を指定します。

    ![Create AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-11.png)

    ![AWS DMS migration task selection rules](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-12.png)

3.  タスクを作成して開始し、タスクが完了するまで待機します。

4.  **テーブル統計**をクリックしてテーブルを確認します。スキーマ名は`ADMIN`です。

    ![Check AWS DMS migration task](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-13.png)

## ステップ9. 下流TiDBクラスタのデータを確認する {#step-9-check-data-in-the-downstream-tidb-cluster}

[TiDB Cloudサーバーレス クラスター](https://tidbcloud.com/clusters/create-cluster)に接続し、テーブル`admin.github_event`データを確認します。次のスクリーンショットに示すように、DMS はテーブル`github_events`と 10,000 行のデータが正常に移行されました。

![Check Data In TiDB](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-14.png)

## まとめ {#summary}

AWS DMS を使用すると、このドキュメントの例に従って、任意のアップストリーム AWS RDS データベースからデータを正常に移行できます。

移行中に問題や障害が発生した場合は、 [クラウドウォッチ](https://console.aws.amazon.com/cloudwatch/home)のログ情報を確認して問題のトラブルシューティングを行うことができます。

![Troubleshooting](/media/tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## 参照 {#see-also}

-   [AWS DMS を使用して MySQL 互換データベースから移行する](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
-   [AWS DMS をTiDB Cloudクラスターに接続する](/tidb-cloud/tidb-cloud-connect-aws-dms.md)
