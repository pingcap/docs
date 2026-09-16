---
title: ti fs refresh-file-system-token
summary: 1 つの TiDB Cloud Filesystem token をローテーションし、その置き換え用の平文値を 1 回だけ返します。
---

# ti fs refresh-file-system-token

指定した Filesystem token をローテーションし、その置き換え値を 1 回だけ返します。以前の値は、認証の変更が反映された後に機能しなくなります。反映には約 10 秒かかる場合があります。

> **Warning:**
>
> Refresh は冪等ではありません。リクエストが成功してもレスポンスを受信できなかった場合は、古い token を使って再試行しないでください。代わりに、新しい置き換え token を生成して配布してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。その機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs refresh-file-system-token
  [--file-system-id <string>]
  [--fs-token <string>]
  [--ttl <duration>]
  [--dry-run]
  [--help]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: 指定した token からデコードされた Filesystem ID を検証します。ローカルで選択された token を読み込む場合、このオプションは必須です。
- `--fs-token <string>`: 現在の token を指定します。shell history や process list への露出を避けるため、`TI_FS_TOKEN` の使用を推奨します。デフォルトでは、まず `TI_FS_TOKEN` を使用し、次に選択されたローカル credential を使用します。
- `--ttl <duration>`: 新しい正の有効期間を秒単位で設定します。最大は 365 日です。以前の有効期間を維持する場合は省略してください。
- `--dry-run`: token をローテーションせずに、token の選択、リージョン、TTL、および既知のローカル mount 競合を検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 選択されたローカル credential を refresh します。

    ```bash
    # ti atomically replaces the local credential after receiving the new token.
    ti fs refresh-file-system-token --file-system-id "<file-system-id>"
    ```

- secret manager から提供された token を refresh します。

    ```bash
    # Read the current token without echoing it or storing it in shell history.
    printf 'Current FS token: ' >&2
    read -r -s TI_FS_TOKEN
    printf '\n' >&2
    export TI_FS_TOKEN

    # Capture the one-time replacement and update the external secret manager yourself.
    TI_REGION_CODE="aws-us-east-1" \
    ti fs refresh-file-system-token > ./refreshed-token.json
    unset TI_FS_TOKEN
    ```

- refresh 中に token の有効期間を変更します。

    ```bash
    # Read the current token without echoing it or storing it in shell history.
    printf 'Current FS token: ' >&2
    read -r -s TI_FS_TOKEN
    printf '\n' >&2
    export TI_FS_TOKEN

    # Rotate the token and set its new lifetime to 30 days.
    TI_REGION_CODE="aws-us-east-1" \
    ti fs refresh-file-system-token --ttl 720h
    unset TI_FS_TOKEN
    ```

## 関連ドキュメント {#related-documentation}

- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [TiDB Cloud CLI のトラブルシューティング](/ai/ti/reference/ti-troubleshooting.md)