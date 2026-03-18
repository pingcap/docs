---
title: Connect to TiDB Cloud Lake Using Node.js
summary: This page describes how to connect to TiDB Cloud Lake using Node.js.
---

# Node.js Driver for Databend

The official Node.js driver providing TypeScript support and Promise-based API for modern JavaScript applications.

## Installation

```bash
npm install databend-driver
```

**Connection String**: See [Drivers Overview](./index.md#connection-string-dsn) for DSN format and connection examples.

---

## Key Features

- ✅ **TypeScript Support**: Full TypeScript definitions included
- ✅ **Promise-based API**: Modern async/await support
- ✅ **Streaming Results**: Efficient handling of large result sets
- ✅ **Connection Pooling**: Built-in connection management

## Data Type Mappings

| Databend | Node.js | Notes |
|----------|---------|-------|
| **Basic Types** | | |
| `BOOLEAN` | `boolean` | |
| `TINYINT` | `number` | |
| `SMALLINT` | `number` | |
| `INT` | `number` | |
| `BIGINT` | `number` | |
| `FLOAT` | `number` | |
| `DOUBLE` | `number` | |
| `DECIMAL` | `string` | Precision preserved |
| `STRING` | `string` | |
| **Date/Time** | | |
| `DATE` | `Date` | |
| `TIMESTAMP` | `Date` | |
| **Complex Types** | | |
| `ARRAY(T)` | `Array` | |
| `TUPLE(...)` | `Array` | |
| `MAP(K,V)` | `Object` | |
| `VARIANT` | `string` | JSON encoded |
| `BINARY` | `Buffer` | |
| `BITMAP` | `string` | Base64 encoded |

---

## Basic Usage

```javascript
const { Client } = require('databend-driver');

// Connect to Databend
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

## Resources

- **NPM Package**: [databend-driver](https://www.npmjs.com/package/databend-driver)
- **GitHub Repository**: [databend-driver](https://github.com/databendlabs/bendsql/tree/main/bindings/nodejs)
- **TypeScript Definitions**: Included in package
