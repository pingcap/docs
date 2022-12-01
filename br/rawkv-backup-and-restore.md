---
title: Back Up and Restore RawKV
summary: Learn how to back up and restore RawKV using BR.
---

# Back Up and Restore RawKV

TiKV and PD can constitute a KV database when used without TiDB, which is called RawKV. TiKV-BR supports data backup and restore for products that use RawKV. TiKV-BR can also upgrade the [`api-version`](https://docs.pingcap.com/tidb/stable/tikv-configuration-file) with converting the RawKV data from `API V1` to `API V2`. 

For more detail, please see [TiKV-BR User Doc](https://tikv.org/docs/dev/concepts/explore-tikv-features/backup-restore/).
