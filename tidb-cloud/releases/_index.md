---
title: TiDB Cloud Releases
summary: TiDB Cloud のリリース ノート、カーネルのバージョン管理、メンテナンス通知について説明します。
---

# TiDB Cloudリリース {#tidb-cloud-releases}

[TiDB Cloud](https://www.pingcap.com/tidb/cloud/)は、オープンソースのハイブリッドトランザクションおよび分析処理（HTAP）データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)をクラウドに提供する、フルマネージドの Database-as-a-Service（DBaaS）です。

TiDB Cloud には、[クラウドプラットフォーム リリース](#cloud-platform-release-notes) と [データベース カーネル リリース](#database-kernel-release-notes) の 2 種類のリリースがあります。これらは独立したリリース サイクルに従い、別々に文書化されています。

## クラウドプラットフォーム リリースノート

クラウドプラットフォーム リリースには、TiDB Cloud のコンソール、API、コントロール プレーンが含まれ、すべての TiDB Cloud プランにわたる新しいプラン機能、UI の変更、統合、運用上の改善が含まれます。

- [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md)

## データベース カーネル リリースノート

データベース カーネルは、SQL クエリを処理し、データを管理するコア エンジンです。TiDB Cloud プランに応じて、ご利用のリソースは異なるカーネルで実行され、それぞれ独自のリリース サイクルを持ちます。

| Plan | Kernel information and release notes |
| --- | --- |
| TiDB Cloud **Starter** | クラシック [TiDB v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3/) カーネルをベースにしたカスタマイズ版 [TiDB X](/tidb-cloud/tidb-x-architecture.md) エンジンで実行されます。 |
| TiDB Cloud **Essential** | デフォルトでは、クラシック [TiDB v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3/) カーネルをベースにしたカスタマイズ版 [TiDB X](/tidb-cloud/tidb-x-architecture.md) エンジンで実行されます。 |
| TiDB Cloud **Premium** | [TiDB X](/tidb-cloud/tidb-x-architecture.md) カーネルの [`TiDB-X-CLOUD.202510.1`](/tidb-cloud/releases/tidb-x-cloud.202510.1.md) バージョンで実行されます。 |
| TiDB Cloud **Dedicated** | クラシック TiDB カーネルで実行され、カーネル バージョンは TiDB Self-Managed のバージョンに直接対応します。現在、新しく作成された TiDB Cloud Dedicated クラスターのデフォルト TiDB バージョンは [v8.5.7](https://docs.pingcap.com/tidb/stable/release-8.5.7/) です。 |

> **Note:**
>
> TiDB Cloud Essential インスタンスを TiDB Cloud Premium と同じカーネルで実行したい場合は、[TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) にお問い合わせください。

## メンテナンス通知 {#maintenance-notifications}

TiDB Cloudメンテナンス通知は、 TiDB Cloudサービスに影響を及ぼす可能性のある、スケジュールされたメンテナンス アクティビティに関する情報を提供します。通知の一覧については、左側のナビゲーション ペインを参照してください。
