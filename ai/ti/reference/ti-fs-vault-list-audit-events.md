---
title: ti fs-vault list-audit-events
summary: Filesystem Vault の監査イベントを一覧表示します。
---

# ti fs-vault list-audit-events

オプションのエージェント、シークレット、時間フィルターを使用して vault の監査イベントを一覧表示します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-vault list-audit-events
  [--agent-id <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--limit <int32>]
  [--secret-name <string>]
  [--since <duration>]
  [--version]
```

## オプション {#options}

- `--agent-id <string>`: エージェント ID でフィルターします。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、コマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、コマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--limit <int32>`: 返されるイベントの最大数。\[default: 100]
- `--secret-name <string>`: Vault シークレット名でフィルターします。
- `--since <duration>`: クライアント側の相対時間フィルター。たとえば `24h`。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 1 つのシークレットのイベントを一覧表示します。

    ```bash
    # Inspect recent access and mutation events for the selected secret.
    ti fs-vault list-audit-events --file-system-id <file-system-id> --secret-name db-prod --limit 20
    ```

- エージェントの最近のイベントを一覧表示します。

    ```bash
    # Filter the audit trail to one delegated identity and time range.
    ti fs-vault list-audit-events --file-system-id <file-system-id> --agent-id deploy-agent --since 24h
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-vault.md)
