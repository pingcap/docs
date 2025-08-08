---
title: Overview of TiDB Backup & Restore Architecture
summary: TiDBは、Backup & Restore（BR）とTiDB Operatorを使用したクラスタデータのバックアップとリストアをサポートしています。TiKVノードからデータをバックアップし、TiKVノードにデータをリストアするタスクを作成できます。アーキテクチャには、フルデータバックアップとリストア、データ変更ログバックアップ、ポイントインタイムリカバリ（PITR）が含まれます。詳細については、各機能のドキュメントを参照してください。
---

# TiDB バックアップとリストアのアーキテクチャの概要 {#overview-of-tidb-backup-x26-restore-architecture}

[TiDB バックアップと復元の概要](/br/backup-and-restore-overview.md)で説明したように、TiDB は複数の種類のクラスターデータのバックアップとリストアをサポートしています。Backup &amp; Restore (BR) とTiDB Operatorを使用してこれらの機能にアクセスし、TiKV ノードからデータをバックアップしたり、TiKV ノードにデータをリストアしたりするタスクを作成できます。

各バックアップおよび復元機能のアーキテクチャの詳細については、次のドキュメントを参照してください。

-   完全なデータのバックアップと復元

    -   [スナップショットデータをバックアップする](/br/br-snapshot-architecture.md#process-of-backup)
    -   [スナップショットバックアップデータを復元する](/br/br-snapshot-architecture.md#process-of-restore)

-   データ変更ログのバックアップ

    -   [ログバックアップ: KVデータの変更のバックアップ](/br/br-log-architecture.md#process-of-log-backup)

-   ポイントインタイムリカバリ（PITR）

    -   [PITR](/br/br-log-architecture.md#process-of-pitr)
