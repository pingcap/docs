---
title: TiDB Cloud API Overview
summary: Learn about what is TiDB Cloud API, its features, and how to use API to manage your TiDB Cloud clusters.
---

# TiDB Cloud API Overview (Beta)

> **Note:**
>
> TiDB Cloud API is in beta.

The TiDB Cloud API is a [REST interface](https://en.wikipedia.org/wiki/Representational_state_transfer) that provides you with programmatic access to manage administrative objects within TiDB Cloud. Through this API, you can automatically and efficiently manage resources such as Projects, Clusters, Backups, Restores, Imports, Billings, and resources in the [Data Service](/tidb-cloud/data-service-overview.md).

The API has the following features:

- **JSON entities.** All entities are expressed in JSON.
- **HTTPS-only.** You can only access the API via HTTPS, ensuring all the data sent over the network is encrypted with TLS.
- **Key-based access and digest authentication.** Before you access TiDB Cloud API, you must generate an API key, refer to [API Key Management](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management). All requests are authenticated through [HTTP Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication), ensuring the API key is never sent over the network.

The TiDB Cloud API is available in two versions:

- v1beta1
    - Cluster-level resources:
        - [TiDB Cloud Starter or Essential Cluster](https://docs.pingcap.com/tidbcloud/api/v1beta1/serverless): manage clusters, branches, data export tasks, and data import tasks for TiDB Cloud Starter or Essential clusters.
        - [TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated): manage clusters, regions, private endpoint connections, and data import tasks for TiDB Cloud Dedicated clusters.
    - Organization or project-level resources:
        - [Billing](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing): manage billing for TiDB Cloud clusters.
        - [Data Service](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice): manage resources in the Data Service for TiDB Cloud clusters.
        - [IAM](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam): manage API keys for TiDB Cloud clusters.
        - [MSP (Deprecated)](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
- [v1beta](https://docs.pingcap.com/tidbcloud/api/v1beta)
    - [Project](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Project)
    - [Cluster](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Cluster)
    - [Backup](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Backup)
    - [Import (Deprecated)](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Import)
    - [Restore](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Restore)
