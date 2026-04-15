---
title: Backup & Restore
summary: TiDB Cloudのバックアップと復元に関する概念について学びましょう。
---

# バックアップと復元 {#backup-x26-restore}

TiDB Cloudバックアップ＆リストア機能は、データのバックアップと復元を可能にすることで、お客様のデータを保護し、事業継続性を確保するように設計されています。

## 自動バックアップ {#automatic-backup}

TiDB Cloudでは、スナップショットバックアップはデフォルトで自動的に取得され、バックアップ保持ポリシーに従って保存されます。

詳細については、以下を参照してください。

-   [TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスの自動バックアップ](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
-   [TiDB Cloud Dedicatedクラスターの自動バックアップ](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## 手動バックアップ {#manual-backup}

TiDB Cloud Dedicatedの手動バックアップ機能は、必要に応じてデータを既知の状態にバックアップし、いつでもその状態に復元できる機能です。

詳細については、 [手動バックアップを実行する](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup)参照してください。

## デュアルリージョンバックアップ {#dual-region-backup}

TiDB Cloud Dedicatedのデュアルリージョンバックアップ機能は、クラスタリージョンから別のリージョンへバックアップを複製できる機能です。この機能を有効にすると、すべてのバックアップが指定されたリージョンに自動的に複製されます。これにより、リージョンをまたいだデータ保護とディザスタリカバリ機能が実現します。データの約99%は1時間以内にセカンダリリージョンに複製できると推定されています。

詳細については、 [デュアルリージョンバックアップを有効にする](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)参照してください。

## 特定時点への復元 {#point-in-time-restore}

ポイントインタイム復元は、任意の時点のデータを新しい TiDB クラスターまたはインスタンスに復元できる機能です。この機能は、以下の目的で使用できます。

-   ディザスタリカバリにおけるRPO（目標復旧時点）を削減する。
-   データ書き込みエラーが発生した場合は、エラー発生前の時点にデータを復元することで解決します。
-   企業の過去のデータを監査する。

ポイントインタイム復元を実行する場合は、以下の点に注意してください。

-   TiDB Cloud Starterインスタンスでは、特定時点への復元機能は利用できません。
-   TiDB Cloud Essentialインスタンスの場合、過去 30 日間の任意の時点に復元できます。詳細については、 [復元モード](/tidb-cloud/backup-and-restore-serverless.md#restore-mode)参照してください。
-   TiDB Cloud Dedicatedクラスターの場合、事前に[PITRを有効にする](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)必要があります。
