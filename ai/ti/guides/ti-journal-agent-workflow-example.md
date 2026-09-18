---
title: TiDB Cloud Filesystem Journal にエージェントワークフローを記録する
summary: ジャーナルを作成し、構造化されたエージェントイベントを追記し、ワークフローを検索し、ジャーナルのハッシュチェーンを検証します。
---

# TiDB Cloud Filesystem Journal にエージェントワークフローを記録する

このワークフローでは、計画、ツール呼び出し、テスト、リトライ、ハンドオフを、構造化され、順序付けられ、検証可能なイベント履歴として記録します。これは、オペレーターが最新の状態だけを示す変更可能なステータスファイルや、散在したコンソール出力に頼るのではなく、複数のワーカーにまたがって何が起きたかを再構築する必要がある場合に使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 仕組み {#how-it-works}

Filesystem ジャーナルは、シーケンス情報、検索可能なフィールド、オプションの冪等性キー、ハッシュチェーン検証を備えた、構造化された追記専用エントリを保存します。通常のテキストファイルとは異なり、ジャーナルエントリは書き込まれた後に編集や切り詰めができず、プロデューサー側で独自のパース、並行処理、またはリトライ重複排除の仕組みを実装する必要もありません。エージェントは `task.started` や `test.finished` のような意味的イベントを追記し、オペレーターはワークフローをクエリして保存されたチェーンを検証できます。

## 前提条件 {#prerequisites}

設定済みのプロファイルまたは FS トークン環境を通じて Filesystem を選択します。

## ステップ 1. ジャーナルを作成する {#step-1-create-the-journal}

```bash
ti fs-journal create-journal \
  --journal-id jrn-agent-demo \
  --journal-kind agent \
  --title "dependency update" \
  --actor agent:dependency-bot \
  --label repository=demo \
  --label environment=test
```

## ステップ 2. ワークフローイベントを追記する {#step-2-append-workflow-events}

```bash
ti fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --idempotency-key dependency-update-start \
  --entry-json '{"type":"task.started","status":"running"}'

ti fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --entry-json '{"type":"test.finished","status":"passed","suite":"unit"}' \
  --entry-json '{"type":"task.finished","status":"completed"}'
```

ワークフローが同じ追記をリトライする可能性がある場合は、冪等性キーを指定し、その論理操作のすべてのリトライで同じキーを再利用します。これにより、サービスは重複エントリの保存を回避します。このオプションを省略すると新しいキーが生成され、リトライする予定のない追記にはそれが適切です。

## ステップ 3. 読み取りと検索 {#step-3-read-and-search}

```bash
ti fs-journal read-journal-entries \
  --journal-id jrn-agent-demo \
  --after-seq 0 \
  --limit 100 \
  --output text

ti fs-journal search-journal-entries \
  --entry-type task.finished \
  --status completed \
  --label repository=demo \
  --include-entries
```

`jrn-agent-demo` に対する順序付きの `read-journal-entries` の結果には、開始、テスト、完了の各イベントが含まれているはずです。

> **Note:**
>
> `search-journal-entries` はジャーナル ID を受け付けないため、選択した Filesystem 内のすべてのジャーナルを検索します。この例では、同じラベルとイベントフィールドを持つ別のジャーナルも検索結果に一致する可能性があります。

`--entry-type` と `--status` のフィルターは、各 `--entry-json` オブジェクト内の `type` フィールドと `status` フィールドに一致します。この例では、ペイロードに `"type":"task.finished"` と `"status":"completed"` を含むエントリを選択します。

## ステップ 4. 整合性を検証する {#step-4-verify-integrity}

```bash
ti fs-journal verify-journal \
  --journal-id jrn-agent-demo \
  --output text
```

結果が成功であれば、保存されたシーケンスとハッシュチェーンに整合性があることを確認できます。

## クリーンアップ {#cleanup}

ジャーナルは追記専用であり、現在の公開 `ti` コマンドには削除コマンドがありません。使い捨てジャーナルを作成する実験では、専用のテスト Filesystem と、`jrn-test-<run-id>` のような一意のジャーナル ID を使用してください。含まれているファイルやジャーナルがすべて不要になった場合にのみ、その Filesystem を削除してください。

## セキュリティおよび運用上の注意 {#security-and-operational-notes}

- API キー、パスワード、秘密情報を含む SQL テキスト、または生のファイル内容をジャーナルのペイロードに入れないでください。
- ハッシュチェーン検証は保存済みチェーンの不整合を検出しますが、元のイベントが真実であったことまでは証明しません。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md)
- [シークレットをエージェントに委任する](/ai/ti/guides/ti-vault-agent-secrets-example.md)
