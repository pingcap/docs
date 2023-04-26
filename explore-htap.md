---
title: Explore HTAP
summary: Learn how to explore and use the features of TiDB HTAP.
---

# HTAP を調べる {#explore-htap}

このガイドでは、TiDB Hybrid Transactional and Analytical Processing (HTAP) の機能を調べて使用する方法について説明します。

> **ノート：**
>
> TiDB HTAPを初めて使用し、すぐに使い始めたい場合は、 [HTAP のクイック スタート](/quick-start-with-htap.md)を参照してください。

## ユースケース {#use-cases}

TiDB HTAP は、急速に増加する大量のデータを処理し、DevOps のコストを削減し、オンプレミスまたはクラウド環境に簡単にデプロイできるため、データ資産の価値をリアルタイムでもたらします。

以下は、HTAP の一般的な使用例です。

-   ハイブリッド ワークロード

    ハイブリッド ロード シナリオでリアルタイムのオンライン分析処理 (OLAP) に TiDB を使用する場合、TiDB のエントリ ポイントをデータに提供するだけで済みます。 TiDB は、特定のビジネスに基づいてさまざまな処理エンジンを自動的に選択します。

-   リアルタイム ストリーム処理

    リアルタイム ストリーム処理シナリオで TiDB を使用する場合、TiDB は常に流れ込むすべてのデータをリアルタイムでクエリできるようにします。同時に、TiDB は高度な並行データ ワークロードとビジネス インテリジェンス (BI) クエリも処理できます。

-   データハブ

    TiDB をデータ ハブとして使用する場合、TiDB は、アプリケーションのデータとデータ ウェアハウスをシームレスに接続することで、特定のビジネス ニーズを満たすことができます。

TiDB HTAPの使用例の詳細については、 [PingCAP Web サイトの HTAP に関するブログ](https://en.pingcap.com/blog/?tag=htap)を参照してください。

## アーキテクチャ {#architecture}

TiDB では、オンライン トランザクション処理 (OLTP) 用の行ベースstorageエンジン[TiKV](/tikv-overview.md)と、オンライン分析処理 (OLAP) 用の列型storageエンジン[TiFlash](/tiflash/tiflash-overview.md)が共存し、データを自動的に複製し、強力な整合性を維持します。

アーキテクチャの詳細については、 [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)を参照してください。

## 環境の準備 {#environment-preparation}

TiDB HTAPの機能を調べる前に、データ量に応じて TiDB と対応するstorageエンジンをデプロイする必要があります。データ量が大きい場合 (たとえば 100 T) は、 TiFlash Massively Parallel Processing (MPP) を主なソリューションとして使用し、TiSpark を補助的なソリューションとして使用することをお勧めします。

-   TiFlash

    -   TiFlashノードのない TiDB クラスターをデプロイした場合は、現在の TiDB クラスターにTiFlashノードを追加します。詳細については、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
    -   TiDB クラスターをデプロイしていない場合は、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)を参照してください。最小限の TiDB トポロジに基づいて、 [TiFlashのトポロジー](/tiflash-deployment-topology.md)もデプロイする必要があります。
    -   TiFlashノードの数を選択する方法を決定するときは、次のシナリオを考慮してください。

        -   小規模な分析処理とアドホック クエリを使用する OLTP がユース ケースに必要な場合は、1 つまたは複数のTiFlashノードを展開します。分析クエリの速度を劇的に向上させることができます。
        -   OLTP スループットがTiFlashノードの I/O 使用率に大きな圧力をかけない場合、各TiFlashノードはより多くのリソースを計算に使用するため、 TiFlashクラスタはほぼ線形のスケーラビリティを持つことができます。 TiFlashノードの数は、予想されるパフォーマンスと応答時間に基づいて調整する必要があります。
        -   OLTP のスループットが比較的高い場合 (たとえば、書き込みまたは更新のスループットが 1,000 万行/時を超える場合)、ネットワークおよび物理ディスクの書き込み容量が限られているため、TiKV とTiFlash間の I/O がボトルネックになり、また、ホットスポットを読み書きする傾向があります。この場合、 TiFlashノードの数は解析処理の計算量と複雑な非線形関係にあるため、システムの実際の状況に基づいてTiFlashノードの数を調整する必要があります。

