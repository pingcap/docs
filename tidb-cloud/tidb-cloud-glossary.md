---
title: TiDB Cloud Glossary
summary: Learn the terms used in TiDB Cloud.
category: glossary
aliases: ['/tidbcloud/glossary']
---

# TiDB Cloud Glossary

## A

### ACID

ACID refers to the four key properties of a transaction: atomicity, consistency, isolation, and durability. Each of these properties is described below.

- **Atomicity** means that either all the changes of an operation are performed, or none of them are. TiDB ensures the atomicity of the [TiDB Region](#region) that stores the Primary Key to achieve the atomicity of transactions.

- **Consistency** means that transactions always bring the database from one consistent state to another. In TiDB, data consistency is ensured before writing data to the memory.

- **Isolation** means that a transaction in process is invisible to other transactions until it completes. This allows concurrent transactions to read and write data without sacrificing consistency. TiDB currently supports the isolation level of `REPEATABLE READ`.

- **Durability** means that once a transaction is committed, it remains committed even in the event of a system failure. TiKV uses persistent storage to ensure durability.

## C

### Chat2Query

Chat2Query is an AI-powered feature integrated into SQL Editor that assists users in generating, debugging, or rewriting SQL queries using natural language instructions. For more information, see [Explore your data with AI-assisted SQL Editor](/tidb-cloud/explore-data-with-chat2query.md).

In addition, TiDB Cloud provides a Chat2Query API for TiDB Cloud Serverless clusters. After it is enabled, TiDB Cloud will automatically create a system Data App called **Chat2Query** and a Chat2Data endpoint in Data Service. You can call this endpoint to let AI generate and execute SQL statements by providing instructions. For more information, see [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md).

### Credit

TiDB Cloud offers a certain number of credits for Proof of Concept (PoC) users. One credit is equivalent to one U.S. dollar. You can use credits to pay TiDB cluster fees before the credits become expired.

## D

### Data App

A Data App in [Data Service (beta)](#data-service) is a collection of endpoints that you can use to access data for a specific application. You can configure authorization settings using API keys to restrict access to endpoints in a Data App.

For more information, see [Manage a Data App](/tidb-cloud/data-service-manage-data-app.md).

### Data Service

Data Service (beta) enables you to access TiDB Cloud data via an HTTPS request using a custom API [endpoint](#endpoint). This feature uses a serverless architecture to handle computing resources and elastic scaling, so you can focus on the query logic in endpoints without worrying about infrastructure or maintenance costs.

For more information, see [Data Service Overview](/tidb-cloud/data-service-overview.md).

### Direct Customer

A direct customer is an end customer who purchases TiDB Cloud and pays invoices directly from PingCAP. This is distinguished from an [MSP customer](#msp-customer).

## E

### Endpoint

An endpoint in Data Service is a web API that you can customize to execute SQL statements. You can specify parameters for your SQL statements, such as the value used in the `WHERE` clause. When a client calls an endpoint and provides values for the parameters in a request URL, the endpoint executes the corresponding SQL statement with the provided parameters and returns the results as part of the HTTP response.

For more information, see [Manage an endpoint](/tidb-cloud/data-service-manage-endpoint.md).

## F

### Full-text search

Unlike [Vector Search](/vector-search/vector-search-overview.md), which focuses on semantic similarity, full-text search lets you retrieve documents for exact keywords. In Retrieval-Augmented Generation (RAG) scenarios, you can use full-text search together with vector search to improve the retrieval quality.

For more information, see [Full-Text Search with SQL](/tidb-cloud/vector-search-full-text-search-sql.md) and [Full-Text Search with Python](/tidb-cloud/vector-search-full-text-search-python.md).

## M

### member

A user that has been invited to an organization, with access to the organization and the clusters of this organization.

### MPP

Starting from v5.0, TiDB introduces Massively Parallel Processing (MPP) architecture through TiFlash nodes, which shares the execution workloads of large join queries among TiFlash nodes. When the MPP mode is enabled, TiDB, based on cost, determines whether to use the MPP framework to perform the calculation. In the MPP mode, the join keys are redistributed through the Exchange operation while being calculated, which distributes the calculation pressure to each TiFlash node and speeds up the calculation. For more information, see [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md).

### MSP Customer

A managed service provider (MSP) customer is an end customer who purchases TiDB Cloud and pays invoices through the MSP channel. This is distinguished from a [direct customer](#direct-customer).

### Managed Service Provider (MSP)

A managed service provider (MSP) is a partner who resells TiDB Cloud and provides value-added services, including but not limited to TiDB Cloud organization management, billing services, and technical support.

## N

### node

Refers to either a data instance (TiKV) or a compute instance (TiDB) or an analytical instance (TiFlash).

## O

### organization

An entity that you create to manage your TiDB Cloud accounts, including a management account with any number of multiple member accounts.

### organization members

Organization members are users who are invited by the organization owner or project owner to join an organization. Organization members can view members of the organization and can be invited to projects within the organization.

## P

### policy

A document that defines permissions applying to a role, user, or organization, such as the access to specific actions or resources.

### project

Based on the projects created by the organization, resources such as personnel, instances, and networks can be managed separately according to projects, and resources between projects do not interfere with each other.

### project members

Project members are users who are invited to join one or more projects of the organization. Project members can manage clusters, network access, backups, and other resources.

## R

### Recycle Bin

The place where the data of deleted clusters with valid backups is stored. Once a backed-up TiDB Cloud Dedicated cluster is deleted, the existing backup files of the cluster are moved to the recycle bin. For backup files from automatic backups, the recycle bin will retain them for a specified period. You can configure the backup retention in **Backup Setting**, and the default is 7 days. For backup files from manual backups, there is no expiration date. To avoid data loss, remember to restore the data to a new cluster in time. Note that if a cluster **has no backup**, the deleted cluster will not be displayed here.

### region

- TiDB Cloud region

    A geographical area in which a TiDB Cloud cluster is deployed. A TiDB Cloud region comprises of at least 3 Availability Zones, and the cluster is deployed across these zones.

- TiDB Region

    The basic unit of data in TiDB. TiKV divides the Key-Value space into a series of consecutive Key segments, and each segment is called a Region. The default size limit for each Region is 96 MB and can be configured.

### replica

A separate database that can be located in the same or different region and contains the same data. A replica is often used for disaster recovery purposes or to improve performance.

### Replication Capacity Unit

The replication of changefeed is charged according to the computing resources, which is the TiCDC replication capacity unit.

### Request Unit

A Request Unit (RU) is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified. For more information, see [TiDB Cloud Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

## S

### Spending limit

Spending limit refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that enables you to set a budget for your TiDB Cloud Serverless clusters. For [scalable clusters](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan), the spending limit must be set to a minimum of $0.01. Also, the scalable cluster can have a free quota if it meets the qualifications. The scalable cluster with a free quota will consume the free quota first.

## T

### TiDB cluster

The collection of [TiDB](https://docs.pingcap.com/tidb/stable/tidb-computing), [TiKV](https://docs.pingcap.com/tidb/stable/tidb-storage), [the Placement Driver](https://docs.pingcap.com/tidb/stable/tidb-scheduling) (PD), and [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) nodes that form a functional working database.

### TiDB node

The computing node that aggregates data from queries returned from transactional or analytical stores. Increasing the number of TiDB nodes will increase the number of concurrent queries that the cluster can handle.

### TiFlash node

The analytical storage node that replicates data from TiKV in real time and supports real-time analytical workloads.

### TiKV node

The storage node that stores the online transactional processing (OLTP) data. It is scaled in multiples of 3 nodes (for example, 3, 6, 9) for high availability, with two nodes acting as replicas. Increasing the number of TiKV nodes will increase the total throughput.

### traffic filter

A list of IP addresses and Classless Inter-Domain Routing (CIDR) addresses that are allowed to access the TiDB Cloud cluster via a SQL client. The traffic filter is empty by default.

## V

### Vector search

[Vector search](/vector-search/vector-search-overview.md) is a search method that prioritizes the meaning of your data to deliver relevant results. Unlike traditional full-text search, which relies on exact keyword matching and word frequency, vector search converts various data types (such as text, images, or audio) into high-dimensional vectors and queries based on the similarity between these vectors. This search method captures the semantic meaning and contextual information of the data, leading to a more precise understanding of user intent. Even when the search terms do not exactly match the content in the database, vector search can still provide results that align with the user's intent by analyzing the semantics of the data.

### Virtual Private Cloud

A logically isolated virtual network partition that provides managed networking service for your resources.

### VPC

Short for Virtual Private Cloud.

### VPC peering

Enables you to connect Virtual Private Cloud ([VPC](#vpc)) networks so that workloads in different VPC networks can communicate privately.

### VPC peering connection

A networking connection between two Virtual Private Clouds (VPCs) that enables you to route traffic between them using private IP addresses and helps you to facilitate data transfer.
