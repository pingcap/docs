---
title: Dataflow 的私有链路连接
summary: 了解如何为 Dataflow 设置私有链路连接。
---

# Dataflow 的私有链路连接

TiDB Cloud 中的数据流服务（如 Changefeed 和 Data Migration (DM)）需要与外部资源（如 RDS 实例和 Kafka 集群）建立可靠的连接。虽然支持公网端点，但私有链路连接提供了更优的选择，具有效率更高、延时更低和安全性更强的优势。

私有链路连接可以在 TiDB Cloud Essential 与你的目标资源之间建立直接连接。这确保了从 TiDB Cloud 到你在其他云平台上的数据库的数据始终在私有网络边界内传输，大幅降低了网络攻击面，并为关键数据流工作负载提供了稳定的吞吐。

## 私有链路连接类型

数据流的私有链路连接有多种类型，具体取决于云服务商和你要访问的服务。每种类型都能在你的 TiDB Cloud 集群与同一云环境中的外部资源（如 RDS 或 Kafka）之间实现安全、私有的网络访问。

### AWS Endpoint Service

此类型的私有链路连接允许部署在 **AWS** 上的 TiDB Cloud 集群连接到你基于 AWS PrivateLink 的 [AWS endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html)。

通过将 AWS 各类服务（如 RDS 实例和 Kafka 服务）与 endpoint service 关联，私有链路连接即可访问这些服务。

### 阿里云 Endpoint Service

