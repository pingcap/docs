---
title: 集成 TiDB Cloud 与 Airbyte
summary: 了解如何使用 Airbyte TiDB 连接器。
---

# 集成 TiDB Cloud 与 Airbyte

[Airbyte](https://airbyte.com/) 是一个开源的数据集成引擎，用于构建提取、加载、转换（ELT）数据管道，并将你的数据整合到数据仓库、数据湖和数据库中。本文档介绍了如何将 Airbyte 连接到 TiDB Cloud，作为数据源或目标端。

## 部署 Airbyte

你可以通过几个简单的步骤在本地部署 Airbyte。

1. 在你的工作环境中安装 [Docker](https://www.docker.com/products/docker-desktop)。

2. 克隆 Airbyte 源代码。

    ```shell
    git clone https://github.com/airbytehq/airbyte.git && \
    cd airbyte
    ```

3. 通过 docker-compose 运行 Docker 镜像。

    ```shell
    docker-compose up
    ```

当你看到 Airbyte 的横幅时，可以使用用户名（`airbyte`）和密码（`password`）访问 [http://localhost:8000](http://localhost:8000) 的 UI 界面。

```
airbyte-server      |     ___    _      __          __
airbyte-server      |    /   |  (_)____/ /_  __  __/ /____
airbyte-server      |   / /| | / / ___/ __ \/ / / / __/ _ \
airbyte-server      |  / ___ |/ / /  / /_/ / /_/ / /_/  __/
airbyte-server      | /_/  |_/_/_/  /_.___/\__, /\__/\___/
airbyte-server      |                     /____/
airbyte-server      | --------------------------------------
airbyte-server      |  Now ready at http://localhost:8000/
airbyte-server      | --------------------------------------
```

## 设置 TiDB 连接器

方便的是，将 TiDB 作为数据源和目标端的设置步骤是相同的。

1. 在侧边栏点击 **Sources** 或 **Destinations**，选择 TiDB 类型以创建新的 TiDB 连接器。

2. 填写以下参数。

    - Host: 你的 TiDB Cloud 集群的 endpoint
    - Port: 数据库的端口
    - Database: 你想要同步数据的数据库
    - Username: 访问数据库的用户名
    - Password: 用户名对应的密码

    你可以在集群的连接对话框中获取这些参数值。要打开该对话框，请前往你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入概览页，然后点击右上角的 **Connect**。

3. 启用 **SSL Connection**，并在 **JDBC URL Params** 中将 TLS 协议设置为 **TLSv1.2** 或 **TLSv1.3**。

    > **注意：**
    >
    > - TiDB Cloud 支持 TLS 连接。你可以在 **TLSv1.2** 和 **TLSv1.3** 中选择你的 TLS 协议，例如 `enabledTLSProtocols=TLSv1.2`。
    > - 如果你希望通过 JDBC 禁用到 TiDB Cloud 的 TLS 连接，需要在 JDBC URL Params 中专门设置 useSSL 为 `false` 并关闭 SSL 连接，例如 `useSSL=false`。
    > - {{{ .starter }}} 和 {{{ .essential }}} 仅支持 TLS 连接。

4. 点击 **Set up source** 或 **destination** 完成连接器的创建。下图展示了将 TiDB 作为数据源的配置示例。

![TiDB source configuration](/media/tidb-cloud/integration-airbyte-parameters.jpg)

你可以使用任意组合的数据源和目标端，例如 TiDB 到 Snowflake，或 CSV 文件到 TiDB。

关于 TiDB 连接器的更多细节，请参阅 [TiDB Source](https://docs.airbyte.com/integrations/sources/tidb) 和 [TiDB Destination](https://docs.airbyte.com/integrations/destinations/tidb)。

## 设置连接

在设置好数据源和目标端后，你可以构建并配置连接。

以下步骤以 TiDB 同时作为数据源和目标端为例。其他连接器可能有不同的参数。

1. 在侧边栏点击 **Connections**，然后点击 **New Connection**。
2. 选择之前建立的数据源和目标端。
3. 进入 **Set up** 连接面板，并为连接创建一个名称，例如 `${source_name} - ${destination-name}`。
4. 将 **Replication frequency** 设置为 **Every 24 hours**，表示该连接每天同步一次数据。
5. 将 **Destination Namespace** 设置为 **Custom format**，并将 **Namespace Custom Format** 设置为 **test**，以将所有数据存储在 `test` 数据库中。
6. 选择 **Sync mode** 为 **Full refresh | Overwrite**。

    > **提示：**
    >
    > TiDB 连接器同时支持 [增量同步和全量刷新同步](https://airbyte.com/blog/understanding-data-replication-modes)。
    >
    > - 在增量模式下，Airbyte 只读取自上次同步作业以来新增的源端记录。首次使用增量模式同步等同于全量刷新模式。
    > - 在全量刷新模式下，Airbyte 每次同步任务都会读取源端的所有记录并复制到目标端。你可以为 Airbyte 中每个名为 **Namespace** 的表单独设置同步模式。

    ![Set up connection](/media/tidb-cloud/integration-airbyte-connection.jpg)

7. 将 **Normalization & Transformation** 设置为 **Normalized tabular data**，以使用默认的标准化模式，或者你也可以为你的作业设置 dbt 文件。关于标准化的更多信息，请参考 [Transformations and Normalization](https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt)。
8. 点击 **Set up connection**。
9. 连接建立后，点击 **ENABLED** 激活同步任务。你也可以点击 **Sync now** 立即同步。

![Sync data](/media/tidb-cloud/integration-airbyte-sync.jpg)

## 限制

- TiDB 连接器无法使用 TiCDC 提供的变更数据捕获（CDC）功能。增量同步是基于游标机制实现的。
- 在默认标准化模式下，TiDB 目标端会将 `timestamp` 类型转换为 `varchar` 类型。这是因为 Airbyte 在传输过程中将 timestamp 类型转换为字符串，而 TiDB 不支持 `cast ('2020-07-28 14:50:15+1:00' as timestamp)`。
- 对于某些大型 ELT 任务，你需要增加 TiDB 中的 [事务限制参数](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions)。

## 参见

[使用 Airbyte 将数据从 TiDB Cloud 迁移到 Snowflake](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/)。