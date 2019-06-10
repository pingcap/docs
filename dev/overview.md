---
title: TiDB Introduction
summary: Learn how to quickly start a TiDB cluster.
category: introduction
aliases: ['/docs/QUICKSTART','/docs/overview/']
---

# TiDB Introduction

TiDB ("Ti" stands for Titanium) is an open-source NewSQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. It is MySQL compatible and features horizontal scalability, strong consistency, and high availability.

TiDB can be deployed on-premise or in-cloud. The following deployment options are officially supported by PingCAP:

- [Ansible Deployment](/dev/how-to/deploy/orchestrated/ansible.md): This guide describes how to deploy TiDB using Ansible. It is strongly recommended for production deployment.
- [Ansible Offline Deployment](/dev/how-to/deploy/orchestrated/offline-ansible.md): If your environment has no access to the internet, you can follow this guide to see how to deploy a TiDB cluster offline using Ansible.
- [Docker Deployment](/dev/how-to/deploy/orchestrated/docker.md): This guide describes how to deploy TiDB using Docker.
- [Docker Compose Deployment](/dev/how-to/get-started/local-cluster/install-from-docker-compose.md): This guide describes how to deploy TiDB using Docker compose. You can follow this guide to quickly deploy a TiDB cluster for testing and development on your local drive.
- [Kubernetes Deployment (beta)](/dev/how-to/get-started/local-cluster/install-from-kubernetes.md): This guide describes how to deploy TiDB on Kubernetes using [TiDB Operator](https://github.com/pingcap/tidb-operator). You can follow this guide to see how to deploy TiDB on Google Kubernetes Engine or deploy TiDB locally using Docker in Docker.
- [Binary Tarball Deployment](/dev/how-to/deploy/from-tarball/production-environment.md): This guide describes how to deploy TiDB from a binary tarball in production. Guides for [development](/dev/how-to/get-started/local-cluster/install-from-binary.md) and [testing](/dev/how-to/deploy/from-tarball/testing-environment.md) environments are also available.

## Community Provided Blog Posts & Tutorials

The following list collects deployment guides and tutorials from the community. The content is subject to change by the contributors.

- [How To Spin Up an HTAP Database in 5 Minutes with TiDB + TiSpark](https://www.pingcap.com/blog/how_to_spin_up_an_htap_database_in_5_minutes_with_tidb_tispark/)
- [Developer install guide (single machine)](http://www.tocker.ca/this-blog-now-powered-by-wordpress-tidb.html)
- [TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/)

_Your contribution is also welcome! Feel free to open a [pull request](https://github.com/pingcap/docs/edit/master/overview.md) to add additional links._

## Source Code

Source code for [all components of the TiDB platform](https://github.com/pingcap) is available on GitHub.

- [TiDB](https://github.com/pingcap/tidb)
- [TiKV](https://github.com/tikv/tikv)
- [PD](https://github.com/pingcap/pd)
- [TiSpark](https://github.com/pingcap/tispark)
- [TiDB Operator](https://github.com/pingcap/tidb-operator)
