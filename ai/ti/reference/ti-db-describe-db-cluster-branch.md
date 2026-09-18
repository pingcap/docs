---
title: ti db describe-db-cluster-branch
summary: TiDB Cloud Starter クラスターのブランチを記述します。
---

# ti db describe-db-cluster-branch

クラスター ID とブランチ ID を指定して、1 つのブランチを記述します。デフォルトの `FULL` ビューでは、TiDB Cloud API から取得可能な完全なブランチ詳細を返します。基本情報のみを取得するには、`--view BASIC` を使用します。このコマンドは、ブランチを読み取る前に親クラスターが Starter であることを確認します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db describe-db-cluster-branch
  --db-cluster-branch-id <string>
  --db-cluster-id <string>
  [--help]
  [--version]
  [--view <string>]
```

## オプション {#options}

- `--db-cluster-branch-id <string>`: Starter DB クラスターのブランチ ID。\[required]
- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。
- `--view <string>`: 詳細レベル: `BASIC` または `FULL`。省略した場合、TiDB Cloud API は `FULL` を使用します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- ブランチを記述する:

    ```bash
    # Return full lifecycle and connection details for one branch.
    ti db describe-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>" --view FULL
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)