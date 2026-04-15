---
title: 2024-04-09 TiDB Cloud Monitoring Features Maintenance Notification
summary: 2024年4月9日に実施されるTiDB Cloud監視機能のメンテナンスの詳細（メンテナンス期間、理由、影響など）についてご確認ください。
---

# [2024-04-09] TiDB Cloud監視機能メンテナンスのお知らせ {#2024-04-09-tidb-cloud-monitoring-features-maintenance-notification}

この通知では、2024年4月9日に実施さTiDB Cloud[監視機能](/tidb-cloud/monitor-tidb-cluster.md)メンテナンスについて知っておくべき詳細を説明します。

## メンテナンスウィンドウ {#maintenance-window}

-   開始時刻：2024年4月9日 08:00 (UTC+0)
-   終了時刻：2024年4月9日 12:00 (UTC+0)
-   所要時間：4時間

## インパクト {#impact}

### 影響を受ける地域 {#affected-regions}

メンテナンス期間中は、以下の地域における監視機能に影響が出ます。

-   TiDB Cloud Dedicatedクラスター：
    -   クラウドプロバイダー：AWS、リージョン：オレゴン（us-west-2）
    -   クラウドプロバイダー：AWS、リージョン：ソウル（ap-northeast-2）
    -   クラウドプロバイダー：AWS、リージョン：フランクフルト（eu-central-1）
    -   クラウドプロバイダー：AWS、リージョン：オレゴン（us-west-2）
    -   クラウドプロバイダー：Google Cloud、リージョン：オレゴン（us-west1）
    -   クラウドプロバイダー：Google Cloud、リージョン：東京（asia-northeast1）
    -   クラウドプロバイダー：Google Cloud、リージョン：シンガポール（asia-southeast1）
    -   クラウドプロバイダー：Google Cloud、リージョン：アイオワ（us-central1）
    -   クラウドプロバイダー：Google Cloud、リージョン：台湾（asia-east1）

-   TiDB Cloud Starterインスタンス：
    -   クラウドプロバイダー：AWS、リージョン：フランクフルト（eu-central-1）
    -   クラウドプロバイダー：AWS、リージョン：オレゴン（us-west-2）

### 影響を受ける監視機能 {#affected-monitoring-features}

> **注記：**
>
> 今回のメンテナンスは、TiDBクラスタの監視機能のみに影響します。その他の機能には影響はありません。TiDBクラスタの管理や、読み書き操作、その他の操作は通常どおり実行できます。

-   **メトリクス**ページは、数回にわたり短時間（それぞれ20分未満）一時的に利用できなくなります。
-   **スロークエリ**ページは、数回の短い期間（それぞれ5分未満）に一時的に利用できなくなります。
-   Prometheus、DataDog、NewRelicとのメトリクス統合には、ブレークポイントが存在する可能性があります。

## 完了と再開 {#completion-and-resumption}

メンテナンスが正常に完了すると、影響を受けた機能が復旧し、より快適なユーザーエクスペリエンスを提供できるようになります。

## サポートを受ける {#get-support}

ご質問やサポートが必要な場合は、弊社の[サポートチーム](/tidb-cloud/tidb-cloud-support.md)までご連絡ください。お客様のご懸念事項に対応し、必要なご案内をさせていただきます。
