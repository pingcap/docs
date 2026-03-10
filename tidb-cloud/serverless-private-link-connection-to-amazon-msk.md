---
title: Connect to Amazon MSK Provisioned via a Private Link Connection
summary: Learn how to connect to an Amazon MSK Provisioned cluster using an Amazon MSK Provisioned private link connection.
---

# Connect to Amazon MSK Provisioned via a Private Link Connection

This document describes how to connect a {{{ .essential }}} cluster to an [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) cluster using an [Amazon MSK Provisioned private link connection](/tidb-cloud/serverless-private-link-connection.md#create-an-amazon-msk-provisioned-private-link-connection).

## Prerequisites for {{{ .essential }}} {#prerequisites-for-essential}

- Your {{{ .essential }}} cluster is hosted on AWS and is active. Retrieve and save the following for later use:

    - AWS Account ID
    - Availability zones (AZ)

To view the AWS account ID and availability zones:

1. In the [TiDB Cloud console](https://tidbcloud.com), go to the cluster overview page of your TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
2. In the **Private Link Connection For Dataflow** area, click **Create Private Link Connection**.
3. In the dialog, note the AWS account ID and availability zones.

## Prerequisites for the Amazon MSK Provisioned cluster

Before you begin, ensure the following for your Amazon MSK Provisioned cluster:
 
- **Region and AZ**: Your Amazon MSK Provisioned cluster is in the same AWS region as your {{{ .essential }}} cluster, and the availability zones of the MSK cluster are the same as your TiDB Cloud cluster.
- **Authentication**: [SASL/SCRAM authentication](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html) is required for the MSK cluster.
- **Broker type**: Do not use the `t4.small` broker type. It does not support private link.
    
For more requirements, see [Amazon MSK multi-VPC private connectivity in a single Region](https://docs.aws.amazon.com/msk/latest/developerguide/aws-access-mult-vpc.html#mvpc-requirements).
    
 If you do not have an Amazon MSK Provisioned cluster, [create one](https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html) in the same region and the same availability zone as your {{{ .essential }}} cluster, and then [set up SASL/SCRAM authentication](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password-tutorial.html) for the created cluster.

- **Secret name**: the secret name must start with `AmazonMSK_`.
- **Encryption**: do not use the default encryption key. Create a new custom AWS KMS key for your secret.

## Step 1. Set up Kafka ACLs for TiDB Cloud access

You must set up Kafka ACLs so that TiDB Cloud can access your Amazon MSK Provisioned cluster. You can use SASL/SCRAM authentication (recommended) or IAM authentication to set up ACLs.

<SimpleTab>
<div label="SASL/SCRAM">

Use this method to create ACLs in the same VPC as your MSK cluster using SASL/SCRAM authentication.

1. Create an EC2 instance (Linux) in the VPC where your MSK cluster is located and SSH to it.

2. Download Kafka and OpenJDK:

    ```shell
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    ```

3. Set the environment. Replace the path with your actual path.

    ```shell
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    ```

4. Create a file named `scram-client.properties` with the following content. Replace `username` and `pswd` with your SASL/SCRAM credentials:

    ```properties
    security.protocol=SASL_SSL
    sasl.mechanism=SCRAM-SHA-512
    sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
        username="username" \
        password="pswd";
    ```

5. Create the ACLs. Replace `bootstrap-server` with your MSK bootstrap server address and port (for example, `b-2.xxxxx.c18.kafka.us-east-1.amazonaws.com:9096`), and replace the path to Kafka if needed:

    ```shell
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --topic '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --group '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config scram-client.properties --add --allow-principal User:<username> --operation All --cluster '*'
    ```

    The principal `User:<username>` is the SASL/SCRAM user that TiDB Cloud uses to access your MSK cluster. Use the username you configured for TiDB Cloud in your MSK ACLs.

</div>

<div label="IAM">

As an alternative to SASL/SCRAM, you can create ACLs in the same VPC as your MSK cluster using IAM authentication. The IAM user or role must have **Amazon MSK** and **Apache Kafka APIs for MSK** permissions.

1. Create an EC2 instance (Linux) in the VPC where your MSK cluster is located and SSH to it.

2. Download Kafka, OpenJDK, and the AWS MSK IAM auth JAR:

    ```shell
    wget https://archive.apache.org/dist/kafka/3.7.1/kafka_2.13-3.7.1.tgz
    tar -zxf kafka_2.13-3.7.1.tgz
    wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz
    tar -zxf openjdk-22.0.2_linux-x64_bin.tar.gz
    wget https://github.com/aws/aws-msk-iam-auth/releases/download/v2.3.5/aws-msk-iam-auth-2.3.5-all.jar
    ```

3. Configure the environment. Replace paths and credentials with your own values.

    ```shell
    export PATH=$PATH:/home/ec2-user/jdk-22.0.2/bin
    export CLASSPATH=/home/ec2-user/aws-msk-iam-auth-2.3.5-all.jar
    export AWS_ACCESS_KEY_ID=<your-access-key-id>
    export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
    ```

4. Create a file named `iam-client.properties` with the following content:

    ```properties
    security.protocol=SASL_SSL
    sasl.mechanism=AWS_MSK_IAM
    sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;
    sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler
    ```

5. Create the ACLs. Replace `bootstrap-server` with your MSK bootstrap server address and port (for example, `b-1.xxxxx.c18.kafka.us-east-1.amazonaws.com:9098`), and replace the path to Kafka if needed:

    ```shell
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --topic '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --group '*'
    /home/ec2-user/kafka_2.13-3.7.1/bin/kafka-acls.sh --bootstrap-server <bootstrap-server> --command-config iam-client.properties --add --allow-principal User:<username> --operation All --cluster '*'
    ```

    The principal `User:<username>` is the SASL/SCRAM user that TiDB Cloud uses to access your MSK cluster. Use the username you configured for TiDB Cloud in your MSK ACLs.

</div>
</SimpleTab>

## Step 2. Configure the MSK cluster

Update the following cluster configuration properties:

- Set `auto.create.topics.enable=true`.
- Add `allow.everyone.if.no.acl.found=false` (required for SASL/SCRAM).
- Keep other properties unchanged or adjust them as needed.

Apply the changes and wait for the cluster status to change from **Updating** to **Active**.

## Step 3. Attach the cluster policy

[Attach the cluster policy](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-policy.html) to allow TiDB Cloud to connect to your MSK cluster. Use the TiDB Cloud AWS account ID you obtained in [Prerequisites](#prerequisites-for-essential).

## Step 4. Turn on multi-VPC connectivity

After the cluster is active, [turn on multi-VPC connectivity](https://docs.aws.amazon.com/msk/latest/developerguide/mvpc-cluster-owner-action-turn-on.html) for the MSK cluster. Multi-VPC connectivity is required for AWS PrivateLink. To connect from TiDB Cloud, you must enable SASL/SCRAM authentication.

Wait for the cluster status to change from **Updating** to **Active** again.

## Step 5. Create an Amazon MSK Provisioned private link connection in TiDB Cloud

Create the private link connection in TiDB Cloud using the `ARN` of your MSK cluster.

For more information, see [Create an Amazon MSK Provisioned private link connection](/tidb-cloud/serverless-private-link-connection.md#create-an-amazon-msk-provisioned-private-link-connection).