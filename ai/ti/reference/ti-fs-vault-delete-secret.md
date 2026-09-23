---
title: ti fs-vault delete-secret
summary: file system Vault からシークレットを削除します。
---

# ti fs-vault delete-secret

file system Vault のシークレットを 1 つ削除します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault delete-secret
  --secret-name <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--secret-name <string>`: Vault シークレット名。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- シークレットを削除します。

    ```bash
    # Remove the selected secret and its fields from the Vault.
    ti fs-vault delete-secret --file-system-id <file-system-id> --secret-name db-prod
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
