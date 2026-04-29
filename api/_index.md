---
title: TiDB API Overview
summary: TiDB CloudおよびTiDB Self-Managedで利用可能なAPIについて学びましょう。
---

# TiDB APIの概要 {#tidb-api-overview}

TiDBは、クラスタのクエリと操作、データレプリケーションの管理、システムステータスの監視などを行うためのさまざまなAPIを提供します。このドキュメントでは[TiDB Cloud](https://docs.pingcap.com/tidbcloud/)と[TiDBセルフマネージド](https://docs.pingcap.com/tidb/stable/)両方で利用可能なAPIの概要を説明します。 .

## TiDB CloudAPI（ベータ版） {#tidb-cloud-api-beta}

[TiDB CloudAPI](/api/tidb-cloud-api-overview.md)は[RESTインターフェース](https://en.wikipedia.org/wiki/Representational_state_transfer)APIであり、プロジェクト、クラスタ、バックアップ、リストア、インポート、請求、データサービスリソースなど、 TiDB Cloud内の管理オブジェクトをプログラムで管理するためのアクセスを提供します。

| API                                       | 説明                                                                           |
| ----------------------------------------- | ---------------------------------------------------------------------------- |
| [v1beta2](/api/tidb-cloud-api-v1beta2.md) | TiDB Cloud Premiumインスタンスを管理します。                                              |
| [v1beta1](/api/tidb-cloud-api-v1beta1.md) | TiDB Cloud Starter、 Essential、およびDedicatedクラスタに加え、課金、データサービス、 IAMリソースを管理します。 |
| [v1beta](/api/tidb-cloud-api-v1beta.md)   | TiDB Cloudのプロジェクト、クラスター、バックアップ、インポート、およびリストアを管理します。                          |

## TiDBセルフマネージドAPI {#tidb-self-managed-api}

TiDB Self-Managedは、TiDBツール用のさまざまなAPIを提供し、クラスタコンポーネントの管理、システムステータスの監視、データレプリケーションワークフローの制御を支援します。

| API                                                                                                                                    | 説明                                                                              |
| -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [TiProxy API](/tiproxy/tiproxy-api.md)                                                                                                 | TiProxyの設定、稼働状況、および監視データにアクセスできます。                                              |
| [データ移行API](/dm/dm-open-api.md)                                                                                                         | DMマスターノードとDMワーカーノード、データソース、およびデータレプリケーションタスクを管理します。                             |
| [モニタリングAPI](/tidb-monitoring-api.md)                                                                                                   | TiDBサーバーの実行状況、テーブルstorage情報、およびTiKVクラスタの詳細を取得します。                               |
| [TiCDC API](/ticdc/ticdc-open-api-v2.md)                                                                                               | TiCDCノードの状態を照会し、レプリケーションタスク（作成、一時停止、再開、更新操作など）を管理します。                           |
| [TiDB OperatorAPI](https://github.com/pingcap/tidb-operator/blob/%7B%7B%7B.tidb-operator-version%7D%7D%7D/docs/api-references/docs.md) | Kubernetes 上で TiDB クラスタを管理します。これには、デプロイ、アップグレード、スケーリング、バックアップ、フェイルオーバーなどが含まれます。 |
