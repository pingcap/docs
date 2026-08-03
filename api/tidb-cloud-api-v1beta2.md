---
title: TiDB Cloud API v1beta2 Overview
summary: Learn about the v1beta2 API of TiDB Cloud.
---

# TiDB Cloud API v1beta2 Overview

The TiDB Cloud API v1beta2 is a RESTful API that gives you programmatic access to manage [TiDB Cloud Premium](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=premium#premium) instances and related resources.

Currently, you can use the following v1beta2 APIs to manage the resources in TiDB Cloud Premium:

- [TiDB Cloud Premium API](https://docs.pingcap.com/tidbcloud/api/v1beta2/premium): manage TiDB Cloud Premium instances, backups, and regions. This API includes the following resources:

    - **TiDB Cloud Premium Instance**: manage the lifecycle and configuration of TiDB Cloud Premium instances, including passwords, CA certificates, and cloud provider information.
    - **Backup**: manage backups for TiDB Cloud Premium instances, including backup-based restore.
    - **Region**: retrieve available regions for creating TiDB Cloud Premium instances.
