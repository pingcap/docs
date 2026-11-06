---
title: TiDB Cloud API v1beta2 Overview
summary: Learn about the v1beta2 API of TiDB Cloud.
---

# TiDB Cloud API v1beta2 Overview

The TiDB Cloud API v1beta2 is a RESTful API that gives you programmatic access to manage [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances (running TiDB version `CLOUD.202603.x` or later), [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) instances, and their related resources.

> **Note:**
>
> For TiDB Cloud Essential instances running TiDB v8.5.3 or earlier, use the [v1beta1 API](/api/tidb-cloud-api-v1beta1.md) instead.

Unless otherwise specified, "TiDB Cloud instance" on this page refers to either a TiDB Cloud Premium instance or a supported TiDB Cloud Essential instance.

The [TiDB Cloud API v1beta2 reference](https://docs.pingcap.com/tidbcloud/api/v1beta2/) provides endpoints to manage the following resources:

- **TiDB Cloud instance**: manage the lifecycle and configuration of TiDB Cloud instances, including passwords, CA certificates, and cloud provider information.
- **Backup**: manage backups for TiDB Cloud instances, including backup-based restore.
- **Changefeed**: manage the lifecycle and configuration of TiDB Cloud changefeeds.
- **Region**: retrieve available regions for creating TiDB Cloud instances.