---
title: Private Link Connections for Dataflow (Beta)
summary: Learn how to set up private link connections for Dataflow.
---

# Private Link Connections for Dataflow (Beta)

Dataflow services in TiDB Cloud, such as Changefeed and Data Migration (DM), require reliable connectivity to external resources such as RDS instances and Kafka clusters. While public endpoints are supported, private link connections provide a superior alternative by providing higher efficiency, lower latency, and enhanced security.

Private link connections enable direct connectivity between {{{ .essential }}} and your target resources. This ensures that data traveling from TiDB Cloud to your databases on other cloud platforms remains entirely within private network boundaries, significantly reducing the network attack surface and ensuring consistent throughput for critical dataflows.

> **Note:**
>
> The Private Link Connections for Dataflow feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Private link connection types

Private link connections for dataflow come in several types depending on the cloud provider and service you need to reach. Each type enables secure and private network access between your TiDB Cloud cluster and external resources (for example, RDS or Kafka) in the same cloud environment.

### AWS Endpoint Service

This type of private link connection enables TiDB Cloud clusters on **AWS** to connect to your [AWS endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html) powered by AWS PrivateLink.

The private link connection can access various AWS services by associating them to the endpoint service, such as RDS instances and Kafka services.

### Alibaba Cloud Endpoint Service

