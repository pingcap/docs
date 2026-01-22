---
title: 在 AWS 中搭建自托管 Kafka Private Link 服务
summary: 本文档介绍如何在 AWS 中为自托管 Kafka 搭建 Private Link 服务，并使其与 TiDB Cloud 协同工作。
aliases: ['/tidbcloud/setup-self-hosted-kafka-private-link-service']
---

# 在 AWS 中搭建自托管 Kafka Private Link 服务

本文档描述了如何在 AWS 中为自托管 Kafka 搭建 Private Link 服务，以及如何使其与 TiDB Cloud 协同工作。

其机制如下：

1. TiDB Cloud VPC 通过私有端点连接到 Kafka VPC。
2. Kafka client 需要直接与所有 Kafka broker 进行通信。
3. 每个 Kafka broker 映射到 TiDB Cloud VPC 内端点的唯一端口。
4. 利用 Kafka 启动/引导程序机制和 AWS 资源实现端口映射。

下图展示了该机制。

![Connect to AWS Self-Hosted Kafka Private Link Service](/media/tidb-cloud/changefeed/connect-to-aws-self-hosted-kafka-privatelink-service.jpeg)

本文以在 AWS 三个可用区（AZ）部署的 Kafka Private Link 服务为例进行说明。你也可以基于类似的端口映射原理进行其他配置，但本文主要覆盖 Kafka Private Link 服务的基础搭建流程。对于生产环境，建议搭建更具弹性、可维护性和可观测性的 Kafka Private Link 服务。

## 前置条件

<CustomContent plan="dedicated">

1. 确保你拥有在自己的 AWS 账户中搭建 Kafka Private Link 服务的以下权限。

    - 管理 EC2 节点
    - 管理 VPC
    - 管理子网
    - 管理安全组
    - 管理负载均衡器
    - 管理端点服务
    - 连接 EC2 节点以配置 Kafka 节点

