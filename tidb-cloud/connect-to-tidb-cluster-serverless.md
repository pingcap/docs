---
title: 连接到你的 TiDB Cloud Starter 或 Essential 集群
summary: 了解如何通过不同方法连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。
---

# 连接到你的 TiDB Cloud Starter 或 Essential 集群

本文档介绍如何连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。

> **提示：**
>
> - 如需了解如何连接到 TiDB Cloud Dedicated 集群，请参阅 [Connect to Your TiDB Cloud Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md)。
> - 本文档重点介绍 TiDB Cloud Starter 和 TiDB Cloud Essential 的网络连接方法。如需通过特定工具、驱动或 ORM 连接到 TiDB，请参阅 [Connect to TiDB](/develop/dev-guide-connect-to-tidb.md)。

## 网络连接方法

在 TiDB Cloud 上创建 TiDB Cloud Starter 或 TiDB Cloud Essential 集群后，你可以通过以下方法之一进行连接：

- 直连

  直连指的是通过 TCP 的 MySQL 原生连接系统。你可以使用任何支持 MySQL 连接的工具连接到你的集群，例如 [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)。

- [Data Service (beta)](/tidb-cloud/data-service-overview.md)

  TiDB Cloud 提供 Data Service 功能，使你能够通过自定义 API endpoint，使用 HTTPS request 连接到托管在 AWS 上的 TiDB Cloud Starter 集群。与直连不同，Data Service 通过 RESTful API 访问你的集群数据，而不是原始 SQL。

- [Serverless Driver (beta)](/develop/serverless-driver.md)

  TiDB Cloud 为 JavaScript 提供了 serverless driver，允许你在边缘环境中以与直连相同的体验连接到 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。

在上述连接方法中，你可以根据需求选择合适的方法：

| 连接方法            | 用户界面         | 场景                                                                                                                                                       |
|--------------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 直连               | SQL/ORM          | 长时间运行的环境，如 Java、Node.js 和 Python。                                                                                                              |
| Data Service       | RESTful API      | 所有浏览器和应用交互。                                                                                                                                     |
| Serverless Driver  | SQL/ORM          | Serverless 和边缘环境，如 [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) 和 [Cloudflare Workers](https://workers.cloudflare.com/)。 |

## 网络

TiDB Cloud Starter 和 TiDB Cloud Essential 支持两种网络连接类型：

- [私有 endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)（推荐）

    私有 endpoint 连接为你的 VPC 中的 SQL client 提供一个私有 endpoint，通过 AWS PrivateLink 安全访问服务，具备高度安全性和单向访问数据库服务的能力，并简化网络管理。

- [公网 endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)

  标准连接会暴露一个公网 endpoint，因此你可以通过 SQL client 从你的笔记本电脑连接到 TiDB 集群。

  TiDB Cloud Starter 和 TiDB Cloud Essential 要求 [TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)，以确保从你的应用到 TiDB 集群的数据传输安全。

下表展示了不同连接方法可用的网络类型：

| 连接方法                  | 网络类型                   | 描述                                                                                                   |
|--------------------------|----------------------------|--------------------------------------------------------------------------------------------------------|
| 直连                     | 公网或私有 endpoint        | 直连可通过公网或私有 endpoint 进行。                                                                   |
| Data Service (beta)      | /                          | 通过 Data Service (beta) 访问托管在 AWS 上的 TiDB Cloud Starter 无需指定网络类型。                      |
| Serverless Driver (beta) | 公网 endpoint              | Serverless Driver 仅支持通过公网 endpoint 连接。                                                       |

## 后续操作

成功连接到 TiDB 集群后，你可以 [使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。