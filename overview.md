---
title: What is TiDB Self-Managed
summary: TiDB の主な機能と使用シナリオについて学習します。
---

# TiDBセルフマネージドとは {#what-is-tidb-self-managed}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[TiDB](https://github.com/pingcap/tidb) （/&#39;taɪdiːbi:/、「Ti」はTitaniumの略）は、ハイブリッドトランザクションおよび分析処理（HTAP）ワークロードをサポートするオープンソースの分散SQLデータベースです。MySQLと互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。TiDBの目標は、OLTP（オンライントランザクション処理）、OLAP（オンライン分析処理）、そしてHTAPサービスをカバーするワンストップデータベースソリューションをユーザーに提供することです。TiDBは、大規模データで高可用性と強力な一貫性が求められる様々なユースケースに適しています。

TiDBセルフマネージドは、TiDBの製品オプションです。ユーザーまたは組織は、独自のインフラストラクチャ上でTiDBを柔軟に導入・管理できます。TiDBセルフマネージドを利用することで、オープンソースの分散SQLのパワーを活用しながら、環境を完全に制御できます。

次のビデオでは、TiDB の主な機能を紹介します。

<iframe width="600" height="450" src="https://www.youtube.com/embed/aWBNNPm21zg?enablejsapi=1" title="なぜ TiDB なのか?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 主な特徴 {#key-features}

-   **簡単な水平スケーリング**

    TiDBアーキテクチャ設計はコンピューティングとstorageを分離しており、コンピューティング容量またはstorage容量を必要に応じてオンラインでスケールアウトまたはスケールインできます。スケーリングプロセスは、アプリケーションの運用および保守担当者にとって透過的です。

-   **金融グレードの高可用性**

    データは複数のレプリカに保存され、トランザクションログの取得にはMulti-Raftプロトコルが使用されます。トランザクションは、レプリカの過半数にデータが正常に書き込まれた場合にのみコミットされます。これにより、少数のレプリカがダウンした場合でも、強力な一貫性と可用性が保証されます。必要に応じて、地理的な場所とレプリカの数を設定することで、さまざまな災害耐性レベルに対応できます。

-   **リアルタイムHTAP**

    TiDBは、行ベースstorageエンジン[TiKV](/tikv-overview.md)と列ベースstorageエンジン（ [TiFlash](/tiflash/tiflash-overview.md)の2つのstorageエンジンを提供します。TiFlashは、Multi-Raft Learnerプロトコルを使用してTiKVからデータをリアルタイムに複製し、TiKV行ベースstorageエンジンとTiFlash列ベースstorageエンジン間のデータの一貫性を確保します。TiKVとTiFlashは、必要に応じて異なるマシンにデプロイすることで、HTAPリソースの分離問題を解決できます。

-   **クラウドネイティブ分散データベース**

    TiDB はクラウド向けに設計された分散データベースで、クラウド プラットフォーム上で柔軟な拡張性、信頼性、セキュリティを提供します。ユーザーは、変化するワークロードの要件に合わせて TiDB を弾力的に拡張できます。TiDB では、各データに少なくとも 3 つのレプリカがあり、それらを異なるクラウド アベイラビリティ ゾーンにスケジュールすることで、データセンター全体の停止を許容できます。1 [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview) Kubernetes 上の TiDB の管理を支援し、TiDB クラスターの運用に関連するタスクを自動化することで、マネージド Kubernetes を提供するあらゆるクラウドに TiDB をより簡単に導入できるようにします。3 [TiDB Cloud](https://pingcap.com/tidb-cloud/)完全に管理された TiDB サービスであり、 [クラウド上のTiDB](https://docs.pingcap.com/tidbcloud/)のパワーを最大限に引き出す最も簡単、経済的、かつ最も回復力のある方法であり、数回クリックするだけで TiDB クラスターを導入して実行できます。

-   **MySQLプロトコルおよびMySQLエコシステムと互換性があります**

    TiDBは、MySQLプロトコル、MySQLの共通機能、そしてMySQLエコシステムと互換性があります。アプリケーションをTiDBに移行する場合、多くの場合、コードを1行も変更する必要がなく、あるいはわずかなコードの変更のみで済みます。さらに、TiDBは、アプリケーションデータをTiDBに簡単に移行するための[データ移行ツール](/ecosystem-tool-user-guide.md)のツールを提供しています。

## ユースケース {#use-cases}

-   **金融業界のシナリオ**

    TiDBは、データの一貫性、信頼性、可用性、拡張性、そして耐災害性に対する高い要件が求められる金融業界のシナリオに最適です。従来のソリューションはコストが高く非効率で、リソース利用率が低く、メンテナンスコストも高くなります。TiDBは、複数のレプリカとMulti-Raftプロトコルを使用して、異なるデータセンター、ラック、マシンにデータをスケジュールすることで、システムのRTO（目標復旧時間）≦30秒、RPO = 0を実現します。

-   **膨大なデータと高同時実行のシナリオ**

    従来のスタンドアロンデータベースでは、急速に成長するアプリケーションのデータ容量要件を満たすことができません。TiDBは、コンピューティングとstorageを分離したアーキテクチャを採用した費用対効果の高いソリューションであり、コンピューティング容量またはstorage容量を個別に容易に拡張できます。コンピューティングレイヤーは最大512ノードをサポートし、各ノードは最大1,000の同時実行をサポートし、最大クラスタ容量はPB（ペタバイト）レベルです。

-   **リアルタイムHTAPシナリオ**

    TiDBは、膨大なデータと高い同時実行性を備え、リアルタイム処理が求められるシナリオに最適です。TiDBはv4.0でTiFlash列指向storageエンジンを導入し、TiKV行ベースstorageエンジンと組み合わせることで、真のHTAPデータベースを実現します。わずかなstorageコストを追加することで、オンライントランザクション処理とリアルタイムデータ分析の両方を同一システムで処理できるため、大幅なコスト削減につながります。

-   **データ集約と二次処理のシナリオ**

    TiDBは、散在するデータを同一システムに集約し、二次処理を実行してT+0またはT+1レポートを生成する必要がある企業に最適です。Hadoopと比較して、TiDBははるかにシンプルです。TiDBが提供するETL（抽出、変換、ロード）ツールやデータ移行ツールを使用して、TiDBにデータを複製できます。SQL文を使用してレポートを直接生成できます。

## 参照 {#see-also}

-   [TiDBアーキテクチャ](/tidb-architecture.md)
-   [TiDBストレージ](/tidb-storage.md)
-   [TiDBコンピューティング](/tidb-computing.md)
-   [TiDB スケジューリング](/tidb-scheduling.md)
