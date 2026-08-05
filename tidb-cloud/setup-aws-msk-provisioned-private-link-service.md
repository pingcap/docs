---
title: 通过 AWS PrivateLink 设置 Amazon MSK Provisioned 集群
summary: 本文档介绍如何设置 Amazon MSK Provisioned 集群，并使用 AWS PrivateLink 将其连接到 TiDB Cloud。
---

# 通过 AWS PrivateLink 设置 Amazon MSK Provisioned 集群

在 TiDB Cloud 中为 Amazon MSK Provisioned 下游服务[创建私有端点](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md)之前，请先配置 MSK 集群，使其支持来自 TiDB Cloud Premium 实例通过 AWS PrivateLink 发起的连接。

本文介绍如何使用[多 VPC 连接](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html)和 [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)，将 TiDB Cloud Premium 实例连接到 [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) 集群。

本指南涵盖完整的设置流程：准备网络和凭证、创建并配置 MSK 集群、启用多 VPC 连接、附加集群策略，以及从 TiDB Cloud 建立 PrivateLink 连接。

## 前提条件 {#prerequisites}

- 一个托管在 AWS 上且处于 **Active** 状态的 [TiDB Cloud Premium 实例](/tidb-cloud/premium/create-tidb-instance-premium.md)。
- TiDB Cloud Premium 实例的 **AWS Account ID** 和 **availability zone IDs (AZ IDs)**。

  获取这些值的方法如下：

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，进入你的实例概览页面，然后点击 **Settings** > **Networking**。
    2. 在 **Private Link Endpoint For External Services** 区域，点击 **Create Private Endpoint for External Services**。
    3. 在弹出的对话框中，将 **Connection Type** 切换为 **AWS MSK Provisioned**，并记下 **AWS Account ID** 和 **availability zone IDs**（例如 `use1-az1`）。

    **关于 AZ 对齐的重要说明**：在跨 AWS 账户验证可用区对齐时，请使用 AZ ID（例如 `use1-az1`），而不是 AZ 名称（例如 `us-east-1a`）。相同的 AZ 名称在不同账户中可能映射到不同的物理可用区。你的 MSK 集群必须使用与 TiDB Cloud Premium 实例相同的 AZ ID。

## 第 1 步：设置 Amazon VPC 和子网 {#step-1-set-up-the-amazon-vpc-and-subnets}

如果你已经有一个 Amazon VPC，并且其中至少包含跨所需可用区的三个私有子网，则可以跳过此步骤。

