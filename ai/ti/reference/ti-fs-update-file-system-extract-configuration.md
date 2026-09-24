---
title: ti fs update-file-system-extract-configuration
summary: ファイルシステムのメディア抽出設定を更新します。
---

# ti fs update-file-system-extract-configuration

1 つの file system に対する、オプションの画像、音声、または動画の抽出設定を更新します。プロバイダーを有効化または置き換えると、実際のプロバイダー検証リクエストが実行されるため、プロバイダー側で少額の料金が発生する場合があります。有効化後、file system のメディアは抽出のために選択したプロバイダーへ送信されます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs update-file-system-extract-configuration
  --file-system-id <string>
  --media-type <string>
  [--dry-run]
  [--enabled <boolean>]
  [--help]
  [--prompt <string>]
  [--provider-api-base <string>]
  [--provider-model <string>]
  [--provider-protocol <string>]
  [--version]
```

## オプション {#options}

- `--file-system-id <string>`: 変更不可の file system ID を設定します。\[required]
- `--media-type <string>`: `image`、`audio`、または `video` を選択します。\[required]
- `--dry-run`: file system バックエンドまたは AI プロバイダーに接続せずに、リクエストを検証します。
- `--enabled <boolean>`: 抽出を明示的に有効化または無効化します。`true` または `false` を指定します。
- `--prompt <string>`: 最大 8 KiB のプロンプトを設定します。空文字列を渡すと、バックエンドのデフォルトのプロンプト動作に戻ります。
- `--provider-api-base <string>`: 有効な HTTPS のプロバイダーベース URL を設定します。
- `--provider-model <string>`: プロバイダーのモデル名を設定します。
- `--provider-protocol <string>`: `openai`、または音声専用の `qwen-asr` を設定します。デフォルトは `openai` です。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

プロバイダー API キーは `TI_FS_AI_PROVIDER_API_KEY` からのみ受け付けます。このキーは検証および暗号化保存のために file system バックエンドへ送信され、`ti` によってローカルに保存されることはなく、マスクされた形式でのみ返されます。`openai` は画像、音声、動画をサポートします。Alibaba Cloud Model Studio Qwen ASR は、`qwen-asr` を通じて音声でサポートされます。その他のサービスは、必要な OpenAI 互換コントラクトを正確に実装している場合にのみ動作します。ネイティブの Anthropic、Gemini、Vertex AI、Bedrock、および Azure OpenAI インターフェイスはサポートされていません。

タイムアウトやレスポンス消失の後に、やみくもに更新を再試行しないでください。プロバイダー側ですでに検証料金が発生しており、バックエンドに設定が保存されている可能性があります。まず対応する describe コマンドを実行してください。

対話型シェルでプロバイダーを有効化する前に、API キーをシェル履歴に残さないように読み取ってエクスポートしてください。

```bash
printf 'Provider API key: ' >&2
read -r -s TI_FS_AI_PROVIDER_API_KEY
printf '\n' >&2
export TI_FS_AI_PROVIDER_API_KEY
```

CI では、マスクされたシークレットから `TI_FS_AI_PROVIDER_API_KEY` を注入してください。コマンドの実行完了後は、この変数を unset してください。

## 例 {#examples}

- OpenAI 互換プロバイダーで画像抽出を有効化する場合:

    ```bash
    # Configure extraction using the provider key from TI_FS_AI_PROVIDER_API_KEY.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model <vision-model>
    ```

- 音声に対して Alibaba Cloud Model Studio Qwen ASR を有効化する場合:

    ```bash
    # Use the DashScope OpenAI-compatible endpoint with the qwen-asr protocol.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type audio \
      --enabled true \
      --provider-api-base https://dashscope.aliyuncs.com/compatible-mode/v1 \
      --provider-model qwen3-asr-flash \
      --provider-protocol qwen-asr
    ```

- 有効化済みの画像設定で、プロンプトのみを変更する場合:

    ```bash
    # Keep the existing provider credentials and update only extraction instructions.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --prompt "Describe the image and return searchable attributes."
    ```

- 画像抽出を無効化する場合:

    ```bash
    # Remove the custom image provider configuration without changing normal file access.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --enabled false
    ```

## 関連ドキュメント {#related-documentation}

- [`ti fs describe-file-system-extract-configuration`](/ai/ti/reference/ti-fs-describe-file-system-extract-configuration.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)