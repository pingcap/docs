---
title: Connect to TiDB Cloud Lake Using Golang
summary: This page describes how to connect to TiDB Cloud Lake using Golang.
---

# Go Driver for Databend

The official Go driver providing a standard `database/sql` interface for seamless integration with existing Go applications.

## Installation

```bash
go get github.com/databendlabs/databend-go
```

**Connection String**: See [Drivers Overview](./index.md#connection-string-dsn) for DSN format and connection examples.

---

## Key Features

- ✅ **Standard Interface**: Full `database/sql` compatibility
- ✅ **Connection Pooling**: Built-in connection management
- ✅ **Bulk Operations**: Efficient batch inserts via transactions
- ✅ **Type Safety**: Comprehensive Go type mappings

## Data Type Mappings

| Databend | Go | Notes |
|----------|----|---------|
| **Integers** | | |
| `TINYINT` | `int8` | |
| `SMALLINT` | `int16` | |
| `INT` | `int32` | |
| `BIGINT` | `int64` | |
| `TINYINT UNSIGNED` | `uint8` | |
| `SMALLINT UNSIGNED` | `uint16` | |
| `INT UNSIGNED` | `uint32` | |
| `BIGINT UNSIGNED` | `uint64` | |
| **Floating Point** | | |
| `FLOAT` | `float32` | |
| `DOUBLE` | `float64` | |
| **Other Types** | | |
| `DECIMAL` | `decimal.Decimal` | Requires decimal package |
| `STRING` | `string` | |
| `DATE` | `time.Time` | |
| `TIMESTAMP` | `time.Time` | |
| `ARRAY(T)` | `string` | JSON encoded |
| `TUPLE(...)` | `string` | JSON encoded |
| `VARIANT` | `string` | JSON encoded |
| `BITMAP` | `string` | Base64 encoded |

---

## Basic Usage

```go
import (
    "database/sql"
    "fmt"
    "log"

    _ "github.com/databendlabs/databend-go"
)

// Connect to Databend
db, err := sql.Open("databend", "<your-dsn>")
if err != nil {
    log.Fatal(err)
}
defer db.Close()

// DDL: Create table
_, err = db.Exec("CREATE TABLE users (id INT, name STRING)")
if err != nil {
    log.Fatal(err)
}

// Write: Insert data
_, err = db.Exec("INSERT INTO users VALUES (?, ?)", 1, "Alice")
if err != nil {
    log.Fatal(err)
}

// Query: Select data
var id int
var name string
err = db.QueryRow("SELECT id, name FROM users WHERE id = ?", 1).Scan(&id, &name)
if err != nil {
    log.Fatal(err)
}

fmt.Printf("User: %d, %s\n", id, name)
```

## Resources

- **GitHub Repository**: [databend-go](https://github.com/databendlabs/databend-go)
- **Go Package**: [pkg.go.dev](https://pkg.go.dev/github.com/datafuselabs/databend-go)
- **Examples**: [GitHub Examples](https://github.com/databendlabs/databend-go/tree/main/examples)
