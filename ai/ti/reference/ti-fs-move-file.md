---
title: ti fs move-file
summary: TiDB Cloud Filesystem 内のファイルを移動します。
---

# ti fs move-file

リモートパスを移動または名前変更します。このコマンドのエイリアスは `ti fs mv` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs move-file
  --from-remote <string>
  --to-remote <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--overwrite]
  [--version]
```

## オプション {#options}

- `--from-remote <string>`: ソースファイルのパス。\[required]
- `--to-remote <string>`: 宛先ファイルのパス。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--overwrite`: 既存の宛先ファイルを置き換えます。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- リモートファイルを移動する:

    ```bash
    # Rename or relocate an object entirely within the selected Filesystem.
    ti fs move-file --file-system-id <file-system-id> --from-remote /draft.md --to-remote /reports/final.md
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)