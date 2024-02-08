---
title: TiDB Introduction
hide_sidebar: true
hide_commit: true
summary: TiDB is an open-source distributed SQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. The guide provides information on features, TiFlash, development, deployment, migration, maintenance, monitoring, tuning, tools, and references. It covers everything from quick start to advanced configurations and tools for TiDB.
---

<LearningPathContainer platform="tidb" title="TiDB" subTitle="TiDB is an open-source distributed SQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. Find the guide, samples, and references you need to use TiDB.">

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

<LearningPath label="Learn" icon="cloud1">

[TiDBとは](https://docs.pingcap.com/tidb/v7.5/overview)

[特徴](https://docs.pingcap.com/tidb/v7.5/basic-features)

[TiFlash](https://docs.pingcap.com/tidb/v7.5/tiflash-overview)

</LearningPath>

<LearningPath label="Try" icon="cloud5">

[TiDB を試してみる](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb)

[HTAP を試してみる](https://docs.pingcap.com/tidb/v7.5/quick-start-with-htap)

[サンプルデータベースのインポート](https://docs.pingcap.com/tidb/v7.5/import-example-data)

</LearningPath>

<LearningPath label="Develop" icon="doc8">

[開発者ガイドの概要](https://docs.pingcap.com/tidb/v7.5/dev-guide-overview)

[クイックスタート](https://docs.pingcap.com/tidb/v7.5/dev-guide-build-cluster-in-cloud)

[応用例](https://docs.pingcap.com/tidb/v7.5/dev-guide-sample-application-java-spring-boot)

</LearningPath>

<LearningPath label="Deploy" icon="deploy">

[ソフトウェアとハ​​ードウェアの要件](https://docs.pingcap.com/tidb/v7.5/hardware-and-software-requirements)

[TiUPを使用した TiDBクラスタのデプロイ](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

[TiDBクラスタをKubernetes にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)

</LearningPath>

<LearningPath label="Migrate" icon="cloud3">

[移行の概要](https://docs.pingcap.com/tidb/v7.5/migration-overview)

[移行ツール](https://docs.pingcap.com/tidb/v7.5/migration-tools)

[典型的なシナリオ](https://docs.pingcap.com/tidb/v7.5/migrate-aurora-to-tidb)

</LearningPath>

<LearningPath label="Maintain" icon="maintain">

[クラスタをアップグレードする](https://docs.pingcap.com/tidb/v7.5/upgrade-tidb-using-tiup)

[クラスタをスケールする](https://docs.pingcap.com/tidb/v7.5/scale-tidb-using-tiup)

[クラスタデータのバックアップと復元](https://docs.pingcap.com/tidb/v7.5/backup-and-restore-overview)

[毎日のチェック](https://docs.pingcap.com/tidb/v7.5/daily-check)

[TiUPを使用して TiDBを管理](https://docs.pingcap.com/tidb/v7.5/maintain-tidb-using-tiup)

</LearningPath>

<LearningPath label="Monitor" icon="cloud6">

[プロメテウスとグラファナを使用する](https://docs.pingcap.com/tidb/v7.5/tidb-monitoring-framework)

[モニタリングAPI](https://docs.pingcap.com/tidb/v7.5/tidb-monitoring-api)

[アラートルール](https://docs.pingcap.com/tidb/v7.5/alert-rules)

</LearningPath>

<LearningPath label="Tune" icon="tidb-cloud-tune">

[チューニングの概要](https://docs.pingcap.com/tidb/v7.5/performance-tuning-overview)

[チューニング方法](https://docs.pingcap.com/tidb/v7.5/performance-tuning-methods)

[OLTP パフォーマンスを調整する](https://docs.pingcap.com/tidb/v7.5/performance-tuning-practices)

[オペレーティング システムを調整する](https://docs.pingcap.com/tidb/v7.5/tune-operating-system)

[構成を調整する](https://docs.pingcap.com/tidb/v7.5/configure-memory-usage)

[SQL パフォーマンスの調整](https://docs.pingcap.com/tidb/v7.5/sql-tuning-overview)

</LearningPath>

<LearningPath label="Tools" icon="doc7">

[TiUP](https://docs.pingcap.com/tidb/v7.5/tiup-overview)

[TiDB Operator](https://docs.pingcap.com/tidb/v7.5/tidb-operator-overview)

[TiDB データ移行 (DM)](https://docs.pingcap.com/tidb/v7.5/dm-overview)

[TiDB Lightning](https://docs.pingcap.com/tidb/v7.5/tidb-lightning-overview)

[Dumpling](https://docs.pingcap.com/tidb/v7.5/dumpling-overview)

[TiCDC](https://docs.pingcap.com/tidb/v7.5/ticdc-overview)

[バックアップと復元 (BR)](https://docs.pingcap.com/tidb/v7.5/backup-and-restore-overview)

[PingCAPクリニック](https://docs.pingcap.com/tidb/v7.5/clinic-introduction)

</LearningPath>

<LearningPath label="Reference" icon="cloud-dev">

[TiDB ロードマップ](https://docs.pingcap.com/tidb/dev/tidb-roadmap)

[TiDBコンフィグレーションファイルのパラメータ](https://docs.pingcap.com/tidb/v7.5/tidb-configuration-file)

[TiDB コマンドライン フラグ](https://docs.pingcap.com/tidb/v7.5/command-line-flags-for-tidb-configuration)

[TiDB コントロール](https://docs.pingcap.com/tidb/v7.5/tidb-control)

[システム変数](https://docs.pingcap.com/tidb/v7.5/system-variables)

[リリースノート](https://docs.pingcap.com/tidb/v7.5/release-notes)

[FAQの概要](https://docs.pingcap.com/tidb/v7.5/faq-overview)

</LearningPath>

</LearningPathContainer>
