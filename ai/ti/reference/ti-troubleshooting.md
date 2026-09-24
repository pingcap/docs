---
title: TiDB Cloud CLI のトラブルシューティング
summary: TiDB Cloud CLI の API 認証、Starter クォータ、SQL 認証情報、中断されたコマンドの失敗を安全に診断する方法を学びます。
---

# TiDB Cloud CLI のトラブルシューティング

このリファレンスを使用して、CLI の認証、Starter、SQL、および中断されたコマンドの失敗を診断します。file system トークン、リージョン、companion プロセス、およびマウントについては、[TiDB Cloud Filesystem のトラブルシューティング](/tidb-cloud-filesystem/filesystem-troubleshooting.md) を参照してください。`--debug` は必要な場合にのみ追加し、共有する前にマスク済みの出力を確認してください。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## API 認証が失敗する {#api-authentication-fails}

症状としては、認証情報の欠落、Digest 認証の失敗、または権限拒否などがあります。

両方の環境変数がセットで設定されていることを確認してください。

```bash
test -n "$TIDB_CLOUD_PUBLIC_KEY"
test -n "$TIDB_CLOUD_PRIVATE_KEY"
```

保存済みの認証情報を使用する場合は、両方の変数を unset してから、プロファイルを確認してください。

```bash
unset TIDB_CLOUD_PUBLIC_KEY TIDB_CLOUD_PRIVATE_KEY
ti db list-db-clusters --db-cluster-type starter --profile default
```

API キーで認証自体は成功しても、コマンドが要求する権限を持っていない場合があります。その操作に必要なアクセス権を持つキーを使用してください。`ti configure` は TiDB Cloud に接続せずにローカル値を検証して保存するため、認証情報の失敗は最初にリモートコマンド実行時に現れます。

## Starter の作成がクォータに達する {#starter-creation-reaches-quota}

クォータおよび容量エラーは、組織が無料の Starter 制限に達したことを意味する場合があります。別のものを作成する前に、既存の Starter リソースを一覧表示してください。

```bash
ti db list-db-clusters --db-cluster-type starter --output text
```

無関係なリソースを削除して自動化を通そうとしないでください。Starter の支出制限では、請求の設定が必要になる場合があります。

## SQL 認証情報が見つからない {#sql-credentials-are-missing}

対象のクラスターに対して、ユーザーを準備または修復してください。

```bash
ti db create-db-sql-users --db-cluster-id "<cluster-id>"
```

その後、明示的なロールを指定して再試行してください。

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT 1"
```

`~/.ti/db_users/<cluster-id>/credentials` を削除すると、ローカルパスワードも削除されます。認証情報を作り出すのではなく、create/repair コマンドを実行してください。

## 中断されたコマンドによってリソースが残ります {#an-interrupted-command-leaves-resources}

リソースを一覧表示し、自分のワークフローで作成されたものだけを特定してください。削除前に describe を使用します。

```bash
ti db describe-db-cluster --db-cluster-id "<cluster-id>"
ti fs describe-file-system --file-system-id "<file-system-id>"
```

サポートされているクリーンアップ内容を事前確認するには、次を実行します。

```bash
ti db delete-db-cluster --db-cluster-id "<cluster-id>" --dry-run
ti fs delete-file-system \
  --file-system-id "<file-system-id>" \
  --dry-run
```

## 問題を報告する {#report-a-problem}

TiDB Cloud CLI のバージョン、OS とアーキテクチャ、コマンド名、安定したエラーコード、および秘匿情報を除去したログを含めてください。API キー、FS または vault トークン、DB パスワード、機密データを含む SQL、またはファイル内容は絶対に含めないでください。問題の報告先は [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues) です。
