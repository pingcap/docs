---
title: TiProxy 配置文件
summary: 了解如何配置 TiProxy。
---

# TiProxy 配置文件

本文档介绍了与 TiProxy 部署和使用相关的配置参数。以下是一个示例配置：

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

## 配置 `tiproxy.toml` 文件

本节介绍 TiProxy 的配置参数。

> **提示：**
>
> 如果需要调整某个配置项的值，请参考 [修改配置](/maintain-tidb-using-tiup.md#modify-the-configuration)。通常修改后需要重启。由于 TiProxy 支持热重载，你可以通过执行 `tiup cluster reload --skip-restart` 来跳过重启。

### proxy

SQL 端口的配置。

#### `addr`

+ 默认值：`0.0.0.0:6000`
+ 支持热重载：否
+ SQL 网关地址。格式为 `<ip>:<port>`。

#### `graceful-wait-before-shutdown`

+ 默认值：`0`
+ 支持热重载：是
+ 单位：秒
+ 当 TiProxy 关闭时，HTTP 状态显示为不健康，但 SQL 端口仍会接受新连接，持续 `graceful-wait-before-shutdown` 秒。之后，TiProxy 会拒绝新连接并逐步关闭客户端。建议在客户端和 TiProxy 之间没有其他代理（如 NLB）时，将其设置为 `0`。

#### `graceful-close-conn-timeout`

+ 默认值：`15`
+ 支持热重载：是
+ 单位：秒
+ 当 TiProxy 关闭时，会在 `graceful-close-conn-timeout` 秒内关闭已完成当前事务的连接（即“排空客户端”）。之后，所有连接会被一次性关闭。`graceful-close-conn-timeout` 在 `graceful-wait-before-shutdown` 之后生效。建议将此超时时间设置得长于事务的生命周期。

#### `max-connections`

+ 默认值：`0`
+ 支持热重载：是
+ 每个 TiProxy 实例最多接受 `max-connections` 个连接。`0` 表示无限制。

#### `conn-buffer-size`

+ 默认值：`32768`
+ 支持热重载：是，但仅对新连接生效
+ 范围：[1024, 16777216]
+ 该配置项决定连接缓冲区的大小。每个连接使用一个读缓冲区和一个写缓冲区。这是在内存和性能之间的权衡。缓冲区越大，性能可能越好，但会占用更多内存。当设置为 `0` 时，TiProxy 使用默认缓冲区大小。

#### `pd-addrs`

+ 默认值：`127.0.0.1:2379`
+ 支持热重载：否
+ TiProxy 连接的 PD 地址。TiProxy 通过获取 PD 上的 TiDB 列表来发现 TiDB 实例。部署 TiProxy 时（通过 TiUP 或 TiDB Operator）会自动设置。

#### `proxy-protocol`

+ 默认值：`""`
+ 支持热重载：是，但仅对新连接生效
+ 可能的值：`""`、`"v2"`
+ 在端口启用 [PROXY protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)。启用后，TiProxy 可以将真实客户端 IP 传递给 TiDB。`"v2"` 表示使用 PROXY 协议版本 2，`""` 表示禁用 PROXY 协议。如果在 TiProxy 上启用 PROXY protocol，还需要在 TiDB 服务器上启用 [PROXY protocol](/tidb-configuration-file.md#proxy-protocol)。

### api

HTTP 网关的配置。

#### `addr`

+ 默认值：`0.0.0.0:3080`
+ 支持热重载：否
+ API 网关地址。可以指定 `ip:port`。

#### `proxy-protocol`

+ 默认值：`""`
+ 支持热重载：否
+ 可能的值：`""`、`"v2"`
+ 在端口启用 [PROXY protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)。`"v2"` 表示使用 PROXY 协议版本 2，`""` 表示禁用。

### log

#### `level`

+ 默认值：`info`
+ 支持热重载：是
+ 可能的值：`debug`、`info`、`warn`、`error`、`panic`
+ 指定日志级别。设置为 `panic` 时，TiProxy 在错误时会触发 panic。

#### `encoder`

+ 默认值：`tidb`
+ 可指定：

    + `tidb`：TiDB 使用的格式。详情请参考 [Unified Log Format](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)。
    + `json`：结构化 JSON 格式。
    + `console`：人类可读的日志格式。

### log.log-file

#### `filename`

+ 默认值：`""`
+ 支持热重载：是
+ 日志文件路径。非空值会启用文件日志。当通过 TiUP 部署 TiProxy 时，文件名会自动设置。

#### `max-size`

+ 默认值：`300`
+ 支持热重载：是
+ 单位：MB
+ 指定日志文件的最大大小。超过此限制后，日志文件会轮转。

#### `max-days`

+ 默认值：`3`
+ 支持热重载：是
+ 指定保留旧日志文件的最大天数。超过此期限的日志文件会被删除。

#### `max-backups`

+ 默认值：`3`
+ 支持热重载：是
+ 指定最多保留的日志文件数量。超出部分会自动删除。

### security

在 `[security]` 部分有四个 TLS 对象，名称不同，但它们的配置格式和字段相同，根据名称的不同会有不同的解释。

```toml
[security]
    [sql-tls]
    skip-ca = true
    [server-tls]
    auto-certs = true
```

所有 TLS 选项都支持热重载。

TLS 对象字段：

+ `ca`：指定 CA
+ `cert`：指定证书
+ `key`：指定私钥
+ `auto-certs`：主要用于测试。如果未指定证书或私钥，则会自动生成证书。
+ `skip-ca`：跳过验证客户端对象的证书或跳过服务器端验证。
+ `min-tls-version`：设置最低 TLS 版本。可能的值为 `1.0`、`1.1`、`1.2` 和 `1.3`。默认值为 `1.2`，允许使用 v1.2 及以上版本的 TLS。
+ `rsa-key-size`：在启用 `auto-certs` 时设置 RSA 密钥长度。
+ `autocert-expire-duration`：设置自动生成证书的默认过期时间。

对象根据名称分为客户端对象或服务器对象。

对于客户端 TLS 对象：

- 必须设置 `ca` 或 `skip-ca` 以跳过验证服务器证书。
- 可选地，设置 `cert` 或 `key` 以进行服务器端的客户端验证。
- 无用字段：auto-certs。

对于服务器 TLS 对象：

+ 可以设置 `cert` 或 `key` 或 `auto-certs` 来支持 TLS 连接，否则 TiProxy 不支持 TLS 连接。
+ 可选地，如果 `ca` 不为空，则启用服务器端的客户端验证。客户端必须提供证书。或者，如果 `skip-ca` 为 true 且 `ca` 不为空，服务器只会验证客户端证书（如果客户端提供的话）。

#### `cluster-tls`

一个客户端 TLS 对象。用于访问 TiDB 或 PD。

#### `require-backend-tls`

+ 默认值：`false`
+ 支持热重载：是，但仅对新连接生效
+ 要求 TiProxy 和 TiDB 服务器之间使用 TLS。如果 TiDB 服务器不支持 TLS，客户端在连接 TiProxy 时会报错。

#### `sql-tls`

一个客户端 TLS 对象。用于访问 TiDB SQL 端口（4000）。

#### `server-tls`

一个服务器 TLS 对象。用于在 SQL 端口（6000）提供 TLS。

#### `server-http-tls`

一个服务器 TLS 对象。用于在 HTTP 状态端口（3080）提供 TLS。
