# Configuration flags

TiDB/TiKV/PD are configurable through command-line flags and environment variables.


##TiDB

The default TiDB ports are 4000 for client requests and 10080 for status report.

### --store
+ the storage engine type
+ Human-readable name for this member.
+ default: "goleveldb"
+ You can choose from "memory", "goleveldb", "BoltDB" or "TiKV". The first three are all local storage engines. TiKV is a distributed storage engine.

### --path
+ the path to the data directory for local storage engines like goleveldb, BoltDB, or memory or the DSN for the distributed storage engine like TiKV. If you use TiKV, specify the path in the following format: $Host:$Port/pd?cluster=$ClusterID.
+ default: "/tmp/tidb"

### -L
+ the log level
+ default: "debug"
+ You can choose from debug, info, warn, error, or fatal.

### -P
+ the listening port for TiDB server
+ default: "4000"
+ TiDB server will accept MySQL client request from this port.

### --status
+ the status report port for TiDB server
+ default: "10080"
+ This is used to get server status.

### --lease
+ the schema lease time in seconds
+ default: "1"
+ This is the schema lease time that is used in online schema changes. The value will affect the DDL statement running time. Do not change it unless you understand the internal mechanism.

### --socket
+ the socket file for connection
+ default: ""
+ You can use the "/tmp/tidb.sock" file.

### --perfschema
+ enable(1) or disable(0) the performance schema
+ default: "0"
+ the value can be (1) or (0). (1) is to enable and (0) is to disable. The Performance Schema provides a way to inspect internal execution of the server at runtime. See [performance schema](http://dev.mysql.com/doc/refman/5.7/en/performance-schema.html) for more information. If you enable the performance schema, the performance will be affected.

### $TIDB_PPROF environment variable
+ An environment variable that is used to enable or disable the runtime profiling data via the HTTP server. The Address is at client URL + "/debug/pprof/".
+ If set $TIDB_PPROF to 0, TiDB will disable pprof. Otherwise TiDB will enable pprof.

## Placement Driver (PD)

### -L

+ the log level
+ default: "info"
+ You can choose from debug, info, warn, error, or fatal.

### -c 

+ the config file
+ default: ""

### --cluster-id

+ the cluster ID to identify unique cluster 
+ default: 0
+ You must use a unique ID to distinguish different clusters. 

### name

+ the human-readable unique name for this PD member
+ default: "pd"
+ If you want to start multiply PDs, you must use different name for each one.

### --host

+ the server host
+ default: "127.0.0.1"
+ You must set this flag so that it can be connected from outside. You can only ignore it in the standalone mode.

### --data-dir

+ the path to the data directory
+ default: "default.${name}"

### --client-port

+ the listening port for client traffic
+ default: 2379
+ The listening address is `0.0.0.0:${client-port}`.

### --advertise-client-port

+ the advertise port for client traffic
+ default: ${client-port}
+ If you use Docker to start PD, and use different ports to map the listening client port, you must set this flag. For example, if you use `-p 12379:2379`, the advertise client port must be 12379 through which the client can connect to PD.

### --peer-port

+ the listening port for peer traffic
+ default 2380
+ The listening address is `0.0.0.0:${peer-port}`.

### --advertise-peer-port

+ the advertise port for peer traffic
+ default: ${peer-port}
+ If you use Docker to start PD, and use different ports to map the listening peer port, you must set this flag. For example, if you use `-p 12380:2380`, the advertise peer port must be 12380 for other peers to connect to.

### --initial-cluster

+ the initial cluster configuration for bootstrapping 
+ default: "{name}=http://{host}:{advertise-peer-port}"
+ You must set this flag to bootstrap PD cluster. For example, if you have three PDs (pd1, pd2, pd3), the initial cluster is "pd1=http://pd1_host:2380,pd2=http://pd2_host:2380,pd3=http://pd3_host:2380".
+ Note: this flag will be deprecated later.

### --initial-cluster-state

+ the initial cluster state ("new" or "existing")
+ default: "new"
+ Note: this flag will be deprecated later.

### --port

+ the listening port for client traffic
+ default: 1234
+ The listening address is `0.0.0.0:${port}`.
+ Note: this flag will be deprecated later.

### --advertise-port

+ the server advertise port for client traffic
+ default: ${port}
+ If you use Docker to start PD, and use different ports to map the listening port, you must set this flag. For example, if you use `-p 11234:1234`, the advertise port must be 11234 through which the client can connect to PD.
+ Note: this flag will be deprecated later.

### --http-port

+ the server http port
+ default: 9090
+ Note: this flag will be deprecated later.

## TiKV

### -P, --port

+ the server listening port for outer traffic
+ default: 20160
+ The listening address is `0.0.0.0:${port}`.

### --advertise-port

+ the server advertise port for outer traffic
+ default: ${port}
+ If you use Docker to start TiKV, and use different ports to map the listening port, you must set this flag. For example, if you use `-p 20161:20160`, the advertise port must be 20161 through which the client can connect to TiKV.

### -H, --host

+ the server host
+ default: "127.0.0.1"
+ You must set this flag so that it can be connected from outside. You can only ignore it in the standalone mode.

### -L, --Log

+ the log level
+ default: "info"
+ You can choose from trace, debug, info, warn, error, or off.

### -C, --config

+ the config file
+ default: ""

### -s, --store

+ the path to the data directory
+ default: "/tmp/tikv/store"

### --capacity

+ the store capacity
+ default: 0 (unlimited)
+ PD uses this flag to determine how to balance this TiKV.

### -S, --dsn

+ the DSN to use, "rocksdb" or "raftkv"
+ default: "rocksdb"
+ You must set the value to "raftkv" in production, because "rocksdb" is for local test only.

### -I, --cluster-id

+ the unique ID to distinguish cluster
+ default: 0
+ The cluster ID must be the same as PD's.

### --pd

+ the pd endpoints
+ default: "127.0.0.1:2379"
+ You must set this flag to let TiKV connect to PD. Multiple endpoints are separated by comma, for example, "pd1:2379,pd2:2379".