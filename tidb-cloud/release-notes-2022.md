---
title: TiDB Cloud Release Notes in 2022
summary: Learn about the release notes of TiDB Cloud in 2022.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2022 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2022}

このページでは、2022 年の[TiDB Cloud](https://en.pingcap.com/tidb-cloud/)のリリース ノートを一覧表示します。

## 2022 年 8 月 30 日 {#august-30-2022}

**一般的な変更**

-   TiDB Cloud [専用ティア](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの新しいネットワーク アクセス管理オプションとして、AWS PrivateLink を利用したエンドポイント接続をサポートします。

    エンドポイント接続は安全でプライベートであり、データを公共のインターネットに公開しません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

    詳細については、 [プライベート エンドポイント接続のセットアップ](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。

**コンソールの変更**

-   [専用ティア](/tidb-cloud/select-cluster-tier.md#dedicated-tier)のクラスターの[接続](/tidb-cloud/connect-to-tidb-cluster.md)のダイアログの [ **VPC Peering** ] タブと [ <strong>Private Endpoint</strong> ] タブで、MySQL、MyCLI、JDBC、Python、Go、および Node.js のサンプル接続文字列を提供します。

    接続コードをコピーしてアプリに貼り付けるだけで、Dedicated Tier クラスターに簡単に接続できます。

## 2022 年 8 月 24 日 {#august-24-2022}

**一般的な変更**

-   Dedicated Tier クラスターの一時停止または再開をサポートします。

    TiDB Cloudで[Dedicated Tier クラスターを一時停止または再開する](/tidb-cloud/pause-or-resume-tidb-cluster.md)できます。クラスターが一時停止されている場合、ノード コンピューティング コストは課金されません。

## 2022 年 8 月 23 日 {#august-23-2022}

**一般的な変更**

-   新しい[開発者層](/tidb-cloud/select-cluster-tier.md#developer-tier)クラスターのデフォルトの TiDB バージョンを[v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)から[v6.2.0](https://docs.pingcap.com/tidb/v6.2/release-6.2.0)にアップグレードします。

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

-   GCP リージョン`Osaka` for [専用ティア](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタ作成のサポートを追加します。

## 2022 年 8 月 2 日 {#august-2-2022}

-   TiDB と TiKV の`4 vCPU, 16 GiB`ノード サイズは、一般提供 (GA) になりました。

    -   `4 vCPU, 16 GiB` TiKV ノードごとに、ストレージ サイズは 200 GiB から 2 TiB です。
    -   推奨される使用シナリオ:

        -   SMB 向けの低ワークロード本番環境
        -   PoC とステージング環境
        -   開発環境

-   [専用層クラスター](/tidb-cloud/select-cluster-tier.md#dedicated-tier)の [**診断**] タブに[モニタリングページ](/tidb-cloud/built-in-monitoring.md)を追加します。

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

-   新しい[開発者層のクラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)に対して[自動休止状態と再開](/tidb-cloud/select-cluster-tier.md#automatic-hibernation-and-resuming)をサポートします。

    Developer Tier クラスターは、7 日間非アクティブになった後も削除されないため、1 年間の無料試用期間が終了するまでいつでも使用できます。非アクティブ状態が 24 時間続くと、Developer Tier クラスターは自動的に休止状態になります。クラスターを再開するには、クラスターに新しい接続を送信するか、 TiDB Cloudコンソールの [**再開**] ボタンをクリックします。クラスターは 50 秒以内に再開され、自動的にサービスに戻ります。

-   new [開発者層のクラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)のユーザー名プレフィックス制限を追加します。

    データベース ユーザー名を使用または設定するときは常に、クラスターのプレフィックスをユーザー名に含める必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

-   [開発者層のクラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)のバックアップおよび復元機能を無効にします。

    Developer Tier クラスターでは、バックアップと復元の機能 (自動バックアップと手動バックアップの両方を含む) が無効になっています。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用して、データをバックアップとしてエクスポートできます。

-   [開発者層](/tidb-cloud/select-cluster-tier.md#developer-tier)クラスターのストレージ サイズを 500 MiB から 1 GiB に増やします。

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

-   カラムナ ストレージ[ティフラッシュ](/tiflash/tiflash-overview.md)は、一般提供 (GA) になりました。

    -   TiFlash により、TiDB は本質的に Hybrid Transactional/Analytical Processing (HTAP) データベースになります。アプリケーション データはまず TiKV に保存され、次にRaftコンセンサス アルゴリズムを介して TiFlash に複製されます。つまり、行ストレージから列ストレージへのリアルタイム レプリケーションです。
    -   TiFlash レプリカを含むテーブルの場合、TiDB オプティマイザーは、コストの見積もりに基づいて、TiKV または TiFlash レプリカのどちらを使用するかを自動的に決定します。

    TiFlash がもたらす利点を体験するには、 [TiDB CloudHTAP クイック スタート ガイド](/tidb-cloud/tidb-cloud-htap-quickstart.md)を参照してください。

-   Dedicated Tier クラスターの TiKV と TiFlash の[ストレージサイズの増加](/tidb-cloud/scale-tidb-cluster.md#increase-node-storage)をサポートします。

-   ノード サイズ フィールドにメモリ情報を表示できるようになりました。

## 2022 年 6 月 28 日 {#june-28-2022}

-   TiDB Cloud Dedicated Tier を[TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1)から[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。

## 2022 年 6 月 23 日 {#june-23-2022}

-   TiDB Cloudの最大値を[TiKVのストレージ容量](/tidb-cloud/size-your-cluster.md#tikv-node-storage)増やします。

    -   8 vCPU または 16 vCPU TiKV: 最大 4 TiB のストレージ容量をサポートします。
    -   4 vCPU TiKV: 最大 2 TiB のストレージ容量をサポートします。

## 2022 年 6 月 21 日 {#june-21-2022}

-   GCP リージョン`Taiwan` for [専用ティア](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタ作成のサポートを追加します。
-   TiDB Cloudコンソールでサポート[ユーザー プロファイルの更新](/tidb-cloud/manage-user-access.md#manage-user-profiles) (名、最終時間、会社名、国、電話番号を含む)。
-   [**TiDB に接続する**](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection)ダイアログで MySQL、MyCLI、JDBC、Python、Go、および Node.js の接続文字列を指定して、TiDB クラスターに簡単に接続できるようにします。
-   データのインポート中にバケット URL からバケット領域を自動的に取得することをサポートして、そのような情報を入力する手間を省きます。

## 2022 年 6 月 16 日 {#june-16-2022}

-   [クラスタ作成プロセス](/tidb-cloud/create-tidb-cluster.md)を単純化します。

    -   クラスターを作成すると、 TiDB Cloudはデフォルトのクラスター名を提供します。デフォルト名を使用することも、更新することもできます。
    -   クラスターを作成する場合、[クラスターの**クラスタ]**ページでパスワードを設定する必要はありません。
    -   クラスターの作成中または作成後に、[**セキュリティ クイック スタート**] ダイアログ ボックスで、クラスターにアクセスするためのルート パスワードと、クラスターに接続するための IP アドレスを設定できます。

## 2022 年 6 月 14 日 {#june-14-2022}

-   TiDB Cloudを Developer Tier の[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。
-   **Project Settings**の入り口を最適化します。 TiDB Cloudコンソールから、ターゲット プロジェクトを選択し、[ <strong>Project Settings</strong> ] タブをクリックして簡単にその設定に移動できます。
-   TiDB Cloudコンソールで有効期限メッセージを提供することにより、パスワード有効期限のエクスペリエンスを最適化します。

## 2022 年 6 月 7 日 {#june-7-2022}

-   [無料で試す](https://tidbcloud.com/free-trial)登録ページを追加して、 TiDB Cloudにすばやくサインアップします。
-   プラン選択ページから**概念実証プラン**オプションを削除します。 14日間の無料PoCトライアルを申し込む場合は、 [PoCに申し込む](https://en.pingcap.com/apply-for-poc/)ページへ。詳細については、 [TiDB Cloudで概念実証 (PoC) を実行する](/tidb-cloud/tidb-cloud-poc.md)を参照してください。
-   電子メールとパスワードを使用してTiDB Cloudにサインアップするユーザーに、90 日ごとにパスワードをリセットするよう求めることで、システムのセキュリティを向上させます。詳細については、 [ユーザーのパスワードを管理する](/tidb-cloud/manage-user-access.md#manage-user-passwords)を参照してください。

## 2022 年 5 月 24 日 {#may-24-2022}

-   Dedicated Tier クラスターを[作成](/tidb-cloud/create-tidb-cluster.md)または[戻す](/tidb-cloud/backup-and-restore.md#restore)使用する場合の TiDB ポート番号のカスタマイズをサポートします。

## 2022 年 5 月 19 日 {#may-19-2022}

-   AWS リージョン`Frankfurt` for [開発者層](/tidb-cloud/select-cluster-tier.md#developer-tier)クラスター作成のサポートを追加します。

## 2022 年 5 月 18 日 {#may-18-2022}

-   GitHub アカウントで[サインアップ](https://tidbcloud.com/signup)つのTiDB Cloudをサポートします。

## 2022 年 5 月 13 日 {#may-13-2022}

-   Google アカウントで[サインアップ](https://tidbcloud.com/signup)つのTiDB Cloudをサポートします。

## 2022 年 5 月 1 日 {#may-1-2022}

-   [作成](/tidb-cloud/create-tidb-cluster.md)または[戻す](/tidb-cloud/backup-and-restore.md#restore) a [専用ティア](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターの場合、TiDB、TiKV、および TiFlash の vCPU サイズの構成をサポートします。
-   クラスター作成のための AWS リージョン`Mumbai`のサポートを追加します。
-   [TiDB Cloud請求](/tidb-cloud/tidb-cloud-billing.md)のコンピューティング、ストレージ、およびデータ転送のコストを更新します。

## 2022 年 4 月 7 日 {#april-7-2022}

-   TiDB Cloudを Developer Tier の[TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr)にアップグレードします。

## 2022 年 3 月 31 日 {#march-31-2022}

TiDB Cloudは一般提供になりました。次のいずれかのオプションを選択でき[サインアップ](https://tidbcloud.com/signup) 。

-   [開発者層](/tidb-cloud/select-cluster-tier.md#developer-tier)から無料で始めましょう。
-   [14 日間の無料 PoC トライアル](https://en.pingcap.com/apply-for-poc/)に申し込む。
-   [専用ティア](/tidb-cloud/select-cluster-tier.md#dedicated-tier)でフル アクセスを取得します。

## 2022 年 3 月 25 日 {#march-25-2022}

新機能：

-   サポート[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md) 。

    TiDB Cloud組み込みアラート機能を使用すると、プロジェクト内のTiDB CloudクラスターがTiDB Cloud組み込みアラート条件のいずれかをトリガーするたびに、電子メールで通知を受けることができます。

## 2022 年 3 月 15 日 {#march-15-2022}

一般的な変更:

-   クラスター サイズが固定されたクラスター層はなくなりました。 TiDB、TiKV、TiFlashの[クラスターサイズ](/tidb-cloud/size-your-cluster.md)台を簡単にカスタマイズできます。
-   TiFlash を使用しない既存のクラスターに[ティフラッシュ](/tiflash/tiflash-overview.md)のノードを追加することをサポートします。
-   [新しいクラスターの作成](/tidb-cloud/create-tidb-cluster.md)の場合、ストレージ サイズ (500 ～ 2048 GiB) の指定をサポートします。クラスターの作成後にストレージ サイズを変更することはできません。
-   新しいパブリック リージョンを導入する: `eu-central-1` .
-   8 vCPU TiFlash を廃止し、16 vCPU TiFlash を提供します。
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

-   TiDB Cloudを Developer Tier の[TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0)にアップグレードします。

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
