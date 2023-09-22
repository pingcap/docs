---
title: Explore HTAP
summary: Learn how to explore and use the features of TiDB HTAP.
---

# HTAP を探索する {#explore-htap}

このガイドでは、TiDB ハイブリッド トランザクションおよび分析処理 (HTAP) の機能を調べて使用する方法について説明します。

> **注記：**
>
> TiDB HTAPを初めて使用し、すぐに使い始めたい場合は、 [HTAP のクイック スタート](/quick-start-with-htap.md)を参照してください。

## ユースケース {#use-cases}

TiDB HTAP は、急速に増加する大量のデータを処理し、DevOps のコストを削減し、セルフホスト環境またはクラウド環境に簡単にデプロイできるため、データ資産の価値をリアルタイムで実現します。

HTAP の一般的な使用例は次のとおりです。

-   ハイブリッド ワークロード

    ハイブリッド ロード シナリオでリアルタイム オンライン分析処理 (OLAP) に TiDB を使用する場合、必要なのはデータへの TiDB のエントリ ポイントのみです。 TiDB は、特定のビジネスに基づいてさまざまな処理エンジンを自動的に選択します。

-   リアルタイムストリーム処理

    リアルタイム ストリーム処理シナリオで TiDB を使用する場合、TiDB は、常に流入するすべてのデータをリアルタイムでクエリできることを保証します。同時に、TiDB は、同時性の高いデータ ワークロードやビジネス インテリジェンス (BI) クエリも処理できます。

-   データハブ

    TiDB をデータ ハブとして使用する場合、TiDB はアプリケーションとデータ ウェアハウスのデータをシームレスに接続することで、特定のビジネス ニーズを満たすことができます。

TiDB HTAPの使用例の詳細については、 [PingCAP Web サイトの HTAP に関するブログ](https://en.pingcap.com/blog/?tag=htap)を参照してください。

TiDB の全体的なパフォーマンスを向上させるには、次の技術シナリオで HTAP を使用することをお勧めします。

-   分析処理パフォーマンスの向上

    アプリケーションに集計や結合操作などの複雑な分析クエリが含まれており、これらのクエリが大量のデータ (1,000 万行以上) に対して実行される場合、テーブルが次の場合には行ベースのstorageエンジン[TiKV](/tikv-overview.md)がパフォーマンス要件を満たさない可能性があります。これらのクエリではインデックスを効果的に使用できないか、インデックスの選択性が低くなります。

-   ハイブリッド ワークロードの分離

    同時実行性の高いオンライン トランザクション処理 (OLTP) ワークロードを処理する際、システムは一部の OLAP ワークロードも処理する必要がある場合があります。システム全体の安定性を確保するには、OLTP パフォーマンスに対する OLAP クエリの影響を回避する必要があります。

-   ETL テクノロジー スタックを簡素化する

    処理されるデータの量が中規模 (100 TB 未満) で、データ処理とスケジューリング プロセスが比較的単純で、同時実行性が高くない (10 未満) 場合は、テクノロジー スタックを簡素化することをお勧めします。あなたのシステム。 OLTP、ETL、OLAP システムで使用される複数の異なるテクノロジ スタックを単一のデータベースに置き換えることにより、トランザクション システムと分析システムの両方の要件を満たすことができます。これにより、技術的な複雑さが軽減され、メンテナンス担当者の必要性が軽減されます。

-   強く一貫した分析

    リアルタイムで一貫性の高いデータ分析と計算を実現し、分析結果がトランザクション データと完全に一致するようにするには、データのレイテンシーと不整合の問題を回避する必要があります。

## アーキテクチャ {#architecture}

TiDB では、オンライン トランザクション処理 (OLTP) 用の行ベースのstorageエンジン[TiKV](/tikv-overview.md)とオンライン分析処理 (OLAP) 用のカラム型storageエンジン[TiFlash](/tiflash/tiflash-overview.md)が共存し、データを自動的に複製し、強整合性を維持します。

アーキテクチャの詳細については、 [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)を参照してください。

## 環境の準備 {#environment-preparation}

TiDB HTAPの機能を調べる前に、データ量に応じて TiDB と対応するstorageエンジンを展開する必要があります。データ量が大きい場合 (100 T など)、 TiFlash大並列処理 (MPP) を主要なソリューションとして使用し、TiSpark を補助ソリューションとして使用することをお勧めします。

-   TiFlash

    -   TiFlashノードのない TiDB クラスターをデプロイした場合は、現在の TiDB クラスターにTiFlashノードを追加します。詳細については、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
    -   TiDB クラスターをデプロイしていない場合は、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)を参照してください。最小限の TiDB トポロジに基づいて、 [TiFlashのトポロジー](/tiflash-deployment-topology.md)もデプロイする必要があります。
    -   TiFlashノードの数を選択する方法を決定するときは、次のシナリオを考慮してください。

        -   ユースケースで小規模な分析処理とアドホック クエリを備えた OLTP が必要な場合は、1 つまたは複数のTiFlashノードをデプロイします。これらにより、分析クエリの速度が大幅に向上します。
        -   OLTP スループットがTiFlashノードの I/O 使用率に重大な圧力を与えない場合、各TiFlashノードは計算により多くのリソースを使用するため、 TiFlashクラスターはほぼ線形のスケーラビリティを持つことができます。 TiFlashノードの数は、予想されるパフォーマンスと応答時間に基づいて調整する必要があります。
        -   OLTP スループットが比較的高い場合 (たとえば、書き込みまたは更新のスループットが 1,000 万行/時間より高い場合)、ネットワークと物理ディスクの書き込み容量が限られているため、TiKV とTiFlash間の I/O がボトルネックになり、また、ホットスポットの読み取りおよび書き込みが発生する傾向があります。この場合、 TiFlashノード数は解析処理の計算量と複雑な非線形関係にあるため、実際のシステムの状況に応じてTiFlashノード数をチューニングする必要があります。

