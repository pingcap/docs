---
title: Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection
summary: Alibaba Cloud Endpoint Service プライベートリンク接続を使用して Alibaba Cloud ApsaraDB RDS for MySQL インスタンスに接続する方法を学習します。
---

# プライベートリンク接続を介して Alibaba Cloud ApsaraDB RDS for MySQL に接続する {#connect-to-alibaba-cloud-apsaradb-rds-for-mysql-via-a-private-link-connection}

このドキュメントでは、 [Alibaba Cloud Endpoint Service プライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md)を使用してTiDB Cloud Essential クラスターを[Alibaba Cloud ApsaraDB RDS for MySQL](https://www.alibabacloud.com/en/product/apsaradb-for-rds-mysql)インスタンスに接続する方法について説明します。

## 前提条件 {#prerequisites}

-   既存の ApsaraDB RDS for MySQL インスタンスがあるか、インスタンスを作成するために必要な権限があります。

-   アカウントにネットワーク コンポーネントを管理するための次の権限があることを確認します。

    -   ロードバランサーの管理
    -   エンドポイントサービスの管理

-   TiDB Cloud Essential クラスターは Alibaba Cloud 上に存在し、アクティブです。後で使用するために、以下の詳細情報を取得して保存してください。

    -   Alibaba CloudアカウントID
    -   可用性ゾーン（AZ）

Alibaba Cloud アカウント ID とアベイラビリティーゾーンを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。
2.  **[データフローのプライベート リンク接続]**領域で、 **[プライベート リンク接続の作成] を**クリックします。
3.  表示されたダイアログで、Alibaba Cloud アカウント ID とアベイラビリティーゾーンを見つけることができます。

## ステップ1. ApsaraDB RDS for MySQLインスタンスをセットアップする {#step-1-set-up-an-apsaradb-rds-for-mysql-instance}

使用する Alibaba Cloud ApsaraDB RDS for MySQL を特定するか、 [新しいRDSを作成する](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/step-1-create-an-apsaradb-rds-for-mysql-instance-and-configure-databases) 。

ApsaraDB RDS for MySQL インスタンスは次の要件を満たしている必要があります。

-   リージョンの一致: インスタンスは、 TiDB Cloud Essential クラスターと同じ Alibaba Cloud リージョンに存在する必要があります。
-   AZ (アベイラビリティ ゾーン) の可用性: アベイラビリティ ゾーンは、 TiDB Cloud Essential クラスターのアベイラビリティ ゾーンと重複する必要があります。
-   ネットワークのアクセシビリティ: インスタンスは適切な IP 許可リストで構成され、VPC 内でアクセス可能である必要があります。

> **注記**
>
> ApsaraDB RDS for MySQL のリージョン間接続はサポートされていません。

## ステップ2. ApsaraDB RDS for MySQLインスタンスをエンドポイントサービスとして公開する {#step-2-expose-the-apsaradb-rds-for-mysql-instance-as-an-endpoint-service}

Alibaba Cloud コンソールでロードバランサーとエンドポイント サービスを設定する必要があります。

### ステップ2.1. ロードバランサーを設定する {#step-2-1-set-up-the-load-balancer}

次のように、ApsaraDB RDS for MySQL と同じリージョンにロードバランサーを設定します。

1.  [サーバーグループ](https://slb.console.alibabacloud.com/nlb/ap-southeast-1/server-groups)に進み、サーバーグループを作成します。以下の情報を入力してください。

    -   **サーバーグループタイプ**: `IP`を選択
    -   **VPC** : ApsaraDB RDS for MySQL が配置されている VPC を入力します。
    -   **バックエンドサーバープロトコル**: `TCP`を選択

2.  作成されたサーバーグループをクリックしてバックエンド サーバーを追加し、ApsaraDB RDS for MySQL インスタンスの IP アドレスを追加します。

    RDS エンドポイントに ping を実行して IP アドレスを取得できます。

3.  [ナショナルリーグ](https://slb.console.alibabacloud.com/nlb)に進み、ネットワークロードバランサーを作成します。以下の情報を入力してください。

    -   **ネットワークタイプ**: `Internal-facing`を選択
    -   **VPC** : ApsaraDB RDS for MySQL が配置されている VPC を選択します。
    -   **ゾーン**: TiDB Cloud Essential クラスタと重複する必要があります
    -   **IPバージョン**: `IPv4`を選択

4.  作成したロードバランサーを見つけて、 **「リスナーの作成」**をクリックします。以下の情報を入力します。

    -   **リスナープロトコル**: `TCP`を選択
    -   **リスナーポート**: データベースポートを入力します。例: MySQLの場合は`3306`
    -   **サーバーグループ**: 前の手順で作成したサーバーグループを選択します

### ステップ2.2. エンドポイントサービスを設定する {#step-2-2-set-up-an-endpoint-service}

ApsaraDB RDS for MySQL と同じリージョンにエンドポイント サービスを設定するには、次の手順を実行します。

1.  エンドポイントサービスを作成するには、 [エンドポイントサービス](https://vpc.console.alibabacloud.com/endpointservice)に進んでください。以下の情報を入力してください。

    -   **サービスリソースタイプ**: `NLB`選択
    -   **サービス リソースの選択**: NLB が含まれるすべてのゾーンを選択し、前の手順で作成した NLB を選択します。
    -   **エンドポイント接続を自動的に受け入れる**: `No`選択することをお勧めします

2.  エンドポイントサービスの詳細ページに移動し、**エンドポイントサービス名**（例： `com.aliyuncs.privatelink.<region>.xxxxx` ）をコピーします。これは後でTiDB Cloudで使用する必要があります。

3.  エンドポイントサービスの詳細ページで、「**サービスホワイトリスト」**タブをクリックし、 **「ホワイトリストに追加」**をクリックして、 [前提条件](#prerequisites)で取得したAlibaba CloudアカウントIDを入力します。

## ステップ3. TiDB Cloudでプライベートリンク接続を作成する {#step-3-create-a-private-link-connection-in-tidb-cloud}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用してプライベート リンク接続を作成できます。

詳細については[Alibaba Cloud Endpoint Service のプライベートリンク接続を作成する](/tidb-cloud/serverless-private-link-connection.md#create-an-alibaba-cloud-endpoint-service-private-link-connection)参照してください。