此类型的私有链路连接允许部署在 **阿里云** 上的 TiDB Cloud 集群连接到你基于阿里云 PrivateLink 的 [阿里云 endpoint service](https://www.alibabacloud.com/help/en/privatelink/share-your-service/#51976edba8no7)。

通过将阿里云各类服务（如 RDS 实例和 Kafka 服务）与 endpoint service 关联，私有链路连接即可访问这些服务。

## 创建 AWS Endpoint Service 私有链路连接

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 创建 AWS Endpoint Service 私有链路连接。

请确保 AWS endpoint service：

- 与你的 TiDB Cloud 集群处于同一区域。
- 将 TiDB Cloud 账户 ID 添加到 **Allow principals** 列表。
- 拥有与你的 TiDB Cloud 集群重叠的可用区。

你可以在 **Create Private Link Connection** 对话框底部获取账户 ID 和可用区信息，或通过以下命令获取：

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **Networking**。

3. 在 **Private Link Connection For Dataflow** 区域，点击 **Create Private Link Connection**。

4. 在 **Create Private Link Connection** 对话框中，填写所需信息：

    - **Private Link Connection Name**：输入私有链路连接的名称。
    - **Connection Type**：选择 **AWS Endpoint Service**。如果未显示该选项，请确保你的集群部署在 AWS 上。
    - **Endpoint Service Name**：输入你的 AWS endpoint service 名称，例如 `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`。

5. 点击 **Create**。

6. 前往 [AWS 控制台](https://console.aws.amazon.com) 的 endpoint service 详情页。在 **Endpoint Connections** 标签页，接受来自 TiDB Cloud 的 endpoint connection request。

</div>

<div label="CLI">

通过 TiDB Cloud CLI 创建私有链路连接：

1. 执行以下命令：

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
    ```

2. 前往 [AWS 控制台](https://console.aws.amazon.com) 的 endpoint service 详情页。在 **Endpoint Connections** 标签页，接受来自 TiDB Cloud 的 endpoint connection request。

</div>
</SimpleTab>

## 创建阿里云 Endpoint Service 私有链路连接

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 创建阿里云 Endpoint Service 私有链路连接。

请确保阿里云 endpoint service：

- 与你的 TiDB Cloud 集群处于同一区域。
- 将 TiDB Cloud 账户 ID 添加到 **Service Whitelist**。
- 拥有与你的 TiDB Cloud 集群重叠的可用区。

你可以在 **Create Private Link Connection** 对话框底部获取账户 ID 和可用区信息，或通过以下命令获取：

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

<SimpleTab>
<div label="Console">

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **Networking**。

3. 在 **Private Link Connection For Dataflow** 区域，点击 **Create Private Link Connection**。

4. 在 **Create Private Link Connection** 对话框中，填写所需信息：

    - **Private Link Connection Name**：输入私有链路连接的名称。
    - **Connection Type**：选择 **Alibaba Cloud Endpoint Service**。如果未显示该选项，请确保你的集群部署在阿里云上。
    - **Endpoint Service Name**：输入阿里云 endpoint service 名称，例如 `com.aliyuncs.privatelink.<region>.epsrv-xxxxxxxxxxxxxxxxx`。

5. 点击 **Create**。

6. 前往 [阿里云控制台](https://console.alibabacloud.com) 的 endpoint service 详情页。在 **Endpoint Connections** 标签页，允许来自 TiDB Cloud 的 endpoint connection request。

</div>

<div label="CLI">

通过 TiDB Cloud CLI 创建私有链路连接：

1. 执行以下命令：

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type ALICLOUD_ENDPOINT_SERVICE --alicloud.endpoint-service-name <endpoint-service-name>
    ```

2. 前往 [阿里云控制台](https://console.alibabacloud.com) 的 endpoint service 详情页。在 **Endpoint Connections** 标签页，允许来自 TiDB Cloud 的 endpoint connection request。

</div>
</SimpleTab>

## 绑定域名到私有链路连接

你可以将域名绑定到私有链路连接。当域名绑定到私有链路连接后，所有来自 TiDB Cloud 数据流服务到该域名的流量都将路由到此私有链路连接。当你的服务在运行时为 client 提供自定义域名（如 Kafka advertised listeners）时，这一功能非常有用。

不同类型的私有链路连接支持绑定不同类型的域名。下表展示了每种私有链路连接类型支持的域名类型。

| 私有链路连接类型                | 支持的域名类型                                         |
|--------------------------------|------------------------------------------------------|
| AWS Endpoint Service           | <ul><li>TiDB Cloud managed (`aws.tidbcloud.com`)</li><li>Confluent Dedicated (`aws.confluent.cloud`)</li></ul>  |
| 阿里云 Endpoint Service        | TiDB Cloud managed (`alicloud.tidbcloud.com`)         |

如果你的域名未包含在此表中，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) 申请支持。

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 将域名绑定到私有链路连接。

<SimpleTab>
<div label="Console">

通过 TiDB Cloud 控制台将域名绑定到私有链路连接，操作如下：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **Networking**。

3. 在 **Private Link Connection For Dataflow** 区域，选择目标私有链路连接，然后点击 **...**。

4. 点击 **Attach Domains**。

5. 在 **Attach Domains** 对话框中，选择域名类型：

    - **TiDB Cloud Managed**：域名将由 TiDB Cloud 自动生成。在生成的域名中，你可以获取该域名的唯一名称。例如，若生成的域名为 `*.use1-az1.dvs6nl5jgveztmla3pxkxgh76i.aws.plc.tidbcloud.com`，则唯一名称为 `dvs6nl5jgveztmla3pxkxgh76i`。点击 **Attach Domains** 进行确认。
    - **Confluent Cloud**：输入 Confluent Cloud Dedicated 集群提供的唯一名称以生成域名，然后点击 **Attach Domains** 进行确认。关于如何获取唯一名称，参见 [通过私有链路连接接入 Confluent Cloud](/tidb-cloud/serverless-private-link-connection-to-aws-confluent.md#step-1-set-up-a-confluent-cloud-network)。

</div>

<div label="CLI">

通过 TiDB Cloud CLI 绑定 TiDB Cloud managed 域名，操作如下：

1. 使用 `dry run` 预览将要绑定的域名。该命令会输出下一步所需的唯一名称。

    ```shell
    ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --dry-run
    ```

2. 使用上一步获取的唯一名称绑定域名。

    ```shell
    ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --unique-name <unique-name>
    ```

如需绑定 Confluent Cloud 域名，执行以下命令：

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type CONFLUENT --unique-name <unique-name>
```

</div>
</SimpleTab>

## 从私有链路连接解绑域名

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 从私有链路连接解绑域名。

<SimpleTab>
<div label="Console">

通过 TiDB Cloud 控制台从私有链路连接解绑域名，操作如下：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **Networking**。

3. 在 **Private Link Connection For Dataflow** 区域，选择目标私有链路连接，然后点击 **...**。

4. 点击 **Detach Domains**，并确认解绑。

</div>

<div label="CLI">

通过 TiDB Cloud CLI 从私有链路连接解绑域名，操作如下：

1. 获取私有链路连接详情，查找 `attach-domain-id`：

    ```shell
    ticloud serverless private-link-connection get -c <cluster-id> --private-link-connection-id <private-link-connection-id>
    ```

2. 根据 `attach-domain-id` 解绑域名：

    ```shell
     ticloud serverless private-link-connection detach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --attach-domain-id <attach-domain-id>
    ```

</div>
</SimpleTab>

## 删除私有链路连接

你可以通过 TiDB Cloud 控制台或 TiDB Cloud CLI 删除私有链路连接。

<SimpleTab>
<div label="Console">

通过 TiDB Cloud 控制台删除私有链路连接，操作如下：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击目标集群名称进入概览页面，然后在左侧导航栏点击 **Settings** > **Networking**。

3. 在 **Private Link Connection For Dataflow** 区域，选择目标私有链路连接，然后点击 **...**。

4. 点击 **Delete**，并确认删除。

</div>

<div label="CLI">

如需删除私有链路连接，执行以下命令：

```shell
ticloud serverless private-link-connection delete -c <cluster-id> --private-link-connection-id <private-link-connection-id>
```

</div>
</SimpleTab>

## 参见

- [通过私有链路连接接入 Confluent Cloud](/tidb-cloud/serverless-private-link-connection-to-aws-confluent.md)
- [通过私有链路连接接入 Amazon RDS](/tidb-cloud/serverless-private-link-connection-to-aws-rds.md)
- [通过私有链路连接接入阿里云 ApsaraDB RDS for MySQL](/tidb-cloud/serverless-private-link-connection-to-alicloud-rds.md)
- [通过私有链路连接接入 AWS 自建 Kafka](/tidb-cloud/serverless-private-link-connection-to-self-hosted-kafka-in-aws.md)
- [通过私有链路连接接入阿里云自建 Kafka](/tidb-cloud/serverless-private-link-connection-to-self-hosted-kafka-in-alicloud.md)
