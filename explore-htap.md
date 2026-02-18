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

HTAP の一般的な使用例は次のとおりです。

-   ハイブリッドワークロード

    ハイブリッドロードシナリオにおいて、リアルタイムオンライン分析処理（OLAP）にTiDBを使用する場合、データへのTiDBのエントリポイントを提供するだけで済みます。TiDBは、特定のビジネスに基づいて異なる処理エンジンを自動的に選択します。

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

-   ETLテクノロジースタックを簡素化

    処理するデータ量が中規模（100TB未満）で、データ処理とスケジューリングのプロセスが比較的単純で、同時実行数もそれほど多くない（10未満）場合は、システムのテクノロジースタックを簡素化することを検討してください。OLTP、ETL、OLAPシステムで使用されている複数の異なるテクノロジースタックを単一のデータベースに置き換えることで、トランザクションシステムと分析システムの両方の要件を満たすことができます。これにより、技術的な複雑さが軽減され、保守担当者の必要性も軽減されます。

-   強一貫性分析

    リアルタイムで強力な一貫性のあるデータ分析と計算を実現し、分析結果がトランザクション データと完全に一致するようにするには、データのレイテンシーと不整合の問題を回避する必要があります。

## アーキテクチャ {#architecture}

TiDB では、オンライン トランザクション処理 (OLTP) 用の行ベースのstorageエンジン[TiKV](/tikv-overview.md)と、オンライン分析処理 (OLAP) 用の列ベースのstorageエンジン[TiFlash](/tiflash/tiflash-overview.md)が共存し、データを自動的に複製し、強力な一貫性を維持します。

アーキテクチャの詳細については、 [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)参照してください。

## 環境の準備 {#environment-preparation}

TiDB HTAP機能を検討する前に、TiDBとその列指向storageエンジンでTiFlashを導入する必要があります。データ量が大きい場合（例えば100 TB）、ソリューションとしてTiFlash Massively Parallel Processing（MPP）の使用をお勧めします。

-   TiFlashノードのないTiDBクラスタをデプロイしている場合は、現在のTiDBクラスタにTiFlashノードを追加してください。詳細については、 [TiFlashクラスターのスケールアウト](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
-   TiDB クラスターをまだデプロイしていない場合は、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。最小限の TiDB トポロジに基づいて、 [TiFlashのトポロジー](/tiflash-deployment-topology.md)もデプロイする必要があります。
-   TiFlashノードの数を選択する方法を決定するときは、次のシナリオを考慮してください。

    -   小規模な分析処理とアドホッククエリを伴うOLTPが必要なユースケースでは、1つまたは複数のTiFlashノードを導入してください。これにより、分析クエリの速度が大幅に向上します。
    -   OLTPスループットがTiFlashノードのI/O使用率に大きな負担をかけない場合、各TiFlashノードはより多くのリソースを計算に使用するため、 TiFlashクラスターはほぼ線形のスケーラビリティを実現できます。TiFlashノードの数は、期待されるパフォーマンスと応答時間に基づいて調整する必要があります。
    -   OLTPスループットが比較的高い場合（例えば、書き込みまたは更新スループットが1,000万行/時間を超える場合）、ネットワークおよび物理ディスクの書き込み容量の制限により、TiKVとTiFlash間のI/Oがボトルネックとなり、読み取りおよび書き込みのホットスポットが発生しやすくなります。この場合、 TiFlashノード数は分析処理の計算量と複雑な非線形関係にあるため、システムの実際の状況に基づいてTiFlashノード数を調整する必要があります。

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## データ準備 {#data-preparation}

TiFlashを導入した後、TiKV はTiFlashにデータを自動的に複製しません。TiFlash にTiFlashする必要があるテーブルを手動で指定する必要があります。その後、TiDB が対応するTiFlashレプリカを作成します。

-   TiDB クラスタにデータがない場合、まずTiDBにデータを移行してください。詳細については、 [データ移行](/migration-overview.md)参照してください。
-   TiDBクラスタに上流から複製されたデータが既に存在する場合、 TiFlashの導入後、データレプリケーションは自動的に開始されません。TiFlashにTiFlashするテーブルを手動で指定する必要があります。詳細については、 [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)参照してください。

## データ処理 {#data-processing}

TiDBでは、クエリまたは書き込みリクエストにSQL文を入力するだけで済みます。TiFlashレプリカを持つテーブルの場合、TiDBはフロントエンドオプティマイザーを使用して最適な実行プランを自動的に選択します。

> **注記：**
>
> TiFlashのMPPモードはデフォルトで有効になっています。SQL文が実行されると、TiDBはオプティマイザを通じてMPPモードで実行するかどうかを自動的に判断します。
>
> -   TiFlashの MPP モードを無効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)システム変数の値を`OFF`に設定します。
> -   クエリ実行のためにTiFlashの MPP モードを強制的に有効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)と[tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を`ON`に設定します。
> -   TiDBが特定のクエリを実行する際にMPPモードを選択するかどうかを確認するには、 [MPPモードでステートメントを説明する](/explain-mpp.md#explain-statements-in-the-mpp-mode)参照してください。3 `EXPLAIN`ステートメントの出力に`ExchangeSender`と`ExchangeReceiver`演算子が含まれている場合、MPPモードが使用されています。

## パフォーマンス監視 {#performance-monitoring}

TiDB を使用する場合、次のいずれかの方法で TiDB クラスターのステータスとパフォーマンス メトリックを監視できます。

-   [TiDBダッシュボード](/dashboard/dashboard-intro.md) : TiDB クラスターの全体的な実行状態を確認したり、読み取りおよび書き込みトラフィックの分布と傾向を分析したり、遅いクエリの詳細な実行情報を確認したりできます。
-   [監視システム（PrometheusとGrafana）](/grafana-overview-dashboard.md) : PD、TiDB、TiKV、 TiFlash、TiCDC、Node_exporter などの TiDB クラスター関連コンポーネントの監視パラメータを確認できます。

TiDB クラスターとTiFlashクラスターのアラート ルールを確認するには、 [TiDB クラスタアラートルール](/alert-rules.md)と[TiFlashアラートルール](/tiflash/tiflash-alert-rules.md)参照してください。

## トラブルシューティング {#troubleshooting}

TiDB の使用中に問題が発生した場合は、次のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [高価なクエリを特定する](/identify-expensive-queries.md)
-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDB クラスタのトラブルシューティング ガイド](/troubleshoot-tidb-cluster.md)
-   [TiFlashクラスタのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

[GitHub の問題](https://github.com/pingcap/tiflash/issues)を作成したり、 [TUGに質問する](https://asktug.com/)に質問を送信したりすることもできます。

## 次は何か {#what-s-next}

-   TiFlash のバージョン、重要なログ、システム テーブルを確認するには、 [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md)参照してください。
-   特定のTiFlashノードを削除するには、 [TiFlashクラスターのスケールアウト](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
