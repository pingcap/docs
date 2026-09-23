---
title: ti fs-vault list-secrets
summary: ファイルシステム Vault の認証情報から参照可能なシークレットを一覧表示します。
---

# ti fs-vault list-secrets

アクティブなオーナーまたは委任された認証情報から参照可能なシークレットを一覧表示します。

このコマンドは、参照可能なシークレットの完全な一覧を返します。結果はページ分割されません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault list-secrets
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定して指定することもできます。
- `--fs-token <string>`: ファイルシステムのオーナートークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、選択したファイルシステム用にローカルに保存されているトークンを使用します。委任認証には、代わりに `--vault-token` または `TI_VAULT_TOKEN` を使用してください。
- `--help`: ヘルプ情報を表示します。
- `--vault-token <string>`: 委任された `ti fs-vault` トークンです。`TI_VAULT_TOKEN` の使用を推奨します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- オーナーに表示されるシークレットを一覧表示します。

    ```bash
    # Return secret metadata without exposing field values.
    ti fs-vault list-secrets --file-system-id <file-system-id>
    ```

- 委任トークンから参照可能なシークレットを一覧表示します。

    ```bash
    # Read the delegated token without echoing it or storing it in shell history.
    printf 'Delegated Vault token: ' >&2
    read -r -s TI_VAULT_TOKEN
    printf '\n' >&2
    export TI_VAULT_TOKEN

    # Restrict results to the token's granted scope.
    ti fs-vault list-secrets --file-system-id <file-system-id>
    unset TI_VAULT_TOKEN
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)