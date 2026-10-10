---
title: 継続的データパイプライン
summary: "{{{ .lake }}} で 2 つの基本機能を使って、エンドツーエンドの change data capture (CDC) フローを構築します。"
---

# 継続的データパイプライン

{{{ .lake }}} で 2 つの基本機能を使って、エンドツーエンドの change data capture (CDC) フローを構築します。

- **Streams** は、消費されるまで、すべての INSERT/UPDATE/DELETE をキャプチャします。
- **Tasks** は、スケジュールに従って、または stream が新しい行を報告したときに SQL を実行します。

## クイックナビゲーション {#quick-navigation}

- [例 1: 追記専用 Stream コピー](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-1-append-only-stream) – insert をキャプチャし、別のテーブルに消費します。
- [例 2: 標準 Stream の更新](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-2-standard-stream-updates--deletes) – update/delete がどのように現れるか、また 1 つの consumer だけが stream を drain できる理由を確認します。
- [例 3: 増分 Stream メトリクス](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-3-incremental-stream-join) – `WITH CONSUME` を使って複数の stream を join し、バッチごとに差分を計算します。
- [例 1: スケジュールされたコピー Task](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md#example-1-scheduled-copy) – 2 つの定期実行 task でファイルを生成してロードします。
- [例 2: Stream トリガーによるマージ](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md#example-2-stream-triggered-merge) – `STREAM_STATUS` が true のときだけ task を実行します。

## {{{ .lake }}} で CDC を使う理由 {#why-cdc-in-lake}

- **軽量** – stream は完全なテーブルを複製せずに、最新の変更セットを保持します。
- **トランザクション対応** – stream の消費は、SQL ステートメントとともに成功するかロールバックされます。
- **増分処理** – `WITH CONSUME` を使って同じクエリを再実行し、新しい行だけを処理できます。
- **スケジュール可能** – task を使うことで、すでに SQL で表現したコピー、merge、またはアラートのロジックを自動化できます。

まず stream の例を確認し、その後 task と組み合わせてパイプラインを自動化してください。