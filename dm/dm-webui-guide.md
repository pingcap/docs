---
title: Use WebUI to manage DM migration tasks.
summary: Learn how to use WebUI to manage DM migration tasks.
---

# 使用 WebUI 管理 DM 迁移任务
# Use WebUI to manage DM migration tasks

DM WebUI 是一个 TiDB Data Migration (DM) 迁移任务管理界面，方便用户以直观的方式管理大量迁移任务，无需使用 dmctl 命令行，简化任务管理的操作步骤。

DM WebUI is web-based GUI management platform for TiDB Data Migration (DM) tasks. It provides a simple and intuitive way to manage a large number of migration tasks, without using the dmctl command line.

本文档介绍 DM WebUI 的访问方式、使用前提、各界面的使用场景以及注意事项。

This document introduces how to access DM WebUI, the prerequisites, the use cases of each interface, and the attention points.

> **Warning:**
>
> - DM WebUI 当前为实验特性，不建议在生产环境中使用。
> - DM WebUI is currently an experimental feature, it is not recommended to use it in the production environment.
> - DM WebUI 中 `task` 的生命周期有所改变，不建议与 dmctl 同时使用。
> - The lifecycle of `task` in DM WebUI has changed, and it is not recommended to use DM WebUI and dmctl at the same time.

DM WebUI 主要包含以下界面：

DM WebUI has the following interfaces:

- **Dashboard**：提供迁移任务运行状态的监控视图。
- **数据迁移**
    - **任务列表**：提供创建迁移任务的界面入口，并展示各迁移任务的详细信息。
    - **上游配置**：用户在此页面配置同步任务的上游数据源信息。
    - **同步详情**：展示更加详细的任务状态信息。
- **集群管理**
    - **成员列表**：展示 DM 集群中所有的 master 和 worker 节点，以及 worker 节点与 source 的绑定关系。

- **Dashboard**: Provides the monitoring view of the migration task statuses.
- **Migration**
    - **Task**: Provides the interface to create a migration task, and displays the detailed information of each migration task.
    - **Source**: Configures the upstream data source information for a migration task.
    - **Replication Detail**: Displays the detailed status information of migration tasks.
- **Cluster**
    - **Members**: Displays the list of all master and worker nodes in the DM cluster, and the binding relationship between worker nodes and the source.

界面示例如下：
The interface is as follows:

![webui](/media/dm/dm-webui-preview-en.png)

## 访问方式
## Access Method

你可以从 DM 集群的任意 master 节点访问 DM WebUI，访问端口与 DM OpenAPI 保持一致，默认为 `8261`。访问地址示例：`http://{master_ip}:{master_port}/dashboard/`。
You can access DM WebUI from any master node of the DM cluster. The access port is `8261` by default and is the same as that of DM OpenAPI. An example pf an access address: `http://{master_ip}:{master_port}/dashboard/`.

## 使用前提
## Prerequisites

为确保 DM WebUI 能正常显示，在使用 DM WebUI 前，确保以下操作或配置已完成：
To ensure that DM WebUI can be displayed properly, before using DM WebUI, make sure that the following operations or configuration have been completed:

+ 开启 DM OpenAPI 配置
+ Enable the DM OpenAPI configuration:

    - 如果你的 DM 集群是通过二进制方式部署的，在该 master 节点的配置中开启 `openapi` 配置项：
    - If your DM cluster is deployed using binary, enable the `openapi` configuration item in the configuration of the master node:

        ```
        openapi = true
        ```

    - 如果你的 DM 集群是通过 TiUP 部署的，在拓扑文件中添加如下配置：
    - If your DM cluster is deployed using TiUP, add the following configuration to the topology file:

        ```yaml
        server_configs:
          master:
            openapi: true
        ```

+ 首次部署 Grafana 时，已正确安装监控相关组件：`monitoring_servers` 和 `grafana_servers`。`grafana_servers` 须按如下进行配置：
+ When deploying Grafana for the first time, make sure that the `monitoring_servers` and `grafana_servers` monitoring components have been correctly installed. `grafana_servers` must be configured as follows:

    ```
    grafana_servers:
      - host: 10.0.1.14
        # port: 3000
        # deploy_dir: /tidb-deploy/grafana-3000
        config:       # 请确保 tiup dm -v 版本在 v1.9.0 以上
          auth.anonymous.enabled: true
          security.allow_embedding: true
    ```

    若 `grafana_servers` 使用了非默认的 IP 和端口，则需要在 WebUI 的 **Dashboard** 界面填写正确的 IP 和端口。
    If the IP and port of `grafana_servers` are not the default ones, you need to fill in the correct IP and port in the **Dashboard** interface.

+ 如果你的 DM 集群是从旧版本升级的，则需要手动修改 Grafana 的配置：
+ If your DM cluster is upgraded from an old version, you need to manually modify the Grafana configuration:

    1. 编辑 `/{deploy-dir}/grafana-{port}/conf/grafana.ini` 文件，按如下所示修改两个配置项：
    1. Edit the `/{deploy-dir}/grafana-{port}/conf/grafana.ini` file as follows:

        ```ini
        [auth.anonymous]
        enabled = true

        [security]
        allow_embedding = true
        ```

    2. 执行 `tiup dm reload` 使新的配置生效。
    2. Run `tiup dm reload` to make the new configuration effective.

