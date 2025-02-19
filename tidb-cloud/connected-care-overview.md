---
title: Connected Care Overview
summary: 新しい世代のTiDB Cloudサポート サービスである Connected Care を紹介します。
aliases: ['/tidbcloud/connected-care-announcement']
---

# コネクテッドケアの概要 {#connected-care-overview}

あらゆる規模のお客様がTiDB Cloudでのユースケースと運用を拡大し続けているため、 TiDB Cloud は進化するニーズに対応するためにサポート サービスを再構築することに注力しています。さらに大きな価値とシームレスなエクスペリエンスを提供するために、 TiDB Cloud は**2025 年 2 月 17 日**に新しいサポート サービスである**Connected Care を**開始することを発表します。

この移行の一環として、現在のサポート プランの提供は購入できなくなり、 **2025 年 2 月 17 日**以降はレガシー サポート プランとして分類されます。ただし、 TiDB Cloud は、レガシー プランに加入している顧客に対して、それぞれの[退職日](#transition-to-connected-care)まで引き続き完全なサポートを提供します。

スムーズな移行と最新機能へのアクセスを確保するために、 TiDB Cloud、顧客が Connected Care サービスに移行して導入することを推奨しています。

## コネクテッドケア {#connected-care}

Connected Care サービスは、最新のコミュニケーション ツール、プロアクティブなサポート、高度な AI 機能を通じてTiDB Cloudとの接続を強化し、シームレスで顧客中心のエクスペリエンスを実現するように設計されています。

Connected Care サービスには、 **Basic** 、 **Developer** (従来の**Standard**プランに相当)、 **Enterprise** 、 **Premium の**4 つのサポート プランがあります。

> **注記**
>
> **Basic** 、 **Enterprise** 、および**Premium**サポート プランでは、従来のプランと同じプラン名が使用されていますが、サービス コミットメントが異なる異なるプランを指します。

次の表は、Connected Care サービスの各サポート プランの概要を示しています。詳細については、 [コネクテッドケアの詳細](/tidb-cloud/connected-care-detail.md)参照してください。

| サポートプラン                                                                                                                                         | 基本               | 開発者        | 企業         | プレミアム                |
| :---------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- | :--------- | :--------- | :------------------- |
| 推奨されるワークロード                                                                                                                                     | 個人または初心者向けプロジェクト | 開発中のワークロード | 本番中のワークロード | 本番のビジネスクリティカルなワークロード |
| 請求とアカウントのサポート                                                                                                                                   | ✔                | ✔          | ✔          | ✔                    |
| テクニカルサポート                                                                                                                                       | <li></li>        | ✔          | ✔          | ✔                    |
| 初期応答時間                                                                                                                                          | <li></li>        | 営業時間       | 7x24       | 7x24                 |
| [コネクテッド：クリニックサービス](/tidb-cloud/tidb-cloud-clinic.md)                                                                                            | <li></li>        | <li></li>  | ✔          | ✔                    |
| [接続: IM での AI チャット](/tidb-cloud/connected-ai-chat-in-im.md)                                                                                     | <li></li>        | <li></li>  | ✔          | ✔                    |
| 接続済み: TiDB Cloudアラートの IM サブスクリプション ( [スラック](/tidb-cloud/monitor-alert-slack.md) 、 [ズーム](/tidb-cloud/monitor-alert-zoom.md) )                    | <li></li>        | <li></li>  | ✔          | ✔                    |
| 接続済み: IM チケットの作成とサブスクリプションの更新 ( [スラック](/tidb-cloud/connected-slack-ticket-creation.md) 、 [ラーク](/tidb-cloud/connected-lark-ticket-creation.md) ) | <li></li>        | <li></li>  | ✔          | ✔                    |
| 接続済み: サポート チケットの IM 対話 ( [スラック](/tidb-cloud/connected-slack-ticket-interaction.md) 、 [ラーク](/tidb-cloud/connected-lark-ticket-interaction.md) )  | <li></li>        | <li></li>  | <li></li>  | ✔                    |
| テクニカルアカウントマネージャー                                                                                                                                | <li></li>        | <li></li>  | <li></li>  | ✔                    |

> **注記**
>
> 4 つのサポート プランすべてのお客様は、サービス リクエストに[PingCAP サポートポータル](https://tidb.support.pingcap.com/)利用できます。

## 従来のサポート サービスと Connected Care サポート サービスの違い {#differences-between-legacy-support-services-and-connected-care-support-services}

Connected Care サービスのサポート プランでは、次のようなまったく新しい機能セットが導入されています。

-   コネクテッド：クリニックサービス

    この機能は、パフォーマンスの問題を迅速に特定し、データベースを最適化し、詳細な分析と実用的な洞察によって全体的なパフォーマンスを向上させるために設計された、高度な監視および診断サービスである Clinic を提供します。詳細については、 [コネクテッド：クリニックサービス](/tidb-cloud/tidb-cloud-clinic.md)参照してください。

-   接続: IM での AI チャット

    この機能を使用すると、インスタント メッセージ (IM) ツールを通じて AI アシスタントとチャットし、質問に対する回答をすぐに受け取ることができます。詳細については、 [接続: IM での AI チャット](/tidb-cloud/connected-ai-chat-in-im.md)参照してください。

-   接続済み: TiDB Cloudアラートの IM サブスクリプション

    この機能により、IM ツール経由でアラート通知を簡単に購読できるようになり、重要な更新についての最新情報を入手できます。詳細については、 [Slackで登録する](/tidb-cloud/monitor-alert-slack.md)および[Zoomで登録する](/tidb-cloud/monitor-alert-zoom.md)参照してください。

-   接続: IM チケットの作成とサブスクリプションの更新

    この機能を使用すると、IM ツールを使用してサポート チケットを作成し、サポート チケットの更新をサブスクライブすることができます。詳細については、 [Slack 経由でチケットを作成し、チケットの更新を購読する](/tidb-cloud/connected-slack-ticket-creation.md)および[Lark 経由でチケットを作成し、チケットの更新を購読する](/tidb-cloud/connected-lark-ticket-creation.md)参照してください。

-   接続: サポートチケットの IM 対話

    この機能により、IM ツールを使用してサポート チケットをすばやく作成し、やり取りして、コミュニケーションを効率化できます。詳細については、 [Slack経由でサポートチケットとやり取りする](/tidb-cloud/connected-slack-ticket-interaction.md)および[Lark経由でサポートチケットとやり取りする](/tidb-cloud/connected-lark-ticket-interaction.md)参照してください。

これらの新機能により、Connected Care サービスは、より優れた接続性、よりパーソナライズされたサポート、さまざまな顧客ニーズに対応するコスト効率の高いソリューションを提供します。

-   新しい**エンタープライズ**および**プレミアム**プラン: Clinic の高度な監視サービス、 TiDB Cloudアラートの IM サブスクリプション、チケット更新の IM サブスクリプション、IM での AI チャット、サポート チケットの IM 対話を通じて、最新のコミュニケーション ツールと高度な AI 機能を顧客に提供します。

-   新しい**開発者**プラン: お客様は、**ベーシック**プランと同じコミュニティと[ティDB.AI](https://tidb.ai/)サポートにアクセスできるほか、無制限のテクニカル サポートに直接接続して接続することもできます。

-   新しい**ベーシック**プラン: お客様はアクティブなコミュニティ チャネルに参加するように案内され、そこで他のコミュニティ メンバーと交流したり、 [ティDB.AI](https://tidb.ai/)とやり取りして技術サポートを受けることができます。

## コネクテッドケアへの移行 {#transition-to-connected-care}

次の表に、従来のサポート プランのシャットダウン スケジュールを示します。

| サポートプラン                        | シャットダウン日   |
| :----------------------------- | :--------- |
| レガシー**ベーシック**プラン               | 2025年2月17日 |
| レガシー**スタンダード**プラン              | 2025年2月17日 |
| 従来の**エンタープライズ**および**プレミアム**プラン | 2026年1月15日 |

レガシー サポート プランがシャットダウンされると、 TiDB Cloudサポートされなくなります。該当するシャットダウン日までに Connected Care のどのサポート プランにも移行しない場合は、Connected Care の**Basic**サポート プランに自動的に移行されます。

## よくある質問 {#faqs}

### 現在のサポート プランを確認または変更するにはどうすればよいですか? {#how-do-i-check-or-make-changes-to-my-current-support-plan}

TiDB Cloudコンソールの[サポート](https://tidbcloud.com/console/org-settings/support)ページにアクセスします。現在のサポート プランは、ページの左上領域に表示されます。

2025 年 2 月 17 日より、**プレミアム**サポート プランを除き、 [サポート](https://tidbcloud.com/console/org-settings/support)ページから新しいサポート プランに移行できます。**プレミアム**プランにアップグレードするには、 [営業担当に問い合わせる](https://www.pingcap.com/contact-us)実行してください。

### 同様のサービスには追加料金を支払う必要がありますか? {#do-i-need-to-pay-more-for-similar-services}

新しい Connected Care サービスは、より包括的で機能豊富なサポート エクスペリエンスを提供しますが、価格は以前のサービスとほぼ同じです。TiDB TiDB Cloud は、お客様の取り組みをより良くサポートするために、付加価値を提供することに引き続き注力しています。

### 従来の<strong>Basic</strong>プランが終了した後、テクニカル サポートを受けるにはどうすればよいですか? {#how-can-i-get-technical-support-after-the-legacy-strong-basic-strong-plan-shuts-down}

[請求とアカウントのサポート](/tidb-cloud/tidb-cloud-support.md#create-an-account-or-billing-support-ticket)引き続きアクセスできます。テクニカル サポートについては、Connected Care サービスのサポート プランの購入を検討してください。1 か月の無料トライアルが含まれる**開発者**プランから始めることをお勧めします。
