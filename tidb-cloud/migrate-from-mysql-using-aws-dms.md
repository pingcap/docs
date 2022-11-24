---
title: Migrate MySQL-Compatible Databases to TiDB Cloud Using AWS DMS
summary: Learn how to migrate data from MySQL-compatible databases into TiDB Cloud using AWS Database Migration Service (AWS DMS).
---

# Migrate MySQL-Compatible Databases to TiDB Cloud Using AWS DMS

AWS Database Migration Service (AWS DMS) is a cloud service that makes it easy to migrate relational databases, data warehouses, NoSQL databases, and other types of data stores. You can use AWS DMS to migrate your data into TiDB Cloud.

This document uses Amazon Relational Database Service (RDS) as an example to show how to migrate data to TiDB Cloud using AWS DMS. The procedure also applies to migrating data from self-built MySQL databases and Amazon Aurora.

In this example, the data source is Amazon RDS, and the data destination is a Dedicated Tier cluster in TiDB Cloud. Both upstream and downstream databases are in the same region. 

## Consideratoins

Before you start the migration, make sure you have read the following:

