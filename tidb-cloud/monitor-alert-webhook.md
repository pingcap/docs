---
title: Webhook経由で購読する
summary: 汎用webhook を介してアラート通知を受信し、TiDB クラスターを監視する方法を学びます。
---

# Webhook経由で購読する

TiDB Cloud では、[汎用webhook](/tidb-cloud/monitor-alert-webhook.md)、[email](/tidb-cloud/monitor-alert-email.md)、[Slack](/tidb-cloud/monitor-alert-slack.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md)、[Flashduty](/tidb-cloud/monitor-alert-flashduty.md)、および [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md) を通じて、アラート通知を簡単に購読できます。このドキュメントでは、汎用webhook を介してアラート通知を購読する方法について説明します。

> **Note:**
>
> 現在、アラート購読は [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) インスタンス、[TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) インスタンス、および [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) クラスターで利用できます。

## 前提条件 {#prerequisites}

- webhook経由での購読機能は、**Enterprise** または **Premium** サポートプランを契約している組織でのみ利用できます。

- アラート通知の受信先となるプラットフォームの webhook URL が必要です（たとえば、Telegram、Microsoft Teams、または JSON ペイロード付きの HTTP POST リクエストを受け付ける独自のオンコールシステムなど）。現在、TiDB Cloud はリクエストヘッダーやペイロード形式のカスタマイズをサポートしていません。

<CustomContent plan="dedicated">

- TiDB Cloud のアラート通知を購読するには、組織に対する `Organization Owner` アクセス、または TiDB Cloud 内の対象プロジェクトに対する `Project Owner` アクセスが必要です。

</CustomContent>

<CustomContent plan="essential,premium">

- TiDB Cloud のアラート通知を購読するには、組織に対する `Organization Owner` アクセス、または TiDB Cloud 内の対象インスタンスに対する `Project Owner` または `Instance Manager` アクセスが必要です。

</CustomContent>

## アラート通知を購読する {#subscribe-to-alert-notifications}

アラート通知のサブスクリプションは、[TiDB Cloud プラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

{{{ .dedicated }}} クラスターのアラート通知を購読するには、次の手順を実行します。

> **Tip:**
>
> {{{ .dedicated }}} では、アラートサブスクリプションは現在のプロジェクト内のすべてのアラートに対して適用されます。プロジェクト内に複数の {{{ .dedicated }}} クラスターがある場合でも、購読は一度だけで済みます。

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、**Project view** タブをクリックします。
2. プロジェクトビューで対象のプロジェクトを見つけ、プロジェクトの <MDSvgIcon name="icon-project-settings" /> をクリックします。
3. 左側のナビゲーションペインで、**Project Settings** の下にある **Alert Subscription** をクリックします。
4. **Alert Subscription** ページで、右上の **Add Subscriber** をクリックします。
5. **Subscriber Type** ドロップダウンリストから **Webhook** を選択します。
6. **Name** フィールドに名前を入力し、**Webhook URL** フィールドに webhook URL を入力します。
7. **Save** をクリックします。バックエンドで接続テストが実行され、保存されます。 

    テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従って問題をトラブルシューティングし、接続を再試行してください。

または、対象の {{{ .dedicated }}} クラスターの **Alert** ページ右上にある **Subscribe** をクリックすることもできます。すると、**Alert Subscription** ページに移動します。

</CustomContent>

<CustomContent plan="essential">

> **Tip:**
>
> {{{ .essential }}} では、アラートサブスクリプションは現在のインスタンス内のすべてのアラートに対して適用されます。複数の {{{ .essential }}} インスタンスがある場合は、各インスタンスごとに個別に購読する必要があります。

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .essential }}} インスタンス名をクリックして概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Alert Subscription** をクリックします。
3. **Alert Subscription** ページで、右上の **Add Subscriber** をクリックします。
4. **Subscriber Type** ドロップダウンリストから **Webhook** を選択します。
5. **Name** フィールドに名前を入力し、**Webhook URL** フィールドに webhook URL を入力します。
6. **Save** をクリックします。バックエンドで接続テストが実行され、保存されます。

    テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従って問題をトラブルシューティングし、接続を再試行してください。

または、対象の {{{ .essential }}} インスタンスの **Alert** ページ右上にある **Subscribe** をクリックすることもできます。すると、**Alert Subscription** ページに移動します。

</CustomContent>

<CustomContent plan="premium">

> **Tip:**
>
> {{{ .premium }}} では、アラートサブスクリプションは現在のインスタンス内のすべてのアラートに対して適用されます。複数の {{{ .premium }}} インスタンスがある場合は、各インスタンスごとに個別に購読する必要があります。

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .premium }}} インスタンス名をクリックして概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Alert Subscription** をクリックします。
3. **Alert Subscription** ページで、右上の **Add Subscriber** をクリックします。
4. **Subscriber Type** ドロップダウンリストから **Webhook** を選択します。
5. **Name** フィールドに名前を入力し、**Webhook URL** フィールドに webhook URL を入力します。
6. **Save** をクリックします。バックエンドで接続テストが実行され、保存されます。 

    テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従って問題をトラブルシューティングし、接続を再試行してください。

または、対象の {{{ .premium }}} インスタンスの **Alert** ページ右上にある **Subscribe** をクリックすることもできます。すると、**Alert Subscription** ページに移動します。

</CustomContent>

アラート条件が変わらない場合、アラートは 3時間ごとに通知を送信します。

## アラート通知の購読を解除する {#unsubscribe-from-alert-notifications}

アラート通知を受信しなくなった場合は、次の手順を実行します。手順は [TiDB Cloud プラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、**Project view** タブをクリックします。
2. プロジェクトビューで対象のプロジェクトを見つけ、プロジェクトの <MDSvgIcon name="icon-project-settings" /> をクリックします。
3. 左側のナビゲーションペインで、**Project Settings** の下にある **Alert Subscription** をクリックします。
4. **Alert Subscription** ページで、削除する対象サブスクライバーの行を見つけ、**...** > **Unsubscribe** をクリックします。
5. **Unsubscribe** をクリックして、購読解除を確定します。

</CustomContent>

<CustomContent plan="essential">

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .essential }}} インスタンス名をクリックして概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Alert Subscription** をクリックします。
3. **Alert Subscription** ページで、削除する対象サブスクライバーの行を見つけ、**...** > **Unsubscribe** をクリックします。
4. **Unsubscribe** をクリックして、購読解除を確定します。

</CustomContent>

<CustomContent plan="premium">

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .premium }}} インスタンス名をクリックして概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Alert Subscription** をクリックします。
3. **Alert Subscription** ページで、削除する対象サブスクライバーの行を見つけ、**...** > **Unsubscribe** をクリックします。
4. **Unsubscribe** をクリックして、購読解除を確定します。

</CustomContent>
