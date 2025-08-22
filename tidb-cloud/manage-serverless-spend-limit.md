---
title: 管理 TiDB Cloud Serverless 可扩展集群的消费限额
summary: 了解如何管理 TiDB Cloud Serverless 可扩展集群的消费限额。
---

# 管理 TiDB Cloud Serverless 可扩展集群的消费限额

> **Note:**
>
> 消费限额仅适用于 TiDB Cloud Serverless [scalable clusters](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)。

消费限额是指你每月愿意为某个特定工作负载支付的最大金额。它是一种成本控制机制，允许你为 TiDB Cloud Serverless 可扩展集群设置预算。

在 TiDB Cloud 的每个组织中，默认最多可以创建 5 个 [free clusters](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)。如果你需要创建更多的 TiDB Cloud Serverless 集群，则需要添加信用卡并创建可扩展集群以进行使用。但如果你在创建更多集群之前删除了一些已有集群，则新集群仍然可以在无需信用卡的情况下创建。

## 使用配额

对于你所在组织的前 5 个 TiDB Cloud Serverless 集群，无论是免费集群还是可扩展集群，TiDB Cloud 都为每个集群提供如下免费使用配额：

- 行存储：5 GiB
- 列存储：5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)：每月 5000 万 RU

一旦某个集群达到其使用配额，将会立即拒绝任何新的连接尝试，直到你 [增加配额](#update-spending-limit) 或新月开始时用量被重置。已在达到配额前建立的连接会保持活跃，但会受到限流。例如，当免费集群的行存储超过 5 GiB 时，该集群会自动限制任何新的连接尝试。

如需了解不同资源（包括读、写、SQL CPU 和网络出口）的 RU 消耗、定价详情以及限流信息，请参见 [TiDB Cloud Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

如果你希望创建一个拥有额外配额的 TiDB Cloud Serverless 集群，可以在集群创建页面编辑消费限额。更多信息请参见 [Create a TiDB Cloud Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md)。

## 更新消费限额

对于 TiDB Cloud Serverless 免费集群，你可以通过升级为可扩展集群来提升使用配额。对于已有的可扩展集群，你可以直接调整每月消费限额。

要为 TiDB Cloud Serverless 集群更新消费限额，请执行以下步骤：

1. 在项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在 **Usage This Month** 区域，点击 **Upgrade to Scalable Cluster**。

    若要调整已有可扩展集群的消费限额，点击 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Edit**。

3. 根据需要编辑每月消费限额。如果你尚未添加支付方式，编辑限额后需要添加信用卡。
4. 点击 **Update Cluster Plan**。