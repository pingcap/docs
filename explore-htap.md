---
title: Explore HTAP
summary: TiDB HTAPの機能を調べて使用する方法を学習します。
---

# HTAPを探索する {#explore-htap}

このガイドでは、TiDB ハイブリッド トランザクションおよび分析処理 (HTAP) の機能を調べて使用する方法について説明します。

> **注記：**
>
> TiDB HTAPを初めて使用し、すぐに使い始めたい場合は、 [TiDB HTAPのクイック スタート](/quick-start-with-htap.md)参照してください。

## ユースケース {#use-cases}

TiDB HTAP は、急速に増加する膨大なデータを処理し、DevOps のコストを削減し、セルフホスト環境またはクラウド環境のいずれかに簡単に展開できるため、データ資産の価値をリアルタイムで高めることができます。

HTAP の一般的な使用例は次のとおりです。

-   ハイブリッドワークロード

    ハイブリッド ロード シナリオでリアルタイムのオンライン分析処理 (OLAP) に TiDB を使用する場合、データへの TiDB のエントリ ポイントを提供するだけで済みます。TiDB は、特定のビジネスに基づいて、さまざまな処理エンジンを自動的に選択します。

-   リアルタイムストリーム処理

    リアルタイム ストリーム処理シナリオで TiDB を使用すると、TiDB は、継続的に流入するすべてのデータをリアルタイムでクエリできることを保証します。同時に、TiDB は、高度な同時データ ワークロードとビジネス インテリジェンス (BI) クエリも処理できます。

-   データハブ

    TiDB をデータ ハブとして使用すると、TiDB はアプリケーションのデータとデータ ウェアハウスをシームレスに接続することで、特定のビジネス ニーズを満たすことができます。

