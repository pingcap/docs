---
title: TiProxy Configuration File
summary: Learn how to configure TiProxy.
---

# TiProxy Configuration File

This document introduces the configuration parameters related to the deployment and use of TiProxy. For the configurations of TiUP deployment topology, see [tiproxy-servers configurations](/tiup/tiup-cluster-topology-reference.md#tiproxy_servers).

The following is an example configuration:

```toml
[proxy]
addr = "0.0.0.0:6000"
max-connections = 100

[api]
addr = "0.0.0.0:3080"

[ha]
virtual-ip = "10.0.1.10/24"
interface = "eth0"

[security]
[security.cluster-tls]
skip-ca = true

[security.sql-tls]
skip-ca = true
```

## Configure the `tiproxy.toml` file

This section introduces the configuration parameters of TiProxy.

> **Tip:**
>
> If you need to adjust the value of a configuration item, refer to [Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration). Normally the modification leads to a restart. Because TiProxy supports hot-reloading, you can skip restart by executing `tiup cluster reload --skip-restart`.

### proxy

Configuration for SQL port.

#### `addr`

+ Default value: `0.0.0.0:6000`
+ Support hot-reload: no
+ The listening address of the SQL service. The format is `<ip>:<port>`. This configuration item is automatically set when you deploy TiProxy using TiUP or TiDB Operator.

#### `advertise-addr`

+ Default value: `""`
+ Support hot-reload: no
+ Specifies the address that other components use to connect to this TiProxy instance. This address only contains the host name, not the port. This address might be different from the host name in [`addr`](#addr). For example, if the `Subject Alternative Name` in TiProxy's TLS certificate contains only the domain name, other components will fail to connect to TiProxy via IP. This configuration item is automatically set when you deploy TiProxy using TiUP or TiDB Operator. If not set, the external IP address of the TiProxy instance is used.

#### `graceful-wait-before-shutdown`

+ Default value: `0`
+ Support hot-reload: yes
+ Unit: second
+ When TiProxy shuts down, the HTTP status returns unhealthy but the SQL port still accepts new connections for `graceful-wait-before-shutdown` seconds. After that, it rejects new connections and drains clients. It is recommended to set it to `0` when there are no other proxies (e.g. NLB) between the client and TiProxy.

#### `graceful-close-conn-timeout`

+ Default value: `15`
+ Support hot-reload: yes
+ Unit: second
+ When TiProxy shuts down, it closes connections when they have completed their current transactions (also known as draining clients) within `graceful-close-conn-timeout` seconds. After that, all the connections are closed at once. `graceful-close-conn-timeout` happens after `graceful-wait-before-shutdown`. It is recommended to set this timeout longer than the lifecycle of a transaction.

#### `max-connections`

+ Default value: `0`
+ Support hot-reload: yes
+ Each TiProxy instance can accept `max-connections` connections at most. `0` means no limitation.

#### `conn-buffer-size`

+ Default value: `32768`
+ Support hot-reload: yes, but only for new connections
+ Range: `[1024, 16777216]`
+ This configuration item lets you decide the connection buffer size. Each connection uses one read buffer and one write buffer. It is a tradeoff between memory and performance. A larger buffer might yield better performance results but consume more memory. When it is `0`, TiProxy uses the default buffer size.

#### `pd-addrs`

+ Default value: `127.0.0.1:2379`
+ Support hot-reload: no
+ The PD addresses TiProxy connects to. TiProxy discovers TiDB instances by fetching the TiDB list from the PD. It is set automatically when TiProxy is deployed by TiUP or TiDB Operator.

#### `proxy-protocol`

+ Default value: `""`
+ Support hot-reload: yes, but only for new connections
+ Possible values: `""`, `"v2"`
+ Enable the [PROXY protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) on the port. By enabling the PROXY protocol, TiProxy can pass the real client IP address to TiDB. `"v2"` indicates using the PROXY protocol version 2, and `""` indicates disabling the PROXY protocol. If the PROXY protocol is enabled on TiProxy, you need to also enable the [PROXY protocol](/tidb-configuration-file.md#proxy-protocol) on the TiDB server.

### api

Configurations for HTTP gateway.

#### `addr`

+ Default value: `0.0.0.0:3080`
+ Support hot-reload: no
+ API gateway address. You can specify `ip:port`.

#### `proxy-protocol`

+ Default value: `""`
+ Support hot-reload: no
+ Possible values: `""`, `"v2"`
+ Enable the [PROXY protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) on the port. `"v2"` indicates using the PROXY protocol version 2, and `""` indicates disabling the PROXY protocol.

### balance

Configurations for the load balancing policy of TiProxy.

#### `label-name`

+ Default value: `""`
+ Support hot-reload: yes
+ Specifies the label name used for [label-based load balancing](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing). TiProxy matches the label values of TiDB servers based on this label name and prioritizes routing requests to TiDB servers with the same label value as itself.
+ The default value of `label-name` is an empty string, indicating that label-based load balancing is not used. To enable this load balancing policy, you need to set this configuration item to a non-empty string and configure both [`labels`](#labels) in TiProxy and [`labels`](/tidb-configuration-file.md#labels) in TiDB. For more information, see [Label-based load balancing](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing).

#### `policy`

+ Default value: `resource`
+ Support hot-reload: yes
+ Possible values: `resource`, `location`, `connection`
+ Specifies the load balancing policy. For the meaning of each possible value, see [TiProxy load balancing policies](/tiproxy/tiproxy-load-balance.md#configure-load-balancing-policies).

### `enable-traffic-replay`

+ Default value: `true`
+ Support hot-reload: yes
+ Possible values: `true`, `false`
+ Specifies whether to enable [traffic replay](/tiproxy/tiproxy-traffic-replay.md). If it is set to `false`, traffic capture and replay operations will result in errors.

### ha

High availability configurations for TiProxy.

#### `virtual-ip`

+ Default value: `""`
+ Support hot-reload: no
+ Specifies the virtual IP address in the CIDR format, such as `"10.0.1.10/24"`. When multiple TiProxy instances in a cluster are configured with the same virtual IP, only one TiProxy instance will be bound to the virtual IP. If this instance goes offline, another TiProxy instance will automatically bind to the IP, ensuring clients can always connect to an available TiProxy through the virtual IP.

The following is an example configuration:

```yaml
server_configs:
  tiproxy:
    ha.virtual-ip: "10.0.1.10/24"
    ha.interface: "eth0"
```

When you need to isolate computing layer resources, you can configure multiple virtual IP addresses and use [label-based load balancing](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing) in combination. For examples, see [label-based load balancing](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing).

> **Note:**
>
> - Virtual IP is only supported on Linux operating systems.
> - The Linux user running TiProxy must have permission to bind IP addresses.
> - The real and virtual IP addresses of one TiProxy instance must be within the same CIDR range.

#### `interface`

+ Default value: `""`
+ Support hot-reload: no
+ Specifies the network interface to bind the virtual IP to, such as `"eth0"`. The virtual IP will be bound to a TiProxy instance only when both [`ha.virtual-ip`](#virtual-ip) and `ha.interface` are set.

### `labels`

+ Default value: `{}`
+ Support hot-reload: yes
+ Specifies server labels. For example, `{ zone = "us-west-1", dc = "dc1" }`.

### log

#### `level`

+ Default value: `info`
+ Support hot-reload: yes
+ Possible values: `debug`, `info`, `warn`, `error`, `panic`
+ Specify the log level. With the `panic` level, TiProxy will panic on errors.

#### `encoder`

+ Default value: `tidb`
+ You can specify:

    + `tidb`: format used by TiDB. For details, refer to [Unified Log Format](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md).
    + `json`: structured JSON format.
    + `console`: human-readable log format.

### log.log-file

#### `filename`

+ Default value: `""`
+ Support hot-reload: yes
+ Log file path. Non empty value will enable logging to file. When TiProxy is deployed with TiUP, the filename is set automatically.

#### `max-size`

+ Default value: `300`
+ Support hot-reload: yes
+ Unit: MB
+ Specifies the maximum size for log files. A log file will be rotated if its size exceeds this limit.

#### `max-days`

+ Default value: `3`
+ Support hot-reload: yes
+ Specifies the maximum number of days to keep old log files. Outdated log files are deleted after surpassing this period.

#### `max-backups`

+ Default value: `3`
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
+ `cert-allowed-cn`: when other components connect to TiProxy with TLS, TiProxy can prevent unauthorized access by verifying the `Common Name` in the caller's certificate. This item specifies a list of `Common Name` of valid callers. After setting this item, this TLS object must enable TLS; otherwise, the item does not take effect. For more information on verifying component caller's identity, see [verify component caller's identity](/enable-tls-between-components.md#verify-component-callers-identity).
+ `auto-certs`: mostly used for tests. It generates certificates if no certificate or key is specified.
+ `skip-ca`: skips verifying certificates using CA on client object or skips server-side verification on server object.
+ `min-tls-version`: sets the minimum TLS version. Possible values are `1.0`, `1.1`, `1.2`, and `1.3`. The default value is `1.2`, which allows v1.2 or higher TLS versions.
+ `rsa-key-size`: sets the RSA key size when `auto-certs` is enabled.
+ `autocert-expire-duration`: sets the default expiration duration for auto-generated certificates.

Objects are classified into client or server objects by their names.

For client TLS object:

- You must set either `ca` or `skip-ca` to skip verifying server certificates.
- Optionally, you can set `cert` or `key` to pass server-side client verification.
- Useless fields: `cert-allowed-cn`, `auto-certs`, `rsa-key-size`, `autocert-expire-duration`.

For server TLS object:

+ You can set either `cert` or `key` or `auto-certs` to support TLS connections. Otherwise, TiProxy doesn't support TLS connections.
+ Optionally, if `ca` is not empty, it enables server-side client verification. The client must provide their certificates. Alternatively, if both `skip-ca` is true and `ca` is not empty, the server will only verify client certificates if they provide one.

#### `cluster-tls`

A client TLS object. It is used to access TiDB or PD.

#### `encryption-key-path`

+ Default value: `""`
+ Support hot-reload: yes
+ Specifies the file path of the key used to encrypt the traffic files during traffic capture. The TiProxy instance used for replay needs to be configured with the same key file. The file must contain a 256-bit (32-byte) hexadecimal string with no additional content. An example of the file content is as follows:

```
3b5896b5be691006e0f71c3040a2949
```

#### `require-backend-tls`

+ Default value: `false`
+ Support hot-reload: yes, but only for new connections
+ Require TLS between TiProxy and TiDB servers. If the TiDB server does not support TLS, clients will report an error when connecting to TiProxy.

#### `sql-tls`

A client TLS object. It is used to access TiDB SQL port (4000).

#### `server-tls`

A server TLS object. It is used to provide TLS on SQL port (6000).

#### `server-http-tls`

A server TLS object. It is used to provide TLS on HTTP status port (3080).
