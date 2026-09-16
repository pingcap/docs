---
title: ti db delete-db-cluster-branch
summary: TiDB Cloud Starter クラスターからブランチを削除します。
---

# ti db delete-db-cluster-branch

TiDB Cloud Starter インスタンスから 1 つのブランチを削除します。このコマンドは、ブランチの読み取りまたは削除を行う前に、親クラスターが Starter であることを検証します。削除レスポンスはポーリングせずに返され、このコマンドでは `--wait` オプションは提供されません。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db delete-db-cluster-branch
  --db-cluster-branch-id <string>
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## オプション {#options}

- `--db-cluster-branch-id <string>`: Starter DB クラスターのブランチ ID。\[required]
- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ブランチを削除する:

    ```bash
    # Delete only the selected branch from its parent TiDB Cloud Starter instance.
    ti db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"
    ```

ブランチが表示されなくなったことを確認するには、`ti db list-db-cluster-branches --db-cluster-id "<cluster-id>"` を実行します。

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)