---
title: 在 AWS 中准备你的 BYOC 环境
summary: 为 TiDB Cloud BYOC 部署准备所需基础设施组件的说明。
---

# 在 AWS 中准备你的 BYOC 环境

在开始 BYOC 部署之前，请先在你的 AWS 环境中准备所需的基础设施组件。请按顺序完成以下步骤。

## Step 1. 获取 TiDB Cloud Organization ID {#step-1-retrieve-tidb-cloud-organization-id}

这是你的组织在 TiDB Cloud 中的唯一标识符。

1. 登录 [TiDB Cloud console](https://tidbcloud.com/)。

    如果你还没有 TiDB Cloud 账户，请点击[这里](https://tidbcloud.com/free-trial)注册。你可以使用电子邮件和密码注册以管理 TiDB Cloud 凭证，也可以通过 Google、GitHub 或 Microsoft 账户使用单点登录（SSO）。

2. 在左侧导航栏中，点击你的个人资料图标 > **Organization Settings**。

3. 在 **Organization Information** 下，复制 **Organization ID** 并保存，供后续使用。

## Step 2. 准备 AWS 账户 {#step-2-prepare-an-aws-account}

我们强烈建议你为 BYOC 环境使用一个**专用 AWS 账户**，以确保隔离、简化合规性管理并实现准确的成本管理。

- **Account ID：**确保你已准备好 12 位 AWS Account ID。
- **Permissions：**确保你拥有 AdministratorAccess 或等效权限，以配置 IAM 角色和 Route 53。

## Step 3. 选择 Region 和可用区（AZ） {#step-3-select-region-and-availability-zones-azs}

TiDB 是一个分布式数据库，需要特定的基础设施来实现高可用。

1. **Region：**选择要部署数据库的 AWS Region。
2. **可用区（AZ）：**根据你的部署目标，选择以下配置之一：

    - **选项 A：生产环境（Multi-AZ）。**你**必须**在所选 Region 中确定至少 **3 个 AZ**。例如：`us-west-2a`、`us-west-2b`、`us-west-2c`。

    - **选项 B：概念验证 / 成本优化（Single-AZ）。**精确选择 **1 个 AZ**。例如：`us-west-2a`。

为 BYOC Region 准备的可用区决定了 TiDB Cloud 放置资源池的位置。创建资源池时，你可以选择 **Zonal** 或 **Regional** 高可用。Zonal 资源池部署在一个可用区中。Regional 资源池要求该 Region 中至少有三个符合条件的可用区。

如果某个 BYOC Region 最初只准备了一个可用区，TiDB Cloud 会将该可用区用于 Zonal 资源池。只有在另外两个符合条件的可用区可用时，你才能创建 Regional 资源池。如果你计划使用 Regional 资源池，请在环境准备阶段确认该 Region 至少提供三个符合条件的可用区。

## Step 4. 为 TiDB 创建 hosted zone {#step-4-create-a-hosted-zone-for-tidb}

为 TiDB 服务 DNS 创建一个 Amazon Route 53 hosted zone。你无需为可观测性（O11Y）提供 hosted zone。

选择以下 hosted zone 类型之一：

- **Public hosted zone：**支持到 TiDB 的公网和私网连接。请参考 [Creating a public hosted zone in AWS documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html)。
- **Private hosted zone：**仅支持私网连接。如果你选择 private hosted zone，则 BYOC 环境将无法使用公网连接。请参考 [Working with private hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html)。

对于 TiDB hosted zone，请使用长度不超过 38 个字符的名称。例如：`byoc.cluster.example.com`。

对于 public hosted zone，请通过将 Route 53 name server（NS）记录添加到父域 DNS 配置中，从其父域委派该 zone。对于 private hosted zone，请将该 hosted zone 关联到需要 DNS 解析的 VPC。

> **Note:**
>
> 如果你计划在多个 AWS Region 中部署 TiDB Cloud BYOC，可以在所有 Region 之间共享同一个 TiDB hosted zone，也可以为每个 Region 使用专用 hosted zone。详情请参见[多 Region 部署](/tidb-cloud/byoc/multi-region-deployment.md)。

## Step 5. 设置私有证书颁发机构（PCA） {#step-5-set-up-private-certificate-authority-pca}

TiDB Cloud 使用 AWS private certificate authority（PCA）服务签发证书，并使用 AWS Certificate Manager（ACM）服务管理数字证书，以通过 mTLS 确保内部数据库集群组件之间的安全通信。

为满足合规要求，TiDB Cloud BYOC 集成了客户提供的 PCA，使用你企业自己的域名为数据节点签发身份证书。这可确保所有加密通信的信任根（Root of Trust）始终严格由你的组织控制。

因此，你必须在部署 Region 中准备一个有效的 subordinate CA。你提供给 TiDB Cloud 的 CA ARN 必须是 subordinate CA 的 ARN。要创建并激活 subordinate CA，你需要一个处于活动状态的 root CA 来为其证书签名。

subordinate CA 证书的有效期必须至少为 **20 年**。请确保用于签署 subordinate CA 证书的 root CA 支持该有效期。

请执行以下步骤：

1. **创建 subordinate CA。**请参考 [Create a private CA in AWS Private CA](https://docs.aws.amazon.com/privateca/latest/userguide/create-CA.html)。

    配置：选择 **Subordinate CA** 作为 CA 类型。不要向 TiDB Cloud 提供 root CA ARN。

2. **安装 subordinate CA 证书。**请参考 [Installing the CA certificate](https://docs.aws.amazon.com/privateca/latest/userguide/PCACertInstall.html)。

3. **记录 ARN。**复制 **Subordinate CA ARN**。

    示例：`arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234...`

4. 在 AWS 控制台中**验证 PCA 信息**。

<!--To confirm: image screenshot-->

> **Note:**
>
> - **对于概念验证或成本优化**：如果你当前处于概念验证（POC）阶段，可以选择使用 Self-Signed Certificates 而不是 AWS Private CA，以降低成本。有关此选项的具体配置说明，请直接联系你的 TiDB Cloud 支持代表。
> - **对于多 Region 部署**：与 hosted zone 类似，在多 Region 部署中，同一个 private certificate authority（PCA）可以在所有 Region 之间共享。你也可以为每个新 Region 创建专用 PCA。详情请参见[多 Region 部署](/tidb-cloud/byoc/multi-region-deployment.md)。

## Step 6. 规划网络 CIDR 范围 {#step-6-plan-network-cidr-ranges}

在开始 BYOC 部署之前，请为可观测性（O11Y）基础设施和资源池规划专用私有 CIDR 范围。请使用 `/16` 到 `/22` 之间的前缀长度。

每个 BYOC 部署 Region 都有一个 O11Y CIDR。资源池 CIDR 会在你创建每个资源池时分别配置。请在部署前规划这些 CIDR 范围，以便能够在没有网络冲突的情况下配置 BYOC 环境和未来的资源池。

请准备以下信息：

| 项目 | 说明 | 示例 |
| ----- | ----- | ----- |
| O11Y CIDR | 为部署 Region 中的可观测性基础设施及相关服务预留的 CIDR 范围。 | `10.1.0.0/22` |
| Resource pool CIDR | 为资源池预留的 CIDR 范围。每个资源池都有自己的 CIDR，资源池创建后无法修改。 | `10.10.0.0/16` |

**CIDR 规划规则与约束**

规划 CIDR 范围时，请确保遵循以下连接规则：

- **内部隔离：**在同一 Region 中，资源池 CIDR 不得与 O11Y CIDR 重叠，也不得彼此重叠。

- **VPC peering 规则：**

    * **不能重叠：**O11Y CIDR 和任何资源池 CIDR 都不得与你现有的应用 VPC、本地网络或 VPN 网络重叠。
    * **客户责任：**TiDB Cloud 无法检测与客户自主管理网络的冲突。你有责任在部署前或创建资源池前规划并验证这些 CIDR 范围。

- **跨 Region CIDR 规划：**不同 Region 中的资源池 CIDR 可以重叠。但是，对于需要跨 Region 连接或复制的资源池，请使用不重叠的 CIDR。

- **跨资源池复制（关键）：**如果你计划部署多个资源池，并且可能需要**在不同资源池中的实例之间复制数据**（例如，使用 TiCDC 进行容灾或数据整合），则它们各自的资源池 CIDR 范围**不得重叠**。

在自动化 Region 部署开始之前，请将规划好的 CIDR 范围提供给你的 TiDB Cloud 代表。

## 总结：所需信息 {#summary-required-information}

请将上面步骤中收集到的信息填写到下表中，并分享给你的 TiDB Cloud 代表，以启动部署。

**所需信息：**

| 类别 | 需要提供的详细信息 | 示例 | 备注 |
| :---- | :---- | :---- | :---- |
| **TiDB Cloud Organization ID** | 你的 TiDB Cloud 组织的唯一标识符 | `1372813089209270552` | Step 1 |
| **AWS Account ID** | 12 位 AWS 账户编号 | `123456789012` | Step 2 |
| **AWS Region** | 选择用于部署的 Region | `us-west-2`, `us-east-1`, `us-east-2` | Step 3。对于多 Region 部署，请列出所有 Region。 |
| **Availability Zones** | 每个 Region 提供 3 个 AZ 或单个 AZ（请注明名称和 ID） | **Us-east-1:** `us-east-1a`, `use1-az1`, `us-east-1b`, `use1-az2`, `us-east-1c`, `use1-az4`; **Us-east-2:** `us-east-2a`, `use2-az1`, `us-east-2b`, `use2-az2`, `us-east-2c`, `use2-az3`; **Us-west-2:** `us-west-2a`, `usw2-az1` | Step 3。注意对**每个**所选 Region 都要满足 AZ 数量要求。 |
| **Subordinate CA ARN** | AWS ACM Private CA ARN | `arn:aws:acm-pca:us-west-2:123456789012:ca/abcd-1234` | Step 5。该 ARN 可在多个 Region 之间共享。 |
| **Hosted Zone Name & Hosted Zone ID** | TiDB hosted zone。你可以提供 public hosted zone 或 private hosted zone。 | **Hosted TiDB zone name:** `clusters.byoc-0929.pingcap.net`; **Hosted TiDB zone ID:** `Z1039122VAY4T8UNWR8E`. | Step 4。该 hosted zone 可在多个 Region 之间共享。 |
| **CIDR** | 客户规划的用于 O11Y 基础设施和资源池的 CIDR 范围 | **O11Y CIDR:** `10.1.0.0/22`; **Resource pool CIDR:** `10.10.0.0/16` | Step 6 |
| **Image Sync Region** | 选择用于镜像同步的 Region ID | `us-west-2` | 详情请参见[镜像同步](/tidb-cloud/byoc/byoc-automated-deployment.md#step-1-image-synchronization)。 |

## 检查并提高 AWS 服务配额 {#review-and-increase-aws-service-quotas}

AWS 服务配额要求因客户环境而异。所需的配额值取决于多种因素，例如你的工作负载规模、目标容量、所选 AWS Region、可用性模式以及预期扩缩容范围。

在环境准备期间，请与 TiDB Cloud 支持团队或你的 TiDB Cloud 代表一起计算部署所需的配额值。如果你当前的 AWS 服务配额低于计算出的要求，请在自动化 Region 部署开始之前申请提高配额。

### 需要检查的配额类别 {#quota-categories-to-review}

请在每个目标 AWS Region 中检查以下配额类别：

- **Amazon EC2 quotas**：与基于 vCPU 的实例使用量以及部署所需实例族相关的配额值。
- **Amazon EBS quotas**：与部署所需存储类型和卷容量相关的配额值。
- **Amazon EKS and scaling-related quotas**：影响 EKS 集群和节点扩缩容能力的配额值，包括 EC2 容量、Auto Scaling Group 限制以及 EKS managed node group 限制。

### 如何申请提高配额 {#how-to-request-a-quota-increase}

1. 登录 AWS Management Console。
2. 进入 Service Quotas。
3. 搜索相关服务：Amazon EC2、Amazon EBS 和 Amazon EKS。
4. 选择所需配额。
5. 点击 **Request quota increase**。
6. 输入目标值并提交请求。

## 下一步 {#what-s-next}

在你准备好 AWS 环境并将所需信息分享给 TiDB Cloud 代表后，请继续阅读 [TiDB Cloud BYOC IAM Configuration](/tidb-cloud/byoc/byoc-configure-iam-permissions.md)，配置自动化 Region 部署所需的 IAM 权限。