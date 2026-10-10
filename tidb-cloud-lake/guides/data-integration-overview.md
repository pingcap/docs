---
title: データ統合の概要
summary: "{{{ .lake }}} の Data Integration 機能は、外部システムから {{{ .lake }}} にデータをインポートまたは同期するための、ビジュアルでノーコードのインターフェースを提供します。"
---

# データ統合の概要

{{{ .lake }}} の Data Integration 機能は、外部システムから {{{ .lake }}} にデータをインポート、同期、または取り込むための、ビジュアルでノーコードのインターフェースを提供します。この機能は、**データソース** と **統合タスク** という 2 つの主要な概念を中心に構成されています。

## 主要な概念 {#key-concepts}

| 概念 | 説明 |
|---------|-------------|
| [データソース](/tidb-cloud-lake/guides/data-sources.md) | 外部システムへのアクセスや通知の送信に使用する、再利用可能な接続設定または認証情報です。たとえば、AWS Access Key / Secret Key、MySQL hostname / username / password、SQS (S3) queue URL、Kafka broker addresses、または FeiShu bot webhook などがあります。 |
| [Integration Tasks](/tidb-cloud-lake/guides/integration-tasks.md) | データの取得元、タスクによるデータの書き込み先または結果の保存方法、使用するランタイムパラメータ、およびタスクの開始方法と監視方法を定義する実行可能なタスクです。 |

データソース自体はデータを移動しません。データソースは、外部システムにアクセスするために必要な情報を保存するだけです。統合タスクは、実際にインポート、スナップショット、継続的な同期、またはメッセージ消費を実行する単位です。

> **Note:**
>
> Data Integration タスクの実行には、サービスホスティング料金が発生します。{{{ .lake }}} は、サービスの実際の実行時間に基づいて、これらの料金を秒単位で課金します。詳細は、[サービスホスティング料金](/tidb-cloud-lake/guides/pricing-billing.md#service-hosting-pricing) を参照してください。

すべてのデータソースが取り込みタスクに対応するわけではありません。たとえば、`FeiShuBot` は、ソースデータを {{{ .lake }}} にロード (load) するためではなく、通知のために使用されます。

## サポートされる統合タスクの種類 {#supported-integration-task-types}

| タスクタイプ | 説明 |
|-----------|-------------|
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | Amazon S3 から CSV、Parquet、または NDJSON ファイルをインポートします。一度限りの取り込みと継続的な取り込みの両方をサポートします。 |
| [Amazon SQS (S3) (Preview)](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) | SQS キューから S3 オブジェクト作成イベントを消費し、対応するオブジェクトデータを {{{ .lake }}} に書き込みます。 |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md) | `Snapshot`、`CDC Only`、または `Snapshot + CDC` モードを使用して、MySQL からテーブルデータを同期します。 |
| [PostgreSQL](/tidb-cloud-lake/guides/integrate-with-postgresql.md) | `Snapshot`、`CDC Only`、または `Snapshot + CDC` モードを使用して、PostgreSQL からテーブルデータを同期します。 |
| [Kafka Consumer Integration Task (Preview)](/tidb-cloud-lake/guides/integrate-with-kafka.md) | Kafka トピックからメッセージを継続的に消費し、メッセージ内容を内部オブジェクトストレージに保存します。 |
| [TiDB Integration Task (Preview)](/tidb-cloud-lake/guides/integrate-with-tidb.md) | `Snapshot`、`CDC Only`、または `Snapshot + CDC` モードを使用して、TiDB からテーブルデータを同期します。 |

## 推奨フロー {#recommended-flow}

1. [データソース](/tidb-cloud-lake/guides/data-sources.md) ページで、再利用可能な接続設定を作成してテストします。
2. [Integration Tasks](/tidb-cloud-lake/guides/integration-tasks.md) ページで、サポートされるタスクタイプとそのユースケースを確認します。
3. タスク固有のガイドを読み、ソースを設定し、データをプレビューし、結果の保存先または結果の表示方法を設定します。
4. [タスク管理](/tidb-cloud-lake/guides/task-management.md) ページを使用して、タスクの開始、ステータスの確認、実行上の問題のトラブルシューティングを行います。