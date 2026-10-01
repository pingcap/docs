---
title: TiDB Cloud Releases
summary: TiDB Cloud のリリースノート、カーネルのバージョン管理、メンテナンス通知について説明します。
---

# TiDB Cloudリリース {#tidb-cloud-releases}

[TiDB Cloud](https://www.pingcap.com/tidb/cloud/)は、オープンソースのハイブリッドトランザクションおよび分析処理（HTAP）データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)をクラウドに提供する、フルマネージドの Database-as-a-Service（DBaaS）です。

TiDB Cloud には、[クラウドプラットフォーム リリース](#cloud-platform-release-notes) と [データベース カーネル リリース](#database-kernel-release-notes) の 2種類のリリースがあります。これらは独立したリリース サイクルに従い、別々に文書化されています。

## クラウドプラットフォーム リリースノート

クラウドプラットフォーム リリースには、TiDB Cloud のコンソール、API、コントロールプレーンが含まれ、すべての TiDB Cloud プランにわたる新しいプラン機能、UI の変更、統合、運用上の改善が含まれます。

- [TiDB Cloud Release Notes](/tidb-cloud/releases/tidb-cloud-release-notes.md)

## データベース カーネル リリースノート

データベース カーネルは、SQL クエリを処理し、データを管理するコア エンジンです。TiDB Cloud プランに応じて、ご利用のリソースは異なるカーネルで実行され、それぞれ独自のリリース サイクルを持ちます。

| Plan | Kernel | Default kernel version for newly created instances or clusters |
| --- | --- | --- |
| TiDB Cloud **Starter** | クラシック TiDB カーネルをベースにしたカスタマイズ版 [TiDB X](/tidb-cloud/tidb-x-architecture.md) エンジンで実行されます。 | [TiDB v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3/) |
| TiDB Cloud **Essential** | 2026 年 6 月 30 日以降に作成された TiDB Cloud Essential インスタンスは、[TiDB X](/tidb-cloud/tidb-x-architecture.md) カーネルで実行されます。 | [TiDB-X-CLOUD.202603.1](/tidb-cloud/releases/tidb-x-cloud.202603.1.md) |
| TiDB Cloud **Premium** | [TiDB X](/tidb-cloud/tidb-x-architecture.md) カーネルで実行されます。 | [TiDB-X-CLOUD.202603.1](/tidb-cloud/releases/tidb-x-cloud.202603.1.md) |
| TiDB Cloud **Dedicated** | クラシック TiDB カーネルで実行されます。 | [TiDB v8.5.8](https://docs.pingcap.com/tidb/stable/release-8.5.8/) |

## メンテナンス通知 {#maintenance-notifications}

TiDB Cloudメンテナンス通知は、 TiDB Cloudサービスに影響を及ぼす可能性のある、スケジュールされたメンテナンス アクティビティに関する情報を提供します。通知の一覧については、左側のナビゲーションペインを参照してください。
