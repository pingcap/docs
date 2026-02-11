---
title: 连接到你的 TiDB Cloud Dedicated 集群
summary: 了解如何通过不同方法连接到你的 TiDB Cloud Dedicated 集群。
---

# 连接到你的 TiDB Cloud Dedicated 集群

本文介绍连接到你的 TiDB Cloud Dedicated 集群的各种方法。

> **提示：**
>
> - 如果你想了解如何连接到 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，请参阅 [Connect to Your TiDB Cloud Starter or Essential Cluster](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。
> - 本文重点介绍 TiDB Cloud Dedicated 的网络连接方法。如果你需要通过特定工具、驱动或 ORM 连接到 TiDB，请参阅 [Connect to TiDB](/develop/dev-guide-connect-to-tidb.md)。

在 TiDB Cloud 上创建 TiDB Cloud Dedicated 集群后，你可以通过以下网络连接方法之一进行连接：

- 直连

    直连使用 MySQL 原生的基于 TCP 的连接系统。你可以使用任何支持 MySQL 连接的工具连接到你的 TiDB Cloud Dedicated 集群，例如 [MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)。TiDB Cloud 还提供了 [SQL Shell](/tidb-cloud/connect-via-sql-shell.md)，可以让你快速体验 TiDB SQL、测试 TiDB 的 MySQL 兼容性，并管理用户权限。

    TiDB Cloud Dedicated 提供三种网络连接类型：

    - [公网连接](/tidb-cloud/connect-via-standard-connection.md)

        公网连接通过流量过滤器暴露一个公网端点，因此你可以通过 SQL 客户端从你的笔记本电脑连接到 TiDB 集群。你可以使用 TLS 连接到 TiDB 集群，确保应用到 TiDB 集群间数据传输的安全性。更多信息请参阅 [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md)。

    - 私有端点（推荐）

        私有端点连接为你的 VPC 内的 SQL 客户端提供一个私有端点，以安全地访问 TiDB Cloud Dedicated 集群。该方式使用不同云服务商提供的私有链路服务，能够以更高的安全性和更简化的网络管理方式实现对数据库服务的单向访问。

        - 对于托管在 AWS 上的 TiDB Cloud Dedicated 集群，私有端点连接使用 AWS PrivateLink。更多信息请参阅 [Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md)。
        - 对于托管在 Azure 上的 TiDB Cloud Dedicated 集群，私有端点连接使用 Azure Private Link。更多信息请参阅 [Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
        - 对于托管在 Google Cloud 上的 TiDB Cloud Dedicated 集群，私有端点连接使用 Google Cloud Private Service Connect。更多信息请参阅 [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

    - [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md)

        如果你需要更低的延时和更高的安全性，可以设置 VPC Peering，并通过你云账户中相应云服务商的 VM 实例使用私有端点进行连接。更多信息请参阅 [Connect to TiDB Cloud Dedicated via VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md)。

- [内置 SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)

    > **注意：**
    >
    > 如需在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上使用 SQL 编辑器，请联系 [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md)。

    如果你的集群托管在 AWS 且 TiDB 版本为 v6.5.0 或更高版本，你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/)中使用 AI 辅助的 SQL 编辑器，最大化数据价值。

    在 SQL 编辑器中，你可以手动编写 SQL 查询语句，或直接在 macOS 上按 <kbd>⌘</kbd> + <kbd>I</kbd>（或在 Windows 或 Linux 上按 <kbd>Control</kbd> + <kbd>I</kbd>），让 [Chat2Query (beta)](/tidb-cloud/tidb-cloud-glossary.md#chat2query) 自动生成 SQL 查询语句。这样你无需本地 SQL 客户端即可对数据库执行 SQL 查询。你可以直观地以表格或图表形式查看查询结果，并轻松查看查询日志。

## 后续操作

成功连接到 TiDB 集群后，你可以 [使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。