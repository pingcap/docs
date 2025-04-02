---
title: TiDB Cloud Release Notes in 2022
summary: 2022 年のTiDB Cloudのリリース ノートについて説明します。
---

# 2022 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2022}

このページには、2022 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートが記載されています。

## 2022年12月28日 {#december-28-2022}

**一般的な変更**

-   現在、すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのデフォルトの TiDB バージョンを[バージョン6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0)から[バージョン6.4.0](https://docs-archive.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードすると、特定の状況でコールド スタートが遅くなります。そのため、すべてのServerless Tierクラスターのデフォルトの TiDB バージョンを v6.4.0 から v6.3.0 にロールバックし、できるだけ早く問題を修正してから、後で再度アップグレードします。

## 2022年12月27日 {#december-27-2022}

**一般的な変更**

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのデフォルトの TiDB バージョンを[バージョン6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0)から[バージョン6.4.0](https://docs-archive.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。

-   Dedicated Tierクラスターのポイントインタイムリカバリ (PITR) が一般提供 (GA) になりました。

    PITR は、任意の時点のデータを新しいクラスターに復元することをサポートします。PITR 機能を使用するには、TiDB クラスターのバージョンが少なくとも v6.4.0 であり、TiKV ノードのサイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。

    [TiDB Cloudコンソール](https://tidbcloud.com)の**バックアップ設定**で PITR 機能を有効または無効にすることができます。

    詳細については[TiDB クラスター データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

-   複数の変更フィード管理と既存の変更フィード編集をサポートします。

    -   さまざまなデータ レプリケーション タスクを管理するために、必要な数だけ変更フィードを作成できるようになりました。現在、各クラスターには最大 10 個の変更フィードを含めることができます。詳細については、 [チェンジフィードの概要](/tidb-cloud/changefeed-overview.md)を参照してください。
    -   一時停止状態の既存の変更フィードの設定を編集できます。詳細については、 [変更フィードを編集する](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)参照してください。

-   Amazon Aurora MySQL、Amazon Relational Database Service (RDS) MySQL、またはセルフホスト型 MySQL 互換データベースからTiDB Cloud Online へのデータの直接移行をサポートします。この機能は現在、一般提供されています。

    -   以下の6つの地域でサービスを提供します。
        -   AWS オレゴン (us-west-2)
        -   AWS 北バージニア (us-east-1)
        -   AWS ムンバイ (ap-south-1)
        -   AWS シンガポール (ap-southeast-1)
        -   AWS 東京 (ap-northeast-1)
        -   AWS フランクフルト (eu-central-1)
    -   複数の仕様をサポートします。必要なパフォーマンスに応じて適切な仕様を選択し、最適なデータ移行エクスペリエンスを実現できます。

    TiDB Cloudへのデータ移行方法については[ユーザードキュメント](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。課金の詳細については[データ移行の請求](/tidb-cloud/tidb-cloud-billing-dm.md)を参照してください。

-   ローカル CSV ファイルをTiDB Cloudにインポートすることをサポートします。

    タスク構成を完了するには数回クリックするだけで、ローカル CSV データを TiDB クラスターにすばやくインポートできます。この方法を使用する場合、クラウドstorageバケット パスとロール ARN を指定する必要はありません。インポート プロセス全体が迅速かつスムーズです。

    詳細については[ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)参照してください。

## 2022年12月20日 {#december-20-2022}

**一般的な変更**

-   プロジェクト情報を提供するためのフィルターとして、ラベル`project name`を[データドッグ](/tidb-cloud/monitor-datadog-integration.md)ダッシュボードに追加します。

    フィルター`project name`使用すると、必要なクラスターをすばやく見つけることができます。

## 2022年12月13日 {#december-13-2022}

**一般的な変更**

-   Serverless Tier向けのTiDB Cloud SQL エディタ (ベータ版) を導入します。

    これは、 Serverless Tierのデータベースに対して SQL クエリを直接編集および実行できる Web ベースの SQL エディターです。Serverless Serverless Tierクラスターの左側のナビゲーション バーで簡単に見つけることができます。

    Serverless Tierの場合、Web SQL Shell は SQL エディターに置き換えられます。

-   Dedicated Tierのデータのストリーミングに[チェンジフィード](/tidb-cloud/changefeed-overview.md)使用をサポートします。

    -   サポート[データ変更ログをMySQLにストリーミングする](/tidb-cloud/changefeed-sink-to-mysql.md) 。

        MySQL/ Auroraから TiDB にデータを移行する場合、予期しないデータ移行の問題を防ぐために、MySQL をスタンバイ データベースとして使用する必要があることがよくあります。この場合、MySQL シンクを使用して、TiDB から MySQL にデータをストリーミングできます。

    -   サポート[データ変更ログを Apache Kafka にストリーミングする](/tidb-cloud/changefeed-sink-to-apache-kafka.md) (ベータ)。

        TiDB データをメッセージ キューにストリーミングすることは、データ統合シナリオでは非常に一般的な要件です。Kafka シンクを使用すると、他のデータ処理システム (Snowflake など) との統合を実現したり、ビジネス消費をサポートしたりできます。

    詳細については[チェンジフィードの概要](/tidb-cloud/changefeed-overview.md)を参照してください。

-   組織の所有者は、**組織設定**で組織の名前を編集できます。

**コンソールの変更**

-   [TiDB Cloudコンソール](https://tidbcloud.com)のナビゲーション レイアウトを最適化して、ユーザーに新しいナビゲーション エクスペリエンスを提供します。

    新しいレイアウトには次の変更が含まれます。

    -   画面の使用効率を最大化するために、左側のナビゲーション バーを導入します。
    -   よりフラットなナビゲーション階層を採用します。

-   Serverless Tierユーザーの[**接続する**](/tidb-cloud/connect-to-tidb-cluster-serverless.md)エクスペリエンスを向上します。

    開発者は、コンテキストを切り替えることなく、数回クリックするだけで SQL エディターや好みのツールに接続できるようになりました。

## 2022年12月6日 {#december-6-2022}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2)から[バージョン6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3)にアップグレードします。

## 2022年11月29日 {#november-29-2022}

**一般的な変更**

-   AWS Marketplace と Google Cloud Marketplace のユーザー エクスペリエンスを向上します。

    TiDB Cloudを初めて使用する場合でも、すでにTiDB Cloudアカウントをお持ちの場合でも、AWS または GCP の請求アカウントにリンクできるようになり、AWS または GCP Marketplace のサブスクリプションの完了が容易になります。

    リンクの作り方については[AWS Marketplace または Google Cloud Marketplace からの請求](/tidb-cloud/tidb-cloud-billing.md#billing-from-aws-marketplace-or-google-cloud-marketplace)参照してください。

## 2022年11月22日 {#november-22-2022}

**一般的な変更**

-   Amazon Aurora MySQL、Amazon Relational Database Service (RDS) MySQL、またはセルフホスト型 MySQL 互換データベースからTiDB Cloud online (ベータ版) への​​データの直接移行をサポートします。

    これまでは、業務を一時停止してオフラインでデータをインポートするか、サードパーティのツールを使用してデータをTiDB Cloudに移行する必要があり、これは複雑でした。現在では、**データ移行**機能を使用すると、 TiDB Cloudコンソールで操作を実行するだけで、最小限のダウンタイムでデータをTiDB Cloudに安全に移行できます。

    さらに、データ移行では、既存のデータと進行中の変更の両方をデータ ソースからTiDB Cloudに移行するための完全および増分データ移行機能が提供されます。

    現在、データ移行機能はまだ**ベータ版**です。3 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ利用可能で、AWS オレゴン (us-west-2) および AWS シンガポール (ap-southeast-1) リージョンでのみ利用可能です。組織ごとに 1 つの移行ジョブを無料で作成できます。組織に対して複数の移行ジョブを作成するには、 [チケットを提出する](/tidb-cloud/tidb-cloud-support.md)が必要です。

    詳細については[データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

## 2022年11月15日 {#november-15-2022}

**一般的な変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのポイントインタイムリカバリ (PITR) をサポートします (ベータ版)。

    PITR は、任意の時点のデータを新しいクラスターに復元することをサポートしています。これを使用して、次のことができます。

    -   災害復旧における RPO を削減します。
    -   エラー イベント前の時点を復元することで、データ書き込みエラーを解決します。
    -   ビジネスの履歴データを監査します。

    PITR 機能を使用するには、TiDB クラスターのバージョンが少なくとも v6.3.0 であり、TiKV ノードのサイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。

    デフォルトでは、バックアップ データはクラスタが作成されたのと同じリージョンに保存されます。日本では、PITR が有効になっている GCP でホストされている TiDB クラスタの場合、バックアップ データを 1 つまたは 2 つのリージョン (東京と大阪) に保存することを選択できます。別のリージョンからデータを復元すると、データの安全性が高まり、リージョン障害を許容できます。

    詳細については[TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

    この機能はまだベータ版であり、リクエストに応じてのみ利用できます。

    -   TiDB Cloudコンソールの右下隅にある**[ヘルプ]**をクリックします。
    -   ダイアログの**説明**フィールドに「PITR を申請」と入力し、 **[送信]**をクリックします。

-   データベース監査ログ機能が GA になりました。

    データベース監査ログを使用すると、ユーザー アクセスの詳細 (実行された SQL ステートメントなど) の履歴をログに記録し、データベース監査ログを定期的に分析して、データベースを安全に保つことができます。

    詳細については[データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)参照してください。

## 2022年11月8日 {#november-8-2022}

**一般的な変更**

-   ユーザーフィードバックチャネルを改善します。

    TiDB Cloudコンソールの**「サポート**&gt;**フィードバックを送信」**でデモやクレジットをリクエストできるようになりました。これは、 TiDB Cloudについて詳しく知りたい場合に役立ちます。

    ご要望を受け取った後、できるだけ早くご連絡してサポートを提供させていただきます。

## 2022年10月28日 {#october-28-2022}

**一般的な変更**

-   Developer Tierが[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)にアップグレードされました。TiDB の完全マネージド型自動スケーリング デプロイメントであるServerless Tier が利用可能になりました。まだベータ版で、無料で使用できます。

    -   Serverless Tierクラスターには、Dedicated Tierクラスターと同様に完全に機能する HTAP 機能が引き続き含まれています。
    -   Serverless Tierでは、クラスターの作成時間が短縮され、コールド スタートが瞬時に行われます。Developer Developer Tierと比較すると、作成時間は数分から数秒に短縮されます。
    -   デプロイメント トポロジについて心配する必要はありません。Serverless Serverless Tier は、リクエストに応じて自動的に調整されます。
    -   Serverless Tier[セキュリティのためにクラスタへのTLS接続を強制する](/tidb-cloud/secure-connections-to-serverless-clusters.md) 。
    -   既存のDeveloper Tierクラスターは、今後数か月以内にServerless Tierに自動的に移行されます。クラスターの使用には影響はなく、ベータ版のServerless Tierクラスターの使用に対して料金は発生しません。

    始めましょ[ここ](/tidb-cloud/tidb-cloud-quickstart.md) .

## 2022年10月25日 {#october-25-2022}

**一般的な変更**

-   TiDB システム変数のサブセットを動的に変更および永続化することをサポートします (ベータ版)。

    標準の SQL ステートメントを使用して、サポートされているシステム変数に新しい値を設定できます。

    ```sql
    SET [GLOBAL|SESSION] <variable>
    ```

    例えば：

    ```sql
    SET GLOBAL tidb_committer_concurrency = 127;
    ```

    変数がレベル`GLOBAL`に設定されている場合、その変数はクラスターに適用され、永続的になります (サーバーを再起動したりリロードした後も有効になります)。レベル`SESSION`の変数は永続的ではなく、現在のセッションでのみ有効です。

    **この機能はまだベータ版であり**、限られた数の変数のみがサポートされています。副作用が不確実なため、他の[システム変数](/system-variables.md)を変更することは推奨されません。TiDB v6.1 に基づいてサポートされているすべての変数については、次のリストを参照してください。

    -   [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)
    -   [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)
    -   [`tidb_enable_batch_dml`](/system-variables.md#tidb_enable_batch_dml)
    -   [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)
    -   [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)
    -   [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    -   [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    -   [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)
    -   [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1)から[バージョン6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2)にアップグレードします。

## 2022年10月19日 {#october-19-2022}

**統合の変更**

-   [Vercel 統合マーケットプレイス](https://vercel.com/integrations#databases)中[TiDB CloudVercel 統合](https://vercel.com/integrations/tidb-cloud)を公開します。

    [ヴェルセル](https://vercel.com)はフロントエンド開発者向けのプラットフォームであり、イノベーターがひらめいた瞬間に創造するために必要なスピードと信頼性を提供します。TiDB TiDB Cloud Vercel 統合を使用すると、Vercel プロジェクトをTiDB Cloudクラスターに簡単に接続できます。詳細については、ドキュメント[TiDB CloudとVercelを統合する](/tidb-cloud/integrate-tidbcloud-with-vercel.md)参照してください。

-   [Vercel テンプレート リスト](https://vercel.com/templates)中[TiDB Cloudスターター テンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter)を公開します。

    このテンプレートは、Vercel とTiDB Cloudを試すための出発点として使用できます。このテンプレートを使用する前に、まず[TiDB Cloudクラスターにデータをインポートする](https://github.com/pingcap/tidb-prisma-vercel-demo#2-import-table-structures-and-data)実行する必要があります。

## 2022年10月18日 {#october-18-2022}

**一般的な変更**

-   Dedicated Tierクラスターの場合、TiKV またはTiFlashノードの最小storageサイズが 500 GiB から 200 GiB に変更されます。これにより、ワークロードのデータ ボリュームが小さいユーザーにとってコスト効率が向上します。

    詳細は[TiKV ノードstorage](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)と[TiFlashノードstorage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)参照してください。

-   TiDB Cloudサブスクリプションをカスタマイズし、コンプライアンス要件を満たすためにオンライン契約を導入します。

    TiDB Cloudコンソールの**請求**ページに[**契約**タブ](/tidb-cloud/tidb-cloud-billing.md#contract)追加されます。契約に関する当社の販売に同意し、契約をオンラインで処理するための電子メールを受信した場合は、 **[契約]**タブに移動して契約を確認して承認できます。契約の詳細については、 [営業担当にお問い合わせください](https://www.pingcap.com/contact-us/)を参照してください。

**ドキュメントの変更**

-   [ドキュメント](/tidb-cloud/terraform-tidbcloud-provider-overview.md)足して[TiDB CloudTerraform プロバイダー](https://registry.terraform.io/providers/tidbcloud/tidbcloud)にします。

    TiDB Cloud Terraform Provider は、 [テラフォーム](https://www.terraform.io/)使用してクラスタ、バックアップ、復元などのTiDB Cloudリソースを管理できるプラグインです。リソースのプロビジョニングとインフラストラクチャ ワークフローを自動化する簡単な方法を探している場合は、 [ドキュメント](/tidb-cloud/terraform-tidbcloud-provider-overview.md)に従ってTiDB Cloud Terraform Provider を試してみてください。

## 2022年10月11日 {#october-11-2022}

**一般的な変更**

-   新しい[Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのデフォルトの TiDB バージョンを[バージョン6.2.0](https://docs-archive.pingcap.com/tidb/v6.2/release-6.2.0)から[バージョン6.3.0](https://docs-archive.pingcap.com/tidb/v6.3/release-6.3.0)にアップグレードします。

**コンソールの変更**

-   [請求詳細ページ](/tidb-cloud/tidb-cloud-billing.md#billing-details)の請求情報を最適化します:

    -   **サービス別概要**セクションで、ノード レベルでより詳細な課金情報を提供します。
    -   **使用状況の詳細**セクションを追加します。使用状況の詳細を CSV ファイルとしてダウンロードすることもできます。

## 2022年9月27日 {#september-27-2022}

**一般的な変更**

-   招待による複数の組織への参加をサポートします。

    TiDB Cloudコンソールでは、参加しているすべての組織を表示し、組織を切り替えることができます。詳細については、 [組織間の切り替え](/tidb-cloud/manage-user-access.md#switch-between-organizations)参照してください。

-   SQL診断用の[遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ページを追加します。

    [スロー クエリ] ページでは、TiDB クラスター内のすべてのスロー クエリを検索して表示し、 [実行計画](https://docs.pingcap.com/tidbcloud/explain-overview) 、SQL 実行情報、その他の詳細を表示して各スロー クエリのボトルネックを調べることができます。

-   アカウントのパスワードをリセットすると、 TiDB Cloud は入力した新しいパスワードを過去 4 つのパスワードと照合し、それらのパスワードを使用しないように通知します。使用された 4 つのパスワードはいずれも許可されません。

    詳細は[パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)参照。

## 2022年9月20日 {#september-20-2022}

**一般的な変更**

-   セルフサービスユーザー向けに[コスト割当ベースの請求書](/tidb-cloud/tidb-cloud-billing.md#invoices)紹介します。

    TiDB Cloud、コストが割り当て量に達すると請求書が生成されます。割り当て量を増やすか、毎月請求書を受け取るには、 [弊社の販売](https://www.pingcap.com/contact-us/)お問い合わせください。

-   データバックアップ費用からstorage運用費を免除します。最新の価格情報については[TiDB Cloudの価格詳細](https://www.pingcap.com/tidb-cloud-pricing-details/)参照してください。

**コンソールの変更**

-   データのインポート用に新しい Web UI を提供します。新しい UI により、ユーザー エクスペリエンスが向上し、データのインポートがより効率的になります。

    新しい UI を使用すると、インポートするデータをプレビューし、インポート プロセスを表示し、すべてのインポート タスクを簡単に管理できます。

**APIの変更**

-   TiDB Cloud API (ベータ版) がすべてのユーザーに利用可能になりました。

    TiDB Cloudコンソールで API キーを作成することにより、API の使用を開始できます。詳細については、 [APIドキュメント](/tidb-cloud/api-overview.md)を参照してください。

## 2022年9月15日 {#september-15-2022}

**一般的な変更**

-   TLS 経由でTiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターへの接続をサポートします。

    Dedicated Tierクラスターの場合、 [接続する](/tidb-cloud/connect-via-standard-connection.md)の**[標準接続]**タブに、TiDB クラスター CA をダウンロードするためのリンクと、TLS 接続用の接続文字列とサンプル コードが表示されるように[TLS経由でDedicated Tierクラスターに接続する](/tidb-cloud/connect-via-standard-connection.md)ました。サードパーティの MySQL クライアント、MyCLI、およびアプリケーション用の複数の接続方法 (JDBC、Python、Go、Node.js など) を使用できます。この機能により、アプリケーションから TiDB クラスターへのデータ転送のセキュリティが確保されます。

## 2022年9月14日 {#september-14-2022}

**コンソールの変更**

-   ユーザー エクスペリエンスを向上させるために、 [クラスター](https://tidbcloud.com/console/clusters)ページ目とクラスター概要ページの UI を最適化します。

    新しいデザインでは、Dedicated Tierへのアップグレード、クラスター接続、およびデータ インポートの入り口が強調表示されます。

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターに Playground を導入します。

    Playground には GitHub イベントのデータセットが事前にロードされており、データをインポートしたりクライアントに接続したりすることなく、即座にクエリを実行してTiDB Cloudを使い始めることができます。

## 2022年9月13日 {#september-13-2022}

**一般的な変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタに対して新しい Google Cloud リージョンをサポートします: `N. Virginia (us-east4)` 。

## 2022年9月9日 {#september-9-2022}

**一般的な変更**

-   クラスターのパフォーマンス状態をよりよく理解できるように、Datadog のDedicated Tierクラスターを[より多くの指標](/tidb-cloud/monitor-datadog-integration.md#metrics-available-to-datadog)提供します。

    [TiDB CloudをDatadogと統合](/tidb-cloud/monitor-datadog-integration.md)お持ちの場合は、これらのメトリクスを Datadog ダッシュボードで直接表示できます。

## 2022年9月6日 {#september-6-2022}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターのデフォルトの TiDB バージョンを[バージョン6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)から[バージョン6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1)にアップグレードします。

**コンソールの変更**

-   これで、 TiDB Cloudコンソールの右上隅にあるエントリから[PoCを申請する](/tidb-cloud/tidb-cloud-poc.md)実行できるようになりました。

**APIの変更**

-   [TiDB CloudAPI](/tidb-cloud/api-overview.md)介して TiKV またはTiFlashノードのstorageの増加をサポートします。スケーリングを行うには、API エンドポイントの`storage_size_gib`フィールドを使用できます。

    現在、 TiDB Cloud API はまだベータ版であり、リクエストに応じてのみ利用可能です。

    詳細は[Dedicated Tierクラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)参照。

## 2022年8月30日 {#august-30-2022}

**一般的な変更**

-   TiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの新しいネットワーク アクセス管理オプションとして、AWS PrivateLink を利用したエンドポイント接続をサポートします。

    エンドポイント接続は安全かつプライベートであり、データがパブリック インターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートしており、ネットワーク管理が容易です。

    詳細については[プライベートエンドポイント接続を設定する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの[接続する](/tidb-cloud/connect-to-tidb-cluster.md)ダイアログの**VPC ピアリング**タブと**プライベート エンドポイント**タブに、MySQL、MyCLI、JDBC、Python、Go、Node.js のサンプル接続文字列を提供します。

    接続コードをコピーしてアプリに貼り付けるだけで、Dedicated Tierクラスターに簡単に接続できます。

## 2022年8月24日 {#august-24-2022}

**一般的な変更**

-   Dedicated Tierクラスターの一時停止または再開をサポートします。

    TiDB Cloudでは[Dedicated Tierクラスターを一時停止または再開する](/tidb-cloud/pause-or-resume-tidb-cluster.md)です。クラスターが一時停止されている場合、ノード コンピューティング コストは課金されません。

## 2022年8月23日 {#august-23-2022}

**一般的な変更**

-   新しい[Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのデフォルトの TiDB バージョンを[バージョン6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)から[バージョン6.2.0](https://docs-archive.pingcap.com/tidb/v6.2/release-6.2.0)にアップグレードします。

**APIの変更**

-   TiDB Cloud API をベータ版として導入します。

    この API を使用すると、クラスターなどのTiDB Cloudリソースを自動的かつ効率的に管理できます。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)参照してください。

    現在、 TiDB Cloud API はまだベータ版であり、リクエストに応じてのみ利用可能です。リクエストを送信することで API アクセスを申請できます。

    -   [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)の右下にある**「ヘルプ」**をクリックします。
    -   ダイアログの**説明**フィールドに「 TiDB Cloud API に申し込む」と入力し、 **[送信]**をクリックします。

## 2022年8月16日 {#august-16-2022}

-   ベータとして TiDB と TiKV の`2 vCPU, 8 GiB (Beta)`ノード サイズを追加します。

    -   `2 vCPU, 8 GiB (Beta)` TiKV ノードごとに、storageサイズは 200 GiB から 500 GiB の間になります。

    -   推奨される使用シナリオ:

        -   中小企業向けの低負荷の本番環境
        -   PoCおよびステージング環境
        -   開発環境

-   PoC ユーザー向けに[クレジット](/tidb-cloud/tidb-cloud-billing.md#credits) (以前はトレイル ポイントと呼ばれていました) を導入します。

    **請求**ページの**クレジット**タブで組織のクレジットに関する情報を確認できるようになりました。クレジットはTiDB Cloud料金の支払いに使用できます。クレジットを取得するには、<a href="mailto:tidbcloud-support@pingcap.com">弊社にお問い合わせ</a>ください。

## 2022年8月9日 {#august-9-2022}

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの作成に GCP リージョン`Osaka`のサポートを追加します。

## 2022年8月2日 {#august-2-2022}

-   TiDB および TiKV の`4 vCPU, 16 GiB`ノード サイズが一般提供 (GA) になりました。

    -   `4 vCPU, 16 GiB` TiKV ノードごとに、storageサイズは 200 GiB から 2 TiB の間になります。
    -   推奨される使用シナリオ:

        -   中小企業向けの低負荷の本番環境
        -   PoCおよびステージング環境
        -   開発環境

-   [Dedicated Tierクラスター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)の**診断**タブに[監視ページ](/tidb-cloud/built-in-monitoring.md)追加します。

    監視ページには、全体的なパフォーマンス診断のためのシステムレベルのエントリが用意されています。トップダウンのパフォーマンス分析方法論に従って、監視ページはデータベース時間の内訳に基づいて TiDB パフォーマンス メトリックを整理し、これらのメトリックをさまざまな色で表示します。これらの色を確認することで、システム全体のパフォーマンスのボトルネックを一目で特定できるため、パフォーマンス診断時間が大幅に短縮され、パフォーマンス分析と診断が簡素化されます。

-   CSV および Parquet ソース ファイルの**データ インポート**ページで**カスタム パターン**を有効または無効にするスイッチを追加します。

    **カスタム パターン**機能は、デフォルトでは無効になっています。ファイル名が特定のパターンに一致する CSV または Parquet ファイルを単一のターゲット テーブルにインポートする場合は、この機能を有効にできます。

    詳細については[CSVファイルのインポート](/tidb-cloud/import-csv-files.md)および[Apache Parquet ファイルのインポート](/tidb-cloud/import-parquet-files.md)参照してください。

-   顧客組織のさまざまなサポート ニーズを満たすために、 TiDB Cloudサポート プラン (Basic、Standard、Enterprise、Premium) を追加します。詳細については、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)参照してください。

-   [クラスター](https://tidbcloud.com/console/clusters)ページ目とクラスターの詳細ページの UI を最適化します。

    -   **クラスター**ページに**[接続] ボタン**と**[データのインポート]**ボタンを追加します。
    -   **[接続] ボタン**と**[データのインポート]**ボタンをクラスターの詳細ページの右上隅に移動します。

## 2022年7月28日 {#july-28-2022}

-   **「Securityクイック スタート」**ダイアログに**「どこからでもアクセスを許可」**ボタンを追加します。これにより、任意の IP アドレスからクラスターにアクセスできるようになります。詳細については、 [クラスタのSecurity設定を構成する](/tidb-cloud/configure-security-settings.md)参照してください。

## 2022年7月26日 {#july-26-2022}

-   新しい[Developer Tierクラスター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)自動休止状態と再開をサポートします。

    Developer Tierクラスターは、7 日間操作が行われなかった後も削除されないため、1 年間の無料トライアルが終了するまでいつでも使用できます。24 時間操作が行われなかった場合、 Developer Tierクラスターは自動的に休止状態になります。クラスターを再開するには、クラスターに新しい接続を送信するか、 TiDB Cloudコンソールの**[再開]**ボタンをクリックします。クラスターは 50 秒以内に再開され、自動的にサービスに戻ります。

-   新しい[Developer Tierクラスター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)にユーザー名プレフィックスの制限を追加します。

    データベース ユーザー名を使用または設定する場合は、ユーザー名にクラスターのプレフィックスを含める必要があります。詳細については、 [ユーザー名プレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)参照してください。

-   [Developer Tierクラスター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)のバックアップと復元機能を無効にします。

    バックアップと復元機能 (自動バックアップと手動バックアップの両方を含む) は、 Developer Tierクラスターでは無効になっています。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用して、データをバックアップとしてエクスポートすることは可能です。

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのstorageサイズを 500 MiB から 1 GiB に増やします。

-   ナビゲーション エクスペリエンスを向上させるために、 TiDB Cloudコンソールにパンくずリストを追加します。

-   TiDB Cloudにデータをインポートするときに、複数のフィルター ルールの構成をサポートします。

-   **プロジェクト設定**から**トラフィック フィルター**ページを削除し、 **TiDB への接続**ダイアログから**デフォルト セットからルールを追加**ボタンを削除します。

## 2022年7月19日 {#july-19-2022}

-   [TiKVノードサイズ](/tidb-cloud/size-your-cluster.md#tikv-vcpu-and-ram) : `8 vCPU, 32 GiB`の新しいオプションを提供します。8 vCPU TiKV ノードの場合は`8 vCPU, 32 GiB`または`8 vCPU, 64 GiB`選択できます。
-   [**TiDBに接続する**](/tidb-cloud/connect-via-standard-connection.md)ダイアログで提供されるサンプル コードで構文の強調表示をサポートし、コードの読みやすさを向上させます。サンプル コードで置き換える必要があるパラメーターを簡単に識別できます。
-   [**データインポートタスク**](/tidb-cloud/import-sample-data.md)ページでインポート タスクを確認した後、 TiDB Cloud がソース データにアクセスできるかどうかを自動的に検証する機能をサポートします。
-   TiDB Cloudコンソールのテーマ カラーを[PingCAPウェブサイト](https://www.pingcap.com/)のテーマ カラーと一致するように変更します。

## 2022年7月12日 {#july-12-2022}

-   Amazon S3 の[**データインポートタスク**](/tidb-cloud/import-sample-data.md)ページに**[検証]**ボタンを追加します。これにより、データのインポートが開始される前にデータ アクセスの問題を検出できるようになります。
-   [**支払方法**](/tidb-cloud/tidb-cloud-billing.md#payment-method)タブで**請求プロファイル**を追加します。**請求プロファイル**に税務登録番号を入力すると、請求書から特定の税金が免除される場合があります。詳細については、 [請求プロファイル情報を編集する](/tidb-cloud/tidb-cloud-billing.md#billing-profile)参照してください。

## 2022年7月5日 {#july-05-2022}

-   列指向storage[TiFlash](/tiflash/tiflash-overview.md)一般提供 (GA) になりました。

    -   TiFlashにより、TiDB は本質的にハイブリッド トランザクション/分析処理 (HTAP) データベースになります。アプリケーション データは最初に TiKV に保存され、その後Raftコンセンサス アルゴリズムを介してTiFlashに複製されます。つまり、行storageから列storageへのリアルタイムの複製です。
    -   TiFlashレプリカを持つテーブルの場合、TiDB オプティマイザーはコスト見積もりに基づいて TiKV レプリカとTiFlashレプリカのどちらを使用するかを自動的に決定します。

    TiFlashがもたらすメリットを体験するには、 [TiDB Cloud HTAP クイック スタート ガイド](/tidb-cloud/tidb-cloud-htap-quickstart.md)参照してください。

-   Dedicated Tierクラスターに対して TiKV とTiFlashの[storageサイズの増加](/tidb-cloud/scale-tidb-cluster.md#change-storage)サポートします。

-   ノード サイズ フィールドにメモリ情報を表示する機能をサポートします。

## 2022年6月28日 {#june-28-2022}

-   TiDB Cloud Dedicated Tierを[TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1)から[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。

## 2022年6月23日 {#june-23-2022}

-   TiDB Cloudの最大値[TiKVのstorage容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage-size)を増やします。

    -   8 vCPU または 16 vCPU TiKV: 最大 4 TiB のstorage容量をサポートします。
    -   4 vCPU TiKV: 最大 2 TiB のstorage容量をサポートします。

## 2022年6月21日 {#june-21-2022}

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの作成に GCP リージョン`Taiwan`のサポートを追加します。
-   TiDB Cloudコンソールで、名、最終時刻、会社名、国、電話番号など、 [ユーザープロファイルの更新](/tidb-cloud/manage-user-access.md#manage-user-profiles)サポートします。
-   [**TiDBに接続する**](/tidb-cloud/connect-via-standard-connection.md)ダイアログで MySQL、MyCLI、JDBC、Python、Go、Node.js の接続文字列を指定すると、TiDB クラスターに簡単に接続できます。
-   データのインポート中にバケット URI からバケット領域を自動的に取得できるようにサポートし、そのような情報を入力する手間を省きます。

## 2022年6月16日 {#june-16-2022}

-   [クラスター作成プロセス](/tidb-cloud/create-tidb-cluster.md)を簡略化します。

    -   クラスターを作成すると、 TiDB Cloudによってデフォルトのクラスター名が提供されます。デフォルトの名前を使用することも、更新することもできます。
    -   クラスターを作成するときに、 **「クラスタの作成」**ページでパスワードを設定する必要はありません。
    -   クラスターの作成中または作成後に、 **[Securityクイック スタート]**ダイアログ ボックスで、クラスターにアクセスするためのルート パスワードと、クラスターに接続するための IP アドレスを設定できます。

## 2022年6月14日 {#june-14-2022}

-   TiDB Cloud をDeveloper Tier[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。
-   **プロジェクト設定**の入り口を最適化します。TiDB TiDB Cloudコンソールから、**プロジェクト設定**タブをクリックして、ターゲット プロジェクトを選択し、その設定に簡単に移動できます。
-   TiDB Cloudコンソールに有効期限メッセージを表示することで、パスワードの有効期限切れのエクスペリエンスを最適化します。

## 2022年6月7日 {#june-7-2022}

-   TiDB Cloudにすぐにサインアップできるように、 [無料でお試し](https://tidbcloud.com/free-trial)登録ページを追加します。
-   プラン選択ページから**概念実証プラン**オプションを削除します。14 日間の PoC トライアルを無料でお申し込みの場合は、<a href="mailto:tidbcloud-support@pingcap.com">お問い合わせください</a>。詳細については、 [TiDB Cloudで概念実証（PoC）を実行する](/tidb-cloud/tidb-cloud-poc.md)参照してください。
-   電子メールとパスワードを使用してTiDB Cloudにサインアップするユーザーに、90 日ごとにパスワードをリセットするように要求することで、システムのセキュリティを強化します。詳細については、 [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)参照してください。

## 2022年5月24日 {#may-24-2022}

-   Dedicated Tierクラスターを[作成する](/tidb-cloud/create-tidb-cluster.md)または[復元する](/tidb-cloud/backup-and-restore.md#restore)する場合、TiDB ポート番号のカスタマイズをサポートします。

## 2022年5月19日 {#may-19-2022}

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターの作成に AWS リージョン`Frankfurt`のサポートを追加します。

## 2022年5月18日 {#may-18-2022}

-   GitHub アカウントで[サインアップ](https://tidbcloud.com/signup) TiDB Cloudをサポートします。

## 2022年5月13日 {#may-13-2022}

-   Google アカウントで[サインアップ](https://tidbcloud.com/signup) TiDB Cloudをサポートします。

## 2022年5月1日 {#may-1-2022}

-   [作成する](/tidb-cloud/create-tidb-cluster.md)または[復元する](/tidb-cloud/backup-and-restore.md#restore)または[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターの場合、TiDB、TiKV、およびTiFlashの vCPU サイズの構成をサポートします。
-   クラスター作成に AWS リージョン`Mumbai`のサポートを追加します。
-   [TiDB Cloud課金](/tidb-cloud/tidb-cloud-billing.md)のコンピューティング、storage、およびデータ転送コストを更新します。

## 2022年4月7日 {#april-7-2022}

-   TiDB Cloud をDeveloper Tier[TiDB v6.0.0](https://docs-archive.pingcap.com/tidb/v6.0/release-6.0.0-dmr)にアップグレードします。

## 2022年3月31日 {#march-31-2022}

TiDB Cloudは現在、一般提供中です。1 [サインアップ](https://tidbcloud.com/signup)クリックして、次のいずれかのオプションを選択できます。

-   まずは[Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)から無料で始めましょう。
-   14 日間の PoC トライアルを無料でお申し込みいただくには、<a href="mailto:tidbcloud-support@pingcap.com">お問い合わせください</a>。
-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)でフルアクセスを取得します。

## 2022年3月25日 {#march-25-2022}

新機能:

-   サポート[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md) 。

    TiDB Cloudの組み込みアラート機能を使用すると、プロジェクト内のTiDB CloudクラスターがTiDB Cloudの組み込みアラート条件のいずれかをトリガーするたびに、電子メールで通知を受け取ることができます。

## 2022年3月15日 {#march-15-2022}

一般的な変更点:

-   固定されたクラスターサイズのクラスター層はなくなりました。TiDB、TiKV、 TiFlashの[クラスターサイズ](/tidb-cloud/size-your-cluster.md)簡単にカスタマイズできます。
-   TiFlashのない既存のクラスターに[TiFlash](/tiflash/tiflash-overview.md)ノードを追加することをサポートします。
-   [新しいクラスターを作成する](/tidb-cloud/create-tidb-cluster.md)場合、storageサイズ (500 ～ 2048 GiB) の指定をサポートします。クラスターの作成後は、storageサイズを変更できません。
-   新しいパブリック リージョンを導入します`eu-central-1` 。
-   8 vCPU TiFlashを廃止し、16 vCPU TiFlashを提供します。
-   CPU とstorageの価格を分離します (どちらも 30% のパブリック プレビュー割引があります)。
-   [請求情報](/tidb-cloud/tidb-cloud-billing.md)と[価格表](https://www.pingcap.com/pricing/)更新します。

新機能:

-   サポート[PrometheusとGrafanaの統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md) 。

    Prometheus と Grafana の統合により、 [プロメテウス](https://prometheus.io/)サービスを設定してTiDB Cloudエンドポイントから主要なメトリックを読み取り、 [グラファナ](https://grafana.com/)使用してメトリックを表示できます。

-   新しいクラスターの選択したリージョンに基づいてデフォルトのバックアップ時間を割り当てることをサポートします。

    詳細については[TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

## 2022年3月4日 {#march-04-2022}

新機能:

-   サポート[Datadog統合](/tidb-cloud/monitor-datadog-integration.md) 。

    Datadog 統合により、 TiDB Cloudを構成して、TiDB クラスターに関するメトリック データを[データドッグ](https://www.datadoghq.com/)に送信できます。その後、これらのメトリックを Datadog ダッシュボードで直接表示できます。

## 2022年2月15日 {#february-15-2022}

一般的な変更:

-   TiDB Cloud をDeveloper Tier[TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0)にアップグレードします。

改善：

-   [CSVファイル](/tidb-cloud/import-csv-files.md)または[Apache Parquet ファイル](/tidb-cloud/import-parquet-files.md) TiDB Cloudにインポートするときにカスタム ファイル名の使用をサポートします。

## 2022年1月11日 {#january-11-2022}

一般的な変更:

-   TiDB Operator を[バージョン1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)にアップグレードします。

改善：

-   [**接続する**](/tidb-cloud/connect-via-standard-connection.md)ページの MySQL クライアントに推奨オプション`--connect-timeout 15`追加します。

バグ修正:

-   パスワードに一重引用符が含まれている場合にユーザーがクラスターを作成できない問題を修正しました。
-   組織に所有者が 1 人しかいない場合でも、所有者を削除したり、別の役割に変更したりできる問題を修正しました。
