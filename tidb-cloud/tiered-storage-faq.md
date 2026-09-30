---
title: 分层存储常见问题
summary: 了解 TiDB Cloud Premium 和 BYOC 中有关分层存储的常见问题，包括 DML、副本和对象存储故障。
---

# 分层存储常见问题

本文解答有关低频访问（IA）存储的常见问题，包括 DML 行为、副本处理、转换进度、缓存配置以及对象存储故障等运维影响。

> **注意：**
>
> 分层存储目前在 {{{ .premium }}} 和 {{{ .byoc }}} 中处于**私有预览**阶段，默认禁用。如需使用，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 为你的实例启用。本文描述的行为反映的是当前预览版实现，正式发布（GA）前可能会发生变化。

## IA 表可以执行 `UPDATE`/`DELETE` 吗？ {#can-ia-tables-execute-update-delete}

可以。`UPDATE` 操作会先将对应数据从对象存储加载到 IA 缓存中，执行修改后再写入新的 SST 文件，流程与常规 `UPDATE` 相同。性能会受到冷读的影响。

## IA 表的 TiFlash 副本可以设置为 IA 吗？ {#can-tiflash-replicas-of-ia-tables-be-set-to-ia}

不可以。TiFlash 不会继承源表的 IA 属性。

## 当对象存储发生故障时，IA 表会怎样？ {#what-happens-to-ia-tables-when-the-object-storage-experiences-an-outage}

IA 表会受到影响并变得不可用，因为所有数据都存放在远端，读请求必须从对象存储获取数据。此外，如果对象存储带宽饱和，IA 的读写性能也会受到影响。

## 在我设置 IA 之前，系统能告诉我哪些数据是冷数据吗？ {#can-the-system-tell-me-which-data-is-cold-before-i-set-ia}

TiDB 不提供内置的冷热数据检测工具。你需要根据自己的业务知识评估数据访问模式。一个通用经验是：对于按时间分区的表，较旧的分区通常访问频率更低。

## 当数据存储在冷存储（IA 层）中时，是存储三个副本，还是只存一份？ {#when-data-is-stored-in-cold-storage-ia-tier-are-all-three-replicas-stored-or-just-one-copy}

只会在 Amazon S3 上存储一份，三个副本共享同一个对象。

在云存储引擎架构中，SST/blob 数据文件在对象存储（S3/DFS）上本来就只有一份：文件由 flush/compaction 上传一次，S3 key 不包含节点/副本信息，三个 Raft 副本通过 Raft 复制的 ChangeSet 引用同一个 file id。三副本机制只适用于 Raft 日志、元信息以及每个节点的本地缓存，不适用于对象存储中的数据。

**成本影响**：S3 上的存储量始终约为数据大小的 1 倍（不会随着副本数增加而倍增）。IA 层节省的是每个节点上的本地磁盘使用量；数据持久性由对象存储本身保证，与副本数无关。

## 存储类转换需要多长时间？如何跟踪其进度？ {#how-long-does-a-storage-class-conversion-take-and-how-do-i-track-its-progress}

在转换进行期间，执行 `SHOW STORAGE_CLASS TRANSITIONS`。读取 `PROGRESS` 可查看完成比例，取值范围为 `0` 到 `1`；也可以比较 `COMPLETED_REPLICAS` 和 `TOTAL_REPLICAS`。读取 `DURATION` 可查看已耗时的秒数。进度每 10 秒采集一次，因此这些值不是实时的。

转换时长主要取决于数据量和转换方向。将表设置为 IA 只会修改元信息，因此速度较快；切换回 Standard 则需要从对象存储下载全部数据，因此耗时会长得多。若要估算你自己集群中的转换时长，可以查询 `mysql.tidb_storage_class_transition_history` 中类似历史转换的 `duration`，并按 `state = 'COMPLETED'` 进行过滤。

完整的列说明和查询示例，请参见[分层存储可观测性](/tidb-cloud/tiered-storage-observability.md)。

## 如果某个转换一直处于 `RUNNING` 状态且进度不再增加，该怎么办？ {#what-if-a-conversion-stays-in-running-and-the-progress-does-not-increase}

转换可能由于系统异常而卡住，例如 TiKV 滚动重启、资源暂时不足，或对象存储短时不可用。你可以结合观察 `DURATION` 和 `COMPLETED_REPLICAS` 来区分这两种情况：如果两者都在持续变化，则说明转换仍在正常推进，只是数据量较大。

