---
title: Connected Care Overview
summary: 新しい世代のTiDB Cloudサポート サービスである Connected Care を紹介します。
aliases: ['/ja/tidbcloud/connected-care-announcement']
---

# コネクテッドケアの概要 {#connected-care-overview}

あらゆる規模のお客様がTiDB Cloud上でユースケースと運用を拡大し続けていることを受け、 TiDB Cloud は、進化するニーズに対応するためにサポートサービスを再構築することに注力しています。さらに高い価値とシームレスなエクスペリエンスを提供するために、 TiDB Cloud は**2025年2月17日**に新しいサポートサービス**「Connected Care」**の提供を開始することを発表いたします。

この移行の一環として、現在のサポートプランは**2025年2月17日**以降、購入できなくなり、レガシーサポートプランとして分類されます。ただし、 TiDB Cloudは、レガシープランにご加入のお客様には、それぞれの[退職日](#transition-to-connected-care)月間、引き続き完全なサポートを提供します。

スムーズな移行と最新機能へのアクセスを確保するために、 TiDB Cloud、お客様に Connected Care サービスへの移行と導入を推奨しています。

## コネクテッドケア {#connected-care}

Connected Care サービスは、最新のコミュニケーション ツール、プロアクティブなサポート、高度な AI 機能を通じてTiDB Cloudとの接続を強化し、シームレスで顧客中心のエクスペリエンスを実現するように設計されています。

Connected Care サービスには、 **Basic** 、 **Developer** (従来の**Standard**プランに相当)、 **Enterprise** 、 **Premium の**4 つのサポート プランがあります。

> **注記**
>
> **Basic** 、 **Enterprise** 、および**Premium の**サポート プランでは、従来のプランと同じプラン名が使用されていますが、サービス コミットメントが異なる異なるプランを指します。

以下の表は、Connected Careサービスの各サポートプランの概要を示しています。詳細については、 [コネクテッドケアの詳細](/tidb-cloud/connected-care-detail.md)ご覧ください。

| サポートプラン                                                                                                                                           | 基本               | 開発者        | 企業         | プレミアム                 |
| :------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------- | :--------- | :--------- | :-------------------- |
| 推奨されるワークロード                                                                                                                                       | 個人または初心者向けプロジェクト | 開発中のワークロード | 本番中のワークロード | 本番中のビジネスクリティカルなワークロード |
| 請求とアカウントサポート                                                                                                                                      | ✔                | ✔          | ✔          | ✔                     |
| テクニカルサポート                                                                                                                                         | <li></li>        | ✔          | ✔          | ✔                     |
| 初期応答時間                                                                                                                                            | <li></li>        | 営業時間       | 7x24       | 7x24                  |
| [コネクテッド：クリニックサービス](/tidb-cloud/tidb-cloud-clinic.md)                                                                                              | <li></li>        | <li></li>  | ✔          | ✔                     |
| [接続：IMでのAIチャット](/tidb-cloud/connected-ai-chat-in-im.md)                                                                                           | <li></li>        | <li></li>  | ✔          | ✔                     |
| 接続済み: TiDB Cloudアラートの IM サブスクリプション ( [スラック](/tidb-cloud/monitor-alert-slack.md) , [ズーム](/tidb-cloud/monitor-alert-zoom.md) )                      | <li></li>        | <li></li>  | ✔          | ✔                     |
| 接続済み: IMチケットの作成とサブスクリプションの更新 ( [スラック](/tidb-cloud/connected-slack-ticket-creation.md) , [ラーク](/tidb-cloud/connected-lark-ticket-creation.md) )    | <li></li>        | <li></li>  | ✔          | ✔                     |
| 接続済み: サポートチケットのIMインタラクション ( [スラック](/tidb-cloud/connected-slack-ticket-interaction.md) , [ラーク](/tidb-cloud/connected-lark-ticket-interaction.md) ) | <li></li>        | <li></li>  | <li></li>  | ✔                     |
| テクニカルアカウントマネージャー                                                                                                                                  | <li></li>        | <li></li>  | <li></li>  | ✔                     |

> **注記**
>
> 4 つのサポート プランすべてのお客様は、サービス リクエストに[PingCAPサポートポータル](https://tidb.support.pingcap.com/)を利用できます。

## 従来のサポートサービスとConnected Careサポートサービスの違い {#differences-between-legacy-support-services-and-connected-care-support-services}

Connected Care サービスのサポート プランでは、次のようなまったく新しい機能セットが導入されています。

-   コネクテッド：クリニックサービス

    この機能は、高度な監視および診断サービスである「クリニック」を提供します。このサービスは、詳細な分析と実用的な洞察に基づいて、パフォーマンスの問題を迅速に特定し、データベースを最適化し、全体的なパフォーマンスを向上させるように設計されています。詳細については、 [コネクテッド：クリニックサービス](/tidb-cloud/tidb-cloud-clinic.md)ご覧ください。

-   接続：IMでのAIチャット

    この機能を使用すると、インスタントメッセージ（IM）ツールを介してAIアシスタントとチャットし、質問への回答をすぐに受け取ることができます。詳細については、 [接続：IMでのAIチャット](/tidb-cloud/connected-ai-chat-in-im.md)ご覧ください。

-   接続済み: TiDB Cloudアラートの IM サブスクリプション

    この機能を使用すると、IMツール経由でアラート通知を簡単に購読でき、重要な更新情報を常に把握できます。詳細については、 [Slackで登録する](/tidb-cloud/monitor-alert-slack.md)と[Zoomで登録する](/tidb-cloud/monitor-alert-zoom.md)ご覧ください。

-   接続: IMチケットの作成とサブスクリプションの更新

    この機能を使用すると、IMツールを通じてサポートチケットを作成し、サポートチケットの更新情報を購読できます。詳細については、 [Slack 経由でチケットを作成し、チケットの更新を購読する](/tidb-cloud/connected-slack-ticket-creation.md)と[Larkでチケットを作成し、チケットの更新を購読する](/tidb-cloud/connected-lark-ticket-creation.md)ご覧ください。

-   接続: サポートチケットの IM によるやり取り

    この機能により、IMツールを介してサポートチケットを迅速に作成し、やり取りすることで、効率的なコミュニケーションを実現できます。詳細については、 [Slack経由でサポートチケットとやり取りする](/tidb-cloud/connected-slack-ticket-interaction.md)と[Lark経由でサポートチケットとやり取りする](/tidb-cloud/connected-lark-ticket-interaction.md)ご覧ください。

これらの新機能により、Connected Care サービスは、より優れた接続性、よりパーソナライズされたサポート、さまざまな顧客ニーズに対応するコスト効率の高いソリューションを提供します。

-   新しい**エンタープライズ**および**プレミアム**プラン: Clinic の高度な監視サービス、 TiDB Cloudアラートの IM サブスクリプション、チケット更新の IM サブスクリプション、IM での AI チャット、サポート チケットの IM 対話を通じて、最新のコミュニケーション ツールと高度な AI 機能を提供します。

-   新しい**開発者**プラン:**ベーシック**プランと同じコミュニティ チャネル ( [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap)と[不和](https://discord.com/invite/KVRZBR2DrG) ) と[TiDB.AI](https://tidb.ai/)サポートへのアクセスに加え、直接接続とテクニカル サポートへの無制限のアクセスが提供されます。

-   新しい**ベーシック**プラン: コミュニティ チャネル ( [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap)と[不和](https://discord.com/invite/KVRZBR2DrG) ) に参加して他のコミュニティ メンバーと交流したり、 [TiDB.AI](https://tidb.ai/)使用して技術サポートを受けることができます。

## コネクテッドケアへの移行 {#transition-to-connected-care}

次の表に、従来のサポート プランのシャットダウン スケジュールを示します。

| サポートプラン                        | シャットダウン日   |
| :----------------------------- | :--------- |
| レガシー**ベーシック**プラン               | 2025年2月17日 |
| レガシー**スタンダード**プラン              | 2025年2月17日 |
| 従来の**エンタープライズ**および**プレミアム**プラン | 2026年1月15日 |

レガシーサポートプランが終了すると、 TiDB Cloudサポートされなくなります。該当する終了日までに Connected Care のサポートプランに移行されない場合、Connected Care の**Basic**サポートプランに自動的に移行されます。

## よくある質問 {#faqs}

### 現在のサポート プランを確認または変更するにはどうすればよいですか? {#how-do-i-check-or-make-changes-to-my-current-support-plan}

[TiDB Cloudコンソール](https://tidbcloud.com/)で、左下隅の**「サポート」を**クリックします。 **「サポート」**ページが表示され、現在のサポートプランが**「CURRENT」**タグで強調表示されます。

**プレミアム**サポートプランを除き、**サポート**ページから新しいサポートプランに移行できます。**プレミアム**プランにアップグレードするには、 [営業担当者に問い合わせる](https://www.pingcap.com/contact-us)クリックしてください。

### 同様のサービスには追加料金を支払う必要がありますか? {#do-i-need-to-pay-more-for-similar-services}

新しいConnected Careサービスは、より包括的で豊富な機能を備えたサポートエクスペリエンスを提供しますが、価格は従来のサービスとほぼ同等です。TiDB TiDB Cloudは、お客様のビジネスをより良くサポートするために、付加価値の提供に引き続き尽力してまいります。

### 従来の<strong>ベーシック</strong>プランが終了した後、テクニカル サポートを受けるにはどうすればよいですか? {#how-can-i-get-technical-support-after-the-legacy-strong-basic-strong-plan-shuts-down}

[請求とアカウントサポート](/tidb-cloud/tidb-cloud-support.md#create-an-account-or-billing-support-ticket)引き続きアクセスできます。テクニカルサポートをご希望の場合は、Connected Care サービスのサポートプランのご購入をご検討ください。1ヶ月の無料トライアルが含まれる**開発者**プランから始めることをお勧めします。
