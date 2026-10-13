---
title: 統合タスク
summary: このページでは、{{{ .lake }}} における統合タスクの概要を説明します。統合タスクは、ソース設定、ターゲットテーブル、実行時パラメータなど、外部ソースから {{{ .lake }}} へのデータフローの定義に使用されます。
---

# 統合タスク

{{{ .lake }}} の統合タスクは、ソースから {{{ .lake }}} へどのようにデータが流れるかを定義します。各タスクは既存のデータソースを参照し、ソース設定、ターゲットの場所または結果の表示方法、およびタスクタイプ固有の実行時パラメータを指定します。

データソースとは異なり、統合タスクは実際にデータ移動、同期、またはメッセージ消費を実行する実行単位です。データソースはアクセス設定を保持し、タスクはスケジューリング、取り込み、同期、消費、停止、再開、および監視を処理します。

## サポートされるタスクタイプ {#supported-task-types}

| タスクタイプ | 説明 |
|--------------|------|
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | Amazon S3 から CSV、Parquet、または NDJSON ファイルをインポートします。1 回限りまたは継続的な取り込みをサポートします。 |
| [Amazon SQS (S3) (Preview)](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md) | SQS キューから S3 オブジェクト作成イベントを消費し、対応するオブジェクトデータを {{{ .lake }}} に書き込みます。 |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md) | `Snapshot`、`CDC Only`、または `Snapshot + CDC` を使用して MySQL からテーブルデータを同期します。 |
| [PostgreSQL](/tidb-cloud-lake/guides/integrate-with-postgresql.md) | `Snapshot`、`CDC Only`、または `Snapshot + CDC` を使用して PostgreSQL からテーブルデータを同期します。 |
| [Kafka Consumer 統合タスク (Preview)](/tidb-cloud-lake/guides/integrate-with-kafka.md) | Kafka トピックからメッセージを継続的に消費し、メッセージ内容を内部オブジェクトストレージに保存します。 |
| [TiDB 統合タスク (Preview)](/tidb-cloud-lake/guides/integrate-with-tidb.md) | `Snapshot`、`CDC Only`、または `Snapshot + CDC` を使用して TiDB からテーブルデータを同期します。 |

## 読み進め方 {#reading-guide}

推奨される読み進め方は次のとおりです。

1. まず [タスク管理](/tidb-cloud-lake/guides/task-management.md) を参照して、タスク作成フロー、開始 / 停止の動作、ステータス、および実行履歴を理解してください。
2. 次に、設定したいソースタイプに対応するタスク固有のガイドを参照してください。

## タスクタイプごとの違い {#task-type-differences}

- S3 タスクはファイルインポートのシナリオ向けに設計されており、主にファイルパスパターン、ファイル形式、および取り込み動作に重点を置いています。
- SQS (S3) タスクは S3 イベント駆動のデータ取り込み向けに設計されており、主に SQS キュー、S3 イベントフィルタ、IAM Role、およびターゲットテーブルに重点を置いています。
- MySQL、PostgreSQL、および TiDB タスクはテーブル同期のシナリオ向けに設計されており、主に同期モード、主キー、増分キャプチャ、およびアーカイブスケジューリングに重点を置いています。
- Kafka Consumer タスクはメッセージ消費のシナリオ向けに設計されており、主にトピック、開始位置、バッチサイズ、バッチ待機間隔、およびテナント stage クエリに重点を置いています。