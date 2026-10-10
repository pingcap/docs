---
title: TiDB Cloud API v1beta2 Overview
summary: Learn about the v1beta2 API of TiDB Cloud.
---

# TiDB Cloud API v1beta2 Overview

The TiDB Cloud API v1beta2 is a RESTful API that gives you programmatic access to manage [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) instances , [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances and related resources.

Currently, you can use the following v1beta2 APIs to manage the resources in TiDB Cloud Premium or Essential:

- [TiDB Cloud Premium/Essential API](https://docs.pingcap.com/tidbcloud/api/v1beta2/premium): manage TiDB Cloud instances, backups, and regions. This API includes the following resources:

    - **TiDB Cloud Premium or Essential Instance**: manage the lifecycle and configuration of TiDB Cloud instances, including passwords, CA certificates, and cloud provider information.
    - **Backup**: manage backups for TiDB Cloud instances, including backup-based restore.
    - **Region**: retrieve available regions for creating TiDB Cloud instances.

> **Note:**
>
> TiDB Cloud API v1beta2 is only available for Essential instances running version CLOUD.202603.x or later. For Essential instances on version v8.5 or earlier, please use the TiDB Cloud API [v1beta1](/api/tidb-cloud-api-v1beta1.md)