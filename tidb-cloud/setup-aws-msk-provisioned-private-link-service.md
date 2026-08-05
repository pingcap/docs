---
title: Set Up an Amazon MSK Provisioned Cluster via AWS PrivateLink
summary: This document explains how to set up an Amazon MSK Provisioned cluster and connect it to TiDB Cloud using AWS PrivateLink.
---

# Set Up an Amazon MSK Provisioned Cluster via AWS PrivateLink

Before [creating a private endpoint](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md) for an Amazon MSK Provisioned downstream service in TiDB Cloud, configure the MSK cluster to support connections from your TiDB Cloud Premium instance through AWS PrivateLink.

This document describes how to connect a TiDB Cloud Premium instance to an [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) cluster using [multi-VPC connectivity](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html) and [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html).

This guide covers the entire setup process: preparing the network and credentials, creating and configuring the MSK cluster, enabling multi-VPC connectivity, attaching a cluster policy, and establishing a PrivateLink connection from TiDB Cloud.

## Prerequisites

- A [TiDB Cloud Premium instance](/tidb-cloud/premium/create-tidb-instance-premium.md) hosted on AWS in the **Active** state.
- The **AWS Account ID** and **availability zone IDs (AZ IDs)** of the TiDB Cloud Premium instance.

  To retrieve these values:

    1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the overview page of your instance, and then click **Settings** > **Networking**.
    2. In the **Private Link Endpoint For External Services** area, click **Create Private Endpoint for External Services**.
    3. In the dialog, switch the **Connection Type** to **AWS MSK Provisioned**, and note the **AWS Account ID** and **availability zone IDs** (for example, `use1-az1`).

    **Important about AZ alignment**: Use AZ IDs (for example, `use1-az1`) rather than AZ names (for example, `us-east-1a`) when verifying availability zone alignment across AWS accounts. The same AZ name can map to different physical zones in different accounts. Your MSK cluster must use the same AZ IDs as your TiDB Cloud Premium instance.

## Step 1. Set up the Amazon VPC and subnets

If you already have an Amazon VPC with at least three private subnets spanning the required availability zones, you can skip this step.

