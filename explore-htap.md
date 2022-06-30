---
title: Explore HTAP
summary: Learn how to explore and use the features of TiDB HTAP.
---

# HTAPを探索する {#explore-htap}

このガイドでは、TiDBハイブリッドトランザクションおよび分析処理（HTAP）の機能を調査および使用する方法について説明します。

> **ノート：**
>
> TiDB HTAPを初めて使用し、すぐに使い始めたい場合は、 [HTAPのクイックスタート](/quick-start-with-htap.md)を参照してください。

## ユースケース {#use-cases}

TiDB HTAPは、急速に増加する大量のデータを処理し、DevOpsのコストを削減し、オンプレミス環境またはクラウド環境のいずれかに簡単に導入できるため、データ資産の価値をリアルタイムで実現できます。

HTAPの一般的な使用例は次のとおりです。

-   ハイブリッドワークロード

    ハイブリッド負荷シナリオでリアルタイムオンライン分析処理（OLAP）にTiDBを使用する場合、データへのTiDBのエントリポイントを提供するだけで済みます。 TiDBは、特定のビジネスに基づいてさまざまな処理エンジンを自動的に選択します。

-   リアルタイムストリーム処理

    リアルタイムストリーム処理シナリオでTiDBを使用する場合、TiDBは、常に流入するすべてのデータをリアルタイムで照会できるようにします。同時に、TiDBは、同時性の高いデータワークロードとビジネスインテリジェンス（BI）クエリを処理することもできます。

-   データハブ

    TiDBをデータハブとして使用する場合、TiDBは、アプリケーションとデータウェアハウスのデータをシームレスに接続することにより、特定のビジネスニーズを満たすことができます。

