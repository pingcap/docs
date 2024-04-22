---
title: Overview of TiDB Backup & Restore Architecture
summary: TiDBは複数のタイプのクラスターデータのバックアップと復元をサポートします。バックアップと復元(BR)とTiDB Operatorを使用して、TiKVノードからデータをバックアップしたり、復元したりするタスクを作成できます。各バックアップおよび復元機能のアーキテクチャの詳細については、次のドキュメントを参照してください。フルデータのバックアップと復元には、スナップショットデータをバックアップするとスナップショットバックアップデータの復元があります。データ変更ログのバックアップには、ログバックアップ：KVデータ変更のバックアップがあります。また、ポイントインタイムリカバリ(PITR)もサポートされています。
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
