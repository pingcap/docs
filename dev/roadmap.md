---
title: TiDB V4.0 Roadmap
summary: Learn about the v4.0 roadmap of TiDB.
category: Roadmap
aliases: ['/docs/ROADMAP/','/docs/roadmap/']
---

<!-- markdownlint-disable MD001 -->

# TiDB V4.0 Roadmap

This document describes the roadmap for TiDB development.

## TiDB

### TiDB

#### Features

* Support TiFlash Storage Engine
* Support Optimizer Trace
* Support Multi-Column Statistics
* Support TopN Statistics for Regular CM-Sketch
* Improve the Plan Cache Feature
* Support Self-adaptive SQL Engine
* Support SQL Tuning Advisor
* Support SQL Plan Management
* Transaction
    + Pessimistic Locking General Availability
    + Support Unlimited Number of Statements in a Transaction
    + Support 10 GB Transactions

#### Performance

* Improve Load CSV/Data Performance
* Improve Prepare Statement Performance
* Support Index for Generated Columns
* Optimize Some Operators of the SQL Engine
    + Improve Performance of Queries by Using Indexes to Return to the Table
    + Split Index Join to Index Merge Join and Index Hash Join
    + Radix Hash Join
    + Index Merge
    + Parallel Stream Aggregate
    + Parallel Merge Sort
    + Parallel Merge Join
    + Full Vectorized Expression Evaluation
* Indexes on Expressions
* Multi-Index Scan
* Support External Storage for Join, Aggregate, and Sort Operators
* Optimize the Execution Engine Concurrency Model
* Support New Cascades Optimizer and Cascades Planner to Increase the Optimizer Searching Space

#### Usability

* Improve the Optimizer Hint Feature
* Quickly Restore Database or Table Metadata and Data
* Dynamically Modify Configuration Items
* Automatically Terminate Idle Connections
* Continue Supporting DDL Statements in MySQL 5.7
* Refactor Log Content
* Support `admin checksum from … to …` to verify the data integrity
* Support Using Standard SQL Statements to Query the DDL History
* Support Using Standard SQL Statements to Manage Binlog
* Support Using Standard SQL Statements to Manage the Cluster
* Merge Multiple Ctrl Tools into One

#### High Availability

* Support High Service Availability with Binlog
* Support High Data Reliability with Binlog

### TiKV

#### Features

* Support Up to 200+ Nodes in a Cluster
* Fast Full Backup and Restoration
* Dynamically Split and Merge Hotspot Regions
* Fine-grained Memory Control
* Raft
    + Joint Consensus
    + Read-only Replicas

#### Performance

* Improve Scan Performance
* Dynamically Increase the Number of Worker Threads
* Flexibly Increase Read-only Replicas
* Optimize the Scheduling System to Prevent QPS Jitter

#### Usability

* Refactor Log Content

### TiFlash

#### Features

* Column-based Storage
* Replicate Data from TiKV Through Raft Learner
* Snapshot Read

### TiSpark

#### Features

* Support Batch Write
* Support Accessing TiFlash

## Data Migration

### Features

* Improve Forward Checking
* Visualized Management of Replication Rules
* Visualized Management of Replication Tasks
* Online Verification on Data Replication

### Usability

* Refactor Log Format and Content

### High Availability

* Support High Service Availability
* Support High Data Reliability

## TiDB Toolkit

### Features

* Integrate Loader into TiDB
* Integrate TiDB Lightning into TiDB

### Performance

* Support Using Multiple `lightning` and `importer` Instances to Parallel Import Data with TiDB Lightning

# TiDB Future Plan

## TiDB

### TiDB

#### Features

* Common Table Expression
* Invisible Index
* Support Modifying Column Types
* Support Second-level Partitions for Partitioned Tables
* Support Interchanging Partitioned Tables and Regular Tables
* Support Inserts and Updates for Views
* Multi-Schema Change
* Configure the Number of Replicas and Distribution Strategy by Tables
* Fine-grained QoS Control
* Flash Back to Any Point-in-time

#### Performance

* Coprocessor Cache
* New Row Storage Format
* Distributed Execution Engine

#### Usability

* Full Link Trace Tool
* Complete Help Information

#### Security

* Column-level Privileges

### TiKV

#### Features

* Fast Incremental Backup and Restoration
* Flash Back to Any Point-in-time
* Hierarchical Storage
* Fine-grained QoS Control
* Configure the Number of Replicas and Distribution Strategy by Regions
* Raft
    + Chain Replication of Data
    + Witness Role
* Storage Engine
    + Support Splitting SSTables According to Guards During Compaction in RocksDB
    + Separate Cold and Hot Data

#### Performance

* Improve Fast Backup Performance
* Improve Fast Restoration Performance
* 1PC
* Support Storage Class Memory Hardware
* New Raft Engine
