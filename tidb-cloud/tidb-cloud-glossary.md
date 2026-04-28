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

In addition, TiDB Cloud provides a Chat2Query API for {{{ .starter }}} instances hosted on AWS. After it is enabled, TiDB Cloud will automatically create a system Data App called **Chat2Query** and a Chat2Data endpoint in Data Service. You can call this endpoint to let AI generate and execute SQL statements by providing instructions. For more information, see [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md).

### Cluster

In TiDB Cloud, a cluster is a dedicated cloud deployment that includes explicit infrastructure details such as node topology, instance types, storage configuration, and scaling model.

Among TiDB Cloud plans, only TiDB Cloud Dedicated clusters use this deployment model.

### Credit

TiDB Cloud offers a certain number of credits for Proof of Concept (PoC) users. One credit is equivalent to one U.S. dollar. You can use credits to pay fees before the credits become expired.

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

Unlike [Vector Search](/ai/concepts/vector-search-overview.md), which focuses on semantic similarity, full-text search lets you retrieve documents for exact keywords. In Retrieval-Augmented Generation (RAG) scenarios, you can use full-text search together with vector search to improve the retrieval quality.

For more information, see [Full-Text Search with SQL](/ai/guides/vector-search-full-text-search-sql.md) and [Full-Text Search with Python](/ai/guides/vector-search-full-text-search-python.md).

## M

### member