This type of private link connection enables TiDB Cloud clusters on **Alibaba Cloud** to connect to your [Alibaba Cloud endpoint service](https://www.alibabacloud.com/help/en/privatelink/share-your-service/#51976edba8no7) powered by Alibaba Cloud PrivateLink.

The private link connection can access various Alibaba Cloud services by associating them to the endpoint service, such as RDS instances and Kafka services.

## Attach Domains

You can attach domains to a private link connection. 

When a domain is attached to the private link connection, all traffic to this domain will be routed to this private link connection. It is useful when your service provides custom domains to clients at runtime, such as Kafka advertised listeners.

Different private link connection types support attaching different domains. The following table shows supported domain types for each private link connection type.

| Private link connection type   | Supported domain type                     |
|--------------------------------|-------------------------------------------|
| AWS Endpoint Service           | <ul><li>TiDB Cloud managed (`aws.tidbcloud.com`)</li><li>Confluent Dedicated (`aws.confluent.cloud`)</li></ul>  |
| Alibaba Cloud Endpoint Service | TiDB Cloud managed (`alicloud.tidbcloud.com`) |

If your domain is not included in this table, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to request the support.

## Manage private link connections

This section describes how to manage private link connections.

### Create an AWS Endpoint Service private link connection

You can create an AWS Endpoint Service private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

Ensure the AWS endpoint service:

- Resides in the same region as your TiDB Cloud cluster.
- Allows connections from the TiDB Cloud account.
- Has availability zones that overlap with your TiDB Cloud cluster.

You can get the account ID and available zones information at the bottom of the **Create Private Link Connection** dialog, or by running the following command.

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow** area, click **Create Private Link Connection**.

4. Enter the required information in the **Create Private Link Connection** dialog:

    - **Private Link Connection Name**: enter a name for the private link connection.
    - **Connection Type**: select **AWS Endpoint Service**. If you cannot find this option, ensure that your cluster is created on AWS.
    - **Endpoint Service Name**: enter your AWS endpoint service name, for example, `com.amazonaws.vpce.<region>.vpce-svc-xxxx`.

5. Click **Create**.

6. Go to the detail page of your endpoint service on the [AWS console](https://console.aws.amazon.com). In the **Endpoint Connections** tab, accept the endpoint connection request from TiDB Cloud.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
```

Then go to the detail page of your endpoint service on AWS console. In the **Endpoint Connections** tab, accept the endpoint connection request from TiDB Cloud.

</div>
</SimpleTab>

### Create an Alibaba Cloud Endpoint Service private link connection

You can create an Alibaba Cloud Endpoint Service private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

Ensure that the Alibaba Cloud endpoint service:

- Resides in the same region of your TiDB Cloud cluster.
- Allows the acceptance of TiDB Cloud account.
- Has overlapping available zones with your TiDB Cloud cluster.

You can get the account ID and available zones information at the bottom of the **Create Private Link Connection** dialog, or by running the following command:

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

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
    - **Endpoint Service Name**: enter the Alibaba Cloud endpoint service name, for example, `com.aliyuncs.privatelink.<region>.xxxxx`.

5. Click **Create**.

6. Go to the detail page of your endpoint service on [Alibaba Cloud console](https://console.alibabacloud.com). In the **Endpoint Connections** tab, allow the endpoint connection request from TiDB Cloud.

</div>

<div label="CLI">

To create a private link connection using the TiDB Cloud CLI:

1. Run the following command:

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type ALICLOUD_ENDPOINT_SERVICE --alicloud.endpoint-service-name <endpoint-service-name>
    ```

2. Go to the detail page of your endpoint service on [Alibaba Cloud console](https://console.alibabacloud.com). In the **Endpoint Connections** tab, allow the endpoint connection request from TiDB Cloud.

</div>
</SimpleTab>

### Delete a private link connection

You can delete private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

<SimpleTab>
<div label="Console">

To delete the private link connection using the TiDB Cloud console, do the following:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow** area, choose the target private link connection, and then click **...**.

4. Click **Delete**, and then confirm the deletion.

</div>

<div label="CLI">

```shell
ticloud serverless private-link-connection delete -c <cluster-id> --private-link-connection-id <private-link-connection-id>
```

</div>
</SimpleTab>

### Attach domains to a private link connection

You can attach domains to a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

<SimpleTab>
<div label="Console">

To attach domains to a private link connection using the TiDB Cloud, do the following:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow** area, choose the target private link connection, and then click **...**.

4. Click **Attach Domains**.

5. In the **Attach Domains** dialog, choose the domain type:

    - **TiDB Cloud Managed**: the domains will be generated automatically by TiDB Cloud. Click **Attach Domains** to confirm.
    - **Confluent Cloud**: enter the Confluent unique name provided by the Confluent Cloud Dedicated cluster to generate the domains, and then click **Attach Domains** to confirm.

</div>

<div label="CLI">

To attach a TiDB Cloud managed domain using TiDB Cloud CLI, do the following:

1. Use dry run to preview the domains to be attached. It outputs a unique name for the next step.

    ```shell
    ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --dry-run
    ```

2. Attach the domains with the unique name from the previous step.

    ```shell
    ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --unique-name <unique-name>
    ```

To attach a Confluent Cloud domain:

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type CONFLUENT --unique-name <unique-name>
```

</div>
</SimpleTab>

### Detach domains from a private link connection

You can detach domains to a private link connection using the TiDB Cloud console or the TiDB Cloud CLI.

<SimpleTab>
<div label="Console">

 To detach domains from a private link connection using the TiDB Cloud console, do the following:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.

3. In the **Private Link Connection For Dataflow** area, choose the target private link connection, and then click **...**.

4. Click **Detach Domains**, and then confirm the detachment.

</div>

<div label="CLI">

To detach domains from a private link connection using the TiDB Cloud CLI, do the following:

1. Get the private link connection details to find the `attach-domain-id`:

    ```shell
    ticloud serverless private-link-connection get -c <cluster-id> --private-link-connection-id <private-link-connection-id>
    ```

2. Detach the domain by the `attach-domain-id`:

    ```shell
     ticloud serverless private-link-connection detach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --attach-domain-id <attach-domain-id>
    ```

</div>
</SimpleTab>

## See Also

- [Connect to Confluent Cloud via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-aws-confluent.md)

<!--
- [Connect to Amazon RDS via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-aws-rds.md)
- [Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection ](/tidbcloud/serverless-private-link-connection-to-alicloud-rds.md)
- [Connect to AWS Self-Hosted Kafka via Private Link Connection](/tidbcloud/serverless-private-link-connection-to-self-hosted-kafka-in-aws.md)
- [Connect to Alibaba Cloud Self-Hosted Kafka via a Private Link Connection](/tidbcloud/serverless-private-link-connection-to-self-hosted-kafka-in-alicloud.md)
-->