---
title: TiDB Cloud Release Notes in 2024
summary: 2024 年のTiDB Cloudのリリース ノートについて説明します。
---

# 2024年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2024}

このページには、2024 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2024年12月17日 {#december-17-2024}

**一般的な変更**

-   TiDB Cloudサーバーレスバックアップとリストアの変更

    -   新しいクラスターへのデータの復元をサポートし、柔軟性を高め、現在のクラスターの操作が中断されないようにします。

    -   クラスタ計画に合わせてバックアップとリストアの戦略を調整します。詳細については、 [TiDB Cloudサーバーレスデータのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md#learn-about-the-backup-setting)参照してください。

    -   スムーズな移行を支援するために、次の互換性ポリシーを適用します。

        -   2024-12-17T10:00:00Z より前に作成されたバックアップは、すべてのクラスターにわたって以前の保持期間に従います。
        -   スケーラブル クラスターのバックアップ時間は現在の構成を保持しますが、フリー クラスターのバックアップ時間はデフォルト設定にリセットされます。

## 2024年12月3日 {#december-3-2024}

**一般的な変更**

-   AWS にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの災害復旧用のリカバリ グループ機能 (ベータ版) を導入します。

    この機能により、 TiDB Cloud Dedicated クラスタ間でデータベースを複製し、地域災害発生時の迅速な復旧が可能になります。プロジェクトオーナー権限をお持ちの場合は、新しいリカバリグループを作成し、データベースをそのグループに割り当てることで、この機能を有効にできます。リカバリグループを使用してデータベースを複製することで、災害対策を強化し、より厳格な可用性SLAを満たし、より厳格な復旧ポイント目標（RPO）と復旧時間目標（RTO）を達成できます。

    詳細については[回復グループを始める](/tidb-cloud/recovery-group-get-started.md)参照してください。

## 2024年11月26日 {#november-26-2024}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4)から[バージョン8.1.1](https://docs.pingcap.com/tidb/stable/release-8.1.1)にアップグレードします。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 、次のシナリオで大容量データの書き込みコストを最大 80% 削減します。

    -   [自動コミットモード](/transaction-overview.md#autocommit)で 16 MiB を超える書き込み操作を実行する場合。
    -   [楽観的取引モデル](/optimistic-transaction.md)で 16 MiB を超える書き込み操作を実行する場合。
    -   あなたが[TiDB Cloudにデータをインポートする](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) .

    この改善により、データ操作の効率とコスト効率が向上し、ワークロードの拡大に応じてさらなる節約が実現します。

## 2024年11月19日 {#november-19-2024}

**一般的な変更**

-   [TiDB Cloudサーバーレス ブランチング (ベータ版)](/tidb-cloud/branch-overview.md) 、ブランチ管理に次の改善が導入されています。

    -   **柔軟なブランチ作成**：ブランチを作成する際に、特定のクラスターまたはブランチを親として選択し、親から使用する正確な時点を指定できます。これにより、ブランチ内のデータを正確に制御できます。

    -   **ブランチのリセット**: ブランチをリセットして、親の最新の状態と同期することができます。

    -   **GitHubとの連携強化**：GitHub App [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)では、プルリクエスト同期時の動作を制御するパラメータ[`branch.mode`](/tidb-cloud/branch-github-integration.md#branchmode)導入されました。デフォルトモード`reset`では、アプリはプルリクエストの最新の変更に合わせてブランチをリセットします。

    詳細については、 [TiDB Cloudサーバーレスブランチの管理](/tidb-cloud/branch-manage.md)および[TiDB Cloud Serverless Branching（ベータ版）をGitHubと統合する](/tidb-cloud/branch-github-integration.md)参照してください。

## 2024年11月12日 {#november-12-2024}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの一時停止期間制限を追加します。

    TiDB Cloud Dedicated では、最大一時停止期間が 7 日間に制限されました。7 日以内にクラスターを手動で再開しない場合、 TiDB Cloudが自動的に再開します。

    この変更は**、2024 年 11 月 12 日以降に作成された組織**にのみ適用されます。この日付以前に作成された組織は、事前に通知して、新しい一時停止動作に段階的に移行します。

    詳細については[TiDB Cloud専用クラスタを一時停止または再開する](/tidb-cloud/pause-or-resume-tidb-cluster.md)参照してください。

-   [Datadog 統合（ベータ版）](/tidb-cloud/monitor-datadog-integration.md) 、新しい地域`AP1` (日本) のサポートが追加されました。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい AWS リージョンをサポートします: `Mumbai (ap-south-1)` 。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対する AWS `São Paulo (sa-east-1)`リージョンのサポートを削除します。

## 2024年10月29日 {#october-29-2024}

**一般的な変更**

-   新しいメトリック: Prometheus 統合に`tidbcloud_changefeed_checkpoint_ts`追加します。

    この指標は、チェンジフィードのチェックポイントタイムスタンプを追跡します。これは、下流に正常に書き込まれた最大のTSO（Timestamp Oracle）を表します。利用可能な指標の詳細については、 [TiDB Cloud をPrometheus および Grafana と統合する (ベータ版)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#metrics-available-to-prometheus)参照してください。

## 2024年10月22日 {#october-22-2024}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3)から[バージョン7.5.4](https://docs.pingcap.com/tidb/v7.5/release-7.5.4)にアップグレードします。

## 2024年10月15日 {#october-15-2024}

**APIの変更**

-   [MSP](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)は2024年10月15日をもって廃止され、将来的に削除される予定です。現在 MSP API をご利用の場合は、 [TiDB Cloudパートナー](https://partner-console.tidbcloud.com/signin)のパートナー管理 API に移行してください。

## 2024年9月24日 {#september-24-2024}

**一般的な変更**

-   AWSでホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに新しい[TiFlash vCPUとRAMサイズ](/tidb-cloud/size-your-cluster.md#tiflash-vcpu-and-ram)を提供: `32 vCPU, 128 GiB`

**CLIの変更**

-   リリース[TiDB CloudCLI v1.0.0-beta.2](https://github.com/tidbcloud/tidbcloud-cli/releases/tag/v1.0.0-beta.2) 。

    TiDB Cloud CLI は次の新機能を提供します。

    -   [`ticloud serverless sql-user`](/tidb-cloud/ticloud-serverless-sql-user-create.md)経由で[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの SQL ユーザー管理をサポートします。
    -   [`ticloud serverless create`](/tidb-cloud/ticloud-cluster-create.md)および[`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md)の[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのパブリック エンドポイントを無効にすることを許可します。
    -   OAuth 認証を使用するときに現在のユーザーに関する情報を取得するための[`ticloud auth whoami`](/tidb-cloud/ticloud-auth-whoami.md)コマンドを追加します。
    -   ソース テーブルを柔軟に選択するために、 [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)の`--sql` `--where`フラグ`--filter`サポートします。
    -   CSV および Parquet ファイルへのデータのエクスポートをサポートします。
    -   ロール ARN を認証情報として使用して Amazon S3 へのデータのエクスポートをサポートし、Google Cloud Storage および Azure Blob Storage へのエクスポートもサポートします。
    -   Amazon S3、Google Cloud Storage、Azure Blob Storage からのデータのインポートをサポートします。
    -   ブランチと特定のタイムスタンプからブランチを作成することをサポートします。

    TiDB Cloud CLI では次の機能が強化されています。

    -   デバッグログを改善しました。資格情報とユーザーエージェントをログに記録できるようになりました。
    -   ローカルエクスポートファイルのダウンロードを毎秒数十 KiB から毎秒数十 MiB に高速化します。

    TiDB Cloud CLI では、次の機能が置き換えられたり、削除されます。

    -   `--s3.bucket-uri`フラグは[`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)では`--s3.uri`に置き換えられます。
    -   [`ticloud serverless export create`](/tidb-cloud/ticloud-serverless-export-create.md)では`--database`と`--table`フラグが削除されました。代わりに`--sql` 、 `--where` 、 `--filter`フラグを使用できます。
    -   [`ticloud serverless update`](/tidb-cloud/ticloud-serverless-update.md)注釈フィールドを更新できなくなりました。

## 2024年9月10日 {#september-10-2024}

**一般的な変更**

-   TiDB Cloudパートナー Web コンソールとオープン API を起動して、 TiDB Cloudパートナーのリソースと課金の管理を強化します。

    マネージドサービスプロバイダー (MSP) と AWS Marketplace チャネルパートナープライベートオファー (CPPO) を介した再販業者は、 [TiDB Cloudパートナー Web コンソール](https://partner-console.tidbcloud.com/)とオープン API を活用して日常業務を効率化できるようになりました。

    詳細については[TiDB Cloudパートナー Web コンソール](/tidb-cloud/tidb-cloud-partners.md)参照してください。

## 2024年9月3日 {#september-3-2024}

**コンソールの変更**

-   [TiDB Cloudコンソール](https://tidbcloud.com/)使用してTiDB Cloud Serverless クラスターからデータをエクスポートすることをサポートします。

    これまで、 TiDB Cloud は[TiDB CloudCLI](/tidb-cloud/cli-reference.md)を使用したデータのエクスポートのみをサポートしていました。今後は、 [TiDB Cloudコンソール](https://tidbcloud.com/)でTiDB Cloud Serverless クラスターからローカルファイルや Amazon S3 にデータを簡単にエクスポートできます。

    詳細については、 [TiDB Cloud Serverlessからデータをエクスポート](/tidb-cloud/serverless-export.md)および[TiDB Cloud Serverless の外部ストレージアクセスを構成する](/tidb-cloud/serverless-external-storage.md)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの接続エクスペリエンスを強化します。

    -   **接続**ダイアログ インターフェースを改訂し、 TiDB Cloud Dedicated ユーザーに、より合理化され効率的な接続エクスペリエンスを提供します。
    -   クラスターのネットワーク構成を簡素化するために、新しいクラスター レベルの**ネットワーク**ページを導入しました。
    -   **「Security設定」**ページを新しい**「パスワード設定」**ページに置き換え、IP アクセス リスト設定を新しい**「ネットワーク」**ページに移動します。

    詳細については[TiDB Cloud専用に接続](/tidb-cloud/connect-to-tidb-cluster.md)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)および[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデータ インポート エクスペリエンスを強化します。

    -   **インポート**ページのレイアウトをより明確なレイアウトに改善します。
    -   TiDB Cloud Serverless クラスターとTiDB Cloud Dedicated クラスターのインポート手順を統合します。
    -   AWS ロール ARN 作成プロセスを簡素化し、接続のセットアップを容易にします。

    詳細については[ファイルからTiDB Cloudにデータをインポートする](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud)参照してください。

## 2024年8月20日 {#august-20-2024}

**コンソールの変更**

-   **プライベート エンドポイント接続の作成**ページのレイアウトを調整し、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで新しいプライベート エンドポイント接続を作成する際のユーザー エクスペリエンスを向上させました。

    詳細については、 [AWS のプライベートエンドポイント経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)および[Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

## 2024年8月6日 {#august-6-2024}

**一般的な変更**

-   AWS での負荷分散に対する課金の変更は[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 。

    2024年8月1日より、 TiDB Cloud Dedicatedの請求書には、 [AWS の料金変更は 2024 年 2 月 1 日から有効になります](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)に合わせたパブリックIPv4アドレスに対する新しいAWS料金が含まれます。パブリックIPv4アドレス1つあたりの料金は1時間あたり0.005ドルで、AWSでホストされるTiDB Cloud Dedicatedクラスター1つあたり月額約10ドルとなります。

    この料金は、 [請求の詳細](/tidb-cloud/tidb-cloud-billing.md#billing-details)の既存の**TiDB Cloud Dedicated - Data Transfer - Load Balancing**サービスの下に表示されます。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)から[バージョン7.5.3](https://docs.pingcap.com/tidb/v7.5/release-7.5.3)にアップグレードします。

**コンソールの変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスター サイズ構成エクスペリエンスを強化します。

    TiDB Cloud Dedicated クラスターの[**クラスタの作成**](/tidb-cloud/create-tidb-cluster.md)目と[**クラスタの変更**](/tidb-cloud/scale-tidb-cluster.md)ページ目の**「クラスタサイズ」**セクションのレイアウトを改良しました。さらに、 **「クラスタサイズ」**セクションにノードサイズの推奨ドキュメントへのリンクが追加され、適切なクラスターサイズの選択に役立ちます。

## 2024年7月23日 {#july-23-2024}

**一般的な変更**

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service) 、ベクター検索エンドポイントの自動生成をサポートします。

    テーブルに[ベクトルデータ型](/vector-search/vector-search-data-types.md)が含まれている場合は、選択した距離関数に基づいてベクトル距離を計算するベクトル検索エンドポイントを自動的に生成できます。

    この機能により、 [ディファイ](https://docs.dify.ai/guides/tools)や[GPT](https://openai.com/blog/introducing-gpts)などの AI プラットフォームとのシームレスな統合が可能になり、高度な自然言語処理と AI 機能によってアプリケーションが強化され、より複雑なタスクやインテリジェントなソリューションが実現します。

    詳細については、 [エンドポイントを自動的に生成する](/tidb-cloud/data-service-manage-endpoint.md#generate-an-endpoint-automatically)および[データアプリをサードパーティツールと統合する](/tidb-cloud/data-service-integrations.md)参照してください。

-   予算機能を導入すると、計画された経費に対する実際のTiDB Cloudコストを追跡し、予期しないコストを防止できます。

    この機能にアクセスするには、組織内で`Organization Owner`または`Organization Billing Admin`ロールに属している必要があります。

    詳細については[TiDB Cloudの予算管理](/tidb-cloud/tidb-cloud-budget.md)参照してください。

## 2024年7月9日 {#july-9-2024}

**一般的な変更**

-   [システムステータス](https://status.tidbcloud.com/)ページを拡張して、 TiDB Cloudシステムの健全性とパフォーマンスに関するより詳細な情報を提供します。

    アクセスするには、 [https://status.tidbcloud.com/](https://status.tidbcloud.com/)直接アクセスするか、右下隅の**[?]**をクリックして**[システム ステータス]**を選択し、 [TiDB Cloudコンソール](https://tidbcloud.com)を経由して移動します。

**コンソールの変更**

-   **VPC ピアリング**ページのレイアウトを改良し、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのうち[VPCピアリング接続の作成](/tidb-cloud/set-up-vpc-peering-connections.md)クラスターのユーザー エクスペリエンスを向上させます。

## 2024年7月2日 {#july-2-2024}

**一般的な変更**

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service) 、データ アプリに直接追加できる定義済みのシステム エンドポイントを含むエンドポイント ライブラリが提供されており、エンドポイント開発の労力が軽減されます。

    現在、ライブラリにはエンドポイント`/system/query`のみが含まれています。これにより、定義済みの`sql`のパラメータにSQL文を渡すだけで、任意のSQL文を実行できます。このエンドポイントにより、SQLクエリの即時実行が容易になり、柔軟性と効率性が向上します。

    詳細については[定義済みのシステムエンドポイントを追加する](/tidb-cloud/data-service-manage-endpoint.md#add-a-predefined-system-endpoint)参照してください。

-   低速クエリのデータstorageを強化します。

    [TiDB Cloudコンソール](https://tidbcloud.com)の低速クエリ アクセスはより安定し、データベースのパフォーマンスに影響を与えなくなりました。

## 2024年6月25日 {#june-25-2024}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)ベクトル検索をサポートします (ベータ版)。

    ベクター検索（ベータ版）機能は、ドキュメント、画像、音声、動画など、様々なデータタイプを対象に、セマンティックな類似性検索を実行するための高度な検索ソリューションを提供します。この機能により、開発者は使い慣れたMySQLスキルを活用して、生成型人工知能（AI）機能を備えたスケーラブルなアプリケーションを容易に構築できます。主な機能は以下のとおりです。

    -   [ベクトルデータ型](/vector-search/vector-search-data-types.md) 、 [ベクトルインデックス](/vector-search/vector-search-index.md) 、および[ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md) 。
    -   [ランチェーン](/vector-search/vector-search-integrate-with-langchain.md) [ラマインデックス](/vector-search/vector-search-integrate-with-llamaindex.md)のエコシステム[ジナAI](/vector-search/vector-search-integrate-with-jinaai-embedding.md) 。
    -   Python のプログラミング言語サポート: [SQLアルケミー](/vector-search/vector-search-integrate-with-sqlalchemy.md) 、および[Django ORM](/vector-search/vector-search-integrate-with-django-orm.md) [ピーウィー](/vector-search/vector-search-integrate-with-peewee.md)
    -   サンプルアプリケーションとチュートリアル: [パイソン](/vector-search/vector-search-get-started-using-python.md)または[SQL](/vector-search/vector-search-get-started-using-sql.md)使用してドキュメントのセマンティック検索を実行します。

    詳細については[ベクトル検索（ベータ版）の概要](/vector-search/vector-search-overview.md)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)では、組織の所有者に毎週の電子メールレポートが提供されるようになりました。

    これらのレポートは、クラスターのパフォーマンスとアクティビティに関する洞察を提供します。毎週自動的に更新されるため、クラスターに関する最新情報を常に把握し、データに基づいた意思決定を行ってクラスターを最適化できます。

-   Chat2Query API v3 エンドポイントをリリースし、Chat2Query API v1 エンドポイント`/v1/chat2data`廃止します。

    Chat2Query API v3 エンドポイントを使用すると、セッションを使用してマルチラウンドの Chat2Query を開始できます。

    詳細については[Chat2Query APIを使い始める](/tidb-cloud/use-chat2query-api.md)参照してください。

**コンソールの変更**

-   Chat2Query (ベータ) の名前を SQL Editor (ベータ) に変更します。

    以前Chat2Queryと呼ばれていたインターフェースは、SQLエディターに名称が変更されました。この変更により、手動によるSQL編集とAIによるクエリ生成の違いが明確になり、使いやすさと全体的なエクスペリエンスが向上します。

    -   **SQL エディター**: TiDB Cloudコンソールで SQL クエリを手動で記述および実行するためのデフォルトのインターフェース。
    -   **Chat2Query** : AI 支援によるテキストクエリ機能。自然言語を使用してデータベースと対話し、SQL クエリを生成、書き換え、最適化できます。

    詳細については[AI支援SQLエディターでデータを探索](/tidb-cloud/explore-data-with-chat2query.md)参照してください。

## 2024年6月18日 {#june-18-2024}

**一般的な変更**

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの 16 vCPU TiFlashと 32 vCPU TiFlashの最大ノードstorageを 2048 GiB から 4096 GiB に増加しました。

    この機能強化により、 TiDB Cloud Dedicated クラスターの分析データstorage容量が増加し、ワークロードのスケーリング効率が向上し、増大するデータ要件に対応できるようになります。

    詳細については[TiFlashノードstorage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)参照してください。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1)から[バージョン7.5.2](https://docs.pingcap.com/tidb/v7.5/release-7.5.2)にアップグレードします。

## 2024年6月4日 {#june-4-2024}

**一般的な変更**

-   AWS にデプロイされた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの災害復旧用のリカバリ グループ機能 (ベータ版) を導入します。

    この機能により、 TiDB Cloud Dedicated クラスタ間でデータベースを複製し、地域災害発生時の迅速な復旧を実現できます。1 ロール`Project Owner`場合は、新しいリカバリグループを作成し、データベースをそのグループに割り当てることで、この機能を有効にできます。リカバリグループを使用してデータベースを複製することで、災害対策を強化し、より厳格な可用性 SLA を満たし、より厳格な復旧ポイント目標 (RPO) と復旧時間目標 (RTO) を達成できます。

    詳細については[回復グループを始める](/tidb-cloud/recovery-group-get-started.md)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)列storage[TiFlash](/tiflash/tiflash-overview.md)課金と計測 (ベータ版) を導入します。

    2024年6月30日まで、 TiDB Cloud Serverlessクラスターの列指向storageは100%割引で無料のままです。この日以降は、各TiDB Cloud Serverlessクラスターに列指向storage用の5GiBの無料割り当てが付与されます。無料割り当てを超えた使用量については課金されます。

    詳細については[TiDB Cloud Serverless の価格詳細](https://www.pingcap.com/tidb-serverless-pricing-details/#storage)参照してください。

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) [存続時間（TTL）](/time-to-live.md)サポートします。

## 2024年5月28日 {#may-28-2024}

**一般的な変更**

-   Google Cloud `Taiwan (asia-east1)`リージョンは[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)機能をサポートしています。

    Google Cloud `Taiwan (asia-east1)`リージョンでホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタが、データ移行（DM）機能をサポートするようになりました。アップストリームデータがこのリージョン内またはその付近に保存されている場合、Google Cloud からTiDB Cloudへのより高速で信頼性の高いデータ移行を活用できるようになります。

-   AWSとGoogle Cloudでホストされる[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのうち[TiDBノードサイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)を提供する： `16 vCPU, 64 GiB`

**APIの変更**

-   以下のリソースを自動的かつ効率的に管理するためのTiDB Cloudデータ サービス API を導入します。

    -   **データ アプリ**: 特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのコレクション。
    -   **データ ソース**: データの操作と取得のためにデータ アプリにリンクされたクラスター。
    -   **エンドポイント**: SQL ステートメントを実行するためにカスタマイズできる Web API。
    -   **データ API キー**: 安全なエンドポイント アクセスに使用されます。
    -   **OpenAPI 仕様**: データ サービスは、各データ アプリの OpenAPI 仕様 3.0 の生成をサポートしており、これにより標準化された形式でエンドポイントと対話できるようになります。

    これらのTiDB Cloudデータ サービス API エンドポイントは、TiDB TiDB Cloud TiDB Cloud API v1beta1 でリリースされています。

    詳細については[APIドキュメント（v1beta1）](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)参照してください。

## 2024年5月21日 {#may-21-2024}

**一般的な変更**

-   Google Cloud でホストされる[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタのうち[TiDBノードサイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)新規に提供します: `8 vCPU, 16 GiB`

## 2024年5月14日 {#may-14-2024}

**一般的な変更**

-   さまざまな地域の顧客にさらに対応できるよう、セクション[**タイムゾーン**](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)のタイムゾーンの選択範囲を拡張します。

-   VPC がTiDB Cloudの VPC とは異なるリージョンにある場合は、 [VPCピアリングの作成](/tidb-cloud/set-up-vpc-peering-connections.md)サポートします。

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service)クエリ パラメータとともにパス パラメータをサポートします。

    この機能により、構造化 URL によるリソース識別が強化され、ユーザー エクスペリエンス、検索エンジン最適化 (SEO)、クライアント統合が改善され、開発者に柔軟性の向上と業界標準への適合性が提供されます。

    詳細については[基本的なプロパティ](/tidb-cloud/data-service-manage-endpoint.md#basic-properties)参照してください。

## 2024年4月16日 {#april-16-2024}

**CLIの変更**

-   新しい[TiDB CloudAPI](/tidb-cloud/api-overview.md)をベースにした[TiDB CloudCLI 1.0.0-beta.1](https://github.com/tidbcloud/tidbcloud-cli)導入します。新しい CLI には、以下の新機能が追加されています。

    -   [TiDB Cloud Serverless クラスターからデータをエクスポートする](/tidb-cloud/serverless-export.md)
    -   [ローカルstorageからTiDB Cloud Serverless クラスターにデータをインポートする](/tidb-cloud/ticloud-import-start.md)
    -   [OAuth による認証](/tidb-cloud/ticloud-auth-login.md)
    -   [TiDB Bot 経由で質問する](/tidb-cloud/ticloud-ai.md)

    TiDB Cloud CLIをアップグレードする前に、この新しいCLIは以前のバージョンと互換性がないことにご注意ください。例えば、CLIコマンドの`ticloud cluster` `ticloud serverless`に更新されました。詳細については、 [TiDB Cloud CLI リファレンス](/tidb-cloud/cli-reference.md)ご覧ください。

## 2024年4月9日 {#april-9-2024}

**一般的な変更**

-   AWS でホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して新しい[TiDBノードサイズ](/tidb-cloud/size-your-cluster.md#tidb-vcpu-and-ram)を指定します: `8 vCPU, 32 GiB` 。

## 2024年4月2日 {#april-2-2024}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに対して、**無料**と**スケーラブルの**2 つのサービス プランを導入します。

    TiDB Cloud Serverlessは、様々なユーザーニーズに対応するため、無料かつスケーラブルなサービスプランを提供しています。初めてご利用になる場合でも、増大するアプリケーション需要に合わせて拡張する場合でも、これらのプランは必要な柔軟性と機能を提供します。

    詳細については[クラスタプラン](/tidb-cloud/select-cluster-tier.md#cluster-plans)参照してください。

-   TiDB Cloud Serverless クラスターの使用量制限に達した際のスロットリング動作を変更しました。これにより、クラスターが使用量制限に達すると、新規接続の試行が直ちに拒否され、既存のオペレーションのサービスが中断されることはありません。

    詳細については[使用量制限](/tidb-cloud/serverless-limitations.md#usage-quota)参照してください。

## 2024年3月5日 {#march-5-2024}

**一般的な変更**

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)から[バージョン7.5.1](https://docs.pingcap.com/tidb/v7.5/release-7.5.1)にアップグレードします。

**コンソールの変更**

-   [**請求する**](https://tidbcloud.com/org-settings/billing/payments)ページに**Cost Explorer**タブを導入します。このタブには、組織のコスト レポートを長期にわたって分析およびカスタマイズするための直感的なインターフェイスが提供されます。

    この機能を使用するには、組織の**請求**ページに移動し、 **Cost Explorer**タブをクリックします。

    詳細については[コストエクスプローラー](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)参照してください。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) [ノードレベルのリソースメトリック](/tidb-cloud/built-in-monitoring.md#server)の**制限**ラベルを表示します。

    **制限**ラベルは、クラスター内の各コンポーネントのCPU、メモリ、storageなどのリソースの最大使用量を示します。この機能強化により、クラスターのリソース使用率の監視プロセスが簡素化されます。

    これらのメトリック制限にアクセスするには、クラスターの**[監視]**ページに移動し、[**メトリック]**タブの**[サーバー]**カテゴリを確認します。

    詳細については[TiDB Cloud Dedicated クラスタのメトリクス](/tidb-cloud/built-in-monitoring.md#server)参照してください。

## 2024年2月21日 {#february-21-2024}

**一般的な変更**

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの TiDB バージョンを[バージョン6.6.0](https://docs.pingcap.com/tidb/v6.6/release-6.6.0)から[バージョン7.1.3](https://docs.pingcap.com/tidb/v7.1/release-7.1.3)にアップグレードします。

## 2024年2月20日 {#february-20-2024}

**一般的な変更**

-   Google Cloud 上でさらに多くのTiDB Cloudノードの作成をサポートします。

    -   Google Cloud の[リージョンCIDRサイズの設定](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) of `/19`では、プロジェクトの任意のリージョン内に最大 124 個のTiDB Cloudノードを作成できるようになりました。
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

    注: プロジェクトの以前のグローバルレベルのCIDR設定は廃止されますが、アクティブな状態にある既存のリージョンCIDRはすべて影響を受けません。既存のクラスタのネットワークには影響はありません。

    詳細については[リージョンのCIDRを設定する](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)参照してください。

-   TiDB Cloud Serverless ユーザーは、クラスターのパブリック エンドポイントを無効にできるようになりました。

    詳細については[パブリックエンドポイントを無効にする](/tidb-cloud/connect-via-standard-connection-serverless.md#disable-a-public-endpoint)参照してください。

-   [データサービス（ベータ版）](https://tidbcloud.com/project/data-service) 、データ アプリ内のエンドポイントにアクセスするためのカスタム ドメインの構成がサポートされています。

    TiDB Cloud Data Service は、デフォルトで各データアプリのエンドポイントにアクセスするためのドメイン`<region>.data.tidbcloud.com`提供します。パーソナライズと柔軟性を高めるため、デフォルトドメインの代わりにデータアプリにカスタムドメインを設定できるようになりました。この機能により、データベースサービスにブランド化された URL を使用でき、セキュリティが強化されます。

    詳細については[データサービスにおけるカスタムドメイン](/tidb-cloud/data-service-custom-domain.md)参照してください。

## 2024年1月3日 {#january-3-2024}

**一般的な変更**

-   エンタープライズ認証プロセスを合理化するために[組織のSSO](https://tidbcloud.com/org-settings/authentication)サポートします。

    この機能を使用すると、 [Securityアサーションマークアップ言語（SAML）](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)または[OpenIDコネクト（OIDC）](https://openid.net/developers/how-connect-works/)使用して、 TiDB Cloud を任意の ID プロバイダー (IdP) とシームレスに統合できます。

    詳細については[組織のSSO認証](/tidb-cloud/tidb-cloud-org-sso-authentication.md)参照してください。

-   新しい[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン7.1.1](https://docs.pingcap.com/tidb/v7.1/release-7.1.1)から[バージョン7.5.0](https://docs.pingcap.com/tidb/v7.5/release-7.5.0)にアップグレードします。

-   [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のデュアルリージョン バックアップ機能が一般提供 (GA) になりました。

    この機能を使用すると、AWS または Google Cloud 内の地理的リージョン間でバックアップを複製できます。これにより、データ保護と災害復旧機能がさらにレイヤーされます。

    詳細については[デュアルリージョンバックアップ](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)参照してください。
