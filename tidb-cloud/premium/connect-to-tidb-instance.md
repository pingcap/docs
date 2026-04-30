---
title: 连接到你的 {{{ .premium }}} 实例
summary: 了解如何通过不同方法连接到你的 {{{ .premium }}} 实例。
---

# 连接到你的 {{{ .premium }}} 实例

本文档介绍如何连接到你的 {{{ .premium }}} 实例。

> **提示：**
>
> 如需了解如何连接到 TiDB Cloud Dedicated 集群，请参见[连接到你的 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-to-tidb-cluster.md)。

## 连接方法 {#connection-methods}

在你的 {{{ .premium }}} 实例于 TiDB Cloud 上创建完成后，你可以通过直连进行连接。

直连是指基于 TCP 的 MySQL 原生连接系统。你可以使用任何支持 MySQL 连接的工具连接到你的实例，例如 [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)。

| Connection method  | User interface     | Scenario                                                                                                                                                       |
|--------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Direct connections | SQL/ORM            | 长时间运行的环境，例如 Java、Node.js 和 Python。                                                                                                               |

## 网络 {#network}

{{{ .premium }}} 提供两种网络连接类型：

- [Private endpoint](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)（推荐）

    Private endpoint 连接提供一个私有端点，使你的 VPC 中的 SQL 客户端能够通过 AWS PrivateLink 安全地访问服务。AWS PrivateLink 为数据库服务提供高安全性和单向访问，并简化网络管理。

- [Public endpoint](/tidb-cloud/premium/connect-to-premium-via-public-connection.md)

    标准连接会暴露一个公共端点，因此你可以通过笔记本电脑上的 SQL 客户端连接到你的 {{{ .premium }}} 实例。

<!-- To ensure the security of data transmission, you need to [establish a TLS connection](/tidb-cloud/premium/tidb-cloud-tls-connect-to-premium.md) from your client to your instance. -->

下表显示了你可以使用的网络：

| Connection method          | Network                      | Description                                                                                                       |
|----------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Direct connections         | Public or private endpoint   | 可以通过公共端点和私有端点进行直连。                                                                              |

## 接下来做什么 {#what-s-next}

成功连接到你的 {{{ .premium }}} 实例后，你可以[使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。