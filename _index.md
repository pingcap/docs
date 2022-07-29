---
title: TiDB Introduction
summary: Learn about the NewSQL database TiDB that supports HTAP workloads.
---

# TiDBの紹介 {#tidb-introduction}

[TiDB](https://github.com/pingcap/tidb) （/&#39;taɪdiːbi：/、 &quot;Ti&quot;はTitaniumの略）は、ハイブリッドトランザクションおよび分析処理（HTAP）ワークロードをサポートするオープンソースの分散型NewSQLデータベースです。これはMySQLと互換性があり、水平方向のスケーラビリティ、強力な一貫性、および高可用性を備えています。 TiDBは、オンプレミスまたはクラウド内にデプロイできます。

クラウド向けに設計されたTiDBは、クラウドプラットフォームで柔軟なスケーラビリティ、信頼性、セキュリティを提供します。ユーザーは、変化するワークロードの要件に合わせてTiDBを柔軟にスケーリングできます。 [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview)は、KubernetesでのTiDBの管理を支援し、運用タスクを自動化します。これにより、マネージドKubernetesを提供するクラウドへのTiDBのデプロイが容易になります。フルマネージドのTiDBサービスである[TiDB Cloud](https://pingcap.com/tidb-cloud/)は、 [クラウド内のTiDB](https://docs.pingcap.com/tidbcloud/)の全力を解き放つ最も簡単で、最も経済的で、最も回復力のある方法であり、数回クリックするだけでTiDBクラスターを展開および実行できます。

<NavColumns><NavColumn><ColumnTitle>TiDBについて</ColumnTitle>

-   [TiDBの紹介](/overview.md)
-   [基本的な機能](/basic-features.md)
-   [TiDB6.1リリースノート](/releases/release-6.1.0.md)
-   [TiDBリリースタイムライン](/releases/release-timeline.md)
-   [MySQLとの互換性](/mysql-compatibility.md)
-   [使用制限](/tidb-limitations.md)

</NavColumn>

<NavColumn><ColumnTitle>クイックスタート</ColumnTitle>

-   [TiDBのクイックスタート](/quick-start-with-tidb.md)
-   [HTAPのクイックスタート](/quick-start-with-htap.md)
-   [TiDBでSQLを探索する](/basic-sql-operations.md)
-   [HTAPを探索する](/explore-htap.md)

</NavColumn>

<NavColumn><ColumnTitle>デプロイして使用する</ColumnTitle>

-   [ハードウェアとソフトウェアの要件](/hardware-and-software-requirements.md)
-   [環境とConfiguration / コンフィグレーションを確認する](/check-before-deployment.md)
-   [TiUPを使用してTiDBクラスターをデプロイする](/production-deployment-using-tiup.md)
-   [分析処理にTiFlashを使用する](/tiflash/tiflash-overview.md)
-   [KubernetesにTiDBをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)

</NavColumn>

<NavColumn><ColumnTitle>データの移行</ColumnTitle>

-   [移行の概要](/migration-overview.md)
-   [CSVファイルからTiDBへのデータの移行](/migrate-from-csv-files-to-tidb.md)
-   [SQLファイルからTiDBへのデータの移行](/migrate-from-sql-files-to-tidb.md)
-   [AuroraからTiDBへのデータの移行](/migrate-aurora-to-tidb.md)

</NavColumn>

<NavColumn><ColumnTitle>管理</ColumnTitle>

-   [TiUPを使用してTiDBをアップグレードする](/upgrade-tidb-using-tiup.md)
-   [TiUPを使用してTiDBをスケーリングする](/scale-tidb-using-tiup.md)
-   [データのバックアップと復元](/br/backup-and-restore-overview.md)
-   [デプロイの導入と管理](/ticdc/manage-ticdc.md)
-   [TiUPを使用してTiDBを管理する](/maintain-tidb-using-tiup.md)
-   [TiFlashを管理する](/tiflash/maintain-tiflash.md)

</NavColumn>

<NavColumn><ColumnTitle>監視と警告</ColumnTitle>

-   [モニタリングフレームワーク](/tidb-monitoring-framework.md)
-   [モニタリングAPI](/tidb-monitoring-api.md)
-   [監視サービスのデプロイ](/deploy-monitoring-services.md)
-   [Grafanaスナップショットのエクスポート](/exporting-grafana-snapshots.md)
-   [アラートルールとソリューション](/alert-rules.md)
-   [TiFlashアラートルールとソリューション](/tiflash/tiflash-alert-rules.md)

</NavColumn>

<NavColumn><ColumnTitle>トラブルシューティング</ColumnTitle>

-   [TiDBトラブルシューティングマップ](/tidb-troubleshooting-map.md)
-   [遅いクエリを特定する](/identify-slow-queries.md)
-   [遅いクエリを分析する](/analyze-slow-queries.md)
-   [SQL診断](/information-schema/information-schema-sql-diagnostics.md)
-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDBクラスターのトラブルシューティング](/troubleshoot-tidb-cluster.md)
-   [TiCDCのトラブルシューティング](/ticdc/troubleshoot-ticdc.md)
-   [TiFlashのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

</NavColumn>

<NavColumn><ColumnTitle>参照</ColumnTitle>

-   [TiDBアーキテクチャ](/tidb-architecture.md)
-   [主要な監視指標](/grafana-overview-dashboard.md)
-   [TLSを有効にする](/enable-tls-between-clients-and-servers.md)
-   [権限管理](/privilege-management.md)
-   [ロールベースのアクセス制御](/role-based-access-control.md)
-   [証明書ベースの認証](/certificate-authentication.md)

</NavColumn>

<NavColumn><ColumnTitle>よくある質問</ColumnTitle>

-   [製品に関するFAQ](/faq/tidb-faq.md)
-   [高可用性に関するFAQ](/faq/high-availability-faq.md)
-   [SQLに関するFAQ](/faq/sql-faq.md)
-   [FAQのデプロイと管理](/faq/deploy-and-maintain-faq.md)
-   [アップグレードおよびアップグレード後のFAQ](/faq/upgrade-faq.md)
-   [移行に関するFAQ](/faq/migration-tidb-faq.md)

</NavColumn>
</NavColumns>
