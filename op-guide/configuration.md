---
title: Configuration Flags
category: operations
---

# Configuration Flags

TiDB/TiKV/PD are configurable through command-line flags and environment variables.


## TiDB

The default TiDB ports are 4000 for client requests and 10080 for status report.

### `--store`
+ the storage engine type
+ Human-readable name for this member.
+ default: "goleveldb"
+ You can choose from "memory", "goleveldb", "BoltDB" or "TiKV". The first three are all local storage engines. TiKV is a distributed storage engine.

### `--path`
+ the path to the data directory for local storage engines like goleveldb, BoltDB, or memory or the DSN for the distributed storage engine like TiKV. If you use TiKV, specify the path in the following format: $Host:$Port.
+ default: "/tmp/tidb"

### `-L`
+ the log level
+ default: "info"
+ You can choose from debug, info, warn, error, or fatal.

### `--log-file`
+ the log file
+ default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### `--host`
+ the listening address for TiDB server
+ default: "0.0.0.0"
+ TiDB server will listen on this address.

### `-P`
+ the listening port for TiDB server
+ default: "4000"
+ TiDB server will accept MySQL client request from this port.

### `--status`
+ the status report port for TiDB server
+ default: "10080"
+ This is used to get server internal data. The data includes [prometheus metrics](https://prometheus.io/) and [pprof](https://golang.org/pkg/net/http/pprof/).
+ Prometheus metrics can be got through "http://host:status_port/metrics".
+ Pprof data can be got through "http://host:status_port/debug/pprof".

### `--lease`
+ the schema lease time in seconds
+ default: "1"
+ This is the schema lease time that is used in online schema changes. The value will affect the DDL statement running time. Do not change it unless you understand the internal mechanism.

### `--socket`
+ the socket file for connection
+ default: ""
+ You can use the "/tmp/tidb.sock" file.

### `--perfschema`
+ enable(true) or disable(false) the performance schema
+ default: false
+ The value can be (true) or (false). (true) is to enable and (false) is to disable. The Performance Schema provides a way to inspect internal execution of the server at runtime. See [performance schema](http://dev.mysql.com/doc/refman/5.7/en/performance-schema.html) for more information. If you enable the performance schema, the performance will be affected.

### `--privilege`
+ enable(true) or disable(false) the privilege check(for debugging)
+ default: true
+ The value can be (true) or (false). (true) is to enable and (false) is to disable. This option is deprecated and will be removed.

### `--skip-grant-table`
+ enables anyone to connect without a password and with all privileges
+ default: false
+ The value can be (true) or (false). This option is usually used to reset password, enabling it requires the root privileges.

### `--report-status`
+ enable(true) or disable(false) the status report and pprof tool.
+ default: true
+ The value can be (true) or (false). (true) is to enable metrics and pprof. (false) is to disable metrics and pprof.

### `--metrics-addr`
+ the Prometheus pushgateway address
+ default: ""
+ Leaving it empty stops the Prometheus client from pushing.

### `--metrics-intervel`
+ the Prometheus client push interval in seconds
+ default: 0
+ Setting the value to 0 stops the Prometheus client from pushing.

### `--cross-join`
+ enable(true) or disable(false) the cross join without any equal condition
+ default: true
+ The value can be (true) or (false). (true) is to enable join without any equal conditions. (false) is to disable it.

### `--ssl-cert`

+ The path to an SSL certificate file in PEM format to use for establishing a secure connection.
+ default: ""
+ When this option is specified along with `--ssl-key`, the server permits but does not require secure connections.
+ If the specified certificate or key is not valid, the server still starts normally but does not permit secure connections.

### `--ssl-key`

+ The path to an SSL key file in PEM format to use for establishing a secure connection, namely the private key of the certificate you specified by `--ssl-cert`.
+ default: ""
+ Currently TiDB does not support keys protected by a passphrase.

### `--ssl-ca`

+ The path to a file in PEM format that contains a list of trusted SSL certificate authorities.
+ default: ""
+ When this option is specified along with `--ssl-cert` and `--ssl-key`, the server verifies the client's certificate via this CA list if the client provides its certificate accordingly.
+ The secure connection will be established without client verification if the client does not provide a certificate even when this option is set.

### `--proxy-protocol-networks`

+ The proxy server’s IP addresses that allowed by PROXY Protocol.
+ default: "" (empty string)
+ The value can be IP address (192.168.1.50) or CIDR (192.168.1.0/24), if more than one address (or CIDR) required, use `,` to split. `*` means any IP addresses. Leaving it empty disable PROXY Protocol.

### `--proxy-protocol-header-timeout`
+ PROXY Protocol header read timeout.
+ default: 5 (seconds)
+ The value set timeout for the PROXY protocol header read. The unit is second. You should not set this value to 0.

## Placement Driver (PD)

### `-L`

+ the log level
+ default: "info"
+ You can choose from debug, info, warn, error, or fatal.

### `--log-file`
+ the log file
+ default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### `--config`

+ the config file
+ default: ""
+ If you set the configuration using the command line, the same setting in the config file will be overwritten.

### `--name`

+ the human-readable unique name for this PD member
+ default: "pd"
+ If you want to start multiply PDs, you must use different name for each one.

### `--data-dir`

+ the path to the data directory
+ default: "default.${name}"

### `--client-urls`

+ the listening URL list for client traffic
+ default: "http://127.0.0.1:2379"

### `--advertise-client-urls`

+ the advertise URL list for client traffic from outside
+ default: ${client-urls}
+ If the client cannot connect to PD through the default listening client URLs, you must manually set the advertise client URLs explicitly.

### `--peer-urls`

+ the listening URL list for peer traffic
+ default: "http://127.0.0.1:2380"

### `--advertise-peer-urls`

+ the advertise URL list for peer traffic from outside
+ default: ${peer-urls}
+ If the peer cannot connect to PD through the default listening peer URLs, you must manually set the advertise peer URLs explicitly.

### `--initial-cluster`

+ the initial cluster configuration for bootstrapping
+ default: "{name}=http://{advertise-peer-url}"
+ For example, if `name` is "pd", and `advertise-peer-urls` is "http://127.0.0.1:2380,http://127.0.0.1:2381", the `initial-cluster` is "pd=http://127.0.0.1:2380,pd=http://127.0.0.1:2381".

### `--join`

+ join the cluster dynamically
+ default: ""
+ If you want to join an existing cluster, you can use `--join="${advertise-client-urls}"`, the `advertise-client-url` is any existing PD's, multiply advertise client urls are separated by comma.

## TiKV

TiKV supports some human readable conversion.

 - File size (based on byte): KB, MB, GB, TB, PB (or lowercase)
 - Time (based on ms): ms, s, m, h

### `-A, --addr`

+ the server listening address
+ default: "127.0.0.1:20160"

### `--advertise-addr`

+ the server advertise address for client traffic.
+ default: ${addr}
+ + If the client cannot connect to TiKV through the default listening address, you must manually set the advertise address explicitly.

### `-L, --Log`

+ the log level
+ default: "info"
+ You can choose from trace, debug, info, warn, error, or off.

### `--log-file`
+ the log file
+ default: ""
+ If this flag is not set, logs will be written to stderr. Otherwise, logs will be stored in the log file which will be automatically rotated every day.

### `-C, --config`

+ the config file
+ default: ""
+ If you set the configuration using the command line, the same setting in the config file will be overwritten.

### `--data-dir`

+ the path to the data directory
+ default: "/tmp/tikv/store"

### `--capacity`

+ the store capacity
+ default: 0 (unlimited)
+ PD uses this flag to determine how to balance the TiKV servers. (Tip: you can use 10GB instead of 1073741824)
