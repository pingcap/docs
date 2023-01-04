---
title: TiDB Cloud Release Notes in 2022
summary: Learn about the release notes of TiDB Cloud in 2022.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2022 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2022}

このページでは、2022 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートを一覧表示します。

## 2022 年 10 月 28 日 {#october-28-2022}

-   Developer Tierは[サーバーレス層](/tidb-cloud/select-cluster-tier.md#serverless-tier)にアップグレードされます。 TiDB の完全マネージド型の自動スケーリング デプロイメントであるサーバーレス層が利用可能になりました。まだベータ版であり、無料で使用できます。

    -   Serverless Tier クラスターには、 Dedicated Tierクラスターとして完全に機能する HTAP 機能が引き続き含まれています。
    -   Serverless Tier は、クラスターの作成時間と瞬時のコールド スタート時間を短縮します。 Developer Tierと比較すると、作成時間が数分から数秒に短縮されます。
    -   展開トポロジについて心配する必要はありません。 Serverless Tier は、リクエストに応じて自動的に調整されます。
    -   サーバーレス ティア[セキュリティのためにクラスタへの TLS 接続を強制します](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md) .
    -   既存のDeveloper Tierクラスターは、今後数か月で Serverless Tier に自動的に移行されます。クラスターを使用する能力に影響はなく、ベータ版の Serverless Tier クラスターの使用に対して課金されることはありません。

    始めましょう[ここ](/tidb-cloud/tidb-cloud-quickstart.md) .

## 2022 年 10 月 25 日 {#october-25-2022}

**一般的な変更**

-   TiDB システム変数のサブセットの動的な変更と永続化をサポートします (ベータ版)。

    標準の SQL ステートメントを使用して、サポートされているシステム変数に新しい値を設定できます。

    ```sql
    SET [GLOBAL|SESSION] <variable>
    ```

    例えば：

    ```sql
    SET GLOBAL tidb_committer_concurrency = 127;
    ```

    変数が`GLOBAL`レベルで設定されている場合、変数はクラスターに適用され、永続的になります (サーバーを再起動またはリロードした後でも有効なままになります)。 `SESSION`レベルの変数は永続的ではなく、現在のセッションでのみ有効です。

    **この機能はまだベータ版**であり、限られた数の変数のみがサポートされています。副作用の不確実性のため、他の[システム変数](/system-variables.md)を変更することはお勧めしません。 TiDB v6.1 に基づいてサポートされているすべての変数については、次のリストを参照してください。

    -   [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)
    -   [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)
    -   [`tidb_enable_batch_dml`](/system-variables.md#tidb_enable_batch_dml)
    -   [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)
    -   [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)
    -   [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    -   [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    -   [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)
    -   [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターのデフォルトの TiDB バージョンを[v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1)から[v6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2)にアップグレードします。

## 2022 年 10 月 19 日 {#october-19-2022}

**統合の変更**

-   [TiDB Cloud Vercel 統合](https://vercel.com/integrations/tidb-cloud) in [Vercel 統合マーケットプレイス](https://vercel.com/integrations#databases)を公開します。

    [ヴェルセル](https://vercel.com)はフロントエンド開発者向けのプラットフォームであり、イノベーターがひらめいた瞬間に作成するために必要なスピードと信頼性を提供します。 TiDB Cloud Vercel Integration を使用すると、Vercel プロジェクトをTiDB Cloudクラスターに簡単に接続できます。詳しくは資料[TiDB Cloudと Vercel の統合](/tidb-cloud/integrate-tidbcloud-with-vercel.md)をご覧ください。

-   [TiDB Cloudスターター テンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter) in [ヴェルセル テンプレート一覧](https://vercel.com/templates)を公開します。

    このテンプレートを最初に使用して、Vercel とTiDB Cloudを試すことができます。このテンプレートを使用する前に、まず[TiDB Cloudクラスターにデータをインポートする](https://github.com/pingcap/tidb-prisma-vercel-demo#2-import-table-structures-and-data)を行う必要があります。

## 2022 年 10 月 18 日 {#october-18-2022}

**一般的な変更**

-   Dedicated Tierクラスターの場合、TiKV またはTiFlashノードの最小ストレージ サイズが 500 GiB から 200 GiB に変更されました。これは、ワークロードが少量のデータ ボリュームであるユーザーにとって、より費用対効果が高くなります。

    詳細については、 [TiKV ノード ストレージ](/tidb-cloud/size-your-cluster.md#tikv-node-storage)および[TiFlashノード ストレージ](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)を参照してください。

-   オンライン契約を導入して、 TiDB Cloudサブスクリプションをカスタマイズし、コンプライアンス要件を満たします。

    TiDB Cloudコンソールの**Billing**ページに[**契約**タブ](/tidb-cloud/tidb-cloud-billing.md#contract)が追加されます。契約に関する当社の販売に同意し、オンラインで契約を処理するための電子メールを受け取った場合は、[契約] タブに移動して<strong>契約</strong>を確認し、同意することができます。コントラクトの詳細については、お気軽に[営業担当にお問い合わせください](https://www.pingcap.com/contact-us/)までお問い合わせください。

**ドキュメントの変更**

-   [TiDB Cloud Terraform プロバイダー](https://registry.terraform.io/providers/tidbcloud/tidbcloud)に[ドキュメンテーション](/tidb-cloud/terraform-tidbcloud-provider-overview.md)を追加します。

    TiDB Cloud Terraform Provider は、 [テラフォーム](https://www.terraform.io/)を使用してクラスター、バックアップ、復元などのTiDB Cloudリソースを管理できるようにするプラグインです。リソースのプロビジョニングとインフラストラクチャのワークフローを自動化する簡単な方法を探している場合は、 [ドキュメンテーション](/tidb-cloud/terraform-tidbcloud-provider-overview.md)に従ってTiDB Cloud Terraform Provider を試すことができます。

## 2022 年 10 月 11 日 {#october-11-2022}

**一般的な変更**

-   新しい[Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier)クラスターのデフォルトの TiDB バージョンを[v6.2.0](https://docs.pingcap.com/tidb/v6.2/release-6.2.0)から[v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)にアップグレードします。

**コンソールの変更**

-   [請求詳細ページ](/tidb-cloud/tidb-cloud-billing.md#billing-details)の請求情報を最適化します。

    -   **[サービスごとの概要]**セクションで、ノード レベルでより詳細な課金情報を提供します。
    -   **使用状況の詳細**セクションを追加します。使用状況の詳細を CSV ファイルとしてダウンロードすることもできます。

## 2022 年 9 月 27 日 {#september-27-2022}

**一般的な変更**

-   招待による複数の組織への参加をサポートします。

    TiDB Cloudコンソールでは、参加しているすべての組織を表示し、それらを切り替えることができます。詳細については、 [組織を切り替える](/tidb-cloud/manage-user-access.md#switch-between-organizations)を参照してください。

-   SQL診断用の[スロークエリ](/tidb-cloud/tune-performance.md#slow-query)ページを追加。

    スロー クエリ ページでは、TiDB クラスター内のすべてのスロー クエリを検索して表示し、その[実行計画](https://docs.pingcap.com/tidbcloud/explain-overview) 、SQL 実行情報、およびその他の詳細を表示して、各スロー クエリのボトルネックを調べることができます。

-   アカウントのパスワードをリセットすると、 TiDB Cloudは新しいパスワードの入力を最近の 4 つのパスワードと照合してチェックし、それらのいずれも使用しないように通知します。 4 つの使用済みパスワードのいずれも許可されません。

    詳細については、 [ユーザーのパスワードを管理する](/tidb-cloud/manage-user-access.md#manage-user-passwords)を参照してください。

## 2022 年 9 月 20 日 {#september-20-2022}

**一般的な変更**

-   セルフサービス ユーザー向けに[コスト クォータ ベースの請求書](/tidb-cloud/tidb-cloud-billing.md#invoices)を紹介します。

    コストがクォータに達すると、 TiDB Cloudは請求書を生成します。クォータを引き上げる、または毎月の請求書を受け取るには、 [私たちの販売](https://www.pingcap.com/contact-us/)にお問い合わせください。

-   データバックアップ費用からストレージ運用費を免除します。最新の価格情報については、 [TiDB Cloudの価格詳細](https://www.pingcap.com/tidb-cloud-pricing-details/)を参照してください。

**コンソールの変更**

-   データ インポート用の新しい Web UI を提供します。新しい UI により、ユーザー エクスペリエンスが向上し、データのインポートがより効率的になります。

    新しい UI を使用すると、インポートするデータをプレビューしたり、インポート プロセスを表示したり、すべてのインポート タスクを簡単に管理したりできます。

**API の変更**

-   TiDB Cloud API (ベータ版) は、すべてのユーザーが利用できるようになりました。

    TiDB Cloudコンソールで API キーを作成することにより、API の使用を開始できます。詳細については、 [API ドキュメント](/tidb-cloud/api-overview.md)を参照してください。

## 2022 年 9 月 15 日 {#september-15-2022}

**一般的な変更**

-   TLS を介したTiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターへの接続をサポートします。

    Dedicated Tierクラスターの場合、 [接続](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection)ダイアログの [**標準接続**] タブに、TiDB クラスター CA をダウンロードするためのリンクが表示され、TLS 接続の接続文字列とサンプル コードも表示されるようになりました。サードパーティの MySQL クライアント、MyCLI、および JDBC、Python、Go、Node.js などのアプリケーション用の複数の接続方法を使用でき[TLS 経由でDedicated Tierクラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) 。この機能により、アプリケーションから TiDB クラスターへのデータ転送のセキュリティが確保されます。

## 2022 年 9 月 14 日 {#september-14-2022}

**コンソールの変更**

-   [クラスター](https://tidbcloud.com/console/clusters)ページとクラスター概要ページの UI を最適化して、ユーザー エクスペリエンスを向上させます。

    新しいデザインでは、 Dedicated Tierへのアップグレード、クラスター接続、およびデータ インポートの入り口が強調されています。

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier)クラスタの Playground を導入します。

    Playground には、事前にロードされた GitHub イベントのデータセットが含まれています。これにより、データをインポートしたり、クライアントに接続したりすることなく、クエリを即座に実行してTiDB Cloudを開始できます。

## 2022 年 9 月 13 日 {#september-13-2022}

**一般的な変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタの新しい Google Cloud リージョンをサポート: `N. Virginia (us-east4)` .

## 2022 年 9 月 9 日 {#september-9-2022}

**一般的な変更**

-   Datadog でDedicated Tierクラスターの[より多くの指標](/tidb-cloud/monitor-datadog-integration.md#metrics-available-to-datadog)を提供して、クラスターのパフォーマンス ステータスをよりよく理解できるようにします。

    [TiDB Cloudと Datadog の統合](/tidb-cloud/monitor-datadog-integration.md)の場合、これらのメトリクスを Datadog ダッシュボードで直接表示できます。

## 2022 年 9 月 6 日 {#september-6-2022}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターのデフォルトの TiDB バージョンを[v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)から[v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1)にアップグレードします。

**コンソールの変更**

-   これで、 TiDB Cloudコンソールの右上隅にあるエントリから[PoCを申し込む](/tidb-cloud/tidb-cloud-poc.md)できるようになりました。

**API の変更**

-   [TiDB CloudAPI](/tidb-cloud/api-overview.md)を介して TiKV またはTiFlashノードのストレージを増やすことをサポートします。 API エンドポイントの`storage_size_gib`フィールドを使用して、スケーリングを行うことができます。

    現在、 TiDB Cloud API はまだベータ版であり、リクエストがあった場合にのみ利用できます。

    詳細については、 [Dedicated Tierクラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)を参照してください。

## 2022 年 8 月 30 日 {#august-30-2022}

**一般的な変更**

-   TiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの新しいネットワーク アクセス管理オプションとして、AWS PrivateLink を利用したエンドポイント接続をサポートします。

    エンドポイント接続は安全でプライベートであり、データを公共のインターネットに公開しません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

    詳細については、 [プライベート エンドポイント接続のセットアップ](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)のクラスターの[接続](/tidb-cloud/connect-to-tidb-cluster.md)のダイアログの [ **VPC Peering** ] タブと [ <strong>Private Endpoint</strong> ] タブで、MySQL、MyCLI、JDBC、Python、Go、および Node.js のサンプル接続文字列を提供します。

    接続コードをコピーしてアプリに貼り付けるだけで、 Dedicated Tierクラスターに簡単に接続できます。

## 2022 年 8 月 24 日 {#august-24-2022}

**一般的な変更**

-   Dedicated Tierクラスターの一時停止または再開をサポートします。

    TiDB Cloudで[Dedicated Tierクラスターを一時停止または再開する](/tidb-cloud/pause-or-resume-tidb-cluster.md)できます。クラスターが一時停止されている場合、ノード コンピューティング コストは課金されません。

## 2022 年 8 月 23 日 {#august-23-2022}

**一般的な変更**

-   新しい[Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier)クラスターのデフォルトの TiDB バージョンを[v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)から[v6.2.0](https://docs.pingcap.com/tidb/v6.2/release-6.2.0)にアップグレードします。

**API の変更**

-   TiDB Cloud API をベータ版として導入。

    この API を通じて、クラスターなどのTiDB Cloudリソースを自動的かつ効率的に管理できます。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

    現在、 TiDB Cloud API はまだベータ版であり、リクエストがあった場合にのみ利用できます。リクエストを送信して、API アクセスを申請できます。

    -   [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)の右下隅にある [**ヘルプ]**をクリックします。
    -   ダイアログで、[**説明**] フィールドに「 TiDB Cloud API に申し込む」と入力し、[<strong>送信</strong>] をクリックします。

## 2022 年 8 月 16 日 {#august-16-2022}

-   ベータとして TiDB と TiKV の`2 vCPU, 8 GiB (Beta)`ノード サイズを追加します。

    -   `2 vCPU, 8 GiB (Beta)`つの TiKV ノードごとに、ストレージ サイズは 200 GiB から 500 GiB の間です。

    -   推奨される使用シナリオ:

        -   SMB 向けの低ワークロード本番環境
        -   PoC とステージング環境
        -   開発環境

-   PoC ユーザー向けに[クレジット](/tidb-cloud/tidb-cloud-billing.md#credits) (以前はトレイル ポイントと呼ばれていました) を導入します。

    [**請求**] ページの [<strong>クレジット</strong>] タブで、組織のクレジットに関する情報を表示できるようになりました。クレジットは、 TiDB Cloud料金の支払いに使用できます。 [お問い合わせ](https://en.pingcap.com/apply-for-poc/)クレジットを獲得できます。

## 2022 年 8 月 9 日 {#august-9-2022}

-   GCP リージョン`Osaka` for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタ作成のサポートを追加します。

## 2022 年 8 月 2 日 {#august-2-2022}

-   TiDB と TiKV の`4 vCPU, 16 GiB`ノード サイズは、一般提供 (GA) になりました。

    -   `4 vCPU, 16 GiB` TiKV ノードごとに、ストレージ サイズは 200 GiB から 2 TiB です。
    -   推奨される使用シナリオ:

        -   SMB 向けの低ワークロード本番環境
        -   PoC とステージング環境
        -   開発環境

-   [Dedicated Tierクラスター](/tidb-cloud/select-cluster-tier.md#dedicated-tier)の [**診断**] タブに[モニタリングページ](/tidb-cloud/built-in-monitoring.md)を追加します。

    [監視] ページには、全体的なパフォーマンス診断のためのシステム レベルのエントリが表示されます。トップダウンのパフォーマンス分析方法に従って、監視ページは、データベース時間の内訳に基づいて TiDB パフォーマンス メトリックを整理し、これらのメトリックを異なる色で表示します。これらの色をチェックすることで、システム全体のパフォーマンスのボトルネックを一目で特定できるため、パフォーマンスの診断時間が大幅に短縮され、パフォーマンスの分析と診断が簡素化されます。

-   CSV および Parquet ソース ファイルの [**データ インポート]**ページで<strong>カスタム パターン</strong>を有効または無効にするスイッチを追加します。

    **カスタム パターン**機能はデフォルトで無効になっています。ファイル名が特定のパターンに一致する CSV ファイルまたは Parquet ファイルを単一のターゲット テーブルにインポートするときに、これを有効にすることができます。

    詳細については、 [CSV ファイルのインポート](/tidb-cloud/import-csv-files.md)および[Apache Parquet ファイルのインポート](/tidb-cloud/import-parquet-files.md)を参照してください。

-   TiDB Cloudサポート プラン (Basic、Standard、Enterprise、Premium) を追加して、お客様の組織のさまざまなサポート ニーズに対応します。詳細については、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)を参照してください。

-   [クラスター](https://tidbcloud.com/console/clusters)ページとクラスターの詳細ページの UI を最適化します。

    -   [**接続**] ボタンと [<strong>データのインポート]</strong>ボタンを [<strong>クラスター]</strong>ページに追加します。
    -   [**接続**] ボタンと [<strong>データのインポート]</strong>ボタンをクラスターの詳細ページの右上隅に移動します。

## 2022 年 7 月 28 日 {#july-28-2022}

-   **[どこからでもアクセスを許可]**ボタンを [<strong>セキュリティ クイック スタート</strong>] ダイアログに追加します。これにより、任意の IP アドレスからクラスターにアクセスできるようになります。詳細については、 [クラスタセキュリティ設定の構成](/tidb-cloud/configure-security-settings.md)を参照してください。

## 2022 年 7 月 26 日 {#july-26-2022}

-   新しい[Developer Tierのクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier)の自動ハイバネーションと再開をサポートします。

    Developer Tierクラスターは、7 日間非アクティブになった後も削除されないため、1 年間の無料試用期間が終了するまでいつでも使用できます。非アクティブ状態が 24 時間続くと、 Developer Tierクラスターは自動的に休止状態になります。クラスターを再開するには、クラスターに新しい接続を送信するか、 TiDB Cloudコンソールの [**再開**] ボタンをクリックします。クラスターは 50 秒以内に再開され、自動的にサービスに戻ります。

-   new [Developer Tierのクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier)のユーザー名プレフィックス制限を追加します。

    データベース ユーザー名を使用または設定するときは常に、クラスターのプレフィックスをユーザー名に含める必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

-   [Developer Tierのクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier)のバックアップおよび復元機能を無効にします。

    Developer Tierクラスターでは、バックアップと復元の機能 (自動バックアップと手動バックアップの両方を含む) が無効になっています。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用して、データをバックアップとしてエクスポートできます。

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier)クラスターのストレージ サイズを 500 MiB から 1 GiB に増やします。

-   パンくずリストをTiDB Cloudコンソールに追加して、ナビゲーション エクスペリエンスを向上させます。

-   データをTiDB Cloudにインポートするときに、複数のフィルター ルールの構成をサポートします。

-   **Project Settings**から<strong>Traffic Filters</strong>ページを削除し、 <strong>Connect to TiDB</strong>ダイアログから<strong>Add Rules from Default Set</strong>ボタンを削除します。

## 2022 年 7 月 19 日 {#july-19-2022}

-   [TiKV ノードサイズ](/tidb-cloud/size-your-cluster.md#tikv-node-size) : `8 vCPU, 32 GiB`の新しいオプションを提供します。 8 vCPU TiKV ノードの場合は、 `8 vCPU, 32 GiB`または`8 vCPU, 64 GiB`のいずれかを選択できます。
-   [**TiDB に接続する**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection)ダイアログで提供されるサンプル コードで構文の強調表示をサポートし、コードの読みやすさを向上させます。サンプル コードで置き換える必要のあるパラメーターを簡単に特定できます。
-   [**データ インポート タスク**](/tidb-cloud/import-sample-data.md)ページでインポート タスクを確認した後、 TiDB Cloudがソース データにアクセスできるかどうかの自動検証をサポートします。
-   TiDB Cloudコンソールのテーマの色を変更して、 [PingCAP ウェブサイト](https://en.pingcap.com/)の色と一致させます。

## 2022 年 7 月 12 日 {#july-12-2022}

-   Amazon S3 の[**データ インポート タスク**](/tidb-cloud/import-sample-data.md)ページに [**検証**] ボタンを追加すると、データのインポートが開始される前にデータ アクセスの問題を検出できます。
-   [**支払方法**](/tidb-cloud/tidb-cloud-billing.md#payment-method)タブの下に**課金プロファイル**を追加します。<strong>請求プロファイル</strong>で税務登録番号を提供することにより、特定の税金が請求書から免除される場合があります。詳細については、 [請求プロファイル情報の編集](/tidb-cloud/tidb-cloud-billing.md#edit-billing-profile-information)を参照してください。

## 2022 年 7 月 5 日 {#july-05-2022}

-   カラムナ ストレージ[TiFlash](/tiflash/tiflash-overview.md)は、一般提供 (GA) になりました。

    -   TiFlashにより、TiDB は本質的に Hybrid Transactional/Analytical Processing (HTAP) データベースになります。アプリケーション データはまず TiKV に保存され、次にRaftコンセンサス アルゴリズムを介してTiFlashに複製されます。つまり、行ストレージから列ストレージへのリアルタイム レプリケーションです。
    -   TiFlashレプリカを含むテーブルの場合、TiDB オプティマイザーは、コストの見積もりに基づいて、TiKV またはTiFlashレプリカのどちらを使用するかを自動的に決定します。

    TiFlashがもたらす利点を体験するには、 [TiDB CloudHTAP クイック スタート ガイド](/tidb-cloud/tidb-cloud-htap-quickstart.md)を参照してください。

-   Dedicated Tierクラスターの TiKV とTiFlashの[ストレージサイズの増加](/tidb-cloud/scale-tidb-cluster.md#increase-node-storage)をサポートします。

-   ノード サイズ フィールドにメモリ情報を表示できるようになりました。

## 2022 年 6 月 28 日 {#june-28-2022}

-   TiDB Cloud Dedicated Tierを[TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1)から[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。

## 2022 年 6 月 23 日 {#june-23-2022}

-   TiDB Cloudの最大値を[TiKVのストレージ容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage)増やします。

    -   8 vCPU または 16 vCPU TiKV: 最大 4 TiB のストレージ容量をサポートします。
    -   4 vCPU TiKV: 最大 2 TiB のストレージ容量をサポートします。

## 2022 年 6 月 21 日 {#june-21-2022}

-   GCP リージョン`Taiwan` for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタ作成のサポートを追加します。
-   TiDB Cloudコンソールでサポート[ユーザー プロファイルの更新](/tidb-cloud/manage-user-access.md#manage-user-profiles) (名、最終時間、会社名、国、電話番号を含む)。
-   [**TiDB に接続する**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection)ダイアログで MySQL、MyCLI、JDBC、Python、Go、および Node.js の接続文字列を指定して、TiDB クラスターに簡単に接続できるようにします。
-   データのインポート中にバケット URI からバケット領域を自動的に取得することをサポートして、そのような情報を入力する手間を省きます。

## 2022 年 6 月 16 日 {#june-16-2022}

-   [クラスタ作成プロセス](/tidb-cloud/create-tidb-cluster.md)を単純化します。

    -   クラスターを作成すると、 TiDB Cloudはデフォルトのクラスター名を提供します。デフォルト名を使用することも、更新することもできます。
    -   クラスターを作成する場合、[クラスターの**クラスタ]**ページでパスワードを設定する必要はありません。
    -   クラスターの作成中または作成後に、[**セキュリティ クイック スタート**] ダイアログ ボックスで、クラスターにアクセスするためのルート パスワードと、クラスターに接続するための IP アドレスを設定できます。

## 2022 年 6 月 14 日 {#june-14-2022}

-   TiDB CloudをDeveloper Tierの[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。
-   **Project Settings**の入り口を最適化します。 TiDB Cloudコンソールから、ターゲット プロジェクトを選択し、[ <strong>Project Settings</strong> ] タブをクリックして簡単にその設定に移動できます。
-   TiDB Cloudコンソールで有効期限メッセージを提供することにより、パスワード有効期限のエクスペリエンスを最適化します。

## 2022 年 6 月 7 日 {#june-7-2022}

-   [無料で試す](https://tidbcloud.com/free-trial)登録ページを追加して、 TiDB Cloudにすばやくサインアップします。
-   プラン選択ページから**概念実証プラン**オプションを削除します。 14日間の無料PoCトライアルを申し込む場合は、 [PoCに申し込む](https://en.pingcap.com/apply-for-poc/)ページへ。詳細については、 [TiDB Cloudで概念実証 (PoC) を実行する](/tidb-cloud/tidb-cloud-poc.md)を参照してください。
-   電子メールとパスワードを使用してTiDB Cloudにサインアップするユーザーに、90 日ごとにパスワードをリセットするよう求めることで、システムのセキュリティを向上させます。詳細については、 [ユーザーのパスワードを管理する](/tidb-cloud/manage-user-access.md#manage-user-passwords)を参照してください。

## 2022 年 5 月 24 日 {#may-24-2022}

-   Dedicated Tierクラスターを[作成](/tidb-cloud/create-tidb-cluster.md)または[戻す](/tidb-cloud/backup-and-restore.md#restore)使用する場合の TiDB ポート番号のカスタマイズをサポートします。

## 2022 年 5 月 19 日 {#may-19-2022}

-   AWS リージョン`Frankfurt` for [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier)クラスター作成のサポートを追加します。

## 2022 年 5 月 18 日 {#may-18-2022}

-   GitHub アカウントで[サインアップ](https://tidbcloud.com/signup)つのTiDB Cloudをサポートします。

## 2022 年 5 月 13 日 {#may-13-2022}

-   Google アカウントで[サインアップ](https://tidbcloud.com/signup)つのTiDB Cloudをサポートします。

## 2022 年 5 月 1 日 {#may-1-2022}

-   [作成](/tidb-cloud/create-tidb-cluster.md)または[戻す](/tidb-cloud/backup-and-restore.md#restore) a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの場合、TiDB、TiKV、およびTiFlashの vCPU サイズの構成をサポートします。
-   クラスター作成のための AWS リージョン`Mumbai`のサポートを追加します。
-   [TiDB Cloud請求](/tidb-cloud/tidb-cloud-billing.md)のコンピューティング、ストレージ、およびデータ転送のコストを更新します。

## 2022 年 4 月 7 日 {#april-7-2022}

-   TiDB CloudをDeveloper Tierの[TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr)にアップグレードします。

## 2022 年 3 月 31 日 {#march-31-2022}

TiDB Cloudは一般提供になりました。次のいずれかのオプションを選択でき[サインアップ](https://tidbcloud.com/signup) 。

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier)から無料で始めましょう。
-   [14 日間の無料 PoC トライアル](https://en.pingcap.com/apply-for-poc/)に申し込む。
-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)でフル アクセスを取得します。

## 2022 年 3 月 25 日 {#march-25-2022}

新機能：

-   サポート[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md) 。

    TiDB Cloud組み込みアラート機能を使用すると、プロジェクト内のTiDB CloudクラスターがTiDB Cloud組み込みアラート条件のいずれかをトリガーするたびに、電子メールで通知を受けることができます。

## 2022 年 3 月 15 日 {#march-15-2022}

一般的な変更:

-   クラスター サイズが固定されたクラスター層はなくなりました。 TiDB、TiKV、 TiFlashの[クラスターサイズ](/tidb-cloud/size-your-cluster.md)台を簡単にカスタマイズできます。
-   TiFlashを使用せずに、既存のクラスターに[TiFlash](/tiflash/tiflash-overview.md)のノードを追加することをサポートします。
-   [新しいクラスターの作成](/tidb-cloud/create-tidb-cluster.md)の場合、ストレージ サイズ (500 ～ 2048 GiB) の指定をサポートします。クラスターの作成後にストレージ サイズを変更することはできません。
-   新しいパブリック リージョンを導入する: `eu-central-1` .
-   8 vCPU TiFlashを廃止し、16 vCPU TiFlashを提供します。
-   CPU とストレージの価格を分けます (どちらも 30% のパブリック プレビュー割引があります)。
-   [課金情報](/tidb-cloud/tidb-cloud-billing.md)と[価格表](https://en.pingcap.com/tidb-cloud/#pricing)を更新します。

新機能:

-   サポート[Prometheus と Grafana の統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md) 。

    Prometheus と Grafana の統合により、 TiDB Cloudエンドポイントから主要なメトリックを読み取り、 [グラファナ](https://grafana.com/)を使用してメトリックを表示するように[プロメテウス](https://prometheus.io/)サービスを構成できます。

-   新しいクラスターの選択されたリージョンに基づくデフォルトのバックアップ時間の割り当てをサポートします。

    詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

## 2022 年 3 月 4 日 {#march-04-2022}

新機能：

-   サポート[Datadog 統合](/tidb-cloud/monitor-datadog-integration.md) 。

    Datadog 統合を使用すると、TiDB クラスターに関するメトリクス データを[データドッグ](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリクスを Datadog ダッシュボードで直接表示できます。

## 2022 年 2 月 15 日 {#february-15-2022}

一般的な変更:

-   TiDB CloudをDeveloper Tierの[TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0)にアップグレードします。

改善：

-   [CSV ファイル](/tidb-cloud/import-csv-files.md)または[Apache 寄木細工のファイル](/tidb-cloud/import-parquet-files.md)をTiDB Cloudにインポートする際のカスタム ファイル名の使用をサポートします。

## 2022 年 1 月 11 日 {#january-11-2022}

一般的な変更:

-   TiDB Operatorを[v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)にアップグレードします。

改善：

-   [**接続**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection)ページで、提案されたオプション`--connect-timeout 15`を MySQL クライアントに追加します。

バグの修正：

-   パスワードに一重引用符が含まれていると、ユーザーがクラスターを作成できないという問題を修正します。
-   組織に所有者が 1 人しかいない場合でも、所有者が削除されたり、別の役割に変更されたりする可能性があるという問題を修正します。
