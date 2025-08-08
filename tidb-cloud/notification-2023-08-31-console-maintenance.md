---
title: 2023-08-31 TiDB Cloud Console Maintenance Notification
summary: 2023 年 8 月 31 日のTiDB Cloud Console メンテナンスの詳細 (メンテナンス ウィンドウ、理由、影響など) について説明します。
---

# [2023-08-31] TiDB Cloudコンソールメンテナンスのお知らせ {#2023-08-31-tidb-cloud-console-maintenance-notification}

この通知では、2023 年 8 月 31 日の[TiDB Cloudコンソール](https://tidbcloud.com/)目のメンテナンスについて知っておく必要のある詳細について説明します。

## メンテナンスウィンドウ {#maintenance-window}

-   日付: 2023-08-31
-   開始時間: 8:00 (UTC+0)
-   終了時間: 10:00 (UTC+0)
-   所要時間: 約2時間

> **注記：**
>
> 現在、ユーザーはTiDB Cloudコンソールのメンテナンスのタイミングを変更できないため、事前に適切な計画を立てる必要があります。

## メンテナンスの理由 {#reason-for-maintenance}

TiDB Cloudコンソールのメタデータサービスをアップグレードし、パフォーマンスと効率性を向上させます。この改善は、高品質なサービスの提供という継続的な取り組みの一環として、すべてのユーザーの皆様により良いエクスペリエンスを提供することを目指しています。

## インパクト {#impact}

メンテナンス期間中、 TiDB Cloudコンソールの UI および API 内での作成および更新に関連する機能に断続的な中断が発生する可能性があります。ただし、TiDB クラスターは通常通りデータの読み取りと書き込みを行うため、オンラインビジネスに悪影響は発生しません。

### TiDB Cloudコンソール UI の影響を受ける機能 {#affected-features-of-tidb-cloud-console-ui}

-   クラスタレベル
    -   クラスタ管理
        -   クラスターを作成する
        -   クラスターを削除する
        -   スケールクラスター
        -   クラスターを一時停止または再開する
        -   クラスターパスワードを変更する
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
        -   VPCピアリングを追加する
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

ご質問やサポートが必要な場合は、 [サポートチーム](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。お客様のご懸念にお答えし、必要なサポートを提供させていただきます。
