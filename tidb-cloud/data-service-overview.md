---
title: TiDB Cloud Data Service (Beta) Overview
summary: 了解 TiDB Cloud 中的 Data Service 及其应用场景。
---

# TiDB Cloud Data Service (Beta) 概述

TiDB Cloud [Data Service (beta)](https://tidbcloud.com/project/data-service) 是一款全托管的低代码后端即服务（BaaS）解决方案，简化了后端应用开发，帮助开发者快速构建高可扩展性、安全、数据驱动的应用。

Data Service 允许你通过自定义 API 端点，以 HTTPS 请求的方式访问 TiDB Cloud 数据。该功能采用无服务器架构，自动处理计算资源和弹性扩展，因此你只需专注于端点中的查询逻辑，无需担心基础设施或运维成本。

> **注意：**
>
> Data Service 仅适用于托管在 AWS 上的 TiDB Cloud Starter。如需在 TiDB Cloud Dedicated 集群中使用 Data Service，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

Data Service 中的端点是你可以自定义以执行 SQL 语句的 Web API。你可以为 SQL 语句指定参数，例如 `WHERE` 子句中使用的值。当客户端调用端点并在请求 URL 中提供参数值时，端点会使用所提供的参数执行相应的 SQL 语句，并将结果作为 HTTP 响应的一部分返回。

为了更高效地管理端点，你可以使用 Data App。Data Service 中的 Data App 是一组端点的集合，你可以用它来访问特定应用的数据。通过创建 Data App，你可以对端点进行分组，并通过 API key 配置授权设置以限制对端点的访问。这样可以确保只有授权用户才能访问和操作你的数据，从而提升应用的安全性。

> **提示：**
>
> TiDB Cloud 为 TiDB 集群提供了 Chat2Query API。启用后，TiDB Cloud 会自动创建一个名为 **Chat2Query** 的系统 Data App 以及一个 Chat2Data 端点在 Data Service 中。你可以调用该端点，通过提供指令让 AI 生成并执行 SQL 语句。
>
> 详细信息请参见 [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

## 应用场景

Data Service 允许你将 TiDB Cloud 无缝集成到任何兼容 HTTPS 的应用或服务中。以下是一些典型的使用场景：

- 直接从移动端或 Web 应用访问 TiDB 集群的数据库。
- 使用无服务器边缘函数调用端点，避免因数据库连接池导致的可扩展性问题。
- 通过将 Data Service 作为数据源，将 TiDB Cloud 集成到数据可视化项目中。这样可以避免暴露数据库连接的用户名和密码，使 API 更安全且更易用。
- 从不支持 MySQL 接口的环境连接数据库，为你访问数据提供更多灵活性和选择。

## 后续步骤

- [Get Started with Data Service](/tidb-cloud/data-service-get-started.md)
- [Get Started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)
- [Manage a Data App](/tidb-cloud/data-service-manage-data-app.md)
- [Manage an Endpoint](/tidb-cloud/data-service-manage-endpoint.md)
