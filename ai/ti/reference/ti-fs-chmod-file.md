---
title: ti fs chmod-file
summary: ファイルシステム内のファイル権限を変更します。
---

# ti fs chmod-file

リモートパスの POSIX モードメタデータを変更します。このコマンドのエイリアスは `ti fs chmod` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs chmod-file
  --mode <string>
  --path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--mode <string>`: 0644 などの 8 進数値で指定する権限モードです。\[required]
- `--path <string>`: ファイルまたはディレクトリのパスです。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステムトークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択したファイルシステム用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください.

## 例 {#examples}

- リモートの権限メタデータを変更します。

    ```bash
    # Restrict the selected file to owner read and write access.
    ti fs chmod-file --file-system-id <file-system-id> --path /reports/final.md --mode 0600
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)