---
title: TiDB Cloud API v1beta1 Overview
summary: Learn about the v1beta1 API of TiDB Cloud.
---

# TiDB Cloud API v1beta1 Overview

The TiDB Cloud API v1beta1 is a RESTful API that gives you programmatic access to manage administrative objects within TiDB Cloud. Through this API, you can automatically and efficiently manage cluster-level resources (such as clusters and branches) and organization- or project-level resources (such as billing, Data Service, and IAM).

Currently, you can use the following v1beta1 APIs to manage the resources in TiDB Cloud:

- Cluster-level resources:
    - [TiDB Cloud Starter or Essential Cluster](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless): manage clusters, branches, data export tasks, and data import tasks for TiDB Cloud Starter or Essential clusers （v8.5 or earlier）.
    - [TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated): manage clusters, regions, private endpoint connections, and data import tasks for TiDB Cloud Dedicated clusters.
- Organization or project-level resources:
    - [Billing](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing): manage billing for TiDB Cloud clusters.
    - [Data Service](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice): manage resources in the Data Service for TiDB Cloud clusters.
    - [IAM](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam): manage API keys for TiDB Cloud clusters.
    - [MSP (Deprecated)](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)

> **Note:**
>
> For Essential clusters on version CLOUD.202603.x or higher, please use TiDB Cloud API [v1beta2](/api/tidb-cloud-api-v1beta2.md)