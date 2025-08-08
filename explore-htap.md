---
title: Explore HTAP
summary: TiDB HTAPの機能を調べて使用する方法を学習します。
---

# HTAPを探索する {#explore-htap}

このガイドでは、TiDB ハイブリッド トランザクションおよび分析処理 (HTAP) の機能を調べて使用する方法について説明します。

> **注記：**
>
> TiDB HTAPを初めて使用し、すぐに使い始めたい場合は、 [TiDB HTAPのクイックスタート](/quick-start-with-htap.md)参照してください。

## ユースケース {#use-cases}

TiDB HTAP は、急速に増加する膨大なデータを処理し、DevOps のコストを削減し、セルフホスト環境またはクラウド環境に簡単に導入できるため、データ資産の価値をリアルタイムで実現します。

The following are the typical use cases of HTAP:

-   ハイブリッドワークロード

    When using TiDB for real-time Online Analytical Processing (OLAP) in hybrid load scenarios, you only need to provide an entry point of TiDB to your data. TiDB automatically selects different processing engines based on the specific business.

-   リアルタイムストリーム処理

    TiDBをリアルタイムストリーム処理シナリオで使用する場合、TiDBは絶えず流入するすべてのデータに対してリアルタイムでクエリを実行できることを保証します。同時に、TiDBは高度な同時実行性を持つデータワークロードやビジネスインテリジェンス（BI）クエリも処理できます。

-   データハブ

    TiDB をデータ ハブとして使用すると、TiDB はアプリケーションのデータとデータ ウェアハウスをシームレスに接続することで、特定のビジネス ニーズを満たすことができます。

TiDB HTAPの使用例の詳細については、 [PingCAPウェブサイトのHTAPに関するブログ](https://www.pingcap.com/blog/?tag=htap)参照してください。

TiDB の全体的なパフォーマンスを向上させるには、次の技術シナリオで HTAP を使用することをお勧めします。

-   分析処理パフォーマンスの向上

    アプリケーションに集計や結合操作などの複雑な分析クエリが含まれており、これらのクエリが大量のデータ (1,000 万行以上) に対して実行される場合、これらのクエリ内のテーブルがインデックスを効果的に使用できないか、インデックスの選択性が低いと、行ベースのstorageエンジン[TiKV](/tikv-overview.md)パフォーマンス要件を満たさない可能性があります。

-   ハイブリッドワークロード分離

    システムは、高同時実行性のオンライントランザクション処理（OLTP）ワークロードを処理する一方で、一部のOLAPワークロードも処理する必要があるかもしれません。システム全体の安定性を確保するためには、OLAPクエリがOLTPパフォーマンスに与える影響を回避する必要があります。

-   Simplify the ETL technology stack

    処理するデータ量が中規模（100TB未満）で、データ処理とスケジューリングのプロセスが比較的単純で、同時実行数もそれほど多くない（10未満）場合は、システムのテクノロジースタックを簡素化することを検討してください。OLTP、ETL、OLAPシステムで使用されている複数の異なるテクノロジースタックを単一のデータベースに置き換えることで、トランザクションシステムと分析システムの両方の要件を満たすことができます。これにより、技術的な複雑さが軽減され、保守担当者の必要性も軽減されます。

-   強一貫性分析

    リアルタイムで強力な一貫性のあるデータ分析と計算を実現し、分析結果がトランザクション データと完全に一致するようにするには、データのレイテンシーと不整合の問題を回避する必要があります。

## アーキテクチャ {#architecture}

TiDB では、オンライン トランザクション処理 (OLTP) 用の行ベースのstorageエンジン[TiKV](/tikv-overview.md)と、オンライン分析処理 (OLAP) 用の列ベースのstorageエンジン[TiFlash](/tiflash/tiflash-overview.md)共存し、データを自動的に複製し、強力な一貫性を維持します。

アーキテクチャの詳細については、 [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)参照してください。

## 環境準備 {#environment-preparation}

TiDB HTAPの機能を検討する前に、データ量に応じてTiDBと対応するstorageエンジンを導入する必要があります。データ量が大きい場合（例えば100 TB）、 TiFlash Massively Parallel Processing（MPP）をメインソリューションとして、TiSparkを補助ソリューションとして使用することをお勧めします。

-   TiFlash

    -   TiFlashノードのないTiDBクラスタをデプロイしている場合は、現在のTiDBクラスタにTiFlashノードを追加してください。詳細については、 [TiFlashクラスターのスケールアウト](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
    -   TiDB クラスターをまだデプロイしていない場合は、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。最小限の TiDB トポロジに基づいて、 [TiFlashのトポロジー](/tiflash-deployment-topology.md)もデプロイする必要があります。
    -   TiFlashノードの数を選択する方法を決定するときは、次のシナリオを考慮してください。

        -   小規模な分析処理とアドホッククエリを伴うOLTPが必要なユースケースでは、1つまたは複数のTiFlashノードを導入してください。これにより、分析クエリの速度が大幅に向上します。
        -   OLTPスループットがTiFlashノードのI/O使用率に大きな負担をかけない場合、各TiFlashノードはより多くのリソースを計算に使用するため、 TiFlashクラスターはほぼ線形のスケーラビリティを実現できます。TiFlashTiFlashの数は、期待されるパフォーマンスと応答時間に基づいて調整する必要があります。
        -   OLTPスループットが比較的高い場合（例えば、書き込みまたは更新スループットが1,000万行/時間を超える場合）、ネットワークおよび物理ディスクの書き込み容量の制限により、TiKVとTiFlash間のI/Oがボトルネックとなり、読み取りおよび書き込みのホットスポットが発生しやすくなります。この場合、 TiFlashノード数は分析処理の計算量と複雑な非線形関係にあるため、システムの実際の状況に基づいてTiFlashノード数を調整する必要があります。

-   ティスパーク

    -   Sparkでデータを分析する必要がある場合は、TiSparkをデプロイしてください。具体的な手順については、 [TiSpark ユーザーガイド](/tispark-overview.md)参照してください。

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## データ準備 {#data-preparation}

TiFlashを導入した後、TiKV はTiFlashにデータを自動的に複製しません。TiFlashに複製する必要があるテーブルを手動で指定する必要があります。その後、TiDB が対応するTiFlashレプリカを作成します。

-   TiDB クラスタにデータがない場合、まずTiDBにデータを移行してください。詳細については、 [データ移行](/migration-overview.md)参照してください。
-   TiDBクラスタに上流から複製されたデータが既に存在する場合、 TiFlashの導入後、データレプリケーションは自動的に開始されません。TiFlashに複製するテーブルを手動で指定する必要があります。詳細については、 [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)参照してください。

## データ処理 {#data-processing}

TiDBでは、クエリまたは書き込みリクエストにSQL文を入力するだけで済みます。TiFlashTiFlashを持つテーブルの場合、TiDBはフロントエンドオプティマイザーを使用して最適な実行プランを自動的に選択します。

> **注記：**
>
> TiFlashのMPPモードはデフォルトで有効になっています。SQL文が実行されると、TiDBはオプティマイザを通じてMPPモードで実行するかどうかを自動的に判断します。
>
> -   TiFlashの MPP モードを無効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)システム変数の値を`OFF`に設定します。
> -   クエリ実行時にTiFlashの MPP モードを強制的に有効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)と[tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を`ON`に設定します。
> -   TiDBが特定のクエリを実行する際にMPPモードを選択するかどうかを確認するには、 [MPPモードでステートメントを説明する](/explain-mpp.md#explain-statements-in-the-mpp-mode)参照してください。3 `EXPLAIN`のステートメントの出力に`ExchangeSender`と`ExchangeReceiver`演算子が含まれている場合、MPPモードが使用されています。

## Performance monitoring {#performance-monitoring}

TiDB を使用する場合、次のいずれかの方法で TiDB クラスターのステータスとパフォーマンス メトリックを監視できます。

-   [TiDBダッシュボード](/dashboard/dashboard-intro.md): you can see the overall running status of the TiDB cluster, analyse distribution and trends of read and write traffic, and learn the detailed execution information of slow queries.
-   [監視システム（PrometheusとGrafana）](/grafana-overview-dashboard.md): you can see the monitoring parameters of TiDB cluster-related components including PD, TiDB, TiKV, TiFlash, TiCDC, and Node_exporter.

TiDB クラスターとTiFlashクラスターのアラート ルールを確認するには、 [TiDB クラスタアラートルール](/alert-rules.md)と[TiFlash alert rules](/tiflash/tiflash-alert-rules.md)参照してください。

## トラブルシューティング {#troubleshooting}

TiDB の使用中に問題が発生した場合は、次のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [高価なクエリを特定する](/identify-expensive-queries.md)
-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDB cluster troubleshooting guide](/troubleshoot-tidb-cluster.md)
-   [TiFlashクラスタのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

[GitHub の問題](https://github.com/pingcap/tiflash/issues)を作成したり、 [TUGに質問する](https://asktug.com/)に質問を送信したりすることもできます。

## 次は何？ {#what-s-next}

-   TiFlash のバージョン、重要なログ、システム テーブルを確認するには、 [Maintain a TiFlash cluster](/tiflash/maintain-tiflash.md)参照してください。
-   特定のTiFlashノードを削除するには、 [TiFlashクラスターのスケールアウト](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
