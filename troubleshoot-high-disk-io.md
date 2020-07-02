---
title: Troubleshoot High Disk I/O Usage in TiDB
summary: Learn how to locate and address the issue of high TiDB storage I/O usage.
category: reference
---

# The processing method of TiDB disk io usage is too high

This article mainly introduces how to locate and deal with the problem of high TiDB disk I/O usage.

## Confirm the current I/O indicators

When the system response slows down, if the bottleneck of the CPU and the bottleneck of data transaction conflicts have been investigated, you need to start with I/O indicators to help determine the current system bottleneck.

### Locate I/O problems from monitor

The fastest position method is to view the overall I/O situation from the monitor. You can view the correspond I/O monitor from the Grafana monitor component, which is deployed by the default cluster deployment tool (TiDB-Ansible, TiUP). The Dashboard relate to I/O has `Overview`, `Node_exporter`, `Disk-Performance`.

#### The first type of panel

In `Overview`> `System Info`> `IO Util`, you can see the I/O status of each machine in the cluster. This indicator is similar to util in Linux iostat monitor. The higher percentage represents the higher disk I/O usage:

- If there is only one machine with high I/O in the monitor, it can assist in judging that there are currently reading and writing hot spots.
- If the I/O of most machines in the monitor is high, then the cluster now has a high I/O load.

If you find that the I/O of a certain machine is relatively high, you can further monitor the use of I/O from monitor `Disk-Performance Dashboard`, combined with metrics such as `Disk Latency` and `Disk Load` to determine whether there is an abnormality, and if necessary use the fio tool to test the disk.

#### The second type of panel

The main persistence component of the TiDB cluster is TiKV cluster. One TiKV instance contains two RocksDB instances: one for storing Raft logs, located in data/raft, and one for storing real data, located in data/db.

In `TiKV-Details`> `Raft IO`, you can see the relevant metrics for disk writes of these two instances:

- `Append log duration`: This monitor indicates the response time of RocksDB writes that store Raft logs. The .99 response should be within 50ms.
- `Apply log duration`: This monitor indicates the response time for RocksDB writes that store real data. The .99 response should be within 100ms.

These two monitors also have `.. per server` monitor panels to provide assistance to view hotspot writes.

#### The third type of panel

In `TiKV-Details`> `Storage`, there are monitor related to storage:

- `Storage command total`: the number of different commands received.
- `Storage async write duration`: includes monitor items such as disk sync duration, which may be related to Raft IO. If you encounter an abnormal situation, you need to check the working status of related components by logs.

#### Other panels

In addition, some other content may be needed to help locate whether the bottleneck is I/O, and you can try to set some recommended parameters. By checking the prewrite/commit/raw-put of TiKV gRPC (raw kv cluster only) duration, it is confirmed that TiKV write is indeed slow. Several common situations are as follows:

- Append log is slow. TiKV Grafana's Raft I/O and append log duration are relatively high. Usually, it is due to slow disk writing. You can check the value of WAL Sync Duration max of RocksDB-raft to confirm, otherwise you may need to report a bug.
- The raftstore thread is busy. TiKV grafana's Raft Propose/propose wait duration is significantly higher than append log duration. Please check the following two points:

    - Is the `store-pool-size` configuration of `[raftstore]` too small (this value is recommended between [1,5], not too large).
    - Is machine's CPU insufficient.

- Apply log is slow. TiKV Grafana's Raft I/O and apply log duration are relatively high, usually accompanied by a relatively high Raft Propose/apply wait duration. The possible situations are as follows:
  
    - The `apply-pool-size` configuration of `[raftstore]` is too small (recommended between [1, 5], not recommended to be too large), Thread CPU/apply cpu is relatively high;
    - The machine's CPU resources are not enough.
    - Region write hotspot issue, the CPU usage of a single apply thread is relatively high (by modifying the Grafana expression, plus by (instance, name) to see the CPU usage of each thread), temporarily for the hot write of a single Region is no solution, this scene is being optimized recently.
    - It is slow to write RocksDB, and the RocksDB kv/max write duration is relatively high (a single Raft log may contain many kvs. When writing RocksDB, 128 kvs will be written to RocksDB in a batch write, so one apply log may involve multiple RocksDB writes).
    - In other cases, bugs need to be reported.

- Raft commit log is slow. TiKV Grafana's Raft I/O and commit log duration are relatively high (this metric is only available in Grafana 4.x). Each Region corresponds to an independent Raft group. Raft has a flow control mechanism, similar to the sliding window mechanism of TCP, through the parameter [raftstore] raft-max-inflight-msgs = 256 to control the size of the sliding window, if there is a hot spot Write and commit log duration is relatively high, you can moderately change the parameters, such as 1024.

### Locate I/O problems from log

- If the client reports `server is busy` error, especially the error message of `raftstore is busy`, it will be related to I/O problem.

    You can check the monitor: grafana -> TiKV -> errors to confirm the specific busy reason. Among them, `server is busy` is TiKV's flow control mechanism. In this way, TiKV informs `tidb/ti-client` that the current pressure of TiKV is too high, and try again later.

- "Write stall" appears in TiKV RocksDB logs.

    It may be that too much level0 sst causes stalls. You can add the parameter `[rocksdb] max-sub-compactions = 2 (or 3)` to speed up the compaction of level0 sst. This parameter means that the compaction tasks of level0 to level1 can be divided into `max-sub-compactions` subtasks to multi-threaded concurrent execution.

    If the disk's I/O capability fail to keep up with the write, it is recommended to scale-in. If the throughput of the disk reaches the upper limit (for example, the throughput of SATA SSD will be much lower than that of NVME SSD), resulting in write stall, but the CPU resource is relatively sufficient, you can try to use a higher compression ratio compression algorithm to relieve the pressure on the disk, use CPU resources Change disk resources.
    
    For example, when the pressure of `default cf compaction` is relatively high, you can change the parameter`[rocksdb.defaultcf] compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd" , "zstd"]`  to `compression-per-level = ["no", "no", "zstd", "zstd", "zstd", "zstd", "zstd"]`.

### I/O problem found from alarm

The cluster deployment tool (TiDB-Ansible, TiUP) is an alarm component that is deployed by default. Officials have preset related alarm items and thresholds. I/O related items include:

- TiKV_write_stall
- TiKV_raft_log_lag
- TiKV_async_request_snapshot_duration_seconds
- TiKV_async_request_write_duration_seconds
- TiKV_raft_append_log_duration_secs
- TiKV_raft_apply_log_duration_secs

## I/O problem handling plan

1. When it is confirmed as a I/O hotspot issue, you need to refer to [TiDB Hot Issue Processing] (/troubleshoot-hot-spot-issues.md) to eliminate the related I/O hotspot situation.
2. When it is confirmed that the overall I/O has reached the bottleneck, and the ability to judge the I/O from the business side will continue to keep up, then you can take advantage of the distributed database's scale capability and adopt the scheme of expanding the number of TiKV nodes to obtain greater overall I/O throughput.
3. Adjust some of the parameters in the above description, and use computing/memory resources in exchange for disk storage resources.
