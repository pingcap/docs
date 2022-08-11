---
title: TiDB Cloud Introduction
summary: Learn about TiDB Cloud and its architecture.
category: intro
---

# TiDB Cloud Introduction

[TiDB Cloud](https://en.pingcap.com/tidb-cloud/) is a fully-managed Database-as-a-Service (DBaaS) that brings [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source Hybrid Transactional and Analytical Processing (HTAP) database, to your cloud, and lets you focus on your applications, not the complexities of your database. You can run TiDB clusters on Google Cloud Platform (GCP) and Amazon Web Services (AWS).

## Why TiDB Cloud

TiDB Cloud allows users with no training to handle complex tasks such as infrastructure management and cluster deployment. You will also get the massive scale and resiliency of TiDB databases in a fully managed Database as a Service (DBaaS), as well as:

- **Fully-Managed TiDB Service**

    Deploy, scale, monitor, and manage TiDB clusters in just a few clicks, through an easy-to-use web-based management platform.

- **Real-Time Analytics**

    Run real-time analytical queries with our Hybrid Transactional and Analytical Processing (HTAP) capabilities.

- **Fast and Customized Scaling**

    Elastically and transparently scale to hundreds of nodes for critical workloads without changing business logic. And you can scale your performance and storage nodes separately to custom tailor to your business needs.

- **High Availability and Reliability**

    Data is replicated across multiple Availability Zones and backed up daily to ensure business continuity for mission-critical applications.

- **High Concurrency**

    Allow thousands of users to simultaneously query your data without losing performance standards.

- **MySQL Compatibility**

    Increase productivity and shorten time-to-market for your applications without the need to rewrite your SQL code.

- **Enterprise Grade Security**

    Secure your data in dedicated networks and machines, with support for encryption both in-flight and at-rest. TiDB Cloud is SOC 2 Type 2 certified.

- **World-Class Support**

    Get the same world-class support through our support portal, email, chat, or video conferencing.

- **Simple Pricing Plans**

    Pay only for what you use, with transparent and upfront pricing with no hidden fees.

## Architecture

![TiDB Cloud architecture](/media/tidb-cloud/tidb-cloud-architecture.png)

- TiDB VPC (Virtual Private Cloud)

    For each TiDB Cloud cluster, all TiDB nodes and auxiliary nodes, including TiDB Operator nodes, logging nodes, and so on, are deployed in an independent VPC.

- TiDB Cloud Central Services

    Central Services, including billing, alerts, meta storage, dashboard UI, are deployed independently. You can access the dashboard UI to operate the TiDB cluster via the internet.

- Your VPC

    You can connect to your TiDB cluster via a VPC peering connection. Refer to [Set up VPC Peering Connection](/tidb-cloud/set-up-vpc-peering-connections.md) for details.
