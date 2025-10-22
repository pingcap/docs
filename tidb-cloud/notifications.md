---
title: Notifications in the TiDB Cloud Console
summary: 通知の種類、目的、表示方法など、 TiDB Cloudコンソールの通知について説明します。
---

# TiDB Cloudコンソールの通知 {#notifications-in-the-tidb-cloud-console}

[TiDB Cloudコンソール](https://tidbcloud.com/) 、重要なアップデート、システムメッセージ、製品の変更、請求リマインダー、その他の関連情報をお知らせする通知機能を提供します。これらの通知により、コンソールを離れることなく最新情報を入手し、必要なアクションを実行できます。

## 通知の種類 {#notification-types}

TiDB Cloudコンソールでは、次のようなさまざまな種類の通知を受け取る場合があります。

-   **情報通知**

    機能の使用に関するヒント、アプリケーションの変更、今後のイベントのリマインダーなどの役立つ更新情報を提供します。

-   **実用的な通知**

    クレジットカードの追加など、特定のアクションを実行するように要求します。

-   **アラート通知**

    システム エラー、セキュリティ警告、重要な更新など、すぐに対応する必要がある重大な問題や緊急イベントを通知します。

-   **請求通知**

    クレジットや割引の更新など、請求関連のアクティビティに関する最新情報を配信します。

-   **フィードバック通知**

    最近のやり取りを評価したり、アンケートに回答したりするなど、機能の使用経験に関するフィードバックをリクエストします。

## 通知リスト {#notifications-list}

次の表は、 TiDB Cloudで使用できる通知と、そのトリガー イベントおよび受信者を示しています。

| 通知                            | トリガーイベント                                                                                   | 通知受信者                                                                                             |
| ----------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| TiDB Cloud Starter クラスターの作成   | [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)クラスターが作成されます。                 | プロジェクトメンバー全員                                                                                      |
| TiDB Cloud Starter クラスターの削除   | TiDB Cloud Starter クラスターが削除されます。                                                           | プロジェクトメンバー全員                                                                                      |
| TiDB Cloud Essential クラスターの作成 | [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターが作成されます。             | プロジェクトメンバー全員                                                                                      |
| TiDB Cloud Essential クラスタの削除  | [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターが削除されます。             | プロジェクトメンバー全員                                                                                      |
| TiDB Cloud専用クラスタの作成           | [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターが作成されます。       | プロジェクトメンバー全員                                                                                      |
| TiDB Cloud専用クラスタの削除           | TiDB Cloud Dedicated クラスターが削除されます。                                                         | プロジェクトメンバー全員                                                                                      |
| 組織予算しきい値アラート                  | 組織[予算のしきい値](/tidb-cloud/tidb-cloud-budget.md)に到達しました。                                      | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer`                 |
| プロジェクト予算しきい値アラート              | プロジェクト[予算のしきい値](/tidb-cloud/tidb-cloud-budget.md)に到達しました。                                  | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer` `Project Owner` |
| スターター クラスターの支出制限しきい値アラート      | 組織内のTiDB Cloud Starter クラスターの数が[支出限度額](/tidb-cloud/manage-serverless-spend-limit.md)達しました。 | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer` `Project Owner` |
| クレジットの更新                      | 組織の[クレジット](/tidb-cloud/tidb-cloud-billing.md#credits)は適用済み、完全に使用済み、再利用済み、または期限切れです。        | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer`                 |
| 割引の更新                         | 組織の[割引](/tidb-cloud/tidb-cloud-billing.md#discounts)が適用、再利用、または期限切れです。                     | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer`                 |
| マーケットプレイスのアップデート              | 組織は、クラウド プロバイダー マーケットプレイスを通じてサブスクリプションまたはサブスクリプション解除を行っています。                               | 組織の全メンバー                                                                                          |
| サポートプランの更新                    | 組織のサポート プラン サブスクリプションが変更されます。                                                              | 組織の全メンバー                                                                                          |

## 通知をビュー {#view-notifications}

通知を表示するには、 [TiDB Cloudコンソール](https://tidbcloud.com/)の左下隅にある**[通知]**をクリックします。

新しい通知がある場合、 **「通知」の**横に未読の通知の数を示す数字が表示されます。
