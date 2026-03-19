---
title: Connect to TiDB Cloud Lake Using Rust
summary: This page describes how to connect to TiDB Cloud Lake using Rust.
---

# Rust Driver for Databend

The official Rust driver providing native connectivity with async/await support and comprehensive type safety for Rust applications.

## Installation

Add the driver to your `Cargo.toml`:

```toml
[dependencies]
databend-driver = "0.30"
tokio = { version = "1", features = ["full"] }
```

**Connection String**: See [Drivers Overview](./index.md#connection-string-dsn) for DSN format and connection examples.

---

## Key Features

- ✅ **Async/Await Support**: Built for modern Rust async programming
- ✅ **Type Safety**: Strong type mapping with Rust's type system
- ✅ **Connection Pooling**: Efficient connection management
- ✅ **Stage Operations**: Upload/download data to/from Databend stages
- ✅ **Streaming Results**: Process large result sets efficiently

## Data Type Mappings

### Basic Types
| Databend  | Rust                  | Notes                    |
| --------- | --------------------- | ------------------------ |
| BOOLEAN   | bool                  |                          |
| TINYINT   | i8, u8                |                          |
| SMALLINT  | i16, u16              |                          |
| INT       | i32, u32              |                          |
| BIGINT    | i64, u64              |                          |
| FLOAT     | f32                   |                          |
| DOUBLE    | f64                   |                          |
| DECIMAL   | String                | Precision preserved      |
| VARCHAR   | String                | UTF-8 encoded            |
| BINARY    | `Vec<u8>`             |                          |

### Date/Time Types
| Databend  | Rust                  | Notes                    |
| --------- | --------------------- | ------------------------ |
| DATE      | chrono::NaiveDate     | Requires chrono crate    |
| TIMESTAMP | chrono::NaiveDateTime | Requires chrono crate    |

### Complex Types
| Databend    | Rust            | Notes                    |
| ----------- | --------------- | ------------------------ |
| ARRAY[T]    | `Vec<T>`        | Nested arrays supported  |
| TUPLE[T, U] | (T, U)          | Multiple element tuples  |
| MAP[K, V]   | `HashMap<K, V>` | Key-value mappings       |
| VARIANT     | String          | JSON-encoded             |
| BITMAP      | String          | Base64-encoded           |
| GEOMETRY    | String          | WKT format               |

---

## Basic Usage

Here's a simple example demonstrating DDL, write, and query operations:

```rust
use databend_driver::Client;
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Connect to Databend
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

## Resources

- **Crates.io**: [databend-driver](https://crates.io/crates/databend-driver)
- **GitHub Repository**: [BendSQL/driver](https://github.com/databendlabs/BendSQL/tree/main/driver)
- **Rust Documentation**: [docs.rs/databend-driver](https://docs.rs/databend-driver)
