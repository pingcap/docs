---
title: Connect to Amazon RDS via a Private Link Connection
summary: Learn how to connect to an Amazon RDS instance using an AWS Endpoint Service private link connection.
---

# Connect to Amazon RDS via a Private Link Connection

This document describes how to connect a {{{ .essential }}} cluster to an [Amazon RDS](https://aws.amazon.com/rds/) instance using an AWS Endpoint Service private link connection.

## Prerequisites

- You have an existing AWS RDS instance or the permissions required to create one.

- Your account has the following permissions to manage networking components:

    - Manage security groups
    - Manage load balancer
    - Manage endpoint services

- Your {{{ .essential }}} is hosted on AWS, and it is active. Retrieve and save the following details for later use:

    - AWS Account ID
    - Availability Zones (AZ)

To view the the AWS account ID and availability zones, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
2. In the **Private Link Connection For Dataflow** area, click **Create Private Link Connection**.
3. In the displayed dialog, you can find the AWS account ID and availability zones.

## Step 1. Set up the Amazon RDS instance

Identify an Amazon RDS instance to use, or [create a new one](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html).

The Amazon RDS instance must meet the following requirements:

- Region match: the instance must reside in the same AWS region as your {{{ .essential }}} cluster.
- The [subnet group](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.Subnets) of your Amazon RDS instance must have overlapping availability zones as your {{{ .essential }}} cluster.
- Set your Amazon RDS instance with a proper security group, and it is accessible within the VPC. For example, you can create a security group with the following rules:

    - An inbound rule that allows MySQL/Aurora: 
        - Type: `MySQL/Aurora`
        - Source: `Anywhere-IPv4`
    
    - An outbound rule that allows MySQL/Aurora: 
        - Type: `MySQL/Aurora`
        - Destination: `Anywhere-IPv4`

> **Note**
>
> To connect to a cross-region RDS instance, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Step 2. Expose the Amazon RDS instance as an endpoint service

You need to set up the load balancer and the AWS Endpoint Service in the AWS console.

### Step 2.1. Set up the load balancer

To set up the load balancer in the same region of your RDS, take the following steps:

1. Go to [Target groups](https://console.aws.amazon.com/ec2/home#CreateTargetGroup) to create a target group. Provide the following information:

    - **Target type**: select `IP addresses`
    - **Protocol and Port**: set protocol to TCP and port to your database port, for example `3306` for MySQL.
    - **IP address type**: select `IPv4`
    - **VPC**: the VPC where your RDS is located
    - **Register targets**: register the IP addresses of your Amazon RDS instance. You can ping the RDS endpoint to get the IP address.
 
    For more information, see [Create a target group for your Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-target-group.html).

2. Go to [Load balancers](https://console.aws.amazon.com/ec2/home#LoadBalancers) to create a network load balancer. Provide the following information:

    - **Schema**: select `Internal`
    - **Load balancer IP address type**: select `IPv4`
    - **VPC**: the VPC where your RDS is located
    - **Availability Zones**: it must overlap with your {{{ .essential }}} cluster
    - **Security groups**: create a new security group with the following rules:
        - An inbound rule that allows MySQL/Aurora: 
            - Type: `MySQL/Aurora`
            - Source: `Anywhere-IPv4`

        - An outbound rule that allows MySQL/Aurora:        
            - Type: `MySQL/Aurora`
            - Destination: `Anywhere-IPv4`

    - **Listeners and routing**:  
        - **Protocol and Port**: set the protocol to TCP and port to your database port, for example `3306` for MySQL
        - **Target group**: select the target group you that create in the previous step
  
   For more information, see [Create a Network Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html).

### Step 2.2. Set up the AWS Endpoint Service

To set up the endpoint service in the same region of your RDS, take the following steps:

1. Go to [Endpoint service](https://console.aws.amazon.com/vpcconsole/home#EndpointServices) to create an endpoint service. Provide the following information:

    - **Load balancer type**: select `Network`
    - **Load balancers**: enter the load balancer you create in the previous step
    - **Supported Regions**: leave it empty if you do not have cross-region requirements.
    - **Require acceptance for endpoint**: it is recommended to select `Acceptance required`
    - **Supported IP address types**: select `Ipv4`

2. Go to the details page of the endpoint service, and then copy the endpoint service name, in the format of `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`. You need to provide it to TiDB Cloud.

3. On the details page of the endpoint service, click the **Allowed principals** tab, and then add the TiDB Cloud account ID to the allowlist, for example, `arn:aws:iam::<account_id>:root`. 

    You can get the account ID in [Prerequisites](#prerequisites).

## Step 3. Create an AWS Endpoint Service private link connection in TiDB Cloud

You can create a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

For more information, see [Create an AWS Endpoint Service Private Link Connection](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection).
