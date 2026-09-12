---
title: 使用驱动连接 TiDB Cloud Lake
summary: 可用于连接 TiDB Cloud Lake 的官方驱动概览。
---

# 使用驱动连接 TiDB Cloud Lake

{{{ .lake }}} 为多种编程语言提供了官方驱动，使你能够从应用程序连接到 {{{ .lake }}} 并与之交互。

## 快速开始 {#quick-start}

1. **选择你的语言** - 可从 Python、Go、Node.js、Java 或 Rust 中选择
2. **获取连接字符串** - 使用下面的 DSN 格式
3. **安装并连接** - 按照对应驱动的文档进行操作

## 连接字符串（DSN） {#connection-string-dsn}

所有 {{{ .lake }}} 驱动都使用相同的 DSN（Data Source Name）格式：

```
lake://user:pwd@host[:port]/[database][?sslmode=disable][&arg1=value1]
```

> **注意：**
>
> `user:pwd` 指的是 {{{ .lake }}} 中的 SQL 用户。请参见 [CREATE USER](/tidb-cloud-lake/sql/create-user.md) 以创建用户并授予权限。

### 连接示例 {#connection-examples}

| 部署         | 连接字符串                                        |
| ------------------ | -------------------------------------------------------- |
| **{{{ .lake }}}** | `lake://user:pwd@host:443/database?warehouse=wh`     |

### 参数参考 {#parameters-reference}

| 参数   | 描述    | {{{ .lake }}}  | 示例                 |
| ----------- | -------------- | -------------- | ----------------------- |
| `sslmode`   | SSL 模式       | 不使用         | `?sslmode=disable`      |
| `warehouse` | 计算集群名称   | 必填           | `?warehouse=compute_wh` |

> **{{{ .lake }}}**：[获取连接信息 →](/tidb-cloud-lake/guides/warehouse.md#obtaining-connection-information)

## 可用驱动 {#available-drivers}

| 语言                | 软件包                                     | 关键特性                                                                  |
| ----------------------- | ------------------------------------------- | ----------------------------------------------------------------------------- |
| **[Python](/tidb-cloud-lake/guides/connect-using-python.md)**  | `tidbcloudlake-driver`<br/>`lake-sqlalchemy` | • 支持同步/异步<br/>• SQLAlchemy 方言<br/>• 兼容 PEP 249        |
| **[Go](/tidb-cloud-lake/guides/connect-using-golang.md)**      | `lake-go`                               | • database/sql 接口<br/>• 连接池<br/>• 批量操作       |
| **[Node.js](/tidb-cloud-lake/guides/connect-using-node-js.md)** | `tidbcloudlake-driver`                           | • TypeScript 支持<br/>• 基于 Promise 的 API<br/>• 流式结果          |
| **[Java](/tidb-cloud-lake/guides/connect-using-java.md)**      | `lake-jdbc`                             | • 兼容 JDBC 4.0<br/>• 连接池<br/>• 预处理语句      |
| **[Rust](/tidb-cloud-lake/guides/connect-using-rust.md)**      | `lake-driver`                           | • 支持 Async/await<br/>• 类型安全查询<br/>• 零拷贝反序列化 |
