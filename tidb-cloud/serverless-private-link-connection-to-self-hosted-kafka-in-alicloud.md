---
title: 通过私有链路连接接入阿里云自建 Kafka
summary: 了解如何通过阿里云 Endpoint Service 私有链路连接，接入阿里云自建 Kafka。
---

# 通过私有链路连接接入阿里云自建 Kafka

本文档介绍如何使用 [阿里云 Endpoint Service 私有链路连接](/tidb-cloud/serverless-private-link-connection.md)，将 TiDB Cloud Essential 集群连接到阿里云自建 Kafka 集群。

其机制如下：

1. 私有链路连接通过 bootstrap 端口连接到你的阿里云 endpoint service，返回在 `advertised.listeners` 中定义的 broker 外部地址。
2. 私有链路连接使用 broker 外部地址连接到你的 endpoint service。
3. 阿里云 endpoint service 将请求转发到你的负载均衡器。
4. 负载均衡器根据端口映射将请求转发到对应的 Kafka broker。

例如，端口映射如下：

| Broker 外部地址端口 | 负载均衡器监听端口 | 负载均衡器后端服务器 |
|----------------------------|------------------------------|-------------|
| 9093                       | 9093                        | broker-node1:39092|
| 9094                       | 9094                        | broker-node2:39092|
| 9095                       | 9095                        | broker-node3:39092|

## 前置条件

- 确保你已有 Kafka 集群，或拥有以下权限以进行集群搭建。

    - 管理 ECS 节点
    - 管理 VPC 和 vSwitch
    - 连接 ECS 节点以配置 Kafka 节点

- 确保你拥有以下权限，以在阿里云账户中搭建负载均衡器和 endpoint service。

    - 管理负载均衡器
    - 管理 endpoint service

- 你的 TiDB Cloud Essential 托管在阿里云，并且处于活跃状态。请获取并保存以下信息以备后用：

    - 阿里云账户 ID
    - 可用区（AZ）

查看阿里云账户 ID 和可用区的方法如下：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入 TiDB 集群的集群总览页面，然后点击左侧导航栏的 **Settings** > **Networking**。
2. 在 **Private Link Connection For Dataflow** 区域，点击 **Create Private Link Connection**。
3. 在弹出的对话框中，你可以找到阿里云账户 ID 和可用区信息。

下表为部署信息示例。

