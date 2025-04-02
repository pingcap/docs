---
title: TiProxy Command-Line Flags
summary: Learn the command-line startup flags of TiProxy.
---

# TiProxy Command-Line Flags

This document introduces the command-line flags that you can use when you launch TiProxy. It also introduces flags of `tiproxyctl`.

## TiProxy Server

This section lists the flags of the server program `tiproxy`.

### `--advertise-addr`

+ Specifies the address that clients use to connect to this TiProxy instance.
+ Type: `string`
+ Default: `""`
+ This flag is automatically set when you deploy TiProxy using TiUP or TiDB Operator. If not set, the external IP address of the TiProxy instance is used.

### `--config`

+ Specifies the path of the TiProxy configuration file.
+ Type: `string`
+ Default: `""`
+ You must specify the configuration file. For detailed configuration items, refer to [Configure TiProxy](/tiproxy/tiproxy-configuration.md). Note that TiProxy automatically reloads the configuration when the configuration file is modified. Therefore, do not directly modify the configuration file. It is recommended to modify the configuration by executing [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) or [`kubectl edit tc`](https://docs.pingcap.com/tidb-in-kubernetes/stable/modify-tidb-configuration).

## TiProxy Control

This section introduces the installation methods, syntax, options, and commands of the client program `tiproxyctl`.

### Install TiProxy Control

You can install TiProxy Control using one of the following two methods.

> **Note:**
>
> TiProxy Control is specifically designed for debugging purposes and might not be fully compatible with future capabilities introduced in TiProxy. It's not recommended to include this tool in application or utility development to get information.

#### Install using TiUP

After installing [TiUP](/tiup/tiup-overview.md), you can use the `tiup install tiproxy` command to download and install the binary programs for TiProxy and TiProxy Control. After installation, you can use `tiup --binary tiproxy` to view the installation path of TiProxy. TiProxy Control is located in the same directory as TiProxy.

For example:

```shell
tiup install tiproxy
# download https://tiup-mirrors.pingcap.com/tiproxy-v1.3.0-linux-amd64.tar.gz 22.51 MiB / 22.51 MiB 100.00% 13.99 MiB/s
ls `tiup --binary tiproxy`ctl
# /root/.tiup/components/tiproxy/v1.3.0/tiproxyctl
```

#### Compile from source code

Compilation environment requirement: [Go](https://golang.org/) 1.21 or later

Compilation procedures: Go to the root directory of the [TiProxy project](https://github.com/pingcap/tiproxy), use the `make` command to compile and generate `tiproxyctl`.

```shell
git clone https://github.com/pingcap/tiproxy.git
cd tiproxy
make
ls bin/tiproxyctl
```

### Syntax

```
tiproxyctl [flags] [command]
```

For example:

```
tiproxyctl --host 127.0.0.1 --port 3080 config get
```

### Options

#### `--host`

+ Specifies the TiProxy server address.
+ Type: `string`
+ Default: `localhost`

#### `--port`

+ Specifies the port number of the TiProxy API gateway.
+ Type: `int`
+ Default: `3080`

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

#### `traffic capture`

The `tiproxyctl traffic capture` command is used to capture traffic.

Options:

- `--output`: (required) specifies the directory to store traffic files.
- `--duration`: (required) specifies the duration of capture. The unit is one of `m` (minutes), `h` (hours), or `d` (days). For example, `--duration=1h` captures traffic for one hour.
- `--compress`: (optional) specifies whether to compress traffic files. `true` means compression, and the compression format is gzip. `false` means no compression. The default value is `true`.
- `--encryption-method`: (optional) specifies the algorithm for encrypting traffic files. Only `""`, `plaintext`, and `aes256-ctr` are supported. `""` and `plaintext` indicate no encryption, and `aes256-ctr` indicates encryption using the `AES256-CTR` algorithm. When specifying encryption, you also need to configure [`encryption-key-path`](/tiproxy/tiproxy-configuration.md#encryption-key-path). The default value is `""`.

Example:

The following command connects to the TiProxy instance at `10.0.1.10:3080`, captures traffic for one hour, and saves it to the `/tmp/traffic` directory on the TiProxy instance:

```shell
tiproxyctl traffic capture --host 10.0.1.10 --port 3080 --output="/tmp/traffic" --duration=1h
```

#### `traffic replay`

The `tiproxyctl traffic replay` command is used to replay captured traffic.

Options:

- `--username`: (required) specifies the database username for replay.
- `--password`: (optional) specifies the password for the username. If not specified, you need to enter the password in an interactive mode.
- `--input`: (required) specifies the directory containing traffic files.
- `--speed`: (optional) specifies the replay speed multiplier. The range is `[0.1, 10]`. The default value is `1`, indicating replay at the original speed.
- `--read-only`: (optional) specifies whether to replay only read-only SQL statements. `true` means to replay only read-only SQL statements, and `false` means to replay all SQL statements. The default value is `false`.

Example:

The following command connects to the TiProxy instance at `10.0.1.10:3080` using username `u1` and password `123456`, reads traffic files from the `/tmp/traffic` directory on the TiProxy instance, and replays the traffic at twice the original speed:

```shell
tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
```

#### `traffic cancel`

The `tiproxyctl traffic cancel` command is used to cancel the current capture or replay job.

#### `traffic show`

The `tiproxyctl traffic show` command is used to display historical capture and replay jobs. It outputs an array of objects, and each object represents a job. Each job has the following fields:

- `type`: the job type. `capture` indicates a traffic capture job, `replay` indicates a traffic replay job
- `status`: the current status of the job. `running` indicates in progress, `done` indicates normal completion, and `canceled` indicates job failure..
- `start_time`: the start time of the job
- `end_time`: the end time if the job has completed. Otherwise, it is empty.
- `progress`: the completion percentage of the job
- `error`: if the job fails, this column contains the reason for the failure. Otherwise, it is empty. For example, `manually stopped` means the user manually cancels the job by executing `CANCEL TRAFFIC JOBS`.
- `output`: the output traffic file path of the capture job
- `duration`: the duration of the traffic capture job
- `compress`: whether the traffic files are compressed
- `encryption_method`: the encryption method of the traffic file
- `input`: the input traffic file path of the replay job
- `username`: the database username for traffic replay
- `speed`: the replay speed multiplier
- `read_only`: whether only replays read-only statements

Example output:

```json
[
  {
    "type": "capture",
    "status": "done",
    "start_time": "2024-09-01T14:30:40.99096+08:00",
    "end_time": "2024-09-01T16:30:40.99096+08:00",
    "progress": "100%",
    "output": "/tmp/traffic",
    "duration": "2h",
    "compress": true
  },
  {
    "type": "capture",
    "status": "canceled",
    "start_time": "2024-09-02T18:30:40.99096+08:00",
    "end_time": "2024-09-02T19:00:40.99096+08:00",
    "progress": "25%",
    "error": "manually stopped",
    "output": "/tmp/traffic",
    "duration": "2h"
  },
  {
    "type": "capture",
    "status": "running",
    "start_time": "2024-09-03T13:31:40.99096+08:00",
    "progress": "45%",
    "output": "/tmp/traffic",
    "duration": "2h"
  }
]
```
