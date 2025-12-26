---
title: Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection
summary: Learn how to connect to an Alibaba Cloud ApsaraDB RDS for MySQL instance using an Alibaba Cloud Endpoint Service private link connection.
---

# Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection 

This document describes how to connect to an Alibaba Cloud ApsaraDB RDS for MySQL instance using an Alibaba Cloud Endpoint Service private link connection.

> **Note:**
>
> The Private Link Connections for Dataflow feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Prerequisites

- ApsaraDB RDS for MySQL: ensure you have an existing ApsaraDB RDS for MySQL instance or the permissions required to create one.

- Alibaba Cloud permissions: verify that your account has the following authorizations to manage networking components:

    - Manage load balancer
    - Manage endpoint services

- {{{ .essential }}} information: confirm that your {{{ .essential }}} is active in Alibaba Cloud. Retrieve and save the following details for later use:

    - Account ID
    - Availability Zones (AZ)

To view the the Alibaba Cloud account ID and available zones, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
2. On the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.
3. You can find the Alibaba Cloud account ID and available zones.

## Step 1. Set up an ApsaraDB RDS for MySQL instance

Identify an Alibaba Cloud ApsaraDB RDS for MySQL you want to use, or [set up a new RDS](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/step-1-create-an-apsaradb-rds-for-mysql-instance-and-configure-databases).

To ensure successful connectivity, your ApsaraDB RDS for MySQL instance must meet the following requirements:

- Region match: the instance must reside in the same Alibaba Cloud region as your {{{ .essential }}} cluster.
- AZ (Availability Zone) availability: the availability zones must overlap with those of your {{{ .essential }}} cluster.
- Network accessibility: the instance must be accessible within the VPC, with an appropriately configured IP allowlist.

> **Note**
>
> Cross-region connections for ApsaraDB RDS for MySQL are not supported.

## Step 2. Expose the ApsaraDB RDS for MySQL instance as an endpoint service

### 1. Set up the load balancer

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
  
### 2. Set up an endpoint service

Set up the endpoint service in the same region of your ApsaraDB RDS for MySQL:

1. Go to [Endpoint service](https://vpc.console.alibabacloud.com/endpointservice) to create an endpoint service. 

    - **Service Resource Type**: select `NLB`
    - **Select Service Resource**: select all zones that NLB is in, and choose the NLB that you created in the previous step
    - **Automatically Accept Endpoint Connections**: it is recommended to choose `No`

2. Go to the details page of the endpoint service, and copy the **Endpoint Service Name**, for example, `com.aliyuncs.privatelink.<region>.xxxxx`. You need to use it for TiDB Cloud later. 

3. On the detail page of the endpoint service, click the **Service Whitelist** tab, click **Add to Whitelist**, and then enter the TiDB Cloud account ID. For more information about how to get the account ID, see [Prerequisites](#prerequisites).

## Step 3. Create a private link connection in TiDB Cloud

You can create a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow** area, click **Create Private Link Connection**.

4. In the **Create Private Link Connection** dialog, enter the required information:

    - **Private Link Connection Name**: enter a name for the private link connection.
    - **Connection Type**: select **Alibaba Cloud Endpoint Service**. If you cannot find this option, ensure that your cluster is created on Alibaba Cloud.
    - **Endpoint Service Name**: enter the endpoint service name you obtained in [Set up an endpoint service](#2-set-up-an-endpoint-service).

5. Click **Create**.

6. Go back to the detail page of the endpoint service on [Alibaba Cloud console](https://account.alibabacloud.com). In the **Endpoint Connections** tab, allow the endpoint connection request from TiDB Cloud.

</div>

<div label="CLI">

To create a private link connection using the TiDB Cloud CLI:

1. Run the following command:

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type ALICLOUD_ENDPOINT_SERVICE --alicloud.endpoint-service-name <endpoint-service-name>
    ```

2. Go back to the detail page of the endpoint service on [Alibaba Cloud console](https://account.alibabacloud.com). In the **Endpoint Connections** tab, allow the endpoint connection request from TiDB Cloud.

</div>
</SimpleTab>

For more information, see [Create an AliCloud Endpoint Service Private Link Connection](/tidb-cloud/serverless-private-link-connection.md#create-an-alicloud-endpoint-service-private-link-connection).