| 信息     | 值    | 备注    | 
|--------|-----------------|---------------------------|
| Region    | `ap-southeast-1`   |  N/A |
| TiDB Cloud 阿里云账户 | `<account_id>`     |    N/A  |
| AZ IDs                              | <ul><li>`ap-southeast-1a` </li><li>`ap-southeast-1b` </li><li> `ap-southeast-1c`</li></ul> |    N/A  |
| Kafka Advertised Listener Pattern   | &lt;broker_id&gt;.unique_name.alicloud.plc.tidbcloud.com:&lt;port&gt;| `unique_name` 是占位符，将在 [步骤 4](#step-4-replace-the-unique-name-placeholder-in-kafka-configuration) 替换为实际值 |

## 步骤 1. 搭建 Kafka 集群

如需部署新集群，请参考 [部署新 Kafka 集群](#deploy-a-new-kafka-cluster)。

如需暴露已有集群，请参考 [重配置运行中的 Kafka 集群](#reconfigure-a-running-kafka-cluster)。

### 部署新 Kafka 集群

#### 1. 搭建 Kafka VPC

Kafka VPC 需要满足以下要求：

- 为 broker 准备三个私有 vSwitch，每个可用区一个。
- 在任意可用区准备一个公有 vSwitch，部署堡垒机节点，该节点可连接互联网和三个私有 vSwitch，便于搭建 Kafka 集群。在生产环境中，你可能已有可连接 Kafka VPC 的堡垒机节点。

创建 Kafka VPC 的步骤如下。

**1.1. 创建 Kafka VPC**

1. 进入 [阿里云控制台 > VPC 控制台](https://vpc.console.alibabacloud.com/vpc)，切换到你希望部署 Kafka 的 Region。

2. 点击 **创建 VPC**，在 **VPC 设置** 页面填写如下信息。

    1. 输入 **名称**，如 `Kafka VPC`。
    2. 选择你希望在 TiDB Cloud 设置私有链路连接的 Region。
    3. 选择 **手动输入 IPv4 CIDR 块**，输入 IPv4 CIDR，例如 `10.0.0.0/16`。
    4. 为每个需要部署 Kafka broker 的 AZ 创建 vSwitch 并配置 IPv4 CIDR。例如：

        - broker-ap-southeast-1a vSwitch 在 `ap-southeast-1a`：10.0.0.0/18
        - broker-ap-southeast-1b vSwitch 在 `ap-southeast-1b`：10.0.64.0/18
        - broker-ap-southeast-1c vSwitch 在 `ap-southeast-1c`：10.0.128.0/18
        - bastion vSwitch 在 `ap-southeast-1a`：10.0.192.0/18

    5. 其他选项保持默认。点击 **确定**。

3. 在 VPC 详情页，记录 VPC ID，例如 `vpc-t4nfx2vcqazc862e9fg06`。

#### 2. 搭建 Kafka broker

**2.1. 创建堡垒机节点**

进入 [ECS 控制台](https://ecs.console.alibabacloud.com/home#/)，在 bastion vSwitch 下创建堡垒机节点。

- **网络与可用区**：`Kafka VPC` 和 `bastion` vSwitch。
- **实例与镜像**：`ecs.t5-lc1m2.small` 实例类型，`Alibaba Cloud Linux` 镜像。
- **网络与安全组**：选择 `分配公网 IPv4 地址`。
- **密钥对**：`kafka-vpc-key-pair`。新建名为 `kafka-vpc-key-pair` 的密钥对。下载 `kafka-vpc-key-pair.pem` 到本地，后续配置使用。
- **安全组**：新建安全组，允许任意来源 SSH 登录。生产环境可收紧规则。
- **实例名称**：`bastion-node`。

**2.2. 创建 broker 节点**

进入 [ECS 控制台](https://ecs.console.alibabacloud.com/home#/)，在各 vSwitch 下创建三个 broker 节点，每个 AZ 一个。

- Broker 1 在 vSwitch `broker-ap-southeast-1a`

    - **网络与可用区**：`Kafka VPC` 和 `broker-ap-southeast-1a` vSwitch
    - **实例与镜像**：`ecs.t5-lc1m2.small` 实例类型，`Alibaba Cloud Linux` 镜像
    - **密钥对**：复用 `kafka-vpc-key-pair`
    - **实例名称**：`broker-node1`
    - **安全组**：新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境可收紧规则。入方向规则：
            - **协议**：`TCP`
            - **端口范围**：`全部`
            - **来源**：`10.0.0.0/16`

- Broker 2 在 vSwitch `broker-ap-southeast-1b`

    - **网络与可用区**：`Kafka VPC` 和 `broker-ap-southeast-1b` vSwitch
    - **实例与镜像**：`ecs.t5-lc1m2.small` 实例类型，`Alibaba Cloud Linux` 镜像
    - **密钥对**：复用 `kafka-vpc-key-pair`
    - **实例名称**：`broker-node2`
    - **安全组**：新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境可收紧规则。入方向规则：
            - **协议**：`TCP`
            - **端口范围**：`全部`
            - **来源**：`10.0.0.0/16`

- Broker 3 在 vSwitch `broker-ap-southeast-1c`

    - **网络与可用区**：`Kafka VPC` 和 `broker-ap-southeast-1c` vSwitch
    - **实例与镜像**：`ecs.t5-lc1m2.small` 实例类型，`Alibaba Cloud Linux` 镜像
    - **密钥对**：复用 `kafka-vpc-key-pair`
    - **实例名称**：`broker-node3`
    - **安全组**：新建安全组，允许来自 Kafka VPC 的所有 TCP。生产环境可收紧规则。入方向规则：
            - **协议**：`TCP`
            - **端口范围**：`全部`
            - **来源**：`10.0.0.0/16`

**2.3. 准备 Kafka 运行时二进制文件**

1. 进入堡垒机节点详情页，获取 **公网 IPv4 地址**。使用 SSH 和之前下载的 `kafka-vpc-key-pair.pem` 登录该节点。

    ```shell
    chmod 400 kafka-vpc-key-pair.pem
    scp -i "kafka-vpc-key-pair.pem" kafka-vpc-key-pair.pem root@{bastion_public_ip}:~/ # 将 {bastion_public_ip} 替换为你的堡垒机节点 IP
    ssh -i "kafka-vpc-key-pair.pem" root@{bastion_public_ip}
    ```

2. 下载二进制文件到堡垒机节点。

    ```shell
    # 下载 Kafka 和 OpenJDK 并解压。可根据需要选择二进制版本。
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. 从堡垒机节点将二进制文件拷贝到每个 broker 节点。

    ```shell
    # 将 {broker-node1-ip} 替换为你的 broker-node1 IP
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz root@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node1-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz root@{broker-node1-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node1-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # 将 {broker-node2-ip} 替换为你的 broker-node2 IP
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz root@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node2-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz root@{broker-node2-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node2-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"

    # 将 {broker-node3-ip} 替换为你的 broker-node3 IP
    scp -i "kafka-vpc-key-pair.pem" kafka_2.13-3.7.1.tgz root@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node3-ip} "tar -zxf kafka_2.13-3.7.1.tgz"
    scp -i "kafka-vpc-key-pair.pem" openjdk-22.0.2_linux-x64_bin.tar.gz root@{broker-node3-ip}:~/
    ssh -i "kafka-vpc-key-pair.pem" root@{broker-node3-ip} "tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz"
    ```

**2.4. 在每个 broker 节点上配置 Kafka 节点**

**2.4.1 配置三节点 KRaft Kafka 集群**

每个节点同时作为 broker 和 controller。对每个 broker 执行如下操作：

1. 对于 `listeners` 项，三个 broker 配置相同，均为 broker 和 controller 角色：

    1. 所有 **controller** 角色节点配置相同的 CONTROLLER listener。如果只添加 **broker** 角色节点，则无需在 `server.properties` 中配置 CONTROLLER listener。
    2. 配置两个 **broker** listener，`INTERNAL` 用于内部访问，`EXTERNAL` 用于 TiDB Cloud 外部访问。

2. 对于 `advertised.listeners` 项，操作如下：

    1. 每个 broker 配置 INTERNAL advertised listener，使用 broker 节点的内网 IP。内部 Kafka 客户端通过该地址访问 broker。
    2. 每个 broker 节点根据 TiDB Cloud 获取的 **Kafka Advertised Listener Pattern** 配置 EXTERNAL advertised listener，帮助 TiDB Cloud 区分不同 broker。不同的 EXTERNAL advertised listener 便于 TiDB Cloud 的 Kafka 客户端路由请求到正确的 broker。

        - `<port>` 用于区分 Kafka Private Link Service 的不同 broker 访问点。请为所有 broker 的 EXTERNAL advertised listener 规划端口范围。这些端口不必是 broker 实际监听的端口，而是负载均衡器为 Private Link Service 监听并转发到不同 broker 的端口。
        - **Kafka Advertised Listener Pattern** 中的 AZ ID 表示 broker 部署的可用区。TiDB Cloud 会根据 AZ ID 路由请求到不同的 endpoint DNS。

      建议为不同 broker 配置不同的 broker ID，便于排查问题。

3. 规划值如下：

    - **CONTROLLER 端口**：`29092`
    - **INTERNAL 端口**：`9092`
    - **EXTERNAL**：`39092`
    - **EXTERNAL advertised listener 端口范围**：`9093~9095`

**2.4.2. 创建配置文件**

使用 SSH 登录每个 broker 节点，创建配置文件 `~/config/server.properties`，内容如下。

```properties
# brokers in ap-southeast-1a

# broker-node1 ~/config/server.properties
# 1. 将 {broker-node1-ip}、{broker-node2-ip}、{broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”中的 “Kafka Advertised Listener Pattern” 配置 EXTERNAL。
# 2.1 模式为 "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"。
# 2.2 如有更多 broker 角色节点，可同理配置。
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node1-ip}:9092,EXTERNAL://b1.unique_name.alicloud.plc.tidbcloud.com:9093
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in ap-southeast-1b

# broker-node2 ~/config/server.properties
# 1. 将 {broker-node1-ip}、{broker-node2-ip}、{broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”中的 “Kafka Advertised Listener Pattern” 配置 EXTERNAL。
# 2.1 模式为 "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"。
# 2.2 如有更多 broker 角色节点，可同理配置。
process.roles=broker,controller
node.id=2
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node2-ip}:9092,EXTERNAL://b2.unique_name.alicloud.plc.tidbcloud.com:9094
controller.listener.names=CONTROLLER
listener.security.protocol.map=INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL
log.dirs=./data
```

```properties
# brokers in ap-southeast-1c

# broker-node3 ~/config/server.properties
# 1. 将 {broker-node1-ip}、{broker-node2-ip}、{broker-node3-ip} 替换为实际 IP。
# 2. 按“前置条件”中的 “Kafka Advertised Listener Pattern” 配置 EXTERNAL。
# 2.1 模式为 "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"。
# 2.2 如有更多 broker 角色节点，可同理配置。
process.roles=broker,controller
node.id=3
controller.quorum.voters=1@{broker-node1-ip}:29092,2@{broker-node2-ip}:29092,3@{broker-node3-ip}:29092
listeners=INTERNAL://0.0.0.0:9092,CONTROLLER://0.0.0.0:29092,EXTERNAL://0.0.0.0:39092
inter.broker.listener.name=INTERNAL
advertised.listeners=INTERNAL://{broker-node3-ip}:9092,EXTERNAL://b3.ap-southeast-1c.unique_name.alicloud.plc.tidbcloud.com:9095
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
# 设置 JAVA_HOME 为脚本目录下的 Java 安装路径
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
    export JAVA_HOME=~/jdk-22.0.2

    # 从 INTERNAL listener 启动
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:9092 | grep 9092
    # 期望输出（实际顺序可能不同）
    {broker-node1-ip}:9092 (id: 1 rack: null) -> (
    {broker-node2-ip}:9092 (id: 2 rack: null) -> (
    {broker-node3-ip}:9092 (id: 3 rack: null) -> (

    # 从 EXTERNAL listener 启动
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092
    # 期望输出最后 3 行（实际顺序可能不同）
    # 与 “从 INTERNAL listener 启动” 的输出不同，因 advertised listener 在 Kafka VPC 内无法解析，可能出现异常或错误。
    # 在你通过 Private Link 创建 changefeed 连接该 Kafka 集群时，TiDB Cloud 侧会使其可解析并路由到正确 broker。
    b1.unique_name.alicloud.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.unique_name.alicloud.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.unique_name.alicloud.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ```

2. 在堡垒机节点创建 producer 脚本 `produce.sh`。

    ```shell
    #!/bin/bash
    BROKER_LIST=$1 # "{broker_address1},{broker_address2}..."

    # 获取当前脚本所在目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # 设置 JAVA_HOME 为脚本目录下的 Java 安装路径
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
    # 设置 JAVA_HOME 为脚本目录下的 Java 安装路径
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

4. 执行 `produce.sh` 和 `consume.sh`，验证 Kafka 集群运行正常。后续网络连通性测试也会复用这些脚本。脚本会以 `--partitions 3 --replication-factor 3` 创建 topic，确保三台 broker 都有数据。确保脚本会连接所有三台 broker，以保证网络连通性测试覆盖。

    ```shell
    # 测试写消息
    sh produce.sh {one_of_broker_ip}:9092
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
    sh consume.sh {one_of_broker_ip}:9092
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

确保你的 Kafka 集群部署在与 TiDB 集群相同的 Region 和 AZ。如果有 broker 在不同 AZ，请迁移到正确的 AZ。

#### 1. 为 broker 配置 EXTERNAL listener

以下配置适用于 Kafka KRaft 集群。ZK 模式配置类似。

1. 规划配置变更。

    1. 为每个 broker 配置 EXTERNAL **listener**，用于 TiDB Cloud 外部访问。选择唯一端口作为 EXTERNAL 端口，例如 `39092`。
    2. 为每个 broker 节点根据 TiDB Cloud 获取的 **Kafka Advertised Listener Pattern** 配置 EXTERNAL **advertised listener**，帮助 TiDB Cloud 区分不同 broker。不同的 EXTERNAL advertised listener 便于 TiDB Cloud 的 Kafka 客户端路由请求到正确的 broker。

        - `<port>` 用于区分 Kafka Private Link Service 的不同 broker 访问点。请为所有 broker 的 EXTERNAL advertised listener 规划端口范围，例如从 9093 开始。这些端口不必是 broker 实际监听的端口，而是负载均衡器为 Private Link Service 监听并转发到不同 broker 的端口。

      建议为不同 broker 配置不同的 broker ID，便于排查问题。

2. 使用 SSH 登录每个 broker 节点，修改每个 broker 的配置文件，内容如下：

    ```properties
    # brokers in ap-southeast-1a

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”中的 “Kafka Advertised Listener Pattern” 添加 EXTERNAL advertised listener
    # 1. 模式为 "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"
    # 2. EXTERNAL 可为 "b1.unique_name.alicloud.plc.tidbcloud.com:9093"，<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9093）替换
    advertised.listeners=...,EXTERNAL://b1.unique_name.alicloud.plc.tidbcloud.com:9093

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```
 
    ```properties
    # brokers in ap-southeast-1b

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”中的 “Kafka Advertised Listener Pattern” 添加 EXTERNAL advertised listener
    # 1. 模式为 "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"
    # 2. EXTERNAL 可为 "b2.unique_name.alicloud.plc.tidbcloud.com:9094"，<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9094）替换
    advertised.listeners=...,EXTERNAL://b2.unique_name.alicloud.plc.tidbcloud.com:9094

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

    ```properties
    # brokers in ap-southeast-1c

    # 添加 EXTERNAL listener
    listeners=INTERNAL:...,EXTERNAL://0.0.0.0:39092

    # 按“前置条件”中的 “Kafka Advertised Listener Pattern” 添加 EXTERNAL advertised listener
    # 1. 模式为 "<broker_id>.unique_name.alicloud.plc.tidbcloud.com:<port>"
    # 2. EXTERNAL 可为 "b2.unique_name.alicloud.plc.tidbcloud.com:9095"，<broker_id> 用 "b" 前缀加 "node.id"，<port> 用 EXTERNAL advertised listener 端口范围内唯一端口（9095）替换
    advertised.listeners=...,EXTERNAL://b3.unique_name.alicloud.plc.tidbcloud.com:9095

    # 配置 EXTERNAL map
    listener.security.protocol.map=...,EXTERNAL:PLAINTEXT
    ```

3. 重新配置所有 broker 后，依次重启 Kafka broker。

#### 2. 在内网测试 EXTERNAL listener 设置

你可以在 Kafka 客户端节点下载 Kafka 和 OpenJDK。

```shell
# 下载 Kafka 和 OpenJDK 并解压。可根据需要选择二进制版本。
wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```

执行以下脚本，测试 bootstrap 是否正常。

```shell
export JAVA_HOME=/root/jdk-22.0.2

# 从 EXTERNAL listener 启动
./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {one_of_broker_ip}:39092

# 期望输出最后 3 行（实际顺序可能不同）
# 因 advertised listener 在你的 Kafka 网络内无法解析，可能出现异常或错误。
# 在你通过 Private Link 创建 changefeed 连接该 Kafka 集群时，TiDB Cloud 侧会使其可解析并路由到正确 broker。
b1.ap-southeast-1a.unique_name.alicloud.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b2.ap-southeast-1b.unique_name.alicloud.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
b3.ap-southeast-1c.unique_name.alicloud.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
```

## 步骤 2. 将 Kafka 集群暴露为私有链路服务

### 1. 配置负载均衡器

创建一个网络负载均衡器，包含四个不同端口的服务器组。一个服务器组用于 bootstrap，其他分别映射到不同 broker。

1. bootstrap 服务器组 => 9092 => broker-node1:39092,broker-node2:39092,broker-node3:39092
2. broker 服务器组 1  => 9093 => broker-node1:39092
3. broker 服务器组 2  => 9094 => broker-node2:39092
4. broker 服务器组 3  => 9095 => broker-node3:39092

如有更多 broker 角色节点，需增加映射。确保 bootstrap 目标组至少有一个节点，建议每个 AZ 各加一个节点以增强可用性。

配置负载均衡器步骤如下：

1. 进入 [服务器组](https://slb.console.alibabacloud.com/nlb/ap-southeast-1/server-groups) 创建四个服务器组。

    - Bootstrap 服务器组 

        - **服务器组类型**：选择 `服务器`
        - **服务器组名称**：`bootstrap-server-group`
        - **VPC**：`Kafka VPC`
        - **后端服务器协议**：选择 `TCP`
        - **后端服务器**：点击已创建的服务器组，添加后端服务器，包括 `broker-node1:39092`、`broker-node2:39092`、`broker-node3:39092`

    - Broker 服务器组 1

        - **服务器组类型**：选择 `服务器`
        - **服务器组名称**：`broker-server-group-1`
        - **VPC**：`Kafka VPC`
        - **后端服务器协议**：选择 `TCP`
        - **后端服务器**：点击已创建的服务器组，添加后端服务器 `broker-node1:39092`

    - Broker 服务器组 2

        - **服务器组类型**：选择 `服务器`
        - **服务器组名称**：`broker-server-group-2`
        - **VPC**：`Kafka VPC`
        - **后端服务器协议**：选择 `TCP`
        - **后端服务器**：点击已创建的服务器组，添加后端服务器 `broker-node2:39092`

    - Broker 服务器组 3

        - **服务器组类型**：选择 `服务器`
        - **服务器组名称**：`broker-server-group-3`
        - **VPC**：`Kafka VPC`
        - **后端服务器协议**：选择 `TCP`
        - **后端服务器**：点击已创建的服务器组，添加后端服务器 `broker-node3:39092`

2. 进入 [NLB](https://slb.console.alibabacloud.com/nlb) 创建网络负载均衡器。

    - **网络类型**：选择 `内网`
    - **VPC**：`Kafka VPC`
    - **可用区**： 
      - `ap-southeast-1a` 选择 `broker-ap-southeast-1a vswitch`
      - `ap-southeast-1b` 选择 `broker-ap-southeast-1b vswitch`
      - `ap-southeast-1c` 选择 `broker-ap-southeast-1c vswitch`
    - **IP 版本**：选择 `IPv4`
    - **实例名称**：`kafka-nlb`
    - 点击 **立即创建** 创建负载均衡器。

3. 找到已创建的负载均衡器，点击 **创建监听**，创建四个 TCP 监听。

    - Bootstrap 服务器组 

        - **监听协议**：选择 `TCP`
        - **监听端口**：`9092`
        - **服务器组**：选择之前创建的 `bootstrap-server-group`

    - Broker 服务器组 1

        - **监听协议**：选择 `TCP`
        - **监听端口**：`9093`
        - **服务器组**：选择之前创建的 `broker-server-group-1`

    - Broker 服务器组 2

        - **监听协议**：选择 `TCP`
        - **监听端口**：`9094`
        - **服务器组**：选择之前创建的 `broker-server-group-2`

    - Broker 服务器组 3

        - **监听协议**：选择 `TCP`
        - **监听端口**：`9095`
        - **服务器组**：选择之前创建的 `broker-server-group-3`

4. 在堡垒机节点测试负载均衡器。此示例仅测试 Kafka bootstrap。由于负载均衡器监听的是 Kafka EXTERNAL listener，EXTERNAL advertised listener 的地址在堡垒机节点无法解析。请记录负载均衡器详情页的 `kafka-lb` DNS 名称，例如 `nlb-o21d6wyjknamw8hjxb.ap-southeast-1.nlb.aliyuncsslbintl.com`。在堡垒机节点执行如下脚本。

    ```shell
    # 将 {lb_dns_name} 替换为实际值
    export JAVA_HOME=~/jdk-22.0.2
    ./kafka_2.13-3.7.1/bin/kafka-broker-api-versions.sh --bootstrap-server {lb_dns_name}:9092

    # 期望输出最后 3 行（实际顺序可能不同）
    b1.unique_name.alicloud.plc.tidbcloud.com:9093 (id: 1 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b2.unique_name.alicloud.plc.tidbcloud.com:9094 (id: 2 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    b3.unique_name.alicloud.plc.tidbcloud.com:9095 (id: 3 rack: null) -> ERROR: org.apache.kafka.common.errors.DisconnectException
    ```

### 2. 配置阿里云 endpoint service

在同一 Region 配置 endpoint service。

1. 进入 [Endpoint service](https://vpc.console.alibabacloud.com/endpointservice) 创建 endpoint service。

    - **服务资源类型**：选择 `NLB`
    - **选择服务资源**：选择 NLB 所在所有可用区，并选择上一步创建的 NLB
    - **自动接受 endpoint 连接**：建议选择 `否`

2. 进入 endpoint service 详情页，复制 **Endpoint Service Name**，如 `com.aliyuncs.privatelink.<region>.xxxxx`。后续在 TiDB Cloud 侧使用。

3. 在 endpoint service 详情页，点击 **服务白名单** 标签，点击 **添加到白名单**，输入你在 [前置条件](#prerequisites) 获取的阿里云账户 ID。

## 步骤 3. 在 TiDB Cloud 创建私有链路连接

在 TiDB Cloud 创建私有链路连接，步骤如下：

1. 在 TiDB Cloud 使用你在 [步骤 2](#2-set-up-an-alibaba-cloud-endpoint-service) 获取的阿里云 endpoint service 名称（如 `com.aliyuncs.privatelink.<region>.xxxxx`）创建私有链路连接。

    详细操作见 [创建阿里云 Endpoint Service 私有链路连接](/tidb-cloud/serverless-private-link-connection.md#create-an-alibaba-cloud-endpoint-service-private-link-connection)。

2. 将域名绑定到私有链路连接，使 TiDB Cloud 的数据流服务可以访问 Kafka 集群。

    详细操作见 [为私有链路连接绑定域名](/tidb-cloud/serverless-private-link-connection.md#attach-domains-to-a-private-link-connection)。注意在 **Attach Domains** 对话框中，需选择 **TiDB Cloud Managed** 作为域名类型，并复制生成域名的 unique name 以备后用。

## 步骤 4. 替换 Kafka 配置中的 unique name 占位符

1. 回到你的 Kafka broker 节点，将每个 broker 的 `advertised.listeners` 配置中的 `unique_name` 占位符替换为上一步获取的实际 unique name。
2. 重新配置所有 broker 后，依次重启 Kafka broker。

现在，你可以使用该私有链路连接和 9092 作为 bootstrap 端口，从 TiDB Cloud 连接到你的 Kafka 集群。