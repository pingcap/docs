---
title: Set Up MSK Provisioned Cluster via Private Link in AWS
summary: This document explains how to set up MSK provisioned cluster in AWS and how to make it work with TiDB Cloud.
---

# Set Up MSK Provisioned Cluster via Private Link in AWS

This document describes how to connect a TiDB Cloud Premium instance to an Amazon MSK Provisioned cluster using multi-VPC connectivity and AWS PrivateLink.

The guide covers the full lifecycle: preparing the network and credentials, creating and configuring the MSK cluster, enabling multi-VPC connectivity, attaching the cluster policy, and establishing the PrivateLink connection from TiDB Cloud.

## Prerequisites for TiDB Cloud Premium

- A TiDB Cloud Premium instance hosted on AWS in the **active** state.
- The **AWS Account ID** and **availability zone IDs (AZ IDs)** of the TiDB Cloud Premium instance.

  To retrieve these values:

    1. In the TiDB Cloud console, navigate to the overview page of your instance, and click **Settings** > **Networking**.
    2. In the **Private Link Endpoint For External Services** area, click **Create Private Endpoint for External Services**.
    3. In the dialog, switch the **Connection Type** to **AWS MSK Provisioned** and note the **AWS Account ID** and **availability zone IDs** (for example, `use1-az1`).

    > **Important about AZ alignment**: Use AZ IDs (e.g., `use1-az1`) rather than AZ names (e.g., `us-east-1a`) when verifying availability zone alignment across AWS accounts. The same AZ name can map to different physical zones in different accounts. Your MSK cluster must use the same AZ IDs as your TiDB Cloud instance.

## Prerequisites for the Amazon MSK Provisioned Cluster

Your MSK cluster must meet the following conditions (whether existing or newly created):

- **Region**: Same AWS region as your TiDB Cloud Premium instance.
- **Availability Zones**: Must match your TiDB Cloud instance AZs (verify by AZ ID, not AZ name).
- **Authentication**: Enable SASL/SCRAM for this TiDB Cloud connection. AWS MSK multi-VPC connectivity also supports IAM and TLS, but this setup uses SASL/SCRAM.
- **Broker type**: `t3.small` is not supported. Choose a larger type.
- **Public access**: Must be disabled.

