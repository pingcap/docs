---
title: TiKV Key Metrics
summary: Learn some key metrics displayed on the Grafana TiKV dashboard.
category: operations
---

# TiKV Key Metrics

If you use Ansible to deploy the TiDB cluster, the monitoring system is deployed at the same time. For more information, see [Overview of the Monitoring Framework](../op-guide/monitor-overview.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and so on. A lot of metrics are there to help you diagnose.

You can get an overview of the component TiKV status from the TiKV dashboard, where the key metrics are displayed. This document provides a detailed description of these key metrics.

## Key metrics description

To understand the key metrics displayed on the Overview dashboard, check the following table:

Row Name | Panel Name | Description | Normal Range
---------------- | ---------------- | ---------------------------------- | --------------
Cluster | store size | The storage size of each TiKV instance |
Cluster | available size | The available capacity size of each TiKV instance |
Cluster | capacity size | The capacity size of each TiKV instance |
Cluster | cpu | The cpu usage of each TiKV instance |
Cluster | memory | The memory usage of each TiKV instance |
Cluster | io utilization | The io utilization of each TiKV instance |
Cluster | MBps | The total bytes and keys of read and write on each TiKV instance |
Cluster | QPS | The QPS of different kinds of commands in each TiKV instance |
Cluster | Errps | The total number of the gRPC message failure |
Cluster | leader | The number of leaders on each TiKV instance |
Cluster | region | The number of Regions on each TiKV instance |
Errors | server is busy | It contains some kinds of events such as write stall, channel full, scheduler busy, and coprocessor full, which will make the TiKV instance unavailable temporarily. |
Errors | server report failures | The total number of reporting failure messages | It should be `0` in normal case.
Errors | raftstore error | The number of different raftstore errors on each TiKV instance |
Errors | scheduler error | The number of different scheduler errors on each TiKV instance |
Errors | coprocessor error | The number of different coprocessor errors on each TiKV instance |
Errors | grpc message error | The number of different gRPC message errors on each TiKV instance |
Errors | leader drop | The count of dropped leader in each TiKV instance |
Errors | leader missing | The count of missing leader in each TiKV instance |
Server | leader | The number of leaders on each TiKV instance |
Server | region | The number of Regions on each TiKV instance |
Server | cf size | The total size of each column family |
Server | store size | The storage size of each TiKV instance |
Server | channel full | The total number of channel full errors on each TiKV instance | It should be `0` in normal case.
Server | server report failures | The total number of reporting failure messages |
Server | region average written keys | The average rate of writing keys to Regions on each TiKV instance |
Server | region average written bytes | The average rate of writing bytes to Regions on each TiKV instance |
Server | active written leaders | The number of active leaders on each TiKV instance |
Server | approximate region size | The approximate Region size | 
Raft IO | apply log duration | The time consumed when Raft apply log |
Raft IO | apply log duration per server | The time consumed when Raft apply log on each TiKV instance |
Raft IO | append log duration | The time consumed when Raft append log |
Raft IO | append log duration per server | The time consumed when Raft append log on each TiKV instance |
Raft Process | ready handled | The count of different ready type of Raft |
Raft Process | process ready duration per server | The time consumed when peer processing ready in Raft | It should be less than `2s` in `.9999`.
Raft Process | process tick duration per server | The time consumed when peer processing tick in Raft |
Raft Process | 0.99 duration of raft store events | The time consumed of raftstore events in `.99` |
Raft Message | sent messages per server | The number of sending Raft messages of each TiKV instance |
Raft Message | flush messages per server | The number of flushing Raft messages of each TiKV instance |
Raft Message | recv messages per server | The number of receiving Raft messages of each TiKV instance |
Raft Message | messages | The number of sending different types of Raft messages  |
Raft Message | vote | The total number of vote messages is sent in Raft |
Raft Message | raft dropped messages | The number of dropping different types of Raft messages |
Raft Propose | raft proposals per ready | The proposal count of all Regions in a mio tick |
Raft Propose | raft read/write proposals | The total number of different kinds of proposals |
Raft Propose | raft read proposals per server | The number of read proposals which are made by each TiKV instance |
Raft Propose | raft write proposals per server | The number of write proposals which are made by each TiKV instance |
Raft Propose | propose wait duration | The wait time of each proposal |
Raft Propose | propose wait duration per server | The wait time of each proposal in each TiKV instance |
Raft Propose | raft log speed | The speed of peers propose log |
Raft Admin | admin proposals | The number of admin proposals |
Raft Admin | admin apply | The number of the processed apply command |
Raft Admin | check split | The number of raftstore split check |
Raft Admin | 99.99% check split duration | The time consumed when running split check in `.9999` |
Local Reader | local reader requests | The number of rejections from the local read thread and The number of total requests |
Local Reader | local read requests duration | The wait time of local read requests |
Local Reader | local read requests batch size | The batch size of local read requests |
Storage | storage command total | The total count of different kinds of commands received |
Storage | storage async request error | The total number of engine asynchronous request errors |
Storage | storage async snapshot duration | The time consumed by processing asynchronous snapshot requests | It should be less than `1s` in `.99`.
Storage | storage async write duration | The time consumed by processing asynchronous write requests | It should be less than `1s` in `.99`.
Scheduler | scheduler stage total | The total number of commands on each stage | There should not be lots of errors in a short time.
Scheduler | scheduler priority commands | The count of different priority commands |
Scheduler | scheduler pending commands | The count of pending commands on each TiKV instance |
Scheduler - batch_get | scheduler stage total | The total number of commands on each stage in batch_get command | There should not be lots of errors in a short time.
Scheduler - batch_get | scheduler command duration | The time consumed when execting batch_get command | It should be less than `1s`.
Scheduler - batch_get | scheduler latch wait duration | The time which is caused by latch wait in batch_get command | It should be less than `1s`.
Scheduler - batch_get | scheduler keys read | The count of keys read by a batch_get command |
Scheduler - batch_get | scheduler keys written | The count of keys written by a batch_get command |
Scheduler - batch_get | scheduler scan details | The keys scan details of each cf when executing batch_get command |
Scheduler - batch_get | scheduelr scan details [lock] | The keys scan details of lock cf when executing batch_get command |
Scheduler - batch_get | scheduelr scan details [write] | The keys scan details of write cf when executing batch_get command |
Scheduler - batch_get | scheduelr scan details [default] | The keys scan details of default cf when executing batch_get command |
Scheduler - cleanup | scheduler stage total | The total number of commands on each stage in cleanup command | There should not be lots of errors in a short time. 
Scheduler - cleanup | scheduler command duration | The time consumed when execting cleanup command | It should be less than `1s`.
Scheduler - cleanup | scheduler latch wait duration | The time which is caused by latch wait in cleanup command | It should be less than `1s`.
Scheduler - cleanup | scheduler keys read | The count of keys read by a cleanup command |
Scheduler - cleanup | scheduler keys written | The count of keys written by a cleanup command |
Scheduler - cleanup | scheduler scan details | The keys scan details of each cf when executing cleanup command |
Scheduler - cleanup | scheduelr scan details [lock] | The keys scan details of lock cf when executing cleanup command |
Scheduler - cleanup | scheduelr scan details [write] | The keys scan details of write cf when executing cleanup command |
Scheduler - cleanup | scheduelr scan details [default] | The keys scan details of default cf when executing cleanup command |
Scheduler - commit | scheduler stage total | The total number of commands on each stage in commit command | There should not be lots of errors in a short time. 
Scheduler - commit | scheduler command duration | The time consumed when execting commit command | It should be less than `1s`.
Scheduler - commit | scheduler latch wait duration | The time which is caused by latch wait in commit command | It should be less than `1s`. 
Scheduler - commit | scheduler keys read | The count of keys read by a commit command |
Scheduler - commit | scheduler keys written | The count of keys written by a commit command |
Scheduler - commit | scheduler scan details | The keys scan details of each cf when executing commit command |
Scheduler - commit | scheduelr scan details [lock] | The keys scan details of lock cf when executing commit command |
Scheduler - commit | scheduelr scan details [write] | The keys scan details of write cf when executing commit command |
Scheduler - commit | scheduelr scan details [default] | The keys scan details of default cf when executing commit command |
Scheduler - gc | scheduler stage total | The total number of commands on each stage in gc command | There should not be lots of errors in a short time. 
Scheduler - gc | scheduler command duration | The time consumed when execting gc command | It should be less than `1s`.
Scheduler - gc | scheduler latch wait duration | The time which is caused by latch wait in gc command | It should be less than `1s`.
Scheduler - gc | scheduler keys read | The count of keys read by a gc command |
Scheduler - gc | scheduler keys written | The count of keys written by a gc command |
Scheduler - gc | scheduler scan details | The keys scan details of each cf when executing gc command |
Scheduler - gc | scheduelr scan details [lock] | The keys scan details of lock cf when executing gc command |
Scheduler - gc | scheduelr scan details [write] | The keys scan details of write cf when executing gc command |
Scheduler - gc | scheduelr scan details [default] | The keys scan details of default cf when executing gc command |
Scheduler - get | scheduler stage total | The total number of commands on each stage in get command | There should not be lots of errors in a short time. 
Scheduler - get | scheduler command duration | The time consumed when execting get command | It should be less than `1s`.
Scheduler - get | scheduler latch wait duration | The time which is caused by latch wait in get command | It should be less than `1s`.
Scheduler - get | scheduler keys read | The count of keys read by a get command |
Scheduler - get | scheduler keys written | The count of keys written by a get command |
Scheduler - get | scheduler scan details | The keys scan details of each cf when executing get command |
Scheduler - get | scheduelr scan details [lock] | The keys scan details of lock cf when executing get command |
Scheduler - get | scheduelr scan details [write] | The keys scan details of write cf when executing get command |
Scheduler - get | scheduelr scan details [default] | The keys scan details of default cf when executing get command |
Scheduler - key_mvcc | scheduler stage total | The total number of commands on each stage in key_mvcc command | There should not be lots of errors in a short time. 
Scheduler - key_mvcc | scheduler command duration | The time consumed when execting key_mvcc command | It should be less than `1s`.
Scheduler - key_mvcc | scheduler latch wait duration | The time which is caused by latch wait in key_mvcc command | It should be less than `1s`.
Scheduler - key_mvcc | scheduler keys read | The count of keys read by a key_mvcc command |
Scheduler - key_mvcc | scheduler keys written | The count of keys written by a key_mvcc command |
Scheduler - key_mvcc | scheduler scan details | The keys scan details of each cf when executing key_mvcc command |
Scheduler - key_mvcc | scheduelr scan details [lock] | The keys scan details of lock cf when executing key_mvcc command |
Scheduler - key_mvcc | scheduelr scan details [write] | The keys scan details of write cf when executing key_mvcc command |
Scheduler - key_mvcc | scheduelr scan details [default] | The keys scan details of default cf when executing key_mvcc command |
Scheduler - prewrite | scheduler stage total | The total number of commands on each stage in prewrite command | There should not be lots of errors in a short time. 
Scheduler - prewrite | scheduler command duration | The time consumed when execting prewrite command | It should be less than `1s`.
Scheduler - prewrite | scheduler latch wait duration | The time which is caused by latch wait in prewrite command | It should be less than `1s`.
Scheduler - prewrite | scheduler keys read | The count of keys read by a prewrite command |
Scheduler - prewrite | scheduler keys written | The count of keys written by a prewrite command |
Scheduler - prewrite | scheduler scan details | The keys scan details of each cf when executing prewrite command |
Scheduler - prewrite | scheduelr scan details [lock] | The keys scan details of lock cf when executing prewrite command |
Scheduler - prewrite | scheduelr scan details [write] | The keys scan details of write cf when executing prewrite command |
Scheduler - prewrite | scheduelr scan details [default] | The keys scan details of default cf when executing prewrite command |
Scheduler - resolve_lock | scheduler stage total | The total number of commands on each stage in resolve_lock command | There should not be lots of errors in a short time. 
Scheduler - resolve_lock | scheduler command duration | The time consumed when execting resolve_lock command | It should be less than `1s`.
Scheduler - resolve_lock | scheduler latch wait duration | The time which is caused by latch wait in resolve_lock command | It should be less than `1s`.
Scheduler - resolve_lock | scheduler keys read | The count of keys read by a resolve_lock command |
Scheduler - resolve_lock | scheduler keys written | The count of keys written by a resolve_lock command |
Scheduler - resolve_lock | scheduler scan details | The keys scan details of each cf when executing resolve_lock command |
Scheduler - resolve_lock | scheduelr scan details [lock] | The keys scan details of lock cf when executing resolve_lock command |
Scheduler - resolve_lock | scheduelr scan details [write] | The keys scan details of write cf when executing resolve_lock command |
Scheduler - resolve_lock | scheduelr scan details [default] | The keys scan details of default cf when executing resolve_lock command |
Scheduler - scan | scheduler stage total | The total number of commands on each stage in scan command | There should not be lots of errors in a short time. 
Scheduler - scan | scheduler command duration | The time consumed when execting scan command | It should be less than `1s`.
Scheduler - scan | scheduler latch wait duration | The time which is caused by latch wait in scan command | It should be less than `1s`.
Scheduler - scan | scheduler keys read | The count of keys read by a scan command |
Scheduler - scan | scheduler keys written | The count of keys written by a scan command |
Scheduler - scan | scheduler scan details | The keys scan details of each cf when executing scan command |
Scheduler - scan | scheduelr scan details [lock] | The keys scan details of lock cf when executing scan command |
Scheduler - scan | scheduelr scan details [write] | The keys scan details of write cf when executing scan command |
Scheduler - scan | scheduelr scan details [default] | The keys scan details of default cf when executing scan command |
Scheduler - scan_lock | scheduler stage total | The total number of commands on each stage in scan_lock command | There should not be lots of errors in a short time.
Scheduler - scan_lock | scheduler command duration | The time consumed when execting scan_lock command | It should be less than `1s`.
Scheduler - scan_lock | scheduler latch wait duration | The time which is caused by latch wait in scan_lock command | It should be less than `1s`.
Scheduler - scan_lock | scheduler keys read | The count of keys read by a scan_lock command |
Scheduler - scan_lock | scheduler keys written | The count of keys written by a scan_lock command |
Scheduler - scan_lock | scheduler scan details | The keys scan details of each cf when executing scan_lock command |
Scheduler - scan_lock | scheduelr scan details [lock] | The keys scan details of lock cf when executing scan_lock command |
Scheduler - scan_lock | scheduelr scan details [write] | The keys scan details of write cf when executing scan_lock command |
Scheduler - scan_lock | scheduelr scan details [default] | The keys scan details of default cf when executing scan_lock command |
Scheduler - start_ts_mvcc | scheduler stage total | The total number of commands on each stage in start_ts_mvcc command | There should not be lots of errors in a short time. 
Scheduler - start_ts_mvcc | scheduler command duration | The time consumed when execting start_ts_mvcc command | It should be less than `1s`.
Scheduler - start_ts_mvcc | scheduler latch wait duration | The time which is caused by latch wait in start_ts_mvcc command | It should be less than `1s`.
Scheduler - start_ts_mvcc | scheduler keys read | The count of keys read by a start_ts_mvcc command |
Scheduler - start_ts_mvcc | scheduler keys written | The count of keys written by a start_ts_mvcc command |
Scheduler - start_ts_mvcc | scheduler scan details | The keys scan details of each cf when executing start_ts_mvcc command |
Scheduler - start_ts_mvcc | scheduelr scan details [lock] | The keys scan details of lock cf when executing start_ts_mvcc command |
Scheduler - start_ts_mvcc | scheduelr scan details [write] | The keys scan details of write cf when executing start_ts_mvcc command |
Scheduler - start_ts_mvcc | scheduelr scan details [default] | The keys scan details of default cf when executing start_ts_mvcc command |
Scheduler - unsafe_destroy_range | scheduler stage total | The total number of commands on each stage in unsafe_destroy_range command | There should not be lots of errors in a short time.
Scheduler - unsafe_destroy_range | scheduler command duration | The time consumed when execting unsafe_destroy_range command | It should be less than `1s`.
Scheduler - unsafe_destroy_range | scheduler latch wait duration | The time which is caused by latch wait in unsafe_destroy_range command | It should be less than `1s`.
Scheduler - unsafe_destroy_range | scheduler keys read | The count of keys read by a unsafe_destroy_range command |
Scheduler - unsafe_destroy_range | scheduler keys written | The count of keys written by a unsafe_destroy_range command |
Scheduler - unsafe_destroy_range | scheduler scan details | The keys scan details of each cf when executing unsafe_destroy_range command |
Scheduler - unsafe_destroy_range | scheduelr scan details [lock] | The keys scan details of lock cf when executing unsafe_destroy_range command |
Scheduler - unsafe_destroy_range | scheduelr scan details [write] | The keys scan details of write cf when executing unsafe_destroy_range command |
Scheduler - unsafe_destroy_range | scheduelr scan details [default] | The keys scan details of default cf when executing unsafe_destroy_range command |
Coprocessor | Request Duration | The time consumed when handling coprocessor read requests |
Coprocessor | Wait Duration | The time consumed when coprocessor requests are wait for being handled | It should be less than `10s` in `.9999`.
Coprocessor | Handle Duration | The time consumed when handling coprocessor requests |
Coprocessor | 95% Request Duration by Store | The time consumed when handling coprocessor read requests in each TiKV instance |
Coprocessor | 95% Wait Duration by Store | The time consumed when coprocessor requests are wait for being handled in each TiKV instance |
Coprocessor | 95% Handle Duration by Store | The time consumed when handling coprocessor requests in each TiKV instance |
Coprocessor | Request Errors | The total number of the push down request errors | There should not be lots of errors in a short time.
Coprocessor | DAG Executors | The total number of DAG executors |
Coprocessor | Scan Keys | The number of keys that each request scans |
Coprocessor | Scan Details | The scan details for each CF |
Coprocessor | Table Scan - Details by CF | The table scan details for each CF |
Coprocessor | Index Scan - Details by CF | The index scan details for each CF |
Coprocessor | Table Scan - Perf Statistics | The total number of RocksDB internal operations from PerfContext when executing table scan |
Coprocessor | Index Scan - Perf Statistics | The total number of RocksDB internal operations from PerfContext when executing index scan |
GC | MVCC Versions | The number of versions for each key |
GC | MVCC Delete Versions | The number of versions deleted by GC for each key |
GC | GC Tasks | The count of GC tasks processed by gc_worker |
GC | GC Tasks Duration | The time consumed when executing GC tasks |
GC | GC Keys (write_cf) | The count of keys in write CF affected during GC |
GC | TiDB GC Actions Result | The TiDB GC action result on Region level |
GC | TiDB GC Worker Actions | The count of TiDB GC worker actions |
GC | TiDB GC Seconds | The time consumed when TiDB is doing GC |
GC | TiDB GC Failure | The count of TiDB GC job failure |
GC | GC LifeTime | The lifetime of TiDB GC |
GC | GC interval | The interval of TiDB GC |
Snapshot | rate snapshot message | The rate of Raft snapshot messages sent |
Snapshot | 99% handle snapshot duration | The time consumed when handling snapshots |
Snapshot | snapshot state count | The number of snapshots in different states |
Snapshot | 99.99% snapshot size | The snapshot size in `.9999`  |
Snapshot | 99.99% snapshot kv count | The number of KV within a snapshot in `.9999`  |
Task | Worker Handled Tasks | The number of tasks handled by worker |
Task | Worker Pending Tasks | Current pending and running tasks of worker | It should be less than `1000`.
Task | FuturePool Handled Tasks | The number of tasks handled by future_pool |
Task | FuturePool Pending Tasks | Current pending and running tasks of future_pool |
Thread CPU | raft store CPU | The CPU utilization of raftstore thread | The CPU usage should be less than `80%`.
Thread CPU | async apply CPU | The CPU utilization of async apply | The CPU usage should be less than `90%`.
Thread CPU | scheduler CPU | The CPU utilization of scheduler | The CPU usage should be less than `80%`.
Thread CPU | Scheduler Worker CPU | The CPU utilization of scheduler worker |
Thread CPU | Storage ReadPool CPU | The CPU utilization of readpool |
Thread CPU | Coprocessor CPU | The CPU utilization of coprocessor |
Thread CPU | snapshot work CPU | The CPU utilization of snapshot work |
Thread CPU | split check CPU | The CPU utilization of split check |
Thread CPU | rocksdb CPU | The CPU utilization of rocksdb |
Thread CPU | grpc poll CPU | The CPU utilization of gRPC | The CPU usage should be less than `80%`.
Rocksdb - kv | Get Operations | The count of get operations |
Rocksdb - kv | Get Duration | The time consumed when execting get operation |
Rocksdb - kv | Seek Operations | The count of seek operations |
Rocksdb - kv | Seek Duration | The time consumed when execting seek operation |
Rocksdb - kv | Write Operations | The count of write operations |
Rocksdb - kv | Write Duration | The time consumed when execting write operation |
Rocksdb - kv | WAL Sync Operations | The count of WAL sync operations |
Rocksdb - kv | WAL Sync Duration | The time consumed when execting WAL sync operation |
Rocksdb - kv | Compaction Operations | The count of compaction and flush operations |
Rocksdb - kv | Compaction Duration | The time consumed when execting compaction and flush operation |
Rocksdb - kv | SST Read Duration | The time consumed when reading SST files |
Rocksdb - kv | Write Stall Duration | The time which is caused by write stall | It should be `0` in normal case.
Rocksdb - kv | Memtable Size | The memtable size of each column family |
Rocksdb - kv | Memtable Hit | The hit rate of memtable |
Rocksdb - kv | Block Cache Size | The block cache size of each column family |
Rocksdb - kv | Block Cache Hit | The hit rate of block cache |
Rocksdb - kv | Block Cache Flow | The flow of different kinds of block cache operations |
Rocksdb - kv | Block Cache Operations | The count of different kinds of block cache operations |
Rocksdb - kv | Keys Flow | The flow of different kinds of operations on keys |
Rocksdb - kv | Total Keys | The count of keys in each column family |
Rocksdb - kv | Read Flow | The flow of different kinds of read operations |
Rocksdb - kv | Bytes / Read | The bytes per read |
Rocksdb - kv | Write Flow | The flow of different kinds of write operations |
Rocksdb - kv | Bytes / Write | The bytes per write |
Rocksdb - kv | Compaction Flow | The flow of different kinds of compaction operations |
Rocksdb - kv | Compaction Pending Bytes | The pending bytes when executing compaction |
Rocksdb - kv | Read Amplification | The read amplification in each TiKV instance |
Rocksdb - kv | Compression Ratio | The compression ratio of each level |
Rocksdb - kv | Number of Snapshots | The number of snapshot of each TiKV instance |
Rocksdb - kv | Oldest Snapshots Duration | The time that the oldest unreleased snapshot survivals |
Rocksdb - kv | Number files at each level | The number of SST files for different column families in each level |
Rocksdb - kv | Ingest SST duration seconds | The time consumed when ingesting SST files |
Rocksdb - kv | Stall conditions changed of each CF | Stall conditions changed of each column family |
Rocksdb - raft | Get Operations | The count of get operations |
Rocksdb - raft | Get Duration | The time consumed when execting get operation |
Rocksdb - raft | Seek Operations | The count of seek operations |
Rocksdb - raft | Seek Duration | The time consumed when execting seek operation |
Rocksdb - raft | Write Operations | The count of write operations |
Rocksdb - raft | Write Duration | The time consumed when execting write operation |
Rocksdb - raft | WAL Sync Operations | The count of WAL sync operations |
Rocksdb - raft | WAL Sync Duration | The time consumed when execting WAL sync operation |
Rocksdb - raft | Compaction Operations | The count of compaction and flush operations |
Rocksdb - raft | Compaction Duration | The time consumed when execting compaction and flush operation |
Rocksdb - raft | SST Read Duration | The time consumed when reading SST files |
Rocksdb - raft | Write Stall Duration | The time which is caused by write stall | It should be `0` in normal case.
Rocksdb - raft | Memtable Size | The memtable size of each column family |
Rocksdb - raft | Memtable Hit | The hit rate of memtable |
Rocksdb - raft | Block Cache Size | The block cache size of each column family |
Rocksdb - raft | Block Cache Hit | The hit rate of block cache |
Rocksdb - raft | Block Cache Flow | The flow of different kinds of block cache operations |
Rocksdb - raft | Block Cache Operations | The count of different kinds of block cache operations |
Rocksdb - raft | Keys Flow | The flow of different kinds of operations on keys |
Rocksdb - raft | Total Keys | The count of keys in each column family |
Rocksdb - raft | Read Flow | The flow of different kinds of read operations |
Rocksdb - raft | Bytes / Read | The bytes per read |
Rocksdb - raft | Write Flow | The flow of different kinds of write operations |
Rocksdb - raft | Bytes / Write | The bytes per write |
Rocksdb - raft | Compaction Flow | The flow of different kinds of compaction operations |
Rocksdb - raft | Compaction Pending Bytes | The pending bytes when executing compaction |
Rocksdb - raft | Read Amplification | The read amplification in each TiKV instance |
Rocksdb - raft | Compression Ratio | The compression ratio of each level |
Rocksdb - raft | Number of Snapshots | The number of snapshot of each TiKV instance |
Rocksdb - raft | Oldest Snapshots Duration | The time that the oldest unreleased snapshot survivals |
Rocksdb - raft | Number files at each level | The number of SST files for different column families in each level |
Rocksdb - raft | Ingest SST duration seconds | The time consumed when ingesting SST files |
Rocksdb - raft | Stall conditions changed of each CF | Stall conditions changed of each column family |
Grpc | grpc message count | The count of different kinds of gRPC message |
Grpc | grpc message failed | The count of different kinds of gRPC message which is failed |
Grpc | 99% grpc message duration | The execution time of gRPC message |
Grpc | grpc gc message count | The count of gRPC GC message |
Grpc | 99% grpc kv_gc message duration | The execution time of gRPC GC message |
PD | PD requests | The count of requests that TiKV sends to PD |
PD | PD request duration (average) | The time consumed by requests that TiKV sends to PD |
PD | PD heartbeats | The total number of PD heartbeat messages |
PD | PD validate peers | The total number of PD worker validate peer task |

## Interface of the TiKV dashboard

![TiKV Dashboard](../media/tikv_dashboard.png)
