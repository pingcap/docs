---
title: Configure TiProxy
summary: Learn how to configure TiProxy.
---

# Configure TiProxy

This document introduces the configuration parameters related to the deployment and use of TiProxy. The following is an example configuration:

```toml
[proxy]
addr = "0.0.0.0:6000"
max-connections = 100

[api]
addr = "0.0.0.0:3080"

[log]
level = "info"

[security]
[security.cluster-tls]
skip-ca = true

[security.sql-tls]
skip-ca = true
```

# ignore-wrong-namespace = true

## Configure the `tiproxy.toml` file

This section introduces the configuration parameters of TiProxy.

> **Tip:**
>
> If you need to adjust the value of a configuration item, refer to [Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration). Normally the modification leads to a restart. Because TiProxy will do configuration hot-reloading, you can skip restart by executing `tiup cluster reload --skip-restart`.

### proxy

Configuration for SQL port.

#### `addr`

+ Default Value: `0.0.0.0:6000`
+ SQL gateway address. The format is `<ip>:<port>`.

#### `graceful-wait-before-shutdown`

+ Default Value: `0`
+ Support hot-reload: yes
+ When the HTTP status is unhealthy, the SQL port accepts new connections for the last `graceful-wait-before-shutdown` seconds. After that, it rejects new connections and drains clients. It is recommended to set it to `0` when there are no other proxies (e.g. NLB) between the client and TiProxy.

#### `graceful-close-conn-timeout`

+ Default Value: `15`
+ Support hot-reload: yes
+ Close connections when they have completed their current transactions (also known as draining clients) within `graceful-close-conn-timeout` seconds. It is recommended to set this timeout longer than the lifecycle of a transaction.

#### `max-connections`

+ Default Value: `0`
+ Support hot-reload: yes
+ TiProxy can accept `max-connections` connections at most. `0` means no limitation.

#### `conn-buffer-size`

+ Default Value: `0`
+ Support hot-reload: yes
+ This configuration item lets you decide the connection buffer size in bytes, e.g. `1024` means 1K buffer. The minimum size is `1K`, and the maximum size is `16M`. It is a tradeoff between memory and performance. By default, when it is `0`, TiProxy will manage the buffer size automatically. However, a larger buffer might yield better performance results. 

#### `pd-addrs`

+ Default Value: `127.0.0.1:2379`
+ Automatically discover TiDB instances and set them as backend.

#### `proxy-protocol`

+ Default Value: ``
+ Support hot-reload: yes
+ Enable proxy protocol handling on the port. You can specify `v2` to handle proxy protocol version 2. `v1` is not supported.

#### `require-backend-tls`

+ Default Value: `true`
+ Support hot-reload: yes
+ Require TLS on backend instances.

### api

Configurations for HTTP gateway.

#### `addr`

+ Default Value: `0.0.0.0:3090`
+ API gateway address. You can specify `ip:port`.

#### `proxy-protocol`

+ Default Value: ``
+ Enable proxy protocol handling on the port. You can specify `v2` to handle proxy protocol version 2. `v1` is not supported.

### log

#### `level`

+ Default Value: `info`
+ Support hot-reload: yes
+ You can specify:

    + `tidb`: format used by TiDB. For details, refer to [Unified Log Format](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md).
    + `json`: structured JSON format.
    + `console`: human-readable log format.

### log.log-file

#### `filename`

+ Default Value: ``
+ Support hot-reload: yes
+ Log file path. Non empty value will enable logging to file.

#### `max-size`

+ Default Value: `300`
+ Support hot-reload: yes
+ Specifies the maximum size, in megabytes, for log files. Logs will be rotated.

#### `max-days`

+ Default Value: `3`
+ Support hot-reload: yes
+ Specifies the maximum number of days to keep old log files. Outdated log files are deleted after surpassing this period.

#### `max-backups`

+ Default Value: `3`
+ Support hot-reload: yes
+ Specifies the maximum number of log files to be retained. Surplus log files will be automatically deleted when an excessive number is reached.

### security

There are four TLS objects in the `[security]` section with different names. They share the same configuration format and fields, but they are interpreted differently depending on their names.

```toml
[security]
    [sql-tls]
    skip-ca = true
    [server-tls]
    auto-certs = true
```

All TLS options are hot-reloaded.

TLS object fields:

+ `ca`: specifies the CA
+ `cert`: specifies the certificate
+ `key`: specifies the private key
+ `auto-certs`: mostly used for tests. It generates certificates if no certificate/key is specified.
+ `skip-ca`: skips verifying certificates using CA on client object or skips server-side verification on server object.
+ `min-tls-version`: sets the minimum TLS version.
+ `rsa-key-size`: sets the RSA key size when `auto-certs` is enabled.
+ `autocert-expire-duration`: sets the default expiration duration for auto-generated certificates.

Objects are classified into client or server objects by their names.

For client TLS object:

- You must set either `ca` or `skip-ca` to skip verifying server certificates.
- Optionally, you can set `cert`/`key` to pass server-side client verification.
- Useless fields: auto-certs.

For server TLS object:

+ You must set either `cert`/`key` or `auto-certs` to generate a temporary certificate, mainly for testing purposes.
+ Optionally, if `ca` is not empty, it enables server-side client verification. The client must provide their certificates. Alternatively, if both `skip-ca` is true and `ca` is not empty, the server will only verify client certificates if they provide one.

#### `cluster-tls`

A client TLS object. It is used to access TiDB or PD.

#### `sql-tls`

A client TLS object. It is used to access TiDB SQL port (4000).

#### `server-tls`

A server TLS object. It is used to provide TLS on SQL port (6000).

#### `server-http-tls`

A server TLS object. It is used to provide TLS on HTTP status port (3080).
