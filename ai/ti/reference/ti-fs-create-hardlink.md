---
title: ti fs create-hardlink
summary: ファイルシステムにハードリンクを作成します。
---

# ti fs create-hardlink

既存のリモートパスへのハードリンクを作成します。このコマンドのエイリアスは `ti fs hardlink` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs create-hardlink
  --link-path <string>
  --source-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--link-path <string>`: TiDB Cloud file system 内で作成するハードリンクのファイルパスです。\[required]
- `--source-path <string>`: TiDB Cloud file system 内の既存のファイルパスです。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ハードリンクを作成します。

    ```bash
    # Expose the same remote file content at a second path.
    ti fs create-hardlink --file-system-id <file-system-id> --source-path /reports/final.md --link-path /reports/final-copy.md
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
