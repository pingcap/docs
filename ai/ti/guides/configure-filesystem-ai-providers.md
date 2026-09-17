---
title: TiDB Cloud Filesystem AI Providers を設定する
summary: CLI を使用して、TiDB Cloud Filesystem のメディア抽出プロバイダと埋め込みプロバイダを確認および設定する方法を学びます。
---

# TiDB Cloud Filesystem AI Providers を設定する

TiDB Cloud Filesystem では、オプションでメディアファイルからテキストを抽出し、保存されたコンテンツの埋め込みを生成できます。これらの機能を有効にするには、CLI を通じて 1 つ以上の AI プロバイダを設定します。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- 対象の Filesystem ID を取得します。
- 選択した AI プロバイダに必要な API キーを取得します。

設定コマンドには、TiDB Cloud API 認証情報と明示的な Filesystem ID が必要です。プロバイダキーは `TI_FS_AI_PROVIDER_API_KEY` を通じて設定します。CLI はこのキーをローカルに永続化しません。Filesystem サービスはこのキーを暗号化して保存し、その後の設定出力ではマスクされた値のみを返します。

対話型シェルでは、シェル履歴に残さずにプロバイダキーを読み取ってエクスポートします。

```bash
printf 'Provider API key: ' >&2
read -r -s TI_FS_AI_PROVIDER_API_KEY
printf '\n' >&2
export TI_FS_AI_PROVIDER_API_KEY
```

CI では、マスクされたシークレットから `TI_FS_AI_PROVIDER_API_KEY` を注入します。プロバイダの設定が完了したら、この変数を unset してください。

> **Note:**
>
> プロバイダ設定を有効化、再有効化、または置き換えると、Filesystem サービスは認証情報、接続性、およびモデル応答を検証するために、プロバイダエンドポイントへ小さな組み込みリクエストを送信します。この検証リクエストにより、プロバイダ側で課金が発生する場合があります。無効化のみ、またはプロンプトのみの更新では、検証リクエストは送信されません。

## メディア抽出設定を確認する {#inspect-media-extraction-configuration}

メディアタイプに対する有効な抽出設定を読み取ります。

```shell
ti fs describe-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image
```

## メディア抽出設定を更新する {#update-media-extraction-configuration}

[`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md) を使用して、画像、音声、または動画の抽出を有効化、更新、または無効化します。たとえば、OpenAI 互換プロバイダを通じて画像抽出を設定するには、次のようにします。

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<vision-model>" \
  --provider-protocol openai
```

`openai` プロトコルは、画像、音声、および動画の抽出をサポートします。`qwen-asr` プロトコルは、Alibaba Cloud Model Studio を通じた音声抽出でのみサポートされます。別のプロバイダのエンドポイントでも、必要な OpenAI 互換 API 仕様を実装していれば動作する可能性があります。Anthropic、Gemini、Vertex AI、Amazon Bedrock、および Azure OpenAI のネイティブインターフェースはサポートされていません。

メディアタイプの抽出を無効にするには、次のようにします。

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled false
```

## 埋め込み設定を確認する {#inspect-embedding-configuration}

埋め込みがアプリケーション管理かデータベース管理かを確認します。

```shell
ti fs describe-file-system-embedding-configuration \
  --file-system-id "<file-system-id>"
```

## 埋め込み設定を更新する {#update-embedding-configuration}

[`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md) を使用して、オプションのアプリケーション管理埋め込み設定を更新します。例:

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model text-embedding-3-small
```

アプリケーション管理埋め込みには、1024 次元ベクトルを返す OpenAI 互換エンドポイントが必要です。これらは、Shared Filesystems と、有効な埋め込みモードが `fts_only` である Native Filesystems で利用できます。Native Filesystem がデータベース管理の自動埋め込みを使用している場合、サービスはこの更新を拒否し、`source=database_auto` を報告します。

プロバイダの設定が完了したら、現在のシェルからキーを削除します。

```shell
unset TI_FS_AI_PROVIDER_API_KEY
```

この設定を無効にするには、次のようにします。

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled false
```

## 設定後のデータフロー {#data-flow-after-configuration}

抽出を有効にすると、Filesystem サービスはメディアコンテンツを設定済みの抽出プロバイダに送信します。抽出されたテキストまたは説明は、設定済みの埋め込みプロバイダに送信されます。データに適したプロバイダアカウントと保持ポリシーを選択してください。

タイムアウト、応答の消失、またはその他の判別しにくいネットワークエラーが原因で更新に失敗した場合は、再試行する前に対応する `describe-file-system-*-configuration` コマンドを実行してください。CLI が応答を受信していなくても、プロバイダ検証リクエストは成功して課金が発生している可能性があります。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem データを操作する](/ai/ti/guides/work-with-filesystem-data.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)