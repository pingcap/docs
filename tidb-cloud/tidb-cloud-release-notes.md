---
title: TiDB Cloud Release Notes in 2025
summary: 2025 年のTiDB Cloudのリリース ノートについて説明します。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2025 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2025}

このページには、2025 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2025年2月18日 {#february-18-2025}

**コンソールの変更**

-   TiDB Cloudの新しいサポート サービスである Connected Care を紹介します。

    Connected Care サービスは、最新のコミュニケーション ツール、プロアクティブなサポート、高度な AI 機能を通じてTiDB Cloudとの接続を強化し、シームレスで顧客中心のエクスペリエンスを実現するように設計されています。

    Connected Care サービスでは、次の機能が導入されています。

    -   **クリニック サービス**: パフォーマンスを最適化するための高度な監視と診断。
    -   **IM での AI チャット**: インスタント メッセージ (IM) ツールを通じて AI による即時サポートを受けることができます。
    -   **アラートとチケット更新の IM サブスクリプション**: IM 経由でアラートとチケットの進行状況に関する最新情報を入手します。
    -   **サポート チケットの IM 対話**: IM ツールを使用してサポート チケットを作成し、対話します。

    詳細については[コネクテッドケアの概要](/tidb-cloud/connected-care-overview.md)参照してください。

-   GCS および Azure Blob Storage から[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターへのデータのインポートをサポートします。

    TiDB Cloud Serverless は、Google Cloud Storage (GCS) および Azure Blob Storage からのデータのインポートをサポートするようになりました。認証には、Google Cloud サービス アカウント キーまたは Azure 共有アクセス署名 (SAS) トークンを使用できます。この機能により、 TiDB Cloud Serverless へのデータ移行が簡素化されます。

    詳細については[Amazon S3、GCS、または Azure Blob ストレージから CSV ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-csv-files-serverless.md)および[Amazon S3、GCS、または Azure Blob ストレージから Apache Parquet ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-parquet-files-serverless.md)参照してください。

## 2025年1月21日 {#january-21-2025}

**コンソールの変更**

-   タスクあたり最大 250 MiB の単一のローカル CSV ファイルを[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターにインポートできるようになりました。以前の制限である 50 MiB から増加されました。

    詳細については[ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)参照してください。

## 2025年1月14日 {#january-14-2025}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい AWS リージョンをサポートします: `Jakarta (ap-southeast-3)` 。

-   [通知](https://tidbcloud.com/console/notifications)機能を導入すると、 [TiDB Cloudコンソール](https://tidbcloud.com/)を通じてTiDB Cloud の更新とアラートを即座に把握できるようになります。

    詳細については[通知](/tidb-cloud/notifications.md)参照してください。

## 2025年1月2日 {#january-2-2025}

**一般的な変更**

-   リソース管理の柔軟性を高めるために、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの TiDB ノード グループの作成をサポートします。

    詳細については[TiDBノードグループの概要](/tidb-cloud/tidb-node-group-overview.md)参照してください。

-   Private Connect (ベータ版) を介して[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを AWS および Google Cloud の汎用 Kafka に接続することをサポートします。

    Private Connect は、クラウド プロバイダーの Private Link または Private Service Connect テクノロジーを活用して、 TiDB Cloud VPC 内の変更フィードがプライベート IP アドレスを使用して顧客の VPC 内の Kafka に接続できるようにします。これにより、それらの Kafka がTiDB Cloud VPC 内で直接ホストされているかのようになります。この機能は、VPC CIDR の競合を防ぎ、セキュリティ コンプライアンス要件を満たすのに役立ちます。

    -   AWS の Apache Kafka の場合は、 [AWS でセルフホスト型 Kafka プライベートリンク サービスをセットアップする](/tidb-cloud/setup-self-hosted-kafka-private-link-service.md)手順に従ってネットワーク接続を構成します。

    -   Google Cloud の Apache Kafka の場合は、 [Google Cloud でセルフホスト型 Kafka プライベート サービス接続を設定する](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)手順に従ってネットワーク接続を構成します。

    この機能を使用すると、追加の[プライベートデータリンクのコスト](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)が発生することに注意してください。

    詳細については[Apache Kafka への Changefeed シンク](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)参照してください。

-   Kafka の変更フィードに追加の構成可能なオプションを導入します。

    -   Debezium プロトコルの使用をサポートします。Debezium はデータベースの変更をキャプチャするためのツールです。キャプチャされたデータベースの変更をイベントと呼ばれるメッセージに変換し、これらのイベントを Kafka に送信します。詳細については、 [TiCDC デベジウム プロトコル](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)参照してください。

    -   すべてのテーブルに対して単一のパーティション ディスパッチャーを定義することも、テーブルごとに異なるパーティション ディスパッチャーを定義することもサポートします。

    -   Kafka メッセージのパーティション分散用に、タイムスタンプと列値という 2 つの新しいディスパッチャ タイプを導入しました。

    詳細については[Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)参照してください。

-   TiDB Cloudでの役割の強化:

    -   TiDB Cloudでのきめ細かなアクセス制御を強化するために、ロール`Project Viewer`と`Organization Billing Viewer`導入します。

    -   次のロールの名前を変更します。

        -   `Organization Member`から`Organization Viewer`
        -   `Organization Billing Admin`から`Organization Billing Manager`
        -   `Organization Console Audit Admin`から`Organization Console Audit Manager`

    詳細については[アイデンティティアクセス管理](/tidb-cloud/manage-user-access.md#organization-roles)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの地域高可用性 (ベータ版)。

    この機能は、最大限のインフラストラクチャ冗長性とビジネス継続性を必要とするワークロード向けに設計されています。主な関数は次のとおりです。

    -   ゾーン障害が発生した場合でも高可用性を確保するために、ノードは複数の可用性ゾーンに分散されます。
    -   PD や TiKV などの重要な OLTP (オンライン トランザクション処理) コンポーネントは、冗長性を確保するために可用性ゾーン全体に複製されます。
    -   自動フェイルオーバーにより、プライマリ ゾーンの障害発生時のサービス中断が最小限に抑えられます。

    この機能は現在、AWS 東京 (ap-northeast-1) リージョンでのみ利用可能で、クラスターの作成時にのみ有効にできます。

    詳細については[TiDB Cloud Serverless の高可用性](/tidb-cloud/serverless-high-availability.md)参照してください。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1)から[バージョン8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)にアップグレードします。

**コンソールの変更**

-   データエクスポートサービスの強化:

    -   [TiDB Cloudコンソール](https://tidbcloud.com/)を介して[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)から Google Cloud Storage および Azure Blob Storage へのデータのエクスポートをサポートします。

    -   [TiDB Cloudコンソール](https://tidbcloud.com/)を介して Parquet ファイルでのデータのエクスポートをサポートします。

    詳細については[TiDB Cloud Serverless からデータをエクスポート](/tidb-cloud/serverless-export.md)および[TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md)参照してください。
