---
title: Features
summary: Learn about feature support status for different TiDB Cloud plans.
---

# Features

This document lists the feature support status for different TiDB Cloud plans, including TiDB Cloud Starter, TiDB Cloud Essential, and TiDB Cloud Dedicated.

> **Tip:**
>
> [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/#starter) is the best way to get started with TiDB Cloud. Additionally, you can try out TiDB Cloud features on [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start).

<table><thead>
  <tr>
    <th>Category</th>
    <th>Feature</th>
    <th style="text-align:center;">Starter</th>
    <th style="text-align:center;">Essential</th>
    <th style="text-align:center;">Dedicated</th>
  </tr></thead>
<tbody>
  <tr>
    <td>Basic </td>
    <td>TiFlash</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2">Data import</td>
    <td>Import (using <code>IMPORT INTO</code> or TiDB Cloud console)</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Data Migration (using the TiDB Cloud console)</td>
    <td style="text-align:center;">❌<br></td>
    <td style="text-align:center;">✅ <br/>(Private preview)</td>
    <td style="text-align:center;">✅<br></td>
  </tr>
  <tr>
    <td rowspan="2">Data export<br></td>
    <td>Export (using the TiDB Cloud console)<br></td>
    <td style="text-align:center;">✅ <br/>(Public preview)</td>
    <td style="text-align:center;">✅ <br/>(Public preview)</td>
    <td style="text-align:center;">❌</td>
  </tr>
  <tr>
    <td>Changefeed<br></td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅ <br/>(Private preview)</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="4">Backup &amp; restore<br></td>
    <td>Automatic backup</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Dual region backup</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Manual backup</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Point-in-time recovery (PITR)</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Storage</td>
    <td>Dual disk</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2">Observability<br></td>
    <td>Alerting</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Third-party integrations</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2">High availability<br></td>
    <td>Failover (cross-AZ)</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Recovery Group (cross region)</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2">Resource allocation</td>
    <td>Node group</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Resource control</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="7">Security<br></td>
    <td>Private endpoint</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>VPC peering</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Database audit logging</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅ <br/>(Private preview)</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Console audit logging</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Customer-Managed Encryption Key (CMEK)</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Log redaction</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Dual-layer encryption</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="3">AI &amp; Development<br></td>
    <td>Vector search</td>
    <td style="text-align:center;">✅ <br/>(Public preview)</td>
    <td style="text-align:center;">✅ <br/>(Public preview)</td>
    <td style="text-align:center;">✅ <br/>(Public preview)</td>
  </tr>
  <tr>
    <td>Data branch</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">❌</td>
  </tr>
  <tr>
    <td>SQL editor</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
  </tr>
  <tr>
    <td rowspan="4">Cloud and regions<br></td>
    <td>AWS</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Alibaba Cloud</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">❌</td>
  </tr>
  <tr>
    <td>Azure</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Google Cloud</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
</tbody></table>