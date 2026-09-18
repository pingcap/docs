---
title: 明示的な SQL ロールで TiDB Cloud Starter をクエリする
summary: TiDB Cloud CLI で管理される SQL ユーザーを準備し、明示的な権限の意図に基づいて読み取り専用、読み書き、管理者ステートメントを実行します。
---

# 明示的な SQL ロールで TiDB Cloud Starter をクエリする

このワークフローでは、3 つの SQL ロールを一度だけ準備し、その後は各ステートメントに対して最小権限のロールを明示的に選択します。各コマンドでデータベースパスワードを扱うことなく、対話的または自動化されたスキーマ操作、データ操作、検証作業に利用できます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 仕組み {#how-it-works}

従来のデータベース接続では、1 つの認証情報を使用し、その認証情報の権限がセッション中維持されます。これに対して、`ti db create-db-sql-users` は 3 つの固定 ID を作成し、それらの認証情報をローカルに保存します。`execute-sql-statement` を呼び出すたびに 1 つの ID を選択して 1 つのステートメントを実行するため、確認ステップで書き込み権限や管理者権限を保持し続ける必要がありません。

| ロール | 用途 |
| --- | --- |
| `admin` | スキーマ変更と権限管理 |
| `read-write` | アプリケーションデータの変更 |
| `read-only` | クエリと検証 |

## 前提条件 {#prerequisites}

- `ti` を設定します。
- アクティブな TiDB Cloud Starter インスタンス ID を選択します。

## ステップ 1. SQL ユーザーを準備する {#step-1-prepare-sql-users}

```bash
ti db create-db-sql-users \
  --db-cluster-id "<cluster-id>"
```

このコマンドは冪等であり、`read_only`、`read_write`、`admin` の認証情報を作成または修復します。

## ステップ 2. スキーマ変更には admin を使用する {#step-2-use-admin-for-schema-changes}

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "CREATE DATABASE IF NOT EXISTS role_demo"

ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --database role_demo \
  --sql "CREATE TABLE IF NOT EXISTS messages (id BIGINT PRIMARY KEY, body VARCHAR(255))"
```

## ステップ 3. データ変更には read-write を使用する {#step-3-use-read-write-for-data-changes}

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-write \
  --database role_demo \
  --sql "INSERT INTO messages(id, body) VALUES (1, 'hello') ON DUPLICATE KEY UPDATE body = VALUES(body)"
```

## ステップ 4. 検証には read-only を使用する {#step-4-use-read-only-for-verification}

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --sql "SELECT id, body FROM messages ORDER BY id" \
  --output text
```

期待される結果には、ID `1` と body `hello` が含まれます。

## ステップ 5. 接続環境を整形する {#step-5-format-a-connection-environment}

表示する代わりに、出力を保護されたローカルファイルへ直接書き込みます。

```bash
umask 077
ti db format-db-connection-string \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --database role_demo \
  --format env \
  --env-include-database-url > .env.tidb
```

`.env.tidb` をコミットしないでください。

`--format env` を使用すると、このコマンドは `TIDB_HOST`、`TIDB_USER`、`TIDB_PASSWORD` などの個別の `TIDB_` 接続変数を書き出します。`--env-include-database-url` オプションを指定すると、単一の MySQL 接続 URL を受け付けるアプリケーション向けに `DATABASE_URL` の値も追加されます。

## クリーンアップ {#cleanup}

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --admin \
  --sql "DROP DATABASE role_demo"

rm -f .env.tidb
```

## セキュリティに関する注意 {#security-notes}

- 各ステートメントでは、最小権限の明示的なロールを使用してください。
- `ti` は 1 回の呼び出しにつき 1 つの SQL ステートメントを受け付けます。
- HTTPS はデフォルトの SQL 実行トランスポートです。代わりに直接 TLS MySQL 接続を開くには、`--transport mysql` を指定してください。CLI が自動的にトランスポートを切り替えることはありません。
- 接続文字列および環境変数の出力には認証情報が含まれます。

## 次のステップ {#what-s-next}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)