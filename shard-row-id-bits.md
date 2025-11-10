---
title: SHARD_ROW_ID_BITS
summary: Learn the SHARD_ROW_ID_BITS attribute.
---

# SHARD_ROW_ID_BITS

This document introduces the `SHARD_ROW_ID_BITS` table attribute, which is used to set the number of bits of the shards after the implicit `_tidb_rowid` is sharded.

## Concept

For the tables with a non-clustered primary key or no primary key, TiDB uses an implicit auto-increment row ID. When a large number of `INSERT` operations are performed, the data is written into a single Region, causing a write hot spot.

To mitigate the hot spot issue, you can configure `SHARD_ROW_ID_BITS`. The row IDs are scattered and the data are written into multiple different Regions.

- `SHARD_ROW_ID_BITS = 4` indicates 16 shards
- `SHARD_ROW_ID_BITS = 6` indicates 64 shards
- `SHARD_ROW_ID_BITS = 0` indicates the default 1 shard

When you set `SHARD_ROW_ID_BITS = S`, the structure of `_tidb_rowid` is as follows:

| Sign bit |  Shard bits | Auto-increment bits |
|--------|--------|--------------|
| 1 bit | `S` bits | `63-S` bits |

- The values of the auto-increment bits are stored in TiKV and allocated sequentially. Each time a value is allocated, the next value is incremented by 1. The auto-increment bits ensure that the column values of `_tidb_rowid` are unique globally. When the value of the auto-increment bits is exhausted (that is, when the maximum value is reached), subsequent automatic allocations fail with the error `Failed to read auto-increment value from storage engine`.
- The value range of `_tidb_rowid`: the maximum number of bits for the final generated value = shard bits + auto-increment bits, so the maximum value is `(2^63)-1`.

> **Note:**
>
> Selection of shard bits (`S`):
>
> - Because the total bits of `_tidb_rowid` is 64, the number of shard bits affects the number of auto-increment bits: when the number of shard bits increases, the number of auto-increment bits decreases, and vice versa. Therefore, you need to balance the randomness of the auto-increment values and the available auto-increment space.
> - The best practice is to set the shard bits to `log(2, x)`, where `x` is the number of TiKV nodes in the cluster. For example, if there are 16 TiKV nodes in a TiDB cluster, it is recommended to set the shard bits to `log(2, 16)`, which equals `4`. After all Regions are evenly scheduled to each TiKV node, the load of bulk writes can be evenly distributed to different TiKV nodes to maximize resource utilization.

<CustomContent platform="tidb">

For details on the usage, see [the Troubleshoot Hotspot Issues guide](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots).

</CustomContent>

<CustomContent platform="tidb-cloud">

For details on the usage, see [the Troubleshoot Hotspot Issues guide](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots).

</CustomContent>

## Examples

```sql
CREATE TABLE t (
    id INT PRIMARY KEY NONCLUSTERED
) SHARD_ROW_ID_BITS = 4;
```

```sql
ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```
