---
title: TiDB Cloud Roadmap
summary: Learn about TiDB Cloud's roadmap for the next few months. See the new features or improvements in advance, follow the progress, learn about the key milestones on the way.
---

# TiDB Cloud Roadmap

The TiDB Cloud roadmap brings you what's coming in the near future, so you can see the new features or improvements in advance, follow the progress, and learn about the key milestones on the way. In the course of development, this roadmap is subject to change based on user needs, feedback, and our assessment.

> **Safe harbor statement:**
>
> Any unreleased features discussed or referenced in our documents, roadmaps, blogs, websites, press releases, or public statements that are not currently available ("unreleased features") are subject to change at our discretion and may not be delivered as planned or at all. Customers acknowledge that purchase decisions are solely based on features and functions that are currently available, and that PingCAP is not obliged to deliver aforementioned unreleased features as part of the contractual agreement unless otherwise stated.

## Developer experience and enterprise-grade features

| Scenario | Feature | Description |
|---|---|---|
| Developer experience | Load sample datasets manually. | Support loading sample datasets into a cluster. You can use this data to quickly get started with testing the features of TiDB Cloud. |
| UI experience | Provide a more convenient feedback channel. | Users can quickly get help with and give feedback on the product. |
| Cloud provider marketplace | Improve the user experience from AWS Marketplace and GCP Marketplace. | Improve the user journey and experience of users who sign up from AWS Marketplace and GCP Marketplace. |
| Enterprise-grade features | Manage multiple organizations. | Support managing multiple organizations. A user can create and join more than one organization. |
| UI experience | Add left navigation. | Present the TiDB Cloud console in the structure of organizations, projects, and users to simplify the layout logic and improve user experience. |
| Developer experience | Add SQL Editor. | Write and run SQL queries, and view the results in the TiDB console. |
| Enterprise-grade features | Support hierarchical user roles and permissions. | Support role-based access control (RBAC) for the TiDB Cloud console. You can manage user permissions in a fine-grained manner, such as by cluster, billing, and member. |

## TiDB kernel

<table>
<thead>
  <tr>
    <th>Scenario</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="2">Support JSON</td>
    <td>Support JSON function.</td>
    <td>In business scenarios that require flexible schema definitions (such as SaaS, Web3, and gaming), the application can use JSON to store information for ODS, transaction indicators, commodities, game characters, and props.</td>
  </tr>
  <tr>
    <td><ul><li>Support expression indexes.</li><li>Support generated columns.</li></ul></td>
    <td>Provides query acceleration for specific field indexes in JSON scenarios.</td>
  </tr>
  <tr>
    <td>Flashback</td>
    <td>Support cluster-level flashback.</td>
    <td>In game rollback scenarios, the flashback can be used to achieve a fast rollback of the current cluster. This solves the common problems in the gaming industry such as version errors and bugs.</td>
  </tr>
  <tr>
    <td>TiFlash result write-back (supports <code>INSERT INTO SELECT</code>)</td>
    <td><ul><li>Easily write analysis results in TiFlash back to TiDB.</li><li>Provide complete ACID transactions, more convenient and reliable than general ETL solutions.</li><li>Set a hard limit on the threshold of intermediate result size, and report an error if the threshold is exceeded.</li><li>Support fully distributed transactions, and remove or relax the limit on the intermediate result size.</li></ul></td>
    <td>These features combined enable a way to materialize intermediate results. The analysis results can be easily reused, which reduces unnecessary ad-hoc queries, improves the performance of BI and other applications (by pulling results directly) and reduces system load (by avoiding duplicated computation), thereby improving the overall data pipeline efficiency and reducing costs. It will make TiFlash an online service.</td>
  </tr>
  <tr>
    <td>Time to live (TTL)</td>
    <td>Support automatically deleting expired table data based on custom rules.</td>
    <td>This feature enables automatic data cleanup in limited data archiving scenarios.</td>
  </tr>
  <tr>
    <td>Multi-value Index</td>
    <td>Support array index.</td>
    <td>Array is one of the commonly used data types in JSON scenarios. For inclusive queries in arrays, multi-value indexes can efficiently improve the query speed. </td>
  </tr>
  <tr>
    <td>TiFlash kernel optimization</td>
    <td><ul><li>FastScan provides weak consistency but faster table scan capability.</li><li>Further optimize the join order, shuffle, and exchange algorithms to improve computing efficiency and boost performance for complex queries.</li><li>Add a fine-grained data sharding mechanism to optimize the <code>COUNT(DISTINCT)</code> function and high cardinality aggregation.</li></ul></td>
    <td>Improve the basic computing capability of TiFlash, and optimize the performance and reliability of the underlying algorithms of the columnar storage and MPP engine.</td>
  </tr>
  <tr>
    <td>TiDB proxy</td>
    <td>Implement automatic load balancing so that upgrading a cluster or modifying configurations does not affect the application. After scaling out or scaling in the cluster, the application can automatically rebalance the connection without reconnecting.</td>
    <td>In scenarios such as upgrades and configuration changes, TiDB proxy is more business-friendly.</td>
  </tr>
