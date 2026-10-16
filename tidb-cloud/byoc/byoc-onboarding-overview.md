---
title: TiDB Cloud BYOC 入门概览
summary: 概述 TiDB Cloud BYOC 入门流程，详细说明客户和 TiDB Cloud 团队各自的职责与步骤。
---

# TiDB Cloud BYOC 入门概览

TiDB Cloud BYOC（Bring Your Own Cloud）是一种企业级解决方案，让您在自己的云环境中运行数据面，同时保留 TiDB Cloud 的全托管体验。

TiDB Cloud BYOC 的部署流程需要您的组织与 TiDB Cloud 团队协作完成。该流程包括安全的基础设施准备、自动化资源配置以及全面验证。要开始 BYOC 入门流程，请[联系销售](https://www.pingcap.com/contact-us/)。

<!--TO confirm: might need to state that currently only AWS is supported and the word AWS is not used in title for future content scale.-->

## 部署阶段 {#deployment-phases}

| 阶段 | 责任方 | 描述 |
| :---- | :---- | :---- |
| [阶段 1：环境准备](/tidb-cloud/byoc/byoc-prepare-environment-aws.md) | 客户 | 准备部署所需的 AWS 基础环境。这包括创建专用的 AWS 账户、为 TiDB 配置公有或私有的 Route 53 托管区域，以及设置私有证书颁发机构（PCA）。 |
| [阶段 2：IAM 引导程序](/tidb-cloud/byoc/byoc-configure-iam-permissions.md) | 客户 | 执行提供的引导程序脚本，以安装所需的 IAM 角色和策略。这将授予 TiDB Cloud 控制面安全管理您 AWS 账户内资源的权限。 |
| [阶段 3：自动化 Region 部署](/tidb-cloud/byoc/byoc-automated-deployment.md) | TiDB Cloud | 在 IAM 权限通过验证后，TiDB Cloud 会自动配置 VPC、EKS 集群和控制面资源。注意：此过程是**完全自动化**的，无需客户干预。 |
| [阶段 4：服务初始化](/tidb-cloud/byoc/byoc-initialize-service.md) | 客户 | 先创建资源池，然后通过控制台在资源池中创建您的 TiDB 实例。之后，[配置堡垒机主机](/tidb-cloud/byoc/byoc-configure-bastion-host.md)和认证脚本，以建立安全的维护通道（Tailscale）和可观测性管道。注意：您也可以选择使用自己的自定义方法来建立维护通道。 |
| [阶段 5：验证](/tidb-cloud/byoc/joint-validation.md) | 共同 | 双方团队协作验证连通性、验证指标采集，并确认系统健康状态，以确保 BYOC 环境已准备就绪可供使用。 |

> **Note:**
>
> 每个阶段都需要团队之间及时协调。我们建议双方组织都分配专门资源，以确保所有阶段都能顺利推进。

## 架构概览 {#architecture-overview}

TiDB Cloud BYOC 采用控制面与数据面分离的架构。TiDB Cloud 控制面由 PingCAP 管理，而 TiDB 数据面运行在您自己的云账户中。

在开始入门流程之前，请先阅读 [TiDB Cloud BYOC 架构](/tidb-cloud/architecture-concepts.md#tidb-cloud-byoc)，以了解 BYOC 控制面、数据面、网络连接模型以及高可用选项。