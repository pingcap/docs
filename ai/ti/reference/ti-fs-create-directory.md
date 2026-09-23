---
title: ti fs create-directory
summary: ファイルシステムにディレクトリを作成します。
---

# ti fs create-directory

リモートディレクトリを作成します。このコマンドのエイリアスは `ti fs mkdir` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs create-directory
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--mode <string>]
  [--version]
```

## オプション {#options}

- `--path <string>`: 作成するディレクトリのファイルシステムパスです。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステムトークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択したファイルシステム用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--mode <string>`: 0755 などの 8 進数値で指定するディレクトリモードです。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください.

## 例 {#examples}

- リモートディレクトリを作成します。

    ```bash
    # Create the directory with explicit POSIX permission metadata.
    ti fs create-directory --file-system-id <file-system-id> --path /reports/archive --mode 0755
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)