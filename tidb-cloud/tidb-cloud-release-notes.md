---
title: TiDB Cloud Release Notes in 2023
summary: Learn about the release notes of TiDB Cloud in 2023.
---

# 2023 年のTiDB Cloudリリース ノート {#tidb-cloud-release-notes-in-2023}

このページには 2023 年[<a href="https://www.pingcap.com/tidb-cloud/">TiDB Cloud</a>](https://www.pingcap.com/tidb-cloud/)のリリースノートが記載されています。

## 2023 年 1 月 10 日 {#january-10-2023}

**一般的な変更点**

-   ローカル CSV ファイルから TiDB にデータをインポートする機能を最適化し、 [<a href="/tidb-cloud/select-cluster-tier.md#serverless-tier-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのユーザー エクスペリエンスを向上させます。

    -   CSV ファイルをアップロードするには、**インポート**ページのアップロード領域にドラッグ アンド ドロップするだけで済みます。
    -   インポート タスクを作成するときに、ターゲット データベースまたはテーブルが存在しない場合は、名前を入力すると、 TiDB Cloudによって自動的に作成されます。作成するターゲット テーブルでは、主キーを指定するか、複数のフィールドを選択して複合主キーを形成できます。
    -   インポートが完了したら、 **「Chat2Query でデータを探索」**をクリックするか、タスク リストでターゲット テーブル名をクリックすると、 [<a href="/tidb-cloud/explore-data-with-chat2query.md">AI を活用した Chat2Query</a>](/tidb-cloud/explore-data-with-chat2query.md)でデータを探索できます。

    詳細については、 [<a href="/tidb-cloud/tidb-cloud-import-local-files.md">ローカル ファイルをTiDB Cloudにインポートする</a>](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

**コンソールの変更**

-   各クラスターに**[Get Support]**オプションを追加して、特定のクラスターのサポートをリクエストするプロセスを簡素化します。

    次のいずれかの方法でクラスターのサポートをリクエストできます。

    -   プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページで、クラスターの行にある**[...]**をクリックし、 **[Get Support]**を選択します。
    -   クラスターの概要ページで、右上隅にある**[...]**をクリックし、 **[サポートを受ける]**を選択します。

## 2023 年 1 月 5 日 {#january-5-2023}

**コンソールの変更**

-   [<a href="/tidb-cloud/select-cluster-tier.md#serverless-tier-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターの SQL Editor (ベータ) の名前を Chat2Query (ベータ) に変更し、AI を使用した SQL クエリの生成をサポートします。

    Chat2Query では、AI に SQL クエリを自動的に生成させることも、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することもできます。

    Chat2Query にアクセスするには、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動し、クラスター名をクリックして、左側のナビゲーション ウィンドウで**[Chat2Query]**をクリックします。

## 2023 年 1 月 4 日 {#january-4-2023}

**一般的な変更点**

-   AWS でホストされ、2022 年 12 月 31 日以降に作成された TiDBDedicated Tierクラスターの**ノード サイズ (vCPU + RAM) を**増やすことで、TiDB、TiKV、およびTiFlashノードのスケールアップをサポートします。

    ノード サイズを[<a href="/tidb-cloud/scale-tidb-cluster.md#increase-node-size">TiDB Cloudコンソールの使用</a>](/tidb-cloud/scale-tidb-cluster.md#increase-node-size)または[<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster">TiDB CloudAPI (ベータ版) を使用する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)に増やすことができます。

-   [<a href="/tidb-cloud/built-in-monitoring.md">**モニタリング**</a>](/tidb-cloud/built-in-monitoring.md)ページのメトリクスの保持期間を 2 日に延長します。

    過去 2 日間のメトリクス データにアクセスできるようになり、クラスターのパフォーマンスと傾向をより柔軟に把握できるようになりました。

    この改善には追加コストはかからず、クラスターの[<a href="/tidb-cloud/built-in-monitoring.md">**モニタリング**</a>](/tidb-cloud/built-in-monitoring.md)ページの**[診断]**タブからアクセスできます。これは、パフォーマンスの問題を特定してトラブルシューティングし、クラスター全体の状態をより効果的に監視するのに役立ちます。

-   Prometheus 統合のための Grafana ダッシュボード JSON のカスタマイズをサポートします。

    [<a href="/tidb-cloud/monitor-prometheus-and-grafana-integration.md">TiDB Cloudと Prometheus を統合</a>](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)お持ちの場合は、事前に構築された Grafana ダッシュボードをインポートしてTiDB Cloudクラスターを監視し、ニーズに合わせてダッシュボードをカスタマイズできるようになりました。この機能により、 TiDB Cloudクラスターの簡単かつ迅速なモニタリングが可能になり、パフォーマンスの問題を迅速に特定するのに役立ちます。

    詳細については、 [<a href="/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics">Grafana GUI ダッシュボードを使用してメトリクスを視覚化する</a>](/tidb-cloud/monitor-prometheus-and-grafana-integration.md#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics)を参照してください。

-   すべての[<a href="/tidb-cloud/select-cluster-tier.md#serverless-tier-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのデフォルトの TiDB バージョンを[<a href="https://docs.pingcap.com/tidb/v6.3/release-6.3.0">v6.3.0</a>](https://docs.pingcap.com/tidb/v6.3/release-6.3.0)から[<a href="https://docs.pingcap.com/tidb/v6.4/release-6.4.0">v6.4.0</a>](https://docs.pingcap.com/tidb/v6.4/release-6.4.0)にアップグレードします。Serverless Tierクラスターのデフォルトの TiDB バージョンを v6.4.0 にアップグレードした後のコールド スタートの問題は解決されました。

**コンソールの変更**

-   [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページとクラスター概要ページの表示を簡素化します。

    -   [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページのクラスター名をクリックすると、クラスターの概要ページに移動し、クラスターの操作を開始できます。
    -   クラスターの概要ページから**[接続] ペイン**と**[インポート]**ペインを削除します。右上隅の**「接続」**をクリックして接続情報を取得し、左側のナビゲーション・ペインで**「インポート」**をクリックしてデータをインポートできます。
