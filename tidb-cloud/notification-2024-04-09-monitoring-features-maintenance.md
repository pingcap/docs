---
title: 2024-04-09 TiDB Cloud Monitoring Features Maintenance Notification
summary: 2024 年 4 月 9 日のTiDB Cloud監視機能のメンテナンスの詳細 (メンテナンス期間、理由、影響など) について説明します。
---

# [2024-04-09] TiDB Cloud監視機能メンテナンス通知 {#2024-04-09-tidb-cloud-monitoring-features-maintenance-notification}

この通知では、2024 年 4 月 9 日のTiDB Cloud [監視機能](/tidb-cloud/monitor-tidb-cluster.md)メンテナンスについて知っておく必要のある詳細について説明します。

## メンテナンス期間 {#maintenance-window}

-   開始時間: 2024-04-09 08:00 (UTC+0)
-   終了時間: 2024-04-09 12:00 (UTC+0)
-   所要時間: 4 時間

## インパクト {#impact}

### 影響を受ける地域 {#affected-regions}

メンテナンス期間中、次のリージョンの監視機能が影響を受けます。

-   TiDB Cloud専用クラスター：
    -   クラウドプロバイダー: AWS、リージョン: オレゴン (us-west-2)
    -   クラウドプロバイダー: AWS、リージョン: ソウル (ap-northeast-2)
    -   クラウドプロバイダー: AWS、リージョン: フランクフルト (eu-central-1)
    -   クラウドプロバイダー: AWS、リージョン: オレゴン (us-west-2)
    -   クラウド プロバイダー: Google Cloud、リージョン: オレゴン (us-west1)
    -   クラウド プロバイダー: Google Cloud、リージョン: 東京 (asia-northeast1)
    -   クラウド プロバイダー: Google Cloud、リージョン: シンガポール (asia-southeast1)
    -   クラウド プロバイダー: Google Cloud、リージョン: アイオワ (us-central1)
    -   クラウド プロバイダー: Google Cloud、リージョン: 台湾 (asia-east1)

-   TiDB Cloudサーバーレス クラスター：
    -   クラウドプロバイダー: AWS、リージョン: フランクフルト (eu-central-1)
    -   クラウドプロバイダー: AWS、リージョン: オレゴン (us-west-2)

### 影響を受ける監視機能 {#affected-monitoring-features}

> **注記：**
>
> メンテナンスは、TiDB クラスターの監視機能にのみ影響します。その他の機能はすべて影響を受けません。引き続き TiDB クラスターを管理し、通常どおり読み取り/書き込み操作やその他の操作を実行できます。

-   **メトリクス**ページは、数回の短い期間 (それぞれ 20 分未満) の間、一時的に利用できなくなります。
-   **スロー クエリ**ページは、数回の短い期間 (それぞれ 5 分未満) 一時的に利用できなくなります。
-   Prometheus、DataDog、NewRelic とのメトリック統合にはブレークポイントがある可能性があります。

## 完了と再開 {#completion-and-resumption}

メンテナンスが正常に完了すると、影響を受けた機能が復元され、さらに優れたエクスペリエンスが提供されます。

## サポートを受ける {#get-support}

ご質問やサポートが必要な場合は、 [サポートチーム](/tidb-cloud/tidb-cloud-support.md)ご連絡ください。お客様の懸念に対処し、必要なガイダンスを提供いたします。
