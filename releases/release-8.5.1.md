---
title: TiDB 8.5.1 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 8.5.1.
---

# TiDB 8.5.1 Release Notes

Release date: January xx, 2025

TiDB version: 8.5.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## Operating system and platform requirement changes

Starting from v8.5.1, TiDB resumes the support for CentOS Linux 7. If you plan to deploy TiDB v8.5 or upgrade your cluster to v8.5, ensure you use TiDB v8.5.1 or a later version.

- According to [CentOS Linux EOL](https://www.centos.org/centos-linux-eol/), the upstream support for CentOS Linux 7 ends on June 30, 2024. In v8.4.0 DMR and v8.5.0, TiDB temporarily suspends the support for CentOS 7 and recommends you to use Rocky Linux 9.1 or later. Upgrading a TiDB cluster on CentOS 7 to v8.4.0 or v8.5.0 will cause the risk of cluster unavailability.

- Although TiDB v8.5.1 and later versions resume the support for CentOS Linux 7, due to its EOL status, it is strongly recommended that you review the [official announcements and security guidance](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol) for CentOS Linux 7 and consider migrating to a supported operating system, such as Rocky Linux 9.1 or later.
