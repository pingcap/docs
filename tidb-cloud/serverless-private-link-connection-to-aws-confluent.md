---
title: Connect to AWS Confluent via a Private Link Connection
summary: Learn how to connect to an AWS Confluent instance using an AWS Endpoint Service private link connection.
---

# Connect to Confluent Cloud via a Private Link Connection

This document describes how to connect a {{{ .essential }}} cluster to a [Confluent Cloud Dedicated cluster](https://docs.confluent.io/cloud/current/clusters/cluster-types.html) on AWS using an [AWS Endpoint Service private link connection](/tidb-cloud/serverless-private-link-connection.md).

> **Note**
>
> Among all Confluent Cloud cluster types on AWS, only Confluent Cloud Dedicated clusters support private link connections.

## Prerequisites
   
- You have a [Confluent Cloud](https://confluent.cloud/) account.

- Your {{{ .essential }}} is hosted on AWS, and it is active. Retrieve and save the following details for later use:

    - AWS Account ID
    - Availability Zones (AZ)

To view the AWS account ID and available zones, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
2. In the **Private Link Connection For Dataflow** area, click **Create Private Link Connection**.
3. In the displayed dialog, you can find the AWS account ID and available zones.

## Step 1. Set up a Confluent Cloud network

Identify a Confluent Cloud network that you want to use, or [create a new Confluent Cloud network on AWS](https://docs.confluent.io/cloud/current/networking/ccloud-network/aws.html#create-ccloud-network-aws).

The Confluent Cloud network must meet the following requirements:

- Type: the network must be a **PrivateLink** network.
- Region match: the network must reside in the same AWS region as your {{{ .essential }}} cluster.
- AZ (Availability Zone) availability: the availability zones of the network must overlap with those of your {{{ .essential }}} cluster.

To get the unique name of the Confluent Cloud network, take the following steps:

1. In the [Confluent Cloud Console](https://confluent.cloud/), navigate to the [**Environments**](https://confluent.cloud/environments) page, and then click the environment where your Confluent Cloud network is located.
2. Click **Network management** and choose **For dedicated clusters** to find the network you created.
3. Go to the **Network overview** page to obtain the DNS subdomain of the Confluent Cloud network. 
4. Extract the unique name of your Confluent Cloud network from the DNS subdomain. For example, if the DNS subdomain is `use1-az1.domnprzqrog.us-east-1.aws.confluent.cloud`, then the unique name is `domnprzqrog.us-east-1`.
5. Save the unique name for later use.


## Step 2. Add a PrivateLink Access to the network

Add a PrivateLink Access to the network you identified or set up in [Step 1](#step-1-set-up-a-confluent-cloud-network). For more information, see [Add a PrivateLink Access in Confluent Cloud](https://docs.confluent.io/cloud/current/networking/private-links/aws-privatelink.html#add-a-privatelink-access-in-ccloud).

During the process, you need to:

- Provide the TiDB Cloud AWS account ID that you obtain in [Prerequisites](#prerequisites).
- Save the `VPC Service Endpoint` provided by Confluent Cloud for later use, usually in the `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx` format.

## Step 3. Create a Confluent Cloud dedicated cluster under the network

Create a Confluent Cloud Dedicated cluster under the network you set up in [Step 1](#step-1-set-up-a-confluent-cloud-network). For more information, see [Create a dedicated cluster in Confluent Cloud](https://docs.confluent.io/cloud/current/clusters/create-cluster.html#create-ak-clusters).

When creating the cluster, use the existing Confluent Cloud network you set up in [Step 1](#step-1-set-up-a-confluent-cloud-network).

## Step 4. Create a private link connection in TiDB Cloud

To create a private link connection in TiDB Cloud, do the following:

1. Create a private link connection in TiDB Cloud using the `VPC Service Endpoint` from Confluent Cloud.

    For more information, see [Create an AWS Endpoint Service private link connection](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection).

    > **Note:**
    >
    > For Confluent Cloud Dedicated clusters on AWS, you do not need to go to the detail page of your endpoint service on the AWS console to manually accept the endpoint connection request from TiDB Cloud. Confluent Cloud processes it automatically.

2. Attach the Confluent Cloud service domains to the private link connection so that dataflow services in TiDB Cloud can access the Confluent cluster.

    For more information, see [Attach domains to a private link connection](/tidb-cloud/serverless-private-link-connection.md#attach-domains-to-a-private-link-connection).
