---
title: Webhook 経由でサブスクライブする
summary: 汎用 webhook を介してアラート通知を受信し、TiDB クラスターを監視する方法を学びます。
---

# Webhook 経由でサブスクライブする

TiDB Cloud では、[Generic Webhook](/tidb-cloud/monitor-alert-webhook.md)、[email](/tidb-cloud/monitor-alert-email.md)、[Slack](/tidb-cloud/monitor-alert-slack.md)、[Zoom](/tidb-cloud/monitor-alert-zoom.md)、[Flashduty](/tidb-cloud/monitor-alert-flashduty.md)、および [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md) を通じて、アラート通知を簡単にサブスクライブできます。このドキュメントでは、汎用 webhook を介してアラート通知をサブスクライブする方法について説明します。

> **Note:**
>
> 現在、アラートサブスクリプションは [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) インスタンス、[TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) インスタンス、および [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) クラスターで利用できます。

## 前提条件 {#prerequisites}

- webhook 経由でのサブスクライブ機能は、**Enterprise** または **Premium** サポートプランを契約している組織でのみ利用できます。

- アラート通知の受信先となるプラットフォームの webhook URL が必要です（たとえば、Telegram、Microsoft Teams、または JSON ペイロード付きの HTTP POST リクエストを受け付ける独自のオンコールシステムなど）。現在、TiDB Cloud はリクエストヘッダーやペイロード形式のカスタマイズをサポートしていません。

<CustomContent plan="dedicated">

- TiDB Cloud のアラート通知をサブスクライブするには、組織に対する `Organization Owner` アクセス、または TiDB Cloud 内の対象プロジェクトに対する `Project Owner` アクセスが必要です。

</CustomContent>

<CustomContent plan="premium">

- TiDB Cloud のアラート通知をサブスクライブするには、組織に対する `Organization Owner` アクセス、または TiDB Cloud 内の対象インスタンスに対する `Project Owner` または `Instance Manager` アクセスが必要です。

</CustomContent>

## アラート通知をサブスクライブする {#subscribe-to-alert-notifications}

アラート通知のサブスクリプションは、[TiDB Cloud プラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

{{{ .dedicated }}} クラスターのアラート通知をサブスクライブするには、次の手順を実行します。

> **Tip:**
>
> {{{ .dedicated }}} では、アラートサブスクリプションは現在のプロジェクト内のすべてのアラートに対して適用されます。プロジェクト内に複数の {{{ .dedicated }}} クラスターがある場合でも、サブスクライブは 1 回だけで済みます。

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
> {{{ .essential }}} では、アラートサブスクリプションは現在のインスタンス内のすべてのアラートに対して適用されます。複数の {{{ .essential }}} インスタンスがある場合は、各インスタンスごとに個別にサブスクライブする必要があります。

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
> {{{ .premium }}} では、アラートサブスクリプションは現在のインスタンス内のすべてのアラートに対して適用されます。複数の {{{ .premium }}} インスタンスがある場合は、各インスタンスごとに個別にサブスクライブする必要があります。

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .premium }}} インスタンス名をクリックして概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Alert Subscription** をクリックします。
3. **Alert Subscription** ページで、右上の **Add Subscriber** をクリックします。
4. **Subscriber Type** ドロップダウンリストから **Webhook** を選択します。
5. **Name** フィールドに名前を入力し、**Webhook URL** フィールドに webhook URL を入力します。
6. **Save** をクリックします。バックエンドで接続テストが実行され、保存されます。 

    テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従って問題をトラブルシューティングし、接続を再試行してください。

または、対象の {{{ .premium }}} インスタンスの **Alert** ページ右上にある **Subscribe** をクリックすることもできます。すると、**Alert Subscription** ページに移動します。

</CustomContent>

アラート条件が変わらない場合、アラートは 3 時間ごとに通知を送信します。

## アラート通知のサブスクライブを解除する {#unsubscribe-from-alert-notifications}

アラート通知を受信しなくなった場合は、次の手順を実行します。手順は [TiDB Cloud プラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、**Project view** タブをクリックします。
2. プロジェクトビューで対象のプロジェクトを見つけ、プロジェクトの <MDSvgIcon name="icon-project-settings" /> をクリックします。
3. 左側のナビゲーションペインで、**Project Settings** の下にある **Alert Subscription** をクリックします。
4. **Alert Subscription** ページで、削除する対象サブスクライバーの行を見つけ、**...** > **Unsubscribe** をクリックします。
5. **Unsubscribe** をクリックして、サブスクライブ解除を確定します。

</CustomContent>

<CustomContent plan="essential">

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .essential }}} インスタンス名をクリックして概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Alert Subscription** をクリックします。
3. **Alert Subscription** ページで、削除する対象サブスクライバーの行を見つけ、**...** > **Unsubscribe** をクリックします。
4. **Unsubscribe** をクリックして、サブスクライブ解除を確定します。

</CustomContent>

<CustomContent plan="premium">

1. [TiDB Cloud console](https://tidbcloud.com) で、組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の {{{ .premium }}} インスタンス名をクリックして概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Alert Subscription** をクリックします。
3. **Alert Subscription** ページで、削除する対象サブスクライバーの行を見つけ、**...** > **Unsubscribe** をクリックします。
4. **Unsubscribe** をクリックして、サブスクライブ解除を確定します。

</CustomContent>