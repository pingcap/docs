# Private Link Connection for Dataflow(Beta)

## Overview

Dataflow services such as Changefeed and Data Migration (DM) in TiDB Cloud require connections to customers' RDS instances or Kafka clusters. While public network connections are technically feasible, Private Link provides a far more efficient and secure networking alternative.

The Private Link Connection enables private, direct connectivity between {{{ .essential }}} and customers' target resources (for example RDS, Kafka) via Private Link. This feature is specifically designed for integration with TiDB Cloud's changefeed, DM and other services that connect from TiDB Cloud to customers' resources, ensuring data transmission remains within private networks.

## Private Link Connection Types

### AWS Endpoint Service

This type of private link connection enables TiDB Cloud clusters on **AWS** to connect to your [AWS endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html) powered by AWS PrivateLink.

The Private Link Connection can access various AWS services by attach them to the endpoint service, including RDS instances and Kafka services, over a private network.

### AliCloud Endpoint Service

This type of private link connection enables TiDB Cloud clusters on **Alibaba Cloud** to connect to your [Alibaba Cloud endpoint service](https://www.alibabacloud.com/help/en/privatelink/share-your-service/) powered by Alibaba Cloud PrivateLink.

The Private Link Connection can access various Alibaba Cloud services by attaching them to the endpoint service, including RDS instances and Kafka services, over a private network.

## Attach Domains

You can attach domains to a private link connection. 

When a domain is attached to the Private Link Connection, all traffic to this domain will be routed to this private link connection. It is useful when your service provides custom domains to clients at runtime, such as Kafka advertised listeners.

Different Private Link Connection types support attaching different domains:

| Private Link Connection Type | Supported Domain Type              |
|-----------------------------|-------------------------------------------|
| AWS Endpoint Service        | TiDB Cloud managed (`aws.tidbcloud.com`), Confluent Dedicated (`aws.confluent.cloud`)  |
| AliCloud Endpoint Service   | TiDB Cloud managed (`alicloud.tidbcloud.com`) |

If your domain is not included, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to request the support.

## Manage Private Link Connections

You can manage Private Link Connections in the Console or via CLI.

### Create an AWS Endpoint Service Private Link Connection

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
    - **Connection Type**: Choose **AWS Endpoint Service**, if you can not find this option, please ensure that your cluster is created in AWS provider.
    - **Endpoint Service Name**: Enter your AWS endpoint service name (for example, `com.amazonaws.vpce.<region>.vpce-svc-xxxx`).

    > **Note:**
    > **Note:**
    > Please make sure the AWS endpoint service:
    > 1. Is in the same region as the TiDB Cloud cluster.
    > 2. Allows connections from the TiDB Cloud account.
    > 3. Has availability zones that overlap with the TiDB Cloud cluster.
    > You can get the account ID and available zones information at the bottom of the dialog.

5. Click the **Create Connection** button.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
```

Please make sure the AWS endpoint service:

1. Allows the acceptance of TiDB Cloud account.
2. Has overlapping available zones of TiDB Cloud cluster.

You can get the account ID and available zones information by the following command:

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

</div>
</SimpleTab>

### Create an AliCloud Endpoint Service Private Link Connection

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
    - **Connection Type**: Choose **AliCloud Endpoint Service**, if you can not find this option, please ensure that your cluster is created in Alibaba Cloud provider.
    - **Endpoint Service Name**: Enter your Alibaba Cloud endpoint service name (for example, `com.aliyuncs.privatelink.<region>.xxxxx`).

    > **Note:**
    > Please make sure the Alibaba Cloud endpoint service:
    > 1. Is in the same region as the TiDB Cloud cluster.
    > 2. Allows connections from the TiDB Cloud account.
    > 3. Has availability zones that overlap with the TiDB Cloud cluster.
    > You can get the account ID and available zones information at the bottom of the dialog.
    > You can get the account ID and available zones information in the button of the dialog.

5. Click the **Create Connection** button.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type ALICLOUD_ENDPOINT_SERVICE --alicloud.endpoint-service-name <endpoint-service-name>
```

Please make sure the Alibaba Cloud endpoint service:

1. In the same region of the TiDB Cloud cluster.
2. Allows the acceptance of TiDB Cloud account.
3. Has overlapping available zones of TiDB Cloud cluster.

You can get the account ID and available zones information by the following command:

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

</div>
</SimpleTab>

### Delete a Private Link Connection

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, choose the target Private Link Connection and click **...**.

4. Click **Delete** and confirm the deletion.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection delete -c <cluster-id> --private-link-connection-id <private-link-connection-id>
```

</div>
</SimpleTab>

### Attach Domains to a Private Link Connection

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, choose the target Private Link Connection and click **...**.

4. Click **Attach Domains**.

5. In the **Attach Domains** dialog choose the domain type:
    - **TiDB Cloud Managed**: The domains will be auto generated by TiDB Cloud, just click **Attach Domains** to confirm.
    - **Confluent Cloud**: Enter the Confluent Unique Name provided by Confluent Cloud Dedicated cluster to generate the domains, and then click **Attach Domains** to confirm.

</div>

<div label="CLI">

To attach a TiDB Cloud managed domain:

First use dry run to preview the domains to be attached, it will output a unique-name for the next step

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --dry-run
```

Then Attach the domains with the unique-name from previous step

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --unique-name <unique-name>
```

To attach a Confluent Cloud domain:

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type CONFLUENT --unique-name <unique-name>
```

</div>
</SimpleTab>

## Detach Domains from a Private Link Connection

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, choose the target Private Link Connection and click **...**.

4. Click **Detach Domains** and confirm the detachment.

</div>

<div label="CLI">

First, get the Private Link Connection details to find the attach-domain-id:

```shell
ticloud serverless private-link-connection get -c <cluster-id> --private-link-connection-id <private-link-connection-id>
```

Then, detach the domain by the attach-domain-id:

```shell
ticloud serverless private-link-connection detach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --attach-domain-id <attach-domian-id>
```

</div>
</SimpleTab>

## See Also

- [Set up a private link connection to AWS RDS](/tidbcloud/serverless-private-link-connection-to-aws-rds.md)
- [Set up a private link connection to Alibaba Cloud RDS](/tidbcloud/serverless-private-link-connection-to-alicloud-rds.md)
- [Set up a private link connection to AWS Confluent](/tidbcloud/serverless-private-link-connection-to-aws-confluent.md)
- [Set up a private link connection to self-hosted Kafka cluster in AWS](/tidbcloud/serverless-private-link-connection-to-self-hosted-kafka-in-aws.md)