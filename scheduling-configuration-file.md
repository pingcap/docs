---
title: Scheduling Configuration File
summary: The Scheduling configuration file includes multiple configuration items such as node name, data path, and node URL.
---

# Scheduling Configuration File

<!-- markdownlint-disable MD001 -->

The Scheduling node is used for providing the `scheduling` microservice for PD. This document is applicable only in PD microservice mode.

> **Tip:**
>
> If you need to adjust the value of a configuration item, refer to [Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration).

### `name`

- The name of the Scheduling node
- Default value: `"Scheduling"`
- To start multiple Scheduling nodes, use a unique name for each node.

### `data-dir`

- The directory in which the Scheduling node stores data
- Default value: `"default.${name}"`

### `listen-addr`

- The client URL that the current Scheduling node listens to
- Default value: `"http://127.0.0.1:3379"`
- When deploying a cluster, you must specify the IP address of the current host as `listen-addr` (for example, `"http://192.168.100.113:3379"`). If the node runs on Docker, specify the Docker IP address as `"http://0.0.0.0:3379"`.

### `advertise-listen-addr`

- The URL for the client to access the Scheduling node
- Default value: `"${listen-addr}"`
- In some situations such as in Docker or NAT network environments, if a client cannot access the Scheduling node through the default client URLs listened to by the Scheduling node, you must manually set `advertise-listen-addr` for client access.
- For example, the internal IP address of Docker is `172.17.0.1`, while the IP address of the host is `192.168.100.113` and the port mapping is set to `-p 3379:3379`. In this case, you can set `advertise-listen-addr="http://192.168.100.113:2379"`. Then, the client can find this service through `http://192.168.100.113:2379`.

### `backend-endpoints`

- The list of backend endpoints of other Scheduling nodes that the current Scheduling node listens to
- Default value: `"http://127.0.0.1:2379"`

### `lease`

- The timeout of the Scheduling Primary Key lease. After the timeout, the system re-elects a Primary.
- Default value: `3`
- Unit: seconds

## security

Configuration items related to security

### `cacert-path`

- The path of the CA file
- Default value: ""

### `cert-path`

- The path of the Privacy Enhanced Mail (PEM) file that contains the X.509 certificate
- Default value: ""

### `key-path`

- The path of the PEM file that contains the X.509 key
- Default value: ""

### `redact-info-log`

- Controls whether to enable log redaction in Scheduling node logs.
- When you set the configuration value to `true`, user data is redacted in Scheduling node logs.
- Default value: `false`

## log

Configuration items related to logs.

### `level`

- Specifies the level of the output log.
- Optional value: `"debug"`, `"info"`, `"warn"`, `"error"`, `"fatal"`
- Default value: `"info"`

### `format`

- The log format
- Optional value: `"text"`, `"json"`
- Default value: `"text"`

### `disable-timestamp`

- Controls whether to disable the automatically generated timestamp in logs.
- Default value: `false`

## log.file

Configuration items related to the log file

### `max-size`

- The maximum size of a single log file. When this value is exceeded, the system automatically splits the log into several files.
- Default value: `300`
- Unit: MiB
- Minimum value: `1`

### `max-days`

- The maximum number of days in which a log is kept.
- If the configuration item is unset or set to the default value `0`, Scheduling does not clean up log files.
- Default value: `0`

### `max-backups`

- The maximum number of log files to be kept.
- If the configuration item is unset or set to the default value `0`, Scheduling keeps all log files.
- Default value: `0`

## metric

Configuration items related to monitoring

### `interval`

- The interval at which monitoring metric data is pushed to Prometheus
- Default value: `15s`