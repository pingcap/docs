---
title: Subscribe via Email
summary: メールによるアラート通知を受け取ることで、TiDBを監視する方法を学びましょう。
---

# メールで購読する {#subscribe-via-email}

TiDB Cloud、電子メール、[スラック](/tidb-cloud/monitor-alert-slack.md)、[ズーム](/tidb-cloud/monitor-alert-zoom.md)、[フラッシュデューティ](/tidb-cloud/monitor-alert-flashduty.md)、 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md)経由でアラート通知を購読する簡単な方法が提供されます。このドキュメントでは、電子メールでアラート通知を購読する方法について説明します。

> **注記：**
>
> 現在、アラート購読は[TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンスおよび[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタで利用可能です。

## 前提条件 {#prerequisites}

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権、またはTiDB Cloudの対象プロジェクトへの`Project Owner`アクセス権が必要です。

## アラート通知を購読する {#subscribe-to-alert-notifications}

アラート通知を受信するには、以下の手順に従ってください。手順は[TiDB Cloudプラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

> **ヒント：**
>
> TiDB Cloud Dedicatedの場合、アラートの購読は現在のプロジェクト内のすべてのアラートに適用されます。プロジェクト内に複数のTiDB Cloud Dedicatedクラスタがある場合でも、購読は一度だけで済みます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。

3.  左側のナビゲーションペインで、 **「プロジェクト設定」**の下にある**「アラート購読」**をクリックします。

4.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

5.  **購読者タイプの**ドロップダウンリストから**「メール」**を選択してください。

6.  メールアドレスを入力してください。

7.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージの指示に従って問題を解決し、接続を再試行してください。

8.  購読を完了するには、 **「保存」**をクリックしてください。

または、 TiDB Cloud Dedicatedクラスタの[**警告**](/tidb-cloud/monitor-built-in-alerting.md#view-alerts)ページの右上隅にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

<CustomContent plan="essential">

> **ヒント：**
>
> TiDB Cloud Essentialの場合、アラートの購読は現在のインスタンス内のすべてのアラートに適用されます。複数のTiDB Cloud Essentialインスタンスをお持ちの場合は、各インスタンスごとに個別に購読する必要があります。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。

3.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

4.  **購読者タイプの**ドロップダウンリストから**「メール」**を選択してください。

5.  メールアドレスを入力してください。

6.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージの指示に従って問題を解決し、接続を再試行してください。

7.  購読を完了するには、 **「保存」**をクリックしてください。

または、 TiDB Cloud Essentialインスタンスの[**警告**](/tidb-cloud/monitor-built-in-alerting.md#view-alerts)ページの右上隅にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

アラート条件に変更がない場合、アラートは3時間ごとにメール通知を送信します。

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
