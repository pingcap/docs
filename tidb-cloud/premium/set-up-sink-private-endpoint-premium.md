---
title: Set Up Private Endpoint for Changefeeds
summary: Learn how to set up a private endpoint for changefeeds.
---

# Set Up Private Endpoint for Changefeeds

This document describes how to create a private endpoint for changefeeds in your {{{ .premium }}} instances, enabling you to securely stream data to self-hosted Kafka, Amazon MSK Provisioned clusters, or MySQL through private connectivity.

## Prerequisites

- Check permissions for private endpoint creation
- Set up your network connection

### Permissions

Only users with one of the following roles in your organization can create private endpoints for changefeeds:

- `Organization Owner`
- `Instance Manager` for the corresponding instance

For more information about roles in TiDB Cloud, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

### Network

Private endpoints leverage the **Private Link** technology from cloud providers, enabling resources in your VPC to connect to services in other VPCs through private IP addresses, as if those services were hosted directly within your VPC.

> **Note:**
>
> - A private endpoint is an organization-level resource and is not tied to a specific {{{ .premium }}} instance. Private endpoints created within the same organization and in the same region can be shared by multiple instances connecting to the same downstream service, so you do not need to create a separate endpoint for each instance.
> - Deleting a {{{ .premium }}} instance does not delete its private endpoints. A private endpoint is automatically deleted if it is not used by any instance for 30 days, even if the instances that previously used it remain available. You can also manually delete a private endpoint when it is no longer needed. However, you cannot delete it while it is in use by any instance.

<SimpleTab>
<div label="AWS">

If your changefeed downstream service is hosted on AWS, collect the following information based on your connection type:

- **AWS Endpoint Service**: the endpoint service name for your downstream service and the availability zones (AZs) where your downstream service is deployed.

    If the Private Endpoint Service is not available for your downstream service, follow [Step 2. Expose the Kafka cluster as Private Link Service](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service) to set up the load balancer and the Private Link Service.

- **Amazon MSK Provisioned**: the ARN of your Amazon MSK Provisioned cluster. To learn about how to create an Amazon MSK Provisioned cluster for changefeeds, see [Set Up an Amazon MSK Provisioned Cluster via AWS PrivateLink](/tidb-cloud/setup-aws-msk-provisioned-private-link-service.md).

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

If your changefeed downstream service is hosted on Alibaba Cloud, collect the following information:

- The name of the Private Endpoint Service for your downstream service
- The availability zones (AZs) where your downstream service is deployed

To grant TiDB Cloud VPC access, you must add the TiDB Cloud's Alibaba Cloud account ID to the allowlist of your endpoint service.

If the Private Endpoint Service is not available for your downstream service, follow [Step 2. Expose the Kafka cluster as Private Link Service](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service) to set up the load balancer and the Private Link Service.

</div>
</CustomContent>

</SimpleTab>

## Step 1. Open the Networking page for your instance

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).

2. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target {{{ .premium }}} instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations and instances.

3. In the left navigation pane, click **Settings** > **Networking**.

## Step 2. Configure the private endpoint for changefeeds

The configuration steps vary depending on the cloud provider where your instance is deployed.

<SimpleTab>
<div label="AWS">

On AWS, choose a connection type based on the downstream service:

- If your downstream service is exposed through an AWS endpoint service, such as self-hosted Kafka or MySQL, select **AWS Endpoint Service**.
- If your downstream service is an Amazon MSK Provisioned cluster, select **Amazon MSK Provisioned**.

**AWS Endpoint Service**

1. On the **Networking** page, click **Create Private Endpoint for External Services** in the **AWS Private Endpoints for External Services** section.
2. In the displayed dialog, enter a name for the private endpoint.
3. Follow the reminder to authorize the [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) of TiDB Cloud to create an endpoint.
4. Enter the **Endpoint Service Name** that you collected in the [Network](#network) section, and then select **AWS Endpoint Service** as the connection type.
5. Select the **Number of AZs**. Ensure that the number of AZs and the AZ IDs match your Kafka deployment.
6. If this private endpoint is created for Apache Kafka, select the **Configure Advertised Listener for Kafka** checkbox.
7. Configure the advertised listener for Kafka using either the **TiDB Managed** domain or the **Custom** domain.

    - To use the **TiDB Managed** domain for advertised listeners, enter a unique string in the **Domain Pattern** field, and then click **Generate**. TiDB Cloud will generate broker addresses with subdomains for each availability zone.
    - To use your own **Custom** domain for advertised listeners, switch the domain type to **Custom**, enter the root domain in the **Custom Domain** field, click **Check**, and then specify the broker subdomains for each availability zone.

8. Click **Create** to validate the configurations and create the private endpoint.

**Amazon MSK Provisioned**

1. On the **Networking** page, click **Create Private Endpoint for External Services** in the **AWS Private Endpoints for External Services** section.
2. In the displayed dialog, enter a name for the private endpoint, and then select **AWS MSK Provisioned** as the connection type.
3. Enter the **MSK Cluster ARN** of your Amazon MSK Provisioned cluster. To learn about how to create an Amazon MSK Provisioned cluster for changefeeds, see [Set Up an Amazon MSK Provisioned Cluster via AWS PrivateLink](/tidb-cloud/setup-aws-msk-provisioned-private-link-service.md).
4. Click **Create** to validate the configurations and create the private endpoint.

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

1. On the **Networking** page, click **Create Private Endpoint for External Services** in the **Alibaba Cloud Private Endpoints for External Services** section.
2. In the **Create Private Endpoint for External Services** dialog, enter a name for the private endpoint.
3. Follow the reminder to add TiDB Cloud's Alibaba Cloud account ID to the allowlist of your endpoint service to grant TiDB Cloud VPC access. For more information, see [managing account IDs in the allowlist of an endpoint service](https://www.alibabacloud.com/help/en/privatelink/user-guide/add-and-manage-service-whitelists).
4. Enter the **Endpoint Service Name** that you collected in the [Network](#network) section.
5. Select the **Number of AZs**. Ensure that the number of AZs and the AZ IDs match your Kafka deployment.
6. If this private endpoint is created for Apache Kafka, select the **Configure Advertised Listener for Kafka** checkbox.
7. Configure the advertised listener for Kafka using either the **TiDB Managed** domain or the **Custom** domain.

    - To use the **TiDB Managed** domain for advertised listeners, enter a unique string in the **Domain Pattern** field, and then click **Generate**. TiDB will generate broker addresses with subdomains for each availability zone.
    - To use your own **Custom** domain for advertised listeners, switch the domain type to **Custom**, enter the root domain in the **Custom Domain** field, click **Check**, and then specify the broker subdomains for each availability zone.

8. Click **Create** to validate the configurations and create the private endpoint.

</div>
</CustomContent>
</SimpleTab>
