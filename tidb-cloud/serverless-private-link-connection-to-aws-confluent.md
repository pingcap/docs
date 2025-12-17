# Set up a Private Link Connection to AWS Confleunt

> **Note**
>
> Only Confluent Dedicated clusters are supported.

This document describes how to connect to an AWS Confluent Dedicated Cluster using an AWS Endpoint Service private link connection.

## Prerequisites
   
1. You have a Confluent Cloud account.

2. Get the {{.essential}} account ID and available zones, save the information for later use.

    1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the TiDB cluster, and then click **Settings** > **Networking** in the left navigation pane.
    2. On the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.
    3. You can find the AWS account ID and available zones information.

## Step 1. Set up a Confluent Cloud network

Identify a Confluent Cloud network you want to use, or [set up a new Confluent Cloud network](https://docs.confluent.io/cloud/current/networking/ccloud-network/aws.html#create-ccloud-network-aws).

The Confluent Cloud network must meet the following requirements:

- The network must be in the same AWS region as your {{.essential}}.
- The network must have overlapping availability zones as your {{.essential}}, recommended to have same availability zones.

On the `Network overview` page, obtain the `DNS subdomain` of the Confluent Cloud network. You need to extract the unique name from it.
For example, if the `DNS subdomain` is `use1-az1.domnprzqrog.us-east-1.aws.confluent.cloud`, then the unique name is `domnprzqrog.us-east-1`.
Please save the unique name for later use.

> **Note**
>
> The Confluent Cloud Dedicated cluster you want TiDB Cloud to connect to must be under this network.

## Step 2. Add a PrivateLink Access to the network

Please add a PrivateLink Access to the network you identified or set up in Step 1. Refer to [Add a PrivateLink Access in Confluent Cloud](https://docs.confluent.io/cloud/current/networking/private-links/aws-privatelink.html#add-a-privatelink-access-in-ccloud).

During the process, you need to:

- Provide the TiDB Cloud AWS account ID you obtained in the Prerequisites section.
- Save the `VPC Service Endpoint` provided by Confluent Cloud for later use, usually in the format of `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`.

## Step 3. Create a Private Link Connection in TiDB Cloud

### 1. Create the AWS Endpoint Service Private Link connection

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

### Attach domains to the private link connection

You will need the unique name you obtained in Step 1.

You can also refer to [Attach Domains to a Private Link Connection](/tidbcloud/serverless-private-link-connection#attach-domains-to-a-private-link-connection) for more details.

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, choose the target Private Link Connection and click **...**.

4. Click **Attach Domains**.

5. In the **Attach Domains** dialog choose the **Confluent Cloud** domain type: Enter the Confluent Unique Name to generate the domains, and then click **Attach Domains** to confirm.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type CONFLUENT --unique-name <unique-name>
```

</div>
</SimpleTab>