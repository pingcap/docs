---
title: ti fs describe-file-system
summary: リモートの TiDB Cloud Filesystem の詳細を表示します。
---

# ti fs describe-file-system

Filesystem の表示名、ラベル、配置、ステータス、クォータ、使用量などの詳細情報を表示します。このコマンドには TiDB Cloud API 認証情報が必要であり、Filesystem トークンは使用しません。

出力には `has_local_token` が含まれ、このマシンに一致するローカルトークンがあるかどうかを示します。利用可能な場合、クォータデータにはメディアおよび動画抽出の上限と使用量が含まれます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs describe-file-system
  --file-system-id <string>
  [--help]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: 変更不可の Filesystem ID を設定します。\[required]
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- Filesystem を表示する場合:

    ```bash
    # Return remote status and whether this machine has a matching local token.
    ti fs describe-file-system --file-system-id <file-system-id>
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)