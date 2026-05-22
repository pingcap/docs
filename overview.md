---
title: What is TiDB Self-Managed
summary: TiDBの主な機能と使用例について学びましょう。
---

# TiDB Self-Managedとは何ですか？ {#what-is-tidb-self-managed}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[TiDB](https://github.com/pingcap/tidb) （/&#39;taɪdiːbi:/、「Ti」はチタンの略）は、ハイブリッドトランザクションおよび分析処理（HTAP）ワークロードをサポートするオープンソースの分散型SQLデータベースです。MySQLと互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。TiDBの目標は、OLTP（オンライントランザクション処理）、OLAP（オンライン分析処理）、およびHTAPサービスを網羅するワンストップのデータベースソリューションをユーザーに提供することです。TiDBは、大規模データで高い可用性と強力な一貫性を必要とするさまざまなユースケースに適しています。

TiDB Self-Managedは、TiDBの製品オプションの一つで、ユーザーや組織が独自のインフラストラクチャ上にTiDBを柔軟にデプロイおよび管理できます。TiDB Self-Managedを利用することで、オープンソースの分散型SQLのパワーを享受しながら、環境を完全に制御できます。

以下のビデオでは、TiDBの主な機能を紹介します。

<iframe width="600" height="450" src="https://www.youtube.com/embed/aWBNNPm21zg?enablejsapi=1" title="Why TiDB?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 主な機能 {#key-features}

-   **水平方向のスケーリングが容易**

    TiDBのアーキテクチャ設計では、コンピューティングとストレージが分離されているため、必要に応じてコンピューティングまたはストレージ容量をオンラインでスケールアウトまたはスケールインできます。このスケーリングプロセスは、アプリケーションの運用および保守担当者にとって透過的です。

-   **金融グレードの高可用性**

    データは複数のレプリカに保存され、トランザクションログの取得にはマルチラフトプロトコルが使用されます。トランザクションは、データが過半数のレプリカに正常に書き込まれた場合にのみコミットされます。これにより、レプリカの一部がダウンした場合でも、高い一貫性と可用性が保証されます。必要に応じて、地理的な場所とレプリカの数を設定することで、さまざまな耐障害性レベルに対応できます。

-   **リアルタイムHTAP**

    TiDBは、行ベースストレージエンジンである[TiKV](/tikv-overview.md)と、カラム型ストレージエンジンである[TiFlash](/tiflash/tiflash-overview.md)という2つのストレージエンジンを提供します。TiFlashは、Multi-Raftラーナープロトコルを使用してTiKVからリアルタイムでデータを複製し、TiKV行ベースストレージエンジンとTiFlashカラム型ストレージエンジン間のデータの一貫性を確保します。HTAPリソースの分離問題を解決するために、必要に応じてTiKVとTiFlashを異なるマシンにデプロイできます。

-   **クラウドネイティブ分散データベース**

    TiDB はクラウド向けに設計された分散データベースで、クラウド プラットフォーム上で柔軟なスケーラビリティ、信頼性、セキュリティを提供します。ユーザーは、変化するワークロードの要件に合わせて TiDB を柔軟に拡張できます。TiDB では、各データに少なくとも 3 つのレプリカがあり、異なるクラウド可用性ゾーンにスケジュールすることで、データ センター全体の停止にも対応できます。TiDB [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview) Kubernetes 上での TiDB の管理を支援し、TiDB クラスターの運用に関連するタスクを自動化することで、マネージド Kubernetes を提供するあらゆるクラウドへの TiDB のデプロイを容易にします。フル マネージド TiDB サービスである[TiDB Cloud](https://pingcap.com/tidb-cloud/) 、[クラウド上のTiDB](https://docs.pingcap.com/tidbcloud/)の真の力を引き出す最も簡単で経済的かつ堅牢な方法であり、数回のクリックだけで TiDB クラスターをデプロイして実行できます。

-   **MySQLプロトコルおよびMySQLエコシステムと互換性があります。**

    TiDBはMySQLプロトコル、MySQLの共通機能、およびMySQLエコシステムと互換性があります。アプリケーションをTiDBに移行する場合、多くの場合、コードを1行も変更する必要はなく、ごくわずかなコードの変更だけで済みます。さらに、TiDBはデータをTiDBに簡単に移行するための[データ移行ツール](/ecosystem-tool-user-guide.md)を提供します。

## ユースケース {#use-cases}

-   **金融業界のシナリオ**

    TiDBは、データの一貫性、信頼性、可用性、拡張性、耐障害性に対する要求が高い金融業界のシナリオに最適です。従来のソリューションは、コストが高く非効率的で、リソース利用率が低く、メンテナンスコストが高額でした。TiDBは、複数のレプリカとマルチラフトプロトコルを使用して、データを異なるデータセンター、ラック、マシンにスケジュールすることで、システムのRTO≦30秒、RPO=0を実現します。

-   **大規模データと高並行処理のシナリオ**

    従来のスタンドアロン型データベースでは、急速に成長するアプリケーションのデータ容量要件を満たすことができません。TiDBは、コンピューティングとストレージを分離したアーキテクチャを採用したコスト効率の高いソリューションであり、コンピューティング容量とストレージ容量を個別に容易に拡張できます。コンピューティングレイヤーは最大512ノードをサポートし、各ノードは最大1,000の同時実行数をサポート、クラスターの最大容量はペタバイト（PB）レベルです。

-   **リアルタイムHTAPシナリオ**

    TiDBは、リアルタイム処理を必要とする膨大なデータ量と高い同時実行性を伴うシナリオに最適です。TiDBはバージョン4.0で、列指向ストレージエンジンTiFlashを導入しました。これは、行指向ストレージエンジンTiKVと組み合わせることで、TiDBを真のHTAPデータベースとして構築します。わずかなストレージコストを追加するだけで、オンライントランザクション処理とリアルタイムデータ分析の両方を同一システムで処理できるため、コストを大幅に削減できます。

-   **データ集約および二次処理シナリオ**

    TiDBは、分散したデータを同一システムに集約し、二次処理を実行してT+0またはT+1レポートを生成する必要がある企業に適しています。Hadoopと比較すると、TiDBははるかにシンプルです。TiDBが提供するETL（抽出、変換、ロード）ツールまたはデータ移行ツールを使用して、データをTiDBに複製できます。レポートはSQLステートメントを使用して直接生成できます。

## 関連項目 {#see-also}

-   [TiDBアーキテクチャ](/tidb-architecture.md)
-   [TiDBストレージ](/tidb-ストレージ.md)
-   [TiDBコンピューティング](/tidb-computing.md)
-   [TiDBスケジューリング](/tidb-scheduling.md)

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="Why #TiDB?" type="video" link="https://www.youtube.com/watch?v=aWBNNPm21zg" imgSrc="https://i.ytimg.com/vi/aWBNNPm21zg/hqdefault.jpg" author="PingCAP" duration="2 mins" />
</RelatedResources>
