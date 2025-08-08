---
title: Backup & Restore
summary: TiDB Cloudのバックアップと復元の概念について学習します。
---

# バックアップと復元 {#backup-x26-restore}

TiDB Cloud のバックアップと復元機能は、クラスター データのバックアップと復元を可能にして、データを保護し、ビジネスの継続性を確保するように設計されています。

## 自動バックアップ {#automatic-backup}

TiDB Cloud Serverless クラスターとTiDB Cloud Dedicated クラスターの両方で、スナップショット バックアップはデフォルトで自動的に作成され、バックアップ保持ポリシーに従って保存されます。

詳細については、以下を参照してください。

-   [TiDB Cloud Serverless クラスターの自動バックアップ](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
-   [TiDB Cloud Dedicated クラスターの自動バックアップ](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## 手動バックアップ {#manual-backup}

手動バックアップは、必要に応じてデータを既知の状態にバックアップし、いつでもその状態に復元できるTiDB Cloud Dedicated の機能です。

詳細については[手動バックアップを実行する](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup)参照してください。

## デュアルリージョンバックアップ {#dual-region-backup}

デュアルリージョンバックアップは、 TiDB Cloud Dedicatedの機能で、クラスタリージョンから別のリージョンにバックアップを複製できます。この機能を有効にすると、すべてのバックアップが指定されたリージョンに自動的に複製されます。これにより、リージョンをまたいだデータ保護とディザスタリカバリ機能が実現します。1時間以内に約99%のデータがセカンダリリージョンに複製されると推定されます。

詳細については[デュアルリージョンバックアップをオンにする](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)参照してください。

## ポイントインタイムリストア {#point-in-time-restore}

ポイントインタイムリストアは、任意の時点のデータを新しいクラスターに復元できる機能です。この機能を使用すると、以下のことが可能になります。

-   災害復旧における RPO を削減します。
-   エラー イベントの前の時点を復元することにより、データ書き込みエラーのケースを解決します。
-   ビジネスの履歴データを監査します。

ポイントインタイム リストアを実行する場合は、次の点に注意してください。

-   TiDB Cloud Serverless クラスターでは、ポイントインタイムリストアはスケーラブルクラスターでのみ利用可能であり、無料クラスターでは利用できません。詳細については、 [復元モード](/tidb-cloud/backup-and-restore-serverless.md#restore-mode)ご覧ください。
-   TiDB Cloud Dedicated クラスターの場合は、事前に[PITRを有効にする](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)実行する必要があります。
