---
title: ti fs diff-layer
summary: TiDB Cloud Filesystem のレイヤー内の変更を表示します。
---

# ti fs diff-layer

1 つのレイヤー内の変更を一覧表示します。必要に応じて、指定したシーケンス番号までの変更を表示できます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs diff-layer
  --layer-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--max-seq <int64>]
  [--version]
```

## オプション {#options}

- `--layer-id <string>`: レイヤーの ID。\[required]
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合は、選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--max-seq <int64>`: 含めるレイヤーの最大シーケンス。`0` を指定すると、すべてのシーケンスを含みます。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- すべてのレイヤー変更を表示する:

    ```bash
    # Return the complete ordered change set for the selected layer.
    ti fs diff-layer --file-system-id <file-system-id> --layer-id "<layer-id>"
    ```

- 以前のレイヤービューを表示する:

    ```bash
    # Limit the diff to changes at or before a sequence number.
    ti fs diff-layer --file-system-id <file-system-id> --layer-id "<layer-id>" --max-seq 100
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)