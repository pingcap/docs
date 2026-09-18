---
title: ti fs find-files
summary: TiDB Cloud Filesystem 内のファイルを検索します。
---

# ti fs find-files

名前、タイプ、タグ、サイズ、または更新時刻でリモートパスを検索します。コマンドのエイリアスは `ti fs find` です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs find-files
  [--file-name-pattern <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--limit <int32>]
  [--max-size-bytes <int64>]
  [--min-size-bytes <int64>]
  [--newer <string>]
  [--older <string>]
  [--path <string>]
  [--resource-type <string>]
  [--tag <string>]
  [--version]
```

## オプション {#options}

- `--file-name-pattern <string>`: `*.md` などのファイル名パターンでフィルタリングします。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--layer-id <string>`: 特定のファイルシステムレイヤー内のファイルとディレクトリを検索します。
- `--limit <int32>`: 結果の最大件数です。0 を指定するとサービスのデフォルト値が使用されます。
- `--max-size-bytes <int64>`: ファイルサイズの上限（バイト単位）です。
- `--min-size-bytes <int64>`: ファイルサイズの下限（バイト単位）です。
- `--newer <string>`: `YYYY-MM-DD` 形式で指定した日付より新しいファイルを返します。
- `--older <string>`: `YYYY-MM-DD` 形式で指定した日付より古いファイルを返します。
- `--path <string>`: ファイルパスのプレフィックスです。\[default: /]
- `--resource-type <string>`: リソースタイプのフィルターです。`file` または `directory` を指定します。
- `--tag <string>`: `key=value` で完全一致するタグに一致させるか、`key` のみを指定してそのタグキーの任意の値に一致させます。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 名前でファイルを検索する場合:

    ```bash
    # Locate Markdown files recursively under the selected remote path.
    ti fs find-files --file-system-id <file-system-id> --path /workspace --file-name-pattern "*.md"
    ```

- メタデータでファイルを検索する場合:

    ```bash
    # Select tagged files that also meet a minimum size threshold.
    ti fs find-files --file-system-id <file-system-id> --path /workspace --tag stage=review --min-size-bytes 1024
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)