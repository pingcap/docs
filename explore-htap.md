---
title: Explore HTAP
summary: TiDB HTAPの機能を探究し、活用する方法を学びましょう。
---

# HTAPを探索する {#explore-htap}

このガイドでは、TiDB ハイブリッドトランザクションおよび分析処理 (HTAP) の機能の探索方法と使用方法について説明します。

> **注記：**
>
> TiDB HTAP を初めて使用し、すぐに使い始めたい場合は、 [TiDB HTAPクイックスタート](/quick-start-with-htap.md)を参照してください。

## ユースケース {#use-cases}

TiDB HTAPは、急速に増加する膨大なデータを処理し、DevOpsのコストを削減し、オンプレミス環境とクラウド環境のどちらにも容易に導入できるため、データ資産の価値をリアルタイムで実現します。

HTAPの典型的な使用例は以下のとおりです。

-   ハイブリッドワークロード

    ハイブリッドロードシナリオでリアルタイムオンライン分析処理（OLAP）にTiDBを使用する場合、データへのTiDBのエントリポイントを提供するだけで済みます。TiDBは、特定の業務に基づいて異なる処理エンジンを自動的に選択します。

-   リアルタイムストリーム処理

    TiDBをリアルタイムストリーム処理シナリオで使用する場合、TiDBは絶えず流入するすべてのデータをリアルタイムでクエリできることを保証します。同時に、TiDBは高負荷な同時データワークロードやビジネスインテリジェンス（BI）クエリも処理できます。

-   データハブ

    TiDBをデータハブとして使用する場合、TiDBはアプリケーションのデータとデータウェアハウスのデータをシームレスに接続することで、特定のビジネスニーズを満たすことができます。

