---
title: ti db update-db-cluster
summary: TiDB Cloud Starter クラスターを更新します。
---

# ti db update-db-cluster

TiDB Cloud Starter インスタンスの表示名または月間支出上限を更新します。`--db-cluster-name` または `--monthly-spending-limit-usd-cents` の少なくとも一方が必要です。このコマンドは Starter インスタンスのみを受け付けます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db update-db-cluster
  --db-cluster-id <string>
  [--db-cluster-name <string>]
  [--dry-run]
  [--help]
  [--monthly-spending-limit-usd-cents <int32>]
  [--version]
```

## オプション {#options}

- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--db-cluster-name <string>`: 新しい Starter DB クラスターの表示名。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--monthly-spending-limit-usd-cents <int32>`: 米ドルセント単位の月間支出上限。省略すると変更されません。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- クラスター名を変更する:

    ```bash
    # Change the TiDB Cloud Starter instance display name without recreating it.
    ti db update-db-cluster --db-cluster-id "<cluster-id>" --db-cluster-name app-db-v2
    ```

- 支出上限の更新をプレビューする:

    ```bash
    # Validate a new monthly limit without applying the change.
    ti db update-db-cluster --db-cluster-id "<cluster-id>" --monthly-spending-limit-usd-cents 1000 --dry-run
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)