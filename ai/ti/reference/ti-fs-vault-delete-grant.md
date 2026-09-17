---
title: ti fs-vault delete-grant
summary: 委任された Filesystem Vault grant を取り消します。
---

# ti fs-vault delete-grant

委任された Filesystem Vault grant を 1 つ取り消します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault delete-grant
  --grant-id <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--reason <string>]
  [--revoked-by <string>]
  [--version]
```

## オプション {#options}

- `--grant-id <string>`: Vault grant ID。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--reason <string>`: 取り消し理由を任意で指定します。
- `--revoked-by <string>`: 取り消し監査エントリの実行者ラベル。\[デフォルト: `ti`]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- grant を取り消すには、次のようにします。

    ```bash
    # Invalidate the delegated token and record the revocation reason.
    ti fs-vault delete-grant --file-system-id <file-system-id> --grant-id "<grant-id>" --reason rotated
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
