---
title: TiDB Cloud BYOC 共同検証
summary: このドキュメントでは、TiDB Cloud BYOC デプロイの共同検証プロセスについて説明します。
---

# TiDB Cloud BYOC 共同検証

最終フェーズでは、環境が安定しており、安全で、かつ十分に可観測であることを確認します。TiDB Cloud チームは、お客様と連携して以下のチェックを実施します。

## 検証チェックリスト {#validation-checklist}

| カテゴリ | 検証項目 | 担当者 |
| :---- | :---- | :---- |
| **接続性** | SQL Endpoint: アプリケーションサーバーからプライベートおよびパブリックの両方の SQL エンドポイントへの接続性を確認します。 | Customer |
| **接続性** | Secure Tunnel (optional): Bastion Host 経由の VPN 接続が安定していることを確認します。 | TiDB Cloud |
| **可観測性** | Metrics: Grafana および Prometheus でシステムメトリクスが正しく表示されていることを確認します。 | TiDB Cloud |
| **可観測性** | Logging: ログが収集されていることを確認します。 | TiDB Cloud |
| **セキュリティ** | Audit: AWS CloudTrail が Bastion Host へのアクセス試行をアクティブに記録していることを確認します。 | Customer |
| **アラート** | Test Alerts: テストアラートをトリガーして、通知配信システムが機能していることを確認します。 | Joint |

すべての検証項目が **Pass** とマークされたら、次の状態になります。

1. このデプロイは正式に **Complete** と見なされます。
2. データ移行またはアプリケーション統合に進むことができます。

## 次のステップ {#what-s-next}

{{{ .byoc }}} デプロイの検証が完了したら、アプリケーションをインスタンスに接続し、データを移行するか、監視、バックアップ、セキュリティなどの運用機能の設定を続けることができます。デプロイ時に付与される権限をさらに削減するには、[TiDB Cloud BYOC Security Hardening](/tidb-cloud/byoc/security-hardening.md) を参照してください。