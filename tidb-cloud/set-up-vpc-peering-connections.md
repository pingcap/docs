---
title: 通过 VPC Peering 连接 TiDB Cloud Dedicated
summary: 了解如何通过 VPC Peering 连接 TiDB Cloud Dedicated。
---

# 通过 VPC Peering 连接 TiDB Cloud Dedicated

> **Note:**
>
> VPC Peering 连接仅适用于托管在 AWS 和 Google Cloud 上的 TiDB Cloud Dedicated 集群。

要通过 VPC Peering 将你的应用程序连接到 TiDB Cloud，你需要与 TiDB Cloud 建立 [VPC Peering](/tidb-cloud/tidb-cloud-glossary.md#vpc-peering)。本文档将指导你在 [AWS 上设置 VPC Peering](#set-up-vpc-peering-on-aws) 和 [Google Cloud 上设置 VPC Peering](#set-up-vpc-peering-on-google-cloud)，并通过 VPC Peering 连接到 TiDB Cloud。

VPC Peering 连接是两个 VPC 之间的网络连接，使你能够使用私有 IP 地址在它们之间路由流量。任一 VPC 中的实例都可以像在同一网络中一样相互通信。

目前，同一项目下同一区域的 TiDB 集群会创建在同一个 VPC 中。因此，一旦在某个项目的某个区域设置了 VPC Peering，该项目在同一区域内创建的所有 TiDB 集群都可以通过你的 VPC 进行连接。不同云服务商的 VPC Peering 设置方式不同。

> **Tip:**
>
> 你也可以通过与 TiDB Cloud 建立 [Private Endpoint 连接](/tidb-cloud/set-up-private-endpoint-connections.md) 来连接你的应用程序到 TiDB Cloud，这种方式安全且私有，不会将你的数据暴露在公网上。推荐优先使用 Private Endpoint 连接而不是 VPC Peering 连接。

## 前置条件：为区域设置 CIDR

CIDR（无类域间路由）是用于为 TiDB Cloud Dedicated 集群创建 VPC 的 CIDR 块。

在向某个区域添加 VPC Peering 请求之前，你必须为该区域设置 CIDR，并在该区域创建首个 TiDB Cloud Dedicated 集群。首个 Dedicated 集群创建完成后，TiDB Cloud 会为该集群创建 VPC，从而允许你与应用程序的 VPC 建立 Peering 连接。

你可以在创建首个 TiDB Cloud Dedicated 集群时设置 CIDR。如果你希望在创建集群前设置 CIDR，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Network Access**。
3. 在 **Network Access** 页面，点击 **Project CIDR** 标签页，然后根据你的云服务商选择 **AWS** 或 **Google Cloud**。
4. 在右上角，点击 **Create CIDR**。在 **Create AWS CIDR** 或 **Create Google Cloud CIDR** 对话框中指定区域和 CIDR 值，然后点击 **Confirm**。

    ![Project-CIDR4](/media/tidb-cloud/Project-CIDR4.png)

    > **Note:**
    >
    > - 为避免与你应用程序所在 VPC 的 CIDR 冲突，你需要在此字段中设置不同的项目 CIDR。
    > - 对于 AWS 区域，建议配置 `/16` 到 `/23` 之间的 IP 范围。支持的网络地址包括：
    >     - 10.250.0.0 - 10.251.255.255
    >     - 172.16.0.0 - 172.31.255.255
    >     - 192.168.0.0 - 192.168.255.255
    > - 对于 Google Cloud 区域，建议配置 `/19` 到 `/20` 之间的 IP 范围。支持的网络地址包括：
    >     - 10.250.0.0 - 10.251.255.255
    >     - 172.16.0.0 - 172.17.255.255
    >     - 172.30.0.0 - 172.31.255.255
    > - TiDB Cloud 会根据区域的 CIDR 块大小限制该项目在该区域内的 TiDB Cloud 节点数量。

5. 查看云服务商及具体区域的 CIDR。

    CIDR 默认处于未激活状态。要激活 CIDR，你需要在目标区域创建集群。当区域 CIDR 激活后，你就可以为该区域创建 VPC Peering。

    ![Project-CIDR2](/media/tidb-cloud/Project-CIDR2.png)

## 在 AWS 上设置 VPC Peering

本节介绍如何在 AWS 上设置 VPC Peering 连接。关于 Google Cloud，请参见 [在 Google Cloud 上设置 VPC Peering](#set-up-vpc-peering-on-google-cloud)。

### 第 1 步：添加 VPC Peering 请求

你可以在 TiDB Cloud 控制台的项目级 **Network Access** 页面或集群级 **Networking** 页面添加 VPC Peering 请求。

<SimpleTab>
<div label="项目级 Network Access 页面设置 VPC Peering">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Network Access**。
3. 在 **Network Access** 页面，点击 **VPC Peering** 标签页，然后点击 **AWS** 子标签。

    默认会显示 **VPC Peering** 配置。

4. 在右上角，点击 **Create VPC Peering**，选择 **TiDB Cloud VPC Region**，然后填写你现有 AWS VPC 的相关信息：

    - Your VPC Region
    - AWS Account ID
    - VPC ID
    - VPC CIDR

    你可以在 [AWS 管理控制台](https://console.aws.amazon.com/) 的 VPC 详情页获取这些信息。TiDB Cloud 支持在同一区域或不同区域的 VPC 之间创建 VPC Peering。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

5. 点击 **Create** 发送 VPC Peering 请求，然后在 **VPC Peering** > **AWS** 标签页查看 VPC Peering 信息。新建的 VPC Peering 状态为 **System Checking**。

6. 若要查看新建 VPC Peering 的详细信息，在 **Action** 列点击 **...** > **View**。将显示 **VPC Peering Details** 页面。

</div>
<div label="集群级 Networking 页面设置 VPC Peering">

1. 打开目标集群的概览页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称，进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Networking**。

3. 在 **Networking** 页面，点击 **Create VPC Peering**，然后填写你现有 AWS VPC 的相关信息：

    - Your VPC Region
    - AWS Account ID
    - VPC ID
    - VPC CIDR

    你可以在 [AWS 管理控制台](https://console.aws.amazon.com/) 的 VPC 详情页获取这些信息。TiDB Cloud 支持在同一区域或不同区域的 VPC 之间创建 VPC Peering。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

4. 点击 **Create** 发送 VPC Peering 请求，然后在 **Networking** > **AWS VPC Peering** 区域查看 VPC Peering 信息。新建的 VPC Peering 状态为 **System Checking**。

5. 若要查看新建 VPC Peering 的详细信息，在 **Action** 列点击 **...** > **View**。将显示 **AWS VPC Peering Details** 页面。

</div>
</SimpleTab>

### 第 2 步：审批并配置 VPC Peering

你可以使用 AWS CLI 或 AWS 控制台来审批并配置 VPC Peering 连接。

<SimpleTab>
<div label="使用 AWS CLI">

1. 安装 AWS 命令行工具（AWS CLI）。

    
    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

2. 根据你的账户信息配置 AWS CLI。获取 AWS CLI 所需信息，请参见 [AWS CLI 配置基础](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)。

    
    ```bash
    aws configure
    ```

3. 用你的账户信息替换以下变量值。

    
    ```bash
    # Sets up the related variables.
    pcx_tidb_to_app_id="<TiDB peering id>"
    app_region="<APP Region>"
    app_vpc_id="<Your VPC ID>"
    tidbcloud_project_cidr="<TiDB Cloud Project VPC CIDR>"
    ```

    例如：

    ```
    # Sets up the related variables
    pcx_tidb_to_app_id="pcx-069f41efddcff66c8"
    app_region="us-west-2"
    app_vpc_id="vpc-0039fb90bb5cf8698"
    tidbcloud_project_cidr="10.250.0.0/16"
    ```

4. 运行以下命令。

    
    ```bash
    # Accepts the VPC peering connection request.
    aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    ```

    
    ```bash
    # Creates route table rules.
    aws ec2 describe-route-tables --region "$app_region" --filters Name=vpc-id,Values="$app_vpc_id" --query 'RouteTables[*].RouteTableId' --output text | tr "\t" "\n" | while read row
    do
        app_route_table_id="$row"
        aws ec2 create-route --region "$app_region" --route-table-id "$app_route_table_id" --destination-cidr-block "$tidbcloud_project_cidr" --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    done
    ```

    > **Note:**
    >
    > 有时，即使路由表规则已成功创建，你仍可能收到 `An error occurred (MissingParameter) when calling the CreateRoute operation: The request must contain the parameter routeTableId` 错误。此时你可以检查已创建的规则并忽略该错误。

    
    ```bash
    # Modifies the VPC attribute to enable DNS-hostname and DNS-support.
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-hostnames
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-support
    ```

完成配置后，VPC Peering 已创建。你可以 [连接到 TiDB 集群](#connect-to-the-tidb-cluster) 验证结果。

</div>
<div label="使用 AWS 控制台">

你也可以使用 AWS 控制台配置 VPC Peering 连接。

1. 在你的 [AWS 管理控制台](https://console.aws.amazon.com/) 中确认接受 Peering 连接请求。

    1. 登录 [AWS 管理控制台](https://console.aws.amazon.com/)，点击顶部菜单栏的 **Services**。在搜索框输入 `VPC` 并进入 VPC 服务页面。

        ![AWS dashboard](/media/tidb-cloud/vpc-peering/aws-vpc-guide-1.jpg)

    2. 在左侧导航栏，打开 **Peering Connections** 页面。在 **Create Peering Connection** 标签页下，Peering 连接状态为 **Pending Acceptance**。

    3. 确认请求方所有者和请求方 VPC 与 [TiDB Cloud 控制台](https://tidbcloud.com) **VPC Peering Details** 页面上的 **TiDB Cloud AWS Account ID** 和 **TiDB Cloud VPC ID** 匹配。右键点击该 Peering 连接，选择 **Accept Request**，在 **Accept VPC peering connection request** 对话框中接受请求。

        ![AWS VPC peering requests](/media/tidb-cloud/vpc-peering/aws-vpc-guide-3.png)

2. 为你的每个 VPC 子网路由表添加到 TiDB Cloud VPC 的路由。

    1. 在左侧导航栏，打开 **Route Tables** 页面。

    2. 搜索属于你的应用程序 VPC 的所有路由表。

        ![Search all route tables related to VPC](/media/tidb-cloud/vpc-peering/aws-vpc-guide-4.png)

    3. 右键点击每个路由表，选择 **Edit routes**。在编辑页面，添加一条目标为 TiDB Cloud CIDR（可在 TiDB Cloud 控制台的 **VPC Peering** 配置页面查看）的路由，并在 **Target** 列填写你的 Peering 连接 ID。

        ![Edit all route tables](/media/tidb-cloud/vpc-peering/aws-vpc-guide-5.png)

3. 确保你的 VPC 已启用私有 DNS 托管区域支持。

    1. 在左侧导航栏，打开 **Your VPCs** 页面。

    2. 选择你的应用程序 VPC。

    3. 右键点击所选 VPC，显示设置下拉列表。

    4. 在设置下拉列表中，点击 **Edit DNS hostnames**。启用 DNS hostnames 并点击 **Save**。

    5. 在设置下拉列表中，点击 **Edit DNS resolution**。启用 DNS resolution 并点击 **Save**。

现在你已成功设置 VPC Peering 连接。接下来，[通过 VPC Peering 连接到 TiDB 集群](#connect-to-the-tidb-cluster)。

</div>
</SimpleTab>

## 在 Google Cloud 上设置 VPC Peering

### 第 1 步：添加 VPC Peering 请求

你可以在 TiDB Cloud 控制台的项目级 **Network Access** 页面或集群级 **Networking** 页面添加 VPC Peering 请求。

<SimpleTab>
<div label="项目级 Network Access 页面设置 VPC Peering">

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏，点击 **Project Settings** > **Network Access**。
3. 在 **Network Access** 页面，点击 **VPC Peering** 标签页，然后点击 **Google Cloud** 子标签。

    默认会显示 **VPC Peering** 配置。

4. 在右上角，点击 **Create VPC Peering**，选择 **TiDB Cloud VPC Region**，然后填写你现有 Google Cloud VPC 的相关信息：

    > **Tip:**
    >
    > 你可以按照 **Google Cloud Project ID** 和 **VPC Network Name** 字段旁的说明查找项目 ID 和 VPC 网络名称。

    - Google Cloud Project ID
    - VPC Network Name
    - VPC CIDR

5. 点击 **Create** 发送 VPC Peering 请求，然后在 **VPC Peering** > **Google Cloud** 标签页查看 VPC Peering 信息。新建的 VPC Peering 状态为 **System Checking**。

6. 若要查看新建 VPC Peering 的详细信息，在 **Action** 列点击 **...** > **View**。将显示 **VPC Peering Details** 页面。

</div>
<div label="集群级 Networking 页面设置 VPC Peering">

1. 打开目标集群的概览页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，进入项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

        > **Tip:**
        >
        > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    2. 点击目标集群名称，进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Networking**。

3. 在 **Networking** 页面，点击 **Create VPC Peering**，然后填写你现有 Google Cloud VPC 的相关信息：

    > **Tip:**
    >
    > 你可以按照 **Google Cloud Project ID** 和 **VPC Network Name** 字段旁的说明查找项目 ID 和 VPC 网络名称。

    - Google Cloud Project ID
    - VPC Network Name
    - VPC CIDR

4. 点击 **Create** 发送 VPC Peering 请求，然后在 **Networking** > **Google Cloud VPC Peering** 区域查看 VPC Peering 信息。新建的 VPC Peering 状态为 **System Checking**。

5. 若要查看新建 VPC Peering 的详细信息，在 **Action** 列点击 **...** > **View**。将显示 **Google Cloud VPC Peering Details** 页面。

</div>
</SimpleTab>

### 第 2 步：审批 VPC Peering

执行以下命令完成 VPC Peering 的设置：

```bash
gcloud beta compute networks peerings create <your-peer-name> --project <your-project-id> --network <your-vpc-network-name> --peer-project <tidb-project-id> --peer-network <tidb-vpc-network-name>
```

> **Note:**
>
> `<your-peer-name>` 可以自定义命名。

现在你已成功设置 VPC Peering 连接。接下来，[通过 VPC Peering 连接到 TiDB 集群](#connect-to-the-tidb-cluster)。

## 连接到 TiDB 集群

1. 在项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称，进入其概览页面。

2. 点击右上角的 **Connect**，并在 **Connection Type** 下拉列表中选择 **VPC Peering**。

    等待 VPC Peering 连接状态从 **system checking** 变为 **active**（大约 5 分钟）。

3. 在 **Connect With** 下拉列表中，选择你偏好的连接方式。对话框底部会显示相应的连接字符串。

4. 使用该连接字符串连接到你的集群。