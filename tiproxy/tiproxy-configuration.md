---
title: Configure TiProxy
summary: Learn how to configure TiProxy.
aliases: ['/docs/dev/tiproxy/tiproxy-configuration/','/docs/dev/reference/tiproxy/configuration/']
---

# Configure TiProxy

This document introduces the configuration parameters related to the deployment and use of TiProxy.

## Configure the `tiproxy.toml` file

This section introduces the configuration parameters of TiProxy.

> **Tip:**
>
> If you need to adjust the value of a configuration item, refer to [Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration).


```toml
[proxy]
# SQL service address
# addr = "0.0.0.0:6000"

# Enable TCP keepalive feature, require OS support.
# tcp-keep-alive = true

# Whether TiProxy requires SSL from the backend TiDB. It will reject connections.
# require-backend-tls = true

# possible values:
#   "" => disable proxy protocol.
#   "v2" => accept proxy protocol if any, require backends to support proxy protocol.
# proxy-protocol = ""

# graceful-wait-before-shutdown is recommanded to be set to 0 when there's no other proxy(e.g. NLB) between the client and TiProxy.
# possible values:
# 	0 => begin to drain clients immediately.
# 	30 => HTTP status returns unhealthy and the SQL port accepts new connections for the last 30 seconds. After that, refuse new connections and drain clients.
# graceful-wait-before-shutdown = 0

# graceful-close-conn-timeout is recommanded to be set longer than the lifecycle of a transaction.
# possible values:
#   0 => force closing connections immediately.
#   15 => close connections when they have finished current transactions (AKA drain clients). After 15s, force closing all the connections.
# graceful-close-conn-timeout = 15

# possible values:
#		"pd-addr:pd-port" => automatically tidb discovery.
# pd-addrs = "127.0.0.1:2379"

# possible values:
#		0 => no limitation.
#		100 => accept as many as 100 connections.
# max-connections = 0

# It's a tradeoff between memory and performance.
# possible values:
#       0 => default value
#		1K to 16M
# conn-buffer-size = 0

[api]
# TiProxy HTTP API gateway
# addr = "0.0.0.0:3080"

# Enable HTTP basic auth or not.
# enable-basic-auth = false
# user = ""
# password = ""

# Same as [proxy.proxy-protocol], but for HTTP port
# proxy-protocol = ""

[log]

# level = "info"

# possible values:
# 	"tidb" => formats used by tidb, check https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md.
# 	"json" => structured json formats.
# 	"console" => log format for human.
# encoder = "tidb"

[log.log-file]

# A non-empty filename will enable logging to file.
#
# filename = ""
# max-size = 300
# max-days = 3
# max-backups = 3

# See the section below for details.
[security]

	# client object
	[security.cluster-tls]
	# access to other components like TiDB or PD, will use this
	# skip-ca = true

	# client object
	[security.sql-tls]
	# access to TiDB SQL(4000) port will use this
	skip-ca = true

	# server object
	[security.server-tls]
	# proxy SQL port will use this
	# auto-certs = true

	# server object
	[security.server-http-tls]
	# proxy HTTP port will use this
	# auto-certs = true
```

### Security Object

There are 4 tls objects in `[security]` section. They share same configuration formats and fields. But are interpreted differently according to their usage.

```
[xxxx-tls]
   ca = "ca.pem"
   cert = "c.pem"
   key = "k.pem"
   auto-certs = true # mostly used by tests. It will generate certs if no cert/key is specified.
   skip-ca = true
   min-tls-version = "1.1" # specify minimum TLS version
   rsa-key-size = 4096 # generated RSA keysize if auto-certs is enabled.
   autocert-expire-duration = "72h" # default expire duration for auto certs.
```

+ Client Object:
  - Requires to set `ca` or `skip-ca` (skip verify server certs).
  - Optionally, `cert`/`key` will be used if server asks, i.e. server-side client verification.
  - Useless fields: auto-certs.

+ Server Object:
  + Requires to set `cert`/`key` or `auto-certs` (generate a temporary cert, mostly for testing).
  + Optionally, non-empty `ca` will enable server-side client verification. Client must provide their certs. Or if `skip-ca` is true with a non-empty `ca`, server will only verify client certs if it actively provide one.
