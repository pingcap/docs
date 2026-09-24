---
title: TiDB Cloud Filesystem を使用して並列エージェント間で読み取り専用データセットを共有する
summary: 1 つの非構造化データセットをアップロードし、同じ読み取り専用でマウントされた名前空間を複数のエージェントワーカーに公開します。
---

# TiDB Cloud Filesystem を使用して並列エージェント間で読み取り専用データセットを共有する

このワークフローでは、複数の短命なワーカーに対して、各サンドボックスへ個別のコピーをダウンロードすることなく、1 つの共有コーパスを提供できます。並列のドキュメント処理エージェントや評価エージェントが、同じ PDF、画像、ログ、またはモデルアーティファクトに一貫してアクセスする必要がある場合に使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 仕組み {#how-it-works}

所有者はコーパスを 1 回アップロードし、各ワーカー用にスコープ付きの読み取り専用 file system トークンを作成します。各ワーカーは同じ file system を選択し、コーパスを読み取り専用でマウントするため、通常のツールでストレージ SDK を使わずに 1 つの共通名前空間をたどることができます。これにより起動時間が短縮され、独立した特定時点のコピーを作成する必要がなくなります。ワーカーが結果を生成する場合は、データセット file system ではなく、別の書き込み可能な出力 file system 内の個別パスに書き込みます。

## 前提条件 {#prerequisites}

- 信頼できるマシンに TiDB Cloud CLI をインストールして設定します。
- 各ワーカーに TiDB Cloud CLI と必要なマウント依存関係をインストールします。
- 信頼できるマシンに `jq` をインストールします。
- トークン転送には、安全なシークレットマネージャーまたは暗号化されたワーカー入力を使用します。

## ステップ 1. コーパスをアップロードする {#step-1-upload-the-corpus}

信頼できるマシンで次を実行します。

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export TI_FS_FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"

ti fs copy-file \
  --from-local ./corpus \
  --to-remote /datasets/corpus \
  --recursive

ti fs find-files \
  --path /datasets/corpus \
  --file-name-pattern "*.pdf" \
  --output text

# Create one short-lived, read-only scoped token per worker.
ti fs generate-file-system-scoped-token \
  --file-system-id "$TI_FS_FILE_SYSTEM_ID" \
  --subject worker-1 \
  --ttl 24h \
  --allow /datasets/corpus:read,list > ./worker-1-token.json
```

シークレットマネージャーを通じて、`worker-1-token.json` の `fs_token` と file system のリージョンコードを転送します。各ワーカーに対して一意のサブジェクトを指定して、トークン生成コマンドを繰り返します。所有者トークンは信頼できるマシン上にのみ保持し、トークンを安全に保存した後は JSON ファイルを削除してください。

## ステップ 2. 各ワーカーでマウントする {#step-2-mount-in-each-worker}

> **Warning:**
>
> 各ワーカーには、コーパスパス配下で `read` と `list` のみを許可するスコープ付きトークンを付与してください。`--read-only` マウントオプションは、マウント経由の意図しない書き込みを防ぎますが、トークンの権限自体を変更するものではありません。

ワーカーのスコープ付きトークンを `TI_FS_TOKEN` として注入し、`TI_REGION_CODE` を file system のリージョンに設定してから、次を実行します。

```bash
mkdir -p "$HOME/corpus"
ti fs mount-file-system \
  --mount-path "$HOME/corpus" \
  --remote-path /datasets/corpus \
  --read-only
```

ワーカーはストレージ SDK を使わずに標準ツールを使用できます。

```bash
find "$HOME/corpus" -type f -name '*.pdf' -print
```

## クリーンアップ {#cleanup}

終了する前に、各ワーカーで file system をアンマウントします。

```bash
ti fs unmount-file-system --mount-path "$HOME/corpus"
```

すべてのワーカーが file system をアンマウントした後、データセットが不要であれば、信頼できるマシンからそれを削除します。

```bash
rm -f ./filesystem.json ./worker-*-token.json
ti fs delete-file-system --file-system-id "$TI_FS_FILE_SYSTEM_ID"
```

## セキュリティおよび運用上の注意 {#security-and-operational-notes}

- 所有者トークンをワーカーに配布しないでください。各ワーカーごとに個別の短命なスコープ付きトークンを生成し、読み取り専用アクセスが認証情報によって強制されるようにします。
- ワーカーが同じ出力 file system に書き込む場合は、エージェントまたは実行 ID ごとに結果パスを分割してください。
- FUSE または WebDAV マウントを利用できないプラットフォームでは、`read-file`、`find-files`、および `copy-file --to-local` を直接使用してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [エージェントサンドボックスで file system を使用する](/ai/ti/guides/ti-agent-sandbox-example.md)
- [TiDB Cloud CLI のリージョン、セキュリティ、および制限事項](/ai/ti/reference/ti-regions-security-and-limitations.md)