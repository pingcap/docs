---
title: ti fs delete-file-system
summary: ファイルシステムを削除します。
---

# ti fs delete-file-system

ファイルシステムの削除を開始します。削除は、コマンドの実行結果が返された後に非同期で実行されます。`--file-system-id` の指定が必須です。表示名、ラベル、およびファイルシステムトークンでは、削除対象のファイルシステムを特定できません。このコマンドを実行するには、TiDB Cloud API 認証情報が必要です。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs delete-file-system
  --file-system-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: 変更不可のファイルシステム ID を設定します。ファイルシステムトークンではこのオプションを置き換えることも、ファイルシステムの削除を認可することもできません。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ファイルシステムを削除する:

    ```bash
    # Request asynchronous deletion and remove only the matching local credential after acceptance.
    ti fs delete-file-system --file-system-id <file-system-id>
    ```

- ファイルシステムの削除をプレビューする:

    ```bash
    # Validate the selected file system without sending the deletion request.
    ti fs delete-file-system --file-system-id <file-system-id> --dry-run
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)