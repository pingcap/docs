---
title: ファイルシステムの AI プロバイダーを設定する
summary: ファイルシステムでメディア抽出と埋め込みのための AI プロバイダーを設定します。
aliases: ['/ja/ai/configure-filesystem-ai-providers']
---

# ファイルシステムの AI プロバイダーを設定する

画像、音声、または動画から検索可能なコンテンツを TiDB Cloud Filesystem に抽出させたい場合、またはセマンティック検索用にカスタム埋め込みプロバイダーを設定したい場合は、このガイドを使用してください。

- **メディア抽出** では、AI プロバイダーを使用して画像、音声、または動画からテキストや説明を抽出し、そのコンテンツを検索できるようにします。
- **埋め込み** では、テキストと抽出された説明をセマンティック検索用のベクトルとして表現します。

これらの機能はオプションであり、それぞれ個別に設定できます。たとえば、カスタム埋め込みプロバイダーを設定せずにメディア抽出だけを設定できます。

このガイドでは、現在の設定を確認する方法、メディア抽出と埋め込みのプロバイダーを設定する方法、不要になったカスタム設定を無効化する方法を説明します。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- [TiDB Cloud CLI をインストールする](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 既存のファイルシステムにアクセスでき、そのファイルシステム ID を取得していること。
- TiDB Cloud API 認証情報を設定していること。このガイドのコマンドでは、TiDB Cloud API 認証情報と明示的なファイルシステム ID が必要であり、ファイルシステムトークンは使用しません。
- プロバイダー設定を有効化または置き換える場合は、プロバイダーのエンドポイント、モデル名、API キーを取得していること。

> **Note:**
>
> カスタムプロバイダーを設定すると、TiDB Cloud Filesystem は処理のためにコンテンツをそのプロバイダーへ送信します。プロバイダーアカウント、およびそのデータ保持ポリシーとプライバシーポリシーが、あなたのデータに適していることを確認してください。

## AI プロバイダーの API キーを指定する {#provide-the-api-key-of-your-ai-provider}

プロバイダー設定を有効化または置き換えるときは、`TI_FS_AI_PROVIDER_API_KEY` を通じて AI プロバイダーの API キーを指定します。

対話型シェルでは、シェル履歴に残さないようにキーを読み取ってエクスポートします。

```bash
printf 'Provider API key: ' >&2
read -r -s TI_FS_AI_PROVIDER_API_KEY
printf '\n' >&2
export TI_FS_AI_PROVIDER_API_KEY
```

TiDB Cloud CLI はキーをローカルに保存しません。ファイルシステムサービスはそれを暗号化して保存し、後で設定を確認したときにはマスクされた値のみを返します。

CI では、CI のシークレット管理メカニズムを通じて `TI_FS_AI_PROVIDER_API_KEY` を指定してください。

> **Note:**
>
> プロバイダー設定を有効化、再有効化、または置き換えると、ファイルシステムサービスは認証情報、接続性、およびモデル応答を検証するために、そのプロバイダーへ小さなリクエストを送信します。プロバイダーによっては、この検証リクエストに対して課金される場合があります。プロバイダーを無効化する場合や、抽出プロンプトのみを更新する場合は、検証リクエストは送信されません。

## メディア抽出を設定する {#configure-media-extraction}

メディア抽出を使用すると、TiDB Cloud Filesystem は画像、音声、または動画を処理し、抽出されたテキストや説明をコンテンツ検索で利用できるようにします。

### 現在の設定を確認する {#check-the-current-configuration}

設定を変更する前に、処理したいメディアタイプの現在の抽出設定を確認してください。

```shell
ti fs describe-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image
```

別のメディアタイプを確認するには、`image` を `audio` または `video` に置き換えてください。

### メディア抽出を有効化または更新する {#enable-or-update-media-extraction}

たとえば、OpenAI 互換プロバイダーで画像抽出を有効化するには、次のようにします。

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<vision-model>" \
  --provider-protocol openai
```

`openai` プロトコルは、画像、音声、動画の抽出をサポートします。音声抽出では、Alibaba Cloud Model Studio とともに `qwen-asr` プロトコルも使用できます。

他のプロバイダーエンドポイントを使用できるのは、それらが必要な OpenAI 互換 API コントラクトを実装している場合に限られます。Anthropic、Gemini、Vertex AI、Amazon Bedrock、Azure OpenAI のネイティブインターフェースはサポートされていません。

利用可能なすべてのオプションについては、[`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md) を参照してください。

### メディア抽出を無効化する {#disable-media-extraction}

メディアタイプの抽出を無効化するには、次のようにします。

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled false
```

## 埋め込みを設定する {#configure-embeddings}

埋め込みは、テキストコンテンツと抽出されたメディア説明を、セマンティック検索用のベクトルとして表現します。

### 現在の設定を確認する {#check-the-current-configuration-1}

カスタム埋め込みプロバイダーを設定する前に、現在の埋め込み設定を確認してください。

```shell
ti fs describe-file-system-embedding-configuration \
  --file-system-id "<file-system-id>"
```

出力の `source` フィールドを確認してください。これが `database_auto` の場合、埋め込みはサービスによって管理されており、カスタムプロバイダーで設定を置き換えることはできません。

### カスタム埋め込みプロバイダーを有効化または更新する {#enable-or-update-a-custom-embedding-provider}

現在の設定でカスタムプロバイダーが許可されている場合は、OpenAI 互換の埋め込みエンドポイントを設定します。

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<embedding-model>"
```

プロバイダーは、OpenAI 互換の埋め込み API を通じて、正確に 1024 次元のベクトルを返す必要があります。他のベクトル次元はサポートされていません。

利用可能なすべてのオプションについては、[`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md) を参照してください。

### カスタム埋め込み設定を無効化する {#disable-the-custom-embedding-configuration}

カスタム埋め込み設定を無効化するには、次のようにします。

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled false
```

## プロバイダー設定を完了する {#finish-configuring-providers}

プロバイダーの設定が完了したら、現在のシェルからプロバイダー API キーを削除してください。

```shell
unset TI_FS_AI_PROVIDER_API_KEY
```

カスタムメディア抽出が有効になっている場合、TiDB Cloud Filesystem は関連するメディアコンテンツを設定済みの抽出プロバイダーに送信します。カスタム埋め込みプロバイダーが有効になっている場合、テキストコンテンツと抽出されたメディア説明が埋め込みプロバイダーに送信されます。

タイムアウト、応答の消失、または更新が成功したかどうか判断できないその他のエラーによって更新に失敗した場合は、すぐにコマンドを再試行しないでください。まず、対応する `describe-file-system-*-configuration` コマンドを実行してください。

CLI が応答を受信していなくても、ファイルシステムサービスはすでに設定を保存し、プロバイダー検証リクエストを送信している可能性があります。

## 次のステップ {#what-s-next}

- [ファイルとディレクトリを操作する](/tidb-cloud-filesystem/work-with-filesystem-data.md) で、ファイルシステムのコンテンツを検索します。
- 完全なコマンド構文とオプションについては、[TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md) を参照してください。