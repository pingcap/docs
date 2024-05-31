---
title: TiProxy Command-Line Flags
summary: Learn the command-line startup flags of TiProxy.
---

# TiProxy Command-Line Flags

This document introduces the command-line flags that you can use when you launch TiProxy. It also introduces flags of `tiproxyctl`.

## TiProxy Server

This section lists the flags of the server program `tiproxy`.

### `--config`

+ Specifies the path of the TiProxy configuration file.
+ Type: `string`
+ Default: `""`
+ You must specify the configuration file. For detailed configuration items, refer to [Configure TiProxy](/tiproxy/tiproxy-configuration.md). Note that TiProxy automatically reloads the configuration when the configuration file is modified. Therefore, do not directly modify the configuration file. It is recommended to modify the configuration by executing [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) or [`kubectl edit tc`](https://docs.pingcap.com/tidb-in-kubernetes/stable/modify-tidb-configuration).

## TiProxy Control

This section introduces the syntax, options, and commands of the client program `tiproxyctl`.

> **Note:**
>
> TiProxy Control is specifically designed for debugging purposes and might not be fully compatible with future capabilities introduced in TiProxy. It's not recommended to include this tool in application or utility development to get information.

### Syntax

```
tiproxyctl [flags] [command]
```

For example:

```
tiproxyctl --curls 127.0.0.1:3080 config get
```

### Options

#### `--log_encoder`

+ Specifies the log format of `tiproxyctl`.
+ Type: `string`
+ Default: `"tidb"`
+ It defaults to the same log format of TiDB. However, you can also specify it as one of the following:

    - `console`: a more human-readable format
    - `json`: a structured log format

#### `--log_level`

+ Specifies the log level of tiproxyctl.
+ Type: `string`
+ Default: `"warn"`
+ You can specify `debug`, `info`, `warn`, `error`, `panic`.

#### `--curls`

+ Specifies the server addresses. You can add multiple listening addresses.
+ Type: `comma separated lists of ip:port`
+ Default: `localhost:3080`
+ Server API gateway addresses.

#### `-k, --insecure`

+ Specifies whether to skip TLS CA verification when dialing to the server.
+ Type: `boolean`
+ Default: `false`
+ Used for testing.

#### `--ca`

+ Specifies the CA when dialing to the server.
+ Type: `string`
+ Default: `""`

#### `--cert`

+ Specifies the certificate when dialing to the server.
+ Type: `string`
+ Default: `""`

### Commands

#### `config set`

The `tiproxyctl config set` command reads a TOML-formatted configuration file from standard input and sets these configuration items to TiProxy. Unspecified configuration items will remain unchanged, so you only need to specify the items that you want to modify.

The following example sets `log.level` as `'warning'`, while leaving other configuration items unchanged.

```bash
$ cat test.toml
[log]
level='warning'
$ cat test.toml | tiproxyctl config set
""
$ tiproxyctl config get | grep level
level = 'warning'
```

#### `config get`

The `tiproxyctl config get` command is used to get the current TiProxy configuration in TOML format.

#### `health`

The `tiproxyctl health` command is used to get the health status of TiProxy and the checksum of the configuration. When TiProxy is running normally, it returns the checksum of the configuration. When TiProxy is shutting down or offline, it returns an error.

Example output:

```json
{"config_checksum":3006078629}
```
