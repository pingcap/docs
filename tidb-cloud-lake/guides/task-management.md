---
title: タスク管理
summary: このページでは、タスク作成フロー、開始および停止の動作、タスクの状態、実行履歴など、データ統合タスクの一般的な操作について説明します。ソース固有の設定については、各タスクの詳細ガイドを参照してください。
---

# タスク管理

このページでは、タスク作成フロー、開始および停止の動作、タスクの状態、実行履歴など、データ統合タスクの一般的な操作について説明します。ソース固有の設定については、各タスクの詳細ガイドを参照してください。

## 一般的なタスク作成フロー {#general-task-creation-flow}

1. **Data** > **Data Integration** に移動し、**Create Task** をクリックします。
2. 既存のデータソースを選択します。
3. ファイルパス、ソーステーブル、同期モード、トピック、フィルター条件など、タスクタイプに応じてソース側のパラメータを入力します。
4. ソースデータをプレビューし、スキーマ、フィールド型、またはメッセージ内容を確認します。
5. タスクタイプに応じて、対象の Warehouse と対象のデータベース / テーブルを選択するか、結果の表示方法を設定します。
6. タスクを作成し、必要に応じて開始します。

## タスクの開始と停止 {#starting-and-stopping-tasks}

タスク作成後の初期状態は **Stopped** です。同期、取り込み、または消費を開始するには、タスクの **Start** をクリックします。

実行中のタスクを停止するには、**Stop** をクリックします。タスクは現在の進行状況を保存しながら、正常にシャットダウンします。

## タスクのステータス {#task-status}

**Data Integration** ページには、すべてのタスクとその現在のステータスが表示されます。

| ステータス | 説明 |
|--------|-------------|
| Running | タスクがデータの同期、インポート、または消費を実行中です |
| Stopped | タスクは現在実行されていません |
| Failed | タスクの実行中にエラーが発生しました |

## 実行履歴の表示 {#viewing-run-history}

タスクをクリックすると、その実行履歴を表示できます。実行履歴には、次の情報が含まれます。

- 実行の開始時刻または終了時刻
- インポートまたは同期された行数、または書き込まれたメッセージオブジェクト数
- エラーの詳細（存在する場合）

## タスクタイプごとの実行時動作 {#runtime-behavior-by-task-type}

- S3 タスクは、1 回だけ実行することも、新しいファイルを継続的にポーリングすることもできます。
- MySQL `Snapshot` タスクは通常、フルロード (load) の完了後に自動的に停止します。
- MySQL `CDC Only` および `Snapshot + CDC` タスクは、手動で停止するまで実行を継続します。
- PostgreSQL `Snapshot` タスクは通常、フルロード (load) の完了後に自動的に停止します。
- PostgreSQL `CDC Only` および `Snapshot + CDC` タスクは、手動で停止するまで実行を継続します。
- SQS (S3) タスクは、SQS キューを継続的にポーリングし、S3 オブジェクト作成イベントを消費して、手動で停止するまでデータを対象テーブルに書き込みます。
- Kafka Consumer タスクは、Kafka トピックを継続的に消費し、手動で停止するまでメッセージ内容を内部オブジェクトストレージに保存します。

フィールドレベルの設定と詳細な動作については、対応するタスクガイドを参照してください。

- [Amazon S3 統合タスク](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md)
- [Amazon SQS (S3) 統合タスク (Preview)](/tidb-cloud-lake/guides/integrate-with-amazon-sqs-s3.md)
- [MySQL Integration Task](/tidb-cloud-lake/guides/integrate-with-mysql.md)
- [PostgreSQL Integration Task](/tidb-cloud-lake/guides/integrate-with-postgresql.md)
- [Kafka Consumer Integration Task (Preview)](/tidb-cloud-lake/guides/integrate-with-kafka.md)