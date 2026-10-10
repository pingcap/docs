---
title: データソース
summary: "{{{ .lake }}} のデータソースは、外部システムへの接続を表します。外部システムにアクセスするために必要な認証情報と接続の詳細を保存し、複数の統合タスクや通知シナリオで再利用できます。"
---

# データソース

{{{ .lake }}} のデータソースは、外部システムへの接続を表します。外部システムにアクセスするために必要な認証情報と接続の詳細を保存し、複数の統合タスクや通知シナリオで再利用できます。

データソース自体は同期を実行しません。その役割はアクセス設定を一元管理することであり、各タスクごとにアカウント、パスワード、キー、または通知エンドポイントを繰り返し入力する必要がなくなります。

## サポートされるデータソースの種類 {#supported-data-source-types}

| 種類 | 用途 |
|------|---------|
| [Amazon S3 - Credentials](/tidb-cloud-lake/guides/aws-credentials.md) | Amazon S3 へのアクセスに必要な Access Key と Secret Key を保存します。これらの認証情報は、複数の S3 インポートタスクで再利用できます。 |
| [Amazon SQS (S3) - IAM Role (Preview)](/tidb-cloud-lake/guides/amazon-sqs-s3-iam-role.md) | SQS (S3) の取り込みに必要な queue URL、リージョン、IAM Role、および S3 パススコープを保存します。S3 オブジェクト作成イベントの消費に使用できます。 |
| [MySQL - Credentials](/tidb-cloud-lake/guides/mysql-credentials.md) | MySQL へのアクセスに必要な host、port、username、password、および database 情報を保存します。これらの設定は、複数の MySQL 同期タスクで再利用できます。 |
| [PostgreSQL - Credentials](/tidb-cloud-lake/guides/postgresql-credentials.md) | PostgreSQL へのアクセスに必要な host、port、username、password、および database 情報を保存します。これらの設定は、複数の PostgreSQL 同期タスクで再利用できます。 |
| [FeiShuBot](/tidb-cloud-lake/guides/feishubot.md) | タスク失敗通知や類似のシナリオ向けに、FeiShu bot webhook とメッセージテンプレートを保存します。 |
| [Kafka - Credentials（プレビュー）](/tidb-cloud-lake/guides/kafka-credentials.md) | Kafka へのアクセスに必要な broker アドレス、認証方式、および接続認証情報を保存します。これらの設定は Kafka Consumer タスクで再利用できます。 |
| [TiDB - Credentials (Preview)](/tidb-cloud-lake/guides/integrate-with-tidb.md) | TiDB Cloud Lake が TiDB クラスターによって stage に配置されたデータを読み取るために使用する、オブジェクトストレージの場所、認証情報、およびオプションのイベントキューを保存します。これらの設定は、複数の TiDB 同期タスクで再利用できます。 |

すべてのデータソースが統合タスクに対応しているわけではありません。たとえば、`FeiShuBot` は通知設定に使用されます。一方、`Amazon S3 - Credentials`、`Amazon SQS (S3) - IAM Role`、`MySQL - Credentials`、`PostgreSQL - Credentials`、`TiDB - Credentials`、および `Kafka - Credentials` は、実際のインポート、同期、またはイベント消費タスクから参照されます。

## データソースの管理 {#managing-data-sources}

**Data** > **Data Sources** に移動します。このページでは、次の操作を実行できます。

- 設定済みのすべてのデータソースを表示する
- 新しいデータソースを作成する
- 既存のデータソースを編集または削除する
- 接続性をテストして認証情報を検証する

> **Tip:**
>
> データソースを保存する前に **Test Connectivity** を実行すると、無効な認証情報、権限不足、ネットワーク制限などの問題をできるだけ早く検出できます。

## 次のステップ {#next-steps}

データソースを作成した後は、その用途に応じて、[統合タスク](/tidb-cloud-lake/guides/integration-tasks.md) または通知設定で参照できます。