TiDB HTAPの使用例の詳細については、 [PingCAP ウェブサイトの HTAP に関するブログ](https://www.pingcap.com/blog/?tag=htap)参照してください。

TiDB の全体的なパフォーマンスを向上させるには、次の技術シナリオで HTAP を使用することをお勧めします。

-   分析処理パフォーマンスの向上

    アプリケーションに集計や結合操作などの複雑な分析クエリが含まれており、これらのクエリが大量のデータ (1,000 万行以上) に対して実行される場合、これらのクエリ内のテーブルがインデックスを効果的に使用できないか、インデックスの選択性が低いと、行ベースのstorageエンジン[ティクヴ](/tikv-overview.md)パフォーマンス要件を満たさない可能性があります。

-   ハイブリッドワークロード分離

    システムは、同時実行性の高いオンライン トランザクション処理 (OLTP) ワークロードを処理する一方で、一部の OLAP ワークロードも処理する必要がある場合があります。システム全体の安定性を確保するには、OLAP クエリが OLTP パフォーマンスに与える影響を回避する必要があります。

-   ETLテクノロジースタックを簡素化

    処理するデータの量が中規模 (100 TB 未満) で、データ処理およびスケジュール プロセスが比較的単純で、同時実行性が高くない (10 未満) 場合は、システムのテクノロジ スタックを簡素化することをお勧めします。OLTP、ETL、OLAP システムで使用される複数の異なるテクノロジ スタックを単一のデータベースに置き換えることで、トランザクション システムと分析システムの両方の要件を満たすことができます。これにより、技術的な複雑さが軽減され、保守担当者の必要性が軽減されます。

-   強い一貫性のある分析

    リアルタイムで強力な一貫性のあるデータ分析と計算を実現し、分析結果がトランザクション データと完全に一致するようにするには、データのレイテンシーと不整合の問題を回避する必要があります。

## アーキテクチャ {#architecture}

TiDB では、オンライン トランザクション処理 (OLTP) 用の行ベースのstorageエンジン[ティクヴ](/tikv-overview.md)とオンライン分析処理 (OLAP) 用の列ベースのstorageエンジン[TiFlash](/tiflash/tiflash-overview.md)が共存し、データを自動的に複製し、強力な一貫性を維持します。

アーキテクチャの詳細については、 [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)参照してください。

## 環境の準備 {#environment-preparation}

TiDB HTAPの機能を検討する前に、データ量に応じて TiDB と対応するstorageエンジンを導入する必要があります。データ量が大きい場合 (たとえば、100 T)、 TiFlash Massively Parallel Processing (MPP) を主なソリューションとして使用し、TiSpark を補助的なソリューションとして使用することをお勧めします。

-   TiFlash

    -   TiFlashノードのない TiDB クラスターをデプロイした場合は、現在の TiDB クラスターにTiFlashノードを追加します。詳細については、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
    -   TiDB クラスターをデプロイしていない場合は、 [TiUP を使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。最小限の TiDB トポロジに基づいて、 [TiFlashのトポロジー](/tiflash-deployment-topology.md)デプロイする必要があります。
    -   TiFlashノードの数を選択する方法を決定するときは、次のシナリオを考慮してください。

        -   ユースケースで小規模な分析処理とアドホック クエリを伴う OLTP が必要な場合は、1 つまたは複数のTiFlashノードを導入します。これにより、分析クエリの速度が大幅に向上します。
        -   OLTP スループットがTiFlashノードの I/O 使用率に大きな負担をかけない場合、各TiFlashノードは計算により多くのリソースを使用するため、 TiFlashクラスターはほぼ線形のスケーラビリティを実現できます。TiFlash ノードの数は、予想されるパフォーマンスと応答時間に基づいて調整する必要があります。
        -   OLTP スループットが比較的高い場合 (たとえば、書き込みまたは更新スループットが 1,000 万行/時間を超える場合)、ネットワークと物理ディスクの書き込み容量が限られているため、TiKV とTiFlash間の I/O がボトルネックになり、読み取りと書き込みのホットスポットも発生しやすくなります。この場合、 TiFlashノードの数は分析処理の計算量と複雑な非線形関係にあるため、システムの実際の状態に基づいてTiFlashノードの数を調整する必要があります。

-   ティスパーク

    -   データを Spark で分析する必要がある場合は、TiSpark をデプロイします。具体的なプロセスについては、 [TiSpark ユーザーガイド](/tispark-overview.md)参照してください。

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## データ準備 {#data-preparation}

TiFlashがデプロイされた後、TiKV はTiFlashにデータを自動的に複製しません。どのテーブルをTiFlashに複製する必要があるかを手動で指定する必要があります。その後、TiDB は対応するTiFlashレプリカを作成します。

-   TiDB クラスタにデータがない場合、まずデータを TiDB に移行します。詳細については、 [データ移行](/migration-overview.md)参照してください。
-   TiDB クラスターにアップストリームから複製されたデータがすでに存在する場合、 TiFlashの導入後、データの複製は自動的には開始されません。 TiFlashに複製するテーブルを手動で指定する必要があります。 詳細については、 [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)参照してください。

## データ処理 {#data-processing}

TiFlashを使用すると、クエリまたは書き込み要求に対して SQL ステートメントを入力するだけで済みます。TiFlash レプリカを持つテーブルの場合、TiDB はフロントエンド オプティマイザーを使用して最適な実行プランを自動的に選択します。

> **注記：**
>
> TiFlashの MPP モードはデフォルトで有効になっています。SQL ステートメントが実行されると、TiDB はオプティマイザーを通じて MPP モードで実行するかどうかを自動的に判断します。
>
> -   TiFlashの MPP モードを無効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)システム変数の値を`OFF`に設定します。
> -   クエリ実行時にTiFlashの MPP モードを強制的に有効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)と[tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を`ON`に設定します。
> -   TiDB が特定のクエリを実行するために MPP モードを選択するかどうかを確認するには、 [MPP モードでステートメントを説明する](/explain-mpp.md#explain-statements-in-the-mpp-mode)参照してください。 `EXPLAIN`ステートメントの出力に`ExchangeSender`および`ExchangeReceiver`演算子が含まれている場合、 MPP モードが使用されています。

## パフォーマンス監視 {#performance-monitoring}

TiDB を使用する場合、次のいずれかの方法で TiDB クラスターのステータスとパフォーマンス メトリックを監視できます。

-   [TiDBダッシュボード](/dashboard/dashboard-intro.md) : TiDB クラスターの全体的な実行ステータスを確認したり、読み取りおよび書き込みトラフィックの分布と傾向を分析したり、遅いクエリの詳細な実行情報を確認したりできます。
-   [監視システム (Prometheus &amp; Grafana)](/grafana-overview-dashboard.md) : PD、TiDB、TiKV、 TiFlash、TiCDC、Node_exporter などの TiDB クラスター関連コンポーネントの監視パラメータを確認できます。

TiDB クラスターとTiFlashクラスターのアラート ルールを確認するには、 [TiDB クラスタアラートルール](/alert-rules.md)と[TiFlashアラートルール](/tiflash/tiflash-alert-rules.md)参照してください。

## トラブルシューティング {#troubleshooting}

TiDB の使用中に問題が発生した場合は、次のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [コストの高いクエリを特定する](/identify-expensive-queries.md)
-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDB クラスタのトラブルシューティング ガイド](/troubleshoot-tidb-cluster.md)
-   [TiFlashクラスタのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

[GitHub の問題](https://github.com/pingcap/tiflash/issues)を作成したり、 [TUGに質問する](https://asktug.com/)に質問を送信したりすることもできます。

## 次は何か {#what-s-next}

-   TiFlash のバージョン、重要なログ、システム テーブルを確認するには、 [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md)参照してください。
-   特定のTiFlashノードを削除するには、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
