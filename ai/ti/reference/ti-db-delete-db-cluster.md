---
title: ti db delete-db-cluster
summary: TiDB Cloud Starter クラスターを削除します。
---

# ti db delete-db-cluster

TiDB Cloud Starter インスタンスを削除します。削除が完了するまで待機するには、`--wait` を使用します。このコマンドは TiDB Cloud Starter インスタンスのみを受け付け、その他のクラスタータイプは拒否します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db delete-db-cluster
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## オプション {#options}

- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。
- `--wait`: TiDB Cloud が削除リクエストを受け付けた後、インスタンスが `DELETED` に到達するまでポーリングします。その後に `not found` または `permission denied` の応答が返された場合も、インスタンスを読み取れなくなっているため、削除完了として扱われます。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- クラスターを削除し、完了まで待機する場合:

    ```bash
    # Wait until TiDB Cloud reports the cluster deleted or no longer accessible.
    ti db delete-db-cluster --db-cluster-id "<cluster-id>" --wait
    ```

- クラスターを非同期で削除する場合:

    ```bash
    # Return after TiDB Cloud accepts deletion while cleanup continues remotely.
    ti db delete-db-cluster --db-cluster-id "<cluster-id>"
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)