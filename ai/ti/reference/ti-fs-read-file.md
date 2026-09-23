---
title: ti fs read-file
summary: ファイルシステムからファイルを読み取ります。
---

# ti fs read-file

リモートファイルまたはバイト範囲を読み取り、標準出力に出力します。このコマンドのエイリアスは `ti fs cat` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs read-file
  --path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--length <int64>]
  [--offset <int64>]
  [--version]
```

## オプション {#options}

- `--path <string>`: 選択したファイルシステム内のファイルパスです。\[required]
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステムトークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択したファイルシステム用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--length <int64>`: 範囲読み取りのバイト長です。
- `--offset <int64>`: 範囲読み取りの 0 ベースのバイトオフセットです。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 完全なファイルを読み取る:

    ```bash
    # Write the remote file contents directly to standard output.
    ti fs read-file --file-system-id <file-system-id> --path /reports/report.md
    ```

- バイト範囲を読み取る:

    ```bash
    # Fetch only the requested range from a large remote object.
    ti fs read-file --file-system-id <file-system-id> --path /archives/large.bin --offset 1024 --length 4096
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)