---
title: ti fs-journal search-journal-entries
summary: Filesystem のジャーナルを検索し、必要に応じて一致するエントリを返します。
---

# ti fs-journal search-journal-entries

ジャーナルを検索し、必要に応じて一致するエントリを返します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-journal search-journal-entries
  [--actor <string>]
  [--cursor <string>]
  [--entry-type <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--include-entries]
  [--journal-kind <string>]
  [--label <string>]
  [--limit <int32>]
  [--since <string>]
  [--status <string>]
  [--subject <string>]
  [--until <string>]
  [--version]
```

## オプション {#options}

- `--actor <string>`: `type:id` 形式のアクター。
- `--cursor <string>`: 前のページで返されたカーソル。続きから取得する場合は、元のリクエストと同じフィルターを繰り返し指定します。
- `--entry-type <string>`: エントリタイプのフィルター。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--include-entries`: 一致結果に完全なエントリペイロードを含めます。
- `--journal-kind <string>`: ジャーナル種別のフィルター。
- `--label <string>`: `key=value` 形式のラベルフィルター。繰り返し指定できます。
- `--limit <int32>`: 読み取る一致結果の最大数。\[default: 100]
- `--since <string>`: 相対期間（`24h` など）または RFC3339 タイムスタンプで指定する下限時刻。
- `--status <string>`: エントリステータスのフィルター。
- `--subject <string>`: サブジェクトのフィルター。繰り返し指定できます。
- `--until <string>`: RFC3339 タイムスタンプで指定する上限時刻。相対期間は使用できません。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- エントリタイプで検索する場合:

    ```bash
    # Find journals containing task-start events and include their payloads.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --entry-type task.started --include-entries
    ```

- ラベルと時刻で検索する場合:

    ```bash
    # Limit deployment journal matches to one environment and time window.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --label env=dev --since 2026-07-01T00:00:00Z --limit 100
    ```

- アクターとサブジェクトで検索する場合:

    ```bash
    # Find events produced by one agent for a specific task subject.
    ti fs-journal search-journal-entries --file-system-id <file-system-id> --actor agent:ti --subject issue-42 --include-entries
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md)