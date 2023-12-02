---
title: 2023-08-31 TiDB Cloud Console Maintenance Notification
summary: Learn about the details of the TiDB Cloud Console maintenance on August 31, 2023, such as the maintenance window, reason, and impact.
---

# [2023-08-31] TiDB Cloudコンソール メンテナンスのお知らせ {#2023-08-31-tidb-cloud-console-maintenance-notification}

このお知らせには、2023年8月31日の[TiDB Cloudコンソール](https://tidbcloud.com/)メンテナンスにあたり、知っておいていただきたい内容が記載されております。

## メンテナンス期間 {#maintenance-window}

-   日付: 2023-08-31
-   開始時刻: 8:00 (UTC+0)
-   終了時刻: 10:00 (UTC+0)
-   所要時間：約2時間

> **注記：**
>
> 現在、ユーザーはTiDB Cloudコンソールのメンテナンスのタイミングを変更できないため、事前にそれに応じて計画を立てる必要があります。

## メンテナンスの理由 {#reason-for-maintenance}

パフォーマンスと効率を向上させるために、 TiDB Cloudコンソールのメタ データベース サービスをアップグレードしています。この改善は、高品質のサービスを提供するという継続的な取り組みの一環として、すべてのユーザーにより良いエクスペリエンスを提供することを目的としています。

## インパクト {#impact}

メンテナンス期間中は、 TiDB Cloudコンソール UI および API 内の作成および更新に関連する機能で断続的な中断が発生する可能性があります。ただし、TiDB クラスターはデータの読み取りと書き込みの通常の操作を維持し、オンライン ビジネスに悪影響を及ぼさないようにします。

### 影響を受けるTiDB Cloudコンソール UI の機能 {#affected-features-of-tidb-cloud-console-ui}

-   クラスタレベル
    -   クラスタ管理
        -   クラスターの作成
        -   クラスターの削除
        -   スケールクラスター
        -   クラスターの一時停止または再開
        -   クラスターのパスワードを変更する
        -   クラスタートラフィックフィルターを変更する
    -   輸入
        -   インポートジョブを作成する
    -   データ移行
        -   移行ジョブを作成する
    -   チェンジフィード
        -   チェンジフィードジョブを作成する
    -   バックアップ
        -   手動バックアップジョブを作成する
        -   自動バックアップジョブ
    -   復元する
        -   復元ジョブの作成
    -   データベース監査ログ
        -   接続性をテストする
        -   アクセスレコードの追加または削除
        -   データベース監査ログを有効または無効にする
        -   データベース監査ログを再開する
-   プロジェクトレベル
    -   ネットワークアクセス
        -   プライベートエンドポイントを作成する
        -   プライベート エンドポイントを削除する
        -   VPC ピアリングの追加
        -   VPC ピアリングの削除
    -   メンテナンス
        -   メンテナンス期間の変更
        -   タスクを延期する
    -   ごみ箱
        -   クラスターの削除
        -   バックアップの削除
        -   クラスターの復元

### 影響を受けるTiDB Cloud API の機能 {#affected-features-of-tidb-cloud-api}

-   クラスタ管理
    -   [クラスターの作成](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateCluster)
    -   [クラスターの削除](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/DeleteCluster)
    -   [クラスターの更新](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)
    -   [AWSCmekの作成](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek)
-   バックアップ
    -   [バックアップを作成する](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/CreateBackup)
    -   [バックアップの削除](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/DeleteBackup)
-   復元する
    -   [復元タスクの作成](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Restore/operation/CreateRestoreTask)
-   輸入
    -   [インポートタスクの作成](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/CreateImportTask)
    -   [更新インポートタスク](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/UpdateImportTask)

## 完了と再開 {#completion-and-resumption}

メンテナンスが正常に完了すると、影響を受けた機能が復元され、さらに優れたエクスペリエンスが提供されます。

## 支持を得ます {#get-support}

ご質問がある場合、またはサポートが必要な場合は、 [支援チーム](/tidb-cloud/tidb-cloud-support.md)までお問い合わせください。私たちはあなたの懸念に対処し、必要なガイダンスを提供するためにここにいます。
