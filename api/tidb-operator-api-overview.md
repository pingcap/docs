---
title: TiDB Operator API Overview
summary: TiDB Operatorの API を学習します。
---

# TiDB Operator API の概要 {#tidb-operator-api-overview}

[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/)は、Kubernetes上のTiDBクラスタの自動運用システムです。デプロイメント、アップグレード、スケーリング、バックアップ、フェイルオーバー、設定変更など、TiDBのライフサイクル全体にわたる管理を提供します。TiDB Operatorを使用することで、パブリッククラウドまたはプライベートクラウドにデプロイされたKubernetesクラスタ内でTiDBをシームレスに実行できます。

Kubernetes 上で TiDB クラスターを管理するには、次のTiDB Operator API を使用できます。

-   [Backup](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#backup)
-   [BackupSchedule](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#backupschedule)
-   [DMCluster](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#dmcluster)
-   [Restore](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#restore)
-   [TidbCluster](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#tidbcluster)
-   [TidbInitializer](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#tidbinitializer)
-   [TidbMonitor](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#tidbmonitor)

詳細については[TiDB Operator API ドキュメント](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md)を参照してください。
