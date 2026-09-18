---
title: ti fs-vault run-with-secret
summary: Filesystem Vault シークレットを使用してプロセスを実行します。
---

# ti fs-vault run-with-secret

1 つのシークレットを環境変数として注入してコマンドを実行します。`--` の後の引数は子コマンドに渡されます。

各シークレットのフィールド名は、子プロセス内で同じ名前の環境変数になります。フィールド名は `[A-Z_][A-Z0-9_]*` に一致する必要があるため、注入する予定のフィールドは大文字の名前で作成してください。小文字を含む名前を含め、いずれかのフィールド名がこのパターンに一致しない場合、または値にサポートされていない制御文字が含まれる場合、コマンドは注入全体を拒否します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault run-with-secret
  --secret-path <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--vault-token <string>]
  [--version]
  -- <command> [args...]
```

## オプション {#options}

- `--secret-path <string>`: `/n/vault/<secret-name>` 形式の正規 Vault パスです。たとえば、`db-prod` として作成されたシークレットのパスは `/n/vault/db-prod` です。\[required]
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: オーナー Filesystem トークンを設定します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択した Filesystem 用にローカルに保存されたトークンを使用します。委任認証には、代わりに `--vault-token` または `TI_VAULT_TOKEN` を使用してください。
- `--help`: ヘルプ情報を表示します。
- `--vault-token <string>`: 委任された `ti fs-vault` トークンです。`TI_VAULT_TOKEN` の使用を推奨します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共有されるオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- シークレットフィールドを使用してプロセスを実行します。

    ```bash
    # Verify that the child process receives DB_URL without printing its value.
    ti fs-vault run-with-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod -- sh -c 'test -n "$DB_URL" && printf "DB_URL is set\n"'
    ```

- 注入されたフィールドを使用してアプリケーションを実行します。

    ```bash
    # Make all fields available only to the child process and its descendants.
    ti fs-vault run-with-secret --file-system-id <file-system-id> --secret-path /n/vault/db-prod -- ./deploy.sh
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