1. In the [Amazon VPC console](https://console.aws.amazon.com/vpc/), [create a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html) with three private subnets, one per availability zone in which your TiDB Cloud Premium instance runs. These subnets must be in the same AZs, matched by AZ ID rather than AZ name.
2. In the VPC dashboard, configure route tables and security groups so that any client EC2 instance you launch later can communicate with the MSK cluster over the private network.
3. Record the AZ IDs of the subnets. You will select these subnets when [creating the MSK cluster](#step-3-create-an-amazon-msk-provisioned-cluster).

## Step 2. Create a SCRAM secret in AWS Secrets Manager

In the [AWS Secrets Manager console](https://console.aws.amazon.com/secretsmanager/), [create a secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) to store the SASL/SCRAM credentials that TiDB Cloud will use to authenticate to your MSK cluster.

When creating the secret, note the following:

- Select **Other type of secrets**.
- For **Secret value**, provide a JSON object containing the username and password.
- For **Encryption key**, select a customer managed AWS KMS key. The default AWS managed key cannot be used with Amazon MSK. If you do not have a customer managed key, [create a symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk) before proceeding.
- The secret name must start with the prefix `AmazonMSK_` (for example, `AmazonMSK_tidb_msk`).

## Step 3. Create an Amazon MSK Provisioned cluster

If you have an existing Amazon MSK Provisioned cluster that meets the following conditions, skip this step.

- **Region**: same AWS region as your TiDB Cloud Premium instance.
- **Availability Zones**: must match your TiDB Cloud Premium instance's AZs (verified by AZ ID, not AZ name).
- **Authentication**: enable [SASL/SCRAM](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html) for the TiDB Cloud connection. Although AWS MSK multi-VPC connectivity also supports IAM and TLS authentication, this setup uses SASL/SCRAM.
- **Broker type**: `t3.small` is not supported. Select a larger broker type.
- **Public access**: must be disabled.
- Additional requirements listed in [Amazon MSK multi-VPC private connectivity documentation](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html#mvpc-requirements).

If you do not have an MSK cluster that meets the preceding requirements, go to the [Amazon MSK console](https://console.aws.amazon.com/msk/), and [create one](https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html) using the same region, VPC, and subnets as you set up in [Step 1](#step-1-set-up-the-amazon-vpc-and-subnets), and follow these settings:

- **Kafka version**: use a version supported by TiDB Cloud (for example, 3.7.x).
- **Broker type**: select a broker type supported by multi-VPC private connectivity (not `t3.small`).
- **Authentication**: enable SASL/SCRAM authentication.
- **Public access**: disable this option.
- **Number of brokers**: at least one per availability zone (minimum of 3).
- **Encryption in transit**: configure according to your security requirements.
- **Client subnets**: select the three private subnets created in [Step 1](#step-1-set-up-the-amazon-vpc-and-subnets).
- **Cluster configuration**: create a custom configuration with these settings (required for initial ACL setup):
    - `auto.create.topics.enable=true`
    - `allow.everyone.if.no.acl.found=true`

After creation, wait for the cluster status to become **Active** and note the **Cluster ARN** from the cluster's **Summary** section.

## Step 4. Associate the SCRAM secret with the Amazon MSK Provisioned cluster

1. In the [Amazon MSK console](https://console.aws.amazon.com/msk/), navigate to **Properties** tab of your MSK cluster, and then locate the **SASL/SCRAM authentication** section.
2. [Associate the secret](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password-tutorial.html) you created in [Step 2](#step-2-create-a-scram-secret-in-aws-secrets-manager) with the cluster.

After the association is complete, wait approximately 30 seconds for the credentials to propagate before proceeding with ACL setup.

## Step 5. Set up Kafka ACLs

TiDB Cloud requires Kafka ACLs to produce messages to your cluster. ACLs must be created within the same VPC as your MSK cluster.

### 5.1 Prepare a client EC2 instance

1. In the [Amazon EC2 console](https://console.aws.amazon.com/ec2/home#Instances), launch an Amazon Linux EC2 instance in the same VPC and one of the same subnets as your MSK cluster.

    > **Tip:**
    >
    > You can use [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) to access the instance without exposing SSH access to the public internet.

2. On the EC2 instance, download and extract the Apache Kafka and OpenJDK archives:

    ```bash
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. Add OpenJDK to the `PATH` environment variable:

    ```bash
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    ```

### 5.2 Create the SCRAM client properties file

On the EC2 instance, create a file named `scram-client.properties` with the following content:

```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="<your-scram-username>" \
    password="<your-scram-password>";
```

### 5.3 Get the bootstrap broker string

1. In the [Amazon MSK console](https://console.aws.amazon.com/msk/), open the **Summary** section of your MSK cluster.
2. Click **View client information** in the upper-right corner.
3. In the dialog, locate the **SASL/SCRAM Private endpoint** entry. It is your bootstrap broker string. Copy it for later use in [Step 5.4](#54-create-the-acls).

### 5.4 Create the ACLs

On the EC2 instance, run the following commands to grant the SCRAM user full access to all topics, consumer groups, and the cluster:

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

If you encounter intermittent authentication failures, wait a few seconds and try again. New SCRAM credentials might take some time to propagate to all brokers.

## Step 6. Update the cluster configuration

After creating the ACLs, update the cluster configuration as follows:

- Keep `auto.create.topics.enable` as `true`.
- Set `allow.everyone.if.no.acl.found` to `false`.

In the [Amazon MSK console](https://console.aws.amazon.com/msk/), apply the updated configuration under **Cluster configuration**. Wait for the cluster status to return to **Active**.

## Step 7. Turn on multi-VPC connectivity

Multi-VPC connectivity is an AWS feature that enables PrivateLink access to your MSK cluster. You need to enable it explicitly.

1. In the [Amazon MSK console](https://console.aws.amazon.com/msk/), go to the **Properties** tab of your MSK cluster. Under **Network settings** > **Multi-VPC connectivity**, [turn on multi-VPC connectivity](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-turn-on.html).
2. Configure the VPC connectivity client authentication to use **SASL/SCRAM** authentication only (IAM and mutual TLS (mTLS) authentication are not needed for the TiDB Cloud connection).

    Wait for the cluster update to complete. This operation typically takes approximately 40 to 60 minutes. You can monitor its progress on the **Cluster operations** tab in the MSK console. Wait for the cluster status to return to **Active**.

3. After the update is complete, confirm the following:

    - Multi-VPC connectivity is enabled.
    - `PublicAccess` is disabled.
    - SASL/SCRAM authentication is enabled for VPC connectivity.

## Step 8. Attach a cluster policy

Attach a resource-based cluster policy to your MSK cluster to grant your TiDB Cloud Premium instance permission to connect.

1. In the [Amazon MSK console](https://console.aws.amazon.com/msk/), navigate to your MSK cluster.
2. Under **Security settings**, click **Edit cluster policy**.
3. In the cluster policy editor, paste the JSON for a resource-based cluster policy, and then click **Save changes**.

    > **Warning:**
    >
    > In the policy, the `Principal` must be the AWS account ID of the TiDB Cloud Premium instance (obtained in the [prerequisites](#prerequisites)), not your own AWS account ID. The connection will fail if you specify the wrong principal.

    The following is an example policy for your reference:

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

For more information, see [Attach a cluster policy to the MSK cluster](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-policy.html).

## Step 9. Create the PrivateLink connection in TiDB Cloud

In the [TiDB Cloud console](https://tidbcloud.com), create the private link connection using the ARN of your MSK cluster.

For more information, see [Create an Amazon MSK Provisioned private link connection](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md#step-2-configure-the-private-endpoint-for-changefeeds).
