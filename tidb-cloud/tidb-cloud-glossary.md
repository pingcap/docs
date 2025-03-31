---
title: TiDB Cloud Glossary
summary: Learn the terms used in TiDB Cloud.
category: glossary
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

### Credit

TiDB Cloud offers a certain number of credits for Proof of Concept (PoC) users. One credit is equivalent to one U.S. dollar. You can use credits to pay TiDB cluster fees before the credits become expired.

## D

### Direct Customer

A direct customer is an end customer who purchases TiDB Cloud and pays invoices directly from PingCAP. This is distinguished from an [MSP customer](#msp-customer).

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

A Request Unit (RU) is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified. For more information, see [TiDB Cloud Starter Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

## S

### Spending limit

Spending limit refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that enables you to set a budget for your [TiDB Cloud Starter clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-starter). If the spending limit is set to 0, the cluster remains in the free tier. If the spending limit is greater than 0, you need to add a credit card.

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

### Virtual Private Cloud

A logically isolated virtual network partition that provides managed networking service for your resources.

### VPC

Short for Virtual Private Cloud.

### VPC peering

Enables you to connect Virtual Private Cloud ([VPC](#vpc)) networks so that workloads in different VPC networks can communicate privately.

### VPC peering connection

A networking connection between two Virtual Private Clouds (VPCs) that enables you to route traffic between them using private IP addresses and helps you to facilitate data transfer.
