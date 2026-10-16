---
title: TiDB Cloud BYOC 自动化 Region 部署
summary: 本文档概述了 AWS 上 TiDB Cloud BYOC 的自动化 Region 部署流程。
---

# TiDB Cloud BYOC 自动化 Region 部署

在 AWS 环境准备就绪并建立好 IAM 权限后，TiDB Cloud 团队将启动自动化资源预配流程。

> **Note:**
>
> 此阶段由 TiDB Cloud 管理，通常不需要客户执行任何操作。如果部署因客户管理的策略、AWS 服务配额或网络限制而受阻，TiDB Cloud 团队会联系您协助处理。

## 部署概览 {#deployment-overview}

自动化 Region 部署包含以下阶段：

1. 将容器镜像同步到您的 AWS 账户。
2. 部署区域管理平面。
3. 部署客户侧可观测性及配套基础设施。
4. 注册并验证新的 BYOC Region。

该部署会在 TiDB Cloud 管理的 AWS 账户和您的 AWS 账户中同时创建资源。此阶段会为后续创建资源池和实例做好 BYOC Region 的准备，但**不会**创建任何 TiDB 资源池或实例。

## 步骤 1：镜像同步 {#step-1-image-synchronization}

镜像同步步骤大约需要 1-2 小时。

**客户操作：**

选择用于 BYOC 部署的 AWS Region，并将 Region 信息提供给您的 TiDB Cloud 代表。

**执行内容：**

TiDB Cloud 会将所需的容器镜像从其中央镜像仓库同步到您 AWS 账户中的 Amazon ECR registry。

在新的 AWS Region 中进行首次部署可能需要更长时间，因为必须同步所有必需镜像。后续在同一 Region 中的部署会复用已同步的镜像，因此通常完成得更快。

## 步骤 2：部署区域管理平面 {#step-2-deploy-the-regional-management-plane}

TiDB Cloud 会在 TiDB Cloud 管理的 AWS 账户中部署区域管理平面。

区域管理平面包含用于管理您的 BYOC 环境生命周期的基础设施和服务，例如：

- 专用 VPC 和 Amazon EKS 集群
- 区域管理与 API 服务
- 配置和元信息服务
- 用于实例预配、调度、扩缩容和恢复的组件
- 与 TiDB Cloud 全局控制面的集成

区域管理平面不会存储您的 TiDB 应用数据。

## 步骤 3：部署客户侧配套基础设施 {#step-3-deploy-customer-side-supporting-infrastructure}

TiDB Cloud 会承担在账户引导期间创建的 IAM 角色，并在您的 AWS 账户中部署所需的配套资源。

这些资源包括：

- 用于可观测性环境的隔离 VPC
- 用于可观测性服务的专用 Amazon EKS 集群
- 指标、日志和告警组件
- 配套的存储、负载均衡器、API 端点、DNS 记录和证书
- 审计日志和服务级别指标资源
- 客户侧环境与区域管理平面之间的安全连接

> **Note:**
>
> 此步骤中创建的 Amazon EKS 集群承载的是可观测性及其他配套服务。它**不是** TiDB 实例的 TiDB 数据面。TiDB 数据面会在您首次通过 TiDB Cloud 控制台创建 BYOC 实例时初始化。

## 步骤 4：注册并验证 BYOC Region {#step-4-register-and-validate-the-byoc-region}

在基础设施和服务部署完成后，TiDB Cloud 会：

- 将该 BYOC Region 注册到 TiDB Cloud 全局控制面。
- 验证区域管理服务运行正常。
- 验证与客户侧可观测性环境的连通性。
- 确认指标和日志能够按预期路径流转。
- 确认该 Region 已准备好创建 TiDB 实例。

## 部署完成 {#deployment-completion}

自动化 Region 部署完成后：

- TiDB Cloud 团队会通知您 BYOC Region 已准备就绪。
- 新的 BYOC Region 可用于创建实例。
- AWS 将开始对部署期间创建的客户自有资源向您的账户收费，例如 Amazon EKS、EC2、NAT Gateway、负载均衡器和存储。

## 后续操作 {#what-s-next}

在您的 {{{ .byoc }}} Region 完全投入运行后，请继续阅读[创建您的第一个 TiDB Cloud BYOC 实例](/tidb-cloud/byoc/byoc-initialize-service.md)，以创建您的第一个 TiDB 实例并配置安全的管理访问。