---
title: 创建您的第一个 TiDB Cloud BYOC 实例
summary: 本文档概述了创建 TiDB Cloud BYOC 实例并设置安全访问的过程。
---

# 创建您的第一个 TiDB Cloud BYOC 实例

部署 BYOC 基础设施后，创建资源池，在资源池中创建您的第一个 {{{ .byoc }}} 实例，并配置安全的管理访问。

## 创建 BYOC 实例 {#create-a-byoc-instance}

现在，您可以直接通过 TiDB Cloud 控制台预配资源池和 TiDB 实例。

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，然后按照[创建资源池](/tidb-cloud/byoc/create-resource-pool-byoc.md)中的说明，在目标云服务商和 region 中创建资源池。

    >**Note:**
    >
    > 创建资源池时，请根据您的工作负载需求选择 **Zonal** 或 **Regional** 高可用。 在该资源池中创建或恢复的 {{{ .byoc }}} 实例会继承资源池的高可用模式。

2. 资源池变为 **Active** 后，按照[创建 {{{ .byoc }}} 实例](/tidb-cloud/byoc/create-tidb-instance-byoc.md)中的说明，在资源池中创建一个新实例。

    * 初始设置时间：在某个 region 中创建**第一个资源池**时，系统需要初始化 Kubernetes 环境，因此可能大约需要 **1 小时**。
    * 后续实例：在处于活动状态的资源池中创建其他实例通常只需要几分钟。

3. 请与您的 TiDB Cloud 代表沟通，以确定适合初始连通性和功能测试的 Request Unit (RU) 设置。他们会根据您的具体测试需求推荐相应的配置。

## 从 Amazon S3 恢复数据到新的 BYOC 实例 {#restore-data-from-amazon-s3-to-a-new-byoc-instance}

在 Amazon S3 中准备好备份文件后，您可以将数据恢复到活动资源池中的新 {{{ .byoc }}} 实例。

1. 配置 Amazon S3 访问（AK/SK）。

    为了让 TiDB Cloud 能够读取您的 S3 备份，您必须通过生成具有适当 S3 读权限的 AWS Access Key ID 和 Secret Access Key（AK/SK）来配置外部存储访问。

    有关详细说明，请参见[使用 AWS Access Key 配置 Amazon S3 访问](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access-using-an-aws-access-key)。

2. 执行恢复过程。

    配置好访问密钥后，您可以从 TiDB Cloud 控制台发起恢复作业。

    在恢复过程中，请在目标云服务商和 region 中选择一个具有足够 vCPU 容量的活动资源池。恢复后的实例会继承所选资源池的高可用模式。

    如果所选资源池已达到其 Pool vCPU Limit，请先提高或关闭该限制，或者选择另一个资源池后再继续。这是因为恢复到新的 {{{ .byoc }}} 实例可能会导致已预配的 vCPU 总数超过 Pool vCPU Limit，并影响同一资源池中所有 {{{ .byoc }}} 实例的性能。

    有关逐步恢复操作，请参见[从云存储恢复备份](/tidb-cloud/premium/backup-and-restore-premium.md#restore-backups-from-cloud-storage)。

## 配置安全的管理访问 {#configure-secure-administrative-access}

为了让 TiDB Cloud Support 能够协助进行故障排查和可观测性相关工作，您可以通过在 VPC 内部署加固的堡垒机主机来配置安全访问通道。

> **Note:**
>
> - 此步骤是**可选的**。您也可以选择提供自己的安全登录方式用于维护。
> - Bastion Host 仅用于故障排查，不需要保持持久连接。您可以随时终止此通道。

有关部署和验证步骤，请参见[为 {{{ .byoc }}} 配置 Bastion Host](/tidb-cloud/byoc/byoc-configure-bastion-host.md)。

## 接下来做什么 {#what-s-next}

创建第一个资源池和 {{{ .byoc }}} 实例并配置安全的管理访问后，请继续阅读 [TiDB Cloud BYOC 联合验证](/tidb-cloud/byoc/joint-validation.md)，以验证连通性、可观测性、安全性和告警。