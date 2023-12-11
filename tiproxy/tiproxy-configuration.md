---
title: Configure TiProxy
summary: Learn how to configure TiProxy.
---

# Configure TiProxy

This document introduces the configuration parameters related to the deployment and use of TiProxy. The following is an example configuration:

## Configure the `tiproxy.toml` file

This section introduces the configuration parameters of TiProxy.

> **Tip:**
>
> If you need to adjust the value of a configuration item, refer to [Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration). Since TiProxy will do config hot-reloading, you can also skip restart by `tiup cluster reload --skip-restart`.

### proxy

Configuration for SQL port.

#### `addr`

+ Default Value: `0.0.0.0:6000`
+ SQL gateway address. You should specify `ip:port`.

#### `graceful-wait-before-shutdown`

+ Default Value: `0`
+ Hot-reload supported.
+ HTTP status returns unhealthy and the SQL port accepts new connections for the last `graceful-wait-before-shutdown` seconds. After that, refuse new connections and drain clients. It is recommanded to be set to 0 when there's no other proxy(e.g. NLB) between the client and TiProxy.

#### `graceful-close-conn-timeout`

+ Default Value: `15`
+ Hot-reload supported.
+ Close connections when they have finished current transactions (AKA drain clients) after `graceful-close-conn-timeout` seconds. It is recommanded to be set longer than the lifecycle of a transaction.

#### `max-connections`

+ Default Value: `0`
+ Hot-reload supported.
+ Accept as many as `max-connections` connections. Zero means no limitation.

#### `conn-buffer-size`

+ Default Value: `0`
+ Hot-reload supported.
+ Tradeoff between memory and performance. Larger buffer may yield better performance result.

#### `pd-addrs`

+ Default Value: `127.0.0.1:2379`
+ Automatically discovery TiDB instances and set them as backend.

#### `proxy-protocol`

+ Default Value: ``
+ Hot-reload supported.
+ Enable proxy protocol handling on the port. You could specify `v2` to handle proxy protocol version 2.

#### `require-backend-tls`

+ Default Value: `true`
+ Hot-reload supported.
+ Require TLS on backend instances.

### api

Configurations for HTTP gateway.

#### `addr`

+ Default Value: `0.0.0.0:3090`
+ API gateway address. You should specify `ip:port`.

#### `proxy-protocol`

+ Default Value: ``
+ Enable proxy protocol handling on the port. You could specify `v2` to handle proxy protocol version 2.

### log

#### `level`

+ Default Value: `info`
+ Hot-reload supported.
+ You can specify:

    + `tidb`: formats used by tidb, check https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md
    + `json`: structured json formats
    + `console`: log format for human.

### log.log-file

#### `filename`

+ Default Value: ``
+ Hot-reload supported.
+ Log file path. Non empty value will enable logging to file.

#### `max-size`

+ Default Value: `300`
+ Hot-reload supported.
+ Log file maximum size, in megabytes. Log will be rotated.

#### `max-days`

+ Default Value: `3`
+ Hot-reload supported.
+ Maximum days to retain old log files. It is deleted once it is too old.

#### `max-backups`

+ Default Value: `3`
+ Hot-reload supported.
+ Maximum number of log files. Extra log files will be deleted once there are too many.

### security

There are 4 tls objects in `[security]` section. They share same configuration formats and fields. But they are interpreted differently according to their usage.

All TLS options are hot-reloaded.

#### TLS object

+ `ca`: specify CA
+ `cert`: specify cert
+ `key`: specify private key
+ `auto-certs`: mostly used by tests. It will generate certs if no cert/key is specified
+ `skip-ca`: skip verifying certs using CA on client object, or skip server-side verification on server object
+ `min-tls-version`: minimum TLS version
+ `rsa-key-size`: generated RSA keysize if `auto-certs` is enabled
+ `autocert-expire-duration`: default expire duration for auto certs.

Client TLS Object:

- Requires to set `ca` or `skip-ca` (skip verify server certs).
- Optionally, `cert`/`key` will be used if server asks, i.e. server-side client verification.
- Useless fields: auto-certs.

Server TLS Object:

+ Requires to set `cert`/`key` or `auto-certs` (generate a temporary cert, mostly for testing).
+ Optionally, non-empty `ca` will enable server-side client verification. Client must provide their certs. Or if `skip-ca` is true with a non-empty `ca`, server will only verify client certs if it actively provide one.

#### `cluster-tls`

A client TLS object. It is used to access TiDB or PD.

#### `sql-tls`

A client TLS object. It is used to access TiDB SQL port (4000).

#### `server-tls`

A server TLS object. It is used to provide TLS on SQL port (6000).

#### `server-http-tls`

A server TLS object. It is used to provide TLS on HTTP status port (3080).
