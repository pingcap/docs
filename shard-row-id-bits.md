---
title: SHARD_ROW_ID_BITS
summary: 了解 SHARD_ROW_ID_BITS 属性。
---

# SHARD_ROW_ID_BITS

本文档介绍了 `SHARD_ROW_ID_BITS` 表属性，用于设置在隐式 `_tidb_rowid` 被分片后，分片的位数。

## 概念

对于具有非聚簇主键或没有主键的表，TiDB 使用隐式的自增行 ID。当执行大量的 `INSERT` 操作时，数据会写入单个 Region，导致写入热点。

为了解决热点问题，你可以配置 `SHARD_ROW_ID_BITS`。行 ID 会被分散，数据会写入多个不同的 Region。

- `SHARD_ROW_ID_BITS = 4` 表示 16 个分片
- `SHARD_ROW_ID_BITS = 6` 表示 64 个分片
- `SHARD_ROW_ID_BITS = 0` 表示默认的 1 个分片

<CustomContent platform="tidb">

关于用法的详细信息，请参见 [Troubleshoot Hotspot Issues guide](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)。

</CustomContent>

<CustomContent platform="tidb-cloud">

关于用法的详细信息，请参见 [Troubleshoot Hotspot Issues guide](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots)。

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