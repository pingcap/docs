---
title: 通过 Private Link 连接访问 AWS 自建 Kafka
summary: 了解如何通过 AWS Endpoint Service Private Link 连接，连接到 AWS 上的自建 Kafka。
---

# 通过 Private Link 连接访问 AWS 自建 Kafka

本文档介绍如何使用 [AWS Endpoint Service Private Link 连接](/tidb-cloud/serverless-private-link-connection.md) 将 TiDB Cloud Essential 集群连接到 AWS 上的自建 Kafka 集群。

其机制如下：

1. Private Link 连接通过 bootstrap broker 地址连接到你的 AWS endpoint service，该地址会返回所有 Kafka broker 的地址和端口。
2. TiDB Cloud 使用返回的 broker 地址和端口，通过 Private Link 连接建立连接。
3. AWS endpoint service 将请求转发到你的负载均衡器。
4. 负载均衡器根据端口映射将请求路由到对应的 Kafka broker。

## 前置条件

- 确保你拥有在 AWS 账户中搭建 Kafka 集群所需的以下权限：

    - 管理 EC2 实例
    - 管理 VPC
    - 管理子网
    - 连接 EC2 实例以配置 Kafka 节点

- 确保你拥有在 AWS 账户中搭建负载均衡器和 endpoint service 所需的以下权限：

    - 管理安全组
    - 管理负载均衡器
    - 管理 endpoint service

- 你的 TiDB Cloud Essential 托管在 AWS 上，并且处于活跃状态。请获取并保存以下信息以备后用：

    - AWS 账户 ID
    - 可用区（AZs）

要查看 AWS 账户 ID 和可用区，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入你的 TiDB 集群的集群总览页面，然后点击左侧导航栏的 **Settings** > **Networking**。
2. 在 **Private Link Connection For Dataflow** 区域，点击 **Create Private Link Connection**。
3. 在弹出的对话框中，你可以找到 AWS 账户 ID 和可用区。

下表展示了一个部署信息示例。

