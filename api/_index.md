---
title: TiDB API Overview
summary: TiDB Cloudおよび TiDB Self-Managed で利用可能な API について学習します。
aliases: ['/tidbcloud/api-overview/']
---

# TiDB APIの概要 {#tidb-api-overview}

TiDBは、クラスタのクエリと操作、データレプリケーションの管理、システムステータスの監視などのための様々なAPIを提供しています。このドキュメントでは、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)と[TiDBセルフマネージド](https://docs.pingcap.com/tidb/stable/)両方で利用可能なAPIの概要を説明します。

## TiDB CloudAPI (ベータ版) {#tidb-cloud-api-beta}

[TiDB CloudAPI](/api/tidb-cloud-api-overview.md)は、プロジェクト、クラスター、バックアップ、復元、インポート、課金、データ サービス リソースなど、 TiDB Cloud内の管理オブジェクトを管理するためのプログラムによるアクセスを提供する[RESTインターフェース](https://en.wikipedia.org/wiki/Representational_state_transfer)です。

| API                                      | 説明                                                                          |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| [v1ベータ1](/api/tidb-cloud-api-v1beta1.md) | TiDB Cloud Starter、Essential、Dedicated クラスターのほか、課金、データ サービス、 IAMリソースも管理します。 |
| [v1ベータ](/api/tidb-cloud-api-v1beta.md)   | TiDB Cloudのプロジェクト、クラスター、バックアップ、インポート、復元を管理します。                              |

## TiDB セルフマネージド API {#tidb-self-managed-api}

TiDB Self-Managed は、クラスター コンポーネントの管理、システム ステータスの監視、データ レプリケーション ワークフローの制御に役立つ TiDB ツール用のさまざまな API を提供します。

| API                                                                                                  | 説明                                                                       |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| [TiProxy API](/tiproxy/tiproxy-api.md)                                                               | TiProxy の構成、ヘルス ステータス、監視データにアクセスします。                                     |
| [データ移行API](/dm/dm-open-api.md)                                                                       | DM マスター ノードと DM ワーカー ノード、データ ソース、およびデータ レプリケーション タスクを管理します。              |
| [監視API](/tidb-monitoring-api.md)                                                                     | TiDBサーバーの実行ステータス、テーブルstorage情報、および TiKV クラスターの詳細を取得します。                  |
| [TiCDC API](/ticdc/ticdc-open-api-v2.md)                                                             | TiCDC ノードのステータスを照会し、操作の作成、一時停止、再開、更新などのレプリケーション タスクを管理します。               |
| [TiDB OperatorAPI](https://github.com/pingcap/tidb-operator/blob/v1.6.4/docs/api-references/docs.md) | デプロイメント、アップグレード、スケーリング、バックアップ、フェイルオーバーなど、Kubernetes 上の TiDB クラスターを管理します。 |
