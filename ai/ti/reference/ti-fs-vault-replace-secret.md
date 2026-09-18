---
title: ti fs-vault replace-secret
summary: Filesystem Vault シークレット内のすべてのフィールドを置き換えます。
---

# ti fs-vault replace-secret

ローカルディレクトリ内のファイルを使用して、1 つのシークレットのすべてのフィールドを置き換えます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault replace-secret
  --from-directory <string>
  --secret-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--from-directory <string>`: このディレクトリ内のファイルがシークレットのフィールドになります。\[required]
- `--secret-path <string>`: `/n/vault/<secret-name>` 形式の正規 Vault パスです。たとえば、`db-prod` として作成されたシークレットのパスは `/n/vault/db-prod` です。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ディレクトリからシークレットを置き換える:

    ```bash
    # Replace all fields with files loaded from the selected directory.
    ti fs-vault replace-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod --from-directory ./secret-fields
    ```

- シークレットの置き換えをプレビューする:

    ```bash
    # Validate the replacement source without changing the stored secret.
    ti fs-vault replace-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod --from-directory ./secret-fields --dry-run
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)