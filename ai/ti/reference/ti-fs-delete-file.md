---
title: ti fs delete-file
summary: TiDB Cloud Filesystem からファイルを削除します。
---

# ti fs delete-file

リモートのファイルまたはディレクトリを削除します。このコマンドのエイリアスは `ti fs rm` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs delete-file
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--recursive]
  [--version]
```

## オプション {#options}

- `--path <string>`: TiDB Cloud file system 内のファイルまたはディレクトリのパス。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されたトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--recursive`: ディレクトリを再帰的に削除します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- リモートファイルを削除する場合:

    ```bash
    # Remove one object from the selected Filesystem.
    ti fs delete-file --file-system-id <file-system-id> --path /reports/obsolete.md
    ```

- ディレクトリを再帰的に削除する場合:

    ```bash
    # Remove a directory and all of its descendants in one request.
    ti fs delete-file --file-system-id <file-system-id> --path /scratch --recursive
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)