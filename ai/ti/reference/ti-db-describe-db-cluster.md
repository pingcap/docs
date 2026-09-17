---
title: ti db describe-db-cluster
summary: TiDB Cloud Starter クラスターの詳細を表示します。
---

# ti db describe-db-cluster

TiDB Cloud Starter インスタンスの情報を取得します。デフォルトの `BASIC` ビューでは、インスタンスの基本情報が返されます。TiDB Cloud API から取得可能な完全な詳細を要求するには、`--view FULL` を使用します。クラスターの API メタデータによって Starter であることを確認できない場合、このコマンドはそのクラスターを拒否します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db describe-db-cluster
  --db-cluster-id <string>
  [--help]
  [--version]
  [--view <string>]
```

## オプション {#options}

- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。
- `--view <string>`: 詳細レベル: `BASIC` または `FULL`。省略した場合、TiDB Cloud API は `BASIC` を使用します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- TiDB Cloud Starter インスタンスの情報を取得します。

    ```bash
    # Return the instance state, placement, and connection metadata.
    ti db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)