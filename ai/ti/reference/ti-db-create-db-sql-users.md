---
title: ti db create-db-sql-users
summary: TiDB Cloud Starter インスタンス用に、TiDB Cloud CLI が管理する SQL ユーザーを作成します。
---

# ti db create-db-sql-users

TiDB Cloud Starter インスタンス用に、`ti` が管理する 3 つの SQL ユーザー（read-only、read-write、admin）を作成または修復します。これらの認証情報はローカルに保存されるため、後続のコマンドで `--read-only`、`--read-write`、または `--admin` を使用して適切なユーザーを選択できます。

これらのユーザーには、以下の事前定義されたアクセスレベルと組み込みの TiDB Cloud ロールがあります。

| `ti` access mode | TiDB Cloud built-in role | 想定用途 |
| --- | --- | --- |
| `read_only` | `role_readonly` | データを変更せずにクエリおよび検証を行う |
| `read_write` | `role_readwrite` | アプリケーションデータのクエリおよび変更を行う |
| `admin` | `role_admin` | スキーマ変更を行い、権限を管理する |

TiDB Cloud のロールモデルについては、[データベースユーザーとロールの管理](/tidb-cloud/configure-sql-users.md) を参照してください。

`ti` は、生成されたユーザー名とパスワードを `~/.ti/db_users/<cluster-id>/credentials` に保存し、3 つのアクセスモードごとに個別の TOML セクションを作成します。POSIX 権限をサポートするシステムでは、認証情報ファイルは所有者のみが読み書きできます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti db create-db-sql-users
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## オプション {#options}

- `--db-cluster-id <string>`: Starter DB クラスター ID。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 管理対象の SQL ユーザーを作成します。

    ```bash
    # Create or reconcile the read-only, read-write, and admin SQL users.
    ti db create-db-sql-users --db-cluster-id "<cluster-id>"
    ```

- SQL ユーザー作成をプレビューします。

    ```bash
    # Show the three managed roles without changing SQL users or local credentials.
    ti db create-db-sql-users --db-cluster-id "<cluster-id>" --dry-run
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)