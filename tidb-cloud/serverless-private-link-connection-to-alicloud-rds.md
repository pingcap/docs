# Set up a Private Link Connection to Alibaba Cloud RDS

This document describes how to connect to an Alibaba Cloud RDS instance using an Alibaba Cloud Endpoint Service private link connection.

## Prerequisites

1. Ensure that you have an RDS instance or have the permissions to create one.

2. Ensure that you have the following authorization to set up a load balancer and endpoint service in your own Alibaba Cloud account.

    - Manage load balancer
    - Manage endpoint services

3. Ensure your {{.essential}} in alibaba cloud provider and get its account ID and available zones, save the information for later use.

    1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
    2. On the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.
    3. You can find the AWS account ID and available zones information.

## Step 1. Set up an RDS instance

Identify an Alibaba Cloud ApsaraDB RDS you want to use, or [set up a new RDS](https://www.alibabacloud.com/help/en/rds/apsaradb-rds-for-mysql/step-1-create-an-apsaradb-rds-for-mysql-instance-and-configure-databases).

The RDS must meet the following requirements:

- The Alibaba Cloud region for your RDS instance must be the same as the region for your {{.essential}}.
- The subnet group of your RDS must have overlapping availability zones as your {{.essential}}.
- Make sure your RDS instance set proper IP whitelist and is accessible within the VPC.

> **Note**
>
> Cross-region RDS instance connection is not supported.

## Step 2. Expose the RDS instance as an endpoint service

### 1. Set up the load balancer

Set up the load balancer in the same region of your RDS:

1. Go to [Server Groups](https://slb.console.alibabacloud.com/nlb/ap-southeast-1/server-groups) to create a server group.

    - **Server Group Type**: `IP`
    - **VPC**: The VPC where your RDS is located
    - **Backend Server Protocol** `TCP`

   Click the created server group to add backend servers: Add the IP address of your RDS instance, you can ping the RDS endpoint to get the IP address.
 
2. Go to [NLB](https://slb.console.alibabacloud.com/nlb) to create a network load balancer.

    - **Network Type**: `Internal-facing`
    - **VPC**: The VPC where your RDS is located
    - **Zone**: Must have overlapping availability zones with your {{.essential}}
    - **IP Version**: `IPv4`

    Find the load balancer you created, and then click **Create Listerner**:
    
    - **Listener Protocol**: TCP
    - **Listener Port**: Database port (for example 3306 for MySQL).
    - **Server Group**: Choose the server group you created in the previous step.
  
### 2. Set up an endpoint service

Set up the endpoint service in the same region of your RDS:

1. Go to [Endpoint service](https://vpc.console.alibabacloud.com/endpointservice) to create an endpoint service. 

    - **Service Resource Type**: `NLB`
    - **Select Service Resource**: Select all zones that NLB is in and choose the NLB you created in the previous step.
    - **Automatically Accept Endpoint Connections**: Recommended to choose `No`

2. Go to the details page of the endpoint service and copy the **Endpoint Service Name**. You will need to provide it to TiDB Cloud. For example, `com.aliyuncs.privatelink.<region>.xxxxx`.

3. On the detail page of the endpoint service, click the **Service Whitelist** tab, click **Add to Whitelist** and input the TiDB Cloud account ID. You can get the account ID in [Prerequisites](#prerequisites).

## Step 3. Create a private link connection in TiDB Cloud

You can also refer to [Create an AliCloud Endpoint Service Private Link Connection](/tidbcloud/serverless-private-link-connection#create-an-alicloud-endpoint-service-private-link-connection) for more details.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.

4. Enter the required information in the **Create Private Link Connection** dialog:

    - **Private Link Connection Name**: Enter a name for the Private Link Connection.
    - **Connection Type**: Choose **AliCloud Endpoint Service**. If you cannot find this option, please ensure that your cluster is created on AWS.
    - **Endpoint Service Name**: Enter the endpoint service name you obtained in Step 2.

5. Click the **Create Connection** button.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type ALICLOUD_ENDPOINT_SERVICE --alicloud.endpoint-service-name <endpoint-service-name>
```

</div>
</SimpleTab>