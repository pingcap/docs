---
title: ti fs-vault read-secret
summary: file system Vault からシークレットを読み取ります。
---

# ti fs-vault read-secret

オーナーまたは委任された認証情報を使用して、完全なシークレットまたは 1 つのフィールドを読み取ります。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault read-secret
  --secret-name <string>
  [--field <string>]
  [--file-system-id <string>]
  [--format <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
```

## オプション {#options}

- `--secret-name <string>`: Vault シークレット名。\[required]
- `--field <string>`: 読み取るオプションのフィールド名。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--format <string>`: 読み取り出力形式: `json`、`raw`、または `env`。\[デフォルト: json]
- `--fs-token <string>`: file system オーナートークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。委任された認証には、代わりに `--vault-token` または `TI_VAULT_TOKEN` を使用します。
- `--help`: ヘルプ情報を表示します。
- `--vault-token <string>`: 委任された `ti fs-vault` トークン。`TI_VAULT_TOKEN` の使用を推奨します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共有されるオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 生テキストとして 1 つのシークレットフィールドを読み取る:

    ```bash
    # Write only the selected field value for direct consumption by a process.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field PASSWORD --format raw
    ```

- フィールドを環境変数代入として整形する:

    ```bash
    # Emit an exportable environment-variable representation of the field.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL --format env
    ```

- 委任された Vault トークンを使用して読み取る:

    ```bash
    # Read the delegated token without echoing it or storing it in shell history.
    printf 'Delegated Vault token: ' >&2
    read -r -s TI_VAULT_TOKEN
    printf '\n' >&2
    export TI_VAULT_TOKEN

    # Access only the field allowed by the delegated token.
    ti fs-vault read-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL --format raw
    unset TI_VAULT_TOKEN
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
