---
title: Golang を使用して TiDB Cloud Lake に接続する
summary: このページでは、Golang を使用して TiDB Cloud Lake に接続する方法について説明します。
---

# Golang を使用して TiDB Cloud Lake に接続する

公式の Go ドライバーは、既存の Go アプリケーションとシームレスに統合できる標準の `database/sql` インターフェースを提供します。

## インストール {#installation}

```bash
go get github.com/tidbcloud/lake-go
```

**Connection String**: DSN の形式と例については、[ドライバー概要](/tidb-cloud-lake/guides/driver-overview.md) を参照してください。

---

## 主な機能 {#key-features}

- ✅ **標準インターフェース**: `database/sql` と完全互換
- ✅ **接続プーリング**: 接続管理を組み込みで提供
- ✅ **一括操作**: トランザクションによる効率的なバッチ挿入
- ✅ **型安全性**: 包括的な Go 型マッピング

## データ型マッピング {#data-type-mappings}

| {{{ .lake }}} | Go | 注記 |
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
| **浮動小数点型** | | |
| `FLOAT` | `float32` | |
| `DOUBLE` | `float64` | |
| **その他の型** | | |
| `DECIMAL` | `decimal.Decimal` | decimal パッケージが必要 |
| `STRING` | `string` | |
| `DATE` | `time.Time` | |
| `TIMESTAMP` | `time.Time` | |
| `ARRAY(T)` | `string` | JSON エンコード |
| `TUPLE(...)` | `string` | JSON エンコード |
| `VARIANT` | `string` | JSON エンコード |
| `BITMAP` | `string` | Base64 エンコード |

---

## 基本的な使い方 {#basic-usage}

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

## リソース {#resources}

- **GitHub Repository**: [lake-go](https://github.com/tidbcloud/lake-go)
- **Examples**: [GitHub Examples](https://github.com/tidbcloud/lake-go/tree/main/examples)