---
title: TiDB Log Backup and PITR Architecture
summary: TiDB log backup and PITR architecture is introduced using a Backup & Restore (BR) tool as an example. The architecture includes log backup process design, system components, and key concepts. The PITR process involves restoring full backup data and log backup data. Log backup generates files such as log data, metadata, and global checkpoint.
---

# TiDB Log Backup and PITR 架构

本文介绍了以 Backup & Restore (BR) 工具为例的 TiDB 日志备份与点-in-时间恢复（PITR）架构与流程。

## 架构

日志备份与 PITR 架构如下：

![BR log backup and PITR architecture](/media/br/br-log-arch.png)

## 日志备份流程

集群日志备份的流程如下：

![BR log backup process design](/media/br/br-log-backup-ts.png)

涉及的系统组件与关键概念：

* **local metadata**：表示由单个 TiKV 节点备份的元数据，包括本地 checkpoint ts、全局 checkpoint ts 和备份文件信息。
* **local checkpoint ts**（在本地元数据中）：表示在该 TiKV 节点中，所有在此时间点之前生成的日志已被备份到目标存储。
* **global checkpoint ts**：表示所有 TiKV 节点中在此时间点之前生成的日志已被备份到目标存储。TiDB Coordinator 通过收集所有 TiKV 节点的 local checkpoint ts 计算得出，并报告给 PD。
* **TiDB Coordinator**：由 TiDB 节点选举产生，负责收集和计算整个日志备份任务的进度（global checkpoint ts）。该组件为无状态设计，故障后由存活的 TiDB 节点中选举出新的 Coordinator。
* **TiKV log backup observer**：运行在 TiDB 集群中的每个 TiKV 节点上，负责备份日志数据。如果某个 TiKV 节点故障，区域重选后由其他 TiKV 节点接管其数据范围的备份，这些节点将从 global checkpoint ts 开始备份故障范围内的数据。

完整的备份流程如下：

1. BR 接收 `br log start` 命令。

   * BR 解析 checkpoint ts（日志备份的起始时间）和备份任务的存储路径。
   * **Register log backup task**：BR 在 PD 中注册日志备份任务。

2. TiKV 监控日志备份任务的创建和更新。

   * **Fetch log backup task**：每个 TiKV 节点的 log backup observer 从 PD 获取日志备份任务，然后在指定范围内备份日志数据。

