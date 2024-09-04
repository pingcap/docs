---
title: 2024-09-15 TiDB Cloud Console Maintenance Notification
summary: 2024 年 9 月 15 日のTiDB Cloud Console メンテナンスの詳細 (メンテナンス ウィンドウ、理由、影響など) について説明します。
---

# [2024-09-15] TiDB Cloudコンソールメンテナンス通知 {#2024-09-15-tidb-cloud-console-maintenance-notification}

この通知では、2024 年 9 月 15 日の[TiDB Cloudコンソール](https://tidbcloud.com/)メンテナンスについて知っておく必要のある詳細について説明します。

## メンテナンス期間 {#maintenance-window}

-   日付: 2024-09-15
-   開始時間: 8:00 (UTC+0)
-   終了時間: 8:10 (UTC+0)
-   所要時間: 約10分

> **注記：**
>
> -   現在、ユーザーはTiDB Cloudコンソールのメンテナンスのタイミングを変更できないため、事前に計画を立てる必要があります。
> -   今後 3 か月間、一部のユーザーには追加の 20 分間のメンテナンス ウィンドウが発生する可能性があります。影響を受けるユーザーには事前に電子メール通知が送信されます。

## メンテナンスの理由 {#reason-for-maintenance}

パフォーマンスと効率性を向上させるために、 TiDB Cloudコンソールのメタ データベース サービスをアップグレードしています。この改善は、高品質なサービスを提供するという当社の継続的な取り組みの一環として、すべてのユーザーに優れたエクスペリエンスを提供することを目的としています。

## インパクト {#impact}

メンテナンス期間中、 TiDB Cloudコンソール UI および API 内での作成と更新に関連する機能に断続的な中断が発生する可能性があります。ただし、TiDB クラスターはデータの読み取りと書き込みの通常の操作を維持し、オンライン ビジネスに悪影響が及ぶことはありません。

### TiDB Cloudコンソール UI の影響を受ける機能 {#affected-features-of-tidb-cloud-console-ui}

-   クラスタレベル
    -   クラスタ管理
        -   クラスターを作成する
        -   クラスターを削除する
        -   スケールクラスター
        -   クラスターを一時停止または再開する
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
        -   復元ジョブを作成する
    -   データベース監査ログ
        -   接続性をテストする
        -   アクセスレコードの追加または削除
        -   データベース監査ログを有効または無効にする
        -   データベース監査ログを再開する
-   プロジェクトレベル
    -   ネットワークアクセス
        -   プライベートエンドポイントを作成する
        -   プライベートエンドポイントを削除する
        -   VPC ピアリングを追加する
        -   VPC ピアリングの削除
    -   メンテナンス
        -   メンテナンスウィンドウを変更する
        -   タスクを延期する
    -   ごみ箱
        -   クラスターを削除する
        -   バックアップを削除する
        -   クラスターを復元する

### TiDB Cloud API の影響を受ける機能 {#affected-features-of-tidb-cloud-api}

-   クラスタ管理
    -   [クラスターの作成](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateCluster)
    -   [クラスターの削除](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/DeleteCluster)
    -   [クラスターの更新](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)
    -   [作成AwsCmek](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek)
-   バックアップ
    -   [バックアップの作成](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/CreateBackup)
    -   [バックアップの削除](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/DeleteBackup)
-   復元する
    -   [復元タスクの作成](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Restore/operation/CreateRestoreTask)
-   輸入
    -   [インポートタスクの作成](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/CreateImportTask)
    -   [インポートタスクの更新](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/UpdateImportTask)

## 完了と再開 {#completion-and-resumption}

メンテナンスが正常に完了すると、影響を受けた機能が復元され、さらに優れたエクスペリエンスが提供されます。

## サポートを受ける {#get-support}

ご質問やサポートが必要な場合は、 [サポートチーム](/tidb-cloud/tidb-cloud-support.md)ご連絡ください。お客様の懸念に対処し、必要なガイダンスを提供いたします。
