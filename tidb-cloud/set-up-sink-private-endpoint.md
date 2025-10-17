---
title: Set Up Private Endpoint for Changefeed
summary: Learn how to set up private endpoint for changefeed.
---

# Set Up Private Endpoint for Changefeed

This document explains how to create a private endpoint for changefeed in TiDB Cloud Dedicated, enabling you to sink data downstream to Self-Hosted Kafka or MySQL.

## Restrictions

- Only Organization Owner and Project Owner roles can create private endpoints for changefeeds.
- Within the same VPC, each Private Endpoint Service in AWS, Service Attachment in Google Cloud, or Private Link Service in Azure can have up to 5 private endpoints. If you exceed this limit, please remove any unused private endpoints before creating new ones.

## Prerequisites

- Set up your network connection

### Network

Private Connect leverages **Private Link** or **Private Service Connect** technologies from cloud providers, allowing resources in your VPC to connect to services in other VPCs using private IP addresses, as if those services were hosted directly within your VPC.

<SimpleTab>

<div label="AWS">
For AWS, prepare the following information. Refer to [Step 2. Expose the Kafka cluster as Private Link Service](https://docs.pingcap.com/tidbcloud/setup-aws-self-hosted-kafka-private-link-service/#step-2-expose-the-kafka-cluster-as-private-link-service) for more details.

- Private Endpoint Service
- Availability Zones where your downstream service is located
- If the private endpoint is created for an Apache Kafka service, you can use either a TiDB managed domain or your own custom domain for the advertised listener.
  - For a TiDB managed domain, prepare the ID for the Kafka Advertised Listener Pattern.
  - For a custom domain, prepare your primary domain and subdomains for the corresponding availability zones.
  </div>

<div label="Google Cloud">
For Google Cloud, prepare the following information. Refer to [Step 2. Expose the Kafka cluster as Private Service Connect](https://docs.pingcap.com/tidbcloud/setup-self-hosted-kafka-private-service-connect/#step-2-expose-the-kafka-cluster-as-private-service-connect) for more details.

- Service Attachment
- If the private endpoint is created for an Apache Kafka service, you can use either a TiDB managed domain or your own custom domain for the advertised listener.
  - For a TiDB managed domain, prepare the ID for the Kafka Advertised Listener Pattern.
  - For a custom domain, prepare your root domain.
  </div>

<div label="Azure">
For Azure, prepare the following information. Refer to [Step 2. Expose the Kafka cluster as Private Link Service](https://docs.pingcap.com/tidbcloud/setup-azure-self-hosted-kafka-private-link-service/#step-2-expose-the-kafka-cluster-as-private-link-service) for more details.

- Alias of the Private Link Service
- If the private endpoint is created for an Apache Kafka service, you can use either a TiDB managed domain or your own custom domain for the advertised listener.
  - For a TiDB managed domain, prepare the ID for the Kafka Advertised Listener Pattern.
  - For a custom domain, prepare your root domain.
  </div>
  </SimpleTab>

## Step 1. Open the private endpoint creation page

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).
2. Navigate to the cluster overview page of the TiDB cluster, then click **Settings** > **Networking**.
3. Click **Create Private Endpoint** in the **Private Endpoint for Changefeed** section.

## Step 2. Configure the private endpoint for changefeed

The configuration steps vary depending on the cloud provider where your cluster is deployed.

<SimpleTab>
<div label="AWS">
1. Authorize the [AWS Principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts) of TiDB Cloud to create an endpoint for your endpoint service. The AWS Principal is provided in the tip on the web page.

2. Enter a **Name** for this **Private Endpoint**.

3. Enter the **Endpoint Service Name** that you configured in [Set Up Self-Hosted Kafka Private Link Service in AWS](https://docs.pingcap.com/tidbcloud/setup-aws-self-hosted-kafka-private-link-service/).

4. Select the **Number of Availability Zones**. Ensure the **Number of AZs** and **AZ IDs** are the same as your Kafka deployment.

5. If this private endpoint is created specifically for Apache Kafka, the **Advertised Listener for Kafka** is required. Enable the switch.

6. The advertised listener for Kafka supports both **TiDB Managed Domain** and **Custom Domain**.

   - If using **TiDB Managed Domain**, enter the same unique ID in the **Kafka Advertised Listener Pattern** that you used when setting up the Kafka Private Link Service in the **Network** section.

   - If using a **Custom Domain**, enter the root domain and click the **Check** button next to it. Then enter the broker subdomains for the corresponding availability zones.

7. Click **Create** to validate the configurations and create the private endpoint.
</div>

<div label="Google Cloud">
1. Authorize the [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) of TiDB Cloud to pre-approve endpoint creation for your Private Service Connect service, or manually approve the endpoint connection request when received. The project ID is provided in the tip on the web page.

2. Enter a **Name** for this **Private Endpoint**.

3. Enter the **Service Attachment** that you configured in [Set up Self Hosted Kafka Private Service Connect in Google Cloud](https://docs.pingcap.com/tidbcloud/setup-self-hosted-kafka-private-service-connect/).

4. If this private endpoint is created specifically for Apache Kafka, the **Advertised Listener for Kafka** is required. Enable the switch.

5. The advertised listener for Kafka supports both **TiDB Managed Domain** and **Custom Domain**.

   - If using **TiDB Managed Domain**, enter the same unique ID in the **Kafka Advertised Listener Pattern** that you used when setting up the Kafka Private Service Connect in the **Network** section.

   - If using a **Custom Domain**, enter the root domain and click the **Check** button next to it. Then enter the broker subdomain.

6. Click **Create** to validate the configurations and create the private endpoint.
</div>

<div label="Azure">
1. Authorize the Azure subscription of TiDB Cloud or allow anyone with your alias to access your Private Link service before creating the changefeed. The Azure subscription is provided in the **Reminders before proceeding** tip on the web page. For more information about Private Link service visibility, see [Control service exposure](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview#control-service-exposure) in Azure documentation.

2. Enter a **Name** for this **Private Endpoint**.

3. Enter the **Alias of Private Link Service** that you configured in [Set Up Self-Hosted Kafka Private Link Service in Azure](https://docs.pingcap.com/tidbcloud/setup-azure-self-hosted-kafka-private-link-service/).

4. If this private endpoint is created specifically for Apache Kafka, the **Advertised Listener for Kafka** is required. Enable the switch.

5. The advertised listener for Kafka supports both **TiDB Managed Domain** and **Custom Domain**.

   - If using **TiDB Managed Domain**, enter the same unique ID in the **Kafka Advertised Listener Pattern** that you used when setting up the Kafka Private Link Service in the **Network** section.

   - If using a **Custom Domain**, enter the root domain and click the **Check** button next to it. Then enter the broker subdomain.

6. Click **Create** to validate the configurations and create the private endpoint.
</div>
</SimpleTab>
