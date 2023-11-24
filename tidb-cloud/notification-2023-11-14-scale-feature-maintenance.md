---
title: 2023-11-14 TiDB Cloud Dedicated Scale Feature Maintenance Notification
summary: Learn about the details of TiDB Cloud Dedicated Scale Feature Maintenance on November 14, 2023, such as the maintenance window and impact.
---

# [2023-11-14] TiDB Cloud専用スケール機能メンテナンスのお知らせ {#2023-11-14-tidb-cloud-dedicated-scale-feature-maintenance-notification}

この通知には、2023 年 11 月 14 日のTiDB Cloud Dended [スケール機能](https://docs.pingcap.com/tidbcloud/scale-tidb-cluster#scale-your-tidb-cluster)のメンテナンスについて知っておく必要がある詳細が記載されています。

## メンテナンス期間 {#maintenance-window}

-   開始時間: 2023-11-14 16:00 (UTC+0)
-   終了時刻: 2023-11-21 16:00 (UTC+0)
-   期間: 7日間

> **注記：**
>
> 2023 年 11 月 16 日更新: メンテナンス期間の終了時間が 2023 年 11 月 16 日から 2023 年 11 月 21 日に延長されました。

## インパクト {#impact}

メンテナンス期間中は[vCPU と RAM を変更する](https://docs.pingcap.com/tidbcloud/scale-tidb-cluster#change-vcpu-and-ram)が無効になり、専用クラスターの vCPU と RAM を変更できません。ただし、 「クラスタの変更」ページでノード番号またはstorageを変更することはできます。 TiDB クラスターはデータの読み取りと書き込みの通常の操作を維持し、オンライン ビジネスに悪影響を与えないようにします。

### 影響を受けるTiDB Cloudコンソール UI の機能 {#affected-features-of-tidb-cloud-console-ui}

-   クラスタレベル
    -   クラスタ管理
        -   クラスターの変更
            -   TiDB、TiKV、またはTiFlashノードの vCPU と RAM を変更します。

### 影響を受けるTiDB Cloud API の機能 {#affected-features-of-tidb-cloud-api}

-   クラスタ管理
    -   [クラスターの更新](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)

## 完成と再開 {#completion-and-resumption}

メンテナンスが正常に完了すると、影響を受けた機能が復元され、さらに優れたエクスペリエンスが提供されます。

## 支持を得ます {#get-support}

ご質問がある場合、またはサポートが必要な場合は、 [支援チーム](/tidb-cloud/tidb-cloud-support.md)までお問い合わせください。私たちはあなたの懸念に対処し、必要なガイダンスを提供するためにここにいます。
