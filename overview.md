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

[<a href="https://github.com/pingcap/tidb">TiDB</a>](https://github.com/pingcap/tidb) (/&#39;taɪdiːbi:/、「Ti」は Titanium の略) は、ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードをサポートするオープンソースの分散 SQL データベースです。 MySQL と互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。 TiDB の目標は、OLTP (オンライン トランザクション処理)、OLAP (オンライン分析処理)、および HTAP サービスをカバーするワンストップ データベース ソリューションをユーザーに提供することです。 TiDB は、高可用性と大規模データの強力な一貫性を必要とするさまざまなユースケースに適しています。

次のビデオでは、TiDB の主要な機能を紹介します。

<iframe width="600" height="450" src="https://www.youtube.com/embed/aWBNNPm21zg?enablejsapi=1" title="TiDB を選ぶ理由" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 主な特徴 {#key-features}

-   **水平方向のスケールアウトまたはスケールインが簡単に行えます**

    コンピューティングとstorageを分離する TiDBアーキテクチャ設計により、必要に応じてオンラインでコンピューティングまたはstorageの容量を個別にスケールアウトまたはスケールインできます。スケーリング プロセスは、アプリケーションの運用スタッフやメンテナンス スタッフにとって透過的です。

-   **金融グレードの高可用性**

    データは複数のレプリカに保存されます。データ レプリカは、Multi-Raft プロトコルを使用してトランザクション ログを取得します。トランザクションは、大部分のレプリカにデータが正常に書き込まれた場合にのみコミットできます。これにより、強力な一貫性と、少数のレプリカがダウンした場合の可用性が保証されます。さまざまな耐災害性レベルの要件を満たすために、必要に応じて地理的な場所とレプリカの数を構成できます。

-   **リアルタイムHTAP**

    TiDB は 2 つのstorageエンジンを提供します[<a href="/tikv-overview.md">TiKV</a>](/tikv-overview.md)は行ベースのstorageエンジン、 [<a href="/tiflash/tiflash-overview.md">TiFlash</a>](/tiflash/tiflash-overview.md)は列指向のstorageエンジンです。 TiFlash は、 Multi-Raft Learnerプロトコルを使用して TiKV からリアルタイムでデータを複製し、TiKV 行ベースのstorageエンジンとTiFlash の列型storageエンジン間のデータの一貫性を確保します。 TiKV とTiFlash は、 HTAP リソース分離の問題を解決するために、必要に応じて別のマシンにデプロイできます。

-   **クラウドネイティブな分散データベース**

    TiDB はクラウド用に設計された分散データベースであり、クラウド プラットフォーム上で柔軟な拡張性、信頼性、セキュリティを提供します。ユーザーは、変化するワークロードの要件に合わせて TiDB を柔軟に拡張できます。 TiDB では、各データには少なくとも 3 つのレプリカがあり、データセンター全体の停止に耐えられるように、異なるクラウド アベイラビリティ ゾーンにスケジュールできます。 [<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview">TiDB Operator</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview) 、Kubernetes 上で TiDB を管理し、TiDB クラスターの操作に関連するタスクを自動化するのに役立ちます。これにより、マネージド Kubernetes を提供するクラウドへの TiDB のデプロイが容易になります。フルマネージド TiDB サービスで[<a href="https://pingcap.com/tidb-cloud/">TiDB Cloud</a>](https://pingcap.com/tidb-cloud/)は、 [<a href="https://docs.pingcap.com/tidbcloud/">クラウド上の TiDB</a>](https://docs.pingcap.com/tidbcloud/)の機能を最大限に活用するための最も簡単、最も経済的、かつ回復力に優れた方法であり、数回クリックするだけで TiDB クラスターを展開して実行できます。

-   **MySQL 5.7プロトコルおよび MySQL エコシステムとの互換性**

    TiDB は、MySQL 5.7プロトコル、MySQL の共通機能、および MySQL エコシステムと互換性があります。アプリケーションを TiDB に移行する場合、多くの場合、コードを 1 行も変更する必要はありません。または、少量のコードを変更するだけで済みます。さらに、TiDB は、アプリケーション データを TiDB に簡単に移行するのに役立つ一連の[<a href="/ecosystem-tool-user-guide.md">データ移行ツール</a>](/ecosystem-tool-user-guide.md)を提供します。

## ユースケース {#use-cases}

-   **データの一貫性、信頼性、可用性、拡張性、耐災害性に対する高い要件を伴う金融業界のシナリオ**

    周知のとおり、金融業界にはデータの一貫性、信頼性、可用性、拡張性、耐災害性に対する高い要件があります。従来のソリューションは、同じ都市にある 2 つのデータ センターでサービスを提供し、別の都市にある 3 番目のデータ センターではデータ ディザスタ リカバリを提供しますが、サービスは提供しません。このソリューションには、リソース使用率が低い、メンテナンス コストが高い、RTO (目標復旧時間) と RPO (目標復旧時点) が期待に応えられないという欠点があります。 TiDB は、複数のレプリカと Multi-Raft プロトコルを使用して、さまざまなデータ センター、ラック、マシンにデータをスケジュールします。一部のマシンに障害が発生した場合、システムは自動的に切り替わり、システム RTO ≦ 30 秒および RPO = 0 が保証されます。

-   **storage容量、スケーラビリティ、同時実行性に対する高い要件を伴う、大量のデータと高い同時実行性のシナリオ**

    アプリケーションが急速に成長するにつれて、データも急増します。従来のスタンドアロン データベースでは、データ容量の要件を満たすことができません。解決策は、シャーディング ミドルウェアまたは分散 SQL データベース (TiDB など) を使用することであり、後者の方がコスト効率が高くなります。 TiDB は、個別のコンピューティングおよびstorageアーキテクチャを採用しており、コンピューティングまたはstorageの容量を個別にスケールアウトまたはスケールインできます。コンピューティングレイヤーは最大 512 ノードをサポートし、各ノードは最大 1,000 の同時実行をサポートし、最大クラスター容量は PB (ペタバイト) レベルです。

-   **リアルタイム HTAP シナリオ**

    5G、モノのインターネット、人工知能の急速な成長に伴い、企業が生成するデータは大幅に増加し続けており、その規模は数百 TB (テラバイト)、あるいは PB レベルに達することもあります。従来のソリューションは、OLTP データベースを使用してオンライン トランザクション アプリケーションを処理し、ETL (抽出、変換、ロード) ツールを使用してデータを OLAP データベースに複製してデータ分析を行うことでした。このソリューションには、storageコストの高さやリアルタイム パフォーマンスの低下など、複数の欠点があります。 TiDB は、v4.0 でTiFlash列型storageエンジンを導入し、TiKV 行ベースのstorageエンジンと組み合わせて、真の HTAP データベースとして TiDB を構築します。少量の追加storageコストで、オンライン トランザクション処理とリアルタイム データ分析の両方を同じシステムで処理できるため、コストが大幅に節約されます。

-   **データ集約と二次処理のシナリオ**

    ほとんどの企業のアプリケーション データは、さまざまなシステムに分散しています。アプリケーションが成長するにつれて、意思決定リーダーは会社全体のビジネス状況を理解し、適切なタイミングで意思決定を行う必要があります。この場合、企業は分散したデータを同一システムに集約し、二次処理を実行してT+0レポートまたはT+1レポートを生成する必要があります。従来のソリューションは ETL と Hadoop を使用することですが、Hadoop システムは複雑であり、運用と保守のコストとstorageのコストが高くなります。 Hadoop と比較すると、TiDB ははるかにシンプルです。 TiDB が提供する ETL ツールまたはデータ移行ツールを使用して、データを TiDB にレプリケートできます。 SQL ステートメントを使用してレポートを直接生成できます。

## こちらも参照 {#see-also}

-   [<a href="/tidb-architecture.md">TiDBアーキテクチャ</a>](/tidb-architecture.md)
-   [<a href="/tidb-storage.md">TiDBストレージ</a>](/tidb-storage.md)
-   [<a href="/tidb-computing.md">TiDB コンピューティング</a>](/tidb-computing.md)
-   [<a href="/tidb-scheduling.md">TiDB スケジューリング</a>](/tidb-scheduling.md)
