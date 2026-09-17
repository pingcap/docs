---
title: ti db execute-sql-statement
summary: TiDB Cloud Starter クラスターに対して 1 つの SQL ステートメントを実行します。
---

# ti db execute-sql-statement

TiDB Cloud Starter インスタンスに対して 1 つの SQL ステートメントを実行します。デフォルトのアクセスロールは read-write です。ロールは明示的に指定することを推奨します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db execute-sql-statement
  --db-cluster-id <string>
  --sql <string>
  [--admin]
  [--database <string>]
  [--help]
  [--read-only]
  [--read-write]
  [--transport <string>]
  [--version]
```

## オプション {#options}

- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--sql <string>`: 実行する 1 つの SQL ステートメント。\[required]
- `--admin`: 用意された admin DB SQL 認証情報を使用します。
- `--database <string>`: データベース / デフォルトスキーマ名。
- `--help`: ヘルプ情報を表示します。
- `--read-only`: 用意された `read_only` DB SQL 認証情報を使用します。
- `--read-write`: 用意された `read_write` DB SQL 認証情報を使用します。
- `--transport <string>`: SQL 実行トランスポート: `https` または `mysql`。\[default: https]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- デフォルトの read-write ロールでステートメントを実行する:

    ```bash
    # Use the default prepared role for normal application reads and writes.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --sql "INSERT INTO app.events(message) VALUES ('ready')"
    ```

- read-only クエリを実行する:

    ```bash
    # Prevent the statement from using read-write or admin credentials.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --read-only --sql "SELECT 1 AS ready" --output text
    ```

- 管理用ステートメントを実行する:

    ```bash
    # Use the admin role for schema creation or privilege management.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --admin --sql "CREATE DATABASE IF NOT EXISTS app"
    ```

- MySQL フォールバックトランスポートを使用する:

    ```bash
    # Open a direct TLS MySQL connection when the workflow requires the MySQL protocol.
    ti db execute-sql-statement --db-cluster-id "<cluster-id>" --transport mysql --sql "SELECT CURRENT_TIMESTAMP"
    ```

## トランスポートを選択する {#choose-a-transport}

デフォルトの `https` トランスポートは、ステートメントを TiDB Cloud HTTPS SQL API に送信します。`mysql` トランスポートは、インスタンスへの直接 TLS MySQL 接続を開き、ステートメントを 1 回実行してから接続を閉じます。`mysql` は、ネットワークまたはワークフローで MySQL プロトコルが特に必要な場合にのみ使用してください。

CLI は、`https` から `mysql` へ自動的にフォールバックしたり、もう一方のトランスポートでステートメントを再試行したりしません。これにより、障害が曖昧な場合に書き込みステートメントが 2 回実行されることを防ぎます。

## 出力 {#output}

JSON 出力には、`fields`、`rows`、`row_count`、該当する場合は `rows_affected`、該当する場合は `last_insert_id`、`transport`、`access_mode`、および `cluster_id` が含まれます。`rows` 内の各項目は、カラム名をキーとするオブジェクトです。

`--output text` を指定すると、クエリ結果はカラム見出しと行数を含むテーブルとして表示されます。行を返さないステートメントでは、影響を受けた行数と、利用可能な場合は最後の insert ID を含む `Query OK` メッセージが出力されます。

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)