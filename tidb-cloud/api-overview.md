---
title: TiDB Cloud API Overview
summary: Learn about what is TiDB Cloud API, its features, and how to use API to manage your TiDB Cloud clusters.
---

# TiDB Cloud API Overview <span style="color: #fff; background-color: #00bfff; border-radius: 4px; font-size: 0.5em; vertical-align: middle; margin-left: 16px; padding: 0 2px;">Beta</span>

> **Note:**
>
> TiDB Cloud API is in beta.

The TiDB Cloud API is a [REST interface](https://en.wikipedia.org/wiki/Representational_state_transfer) that provides you with programmatic access to manage administrative objects within TiDB Cloud. Through this API, you can automatically and efficiently manage resources such as Projects, Clusters, Backups, Restores, Imports, Billings, and resources in the [Data Service](/tidb-cloud/data-service-overview.md).

The API has the following features:

- **JSON entities.** All entities are expressed in JSON.
- **HTTPS-only.** You can only access the API via HTTPS, ensuring all the data sent over the network is encrypted with TLS.
- **Key-based access and digest authentication.** Before you access TiDB Cloud API, you must generate an API key, refer to [API Key Management](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management). All requests are authenticated through [HTTP Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication), ensuring the API key is never sent over the network.

To start using TiDB Cloud API, refer to the following resources in TiDB Cloud API Documentation:

- [Get Started](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started)
- [Authentication](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)
- [Rate Limiting](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Rate-Limiting)
- API Full References
    - v1beta1
        - [Billing](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing)
        - [Data Service](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)
        - [IAM](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam)
        - [MSP](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
    - [v1beta](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project)
- [Changelog](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog)
