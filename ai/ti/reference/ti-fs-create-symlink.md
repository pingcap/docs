---
title: ti fs create-symlink
summary: ファイルシステムにシンボリックリンクを作成します。
---

# ti fs create-symlink

シンボリックリンクを作成します。このコマンドのエイリアスは `ti fs symlink` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs create-symlink
  --link-path <string>
  --target <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--link-path <string>`: 作成するシンボリックリンクのファイルパスです。\[required]
- `--target <string>`: リンク先となる実際のファイルパスです。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステムトークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択したファイルシステム用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください.

## 例 {#examples}

- シンボリックリンクを作成します。

    ```bash
    # Create a relative symbolic link inside the remote namespace.
    ti fs create-symlink --file-system-id <file-system-id> --target final.md --link-path /reports/latest.md
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)