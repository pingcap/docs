---
title: ti fs-vault create-grant
summary: 委任された file system Vault grant を作成します。
---

# ti fs-vault create-grant

1 つの agent と scope に対して、期限付きの委任 grant を作成します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault create-grant
  --agent-id <string>
  --permission <string>
  --scope <string>
  --ttl <duration>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--label-hint <string>]
  [--token-only]
  [--version]
```

## オプション {#options}

- `--agent-id <string>`: 委任 grant の Agent ID。\[required]
- `--permission <string>`: grant 権限: `read` または `write`。現在の権限の動作については、[付与可能な権限](#grant-permissions) を参照してください。\[required]
- `--scope <string>`: すべてのフィールドを対象とする場合は `<secret-name>`、1 つのフィールドを対象とする場合は `<secret-name>/<field-name>` 形式の secret scope。繰り返し指定できます。同等の正規 Vault パス `/n/vault/<secret-name>` および `/n/vault/<secret-name>/<field-name>` も使用できます。\[required]
- `--ttl <duration>`: grant の有効期間。たとえば `1h`。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: file system トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した file system 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--label-hint <string>`: 任意の grant ラベルヒント。
- `--token-only`: 委任 bearer トークンのみを出力します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 付与可能な権限 {#grant-permissions}

| 権限 | 現在の `ti` の動作 |
| --- | --- |
| `read` | grant scope 内で、委任された `list-secrets`、`read-secret`、`run-with-secret`、および `mount-vault` 操作を許可します。 |
| `write` | サービスはこの権限を受け付けますが、read 権限は含まれません。現在の `ti` コマンドでは、委任トークンを使用して secret を書き込む操作は公開されていません。 |

## 例 {#examples}

- 一時的な read grant を作成します。

    ```bash
    # Limit an agent to one secret field for ten minutes.
    ti fs-vault create-grant --file-system-id <file-system-id> --agent-id deploy-agent --scope db-prod/DB_URL --permission read --ttl 10m
    ```

- 委任トークンのみを返します。

    ```bash
    # Produce token-only output for injection into an isolated CI job.
    ti fs-vault create-grant --file-system-id <file-system-id> --agent-id ci-agent --scope api-dev/TOKEN --permission read --ttl 5m --token-only
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
