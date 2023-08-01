---
title: TiDB Data Migration Shard Merge
summary: Learn the shard merge feature of DM.
---

# TiDB データ移行シャード マージ {#tidb-data-migration-shard-merge}

TiDB データ移行 (DM) は、アップストリームの MySQL/MariaDB シャード テーブル内の DML データと DDL データのマージと、マージされたデータのダウンストリーム TiDB テーブルへの移行をサポートします。

小規模なデータセットの MySQL シャードを TiDB に移行してマージする必要がある場合は、 [このチュートリアル](/migrate-small-mysql-shards-to-tidb.md)を参照してください。

## 制限 {#restrictions}

現在、シャード マージ機能は限られたシナリオでのみサポートされています。詳細は[シャーディング DDL の使用法悲観的モードでの制限事項](/dm/feature-shard-merge-pessimistic.md#restrictions) 、 [シャーディング DDL の使用法楽観的モードでの制限事項](/dm/feature-shard-merge-optimistic.md#restrictions)を参照してください。

## パラメータを設定する {#configure-parameters}

タスク構成ファイルで、 `shard-mode` ～ `pessimistic`を設定します。

```yaml
shard-mode: "pessimistic"
# The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default
# which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic"
# mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you
# can set it to the "optimistic" mode.
```

## シャーディング DDL ロックを手動で処理する {#handle-sharding-ddl-locks-manually}

一部の異常なシナリオでは、 [DDL ロックのシャーディングを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)を行う必要があります。
