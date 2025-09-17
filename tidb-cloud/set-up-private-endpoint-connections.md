---
title: 通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群
summary: 了解如何通过私有终端节点使用 AWS 连接到你的 TiDB Cloud 集群。
---

# 通过 AWS PrivateLink 连接到 TiDB Cloud Dedicated 集群

本文档介绍如何通过 [AWS PrivateLink](https://aws.amazon.com/privatelink) 连接到你的 TiDB Cloud Dedicated 集群。

> **提示：**
>
> - 如需了解如何通过私有终端节点连接到 TiDB Cloud Serverless 集群，请参见 [Connect to TiDB Cloud Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。
> - 如需了解如何通过 Azure 私有终端节点连接到 TiDB Cloud Dedicated 集群，请参见 [Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)。
> - 如需了解如何通过 Google Cloud 私有终端节点连接到 TiDB Cloud Dedicated 集群，请参见 [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

TiDB Cloud 支持通过 [AWS PrivateLink](https://aws.amazon.com/privatelink) 实现对托管在 AWS VPC 中的 TiDB Cloud 服务的高度安全且单向的访问，就像服务部署在你自己的 VPC 中一样。你的 VPC 中会暴露一个私有终端节点，你可以通过该终端节点并具备相应权限后连接到 TiDB Cloud 服务。

借助 AWS PrivateLink，终端节点连接安全且私密，不会将你的数据暴露在公网上。此外，终端节点连接支持 CIDR 重叠，便于网络管理。

私有终端节点的架构如下所示：

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

关于私有终端节点和终端节点服务的更详细定义，请参见以下 AWS 文档：

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 限制

- 只有 **Organization Owner** 和 **Project Owner** 角色可以创建私有终端节点。
- 私有终端节点和要连接的 TiDB 集群必须位于同一区域。

在大多数场景下，建议优先使用私有终端节点连接而不是 VPC 对等连接。但在以下场景下，应使用 VPC 对等连接而不是私有终端节点连接：

- 你正在使用 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 集群，将数据从源 TiDB 集群跨区域同步到目标 TiDB 集群，以实现高可用。目前，私有终端节点不支持跨区域连接。
- 你正在使用 TiCDC 集群将数据同步到下游集群（如 Amazon Aurora、MySQL 和 Kafka），但无法自行维护终端节点服务。
- 你需要直接连接到 PD 或 TiKV 节点。

## 前提条件

请确保在 AWS VPC 设置中已启用 DNS 主机名和 DNS 解析。在 [AWS 管理控制台](https://console.aws.amazon.com/) 中创建 VPC 时，这些选项默认是关闭的。

## 设置私有终端节点连接并连接到你的集群

要通过私有终端节点连接到 TiDB Cloud Dedicated 集群，请完成以下步骤：

1. [选择 TiDB 集群](#step-1-select-a-tidb-cluster)
2. [创建 AWS 接口终端节点](#step-2-create-an-aws-interface-endpoint)
3. [创建私有终端节点连接](#step-3-create-a-private-endpoint-connection)
4. [启用私有 DNS](#step-4-enable-private-dns)
5. [连接到你的 TiDB 集群](#step-5-connect-to-your-tidb-cluster)

如果你有多个集群，需要对每个希望通过 AWS PrivateLink 连接的集群重复上述步骤。

### Step 1. 选择 TiDB 集群

1. 在项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB 集群的名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框。
3. 在 **Connection Type** 下拉列表中选择 **Private Endpoint**，然后点击 **Create Private Endpoint Connection**。

> **注意：**
>
> 如果你已经创建了私有终端节点连接，激活的终端节点会显示在连接对话框中。如需创建更多私有终端节点连接，请通过左侧导航栏点击 **Settings** > **Networking** 进入 **Networking** 页面。

### Step 2. 创建 AWS 接口终端节点

> **注意：**
>
> 对于 2023 年 3 月 28 日之后创建的每个 TiDB Cloud Dedicated 集群，系统会在集群创建后 3 到 4 分钟内自动创建对应的终端节点服务。

如果你看到 `TiDB Private Link Service is ready` 消息，说明对应的终端节点服务已就绪。你可以提供以下信息来创建终端节点。

1. 填写 **Your VPC ID** 和 **Your Subnet IDs** 字段。你可以在 [AWS 管理控制台](https://console.aws.amazon.com/) 中找到这些 ID。若有多个子网，使用空格分隔各个 ID。
2. 点击 **Generate Command** 获取如下终端节点创建命令。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

然后，你可以通过 AWS CLI 或 [AWS 管理控制台](https://aws.amazon.com/console/) 创建 AWS 接口终端节点。

<SimpleTab>
<div label="Use AWS CLI">

如需使用 AWS CLI 创建 VPC 接口终端节点，请执行以下步骤：

1. 复制生成的命令并在终端中运行。
2. 记录你刚刚创建的 VPC 终端节点 ID。

> **提示：**
>
> - 在运行命令前，你需要已安装并配置好 AWS CLI。详情请参见 [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。
>
> - 如果你的服务跨越了三个以上的可用区（AZ），你会收到一条错误消息，提示 VPC 终端节点服务不支持该子网的可用区。该问题通常发生在你选择的区域中存在额外的可用区，而你的 TiDB 集群并未部署在该可用区。在这种情况下，你可以联系 [PingCAP 技术支持](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

</div>
<div label="Use AWS Console">

如需使用 AWS 管理控制台创建 VPC 接口终端节点，请执行以下步骤：

1. 登录 [AWS 管理控制台](https://aws.amazon.com/console/)，并打开 Amazon VPC 控制台 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)。
2. 在导航栏点击 **Endpoints**，然后点击右上角的 **Create Endpoint**。

    会显示 **Create endpoint** 页面。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. 在 **Endpoint settings** 区域，如有需要填写名称标签，然后选择 **Endpoint services that use NLBs and GWLBs** 选项。
4. 在 **Service settings** 区域，输入生成命令中的服务名称 `${your_endpoint_service_name}`（即 `--service-name ${your_endpoint_service_name}`）。
5. 点击 **Verify service**。
6. 在 **Network settings** 区域，从下拉列表中选择你的 VPC。
7. 在 **Subnets** 区域，选择你的 TiDB 集群所在的可用区。

    > **提示：**
    >
    > 如果你的服务跨越了三个以上的可用区（AZ），你可能无法在 **Subnets** 区域选择 AZ。该问题通常发生在你选择的区域中存在额外的可用区，而你的 TiDB 集群并未部署在该可用区。在这种情况下，请联系 [PingCAP 技术支持](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

8. 在 **Security groups** 区域，正确选择你的安全组。

    > **注意：**
    >
    > 请确保所选安全组允许你的 EC2 实例通过 4000 端口或自定义端口入站访问。

9. 点击 **Create endpoint**。

</div>
</SimpleTab>

### Step 3. 创建私有终端节点连接

1. 返回 TiDB Cloud 控制台。
2. 在 **Create AWS Private Endpoint Connection** 页面，输入你的 VPC 终端节点 ID。
3. 点击 **Create Private Endpoint Connection**。

> **提示：**
>
> 你可以在以下两个页面查看和管理私有终端节点连接：
>
> - 集群级 **Networking** 页面：通过左上角下拉框切换到目标集群，然后点击左侧导航栏的 **Settings** > **Networking**。
> - 项目级 **Network Access** 页面：通过左上角下拉框切换到目标项目，然后点击左侧导航栏的 **Project Settings** > **Network Access**。

### Step 4. 启用私有 DNS

在 AWS 中启用私有 DNS。你可以使用 AWS CLI 或 AWS 管理控制台。

<SimpleTab>
<div label="Use AWS CLI">

如需使用 AWS CLI 启用私有 DNS，请从 **Create Private Endpoint Connection** 页面复制以下 `aws ec2 modify-vpc-endpoint` 命令，并在 AWS CLI 中运行。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

或者，你也可以在集群的 **Networking** 页面找到该命令。定位到私有终端节点，在 **Action** 列点击 **...*** > **Enable DNS**。

</div>
<div label="Use AWS Console">

如需在 AWS 管理控制台启用私有 DNS：

1. 进入 **VPC** > **Endpoints**。
2. 右键点击你的终端节点 ID，选择 **Modify private DNS name**。
3. 勾选 **Enable for this endpoint** 复选框。
4. 点击 **Save changes**。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### Step 5. 连接到你的 TiDB 集群

在你接受私有终端节点连接后，会自动返回连接对话框。

1. 等待私有终端节点连接状态从 **System Checking** 变为 **Active**（大约 5 分钟）。
2. 在 **Connect With** 下拉列表中选择你偏好的连接方式。对话框底部会显示对应的连接字符串。
3. 使用该连接字符串连接到你的集群。

> **提示：**
>
> 如果无法连接到集群，可能是 AWS 中 VPC 终端节点的安全组设置不正确。解决方法请参见 [此常见问题](#troubleshooting)。

### 私有终端节点状态参考

使用私有终端节点连接时，私有终端节点或私有终端节点服务的状态会显示在以下页面：

- 集群级 **Networking** 页面：通过左上角下拉框切换到目标集群，然后点击左侧导航栏的 **Settings** > **Networking**。
- 项目级 **Network Access** 页面：通过左上角下拉框切换到目标项目，然后点击左侧导航栏的 **Project Settings** > **Network Access**。

私有终端节点可能的状态说明如下：

- **Not Configured**：已创建终端节点服务，但尚未创建私有终端节点。
- **Pending**：等待处理。
- **Active**：你的私有终端节点已就绪。此状态下无法编辑该私有终端节点。
- **Deleting**：私有终端节点正在删除中。
- **Failed**：私有终端节点创建失败。你可以点击该行的 **Edit** 重试创建。

私有终端节点服务可能的状态说明如下：

- **Creating**：终端节点服务正在创建中，需等待 3 到 5 分钟。
- **Active**：终端节点服务已创建，无论私有终端节点是否已创建。
- **Deleting**：终端节点服务或集群正在删除中，需等待 3 到 5 分钟。

## 故障排查

### 启用私有 DNS 后，无法通过私有终端节点连接到 TiDB 集群，原因是什么？

你可能需要在 AWS 管理控制台中为 VPC 终端节点正确设置安全组。进入 **VPC** > **Endpoints**，右键点击你的 VPC 终端节点，选择合适的 **Manage security groups**。确保你 VPC 内的安全组允许你的 EC2 实例通过 4000 端口或自定义端口入站访问。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)