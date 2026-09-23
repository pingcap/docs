---
title: ti fs-vault create-secret
summary: file system Vault にシークレットを作成します。
---

# ti fs-vault create-secret

1 つ以上の `NAME=value` または `NAME=@file` フィールドからシークレットを作成します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault create-secret
  --field <string>
  --secret-name <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--field <string>`: シークレットフィールドの割り当て `key=value`、`key=@file`、または `key=-` を指定します。繰り返し指定できます。`key=-` は標準入力を読み取ります。複数のフィールドで `-` を使用した場合、それぞれに同じ標準入力値が渡されます。\[required]
- `--secret-name <string>`: Vault シークレット名。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください.

## 例 {#examples}

- 値とファイルからシークレットを作成する:

    ```bash
    # Keep the password out of the command line by reading it from a local file.
    ti fs-vault create-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL=mysql://example --field PASSWORD=@./password.txt
    ```

- 標準入力からシークレットフィールドを読み取る:

    ```bash
    # Supply a sensitive token through a pipe instead of a process argument.
    printf '%s' "$API_TOKEN" | ti fs-vault create-secret --file-system-id <file-system-id> --secret-name api-dev --field TOKEN=-
    ```

- シークレット作成をプレビューする:

    ```bash
    # Validate field assignments without storing secret material.
    ti fs-vault create-secret --file-system-id <file-system-id> --secret-name api-dev --field TOKEN=@./token.txt --dry-run
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)