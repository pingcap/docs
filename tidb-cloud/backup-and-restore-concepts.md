---
title: Backup & Restore
summary: TiDB Cloudのバックアップと復元の概念について学習します。
---

# バックアップと復元 {#backup-x26-restore}

TiDB Cloud のバックアップと復元機能は、クラスター データをバックアップおよび復元できるようにすることで、データを保護し、ビジネスの継続性を確保するように設計されています。

## 自動バックアップ {#automatic-backup}

TiDB Cloud Serverless クラスターとTiDB Cloud Dedicated クラスターの両方で、スナップショット バックアップはデフォルトで自動的に作成され、バックアップ保持ポリシーに従って保存されます。

詳細については、以下を参照してください。

-   [TiDB Cloud Serverless クラスターの自動バックアップ](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
-   [TiDB Cloud Dedicated クラスターの自動バックアップ](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## 手動バックアップ {#manual-backup}

手動バックアップは、必要に応じてデータを既知の状態にバックアップし、いつでもその状態に復元できるTiDB Cloud Dedicated の機能です。

詳細については[手動バックアップを実行する](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup)参照してください。

## デュアルリージョンバックアップ {#dual-region-backup}

デュアル リージョン バックアップは、クラスター リージョンから別のリージョンにバックアップを複製できるTiDB Cloud Dedicated の機能です。この機能を有効にすると、すべてのバックアップが指定されたリージョンに自動的に複製されます。これにより、リージョン間のデータ保護と災害復旧機能が提供されます。約 99% のデータが 1 時間以内にセカンダリ リージョンに複製されると推定されます。

詳細については[デュアルリージョンバックアップをオンにする](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)参照してください。

## ポイントインタイム復元 {#point-in-time-restore}

ポイントインタイム リストアは、任意の時点のデータを新しいクラスターに復元できる機能です。この機能を使用すると、次のことができます。

-   災害復旧における RPO を削減します。
-   エラー イベント前の時点を復元することで、データ書き込みエラーのケースを解決します。
-   ビジネスの履歴データを監査します。

ポイントインタイム リストアを実行する場合は、次の点に注意してください。

-   TiDB Cloud Serverless クラスターの場合、ポイントインタイム リストアはスケーラブル クラスターでのみ使用でき、無料クラスターでは使用できません。詳細については、 [復元モード](/tidb-cloud/backup-and-restore-serverless.md#restore-mode)参照してください。
-   TiDB Cloud Dedicated クラスターの場合は、事前に[PITRを有効にする](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)が必要です。
