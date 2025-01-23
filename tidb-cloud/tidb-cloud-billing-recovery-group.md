---
title: Recovery Group Billing
summary: Learn about billing for recovery groups in TiDB Cloud.
---

# Recovery Group Billing

TiDB Cloud bills for recovery groups based on the deployed size of your TiKV nodes in the primary cluster of the recovery group. When you [create a recovery group](/tidb-cloud/recovery-group-get-started.md) for a cluster, you can select the primary cluster for the recovery group. The larger the TiKV configuration, the higher the cost for recovery group protection.

TiDB Cloud also bills for data processing per GiB basis. The data processing price varies depending on whether the data is replicated to a secondary cluster in another region, or within the same region.

## Pricing

To learn about the supported regions and the pricing for TiDB Cloud recovery groups, see [Recovery Group Cost](https://www.pingcap.com/tidb-cloud-pricing-details/#recovery-group-cost).
