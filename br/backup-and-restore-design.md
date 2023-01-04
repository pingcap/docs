---
title: Overview of TiDB Backup & Restore Architecture
summary: Learn about the architecture design of TiDB backup and restore features.
---

# TiDB のバックアップと復元のアーキテクチャの概要 {#overview-of-tidb-backup-x26-restore-architecture}

[TiDB のバックアップと復元の概要](/br/backup-and-restore-overview.md)で説明したように、TiDB は複数の種類のクラスター データのバックアップと復元をサポートしています。 Backup &amp; Restore (BR) とTiDB Operatorを使用してこれらの機能にアクセスし、タスクを作成して TiKV ノードからデータをバックアップしたり、TiKV ノードにデータを復元したりできます。

各バックアップおよび復元機能のアーキテクチャの詳細については、次のドキュメントを参照してください。

-   完全なデータのバックアップと復元

    -   [スナップショット データのバックアップ](/br/br-snapshot-architecture.md#process-of-backup)
    -   [スナップショット バックアップ データの復元](/br/br-snapshot-architecture.md#process-of-restore)

-   データ変更ログのバックアップ

    -   [ログバックアップ：KVデータ変更のバックアップ](/br/br-log-architecture.md#process-of-log-backup)

-   ポイントインタイムリカバリ (PITR)

    -   [PITR](/br/br-log-architecture.md#process-of-pitr)
