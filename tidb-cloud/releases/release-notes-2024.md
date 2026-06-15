---
title: TiDB Cloud Release Notes in 2024
summary: TiDB Cloudの2024年のリリースノートについてご確認ください。
---

# TiDB Cloud 2024年リリースノート {#tidb-cloud-release-notes-in-2024}

このページには、2024年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリースノートが掲載されています。

## 2024年12月17日 {#december-17-2024}

**全般的な変更**

-   TiDB Cloud Serverlessのバックアップと変更の復元

    -   新しいクラスターへのデータ復元をサポートすることで、柔軟性が向上し、現在のクラスターの運用が中断されないことが保証されます。

    -   クラスター計画に合わせてバックアップと復元の戦略を調整します。詳細については、 [TiDB Cloud Serverless データのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md#learn-about-the-backup-setting)参照してください。

    -   スムーズな移行を支援するために、以下の互換性ポリシーを適用してください。

        -   2024年12月17日10:00:00（UTC）より前に作成されたバックアップは、すべてのクラスターにおいて以前の保持期間に従います。
        -   スケーラブルなクラスターのバックアップ時間は現在の構成を維持しますが、フリークラスターのバックアップ時間はデフォルト設定にリセットされます。

## 2024年12月3日 {#december-3-2024}

**全般的な変更**

-   AWS上にデプロイされた[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのディザスタリカバリのためのリカバリグループ機能（ベータ版）を導入します。

    この機能を使用すると、TiDB Cloud Dedicatedクラスター間でデータベースを複製できるため、地域的な災害が発生した場合でも迅速なリカバリが可能になります。プロジェクト オーナーの役割をお持ちの場合は、新しいリカバリグループを作成し、データベースをそのグループに割り当てることで、この機能を有効にできます。リカバリグループを使用してデータベースを複製することで、災害対策を強化し、より厳格な可用性 SLA を満たし、より積極的なリカバリ ポイント オブ パーセンテージ (RPO) およびリカバリ 時間 オブ パーセンテージ (RTO) を実現できます。

## 2024年11月26日 {#november-26-2024}

**全般的な変更**

-   新しい[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[v7.5.4](https://docs.pingcap.com/tidb/stable/release-7.5.4)から[v8.1.1](https://docs.pingcap.com/tidb/stable/release-8.1.1)にアップグレードします。

-   [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)以下のシナリオにおいて、大規模データ書き込みのコストを最大80%削減します。

    -   [自動コミットモード](/transaction-overview.md#autocommit)で 16 MiB を超える書き込み操作を実行したとき。
    -   [楽観的トランザクションモデル](/optimistic-transaction.md)で16 MiBを超える書き込み操作を実行した場合。
    -   [TiDB Cloudにデータをインポートする](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)とき。

    この改善により、データ運用の効率性とコスト効率が向上し、ワークロードの規模が拡大するにつれて、より大きなコスト削減効果が得られます。

## 2024年11月19日 {#november-19-2024}

**全般的な変更**

-   [TiDB Cloudのサーバーレスブランチ機能（ベータ版）](/tidb-cloud/branch-overview.md)では、ブランチ管理に次の改善が導入されています。

    -   **柔軟なブランチ作成**：ブランチを作成する際、特定のクラスターまたはブランチを親として選択し、親から使用する正確な時点を指定できます。これにより、ブランチ内のデータを正確に制御できます。

    -   **ブランチのリセット**：ブランチをリセットして、親ブランチの最新の状態と同期させることができます。

    -   **GitHubとの連携機能の改善**： [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)GitHubアプリでは`reset`プルリクエストの同期時の動作を制御する[`branch.mode`](/tidb-cloud/branch-github-integration.md#branchmode)パラメータが導入されました。デフォルトモードでは、アプリはプルリクエストの最新の変更に合わせてブランチをリセットします。

    詳細については、 [TiDB Cloud Serverless Branchs の管理](/tidb-cloud/branch-manage.md)および[TiDB Cloud Serverless Branching (ベータ版) を GitHub と統合する](/tidb-cloud/branch-github-integration.md)参照してください。

## 2024年11月12日 {#november-12-2024}

**全般的な変更**

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの一時停止時間制限を追加します。

    TiDB Cloud Dedicatedでは、最大一時停止期間が7日間に制限されました。7日以内に手動でクラスターを再開しない場合、 TiDB Cloudが自動的に再開します。

    この変更は**、2024年11月12日以降に作成された組織**にのみ適用されます。この日付以前に作成された組織は、事前通知の上、段階的に新しい一時停止動作に移行します。

    詳細については、[TiDB Cloud Dedicatedクラスタの一時停止または再開](/tidb-cloud/pause-or-resume-tidb-cluster.md)を参照してください。

-   [Datadogとの連携（ベータ版）](/tidb-cloud/monitor-datadog-integration.md)では、新しいリージョン`AP1` (日本) のサポートが追加されました。

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスター向けに新しい AWS リージョンをサポートします: `Mumbai (ap-south-1)` 。

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの AWS `São Paulo (sa-east-1)`リージョンのサポートを削除します。

## 2024年10月29日 {#october-29-2024}

**全般的な変更**

-   新しいメトリック: Prometheus との統合のために`tidbcloud_changefeed_checkpoint_ts`を追加します。

    このメトリックは、変更フィードのチェックポイント タイムスタンプを追跡し、ダウンストリームに正常に書き込まれた最大の TSO (Timestamp Oracle) を表します。利用可能なメトリクスの詳細については、 [TiDB CloudとPrometheusおよびGrafanaの統合（ベータ版）](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)を参照してください。

## 2024年10月22日 {#october-22-2024}

**全般的な変更**

-   新しい[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[v7.5.3](https://docs.pingcap.com/tidb/stable/release-7.5.3)から[v7.5.4](https://docs.pingcap.com/tidb/stable/release-7.5.4)にアップグレードします。

## 2024年10月15日 {#october-15-2024}

**APIの変更**

-   [MSP](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)は2024年10月15日をもって非推奨となり、今後削除される予定です。現在MSP APIをご利用の場合は、 [TiDB Cloudパートナー](https://partner-console.tidbcloud.com/signin)のパートナー管理APIに移行してください。

## 2024年9月24日 {#september-24-2024}

**全般的な変更**

-   AWS でホストされている[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに新しい[TiFlashのvCPUとRAMサイズ](/tidb-cloud/size-your-cluster.md#tiflash-vcpu-and-ram)を指定します: `32 vCPU, 128 GiB`

**CLIの変更**

-   [TiDB Cloud CLI v1.0.0-beta.2](https://github.com/tidbcloud/tidbcloud-cli/releases/tag/v1.0.0-beta.2)をリリースしました。

    TiDB Cloud CLIには、以下の新機能が追加されました。

    -   [`ticloud serverless sql-user`](/tidb-cloud/ticloud-serverless-sql-user-create.md)を介して、 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)クラスターの SQL ユーザー管理をサポートします。
    -   [`ticloud serverless create`](/tidb-cloud/ticloud-cluster-create.md)および[`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md)で、 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)クラスターのパブリック エンドポイントを無効にできるようにします。
    -   OAuth認証を使用する際に、現在のユーザーに関する情報を取得するには、 [`ticloud auth whoami`](/tidb-cloud/ticloud-auth-whoami.md)コマンドを追加してください。
    -   [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)で`--sql` 、 `--where` 、および`--filter`フラグをサポートし、ソース テーブルを柔軟に選択できるようにします。
    -   CSVファイルおよびParquetファイルへのデータエクスポートをサポートします。
    -   ロールARNを認証情報として使用してAmazon S3にデータをエクスポートする機能をサポートするとともに、Google Cloud StorageおよびAzure Blob Storageへのエクスポートもサポートします。
    -   Amazon S3、Google Cloud Storage、Azure Blob Storageからのデータインポートをサポートします。
    -   ブランチと特定のタイムスタンプから新しいブランチを作成する機能をサポートします。

    TiDB Cloud CLIは、以下の機能を強化します。

    -   デバッグログ機能を改善しました。認証情報とユーザーエージェントをログに記録できるようになりました。
    -   ローカルエクスポートファイルのダウンロード速度を、毎秒数十キロバイトから毎秒数十ミリバイトに高速化します。

    TiDB Cloud CLI では、以下の機能が置き換えられるか、削除されます。

    -   [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)では、 `--s3.bucket-uri`フラグが`--s3.uri`に置き換えられます。
    -   [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)では、 `--database`および`--table`フラグが削除されました。代わりに、 `--sql` 、 `--where` 、および`--filter`フラグを使用できます。
    -   [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md) 、アノテーション フィールドを更新できなくなりました。

## 2024年9月10日 {#september-10-2024}

**全般的な変更**

-   TiDB Cloudパートナー向けのリソースおよび請求管理を強化するため、 TiDB CloudパートナーWebコンソールとオープンAPIをリリースしました。

    AWS Marketplace Channel Partner Private Offer (CPPO) を通じてマネージド サービス プロバイダー (MSP) と再販業者は[TiDB CloudパートナーWebコンソール](https://partner-console.tidbcloud.com/)とオープン API を活用して日常業務を合理化できるようになりました。

    詳細については、 [TiDB CloudパートナーWebコンソール](/tidb-cloud/tidb-cloud-partners.md)を参照してください。

## 2024年9月3日 {#september-3-2024}

**コンソールの変更**

-   TiDB Cloud [TiDB Cloudコンソール](https://tidbcloud.com/)Cloud Serverlessクラスターからのデータのエクスポートをサポートします。

    以前は、 TiDB Cloud は[TiDB Cloud CLI](/tidb-cloud/cli-reference.md)を使用したデータエクスポートのみをサポートしていました。今後は、 [TiDB Cloudコンソール](https://tidbcloud.com/)TiDB Cloud Serverless クラスターからローカルファイルや Amazon S3 へ簡単にデータをエクスポートできます。

    詳細については、 [TiDB Cloud Serverless からデータをエクスポート](/tidb-cloud/serverless-export.md)[TiDB Cloud Serverless の外部ストレージアクセスを構成する](/tidb-cloud/configure-external-storage-access.md)参照してください。

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの接続エクスペリエンスを向上させます。

    -   TiDB Cloud Dedicatedユーザーがよりスムーズで効率的な接続体験を得られるよう、**接続**ダイアログのインターフェースを改訂します。
    -   クラスターのネットワーク設定を簡素化するために、新しいクラスターレベルの**ネットワーク設定**ページを導入しました。
    -   **Security設定**ページを新しい**パスワード設定**ページに置き換え、IPアクセスリストの設定を新しい**ネットワーク**ページに移動します。

    詳細については、 [TiDB Cloud Dedicatedに接続します](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

-   [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデータインポートエクスペリエンスを向上させます。

    -   **インポート**ページのレイアウトをより分かりやすいものに改善する。
    -   TiDB Cloud Serverless クラスターとTiDB Cloud Dedicatedクラスターのインポート手順を統一します。
    -   AWSロールARNの作成プロセスを簡素化し、接続設定を容易にします。

    詳細については、 [ファイルからデータをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)参照してください。

## 2024年8月20日 {#august-20-2024}

**コンソールの変更**

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで新しいプライベートエンドポイント接続を作成する際のユーザーエクスペリエンスを向上させるため、 **「プライベートエンドポイント接続の作成」**ページのレイアウトを改良します。

    詳細については、 [AWSのプライベートエンドポイントを介してTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)および[Google Cloud Private Service Connect を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

## 2024年8月6日 {#august-6-2024}

**全般的な変更**

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) AWS上でのロードバランシングに関する課金体系の変更。

    2024 年 8 月 1 日以降、 TiDB Cloud Dedicated の請求書には、AWS [AWSの料金改定は2024年2月1日から適用されます。](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)各パブリック IPv4 アドレスの料金は 1 時間あたり 0.005 ドルで、これは AWS でホストされるTiDB Cloud Dedicatedクラスターごとに月額約 10 ドルになります。

    この料金は、お客様の既存の**TiDB Cloud Dedicated - Data Transfer - Load Balancing**サービスの下に表示されます。 [請求明細](/tidb-cloud/tidb-cloud-billing.md#billing-details)。

-   新しい[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[v7.5.2](https://docs.pingcap.com/tidb/stable/release-7.5.2)から[v7.5.3](https://docs.pingcap.com/tidb/stable/release-7.5.3)にアップグレードします。

**コンソールの変更**

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスタサイズ構成エクスペリエンスを向上させます。

    TiDB Cloud Dedicatedクラスターの [**クラスタを作成する**](/tidb-cloud/create-tidb-cluster.md)ページと「クラスター [**クラスタの変更**](/tidb-cloud/scale-tidb-cluster.md)ページの**「クラスタサイズ」**セクションのレイアウトを調整します。さらに、 **「クラスタサイズ」**セクションには、適切なクラスター サイズの選択に役立つノード サイズの推奨ドキュメントへのリンクが含まれるようになりました。

## 2024年7月23日 {#july-23-2024}

**全般的な変更**

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service)ベクトル検索エンドポイントの自動生成をサポートしています。

    テーブルに が含まれている場合、選択した距離関数に基づいてベクトル距離を計算する [ベクトルデータ型](/ai/reference/vector-search-data-types.md)検索エンドポイントを自動的に生成できます。

    この機能により[ダイファイ](https://dify.ai/)や[GPT](https://openai.com/blog/introducing-gpts)などのAIプラットフォームとのシームレスな統合が可能になり、高度な自然言語処理とAI機能を活用して、より複雑なタスクやインテリジェントなソリューションに対応できるアプリケーションを構築できます。

    詳細については、 [エンドポイントを自動的に生成する](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)および[データアプリをサードパーティツールと統合する](/tidb-cloud/data-service-integrations.md)参照してください。

-   TiDB Cloudの実際のコストを計画された支出と比較して追跡し、予期せぬコストの発生を防ぐのに役立つ予算機能を導入します。

    この機能にアクセスするには、組織内で`Organization Owner`または`Organization Billing Admin`の役割を担っている必要があります。

    詳細については、 [TiDB Cloudの予算を管理する](/tidb-cloud/tidb-cloud-budget.md)参照してください。

## 2024年7月9日 {#july-9-2024}

**全般的な変更**

-   システム[システムステータス](https://status.tidbcloud.com/)ページを強化して、 TiDB Cloudシステムの健全性とパフォーマンスについてのより良い洞察を提供します。

    アクセスするには、 [https://status.tidbcloud.com/](https://status.tidbcloud.com/)直接アクセスするか、 [TiDB Cloudコンソール](https://tidbcloud.com)を介してナビゲートしてください。右下隅の**「？」**をクリックして**「システムステータス」**を選択します。

**コンソールの変更**

-   **VPC ピアリング**ページのレイアウトを調整して、 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでの[VPCピアリング接続の作成](/tidb-cloud/set-up-vpc-peering-connections.md)のユーザー エクスペリエンスを向上させます。

## 2024年7月2日 {#july-2-2024}

**全般的な変更**

-   データ [データサービス（ベータ版）](https://tidbcloud.com/project/data-service)は、データ アプリに直接追加できる事前定義されたシステム エンドポイントを含むエンドポイント ライブラリを提供し、エンドポイント開発の労力を軽減します。

    現在、このライブラリには`/system/query`エンドポイントのみが含まれています。このエンドポイントを使用すると、定義済みの`sql`パラメータにSQL文を渡すだけで、任意のSQL文を実行できます。このエンドポイントにより、SQLクエリを即座に実行できるため、柔軟性と効率性が向上します。

    詳細については、 [定義済みのシステムエンドポイントを追加します](/tidb-cloud/data-service-manage-endpoint.md#add-a-predefined-system-endpoint)参照してください。

-   低速クエリのデータstorageを強化する。

    [TiDB Cloudコンソール](https://tidbcloud.com)におけるクエリアクセスの遅延は、より安定し、データベースのパフォーマンスに影響を与えなくなりました。

## 2024年6月25日 {#june-25-2024}

**全般的な変更**

-   [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)ベクトル検索をサポートしています（ベータ版）。

    ベクトル検索（ベータ版）機能は、文書、画像、音声、動画など、さまざまなデータタイプにわたる意味的類似性検索を実行するための高度な検索ソリューションを提供します。この機能により、開発者は使い慣れたMySQLのスキルを使用して、生成型人工知能（AI）機能を備えたスケーラブルなアプリケーションを容易に構築できます。主な機能は以下のとおりです。

    -   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)、[ベクトルインデックス](/ai/reference/vector-search-index.md)、および[ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)。
    -   [ラングチェーン](/ai/integrations/vector-search-integrate-with-langchain.md)、 [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md)インデックス、 [Jina AI](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)とのエコシステム統合。
    -   Python のプログラミング言語サポート: [SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md) 、 [ピーウィー](/ai/integrations/vector-search-integrate-with-peewee.md)、および[Django ORM](/ai/integrations/vector-search-integrate-with-django-orm.md) 。
    -   サンプルアプリケーションとチュートリアル： [Python](/ai/quickstart-via-python.md)または[SQL](/ai/quickstart-via-sql.md)を使用してドキュメントのセマンティック検索を実行します。

    詳細については、[ベクトル検索（ベータ版）の概要](/ai/concepts/vector-search-overview.md)を参照してください。

-   [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter) 、組織オーナー向けに週次メールレポートの提供を開始しました。

    これらのレポートは、クラスターのパフォーマンスとアクティビティに関する洞察を提供します。毎週自動的に更新されるレポートを受け取ることで、クラスターの状況を常に把握し、データに基づいた意思決定を行ってクラスターを最適化することができます。

-   Chat2Query API v3 エンドポイントをリリースし、Chat2Query API v1 エンドポイント`/v1/chat2data`を非推奨にします。

    Chat2Query API v3のエンドポイントを使用すると、セッションを利用して複数ラウンドのChat2Queryを開始できます。

    詳細については、 [Chat2Query API を使い始めましょう](/tidb-cloud/use-chat2query-api.md)を参照してください。

**コンソールの変更**

-   Chat2Query（ベータ版）をSQL Editor（ベータ版）に名称変更します。

    以前はChat2Queryと呼ばれていたインターフェースは、SQL Editorに名称変更されました。この変更により、手動によるSQL編集とAIによるクエリ生成の区別が明確になり、使いやすさと全体的なユーザーエクスペリエンスが向上します。

    -   **SQLエディタ**： TiDB CloudコンソールでSQLクエリを手動で記述および実行するためのデフォルトインターフェース。
    -   **Chat2Query** ：AIを活用したテキストクエリ機能で、自然言語を使ってデータベースと対話し、SQLクエリを生成、書き換え、最適化することができます。

    詳細については、[AI支援型SQLエディタでデータを探索しよう](/tidb-cloud/explore-data-with-chat2query.md)参照してください。

## 2024年6月18日 {#june-18-2024}

**全般的な変更**

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタの16 vCPU TiFlashおよび32 vCPU TiFlashの最大ノードstorageを2048 GiBから4096 GiBに増加します。

    この機能強化により、TiDB Cloud Dedicatedクラスタの分析データstorage容量が増加し、ワークロードのスケーリング効率が向上し、増大するデータ要件に対応できるようになります。

    詳細については、 [TiFlashノードstorage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)を参照してください。

-   新しい[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[v7.5.1](https://docs.pingcap.com/tidb/stable/release-7.5.1)から[v7.5.2](https://docs.pingcap.com/tidb/stable/release-7.5.2)にアップグレードします。

## 2024年6月4日 {#june-4-2024}

**全般的な変更**

-   AWS上にデプロイされた[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのディザスタリカバリのためのリカバリグループ機能（ベータ版）を導入します。

    この機能を使用すると、TiDB Cloud Dedicatedクラスター間でデータベースを複製できるため、地域的な災害が発生した場合でも迅速なリカバリが可能になります。 `Project Owner`ロールをお持ちの場合は、新しいリカバリグループを作成し、データベースをそのグループに割り当てることで、この機能を有効にできます。リカバリグループを使用してデータベースを複製することで、災害対策を強化し、より厳格な可用性 SLA を満たし、より積極的な復旧ポイント目標 (RPO) および復旧時間目標 (RTO) を達成できます。

-   [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)カラム型storage[TiFlash](/tiflash/tiflash-overview.md)向けに、課金および計測機能 (ベータ版) を導入します。

    2024年6月30日まで、 TiDB Cloud Serverlessクラスターのカラム型storageは100%割引で無料です。この日以降は、各TiDB Cloud Serverlessクラスターに5 GiBのカラム型storageの無料クォータが付与されます。無料クォータを超過した場合は、料金が発生します。

    詳細については、 [TiDB Cloud Serverlessの料金詳細](https://www.pingcap.com/tidb-serverless-pricing-details/#storage)を参照してください。

-   [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)[生きる時間（TTL）](/time-to-live.md)をサポートします。

## 2024年5月28日 {#may-28-2024}

**全般的な変更**

-   Google Cloud `Taiwan (asia-east1)`リージョンは[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能をサポートしています。

    Google Cloud `Taiwan (asia-east1)`リージョンでホストされている[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターが、データ移行（DM）機能をサポートするようになりました。アップストリームデータがこのリージョン内またはその近隣に保存されている場合、Google CloudからTiDB Cloudへのより高速で信頼性の高いデータ移行を利用できるようになります。

-   AWS および Google Cloud でホストされる[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに新しい[TiDBノードサイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)を指定します: `16 vCPU, 64 GiB`

**APIの変更**

-   TiDB Cloud Data Service APIを導入することで、以下のリソースを自動的かつ効率的に管理できるようになります。

    -   **データアプリ**：特定のアプリケーションのデータにアクセスするために使用できるエンドポイントの集合。
    -   **データソース**：データ操作およびデータ取得のためにデータアプリにリンクされたクラスター。
    -   **エンドポイント**：SQL文を実行するようにカスタマイズ可能なWeb API。
    -   **データAPIキー**：エンドポイントへの安全なアクセスに使用されます。
    -   **OpenAPI仕様**：データサービスは、各データアプリに対してOpenAPI仕様3.0を生成することをサポートしており、これにより、標準化された形式でエンドポイントとやり取りすることが可能になります。

    これらのTiDB Cloud Data Service API エンドポイントは、 TiDB Cloudの最新 API バージョンであるTiDB Cloud API v1beta1 でリリースされています。

    詳細については、 [APIドキュメント（v1beta1）](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)を参照してください。

## 2024年5月21日 {#may-21-2024}

**全般的な変更**

-   Google Cloud でホストされる[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに新しい[TiDBノードサイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)を指定します: `8 vCPU, 16 GiB`

## 2024年5月14日 {#may-14-2024}

**全般的な変更**

-   さまざまな地域の顧客によりよく対応できるように、タイム[**タイムゾーン**](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)セクションのタイム ゾーンの選択を拡大します。

-   VPC がTiDB Cloudの VPC とは異なるリージョンにある場合、 [VPCピアリングの作成](/tidb-cloud/set-up-vpc-peering-connections.md)サポートします。

-   データ [データサービス（ベータ版）](https://tidbcloud.com/project/data-service)クエリ パラメーターとともにパス パラメーターをサポートしています。

    この機能は、構造化URLによるリソース識別を強化し、ユーザーエクスペリエンス、検索エンジン最適化（SEO）、クライアント統合を改善することで、開発者により柔軟性を提供し、業界標準との整合性を高めます。

    詳細については、 [基本特性](/tidb-cloud/data-service-manage-endpoint.md#basic-properties)を参照してください。

## 2024年4月16日 {#april-16-2024}

**CLIの変更**

-   新しい[TiDB CloudAPI](https://docs.pingcap.com/api/tidb-cloud-api-overview)をベースに構築された[TiDB Cloud CLI 1.0.0-beta.1](https://github.com/tidbcloud/tidbcloud-cli)をご紹介します。この新しい CLI には、以下の新機能が搭載されています。

    -   [TiDB Cloud Serverlessクラスターからデータをエクスポートする](/tidb-cloud/serverless-export.md)
    -   [ローカルstorageからTiDB Cloudサーバーレスクラスターにデータをインポートする](/tidb-cloud/ticloud-import-start.md)
    -   [OAuth経由で認証する](/tidb-cloud/ticloud-auth-login.md)

    TiDB Cloud CLI をアップグレードする前に、この新しい CLI は以前のバージョンと互換性がないことに注意してください。たとえば、CLI コマンドの`ticloud cluster`は`ticloud serverless`に更新されます。詳細については、 [TiDB Cloud CLI リファレンス](/tidb-cloud/cli-reference.md)参照してください。 .

## 2024年4月9日 {#april-9-2024}

**全般的な変更**

-   AWS: `8 vCPU, 32 GiB`でホストされる[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに新しい[TiDBノードサイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)を指定します。

## 2024年4月2日 {#april-2-2024}

**全般的な変更**

-   [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)クラスター向けに、**無料プラン**と**スケーラブルプラン**の 2 つのサービス プランを導入します。

    TiDB Cloud Serverlessは、多様なユーザーニーズに対応するため、無料プランと拡張可能なサービスプランを提供しています。これからサービスを開始する場合でも、アプリケーションの需要増加に合わせて規模を拡大する場合でも、これらのプランは必要な柔軟性と機能を提供します。

    詳細については、[クラスタ計画](/tidb-cloud/select-cluster-tier.md)を参照してください。

-   TiDB Cloud Serverless クラスターが使用量クォータに達した際のスロットリング動作を変更します。クラスターが使用量クォータに達すると、新規接続試行を即座に拒否し、既存の操作に対するサービスの中断を防ぎます。

    詳細については、 [使用クォータ](/tidb-cloud/serverless-limitations.md#usage-quota)参照してください。

## 2024年3月5日 {#march-5-2024}

**全般的な変更**

-   新しい[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[v7.5.0](https://docs.pingcap.com/tidb/stable/release-7.5.0)から[v7.5.1](https://docs.pingcap.com/tidb/stable/release-7.5.1)にアップグレードします。

**コンソールの変更**

-   [**請求する**](https://tidbcloud.com/org-settings/billing/payments)ページに**「コストエクスプローラー」**タブを導入します。このタブは、組織のコストレポートを時系列で分析およびカスタマイズするための直感的なインターフェースを提供します。

    この機能を使用するには、組織の**請求**ページに移動し、 **「コストエクスプローラー」**タブをクリックしてください。

    詳細については、 [コストエクスプローラー](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)を参照してください。

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) [ノードレベルのリソースメトリクス](/tidb-cloud/built-in-monitoring.md#server)の**制限**ラベルを表示します。

    **制限**ラベルには、クラスター内の各コンポーネントにおけるCPU、メモリ、storageなどのリソースの最大使用量が表示されます。この機能強化により、クラスターのリソース使用率の監視が簡素化されます。

    これらのメトリック制限にアクセスするには、クラスターの**監視**ページに移動し、 **[メトリック]**タブの**[サーバー]**カテゴリを確認してください。

    詳細については、 [TiDB Cloud Dedicatedクラスターのメトリクス](/tidb-cloud/built-in-monitoring.md#server)を参照してください。

## 2024年2月21日 {#february-21-2024}

**全般的な変更**

-   [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#starter)クラスターの TiDB バージョンを[v6.6.0](https://docs.pingcap.com/tidb/stable/release-6.6.0)から[v7.1.3](https://docs.pingcap.com/tidb/stable/release-7.1.3)にアップグレードします。

## 2024年2月20日 {#february-20-2024}

**全般的な変更**

-   Google Cloud上にTiDB Cloudノードをさらに作成できるようにサポートします。

    -   Google Cloud の`/19`の[地域別CIDRサイズの設定](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)により、プロジェクトの任意のリージョン内に最大 124 個のTiDB Cloudノードを作成できるようになりました。
    -   プロジェクトのいずれかのリージョンで 124 を超えるノードを作成する場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡して`/16`から`/18`の範囲の IP 範囲のサイズをカスタマイズするサポートを受けることができます。

## 2024年1月23日 {#january-23-2024}

**全般的な変更**

-   TiDB、TiKV、およびTiFlashのノードサイズオプションとして、32 vCPUを追加します。

    各`32 vCPU, 128 GiB` TiKV ノードのstorageは200 GiB から 6144 GiB の範囲です。

    次のようなシナリオでは、このようなノードの使用をお勧めします。

    -   高負荷本番環境
    -   極めて高い性能

## 2024年1月16日 {#january-16-2024}

**全般的な変更**

-   プロジェクトにおけるCIDR構成を強化する。

    -   各プロジェクトごとに、地域レベルのCIDRを直接設定できます。
    -   より幅広いCIDR値の中から、CIDR構成を選択できます。

    注：プロジェクトに対する以前のグローバルレベルのCIDR設定は廃止されますが、アクティブな状態にある既存の地域別CIDRはすべて影響を受けません。既存のクラスターのネットワークにも影響はありません。

    詳細については、 [地域ごとにCIDRを設定する](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)参照してください。

-   TiDB Cloud Serverlessのユーザーは、クラスターのパブリックエンドポイントを無効にすることができるようになりました。

    詳細については、 [公開エンドポイントを無効にする](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint)ご覧ください。

-   データ [データサービス（ベータ版）](https://tidbcloud.com/project/data-service)データ アプリのエンドポイントにアクセスするためのカスタム ドメインの構成をサポートしています。

    TiDB Cloud Data Serviceは、デフォルトでは各データアプリのエンドポイントにアクセスするためのドメイン`<region>.data.tidbcloud.com`を提供します。パーソナライズと柔軟性をさらに高めるため、デフォルトドメインの代わりにデータアプリにカスタムドメインを設定できるようになりました。この機能により、データベースサービスにブランドURLを使用でき、セキュリティも強化されます。

    詳細については、 [データサービスのカスタムドメイン](/tidb-cloud/data-service-custom-domain.md)参照してください。

## 2024年1月3日 {#january-3-2024}

**全般的な変更**

-   企業認証プロセスを効率化するために、 [組織SSO](https://tidbcloud.com/org-settings/authentication)をサポートします。

    この機能を使用すると、 [Securityアサーションマークアップ言語（SAML）](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)または[OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/)を使用して、 TiDB Cloud を任意のアイデンティティ プロバイダー (IdP) とシームレスに統合できます。

    詳細については、 [組織のSSO認証](/tidb-cloud/tidb-cloud-org-sso-authentication.md)を参照してください。

-   新しい[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[v7.1.1](https://docs.pingcap.com/tidb/stable/release-7.1.1)から[v7.5.0](https://docs.pingcap.com/tidb/stable/release-7.5.0)にアップグレードします。

-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のデュアルリージョンバックアップ機能が、一般提供（GA）を開始しました。

    この機能を使用すると、AWSまたはGoogle Cloud内の地理的に離れたリージョン間でバックアップを複製できます。この機能は、データ保護とディザスタリカバリ機能をさらにレイヤーします。

    詳細については、 [デュアルリージョンバックアップ](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)を参照してください。
