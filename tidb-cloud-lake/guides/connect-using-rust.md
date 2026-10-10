---
title: Rust を使用して TiDB Cloud Lake に接続する
summary: このページでは、Rust を使用して TiDB Cloud Lake に接続する方法について説明します。
---

# Rust を使用して TiDB Cloud Lake に接続する

公式の Rust ドライバーは、async/await サポートと包括的な型安全性を備え、Rust アプリケーション向けにネイティブ接続を提供します。

## インストール {#installation}

ドライバーを `Cargo.toml` に追加します。

```toml
[dependencies]
lake-driver = "0.1.5-alpha.2"
tokio = { version = "1", features = ["full"] }
```

**Connection String**: DSN の形式と例については、[ドライバー概要](/tidb-cloud-lake/guides/driver-overview.md) を参照してください。

---

## 主な機能 {#key-features}

- ✅ **Async/Await Support**: モダンな Rust 非同期プログラミング向けに構築
- ✅ **Type Safety**: Rust の型システムによる強力な型マッピング
- ✅ **Connection Pooling**: 効率的な接続管理
- ✅ **Stage Operations**: {{{ .lake }}} stage との間でデータをアップロード/ダウンロード
- ✅ **Streaming Results**: 大規模な結果セットを効率的に処理

## データ型マッピング {#data-type-mappings}

### 基本型 {#basic-types}

| {{{ .lake }}} | Rust                  | 注記                     |
| --------- | --------------------- | ------------------------ |
| BOOLEAN   | bool                  |                          |
| TINYINT   | i8, u8                |                          |
| SMALLINT  | i16, u16              |                          |
| INT       | i32, u32              |                          |
| BIGINT    | i64, u64              |                          |
| FLOAT     | f32                   |                          |
| DOUBLE    | f64                   |                          |
| DECIMAL   | String                | 精度を保持               |
| VARCHAR   | String                | UTF-8 エンコード         |
| BINARY    | `Vec<u8>`             |                          |

### 日付/時刻型 {#date-time-types}

| {{{ .lake }}} | Rust                  | 注記                     |
| --------- | --------------------- | ------------------------ |
| DATE      | chrono::NaiveDate     | chrono crate が必要      |
| TIMESTAMP | chrono::NaiveDateTime | chrono crate が必要      |

### 複合型 {#complex-types}

| {{{ .lake }}} | Rust            | 注記                     |
| ----------- | --------------- | ------------------------ |
| ARRAY[T]    | `Vec<T>`        | ネストされた配列をサポート |
| TUPLE[T, U] | (T, U)          | 複数要素のタプル         |
| MAP[K, V]   | `HashMap<K, V>` | キーと値のマッピング     |
| VARIANT     | String          | JSON エンコード          |
| BITMAP      | String          | Base64 エンコード        |
| GEOMETRY    | String          | WKT 形式                 |

---

## 基本的な使い方 {#basic-usage}

以下は、DDL、書き込み、およびクエリ操作を示すシンプルな例です。

```rust
use lake_driver::Client;
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Connect to TiDB Cloud Lake
    let client = Client::new("<your-dsn>".to_string());
    let conn = client.get_conn().await?;

    // DDL: Create table
    conn.exec("CREATE TABLE IF NOT EXISTS users (id INT, name VARCHAR, created_at TIMESTAMP)")
        .await?;

    // Write: Insert data
    conn.exec("INSERT INTO users VALUES (1, 'Alice', '2023-12-01 10:00:00')")
        .await?;
    conn.exec("INSERT INTO users VALUES (2, 'Bob', '2023-12-01 11:00:00')")
        .await?;

    // Query: Select data
    let mut rows = conn.query_iter("SELECT id, name, created_at FROM users ORDER BY id")
        .await?;

    while let Some(row) = rows.next().await {
        let (id, name, created_at): (i32, String, chrono::NaiveDateTime) =
            row?.try_into()?;
        println!("User {}: {} (created: {})", id, name, created_at);
    }

    Ok(())
}
```

## リソース {#resources}

- **Crates.io**: [lake-driver](https://crates.io/crates/lake-driver)
- **GitHub リポジトリ**: [LakeSQL/driver](https://github.com/tidbcloud/lakesql/tree/main/driver)
- **Rust ドキュメント**: [docs.rs/lake-driver](https://docs.rs/lake-driver)