| 信息     | 值    | 备注    | 
|--------|-----------------|---------------------------|
| Region    | Oregon (`us-west-2`)    |  N/A |
| Principal of TiDB Cloud AWS Account | `arn:aws:iam::<account_id>:root`     |    N/A  |
| AZ IDs                              | <ul><li>`usw2-az1` </li><li>`usw2-az2` </li><li> `usw2-az3`</li></ul>  | 将 AZ ID 与 AWS 账户中的 AZ 名称对齐。<br/>示例： <ul><li> `usw2-az1` => `us-west-2a` </li><li> `usw2-az2` => `us-west-2c` </li><li>`usw2-az3` => `us-west-2b`</li></ul>  |
| Kafka Advertised Listener Pattern   | <ul><li> `usw2-az1` => &lt;broker_id&gt;.usw2-az1.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li><li> `usw2-az2` => &lt;broker_id&gt;.usw2-az2.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li><li> `usw2-az3` => &lt;broker_id&gt;.usw2-az3.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li></ul>    | 将 AZ 名称映射到 AZ 指定的模式。确保你稍后为特定 AZ 的 broker 配置了正确的模式。 <ul><li> `us-west-2a` => &lt;broker_id&gt;.usw2-az1.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li><li> `us-west-2c` => &lt;broker_id&gt;.usw2-az2.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li><li> `us-west-2b` => &lt;broker_id&gt;.usw2-az3.unique_name.aws.plc.tidbcloud.com:&lt;port&gt; </li></ul> `unique_name` 是一个占位符，将在 [步骤 4](#step-4-replace-the-unique-name-placeholder-in-kafka-configuration) 中替换为实际值。  |

## 步骤 1. 搭建 Kafka 集群

如果你需要部署新集群，请参考 [部署新 Kafka 集群](#deploy-a-new-kafka-cluster)。

如果你需要暴露已有集群，请参考 [重新配置运行中的 Kafka 集群](#reconfigure-a-running-kafka-cluster)。

### 部署新 Kafka 集群

#### 1. 搭建 Kafka VPC

Kafka VPC 需要满足以下要求：

- 为 broker 准备三个私有子网，每个 AZ 一个。
- 在任意 AZ 中准备一个公有子网，部署堡垒机节点，该节点可以连接互联网和三个私有子网，便于搭建 Kafka 集群。在生产环境中，你可能有自己的堡垒机节点用于连接 Kafka VPC。

在创建子网前，请根据 AZ ID 与 AZ 名称的映射关系创建子网。以如下映射为例：

- `usw2-az1` => `us-west-2a`
- `usw2-az2` => `us-west-2c`
- `usw2-az3` => `us-west-2b`

在以下 AZ 中创建私有子网：

- `us-west-2a`
- `us-west-2c`
- `us-west-2b`

按照以下步骤创建 Kafka VPC。

**1.1. 创建 Kafka VPC**

1. 进入 [AWS 控制台 > VPC 控制台](https://console.aws.amazon.com/vpcconsole/home?#vpcs:)，切换到你希望部署 Kafka 的 Region。
2. 点击 **Create VPC**。在 **VPC settings** 页面填写如下信息：

    1. 选择 **VPC only**。
    2. 在 **Name tag** 输入标签，例如 `Kafka VPC`。
    3. 选择 **IPv4 CIDR manual input**，输入 IPv4 CIDR，例如 `10.0.0.0/16`。
    4. 其他选项保持默认。点击 **Create VPC**。
    5. 在 VPC 详情页，记录 VPC ID，例如 `vpc-01f50b790fa01dffa`。

**1.2. 在 Kafka VPC 中创建私有子网**

1. 进入 [Subnets 列表页](https://console.aws.amazon.com/vpcconsole/home?#subnets:)。
2. 点击 **Create subnet**。
3. 选择你之前记录的 **VPC ID**（本例为 `vpc-01f50b790fa01dffa`）。
4. 添加三个子网，填写如下信息。建议在子网名称中加入 AZ ID，便于后续配置 broker，因为 TiDB Cloud 要求在 broker 的 `advertised.listener` 配置中编码 AZ ID。

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
2. 选择你之前记录的 **VPC ID**（本例为 `vpc-01f50b790fa01dffa`）。
3. 在任意 AZ 添加公有子网，填写如下信息：

   - **Subnet name**: `bastion`
   - **IPv4 subnet CIDR block**: `10.0.192.0/18`

4. 将 bastion 子网配置为公有子网。

    1. 进入 [VPC 控制台 > Internet gateways](https://console.aws.amazon.com/vpcconsole/home#igws:)，创建名为 `kafka-vpc-igw` 的 Internet Gateway。
    2. 在 **Internet gateways Detail** 页面，点击 **Actions** 下的 **Attach to VPC**，将 Internet Gateway 绑定到 Kafka VPC。
    3. 进入 [VPC 控制台 > Route tables](https://console.aws.amazon.com/vpcconsole/home#CreateRouteTable:)，在 Kafka VPC 中创建一张路由表，并添加如下路由：

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
- **Key pair**: `kafka-vpc-key-pair`。新建名为 `kafka-vpc-key-pair` 的密钥对。下载 `kafka-vpc-key-pair.pem` 到本地，后续配置使用。
- 网络设置

    - **VPC**: `Kafka VPC`
    - **Subnet**: `bastion`
    - **Auto-assign public IP**: `Enable`
    - **Security Group**: 新建安全组，允许任意来源 SSH 登录。生产环境下可收紧规则。

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
        - **Security Group**: 新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境下可收紧规则。
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
        - **Security Group**: 新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境下可收紧规则。
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
        - **Security Group**: 新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境下可收紧规则。
            - **Protocol**: `TCP`
            - **Port range**: `0 - 65535`
            - **Source**: `10.0.0.0/16`

**2.3. 准备 Kafka 运行时二进制文件**

1. 进入堡垒机节点详情页，获取 **Public IPv4 address**。使用 SSH 登录该节点，使用之前下载的 `kafka-vpc-key-pair.pem`。

    ```shell
    chmod 400 kafka-vpc-key-pair.pem
    ssh -i "kafka-vpc-key-pair.pem" ec2-user@{bastion_public_ip} # 将 {bastion_public_ip} 替换为你的堡垒机节点 IP，例如 54.186.149.187
    scp -i "kafka-vpc-key-pair.pem" kafka-vpc-key-pair.pem ec2-user@{bastion_public_ip}:~/
    ```

2. 下载二进制文件。

    ```shell
    # 下载 Kafka 和 OpenJDK 并解压。你可以根据需要选择二进制版本。
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

每个节点都将同时作为 broker 和 controller 角色。对每个 broker 执行以下操作：

1. 对于 `listeners` 项，三个 broker 都相同，均作为 broker 和 controller 角色：

    1. 对所有 **controller** 角色节点配置相同的 CONTROLLER listener。如果你只想添加 **broker** 角色节点，则无需在 `server.properties` 中配置 CONTROLLER listener。
    2. 配置两个 **broker** listener，`INTERNAL` 用于内部访问，`EXTERNAL` 用于 TiDB Cloud 的外部访问。

2. 对于 `advertised.listeners` 项，操作如下：

    1. 为每个 broker 配置 INTERNAL advertised listener，使用 broker 节点的内网 IP。内部 Kafka 客户端通过该地址访问 broker。
    2. 为每个 broker 节点配置 EXTERNAL advertised listener，基于你从 TiDB Cloud 获取的 **Kafka Advertised Listener Pattern**，帮助 TiDB Cloud 区分不同 broker。不同的 EXTERNAL advertised listener 能帮助 TiDB Cloud 的 Kafka 客户端将请求路由到正确的 broker。

        - `<port>` 用于区分来自 Kafka Private Link Service 访问点的 broker。为所有 broker 的 EXTERNAL advertised listener 规划一个端口范围。这些端口不必是 broker 实际监听的端口，而是负载均衡器为 Private Link Service 监听的端口，会将请求转发到不同 broker。
        - **Kafka Advertised Listener Pattern** 中的 `AZ ID` 表示 broker 部署的位置。TiDB Cloud 会根据 AZ ID 路由请求到不同的 endpoint DNS 名称。
     
      建议为不同 broker 配置不同的 broker ID，便于排查问题。

3. 规划值如下：

    - **CONTROLLER 端口**: `29092`
    - **INTERNAL 端口**: `9092`
    - **EXTERNAL**: `39092`
    - **EXTERNAL advertised listener 端口范围**: `9093~9095`

**2.4.2. 创建配置文件**

使用 SSH 登录每个 broker 节点。创建配置文件 `~/config/server.properties`，内容如下。

```properties
# brokers in usw2-az1

# broker-node1 ~/config/server.properties
# 1. 将 {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”章节的 “Kafka Advertised Listener Pattern” 配置 EXTERNAL。
# 2.1 AZ(ID: usw2-az1) 的模式为 "<broker_id>.usw2-az1.unique_name.aws.plc.tidbcloud.com:<port>"。
# 2.2 因此 EXTERNAL 可为 "b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093"。<broker_id> 用 "b" 前缀加 "node.id" 属性，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9093）。
# 2.3 若同一 AZ 有更多 broker 角色节点，可同样配置。
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node1-ip}:9092,EXTERNAL://b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in usw2-az2

# broker-node2 ~/config/server.properties
# 1. 将 {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”章节的 “Kafka Advertised Listener Pattern” 配置 EXTERNAL。
# 2.1 AZ(ID: usw2-az2) 的模式为 "<broker_id>.usw2-az2.unique_name.aws.plc.tidbcloud.com:<port>"。
# 2.2 因此 EXTERNAL 可为 "b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094"。<broker_id> 用 "b" 前缀加 "node.id" 属性，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9094）。
# 2.3 若同一 AZ 有更多 broker 角色节点，可同样配置。
process.roles=broker,controller
node.id=2
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node2-ip}:9092,EXTERNAL://b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in usw2-az3

# broker-node3 ~/config/server.properties
# 1. 将 {broker-node1-ip}, {broker-node2-ip}, {broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”章节的 “Kafka Advertised Listener Pattern” 配置 EXTERNAL。
# 2.1 AZ(ID: usw2-az3) 的模式为 "<broker_id>.usw2-az3.unique_name.aws.plc.tidbcloud.com:<port>"。
# 2.2 因此 EXTERNAL 可为 "b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095"。<broker_id> 用 "b" 前缀加 "node.id" 属性，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9095）。
# 2.3 若同一 AZ 有更多 broker 角色节点，可同样配置。
process.roles=broker,controller
node.id=3
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node3-ip}:9092,EXTERNAL://b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095
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
# 查找所有 Kafka 进程 ID
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

1. 测试 Kafka bootstrap。

    ```shell
    export JAVA_HOME=/home/ec2-user/jdk-22.0.2

    # 从 INTERNAL listener 启动
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:9092 | grep 9092
    # 期望输出（实际顺序可能不同）
    {broker-node1-ip}:9092 (id: 1 rack: null) -> (
    {broker-node2-ip}:9092 (id: 2 rack: null) -> (
    {broker-node3-ip}:9092 (id: 3 rack: null) -> (

    # 从 EXTERNAL listener 启动
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092
    # 期望输出最后 3 行（实际顺序可能不同）
    # 与 “从 INTERNAL listener 启动” 的输出不同，可能会出现异常或错误，因为 advertised listener 在 Kafka VPC 中无法解析。
    # 我们会在 TiDB Cloud 侧使其可解析，并在你通过 Private Link 创建连接到该 Kafka 集群的 changefeed 时，将请求路由到正确的 broker。
    b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
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

4. 执行 `produce.sh` 和 `consume.sh`，验证 Kafka 集群是否运行正常。这些脚本也会在后续网络连通性测试中复用。脚本会以 `--partitions 3 --replication-factor 3` 创建 topic，确保三个 broker 都有数据。确保脚本会连接所有三个 broker，以保证网络连通性被测试。

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
    # 期望示例输出（实际消息顺序可能不同）
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

### 重新配置运行中的 Kafka 集群

确保你的 Kafka 集群部署在与 TiDB 集群相同的 Region 和 AZ。如果有 broker 在不同 AZ，请将其迁移到正确的 AZ。

#### 1. 为 broker 配置 EXTERNAL listener

以下配置适用于 Kafka KRaft 集群。ZK 模式配置类似。

1. 规划配置变更。

    1. 为每个 broker 配置 EXTERNAL **listener**，用于 TiDB Cloud 的外部访问。选择唯一端口作为 EXTERNAL 端口，例如 `39092`。
    2. 为每个 broker 节点配置 EXTERNAL **advertised listener**，基于你从 TiDB Cloud 获取的 **Kafka Advertised Listener Pattern**，帮助 TiDB Cloud 区分不同 broker。不同的 EXTERNAL advertised listener 能帮助 TiDB Cloud 的 Kafka 客户端将请求路由到正确的 broker。

        - `<port>` 用于区分来自 Kafka Private Link Service 访问点的 broker。为所有 broker 的 EXTERNAL advertised listener 规划一个端口范围，例如从 9093 开始。这些端口不必是 broker 实际监听的端口，而是负载均衡器为 Private Link Service 监听的端口，会将请求转发到不同 broker。
        - **Kafka Advertised Listener Pattern** 中的 `AZ ID` 表示 broker 部署的位置。TiDB Cloud 会根据 AZ ID 路由请求到不同的 endpoint DNS 名称。

      建议为不同 broker 配置不同的 broker ID，便于排查问题。

2. 使用 SSH 登录每个 broker 节点。修改每个 broker 的配置文件，内容如下：

    ```properties
    # brokers in usw2-az1

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”章节的 “Kafka Advertised Listener Pattern” 添加 EXTERNAL advertised listener
    # 1. AZ(ID: usw2-az1) 的模式为 "<broker_id>.usw2-az1.unique_name.aws.plc.tidbcloud.com:<port>"
    # 2. 因此 EXTERNAL 可为 "b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093"，<broker_id> 用 "b" 前缀加 "node.id" 属性，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9093）
    advertised.listeners=...,EXTERNAL://b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```
 
    ```properties
    # brokers in usw2-az2

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”章节的 “Kafka Advertised Listener Pattern” 添加 EXTERNAL advertised listener
    # 1. AZ(ID: usw2-az2) 的模式为 "<broker_id>.usw2-az2.unique_name.aws.plc.tidbcloud.com:<port>"
    # 2. 因此 EXTERNAL 可为 "b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094"，<broker_id> 用 "b" 前缀加 "node.id" 属性，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9094）
    advertised.listeners=...,EXTERNAL://b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

    ```properties
    # brokers in usw2-az3

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”章节的 “Kafka Advertised Listener Pattern” 添加 EXTERNAL advertised listener
    # 1. AZ(ID: usw2-az3) 的模式为 "<broker_id>.usw2-az3.unique_name.aws.plc.tidbcloud.com:<port>"
    # 2. 因此 EXTERNAL 可为 "b2.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095"，<broker_id> 用 "b" 前缀加 "node.id" 属性，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9095）
    advertised.listeners=...,EXTERNAL://b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

3. 重新配置所有 broker 后，逐个重启 Kafka broker。

#### 2. 在内网测试 EXTERNAL listener 设置

你可以在 Kafka client 节点下载 Kafka 和 OpenJDK。

```shell
# 下载 Kafka 和 OpenJDK 并解压。你可以根据需要选择二进制版本。
wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```

执行以下脚本，测试 bootstrap 是否正常。

```shell
export JAVA_HOME=/home/ec2-user/jdk-22.0.2

# 从 EXTERNAL listener 启动
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# 期望输出最后 3 行（实际顺序可能不同）
# 由于 advertised listener 在你的 Kafka 网络中无法解析，会有一些异常或错误。
# 我们会在 TiDB Cloud 侧使其可解析，并在你通过 Private Link 创建连接到该 Kafka 集群的 changefeed 时，将请求路由到正确的 broker。
b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

## 步骤 2. 将 Kafka 集群暴露为 Private Link 服务

### 1. 搭建负载均衡器

创建一个网络负载均衡器，包含四个 target group，监听不同端口。一个 target group 用于 bootstrap，其他分别映射到不同 broker。

1. bootstrap target group => 9092 => broker-node1:39092,broker-node2:39092,broker-node3:39092
2. broker target group 1  => 9093 => broker-node1:39092
3. broker target group 2  => 9094 => broker-node2:39092
4. broker target group 3  => 9095 => broker-node3:39092

如果有更多 broker 角色节点，需要添加更多映射。确保 bootstrap target group 至少有一个节点，建议每个 AZ 各加一个节点以增强可用性。

按以下步骤搭建负载均衡器：

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
        - `usw2-az1` 绑定 `broker-usw2-az1 subnet`
        - `usw2-az2` 绑定 `broker-usw2-az2 subnet`
        - `usw2-az3` 绑定 `broker-usw2-az3 subnet`
    - **Security groups**: 新建安全组，规则如下。
        - 入站规则允许来自 Kafka VPC 的所有 TCP：Type - `{ports of target groups}`，如 `9092-9095`；Source - `{TiDB Cloud 的 CIDR}`。获取 Region 内 TiDB Cloud 的 CIDR，请在 [TiDB Cloud 控制台](https://tidbcloud.com) 左上角切换到目标项目，点击 **Project Settings** > **Network Access**，再点击 **Project CIDR** > **AWS**。
        - 出站规则允许所有 TCP 到 Kafka VPC：Type - `All TCP`；Destination - `Anywhere-IPv4`
    - Listeners 和路由：
        - Protocol: `TCP`; Port: `9092`; Forward to: `bootstrap-target-group`
        - Protocol: `TCP`; Port: `9093`; Forward to: `broker-target-group-1`
        - Protocol: `TCP`; Port: `9094`; Forward to: `broker-target-group-2`
        - Protocol: `TCP`; Port: `9095`; Forward to: `broker-target-group-3`

3. 在堡垒机节点测试负载均衡器。本例只测试 Kafka bootstrap。由于负载均衡器监听的是 Kafka EXTERNAL listener，EXTERNAL advertised listener 的地址在堡垒机节点无法解析。记录负载均衡器详情页的 `kafka-lb` DNS 名称，例如 `kafka-lb-77405fa57191adcb.elb.us-west-2.amazonaws.com`。在堡垒机节点执行脚本。

    ```shell
    # 将 {lb_dns_name} 替换为实际值
    export JAVA_HOME=/home/ec2-user/jdk-22.0.2
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {lb_dns_name}:9092

    # 期望输出最后 3 行（实际顺序可能不同）
    b1.usw2-az1.unique_name.aws.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.usw2-az2.unique_name.aws.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.usw2-az3.unique_name.aws.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException

    # 你也可以尝试在 9093/9094/9095 端口 bootstrap。由于 AWS 的 NLB 默认会将 LB DNS 解析到任意可用区的 IP，并默认关闭跨区负载均衡，因此会概率性成功。
    # 如果你在 LB 启用跨区负载均衡，则会成功。但这不是必须的，且可能带来额外的跨 AZ 流量。
    ```

### 2. 搭建 AWS endpoint service

1. 进入 [Endpoint service](https://console.aws.amazon.com/vpcconsole/home#EndpointServices:)，点击 **Create endpoint service**，为 Kafka 负载均衡器创建 Private Link 服务。

    - **Name**: `kafka-pl-service`
    - **Load balancer type**: `Network`
    - **Load balancers**: `kafka-lb`
    - **Included Availability Zones**: `usw2-az1`,`usw2-az2`, `usw2-az3`
    - **Require acceptance for endpoint**: `Acceptance required`
    - **Enable private DNS name**: `No`

2. 记录 **Service name**，你需要将其提供给 TiDB Cloud，例如 `com.amazonaws.vpce.us-west-2.vpce-svc-0f49e37e1f022cd45`。

3. 在 kafka-pl-service 详情页，点击 **Allow principals** 标签页，添加你在 [前置条件](#prerequisites) 获取的 AWS 账户 ID 到 allowlist，例如 `arn:aws:iam::<account_id>:root`。

## 步骤 3. 在 TiDB Cloud 创建 Private Link 连接

在 TiDB Cloud 创建 Private Link 连接，操作如下：

1. 使用你在 [步骤 2](#2-set-up-an-aws-endpoint-service) 获取的 AWS endpoint service name（如 `com.amazonaws.vpce.<region>.vpce-svc-xxxx`）在 TiDB Cloud 创建 Private Link 连接。

    详细操作见 [创建 AWS Endpoint Service Private Link 连接](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection)。

2. 将域名绑定到 Private Link 连接，以便 TiDB Cloud 的数据流服务可以访问 Kafka 集群。

    详细操作见 [将域名绑定到 Private Link 连接](/tidb-cloud/serverless-private-link-connection.md#attach-domains-to-a-private-link-connection)。注意在 **Attach Domains** 对话框中，需选择 **TiDB Cloud Managed** 作为域名类型，并复制生成域名的 unique name 以备后用。

## 步骤 4. 替换 Kafka 配置中的 unique_name 占位符

1. 回到你的 Kafka broker 节点，将每个 broker 的 `advertised.listeners` 配置中的 `unique_name` 占位符替换为上一步获取的实际 unique name。
2. 重新配置所有 broker 后，逐个重启 Kafka broker。

现在，你可以使用该 Private Link 连接和 9092 作为 bootstrap 端口，从 TiDB Cloud 连接到你的 Kafka 集群。