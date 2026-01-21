---
title: Changefeed（Beta）
summary: TiDB Cloud changefeed 帮助你将数据从 TiDB Cloud 流式传输到其他数据服务。
---

# Changefeed（Beta）

TiDB Cloud changefeed 帮助你将数据从 TiDB Cloud 流式传输到其他数据服务。目前，TiDB Cloud 支持将数据流式传输到 Apache Kafka 和 MySQL。

> **注意：**
>
> - 目前，TiDB Cloud 每个 TiDB Cloud Essential 集群最多只允许创建 10 个 changefeed。
> - 对于 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群，changefeed 功能不可用。

## 支持的区域

changefeed 功能目前在以下区域可用：

| 云服务商 | 支持的区域 |
| --- | --- |
| AWS          | <ul><li>`ap-southeast-1`</li><li>`eu-central-1`</li><li>`us-east-1`</li><li>`us-west-2`</li></ul> |
| 阿里云 | <ul><li>`ap-southeast-1`</li><li>`ap-southeast-5`</li><li>`cn-hongkong`</li></ul> |

未来将支持更多区域。如果你需要在特定区域立即获得支持，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 查看 Changefeed 页面

要访问 changefeed 功能，请按照以下步骤操作：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，并进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏点击 **Data** > **Changefeed**。此时会显示 changefeed 页面。

在 **Changefeed** 页面，你可以创建 changefeed，查看已有 changefeed 列表，并对已有 changefeed 进行操作（如暂停、恢复、编辑和删除 changefeed）。

## 创建 changefeed

要创建 changefeed，请参考以下教程：

- [Sink to Apache Kafka](/tidb-cloud/essential-changefeed-sink-to-kafka.md)
- [Sink to MySQL](/tidb-cloud/essential-changefeed-sink-to-mysql.md)

## 查看 changefeed

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 查看 changefeed。

<SimpleTab>
<div label="Console">

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要查看的 changefeed，在 **Action** 列点击 **...** > **View**。
3. 你可以查看 changefeed 的详细信息，包括其配置、状态和统计/指标（信息）。

</div>

<div label="CLI">

运行以下命令：

```bash
ticloud serverless changefeed get --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

</div>
</SimpleTab>

## 暂停或恢复 changefeed

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 暂停或恢复 changefeed。

<SimpleTab>
<div label="Console">

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要暂停或恢复的 changefeed，在 **Action** 列点击 **...** > **Pause/Resume**。

</div>

<div label="CLI">

要暂停 changefeed，运行以下命令：

```bash
ticloud serverless changefeed pause --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

要恢复 changefeed：

```
ticloud serverless changefeed resume -c <cluster-id> --changefeed-id <changefeed-id>
```

</div>
</SimpleTab>

## 编辑 changefeed

> **注意：**
>
> TiDB Cloud 目前仅允许在 changefeed 处于暂停状态时进行编辑。

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 编辑 changefeed。

<SimpleTab>
<div label="Console">

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要暂停的 changefeed，在 **Action** 列点击 **...** > **Pause**。
3. 当 changefeed 状态变为 `Paused` 后，点击 **...** > **Edit** 以编辑对应的 changefeed。

    TiDB Cloud 默认会填充 changefeed 配置。你可以修改以下配置项：

    - Apache Kafka sink：除 **Destination**、**Connection** 和 **Start Position** 外的所有配置
    - MySQL sink：除 **Destination**、**Connection** 和 **Start Position** 外的所有配置

4. 编辑配置后，点击 **...** > **Resume** 以恢复对应的 changefeed。

</div>

<div label="CLI">

编辑 Apache Kafka sink 的 changefeed：

```bash
ticloud serverless changefeed edit --cluster-id <cluster-id> --changefeed-id <changefeed-id> --name <new-displayName> --kafka <full-specified-kafka> --filter <full-specified-filter>
```

编辑 MySQL sink 的 changefeed：

```bash
ticloud serverless changefeed edit --cluster-id <cluster-id> --changefeed-id <changefeed-id> --name <new-displayName> --mysql <full-specified-mysql> --filter <full-specified-filter>
```

</div>
</SimpleTab>

## 复制 changefeed

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要复制的 changefeed，在 **Action** 列点击 **...** > **Duplicate**。
3. TiDB Cloud 会自动用原有设置填充新的 changefeed 配置。你可以根据需要查看并修改配置。
4. 确认配置后，点击 **Submit** 以创建并启动新的 changefeed。

## 删除 changefeed

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 删除 changefeed。

<SimpleTab>
<div label="Console">

1. 进入目标 TiDB 集群的 [**Changefeed**](#view-the-changefeed-page) 页面。
2. 找到你想要删除的 changefeed，在 **Action** 列点击 **...** > **Delete**。

</div>

<div label="CLI">

运行以下命令：

```bash
ticloud serverless changefeed delete --cluster-id <cluster-id> --changefeed-id <changefeed-id>
```

</div>
</SimpleTab>

## Changefeed 计费

changefeed 在 beta 阶段免费。

## Changefeed 状态

在运行过程中，changefeed 可能因错误而失败，或被手动暂停或恢复。这些操作会导致 changefeed 状态发生变化。

各状态说明如下：

- `CREATING`：changefeed 正在创建中。
- `CREATE_FAILED`：changefeed 创建失败。你需要删除该 changefeed 并重新创建。
- `RUNNING`：changefeed 正常运行，checkpoint-ts 正常推进。
- `PAUSED`：changefeed 已暂停。
- `WARNING`：changefeed 返回警告。由于某些可恢复的错误，changefeed 无法继续。处于该状态的 changefeed 会持续尝试恢复，直到状态变为 `RUNNING`。该状态下的 changefeed 会阻塞 [GC 操作](https://docs.pingcap.com/tidb/stable/garbage-collection-overview)。
- `RUNNING_FAILED`：changefeed 运行失败。由于某些错误，changefeed 无法恢复且无法自动修复。如果在增量数据的垃圾回收（GC）之前解决了问题，你可以手动恢复失败的 changefeed。增量数据的默认生存时间（TTL）为 24 小时，即 changefeed 中断后 24 小时内 GC 机制不会删除任何数据。