-   ティスパーク

    -   データを Spark で分析する必要がある場合は、TiSpark をデプロイします。具体的なプロセスについては、 [TiSpark ユーザーガイド](/tispark-overview.md)を参照してください。

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## データ準備 {#data-preparation}

TiFlashがデプロイされた後、TiKV はデータをTiFlashに自動的に複製しません。 TiFlashにレプリケートする必要があるテーブルを手動で指定する必要があります。その後、TiDB は対応するTiFlashレプリカを作成します。

-   TiDB クラスタにデータがない場合は、まずデータを TiDB に移行します。詳細については、 [データ移行](/migration-overview.md)を参照してください。
-   TiDB クラスターにアップストリームからのレプリケートされたデータが既にある場合、 TiFlashのデプロイ後、データのレプリケーションは自動的に開始されません。 TiFlashに複製するテーブルを手動で指定する必要があります。詳細については、 [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)を参照してください。

## 情報処理 {#data-processing}

TiDB では、クエリまたは書き込み要求の SQL ステートメントを入力するだけです。 TiFlashレプリカを含むテーブルの場合、TiDB はフロントエンド オプティマイザを使用して、最適な実行計画を自動的に選択します。

> **ノート：**
>
> TiFlashの MPP モードはデフォルトで有効になっています。 SQL ステートメントが実行されると、TiDB はオプティマイザーを介して MPP モードで実行するかどうかを自動的に決定します。
>
> -   TiFlashの MPP モードを無効にするには、システム変数[tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)の値を`OFF`に設定します。
> -   クエリ実行のためにTiFlashの MPP モードを強制的に有効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)と[tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を`ON`に設定します。
> -   TiDB が特定のクエリを実行するために MPP モードを選択するかどうかを確認するには、 [MPP モードの Explain ステートメント](/explain-mpp.md#explain-statements-in-the-mpp-mode)を参照してください。 `EXPLAIN`ステートメントの出力に`ExchangeSender`および`ExchangeReceiver`演算子が含まれている場合、MPP モードが使用されています。

## パフォーマンス監視 {#performance-monitoring}

TiDB を使用する場合、次のいずれかの方法で TiDB クラスターのステータスとパフォーマンス メトリックを監視できます。

-   [TiDB ダッシュボード](/dashboard/dashboard-intro.md) : TiDB クラスターの全体的な実行状況を確認し、読み取りおよび書き込みトラフィックの分布と傾向を分析し、スロー クエリの詳細な実行情報を学習できます。
-   [監視システム (Prometheus &amp; Grafana)](/grafana-overview-dashboard.md) : PD、TiDB、TiKV、 TiFlash、TiCDC、および Node_exporter を含む TiDB クラスター関連コンポーネントの監視パラメーターを表示できます。

TiDB クラスターとTiFlashクラスターのアラート ルールを確認するには、 [TiDB クラスターのアラート ルール](/alert-rules.md)と[TiFlashアラート ルール](/tiflash/tiflash-alert-rules.md)を参照してください。

## トラブルシューティング {#troubleshooting}

TiDB の使用中に問題が発生した場合は、次のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [高価なクエリを特定する](/identify-expensive-queries.md)
-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDB クラスターのトラブルシューティング ガイド](/troubleshoot-tidb-cluster.md)
-   [TiFlashクラスタのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

また[Github の問題](https://github.com/pingcap/tiflash/issues)を作成したり、 [アスクトゥグ](https://asktug.com/)で質問を送信したりすることもできます。

## 次は何ですか {#what-s-next}

-   TiFlashのバージョン、重要なログ、システム テーブルを確認するには、 [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md)を参照してください。
-   特定のTiFlashノードを削除するには、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
