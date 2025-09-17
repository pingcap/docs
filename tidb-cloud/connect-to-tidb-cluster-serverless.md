---
title: 连接到你的 TiDB Cloud Starter 或 Essential 集群
summary: 了解如何通过不同方式连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。
---

# 连接到你的 TiDB Cloud Starter 或 Essential 集群

本文档介绍如何连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。

> **Tip:**
>
> 如果你想了解如何连接到 TiDB Cloud Dedicated 集群，请参见 [Connect to Your TiDB Cloud Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md)。

## 连接方式

在 TiDB Cloud 上创建好 TiDB Cloud Starter 或 TiDB Cloud Essential 集群后，你可以通过以下任一方式进行连接：

- 直连

  直连指的是通过 TCP 的 MySQL 原生连接系统。你可以使用任何支持 MySQL 连接的工具连接到你的集群，例如 [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)。

- [Data Service (beta)](/tidb-cloud/data-service-overview.md)

  TiDB Cloud 提供了 Data Service 功能，使你可以通过自定义 API 端点，使用 HTTPS 请求连接托管在 AWS 上的 TiDB Cloud Starter 集群。与直连不同，Data Service 通过 RESTful API 访问你的集群数据，而不是原始 SQL。

- [Serverless Driver (beta)](/tidb-cloud/serverless-driver.md)

  TiDB Cloud 为 JavaScript 提供了 serverless driver，允许你在边缘环境中以与直连相同的体验连接到 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。

在上述连接方式中，你可以根据需求选择合适的方式：

| 连接方式           | 用户界面         | 场景                                                                                                                                                       |
|--------------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 直连               | SQL/ORM          | 长时间运行的环境，如 Java、Node.js 和 Python。                                                                                                             |
| Data Service       | RESTful API      | 所有浏览器和应用程序交互。                                                                                                                                |
| Serverless Driver  | SQL/ORM          | Serverless 和边缘环境，如 [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/)。 |

## 网络

TiDB Cloud Starter 和 TiDB Cloud Essential 支持两种网络连接类型：

- [私有端点](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)（推荐）

    私有端点连接为你的 VPC 中的 SQL 客户端提供一个私有端点，通过 AWS PrivateLink 安全访问服务，具备高度安全性和单向访问数据库服务的能力，并简化网络管理。

- [公网端点](/tidb-cloud/connect-via-standard-connection-serverless.md)

  标准连接会暴露一个公网端点，因此你可以通过笔记本上的 SQL 客户端连接到你的 TiDB 集群。

  TiDB Cloud Starter 和 TiDB Cloud Essential 要求 [TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)，以确保从你的应用程序到 TiDB 集群的数据传输安全。

下表展示了不同连接方式可用的网络类型：

| 连接方式                  | 网络类型                  | 说明                                                                                                       |
|---------------------------|---------------------------|------------------------------------------------------------------------------------------------------------|
| 直连                      | 公网或私有端点            | 直连可以通过公网或私有端点进行。                                                                           |
| Data Service (beta)       | /                         | 通过 Data Service (beta) 访问托管在 AWS 上的 TiDB Cloud Starter 无需指定网络类型。                         |
| Serverless Driver (beta)  | 公网端点                  | Serverless Driver 仅支持通过公网端点连接。                                                                 |

## 后续操作

成功连接到你的 TiDB 集群后，你可以 [使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。