-   ティスパーク

    -   データを Spark で分析する必要がある場合は、TiSpark をデプロイします。具体的なプロセスについては、 [TiSpark ユーザーガイド](/tispark-overview.md)を参照してください。

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## データの準備 {#data-preparation}

TiFlashの展開後、TiKV はデータをTiFlashに自動的に複製しません。どのテーブルをTiFlashに複製する必要があるかを手動で指定する必要があります。その後、TiDB は対応するTiFlashレプリカを作成します。

-   TiDBクラスタにデータがない場合は、まずデータを TiDB に移行します。詳細については、 [データ移行](/migration-overview.md)を参照してください。
-   TiDB クラスターにアップストリームからレプリケートされたデータがすでに存在する場合、 TiFlashの展開後、データ レプリケーションは自動的に開始されません。 TiFlashに複製するテーブルを手動で指定する必要があります。詳細については、 [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)を参照してください。

## 情報処理 {#data-processing}

TiDB を使用すると、クエリまたは書き込みリクエストの SQL ステートメントを入力するだけで済みます。 TiFlashレプリカを含むテーブルの場合、TiDB はフロントエンド オプティマイザーを使用して、最適な実行プランを自動的に選択します。

> **注記：**
>
> TiFlashの MPP モードはデフォルトで有効になっています。 SQL ステートメントが実行されると、TiDB はオプティマイザーを通じて MPP モードで実行するかどうかを自動的に決定します。
>
> -   TiFlashの MPP モードを無効にするには、システム変数[tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)の値を`OFF`に設定します。
> -   クエリ実行のためにTiFlashの MPP モードを強制的に有効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)と[tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を`ON`に設定します。
> -   TiDB が特定のクエリを実行するために MPP モードを選択するかどうかを確認するには、 [MPP モードでの Explain ステートメント](/explain-mpp.md#explain-statements-in-the-mpp-mode)を参照してください。 `EXPLAIN`ステートメントの出力に`ExchangeSender`および`ExchangeReceiver`演算子が含まれる場合、MPP モードが使用されています。

## パフォーマンス監視 {#performance-monitoring}

TiDB を使用する場合、次のいずれかの方法で TiDB クラスターのステータスとパフォーマンス メトリックを監視できます。

-   [TiDB ダッシュボード](/dashboard/dashboard-intro.md) : TiDB クラスターの全体的な実行ステータスを確認し、読み取りおよび書き込みトラフィックの分布と傾向を分析し、遅いクエリの詳細な実行情報を確認できます。
-   [監視システム (Prometheus &amp; Grafana)](/grafana-overview-dashboard.md) : PD、TiDB、TiKV、 TiFlash、TiCDC、Node_exporter などの TiDB クラスター関連コンポーネントのモニタリング パラメーターを表示できます。

TiDB クラスターとTiFlashクラスターのアラート ルールを確認するには、 [TiDB クラスターのアラート ルール](/alert-rules.md)と[TiFlashアラート ルール](/tiflash/tiflash-alert-rules.md)を参照してください。

## トラブルシューティング {#troubleshooting}

TiDB の使用中に問題が発生した場合は、次のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [負荷の高いクエリを特定する](/identify-expensive-queries.md)
-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDB クラスターのトラブルシューティング ガイド](/troubleshoot-tidb-cluster.md)
-   [TiFlashクラスタのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

[GitHubの問題](https://github.com/pingcap/tiflash/issues)を作成したり、 [AskTUG](https://asktug.com/)で質問を送信したりすることもできます。

## 次は何ですか {#what-s-next}

-   TiFlashのバージョン、重要なログ、システム テーブルを確認するには、 [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md)を参照してください。
-   特定のTiFlashノードを削除するには、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
