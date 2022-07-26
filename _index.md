---
title: TiDB Introduction
summary: Learn about the NewSQL database TiDB that supports HTAP workloads.
aliases: ['/docs/dev/','/docs/dev/adopters/','/tidb/dev/adopters']
---

# TiDB Introduction

[TiDB](https://github.com/pingcap/tidb) (/’taɪdiːbi:/, "Ti" stands for Titanium) is an open-source, distributed, NewSQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. It is MySQL compatible and features horizontal scalability, strong consistency, and high availability. TiDB can be deployed on-premise or in-cloud.

Designed for the cloud, TiDB provides flexible scalability, reliability and security on the cloud platform. Users can elastically scale TiDB to meet the requirements of their changing workloads. [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/tidb-operator-overview) helps manage TiDB on Kubernetes and automates operating tasks, which makes TiDB easier to deploy on any cloud that provides managed Kubernetes. [TiDB Cloud](https://pingcap.com/tidb-cloud/), the fully-managed TiDB service, is the easiest, most economical, and most resilient way to unlock the full power of [TiDB in the cloud](https://docs.pingcap.com/tidbcloud/), allowing you to deploy and run TiDB clusters with just a few clicks.

<NavColumns>
<NavColumn>
<ColumnTitle>About TiDB</ColumnTitle>

- [TiDB Introduction](/overview.md)
- [Basic Features](/basic-features.md)
- [TiDB 6.1 Release Notes](/releases/release-6.1.0.md)
- [TiDB Release Timeline](/releases/release-timeline.md)
- [Compatibility with MySQL](/mysql-compatibility.md)
- [Usage Limitations](/tidb-limitations.md)

</NavColumn>

<NavColumn>
<ColumnTitle>Quick Start</ColumnTitle>

- [Quick Start with TiDB](/quick-start-with-tidb.md)
- [Quick Start with HTAP](/quick-start-with-htap.md)
- [Explore SQL with TiDB](/basic-sql-operations.md)
- [Explore HTAP](/explore-htap.md)

</NavColumn>

<NavColumn>
<ColumnTitle>Deploy and Use</ColumnTitle>

- [Hardware and Software Requirements](/hardware-and-software-requirements.md)
- [Check Environment and Configuration](/check-before-deployment.md)
- [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md)
- [Use TiFlash for Analytical Processing](/tiflash/tiflash-overview.md)
- [Deploy TiDB in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable)

</NavColumn>

<NavColumn>
<ColumnTitle>Migrate Data</ColumnTitle>

- [Migration Overview](/migration-overview.md)
- [Migrate Data from CSV Files to TiDB](/migrate-from-csv-files-to-tidb.md)
- [Migrate Data from SQL Files to TiDB](/migrate-from-sql-files-to-tidb.md)
- [Migrate Data from Amazon Aurora to TiDB](/migrate-aurora-to-tidb.md)

</NavColumn>

<NavColumn>
<ColumnTitle>Maintain</ColumnTitle>

- [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md)
- [Scale TiDB Using TiUP](/scale-tidb-using-tiup.md)
- [Back up and Restore Data](/br/backup-and-restore-overview.md)
- [Deploy and Manage TiCDC](/ticdc/manage-ticdc.md)
- [Maintain TiDB Using TiUP](/maintain-tidb-using-tiup.md)
- [Maintain TiFlash](/tiflash/maintain-tiflash.md)

</NavColumn>

<NavColumn>
<ColumnTitle>Monitor and Alert</ColumnTitle>

- [Monitoring Framework](/tidb-monitoring-framework.md)
- [Monitoring API](/tidb-monitoring-api.md)
- [Deploy Monitoring Services](/deploy-monitoring-services.md)
- [Export Grafana Snapshots](/exporting-grafana-snapshots.md)
- [Alert Rules and Solutions](/alert-rules.md)
- [TiFlash Alert Rules and Solutions](/tiflash/tiflash-alert-rules.md)

</NavColumn>

<NavColumn>
<ColumnTitle>Troubleshoot</ColumnTitle>

- [TiDB Troubleshooting Map](/tidb-troubleshooting-map.md)
- [Identify Slow Queries](/identify-slow-queries.md)
- [Analyze Slow Queries](/analyze-slow-queries.md)
- [SQL Diagnostics](/information-schema/information-schema-sql-diagnostics.md)
- [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md)
- [Troubleshoot the TiDB Cluster](/troubleshoot-tidb-cluster.md)
- [Troubleshoot TiCDC](/ticdc/troubleshoot-ticdc.md)
- [Troubleshoot TiFlash](/tiflash/troubleshoot-tiflash.md)

</NavColumn>

<NavColumn>
<ColumnTitle>Reference</ColumnTitle>

- [TiDB Architecture](/tidb-architecture.md)
- [Key Monitoring Metrics](/grafana-overview-dashboard.md)
- [Enable TLS](/enable-tls-between-clients-and-servers.md)
- [Privilege Management](/privilege-management.md)
- [Role-Based Access Control](/role-based-access-control.md)
- [Certificate-Based Authentication](/certificate-authentication.md)

</NavColumn>

<NavColumn>
<ColumnTitle>FAQs</ColumnTitle>

- [Product FAQs](/faq/tidb-faq.md)
- [High Availability FAQs](/faq/high-availability-faq.md)
- [SQL FAQs](/faq/sql-faq.md)
- [Deploy and Maintain FAQs](/faq/deploy-and-maintain-faq.md)
- [Upgrade and After Upgrade FAQs](/faq/upgrade-faq.md)
- [Migration FAQs](/faq/migration-tidb-faq.md)

</NavColumn>
</NavColumns>
