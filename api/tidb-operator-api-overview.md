---
title: TiDB Operator API Overview
summary: TiDB Operatorの API を学習します。
---

# TiDB OperatorAPI の概要 {#tidb-operator-api-overview}

[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/)は、Kubernetes上のTiDBクラスタの自動運用システムです。デプロイメント、アップグレード、スケーリング、バックアップ、フェイルオーバー、設定変更など、TiDBのライフサイクル全体にわたる管理を提供します。TiDB TiDB Operatorを使用することで、パブリッククラウドまたはプライベートクラウドにデプロイされたKubernetesクラスタ内でTiDBをシームレスに実行できます。

Kubernetes 上で TiDB クラスターを管理するには、次のTiDB OperatorAPI を使用できます。

-   [バックアップ](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#backup)
-   [バックアップスケジュール](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#backupschedule)
-   [DMCluster](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#dmcluster)
-   [復元する](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#restore)
-   [Tidbクラスタ](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#tidbcluster)
-   [Tidbイニシャライザー](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#tidbinitializer)
-   [Tidbモニター](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md#tidbmonitor)

詳細については[TiDB OperatorAPI ドキュメント](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md)参照してください。
