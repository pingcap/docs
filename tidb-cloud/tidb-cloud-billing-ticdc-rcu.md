---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# Changefeed Billing

<CustomContent plan="dedicated">

## RCU cost for TiDB Cloud Dedicate

TiDB Cloud Dedicate measures the capacity of [changefeeds](/tidb-cloud/changefeed-overview.md) in TiCDC Replication Capacity Units (RCUs). When you [create a changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) for a cluster, you can select an appropriate specification. The higher the RCU, the better the replication performance. You will be charged for these TiCDC changefeed RCUs.

### Number of TiCDC RCUs

The following table lists the specifications and corresponding replication performances for changefeeds:

| Specification | Maximum replication performance |
|---------------|---------------------------------|
| 2 RCUs        | 5,000 rows/s                    |
| 4 RCUs        | 10,000 rows/s                   |
| 8 RCUs        | 20,000 rows/s                   |
| 16 RCUs       | 40,000 rows/s                   |
| 24 RCUs       | 60,000 rows/s                   |
| 32 RCUs       | 80,000 rows/s                   |
| 40 RCUs       | 100,000 rows/s                  |
| 64 RCUs       | 160,000 rows/s                  |
| 96 RCUs       | 240,000 rows/s                  |
| 128 RCUs      | 320,000 rows/s                  |
| 192 RCUs      | 480,000 rows/s                  |
| 256 RCUs      | 640,000 rows/s                  |
| 320 RCUs      | 800,000 rows/s                  |
| 384 RCUs      | 960,000 rows/s                  |

> **Note:**
>
> The preceding performance data is for reference only and might vary in different scenarios. It is strongly recommended that you conduct a real workload test before using the changefeed feature in a production environment. For further assistance, contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

### Price

To learn about the supported regions and the price of TiDB Cloud for each TiCDC RCU, see [Changefeed Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#changefeed-cost).

</CustomContent>

<CustomContent plan="premium">
## CCU cost for TiDB Cloud Premium

TiDB Cloud Premium measures the capacity of [changefeeds](/tidb-cloud/changefeed-overview-premium.md) in TiCDC Changefeed Capacity Units (CCUs). When you [create a changefeed](/tidb-cloud/changefeed-overview-premium.md#create-a-changefeed) for a instance, you can select an appropriate specification. The higher the CCU, the better the replication performance. You will be charged for these TiCDC CCUs.

### Number of TiCDC CCUs

The following table lists the specifications and corresponding replication performances for changefeeds:

| Specification | Maximum replication performance |
|---------------|---------------------------------|
| 2 CCUs        | 5,000 rows/s                    |
| 4 CCUs        | 10,000 rows/s                   |
| 8 CCUs        | 20,000 rows/s                   |
| 16 CCUs       | 40,000 rows/s                   |
| 24 CCUs       | 60,000 rows/s                   |
| 32 CCUs       | 80,000 rows/s                   |
| 40 CCUs       | 100,000 rows/s                  |
| 64 CCUs       | 160,000 rows/s                  |
| 96 CCUs       | 240,000 rows/s                  |
| 128 CCUs      | 320,000 rows/s                  |
| 192 CCUs      | 480,000 rows/s                  |
| 256 CCUs      | 640,000 rows/s                  |
| 320 CCUs      | 800,000 rows/s                  |
| 384 CCUs      | 960,000 rows/s                  |

> **Note:**
>
> The preceding performance data is for reference only and might vary in different scenarios. It is strongly recommended that you conduct a real workload test before using the changefeed feature in a production environment. For further assistance, contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

### Price

As Premium is currently in private preview, you can [contact our sales](https://www.pingcap.com/contact-us/) for pricing details.

</CustomContent>

## Private Data Link cost

If you choose the **Private Link** or **Private Service Connect** network connectivity method, additional **Private Data Link** costs will be incurred. These charges fall under the [Data Transfer Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost) category.

The price of **Private Data Link** is **$0.01/GiB**, the same as **Data Processed** of [AWS Interface Endpoint pricing](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing), **Consumer data processing** of [Google Cloud Private Service Connect pricing](https://cloud.google.com/vpc/pricing#psc-forwarding-rules), and **Inbound/Outbound Data Processed** of [Azure Private Link pricing](https://azure.microsoft.com/en-us/pricing/details/private-link/).
