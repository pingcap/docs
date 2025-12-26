---
title: Private Link Connections for Dataflow (Beta)
summary: Learn how to set up private link connections for Dataflow.
---

# Private Link Connections for Dataflow (Beta)

## Overview

Dataflow services in TiDB Cloud, such as Changefeed and Data Migration (DM), require reliable connectivity to external resources such as RDS instances and Kafka clusters. While public endpoints are supported, private link connections provide a superior alternative by providing higher efficiency, lower latency, and enhanced security.

By facilitating direct, private connectivity between {{{ .essential }}} and your target resources, private link ensures that data traffic never traverses the public internet. This architecture is purpose-built for high-performance integrations, significantly reducing the network attack surface while maintaining consistent data throughput for critical replication tasks.

## Private link connection types

### AWS Endpoint Service

This type of private link connection enables TiDB Cloud clusters on **AWS** to connect to your [AWS endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html) powered by AWS PrivateLink.

The private link connection can access various AWS services by associating them to the endpoint service, such as RDS instances and Kafka services.

### Alibaba Cloud Endpoint Service

This type of private link connection enables TiDB Cloud clusters on **Alibaba Cloud** to connect to your [Alibaba Cloud endpoint service](https://www.alibabacloud.com/help/en/privatelink/share-your-service/#51976edba8no7) powered by Alibaba Cloud PrivateLink.

The private link connection can access various Alibaba Cloud services by associating them to the endpoint service, such as RDS instances and Kafka services.

## Attach Domains

You can attach domains to a private link connection. 

When a domain is attached to the private link connection, all traffic to this domain will be routed to this private link connection. It is useful when your service provides custom domains to clients at runtime, such as Kafka advertised listeners.

Different private link connection types support attaching different domains:

| Private link connection type | Supported domain type              |
|-----------------------------|-------------------------------------------|
| AWS Endpoint Service        | <ul><li>TiDB Cloud managed (`aws.tidbcloud.com`)</li><li>Confluent Dedicated (`aws.confluent.cloud`)</li></ul>  |
| AliCloud Endpoint Service   | TiDB Cloud managed (`alicloud.tidbcloud.com`) |

If your domain is not included, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to request the support.

## Manage private link connections

You can create a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

### Create an AWS Endpoint Service private link connection

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.

4. Enter the required information in the **Create Private Link Connection** dialog:

    - **Private Link Connection Name**: Enter a name for the private link connection.
    - **Connection Type**: Choose **AWS Endpoint Service**, if you can not find this option, please ensure that your cluster is created in AWS provider.
    - **Endpoint Service Name**: Enter your AWS endpoint service name (for example, `com.amazonaws.vpce.<region>.vpce-svc-xxxx`).

    > **Note:**
    >
    > Please make sure the AWS endpoint service:
    > 
    > 1. In the same region as your TiDB Cloud cluster.
    > 2. Allows connections from the TiDB Cloud account.
    > 3. Has availability zones that overlap with your TiDB Cloud cluster.
    > 
    > You can get the account ID and available zones information at the bottom of the dialog.

5. Click the **Create Connection** button.

6. Then go to the detail page of your endpoint service on AWS console. In the **Endpoint Connections** tab, accept the endpoint connection request from TiDB Cloud.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
```

Then go to the detail page of your endpoint service on AWS console. In the **Endpoint Connections** tab, accept the endpoint connection request from TiDB Cloud.

Please make sure the AWS endpoint service:

1. In the same region of your TiDB Cloud cluster.
2. Allows the acceptance of TiDB Cloud account.
3. Has overlapping available zones of your TiDB Cloud cluster.

You can get the account ID and available zones information by the following command:

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

</div>
</SimpleTab>

### Create an Alibaba Cloud Endpoint Service private link connection

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, click **Create Private Link Connection**.

4. Enter the required information in the **Create Private Link Connection** dialog:

    - **Private Link Connection Name**: Enter a name for the private link connection.
    - **Connection Type**: Choose **Alibaba Cloud Endpoint Service**. If you can not find this option, ensure that your cluster is created in Alibaba Cloud.
    - **Endpoint Service Name**: Enter your Alibaba Cloud endpoint service name (for example, `com.aliyuncs.privatelink.<region>.xxxxx`).

    > **Note:**
    > 
    > Please make sure the Alibaba Cloud endpoint service:
    > 
    > 1. In the same region as your TiDB Cloud cluster.
    > 2. Allows connections from the TiDB Cloud account.
    > 3. Has availability zones that overlap with your TiDB Cloud cluster.
    > 
    > You can get the account ID and available zones information at the bottom of the dialog.

5. Click **Create Connection**.

6. Then go to the detail page of your endpoint service on Alibaba Cloud console. In the **Endpoint Connections** tab, allow the endpoint connection request from TiDB Cloud.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type ALICLOUD_ENDPOINT_SERVICE --alicloud.endpoint-service-name <endpoint-service-name>
```

Then go to the detail page of your endpoint service on Alibaba Cloud console. In the **Endpoint Connections** tab, allow the endpoint connection request from TiDB Cloud.

Please make sure the Alibaba Cloud endpoint service:

1. In the same region of your TiDB Cloud cluster.
2. Allows the acceptance of TiDB Cloud account.
3. Has overlapping available zones of your TiDB Cloud cluster.

You can get the account ID and available zones information by the following command:

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

</div>
</SimpleTab>

### Delete a private link connection

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, choose the target private link connection and click **...**.

4. Click **Delete** and confirm the deletion.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection delete -c <cluster-id> --private-link-connection-id <private-link-connection-id>
```

</div>
</SimpleTab>

### Attach domains to a private link connection

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, choose the target private link connection and click **...**.

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

### Detach Domains from a private link connection

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow**, choose the target private link connection and click **...**.

4. Click **Detach Domains** and confirm the detachment.

</div>

<div label="CLI">

First, get the private link connection details to find the attach-domain-id:

```shell
ticloud serverless private-link-connection get -c <cluster-id> --private-link-connection-id <private-link-connection-id>
```

Then, detach the domain by the attach-domain-id:

```shell
ticloud serverless private-link-connection detach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --attach-domain-id <attach-domain-id>
```

</div>
</SimpleTab>

## See Also

- [Connect to Amazon RDS via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-aws-rds.md)
- [Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection ](/tidbcloud/serverless-private-link-connection-to-alicloud-rds.md)
- [Connect to Confluent Cloud via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-aws-confluent.md)
- [Connect to AWS Self-Hosted Kafka via Private Link Connection](/tidbcloud/serverless-private-link-connection-to-self-hosted-kafka-in-aws.md)
- [Connect to Alibaba Cloud Self-Hosted Kafka via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-self-hosted-kafka-in-alicloud.md)