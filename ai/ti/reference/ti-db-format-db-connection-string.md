---
title: ti db format-db-connection-string
summary: TiDB Cloud CLI で管理される SQL ユーザー向けの接続文字列を整形します。
---

# ti db format-db-connection-string

保存されている SQL 認証情報を、読み書き、読み取り専用、または管理者アクセス用に整形します。ロールオプションを指定しない場合、このコマンドは `read_write` を使用します。このコマンドは、ローカルの SQL 認証情報を読み込む前に、クラスターが Starter であることを検証します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db format-db-connection-string
  --db-cluster-id <string>
  [--admin]
  [--database <string>]
  [--env-database-url-name <string>]
  [--env-include-database-url]
  [--env-prefix <string>]
  [--format <string>]
  [--help]
  [--read-only]
  [--read-write]
  [--version]
```

## オプション {#options}

- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--admin`: 準備済みの管理者 DB SQL 認証情報を使用します。
- `--database <string>`: データベース名 / デフォルトスキーマ名。
- `--env-database-url-name <string>`: `--format env` 用の Database URL 変数名。\[default: DATABASE_URL]
- `--env-include-database-url`: `--format env` とともに Database URL 変数を含めます。
- `--env-prefix <string>`: `--format env` 用の dotenv 変数プレフィックス。\[default: TIDB_]
- `--format <string>`: 接続文字列の形式: `mysql-uri`、`jdbc`、`go-sql-driver`、`sqlalchemy`、または `env`。\[default: mysql-uri]
- `--help`: ヘルプ情報を表示します。
- `--read-only`: 準備済みの `read_only` DB SQL 認証情報を使用します。
- `--read-write`: 準備済みの `read_write` DB SQL 認証情報を使用します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 読み書き用の MySQL URI を整形する:

    ```bash
    # Use the default application role in tools that accept a MySQL URI.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-write --format mysql-uri
    ```

- 読み取り専用の dotenv 変数を整形する:

    ```bash
    # Emit environment assignments for a workload that must not modify data.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-only --format env --env-prefix TIDB_
    ```

- 管理者 JDBC URL を整形する:

    ```bash
    # Generate a JDBC connection value with the prepared admin credentials.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --admin --format jdbc --database app
    ```

- dotenv 出力に DATABASE_URL を含める:

    ```bash
    # Emit both component variables and a conventional DATABASE_URL value.
    ti db format-db-connection-string --db-cluster-id "<cluster-id>" --read-write --format env --env-include-database-url
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)