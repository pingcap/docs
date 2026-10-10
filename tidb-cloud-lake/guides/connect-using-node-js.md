---
title: Node.js を使用して TiDB Cloud Lake に接続する
summary: このページでは、Node.js を使用して TiDB Cloud Lake に接続する方法について説明します。
---

# Node.js を使用して TiDB Cloud Lake に接続する

公式の Node.js ドライバーは、TypeScript サポートと Promise ベースの API を提供し、モダンな JavaScript アプリケーションに対応しています。

## インストール {#installation}

```bash
npm install tidbcloudlake-driver
```

**Connection String**: DSN の形式と例については、[ドライバー概要](/tidb-cloud-lake/guides/driver-overview.md) を参照してください。

---

## 主な機能 {#key-features}

- ✅ **TypeScript Support**: 完全な TypeScript 定義を同梱
- ✅ **Promise-based API**: モダンな async/await をサポート
- ✅ **Streaming Results**: 大規模な結果セットを効率的に処理
- ✅ **Connection Pooling**: 組み込みの接続管理

## データ型のマッピング {#data-type-mappings}

| {{{ .lake }}} | Node.js | 注記 |
|----------|---------|-------|
| **基本型** | | |
| `BOOLEAN` | `boolean` | |
| `TINYINT` | `number` | |
| `SMALLINT` | `number` | |
| `INT` | `number` | |
| `BIGINT` | `number` | |
| `FLOAT` | `number` | |
| `DOUBLE` | `number` | |
| `DECIMAL` | `string` | 精度を保持 |
| `STRING` | `string` | |
| **日付/時刻** | | |
| `DATE` | `Date` | |
| `TIMESTAMP` | `Date` | |
| **複合型** | | |
| `ARRAY(T)` | `Array` | |
| `TUPLE(...)` | `Array` | |
| `MAP(K,V)` | `Object` | |
| `VARIANT` | `string` | JSON エンコード |
| `BINARY` | `Buffer` | |
| `BITMAP` | `string` | Base64 エンコード |

---

## 基本的な使い方 {#basic-usage}

```javascript
const { Client } = require('tidbcloudlake-driver');

// Connect to {{{ .lake }}}
const client = new Client('<your-dsn>');
const conn = await client.getConn();

// DDL: Create table
await conn.exec(`CREATE TABLE users (
    id INT,
    name STRING,
    email STRING
)`);

// Write: Insert data
await conn.exec("INSERT INTO users VALUES (?, ?, ?)", [1, "Alice", "alice@example.com"]);

// Query: Select data
const rows = await conn.queryIter("SELECT id, name, email FROM users WHERE id = ?", [1]);
for await (const row of rows) {
    console.log(row.values());
}

conn.close();
```

## リソース {#resources}

- **NPM Package**: [tidbcloudlake-driver](https://www.npmjs.com/package/tidbcloudlake-driver)
- **GitHub Repository**: [tidbcloudlake-driver](https://github.com/tidbcloud/lakesql/tree/main/bindings/nodejs)
- **TypeScript Definitions**: パッケージに含まれています