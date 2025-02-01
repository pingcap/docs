---
title: What is TiDB Self-Managed
summary: TiDB の主な機能と使用シナリオについて学習します。
---

# TiDB Self-Managedとは何か {#what-is-tidb-self-managed}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[ティビ](https://github.com/pingcap/tidb) (/&#39;taɪdiːbi:/、「Ti」は Titanium の略) は、ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードをサポートするオープンソースの分散 SQL データベースです。MySQL と互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。TiDB の目標は、OLTP (オンライン トランザクション処理)、OLAP (オンライン分析処理)、および HTAP サービスをカバーするワンストップ データベース ソリューションをユーザーに提供することです。TiDB は、大規模データで高可用性と強力な一貫性を必要とするさまざまなユース ケースに適しています。

TiDB Self-Managed は TiDB の製品オプションであり、ユーザーまたは組織は、完全な柔軟性をもって独自のインフラストラクチャ上で TiDB を展開および管理できます。TiDB Self-Managed を使用すると、環境を完全に制御しながら、オープン ソースの分散 SQL のパワーを活用できます。

次のビデオでは、TiDB の主な機能を紹介します。

<iframe width="600" height="450" src="https://www.youtube.com/embed/aWBNNPm21zg?enablejsapi=1" title="なぜ TiDB なのか?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 主な特徴 {#key-features}

-   **簡単な水平スケーリング**

    TiDBアーキテクチャ設計では、コンピューティングとstorageが分離されているため、必要に応じてコンピューティング容量またはstorage容量をオンラインでスケールアウトまたはスケールインできます。スケーリング プロセスは、アプリケーションの運用および保守スタッフに対して透過的です。

-   **金融グレードの高可用性**

    データは複数のレプリカに保存され、Multi-Raft プロトコルを使用してトランザクション ログが取得されます。トランザクションは、大多数のレプリカにデータが正常に書き込まれた場合にのみコミットできます。これにより、少数のレプリカがダウンした場合でも、強力な一貫性と可用性が保証されます。さまざまな災害耐性レベルを満たすために、必要に応じて地理的な場所とレプリカの数を構成できます。

-   **リアルタイムHTAP**

    TiDB は、行ベースのstorageエンジン[ティクヴ](/tikv-overview.md)と列ベースのstorageエンジン[TiFlash](/tiflash/tiflash-overview.md) 2 つのstorageエンジンを提供します。TiFlashは、 Multi-Raft Learnerプロトコルを使用して、TiKV からデータをリアルタイムで複製し、TiKV 行ベースのstorageエンジンとTiFlash列ベースのstorageエンジン間でデータの一貫性を確保します。TiKV とTiFlash は、 HTAP リソースの分離の問題を解決するために、必要に応じて異なるマシンに展開できます。

-   **クラウドネイティブ分散データベース**

    TiDB はクラウド向けに設計された分散データベースで、クラウド プラットフォーム上で柔軟な拡張性、信頼性、セキュリティを提供します。ユーザーは、変化するワークロードの要件に合わせて TiDB を柔軟に拡張できます。TiDB では、各データに少なくとも 3 つのレプリカがあり、異なるクラウド アベイラビリティ ゾーンにスケジュール設定して、データセンター全体の停止を許容できます[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview) 、Kubernetes 上の TiDB の管理に役立ち、TiDB クラスターの操作に関連するタスクを自動化するため、マネージド Kubernetes を提供するクラウドであればどこでも TiDB を簡単に導入できます[TiDB Cloud](https://pingcap.com/tidb-cloud/)は完全に管理された TiDB サービスであり、 [クラウド上の TiDB](https://docs.pingcap.com/tidbcloud/)のパワーを最大限に引き出す最も簡単、経済的、かつ最も回復力のある方法であり、数回クリックするだけで TiDB クラスターを導入して実行できます。

-   **MySQLプロトコルおよびMySQLエコシステムと互換性があります**

    TiDB は、MySQL プロトコル、MySQL の共通機能、および MySQL エコシステムと互換性があります。アプリケーションを TiDB に移行するには、多くの場合、コードを 1 行も変更する必要がないか、少量のコードを変更するだけで済みます。さらに、TiDB は、アプリケーション データを TiDB に簡単に移行できるようにするための一連の[データ移行ツール](/ecosystem-tool-user-guide.md)を提供します。

## ユースケース {#use-cases}

-   **金融業界のシナリオ**

    TiDB は、データの一貫性、信頼性、可用性、スケーラビリティ、および耐災害性に対する要件が高い金融業界のシナリオに最適です。従来のソリューションはコストがかかり、非効率的で、リソースの使用率が低く、メンテナンス コストが高くなります。TiDB は、複数のレプリカと Multi-Raft プロトコルを使用して、さまざまなデータ センター、ラック、およびマシンにデータをスケジュールし、システム RTO ≦ 30 秒、RPO = 0 を保証します。

-   **膨大なデータと高同時実行シナリオ**

    従来のスタンドアロン データベースでは、急速に成長するアプリケーションのデータ容量要件を満たすことができません。TiDB は、コンピューティングとstorageをアーキテクチャにアーキテクチャ化したコスト効率の高いソリューションで、コンピューティングまたはstorage容量を個別に簡単に拡張できます。コンピューティングレイヤーは最大 512 ノードをサポートし、各ノードは最大 1,000 の同時実行をサポートし、最大クラスター容量は PB (ペタバイト) レベルです。

-   **リアルタイム HTAP シナリオ**

    TiDB は、リアルタイム処理を必要とする大量のデータと高い同時実行性を伴うシナリオに最適です。TiDB は、v4.0 でTiFlash列指向storageエンジンを導入し、これを TiKV 行ベースstorageエンジンと組み合わせることで、TiDB を真の HTAP データベースとして構築します。わずかな追加storageコストで、オンライン トランザクション処理とリアルタイム データ分析の両方を同じシステムで処理できるため、コストを大幅に節約できます。

-   **データ集約と二次処理のシナリオ**

    TiDB は、散在するデータを同じシステムに集約し、二次処理を実行して T+0 または T+1 レポートを生成する必要がある企業に適しています。Hadoop と比較すると、TiDB ははるかにシンプルです。TiDB が提供する ETL (抽出、変換、ロード) ツールまたはデータ移行ツールを使用して、データを TiDB に複製できます。SQL ステートメントを使用してレポートを直接生成できます。

## 参照 {#see-also}

-   [TiDBアーキテクチャ](/tidb-architecture.md)
-   [TiDB ストレージ](/tidb-storage.md)
-   [TiDBコンピューティング](/tidb-computing.md)
-   [TiDB スケジューリング](/tidb-scheduling.md)
