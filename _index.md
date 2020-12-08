---
title: TiDB Introduction
summary: Learn how to quickly start a TiDB cluster.
aliases: ['/docs/v2.1/']
---

# TiDB Introduction

[TiDB](https://github.com/pingcap/tidb) ("Ti" stands for Titanium) is an open-source NewSQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. It is MySQL compatible and features horizontal scalability, strong consistency, and high availability.

TiDB can be deployed on-premise or in-cloud. The following deployment options are officially supported by PingCAP:

- [Ansible Deployment](/online-deployment-using-ansible.md): This guide describes how to deploy TiDB using TiDB Ansible. It is strongly recommended for production deployment.
- [Ansible Offline Deployment](/offline-deployment-using-ansible.md): If your environment has no access to the internet, you can follow this guide to see how to deploy a TiDB cluster offline using TiDB Ansible.
- [Docker Deployment](/test-deployment-using-docker.md): This guide describes how to deploy TiDB using Docker.
- [Binary Tarball Deployment](/production-deployment-from-binary-tarball.md): This guide describes how to deploy TiDB from a binary tarball in production. Guides for [development](/deploy-tidb-from-binary.md) and [testing](/test-deployment-from-binary-tarball.md) environments are also available.

## Community Provided Blog Posts & Tutorials

The following list collects deployment guides and tutorials from the community. The content is subject to change by the contributors.

- [How To Spin Up an HTAP Database in 5 Minutes with TiDB + TiSpark](https://pingcap.com/blog/how_to_spin_up_an_htap_database_in_5_minutes_with_tidb_tispark/)
- [Developer install guide (single machine)](http://www.tocker.ca/this-blog-now-powered-by-wordpress-tidb.html)
- [TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/)

_Your contribution is also welcome! Feel free to open a [pull request](https://github.com/pingcap/docs/blob/release-2.1/overview.md) to add additional links._

## Source Code

Source code for [all components of the TiDB platform](https://github.com/pingcap) is available on GitHub.

<<<<<<< HEAD
- [TiDB](https://github.com/pingcap/tidb)
- [TiKV](https://github.com/tikv/tikv)
- [PD](https://github.com/pingcap/pd)
- [TiSpark](https://github.com/pingcap/tispark)
- [TiDB Operator](https://github.com/pingcap/tidb-operator)
=======
- [Hardware and Software Requirements](/hardware-and-software-requirements.md)
- [Check Environment and Configuration](/check-before-deployment.md)
- [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md)
- [Use TiFlash for Analytical Processing](/tiflash/tiflash-overview.md)
- [Deploy TiDB in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable)

</NavColumn>

<NavColumn>
<ColumnTitle>Migrate Data</ColumnTitle>

- [Migration Overview](/migration-overview.md)
- [Migrate from Aurora MySQL Database](/migrate-from-aurora-mysql-database.md)
- [Migrate from CSV Files](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)
- [Migrate from MySQL SQL Files](/migrate-from-mysql-dumpling-files.md)

</NavColumn>

<NavColumn>
<ColumnTitle>Maintain</ColumnTitle>

- [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md)
- [Scale TiDB Using TiUP](/scale-tidb-using-tiup.md)
- [Back up and Restore Data](/br/backup-and-restore-tool.md)
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
>>>>>>> de4cd64d... monitoring: document MetricsTool (Export Grafana Snapshots) (#4302)
