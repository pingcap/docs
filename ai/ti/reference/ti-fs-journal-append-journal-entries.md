---
title: ti fs-journal append-journal-entries
summary: ファイルシステムジャーナルにエントリを追加します。
---

# ti fs-journal append-journal-entries

1 つの JSON イベントまたは JSON 配列をジャーナルに追加します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-journal append-journal-entries
  --journal-id <string>
  [--dry-run]
  [--entry-json <string>]
  [--entry-type <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--idempotency-key <string>]
  [--json-array]
  [--source <string>]
  [--subject <string>]
  [--version]
```

## オプション {#options}

- `--journal-id <string>`: ジャーナル ID。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--entry-json <string>`: 1 つの JSON ジャーナルエントリオブジェクト。繰り返し指定できます。サポートされるフィールドについては、[エントリ JSON 形式](#entry-json-format) を参照してください。
- `--entry-type <string>`: 入力オブジェクトで `type` が省略されている場合に使用するエントリタイプ。入力オブジェクト内で明示的に指定された `type` が優先されます。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステムトークンを設定します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択したファイルシステム用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--idempotency-key <string>`: 同じ追加リクエストの再試行を重複排除するために使用するキー。省略した場合、呼び出しごとに新しいキーが割り当てられます。
- `--json-array`: JSONL の代わりに標準入力から JSON 配列を読み取ります。
- `--source <string>`: エントリソース。
- `--subject <string>`: エントリのサブジェクト。繰り返し指定できます。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## エントリ JSON 形式 {#entry-json-format}

各入力オブジェクトは、次のフィールドをサポートします。

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `type` | string | イベントタイプ。`--entry-type` でデフォルトが指定されていない限り必須です。小文字で始まる必要があり、小文字、数字、アンダースコア (`_`)、ピリオド (`.`)、またはハイフン (`-`) を含めることができます。 |
| `schema_version` | integer | イベントペイロードのスキーマバージョン。`1` 未満の値は `1` として扱われます。 |
| `status` | string | オプションのユーザー定義ステータス。CLI はこれを小文字に変換します。 |
| `occurred_at` | RFC3339 timestamp | イベントが発生した時刻。省略した場合、サービスが時刻を設定します。 |
| `actor` | object | `type` および `id` の string フィールドを持つオプションのアクター。 |
| `source` | string | イベントソース。サポートされる値は `self_reported`、`gateway_observed`、`server_observed`、`imported` です。 \[default: `self_reported`] |
| `parent_entry_id` | string | オプションの親イベント ID。 |
| `correlation_id` | string | 関連するイベントをグループ化するためのオプションの ID。 |
| `subjects` | array of strings | `type:id` 形式のサブジェクト。`--subject` で指定した値はこの配列に追加されます。 |
| `summary` | JSON value | オプションのインラインイベントペイロード。 |

artifact 参照は現在サポートされていません。エントリに `artifacts` または `artifact_refs` を含めないでください。

`--source` を指定すると、すべての入力オブジェクトの `source` 値が置き換えられます。`--entry-type` は `type` が省略されているオブジェクトにのみ適用されます。

> **Important:**
>
> 追加操作を安全に再試行できるようにするには、論理リクエストに対する idempotency key を選択し、再試行のたびに同じキーを再利用してください。`--idempotency-key` を省略すると、再試行時に新しいキーが割り当てられ、重複したエントリが追加される可能性があります。

## 例 {#examples}

- 1 つの JSON エントリを追加します。

    ```bash
    # Record an event object and let the CLI or service apply default metadata.
    ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --entry-json '{"type":"task.started"}'
    ```

- 冪等な型付きエントリを追加します。

    ```bash
    # Prevent retries from recording the same completion event twice.
    ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --entry-type task.completed --subject issue:42 --idempotency-key issue-42-complete
    ```

- 標準入力から JSON 配列を追加します。

    ```bash
    # Batch multiple ordered events in a single append operation.
    printf '[{"type":"step.started"},{"type":"step.completed"}]' | ti fs-journal append-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --json-array
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md)