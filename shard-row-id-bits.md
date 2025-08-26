---
title: SHARD_ROW_ID_BITS
summary: 了解 SHARD_ROW_ID_BITS 属性。
---

# SHARD_ROW_ID_BITS

本文介绍了 `SHARD_ROW_ID_BITS` 表属性，该属性用于设置隐式 `_tidb_rowid` 分片后的分片位数。

## 概念

对于没有聚簇主键或没有主键的表，TiDB 会使用隐式自增行 ID。当执行大量 `INSERT` 操作时，数据会写入到单个 Region，导致写入热点问题。

为缓解热点问题，你可以配置 `SHARD_ROW_ID_BITS`。这样行 ID 会被打散，数据会写入到多个不同的 Region。

- `SHARD_ROW_ID_BITS = 4` 表示 16 个分片
- `SHARD_ROW_ID_BITS = 6` 表示 64 个分片
- `SHARD_ROW_ID_BITS = 0` 表示默认的 1 个分片

当你设置 `SHARD_ROW_ID_BITS = S` 时，`_tidb_rowid` 的结构如下：

| 符号位 | 分片位 | 自增位 |
|--------|--------|--------------|
| 1 位 | `S` 位 | `63-S` 位 |

- 自增位的值存储在 TiKV 中，并按顺序分配。每次分配一个值，下一个值递增 1。自增位保证了 `_tidb_rowid` 列的值在全局范围内唯一。当自增位的值被耗尽（即达到最大值时），后续的自动分配会失败，并报错 `Failed to read auto-increment value from storage engine`。
- `_tidb_rowid` 的取值范围：最终生成值的最大位数 = 分片位数 + 自增位数，因此最大值为 `(2^63)-1`。

> **Note:**
>
> 分片位（`S`）的选择：
>
> - 由于 `_tidb_rowid` 总共为 64 位，分片位数会影响自增位数：分片位数增加时，自增位数减少，反之亦然。因此，你需要在自增值的随机性和可用的自增空间之间进行权衡。
> - 最佳实践是将分片位设置为 `log(2, x)`，其中 `x` 为集群中 TiKV 节点的数量。例如，如果 TiDB 集群中有 16 个 TiKV 节点，建议将分片位设置为 `log(2, 16)`，即 `4`。当所有 Region 被均匀调度到每个 TiKV 节点后，大批量写入的负载可以均匀分布到不同的 TiKV 节点，从而最大化资源利用率。

<CustomContent platform="tidb">

关于用法的详细信息，请参见 [热点问题排查指南](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)。

</CustomContent>

<CustomContent platform="tidb-cloud">

关于用法的详细信息，请参见 [热点问题排查指南](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots)。

</CustomContent>

## 示例

```sql
CREATE TABLE t (
    id INT PRIMARY KEY NONCLUSTERED
) SHARD_ROW_ID_BITS = 4;
```

```sql
ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```