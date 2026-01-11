---
title: Features
summary: Learn about feature support status for different TiDB Cloud plans.
---

# Features

This document lists the feature support status for different TiDB Cloud plans, including {{{ .starter }}}, Essential, and Dedicated.

> **Tip:**
>
> [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) is the best way to get started with TiDB Cloud. Additionally, you can try out TiDB Cloud features on [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start).

- ✅: The feature is generally available or public preview.
- 🔒: The feature is private preveiw.
- 🚧: The feature is under development.
- ❌: The feature is currently not available.

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
    <td rowspan="4" style="background-color: white;">Basics</td>
    <td>Scalable Transaction Processing</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Analytical Processing</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Vector storage & search</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
  </tr>
  <tr>
    <td>API</td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
  </tr>
  <tr>
    <td rowspan="2" style="background-color: white;">Develop friendly</td>
    <td>Data branch</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>SQL editor</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td rowspan="7" style="background-color: white;">Cluster management</td>
    <td>Pay as you use</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center;">❌</td>
  </tr>
  <tr>
    <td>Auto scale with workload</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center;">❌</td>
  </tr>
  <tr>
    <td>Manual modify cluster</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Password setting</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Pause & resume</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>System maintenance window</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Backup file recycle bin</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="4" style="background-color: white;">Data process</td>
    <td>Data import via CSV, Parquet, and SQL files to TiDB Cloud</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Data migration from MySQL-compatible databases into TiDB Cloud</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">🔒 <br/><span style="font-size: 14px; white-space: nowrap;">(Private preview)</span></td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Data export via CSV, Parquet, and SQL files to local or object storages</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>Changefeed allows you to replicate change data to Kafka or other MySQL-compatible databases</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">(Public preview)</span></td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="5" style="background-color: white;">Backup &amp; restore</td>
    <td>Automatic backup</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Manual backup</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Dual region backup</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Point-in-time recovery (PITR)</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Restore</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="7" style="background-color: white;">Observability</td>
    <td>Built-in metrics</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Alerting</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">🚧</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>SQL Statement Statistic</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Slow Query Log</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Top SQL</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Events</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Third-party integrations, such as Datadog, Promtheus, New Relic</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="1" style="background-color: white;">High availability</td>
    <td>Failover (cross-AZ)</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2" style="background-color: white;">Resource allocation</td>
    <td>Node group</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Resource control</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="3" style="background-color: white;">Network connection</td>
    <td>Private endpoint</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Public endpoint</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center; font-size: 14px;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>VPC peering</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="6" style="background-color: white;">Security</td>
    <td>Database audit logging</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">🔒 <br/><span style="font-size: 14px; white-space: nowrap;">(Private preview)</span></td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Console audit logging</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Log redaction</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>CMEK</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Dual-layer encryption</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>IAM, including email and pwd login, standard SSO, and organization SSO.</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="4" style="background-color: white;">Cloud and regions</td>
    <td>AWS</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Alibaba Cloud</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>Azure</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Google Cloud</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
</tbody></table>

> **Tip:**
>
> To request a feature in private preview, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in the feature name in the **Description** field and click **Submit**.