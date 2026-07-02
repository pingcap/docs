---
title: 通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 Essential
summary: 了解如何通过私有端点连接到你的 {{{ .starter }}} 或 Essential 实例。
---

# 通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 Essential

本文档介绍如何通过 AWS PrivateLink 连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 实例。

> **Tip:**
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

## 选择端点模型 {#choose-an-endpoint-model}

根据你的 TiDB Cloud 计划，选择合适的私有端点模型：

- 对于 {{{ .starter }}} 实例，或 2026 年 7 月 1 日之前创建的 {{{ .essential }}} 实例，请使用[**端点共享模型**](#set-up-a-private-endpoint-with-aws-endpoint-shared-model)。在此模型中，同一 AWS Region 和 VPC 中的多个 {{{ .starter }}} 或 {{{ .essential }}} 实例可以共享一个私有端点。
- 对于从 2026 年 7 月 1 日开始创建的 {{{ .essential }}} 实例，请使用[**端点独占模型**](#set-up-a-private-endpoint-with-aws-endpoint-exclusive-model)。在此模型中，每个 {{{ .essential }}} 实例使用其各自独立的私有端点。此模型无需在连接时包含[账户前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)，但你需要为每个 {{{ .essential }}} 实例重复执行设置步骤。

## 使用 AWS 设置私有端点（端点共享模型） {#set-up-a-private-endpoint-with-aws-endpoint-shared-model}

要使用共享模型通过私有端点连接到你的 {{{ .starter }}} 或 {{{ .essential }}} 实例，请按照以下步骤操作：

1. [选择 {{{ .starter }}} 或 Essential 实例](#step-1-choose-a-tidb-instance)
2. [创建 AWS interface 端点](#step-2-create-an-aws-interface-endpoint)
3. [在 TiDB Cloud 中授权你的私有端点（可选）](#step-3-authorize-your-private-endpoint-in-tidb-cloud-optional)
4. [连接到你的 {{{ .starter }}} 或 Essential 实例](#step-4-connect-to-your-tidb)

### Step 1. 选择 {{{ .starter }}} 或 Essential 实例 {#step-1-choose-a-tidb-instance}

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击目标 {{{ .starter }}} 或 {{{ .essential }}} 实例的名称，进入其概览页面。
2. 点击右上角的 **Connect**。此时会显示连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 记下 **Service Name**、**Availability Zone ID** 和 **Region ID**。

    > **注意：**
    >
    > 对于 AWS 区域中的每个 VPC，你只需创建一个私有端点。该端点可供该 AWS 区域中同一 VPC 内的所有 {{{ .starter }}} 或 {{{ .essential }}} 实例使用，但不能跨 VPC 共享。

### Step 2. 创建 AWS interface 端点

<SimpleTab>
<div label="Use AWS Console">

如需使用 AWS Management Console 创建 VPC interface 端点，请执行以下步骤：

1. 登录 [AWS Management Console](https://aws.amazon.com/console/)，并打开 Amazon VPC 控制台 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)。
2. 在导航栏点击 **Endpoints**，然后点击右上角的 **Create Endpoint**。

    会显示 **Create endpoint** 页面。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. 选择 **Endpoint services that use NLBs and GWLBs**。
4. 输入你在 [step 1](#step-1-choose-a-tidb-instance) 获取的 service name。
5. 点击 **Verify service**。
6. 在下拉列表中选择你的 VPC。展开 **Additional settings** 并勾选 **Enable DNS name** 复选框。
7. 在 **Subnets** 区域，选择你的 {{{ .starter }}} 或 Essential 实例所在的 availability zone，并选择 Subnet ID。
8. 在 **Security groups** 区域，正确选择你的安全组。

    > **注意：**
    >
    > 请确保所选安全组允许你的 EC2 实例在 port 4000 上的入站 access。

9. 点击 **Create endpoint**。

</div>
<div label="Use AWS CLI">

如需使用 AWS CLI 创建 VPC interface 端点，请执行以下步骤：

1. 获取 **VPC ID** 和 **Subnet ID**，可在 AWS Management Console 的相关页面找到。请确保填写你在 [step 1](#step-1-choose-a-tidb-instance) 获取的 **Availability Zone ID**。
2. 复制下方命令，将相关参数替换为你获取的信息，然后在终端中 execute。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **Tip:**
>
> 在运行命令前，你需要已安装并配置好 AWS CLI。详情参见 [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。

</div>
</SimpleTab>

然后你可以通过私有 DNS name 连接到端点 service。

### Step 3. 在 TiDB Cloud 中授权你的私有端点（可选） {#step-3-authorize-your-private-endpoint-in-tidb-cloud-optional}

> **注意：**
>
> 此步骤为可选。仅当你希望将访问限制为特定私有端点连接时，才需要配置 **Authorized Networks**。如果未配置任何规则，则默认允许所有私有端点连接。

创建 AWS interface 端点后，你可以为目标 {{{ .starter }}} 或 {{{ .essential }}} 实例授权该端点以限制访问。

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击目标 TiDB Cloud Starter 或 TiDB Cloud Essential 实例的名称，进入其概览页面。
2. 在左侧导航栏点击 **Settings** > **Networking**。
3. 向下滚动到 **Private Endpoint** 部分，找到 **Authorized Networks** 表格。
4. 点击 **Add Rule** 添加防火墙规则。

    - **Endpoint Service Name**：粘贴你在 [Step 1](#step-1-choose-a-tidb-instance) 获取的 service name。
    - **Firewall Rule Name**：输入用于标识此连接的名称。
    - **Your VPC Endpoint ID**：粘贴你在 AWS Management Console 获取的 22 位 VPC Endpoint ID（以 `vpce-` 开头）。

    > **Tip:**
    >
    > - 如果将 **Authorized Networks** 表留空，则默认允许所有私有端点连接。
    > - 如需允许来自你的云 Region 的所有 private endpoint 连接（用于测试或开放 access），可在 **Your VPC Endpoint ID** 字段中输入单个星号（`*`）。

5. 点击 **Submit**。

### Step 4. 连接到你的 {{{ .starter }}} 或 Essential 实例 {#step-4-connect-to-your-tidb}

创建 interface 端点后，返回 TiDB Cloud 控制台并执行以下步骤：

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击目标 {{{ .starter }}} 或 Essential 实例的名称，进入其概览页面。
2. 点击右上角的 **Connect**。此时会显示连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**。
4. 在 **Connect With** 下拉列表中，选择你偏好的连接方式。对话框底部会显示相应的连接字符串。
5. 使用该连接字符串连接到你的 {{{ .starter }}} 或 Essential 实例。

> **Tip:**
>
> 如果你无法连接到 {{{ .starter }}} 或 Essential 实例，原因可能是 AWS 中 VPC 端点的安全组设置不正确。请参见[此常见问题](#troubleshooting)获取解决方案。
>
> 创建 VPC 端点时，如果遇到错误 `private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`，说明该 VPC 中已存在一个私有端点。对于相同的私有 DNS 名称，你无需再创建另一个端点。

## 使用 AWS 设置私有端点（端点独占模型） {#set-up-a-private-endpoint-with-aws-endpoint-exclusive-model}

> **注意：**
>
> 目前，端点独占模型仅适用于在部分 AWS 区域中从 2026 年 7 月 1 日开始创建的 {{{ .essential }}} 实例。如果你的实例不支持此模型，可以改用[端点共享模型](#set-up-a-private-endpoint-with-aws-endpoint-shared-model)。

在端点独占模型中，每个 {{{ .essential }}} 实例使用其各自独立的私有端点。此模型无需在连接时包含[账户前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)，但你需要为每个 {{{ .essential }}} 实例重复执行设置步骤。

要使用独占模型通过私有端点连接到 {{{ .essential }}} 实例，请执行以下步骤：

1. [选择 {{{ .essential }}} 实例](#step-1-select-an-essential-instance)
2. [创建 AWS interface 端点](#step-2-create-an-aws-interface-endpoint-exclusive-model)
3. [创建私有端点连接](#step-3-create-a-private-endpoint-connection-exclusive-model)
4. [启用私有 DNS](#step-4-enable-private-dns-exclusive-model)
5. [连接到你的 {{{ .essential }}} 实例](#step-5-connect-to-your-essential-instance)

如果你有多个实例，则需要为每个要使用 AWS PrivateLink 连接的实例重复执行这些步骤。

### Step 1. 选择 {{{ .essential }}} 实例 {#step-1-select-an-essential-instance}

1. 在 TiDB Cloud 控制台的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面上，点击目标 {{{ .essential }}} 实例的名称，进入其概览页面。
2. 点击右上角的 **Connect**。此时会显示连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**，然后点击 **Create Private Endpoint Connection**。

> **注意：**
>
> 如果你已经创建了私有端点连接，活动端点会显示在连接对话框中。要创建更多私有端点连接，请点击左侧导航栏中的 **Settings** > **Networking**，进入 **Networking** 页面。

### Step 2. 创建 AWS interface 端点 {#step-2-create-an-aws-interface-endpoint-exclusive-model}

> **注意：**
>
> 对于每个 {{{ .essential }}} 实例，对应的端点服务会在实例创建后 3 到 4 分钟自动创建。

在连接对话框中，如果你看到 `TiDB Private Link Service is ready` 消息，则表示对应的端点服务已就绪。你可以提供以下信息来创建端点。

1. 在连接对话框中，点击 **How to Generate VPC Endpoint ID**，然后填写 **Your VPC ID** 和 **Your Subnet IDs** 字段。你可以从 [AWS Management Console](https://console.aws.amazon.com/) 中找到这些 ID。对于多个子网，请输入以空格分隔的 ID。

2. 点击 **Generate Command** 获取以下端点创建命令。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

然后，你可以使用 AWS CLI 或 [AWS Management Console](https://aws.amazon.com/console/) 创建 AWS interface 端点。

<SimpleTab>
<div label="Use AWS CLI">

要使用 AWS CLI 创建 VPC interface 端点，请执行以下步骤：

1. 复制生成的命令并在终端中运行。
2. 记录刚刚创建的 VPC 端点 ID。

> **Tip:**
>
> - 运行命令前，你需要先安装并配置 AWS CLI。详情请参见 [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。
>
> - 如果你的服务跨越三个以上的可用区（AZ），你将收到一条错误消息，指出 VPC 端点服务不支持该子网所在的 AZ。当你所选 Region 中除了 {{{ .essential }}} 实例所在的 AZ 之外还存在额外的 AZ 时，就会出现此问题。在这种情况下，你可以联系 [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

</div>
<div label="Use AWS Console">

要使用 AWS Management Console 创建 VPC interface 端点，请执行以下步骤：

1. 登录 [AWS Management Console](https://aws.amazon.com/console/)，并在 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/) 打开 Amazon VPC 控制台。
2. 在导航窗格中点击 **Endpoints**，然后点击右上角的 **Create Endpoint**。

    此时会显示 **Create endpoint** 页面。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. 在 **Endpoint settings** 区域中，根据需要填写名称标签，然后选择 **Endpoint services that use NLBs and GWLBs** 选项。
4. 在 **Service settings** 区域中，输入生成命令中的服务名称 `${your_endpoint_service_name}`（`--service-name ${your_endpoint_service_name}`）。
5. 点击 **Verify service**。
6. 在 **Network settings** 区域中，从下拉列表中选择你的 VPC。
7. 在 **Subnets** 区域中，选择 {{{ .essential }}} 实例所在的可用区。

    > **Tip:**
    >
    > 如果你的服务跨越三个以上的可用区（AZ），你可能无法在 **Subnets** 区域中选择 AZ。当你所选 Region 中除了 {{{ .essential }}} 实例所在的 AZ 之外还存在额外的 AZ 时，就会出现此问题。在这种情况下，请联系 [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

8. 在 **Security groups** 区域中，正确选择你的安全组。

    > **注意：**
    >
    > 确保所选安全组允许你的 EC2 实例通过端口 `4000` 或自定义端口进行入站访问。

9. 点击 **Create endpoint**。

</div>
</SimpleTab>

### Step 3. 创建私有端点连接 {#step-3-create-a-private-endpoint-connection-exclusive-model}

1. 返回 TiDB Cloud 控制台。
2. 在 **Create AWS Private Endpoint Connection** 页面上，输入你的 VPC 端点 ID。
3. 点击 **Create Private Endpoint Connection**。

> **Tip:**
>
> 你可以在目标 {{{ .essential }}} 实例的 **Networking** 页面上查看和管理私有端点连接。要访问此页面，请点击左侧导航栏中的 **Settings** > **Networking**。

### Step 4. 启用私有 DNS {#step-4-enable-private-dns-exclusive-model}

在 AWS 中启用私有 DNS。你可以使用 AWS CLI 或 AWS Management Console。

<SimpleTab>
<div label="Use AWS CLI">

要使用 AWS CLI 启用私有 DNS，请从 **Create Private Endpoint Connection** 页面复制以下 `aws ec2 modify-vpc-endpoint` 命令，并在 AWS CLI 中运行。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

或者，你也可以在实例的 **Networking** 页面上找到该命令。找到私有端点后，在 **Action** 列中点击 **...** > **Enable DNS**。

</div>
<div label="Use AWS Console">

要在 AWS Management Console 中启用私有 DNS：

1. 前往 **VPC** > **Endpoints**。
2. 右键点击你的端点 ID，然后选择 **Modify private DNS name**。
3. 选中 **Enable for this endpoint** 复选框。
4. 点击 **Save changes**。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### Step 5. 连接到你的 {{{ .essential }}} 实例 {#step-5-connect-to-your-essential-instance}

接受私有端点连接后，你会被重定向回连接对话框。

1. 等待私有端点连接状态从 **System Checking** 变为 **Active**（大约 5 分钟）。
2. 在 **Connect With** 下拉列表中，选择你偏好的连接方法。对应的连接字符串会显示在对话框底部。
3. 使用该连接字符串连接到你的实例。

> **Tip:**
>
> 如果你无法连接到实例，原因可能是 AWS 中 VPC 端点的安全组设置不正确。请参见[此常见问题](#troubleshooting)了解解决方法。

## 故障排查

### I cannot connect to a {{{ .starter }}} or Essential instance via a private endpoint after enabling private DNS. Why? {#i-cannot-connect-to-a-starter-or-essential-instance-via-a-private-endpoint-after-enabling-private-dns-why}

你可能需要在 AWS Management Console 中正确设置 VPC 端点的安全组。前往 **VPC** > **Endpoints**。右键点击你的 VPC 端点，然后选择合适的 **Manage security groups**。应选择 VPC 内允许你的 EC2 实例通过 Port 4000 或自定义端口进行入站访问的安全组。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