</tbody>
</table>

## Diagnosis and maintenance

<table>
<thead>
  <tr>
    <th>Scenario</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Self-service cluster analysis and diagnosis using reports</td>
    <td><ul><li>Cluster health report.</li><li>Cluster status comparison report.</li><li>Cluster performance analysis report.</li><li>Cluster system check report.</li></ul></td>
    <td><ul><li>Provide diagnosis and analysis reports for several different usage scenarios.</li><li>Locate cluster failures for some scenarios and provide recommended solutions.</li><li>Provide cluster key status summary for some scenarios.</li></ul></td>
  </tr>
  <tr>
    <td>SQL tuning for HTAP workloads</td>
    <td><ul><li>Provide SQL execution information from the perspective of applications.</li><li>Provide suggestions on optimizing SQL for TiFlash and TiKV in HTAP workloads.</li></ul></td>
    <td><ul><li>Provide a dashboard that displays a SQL execution overview from the perspective of applications in HTAP workloads.</li><li>For one or several HTAP scenarios, provide suggestions on SQL optimization.</li></ul></td>
  </tr>
  <tr>
    <td>Cluster diagnosis data accessibility </td>
    <td><ul><li>Access diagnosis data online in real time.</li><li>Access diagnosis data offline.</li><li>Build logic for data reconstruction.</li></ul></td>
    <td><ul><li>Integrate with various monitoring and diagnosis systems to improve the real-time data access capability.</li><li>Provide offline data access for large-scale diagnosis, analysis, and tuning.</li><li>Improve data stability and build logic for data reconstruction.</li></ul></td>
  </tr>
  <tr>
    <td>TiDB Cloud service tracing</td>
    <td>Build the monitoring links for each component of TiDB Cloud service.</td>
    <td><ul><li>Build the tracing links for each component of TiDB Cloud service in user scenarios.</li><li>Provide assessment on service availability from the perspective of users.</li></ul></td>
  </tr>
</tbody>
</table>

## Data backup and migration

<table>
<thead>
  <tr>
    <th>Scenario</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Data replication to Kafka via TiCDC</td>
    <td>Reduce TiCDC replication latency in planned offline scenarios.</td>
    <td>When TiKV, TiDB, PD, or TiCDC nodes are offline in a planned maintenance window, the replication latency of TiCDC can be reduced to less than 10 seconds.</td>
  </tr>
  <tr>
    <td>Data disaster recovery</td>
    <td>TiCDC provides cross-region disaster recovery on the cloud.</td>
    <td>TiCDC provides disaster recovery that ensures data eventual consistency with lower cost on TiDB Cloud.</td>
  </tr>
  <tr>
    <td>Point-in-time recovery (PITR)</td>
    <td>Support PITR on the cloud.</td>
    <td>Support cluster-level PITR on the cloud.</td>
  </tr>
  <tr>
    <td>Backup and restore</td>
    <td>Backup and restore service on the cloud based on EBS snapshots.</td>
    <td>Backup and restore service on the cloud based on AWS EBS or GCP persistent disk snapshots.</td>
  </tr>
  <tr>
    <td rowspan="2">Online data migration</td>
    <td>Support full data migration from Amazon Relational Database Service (RDS).</td>
    <td>Full data migration from RDS to TiDB Cloud</td>
  </tr>
  <tr>
    <td>Support incremental data migration from RDS.</td>
    <td>Full and incremental data migration from MySQL services such as Amazon RDS and Aurora to TiDB Cloud.</td>
  </tr>
</tbody>
</table>

## Security

<table>
<thead>
  <tr>
    <th>Scenario</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Enterprise-grade SSO support</td>
    <td>Support quick configurations of SSO to TiDB Cloud via Okta.</td>
    <td>Provide a fast sign-in method for enterprise users. </td>
  </tr>
  <tr>
    <td>Encrypted backup and restore</td>
    <td>Support encrypted backup and restore.</td>
    <td>Provide a method to securely back up and restore a database.</td>
  </tr>
</tbody>
</table>
