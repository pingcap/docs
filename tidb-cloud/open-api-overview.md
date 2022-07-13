# TiDB Cloud Open API Overview

The TiDB Cloud Open API is a [REST interface](https://en.wikipedia.org/wiki/Representational_state_transfer) that allows you programmatic access to manage administrative objects within TiDB Cloud, including projects, cluster deployments, backups, and so on.

The API has the following features:

- **JSON entities.** All entities are expressed in JSON.
- **HTTPS-only.** You can only access the API via HTTPS, ensuring all the data sent over the network is encrypted with TLS.
- **Key-based access and digest authentication.** Before you access TiDB Cloud Open API, you must generate an API key. All requests are authenticated through [HTTP Digest Authentication](https://en.wikipedia.org/wiki/Digest_access_authentication), ensuring the API key is never sent over the network.

To start using TiDB Cloud Open API, see the following resources:

- [Get started](/xxx)
- [API full references](xxxx/tidbcloud/api/v1)
