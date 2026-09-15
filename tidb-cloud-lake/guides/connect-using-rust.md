---
title: 使用 Rust 连接 TiDB Cloud Lake
summary: 本页介绍如何使用 Rust 连接 TiDB Cloud Lake。
---

# 使用 Rust 连接 TiDB Cloud Lake

官方 Rust driver 为 Rust 应用提供原生连接能力，支持 async/await，并具备全面的类型安全。

## 安装 {#installation}

将 driver 添加到你的 `Cargo.toml` 中：

```toml
[dependencies]
lake-driver = "0.1.5-alpha.2"
tokio = { version = "1", features = ["full"] }
```

**Connection String**：有关 DSN 格式和示例，请参见[驱动概览](/tidb-cloud-lake/guides/driver-overview.md)。

---

## 主要特性 {#key-features}

- ✅ **Async/Await Support**：专为现代 Rust 异步编程构建
- ✅ **Type Safety**：结合 Rust 类型系统的强类型映射
- ✅ **Connection Pooling**：高效的连接管理
- ✅ **Stage Operations**：向 {{{ .lake }}} stages 上传/下载数据
- ✅ **Streaming Results**：高效处理大型结果集

## 数据类型映射 {#data-type-mappings}

### 基本类型 {#basic-types}

| {{{ .lake }}} | Rust                  | 备注                     |
| --------- | --------------------- | ------------------------ |
| BOOLEAN   | bool                  |                          |
| TINYINT   | i8, u8                |                          |
| SMALLINT  | i16, u16              |                          |
| INT       | i32, u32              |                          |
| BIGINT    | i64, u64              |                          |
| FLOAT     | f32                   |                          |
| DOUBLE    | f64                   |                          |
| DECIMAL   | String                | 保留精度                 |
| VARCHAR   | String                | UTF-8 编码               |
| BINARY    | `Vec<u8>`             |                          |

### 日期/时间类型 {#date-time-types}

| {{{ .lake }}} | Rust                  | 备注                    |
| --------- | --------------------- | ------------------------ |
| DATE      | chrono::NaiveDate     | 需要 chrono crate    |
| TIMESTAMP | chrono::NaiveDateTime | 需要 chrono crate    |

### 复杂类型 {#complex-types}

| {{{ .lake }}} | Rust            | 说明                     |
| ----------- | --------------- | ------------------------ |
| ARRAY[T]    | `Vec<T>`        | 支持嵌套数组             |
| TUPLE[T, U] | (T, U)          | 多元素元组               |
| MAP[K, V]   | `HashMap<K, V>` | 键值映射                 |
| VARIANT     | String          | JSON 编码                |
| BITMAP      | String          | Base64 编码              |
| GEOMETRY    | String          | WKT 格式                 |

---

## 基本用法 {#basic-usage}

以下是一个简单示例，演示 DDL、写入和查询操作：

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

## 资源 {#resources}

- **Crates.io**: [lake-driver](https://crates.io/crates/lake-driver)
- **GitHub Repository**: [LakeSQL/driver](https://github.com/tidbcloud/lakesql/tree/main/driver)
- **Rust Documentation**: [docs.rs/lake-driver](https://docs.rs/lake-driver)