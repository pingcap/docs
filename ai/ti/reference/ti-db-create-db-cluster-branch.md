---
title: ti db create-db-cluster-branch
summary: TiDB Cloud Starter クラスターのブランチを作成します。
---

# ti db create-db-cluster-branch

1 つの TiDB Cloud Starter インスタンスに対してブランチを作成します。`--wait` を指定すると、ブランチが `ACTIVE` になるまで待機します。このコマンドは、ブランチを作成する前に親クラスターが Starter であることを検証します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db create-db-cluster-branch
  --db-cluster-branch-name <string>
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## オプション {#options}

- `--db-cluster-branch-name <string>`: Starter DB クラスターのブランチ表示名。\[required]
- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。
- `--wait`: 作成されたブランチが `ACTIVE` になるまで待機してから戻ります。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ブランチを作成し、アクティブになるまで待機する場合:

    ```bash
    # Wait until the new database branch can accept connections.
    ti db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name dev --wait
    ```

- ブランチ作成をプレビューする場合:

    ```bash
    # Validate the parent cluster and branch request without creating it.
    ti db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name preview --dry-run
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)