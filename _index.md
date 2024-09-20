---
title: TiDB Introduction
hide_sidebar: true
hide_commit: true
summary: TiDB は、ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードをサポートするオープン ソースの分散 SQL データベースです。このガイドでは、機能、 TiFlash、開発、展開、移行、保守、監視、チューニング、ツール、リファレンスに関する情報を提供します。クイック スタートから TiDB の高度な構成やツールまで、すべてを網羅しています。
---

<LearningPathContainer platform="tidb" title="TiDB Self-Managed" subTitle="TiDB is an open-source distributed SQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. Find the guide, samples, and references you need to use TiDB.">

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

<LearningPath label="Learn" icon="cloud1">

[TiDBとは](https://docs.pingcap.com/tidb/v8.1/overview)

[特徴](https://docs.pingcap.com/tidb/v8.1/basic-features)

[TiFlash](https://docs.pingcap.com/tidb/v8.1/tiflash-overview)

</LearningPath>

<LearningPath label="Try" icon="cloud5">

[TiDB を試してみる](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb)

[HTAPを試してみる](https://docs.pingcap.com/tidb/v8.1/quick-start-with-htap)

[サンプルデータベースのインポート](https://docs.pingcap.com/tidb/v8.1/import-example-data)

</LearningPath>

<LearningPath label="Develop" icon="doc8">

[開発者ガイドの概要](https://docs.pingcap.com/tidb/v8.1/dev-guide-overview)

[クイックスタート](https://docs.pingcap.com/tidb/v8.1/dev-guide-build-cluster-in-cloud)

[アプリケーション例](https://docs.pingcap.com/tidb/v8.1/dev-guide-sample-application-java-spring-boot)

</LearningPath>

<LearningPath label="Deploy" icon="deploy">

[ソフトウェアおよびハードウェアの要件](https://docs.pingcap.com/tidb/v8.1/hardware-and-software-requirements)

[TiUPを使用して TiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

[Kubernetes に TiDBクラスタをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)

</LearningPath>

<LearningPath label="Migrate" icon="cloud3">

[移行の概要](https://docs.pingcap.com/tidb/v8.1/migration-overview)

[移行ツール](https://docs.pingcap.com/tidb/v8.1/migration-tools)

[典型的なシナリオ](https://docs.pingcap.com/tidb/v8.1/migrate-aurora-to-tidb)

</LearningPath>

<LearningPath label="Maintain" icon="maintain">

[クラスタのアップグレード](https://docs.pingcap.com/tidb/v8.1/upgrade-tidb-using-tiup)

[クラスタのスケール](https://docs.pingcap.com/tidb/v8.1/scale-tidb-using-tiup)

[クラスタデータのバックアップと復元](https://docs.pingcap.com/tidb/v8.1/backup-and-restore-overview)

[毎日のチェック](https://docs.pingcap.com/tidb/v8.1/daily-check)

[TiUPを使用して TiDB を管理](https://docs.pingcap.com/tidb/v8.1/maintain-tidb-using-tiup)

</LearningPath>

<LearningPath label="Monitor" icon="cloud6">

[PrometheusとGrafanaを使用する](https://docs.pingcap.com/tidb/v8.1/tidb-monitoring-framework)

[監視API](https://docs.pingcap.com/tidb/v8.1/tidb-monitoring-api)

[アラートルール](https://docs.pingcap.com/tidb/v8.1/alert-rules)

</LearningPath>

<LearningPath label="Tune" icon="tidb-cloud-tune">

[チューニングの概要](https://docs.pingcap.com/tidb/v8.1/performance-tuning-overview)

[チューニング方法](https://docs.pingcap.com/tidb/v8.1/performance-tuning-methods)

[OLTPパフォーマンスの調整](https://docs.pingcap.com/tidb/v8.1/performance-tuning-practices)

[オペレーティングシステムの調整](https://docs.pingcap.com/tidb/v8.1/tune-operating-system)

[構成の調整](https://docs.pingcap.com/tidb/v8.1/configure-memory-usage)

[SQLパフォーマンスのチューニング](https://docs.pingcap.com/tidb/v8.1/sql-tuning-overview)

</LearningPath>

<LearningPath label="Tools" icon="doc7">

[TiUP](https://docs.pingcap.com/tidb/v8.1/tiup-overview)

[TiDB Operator](https://docs.pingcap.com/tidb/v8.1/tidb-operator-overview)

[TiDB データ移行 (DM)](https://docs.pingcap.com/tidb/v8.1/dm-overview)

[TiDB Lightning](https://docs.pingcap.com/tidb/v8.1/tidb-lightning-overview)

[Dumpling](https://docs.pingcap.com/tidb/v8.1/dumpling-overview)

[ティCDC](https://docs.pingcap.com/tidb/v8.1/ticdc-overview)

[バックアップと復元 (BR)](https://docs.pingcap.com/tidb/v8.1/backup-and-restore-overview)

[PingCAPクリニック](https://docs.pingcap.com/tidb/v8.1/clinic-introduction)

</LearningPath>

<LearningPath label="Reference" icon="cloud-dev">

[TiDB ロードマップ](https://docs.pingcap.com/tidb/v8.1/tidb-roadmap)

[TiDBコンフィグレーションファイルのパラメータ](https://docs.pingcap.com/tidb/v8.1/tidb-configuration-file)

[TiDB コマンドラインフラグ](https://docs.pingcap.com/tidb/v8.1/command-line-flags-for-tidb-configuration)

[TiDB コントロール](https://docs.pingcap.com/tidb/v8.1/tidb-control)

[システム変数](https://docs.pingcap.com/tidb/v8.1/system-variables)

[リリースノート](https://docs.pingcap.com/tidb/v8.1/release-notes)

[FAQの概要](https://docs.pingcap.com/tidb/v8.1/faq-overview)

</LearningPath>

</LearningPathContainer>
