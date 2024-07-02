---
title: TSO Configuration Flags
summary: The TSO configuration flags can be configured via command line flags or environment variables.
---

# TSO Configuration Flags

The TSO node is used for providing the `tso` microservice for PD. You can configure it using command-line flags or environment variables.

## `--advertise-listen-addr`

- The URL for the client to access the TSO node.
- Default: `${listen-addr}`
- In some situations such as in Docker or NAT network environments, if a client cannot access the TSO node through the default client URLs listened to by `tso`, you must manually set `--advertise-listen-addr` for client access.
- For example, the internal IP address of Docker is `172.17.0.1`, while the IP address of the host is `192.168.100.113` and the port mapping is set to `-p 3379:3379`. In this case, you can set `--advertise-listen-addr="http://192.168.100.113:3379"`. Then, the client can find this service through `http://192.168.100.113:3379`.

## `--backend-endpoints`

- The list of backend endpoints of other TSO nodes that the current TSO node listens to.
- Default: `http://127.0.0.1:2379`

## `--cacert`

- The file path of CA, used to enable TLS.
- Default: `""`

## `--cert`

- The path of the PEM file including the X.509 certificate, used to enable TLS.
- Default: `""`

## `--config`

- The configuration file.
- Default: `""`
- If you specify a configuration file, the TSO node first reads configurations from that file. If the same configurations are also specified via command line flags, the TSO node uses the command line flag configurations to overwrite those in the configuration file.

## `--data-dir`

- The path to the data directory on the TSO node.
- Default: `"default.${name}"`

## `--key`

- The path of the PEM file including the X.509 key, used to enable TLS.
- Default: `""`

## `--listen-addr`

- The client URL that the current TSO node listens to.
- Default: `"http://127.0.0.1:3379"`
- When deploying a cluster, you must specify the IP address of the current host as `--listen-addr` (for example, `"http://192.168.100.113:3379"`). If the node runs on Docker, specify the Docker IP address as `"http://0.0.0.0:3379"`.

## `--log-file`

- The log file.
- Default: `""`
- If this flag is not set, logs are output to "stderr". If this flag is set, logs are output to the corresponding file.

## `-L`

- The log level.
- Default: `"info"`
- Optional values: `"debug"`, `"info"`, `"warn"`, `"error"`, `"fatal"`

## `-V`, `--version`

- Output the version information and exit.