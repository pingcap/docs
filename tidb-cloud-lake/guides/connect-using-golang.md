---
title: 使用 Golang 连接 TiDB Cloud Lake
summary: 本页介绍如何使用 Golang 连接 TiDB Cloud Lake。
---

# 使用 Golang 连接 TiDB Cloud Lake

官方 Go 驱动提供了标准的 `database/sql` 接口，可与现有 Go 应用无缝集成。

## 安装 {#installation}

```bash
go get github.com/tidbcloud/lake-go
```

**Connection String**：有关 DSN 格式和示例，请参见[驱动概览](/tidb-cloud-lake/guides/driver-overview.md)。

---

## 主要特性 {#key-features}

- ✅ **标准接口**：完全兼容 `database/sql`
- ✅ **连接池**：内置连接管理
- ✅ **批量操作**：通过事务高效执行批量插入
- ✅ **类型安全**：提供全面的 Go 类型映射

## 数据类型映射 {#data-type-mappings}

| {{{ .lake }}} | Go | 说明 |
|----------|----|---------|
| **整数型** | | |
| `TINYINT` | `int8` | |
| `SMALLINT` | `int16` | |
| `INT` | `int32` | |
| `BIGINT` | `int64` | |
| `TINYINT UNSIGNED` | `uint8` | |
| `SMALLINT UNSIGNED` | `uint16` | |
| `INT UNSIGNED` | `uint32` | |
| `BIGINT UNSIGNED` | `uint64` | |
| **浮点型** | | |
| `FLOAT` | `float32` | |
| `DOUBLE` | `float64` | |
| **其他类型** | | |
| `DECIMAL` | `decimal.Decimal` | 需要 decimal 包 |
| `STRING` | `string` | |
| `DATE` | `time.Time` | |
| `TIMESTAMP` | `time.Time` | |
| `ARRAY(T)` | `string` | JSON 编码 |
| `TUPLE(...)` | `string` | JSON 编码 |
| `VARIANT` | `string` | JSON 编码 |
| `BITMAP` | `string` | Base64 编码 |

---

## 基本用法 {#basic-usage}

```go
import (
    "database/sql"
    "fmt"
    "log"

    _ "github.com/tidbcloud/lake-go"
)

// Connect to {{{ .lake }}}
db, err := sql.Open("lake", "<your-dsn>")
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

## 资源 {#resources}

- **GitHub 仓库**：[lake-go](https://github.com/tidbcloud/lake-go)
- **示例**：[GitHub Examples](https://github.com/tidbcloud/lake-go/tree/main/examples)