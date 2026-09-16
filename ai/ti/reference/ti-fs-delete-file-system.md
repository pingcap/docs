---
title: ti fs delete-file-system
summary: TiDB Cloud Filesystem を削除します。
---

# ti fs delete-file-system

Filesystem の削除を開始します。削除は、コマンドの実行結果が返された後に非同期で実行されます。`--file-system-id` の指定が必須です。表示名、ラベル、および Filesystem トークンでは、削除対象の Filesystem を特定できません。このコマンドを実行するには、TiDB Cloud API 認証情報が必要です。

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

- `--file-system-id <string>`: 変更不可の Filesystem ID を設定します。FS トークンではこのオプションを置き換えることも、Filesystem の削除を認可することもできません。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- Filesystem を削除する:

    ```bash
    # Request asynchronous deletion and remove only the matching local credential after acceptance.
    ti fs delete-file-system --file-system-id <file-system-id>
    ```

- Filesystem の削除をプレビューする:

    ```bash
    # Validate the selected Filesystem without sending the deletion request.
    ti fs delete-file-system --file-system-id <file-system-id> --dry-run
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)