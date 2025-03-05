---
title: Interact with Support Tickets via Slack
summary: サポート チケットの Slack のやり取りに関する詳細情報を紹介します。
---

# Slack経由でサポートチケットとやり取りする {#interact-with-support-tickets-via-slack}

**Premium** [サポートプラン](/tidb-cloud/connected-care-detail.md)に加入している顧客向けに、 TiDB Cloud は[スラック](https://slack.com/)で**Assist**と呼ばれるチケット ボットを提供し、サポート チケットのより包括的なやり取りと管理をサポートします。

> **注記：**
>
> Slack のチケット サポート機能は、リクエストに応じてご利用いただけます。この機能を試してみたい場合は、 TiDB Cloudサポート ( <a href="mailto:support@pingcap.com">[サポート](mailto:support@pingcap.com)</a>にお問い合わせいただくか、テクニカル アカウント マネージャー (TAM) にご連絡ください。

## サポートチケットとのやり取り {#interact-with-support-tickets}

チャネルに**Assist**アプリが追加されている場合は、 **Assist**を使用してチケットを送信できます。リクエストを送信するには 2 つの方法があります。

-   **方法1: チケット作成のメッセージに🎫絵文字を追加する**

    チケットを作成する必要があるメッセージの横にある絵文字アイコンをクリックします。検索ボックスに`ticket`と入力して🎫絵文字をすばやく見つけ、🎫をクリックします。

    ![slack-ticket-interaction-1](/media/tidb-cloud/connected-slack-ticket-interaction-1.png)

    ![slack-ticket-interaction-2](/media/tidb-cloud/connected-slack-ticket-interaction-2.png)

    **Assist**アプリから**、「リクエストを送信」**ボタンを含むメッセージが送信されます。その後、ボタンをクリックしてフォームに入力し、リクエストを送信します。

    ![slack-ticket-interaction-3](/media/tidb-cloud/connected-slack-ticket-interaction-3.png)

    ![slack-ticket-interaction-4](/media/tidb-cloud/connected-slack-ticket-interaction-4.png)

-   **方法 2: チケット作成のために、問題の説明とともに`/assist`または`/assist`入力します。**

    もう 1 つのより速い方法は、メッセージ ボックスに`/assist`または`/assist [problem description]`と入力して**Enter キー**を押すことです。入力して送信するためのリクエスト送信フォームが表示されます。

    ![slack-ticket-interaction-5](/media/tidb-cloud/connected-slack-ticket-interaction-5.png)

送信後、Assist アプリはスレッド内に確認メッセージを送信します。このメッセージには、チケット リンクとチケットのステータスが含まれます。

**Premium** [サポートプラン](/tidb-cloud/connected-care-detail.md)にご加入のお客様の場合、Slack とチケットシステム間の双方向の情報同期がサポートされます。

チケットに対するサポート エンジニアのコメントは Slack メッセージ スレッドに同期されるため、ユーザーはサポート ポータルに移動してコメントを表示する必要はありません。ユーザーはこのメッセージ スレッドで直接返信することができ、これらの返信はチケット システムに同期されます。

これにより、**プレミアム**サポート プランに加入している顧客は、Slack を離れることなく、チケットをすばやく作成、応答、管理できるようになります。

![slack-ticket-interaction-6](/media/tidb-cloud/connected-slack-ticket-interaction-6.png)

## よくある質問 {#faqs}

-   チケットのステータスを確認するにはどうすればいいですか?

    チケットの作成に使用したメール アドレスで[PingCAP ヘルプセンター](https://tidb.support.pingcap.com/servicedesk/customer/user/requests)にログインします。現在のアカウントのすべての過去のチケットとそのステータスを表示できます。

## サポートに問い合わせる {#contact-support}

ご質問やご不明な点がございましたら、サポート チーム<a href="mailto:support@pingcap.com">[サポート](mailto:support@pingcap.com)</a>までお問い合わせください。
