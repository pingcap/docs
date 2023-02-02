---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# 2023 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2023}

このページでは、2023 年の[TiDB Cloud](https://www.pingcap.com/tidb-cloud/)のリリース ノートを一覧表示します。

## 2023 年 1 月 18 日 {#january-18-2023}

**一般的な変更**

-   Microsoft アカウントで[サインアップ](https://tidbcloud.com/free-trial)つのTiDB Cloudをサポートします。

## 2023 年 1 月 17 日 {#january-17-2023}

**一般的な変更**

-   新しい[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターのデフォルトの TiDB バージョンを[v6.1.3](https://docs.pingcap.com/tidb/stable/release-6.1.3)から[v6.5.0](https://docs.pingcap.com/tidb/stable/release-6.5.0)にアップグレードします。

-   新規サインアップ ユーザーの場合、 TiDB Cloudは無料の[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターを自動的に作成するため、 TiDB Cloudでデータ探索の旅をすぐに開始できます。

-   [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスター: `Seoul (ap-northeast-2)`の新しい AWS リージョンをサポートします。

    このリージョンでは、次の機能が有効になっています。

    -   [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
    -   [changefeed を使用してTiDB Cloudから他のデータ サービスにデータをストリーミングする](/tidb-cloud/changefeed-overview.md)
    -   [TiDB クラスター データのバックアップと復元](/tidb-cloud/backup-and-restore.md)

## 2023 年 1 月 10 日 {#january-10-2023}

**一般的な変更**

-   ローカル CSV ファイルから TiDB にデータをインポートする機能を最適化して、 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのユーザー エクスペリエンスを向上させます。

    -   CSV ファイルをアップロードするには、**インポート**ページのアップロード エリアにドラッグ アンド ドロップするだけです。
    -   インポート タスクを作成するときに、ターゲット データベースまたはテーブルが存在しない場合は、名前を入力して、 TiDB Cloudが自動的に作成できるようにすることができます。作成するターゲット テーブルでは、主キーを指定するか、複数のフィールドを選択して複合主キーを形成できます。
    -   インポートが完了したら、[ **Chat2Query でデータを探索**] をクリックするか、タスク リストで対象のテーブル名をクリックして、 [AI 搭載の Chat2Query](/tidb-cloud/explore-data-with-chat2query.md)でデータを探索できます。

    詳細については、 [ローカル ファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

**コンソールの変更**

-   各クラスターに**Get Support**オプションを追加して、特定のクラスターのサポートを要求するプロセスを簡素化します。

    次のいずれかの方法で、クラスターのサポートをリクエストできます。

    -   プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページで、クラスターの行にある**...**をクリックし、 <strong>Get Support</strong>を選択します。
    -   クラスターの概要ページで、右上隅にある [ **...** ] をクリックし、[<strong>サポート</strong>を受ける] を選択します。

## 2023 年 1 月 5 日 {#january-5-2023}

**コンソールの変更**

-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターの SQL エディター (ベータ) の名前を Chat2Query (ベータ) に変更し、AI を使用した SQL クエリの生成をサポートします。

    Chat2Query では、AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で記述して、端末なしでデータベースに対して SQL クエリを実行することができます。

    Chat2Query にアクセスするには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、クラスター名をクリックしてから、左側のナビゲーション ペインで [ **Chat2Query** ] をクリックします。

## 2023 年 1 月 4 日 {#january-4-2023}

**一般的な変更**

-   AWS でホストされ、2022 年 12 月 31 日以降に作成された TiDB Dedicated Tierクラスターの**ノード サイズ (vCPU + RAM)**を増やすことで、TiDB、TiKV、およびTiFlashノードのスケールアップをサポートします。

    ノード サイズを[TiDB Cloudコンソールの使用](/tidb-cloud/scale-tidb-cluster.md#increase-node-size)または[TiDB CloudAPI (ベータ版) を使用する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)増やすことができます。

-   [**モニタリング**](/tidb-cloud/built-in-monitoring.md)ページのメトリクスの保持期間を 2 日間に延長します。

    過去 2 日間のメトリクス データにアクセスできるようになり、クラスターのパフォーマンスと傾向に対する柔軟性と可視性が向上しました。

    この改善は追加料金なしで提供され、クラスターの[**モニタリング**](/tidb-cloud/built-in-monitoring.md)ページの [**診断**] タブでアクセスできます。これは、パフォーマンスの問題を特定してトラブルシューティングし、クラスターの全体的な状態をより効果的に監視するのに役立ちます。

-   Prometheus 統合のための Grafana ダッシュボード JSON のカスタマイズをサポートします。

    [TiDB Cloudと Prometheus の統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)をお持ちの場合は、ビルド済みの Grafana ダッシュボードをインポートして、 TiDB Cloudクラスターを監視し、必要に応じてダッシュボードをカスタマイズできます。この機能により、 TiDB Cloudクラスターの簡単かつ迅速な監視が可能になり、パフォーマンスの問題をすばやく特定するのに役立ちます。

    詳細については、 [Grafana GUI ダッシュボードを使用してメトリックを視覚化する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)を参照してください。

-   すべての[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのデフォルトの TiDB バージョンを[v6.3.0](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[v6.4.0](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。Serverless Tierクラスターのデフォルトの TiDB バージョンを v6.4.0 にアップグレードした後のコールド スタートの問題が解決されました。

**コンソールの変更**

-   [**クラスター**](https://tidbcloud.com/console/clusters)ページとクラスター概要ページの表示を簡素化します。

    -   [**クラスター**](https://tidbcloud.com/console/clusters)ページでクラスター名をクリックすると、クラスターの概要ページに入り、クラスターの操作を開始できます。
    -   クラスターの概要ページから [**接続**] ペインと [<strong>インポート</strong>] ペインを削除します。右上隅の [<strong>接続</strong>] をクリックして接続情報を取得し、左側のナビゲーション ペインで [<strong>インポート</strong>] をクリックしてデータをインポートできます。
