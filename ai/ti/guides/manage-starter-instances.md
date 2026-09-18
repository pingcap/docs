---
title: TiDB Cloud Starter インスタンスを管理する
summary: TiDB Cloud CLI を使用して、Starter インスタンス、ブランチ、SQL ユーザー、接続、SQL ステートメントを作成および管理する方法を学びます。
---

# TiDB Cloud Starter インスタンスを管理する

このドキュメントでは、TiDB Cloud CLI の `ti db` コマンドを使用して、ターミナルまたは自動化ワークフローから TiDB Cloud Starter インスタンス、ブランチ、および SQL アクセスを管理する方法について説明します。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- TiDB Cloud Starter にアクセスできる認証情報を使用してプロファイルを設定します。

## TiDB Cloud Starter インスタンスを作成する {#create-a-tidb-cloud-starter-instance}

TiDB Cloud Starter インスタンスを作成し、アクティブになるまで待機します。

```shell
ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --wait
```

## インスタンスを一覧表示する {#list-instances}

有効なリージョン内の TiDB Cloud Starter インスタンスを一覧表示します。

```shell
ti db list-db-clusters --db-cluster-type starter --output text
```

TiDB Cloud Starter インスタンスの情報を取得するには、その ID を [`describe-db-cluster`](/ai/ti/reference/ti-db-describe-db-cluster.md) に渡します。

## ブランチを管理する {#manage-branches}

インスタンスから開発ブランチを作成します。

```shell
ti db create-db-cluster-branch \
  --db-cluster-id "<instance-id>" \
  --db-cluster-branch-name dev \
  --wait
```

ブランチの一覧表示、詳細表示、および削除コマンドを使用して、そのライフサイクルを管理します。各コマンドの完全なオプションについては、[`ti db` コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)を参照してください。

## SQL アクセスを設定する {#configure-sql-access}

インスタンス用の読み取り専用、読み取り/書き込み、および管理者 SQL ユーザーを作成または修復します。

```shell
ti db create-db-sql-users --db-cluster-id "<instance-id>"
```

保存されている認証情報をアプリケーション向けに整形します。

```shell
ti db format-db-connection-string \
  --db-cluster-id "<instance-id>" \
  --read-only \
  --format env
```

## SQL を実行する {#execute-sql}

明示的な SQL ロールを指定して 1 つのステートメントを実行します。

```shell
ti db execute-sql-statement \
  --db-cluster-id "<instance-id>" \
  --read-only \
  --sql "SELECT 1"
```

読み取り専用、読み取り/書き込み、および管理操作を分離するワークフローについては、[明示的な SQL ロールで TiDB Cloud Starter をクエリする](/ai/ti/guides/ti-query-sql-with-roles-example.md)を参照してください。

## インスタンスを削除する {#delete-an-instance}

インスタンスが不要になったら、それを削除し、削除が確認できるようになるまで待機します。

```shell
ti db delete-db-cluster --db-cluster-id "<instance-id>" --wait
```

## 次のステップ {#what-s-next}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)
- [日次の TiDB Cloud CLI ワークフローを実行する](/ai/ti/guides/ti-daily-workflow-example.md)