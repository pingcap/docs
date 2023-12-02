---
title: TiDB Cloud Release Notes in 2022
summary: Learn about the release notes of TiDB Cloud in 2022.
---

# 2022 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2022}

このページには 2022 年[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリースノートが記載されています。

## 2022年12月28日 {#december-28-2022}

**一般的な変更点**

-   現在、すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのデフォルトの TiDB バージョンを[v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードすると、特定の状況でコールド スタートが遅くなります。そこで、すべてのServerless Tierクラスターのデフォルトの TiDB バージョンを v6.4.0 から v6.3.0 にロールバックし、できるだけ早く問題を修正し、後で再度アップグレードします。

## 2022年12月27日 {#december-27-2022}

**一般的な変更点**

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのデフォルトの TiDB バージョンを[v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。

-   Dedicated Tierクラスターのポイントインタイム リカバリ (PITR) が一般提供 (GA) になりました。

    PITR は、任意の時点のデータを新しいクラスターに復元することをサポートします。 PITR 機能を使用するには、TiDB クラスターのバージョンが v6.4.0 以上であり、TiKV ノード サイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。

    [TiDB Cloudコンソール](https://tidbcloud.com)の**バックアップ設定**で PITR 機能を有効または無効にできます。

    詳細については、 [TiDB クラスターデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

-   複数の変更フィードの管理と既存の変更フィードの編集をサポートします。

    -   さまざまなデータ レプリケーション タスクを管理するために、必要なだけ変更フィードを作成できるようになりました。現在、各クラスターには最大 10 個の変更フィードを含めることができます。詳細については、 [チェンジフィードの概要](/tidb-cloud/changefeed-overview.md)を参照してください。
    -   一時停止ステータスでも、既存の変更フィードの設定を編集できます。詳細については、 [変更フィードを編集する](/tidb-cloud/changefeed-overview.md#edit-a-changefeed)を参照してください。

-   Amazon Aurora MySQL、Amazon Relational Database Service (RDS) MySQL、またはセルフホスト型 MySQL 互換データベースからTiDB Cloudオンラインへのデータの直接移行をサポートします。この機能は現在一般提供されています。

    -   以下の6つのリージョンでサービスを提供します。
        -   AWS オレゴン州 (us-west-2)
        -   AWS 北バージニア (us-east-1)
        -   AWS ムンバイ (ap-south-1)
        -   AWS シンガポール (ap-southeast-1)
        -   AWS 東京 (ap-northeast-1)
        -   AWS フランクフルト (eu-central-1)
    -   複数の仕様をサポートします。必要なパフォーマンスに応じて適切な仕様を選択して、最適なデータ移行エクスペリエンスを実現できます。

    データをTiDB Cloudに移行する方法については、 [ユーザードキュメント](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。請求の詳細については、 [データ移行の請求](/tidb-cloud/tidb-cloud-billing-dm.md)を参照してください。

-   ローカル CSV ファイルのTiDB Cloudへのインポートをサポートします。

    数回クリックするだけでタスク構成が完了し、ローカル CSV データを TiDB クラスターにすばやくインポートできます。この方法を使用する場合、クラウドstorageバケット パスとロール ARN を指定する必要はありません。インポートプロセス全体は迅速かつスムーズです。

    詳細については、 [ローカル ファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

## 2022年12月20日 {#december-20-2022}

**一般的な変更点**

-   ラベル`project name`フィルターとして[データドッグ](/tidb-cloud/monitor-datadog-integration.md)ダッシュボードに追加し、プロジェクト情報を提供します。

    フィルター`project name`を使用すると、必要なクラスターをすばやく見つけることができます。

## 2022年12月13日 {#december-13-2022}

**一般的な変更点**

-   Serverless Tier用のTiDB Cloud SQL Editor (ベータ) を導入します。

    これは、Serverless Tierのデータベースに対して SQL クエリを直接編集して実行できる Web ベースの SQL エディターです。Serverless Tierクラスターの左側のナビゲーション バーで簡単に見つけることができます。

    Serverless Tierの場合、Web SQL シェルは SQL エディターに置き換えられます。

-   [変更フィード](/tidb-cloud/changefeed-overview.md)を使用したDedicated Tierのデータのストリーミングをサポートします。

    -   サポート[データ変更ログを MySQL にストリーミングする](/tidb-cloud/changefeed-sink-to-mysql.md) ．

        データを MySQL/ Auroraから TiDB に移行する場合、予期しないデータ移行の問題を防ぐために、MySQL をスタンバイ データベースとして使用することが必要になることがよくあります。この場合、MySQL シンクを使用して TiDB から MySQL にデータをストリーミングできます。

    -   サポート[データ変更ログを Apache Kafka にストリーミングする](/tidb-cloud/changefeed-sink-to-apache-kafka.md) (ベータ版)。

        TiDB データをメッセージ キューにストリーミングすることは、データ統合シナリオの非常に一般的な要件です。 Kafka シンクを使用して、他のデータ処理システム (Snowflake など) との統合を実現したり、ビジネス消費をサポートしたりできます。

    詳細については、 [チェンジフィードの概要](/tidb-cloud/changefeed-overview.md)を参照してください。

-   組織の所有者は、**組織の設定**で組織の名前を編集できます。

**コンソールの変更**

-   [TiDB Cloudコンソール](https://tidbcloud.com)のナビゲーション レイアウトを最適化して、ユーザーに新しいナビゲーション エクスペリエンスを提供します。

    新しいレイアウトには次の変更が含まれています。

    -   画面の使用効率を最大化するために、左側のナビゲーション バーを導入します。
    -   よりフラットなナビゲーション階層を採用します。

-   Serverless Tierユーザーの[**接続する**](/tidb-cloud/connect-to-tidb-cluster-serverless.md)を向上します。

    開発者は、コンテキストを切り替えることなく、数回クリックするだけで SQL エディターまたは好みのツールに接続できるようになりました。

## 2022 年 12 月 6 日 {#december-6-2022}

**一般的な変更点**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2)から[v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3)にアップグレードします。

## 2022年11月29日 {#november-29-2022}

**一般的な変更点**

-   AWS Marketplace と Google Cloud Marketplace のユーザー エクスペリエンスを向上させます。

    TiDB Cloudを初めて使用するか、すでにTiDB Cloudアカウントをお持ちであるかに関係なく、AWS または GCP 請求先アカウントとリンクできるようになり、AWS または GCP Marketplace のサブスクリプションを簡単に完了できるようになりました。

    リンクの仕方については[AWS Marketplace または Google Cloud Marketplace からの請求](/tidb-cloud/tidb-cloud-billing.md#billing-from-aws-marketplace-or-google-cloud-marketplace)を参照してください。

## 2022年11月22日 {#november-22-2022}

**一般的な変更点**

-   Amazon Aurora MySQL、Amazon Relational Database Service (RDS) MySQL、またはセルフホスト型 MySQL 互換データベースからTiDB Cloudオンライン (ベータ) へのデータの直接移行をサポートします。

    以前は、ビジネスを一時停止してオフラインでデータをインポートするか、サードパーティのツールを使用してデータをTiDB Cloudに移行する必要がありましたが、これは複雑でした。**データ移行**機能を使用すると、 TiDB Cloudコンソールで操作を実行するだけで、最小限のダウンタイムでデータをTiDB Cloudに安全に移行できます。

    さらに、データ移行は、既存のデータと進行中の変更の両方をデータ ソースからTiDB Cloudに移行するための完全および増分データ移行機能を提供します。

    現在、データ移行機能はまだ**ベータ版**です。これは[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターでのみ、AWS オレゴン (us-west-2) および AWS シンガポール (ap-southeast-1) リージョンでのみ使用できます。組織ごとに 1 つの移行ジョブを無料で作成できます。組織に対して複数の移行ジョブを作成するには、 [チケットを提出する](/tidb-cloud/tidb-cloud-support.md)を行う必要があります。

    詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

## 2022 年 11 月 15 日 {#november-15-2022}

**一般的な変更点**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのポイントインタイム リカバリ (PITR) をサポートします (ベータ版)。

    PITR は、任意の時点のデータを新しいクラスターに復元することをサポートします。これを使用して次のことができます。

    -   災害復旧における RPO を削減します。
    -   エラー イベントの前の時点を復元することで、データ書き込みエラーを解決します。
    -   ビジネスの履歴データを監査します。

    PITR 機能を使用するには、TiDB クラスターのバージョンが v6.3.0 以上で、TiKV ノード サイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。

    デフォルトでは、バックアップ データはクラスターが作成されたのと同じリージョンに保存されます。日本では、PITR が有効になっている GCP でホストされている TiDB クラスターの場合、バックアップ データを 1 つまたは 2 つのリージョン (東京または大阪) に保存することを選択できます。代替リージョンからデータを復元すると、より高いレベルのデータの安全性が提供され、リージョンの障害に耐えることができます。

    詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

    この機能はまだベータ版であり、リクエストがあった場合にのみ利用可能です。

    -   TiDB Cloudコンソールの右下隅にある**[ヘルプ]**をクリックします。
    -   ダイアログの**説明**フィールドに「PITR の申請」と入力し、 **[送信]**をクリックします。

-   データベース監査ログ機能は現在一般提供されています。

    データベース監査ログを使用すると、ユーザー アクセスの詳細 (実行された SQL ステートメントなど) の履歴をログに記録し、データベース監査ログの定期的な分析を実行できるため、データベースを安全に保つことができます。

    詳細については、 [データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)を参照してください。

## 2022 年 11 月 8 日 {#november-8-2022}

**一般的な変更点**

-   ユーザーフィードバックチャネルを改善します。

    TiDB Cloudコンソールの**[サポート]** &gt; **[フィードバックを送信]**でデモまたはクレジットをリクエストできるようになりました。これは、 TiDB Cloudについて詳しく知りたい場合に役立ちます。

    リクエストを受信後、できるだけ早くサポートを提供するためにご連絡させていただきます。

## 2022年10月28日 {#october-28-2022}

**一般的な変更点**

-   Developer Tierが[Serverless Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)にアップグレードされました。 TiDB のフルマネージド自動スケーリング展開であるServerless Tierが利用可能になりました。まだベータ版であり、無料で使用できます。

    -   Serverless Tierクラスターには、Dedicated Tierクラスターとして完全に機能する HTAP 機能が含まれています。
    -   Serverless Tierにより、クラスターの作成時間が短縮され、コールド スタート時間が瞬時に開始されます。Developer Tierと比較して、作成時間は数分から数秒に短縮されます。
    -   導入トポロジについて心配する必要はありません。Serverless Tierはリクエストに応じて自動的に調整されます。
    -   Serverless Tier[セキュリティのためにクラスターへの TLS 接続を強制します](/tidb-cloud/secure-connections-to-serverless-clusters.md) 。
    -   既存のDeveloper Tierクラスターは、今後数か月以内にServerless Tierに自動的に移行されます。クラスターを使用する機能には影響はなく、ベータ版のServerless Tierクラスターの使用に対して料金が発生することはありません。

    始めましょう[ここ](/tidb-cloud/tidb-cloud-quickstart.md) .

## 2022年10月25日 {#october-25-2022}

**一般的な変更点**

-   TiDB システム変数のサブセットの動的変更と永続化をサポートします (ベータ版)。

    標準 SQL ステートメントを使用して、サポートされているシステム変数に新しい値を設定できます。

    ```sql
    SET [GLOBAL|SESSION] <variable>
    ```

    例えば：

    ```sql
    SET GLOBAL tidb_committer_concurrency = 127;
    ```

    変数が`GLOBAL`レベルに設定されている場合、その変数はクラスターに適用され、永続的になります (サーバーを再起動またはリロードした後でも有効な状態が維持されます)。レベル`SESSION`の変数は永続的ではなく、現在のセッションでのみ有効です。

    **この機能はまだベータ版であり**、限られた数の変数のみがサポートされています。副作用が不確実であるため、他の[システム変数](/system-variables.md)を変更することはお勧めできません。 TiDB v6.1 に基づいてサポートされているすべての変数については、次のリストを参照してください。

    -   [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)
    -   [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)
    -   [`tidb_enable_batch_dml`](/system-variables.md#tidb_enable_batch_dml)
    -   [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)
    -   [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)
    -   [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    -   [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    -   [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)
    -   [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1)から[v6.1.2](https://docs.pingcap.com/tidb/stable/release-6.1.2)にアップグレードします。

## 2022年10月19日 {#october-19-2022}

**統合の変更点**

-   [Vercel 統合マーケットプレイス](https://vercel.com/integrations#databases)に[TiDB CloudVercel の統合](https://vercel.com/integrations/tidb-cloud)を発行します。

    [ヴェルセル](https://vercel.com)はフロントエンド開発者向けのプラットフォームで、イノベーターがインスピレーションの瞬間に作成する必要があるスピードと信頼性を提供します。 TiDB Cloud Vercel Integration を使用すると、Vercel プロジェクトをTiDB Cloudクラスターに簡単に接続できます。詳細は資料[TiDB Cloudと Vercel を統合する](/tidb-cloud/integrate-tidbcloud-with-vercel.md)を参照してください。

-   [ヴェルセルテンプレート一覧](https://vercel.com/templates)に[TiDB Cloudスターター テンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter)を発行します。

    このテンプレートを使用して、Vercel とTiDB Cloudを試すことができます。このテンプレートを使用する前に、まず[TiDB Cloudクラスターにデータをインポートする](https://github.com/pingcap/tidb-prisma-vercel-demo#2-import-table-structures-and-data)を行う必要があります。

## 2022 年 10 月 18 日 {#october-18-2022}

**一般的な変更点**

-   Dedicated Tierクラスターの場合、TiKV またはTiFlashノードの最小storageサイズが 500 GiB から 200 GiB に変更されます。これは、ワークロードのデータ量が少ないユーザーにとって、よりコスト効率が高くなります。

    詳細については、 [TiKVノードstorage](/tidb-cloud/size-your-cluster.md#tikv-node-storage)および[TiFlashノードstorage](/tidb-cloud/size-your-cluster.md#tiflash-node-storage)を参照してください。

-   TiDB Cloudサブスクリプションをカスタマイズし、コンプライアンス要件を満たすためにオンライン契約を導入します。

    TiDB Cloudコンソールの**[請求]**ページに[**契約**タブ](/tidb-cloud/tidb-cloud-billing.md#contract)が追加されます。当社の販売契約に同意し、オンラインで契約を処理するための電子メールを受け取った場合は、 **「契約」**タブに移動して契約を確認し、同意することができます。契約について詳しく知りたい場合は、お気軽に[弊社営業担当までお問い合わせください](https://www.pingcap.com/contact-us/)までお問い合わせください。

**ドキュメントの変更**

-   [TiDB CloudTerraform プロバイダー](https://registry.terraform.io/providers/tidbcloud/tidbcloud)に[ドキュメンテーション](/tidb-cloud/terraform-tidbcloud-provider-overview.md)を加えます。

    TiDB Cloud Terraform Provider は、 [テラフォーム](https://www.terraform.io/)を使用してクラスター、バックアップ、復元などのTiDB Cloudリソースを管理できるようにするプラグインです。リソース プロビジョニングとインフラストラクチャ ワークフローを自動化する簡単な方法をお探しの場合は、 [ドキュメンテーション](/tidb-cloud/terraform-tidbcloud-provider-overview.md)に従ってTiDB Cloud Terraform Provider を試してください。

## 2022 年 10 月 11 日 {#october-11-2022}

**一般的な変更点**

-   新しい[Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのデフォルトの TiDB バージョンを[v6.2.0](https://docs.pingcap.com/tidb/v6.2/release-6.2.0)から[v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)にアップグレードします。

**コンソールの変更**

-   [請求詳細ページ](/tidb-cloud/tidb-cloud-billing.md#billing-details)の請求情報を最適化します。

    -   **[サービスごとの概要]**セクションで、ノード レベルでより詳細な請求情報を提供します。
    -   **「使用状況の詳細」**セクションを追加します。使用状況の詳細を CSV ファイルとしてダウンロードすることもできます。

## 2022年9月27日 {#september-27-2022}

**一般的な変更点**

-   招待による複数の組織への参加をサポートします。

    TiDB Cloudコンソールでは、参加しているすべての組織を表示し、組織間を切り替えることができます。詳細は[組織間の切り替え](/tidb-cloud/manage-user-access.md#switch-between-organizations)を参照してください。

-   SQL診断ページを[遅いクエリ](/tidb-cloud/tune-performance.md#slow-query)ページ追加しました。

    [スロー クエリ] ページでは、TiDB クラスター内のすべてのスロー クエリを検索して表示し、SQL 実行情報やその他の詳細を表示して[実行計画](https://docs.pingcap.com/tidbcloud/explain-overview)スロー クエリのボトルネックを調査できます。

-   アカウントのパスワードをリセットすると、 TiDB Cloudは新しいパスワード入力を最後の 4 つのパスワードと照合してチェックし、それらのいずれも使用しないように警告します。使用された 4 つのパスワードはいずれも許可されません。

    詳細は[パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)を参照してください。

## 2022 年 9 月 20 日 {#september-20-2022}

**一般的な変更点**

-   セルフサービスユーザー向けの[コスト割り当てベースの請求書](/tidb-cloud/tidb-cloud-billing.md#invoices)を紹介します。

    費用が割り当てに達すると、 TiDB Cloudは請求書を生成します。割り当てを引き上げる場合、または毎月の請求書を受け取る場合は、 [私たちの販売](https://www.pingcap.com/contact-us/)にお問い合わせください。

-   データバックアップコストからstorage運用料を免除します。最新の価格情報については[TiDB Cloudの料金詳細](https://www.pingcap.com/tidb-cloud-pricing-details/)参照してください。

**コンソールの変更**

-   データインポート用の新しいWeb UIを提供します。新しい UI はユーザー エクスペリエンスを向上させ、データのインポートをより効率的にします。

    新しい UI を使用すると、インポートするデータをプレビューし、インポート プロセスを表示し、すべてのインポート タスクを簡単に管理できます。

**APIの変更**

-   TiDB Cloud API (ベータ版) がすべてのユーザーに利用可能になりました。

    TiDB Cloudコンソールで API キーを作成することで、API の使用を開始できます。詳細については、 [APIドキュメント](/tidb-cloud/api-overview.md)を参照してください。

## 2022 年 9 月 15 日 {#september-15-2022}

**一般的な変更点**

-   TLS 経由のTiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターへの接続をサポートします。

    Dedicated Tierクラスターの場合、 [接続する](/tidb-cloud/connect-via-standard-connection.md)ダイアログの**「標準接続」**タブに、TiDB クラスター CA をダウンロードするためのリンクが提供されるようになりました。また、TLS 接続の接続文字列とサンプル コードも提供されます。サードパーティの MySQL クライアント、MyCLI、および JDBC、Python、Go、Node.js などのアプリケーションの複数の接続方法を使用でき[TLS 経由でDedicated Tierクラスターに接続する](/tidb-cloud/connect-via-standard-connection.md) 。この機能により、アプリケーションから TiDB クラスターへのデータ送信のセキュリティが確保されます。

## 2022 年 9 月 14 日 {#september-14-2022}

**コンソールの変更**

-   ユーザーエクスペリエンスを向上させるために、 [クラスター](https://tidbcloud.com/console/clusters)ページとクラスター概要ページの UI を最適化します。

    新しいデザインでは、Dedicated Tierへのアップグレード、クラスター接続、データインポートの入り口が強調表示されています。

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターの Playground を導入します。

    Playground には、GitHub イベントのプリロードされたデータセットが含まれており、データをインポートしたりクライアントに接続したりせずに、クエリを即座に実行してTiDB Cloudの使用を開始できます。

## 2022 年 9 月 13 日 {#september-13-2022}

**一般的な変更点**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスタの新しい Google Cloud リージョンをサポートします: `N. Virginia (us-east4)` .

## 2022 年 9 月 9 日 {#september-9-2022}

**一般的な変更点**

-   クラスターのパフォーマンス ステータスをよりよく理解できるように、Datadog でDedicated Tierクラスターの[さらに多くの指標](/tidb-cloud/monitor-datadog-integration.md#metrics-available-to-datadog)提供します。

    [TiDB Cloudと Datadog を統合](/tidb-cloud/monitor-datadog-integration.md)ある場合は、Datadog ダッシュボードでこれらのメトリクスを直接表示できます。

## 2022 年 9 月 6 日 {#september-6-2022}

**一般的な変更点**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターのデフォルトの TiDB バージョンを[v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)から[v6.1.1](https://docs.pingcap.com/tidb/stable/release-6.1.1)にアップグレードします。

**コンソールの変更**

-   TiDB Cloudコンソールの右上隅にあるエントリから[PoC を申請する](/tidb-cloud/tidb-cloud-poc.md)を実行できるようになりました。

**APIの変更**

-   [TiDB CloudAPI](/tidb-cloud/api-overview.md)による TiKV またはTiFlashノードのstorageの増加をサポートします。 API エンドポイントの`storage_size_gib`フィールドを使用してスケーリングを行うことができます。

    現在、 TiDB Cloud API はまだベータ版であり、リクエストがあった場合にのみ利用可能です。

    詳細は[Dedicated Tierクラスターを変更する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)を参照してください。

## 2022年8月30日 {#august-30-2022}

**一般的な変更点**

-   TiDB Cloud [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの新しいネットワーク アクセス管理オプションとして、AWS PrivateLink を利用したエンドポイント接続をサポートします。

    エンドポイント接続は安全かつプライベートであり、データが公共のインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

    詳細については、 [プライベートエンドポイント接続のセットアップ](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。

**コンソールの変更**

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの[接続する](/tidb-cloud/connect-to-tidb-cluster.md)ダイアログの**[VPC ピアリング]**タブと**[プライベート エンドポイント]**タブで、MySQL、MyCLI、JDBC、Python、Go、および Node.js のサンプル接続文字列を提供します。

    接続コードをコピーしてアプリに貼り付けるだけで、Dedicated Tierクラスターに簡単に接続できます。

## 2022 年 8 月 24 日 {#august-24-2022}

**一般的な変更点**

-   Dedicated Tierクラスターの一時停止または再開をサポートします。

    TiDB Cloudでは[Dedicated Tierクラスターを一時停止または再開する](/tidb-cloud/pause-or-resume-tidb-cluster.md)を行うことができます。クラスターが一時停止されている場合、ノード コンピューティング コストは請求されません。

## 2022 年 8 月 23 日 {#august-23-2022}

**一般的な変更点**

-   新しい[Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのデフォルトの TiDB バージョンを[v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)から[v6.2.0](https://docs.pingcap.com/tidb/v6.2/release-6.2.0)にアップグレードします。

**APIの変更**

-   TiDB Cloud API をベータ版として導入します。

    この API を通じて、クラスターなどのTiDB Cloudリソースを自動的かつ効率的に管理できます。詳細については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta)を参照してください。

    現在、 TiDB Cloud API はまだベータ版であり、リクエストがあった場合にのみ利用可能です。リクエストを送信して API アクセスを申請できます。

    -   [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)の右下隅にある**[ヘルプ]**をクリックします。
    -   ダイアログの**説明**フィールドに「 TiDB Cloud APIの申請」と入力し、 **「送信」**をクリックします。

## 2022 年 8 月 16 日 {#august-16-2022}

-   TiDB と TiKV の`2 vCPU, 8 GiB (Beta)`ノード サイズをベータ版として追加します。

    -   各`2 vCPU, 8 GiB (Beta)` TiKV ノードのstorageサイズは 200 GiB ～ 500 GiB です。

    -   推奨される使用シナリオ:

        -   SMB向けのワークロードの低い本番環境
        -   PoC およびステージング環境
        -   開発環境

-   PoC ユーザー向けに[クレジット](/tidb-cloud/tidb-cloud-billing.md#credits) (以前はトレイル ポイントと呼ばれていた) を導入します。

    **「請求」**ページの**「クレジット」**タブで組織のクレジットに関する情報を表示できるようになりました。クレジットはTiDB Cloud料金の支払いに使用できます。 [お問い合わせ](https://en.pingcap.com/apply-for-poc/)でクレジットを獲得できます。

## 2022 年 8 月 9 日 {#august-9-2022}

-   GCP リージョン`Osaka` for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスター作成のサポートを追加します。

## 2022 年 8 月 2 日 {#august-2-2022}

-   TiDB と TiKV の`4 vCPU, 16 GiB`ノード サイズが一般提供 (GA) になりました。

    -   各`4 vCPU, 16 GiB` TiKV ノードのstorageサイズは 200 GiB ～ 2 TiB です。
    -   推奨される使用シナリオ:

        -   SMB向けのワークロードの低い本番環境
        -   PoC およびステージング環境
        -   開発環境

-   [Dedicated Tierクラスター](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)の**[診断]**タブに[モニタリングページ](/tidb-cloud/built-in-monitoring.md)を追加します。

    [監視] ページには、全体的なパフォーマンス診断のためのシステム レベルのエントリが表示されます。トップダウンのパフォーマンス分析手法に従って、[モニタリング] ページはデータベース時間の内訳に基づいて TiDB パフォーマンス メトリックを編成し、これらのメトリックをさまざまな色で表示します。これらの色を確認することで、システム全体の性能ボトルネックを一目で特定することができ、性能診断時間を大幅に短縮し、性能解析と診断を簡素化します。

-   CSV および Parquet ソース ファイルの**[データ インポート]**ページで**カスタム パターン**を有効または無効にするスイッチを追加します。

    **カスタム パターン**機能はデフォルトでは無効になっています。ファイル名が特定のパターンに一致する CSV または Parquet ファイルを単一のターゲット テーブルにインポートする場合、これを有効にできます。

    詳細については、 [CSVファイルをインポートする](/tidb-cloud/import-csv-files.md)および[Apache Parquet ファイルをインポートする](/tidb-cloud/import-parquet-files.md)を参照してください。

-   TiDB Cloudサポート プラン (ベーシック、スタンダード、エンタープライズ、プレミアム) を追加して、顧客の組織のさまざまなサポート ニーズに対応します。詳細については、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)を参照してください。

-   [クラスター](https://tidbcloud.com/console/clusters)ページとクラスターの詳細ページの UI を最適化します。

    -   **「クラスター」**ページに**「接続」**ボタンと**「データのインポート」**ボタンを追加します。
    -   **[接続]**ボタンと**[データのインポート]**ボタンをクラスターの詳細ページの右上隅に移動します。

## 2022 年 7 月 28 日 {#july-28-2022}

-   **[Securityクイック スタート]**ダイアログに**[どこからでもアクセスを許可]**ボタンを追加すると、任意の IP アドレスからクラスターにアクセスできるようになります。詳細については、 [クラスタのSecurity設定を構成する](/tidb-cloud/configure-security-settings.md)を参照してください。

## 2022 年 7 月 26 日 {#july-26-2022}

-   新しい[Developer Tierクラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)の自動休止状態と再開をサポートします。

    Developer Tierクラスターは 7 日間非アクティブになっても削除されないため、1 年間の無料トライアルが終了するまでいつでも使用できます。非アクティブ状態が 24 時間続くと、Developer Tierクラスターは自動的に休止状態になります。クラスターを再開するには、クラスターに新しい接続を送信するか、 TiDB Cloudコンソールの**[再開]**ボタンをクリックします。クラスターは 50 秒以内に再開され、自動的にサービスに戻ります。

-   新しい[Developer Tierクラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)にユーザー名プレフィックス制限を追加します。

    データベース ユーザー名を使用または設定するときは、ユーザー名にクラスターのプレフィックスを含める必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

-   [Developer Tierクラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)のバックアップおよび復元機能を無効にします。

    Developer Tierクラスターでは、バックアップおよび復元機能 (自動バックアップと手動バックアップの両方を含む) が無効になっています。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用してデータをバックアップとしてエクスポートすることもできます。

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのstorageサイズを 500 MiB から 1 GiB に増加します。

-   TiDB Cloudコンソールにパンくずリストを追加して、ナビゲーション エクスペリエンスを向上させます。

-   データをTiDB Cloudにインポートする際の複数のフィルター ルールの構成をサポートします。

-   **[プロジェクト設定]**から**[トラフィック フィルター]**ページを削除し、 **[TiDB に接続**] ダイアログから**[デフォルト セットからルールを追加]**ボタンを削除します。

## 2022 年 7 月 19 日 {#july-19-2022}

-   [TiKV ノードのサイズ](/tidb-cloud/size-your-cluster.md#tikv-vcpu-and-ram) : `8 vCPU, 32 GiB`の新しいオプションを提供します。 8 vCPU TiKV ノードの場合は`8 vCPU, 32 GiB`または`8 vCPU, 64 GiB`を選択できます。
-   [**TiDB に接続する**](/tidb-cloud/connect-via-standard-connection.md)ダイアログで提供されるサンプル コードで構文の強調表示をサポートし、コードの読みやすさを向上させます。サンプル コードで置き換える必要があるパラメーターを簡単に特定できます。
-   [**データインポートタスク**](/tidb-cloud/import-sample-data.md)ページでインポート タスクを確認した後、 TiDB Cloud がソース データにアクセスできるかどうかの自動検証をサポートします。
-   TiDB Cloudコンソールのテーマの色を変更して、 [PingCAP ウェブサイト](https://en.pingcap.com/)のテーマの色と一致させます。

## 2022 年 7 月 12 日 {#july-12-2022}

-   Amazon S3 の[**データインポートタスク**](/tidb-cloud/import-sample-data.md)ページに**[検証]**ボタンを追加します。これにより、データのインポートが開始される前にデータ アクセスの問題を検出できます。
-   [**支払方法**](/tidb-cloud/tidb-cloud-billing.md#payment-method)タブの下に**請求プロファイル**を追加します。 **[請求プロファイル]**に納税登録番号を入力すると、請求書から特定の税金が免除される場合があります。詳細については、 [請求プロファイル情報の編集](/tidb-cloud/tidb-cloud-billing.md#edit-billing-profile-information)を参照してください。

## 2022 年 7 月 5 日 {#july-05-2022}

-   コラム型storage[TiFlash](/tiflash/tiflash-overview.md)は現在、一般提供 (GA) されています。

    -   TiFlash は、 TiDB を本質的にハイブリッド トランザクション/分析処理 (HTAP) データベースにします。アプリケーション データはまず TiKV に保存され、次にRaftコンセンサス アルゴリズムを介してTiFlashにレプリケートされます。つまり、行storageから列storageへのリアルタイム レプリケーションとなります。
    -   TiFlashレプリカを含むテーブルの場合、TiDB オプティマイザーはコスト見積もりに基づいて TiKV レプリカとTiFlashレプリカのどちらを使用するかを自動的に決定します。

    TiFlashによってもたらされる利点を体験するには、 [TiDB CloudHTAP クイック スタート ガイド](/tidb-cloud/tidb-cloud-htap-quickstart.md)を参照してください。

-   Dedicated Tierクラスターの TiKV およびTiFlashの[storageサイズを増やす](/tidb-cloud/scale-tidb-cluster.md#change-storage)をサポートします。

-   ノード サイズ フィールドのメモリ情報の表示をサポートします。

## 2022 年 6 月 28 日 {#june-28-2022}

-   TiDB CloudDedicated Tierを[TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1)から[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。

## 2022 年 6 月 23 日 {#june-23-2022}

-   TiDB Cloudの最大値を[TiKVのstorage容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage)に増やします。

    -   8 vCPU または 16 vCPU TiKV: 最大 4 TiB のstorage容量をサポートします。
    -   4 vCPU TiKV: 最大 2 TiB のstorage容量をサポートします。

## 2022 年 6 月 21 日 {#june-21-2022}

-   GCP リージョン`Taiwan` for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスター作成のサポートを追加します。
-   TiDB Cloudコンソールでのサポート[ユーザープロファイルの更新](/tidb-cloud/manage-user-access.md#manage-user-profiles) (姓、姓、会社名、国、電話番号など)。
-   [**TiDB に接続する**](/tidb-cloud/connect-via-standard-connection.md)ダイアログで MySQL、MyCLI、JDBC、Python、Go、および Node.js の接続文字列を指定すると、TiDB クラスターに簡単に接続できるようになります。
-   データのインポート中にバケット URI からバケット リージョンを自動的に取得する機能をサポートし、そのような情報を入力する手間を省きます。

## 2022 年 6 月 16 日 {#june-16-2022}

-   [クラスター作成プロセス](/tidb-cloud/create-tidb-cluster.md)を簡略化します。

    -   クラスターを作成すると、 TiDB Cloudデフォルトのクラスター名が提供されます。デフォルトの名前を使用することも、それを更新することもできます。
    -   クラスターを作成する場合、 **「クラスタの作成」**ページでパスワードを設定する必要はありません。
    -   クラスターの作成中または作成後に、 **[Securityクイック スタート]**ダイアログ ボックスで、クラスターにアクセスするための root パスワードと、クラスターに接続するための IP アドレスを設定できます。

## 2022 年 6 月 14 日 {#june-14-2022}

-   TiDB CloudをDeveloper Tierの[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。
-   **プロジェクト設定**の入り口を最適化します。 TiDB Cloudコンソールからターゲット プロジェクトを選択し、 **[プロジェクト設定]**タブをクリックしてその設定に簡単に移動できます。
-   TiDB Cloudコンソールで有効期限メッセージを提供することで、パスワードの有効期限のエクスペリエンスを最適化します。

## 2022 年 6 月 7 日 {#june-7-2022}

-   TiDB Cloudにすぐにサインアップするには、 [無料でお試しください](https://tidbcloud.com/free-trial)登録ページを追加します。
-   プラン選択ページから**概念実証プラン**オプションを削除します。 14 日間の PoC トライアルを無料で申し込む場合は、 [PoC に応募する](https://en.pingcap.com/apply-for-poc/)ページに進んでください。詳細については、 [TiDB Cloudを使用して概念実証 (PoC) を実行する](/tidb-cloud/tidb-cloud-poc.md)を参照してください。
-   電子メールとパスワードを使用してTiDB Cloudにサインアップするユーザーに、90 日ごとにパスワードをリセットするよう求めることで、システムのセキュリティを向上させます。詳細については、 [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)を参照してください。

## 2022 年 5 月 24 日 {#may-24-2022}

-   Dedicated Tierクラスターを[作成する](/tidb-cloud/create-tidb-cluster.md)または[復元する](/tidb-cloud/backup-and-restore.md#restore)にする場合の TiDB ポート番号のカスタマイズをサポートします。

## 2022 年 5 月 19 日 {#may-19-2022}

-   AWS リージョン`Frankfurt` for [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスター作成のサポートを追加します。

## 2022 年 5 月 18 日 {#may-18-2022}

-   GitHub アカウントで[サインアップ](https://tidbcloud.com/signup) TiDB Cloudをサポートします。

## 2022 年 5 月 13 日 {#may-13-2022}

-   Google アカウントで[サインアップ](https://tidbcloud.com/signup) TiDB Cloudをサポートします。

## 2022 年 5 月 1 日 {#may-1-2022}

-   [作成する](/tidb-cloud/create-tidb-cluster.md)または[復元する](/tidb-cloud/backup-and-restore.md#restore) a [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターの場合、TiDB、TiKV、およびTiFlashの vCPU サイズの構成をサポートします。
-   クラスター作成のための AWS リージョン`Mumbai`のサポートを追加します。
-   [TiDB Cloudの請求](/tidb-cloud/tidb-cloud-billing.md)のコンピューティング、storage、およびデータ転送のコストを更新します。

## 2022 年 4 月 7 日 {#april-7-2022}

-   TiDB CloudをDeveloper Tierの[TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr)にアップグレードします。

## 2022年3月31日 {#march-31-2022}

TiDB Cloudは現在一般提供されています。 [サインアップ](https://tidbcloud.com/signup) 、次のオプションのいずれかを選択できます。

-   [Developer Tier](/tidb-cloud/select-cluster-tier.md#tidb-serverless)から無料で始めましょう。
-   [14 日間の PoC トライアルを無料で実施](https://en.pingcap.com/apply-for-poc/)に応募してください。
-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)でフルアクセスを取得します。

## 2022 年 3 月 25 日 {#march-25-2022}

新機能：

-   サポート[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md) ．

    TiDB Cloud組み込みアラート機能を使用すると、プロジェクト内のTiDB CloudクラスターがTiDB Cloud Cloud 組み込みアラート条件のいずれかをトリガーするたびに、電子メールで通知を受け取ることができます。

## 2022 年 3 月 15 日 {#march-15-2022}

一般的な変更点:

-   固定クラスター サイズのクラスター層はもうありません。 TiDB、TiKV、 TiFlashの[クラスターサイズ](/tidb-cloud/size-your-cluster.md)を簡単にカスタマイズできます。
-   TiFlashを使用しない既存のクラスターへの[TiFlash](/tiflash/tiflash-overview.md)ノードの追加をサポートします。
-   [新しいクラスターの作成](/tidb-cloud/create-tidb-cluster.md)の場合、storageサイズ (500 ～ 2048 GiB) の指定をサポートします。クラスターの作成後にstorageサイズを変更することはできません。
-   新しいパブリック領域を導入します。 `eu-central-1` .
-   8 vCPU TiFlashを廃止し、16 vCPU TiFlashを提供します。
-   CPU とstorageの価格は別になります (どちらも 30% のパブリック プレビュー割引があります)。
-   [請求情報](/tidb-cloud/tidb-cloud-billing.md)と[価格表](https://en.pingcap.com/tidb-cloud/#pricing)を更新します。

新機能:

-   サポート[Prometheus と Grafana の統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md) ．

    Prometheus と Grafana の統合により、 TiDB Cloudエンドポイントから主要なメトリクスを読み取り、 [グラファナ](https://grafana.com/)を使用してメトリクスを表示するように[プロメテウス](https://prometheus.io/)サービスを構成できます。

-   新しいクラスターの選択したリージョンに基づいて、デフォルトのバックアップ時間の割り当てをサポートします。

    詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

## 2022 年 3 月 4 日 {#march-04-2022}

新機能：

-   サポート[Datadog の統合](/tidb-cloud/monitor-datadog-integration.md) ．

    Datadog 統合を使用すると、TiDB クラスターに関するメトリック データを[データドッグ](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成できます。その後、これらのメトリクスを Datadog ダッシュボードで直接表示できるようになります。

## 2022 年 2 月 15 日 {#february-15-2022}

全体的な変更:

-   TiDB CloudをDeveloper Tierの[TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0)にアップグレードします。

改善：

-   [CSVファイル](/tidb-cloud/import-csv-files.md)または[Apache パーケット ファイル](/tidb-cloud/import-parquet-files.md)をTiDB Cloudにインポートする際のカスタム ファイル名の使用をサポートします。

## 2022 年 1 月 11 日 {#january-11-2022}

全体的な変更:

-   TiDB Operatorを[v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)にアップグレードします。

改善：

-   提案されたオプション`--connect-timeout 15` [**接続する**](/tidb-cloud/connect-via-standard-connection.md)ページの MySQL クライアントに追加します。

バグの修正：

-   パスワードに一重引用符が含まれている場合、ユーザーがクラスターを作成できない問題を修正します。
-   組織に所有者が 1 人しかいない場合でも、所有者が削除されたり、別の役割に変更されたりする可能性があるという問題を修正します。