2. 如果你还没有 TiDB Cloud Dedicated 集群，请[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。

3. 从你的 TiDB Cloud Dedicated 集群获取 Kafka 部署信息。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入 TiDB 集群的概览页面，然后点击左侧导航栏的 **Data** > **Changefeed**。
    2. 在概览页面，找到 TiDB 集群的 Region。确保你的 Kafka 集群将部署在同一 Region。
    3. 点击 **Create Changefeed**。
        1. 在 **Destination** 选择 **Kafka**。
        2. 在 **Connectivity Method** 选择 **Private Link**。
    4. 记下 **Reminders before proceeding** 中 TiDB Cloud AWS 账户的信息。你需要用它来授权 TiDB Cloud 创建 Kafka Private Link 服务的端点。
    5. 选择 **Number of AZs**。本例选择 **3 AZs**。记下你希望部署 Kafka 集群的 AZ ID。如果你想了解 AZ 名称与 AZ ID 的对应关系，请参见 [Availability Zone IDs for your AWS resources](https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html)。
    6. 为你的 Kafka Private Link 服务输入唯一的 **Kafka Advertised Listener Pattern**。
        1. 输入一个唯一的随机字符串，只能包含数字或小写字母。你将用它来生成 **Kafka Advertised Listener Pattern**。
        2. 点击 **Check usage and generate** 检查该随机字符串是否唯一，并生成用于组装 Kafka broker EXTERNAL advertised listener 的 **Kafka Advertised Listener Pattern**。

</CustomContent>
<CustomContent plan="premium">

1. 确保你拥有在自己的 AWS 账户中搭建 Kafka Private Link 服务的以下权限。

    - 管理 EC2 节点
    - 管理 VPC
    - 管理子网
    - 管理安全组
    - 管理负载均衡器
    - 管理端点服务
    - 连接 EC2 节点以配置 Kafka 节点

2. 如果你还没有 TiDB Cloud Premium 实例，请[创建 TiDB Cloud Premium 实例](/tidb-cloud/premium/create-tidb-instance-premium.md)。

3. 从你的 TiDB Cloud Premium 实例获取 Kafka 部署信息。

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入 TiDB 实例的概览页面，然后点击左侧导航栏的 **Data** > **Changefeed**。
    2. 在概览页面，找到 TiDB 实例的 Region。确保你的 Kafka 集群将部署在同一 Region。
    3. 创建 changefeed，请参考以下教程：

        - [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)

</CustomContent>

请记录所有部署信息，后续配置 Kafka Private Link 服务时需要用到。

下表为部署信息示例。

| 信息     | 值    | 备注    | 
|--------|-----------------|---------------------------|
| Region    | Oregon (`us-west-2`)    |  N/A |
| TiDB Cloud AWS 账户的 Principal | `arn:aws:iam::<account_id>:root`     |    N/A  |
| AZ IDs                              | <ul><li>`usw2-az1` </li><li>`usw2-az2` </li><li> `usw2-az3`</li></ul>  | 将 AZ ID 与 AWS 账户中的 AZ 名称对应。<br/>示例：<ul><li> `usw2-az1` => `us-west-2a` </li><li> `usw2-az2` => `us-west-2c` </li><li>`usw2-az3` => `us-west-2b`</li></ul>  |
| Kafka Advertised Listener Pattern   | 唯一随机字符串: `abc` <br/>为各 AZ 生成的 pattern: <ul><li> `usw2-az1` => &lt;broker_id&gt;.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li><li> `usw2-az2` => &lt;broker_id&gt;.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li><li> `usw2-az3` => &lt;broker_id&gt;.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li></ul>    | 将 AZ 名称映射到对应的 AZ pattern。确保后续在特定 AZ 的 broker 上配置正确的 pattern。<ul><li> `us-west-2a` => &lt;broker_id&gt;.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li><li> `us-west-2c` => &lt;broker_id&gt;.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li><li> `us-west-2b` => &lt;broker_id&gt;.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:&lt;port&gt; </li></ul>|

## 步骤 1. 搭建 Kafka 集群

如果你需要部署新集群，请参考 [部署新 Kafka 集群](#deploy-a-new-kafka-cluster)。

如果你需要暴露已有集群，请参考 [重配置运行中的 Kafka 集群](#reconfigure-a-running-kafka-cluster)。

### 部署新 Kafka 集群

#### 1. 搭建 Kafka VPC

Kafka VPC 需要满足以下要求：

- 为 broker 准备三个私有子网，每个 AZ 一个。
- 在任意 AZ 创建一个公有子网，部署堡垒机节点，该节点可连接互联网和三个私有子网，便于搭建 Kafka 集群。在生产环境中，你可以有自己的堡垒机节点连接 Kafka VPC。

在创建子网前，请根据 AZ ID 与 AZ 名称的映射关系创建子网。以如下映射为例：

- `usw2-az1` => `us-west-2a`
- `usw2-az2` => `us-west-2c`
- `usw2-az3` => `us-west-2b`

在以下 AZ 创建私有子网：

- `us-west-2a`
- `us-west-2c`
- `us-west-2b`

按如下步骤创建 Kafka VPC。

**1.1. 创建 Kafka VPC**

1. 进入 [AWS 控制台 > VPC 控制面板](https://console.aws.amazon.com/vpcconsole/home?#vpcs:)，切换到你希望部署 Kafka 的 Region。

2. 点击 **Create VPC**。在 **VPC settings** 页面填写如下信息：

    1. 选择 **VPC only**。
    2. **Name tag** 输入标签，例如 `Kafka VPC`。
    3. 选择 **IPv4 CIDR manual input**，输入 IPv4 CIDR，例如 `10.0.0.0/16`。
    4. 其他选项保持默认。点击 **Create VPC**。
    5. 在 VPC 详情页，记下 VPC ID，例如 `vpc-01f50b790fa01dffa`。

**1.2. 在 Kafka VPC 中创建私有子网**

1. 进入 [Subnets 列表页](https://console.aws.amazon.com/vpcconsole/home?#subnets:)。
2. 点击 **Create subnet**。
3. 选择之前记录的 **VPC ID**（本例为 `vpc-01f50b790fa01dffa`）。
4. 添加三个子网，信息如下。建议在子网名称中加入 AZ ID，便于后续配置 broker，因为 TiDB Cloud 要求在 broker 的 `advertised.listener` 配置中编码 AZ ID。

    - `us-west-2a` 的子网
        - **Subnet name**: `broker-usw2-az1`
        - **Availability Zone**: `us-west-2a`
        - **IPv4 subnet CIDR block**: `10.0.0.0/18`

    - `us-west-2c` 的子网
        - **Subnet name**: `broker-usw2-az2`
        - **Availability Zone**: `us-west-2c`
        - **IPv4 subnet CIDR block**: `10.0.64.0/18`

    - `us-west-2b` 的子网
        - **Subnet name**: `broker-usw2-az3`
        - **Availability Zone**: `us-west-2b`
        - **IPv4 subnet CIDR block**: `10.0.128.0/18`

5. 点击 **Create subnet**。进入 **Subnets Listing** 页面。

**1.3. 在 Kafka VPC 中创建公有子网**

1. 点击 **Create subnet**。
2. 选择之前记录的 **VPC ID**（本例为 `vpc-01f50b790fa01dffa`）。
3. 在任意 AZ 添加公有子网，信息如下：

   - **Subnet name**: `bastion`
   - **IPv4 subnet CIDR block**: `10.0.192.0/18`

4. 将 bastion 子网配置为公有子网。

    1. 进入 [VPC 控制台 > Internet gateways](https://console.aws.amazon.com/vpcconsole/home#igws:)，创建名为 `kafka-vpc-igw` 的 Internet Gateway。
    2. 在 **Internet gateways Detail** 页面，点击 **Actions** 下的 **Attach to VPC**，将 Internet Gateway 关联到 Kafka VPC。
    3. 进入 [VPC 控制台 > Route tables](https://console.aws.amazon.com/vpcconsole/home#CreateRouteTable:)，在 Kafka VPC 中创建路由表并添加如下路由：

       - **Name**: `kafka-vpc-igw-route-table`
       - **VPC**: `Kafka VPC`
       - **Route**: 
           - **Destination**: `0.0.0.0/0`
           - **Target**: `Internet Gateway`, `kafka-vpc-igw`

    4. 将路由表关联到 bastion 子网。在路由表详情页，点击 **Subnet associations > Edit subnet associations**，添加 bastion 子网并保存。

#### 2. 搭建 Kafka broker

**2.1. 创建堡垒机节点**

进入 [EC2 列表页](https://console.aws.amazon.com/ec2/home#Instances:)，在 bastion 子网中创建堡垒机节点。

- **Name**: `bastion-node`
- **Amazon Machine Image**: `Amazon Linux`
- **Instance Type**: `t2.small`
- **Key pair**: `kafka-vpc-key-pair`。新建名为 `kafka-vpc-key-pair` 的密钥对，并下载 `kafka-vpc-key-pair.pem` 到本地，后续配置用。
- 网络设置

    - **VPC**: `Kafka VPC`
    - **Subnet**: `bastion`
    - **Auto-assign public IP**: `Enable`
    - **Security Group**: 新建安全组，允许任意来源 SSH 登录。生产环境可收紧规则。

**2.2. 创建 broker 节点**

进入 [EC2 列表页](https://console.aws.amazon.com/ec2/home#Instances:)，在 broker 子网中创建三个 broker 节点，每个 AZ 一个。

- 子网 `broker-usw2-az1` 的 broker 1

    - **Name**: `broker-node1`
    - **Amazon Machine Image**: `Amazon Linux`
    - **Instance Type**: `t2.large`
    - **Key pair**: 复用 `kafka-vpc-key-pair`
    - 网络设置

        - **VPC**: `Kafka VPC`
        - **Subnet**: `broker-usw2-az1`
        - **Auto-assign public IP**: `Disable`
        - **Security Group**: 新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境可收紧规则。
            - **Protocol**: `TCP`
            - **Port range**: `0 - 65535`
            - **Source**: `10.0.0.0/16`

- 子网 `broker-usw2-az2` 的 broker 2

    - **Name**: `broker-node2`
    - **Amazon Machine Image**: `Amazon Linux`
    - **Instance Type**: `t2.large`
    - **Key pair**: 复用 `kafka-vpc-key-pair`
    - 网络设置

        - **VPC**: `Kafka VPC`
        - **Subnet**: `broker-usw2-az2`
        - **Auto-assign public IP**: `Disable`
        - **Security Group**: 新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境可收紧规则。
            - **Protocol**: `TCP`
            - **Port range**: `0 - 65535`
            - **Source**: `10.0.0.0/16`

- 子网 `broker-usw2-az3` 的 broker 3

    - **Name**: `broker-node3`
    - **Amazon Machine Image**: `Amazon Linux`
    - **Instance Type**: `t2.large`
    - **Key pair**: 复用 `kafka-vpc-key-pair`
    - 网络设置

        - **VPC**: `Kafka VPC`
        - **Subnet**: `broker-usw2-az3`
        - **Auto-assign public IP**: `Disable`
        - **Security Group**: 新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境可收紧规则。
            - **Protocol**: `TCP`
            - **Port range**: `0 - 65535`
            - **Source**: `10.0.0.0/16`

**2.3. 准备 Kafka 运行时二进制文件**

1. 进入堡垒机节点详情页，获取 **Public IPv4 address**。使用 SSH 登录该节点，并用之前下载的 `kafka-vpc-key-pair.pem`。

    ```shell
    chmod 400 kafka-vpc-key-pair.pem
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{bastion_public_ip} # 将 {bastion_public_ip} 替换为你的堡垒机节点 IP，例如 54.186.149.187
    scp -i "kafka-vpc-key-pair.pem" kafka-vpc-key-pair.pem ec2-user@{bastion_public_ip}:~/
    ```

2. 下载二进制文件。

    ```shell
    # 下载 Kafka 和 OpenJDK 并解压。你可根据需要选择二进制版本。
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. 将二进制文件复制到每个 broker 节点。

    ```shell
    # 将 {broker-node1-ip} 替换为你的 broker-node1 IP
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node1-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node1-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # 将 {broker-node2-ip} 替换为你的 broker-node2 IP
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node2-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node2-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # 将 {broker-node3-ip} 替换为你的 broker-node3 IP
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz ec2-user@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node3-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz ec2-user@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{broker-node3-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    ```

**2.4. 在每个 broker 节点上搭建 Kafka 节点**

**2.4.1 使用三节点搭建 KRaft Kafka 集群**

每个节点都将同时作为 broker 和 controller 角色。对每个 broker 执行如下操作：

1. 对于 `listeners` 项，三台 broker 配置相同，均为 broker 和 controller 角色：

    1. 所有 **controller** 角色节点配置相同的 CONTROLLER listener。如果只添加 **broker** 角色节点，则无需在 `server.properties` 中配置 CONTROLLER listener。
    2. 配置两个 **broker** listener，`INTERNAL` 用于内部访问，`EXTERNAL` 用于 TiDB Cloud 外部访问。

2. 对于 `advertised.listeners` 项，操作如下：

    1. 为每个 broker 配置 INTERNAL advertised listener，使用 broker 节点的内网 IP。内部 Kafka client 通过该地址访问 broker。
    2. 为每个 broker 节点配置 EXTERNAL advertised listener，基于 TiDB Cloud 获取的 **Kafka Advertised Listener Pattern**，帮助 TiDB Cloud 区分不同 broker。不同的 EXTERNAL advertised listener 使 TiDB Cloud 的 Kafka client 能路由到正确的 broker。

        - `<port>` 用于区分 Kafka Private Link Service 访问点的 broker。为所有 broker 的 EXTERNAL advertised listener 规划端口范围。这些端口不必是 broker 实际监听的端口，而是 Private Link Service 负载均衡器监听的端口，会转发到不同 broker。
        - **Kafka Advertised Listener Pattern** 中的 `AZ ID` 表示 broker 部署的可用区。TiDB Cloud 会根据 AZ ID 路由到不同的端点 DNS 名称。

      建议为不同 broker 配置不同的 broker ID，便于排查问题。

3. 规划值如下：

    - **CONTROLLER 端口**: `29092`
    - **INTERNAL 端口**: `9092`
    - **EXTERNAL**: `39092`
    - **EXTERNAL advertised listener 端口范围**: `9093~9095`

**2.4.2. 创建配置文件**

使用 SSH 登录每个 broker 节点，创建 `~/config/server.properties` 配置文件，内容如下。

```properties
# brokers in usw2-az1

# broker-node1 ~/config/server.properties
# 1. 将 {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”章节的 "Kafka Advertised Listener Pattern" 配置 EXTERNAL。
# 2.1 AZ(ID: usw2-az1) 的 pattern 为 "<broker_id>.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"。
# 2.2 EXTERNAL 可为 "b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093"。<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9093）。
# 2.3 若同一 AZ 有更多 broker 角色节点，可同样配置。
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node1-ip}:9092,EXTERNAL://b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in usw2-az2

# broker-node2 ~/config/server.properties
# 1. 将 {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”章节的 "Kafka Advertised Listener Pattern" 配置 EXTERNAL。
# 2.1 AZ(ID: usw2-az2) 的 pattern 为 "<broker_id>.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"。
# 2.2 EXTERNAL 可为 "b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094"。<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9094）。
# 2.3 若同一 AZ 有更多 broker 角色节点，可同样配置。
process.roles=broker,controller
node.id=2
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node2-ip}:9092,EXTERNAL://b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in usw2-az3

# broker-node3 ~/config/server.properties
# 1. 将 {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”章节的 "Kafka Advertised Listener Pattern" 配置 EXTERNAL。
# 2.1 AZ(ID: usw2-az3) 的 pattern 为 "<broker_id>.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"。
# 2.2 EXTERNAL 可为 "b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095"。<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9095）。
# 2.3 若同一 AZ 有更多 broker 角色节点，可同样配置。
process.roles=broker,controller
node.id=3
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node3-ip}:9092,EXTERNAL://b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

**2.4.3 启动 Kafka broker**

创建脚本并在每个 broker 节点上执行以启动 Kafka broker。

```shell
#!/bin/bash

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 设置 JAVA_HOME
export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
# 定义变量
KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
KAFKA_STORAGE_CMD=$KAFKA_DIR/kafka-storage.sh
KAFKA_START_CMD=$KAFKA_DIR/kafka-server-start.sh
KAFKA_DATA_DIR=$SCRIPT_DIR/data
KAFKA_LOG_DIR=$SCRIPT_DIR/log
KAFKA_CONFIG_DIR=$SCRIPT_DIR/config

# 清理步骤，便于多次实验
# 查找所有 Kafka 进程
KAFKA_PIDS=$(ps aux | grep 'kafka.Kafka' | grep -v grep | awk '{print $2}')
if [ -z "$KAFKA_PIDS" ]; then
  echo "No Kafka processes are running."
else
  # 杀死每个 Kafka 进程
  echo "Killing Kafka processes with PIDs: $KAFKA_PIDS"
  for PID in $KAFKA_PIDS; do
    kill -9 $PID
    echo "Killed Kafka process with PID: $PID"
  done
  echo "All Kafka processes have been killed."
fi

rm -rf $KAFKA_DATA_DIR
mkdir -p $KAFKA_DATA_DIR
rm -rf $KAFKA_LOG_DIR
mkdir -p $KAFKA_LOG_DIR

# Magic id: BRl69zcmTFmiPaoaANybiw, 你可以自定义
$KAFKA_STORAGE_CMD format -t "BRl69zcmTFmiPaoaANybiw" -c "$KAFKA_CONFIG_DIR/server.properties" > $KAFKA_LOG_DIR/server_format.log   
LOG_DIR=$KAFKA_LOG_DIR nohup $KAFKA_START_CMD "$KAFKA_CONFIG_DIR/server.properties" &
```

**2.5. 在堡垒机节点测试集群设置**

1. 测试 Kafka 启动/引导程序。

    ```shell
    export JAVA_HOME=/home/ec2-user/jdk-22.0.2

    # 从 INTERNAL listener 启动/引导程序
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:9092 | grep 9092
    # 期望输出（实际顺序可能不同）
    {broker-node1-ip}:9092 (id: 1 rack: null) -> (
    {broker-node2-ip}:9092 (id: 2 rack: null) -> (
    {broker-node3-ip}:9092 (id: 3 rack: null) -> (

    # 从 EXTERNAL listener 启动/引导程序
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092
    # 期望输出最后 3 行（实际顺序可能不同）
    # 与 "从 INTERNAL listener 启动/引导程序" 的区别在于，因 advertised listener 在 Kafka VPC 内无法解析，可能出现异常或错误。
    # 后续会在 TiDB Cloud 侧使其可解析，并在你通过 Private Link 创建 changefeed 连接该 Kafka 集群时路由到正确的 broker。
    b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ```

2. 在堡垒机节点创建 producer 脚本 `produce.sh`。

    ```shell
    #!/bin/bash
    BROKER_LIST=$1 # "{broker_address1},{broker_address2}..."

    # 获取当前脚本所在目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # 设置 JAVA_HOME
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    # 定义 Kafka 目录
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"

    # 如果不存在则创建 topic
    create_topic() {
        echo "Creating topic if it does not exist..."
        $KAFKA_DIR/kafka-topics.sh --create --topic $TOPIC --bootstrap-server $BROKER_LIST --if-not-exists --partitions 3 --replication-factor 3
    }

    # 向 topic 生产消息
    produce_messages() {
        echo "Producing messages to the topic..."
        for ((chrono=1; chrono <= 10; chrono++)); do
            message="Test message "$chrono
            echo "Create "$message
            echo $message | $KAFKA_DIR/kafka-console-producer.sh --broker-list $BROKER_LIST --topic $TOPIC
        done
    }
    create_topic
    produce_messages 
    ```

3. 在堡垒机节点创建 consumer 脚本 `consume.sh`。

    ```shell
    #!/bin/bash

    BROKER_LIST=$1 # "{broker_address1},{broker_address2}..."

    # 获取当前脚本所在目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # 设置 JAVA_HOME
    export JAVA_HOME="$SCRIPT_DIR/jdk-22.0.2"
    # 定义 Kafka 目录
    KAFKA_DIR="$SCRIPT_DIR/kafka_2.13-3.7.1/bin"
    TOPIC="test-topic"
    CONSUMER_GROUP="test-group"
    # 从 topic 消费消息
    consume_messages() {
        echo "Consuming messages from the topic..."
        $KAFKA_DIR/kafka-console-consumer.sh --bootstrap-server $BROKER_LIST --topic $TOPIC --from-beginning --timeout-ms 5000 --consumer-property group.id=$CONSUMER_GROUP
    }
    consume_messages
    ```

4. 执行 `produce.sh` 和 `consume.sh`，验证 Kafka 集群运行正常。后续网络连通性测试也会复用这些脚本。脚本会用 `--partitions 3 --replication-factor 3` 创建 topic，确保三台 broker 都有数据，且脚本会连接所有 broker，保证网络连通性被测试。

    ```shell
    # 测试写消息
    ./produce.sh {one_of_broker_ip}:9092
    ```

    ```shell
    # 期望输出
    Creating topic if it does not exist...

    Producing messages to the topic...
    Create Test message 1
    >>Create Test message 2
    >>Create Test message 3
    >>Create Test message 4
    >>Create Test message 5
    >>Create Test message 6
    >>Create Test message 7
    >>Create Test message 8
    >>Create Test message 9
    >>Create Test message 10
    ```

    ```shell
    # 测试读消息
    ./consume.sh {one_of_broker_ip}:9092
    ```

    ```shell
    # 期望输出示例（实际消息顺序可能不同）
    Consuming messages from the topic...
    Test message 3
    Test message 4
    Test message 5
    Test message 9
    Test message 10
    Test message 6
    Test message 8
    Test message 1
    Test message 2
    Test message 7
    [2024-11-01 08:54:27,547] ERROR Error processing message, terminating consumer process:  (kafka.tools.ConsoleConsumer$)
    org.apache.kafka.common.errors.TimeoutException
    Processed a total of 10 messages
    ```

### 重配置运行中的 Kafka 集群

<CustomContent plan="dedicated">

确保你的 Kafka 集群部署在与 TiDB 集群相同的 Region 和 AZ。如果有 broker 在不同 AZ，请将其迁移到正确的 AZ。

</CustomContent>
<CustomContent plan="premium">

确保你的 Kafka 集群部署在与 TiDB 实例相同的 Region 和 AZ。如果有 broker 在不同 AZ，请将其迁移到正确的 AZ。

</CustomContent>

#### 1. 为 broker 配置 EXTERNAL listener

以下配置适用于 Kafka KRaft 集群。ZK 模式配置类似。

1. 规划配置变更。

    1. 为每个 broker 配置 EXTERNAL **listener**，用于 TiDB Cloud 外部访问。选择唯一端口作为 EXTERNAL 端口，例如 `39092`。
    2. 为每个 broker 节点配置 EXTERNAL **advertised listener**，基于 TiDB Cloud 获取的 **Kafka Advertised Listener Pattern**，帮助 TiDB Cloud 区分不同 broker。不同的 EXTERNAL advertised listener 使 TiDB Cloud 的 Kafka client 能路由到正确的 broker。

        - `<port>` 用于区分 Kafka Private Link Service 访问点的 broker。为所有 broker 的 EXTERNAL advertised listener 规划端口范围，例如从 `9093` 开始。这些端口不必是 broker 实际监听的端口，而是 Private Link Service 负载均衡器监听的端口，会转发到不同 broker。
        - **Kafka Advertised Listener Pattern** 中的 `AZ ID` 表示 broker 部署的可用区。TiDB Cloud 会根据 AZ ID 路由到不同的端点 DNS 名称。

      建议为不同 broker 配置不同的 broker ID，便于排查问题。

2. 使用 SSH 登录每个 broker 节点，修改各自的配置文件，内容如下：

    ```properties
    # brokers in usw2-az1

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”章节的 "Kafka Advertised Listener Pattern" 添加 EXTERNAL advertised listener
    # 1. AZ(ID: usw2-az1) 的 pattern 为 "<broker_id>.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
    # 2. EXTERNAL 可为 "b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093"，<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9093）
    advertised.listeners=...,EXTERNAL://b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```
 
    ```properties
    # brokers in usw2-az2

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”章节的 "Kafka Advertised Listener Pattern" 添加 EXTERNAL advertised listener
    # 1. AZ(ID: usw2-az2) 的 pattern 为 "<broker_id>.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
    # 2. EXTERNAL 可为 "b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094"，<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9094）
    advertised.listeners=...,EXTERNAL://b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

    ```properties
    # brokers in usw2-az3

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”章节的 "Kafka Advertised Listener Pattern" 添加 EXTERNAL advertised listener
    # 1. AZ(ID: usw2-az3) 的 pattern 为 "<broker_id>.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:<port>"
    # 2. EXTERNAL 可为 "b2.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095"，<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9095）
    advertised.listeners=...,EXTERNAL://b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

3. 重新配置所有 broker 后，依次重启 Kafka broker。

#### 2. 在内网测试 EXTERNAL listener 设置

你可以在 Kafka client 节点下载 Kafka 和 OpenJDK。

```shell
# 下载 Kafka 和 OpenJDK 并解压。你可根据需要选择二进制版本。
wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```

执行以下脚本，测试启动/引导程序是否正常。

```shell
export JAVA_HOME=/home/ec2-user/jdk-22.0.2

# 从 EXTERNAL listener 启动/引导程序
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# 期望输出最后 3 行（实际顺序可能不同）
# 因 advertised listener 在 Kafka 网络内无法解析，会有异常或错误。
# 后续会在 TiDB Cloud 侧使其可解析，并在你通过 Private Link 创建 changefeed 连接该 Kafka 集群时路由到正确的 broker。
b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

## 步骤 2. 将 Kafka 集群暴露为 Private Link 服务

### 1. 搭建负载均衡器

创建一个网络负载均衡器，包含四个 target group，端口各不相同。一个 target group 用于启动/引导程序，其余分别映射到不同 broker。

1. bootstrap target group => 9092 => broker-node1:39092,broker-node2:39092,broker-node3:39092
2. broker target group 1  => 9093 => broker-node1:39092
3. broker target group 2  => 9094 => broker-node2:39092
4. broker target group 3  => 9095 => broker-node3:39092

如果有更多 broker 角色节点，需要添加更多映射。确保 bootstrap target group 至少有一个节点，建议每个 AZ 各加一个节点以增强容错。

按如下步骤搭建负载均衡器：

1. 进入 [Target groups](https://console.aws.amazon.com/ec2/home#CreateTargetGroup:) 创建四个 target group。

    - Bootstrap target group 

        - **Target type**: `Instances`
        - **Target group name**: `bootstrap-target-group`
        - **Protocol**: `TCP`
        - **Port**: `9092`
        - **IP address type**: `IPv4`
        - **VPC**: `Kafka VPC`
        - **Health check protocol**: `TCP`
        - **Register targets**: `broker-node1:39092`, `broker-node2:39092`, `broker-node3:39092`

    - Broker target group 1

        - **Target type**: `Instances`
        - **Target group name**: `broker-target-group-1`
        - **Protocol**: `TCP`
        - **Port**: `9093`
        - **IP address type**: `IPv4`
        - **VPC**: `Kafka VPC`
        - **Health check protocol**: `TCP`
        - **Register targets**: `broker-node1:39092`

    - Broker target group 2

        - **Target type**: `Instances`
        - **Target group name**: `broker-target-group-2`
        - **Protocol**: `TCP`
        - **Port**: `9094`
        - **IP address type**: `IPv4`
        - **VPC**: `Kafka VPC`
        - **Health check protocol**: `TCP`
        - **Register targets**: `broker-node2:39092`

    - Broker target group 3

        - **Target type**: `Instances`
        - **Target group name**: `broker-target-group-3`
        - **Protocol**: `TCP`
        - **Port**: `9095`
        - **IP address type**: `IPv4`
        - **VPC**: `Kafka VPC`
        - **Health check protocol**: `TCP`
        - **Register targets**: `broker-node3:39092`

2. 进入 [Load balancers](https://console.aws.amazon.com/ec2/home#LoadBalancers:) 创建网络负载均衡器。

    - **Load balancer name**: `kafka-lb`
    - **Schema**: `Internal`
    - **Load balancer IP address type**: `IPv4`
    - **VPC**: `Kafka VPC`
    - **Availability Zones**: 
        - `usw2-az1` 及其 `broker-usw2-az1` 子网
        - `usw2-az2` 及其 `broker-usw2-az2` 子网
        - `usw2-az3` 及其 `broker-usw2-az3` 子网
    - **Security groups**: 新建安全组，规则如下。
        - 入站规则允许来自 Kafka VPC 的所有 TCP：Type - `{ports of target groups}`，如 `9092-9095`；Source - `{TiDB Cloud 的 CIDR}`。获取 Region 内 TiDB Cloud 的 CIDR，请在 [TiDB Cloud 控制台](https://tidbcloud.com) 左上角切换到目标项目，点击 **Project Settings** > **Network Access**，再点击 **Project CIDR** > **AWS**。
        - 出站规则允许所有 TCP 到 Kafka VPC：Type - `All TCP`；Destination - `Anywhere-IPv4`
    - Listeners and routing:
        - Protocol: `TCP`; Port: `9092`; Forward to: `bootstrap-target-group`
        - Protocol: `TCP`; Port: `9093`; Forward to: `broker-target-group-1`
        - Protocol: `TCP`; Port: `9094`; Forward to: `broker-target-group-2`
        - Protocol: `TCP`; Port: `9095`; Forward to: `broker-target-group-3`

3. 在堡垒机节点测试负载均衡器。本例只测试 Kafka 启动/引导程序。由于负载均衡器监听的是 Kafka EXTERNAL listener，EXTERNAL advertised listener 的地址在堡垒机节点不可解析。记下负载均衡器详情页的 `kafka-lb` DNS 名称，例如 `kafka-lb-77405fa57191adcb.elb.us-west-2.amazonaws.com`。在堡垒机节点执行如下脚本。

    ```shell
    # 将 {lb_dns_name} 替换为实际值
    export JAVA_HOME=/home/ec2-user/jdk-22.0.2
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {lb_dns_name}:9092

    # 期望输出最后 3 行（实际顺序可能不同）
    b1.usw2-az1.abc.us-west-2.aws.3199015.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.usw2-az2.abc.us-west-2.aws.3199015.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.usw2-az3.abc.us-west-2.aws.3199015.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException

    # 你也可以尝试在 9093/9094/9095 端口启动/引导程序。由于 AWS 的 NLB 默认将 LB DNS 解析到任意可用区的 IP，且默认关闭跨区负载均衡，因此有概率成功。
    # 如果你在 LB 启用跨区负载均衡，则一定成功。但这通常没必要，且可能带来额外的跨 AZ 流量。
    ```

### 2. 搭建 Private Link 服务

1. 进入 [Endpoint service](https://console.aws.amazon.com/vpcconsole/home#EndpointServices:)，点击 **Create endpoint service**，为 Kafka 负载均衡器创建 Private Link 服务。

    - **Name**: `kafka-pl-service`
    - **Load balancer type**: `Network`
    - **Load balancers**: `kafka-lb`
    - **Included Availability Zones**: `usw2-az1`,`usw2-az2`, `usw2-az3`
    - **Require acceptance for endpoint**: `Acceptance required`
    - **Enable private DNS name**: `No`

2. 记下 **Service name**，你需要将其提供给 TiDB Cloud，例如 `com.amazonaws.vpce.us-west-2.vpce-svc-0f49e37e1f022cd45`。

3. 在 kafka-pl-service 详情页，点击 **Allow principals** 标签页，允许 TiDB Cloud 的 AWS 账户创建端点。你可以在[前置条件](#prerequisites)中获取 TiDB Cloud 的 AWS 账户，例如 `arn:aws:iam::<account_id>:root`。

## 步骤 3. 从 TiDB Cloud 连接

1. 回到 [TiDB Cloud 控制台](https://tidbcloud.com)，为 <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent> 创建 changefeed，通过 **Private Link** 连接到 Kafka 集群。详细操作请参见 [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)。

2. 当你进行 **Configure the changefeed target > Connectivity Method > Private Link** 配置时，按下表填写对应字段，其他字段按需填写。

    - **Kafka Type**: `3 AZs`。确保你的 Kafka 集群部署在同样的三个 AZ。
    - **Kafka Advertised Listener Pattern**: `abc`。与[前置条件](#prerequisites)中用于生成 **Kafka Advertised Listener Pattern** 的唯一随机字符串一致。
    - **Endpoint Service Name**: Kafka 服务名。
    - **Bootstrap Ports**: `9092`。只需一个端口，因为你已在其后配置了专用的 bootstrap target group。

3. 按照 [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) 的步骤继续操作。

至此，你已成功完成全部操作。

## 常见问题

### 如何从两个不同的 TiDB Cloud 项目连接同一个 Kafka Private Link 服务？

如果你已按本文档成功完成第一个项目的连接，可以按如下方式让第二个项目也连接同一个 Kafka Private Link 服务：

1. 按本文档从头操作。

2. 当你进行 [步骤 1. 搭建 Kafka 集群](#step-1-set-up-a-kafka-cluster) 时，参考 [重配置运行中的 Kafka 集群](#reconfigure-a-running-kafka-cluster) 新增一组 EXTERNAL listener 和 advertised listener，可命名为 **EXTERNAL2**。注意 **EXTERNAL2** 的端口范围不能与 **EXTERNAL** 重叠。

3. 重新配置 broker 后，在负载均衡器中新增一组 target group，包括 bootstrap 和 broker target group。

4. 配置 TiDB Cloud 连接时，填写如下信息：

    - 新的 Bootstrap 端口
    - 新的 Kafka Advertised Listener Group
    - 相同的 Endpoint Service
