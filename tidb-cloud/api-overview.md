---
title: TiDB Cloud API Overview
summary: Learn about what is TiDB Cloud API, its features, and how to use API to manage your TiDB Cloud clusters.
---

# TiDB Cloud API Overview

The TiDB Cloud API is a [REST interface](https://en.wikipedia.org/wiki/Representational_state_transfer) that provides you with programmatic access to manage administrative objects within TiDB Cloud. Through this API, you can manage resources automatically and efficiently:

* Projects
* Clusters
* Backups
* Restores

The API has the following features:

- **JSON entities.** All entities are expressed in JSON.
- **HTTPS-only.** You can only access the API via HTTPS, ensuring all the data sent over the network is encrypted with TLS.
- **Key-based access and digest authentication.** Before you access TiDB Cloud API, you must generate an API key. All requests are authenticated through [HTTP Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication), ensuring the API key is never sent over the network.

To start using TiDB Cloud API, refer to the following resources:

- [Get Started](https://docs.pingcap.com/tidbcloud/api/v1#section/Get-Started)
- [Authentication](https://docs.pingcap.com/tidbcloud/api/v1#section/Authentication)
- [Rate Limiting](https://docs.pingcap.com/tidbcloud/api/v1#section/Rate-Limiting)
- [API Full References](https://docs.pingcap.com/tidbcloud/api/v1#tag/Project)
