---
title: ti fs describe-file
summary: ファイルシステム内のファイルの情報を表示します。
---

# ti fs describe-file

1 つのリモートパスのメタデータを表示します。このコマンドのエイリアスは `ti fs stat` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs describe-file
  --path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--path <string>`: TiDB Cloud file system 内のファイルまたはディレクトリのパス。\[required]
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- リモートファイルの情報を表示する:

    ```bash
    # Inspect file size, metadata, tags, and revision information.
    ti fs describe-file --file-system-id <file-system-id> --path /reports/report.md
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)