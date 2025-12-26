---
title: Connect to AWS Confluent via a Private Link Connection
summary: Learn how to connect to an AWS Confluent instance using an AWS Confluent Endpoint Service private link connection.
---

# Connect to Confluent Cloud via a Private Link Connection

This document describes how to connect to a Confluent Cloud Dedicated cluster on AWS using an AWS Endpoint Service private link connection.

> **Note**
>
> - Only Confluent Cloud Dedicated clusters on AWS are supported.
> - The Private Link Connections for Dataflow feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Prerequisites
   
- You have a Confluent Cloud account.

- Confirm that your {{{ .essential }}} is active in AWS. Retrieve and save the following details for later use:

    - Account ID
    - Availability Zones (AZ)

To view the the AWS account ID and available zones, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
2. On the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.
3. You can find the AWS account ID and available zones.

## Step 1. Set up a Confluent Cloud network

Identify a Confluent Cloud network you want to use, or [create a new Confluent Cloud network on AWS](https://docs.confluent.io/cloud/current/networking/ccloud-network/aws.html#create-ccloud-network-aws).

The Confluent Cloud network must meet the following requirements:

- Type: the network must be a privatelink network.
- Region match: the instance must reside in the same AWS region as your {{{ .essential }}} cluster.
- AZ (Availability Zone) availability: the availability zones must overlap with those of your {{{ .essential }}} cluster.

To get the unique name of the Confluent Cloud network:

1. On the `Network overview` page, obtain the `DNS subdomain` of the Confluent Cloud network. 
2. Extract the unique name from it. For example, if the `DNS subdomain` is `use1-az1.domnprzqrog.us-east-1.aws.confluent.cloud`, then the unique name is `domnprzqrog.us-east-1`.
3. Save the unique name for later use.

> **Note**
>
> The Confluent Cloud Dedicated cluster must be deployed in this network.

## Step 2. Add a PrivateLink Access to the network

Add a PrivateLink Access to the network you identified or set up in Step 1. For more information, see [Add a PrivateLink Access in Confluent Cloud](https://docs.confluent.io/cloud/current/networking/private-links/aws-privatelink.html#add-a-privatelink-access-in-ccloud).

During the process, you need to:

- Provide the TiDB Cloud AWS account ID that you obtain in [Prerequisites](#prerequisites).
- Save the `VPC Service Endpoint` provided by Confluent Cloud for later use, usually in the format of `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`.

## Step 3. Create a private link connection in TiDB Cloud

To create a private link connection in TiDB Cloud, do the following:

### 1. Create the AWS Endpoint Service private link connection

You can create a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow** area, click **Create Private Link Connection**.

4. Enter the required information in the **Create Private Link Connection** dialog:

    - **Private Link Connection Name**: enter a name for the private link connection.
    - **Connection Type**: select **AWS Endpoint Service**. If you cannot find this option, ensure that your cluster is created on AWS.
    - **Endpoint Service Name**: enter the `VPC Service Endpoint` you obtained in [Step 2](#step-2-add-a-privatelink-access-to-the-network).

5. Click **Create**.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
```

</div>
</SimpleTab>

You can also refer to [Create an AWS Endpoint Service Private Link Connection](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection) for more details.

### 2. Attach domains to the private link connection

You can create a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow** area, choose the target private link connection and then click **...**.

4. Click **Attach Domains**.

5. In the **Attach Domains** dialog, choose the **Confluent Cloud** domain type, enter the Confluent unique name to generate the domains, and then click **Attach Domains** to confirm.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type CONFLUENT --unique-name <unique-name>
```

</div>
</SimpleTab>

For more information, see [Attach Domains to a Private Link Connection](/tidb-cloud/serverless-private-link-connection.md#attach-domains-to-a-private-link-connection).
