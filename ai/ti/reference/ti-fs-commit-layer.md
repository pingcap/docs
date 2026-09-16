---
title: ti fs commit-layer
summary: TiDB Cloud Filesystem のレイヤーをコミットします。
---

# ti fs commit-layer

1 つのレイヤーを、そのベース Filesystem に適用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs commit-layer
  --layer-id <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--layer-id <string>`: レイヤー ID。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- レイヤーをコミットします。

    ```bash
    # Apply the selected layer's changes to its base Filesystem view.
    ti fs commit-layer --file-system-id <file-system-id> --layer-id "<layer-id>"
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)