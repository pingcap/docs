---
title: Migration Overview
summary: This document describes how to migrate data from databases or data formats (CSV/SQL).
aliases: ['/docs/dev/migration-overview/']
---

# Migration Overview

This document describes how to migrate data to TiDB, which provides the following data migration features:

- Full data migration: use `TiDB Lightning` to import data(CSV/Aurora Snapshot/mydumper sql) to TiDB cluster; to better match with full migration from MySQL/MariaDB database, TiDB also provides a data export tool, `dumpling`, which supports exporting full data as CSV/mydumper sql format;

  - Fast-initializing TiDB clusters: `TiDB Lightning` also provides the fast import feature, which can achieve the effect of fast initialization of specified tables of TiDB clusters. Before using this feature, you need to understand that the fast import period has a great impact on TiDB clusters, and the clusters are not available;

- Incremental data migration: use `DM` to replicate Binlog from MySQL/MariaDB/Aurora to TiDB, which can greatly reduce the downtime window during migration; in addition, `DM` provides full data migration for small data volume databases (< 1T);

- TiDB Cluster Replication: TiDB supports backup recovery, which allows you to initialize a snapshot of TiDB to a new TiDB cluster.

Depending on the type of database where the migrated data is located, deployment location, data size, business requirements and other factors, there will be different data migration options. The following shows some common data migration scenarios to facilitate users to choose the most suitable data migration solution based on these clues.

## Migrate from Aurora/RDS to TiDB

To migrate data from Aurora/RDS to a TiDB cluster deployed in the same Cloud, it is recommended that data migration be done in two steps, full migration and incremental migration, using the Cloud storage service. Choose the appropriate step based on your needs.

In addition, given that Aurora/RDS and TiDB are deployed in different regions, even different Cloud Provider, the solution also includes a description of best practices for migrating data from different regions beforehand.

- Full Data Migration
  - Aurora Full Data Migration to TiDB Tutorial
  - RDS/Self-host MySQL Full Data Migration to TiDB on AWS Tutorial
  - RDS/self-host MySQL Full Data Migration to TiDB on GCP Tutorial

- Aurora/AWS RDS Incremental Data (Binlog) replication to TiDB Tutorial

## Migrate from MySQL to TiDB

Without Cloud storage (S3) service, the network connectivity and latency between MySQL and TiDB are good, you can consider the following solution to migrate data from MySQL to TiDB

- One-Click Migration of MySQL Data to TiDB Tutorial

If you want the import to be fast enough or if the data size is very large (e.g. > 2T), and you allow the TiDB cluster offline during the migration, then you can use `TiDB Lightning` for a fast import of the full amount of data, and then use `DM` for incremental data (Binlog) replication depending on your needs

- fast data import to TiDB tutorial

## Merge Shard Tables (on multiple MySQL) instance to TiDB

If your uses MySQL shard scheme and you want to merge all shard data into TiDB, you can use `DM` for shard merge migration.

- Shard merge migration to TiDB tutorial

If the total size of the shard table is very large (e.g.  > 2T) and allows the TiDB cluster offline during the migration, then you can use Lightning to perform a fast merge import of the full amount of shard data, and then choose to use `DM` for incremental shard data (Binlog) merge replication  according to needs

- Fast merge import of shard data to TiDB tutorial

## Migrate to TiDB Cloud

If you want to use TiDB Cloud and migrate your current business to TiDB Cloud, then you can refer to the following tutorial

- Migrating across Clouds to TiDB Cloud
- Migrating to TiDB Cloud from IDC

## Restore a new TiDB Cluster

If you need to build a disaster recovery cluster or want to replicate a snapshot of your existing TiDB data to a new TiDB clusters for testing, then you can use BR to backup your existing cluster and then restore the backup data to a new cluster

- Building a TiDB Disaster Recovery Cluster Tutorial
- Restore TiDB Snapshots to a New TiDB Cluster Tutorial
