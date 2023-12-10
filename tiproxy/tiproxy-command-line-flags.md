---
title: TiProxy Command-line Flags
summary: Learn the command-line startup flags of TiProxy.
aliases: ['/docs/dev/tiproxy/tiproxy-command-line-flags/']
---

# TiProxy Command-Line Flags

This document introduces the command-line flags that you can use when you launch TiProxy. It also introduce flags of `tiproxyctl`.

## TiProxy Server

This is the server program `tiproxy`.

### `--config string`

+ Specifies the path of the TiProxy configuration file
+ Default: ""
+ You must specify the configuration file. For detailed configuration items, refer to [TiProxy configuration parameters](/tiproxy/tiproxy-configuration.md).

### `--log_encoder string`

+ Specifies the log format of TiProxy
+ Default: ""
+ Fallback to the same format as TiDB when empty.

### `--log_level string`

+ Specifies the log level of TiProxy
+ Default: ""
+ Fallback to *info* when empty.

## TiProxy Ctl

This is the client program `tiproxyctl`.

### `--log_encoder string`

+ Specifies the log format of ctl
+ Default: "tidb"
+ Refer previous description.

### `--log_level string`

+ Specifies the log level of ctl
+ Default: "warn"
+ Refer previous description.

### `--curls urls`

+ Specifies the server addresses.
+ Default: "[localhost:3080]"
+ Server API gateway addresses.

### `-k, --insecure`

+ Whether skip TLS CA verification when dial to the server
+ Default: "false"
+ Useful for testing.

### `--ca string`

+ Specifies the ca when dial to the server.
+ Default: ""
+ For security.

### `--cert string`

+ Specifies the cert when dial to the server.
+ Default: ""
+ For security.
