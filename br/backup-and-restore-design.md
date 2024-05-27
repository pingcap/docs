---
title: Overview of TiDB Backup & Restore Architecture
summary: TiDB は、Backup & Restore (BR) とTiDB Operatorを使用して、クラスター データのバックアップと復元をサポートします。TiKV ノードからデータをバックアップし、TiKV ノードにデータを復元するタスクを作成できます。アーキテクチャには、完全なデータ バックアップと復元、データ変更ログのバックアップ、およびポイントインタイム リカバリ (PITR) が含まれます。詳細については、各機能の特定のドキュメントを参照してください。
---

# TiDB バックアップと復元アーキテクチャの概要 {#overview-of-tidb-backup-x26-restore-architecture}

[TiDB バックアップと復元の概要](/br/backup-and-restore-overview.md)で説明したように、TiDB は複数のタイプのクラスター データのバックアップと復元をサポートしています。Backup &amp; Restore (BR) とTiDB Operatorを使用してこれらの機能にアクセスし、TiKV ノードからデータをバックアップしたり、TiKV ノードにデータを復元したりするタスクを作成できます。

各バックアップおよび復元機能のアーキテクチャの詳細については、次のドキュメントを参照してください。

-   完全なデータバックアップと復元

    -   [スナップショットデータをバックアップする](/br/br-snapshot-architecture.md#process-of-backup)
    -   [スナップショットバックアップデータを復元する](/br/br-snapshot-architecture.md#process-of-restore)

-   データ変更ログのバックアップ

    -   [ログバックアップ: KVデータの変更のバックアップ](/br/br-log-architecture.md#process-of-log-backup)

-   ポイントインタイムリカバリ (PITR)

    -   [ピトル](/br/br-log-architecture.md#process-of-pitr)
