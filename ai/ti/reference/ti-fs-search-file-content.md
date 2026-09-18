---
title: ti fs search-file-content
summary: TiDB Cloud Filesystem 内のファイル内容を検索します。
---

# ti fs search-file-content

必要に応じてレイヤー内も含めて、リモートのファイル内容を検索します。このコマンドのエイリアスは `ti fs grep` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs search-file-content
  --pattern <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--limit <int32>]
  [--path <string>]
  [--version]
```

## オプション {#options}

- `--pattern <string>`: 抽出されたファイル内容と説明に対して、全文検索および設定されている場合はセマンティック検索に使用されるテキストクエリです。この値は正規表現や glob ではありません。\[required]
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--layer-id <string>`: ファイルシステムのレイヤー内を検索します。
- `--limit <int32>`: 検索結果の最大件数です。0 を指定するとサービスのデフォルト値が使用されます。
- `--path <string>`: 検索対象のファイルパス接頭辞です。\[default: /]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ベース Filesystem の内容を検索します。

    ```bash
    # Find matching text under a remote directory and limit the result count.
    ti fs search-file-content --file-system-id <file-system-id> --path /workspace --pattern "TODO" --limit 50
    ```

- レイヤー内の内容を検索します。

    ```bash
    # Inspect uncommitted layer content separately from the base Filesystem.
    ti fs search-file-content --file-system-id <file-system-id> --path /workspace --pattern "deprecated" --layer-id "<layer-id>"
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)