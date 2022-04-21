---
title: TiDB Cloud Introduction
summary: Learn about TiDB Cloud and its architecture.
category: intro
---

# TiDB Cloud Introduction

[TiDB Cloud](https://pingcap.com/products/tidbcloud) is a fully-managed Database-as-a-Service (DBaaS) that brings everything great about TiDB to your cloud, and lets you focus on your applications, not the complexities of your database.

## Why TiDB Cloud

- Operational Analytics

    Support massive-scale, mission-critical OLTP and real-time analytics workloads right out of the box.

- Multi-Cloud Support

    Stay flexible without cloud vendor lock-in. TiDB Cloud is currently available on AWS and GCP.

- Productivity Boosting

    Boost your productivity with easy deployment, operations, and monitoring on TiDB Cloud in just a few clicks.

- Enterprise Grade Security

    Secure your data in dedicated networks and machines, with support for encryption both in flight and at rest.

- Highly Resilient

    Data is replicated across multiple Availability Zones and backed up daily to ensure your service is always on.

- Expert Support

    We support thousands of TiDB users, and we bring that same experience to our TiDB Cloud users.

## Architecture

![TiDB Cloud architecture](/cloud/media/tidb-cloud-architecture.png)

- TiDB VPC (Virtual Private Cloud)

    For each TiDB Cloud cluster, all TiDB nodes and auxiliary nodes, including TiDB Operator nodes, logging nodes, and so on, are deployed in an independent VPC.

- TiDB Cloud Central Services

    Central Services, including billing, alerts, meta storage, dashboard UI, are deployed independently. You can access the dashboard UI to operate the TiDB Cluster cluster via the Internet.

- Your VPC

    You can connect to your TiDB cluster via a VPC peering connection. Refer to [Set up VPC Peering Connection](/cloud/set-up-vpc-peering-connections.md) for details.
