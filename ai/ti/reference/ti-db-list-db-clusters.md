---
title: ti db list-db-clusters
summary: TiDB Cloud Starter クラスターを一覧表示します。
---

# ti db list-db-clusters

選択したリージョン内の TiDB Cloud Starter インスタンスを一覧表示します。必要に応じて、ページネーション、フィルタリング、並べ替え、JMESPath による射影を指定できます。必須の `--db-cluster-type` は `starter` である必要があります。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db list-db-clusters
  --db-cluster-type <string>
  [--filter <string>]
  [--help]
  [--order-by <string>]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## オプション {#options}

- `--db-cluster-type <string>`: DB クラスターのタイプです。`starter` である必要があります。\[required]
- `--filter <string>`: TiDB Cloud Starter API のフィルタ式です。API は、`region.provider`、`region.name`、`state`、`projectId`、`clusterId`、`displayName`、`labels.<key>` に対して、Google AIP スタイルの `=` および `AND` 式をサポートします。
- `--help`: ヘルプ情報を表示します。
- `--order-by <string>`: TiDB Cloud Starter API の `orderBy` 式です。`ti` はこの値を解釈せず、そのまま API に渡します。
- `--page-size <int32>`: 返される検証済みクラスターの数です。省略した場合、または `0` に設定した場合のデフォルトは `10` です。最大値は `1000` です。
- `--page-token <string>`: 以前の互換性のある list-db-clusters 呼び出しで返された、不透明な ti ページトークンです。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- クラスターを一覧表示する:

    ```bash
    # Return TiDB Cloud Starter instances in the profile's configured region as structured JSON.
    ti db list-db-clusters --db-cluster-type starter
    ```

- 別のリージョンのクラスターを一覧表示する:

    ```bash
    # Override the region for this invocation without changing the profile.
    ti --region aws-us-west-2 db list-db-clusters --db-cluster-type starter
    ```

- クラスターのフィールドを選択する:

    ```bash
    # Reduce the result to IDs, names, and lifecycle states.
    ti db list-db-clusters --db-cluster-type starter --query 'clusters[].{id:id,name:display_name,state:state}'
    ```

- アクティブなクラスターをフィルタリングする:

    ```bash
    # Combine this filter with the mandatory effective-region filter.
    ti db list-db-clusters --db-cluster-type starter --filter 'state="ACTIVE"'
    ```

## リージョン解決 {#region-resolution}

有効なリージョンは、グローバル `--region`、次に `TI_REGION_CODE`、次に選択したプロファイルの `region_code` の順に解決されます。ユーザー指定の `--filter` 式は、この必須のリージョンスコープと結合されるため、結果を他のリージョンに拡張することはできません。

リージョンをまたぐインスタンスおよび非Starter インスタンスは除外されます。また、サービスプランまたはリージョン情報の欠落や競合により、選択したリージョン内の Starter インスタンスであることを `ti` が検証できない場合も、そのインスタンスは除外されます。

## フィルタと並べ替えの動作 {#filter-and-ordering-behavior}

`ti` は、ユーザー指定のフィルタ式および並べ替え式を TiDB Cloud Starter API に渡します。無効または未サポートの式は API によって拒否されます。API の仕様については、[TiDB Cloud API v1beta1 の概要](/api/tidb-cloud-api-v1beta1.md) を参照してください。

## ページトークンの再利用 {#page-token-reuse}

このコマンドは、1 つの結果ページを満たすために複数の TiDB Cloud API ページを取得でき、`ti` の `next_page_token` を返します。検証済みの結果外のリソースを含む可能性があるため、API の `total_size` は省略されます。

ページトークンは、同じプロファイル、クラスタータイプ、リージョン、フィルタ、並べ替えでのみ再利用できます。再実行時のページが変更されている場合は、`--page-token` を付けずに一覧取得をやり直してください。

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)