## Dashboard
## Dashboard

要查看迁移任务的监控，你可访问 **Dashboard** 页面。**Dashboard** 是内嵌了 DM 的 Grafana Dashboard，包含 `Standard` 和 `Professional` 两个视图，分别从标准角度展现监控信息，和从更专业的角度展现更详细的监控信息。
To see the monitoring of migration tasks, visit the **Dashboard** page. **Dashboard** is an embedded Grafana Dashboard that contains `Standard` and `Professional` views, each of which displays monitoring information from a standard perspective, or from a more professional perspective.

## 数据迁移
## Migration

**数据迁移**包含**上游配置**、**任务列表**、**同步详情**三个界面。
**Migration** includes **Source**, **Task**, and **Replication Detail** pages.

## 上游配置
## Source

创建迁移任务之前，你需要先创建同步任务的上游数据源信息。你可在**上游配置**页面创建上游任务的配置。创建时，请注意以下事项：
Before creating a migration task, you need to create the data source information of the upstream for the replication task. You can create the upstream task configuration in the **Source** page. When creating tasks, pay attention to the following items:

- 如果存在主从切换，请务必在上游 MySQL 开启 GTID，并在创建上游配置时将 GTID 设为 `True`，否则数据迁移任务将在主从切换时中断（AWS Aurora 除外）。
- If there is a switch between primary and secondary node, enable GTID in the upstream MySQL and set GTID to `True` when creating the upstream configuration; otherwise, the migration task will be interrupted during the switch (except for AWS Aurora).
- 若某个上游数据库需要临时下线，可将其“停用”，但停用期间其他正在同步的 MySQL 实例不可执行 DDL 操作，否则停用的实例被启用后将无法正常同步。
- If a MySQL instance needs to be temporarily made offline, you can disable the instance. However, when the MySQL instance is being disabled, other MySQL instances running migration tasks cannot execute DDL operations; otherwise, the disabled instance cannot properly migrate data after it is enabled.
- 当多个迁移任务使用同一个上游时，可能对其造成额外压力。开启 relay log 可降低对上游的影响，建议开启 relay log。
- When multiple migration tasks use the same upstream, it might cause additional stress. Enabling relay log can reduce the impact on the upstream, and it is recommended to enable relay log.

### 任务列表
### Task

你可通过**任务列表**界面查看迁移任务详情，并创建迁移任务。
You can view the migration task details in the **Task** page, and create migration tasks.

#### 查看迁移任务详情
#### View migration task details

在任务列表中，点击任务名称，详情页面会从右侧滑出。详情页面展示了更加详细的任务状态信息。在信息详情页面，你可以查看每一个子任务的运行情况，以及此迁移任务当前完整的配置项信息。
In the task list, click the task name to view the details page from the right. The details page displays more detailed task status information. In the details page, you can view the status of each sub-task and the current configuration information of the migration task.

在 DM 中，迁移任务中的每一个子任务可能处于不同的阶段，即全量导出 (dump) -> 全量导入 (load) -> 增量同步 (sync)。因此任务的当前阶段以子任务所处阶段的统计信息来展示，可以更加清楚的了解任务运行情况。
In DM, each sub-task of a migration task might be in different stages, namely full dump -> full import (load) -> incremental replication (sync). Therefore, the statistics of a task status and the sub-task statuses can help you better understand the running status of the task.

#### 创建迁移任务
#### Create migration tasks

要在该界面创建任务，点击右上角的**添加**按钮即可。创建迁移任务时，你可以使用以下任一方式：
To create a migration task on this page, click the **Add** button on the top right corner. You can use one of the following methods to create a migration task:

- 通过向导方式。通过 WebUI 根据指引一步步填写所需信息进行任务创建，此种方式比较适合入门级用户及日常使用。
- By following the WebUI instruction. Fill in the required information step by step on the WebUI, and this method is suitable for beginners and for daily use.
- 通过配置文件。通过直接粘贴或编写 JSON 格式的任务配置文件进行创建，支持更多的参数调整，适合熟练的用户使用。
- By using configuration file. Paste or write a JSON-formatted configuration file to create a migration task. This method support adjusting more parameters and is suitable for more advanced users.

## 同步详情
## Replication detail

你可以通过**同步详情**页面查看迁移任务中所配置迁移规则的运行情况。同步详情页面支持根据任务、数据源、表库名称进行查询。
You can view the status of the migration rules configured for a migration task on the **Replication Detail** page. This page supports querying by task, source, and database name.

查询结果中包含上游表至下游表的对应信息，因此请慎重使用 `.*` 等，以防止查询结果过多导致页面反应迟缓。
The query result contains the corresponding information of the upstream table and the downstream table, so be careful using `.*` in case that too many query results slow down the page response.

## 集群管理
## Cluster

### 成员列表
### Members

**成员列表**页面展示 DM 集群中所有的 master 和 worker 节点，以及 worker 节点与 source 的绑定关系。你可在此页面对 master 和 worker 节点执行简单的 online 或 offline 操作。
The **Members** page displays all the master and worker nodes in the DM cluster, and the binding relationship between worker nodes and the source. You can perform simple online or offline operations on master and worker nodes on this page.
