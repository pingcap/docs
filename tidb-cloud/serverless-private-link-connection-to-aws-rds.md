# Set up a Private Link Connection to AWS RDS

This document describes how to connect to an AWS RDS instance using an AWS Endpoint Service private link connection.

## Prerequisites

1. Ensure that you have an RDS instance or have the permissions to create one.

2. Ensure that you have the following authorization to set up a load balancer and endpoint service in your own AWS account.

    - Manage security groups
    - Manage load balancer
    - Manage endpoint services

3. Get the {{.essential}} account ID and available zones, save the information for later use.

    1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
    2. On the **Private Link Connection For Dataflow**, Click **Create Private Link Connection**.
    3. You can find the AWS account ID and available zones information.

## Step 1. Set up RDS instance

Identify an AWS RDS instance to use, or [set up a new one](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html).

The RDS must meet the following requirements:

- The RDS must be in the same AWS region as your {{.essential}}.
- The subnet group of your RDS must have overlapping availability zones as your {{.essential}}.
- Make sure your RDS instance set proper security group and is accessible within the VPC.

> **Note**
>
> To connect to a cross-region RDS instance, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Step 2. Expose the RDS instance as an endpoint service

### 1. Set up the load balancer

Set up the load balancer in the same region of your RDS:

1. Go to [Target groups](https://console.aws.amazon.com/ec2/home#CreateTargetGroup) to create a target group.

     - **Target type**: `IP addresses`
     - **Protocol and Port**: Set protocol to TCP and port to your database port (for example 3306 for MySQL).
     - **IP address type**: `IPv4`
     - **VPC**: The VPC where your RDS is located
     - **Register targets**: Register the IP addresses of your RDS instance. You can ping the RDS endpoint to get the IP address.
 
   For detailed instructions, refer to [this guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-target-group.html).

2. Go to [Load balancers](https://console.aws.amazon.com/ec2/home#LoadBalancers) to create a network load balancer.

    - **Schema**: `Internal`
    - **Load balancer IP address type**: `IPv4`
    - **VPC**: The VPC where your RDS is located
    - **Availability Zones**: Must have overlapping availability zones with your {{.essential}}
    - **Security groups**: Create a new security group with the following rules.
        - Inbound rule allows MySQL/Aurora: Type - `MySQL/Aurora`; Source - `Anywhere-IPv4`.
        - Outbound rule allows all TCP: Type - `All TCP`; Destination - `Anywhere-IPv4`
    - **Listeners and routing**:
        - Protocol and Port: Set protocol to TCP and port to your database port (for example 3306 for MySQL).
        - Target group: Select the target group you created in the previous step.
  
   For detailed instructions, refer to [this guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html).

### 2. Set up AWS Endpoint Service

Set up the endpoint service in the same region of your RDS:

1. Go to [Endpoint service](https://console.aws.amazon.com/vpcconsole/home#EndpointServices) to create an endpoint service. 

    - **Load balancer type**: `Network`
    - **Load balancers**: The load balancer you created in the previous step.
    - **Supported Regions**: Leave it empty if you don't have cross-region requirements.
    - **Require acceptance for endpoint**: Recommended to check `Acceptance required`
    - **Supported IP address types**: `Ipv4`

2. Go to the details page of the endpoint service and copy the **Service name**. You need to provide it to TiDB Cloud, for example `com.amazonaws.vpce.<region>.vpce-svc-xxx`.

3. On the details page of the endpoint service, click the **Allow principals** tab, and add the TiDB Cloud account ID to the allowlist. You can get the account ID in [Prerequisites](#prerequisites), for example, `arn:aws:iam::<account_id>:root`.

## Step 3. Create a Private Link Connection in TiDB Cloud

You can also refer to [Create an AWS Endpoint Service Private Link Connection](/tidbcloud/serverless-private-link-connection#create-an-aws-endpoint-service-private-link-connection) for more details.

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
    - **Connection Type**: Choose **AWS Endpoint Service**. If you cannot find this option, please ensure that your cluster is created on AWS.
    - **Endpoint Service Name**: Enter the endpoint service name you obtained in Step 2.

5. Click the **Create Connection** button.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
```

</div>
</SimpleTab>