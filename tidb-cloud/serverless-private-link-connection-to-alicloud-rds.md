---
title: Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection
summary: Learn how to connect to an Alibaba Cloud ApsaraDB RDS for MySQL instance using an Alibaba Cloud Endpoint Service private link connection.
---

# Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection 

This document describes how to connect a {{{ .essential }}} cluster to an [Alibaba Cloud ApsaraDB RDS for MySQL](https://www.alibabacloud.com/en/product/apsaradb-for-rds-mysql) instance using an Alibaba Cloud Endpoint Service private link connection.

## Prerequisites

- You have an existing ApsaraDB RDS for MySQL instance or the permissions required to create one.

- Verify that your account has the following permissions to manage networking components:

    - Manage load balancer
    - Manage endpoint services

- Your {{{ .essential }}} cluster is on Alibaba Cloud, and it is active. Retrieve and save the following details for later use:

    - Account ID
    - Availability Zones (AZ)

To view the the Alibaba Cloud account ID and availability zones, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
2. In the **Private Link Connection For Dataflow** area, click **Create Private Link Connection**.
3. In the displayed dialog, you can find the Alibaba Cloud account ID and availability zones.

## Step 1. Set up an ApsaraDB RDS for MySQL instance

Identify an Alibaba Cloud ApsaraDB RDS for MySQL that you want to use, or [set up a new RDS](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/step-1-create-an-apsaradb-rds-for-mysql-instance-and-configure-databases).

Your ApsaraDB RDS for MySQL instance must meet the following requirements:

- Region match: the instance must reside in the same Alibaba Cloud region as your {{{ .essential }}} cluster.
- AZ (Availability Zone) availability: the availability zones must overlap with those of your {{{ .essential }}} cluster.
- Network accessibility: the instance must be configured with proper IP whitelist and be accessible within the VPC.

> **Note**
>
> Cross-region connections for ApsaraDB RDS for MySQL are not supported.

## Step 2. Expose the ApsaraDB RDS for MySQL instance as an endpoint service

You need to set up the load balancer and the endpoint service in the Alibaba Cloud console.

### Step 2.1. Set up the load balancer

Set up the load balancer in the same region of your ApsaraDB RDS for MySQL as follows:

1. Go to [Server Groups](https://slb.console.alibabacloud.com/nlb/ap-southeast-1/server-groups) to create a server group.

    - **Server Group Type**: select `IP`
    - **VPC**: enter the VPC where your ApsaraDB RDS for MySQL is located
    - **Backend Server Protocol**: select `TCP`

    Click the created server group to add backend servers. Add the IP address of your ApsaraDB RDS for MySQL instance. You can ping the for MySQL RDS endpoint to get the IP address.
 
2. Go to [NLB](https://slb.console.alibabacloud.com/nlb) to create a network load balancer.

    - **Network Type**: select `Internal-facing`
    - **VPC**: select the VPC where your ApsaraDB RDS for MySQL is located
    - **Zone**: it must overlap with your {{{ .essential }}} cluster
    - **IP Version**: select `IPv4`

    Find the load balancer you created, and then click **Create Listener**:
    
    - **Listener Protocol**: select `TCP`
    - **Listener Port**: enter the database port, for example, `3306` for MySQL
    - **Server Group**: choose the server group you created in the previous step
  
### Step 2.2. Set up an endpoint service

Set up the endpoint service in the same region of your ApsaraDB RDS for MySQL:

1. Go to [Endpoint service](https://vpc.console.alibabacloud.com/endpointservice) to create an endpoint service. 

    - **Service Resource Type**: select `NLB`
    - **Select Service Resource**: select all zones that NLB is in, and choose the NLB that you created in the previous step
    - **Automatically Accept Endpoint Connections**: it is recommended to choose `No`

2. Go to the details page of the endpoint service, and copy the **Endpoint Service Name**, for example, `com.aliyuncs.privatelink.<region>.xxxxx`. You need to use it for TiDB Cloud later. 

3. On the detail page of the endpoint service, click the **Service Whitelist** tab, click **Add to Whitelist**, and then enter the TiDB Cloud account ID. 

    For more information about how to get the account ID, see [Prerequisites](#prerequisites).

## Step 3. Create a private link connection in TiDB Cloud

You can create a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

For more information, see [Create an Alibaba Cloud Endpoint Service private link connection](/tidb-cloud/serverless-private-link-connection.md#create-an-alibaba-cloud-endpoint-service-private-link-connection).
