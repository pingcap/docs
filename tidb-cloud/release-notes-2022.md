---
title: TiDB Cloud Release Notes in 2022
summary: Learn about the release notes of TiDB Cloud in 2022.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2022年のTiDB Cloudリリースノート {#tidb-cloud-release-notes-in-2022}

このページには、2022年の[TiDB Cloud](https://en.pingcap.com/tidb-cloud/)のリリースノートがリストされています。

## 2022 年 7 月 28 日 {#july-28-2022}

-   **[どこからでもアクセスを許可**する]ボタンを[<strong>セキュリティクイックスタート</strong>]ダイアログに追加します。これにより、任意のIPアドレスからクラスタにアクセスできるようになります。詳細については、 [クラスタセキュリティ設定を構成する](/tidb-cloud/configure-security-settings.md)を参照してください。

## 2022年7月26日 {#july-26-2022}

-   新しい開発者層クラスターの自動休止状態と再開をサポートします。

    開発者層クラスタは、7日間使用されなかった後も削除されないため、1年間の無料試用期間が終了するまでいつでも使用できます。 24時間非アクティブになると、開発者層クラスタは自動的に休止状態になります。クラスターを再開するには、クラスタに新しい接続を送信するか、 TiDB Cloudコンソールの[**再開**]ボタンをクリックしクラスタ。クラスタは50秒以内に再開され、自動的にサービスに戻ります。

-   新しい開発者層クラスターのユーザー名プレフィックス制限を追加します

    データベースのユーザー名を使用または設定する場合は常に、クラスタのプレフィックスをユーザー名に含める必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。

-   開発者層クラスターのバックアップと復元機能を無効にします。

    開発者層クラスターでは、バックアップと復元機能（自動バックアップと手動バックアップの両方を含む）が無効になっています。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用して、データをバックアップとしてエクスポートすることもできます。

-   開発者層クラスタのストレージサイズを500MiBから1GiBに増やします。

-   ナビゲーションエクスペリエンスを向上させるために、 TiDB Cloudコンソールにブレッドクラムを追加します。

-   TiDB Cloudにデータをインポートするときに、複数のフィルタールールの構成をサポートします。

-   **[プロジェクト設定]**から[<strong>トラフィックフィルター</strong>]ページを削除し、[ <strong>TiDBに接続</strong>]ダイアログから[<strong>デフォルトセットからルールを追加</strong>]ボタンを削除します。

## 2022年7月19日 {#july-19-2022}

-   TiKVノードサイズの新しいオプションを提供します： `8 vCPU, 32 GiB` 。 8vCPUTiKVノードには`8 vCPU, 32 GiB`または`8 vCPU, 64 GiB`のいずれかを選択できます。
-   [ **TiDBに接続**]ダイアログで提供されるサンプルコードで構文の強調表示をサポートして、コードの可読性を向上させます。サンプルコードで、置き換える必要のあるパラメータを簡単に特定できます。
-   **[データインポートタスク**]ページでインポートタスクを確認した後、 TiDB Cloudがソースデータにアクセスできるかどうかの自動検証をサポートします。
-   TiDB Cloudコンソールのテーマの色を変更して、 [PingCAPWebサイト](https://en.pingcap.com/)のテーマの色と一致させます。

## 2022年7月12日 {#july-12-2022}

-   Amazon S3の**[データインポートタスク**]ページに[<strong>検証</strong>]ボタンを追加します。これは、データインポートを開始する前にデータアクセスの問題を検出するのに役立ちます。
-   [**支払い方法**]タブで<strong>請求プロファイル</strong>を追加します。<strong>請求プロファイル</strong>に税登録番号を入力すると、特定の税が請求書から免除される場合があります。

## 2022年7月5日 {#july-05-2022}

-   カラム型ストレージTiFlashは現在一般提供（GA）になっています。

    -   TiFlashは、TiDBを本質的にハイブリッドトランザクション/分析処理（HTAP）データベースにします。アプリケーションデータは最初にTiKVに保存され、次にRaftコンセンサスアルゴリズムを介してTiFlashに複製されます。つまり、行ストレージから列ストレージへのリアルタイムレプリケーションです。
    -   TiFlashレプリカを含むテーブルの場合、TiDBオプティマイザは、コスト見積もりに基づいて、TiKVまたはTiFlashレプリカのどちらを使用するかを自動的に決定します。

    TiFlashがもたらすメリットを体験するには、 [TiDB Cloudクイックスタートガイド](/tidb-cloud/tidb-cloud-htap-quickstart.md)を参照してください。

-   専用層クラスタのTiKVとTiFlashの[ストレージサイズを増やす](/tidb-cloud/scale-tidb-cluster.md)をサポートします。

-   ノードサイズフィールドでのメモリ情報の表示をサポートします。

## 2022 年 6 月 28 日 {#june-28-2022}

-   TiDB Cloud専用階層を[TiDB v5.4.1](https://docs.pingcap.com/tidb/stable/release-5.4.1)から[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。

## 2022 年 6 月 23 日 {#june-23-2022}

-   TiDB Cloud上のTiKVの最大ストレージ容量を増やします。

    -   8vCPUまたは16vCPUTiKV：最大4TiBのストレージ容量をサポートします。
    -   4 vCPU TiKV：最大2TiBのストレージ容量をサポートします。

## 2022 年 6 月 21 日 {#june-21-2022}

-   専用層クラスタを作成するためのGCPリージョン`Taiwan`のサポートを追加します。
-   名、前回、会社名、国、電話番号など、 TiDB Cloudコンソールで[ユーザープロファイルの更新](/tidb-cloud/manage-user-access.md#manage-user-profiles)をサポートします。
-   TiDB CloudコンソールでMySQL、MyCLI、JDBC、Python、Go、Node.jsの接続文字列を提供して、TiDBクラスタに簡単に接続できるようにします。
-   データのインポート中にバケットURLからバケット領域を自動的に取得することをサポートして、そのような情報を入力する手間を省きます。

## 2022年6月16日 {#june-16-2022}

-   クラスタ作成プロセスを簡素化します。

    -   クラスタを作成すると、 TiDB Cloudがデフォルトのクラスタ名を提供します。デフォルトの名前を使用するか、更新することができます。
    -   クラスタを作成する場合、「クラスターの**作成**」ページでパスワードを設定する必要はありません。
    -   クラスタの作成中または作成後に、[**セキュリティクイックスタート**]ダイアログボックスで、クラスタにアクセスするためのルートパスワードと、クラスタに接続するためのIPアドレスを設定できます。

## 2022年6月14日 {#june-14-2022}

-   開発者層向けにTiDB Cloudを[TiDB v6.1.0](https://docs.pingcap.com/tidb/stable/release-6.1.0)にアップグレードします。
-   **プロジェクト設定**の入り口を最適化します。 TiDB Cloudコンソールから、[<strong>プロジェクト設定</strong>]タブをクリックして、ターゲットプロジェクトを選択し、その設定に簡単に移動できます。
-   TiDB Cloudコンソールで有効期限メッセージを提供することにより、パスワードの有効期限のエクスペリエンスを最適化します。

## 2022 年 6 月 7 日 {#june-7-2022}

-   [無料でお試しください](https://tidbcloud.com/free-trial)の登録ページを追加して、 TiDB Cloudにすばやくサインアップします。
-   プラン選択ページから**概念実証プラン**オプションを削除します。 14日間のPoCトライアルを無料で申請する場合は、 [PoCに申し込む](https://en.pingcap.com/apply-for-poc/)ページにアクセスしてください。詳細については、 [TiDB Cloudで概念実証（PoC）を実行する](/tidb-cloud/tidb-cloud-poc.md)を参照してください。
-   電子メールとパスワードを使用してTiDB Cloudにサインアップするユーザーに、90日ごとにパスワードをリセットするように求めることにより、システムのセキュリティを向上させます。

## 2022 年 5 月 24 日 {#may-24-2022}

-   専用層クラスタを作成または復元するときに、TiDBポート番号のカスタマイズをサポートします。

## 2022年5月19日 {#may-19-2022}

-   開発者層クラスタの作成のためにAWSリージョン`Frankfurt`のサポートを追加します。

## 2022年5月18日 {#may-18-2022}

-   GitHubアカウントで[サインアップ](https://tidbcloud.com/signup)つのTiDB Cloudをサポートします。

## 2022年5月13日 {#may-13-2022}

-   Googleアカウントで[サインアップ](https://tidbcloud.com/signup)つのTiDB Cloudをサポートします。

## 2022年5月1日 {#may-1-2022}

-   クラスタを作成または復元するときに、TiDB、TiKV、およびTiFlashのvCPUサイズの構成をサポートします。
-   クラスタ作成のためのAWSリージョン`Mumbai`のサポートを追加します。
-   コンピューティング、ストレージ、およびデータ転送のコストを[TiDB Cloud課金](/tidb-cloud/tidb-cloud-billing.md)に更新します。

## 2022年4月7日 {#april-7-2022}

-   開発者層向けにTiDB Cloudを[TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr)にアップグレードします。

## 2022年3月31日 {#march-31-2022}

TiDB Cloudが一般提供になりました。 [サインアップ](https://tidbcloud.com/signup)を選択して、次のオプションのいずれかを選択できます。

-   開発者層を無料で始めましょう。
-   14日間のPoCトライアルを無料で申請してください。
-   専用層でフルアクセスを取得します。

## 2022年3月25日 {#march-25-2022}

新機能：

-   サポート[TiDB Cloudの組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md) 。

    TiDB Cloudの組み込みアラート機能を使用すると、プロジェクト内のTiDB CloudクラスタがTiDB Cloudの組み込みアラート条件の1つをトリガーするたびに、電子メールで通知を受けることができます。

## 2022 年 3 月 15 日 {#march-15-2022}

一般的な変更：

-   固定クラスタサイズのクラスタ層はもうありません。 TiDB、TiKV、TiFlashのクラスタサイズを簡単にカスタマイズできます。
-   TiFlashを使用しない既存のクラスタへのTiFlashノードの追加をサポートします。
-   新しいクラスタを作成するときに、ストレージサイズ（500〜2048 GiB）の指定をサポートします。クラスタの作成後にストレージサイズを変更することはできません。
-   新しいパブリックリージョンを導入します： `eu-central-1` 。
-   8 vCPU TiFlashを非推奨にし、16vCPUTiFlashを提供します。
-   CPUとストレージの価格を分けてください（どちらも30％のパブリックプレビュー割引があります）。
-   [課金情報](/tidb-cloud/tidb-cloud-billing.md)と[価格表](https://en.pingcap.com/tidb-cloud/#pricing)を更新します。

新機能：

-   サポート[PrometheusとGrafanaの統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md) 。

    PrometheusとGrafanaの統合により、 TiDB Cloudエンドポイントから主要なメトリックを読み取り、 [グラファナ](https://grafana.com/)を使用してメトリックを表示するように[プロメテウス](https://prometheus.io/)のサービスを構成できます。

-   新しいクラスタの選択した領域に基づいて、デフォルトのバックアップ時間の割り当てをサポートします。

    詳細については、 [TiDBクラスターデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

## 2022年3月4日 {#march-04-2022}

新機能：

-   サポート[Datadogの統合](/tidb-cloud/monitor-datadog-integration.md) 。

    Datadog統合を使用すると、TiDBクラスターに関するメトリックデータを[Datadog](https://www.datadoghq.com/)に送信するようにTiDB Cloudを構成できます。その後、Datadogダッシュボードでこれらのメトリックを直接表示できます。

## 2022 年 2 月 15 日 {#february-15-2022}

一般的な変更：

-   開発者層向けにTiDB Cloudを[TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0)にアップグレードします。

改善：

-   [CSVファイル](/tidb-cloud/import-csv-files.md)または[ApacheParquetファイル](/tidb-cloud/import-parquet-files.md)をTiDB Cloudにインポートするときにカスタムファイル名を使用することをサポートします。

## 2022年1月11日 {#january-11-2022}

一般的な変更：

-   TiDB Operatorを[v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)にアップグレードします。

改善：

-   提案されたオプション`--connect-timeout 15`を[**接続**]ページのMySQLクライアントに追加します。

バグの修正：

-   パスワードに一重引用符が含まれている場合、ユーザーがクラスタを作成できない問題を修正します。
-   組織に所有者が1人しかいない場合でも、所有者を削除したり、別の役割に変更したりできるという問題を修正します。