A user that has been invited to an [organization](#organization) in TiDB Cloud.

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

A top level container to manage your TiDB Cloud accounts (including a management account with any number of multiple member accounts), [projects](#project), and [resources](#tidb-cloud-resource).

### organization members

Organization members are users who are invited by the organization owner or project owner to join an organization. Organization members can view members of the organization and can be invited to projects within the organization.

## P

### policy

A document that defines permissions applying to a role, user, or organization, such as the access to specific actions or resources.

### project

In TiDB Cloud, you can use projects to group and manage your TiDB resources.

- For <CustomContent plan="starter,essential,dedicated">{{{ .starter }}} and Essential</CustomContent><CustomContent plan="premium">{{{ .starter }}}, Essential, and Premium</CustomContent> instances, projects are optional, which means you can either group these instances in a project or keep these instances at the organization level.
- For {{{ .dedicated }}} clusters, projects are required.

The function of a project varies by project type. Currently, there are three types of projects:

- **TiDB Dedicated project**: This project type is used only for {{{ .dedicated }}} clusters. It helps you manage settings for {{{ .dedicated }}} clusters separately by project, such as RBAC, networks, maintenance, alert subscriptions, and encryption access.
- **TiDB X project**: This project type is used only for TiDB X instances (<CustomContent plan="starter,essential,dedicated">{{{ .starter }}} and Essential</CustomContent><CustomContent plan="premium">{{{ .starter }}}, Essential, and Premium</CustomContent>). It helps you manage RBAC for TiDB X instances by project. A TiDB X project is the default project type when you create a project on the [**My TiDB**](https://tidbcloud.com/tidbs) page.
- **TiDB X virtual project**: This project is virtual and does not provide any management capabilities. It acts as a virtual container for TiDB X instances (<CustomContent plan="starter,essential,dedicated">{{{ .starter }}} and Essential</CustomContent><CustomContent plan="premium">{{{ .starter }}}, Essential, and Premium</CustomContent>) that do not belong to any project, so these instances can be accessed through the TiDB Cloud API by using a project ID. Each organization has a unique virtual project ID. You can get this ID from the project view on the [**My TiDB**](https://tidbcloud.com/tidbs) page.

For more information about the differences between these project types, see [Projects](/tidb-cloud/manage-user-access.md#projects).

### project members

Project members are users who are invited to join one or more projects of the organization.

## R

### Recycle Bin

The place where the data of deleted [TiDB Cloud resources](#tidb-cloud-resource) with valid backups is stored.

Once a backed-up TiDB Cloud resource is deleted, the existing backup files of it are moved to the Recycle Bin. For backup files from automatic backups, the Recycle Bin will retain them for a specified period. You can configure the backup retention in **Backup Setting**, and the default is 7 days. For backup files from manual backups, there is no expiration date. To avoid data loss, remember to restore the data to a new TiDB Cloud resource in time. Note that if a TiDB Cloud resource **has no backup**, the deleted resource will not be displayed in the Recycle Bin.

<CustomContent plan="starter,essential,dedicated">

Currently, only {{{ .dedicated }}} clusters support the Recycle Bin feature.

</CustomContent>

<CustomContent plan="premium">

Currently, only {{{ .premium }}} instances and {{{ .dedicated }}} clusters support the Recycle Bin feature.

</CustomContent>

### region

- TiDB Cloud region

    A geographical area in which a TiDB Cloud resource is deployed. A TiDB Cloud region comprises of at least 3 Availability Zones, and the cluster or instance is deployed across these zones.

- TiDB Region

    The basic unit of data in TiDB. TiKV divides the Key-Value space into a series of consecutive Key segments, and each segment is called a Region. The default size limit for each Region is 96 MB and can be configured.

### replica

A separate database that can be located in the same or different region and contains the same data. A replica is often used for disaster recovery purposes or to improve performance.

### Replication Capacity Unit (RCU)

TiDB Cloud measures the capacity of [changefeeds](/tidb-cloud/changefeed-overview.md) in TiCDC Replication Capacity Units (RCUs). When you create a changefeed, you can select an appropriate specification. The higher the RCU, the better the replication performance. You will be charged for these TiCDC changefeed RCUs. For more information, see [Changefeed Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#changefeed-cost).

### Request Capacity Unit (RCU)

For {{{ .essential }}} and {{{ .premium }}}, a Request Capacity Unit (RCU) is a unit of measure used to represent the provisioned compute capacity for your {{{ .essential }}} or {{{ .premium }}} instance. One RCU provides a fixed amount of compute resources that can process a certain number of RUs per second. The number of RCUs you provision determines the baseline performance and throughput capacity of your instance. However, the way RCUs are managed differs between {{{ .essential }}} and {{{ .premium }}}:

- {{{ .essential }}} automatically provisions RCUs based on your workload. As your QPS increases, TiDB Cloud dynamically scales up the provisioned RCUs to maintain performance. For more information, see [{{{ .essential }}} Pricing Details](https://www.pingcap.com/tidb-cloud-essential-pricing-details/).
- {{{ .premium }}} lets you specify the maximum RCU (`RCU_max`) for your workload. TiDB Cloud automatically scales capacity within the range of `0.25 * RCU_max` to `RCU_max` based on real-time demand. For more information, see [Request units and capacity in {{{ .premium }}}](/tidb-cloud/architecture-concepts.md#request-units-and-capacity-in-premium).

### Request Unit (RU)

For {{{ .starter }}}, Essential, and Premium, a Request Unit (RU) is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified. However, the billing models for these plans are different:

- {{{ .starter }}} is billed based on the total number of RUs consumed. For more information, see [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/).
- {{{ .essential }}} is billed based on the number of provisioned [Request Capacity Units (RCUs)](#request-capacity-unit-rcu). One RCU provides a fixed amount of compute resources that can process a certain number of RUs-per-second. For more information, see [{{{ .essential }}} Pricing Details](https://www.pingcap.com/tidb-cloud-essential-pricing-details/).
- {{{ .premium }}} is billed based on the actual RUs consumed by your workload. TiDB Cloud calculates the average RUs per second every minute and converts the value to [Request Capacity Units (RCUs)](#request-capacity-unit-rcu) for billing. For more information, see [Request units and capacity in {{{ .premium }}}](/tidb-cloud/architecture-concepts.md#request-units-and-capacity-in-premium).

For TiDB Cloud Dedicated and TiDB Self-Managed, a Request Unit (RU) is a resource abstraction unit that represents system resource consumption, which currently includes CPU, IOPS, and IO bandwidth metrics. It is used by the resource control feature to limit, isolate, and manage resources consumed by database requests, **not for billing purposes**. For more information, see [Use Resource Control to Achieve Resource Group Limitation and Flow Control](/tidb-resource-control-ru-groups.md).

## S

### Spending limit

[Spending limit](/tidb-cloud/manage-serverless-spend-limit.md) refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that enables you to set a budget for your {{{ .starter }}} instances. If the spending limit is set to 0, the {{{ .starter }}} instance remains free. If the spending limit is greater than 0, you need to add a credit card.

## T

### TiDB cluster

In TiDB Cloud, a cluster is a dedicated cloud deployment of TiDB that includes explicit infrastructure details such as node topology (where you can specify the number of [TiDB](/tidb-computing.md) nodes, [TiKV](/tidb-storage.md) nodes, and [TiFlash](/tiflash/tiflash-overview.md) nodes), storage configuration, and scaling model.

### TiDB node

The computing node that aggregates data from queries returned from transactional or analytical stores. Increasing the number of TiDB nodes will increase the number of concurrent queries that the {{{ .dedicated }}} cluster can handle.

### TiDB Cloud resource

A TiDB Cloud resource is a manageable TiDB Cloud deployment unit. It can be one of the following:

- A TiDB X instance (a service-oriented TiDB Cloud offering built on the [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md)), such as a <CustomContent plan="starter,essential,dedicated">{{{ .starter }}} or Essential</CustomContent><CustomContent plan="premium">{{{ .starter }}}, Essential, or Premium</CustomContent> instance
- A {{{ .dedicated }}} cluster

### TiDB X

A new distributed SQL architecture that makes cloud-native object storage the backbone of TiDB. By decoupling compute and storage, TiDB X enables TiDB to scale intelligently, adapting in real time to workload patterns, business cycles, and data characteristics.

The TiDB X architecture is now available in <CustomContent plan="starter,essential,dedicated">{{{ .starter }}} and Essential</CustomContent><CustomContent plan="premium">{{{ .starter }}}, Essential, and Premium</CustomContent>. For more information, see [Introducing TiDB X: A New Foundation for Distributed SQL in the Era of AI](https://www.pingcap.com/blog/introducing-tidb-x-a-new-foundation-distributed-sql-ai-era/) and [PingCAP Launches TiDB X and New AI Capabilities at SCaiLE Summit 2025](https://www.pingcap.com/press-release/pingcap-launches-tidb-x-new-ai-capabilities/).

### TiDB X instance

A TiDB X instance is a service-oriented TiDB Cloud offering built on the [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md). It does not require you to manage or understand the underlying cluster topology.

Among TiDB Cloud plans, <CustomContent plan="starter,essential,dedicated">{{{ .starter }}} and Essential</CustomContent><CustomContent plan="premium">{{{ .starter }}}, Essential, and Premium</CustomContent> are using the TiDB X architecture. Therefore, when "TiDB X instance" is mentioned, it refers to a <CustomContent plan="starter,essential,dedicated">{{{ .starter }}} or Essential</CustomContent><CustomContent plan="premium">{{{ .starter }}}, Essential, or Premium</CustomContent> instance.

### TiFlash node

The analytical storage node that replicates data from TiKV in real time and supports real-time analytical workloads.

### TiKV node

The storage node that stores the online transactional processing (OLTP) data. It is scaled in multiples of 3 nodes (for example, 3, 6, 9) for high availability, with two nodes acting as replicas. Increasing the number of TiKV nodes will increase the total throughput.

### traffic filter

A list of IP addresses and Classless Inter-Domain Routing (CIDR) addresses that are allowed to access the TiDB Cloud resource via a SQL client. The traffic filter is empty by default.

## V

### Vector search

[Vector search](/ai/concepts/vector-search-overview.md) is a search method that prioritizes the meaning of your data to deliver relevant results. Unlike traditional full-text search, which relies on exact keyword matching and word frequency, vector search converts various data types (such as text, images, or audio) into high-dimensional vectors and queries based on the similarity between these vectors. This search method captures the semantic meaning and contextual information of the data, leading to a more precise understanding of user intent. Even when the search terms do not exactly match the content in the database, vector search can still provide results that align with the user's intent by analyzing the semantics of the data.

### Virtual Private Cloud

A logically isolated virtual network partition that provides managed networking service for your resources.

### VPC

Short for Virtual Private Cloud.

### VPC peering

Enables you to connect Virtual Private Cloud ([VPC](#vpc)) networks so that workloads in different VPC networks can communicate privately.

### VPC peering connection

A networking connection between two Virtual Private Clouds (VPCs) that enables you to route traffic between them using private IP addresses and helps you to facilitate data transfer.
