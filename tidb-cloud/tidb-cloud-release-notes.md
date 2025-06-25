---
title: TiDB Cloud Release Notes in 2025
summary: 2025 年のTiDB Cloudのリリース ノートについて説明します。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2025年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2025}

このページには、2025 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2025年6月24日 {#june-24-2025}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)データベース監査ログ（ベータ版）がリクエストに応じて利用可能になりました。この機能を使用すると、ユーザーアクセスの詳細（実行されたSQL文など）の履歴をログに記録できます。

    この機能をリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポートをリクエスト」**をクリックします。次に、「説明」フィールドに「 TiDB Cloud Serverless データベース監査ログの申請」と入力し、 **「送信」を**クリックします。

    詳細については[TiDB Cloudサーバーレス データベース監査ログ](/tidb-cloud/serverless-audit-logging.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)ユーザー制御のログ編集をサポートします。

    TiDB Cloud Dedicated クラスターのログ編集を有効または無効にして、クラスター ログの編集ステータスを自分で管理できるようになりました。

    詳細については[ユーザー制御のログ編集](/tidb-cloud/tidb-cloud-log-redaction.md)参照してください。

-   顧客管理の暗号化キー (CMEK) を使用した保存時の暗号化が、AWS でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで一般提供 (GA) されました。

    この機能を使用すると、キー管理サービス (KMS) を通じて管理する対称暗号化キーを活用して、保存中のデータを保護できます。

    詳細については[顧客管理の暗号化キーを使用した保存時の暗号化](/tidb-cloud/tidb-cloud-encrypt-cmek.md)参照してください。

## 2025年6月17日 {#june-17-2025}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの場合、16 vCPU および 32 vCPU を持つ TiKV ノードの最大storageサイズが**6144 GiB**から**4096 GiB**に変更されます。

    詳細については[TiKVノードのstorageサイズ](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)参照してください。

**コンソールの変更**

-   左側のナビゲーション ペインを改良して、全体的なナビゲーション エクスペリエンスを向上させます。

    -   新しい<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" stroke-width="1.5" class="" style="width: calc(1.25rem * var(--mantine-scale)); height: calc(1.25rem * var(--mantine-scale));"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9 3v18M7.8 3h8.4c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C21 5.28 21 6.12 21 7.8v8.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V7.8c0-1.68 0-2.52.327-3.162a3 3 0 0 1 1.311-1.311C5.28 3 6.12 3 7.8 3" stroke-width="inherit"></path></svg>アイコンが左上隅に表示されるようになりました。これにより、必要に応じて左側のナビゲーション ペインを簡単に非表示にしたり表示したりできるようになります。

    -   左上隅にコンボ ボックスが追加され、組織、プロジェクト、クラスターを 1 つの中央の場所からすばやく切り替えることができるようになりました。

        <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/tidb-cloud-combo-box.png" width="200" />

    -   左側のナビゲーション ペインに表示されるエントリは、コンボ ボックスの現在の選択内容に応じて動的に調整されるようになり、最も関連性の高い機能に集中できるようになります。

    -   すぐにアクセスできるように、**サポート**、**通知**、アカウント エントリが、すべてのコンソール ページの左側のナビゲーション ペインの下部に常に表示されるようになりました。

## 2025年6月4日 {#june-4-2025}

**一般的な変更**

-   Microsoft Azure の[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)パブリック プレビューで利用できるようになりました。

    今回のリリースにより、 TiDB Cloud はAWS、Google Cloud、Azure の 3 つの主要なパブリック クラウド プラットフォームすべてをサポートするようになり、ビジネス ニーズとクラウド戦略に最適な場所にTiDB Cloud Dedicated クラスターを展開できるようになりました。

    -   AWS および Google Cloud で利用可能なすべてのコア機能は、Azure で完全にサポートされています。
    -   Azure サポートは現在、米国東部 2、東日本、東南アジアの 3 つのリージョンで利用可能で、近日中にさらに多くのリージョンで利用可能になる予定です。
    -   Azure 上のTiDB Cloud Dedicated クラスターには、TiDB バージョン v7.5.3 以降が必要です。

    Azure でTiDB Cloud Dedicated をすぐに使い始めるには、次のドキュメントを参照してください。

    -   [Azure 上にTiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)
    -   [Azure プライベート エンドポイント経由でTiDB Cloud専用クラスタを接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)
    -   [Azure 上のTiDB Cloud専用クラスタにデータをインポートする](/tidb-cloud/import-csv-files.md)

-   Prometheus 統合により、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの監視機能を強化するためのメトリックがさらに提供されます。

    これで、 `tidbcloud_disk_read_latency`や`tidbcloud_kv_request_duration`などの追加のメトリックを Prometheus に統合して、 TiDB Cloud Dedicated のパフォーマンスのより多くの側面を追跡できるようになりました。

    利用可能なメトリックと、既存ユーザーと新規ユーザーの両方に対してメトリックを有効にする方法の詳細については、 [TiDB Cloud をPrometheus および Grafana と統合する (ベータ版)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)参照してください。

-   TiKV [標準](/tidb-cloud/size-your-cluster.md#standard-storage)および[パフォーマンス](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage)storageの価格が正式に発表されました。

    割引期間は**2025年6月5日 UTC 00:00**に終了します。その後、価格は通常価格に戻ります。TiDB TiDB Cloud Dedicated の価格については、 [TiDB Cloud専用料金の詳細](https://www.pingcap.com/tidb-dedicated-pricing-details/#node-cost)ご覧ください。

**コンソールの変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのTiFlashノードのサイズを構成する際のインタラクティブ エクスペリエンスを強化します。

    TiDB Cloud Dedicated クラスターを作成するときに、トグル スイッチを使用してTiFlash構成を制御できるようになりました。これにより、構成エクスペリエンスがより直感的でシームレスになります。

## 2025年5月27日 {#may-27-2025}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの変更フィードを使用して[アパッチパルサー](https://pulsar.apache.org)へのストリーミング データをサポートします。

    この機能により、 TiDB Cloud Dedicated クラスタをより幅広い下流システムと統合できるようになり、追加のデータ統合要件にも対応できるようになります。この機能を使用するには、 TiDB Cloud Dedicated クラスタのバージョンが v7.5.1 以降であることを確認してください。

    詳細については[アパッチパルサーに沈む](/tidb-cloud/changefeed-sink-to-apache-pulsar.md)参照してください。

## 2025年5月13日 {#may-13-2025}

**一般的な変更**

-   AI アプリケーション向けのフルテキスト検索 (ベータ版) が[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)で利用可能になりました。

    TiDB Cloud Serverlessは、全文検索（ベータ版）をサポートしました。これにより、AIおよび検索拡張生成（RAG）アプリケーションは、正確なキーワードでコンテンツを検索できるようになります。これは、意味的類似性に基づいてコンテンツを検索するベクトル検索を補完するものです。この2つの手法を組み合わせることで、RAGワークフローにおける検索精度と回答品質が大幅に向上します。主な機能は以下のとおりです。

    -   直接テキスト検索: 埋め込みを必要とせずに文字列列を直接クエリします。
    -   多言語サポート: 言語指定を必要とせずに、同じテーブル内でも複数の言語のテキストを自動的に検出して分析します。
    -   関連性に基づくランキング: 関連性を最適にするために、結果は業界標準の BM25 アルゴリズムを使用してランク付けされます。
    -   ネイティブ SQL 互換性: フィルタリング、グループ化、フルテキスト検索との結合などの SQL 機能をシームレスに使用します。

    開始するには、 [SQLによる全文検索](/tidb-cloud/vector-search-full-text-search-sql.md)または[Pythonによる全文検索](/tidb-cloud/vector-search-full-text-search-python.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの最大TiFlashノードstorageを増やします。

    -   8 vCPU TiFlashの場合、2048 GiBから4096 GiB
    -   32 vCPU TiFlashの場合、4096 GiBから8192 GiB

    この機能強化により、 TiDB Cloud Dedicated クラスターの分析データstorage容量が増加し、ワークロードのスケーリング効率が向上し、増大するデータ要件に対応できるようになります。

    詳細については[TiFlashノードstorage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)参照してください。

-   メンテナンス タスクを構成および再スケジュールするための直感的なオプションを提供することで、メンテナンス ウィンドウの構成エクスペリエンスを強化します。

    詳細については[メンテナンスウィンドウを構成する](/tidb-cloud/configure-maintenance-window.md)参照してください。

-   TiKV [標準](/tidb-cloud/size-your-cluster.md#standard-storage)および[パフォーマンス](/tidb-cloud/size-your-cluster.md#performance-and-plus-storage)storageタイプの割引期間を延長します。プロモーションは2025年6月5日に終了します。この日以降は、価格が標準料金に戻ります。

**コンソールの変更**

-   **バックアップ設定**ページのレイアウトを調整して、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのバックアップ構成エクスペリエンスを向上させます。

    詳細については[TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

## 2025年4月22日 {#april-22-2025}

**一般的な変更**

-   Alibaba Cloud OSS へのデータエクスポートがサポートされるようになりました。

    [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターは、 [アクセスキーペア](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair)使用して[Alibaba Cloud オブジェクト ストレージ サービス (OSS)](https://www.alibabacloud.com/en/product/object-storage-service)にデータをエクスポートできるようになりました。

    詳細については[TiDB Cloud Serverlessからデータをエクスポート](/tidb-cloud/serverless-export.md#alibaba-cloud-oss)参照してください。

## 2025年4月15日 {#april-15-2025}

**一般的な変更**

-   [Alibaba Cloud オブジェクト ストレージ サービス (OSS)](https://www.alibabacloud.com/en/product/object-storage-service)クラスターから[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターへのデータのインポートをサポートします。

    この機能により、 TiDB Cloud Serverlessへのデータ移行が簡素化されます。認証にはAccessKeyペアを使用できます。

    詳細については、次のドキュメントを参照してください。

    -   [Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud OSS から CSV ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-csv-files-serverless.md)
    -   [Amazon S3、GCS、Azure Blob Storage、または Alibaba Cloud OSS から Apache Parquet ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-parquet-files-serverless.md)

## 2025年4月1日 {#april-1-2025}

**一般的な変更**

-   [TiDB ノードグループ](/tidb-cloud/tidb-node-group-overview.md)機能が、AWS と Google Cloud でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで一般提供 (GA) されました。

    この機能により、単一クラスター内での**きめ細かなコンピューティング リソースの分離**が可能になり、マルチテナントまたはマルチワークロードのシナリオでパフォーマンスとリソース割り当てを最適化できます。

    **主な利点:**

    -   **リソースの分離**:

        -   TiDB ノードを論理的に分離されたユニットにグループ化し、1 つのグループのワークロードが他のグループに影響を与えないようにします。
        -   アプリケーションまたはビジネス ユニット間のリソース競合を防止します。

    -   **簡素化された管理**：

        -   すべてのノード グループを単一のクラスター内で管理し、運用オーバーヘッドを削減します。
        -   需要に応じてグループを個別にスケールします。

    メリットの詳細については[技術ブログ](https://www.pingcap.com/blog/tidb-cloud-node-groups-scaling-workloads-predictable-performance/)ご覧ください。開始するには[TiDBノードグループの管理](/tidb-cloud/tidb-node-group-management.md)ご覧ください。

-   AWS でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスター内の TiKV ノードに[標準storage](/tidb-cloud/size-your-cluster.md#standard-storage)タイプを導入します。

    標準storageタイプは、パフォーマンスとコスト効率のバランスが取れているため、ほとんどのワークロードに最適です。

    **主な利点:**

    -   **パフォーマンスの向上**: Raftログに十分なディスク リソースを予約し、 Raftとデータstorage間の I/O 競合を減らして、TiKV の読み取りと書き込みのパフォーマンスを向上させます。
    -   **強化された安定性**: 重要なRaft操作をデータ ワークロードから分離し、より予測可能なパフォーマンスを確保します。
    -   **コスト効率**: 従来のstorageタイプと比較して、競争力のある価格でより高いパフォーマンスを実現します。

    **可用性：**

    標準storageタイプは、2025年4月1日以降に作成され、AWSでホストされ、サポート対象バージョン（バージョン7.5.5、8.1.2、または8.5.0以上）の新規クラスター[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)に自動的に適用されます。既存のクラスターは引き続き以前の[基本的なstorage](/tidb-cloud/size-your-cluster.md#basic-storage)タイプを使用しているため、移行は不要です。

    スタンダードstorageの料金はベーシックstorageの料金と異なります。詳しくは[価格](https://www.pingcap.com/tidb-dedicated-pricing-details/)ご覧ください。

## 2025年3月25日 {#march-25-2025}

**コンソールの変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスター内のパブリック エンドポイントのファイアウォール ルールをサポートします。

    TiDB Cloud Serverless クラスターのファイアウォールルールを設定して、パブリックエンドポイント経由のアクセスを制御できるようになりました[TiDB Cloudコンソール](https://tidbcloud.com/)で許可する IP アドレスまたは範囲を直接指定することで、セキュリティを強化できます。

    詳細については[パブリックエンドポイント用のTiDB Cloudサーバーレス ファイアウォール ルールを構成する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)参照してください。

## 2025年3月18日 {#march-18-2025}

**一般的な変更**

-   リソース管理の柔軟性を高めるために、Google Cloud にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに対して TiDB ノード グループの作成をサポートします。

    詳細については[TiDBノードグループの概要](/tidb-cloud/tidb-node-group-overview.md)参照してください。

-   AWS にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのTiDB Cloudにデータベース監査ログ ファイルを保存することをサポートします。

    これらの監査ログファイルはTiDB Cloudから直接ダウンロードできます。この機能はリクエストに応じてのみ利用可能であることにご注意ください。

    詳細については[データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)参照してください。

-   多要素認証（MFA）の管理を改善することで、 TiDB Cloudアカウントのセキュリティを強化します。この機能は、 TiDB Cloudのパスワードベースのログインに適用されます。

    詳細については[パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)参照してください。

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

    TiDB Cloud Serverless は、Google Cloud Storage (GCS) および Azure Blob Storage からのデータのインポートをサポートするようになりました。認証には、Google Cloud サービス アカウント キーまたは Azure Shared Access Signature (SAS) トークンを使用できます。この機能により、 TiDB Cloud Serverless へのデータ移行が簡素化されます。

    詳細については、 [Amazon S3、GCS、Azure Blob Storage から CSV ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-csv-files-serverless.md)および[Amazon S3、GCS、または Azure Blob Storage から Apache Parquet ファイルをTiDB Cloud Serverless にインポートする](/tidb-cloud/import-parquet-files-serverless.md)参照してください。

## 2025年1月21日 {#january-21-2025}

**コンソールの変更**

-   タスクあたり最大 250 MiB の単一のローカル CSV ファイルを[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターにインポートできるようになりました。これは、以前の 50 MiB の制限から増加されました。

    詳細については[ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)参照してください。

## 2025年1月14日 {#january-14-2025}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい AWS リージョンをサポートします: `Jakarta (ap-southeast-3)` 。

-   通知機能を導入すると、 [TiDB Cloudコンソール](https://tidbcloud.com/)を通じてTiDB Cloud の更新とアラートに関する最新情報を即座に入手できます。

    詳細については[通知](/tidb-cloud/notifications.md)参照してください。

## 2025年1月2日 {#january-2-2025}

**一般的な変更**

-   リソース管理の柔軟性を高めるために、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの TiDB ノード グループの作成をサポートします。

    詳細については[TiDBノードグループの概要](/tidb-cloud/tidb-node-group-overview.md)参照してください。

-   Private Connect (ベータ版) を介して[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターを AWS および Google Cloud の汎用 Kafka に接続することをサポートします。

    Private Connect は、クラウドプロバイダーの Private Link または Private Service Connect テクノロジーを活用し、 TiDB Cloud VPC 内の変更フィードがプライベート IP アドレスを使用してお客様の VPC 内の Kafka に接続できるようにします。これにより、Kafka がTiDB Cloud VPC 内で直接ホストされているかのように扱われます。この機能は、VPC CIDR の競合を防ぎ、セキュリティコンプライアンス要件を満たすのに役立ちます。

    -   AWS の Apache Kafka の場合は、 [AWS でセルフホスト型 Kafka プライベートリンク サービスをセットアップする](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md)手順に従ってネットワーク接続を構成します。

    -   Google Cloud の Apache Kafka の場合は、 [Google Cloud でセルフホスト型 Kafka プライベート サービス接続を設定する](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md)手順に従ってネットワーク接続を構成します。

    この機能を使用すると、追加の[プライベートデータリンクのコスト](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md#private-data-link-cost)が発生することに注意してください。

    詳細については[Apache Kafka への Changefeed シンク](/tidb-cloud/changefeed-sink-to-apache-kafka.md#network)参照してください。

-   Kafka の変更フィードに追加の構成可能なオプションを導入します。

    -   Debeziumプロトコルの使用をサポートします。Debeziumはデータベースの変更をキャプチャするためのツールです。キャプチャされたデータベースの変更はイベントと呼ばれるメッセージに変換され、Kafkaに送信されます。詳細については、 [TiCDC デベジウムプロトコル](https://docs.pingcap.com/tidb/v8.1/ticdc-debezium)ご覧ください。

    -   すべてのテーブルに対して単一のパーティション ディスパッチャーを定義することも、異なるテーブルに対して異なるパーティション ディスパッチャーを定義することもサポートします。

    -   Kafka メッセージのパーティション分散用に、タイムスタンプと列値という 2 つの新しいディスパッチャ タイプを導入しました。

    詳細については[Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)参照してください。

-   TiDB Cloudでの役割の強化:

    -   TiDB Cloudでのきめ細かなアクセス制御を強化するために、ロール`Project Viewer`と`Organization Billing Viewer`導入します。

    -   次のロールの名前を変更します。

        -   `Organization Member`から`Organization Viewer`
        -   `Organization Billing Admin`から`Organization Billing Manager`
        -   `Organization Console Audit Admin`から`Organization Console Audit Manager`

    詳細については[アイデンティティアクセス管理](/tidb-cloud/manage-user-access.md#organization-roles)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのリージョン高可用性 (ベータ版)。

    この機能は、最大限のインフラストラクチャ冗長性とビジネス継続性を必要とするワークロード向けに設計されています。主な関数は次のとおりです。

    -   ノードは複数の可用性ゾーンに分散され、ゾーン障害が発生した場合でも高可用性が確保されます。
    -   PD や TiKV などの重要な OLTP (オンライン トランザクション処理) コンポーネントは、冗長性を確保するために可用性ゾーン全体に複製されます。
    -   自動フェイルオーバーにより、プライマリ ゾーンの障害時のサービス中断が最小限に抑えられます。

    この機能は現在、AWS 東京 (ap-northeast-1) リージョンでのみ利用可能で、クラスターの作成時にのみ有効にできます。

    詳細については[TiDB Cloud Serverless の高可用性](/tidb-cloud/serverless-high-availability.md)参照してください。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン8.1.1](https://docs.pingcap.com/tidb/v8.1/release-8.1.1)から[バージョン8.1.2](https://docs.pingcap.com/tidb/v8.1/release-8.1.2)にアップグレードします。

**コンソールの変更**

-   データエクスポートサービスの強化:

    -   [TiDB Cloudコンソール](https://tidbcloud.com/)を介して[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)から Google Cloud Storage および Azure Blob Storage へのデータのエクスポートをサポートします。

    -   [TiDB Cloudコンソール](https://tidbcloud.com/)を介して Parquet ファイルでのデータのエクスポートをサポートします。

    詳細については、 [TiDB Cloud Serverlessからデータをエクスポート](/tidb-cloud/serverless-export.md)および[TiDB Cloud Serverless の外部ストレージアクセスを構成する](/tidb-cloud/serverless-external-storage.md)参照してください。
