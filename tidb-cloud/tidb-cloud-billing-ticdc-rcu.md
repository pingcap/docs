---
title: Changefeed Billing
summary: Learn about billing for changefeeds in TiDB Cloud.
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# Changefeed Billing

TiDB Cloud measures the capacity of changefeeds in TiCDC Replication Capacity Units (RCUs). When you create the first changefeed for a cluster, TiDB Cloud automatically sets up TiCDC RCUs for you, and you will be charged for these TiCDC RCUs. All changefeeds that are created in a single cluster share the same TiCDC RCUs.

## Number of TiCDC RCUs

For each TiDB cluster, the number of TiCDC RCUs is set up by TiDB Cloud according to the total vCPU count of all TiKV nodes in your cluster as follows:

| Total vCPUs of all TiKV nodes | Number of RCUs |
|------------------------------|----------------|
| < 48                         | 16             |
| >= 48, and < 120             | 24             |
| >= 120, and <= 168           | 32             |
| > 168                        | 40             |

## Price

To learn about the supported regions and the price of TiDB Cloud for each TiCDC RCU, see [Changefeed Cost](https://www.pingcap.com/tidb-cloud-pricing-details/#changefeed-cost).
