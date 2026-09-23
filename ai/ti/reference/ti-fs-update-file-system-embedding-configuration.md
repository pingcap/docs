---
title: ti fs update-file-system-embedding-configuration
summary: ファイルシステムの埋め込み設定を置き換えます。
---

# ti fs update-file-system-embedding-configuration

1 つの file system に対して、オプションのアプリ管理埋め込みを有効または無効にします。有効化すると、実際のプロバイダー検証リクエストが実行され、プロバイダー側で少額の料金が発生する場合があります。有効化後は、テキストまたは抽出された説明が選択した埋め込みプロバイダーに送信されます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs update-file-system-embedding-configuration
  --enabled <boolean>
  --file-system-id <string>
  [--dry-run]
  [--help]
  [--provider-api-base <string>]
  [--provider-model <string>]
  [--version]
```

## オプション {#options}

- `--enabled <boolean>`: 完全なプロバイダー設定とともに `true` を指定するか、プロバイダーオプションなしで `false` を指定します。\[required]
- `--file-system-id <string>`: 変更不可の file system ID を設定します。\[required]
- `--dry-run`: file system バックエンドまたは埋め込みプロバイダーに接続せずに、リクエストを検証します。
- `--provider-api-base <string>`: 有効な HTTPS の OpenAI 互換プロバイダーベース URL を設定します。
- `--provider-model <string>`: ちょうど 1024 次元を返す埋め込みモデルを設定します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

プロバイダー API キーは `TI_FS_AI_PROVIDER_API_KEY` からのみ受け付けられます。このキーは検証および暗号化保存のために file system バックエンドへ送信され、`ti` によってローカルに保存されることはなく、マスクされた形式でのみ返されます。埋め込みには、OpenAI 互換の `/v1/embeddings` コントラクトに正確に一致することが必要です。ネイティブのプロバイダーインターフェースはサポートされていません。

`source` が `database_auto` の file system は、データベース管理の埋め込みを使用しているため、このコマンドでは変更できません。タイムアウトや応答消失の後に、やみくもに更新を再試行しないでください。まず describe コマンドを実行して、更新が成功したかどうかを確認してください。

## 例 {#examples}

- アプリ管理埋め込みを有効にする:

    ```bash
    # Read the provider key without echoing it or storing it in shell history.
    printf 'Provider API key: ' >&2
    read -r -s TI_FS_AI_PROVIDER_API_KEY
    printf '\n' >&2
    export TI_FS_AI_PROVIDER_API_KEY

    # Configure a model that returns exactly 1024 dimensions.
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model text-embedding-3-small
    unset TI_FS_AI_PROVIDER_API_KEY
    ```

- プロバイダーを検証または保存せずに、有効化をプレビューする:

    ```bash
    # Read the provider key without echoing it or storing it in shell history.
    printf 'Provider API key: ' >&2
    read -r -s TI_FS_AI_PROVIDER_API_KEY
    printf '\n' >&2
    export TI_FS_AI_PROVIDER_API_KEY

    # Validate local inputs and show a redacted request plan.
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model text-embedding-3-small \
      --dry-run
    unset TI_FS_AI_PROVIDER_API_KEY
    ```

- アプリ管理埋め込みを無効にする:

    ```bash
    # Remove custom embedding configuration without changing normal file access.
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled false
    ```

## 関連ドキュメント {#related-documentation}

- [`ti fs describe-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-describe-file-system-embedding-configuration.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)