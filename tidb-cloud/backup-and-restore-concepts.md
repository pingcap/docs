---
title: Backup & Restore
summary: TiDB Cloudのバックアップと復元に関する概念について学びましょう。
---

# バックアップと復元 {#backup-x26-restore}

TiDB Cloudバックアップ＆リストア機能は、データのバックアップと復元を可能にすることで、お客様のデータを保護し、事業継続性を確保するように設計されています。

<CustomContent plan="byoc">

TiDB Cloud BYOC では、データプレーンをお客様自身のクラウドアカウントで実行しながら、TiDB Cloudコンソールを通じてバックアップおよび復元の操作を管理できます。これにより、データプレーンをお客様のクラウド環境内に保持したまま、マネージドなバックアップおよび復元の利用体験を提供します。

</CustomContent>

## 自動バックアップ {#automatic-backup}

TiDB Cloudでは、スナップショットバックアップはデフォルトで自動的に取得され、バックアップ保持ポリシーに従って保存されます。

詳細については、以下を参照してください。

- [TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスの自動バックアップ](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
- [TiDB Cloud Premium <CustomContent plan="byoc">および TiDB Cloud BYOC </CustomContent>インスタンスの自動バックアップ](/tidb-cloud/premium/backup-and-restore-premium.md#automatic-backups)
- [TiDB Cloud Dedicatedクラスターの自動バックアップ](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## 手動バックアップ {#manual-backup}

手動バックアップを使用すると、必要に応じてデータを既知の状態にバックアップし、その状態にいつでも復元できます。手動バックアップは、システムのアップグレード、重要なデータの削除、元に戻せないスキーマ変更などの高リスクな操作を実行する前に利用できます。

{{{ .premium }}}<CustomContent plan="byoc">, {{{ .byoc }}},</CustomContent> および TiDB Cloud Dedicated は手動バックアップをサポートしています。手動バックアップは、制御された復元ポイントを提供し、明示的に削除するまで保持されます。手動バックアップは PITR または部分バックアップをサポートしておらず、復元を実行するたびに新しいインスタンスが作成されます。

詳細については、以下を参照してください。

- [{{{ .premium }}}<CustomContent plan="byoc"> および {{{ .byoc }}}</CustomContent> インスタンスの手動バックアップ](/tidb-cloud/premium/backup-and-restore-premium.md#manual-backups)
- [TiDB Cloud Dedicated クラスターの手動バックアップを実行する](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup)

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
-   TiDB Cloud Essentialインスタンスの場合、過去30日間の任意の時点に復元できます。詳細については、 [復元モード](/tidb-cloud/backup-and-restore-serverless.md#restore-mode)参照してください。
-   TiDB Cloud Dedicatedクラスターの場合、事前に[PITRを有効にする](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)必要があります。

## Restore {#restore}

TiDB Cloud は、バックアップスナップショットまたはポイントインタイムリカバリから、新しいクラスターまたはインスタンスにデータを復元することをサポートしています。復元操作は、誤ったデータ損失、データ破損、またはアプリケーションエラーからのリカバリに役立ちます。

{{{ .premium }}}<CustomContent plan="byoc"> および {{{ .byoc }}}</CustomContent> インスタンスでは、新しいインスタンスにデータを復元できます。自動バックアップ、手動バックアップ、またはサポートされている外部クラウドストレージのバックアップから復元できます。PITR は自動バックアップでのみサポートされ、手動バックアップではサポートされません。
