---
title: 使用 Node.js 连接 TiDB Cloud Lake
summary: 本页介绍如何使用 Node.js 连接 TiDB Cloud Lake。
---

# 使用 Node.js 连接 TiDB Cloud Lake

官方 Node.js 驱动为现代 JavaScript 应用提供 TypeScript 支持和基于 Promise 的 API。

## 安装 {#installation}

```bash
npm install tidbcloudlake-driver
```

**Connection String**：有关 DSN 格式和示例，请参见[驱动概览](/tidb-cloud-lake/guides/driver-overview.md)。

---

## 主要特性 {#key-features}

- ✅ **TypeScript Support**：包含完整的 TypeScript 定义
- ✅ **Promise-based API**：支持现代 async/await
- ✅ **Streaming Results**：高效处理大型结果集
- ✅ **Connection Pooling**：内置连接管理

## 数据类型映射 {#data-type-mappings}

| {{{ .lake }}} | Node.js | 说明 |
|----------|---------|-------|
| **基本类型** | | |
| `BOOLEAN` | `boolean` | |
| `TINYINT` | `number` | |
| `SMALLINT` | `number` | |
| `INT` | `number` | |
| `BIGINT` | `number` | |
| `FLOAT` | `number` | |
| `DOUBLE` | `number` | |
| `DECIMAL` | `string` | 保留精度 |
| `STRING` | `string` | |
| **日期/时间** | | |
| `DATE` | `Date` | |
| `TIMESTAMP` | `Date` | |
| **复杂类型** | | |
| `ARRAY(T)` | `Array` | |
| `TUPLE(...)` | `Array` | |
| `MAP(K,V)` | `Object` | |
| `VARIANT` | `string` | JSON 编码 |
| `BINARY` | `Buffer` | |
| `BITMAP` | `string` | Base64 编码 |

---

## 基本用法 {#basic-usage}

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

## 资源 {#resources}

- **NPM Package**：[tidbcloudlake-driver](https://www.npmjs.com/package/tidbcloudlake-driver)
- **GitHub Repository**：[tidbcloudlake-driver](https://github.com/tidbcloud/lakesql/tree/main/bindings/nodejs)
- **TypeScript Definitions**：包中已包含