TiDB HTAPの使用例の詳細については、 [PingCAPウェブサイト上のHTAPに関するブログ](https://www.pingcap.com/blog/?tag=htap)参照してください。

TiDBの全体的なパフォーマンスを向上させるため、以下の技術的なシナリオではHTAPを使用することをお勧めします。

-   分析処理性能を向上させる

    アプリケーションに集計や結合操作などの複雑な分析クエリが含まれ、これらのクエリが大量のデータ（1,000万行以上）に対して実行される場合、これらのクエリ内のテーブルがインデックスを効果的に使用できないか、インデックスの選択性が低い場合、行ベースのstorageエンジン[ティクヴ](/tikv-overview.md)はパフォーマンス要件を満たせない可能性があります。

-   ハイブリッドワークロードの分離

    高負荷なオンライン・トランザクション処理（OLTP）ワークロードを処理する際、システムは同時にOLAPワークロードも処理する必要が生じる場合があります。システム全体の安定性を確保するため、OLAPクエリがOLTPのパフォーマンスに与える影響を回避することが求められます。

-   ETLテクノロジースタックを簡素化する

    処理するデータ量が中規模（100 TB未満）で、データ処理とスケジューリングのプロセスが比較的単純で、同時実行数が高くない（10未満）場合は、システムのテクノロジースタックを簡素化することを検討すると良いでしょう。OLTP、ETL、OLAPシステムで使用されている複数の異なるテクノロジースタックを単一のデータベースに置き換えることで、トランザクションシステムと分析システムの両方の要件を満たすことができます。これにより、技術的な複雑さが軽減され、保守担当者の必要性も低減されます。

-   非常に一貫性のある分析

    リアルタイムかつ高い一貫性を備えたデータ分析と計算を実現し、分析結果がトランザクションデータと完全に一致するようにするには、データのレイテンシーや不整合の問題を回避する必要があります。

## アーキテクチャ {#architecture}

TiDBでは、オンライン・トランザクション処理（OLTP）用の行ベースのstorageエンジン[ティクヴ](/tikv-overview.md)と、オンライン分析処理（OLAP）用の列ベースのstorageエンジンである[TiFlash](/tiflash/tiflash-overview.md)が共存し、データを自動的に複製し、強力な一貫性を維持します。

アーキテクチャの詳細については、 [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)を参照してください。

## 環境準備 {#environment-preparation}

TiDB HTAPの機能を検討する前に、TiDBとそのカラム型storageエンジンであるTiFlashを導入する必要があります。データ量が大きい場合（例えば100テラバイト）、ソリューションとしてTiFlashの大規模並列処理（MPP）を使用することをお勧めします。

-   TiFlashノードのない TiDB クラスターをデプロイした場合は、現在の TiDB クラスターにTiFlashノードを追加します。詳細については、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
-   TiDB クラスターをデプロイしていない場合は、 [TiUPを使用してTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。最小限の TiDB トポロジーに基づいて、 [TiFlashのトポロジー](/tiflash-deployment-topology.md)もデプロイする必要があります。
-   TiFlashノードの数を決定する際には、以下のシナリオを考慮してください。

    -   小規模な分析処理とアドホッククエリを伴うOLTPが必要な場合は、1台または複数台のTiFlashノードを導入してください。分析クエリの速度を劇的に向上させることができます。
    -   OLTPのスループットがTiFlashノードのI/O使用率に大きな負荷をかけない場合、各TiFlashノードは計算により多くのリソースを使用するため、 TiFlashクラスタはほぼ線形のスケーラビリティを実現できます。TiFlashノードの数は、期待されるパフォーマンスと応答時間に基づいて調整する必要があります。
    -   OLTPのスループットが比較的高い場合（例えば、書き込みまたは更新のスループットが1時間あたり1,000万行を超える場合）、ネットワークディスクと物理ディスクの書き込み容量が限られているため、TiKVとTiFlash間のI/Oがボトルネックとなり、読み書きのホットスポットが発生しやすくなります。この場合、 TiFlashノードの数は解析処理の計算量と複雑な非線形関係にあるため、システムの実際の状態に基づいてTiFlashノードの数を調整する必要があります。

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## データ準備 {#data-preparation}

TiFlashがデプロイされた後、TiKVは自動的にTiFlashにデータを複製しません。TiFlashにTiFlashする必要のあるテーブルを手動で指定する必要があります。その後、TiDBが対応するTiFlashレプリカを作成します。

-   TiDBクラスタにデータがない場合は、まずデータを TiDB に移行します。詳細については、[データ移行](/migration-overview.md)参照してください。
-   TiDBクラスタに既にアップストリームからレプリケートされたデータが存在する場合、 TiFlashのデプロイ後、データレプリケーションは自動的に開始されません。TiFlashにレプリケートするテーブルを手動で指定する必要があります。詳細については、 TiFlash[TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)参照してください。 。

## データ処理 {#data-processing}

TiDBでは、クエリや書き込みリクエストに対してSQL文を入力するだけで済みます。TiFlashレプリカを持つテーブルの場合、TiDBはフロントエンドオプティマイザを使用して最適な実行プランを自動的に選択します。

> **注記：**
>
> TiFlashのMPPモードはデフォルトで有効になっています。SQL文が実行されると、TiDBはオプティマイザを通じてMPPモードで実行するかどうかを自動的に判断します。
>
> -   TiFlashの MPP モードを無効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)システム変数の値を`OFF`に設定します。
> -   TiFlashの MPP モードをクエリ実行用に強制的に有効にするには、 [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50)と[tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を`ON`に設定します。
> -   TiDB が特定のクエリを実行する際に MPP モードを選択しているかどうかを確認するには、 [MPPモードの説明文](/explain-mpp.md#explain-statements-in-the-mpp-mode)を参照してください。 `EXPLAIN`ステートメントの出力に`ExchangeSender`および`ExchangeReceiver`演算子が含まれている場合、MPP モードが使用されています。

## パフォーマンス監視 {#performance-monitoring}

TiDBを使用する場合、TiDBクラスタの状態とパフォーマンス指標は、以下のいずれかの方法で監視できます。

-   [TiDBダッシュボード](/dashboard/dashboard-intro.md): TiDBクラスターの全体的な実行ステータスを確認し、読み取りおよび書き込みトラフィックの分布と傾向を分析し、遅いクエリの詳細な実行情報を知ることができます。
-   [監視システム（PrometheusおよびGrafana）](/grafana-overview-dashboard.md) : PD、TiDB、TiKV、 TiFlash、TiCDC、Node_exporterなどのTiDBクラスター関連コンポーネントの監視パラメータを確認できます。

TiDB クラスターおよびTiFlashクラスターのアラート ルールを確認するには、 [TiDBクラスタアラートルール](/alert-rules.md)および[TiFlashアラートルール](/tiflash/tiflash-alert-rules.md)を参照してください。

## トラブルシューティング {#troubleshooting}

TiDBの使用中に問題が発生した場合は、以下のドキュメントを参照してください。

-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [高額なクエリを特定する](/identify-expensive-queries.md)
-   [ホットスポットの問題をトラブルシューティングする](/troubleshoot-hot-spot-issues.md)
-   [TiDBクラスタのトラブルシューティングガイド](/troubleshoot-tidb-cluster.md)
-   [TiFlashクラスタのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

[GitHub Issues](https://github.com/pingcap/tiflash/issues)を作成したり、 [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)のコミュニティに質問したりすることもできます。

## 次は？ {#what-s-next}

-   TiFlash のバージョン、重要なログ、システム テーブルを確認するには、 [TiFlashクラスタを管理](/tiflash/maintain-tiflash.md)参照してください。
-   特定のTiFlashノードを削除するには、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
