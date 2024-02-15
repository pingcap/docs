---
title: Overview of TiDB Backup & Restore Architecture
summary: TiDB supports backup and restore for cluster data using Backup & Restore (BR) and TiDB Operator. Tasks can be created to back up data from TiKV nodes and restore data to TiKV nodes. The architecture includes full data backup and restore, data change log backup, and point-in-time recovery (PITR). For details, refer to specific documents for each feature.
---

# TiDB バックアップおよび復元アーキテクチャの概要 {#overview-of-tidb-backup-x26-restore-architecture}

[TiDB のバックアップと復元の概要](/br/backup-and-restore-overview.md)で説明したように、TiDB は複数のタイプのクラスター データのバックアップと復元をサポートします。バックアップと復元 (BR) とTiDB Operatorを使用してこれらの機能にアクセスし、TiKV ノードからデータをバックアップしたり、TiKV ノードにデータを復元したりするタスクを作成できます。

各バックアップおよび復元機能のアーキテクチャの詳細については、次のドキュメントを参照してください。

-   フルデータのバックアップと復元

    -   [スナップショットデータをバックアップする](/br/br-snapshot-architecture.md#process-of-backup)
    -   [スナップショットバックアップデータの復元](/br/br-snapshot-architecture.md#process-of-restore)

-   データ変更ログのバックアップ

    -   [ログバックアップ：KVデータ変更のバックアップ](/br/br-log-architecture.md#process-of-log-backup)

-   ポイントインタイムリカバリ (PITR)

    -   [PITR](/br/br-log-architecture.md#process-of-pitr)
