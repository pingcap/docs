---
title: Back Up and Restore RawKV
summary: Learn how to back up and restore RawKV using BR.
---

# Back Up and Restore RawKV

TiKV and PD can constitute a KV database when used without TiDB, which is called RawKV. TiKV-BR supports data backup and restore for products that use RawKV. TiKV-BR can also upgrade the [`api-version`](https://docs.pingcap.com/tidb/stable/tikv-configuration-file) from `API V1` to `API V2` to convert RawKV data. 

With API v2, TiKV-BR can also cooperate with TiKV-CDC with finish the data backup and replication. Please see [TiKV-CDC User Docs](https://tikv.org/docs/dev/concepts/explore-tikv-features/cdc/cdc/#how-to-replicate-tikv-cluster-with-existing-data).


For more details, please see [TiKV-BR User Docs](https://tikv.org/docs/dev/concepts/explore-tikv-features/backup-restore/).
