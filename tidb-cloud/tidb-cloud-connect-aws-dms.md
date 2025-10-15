---
title: 连接 AWS DMS 到 TiDB Cloud 集群
summary: 了解如何使用 AWS Database Migration Service (AWS DMS) 从 TiDB Cloud 迁移数据或向 TiDB Cloud 迁移数据。
---

# 连接 AWS DMS 到 TiDB Cloud 集群

[AWS Database Migration Service (AWS DMS)](https://aws.amazon.com/dms/) 是一项云服务，可以实现关系型数据库、数据仓库、NoSQL 数据库以及其他类型数据存储的迁移。你可以使用 AWS DMS 将数据从 TiDB Cloud 集群迁移出去，或迁移到 TiDB Cloud 集群中。本文档介绍如何将 AWS DMS 连接到 TiDB Cloud 集群。

## 前置条件

### 拥有具备足够权限的 AWS 账号

你需要拥有一个具备足够权限以管理 DMS 相关资源的 AWS 账号。如果没有，请参考以下 AWS 文档：

- [注册 AWS 账号](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SettingUp.html#sign-up-for-aws)
- [AWS Database Migration Service 的身份与访问管理](https://docs.aws.amazon.com/dms/latest/userguide/security-iam.html)

### 拥有 TiDB Cloud 账号和 TiDB 集群

你需要拥有一个 TiDB Cloud 账号，以及 TiDB Cloud Starter、TiDB Cloud Essential 或 TiDB Cloud Dedicated 集群。如果没有，请参考以下文档进行创建：

- [创建 TiDB Cloud Starter 或 Essential 集群](/tidb-cloud/create-tidb-cluster-serverless.md)
- [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)

## 配置网络

在创建 DMS 资源之前，你需要正确配置网络，以确保 DMS 能够与 TiDB Cloud 集群通信。如果你不熟悉 AWS，建议联系 AWS 支持。以下为你提供几种可能的配置方式，供参考。

<SimpleTab>

<div label="TiDB Cloud Starter or Essential">

对于 TiDB Cloud Starter 或 TiDB Cloud Essential，你的客户端可以通过公有端点或私有端点连接到集群。

<CustomContent language="en,zh">

- 若要[通过公有端点连接 TiDB Cloud Starter 或 Essential 集群](/tidb-cloud/connect-via-standard-connection-serverless.md)，请执行以下任一操作，确保 DMS 复制实例能够访问互联网。

    - 在公有子网中部署复制实例，并启用 **Public accessible**。更多信息请参见 [互联网访问配置](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)。

    - 在私有子网中部署复制实例，并将私有子网的流量路由到公有子网。在此场景下，你至少需要三个子网：两个私有子网和一个公有子网。两个私有子网组成一个子网组，复制实例部署在其中。然后你需要在公有子网中创建一个 NAT 网关，并将两个私有子网的流量路由到该 NAT 网关。更多信息请参见 [从私有子网访问互联网](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)。

- 若要通过私有端点连接 TiDB Cloud Starter 或 Essential 集群，请先参考以下文档设置私有端点，并在私有子网中部署复制实例。

    - [通过 AWS PrivateLink 连接 TiDB Cloud Starter 或 Essential](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
    - [通过阿里云私有端点连接 TiDB Cloud Starter 或 Essential](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

</CustomContent>

<CustomContent language="ja">

- To [connect to a TiDB Cloud Starter or Essential cluster via public endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md), do one of the following to make sure that the DMS replication instance can access the internet.

    - Deploy the replication instance in public subnets and enable **Public accessible**. For more information, see [Configuration for internet access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access).

    - Deploy the replication instance in private subnets and route traffic in the private subnets to public subnets. In this case, you need at least three subnets, two private subnets, and one public subnet. The two private subnets form a subnet group where the replication instance lives. Then you need to create a NAT gateway in the public subnet and route traffic of the two private subnets to the NAT gateway. For more information, see [Access the internet from a private subnet](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access).

- To connect to a TiDB Cloud Starter or TiDB Cloud Essential cluster via private endpoint, refer to [Connect to TiDB Cloud Starter or Essential via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) to set up a private endpoint first and deploy the replication instance in private subnets.

</CustomContent>

</div>

<div label="TiDB Cloud Dedicated">

对于 TiDB Cloud Dedicated，你的客户端可以通过公有端点、私有端点或 VPC 对等连接到集群。

- 若要[通过公有端点连接 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-via-standard-connection.md)，请执行以下任一操作，确保 DMS 复制实例能够访问互联网。此外，你还需要将复制实例或 NAT 网关的公有 IP 地址添加到集群的 [IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

    - 在公有子网中部署复制实例，并启用 **Public accessible**。更多信息请参见 [互联网访问配置](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)。

    - 在私有子网中部署复制实例，并将私有子网的流量路由到公有子网。在此场景下，你至少需要三个子网：两个私有子网和一个公有子网。两个私有子网组成一个子网组，复制实例部署在其中。然后你需要在公有子网中创建一个 NAT 网关，并将两个私有子网的流量路由到该 NAT 网关。更多信息请参见 [从私有子网访问互联网](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)。

- 若要通过私有端点连接 TiDB Cloud Dedicated 集群，请先[设置私有端点](/tidb-cloud/set-up-private-endpoint-connections.md)，并在私有子网中部署复制实例。

- 若要通过 VPC 对等连接连接 TiDB Cloud Dedicated 集群，请先[设置 VPC 对等连接](/tidb-cloud/set-up-vpc-peering-connections.md)，并在私有子网中部署复制实例。

</div>
</SimpleTab>

## 创建 AWS DMS 复制实例

1. 在 AWS DMS 控制台，进入 [**Replication instances**](https://console.aws.amazon.com/dms/v2/home#replicationInstances) 页面，并切换到对应的区域。建议 AWS DMS 与 TiDB Cloud 使用相同的区域。

   ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-replication-instances.png)

2. 点击 **Create replication instance**。

3. 填写实例名称、ARN 和描述。

4. 在 **Instance configuration** 部分，配置实例：
    - **Instance class**：选择合适的实例类型。更多信息请参见 [选择复制实例类型](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.Types.html)。
    - **Engine version**：保持默认配置。
    - **High Availability**：根据你的业务需求选择 **Multi-AZ** 或 **Single-AZ**。

5. 在 **Allocated storage (GiB)** 字段配置存储空间。

6. 配置连接性和安全性。你可以参考[上一节](#configure-network)的网络配置说明。

    - **Network type - new**：选择 **IPv4**。
    - **Virtual private cloud (VPC) for IPv4**：选择你需要的 VPC。
    - **Replication subnet group**：为你的复制实例选择一个子网组。
    - **Public accessible**：根据你的网络配置进行设置。

    ![Connectivity and security](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-connectivity-security.png)

7. 如有需要，配置 **Advanced settings**、**Maintenance** 和 **Tags** 部分，然后点击 **Create replication instance** 完成实例创建。

> **注意：**
>
> AWS DMS 也支持无服务器（serverless）复制。详细步骤请参见 [创建无服务器复制](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Serverless.Components.html#CHAP_Serverless.create)。与复制实例不同，AWS DMS 无服务器复制不提供 **Public accessible** 选项。

## 创建 TiDB Cloud DMS 端点

在连接性方面，将 TiDB Cloud 集群作为源端或目标端的步骤类似，但 DMS 对源端和目标端的数据库设置有一些不同的要求。更多信息请参见 [将 MySQL 作为源端](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html) 或 [将 MySQL 作为目标端](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.MySQL.html)。当使用 TiDB Cloud 集群作为源端时，你只能选择 **Migrate existing data**，因为 TiDB 不支持 MySQL binlog。

1. 在 AWS DMS 控制台，进入 [**Endpoints**](https://console.aws.amazon.com/dms/v2/home#endpointList) 页面，并切换到对应的区域。

    ![Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-create-endpoint.png)

2. 点击 **Create endpoint** 创建目标数据库端点。

3. 在 **Endpoint type** 部分，选择 **Source endpoint** 或 **Target endpoint**。

4. 在 **Endpoint configuration** 部分，填写 **Endpoint identifier** 和 ARN 字段。然后，将 **Source engine** 或 **Target engine** 选择为 **MySQL**。

5. 在 **Access to endpoint database** 字段，勾选 **Provide access information manually**，并按如下方式填写集群信息：

    <SimpleTab>

    <div label="TiDB Cloud Starter or Essential">

    - **Server name**：集群的 `HOST`。
    - **Port**：集群的 `PORT`。
    - **User name**：用于迁移的集群用户。确保其满足 DMS 要求。
    - **Password**：集群用户的密码。
    - **Secure Socket Layer (SSL) mode**：如果你通过公有端点连接，强烈建议将模式设置为 **verify-full** 以确保传输安全。如果你通过私有端点连接，可以将模式设置为 **none**。
    - （可选）**CA certificate**：使用 [ISRG Root X1 证书](https://letsencrypt.org/certs/isrgrootx1.pem)。更多信息请参见 [TLS 连接到 TiDB Cloud Starter 或 Essential](/tidb-cloud/secure-connections-to-serverless-clusters.md)。

    </div>

    <div label="TiDB Cloud Dedicated">

    - **Server name**：TiDB Cloud Dedicated 集群的 `HOST`。
    - **Port**：TiDB Cloud Dedicated 集群的 `PORT`。
    - **User name**：用于迁移的 TiDB Cloud Dedicated 集群用户。确保其满足 DMS 要求。
    - **Password**：TiDB Cloud Dedicated 集群用户的密码。
    - **Secure Socket Layer (SSL) mode**：如果你通过公有端点连接，强烈建议将模式设置为 **verify-full** 以确保传输安全。如果你通过私有端点连接，可以将其设置为 **none**。
    - （可选）**CA certificate**：根据 [TLS 连接到 TiDB Cloud Dedicated](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md) 获取 CA 证书。

    </div>
    </SimpleTab>

     ![Provide access information manually](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-configure-endpoint.png)

6. 如果你希望将该端点创建为 **Target endpoint**，请展开 **Endpoint settings** 部分，勾选 **Use endpoint connection attributes**，然后将 **Extra connection attributes** 设置为 `Initstmt=SET FOREIGN_KEY_CHECKS=0;`。

7. 如有需要，配置 **KMS Key** 和 **Tags** 部分。点击 **Create endpoint** 完成实例创建。