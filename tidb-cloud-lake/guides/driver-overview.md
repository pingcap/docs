---
title: ドライバーを使用して TiDB Cloud Lake に接続する
summary: TiDB Cloud Lake への接続に使用できる公式ドライバーの概要。
---

# ドライバーを使用して TiDB Cloud Lake に接続する

{{{ .lake }}} は複数のプログラミング言語向けに公式ドライバーを提供しており、アプリケーションから {{{ .lake }}} に接続して操作できます。

## クイックスタート {#quick-start}

1. **言語を選択** - Python、Go、Node.js、Java、または Rust から選択します
2. **接続文字列を取得** - 以下の DSN 形式を使用します
3. **インストールして接続** - ドライバーごとのドキュメントに従います

## 接続文字列（DSN） {#connection-string-dsn}

すべての {{{ .lake }}} ドライバーは、同じ DSN（Data Source Name）形式を使用します。

```
lake://user:pwd@host[:port]/[database][?sslmode=disable][&arg1=value1]
```

> **Note:**
>
> `user:pwd` は {{{ .lake }}} の SQL ユーザーを指します。ユーザーの作成と権限の付与については、[CREATE USER](/tidb-cloud-lake/sql/create-user.md) を参照してください。

### 接続例 {#connection-examples}

| デプロイメント         | 接続文字列                                        |
| ------------------ | -------------------------------------------------------- |
| **{{{ .lake }}}** | `lake://user:pwd@host:443/database?warehouse=wh`     |

### パラメーターリファレンス {#parameters-reference}

| パラメーター   | 説明    | {{{ .lake }}}  | 例                 |
| ----------- | -------------- | -------------- | ----------------------- |
| `sslmode`   | SSL モード       | 使用しない       | `?sslmode=disable`      |
| `warehouse` | Warehouse 名 | 必須       | `?warehouse=compute_wh` |

> **{{{ .lake }}}**: [接続情報を取得 →](/tidb-cloud-lake/guides/warehouse.md#obtaining-connection-information)

## 利用可能なドライバー {#available-drivers}

| 言語                | パッケージ                                     | 主な機能                                                                  |
| ----------------------- | ------------------------------------------- | ----------------------------------------------------------------------------- |
| **[Python](/tidb-cloud-lake/guides/connect-using-python.md)**  | `tidbcloudlake-driver`<br/>`lake-sqlalchemy` | • 同期/非同期をサポート<br/>• SQLAlchemy 方言<br/>• PEP 249 互換        |
| **[Go](/tidb-cloud-lake/guides/connect-using-golang.md)**      | `lake-go`                               | • database/sql インターフェース<br/>• 接続プーリング<br/>• 一括操作       |
| **[Node.js](/tidb-cloud-lake/guides/connect-using-node-js.md)** | `tidbcloudlake-driver`                           | • TypeScript をサポート<br/>• Promise ベースの API<br/>• 結果のストリーミング          |
| **[Java](/tidb-cloud-lake/guides/connect-using-java.md)**      | `lake-jdbc`                             | • JDBC 4.0 互換<br/>• 接続プーリング<br/>• プリペアドステートメント      |
| **[Rust](/tidb-cloud-lake/guides/connect-using-rust.md)**      | `lake-driver`                           | • async/await をサポート<br/>• 型安全なクエリ<br/>• ゼロコピー逆シリアル化 |