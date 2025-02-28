---
title: DM-master Configuration File
summary: Learn the configuration file of DM-master.
---

# DM-master Configuration File

This document introduces the configuration of DM-master, including a configuration file template and a description of each configuration parameter in this file.

## Configuration file template

The following is a configuration file template of DM-master.

```toml
name = "dm-master"

# log configuration
log-level = "info"
log-file = "dm-master.log"

# DM-master listening address
master-addr = ":8261"
advertise-addr = "127.0.0.1:8261"

# URLs for peer traffic
peer-urls = "http://127.0.0.1:8291"
advertise-peer-urls = "http://127.0.0.1:8291"

# cluster configuration
initial-cluster = "master1=http://127.0.0.1:8291,master2=http://127.0.0.1:8292,master3=http://127.0.0.1:8293"
join = ""

ssl-ca = "/path/to/ca.pem"
ssl-cert = "/path/to/cert.pem"
ssl-key = "/path/to/key.pem"
cert-allowed-cn = ["dm"]

secret-key-path = "/path/to/secret/key"
```

## Configuration parameters

This section introduces the configuration parameters of DM-master.

### Global configuration

#### `name`

- The name of the DM-master.

#### `log-level`

- Specifies a log level.
- Default value: `info`
- Value options: `debug`, `info`, `warn`, `error`, `fatal`

#### `log-file`

- Specifies the log file directory. If the parameter is not specified, the logs are printed onto the standard output.

#### `master-addr`

- Specifies the address of DM-master which provides services. You can omit the IP address and specify the port number only, such as `":8261"`.

#### `advertise-addr`

- Specifies the address that DM-master advertises to the outside world.

#### `peer-urls`

- Specifies the peer URL of the DM-master node.

#### `advertise-peer-urls`

- Specifies the peer URL that DM-master advertises to the outside world. The value of `advertise-peer-urls` is by default the same as that of [`peer-urls`](#peer-urls).

#### `initial-cluster`

- The value of `initial-cluster` is the combination of the [`advertise-peer-urls`](#advertise-peer-urls) value of all DM-master nodes in the initial cluster.

#### `join`

- The value of `join` is the combination of the [`advertise-peer-urls`](#advertise-peer-urls) value of the existing DM-master nodes in the cluster. If the DM-master node is newly added, replace `initial-cluster` with `join`.

#### `ssl-ca`

- The path of the file that contains list of trusted SSL CAs for DM-master to connect with other components.

#### `ssl-cert`

- The path of the file that contains X509 certificate in PEM format for DM-master to connect with other components.

#### `ssl-key`

- The path of the file that contains X509 key in PEM format for DM-master to connect with other components.

#### `cert-allowed-cn`

- Common Name list.

#### `secret-key-path`

- The file path of the secret key, which is used to encrypt and decrypt upstream and downstream passwords. The file must contain a 64-character hexadecimal AES-256 secret key. One way to generate this key is by calculating SHA256 checksum of random data, such as `head -n 256 /dev/urandom | sha256sum`. For more information, see [Customize a secret key for DM encryption and decryption](/dm/dm-customized-secret-key.md).