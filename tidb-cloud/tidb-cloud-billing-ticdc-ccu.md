---
title: Changefeed Billing for TiDB Cloud Premium
summary: Learn about billing for changefeeds in TiDB Cloud Premium.
---

# Changefeed Billing for TiDB Cloud Premium

This document describes the billing details for changefeeds in TiDB Cloud Premium.

## CCU cost

TiDB Cloud Premium measures the capacity of [changefeeds](/tidb-cloud/changefeed-overview.md) in TiCDC Changefeed Capacity Units (CCUs). When you [create a changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) for an instance, you can select an appropriate specification. The higher the CCU, the better the replication performance. You will be charged for these TiCDC CCUs.

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

Currently, TiDB Cloud Premium is in private preview. You can [contact our sales](https://www.pingcap.com/contact-us/) for pricing details.

## Private Data Link cost

If you choose the **Private Link** or **Private Service Connect** network connectivity method, additional **Private Data Link** costs will be incurred. These charges fall under the [Data Transfer Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost) category.

The price of **Private Data Link** is **$0.01/GiB**, the same as **Data Processed** of [AWS Interface Endpoint pricing](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing), **Consumer data processing** of [Google Cloud Private Service Connect pricing](https://cloud.google.com/vpc/pricing#psc-forwarding-rules), and **Inbound/Outbound Data Processed** of [Azure Private Link pricing](https://azure.microsoft.com/en-us/pricing/details/private-link/).
