---
title: 通过 Private Link 连接访问 Amazon MSK Provisioned
summary: 了解如何使用 Amazon MSK Provisioned Private Link 连接访问 Amazon MSK Provisioned 集群。
---

# 通过 Private Link 连接访问 Amazon MSK Provisioned

本文档介绍如何通过 [Amazon MSK Provisioned Private Link 连接](/tidb-cloud/serverless-private-link-connection.md#create-an-amazon-msk-provisioned-private-link-connection) 将 TiDB Cloud Essential 实例连接到 [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) 集群。

## TiDB Cloud Essential 的前置条件 {#prerequisites-for-essential}

- 你的 TiDB Cloud Essential 实例托管在 AWS 上并处于活跃状态。请获取并保存以下信息以备后用：

    - AWS 账户 ID
    - 可用区（AZ）

查看 AWS 账户 ID 和可用区的方法如下：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入你的 TiDB Cloud Essential 实例的总览页面，然后点击左侧导航栏的 **Settings** > **Networking**。
2. 在 **Private Link Connection For Dataflow** 区域，点击 **Create Private Link Connection**。
3. 在弹窗中，记下 AWS 账户 ID 和可用区信息。

## Amazon MSK Provisioned 集群的前置条件

在开始之前，请确保你的 Amazon MSK Provisioned 集群满足以下条件：
 
- **Region 和 AZ**：你的 Amazon MSK Provisioned 集群与 TiDB Cloud Essential 实例位于同一个 AWS Region，且 MSK 集群的可用区与 TiDB Cloud Essential 实例一致。
- **认证**：MSK 集群需要启用 [SASL/SCRAM 认证](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html)。
- **Broker 类型**：不要使用 `t4.small` broker 类型。该类型不支持 Private Link。
    
更多要求请参见 [Amazon MSK 单 Region 多 VPC 私有连接要求](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html#mvpc-requirements)。
    
如果你还没有 Amazon MSK Provisioned 集群，请在与你的 TiDB Cloud Essential 实例相同的 Region 和可用区 [创建一个集群](https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html)，并为新建的集群 [配置 SASL/SCRAM 认证](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password-tutorial.html)。

- **Secret name**：secret 名称必须以 `AmazonMSK_` 开头。
- **加密**：不要使用默认加密密钥。请为你的 secret 创建新的自定义 AWS KMS 密钥。

## 步骤 1. 为 TiDB Cloud 访问配置 Kafka ACL

你必须配置 Kafka ACL，以便 TiDB Cloud 能够访问你的 Amazon MSK Provisioned 集群。你可以使用 SASL/SCRAM 认证（推荐）或 IAM 认证来配置 ACL。

<SimpleTab>
<div label="SASL/SCRAM">

使用此方法在与你的 MSK 集群相同的 VPC 内，通过 SASL/SCRAM 认证创建 ACL。

1. 在 MSK 集群所在的 VPC 内创建一台 EC2 实例（Linux），并通过 SSH 连接到该实例。

2. 下载 Kafka 和 OpenJDK：

    ```shell
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. 配置环境变量。请将路径替换为你的实际路径。

    ```shell
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    ```

4. 创建名为 `scram-client.properties` 的文件，并写入以下内容。将 `username` 和 `pswd` 替换为你的 SASL/SCRAM 凭证：

    ```properties
    security.protocol=SASL_SSL
    sasl.mechanism=SCRAM-SHA-512
    sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
        username="username" \
        password="pswd";
    ```

5. 创建 ACL。将 `bootstrap-server` 替换为你的 MSK 启动服务器地址和端口（例如，`b-2.xxxxx.c18.kafka.us-east-1.amazonaws.com:9096`），如有需要也可替换 Kafka 路径：

    ```shell
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --topic '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --group '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --cluster '*'
    ```

    其中 principal `User:<username>` 是 TiDB Cloud 用于访问你的 MSK 集群的 SASL/SCRAM 用户。请使用你在 MSK ACL 中为 TiDB Cloud 配置的用户名。

</div>

<div label="IAM">

作为 SASL/SCRAM 的替代方案，你也可以在与你的 MSK 集群相同的 VPC 内，通过 IAM 认证创建 ACL。IAM 用户或角色必须拥有 **Amazon MSK** 和 **Apache Kafka APIs for MSK** 权限。

1. 在 MSK 集群所在的 VPC 内创建一台 EC2 实例（Linux），并通过 SSH 连接到该实例。

2. 下载 Kafka、OpenJDK 以及 AWS MSK IAM 认证 JAR 包：

    ```shell
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    wget https://github.com/aws/aws-msk-iam-auth/releases/download/v2.3.5/aws-msk-iam-auth-2.3.5-all.jar
    ```

3. 配置环境变量。请将路径和凭证替换为你自己的值。

    ```shell
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    export CLASSPATH=/home/ec2-user/aws-msk-iam-auth-2.3.5-all.jar
    export AWS_ACCESS_KEY_ID=<your-access-key-id>
    export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
    ```

4. 创建名为 `iam-client.properties` 的文件，并写入以下内容：

    ```properties
    security.protocol=SASL_SSL
    sasl.mechanism=AWS_MSK_IAM
    sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;
    sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler
    ```

5. 创建 ACL。将 `bootstrap-server` 替换为你的 MSK 启动服务器地址和端口（例如，`b-1.xxxxx.c18.kafka.us-east-1.amazonaws.com:9098`），如有需要也可替换 Kafka 路径：

    ```shell
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --topic '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --group '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --cluster '*'
    ```

    其中 principal `User:<username>` 是 TiDB Cloud 用于访问你的 MSK 集群的 SASL/SCRAM 用户。请使用你在 MSK ACL 中为 TiDB Cloud 配置的用户名。

</div>
</SimpleTab>

## 步骤 2. 配置 MSK 集群

更新以下集群配置属性：

- 设置 `auto.create.topics.enable=true`。
- 添加 `allow.everyone.if.no.acl.found=false`（SASL/SCRAM 必需）。
- 其他属性保持不变或根据需要调整。

应用更改后，等待集群状态从 **Updating** 变为 **Active**。

## 步骤 3. 关联集群策略

[关联集群策略](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-policy.html)，以允许 TiDB Cloud 连接你的 MSK 集群。请使用你在 [前置条件](#prerequisites-for-essential) 中获取的 TiDB Cloud AWS 账户 ID。

## 步骤 4. 开启多 VPC 连接

集群变为活跃后，为 MSK 集群 [开启多 VPC 连接](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-turn-on.html)。AWS PrivateLink 需要开启多 VPC 连接。要从 TiDB Cloud 连接，必须启用 SASL/SCRAM 认证。

等待集群状态再次从 **Updating** 变为 **Active**。

## 步骤 5. 在 TiDB Cloud 中创建 Amazon MSK Provisioned Private Link 连接

使用你的 MSK 集群的 `ARN`，在 TiDB Cloud 中创建 Private Link 连接。

更多信息请参见 [创建 Amazon MSK Provisioned Private Link 连接](/tidb-cloud/serverless-private-link-connection.md#create-an-amazon-msk-provisioned-private-link-connection)。
