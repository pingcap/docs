---
title: ti fs import-file-system-token
summary: 既存の TiDB Cloud Filesystem トークンをインポートします。
---

# ti fs import-file-system-token

既存の Filesystem トークンを検証し、選択したローカルプロファイルに保存します。Filesystem ID はトークンから導出されます。トークンが想定した Filesystem に属していることを確認するには、オプションの `--file-system-id` を使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs import-file-system-token
  [--dry-run]
  [--file-system-id <string>]
  [--from-file <string>]
  [--fs-token <string>]
  [--help]
  [--replace]
  [--version]
```

## オプション {#options}

- `--dry-run`: ローカル認証情報を書き込まずに、トークンと保存先を検証します。
- `--file-system-id <string>`: トークンがこの file system ID に属していることを確認します。
- `--from-file <string>`: オーナー専用ファイルからトークンを読み取ります。標準入力を使用する場合は `-` を指定します。
- `--fs-token <string>`: トークンを直接指定します。プロセス引数への露出を避けるため、`TI_FS_TOKEN` または `--from-file` の使用を推奨します。
- `--help`: ヘルプ情報を表示します。
- `--replace`: 検証後、同じ file system に対してローカルに保存されている別のトークンを置き換えます。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 保護されたファイルからトークンをインポートする:

    ```bash
    # Validate the token remotely and store it under its embedded file system ID.
    chmod 600 ./fs-token
    ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
    ```

- 標準入力からトークンをインポートする:

    ```bash
    # Avoid placing the token in shell history or a process argument.
    cat ./fs-token | ti fs import-file-system-token --from-file - --region aws-us-east-1
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
