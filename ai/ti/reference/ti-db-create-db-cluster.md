---
title: ti db create-db-cluster
summary: TiDB Cloud Starter クラスターを作成します。
---

# ti db create-db-cluster

TiDB Cloud Starter インスタンスを作成します。必須の `--db-cluster-type` は `starter` である必要があり、暗黙的な型指定はありません。`--wait` を指定すると、クラスターが `ACTIVE` になるまで待機します。

このリクエストではプロジェクトを選択しません。TiDB Cloud はサーバー側のプロジェクトルールに従ってインスタンスを割り当て、`ti` はレスポンス内のプロジェクトメタデータをそのまま保持します。`ti` を使用してプロジェクトを選択または設定することはできません。

TiDB Cloud CLI は、返されたサービスプランを検証します。作成の受け付け後に検証が失敗した場合、`ti` はクラスター ID を報告し、調査用にそのインスタンスを保持します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db create-db-cluster
  --db-cluster-name <string>
  --db-cluster-type <string>
  [--dry-run]
  [--help]
  [--monthly-spending-limit-usd-cents <int32>]
  [--version]
  [--wait]
```

## オプション {#options}

- `--db-cluster-name <string>`: Starter DB クラスターの表示名です。\[required]
- `--db-cluster-type <string>`: DB クラスターのタイプです。`starter` である必要があります。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--monthly-spending-limit-usd-cents <int32>`: 月間利用上限を米ドルセント単位で指定します。省略した場合、`ti` は利用上限を送信せず、TiDB Cloud がデフォルトのルールを適用します。詳細は、[TiDB Cloud Starter インスタンスの利用上限を管理する](/tidb-cloud/manage-serverless-spend-limit.md) を参照してください。
- `--version`: バージョン情報を表示します。
- `--wait`: 作成したクラスターが `ACTIVE` になるまで待機してから戻ります。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- クラスターを作成し、アクティブになるまで待機します。

    ```bash
    # Wait until the new TiDB Cloud Starter instance reaches the ACTIVE state.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --wait
    ```

- クラスターを非同期で作成します。

    ```bash
    # Return after TiDB Cloud accepts creation so another process can poll the cluster.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name background-db
    ```

- クラスター作成をプレビューします。

    ```bash
    # Validate the request and resolved defaults without creating a cluster.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --dry-run
    ```

- 月間利用上限を設定します。

    ```bash
    # Create a paid TiDB Cloud Starter instance with a monthly limit expressed in US dollar cents.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name production-db --monthly-spending-limit-usd-cents 1000 --wait
    ```

## 作成後の検証に失敗した場合 {#if-post-creation-verification-fails}

TiDB Cloud が作成リクエストを受け付けたものの、`ti` が返されたリソースを Starter インスタンスとして検証できない場合は、エラー内のクラスター ID を確認してください。保持されたリソースは、次のコマンドで確認できます。

```bash
ti db describe-db-cluster --db-cluster-id "<cluster-id>"
```

`ti` が引き続きサービスプランを検証できない場合は、TiDB Cloud コンソールでリソースを確認または削除してください。最初のリクエストでインスタンスが作成されたかどうかを確認するまでは、create コマンドを再実行しないでください。

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)