3. 日志备份观察者持续备份 KV 变更日志。

   * **Read kv change data**：读取 KV 变更数据，并将变更日志保存到[自定义格式的备份文件](#log-backup-files)中。
   * **Fetch global checkpoint ts**：从 PD 获取 global checkpoint ts。
   * **Generate local metadata**：生成备份任务的本地元数据，包括 local checkpoint ts、global checkpoint ts 和备份文件信息。
   * **Upload log data & metadata**：定期将备份文件和本地元数据上传到目标存储。
   * **Configure GC**：请求 PD 阻止未备份的数据（大于 local checkpoint ts）被 TiDB GC 机制回收。

4. TiDB Coordinator 监控日志备份任务的进度。

   * **Watch backup progress**：通过轮询所有 TiKV 节点获取每个 Region（Region checkpoint ts）的备份进度。
   * **Report global checkpoint ts**：根据 Region checkpoint ts 计算整个日志备份任务的进度（global checkpoint ts），并报告给 PD。

5. PD 持久化日志备份任务的状态，可以通过 `br log status` 查看。

## PITR 流程

点-in-时间恢复（PITR）的流程如下：

![Point-in-time recovery process design](/media/br/pitr-ts.png)

完整的 PITR 流程如下：

1. BR 接收 `br restore point` 命令。

   * BR 解析全备数据地址、日志备份数据地址和点-in-时间恢复时间。
   * 查询备份数据中的还原对象（数据库或表），并检查待还原的表是否存在且符合还原要求。

2. BR 还原全备数据。

   * 还原全备数据。关于快照备份数据还原的详细流程，参考 [Restore snapshot backup data](/br/br-snapshot-architecture.md#process-of-restore)。

3. BR 还原日志备份数据。

   * **Read backup data**：读取日志备份数据，计算需要还原的日志数据。
   * **Fetch Region info**：通过访问 PD 获取所有 Region 的分布信息。
   * **Request TiKV to restore data**：创建日志还原请求并发送给对应的 TiKV 节点。该请求包含待还原的日志备份数据信息。

4. TiKV 接受 BR 的还原请求并启动日志还原工作。

   * 日志还原工作获取需要还原的日志备份数据。

5. TiKV 还原日志备份数据。

   * **Download KVs**：日志还原工作根据还原请求，从备份存储下载对应的备份数据到本地目录。
   * **Rewrite KVs**：日志还原工作根据还原集群表的表 ID 重写 KV 数据，即用新表 ID 替换 [Key-Value](/tidb-computing.md#mapping-table-data-to-key-value) 中的原始表 ID。还原工作也会以相同方式重写索引 ID。
   * **Apply KVs**：日志还原工作通过 raft 接口将处理后的 KV 数据写入存储（RocksDB）。
   * **Report restore result**：日志还原工作将还原结果返回给 BR。

6. BR 接收每个 TiKV 节点的还原结果。

   * 如果部分数据因 `RegionNotFound` 或 `EpochNotMatch` 等原因未能还原，例如某个 TiKV 节点宕机，BR 会重试还原。
   * 如果有数据无法还原且无法重试，整个还原任务失败。
   * 所有数据还原完成后，还原任务成功。

## 日志备份文件

日志备份会生成以下类型的文件：

- `{resolved_ts}-{uuid}.meta` 文件：每次每个 TiKV 节点上传日志备份数据时生成，存储本次上传的所有日志备份文件的元数据。`{resolved_ts}` 为 TiKV 节点的 resolved timestamp。日志备份任务的最新 `resolved_ts` 为所有 TiKV 节点中最小的 resolved timestamp。`{uuid}` 在文件创建时随机生成。
- `{store_id}.ts` 文件：每次每个 TiKV 节点上传日志备份数据时更新，存储全局 checkpoint ts。`{store_id}` 为 TiKV 节点的存储 ID。
- `{min_ts}-{uuid}.log` 文件：存储备份任务的 KV 变更日志数据。`{min_ts}` 为该文件中 KV 变更日志数据的最小 TSO 时间戳，`{uuid}` 在文件创建时随机生成。
- `v1_stream_truncate_safepoint.txt` 文件：存储由 `br log truncate` 删除的存储中最新备份数据对应的时间戳。

### 备份文件结构

```
.
├── v1
│   ├── backupmeta
│   │   ├── ...
│   │   └── {resolved_ts}-{uuid}.meta
│   ├── global_checkpoint
│   │   └── {store_id}.ts
│   └── {date}
│       └── {hour}
│           └── {store_id}
│               ├── ...
│               └── {min_ts}-{uuid}.log
└── v1_stream_truncate_safepoint.txt
```

备份文件目录结构说明：

- `backupmeta`：存储备份元数据。文件名中的 `resolved_ts` 表示备份进度，意味着该 TSO 之前的数据已完全备份。但请注意，该 TSO 仅反映某些分片的备份进度。
- `global_checkpoint`：代表全局备份进度，记录可以用 `br restore point` 还原的最新时间点。
- `{date}/{hour}`：存储对应日期和小时的备份数据。清理存储时，建议使用 `br log truncate`，而非手动删除数据。因为元数据引用了该目录中的数据，手动删除可能导致还原失败或还原后数据不一致。

示例：

```
.
├── v1
│   ├── backupmeta
│   │   ├── ...
│   │   ├── 435213818858112001-e2569bda-a75a-4411-88de-f469b49d6256.meta
│   │   ├── 435214043785779202-1780f291-3b8a-455e-a31d-8a1302c43ead.meta
│   │   └── 435214443785779202-224f1408-fff5-445f-8e41-ca4fcfbd2a67.meta
│   ├── global_checkpoint
│   │   ├── 1.ts
│   │   ├── 2.ts
│   │   └── 3.ts
│   └── 20220811
│       └── 03
│           ├── 1
│           │   ├── ...
│           │   ├── 435213866703257604-60fcbdb6-8f55-4098-b3e7-2ce604dafe54.log
│           │   └── 435214023989657606-72ce65ff-1fa8-4705-9fd9-cb4a1e803a56.log
│           ├── 2
│           │   ├── ...
│           │   ├── 435214102632857605-11deba64-beff-4414-bc9c-7a161b6fb22c.log
│           │   └── 435214417205657604-e6980303-cbaa-4629-a863-1e745d7b8aed.log
│           └── 3
│               ├── ...
│               ├── 435214495848857605-7bf65e92-8c43-427e-b81e-f0050bd40be0.log
│               └── 435214574492057604-80d3b15e-3d9f-4b0c-b133-87ed3f6b2697.log
└── v1_stream_truncate_safepoint.txt
```