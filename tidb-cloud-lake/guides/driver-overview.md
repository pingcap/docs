---
title: Connect to TiDB Cloud Lake Using Drivers
summary: An overview of the official drivers available for connecting to TiDB Cloud Lake.
---

# Connect to TiDB Cloud Lake Using Drivers

{{{ .lake }}} provides official drivers for multiple programming languages, enabling you to connect and interact with {{{ .lake }}} from your applications.

## Quick Start

1. **Choose your language** - Select from Python, Go, Node.js, Java, or Rust
2. **Get your connection string** - Use the DSN format below
3. **Install and connect** - Follow the driver-specific documentation

## Connection String (DSN)

All {{{ .lake }}} drivers use the same DSN (Data Source Name) format:

```
lake://user:pwd@host[:port]/[database][?sslmode=disable][&arg1=value1]
```

> **Note:**
>
> The `user:pwd` refers to SQL users in {{{ .lake }}}. See [CREATE USER](/tidb-cloud-lake/sql/create-user.md) to create users and grant privileges.

### Connection Examples

| Deployment         | Connection String                                        |
| ------------------ | -------------------------------------------------------- |
| **{{{ .lake }}}** | `lake://user:pwd@host:443/database?warehouse=wh`     |

### Parameters Reference

| Parameter   | Description    | {{{ .lake }}}  | Example                 |
| ----------- | -------------- | -------------- | ----------------------- |
| `sslmode`   | SSL mode       | Not used       | `?sslmode=disable`      |
| `warehouse` | Warehouse name | Required       | `?warehouse=compute_wh` |

> **{{{ .lake }}}**: [Get connection info →](/tidb-cloud-lake/guides/warehouse.md#obtaining-connection-information)

## Available Drivers

| Language                | Package                                     | Key Features                                                                  |
| ----------------------- | ------------------------------------------- | ----------------------------------------------------------------------------- |
| **[Python](/tidb-cloud-lake/guides/connect-using-python.md)**  | `databend-driver`<br/>`databend-sqlalchemy` | • Sync/async support<br/>• SQLAlchemy dialect<br/>• PEP 249 compatible        |
| **[Go](/tidb-cloud-lake/guides/connect-using-golang.md)**      | `databend-go`                               | • database/sql interface<br/>• Connection pooling<br/>• Bulk operations       |
| **[Node.js](/tidb-cloud-lake/guides/connect-using-node-js.md)** | `databend-driver`                           | • TypeScript support<br/>• Promise-based API<br/>• Streaming results          |
| **[Java](/tidb-cloud-lake/guides/connect-using-java.md)**      | `databend-jdbc`                             | • JDBC 4.0 compatible<br/>• Connection pooling<br/>• Prepared statements      |
| **[Rust](/tidb-cloud-lake/guides/connect-using-rust.md)**      | `databend-driver`                           | • Async/await support<br/>• Type-safe queries<br/>• Zero-copy deserialization |
