---
title: TiDB Data Migration Shard Merge
summary: DM のシャードマージ機能について学習します。
---

# TiDB データ移行シャードマージ {#tidb-data-migration-shard-merge}

TiDB データ移行 (DM) は、アップストリーム MySQL/MariaDB シャード テーブル内の DML および DDL データのマージと、マージされたデータのダウンストリーム TiDB テーブルへの移行をサポートします。

小さなデータセットの MySQL シャードを TiDB に移行してマージする必要がある場合は、 [このチュートリアル](/migrate-small-mysql-shards-to-tidb.md)を参照してください。

## 制限 {#restrictions}

現在、シャードマージ機能は限られたシナリオでのみサポートされています。詳細については、 [シャーディングDDLの使用悲観的モードでの制限](/dm/feature-shard-merge-pessimistic.md#restrictions)と[シャーディングDDLの使用楽観的モードでの制限](/dm/feature-shard-merge-optimistic.md#restrictions)を参照してください。

## パラメータを設定する {#configure-parameters}

タスク設定ファイルで、 `shard-mode`を`pessimistic`に設定します。

```yaml
shard-mode: "pessimistic"
# The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default
# which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic"
# mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you
# can set it to the "optimistic" mode.
```

## シャーディングDDLロックを手動で処理する {#handle-sharding-ddl-locks-manually}

異常なシナリオでは、 [シャーディングDDLロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)実行する必要があります。
