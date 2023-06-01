---
title: Overview of TiDB Backup & Restore Architecture
summary: Learn about the architecture design of TiDB backup and restore features.
---

# TiDB バックアップおよび復元アーキテクチャの概要 {#overview-of-tidb-backup-x26-restore-architecture}

[<a href="/br/backup-and-restore-overview.md">TiDB のバックアップと復元の概要</a>](/br/backup-and-restore-overview.md)で説明したように、TiDB は複数のタイプのクラスター データのバックアップと復元をサポートしています。バックアップと復元 (BR) とTiDB Operatorを使用してこれらの機能にアクセスし、TiKV ノードからデータをバックアップしたり、TiKV ノードにデータを復元したりするタスクを作成できます。

各バックアップおよび復元機能のアーキテクチャの詳細については、次のドキュメントを参照してください。

-   フルデータのバックアップと復元

    -   [<a href="/br/br-snapshot-architecture.md#process-of-backup">スナップショットデータをバックアップする</a>](/br/br-snapshot-architecture.md#process-of-backup)
    -   [<a href="/br/br-snapshot-architecture.md#process-of-restore">スナップショットバックアップデータの復元</a>](/br/br-snapshot-architecture.md#process-of-restore)

-   データ変更ログのバックアップ

    -   [<a href="/br/br-log-architecture.md#process-of-log-backup">ログバックアップ：KVデータ変更のバックアップ</a>](/br/br-log-architecture.md#process-of-log-backup)

-   ポイントインタイムリカバリ (PITR)

    -   [<a href="/br/br-log-architecture.md#process-of-pitr">PITR</a>](/br/br-log-architecture.md#process-of-pitr)