For additional requirements, see [Amazon MSK multi-VPC private connectivity documentation](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html#mvpc-requirements).

## Step 1. Set Up the VPC and Subnets

If you already have a VPC with at least three private subnets spanning the required availability zones, you can skip this step.

Create a VPC in the target region with three private subnets, one per availability zone in which your TiDB Cloud instance runs. These subnets must be in the same AZs (matched by AZ ID, not AZ name). Configure route tables and security groups so that any client EC2 instance you launch later can communicate with the MSK cluster over the private network.

Record the AZ IDs of the subnets. The MSK cluster will use these subnets at creation time.

## Step 2. Create a SCRAM Secret in AWS Secrets Manager

Create a secret in AWS Secrets Manager to store the SASL/SCRAM credentials that TiDB Cloud will use to authenticate against your MSK cluster.

When creating the secret, select "Other type of secret". The name of the secret must start with the prefix AmazonMSK_ (for example, AmazonMSK_tidb_msk). Under the secret value, provide a JSON object containing the username and password.

Note: For encryption, you must use a custom AWS KMS key (create a new symmetric custom key if you do not have one); the default AWS managed key will not work.

## Step 3. Create the Provisioned MSK Cluster

If you do not already have an MSK cluster that satisfies the prerequisites, create one in the AWS Console. The cluster will inherit the region, VPC, and subnets you set up in Step 1, and must use a non-`t4.small` broker type with SASL/SCRAM authentication and public access disabled.

Additional creation settings:

- **Kafka version**: Use a version supported by TiDB Cloud (for example, 3.7.x).
- **Number of brokers**: At least one per availability zone (minimum of 3).
- **Encryption in transit**: Configure according to your security requirements.
- **Client subnets**: Select the three private subnets created in Step 1.
- **Cluster configuration**: Create a custom configuration with these settings (required for initial ACL setup):
  - `auto.create.topics.enable=true`
  - `allow.everyone.if.no.acl.found=true`

After creation, wait for the cluster status to become **Active** and note the **Cluster ARN** from the cluster's **Summary** section.

## Step 4. Associate the SCRAM Secret with the MSK Cluster

In the AWS MSK console, navigate to your cluster's **Properties** tab and find the **SASL/SCRAM authentication** section. Associate the secret you created in Step 2 with the cluster.

After the association completes, wait approximately 30 seconds for the credentials to propagate before proceeding with ACL setup.

## Step 5. Set Up Kafka ACLs

TiDB Cloud needs Kafka ACLs to produce and consume messages on your cluster. ACLs must be created from inside the same VPC as your MSK cluster.

### 5.1 Prepare a Client EC2 Instance

Launch a Linux EC2 instance in the same VPC and one of the same subnets as your MSK cluster. You can use AWS Systems Manager Session Manager to access it without opening SSH to the public internet.

On the instance, download and extract the Kafka binaries and OpenJDK:

```bash
wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
tar -zxf kafka_2.13-3.7.1.tgz
wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
```

Set the environment:

```bash
export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
```

### 5.2 Create the SCRAM Client Properties File

On the EC2 instance, create a file named `scram-client.properties` with the following content:

```properties
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="<your-scram-username>" \
    password="<your-scram-password>";
```

### 5.3 Retrieve the Bootstrap Brokers

In the AWS MSK console, open your cluster's **Summary** section. Click **View client information** in the upper-right corner. In the popup, locate the **SASL/SCRAM Private endpoint** entry. This is your bootstrap server URI. Copy it for use in the ACL commands below.

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

If you encounter intermittent authentication failures, wait a few seconds and retry, as new SCRAM credentials can take a moment to propagate across all brokers.

## Step 6. Update the Cluster Configuration

Now that ACLs are in place, update the cluster configuration to the secure setting:

- `auto.create.topics.enable` stays `true`
- Change `allow.everyone.if.no.acl.found` to `false`

Apply the updated configuration in the AWS MSK console under **Cluster configuration**. Wait for the cluster to return to **Active** status.

## Step 7. Turn On Multi-VPC Connectivity

Multi-VPC connectivity is the AWS feature that enables PrivateLink access to your MSK cluster. It must be explicitly enabled.

In the AWS MSK console, go to your cluster's **Properties** tab. Under **Network settings** > **Multi-VPC connectivity**, turn it on. Configure the VPC connectivity client authentication to use **SASL/SCRAM** only (IAM and TLS are not needed for the TiDB Cloud connection).

This operation triggers a long-running cluster update. Expect it to take approximately 40 to 60 minutes. You can monitor progress in the MSK console under the **Cluster operations** tab. Wait for the cluster to return to **Active**.

When the update completes, confirm that:

- Multi-VPC connectivity is enabled
- `PublicAccess` is disabled
- VPC connectivity SASL/SCRAM authentication is enabled

## Step 8. Attach a Cluster Policy

Attach a resource-based cluster policy to your MSK cluster that grants your TiDB Cloud instance permission to connect. The **Principal** must be the AWS account ID of your TiDB Cloud Premium instance (obtained in the prerequisites).

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

> **Critical**: The `Principal` must be the AWS account ID provided by TiDB Cloud, not your own AWS account ID. Using the wrong principal will cause the connection to fail.

Attach this policy to your MSK cluster. In the AWS MSK console, navigate to your cluster and use the **Cluster policy** editor under the **Properties** tab to paste this JSON.

For more information, see [Attach a cluster policy to the MSK cluster](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-policy.html).

## Step 9. Create the PrivateLink Connection in TiDB Cloud

Create the private link connection in TiDB Cloud using the ARN of your MSK cluster.

For more information, see [Create an Amazon MSK Provisioned private link connection](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md#step-2-configure-the-private-endpoint-for-changefeeds).