你无法自行处理卡住的转换。请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。问题解决后，转换会继续进行，无需你执行任何额外操作。

## 如果在上一次转换完成前执行反向 `ALTER TABLE`，会发生什么？ {#what-happens-if-i-run-the-reverse-alter-table-before-the-previous-conversion-finishes}

之前的转换会失效。在 `SHOW STORAGE_CLASS TRANSITIONS` 中，该表或分区对应的行会被新的转换替换：转换方向会改变，进度也会重新从头开始计算。

在 `mysql.tidb_storage_class_transition_history` 中，已失效转换的历史记录会被更新为 `state = 'SUPERSEDED'`。其 `finish_time` 为新转换的开始时间，`completed_replicas` 和 `total_replicas` 则为失效前最后一次观测到的值。反转转换并不一定会丢弃所有已完成的工作。已经符合新目标的 Region 可以跳过，已有的本地文件在适用时也可以复用。

在统计转换时长时，请按 `state = 'COMPLETED'` 进行过滤：`SUPERSEDED` 记录中的 `duration` 只表示其失效前的持续时间，而不是一次完整转换的时长。

## 我可以增加 IA 数据的本地缓存吗？这样会增加成本吗？ {#can-i-increase-the-local-cache-for-ia-data-and-does-it-cost-more}

可以，但调整缓存级别除了需要启用分层存储预览外，还需要单独加入 allowlist。请先联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 启用该功能。然后在 **Overview** > **Capacity** > **Update Capacity** > **Storage Acceleration** 中选择更高的 IA 缓存级别。可用级别包括 **Economy**、**Default**、**Balanced** 和 **Deep**。级别越高，缓存在本地磁盘上的 IA 数据越多，冷读性能也越好。

这确实会增加成本。在 {{{ .premium }}} 中，每个缓存级别都有一个 IA 存储等效系数，从 **Economy** 的 0.9x 到 **Deep** 的 1.8x 不等，计费时会将该系数应用到你上报的 IA 存储用量上。在 {{{ .byoc }}} 中，不适用该系数：额外资源会在你自己的云账户中配置，并由你的云服务提供商计费。该变更属于热修改，无需重启。各级别的系数请参见 [TiDB Cloud 计费](/tidb-cloud/tidb-cloud-billing.md)。

请注意，缓存级别作用于底层 TiKV 物理集群，而不是单个逻辑实例。如果你的账户在同一个物理集群上运行多个逻辑实例，那么在一个实例上进行的修改也会应用到其他实例。

## 修改缓存级别或 segment size 会重写对象存储中的数据吗？ {#does-changing-the-cache-level-or-the-segment-size-rewrite-data-in-object-storage}

不会。修改缓存级别只会调整本地缓存中保留的数据量，并以热修改方式生效。

segment size（`kvengine.ia.segment-size`，仅在 {{{ .byoc }}} 中可用）只会改变从对象存储读取数据以及将数据写入本地缓存时的粒度。SST 文件在对象存储中是以完整对象形式存储的，并不会按 segment 组织，因此对象存储中的任何内容都不会被重写。该参数仅在启动时生效，因此需要对 TiKV 节点执行滚动重启，之后本地缓存会按新的粒度逐步重建。

## 我该如何判断某张表是否应该继续保留在 IA 中？ {#how-do-i-decide-whether-a-table-should-stay-in-ia}

比较 statement summary 表中的 `IA_EXEC_COUNT` 和 `EXEC_COUNT`，即可了解读取 IA 数据的执行占比，同时查看集群级别的 **IA Cache Hit Rate** 面板。

- 如果访问该表的大多数语句始终保持较高的冷读比例，说明 IA 的缓存命中率过低。可以考虑将该表切回 Standard，或提高缓存级别。
- 如果冷读比例较低，但少数语句每次都会读取大量数据，那么应优先优化这些语句，而不是将整张表切回。

## 我可以在哪里查看 IA 缓存命中率？ {#where-can-i-see-the-ia-cache-hit-rate}

在 Cloud Console 中，进入 **Monitoring** > **Metrics** > **Instance Overview**，然后打开 **IA Cache Performance** 面板组。该面板组包含缓存命中率、缓存未命中率、远程读取的 segment 数量与数据量，以及远程读取等待时间。

当命中率低于 85% 时，会显示黄色指示器。如果集群中没有 IA 表，这些面板会显示 **No IA data**。