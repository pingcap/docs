---
title: 通过 AWS PrivateLink 连接到 {{{ .premium }}}
summary: 了解如何通过 AWS 的私有端点连接到你的 {{{ .premium }}} 实例。
---

# 通过 AWS PrivateLink 连接到 {{{ .premium }}}

本文档介绍如何通过 [AWS PrivateLink](https://aws.amazon.com/privatelink) 连接到你的 {{{ .premium }}} 实例。

> **Tip:**
>
> 如需了解如何通过 AWS PrivateLink 连接到 {{{ .starter }}} 或 {{{ .essential }}} 实例，请参见 [Connect to {{{ .starter }}} or Essential via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。

TiDB Cloud 支持通过 [AWS PrivateLink](https://aws.amazon.com/privatelink) 以高度安全的单向方式访问托管在 AWS VPC 中的 TiDB Cloud 服务，就像该服务位于你自己的 VPC 中一样。你的 VPC 中会暴露一个私有端点，在获得权限后，你可以通过该端点创建到 TiDB Cloud 服务的连接。

借助 AWS PrivateLink，端点连接是安全且私有的，不会将你的数据暴露到公共互联网。此外，端点连接支持 CIDR 重叠，并且更便于网络管理。

私有端点的架构如下：

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

有关私有端点和端点服务的更详细定义，请参见以下 AWS 文档：

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 限制 {#restrictions}

- 只有具有 `Organization Owner` 角色的用户才能创建私有端点连接。
- 私有端点和你要连接的 {{{ .premium }}} 实例必须位于同一区域。

## 前提条件 {#prerequisites}

请确保在 AWS VPC 设置中同时启用了 DNS hostnames 和 DNS resolution。在 [AWS Management Console](https://console.aws.amazon.com/) 中创建 VPC 时，这两项默认是禁用的。

## 设置私有端点连接并连接到你的实例 {#set-up-a-private-endpoint-connection-and-connect-to-your-instance}

要通过私有端点连接到你的 {{{ .premium }}} 实例，请按以下步骤操作：

1. [选择一个 {{{ .premium }}} 实例](#step-1-select-a-premium-instance)
2. [创建 AWS interface endpoint](#step-2-create-an-aws-interface-endpoint)
3. [创建私有端点连接](#step-3-create-a-private-endpoint-connection)
4. [启用 private DNS](#step-4-enable-private-dns)
5. [连接到你的 {{{ .premium }}} 实例](#step-5-connect-to-your-premium-instance)

如果你有多个实例，则需要对每个希望通过 AWS PrivateLink 连接的实例重复这些步骤。

### 步骤 1. 选择一个 {{{ .premium }}} 实例 {#step-1-select-a-premium-instance}

1. 在 TiDB Cloud 控制台的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面上，点击目标 {{{ .premium }}} 实例的名称，进入其概览页面。
2. 点击右上角的 **Connect**。此时会显示连接对话框。
3. 在 **Connection Type** 下拉列表中，选择 **Private Endpoint**，然后点击 **Create Private Endpoint Connection**。

> **Note:**
>
> 如果你已经创建了私有端点连接，活动端点会显示在连接对话框中。要创建额外的私有端点连接，请在左侧导航栏中点击 **Settings** > **Networking**，进入 **Networking** 页面。

### 步骤 2. 创建 AWS interface endpoint {#step-2-create-an-aws-interface-endpoint}

> **Note:**
>
> 对于每个 {{{ .premium }}} 实例，相应的端点服务会在实例创建后 3 到 4 分钟自动创建。

如果你看到 `TiDB Private Link Service is ready` 消息，则表示相应的端点服务已就绪。你可以提供以下信息来创建端点。

1. 填写 **Your VPC ID** 和 **Your Subnet IDs** 字段。你可以在 [AWS Management Console](https://console.aws.amazon.com/) 中找到这些 ID。对于多个子网，请输入以空格分隔的 ID。
2. 点击 **Generate Command** 获取以下端点创建命令。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

然后，你可以使用 AWS CLI 或 [AWS Management Console](https://aws.amazon.com/console/) 创建 AWS interface endpoint。

<SimpleTab>
<div label="Use AWS CLI">

要使用 AWS CLI 创建 VPC interface endpoint，请执行以下步骤：

1. 复制生成的命令并在终端中运行。
2. 记录你刚刚创建的 VPC endpoint ID。

> **Tip:**
>
> - 在运行命令之前，你需要先安装并配置 AWS CLI。详情请参见 [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。
>
> - 如果你的服务跨越三个以上的 availability zone (AZ)，你会收到一条错误消息，提示 VPC endpoint service 不支持该子网所在的 AZ。当你所选区域中存在一个额外的 AZ，而该 AZ 不在你的 {{{ .premium }}} 实例所在的 AZ 范围内时，就会出现此问题。在这种情况下，你可以联系 [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

</div>
<div label="Use AWS Console">

要使用 AWS Management Console 创建 VPC interface endpoint，请执行以下步骤：

1. 登录 [AWS Management Console](https://aws.amazon.com/console/)，并在 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/) 打开 Amazon VPC 控制台。
2. 在导航窗格中点击 **Endpoints**，然后点击右上角的 **Create Endpoint**。

    此时会显示 **Create endpoint** 页面。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. 在 **Endpoint settings** 区域中，根据需要填写名称标签，然后选择 **Endpoint services that use NLBs and GWLBs** 选项。
4. 在 **Service settings** 区域中，输入生成命令中的服务名称 `${your_endpoint_service_name}`（`--service-name ${your_endpoint_service_name}`）。
5. 点击 **Verify service**。
6. 在 **Network settings** 区域中，在下拉列表中选择你的 VPC。
7. 在 **Subnets** 区域中，选择你的 {{{ .premium }}} 实例所在的可用区。

    > **Tip:**
    >
    > 如果你的服务跨越三个以上的 availability zone (AZ)，你可能无法在 **Subnets** 区域中选择 AZ。当你所选区域中存在一个额外的 AZ，而该 AZ 不在你的 {{{ .premium }}} 实例所在的 AZ 范围内时，就会出现此问题。在这种情况下，请联系 [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)。

8. 在 **Security groups** 区域中，正确选择你的安全组。

    > **Note:**
    >
    > 请确保所选安全组允许你的 EC2 实例通过端口 `4000` 或客户自定义端口进行入站访问。

9. 点击 **Create endpoint**。

</div>
</SimpleTab>

### 步骤 3. 创建私有端点连接 {#step-3-create-a-private-endpoint-connection}

1. 返回 TiDB Cloud 控制台。
2. 在 **Create AWS Private Endpoint Connection** 页面上，输入你的 VPC endpoint ID。
3. 点击 **Create Private Endpoint Connection**。

> **Tip:**
>
> 你可以在目标 {{{ .premium }}} 实例的 **Networking** 页面查看和管理私有端点连接。要访问此页面，请在左侧导航栏中点击 **Settings** > **Networking**。

### 步骤 4. 启用 private DNS {#step-4-enable-private-dns}

在 AWS 中启用 private DNS。你可以使用 AWS CLI，也可以使用 AWS Management Console。

<SimpleTab>
<div label="Use AWS CLI">

要使用 AWS CLI 启用 private DNS，请从 **Create Private Endpoint Connection** 页面复制以下 `aws ec2 modify-vpc-endpoint` 命令，并在 AWS CLI 中运行。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

或者，你也可以在实例的 **Networking** 页面找到该命令。找到私有端点后，在 **Action** 列中点击 **...** > **Enable DNS**。

</div>
<div label="Use AWS Console">

要在 AWS Management Console 中启用 private DNS：

1. 前往 **VPC** > **Endpoints**。
2. 右键点击你的 endpoint ID，然后选择 **Modify private DNS name**。
3. 选中 **Enable for this endpoint** 复选框。
4. 点击 **Save changes**。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### 步骤 5. 连接到你的 {{{ .premium }}} 实例 {#step-5-connect-to-your-premium-instance}

接受私有端点连接后，你会被重定向回连接对话框。

1. 等待私有端点连接状态从 **System Checking** 变为 **Active**（大约 5 分钟）。
2. 在 **Connect With** 下拉列表中，选择你偏好的连接方式。相应的连接字符串会显示在对话框底部。
3. 使用该连接字符串连接到你的实例。

> **Tip:**
>
> 如果你无法连接到实例，原因可能是 AWS 中你的 VPC endpoint 的安全组设置不正确。解决方案请参见[此 FAQ](#troubleshooting)。

### 私有端点状态参考 {#private-endpoint-status-reference}

使用私有端点连接时，私有端点和私有端点服务的状态会显示在实例级别的 **Networking** 页面上：

1. 进入你组织的 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .premium }}} 实例的名称，进入其概览页面。
2. 在左侧导航栏中点击 **Settings** > **Networking**。

私有端点的可能状态说明如下：

- **Not Configured**：端点服务已创建，但私有端点尚未创建。
- **Pending**：等待处理。
- **Active**：你的私有端点已可用。在此状态下，你不能编辑私有端点。
- **Deleting**：私有端点正在删除中。
- **Failed**：私有端点创建失败。你可以点击该行中的 **Edit** 重试创建。

私有端点服务的可能状态说明如下：

- **Creating**：端点服务正在创建中，耗时 3 到 5 分钟。
- **Active**：端点服务已创建，无论私有端点是否已创建。
- **Deleting**：端点服务或实例正在删除中，耗时 3 到 5 分钟。

## 故障排查 {#troubleshooting}

### 启用 private DNS 后，我为什么仍然无法通过私有端点连接到 {{{ .premium }}} 实例？ {#i-cannot-connect-to-a-premium-instance-via-a-private-endpoint-after-enabling-private-dns-why}

你可能需要在 AWS Management Console 中正确设置 VPC endpoint 的安全组。为此，请前往 **VPC** > **Endpoints**，右键点击你的 VPC endpoint，然后选择 **Manage security groups**。确保所选安全组允许你的 EC2 实例通过端口 `4000` 或客户自定义端口进行入站访问。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)