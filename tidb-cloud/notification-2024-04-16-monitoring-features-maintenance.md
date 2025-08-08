---
title: 2024-04-16 TiDB Cloud Monitoring Features Maintenance Notification
summary: 2024 年 4 月 16 日のTiDB Cloud監視機能のメンテナンスの詳細 (メンテナンス期間、理由、影響など) について説明します。
---

# [2024-04-16] TiDB Cloud監視機能メンテナンスのお知らせ {#2024-04-16-tidb-cloud-monitoring-features-maintenance-notification}

この通知では、2024 年 4 月 16 日のTiDB Cloud [監視機能](/tidb-cloud/monitor-tidb-cluster.md)メンテナンスについて知っておく必要のある詳細について説明します。

## メンテナンスウィンドウ {#maintenance-window}

-   開始時間: 2024-04-16 08:00 (UTC+0)
-   終了時間: 2024-04-16 12:00 (UTC+0)
-   所要時間: 4時間

## インパクト {#impact}

### 影響を受けた地域 {#affected-regions}

メンテナンス期間中、次のリージョンの監視機能が影響を受けます。

-   TiDB Cloud専用クラスター：
    -   クラウドプロバイダー: AWS、リージョン: 東京 (ap-northeast-1)
    -   クラウドプロバイダー: AWS、リージョン: 北バージニア (us-east-1)

-   TiDB Cloudサーバーレス クラスター：
    -   クラウドプロバイダー: AWS、リージョン: 東京 (ap-northeast-1)
    -   クラウドプロバイダー: AWS、リージョン: 北バージニア (us-east-1)

### 影響を受ける監視機能 {#affected-monitoring-features}

> **注記：**
>
> このメンテナンスは、TiDB クラスタの監視機能にのみ影響します。その他の機能には影響はありません。引き続き TiDB クラスタを管理し、読み取り/書き込み操作やその他の操作を通常どおり実行できます。

-   **メトリクス**ページは、数回の短い期間 (それぞれ 20 分未満) の間、一時的に利用できなくなります。
-   **スロー クエリ**ページは、数回の短い期間 (それぞれ 5 分未満) の間、一時的に利用できなくなります。
-   Prometheus、DataDog、NewRelic とのメトリック統合にはブレークポイントが存在する可能性があります。

## 完了と再開 {#completion-and-resumption}

メンテナンスが正常に完了すると、影響を受けた機能が復元され、さらに優れたエクスペリエンスが提供されます。

## サポートを受ける {#get-support}

ご質問やサポートが必要な場合は、 [サポートチーム](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。お客様のご懸念にお答えし、必要なサポートを提供させていただきます。
