---
title: TiDB Cloud Filesystem を使用して分離されたジョブ間で CI アーティファクトを受け渡す
summary: ビルド出力を TiDB Cloud Filesystem に永続化し、完全な TiDB Cloud CLI プロファイルをコピーせずに後続の CI ジョブから利用します。
---

# TiDB Cloud Filesystem を使用して分離されたジョブ間で CI アーティファクトを受け渡す

このワークフローでは、分離された CI ジョブまたはランナー間でアーティファクトを受け渡すための永続的な受け渡しポイントとして file system を使用します。ビルド出力を生成ジョブの終了後も保持し、プロバイダー固有のアーティファクト API、保持モデル、ダウンロードワークフローを追加せずに、後続のコンシューマージョブで利用できるようにする必要がある場合に使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは予告なく変更される場合があります。

## 仕組み {#how-it-works}

パイプラインは、1 つの file system トークンとリージョンを両方のジョブに注入します。トークンは file system を識別します。生成側ジョブは `/ci/${RUN_ID}/` のような今回の実行に固有のパス配下に出力をアップロードし、コンシューマー側ジョブは別のランナー上でその正確なパスからデータをダウンロードまたはストリーミングします。どちらのジョブにも TiDB Cloud API キーやコピーされた `~/.ti/` ディレクトリは不要です。

## 前提条件 {#prerequisites}

信頼できるマシンで [file system を作成](/tidb-cloud-filesystem/manage-filesystem-resources.md#create-a-file-system) し、次の値を保護された CI シークレットまたは変数として保存します。

```text
TI_FS_TOKEN
TI_REGION_CODE
```

並行して実行されるパイプラインを分離するために、`RUN_ID` のような CI 生成の実行識別子を使用します。

## 生成側ジョブ {#producer-job}

アーティファクトをビルドしてからアップロードします。

```bash
tar -czf app.tar.gz ./dist
ti fs copy-file \
  --from-local ./app.tar.gz \
  --to-remote "/ci/${RUN_ID}/app.tar.gz" \
  --tag pipeline=build \
  --description "artifact for run ${RUN_ID}"
```

## コンシューマー側ジョブ {#consumer-job}

別のランナーからアーティファクトをダウンロードして検証します。

```bash
ti fs copy-file \
  --from-remote "/ci/${RUN_ID}/app.tar.gz" \
  --to-local ./app.tar.gz \
  --create-parents

tar -tzf app.tar.gz
```

標準入力を受け付けるコマンドの場合は、中間のローカルファイルを避けられます。

```bash
ti fs copy-file --from-remote "/ci/${RUN_ID}/app.tar.gz" --to-stdout \
  | tar -tzf -
```

## クリーンアップと分離 {#cleanup-and-isolation}

すべてのコンシューマーが完了した後で、今回の実行に固有のディレクトリのみを削除します。

```bash
ti fs delete-file --path "/ci/${RUN_ID}" --recursive
```

一意の実行 ID を使用し、個々のジョブから file system 全体を削除しないでください。file system の削除には信頼されたコントロールプレーンの設定が必要であり、別個の所有者操作として維持する必要があります。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud CLI のリージョン、セキュリティ、および制限事項](/ai/ti/reference/ti-regions-security-and-limitations.md)