1. 在 [Amazon VPC 控制台](https://console.aws.amazon.com/vpc/)中，[创建一个 VPC](https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html)，并创建三个私有子网，每个子网对应一个运行 TiDB Cloud Premium 实例的可用区。这些子网必须位于相同的 AZ 中，并且应通过 AZ ID 而不是 AZ 名称进行匹配。
2. 在 VPC 仪表板中，配置路由表和安全组，以便你后续启动的任何客户端 EC2 实例都可以通过私有网络与 MSK 集群通信。
3. 记录这些子网的 AZ ID。你将在[创建 MSK 集群](#step-3-create-an-amazon-msk-provisioned-cluster)时选择这些子网。

## 第 2 步：在 AWS Secrets Manager 中创建 SCRAM secret {#step-2-create-a-scram-secret-in-aws-secrets-manager}

在 [AWS Secrets Manager 控制台](https://console.aws.amazon.com/secretsmanager/)中，[创建一个 secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html)，用于存储 TiDB Cloud 连接到你的 MSK 集群时使用的 SASL/SCRAM 凭证。

创建 secret 时，请注意以下事项：

- 选择 **Other type of secrets**。
- 对于 **Secret value**，提供一个包含用户名和密码的 JSON 对象。
- 对于 **Encryption key**，选择一个客户管理的 AWS KMS key。Amazon MSK 不能使用默认的 AWS 托管 key。如果你还没有客户管理的 key，请先[创建一个对称加密 KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk)。
- secret 名称必须以 `AmazonMSK_` 为前缀（例如 `AmazonMSK_tidb_msk`）。

## 第 3 步：创建 Amazon MSK Provisioned 集群 {#step-3-create-an-amazon-msk-provisioned-cluster}

如果你已有一个满足以下条件的 Amazon MSK Provisioned 集群，请跳过此步骤。

- **Region**：与 TiDB Cloud Premium 实例位于相同的 AWS region。
- **Availability Zones**：必须与 TiDB Cloud Premium 实例的 AZ 一致（通过 AZ ID 验证，而不是 AZ 名称）。
- **Authentication**：为 TiDB Cloud 连接启用 [SASL/SCRAM](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html)。虽然 AWS MSK 多 VPC 连接也支持 IAM 和 TLS 认证，但本设置使用 SASL/SCRAM。
- **Broker type**：不支持 `t3.small`。请选择更大的 broker 类型。
- **Public access**：必须禁用。
- [Amazon MSK 多 VPC 私有连接文档](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html#mvpc-requirements)中列出的其他要求。

如果你没有满足上述要求的 MSK 集群，请前往 [Amazon MSK 控制台](https://console.aws.amazon.com/msk/)，使用你在[第 1 步](#step-1-set-up-the-amazon-vpc-and-subnets)中设置的相同 region、VPC 和子网[创建一个集群](https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html)，并按以下设置进行配置：

- **Kafka version**：使用 TiDB Cloud 支持的版本（例如 3.7.x）。
- **Broker type**：选择多 VPC 私有连接支持的 broker 类型（不是 `t3.small`）。
- **Authentication**：启用 SASL/SCRAM 认证。
- **Public access**：禁用此选项。
- **Number of brokers**：每个可用区至少一个（最少 3 个）。
- **Encryption in transit**：根据你的安全要求进行配置。
- **Client subnets**：选择在[第 1 步](#step-1-set-up-the-amazon-vpc-and-subnets)中创建的三个私有子网。
- **Cluster configuration**：创建一个自定义配置，并包含以下设置（初始 ACL 设置所必需）：
    - `auto.create.topics.enable=true`
    - `allow.everyone.if.no.acl.found=true`

创建完成后，等待集群状态变为 **Active**，并从集群的 **Summary** 部分记下 **Cluster ARN**。

## 第 4 步：将 SCRAM secret 关联到 Amazon MSK Provisioned 集群 {#step-4-associate-the-scram-secret-with-the-amazon-msk-provisioned-cluster}

1. 在 [Amazon MSK 控制台](https://console.aws.amazon.com/msk/)中，进入你的 MSK 集群的 **Properties** 标签页，然后找到 **SASL/SCRAM authentication** 部分。
2. 将你在[第 2 步](#step-2-create-a-scram-secret-in-aws-secrets-manager)中创建的 secret[关联](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password-tutorial.html)到该集群。

关联完成后，请等待大约 30 秒，让凭证传播完成，然后再继续进行 ACL 设置。

## 第 5 步：设置 Kafka ACL {#step-5-set-up-kafka-acls}

TiDB Cloud 需要 Kafka ACL 才能向你的集群生产消息。ACL 必须在与你的 MSK 集群相同的 VPC 内创建。

### 5.1 准备客户端 EC2 实例 {#51-prepare-a-client-ec2-instance}

1. 在 [Amazon EC2 控制台](https://console.aws.amazon.com/ec2/home#Instances)中，在与你的 MSK 集群相同的 VPC 和其中一个相同子网内启动一个 Amazon Linux EC2 实例。

    > **Tip:**
    >
    > 你可以使用 [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) 访问该实例，而无需将 SSH 访问暴露到公共互联网。

2. 在 EC2 实例上，下载并解压 Apache Kafka 和 OpenJDK 压缩包：

    ```bash
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. 将 OpenJDK 添加到 `PATH` 环境变量中：

    ```bash
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    ```

### 5.2 创建 SCRAM 客户端属性文件 {#52-create-the-scram-client-properties-file}

在 EC2 实例上，创建一个名为 `scram-client.properties` 的文件，内容如下：

```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="<your-scram-username>" \
    password="<your-scram-password>";
```

### 5.3 获取 bootstrap broker 字符串 {#53-get-the-bootstrap-broker-string}

1. 在 [Amazon MSK 控制台](https://console.aws.amazon.com/msk/)中，打开你的 MSK 集群的 **Summary** 部分。
2. 点击右上角的 **View client information**。
3. 在对话框中，找到 **SASL/SCRAM Private endpoint** 条目。它就是你的 bootstrap broker 字符串。复制它，以便在后续的[第 5.4 步](#54-create-the-acls)中使用。

### 5.4 创建 ACL {#54-create-the-acls}

在 EC2 实例上，运行以下命令，为 SCRAM 用户授予对所有 topic、consumer group 和集群的完全访问权限：

```bash
export BOOTSTRAP=<sasl-scram-private-endpoint>

/home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh \
  --bootstrap-server $BOOTSTRAP --command-config scram-client.properties \
  --add --allow-principal User:<scram-username> --operation All --topic '*'

/home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh \
  --bootstrap-server $BOOTSTRAP --command-config scram-client.properties \
  --add --allow-principal User:<scram-username> --operation All --group '*'

/home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh \
  --bootstrap-server $BOOTSTRAP --command-config scram-client.properties \
  --add --allow-principal User:<scram-username> --operation All --cluster
```

如果你遇到间歇性的认证失败，请等待几秒钟后重试。新的 SCRAM 凭证可能需要一些时间才能传播到所有 broker。

## 第 6 步：修改集群配置 {#step-6-update-the-cluster-configuration}

创建 ACL 后，请按如下方式修改集群配置：

- 保持 `auto.create.topics.enable` 为 `true`。
- 将 `allow.everyone.if.no.acl.found` 设置为 `false`。

在 [Amazon MSK 控制台](https://console.aws.amazon.com/msk/)中，在 **Cluster configuration** 下应用修改后的配置。等待集群状态恢复为 **Active**。

## 第 7 步：开启多 VPC 连接 {#step-7-turn-on-multi-vpc-connectivity}

多 VPC 连接是 AWS 的一项功能，可为你的 MSK 集群启用 PrivateLink 访问。你需要显式启用此功能。

1. 在 [Amazon MSK 控制台](https://console.aws.amazon.com/msk/)中，进入你的 MSK 集群的 **Properties** 标签页。在 **Network settings** > **Multi-VPC connectivity** 下，[开启多 VPC 连接](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-turn-on.html)。
2. 将 VPC 连接的客户端认证配置为仅使用 **SASL/SCRAM** 认证（TiDB Cloud 连接不需要 IAM 和 mutual TLS (mTLS) 认证）。

    等待集群修改完成。此操作通常需要大约 40 到 60 分钟。你可以在 MSK 控制台的 **Cluster operations** 标签页中监控其进度。等待集群状态恢复为 **Active**。

3. 修改完成后，确认以下内容：

    - 已启用多 VPC 连接。
    - `PublicAccess` 已禁用。
    - 已为 VPC 连接启用 SASL/SCRAM 认证。

## Step 8. 关联集群策略 {#step-8-attach-a-cluster-policy}

将基于资源的集群策略关联到你的 MSK 集群，以授予你的 TiDB Cloud Premium 实例连接权限。

1. 在 [Amazon MSK console](https://console.aws.amazon.com/msk/) 中，进入你的 MSK 集群。
2. 在 **Security settings** 下，点击 **Edit cluster policy**。
3. 在集群策略编辑器中，粘贴基于资源的集群策略 JSON，然后点击 **Save changes**。

    > **Warning:**
    >
    > 在该策略中，`Principal` 必须是 TiDB Cloud Premium 实例的 AWS account ID（在[前提条件](#prerequisites)中获取），而不是你自己的 AWS account ID。如果指定了错误的 principal，连接将失败。

    以下是一个策略示例，供你参考：

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "<tidb-cloud-aws-account-id>"
          },
          "Action": [
            "kafka:CreateVpcConnection",
            "kafka:GetBootstrapBrokers",
            "kafka:DescribeCluster",
            "kafka:DescribeClusterV2",
            "kafka-cluster:*"
          ],
          "Resource": "arn:aws:kafka:<region>:<account-id>:cluster/<cluster-name>/*"
        },
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "<tidb-cloud-aws-account-id>"
          },
          "Action": "kafka-cluster:*",
          "Resource": "arn:aws:kafka:<region>:<account-id>:topic/<cluster-name>/*"
        },
        {
          "Effect": "Allow",
          "Principal": {
            "AWS": "<tidb-cloud-aws-account-id>"
          },
          "Action": "kafka-cluster:*",
          "Resource": "arn:aws:kafka:<region>:<account-id>:group/<cluster-name>/*"
        }
      ]
    }
    ```

更多信息，请参见 [Attach a cluster policy to the MSK cluster](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-policy.html)。

## Step 9. 在 TiDB Cloud 中创建 PrivateLink 连接 {#step-9-create-the-privatelink-connection-in-tidb-cloud}

在 [TiDB Cloud console](https://tidbcloud.com) 中，使用你的 MSK 集群 ARN 创建 private link connection。

更多信息，请参见 [Create an Amazon MSK Provisioned private link connection](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md#step-2-configure-the-private-endpoint-for-changefeeds)。