TiDB HTAPの使用例の詳細については、 [PingCAPWebサイトのHTAPに関するブログ](https://en.pingcap.com/blog/?tag=htap)を参照してください。

## 建築 {#architecture}

TiDBでは、オンライントランザクション処理（OLTP）用の行ベースのストレージエンジン[TiKV](/tikv-overview.md)とオンライン分析処理（OLAP）用の列型ストレージエンジン[TiFlash](/tiflash/tiflash-overview.md)が共存し、データを自動的に複製し、強力な一貫性を維持します。

アーキテクチャの詳細については、 [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)を参照してください。

## 環境の準備 {#environment-preparation}

TiDB HTAPの機能を調べる前に、データ量に応じてTiDBと対応するストレージエンジンを展開する必要があります。データ量が多い場合（たとえば、100 T）、TiFlash超並列処理（MPP）をプライマリソリューションとして使用し、TiSparkを補足ソリューションとして使用することをお勧めします。

-   TiFlash

    -   TiFlashノードのないTiDBクラスタをデプロイした場合は、現在のTiDBクラスタにTiFlashノードを追加します。詳細については、 [TiFlashクラスタをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
    -   TiDBクラスタをデプロイしていない場合は、 [TiUPを使用してTiDBクラスターをデプロイする](/production-deployment-using-tiup.md)を参照してください。最小限のTiDBトポロジに基づいて、 [TiFlashのトポロジー](/tiflash-deployment-topology.md)を展開する必要もあります。
    -   TiFlashノードの数を選択する方法を決定するときは、次のシナリオを考慮してください。

        -   ユースケースで小規模な分析処理とアドホッククエリを使用するOLTPが必要な場合は、1つまたは複数のTiFlashノードをデプロイします。それらは分析クエリの速度を劇的に向上させることができます。
        -   OLTPスループットがTiFlashノードのI/O使用率に大きな圧力をかけない場合、各TiFlashノードは計算により多くのリソースを使用するため、TiFlashクラスタはほぼ線形のスケーラビリティを持つことができます。 TiFlashノードの数は、予想されるパフォーマンスと応答時間に基づいて調整する必要があります。
        -   ネットワークと物理ディスクの書き込み容量が限られているために、OLTPスループットが比較的高い場合（たとえば、書き込みまたは更新のスループットが1,000万ライン/時間より高い場合）、TiKVとTiFlash間のI/Oがボトルネックになります。また、ホットスポットの読み取りと書き込みを行う傾向があります。この場合、TiFlashノードの数は分析処理の計算量と複雑な非線形関係にあるため、システムの実際の状態に基づいてTiFlashノードの数を調整する必要があります。

-   TiSpark

    -   データをSparkで分析する必要がある場合は、TiSparkをデプロイします。特定のプロセスについては、 [TiSparkユーザーガイド](/tispark-overview.md)を参照してください。

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## データの準備 {#data-preparation}

TiFlashがデプロイされた後、TiKVはデータをTiFlashに自動的に複製しません。 TiFlashに複製する必要のあるテーブルを手動で指定する必要があります。その後、TiDBは対応するTiFlashレプリカを作成します。

-   TiDBクラスターにデータがない場合は、最初にデータをTiDBに移行します。詳細については、 [データ移行](/migration-overview.md)を参照してください。
-   TiDBクラスタにアップストリームからレプリケートされたデータが既にある場合、TiFlashがデプロイされた後、データレプリケーションは自動的に開始されません。 TiFlashに複製するテーブルを手動で指定する必要があります。詳細については、 [TiFlashを使用する](/tiflash/use-tiflash.md)を参照してください。

## 情報処理 {#data-processing}

TiDBを使用すると、クエリまたは書き込み要求のSQLステートメントを入力するだけで済みます。 TiFlashレプリカを含むテーブルの場合、TiDBはフロントエンドオプティマイザーを使用して、最適な実行プランを自動的に選択します。

> **ノート：**
>
> TiFlashのMPPモードはデフォルトで有効になっています。 SQLステートメントが実行されると、TiDBはオプティマイザーを介してMPPモードで実行するかどうかを自動的に決定します。
>
> -   TiFlashのMPPモードを無効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)システム変数の値を`OFF`に設定します。
> -   クエリ実行でTiFlashのMPPモードを強制的に有効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)と[tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を`ON`に設定します。
> -   TiDBが特定のクエリを実行するためにMPPモードを選択するかどうかを確認するには、 [MPPモードでのステートメントの説明](/explain-mpp.md#explain-statements-in-the-mpp-mode)を参照してください。 `EXPLAIN`ステートメントの出力に`ExchangeSender`および`ExchangeReceiver`オペレーターが含まれている場合、MPPモードが使用されています。

## パフォーマンス監視 {#performance-monitoring}

TiDBを使用する場合、次のいずれかの方法でTiDBクラスタのステータスとパフォーマンスメトリックを監視できます。

-   [TiDBダッシュボード](/dashboard/dashboard-intro.md) ：TiDBクラスタの全体的な実行状況を確認し、読み取りおよび書き込みトラフィックの分布と傾向を分析し、低速クエリの詳細な実行情報を学習できます。
-   [監視システム（Prometheus＆Grafana）](/grafana-overview-dashboard.md) ：PD、TiDB、TiKV、TiFlash、TiCDC、Node_exporterなどのTiDBクラスター関連コンポーネントの監視パラメーターを確認できます。

TiDBクラスタとTiFlashクラスタのアラートルールを確認するには、 [TiDBクラスタアラートルール](/alert-rules.md)と[TiFlashアラートルール](/tiflash/tiflash-alert-rules.md)を参照してください。

## トラブルシューティング {#troubleshooting}

TiDBの使用中に問題が発生した場合は、次のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [高価なクエリを特定する](/identify-expensive-queries.md)
-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDBクラスタトラブルシューティングガイド](/troubleshoot-tidb-cluster.md)
-   [TiFlashクラスターのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

[Githubの問題](https://github.com/pingcap/tiflash/issues)を作成するか、 [AskTUG](https://asktug.com/)に質問を送信することもできます。

## 次は何ですか {#what-s-next}

-   TiFlashのバージョン、重要なログ、システムテーブルを確認するには、 [TiFlashクラスタを管理する](/tiflash/maintain-tiflash.md)を参照してください。
-   特定のTiFlashノードを削除するには、 [TiFlashクラスタをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
