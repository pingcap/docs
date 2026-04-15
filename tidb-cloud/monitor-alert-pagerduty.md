---
title: Subscribe via PagerDuty
summary: PagerDuty経由でアラート通知を受け取ることで、TiDBを監視する方法を学びましょう。
---

# PagerDuty経由で購読する {#subscribe-via-pagerduty}

TiDB Cloud は、PagerDuty、[スラック](/tidb-cloud/monitor-alert-slack.md)、[メール](/tidb-cloud/monitor-alert-email.md)、[ズーム](/tidb-cloud/monitor-alert-zoom.md)、[フラッシュデューティ](/tidb-cloud/monitor-alert-flashduty.md)経由でアラート通知を購読する簡単な方法を提供します。このドキュメントでは、PagerDuty 経由でアラート通知をサブスクライブする方法について説明します。

> **注記：**
>
> 現在、アラート購読は[TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンスおよび[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタで利用可能です。

## 前提条件 {#prerequisites}

-   PagerDuty 経由のサブスクライブ機能は、 **Enterprise**または**Premium**[サポートプラン](/tidb-cloud/connected-care-overview.md)にサブスクライブしている組織のみが利用できます。

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権、またはTiDB Cloudの対象プロジェクトへの`Project Owner`アクセス権が必要です。

## アラート通知を購読する {#subscribe-to-alert-notifications}

アラート通知を受け取るには、以下の手順に従ってください。

### ステップ1. PagerDutyの統合キーを生成する {#step-1-generate-a-pagerduty-integration-key}

1.  [PagerDutyイベントAPI v2の概要](https://developer.pagerduty.com/docs/events-api-v2-overview#getting-started)の概要の手順に従って、**イベント API v2**タイプの統合キーを生成します。
2.  生成された統合キーを保存して、次のステップで使用してください。

### ステップ2. TiDB Cloudから購読する {#step-2-subscribe-from-tidb-cloud}

アラート通知のサブスクリプションは[TiDB Cloudプラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

> **ヒント：**
>
> TiDB Cloud Dedicatedの場合、アラートの購読は現在のプロジェクト内のすべてのアラートに適用されます。プロジェクト内に複数のTiDB Cloud Dedicatedクラスタがある場合でも、購読は一度だけで済みます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。

3.  左側のナビゲーションペインで、 **「プロジェクト設定」**の下にある**「アラート購読」**をクリックします。

4.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

5.  **購読者タイプの**ドロップダウンリストから**「PagerDuty」を**選択してください。

6.  「**名前」**欄に名前を入力し、 **「統合キー」**欄にPagerDutyの統合キーを入力してください。

7.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージの指示に従って問題を解決し、接続を再試行してください。

8.  購読を完了するには、 **「保存」**をクリックしてください。

または、 TiDB Cloud Dedicatedクラスタの**アラート**ページの右上にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

<CustomContent plan="essential">

> **ヒント：**
>
> TiDB Cloud Essentialの場合、アラートの購読は現在のインスタンス内のすべてのアラートに適用されます。複数のインスタンスがある場合は、各インスタンスごとに個別に購読する必要があります。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。

3.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

4.  **購読者タイプの**ドロップダウンリストから**「PagerDuty」を**選択してください。

5.  「**名前」**欄に名前を入力し、 **「統合キー」**欄にPagerDutyの統合キーを入力してください。

6.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージの指示に従って問題を解決し、接続を再試行してください。

7.  購読を完了するには、 **「保存」**をクリックしてください。

または、 TiDB Cloud Essentialインスタンスの**アラート**ページの右上隅にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

アラート条件に変更がない場合、アラートは3時間ごとに通知を送信します。

## アラート通知の購読を解除する {#unsubscribe-from-alert-notifications}

アラート通知の受信を停止したい場合は、以下の手順に従ってください。手順は[TiDB Cloudプラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。
2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。
3.  左側のナビゲーションペインで、 **「プロジェクト設定」**の下にある**「アラート購読」**をクリックします。
4.  **アラート購読**ページで、削除する対象の購読者の行を見つけて、 **[...]** &gt; **[購読解除]**をクリックします。
5.  購読解除を確定するには、 **「購読解除」**をクリックしてください。

</CustomContent>

<CustomContent plan="essential">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。
3.  **アラート購読**ページで、削除する対象の購読者の行を見つけて、 **[...]** &gt; **[購読解除]**をクリックします。
4.  購読解除を確定するには、 **「購読解除」**をクリックしてください。

</CustomContent>
