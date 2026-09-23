---
title: ti fs-journal read-journal-entries
summary: file system ジャーナルからエントリを読み取ります。
---

# ti fs-journal read-journal-entries

1 つのジャーナルから、シーケンス順にエントリを読み取ります。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-journal read-journal-entries
  --journal-id <string>
  [--after-seq <int64>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--limit <int32>]
  [--version]
```

## オプション {#options}

- `--journal-id <string>`: ジャーナル ID。\[required]
- `--after-seq <int64>`: このシーケンス番号の後のエントリを読み取ります。省略した場合、または `0` に設定した場合は、最も早いエントリから読み取りを開始します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--limit <int32>`: 読み取るエントリの最大数。\[default: 100]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ジャーナルエントリを読み取る:

    ```bash
    # Return the first page of ordered entries for a journal.
    ti fs-journal read-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo
    ```

- シーケンス番号の後から続けて読み取る:

    ```bash
    # Read the next page after the last sequence processed by a consumer.
    ti fs-journal read-journal-entries --file-system-id <file-system-id> --journal-id jrn-demo --after-seq 100 --limit 50
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md)