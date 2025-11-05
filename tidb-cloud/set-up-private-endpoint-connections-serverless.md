---
title: 通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 Essential
summary: 了解如何通过私有终端节点连接到你的 TiDB Cloud 集群。
---

# 通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 Essential

本文档介绍如何通过 AWS PrivateLink 连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群。

> **Tip:**
>
> - 如果你想了解如何通过 AWS 私有终端节点连接 TiDB Cloud Dedicated 集群，请参见 [Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md)。
> - 如果你想了解如何通过 Azure 私有终端节点连接 TiDB Cloud Dedicated 集群，请参见 [Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
> - 如果你想了解如何通过 Google Cloud 私有终端节点连接 TiDB Cloud Dedicated 集群，请参见 [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

TiDB Cloud 支持通过 [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc) 实现对托管在 AWS VPC 中的 TiDB Cloud 服务的高度安全、单向访问，就像该服务部署在你自己的 VPC 中一样。你的 VPC 中会暴露一个私有终端节点，你可以通过该终端节点并具备相应权限后连接到 TiDB Cloud 服务。

借助 AWS PrivateLink，终端节点连接安全且私密，不会将你的数据暴露在公网。此外，终端节点连接支持 CIDR 重叠，便于网络管理。

私有终端节点的架构如下所示：

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

关于私有终端节点和终端节点服务的更详细定义，请参见以下 AWS 文档：

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 限制

- 目前，TiDB Cloud 仅在终端节点服务托管于 AWS 时支持 AWS PrivateLink 连接。如果服务托管在其他云服务商，AWS PrivateLink 连接不适用。
- 不支持跨区域的私有终端节点连接。

## 前提条件

请确保在 AWS VPC 设置中已启用 DNS 主机名和 DNS 解析。在 [AWS 管理控制台](https://console.aws.amazon.com/) 中创建 VPC 时，这些选项默认是关闭的。

## 使用 AWS 设置私有终端节点

要通过私有终端节点连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 集群，请按照以下步骤操作：

1. [选择 TiDB 集群](#step-1-choose-a-tidb-cluster)
2. [创建 AWS 接口终端节点](#step-2-create-an-aws-interface-endpoint)
3. [连接到你的 TiDB 集群](#step-3-connect-to-your-tidb-cluster)

### Step 1. 选择 TiDB 集群

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 集群的名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 记录下 **Service Name**、**Availability Zone ID** 和 **Region ID**。

    > **Note:**
    >
    > 每个 AWS 区域只需创建一个私有终端节点，该终端节点可被同一区域内的所有 TiDB Cloud Starter 或 TiDB Cloud Essential 集群共享。

### Step 2. 创建 AWS 接口终端节点

<SimpleTab>
<div label="Use AWS Console">

如需使用 AWS 管理控制台创建 VPC 接口终端节点，请执行以下步骤：

1. 登录 [AWS 管理控制台](https://aws.amazon.com/console/)，并打开 Amazon VPC 控制台 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)。
2. 在导航栏点击 **Endpoints**，然后点击右上角的 **Create Endpoint**。

    会显示 **Create endpoint** 页面。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. 选择 **Endpoint services that use NLBs and GWLBs**。
4. 输入你在 [step 1](#step-1-choose-a-tidb-cluster) 中获取的 service name。
5. 点击 **Verify service**。
6. 在下拉列表中选择你的 VPC。展开 **Additional settings**，勾选 **Enable DNS name** 复选框。
7. 在 **Subnets** 区域，选择你的 TiDB 集群所在的可用区，并选择 Subnet ID。
8. 在 **Security groups** 区域，正确选择你的安全组。

    > **Note:**
    >
    > 请确保所选安全组允许你的 EC2 实例在 4000 端口上的入站访问。

9. 点击 **Create endpoint**。

</div>
<div label="Use AWS CLI">

如需使用 AWS CLI 创建 VPC 接口终端节点，请执行以下步骤：

1. 要获取 **VPC ID** 和 **Subnet ID**，请前往 AWS 管理控制台，在相关区域查找。确保你填写了在 [step 1](#step-1-choose-a-tidb-cluster) 中获取的 **Availability Zone ID**。
2. 复制下方命令，将相关参数替换为你获取的信息，然后在终端中执行。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **Tip:**
>
> 在运行命令前，你需要已安装并配置好 AWS CLI。详情请参见 [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。

</div>
</SimpleTab>

然后你就可以通过私有 DNS 名称连接到终端节点服务。

### Step 3: 连接到你的 TiDB 集群

创建接口终端节点后，返回 TiDB Cloud 控制台并按以下步骤操作：

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 在 **Connect With** 下拉列表中，选择你偏好的连接方式。对话框底部会显示对应的连接字符串。
5. 使用该连接字符串连接到你的集群。

> **Tip:**
>
> 如果你无法连接到集群，可能是 AWS 中 VPC 终端节点的安全组设置不正确。解决方法请参见 [此 FAQ](#troubleshooting)。
>
> 如果在创建 VPC 终端节点时遇到错误 `private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`，说明已经创建过私有终端节点，无需重复创建。

## 故障排查

### 启用私有 DNS 后，无法通过私有终端节点连接 TiDB 集群，为什么？

你可能需要在 AWS 管理控制台中正确设置 VPC 终端节点的安全组。进入 **VPC** > **Endpoints**，右键你的 VPC 终端节点，选择合适的 **Manage security groups**。在你的 VPC 内选择允许 EC2 实例通过 4000 端口或自定义端口入站访问的安全组。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
