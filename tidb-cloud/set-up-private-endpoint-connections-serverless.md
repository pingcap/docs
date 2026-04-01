---
title: 通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 Essential
summary: 了解如何通过私有端点连接到你的 TiDB Cloud 集群。
---

# 通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 Essential

本文档介绍如何通过 AWS PrivateLink 连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。

> **提示：**
>
> - 如需了解如何通过 AWS 私有端点连接 TiDB Cloud Dedicated 集群，请参见 [Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md)。
> - 如需了解如何通过 Azure 私有端点连接 TiDB Cloud Dedicated 集群，请参见 [Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
> - 如需了解如何通过 Google Cloud 私有端点连接 TiDB Cloud Dedicated 集群，请参见 [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

TiDB Cloud 支持通过 [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc) 在 AWS VPC 中对 TiDB Cloud service 进行高度安全的单向 access，就像 service 部署在你自己的 VPC 中一样。你的 VPC 中会暴露一个私有端点，你可以通过该端点并具备权限后连接到 TiDB Cloud service。

借助 AWS PrivateLink，端点连接安全且私密，不会将你的数据暴露在公网。此外，端点连接支持 CIDR 重叠，便于网络管理。

私有端点的 architecture 如下所示：

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

如需了解私有端点和端点 service 的更详细定义，请参见以下 AWS 文档：

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 限制

- 目前，TiDB Cloud 仅支持当端点 service 托管在 AWS 时的 AWS PrivateLink 连接。如果 service 托管在其他云服务商，AWS PrivateLink 连接不适用。
- 不支持跨 Region 的私有端点连接。

## 前提条件

请确保在 AWS VPC 设置中已启用 DNS hostnames 和 DNS resolution。在 [AWS Management Console](https://console.aws.amazon.com/) 中创建 VPC 时，这些选项默认是禁用的。

## 使用 AWS 设置私有端点

要通过私有端点连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，请按照以下步骤操作：

1. [选择 TiDB 集群](#step-1-choose-a-tidb-cluster)
2. [创建 AWS interface 端点](#step-2-create-an-aws-interface-endpoint)
3. [在 TiDB Cloud 中授权你的私有端点](#step-3-authorize-your-private-endpoint-in-tidb-cloud)
4. [连接到你的 TiDB 集群](#step-4-connect-to-your-tidb-cluster)

### Step 1. 选择 TiDB 集群

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 记录下 **Service Name**、**Availability Zone ID** 和 **Region ID**。

    > **注意：**
    >
    > 每个 AWS Region 只需创建一个私有端点，该端点可被同一 Region 内的所有 TiDB Cloud Starter 或 TiDB Cloud Essential 集群共享。

### Step 2. 创建 AWS interface 端点

<SimpleTab>
<div label="Use AWS Console">

如需使用 AWS Management Console 创建 VPC interface 端点，请执行以下步骤：

1. 登录 [AWS Management Console](https://aws.amazon.com/console/)，并打开 Amazon VPC 控制台 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)。
2. 在导航栏点击 **Endpoints**，然后点击右上角的 **Create Endpoint**。

    会显示 **Create endpoint** 页面。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. 选择 **Endpoint services that use NLBs and GWLBs**。
4. 输入你在 [step 1](#step-1-choose-a-tidb-cluster) 获取的 service name。
5. 点击 **Verify service**。
6. 在下拉列表中选择你的 VPC。展开 **Additional settings** 并勾选 **Enable DNS name** 复选框。
7. 在 **Subnets** 区域，选择你的 TiDB 集群所在的 availability zone，并选择 Subnet ID。
8. 在 **Security groups** 区域，正确选择你的安全组。

    > **注意：**
    >
    > 请确保所选安全组允许你的 EC2 实例在 port 4000 上的入站 access。

9. 点击 **Create endpoint**。

</div>
<div label="Use AWS CLI">

如需使用 AWS CLI 创建 VPC interface 端点，请执行以下步骤：

1. 获取 **VPC ID** 和 **Subnet ID**，可在 AWS Management Console 的相关页面找到。请确保填写你在 [step 1](#step-1-choose-a-tidb-cluster) 获取的 **Availability Zone ID**。
2. 复制下方命令，将相关参数替换为你获取的信息，然后在终端中 execute。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **提示：**
>
> 在运行命令前，你需要已安装并配置好 AWS CLI。详情参见 [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。

</div>
</SimpleTab>

然后你可以通过私有 DNS name 连接到端点 service。

### Step 3. 在 TiDB Cloud 中授权你的私有端点

创建 AWS interface 端点后，必须将其添加到集群的 allowlist。

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 在左侧导航栏点击 **Settings** > **Networking**。
3. 向下滚动到 **Private Endpoint** 部分，找到 **Authorized Networks** 表格。
4. 点击 **Add Rule** 添加防火墙规则。

    - **Endpoint Service Name**：粘贴你在 [Step 1](#step-1-choose-a-tidb-cluster) 获取的 service name。
    - **Firewall Rule Name**：输入用于标识此连接的名称。
    - **Your VPC Endpoint ID**：粘贴你在 AWS Management Console 获取的 22 位 VPC Endpoint ID（以 `vpce-` 开头）。

    > **提示：**
    > 
    > 如需允许来自你的云 Region 的所有 Private Endpoint 连接（用于测试或开放 access），可在 **Your VPC Endpoint ID** 字段中输入单个星号（`*`）。

5. 点击 **Submit**。

### Step 4. 连接到你的 TiDB 集群

创建 interface 端点后，返回 TiDB Cloud 控制台并执行以下操作：

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 在 **Connect With** 下拉列表中，选择你偏好的连接 method。对话框底部会显示对应的连接 string。
5. 使用该连接 string 连接到你的集群。

> **提示：**
>
> 如果无法连接到集群，可能是 AWS 中 VPC 端点的安全组设置不正确。解决方法请参见 [此 FAQ](#troubleshooting)。
>
> 创建 VPC 端点时，如果遇到错误 `private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`，说明已存在私有端点，无需重复创建。

## 故障排查

### 启用私有 DNS 后无法通过私有端点连接 TiDB 集群，原因是什么？

你可能需要在 AWS Management Console 中正确设置 VPC 端点的安全组。进入 **VPC** > **Endpoints**，右键你的 VPC 端点，选择合适的 **Manage security groups**。确保你的 VPC 内有允许 EC2 实例在 Port 4000 或自定义 port 入站 access 的安全组。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)