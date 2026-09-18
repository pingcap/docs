---
title: TiDB Cloud Filesystem リソースを管理する
summary: TiDB Cloud CLI を使用して、TiDB Cloud Filesystem リソースを安全に作成、確認、チェック、選択、削除する方法を学びます。
---

# TiDB Cloud Filesystem リソースを管理する

TiDB Cloud Filesystem は、AI エージェントと自動化ワークロード向けに設計されたサーバーレス分散ファイルシステムです。ローカルマシン、サンドボックス、または CI ランナーからのアクセスに依存せず、永続的で共有可能なファイル名前空間を提供します。

TiDB Cloud CLI コマンドを通じてファイルに直接アクセスすることも、Filesystem をサポートされた環境にマウントしてローカルファイルシステムのように操作することもできます。これにより、エージェントの状態の保持、分離された環境間でのファイル共有、CI アーティファクトの受け渡し、再利用可能なワークスペースの管理に役立ちます。

このドキュメントでは、[`ti fs` コマンド](/ai/ti/reference/ti-filesystem.md)を使用して Filesystem リソースを作成、確認、選択、削除する方法について説明します。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- TiDB Cloud API 認証情報を使用してプロファイルを設定します。
- `jq` をインストールするか、別の JSON プロセッサを使用してコマンド出力を安全に取得します。

## Filesystem を作成する {#create-a-filesystem}

Filesystem を作成し、返された ID と 1 回限りのオーナートークンを、誰でも読み取り可能ではないファイルに保存します。`--wait` フラグを指定すると、CLI はデータプレーンアクセスの準備が整うまでポーリングしてから結果を返します。

```shell
umask 077
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait > ./filesystem.json

export TI_FS_FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

> **Warning:**
>
> JSON レスポンスには `fs_token` が 1 回だけ含まれます。CLI はこのトークンをローカルの認証情報ディレクトリにも自動的に保存します。ただし、ローカルストレージが失われた場合、このトークンを再取得することはできません。バックアップコピーをシークレットマネージャーに保存し、その後 `filesystem.json` を削除してください。

> **Note:**
>
> Filesystem のラベルには、認証情報、接続文字列、プライベートパス、または個人データを含めないでください。

## Filesystem を一覧表示して確認する {#list-and-inspect-filesystems}

有効なリージョンで利用可能な Filesystem を一覧表示します。

```shell
ti fs list-file-systems --output text
```

1 つの Filesystem の信頼できるメタデータを読み取ります。

```shell
ti fs describe-file-system --file-system-id "<file-system-id>"
```

複数の Filesystem にアクセスできる場合は、`--file-system-id` を明示的に指定するか、`TI_FS_FILE_SYSTEM_ID` 環境変数を設定してください。CLI は Filesystem を自動的に選択しません。

## アクセスをチェックする {#check-access}

リソースの選択、エンドポイント解決、認証情報、および companion アクセスを検証します。

```shell
ti fs check-file-system --file-system-id "<file-system-id>"
```

## Filesystem を削除する {#delete-a-filesystem}

> **Warning:**
>
> Filesystem を削除する前に、その Filesystem に対するアクティブなローカルマウントをすべて drain してアンマウントしてください。CLI はこれを自動では実行しません。

明示的な ID を指定して Filesystem を削除します。

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

Filesystem の削除は非同期です。サービスがリクエストを受け付けると、CLI は Filesystem のステータスを `deleting` として報告し、一致するローカル認証情報を削除します。この出力は、リモートでの削除が完了したことを意味するものではありません。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem トークンを管理する](/ai/ti/guides/manage-filesystem-tokens.md)
- [TiDB Cloud Filesystem データを操作する](/ai/ti/guides/work-with-filesystem-data.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
