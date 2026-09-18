---
title: ti db list-db-cluster-branches
summary: TiDB Cloud Starter クラスターのブランチを一覧表示します。
---

# ti db list-db-cluster-branches

1 つの TiDB Cloud Starter インスタンスのブランチを、必要に応じてページネーション付きで一覧表示します。このコマンドは、ブランチを一覧表示する前に親クラスターが Starter であることを検証します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db list-db-cluster-branches
  --db-cluster-id <string>
  [--help]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## オプション {#options}

- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--help`: ヘルプ情報を表示します。
- `--page-size <int32>`: リクエストするブランチ数です。省略した場合、または `0` に設定した場合、API は最大 `10` 件を返します。API の最大値は `100` で、`100` を超える値は `100` に設定されます。
- `--page-token <string>`: 以前の list-db-cluster-branches 呼び出しで返されたページトークンです。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- クラスターのブランチを一覧表示します。

    ```bash
    # Return all branches that belong to the selected TiDB Cloud Starter instance.
    ti db list-db-cluster-branches --db-cluster-id "<cluster-id>"
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)