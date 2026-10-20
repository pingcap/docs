<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD041 -->

# 目次

## はじめに

- TiDB Cloud を選ぶ理由
  - [概要](/tidb-cloud/tidb-cloud-intro.md)
  - [機能](/tidb-cloud/features.md)
  - [PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md)
- はじめに
  - [TiDB Cloud Starter を試す](/tidb-cloud/starter/pg-quickstart.md)

## ガイド

- [プランを選択する](/tidb-cloud/select-cluster-tier.md)
- [TiDB Cloudのリソースとプロジェクトを管理する](/tidb-cloud/manage-projects-and-resources.md)
- {{{ .starter }}} インスタンスを管理する
  - [{{{ .starter }}} インスタンスを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)
  - [パブリックエンドポイント経由で {{{ .starter }}} インスタンスに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)
  - [TiDB Cloud データをバックアップおよび復元する](/tidb-cloud/backup-and-restore-serverless.md)
  - モニタリングとアラート
    - [概要](/tidb-cloud/monitor-tidb-cluster.md)
    - [組み込みメトリクス](/tidb-cloud/starter/built-in-monitoring-pg.md)
    - [イベント](/tidb-cloud/tidb-cloud-events.md)
  - [{{{ .starter }}} インスタンスを削除する](/tidb-cloud/delete-tidb-cluster.md)
- [PostgreSQL から TiDB Cloud Starter に移行する](/tidb-cloud/starter/import-with-psql.md)
- セキュリティ
  - [セキュリティ概要](/tidb-cloud/security-overview.md)
  - ID とアクセス制御
    - [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)
    - [標準SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md)
    - [Cloud Organization SSO認証](/tidb-cloud/tidb-cloud-org-sso-authentication.md)
    - [IDアクセス管理](/tidb-cloud/manage-user-access.md)
    - [OAuth 2.0](/tidb-cloud/oauth2.md)
  - ネットワークアクセス制御
    - [TiDB Cloud への TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)
  - 監査管理
    - [コンソール監査ログ](/tidb-cloud/tidb-cloud-console-auditing.md)

## リファレンス

- PostgreSQL 拡張機能
  - [概要](/tidb-cloud/starter/pg-extensions-overview.md)
  - [ベクトル検索](/tidb-cloud/starter/pg-vector-search.md)
  - [全文検索](/tidb-cloud/starter/pg-full-text-search.md)
  - [Parquet データをインポート](/tidb-cloud/starter/pg-parquet-import.md)
- SQL リファレンス
  - [概要](/tidb-cloud/starter/pg-sql-reference-overview.md)
  - [DDL](/tidb-cloud/starter/pg-ddl.md)
  - [DML とクエリ](/tidb-cloud/starter/pg-dml-queries.md)
  - [データ型](/tidb-cloud/starter/pg-data-types.md)
  - [組み込み関数](/tidb-cloud/starter/pg-built-in-functions.md)
  - [高度な SQL](/tidb-cloud/starter/pg-advanced-sql.md)
  - [認証とロール](/tidb-cloud/starter/pg-auth-roles.md)
  - [トランザクションと COPY](/tidb-cloud/starter/pg-transactions-copy.md)
  - [セッションパラメータ](/tidb-cloud/starter/pg-session-parameters.md)
  - [システムカタログ](/tidb-cloud/starter/pg-system-catalog.md)
  - [行レベルセキュリティ](/tidb-cloud/starter/pg-row-level-security.md)
  - [制限事項と制約](/tidb-cloud/starter/pg-limits-constraints.md)
- 一般リファレンス
  - TiDB Classic アーキテクチャ
    - [概要](/tidb-architecture.md)
    - [ストレージ](/tidb-storage.md)
    - [コンピューティング](/tidb-computing.md)
    - [スケジューリング](/tidb-scheduling.md)
    - [TSO](/tso.md)
  - [TiDB Xアーキテクチャ](/tidb-cloud/tidb-x-architecture.md)
  - ストレージエンジン
    - TiKV
      - [TiKVの概要](/tikv-overview.md)
      - [RocksDBの概要](/storage-engine/rocksdb-overview.md)
    - TiFlash
      - [TiFlashの概要](/tiflash/tiflash-overview.md)
      - [ディスクへのスピル](/tiflash/tiflash-spill-disk.md)
  - TiDB Cloud Partner Web Console
    - [TiDB Cloud パートナー](/tidb-cloud/tidb-cloud-partners.md)
    - [MSP顧客](/tidb-cloud/managed-service-provider-customer.md)
    - [再販業者の顧客](/tidb-cloud/cppo-customer.md)
  - [{{{ .starter }}} と Essential の制限事項](/tidb-cloud/serverless-limitations.md)
  - [TiDB X インスタンスで制限される SQL 機能](/tidb-cloud/limited-sql-features-tidb-x.md)
  - [TiDB の制限](/tidb-limitations.md)
  - [システム変数](/system-variables.md)
  - [サーバーステータス変数](/status-variables.md)
  - [テーブルフィルター](/table-filter.md)
  - [外部ストレージサービスの URI 形式](/external-storage-uri.md)
  - [データとインデックス間の不整合のトラブルシューティング](/troubleshoot-data-inconsistency-errors.md)
  - [通知](/tidb-cloud/notifications.md)
- サポートプラン
  - [Connected Careの概要](/tidb-cloud/connected-care-overview.md)
  - [Connected Careの詳細](/tidb-cloud/connected-care-detail.md)
  - Connected Care サポートサービスの機能
    - [Connected: IMでのAIチャット](/tidb-cloud/connected-ai-chat-in-im.md)
    - TiDB Cloud アラート向け Connected: IM サブスクリプション
      - [Slack経由で購読する](/tidb-cloud/monitor-alert-slack.md)
      - [Zoom経由で購読する](/tidb-cloud/monitor-alert-zoom.md)
      - [Flashduty経由で購読する](/tidb-cloud/monitor-alert-flashduty.md)
      - [PagerDuty経由で購読する](/tidb-cloud/monitor-alert-pagerduty.md)
      - [Webhook経由で購読する](/tidb-cloud/monitor-alert-webhook.md)
      - [Lark経由で購読する](/tidb-cloud/monitor-alert-lark.md)
    - Connected: IM チケット作成および更新サブスクリプション
      - [Slack 経由でチケットを作成し、チケット更新を購読する](/tidb-cloud/connected-slack-ticket-creation.md)
      - [Larkでチケットを作成し、チケットの更新を購読する](/tidb-cloud/connected-lark-ticket-creation.md)
    - Connected: サポートチケット向け IM インタラクション
      - [Slack経由でサポートチケットとやり取りする](/tidb-cloud/connected-slack-ticket-interaction.md)
      - [Lark経由でサポートチケットとやり取りする](/tidb-cloud/connected-lark-ticket-interaction.md)
  - [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)
- FAQ
  - [TiDB Cloudよくある質問](/tidb-cloud/tidb-cloud-faq.md)
  - [PostgreSQL互換 TiDB Cloud Starter FAQ](/tidb-cloud/starter/pg-faq.md)
- [用語集](/tidb-cloud/tidb-cloud-glossary.md)