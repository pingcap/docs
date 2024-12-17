---
title: TiDB Cloud Release Notes in 2024
summary: 2024 年のTiDB Cloudのリリース ノートについて説明します。
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2024 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2024}

このページには、2024 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2024年12月3日 {#december-3-2024}

**一般的な変更**

-   AWS にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの災害復旧のためのリカバリ グループ機能 (ベータ版) を導入します。

    この機能により、 TiDB Cloud Dedicated クラスター間でデータベースを複製できるため、地域災害が発生した場合でも迅速な復旧が可能になります。プロジェクト オーナーの役割を担っている場合は、新しい復旧グループを作成し、そのグループにデータベースを割り当てることで、この機能を有効にできます。復旧グループを使用してデータベースを複製することで、災害への備えを強化し、より厳格な可用性 SLA を満たし、より積極的な復旧ポイント目標 (RPO) と復旧時間目標 (RTO) を達成できます。

    詳細については[回復グループを始める](/tidb-cloud/recovery-group-get-started.md)参照してください。

## 2024年11月26日 {#november-26-2024}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4)から[バージョン8.1.1](https://docs.pingcap.com/tidb/stable/release-8.1.1)にアップグレードします。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 、次のシナリオで大容量データの書き込みコストを最大 80% 削減します。

    -   [自動コミットモード](/transaction-overview.md#autocommit)で 16 MiB を超える書き込み操作を実行する場合。
    -   [楽観的取引モデル](/optimistic-transaction.md)で 16 MiB を超える書き込み操作を実行する場合。
    -   [TiDB Cloudにデータをインポートする](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) .

    この改善により、データ操作の効率とコスト効率が向上し、ワークロードの拡大に応じてより大きな節約が実現します。

## 2024年11月19日 {#november-19-2024}

**一般的な変更**

-   [TiDB Cloudサーバーレス ブランチング (ベータ版)](/tidb-cloud/branch-overview.md)ブランチ管理に次の改善が導入されています。

    -   **柔軟なブランチ作成**: ブランチを作成するときに、特定のクラスターまたはブランチを親として選択し、親から使用する正確な時点を指定できます。これにより、ブランチ内のデータを正確に制御できます。

    -   **ブランチのリセット**: ブランチをリセットして、親の最新の状態と同期することができます。

    -   **GitHub 統合の改善**: [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching) GitHub アプリでは、プル リクエストの同期中の動作を制御する[`branch.mode`](/tidb-cloud/branch-github-integration.md#branchmode)パラメーターが導入されています。デフォルト モード`reset`では、アプリはプル リクエストの最新の変更に合わせてブランチをリセットします。

    詳細については[TiDB Cloudサーバーレス ブランチの管理](/tidb-cloud/branch-manage.md)および[TiDB Cloud Serverless Branching (ベータ版) を GitHub と統合する](/tidb-cloud/branch-github-integration.md)参照してください。

## 2024年11月12日 {#november-12-2024}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの一時停止期間制限を追加します。

    TiDB Cloud Dedicated では、最大一時停止期間が 7 日間に制限されるようになりました。7 日以内にクラスターを手動で再開しない場合は、 TiDB Cloud自動的に再開されます。

    この変更は**、2024 年 11 月 12 日以降に作成された組織**にのみ適用されます。この日付以前に作成された組織は、事前に通知して、新しい一時停止動作に段階的に移行します。

    詳細については[TiDB Cloud専用クラスタを一時停止または再開する](/tidb-cloud/pause-or-resume-tidb-cluster.md)参照してください。

-   [Datadog 統合 (ベータ版)](/tidb-cloud/monitor-datadog-integration.md) 、新しい地域`AP1` (日本) のサポートが追加されました。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい AWS リージョンをサポートします: `Mumbai (ap-south-1)` 。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対する AWS `São Paulo (sa-east-1)`リージョンのサポートを削除します。

## 2024年10月29日 {#october-29-2024}

**一般的な変更**

-   新しいメトリック: Prometheus 統合に`tidbcloud_changefeed_checkpoint_ts`を追加します。

    このメトリックは、変更フィードのチェックポイント タイムスタンプを追跡し、ダウンストリームに正常に書き込まれた最大の TSO (Timestamp Oracle) を表します。使用可能なメトリックの詳細については、 [TiDB Cloud をPrometheus および Grafana と統合する (ベータ版)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)参照してください。

## 2024年10月22日 {#october-22-2024}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3)から[バージョン7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4)にアップグレードします。

## 2024年10月15日 {#october-15-2024}

**APIの変更**

-   [MSP](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)は 2024 年 10 月 15 日をもって廃止となり、今後削除される予定です。現在 MSP API をご利用の場合は、 [TiDB Cloudパートナー](https://partner-console.tidbcloud.com/signin)のパートナー管理 API に移行してください。

## 2024年9月24日 {#september-24-2024}

**一般的な変更**

-   AWSでホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのうち[TiFlash vCPU と RAM サイズ](/tidb-cloud/size-your-cluster.md#tiflash-vcpu-and-ram)新規に提供します: `32 vCPU, 128 GiB`

**CLIの変更**

-   リリース[TiDB CloudCLI v1.0.0-beta.2](https://github.com/tidbcloud/tidbcloud-cli/releases/tag/v1.0.0-beta.2) 。

    TiDB Cloud CLI は、次の新機能を提供します。

    -   [`ticloud serverless sql-user`](/tidb-cloud/ticloud-serverless-sql-user-create.md)経由で[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの SQL ユーザー管理をサポートします。
    -   [`ticloud serverless create`](/tidb-cloud/ticloud-cluster-create.md)および[`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md)の[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)のクラスターのパブリック エンドポイントを無効にすることを許可します。
    -   OAuth 認証を使用するときに現在のユーザーに関する情報を取得するには、 [`ticloud auth whoami`](/tidb-cloud/ticloud-auth-whoami.md)コマンドを追加します。
    -   ソース テーブルを柔軟に選択するために`--where` [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)の`--sql` 、および`--filter`フラグをサポートします。
    -   CSV および Parquet ファイルへのデータのエクスポートをサポートします。
    -   ロール ARN を認証情報として使用して Amazon S3 にデータをエクスポートする機能をサポートし、Google Cloud Storage および Azure Blob Storage へのエクスポートもサポートします。
    -   Amazon S3、Google Cloud Storage、Azure Blob Storage からのデータのインポートをサポートします。
    -   ブランチと特定のタイムスタンプからブランチを作成する機能をサポートします。

    TiDB Cloud CLI では、次の機能が強化されています。

    -   デバッグ ログを改善しました。資格情報とユーザー エージェントをログに記録できるようになりました。
    -   ローカルエクスポートファイルのダウンロードを毎秒数十 KiB から毎秒数十 MiB に高速化します。

    TiDB Cloud CLI では、次の機能が置き換えられたり、削除されます。

    -   [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)では、 `--s3.bucket-uri`フラグが`--s3.uri`に置き換えられます。
    -   [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)では、フラグ`--database`と`--table`削除されています。代わりに、フラグ`--sql` 、 `--where` 、および`--filter`使用できます。
    -   [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md)注釈フィールドを更新できなくなりました。

## 2024年9月10日 {#september-10-2024}

**一般的な変更**

-   TiDB Cloudパートナー Web コンソールとオープン API を起動して、 TiDB Cloudパートナーのリソースと課金の管理を強化します。

    マネージドサービスプロバイダー (MSP) と AWS Marketplace チャネルパートナープライベートオファー (CPPO) を介した再販業者は、 [TiDB Cloudパートナー Web コンソール](https://partner-console.tidbcloud.com/)とオープン API を活用して日常業務を効率化できるようになりました。

    詳細については[TiDB Cloudパートナー Web コンソール](/tidb-cloud/tidb-cloud-partners.md)参照してください。

## 2024年9月3日 {#september-3-2024}

**コンソールの変更**

-   [TiDB Cloudコンソール](https://tidbcloud.com/)使用してTiDB Cloud Serverless クラスターからデータをエクスポートすることをサポートします。

    これまで、 TiDB Cloud[TiDB CloudCLI](/tidb-cloud/cli-reference.md)使用したデータのエクスポートのみがサポートされていました。現在では、 [TiDB Cloudコンソール](https://tidbcloud.com/)使用して、 TiDB Cloud Serverless クラスターからローカル ファイルや Amazon S3 にデータを簡単にエクスポートできます。

    詳細については[TiDB Cloud Serverless からデータをエクスポート](/tidb-cloud/serverless-export.md)および[TiDB Cloud Serverless の外部ストレージ アクセスを構成する](/tidb-cloud/serverless-external-storage.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの接続エクスペリエンスを強化します。

    -   **接続**ダイアログ インターフェイスを改訂し、 TiDB Cloud Dedicated ユーザーに、より合理化され効率的な接続エクスペリエンスを提供します。
    -   クラスターのネットワーク構成を簡素化するために、新しいクラスター レベルの**ネットワーク**ページを導入しました。
    -   **Security設定**ページを新しい**パスワード設定**ページに置き換え、IP アクセス リスト設定を新しい**ネットワーク**ページに移動します。

    詳細については[TiDB Cloud専用に接続](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)および[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデータ インポート エクスペリエンスを強化します。

    -   **インポート**ページのレイアウトをより明確なレイアウトに改良します。
    -   TiDB Cloud Serverless クラスターとTiDB Cloud Dedicated クラスターのインポート手順を統一します。
    -   AWS ロール ARN 作成プロセスを簡素化し、接続のセットアップを容易にします。

    詳細については[ファイルからTiDB Cloudにデータをインポートする](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)参照してください。

## 2024年8月20日 {#august-20-2024}

**コンソールの変更**

-   **プライベート エンドポイント接続の作成**ページのレイアウトを調整し、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで新しいプライベート エンドポイント接続を作成する際のユーザー エクスペリエンスを向上させます。

    詳細については[AWS のプライベートエンドポイント経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)および[Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

## 2024年8月6日 {#august-6-2024}

**一般的な変更**

-   AWS での負荷分散に対する請求の変更は[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 。

    2024 年 8 月 1 日より、 TiDB Cloud Dedicated の請求書には、 [AWS の料金変更は 2024 年 2 月 1 日より有効になります](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)に合わせたパブリック IPv4 アドレスの新しい AWS 料金が含まれます。パブリック IPv4 アドレスごとの料金は 1 時間あたり 0.005 ドルで、AWS でホストされるTiDB Cloud Dedicated クラスターごとに月額約 10 ドルになります。

    この料金は、 [請求の詳細](/tidb-cloud/tidb-cloud-billing.md#billing-details)の既存の**TiDB Cloud Dedicated - Data Transfer - Load Balancing**サービスの下に表示されます。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)から[バージョン7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3)にアップグレードします。

**コンソールの変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスター サイズ構成エクスペリエンスを強化します。

    TiDB Cloud Dedicated クラスターの[**クラスタの作成**](/tidb-cloud/create-tidb-cluster.md)ページ目と[**クラスタの変更**](/tidb-cloud/scale-tidb-cluster.md)ページ目の**クラスタサイズ**セクションのレイアウトを改良しました。さらに、**クラスタサイズ**セクションには、適切なクラスター サイズを選択するのに役立つノード サイズの推奨ドキュメントへのリンクが含まれるようになりました。

## 2024年7月23日 {#july-23-2024}

**一般的な変更**

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)ベクター検索エンドポイントの自動生成をサポートします。

    テーブルに[ベクトルデータ型](/tidb-cloud/vector-search-data-types.md)含まれている場合は、選択した距離関数に基づいてベクトル距離を計算するベクトル検索エンドポイントを自動的に生成できます。

    この機能により、 [ディファイ](https://docs.dify.ai/guides/tools)や[GPT は](https://openai.com/blog/introducing-gpts)などの AI プラットフォームとのシームレスな統合が可能になり、高度な自然言語処理と AI 機能によってアプリケーションが強化され、より複雑なタスクやインテリジェントなソリューションが実現します。

    詳細については[エンドポイントを自動的に生成する](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)および[データアプリをサードパーティツールと統合する](/tidb-cloud/data-service-integrations.md)参照してください。

-   予算機能を導入すると、計画された費用に対する実際のTiDB Cloudコストを追跡し、予期しないコストを防ぐことができます。

    この機能にアクセスするには、組織内で`Organization Owner`または`Organization Billing Admin`のロールを持っている必要があります。

    詳細については[TiDB Cloudの予算管理](/tidb-cloud/tidb-cloud-budget.md)参照してください。

## 2024年7月9日 {#july-9-2024}

**一般的な変更**

-   [システムステータス](https://status.tidbcloud.com/)ページを拡張して、 TiDB Cloudシステムの健全性とパフォーマンスに関するより詳細な情報を提供します。

    アクセスするには、 [https://status.tidbcloud.com/](https://status.tidbcloud.com/)直接アクセスするか、右下隅の [ **?]**をクリックして**[システム ステータス]**を選択し、 [TiDB Cloudコンソール](https://tidbcloud.com)を経由して移動します。

**コンソールの変更**

-   **VPC ピアリング**ページのレイアウトを調整して、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのうち[VPC ピアリング接続の作成](/tidb-cloud/set-up-vpc-peering-connections.md)クラスターのユーザー エクスペリエンスを向上させます。

## 2024年7月2日 {#july-2-2024}

**一般的な変更**

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service) 、データ アプリに直接追加できる定義済みのシステム エンドポイントを含むエンドポイント ライブラリが提供されるため、エンドポイント開発の労力が軽減されます。

    現在、ライブラリには`/system/query`エンドポイントのみが含まれており、定義済みの`sql`パラメータでステートメントを渡すだけで、任意の SQL ステートメントを実行できます。このエンドポイントにより、SQL クエリの即時実行が容易になり、柔軟性と効率性が向上します。

    詳細については[定義済みのシステムエンドポイントを追加する](/tidb-cloud/data-service-manage-endpoint.md#add-a-predefined-system-endpoint)参照してください。

-   低速クエリデータstorageを強化します。

    [TiDB Cloudコンソール](https://tidbcloud.com)の低速クエリ アクセスはより安定し、データベースのパフォーマンスに影響を与えなくなりました。

## 2024年6月25日 {#june-25-2024}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)ベクトル検索をサポートします (ベータ版)。

    ベクター検索 (ベータ) 機能は、ドキュメント、画像、音声、ビデオなど、さまざまなデータ タイプにわたって意味的類似性検索を実行するための高度な検索ソリューションを提供します。この機能により、開発者は使い慣れた MySQL スキルを使用して、生成型人工知能 (AI) 機能を備えたスケーラブルなアプリケーションを簡単に構築できます。主な機能は次のとおりです。

    -   [ベクトルデータ型](/tidb-cloud/vector-search-data-types.md) 、 [ベクトルインデックス](/tidb-cloud/vector-search-index.md) 、および[ベクトル関数と演算子](/tidb-cloud/vector-search-functions-and-operators.md) 。
    -   [ランチェーン](/tidb-cloud/vector-search-integrate-with-langchain.md) [ラマインデックス](/tidb-cloud/vector-search-integrate-with-llamaindex.md) [ジナAI](/tidb-cloud/vector-search-integrate-with-jinaai-embedding.md)エコシステム統合。
    -   Python [Django ORM](/tidb-cloud/vector-search-integrate-with-django-orm.md)プログラミング言語サポート: [SQLアルケミー](/tidb-cloud/vector-search-integrate-with-sqlalchemy.md) 、および[ピーウィー](/tidb-cloud/vector-search-integrate-with-peewee.md) 。
    -   サンプルアプリケーションとチュートリアル: [パイソン](/tidb-cloud/vector-search-get-started-using-python.md)または[構文](/tidb-cloud/vector-search-get-started-using-sql.md)使用してドキュメントのセマンティック検索を実行します。

    詳細については[ベクトル検索（ベータ版）の概要](/tidb-cloud/vector-search-overview.md)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)では、組織の所有者向けに毎週の電子メールレポートが提供されるようになりました。

    これらのレポートは、クラスターのパフォーマンスとアクティビティに関する洞察を提供します。毎週の自動更新を受信することで、クラスターに関する情報を常に把握し、データに基づいた意思決定を行ってクラスターを最適化できます。

-   Chat2Query API v3 エンドポイントをリリースし、Chat2Query API v1 エンドポイント`/v1/chat2data`を廃止します。

    Chat2Query API v3 エンドポイントを使用すると、セッションを使用して複数ラウンドの Chat2Query を開始できます。

    詳細については[Chat2Query APIを使い始める](/tidb-cloud/use-chat2query-api.md)参照してください。

**コンソールの変更**

-   Chat2Query (ベータ版) の名前を SQL Editor (ベータ版) に変更します。

    以前 Chat2Query と呼ばれていたインターフェースの名前が SQL Editor に変更されました。この変更により、手動の SQL 編集と AI 支援によるクエリ生成の違いが明確になり、使いやすさと全体的なエクスペリエンスが向上します。

    -   **SQL エディター**: TiDB Cloudコンソールで SQL クエリを手動で記述および実行するためのデフォルトのインターフェース。
    -   **Chat2Query** : AI 支援のテキストクエリ機能。自然言語を使用してデータベースと対話し、SQL クエリを生成、書き換え、最適化できます。

    詳細については[AI支援SQLエディターでデータを探索](/tidb-cloud/explore-data-with-chat2query.md)参照してください。

## 2024年6月18日 {#june-18-2024}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの 16 vCPU TiFlashと 32 vCPU TiFlashの最大ノードstorageを2048 GiB から 4096 GiB に増加します。

    この機能強化により、 TiDB Cloud Dedicated クラスターの分析データstorage容量が増加し、ワークロードのスケーリング効率が向上し、増大するデータ要件に対応できるようになります。

    詳細については[TiFlashノードstorage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)参照してください。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1)から[バージョン7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)にアップグレードします。

## 2024年6月4日 {#june-4-2024}

**一般的な変更**

-   AWS にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの災害復旧のためのリカバリ グループ機能 (ベータ版) を導入します。

    この機能により、 TiDB Cloud Dedicated クラスター間でデータベースを複製し、地域災害が発生した場合に迅速な復旧を実現できます。 `Project Owner`ロールの場合は、新しい復旧グループを作成し、そのグループにデータベースを割り当てることで、この機能を有効にできます。 復旧グループを使用してデータベースを複製することで、災害への備えを強化し、より厳格な可用性 SLA を満たし、より積極的な復旧ポイント目標 (RPO) と復旧時間目標 (RTO) を達成できます。

    詳細については[回復グループを始める](/tidb-cloud/recovery-group-get-started.md)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)列storage[TiFlash](/tiflash/tiflash-overview.md)の課金と計測 (ベータ版) を導入します。

    2024 年 6 月 30 日まで、 TiDB Cloud Serverless クラスターの列指向storageは100% 割引で無料のままです。この日以降、各TiDB Cloud Serverless クラスターには、列指向storage用の 5 GiB の無料割り当てが含まれます。無料割り当てを超えた使用には料金が発生します。

    詳細については[TiDB Cloud Serverless の価格詳細](https://www.pingcap.com/tidb-serverless-pricing-details/#storage)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) [存続時間 (TTL)](/time-to-live.md)をサポートします。

## 2024年5月28日 {#may-28-2024}

**一般的な変更**

-   Google Cloud `Taiwan (asia-east1)`リージョンは[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能をサポートしています。

    Google Cloud `Taiwan (asia-east1)`リージョンでホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタが、データ移行（DM）機能をサポートするようになりました。アップストリーム データがこのリージョン内またはその付近に保存されている場合は、Google Cloud からTiDB Cloudへのより高速で信頼性の高いデータ移行を利用できるようになります。

-   AWSとGoogle Cloudでホストされる[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタのうち[TiDB ノード サイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)新たに提供: `16 vCPU, 64 GiB`

**APIの変更**

-   以下のリソースを自動的かつ効率的に管理するためのTiDB Cloudデータ サービス API を導入します。

    -   **データ アプリ**: 特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのコレクション。
    -   **データ ソース**: データの操作と取得のためにデータ アプリにリンクされたクラスター。
    -   **エンドポイント**: SQL ステートメントを実行するためにカスタマイズできる Web API。
    -   **データ API キー**: 安全なエンドポイント アクセスに使用されます。
    -   **OpenAPI 仕様**: データ サービスは、各データ アプリの OpenAPI 仕様 3.0 の生成をサポートしており、これにより標準化された形式でエンドポイントと対話できるようになります。

    これらのTiDB Cloud Data Service API エンドポイントは、 TiDB Cloudの最新の API バージョンであるTiDB Cloud API v1beta1 でリリースされています。

    詳細については[API ドキュメント (v1beta1)](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)参照してください。

## 2024年5月21日 {#may-21-2024}

**一般的な変更**

-   Google Cloud でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタのうち[TiDB ノード サイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)新たに提供: `8 vCPU, 16 GiB`

## 2024年5月14日 {#may-14-2024}

**一般的な変更**

-   さまざまな地域の顧客にさらに対応できるよう、セクション[**タイムゾーン**](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)のタイム ゾーンの選択範囲を拡張します。

-   VPC がTiDB Cloudの VPC とは異なるリージョンにある場合は[VPCピアリングの作成](/tidb-cloud/set-up-vpc-peering-connections.md)サポートします。

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)クエリ パラメータとともにパス パラメータをサポートします。

    この機能により、構造化 URL によるリソース識別が強化され、ユーザー エクスペリエンス、検索エンジン最適化 (SEO)、クライアント統合が改善され、開発者の柔軟性が向上し、業界標準との整合性が向上します。

    詳細については[基本的なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#basic-properties)参照してください。

## 2024年4月16日 {#april-16-2024}

**CLIの変更**

-   新しい[TiDB CloudAPI](/tidb-cloud/api-overview.md)ベースに構築された[TiDB CloudCLI 1.0.0-beta.1](https://github.com/tidbcloud/tidbcloud-cli)導入します。新しい CLI には、次の新機能が追加されています。

    -   [TiDB Cloud Serverless クラスターからデータをエクスポートする](/tidb-cloud/serverless-export.md)
    -   [ローカルstorageからTiDB Cloud Serverlessクラスターにデータをインポートする](/tidb-cloud/ticloud-import-start.md)
    -   [OAuth による認証](/tidb-cloud/ticloud-auth-login.md)
    -   [TiDBボット経由で質問する](/tidb-cloud/ticloud-ai.md)

    TiDB Cloud CLI をアップグレードする前に、この新しい CLI は以前のバージョンと互換性がないことに注意してください。たとえば、CLI コマンドの`ticloud cluster` `ticloud serverless`に更新されました。詳細については、 [TiDB Cloud CLI リファレンス](/tidb-cloud/cli-reference.md)参照してください。

## 2024年4月9日 {#april-9-2024}

**一般的な変更**

-   AWS でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい[TiDB ノード サイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)を提供します: `8 vCPU, 32 GiB` 。

## 2024年4月2日 {#april-2-2024}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに対して、**無料**と**スケーラブルの**2 つのサービス プランを導入します。

    さまざまなユーザー要件を満たすために、 TiDB Cloud Serverless は無料かつスケーラブルなサービス プランを提供しています。始めたばかりの場合でも、増大するアプリケーション需要に対応するために拡張する場合でも、これらのプランは必要な柔軟性と機能を提供します。

    詳細については[クラスタ計画](/tidb-cloud/select-cluster-tier.md#cluster-plans)参照してください。

-   使用量の割り当てに達したときのTiDB Cloud Serverless クラスターのスロットル動作を変更します。クラスターが使用量の割り当てに達すると、新しい接続の試行が直ちに拒否されるようになり、既存の操作に対するサービスが中断されなくなります。

    詳細については[使用量制限](/tidb-cloud/serverless-limitations.md#usage-quota)参照してください。

## 2024年3月5日 {#march-5-2024}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)から[バージョン7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1)にアップグレードします。

**コンソールの変更**

-   [**請求する**](https://tidbcloud.com/console/org-settings/billing/payments)ページに「**コスト エクスプローラー」**タブを導入します。このタブは、組織のコスト レポートを長期にわたって分析およびカスタマイズするための直感的なインターフェイスを提供します。

    この機能を使用するには、組織の**請求**ページに移動し、**コスト エクスプローラー**タブをクリックします。

    詳細については[コストエクスプローラー](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) [ノードレベルのリソースメトリック](/tidb-cloud/built-in-monitoring.md#server)の**制限**ラベルを表示します。

    **制限**ラベルには、クラスター内の各コンポーネントの CPU、メモリ、storageなどのリソースの最大使用量が表示されます。この機能強化により、クラスターのリソース使用率を監視するプロセスが簡素化されます。

    これらのメトリック制限にアクセスするには、クラスターの**[監視]**ページに移動し、 **[メトリック]**タブの**[サーバー]**カテゴリを確認します。

    詳細については[TiDB Cloud Dedicated クラスタのメトリクス](/tidb-cloud/built-in-monitoring.md#server)参照してください。

## 2024年2月21日 {#february-21-2024}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの TiDB バージョンを[バージョン6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)から[バージョン7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3)にアップグレードします。

## 2024年2月20日 {#february-20-2024}

**一般的な変更**

-   Google Cloud 上でさらに多くのTiDB Cloudノードの作成をサポートします。

    -   Google Cloud の[リージョン CIDR サイズの設定](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) of `/19`では、プロジェクトの任意のリージョン内に最大 124 個のTiDB Cloudノードを作成できるようになりました。
    -   プロジェクトの任意のリージョンに 124 を超えるノードを作成する場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)連絡して、 `/16`から`/18`までの IP 範囲のサイズをカスタマイズするためのサポートを受けることができます。

## 2024年1月23日 {#january-23-2024}

**一般的な変更**

-   TiDB、TiKV、 TiFlashのノード サイズ オプションとして 32 vCPU を追加します。

    `32 vCPU, 128 GiB` TiKV ノードごとに、ノードstorageの範囲は 200 GiB から 6144 GiB になります。

    次のシナリオでは、このようなノードを使用することをお勧めします。

    -   高負荷の本番環境
    -   非常に高いパフォーマンス

## 2024年1月16日 {#january-16-2024}

**一般的な変更**

-   プロジェクトの CIDR 構成を強化します。

    -   各プロジェクトに対してリージョン レベルの CIDR を直接設定できます。
    -   より広範な CIDR 値から CIDR 構成を選択できます。

    注: プロジェクトの以前のグローバル レベルの CIDR 設定は廃止されますが、アクティブ状態にある既存のリージョン CIDR はすべて影響を受けません。既存のクラスターのネットワークには影響はありません。

    詳細については[リージョンのCIDRを設定する](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)参照してください。

-   TiDB Cloud Serverless ユーザーは、クラスターのパブリック エンドポイントを無効にすることができるようになりました。

    詳細については[パブリックエンドポイントを無効にする](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint)参照してください。

-   [データ サービス (ベータ版)](https://tidbcloud.com/console/data-service)データ アプリ内のエンドポイントにアクセスするためのカスタム ドメインの構成がサポートされています。

    デフォルトでは、 TiDB Cloud Data Service は各データ アプリのエンドポイントにアクセスするためのドメイン`<region>.data.tidbcloud.com`を提供します。パーソナライズと柔軟性を高めるために、デフォルトのドメインを使用する代わりに、データ アプリのカスタム ドメインを構成できるようになりました。この機能により、データベース サービスにブランド化された URL を使用でき、セキュリティが強化されます。

    詳細については[データ サービスにおけるカスタム ドメイン](/tidb-cloud/data-service-custom-domain.md)参照してください。

## 2024年1月3日 {#january-3-2024}

**一般的な変更**

-   エンタープライズ認証プロセスを合理化するためのサポート[組織の SSO](https://tidbcloud.com/console/preferences/authentication) 。

    この機能を使用すると、 [Securityアサーションマークアップ言語 (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)または[OpenIDコネクト（OIDC）](https://openid.net/developers/how-connect-works/)使用して、 TiDB Cloud を任意の ID プロバイダー (IdP) とシームレスに統合できます。

    詳細については[組織のSSO認証](/tidb-cloud/tidb-cloud-org-sso-authentication.md)参照してください。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)から[バージョン7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)にアップグレードします。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のデュアル リージョン バックアップ機能が一般提供 (GA) になりました。

    この機能を使用すると、AWS または Google Cloud 内の地理的リージョン間でバックアップを複製できます。この機能により、データ保護と災害復旧機能の追加レイヤーが提供されます。

    詳細については[デュアルリージョンバックアップ](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)参照してください。
