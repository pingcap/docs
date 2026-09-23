---
title: ti fs-vault mount-vault
summary: 読み取り専用の file system Vault ビューをマウントします。
---

# ti fs-vault mount-vault

読み取り可能な vault フィールドを、ローカルの読み取り専用 FUSE ファイルシステムとしてマウントします。

Linux では、FUSE3 をインストールし、`/dev/fuse` を利用可能にしてください。macOS では、macFUSE をインストールし、そのシステム拡張を承認してください。Windows では Vault マウントはサポートされていません。代わりに `read-secret`、`list-secrets`、または `run-with-secret` を使用してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault mount-vault
  --mount-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--ready-timeout <duration>]
  [--vault-token <string>]
  [--version]
```

## オプション {#options}

- `--mount-path <string>`: ローカルのマウントパス。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステムのオーナートークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択したファイルシステム用にローカルに保存されているトークンを使用します。委任認証には、代わりに `--vault-token` または `TI_VAULT_TOKEN` を使用してください。
- `--help`: ヘルプ情報を表示します。
- `--ready-timeout <duration>`: バックグラウンドマウントの準備が完了するまで待機する時間。\[default: `30s`]
- `--vault-token <string>`: 委任された `ti fs-vault` トークン。`TI_VAULT_TOKEN` の使用を推奨します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

どちらの例を実行する前にも、委任された Vault トークンを注入してください。対話型シェルでは、シェル履歴に残さないように読み取ってエクスポートします。

```bash
printf 'Delegated Vault token: ' >&2
read -r -s TI_VAULT_TOKEN
printf '\n' >&2
export TI_VAULT_TOKEN
```

マウントが不要になったら、アンマウントして `unset TI_VAULT_TOKEN` を実行してください。

- 委任された Vault ビューをマウントする:

    ```bash
    # Expose only the paths allowed by TI_VAULT_TOKEN.
    ti fs-vault mount-vault --file-system-id <file-system-id> --mount-path ./vault
    ```

- Vault マウントの準備完了までの待機時間を長くする:

    ```bash
    # Increase the readiness timeout on a slower host or network.
    ti fs-vault mount-vault --file-system-id <file-system-id> --mount-path ./vault --ready-timeout 60s
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
