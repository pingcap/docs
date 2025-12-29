---
title: Connect to Amazon RDS via a Private Link Connection
summary: Learn how to connect to an Amazon RDS instance using an AWS Endpoint Service private link connection.
---

# Connect to Amazon RDS via a Private Link Connection

This document describes how to connect to an Amazon RDS instance using an AWS Endpoint Service private link connection.

> **Note:**
>
> The Private Link Connections for Dataflow feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Prerequisites

- AWS RDS: ensure you have an existing AWS RDS instance or the permissions required to create one.

- AWS permissions: verify that your account has the following authorizations to manage networking components:

    - Manage security groups
    - Manage load balancer
    - Manage endpoint services

- {{{ .essential }}} information: confirm that your {{{ .essential }}} is active in AWS. Retrieve and save the following details for later use:

    - Account ID
    - Availability Zones (AZ)

To view the the AWS account ID and available zones, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
2. On the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.
3. You can find the AWS account ID and available zones.

## Step 1. Set up the Amazon RDS instance

Identify an Amazon RDS instance to use, or [create a new one](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html).

The Amazon RDS instance must meet the following requirements:

- Region match: the instance must reside in the same AWS region as your {{{ .essential }}} cluster.
- The [subnet group](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.Subnets) of your Amazon RDS instance must have overlapping availability zones as your {{{ .essential }}} cluster.
- Set your Amazon RDS instance with a proper security group, and it is accessible within the VPC. For example, you can create a security group with the following rules:
    - An inbound rule that allows MySQL/Aurora: 
        Type: `MySQL/Aurora`
        Source: `Anywhere-IPv4`
    - An outbound rule that allows MySQL/Aurora:
        Type: `MySQL/Aurora`
        Destination: `Anywhere-IPv4`

> **Note**
>
> To connect to a cross-region RDS instance, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Step 2. Expose the Amazon RDS instance as an endpoint service

### 1. Set up the load balancer

Set up the load balancer in the same region of your RDS:

1. Go to [Target groups](https://console.aws.amazon.com/ec2/home#CreateTargetGroup) to create a target group.

    - **Target type**: `IP addresses`
    - **Protocol and Port**: Set protocol to TCP and port to your database port (for example 3306 for MySQL).
    - **IP address type**: `IPv4`
    - **VPC**: The VPC where your RDS is located
    - **Register targets**: Register the IP addresses of your RDS instance. You can ping the RDS endpoint to get the IP address.
 
    For detailed instructions, see [Create a target group for your Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-target-group.html).

2. Go to [Load balancers](https://console.aws.amazon.com/ec2/home#LoadBalancers) to create a network load balancer.

    - **Schema**: `Internal`
    - **Load balancer IP address type**: `IPv4`
    - **VPC**: the VPC where your RDS is located
    - **Availability Zones**: it must overlap with your {{{ .essential }}} cluster
    - **Security groups**: create a new security group with the following rules:
        - An inbound rule that allows MySQL/Aurora: 
            Type: `MySQL/Aurora`
            Source: `Anywhere-IPv4`
        - An outbound rule that allows MySQL/Aurora:
            Type: `MySQL/Aurora`
            Destination: `Anywhere-IPv4`
    - **Listeners and routing**:
        - Protocol and Port: set the protocol to TCP and port to your database port, for example `3306` for MySQL
        - Target group: select the target group you that create in the previous step
  
   For detailed instructions, see [Create a Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html).

### 2. Set up the AWS Endpoint Service

Set up the endpoint service in the same region of your RDS:

1. Go to [Endpoint service](https://console.aws.amazon.com/vpcconsole/home#EndpointServices) to create an endpoint service. 

    - **Load balancer type**: `Network`
    - **Load balancers**: the load balancer you created in the previous step.
    - **Supported Regions**: leave it empty if you don't have cross-region requirements.
    - **Require acceptance for endpoint**: it is recommended to select `Acceptance required`
    - **Supported IP address types**: `Ipv4`

2. Go to the details page of the endpoint service, and then copy the endpoint service name, in the format of `com.amazonaws.vpce.<region>.vpce-svc-xxx`. You need to provide it to TiDB Cloud.

3. On the details page of the endpoint service, click the **Allow principals** tab, and then add the TiDB Cloud account ID to the allowlist, for example, `arn:aws:iam::<account_id>:root`. You can get the account ID in [Prerequisites](#prerequisites).

## Step 3. Create a private link connection in TiDB Cloud

You can create a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.

4. Enter the required information in the **Create Private Link Connection** dialog:

    - **Private Link Connection Name**: enter a name for the private link connection.
    - **Connection Type**: select **AWS Endpoint Service**. If you cannot find this option, ensure that your cluster is created on AWS.
    - **Endpoint Service Name**: enter the endpoint service name you obtained in [Step 2](#2-set-up-the-aws-endpoint-service).

5. Click **Create**.

6. Go to the detail page of your endpoint service on the [AWS console](https://console.aws.amazon.com). In the **Endpoint Connections** tab, accept the endpoint connection request from TiDB Cloud.

</div>

<div label="CLI">

To create a private link connection using the TiDB Cloud CLI:

1. Run the following command:

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
    ```

2. Go to the detail page of your endpoint service on the [AWS console](https://console.aws.amazon.com). In the **Endpoint Connections** tab, accept the endpoint connection request from TiDB Cloud.

</div>
</SimpleTab>

You can also refer to [Create an AWS Endpoint Service Private Link Connection](/tidbcloud/serverless-private-link-connection#create-an-aws-endpoint-service-private-link-connection) for more details.
