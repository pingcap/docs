---
title: Set Up Private Endpoint for Changefeeds
summary: Learn how to set up a private endpoint for changefeeds.
---

# Set Up Private Endpoint for Changefeeds

This document describes how to create a private endpoint for changefeeds in your TiDB Cloud Dedicated clusters, enabling you to securely stream data to self-hosted Kafka or MySQL through private connectivity.

## Restrictions

Within the same VPC, each Private Endpoint Service in AWS, Service Attachment in Google Cloud, or Private Link Service in Azure can have up to 5 private endpoints. If this limit is exceeded, remove any unused private endpoints before creating new ones.

## Prerequisites

- Check permissions for private endpoint creation
- Set up your network connection

### Permissions

Only users with the `Organization Owner`, `Project Owner` or `Project Data Access Read-Write` roles in your organization can create private endpoints for changefeeds. For more information about roles in TiDB Cloud, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

### Network

Private endpoints leverage **Private Link** or **Private Service Connect** technologies from cloud providers, enabling resources in your VPC to connect to services in other VPCs through private IP addresses, as if those services were hosted directly within your VPC.

<SimpleTab>
<div label="AWS">

If your changefeed downstream service is hosted on AWS, collect the following information:

- The name of the Private Endpoint Service for your downstream service
- The availability zones (AZs) where your downstream service is deployed

If the Private Endpoint Service is not available for your downstream service, follow [Step 2. Expose the Kafka cluster as Private Link Service](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service) to set up the load balancer and the Private Link Service.

</div>

<div label="Google Cloud">

If your changefeed downstream service is hosted on Google Cloud, collect the Service Attachment information of your downstream service.

If Service Attachment is not available for your downstream service, follow [Step 2. Expose Kafka-proxy as Private Service Connect Service](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md#step-2-expose-kafka-proxy-as-private-service-connect-service) to get the Service Attachment information.

</div>

<div label="Azure">

If your changefeed downstream service is hosted on Azure, collect the alias of the Private Link Service of your downstream service.

If the Private Endpoint Service is not available for your downstream service, follow [Step 2. Expose the Kafka cluster as Private Link Service](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service) to set up the load balancer and the Private Link Service.

</div>
</SimpleTab>

## Step 1. Open the Networking page for your cluster

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).
2. On the [**Clusters**](https://tidbcloud.com/project/clusters) page, click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

3. In the left navigation pane, click **Settings** > **Networking**.

## Step 2. Configure the private endpoint for changefeeds

The configuration steps vary depending on the cloud provider where your cluster is deployed.

<SimpleTab>
<div label="AWS">

1. On the **Networking** page, click **Create Private Endpoint** in the **AWS Private Endpoint for Changefeed** section.
2. In the **Create Private Endpoint for Changefeed** dialog, enter a name for the private endpoint.
3. Follow the reminder to authorize the [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) of TiDB Cloud to create an endpoint.
4. Enter the **Endpoint Service Name** that that you collected in the [Network](#network) section.
5. Select the **Number of AZs**. Ensure that the number of AZs and the AZ IDs match your Kafka deployment.
6. If this private endpoint is created for Apache Kafka, enable the **Advertised Listener for Kafka** option.
7. Configure the advertised listener for Kafka using either **TiDB Managed** domain or **Custom** domain.

    - To use **TiDB Managed** domain for advertised listeners, enter a unique string in the **Domain Pattern** field, and then click **Generate**. TiDB will generate broker addresses with subdomains for each availability zone.
    - To use your own **Custom** domain for advertised listeners, switch the domain type to **Custom**, enter the root domain in the **Custom Domain** field, click **Check**, and then specify the broker subdomains for each availability zone.

8. Click **Create** to validate the configurations and create the private endpoint.

</div>

<div label="Google Cloud">

1. On the **Networking** page, click **Create Private Endpoint** in the **Google Cloud Private Endpoint for Changefeed** section.
2. In the **Create Private Endpoint for Changefeed** dialog, enter a name for the private endpoint.
3. Follow the reminder to authorize the [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) of TiDB Cloud to pre-approve endpoint creation, or manually approve the endpoint connection request when you receive it.
4. Enter the **Service Attachment** that that you collected in the [Network](#network) section.
5. If this private endpoint is created for Apache Kafka, enable the **Advertised Listener for Kafka** option.
6. Configure the advertised listener for Kafka using either **TiDB Managed** domain or **Custom** domain.

    - To use **TiDB Managed** domain for advertised listeners, enter a unique string in the **Domain Pattern** field, and then click **Generate**. TiDB will generate broker addresses with subdomains for each availability zone.
    - To use your own **Custom** domain for advertised listeners, switch the domain type to **Custom**, enter the root domain in the **Custom Domain** field, click **Check**, and then specify the broker subdomains for each availability zone.

7. Click **Create** to validate the configurations and create the private endpoint.

</div>

<div label="Azure">

1. On the **Networking** page, click **Create Private Endpoint** in the **Azure Private Endpoint for Changefeed** section.
2. In the **Create Private Endpoint for Changefeed** dialog, enter a name for the private endpoint.
3. Follow the reminder to authorize the Azure subscription of TiDB Cloud or allow anyone with your alias to access your Private Link service before creating the changefeed. For more information about Private Link service visibility, see [Control service exposure](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview#control-service-exposure) in Azure documentation.
4. Enter the **Alias of Private Link Service** that you collected in the [Network](#network) section.
5. If this private endpoint is created for Apache Kafka, enable the **Advertised Listener for Kafka** option.
6. Configure the advertised listener for Kafka using either **TiDB Managed** domain or **Custom** domain.

    - To use **TiDB Managed** domain for advertised listeners, enter a unique string in the **Domain Pattern** field, and then click **Generate**. TiDB will generate broker addresses with subdomains for each availability zone.
    - To use your own **Custom** domain for advertised listeners, switch the domain type to **Custom**, enter the root domain in the **Custom Domain** field, click **Check**, and then specify the broker subdomains for each availability zone.
7. Click **Create** to validate the configurations and create the private endpoint.

</div>
</SimpleTab>
