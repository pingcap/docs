---
title: ti fs list-files
summary: TiDB Cloud Filesystem 内のファイルを一覧表示します。
---

# ti fs list-files

リモートパス配下のエントリを一覧表示します。このコマンドのエイリアスは `ti fs ls` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs list-files
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--path <string>]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--path <string>`: ファイルシステムのディレクトリパスです。\[default: /]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- リモートディレクトリを一覧表示する場合:

    ```bash
    # Return the entries under a specific Filesystem path.
    ti fs list-files --file-system-id <file-system-id> --path /reports
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)