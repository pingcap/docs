---
title: TiDB Introduction
summary: Learn about the key features and usage scenarios of TiDB.
---

# TiDB の紹介 {#tidb-introduction}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[TiDB](https://github.com/pingcap/tidb) (/&#39;taɪdiːbi:/、「Ti」は Titanium の略) は、ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードをサポートするオープンソースの分散 SQL データベースです。 MySQL と互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。 TiDB の目標は、OLTP (オンライン トランザクション処理)、OLAP (オンライン分析処理)、および HTAP サービスをカバーするワンストップ データベース ソリューションをユーザーに提供することです。 TiDB は、高可用性と大規模データの強力な一貫性を必要とするさまざまなユースケースに適しています。

次のビデオでは、TiDB の主要な機能を紹介します。

<iframe width="600" height="450" src="https://www.youtube.com/embed/aWBNNPm21zg?enablejsapi=1" title="TiDB を選ぶ理由" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 主な特徴 {#key-features}

-   **簡単な水平スケーリング**

    TiDBアーキテクチャ設計はコンピューティングをstorageから分離し、必要に応じてコンピューティングまたはstorageの容量をオンラインでスケールアウトまたはスケールインできるようにします。スケーリング プロセスは、アプリケーションの運用スタッフやメンテナンス スタッフにとって透過的です。

-   **金融グレードの高可用性**

    データは複数のレプリカに保存され、トランザクション ログの取得には Multi-Raft プロトコルが使用されます。トランザクションは、大部分のレプリカにデータが正常に書き込まれた場合にのみコミットできます。これにより、少数のレプリカがダウンした場合でも、強力な一貫性と可用性が保証されます。さまざまな災害耐性レベルを満たすために、必要に応じて地理的位置とレプリカの数を構成できます。

-   **リアルタイムHTAP**

    TiDB は 2 つのstorageエンジンを提供します[TiKV](/tikv-overview.md)は行ベースのstorageエンジン、 [TiFlash](/tiflash/tiflash-overview.md)は列指向のstorageエンジンです。 TiFlash は、 Multi-Raft Learnerプロトコルを使用して TiKV からリアルタイムでデータを複製し、TiKV 行ベースのstorageエンジンとTiFlash列型storageエンジンの間で一貫したデータを保証します。 TiKV とTiFlash は、 HTAP リソース分離の問題を解決するために、必要に応じて別のマシンにデプロイできます。

-   **クラウドネイティブな分散データベース**

    TiDB はクラウド用に設計された分散データベースであり、クラウド プラットフォーム上で柔軟な拡張性、信頼性、セキュリティを提供します。ユーザーは、変化するワークロードの要件に合わせて TiDB を柔軟に拡張できます。 TiDB では、各データに少なくとも 3 つのレプリカがあり、データセンター全体の停止に耐えられるように、異なるクラウド アベイラビリティ ゾーンにスケジュールできます。 [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview) Kubernetes 上で TiDB を管理し、TiDB クラスターの運用に関連するタスクを自動化するのに役立ち、マネージド Kubernetes を提供するあらゆるクラウドへの TiDB のデプロイが容易になります。フルマネージド TiDB サービスで[TiDB Cloud](https://pingcap.com/tidb-cloud/)は、 [クラウド上の TiDB](https://docs.pingcap.com/tidbcloud/)の機能を最大限に活用するための最も簡単、最も経済的、かつ復元力の高い方法であり、数回クリックするだけで TiDB クラスターを展開して実行できます。

-   **MySQL 5.7プロトコルおよび MySQL エコシステムとの互換性**

    TiDB は、MySQL 5.7プロトコル、MySQL の共通機能、および MySQL エコシステムと互換性があります。アプリケーションを TiDB に移行する場合、多くの場合、コードを 1 行も変更する必要はありません。または、少量のコードを変更するだけで済みます。さらに、TiDB は、アプリケーション データを TiDB に簡単に移行するのに役立つ一連の[データ移行ツール](/ecosystem-tool-user-guide.md)を提供します。

## ユースケース {#use-cases}

-   **金融業界のシナリオ**

    TiDB は、データの一貫性、信頼性、可用性、スケーラビリティ、耐災害性に対する高い要件が求められる金融業界のシナリオに最適です。従来のソリューションはコストが高く非効率的であり、リソース使用率が低く、メンテナンスコストが高くつきます。 TiDB は、複数のレプリカと Multi-Raft プロトコルを使用して、さまざまなデータセンター、ラック、マシンにデータをスケジュールし、システム RTO ≦ 30 秒および RPO = 0 を保証します。

-   **大量のデータと高い同時実行性のシナリオ**

    従来のスタンドアロン データベースでは、急速に成長するアプリケーションのデータ容量要件を満たすことができません。 TiDB は、個別のコンピューティング アーキテクチャとstorageアーキテクチャを採用したコスト効率の高いソリューションであり、コンピューティング容量またはstorage容量を個別に簡単にスケーリングできます。コンピューティングレイヤーは最大 512 ノードをサポートし、各ノードは最大 1,000 の同時実行をサポートし、最大クラスター容量は PB (ペタバイト) レベルです。

-   **リアルタイム HTAP シナリオ**

    TiDB は、リアルタイム処理を必要とする大量のデータと高い同時実行性を伴うシナリオに最適です。 TiDB は、v4.0 でTiFlash列型storageエンジンを導入し、TiKV 行ベースのstorageエンジンと組み合わせて、真の HTAP データベースとして TiDB を構築します。少量の追加storageコストで、オンライン トランザクション処理とリアルタイム データ分析の両方を同じシステムで処理できるため、コストが大幅に節約されます。

-   **データ集約と二次処理のシナリオ**

    TiDB は、分散したデータを同じシステムに集約し、二次処理を実行して T+0 または T+1 レポートを生成する必要がある企業に適しています。 Hadoop と比較すると、TiDB ははるかにシンプルです。 TiDB が提供する ETL (抽出、変換、ロード) ツールまたはデータ移行ツールを使用して、データを TiDB に複製できます。 SQL ステートメントを使用してレポートを直接生成できます。

## こちらも参照 {#see-also}

-   [TiDBアーキテクチャ](/tidb-architecture.md)
-   [TiDBストレージ](/tidb-storage.md)
-   [TiDB コンピューティング](/tidb-computing.md)
-   [TiDB スケジューリング](/tidb-scheduling.md)
