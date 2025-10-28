---
title: Set Up Private Endpoint for Changefeeds
summary: Learn how to set up a private endpoint for changefeeds.
---

# Set Up Private Endpoint for Changefeeds

This document describes how to create a private endpoint for changefeeds in your TiDB Cloud Premium instances, enabling you to securely stream data to self-hosted Kafka or MySQL through private connectivity.

## Prerequisites

- Check permissions for private endpoint creation
- Set up your network connection

### Permissions

Only users with any of the following roles in your organization can create private endpoints for changefeeds:

- `Organization Owner`
- `Instance Admin` for the corresponding instance


For more information about roles in TiDB Cloud, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

### Network

Private endpoints leverage the **Private Link** technology from cloud providers, enabling resources in your VPC to connect to services in other VPCs through private IP addresses, as if those services were hosted directly within your VPC.

<SimpleTab>
<div label="AWS">

If your changefeed downstream service is hosted on AWS, collect the following information:

- The name of the Private Endpoint Service for your downstream service
- The availability zones (AZs) where your downstream service is deployed

If the Private Endpoint Service is not available for your downstream service, follow [Step 2. Expose the Kafka instance as Private Link Service](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-instance-as-private-link-service) to set up the load balancer and the Private Link Service.

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

If your changefeed downstream service is hosted on Alibaba Cloud, collect the following information:

- The name of the Private Endpoint Service for your downstream service
- The availability zones (AZs) where your downstream service is deployed

</div>
</CustomContent>

</SimpleTab>

## Step 1. Open the Networking page for your instance

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).

2. On the [**TiDB Instances**](https://tidbcloud.com/tidbs) page, click the name of your target instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations and instances.

3. In the left navigation pane, click **Settings** > **Networking**.

## Step 2. Configure the private endpoint for changefeeds

The configuration steps vary depending on the cloud provider where your instance is deployed.

<SimpleTab>
<div label="AWS">

1. On the **Networking** page, click **Create Private Endpoint** in the **AWS Private Endpoint for Changefeed** section.
2. In the **Create Private Endpoint for Changefeed** dialog, enter a name for the private endpoint.
3. Follow the reminder to authorize the [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) of TiDB Cloud to create an endpoint.
4. Enter the **Endpoint Service Name** that you collected in the [Network](#network) section.
5. Select the **Number of AZs**. Ensure that the number of AZs and the AZ IDs match your Kafka deployment.
6. If this private endpoint is created for Apache Kafka, enable the **Advertised Listener for Kafka** option.
7. Configure the advertised listener for Kafka using either the **TiDB Managed** domain or the **Custom** domain.

    - To use the **TiDB Managed** domain for advertised listeners, enter a unique string in the **Domain Pattern** field, and then click **Generate**. TiDB will generate broker addresses with subdomains for each availability zone.
    - To use your own **Custom** domain for advertised listeners, switch the domain type to **Custom**, enter the root domain in the **Custom Domain** field, click **Check**, and then specify the broker subdomains for each availability zone.

8. Click **Create** to validate the configurations and create the private endpoint.

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

1. On the **Networking** page, click **Create Private Endpoint** in the **Alibaba Cloud Private Endpoint for Changefeed** section.
2. In the **Create Private Endpoint for Changefeed** dialog, enter a name for the private endpoint.
3. Follow the reminder to whitelist TiDB Cloud's Alibaba Cloud account ID for your endpoint service to grant the TiDB Cloud VPC access.

4. Enter the **Endpoint Service Name** that you collected in the [Network](#network) section.
5. Select the **Number of AZs**. Ensure that the number of AZs and the AZ IDs match your Kafka deployment.
6. If this private endpoint is created for Apache Kafka, enable the **Advertised Listener for Kafka** option.
7. Configure the advertised listener for Kafka using either the **TiDB Managed** domain or the **Custom** domain.

    - To use the **TiDB Managed** domain for advertised listeners, enter a unique string in the **Domain Pattern** field, and then click **Generate**. TiDB will generate broker addresses with subdomains for each availability zone.
    - To use your own **Custom** domain for advertised listeners, switch the domain type to **Custom**, enter the root domain in the **Custom Domain** field, click **Check**, and then specify the broker subdomains for each availability zone.

8. Click **Create** to validate the configurations and create the private endpoint.

</div>
</CustomContent>
</SimpleTab>
