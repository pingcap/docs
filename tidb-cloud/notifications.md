---
title: Notifications in the TiDB Cloud Console
summary: TiDB Cloudコンソールにおける通知について、通知の種類、目的、表示方法などを学びましょう。
---

# TiDB Cloudコンソールの通知 {#notifications-in-the-tidb-cloud-console}

[TiDB Cloudコンソール](https://tidbcloud.com/)重要なアップデート、システムメッセージ、製品変更、請求リマインダー、その他の関連情報について通知を提供します。これらの通知により、コンソールから離れることなく最新情報を把握し、必要なアクションを実行できます。

## 通知の種類 {#notification-types}

TiDB Cloudコンソールでは、次のようなさまざまな種類の通知を受け取る可能性があります。

-   **情報通知**

    機能の使い方に関するヒント、アプリケーションの変更点、今後のイベントのリマインダーなど、役立つ最新情報を提供します。

-   **実行可能な通知**

    クレジットカードの追加など、特定の操作を実行するように促します。

-   **アラート通知**

    システムエラー、セキュリティ警告、重要なアップデートなど、即時対応が必要な重大な問題や緊急の事態について通知します。

-   **請求通知**

    クレジットや割引に関する最新情報など、請求関連の活動に関する最新情報を配信します。

-   **フィードバック通知**

    最近の操作を評価したり、アンケートに回答したりするなど、機能の使用体験に関するフィードバックをリクエストしてください。

## 通知リスト {#notifications-list}

以下の表は、TiDB Cloudで利用可能な通知、そのトリガーイベント、および受信者の一覧です。

| 通知                            | トリガーイベント                                                                                     | 通知受信者                                                                                                     |
| ----------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| TiDB Cloud Starterインスタンスの作成   | [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)インスタンスが作成されます。               | プロジェクトメンバー全員                                                                                              |
| TiDB Cloud Starterインスタンスの削除   | TiDB Cloud Starterインスタンスが削除されました。                                                            | プロジェクトメンバー全員                                                                                              |
| TiDB Cloud Essentialインスタンスの作成 | [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンスが作成されます。           | プロジェクトメンバー全員                                                                                              |
| TiDB Cloud Essentialインスタンスの削除 | [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンスが削除されました。          | プロジェクトメンバー全員                                                                                              |
| TiDB Cloud Dedicatedクラスタの作成   | [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターが作成されます。 | プロジェクトメンバー全員                                                                                              |
| TiDB Cloud Dedicatedクラスタの削除   | TiDB Cloud Dedicatedクラスターが削除されました。                                                           | プロジェクトメンバー全員                                                                                              |
| 組織予算のしきい値アラート                 | 組織の[予算の上限](/tidb-cloud/tidb-cloud-budget.md)達しました。                                           | `Organization Owner` 、 `Organization Billing Manager` 、および`Organization Billing Viewer`                   |
| プロジェクト予算のしきい値アラート             | プロジェクト[予算の上限](/tidb-cloud/tidb-cloud-budget.md)達しました。                                        | `Organization Owner` 、 `Organization Billing Manager` 、 `Organization Billing Viewer` 、および`Project Owner` |
| Starterインスタンスの支出制限しきい値アラート    | 組織内のTiDB Cloud Starterインスタンスの[支出限度額](/tidb-cloud/manage-serverless-spend-limit.md)に達しました。    | `Organization Owner` 、 `Organization Billing Manager` 、 `Organization Billing Viewer` 、および`Project Owner` |
| クレジットの更新                      | 組織の [クレジット](/tidb-cloud/tidb-cloud-billing.md#credits)が適用、完全に使用、回収、または期限切れになります。             | `Organization Owner` 、 `Organization Billing Manager` 、および`Organization Billing Viewer`                   |
| 割引情報                          | 組織向けの[割引](/tidb-cloud/tidb-cloud-billing.md#discounts)は、適用、回収、または期限切れとなります。                  | `Organization Owner` 、 `Organization Billing Manager` 、および`Organization Billing Viewer`                   |
| マーケットプレイスのアップデート              | 組織は、クラウドプロバイダーのマーケットプレイスを通じて、サブスクリプション契約またはサブスクリプション解除契約を締結している。                             | 組織のすべてのメンバー                                                                                               |
| サポートプランの更新                    | 組織のサポートプランの契約内容が変更されました。                                                                     | 組織のすべてのメンバー                                                                                               |

## 通知をビュー {#view-notifications}

通知を表示するには、 [TiDB Cloudコンソール](https://tidbcloud.com/)の左下隅にある**「通知」**をクリックします。

新しい通知が届くと、**通知の**横に未読の通知の数を示す数字が表示されます。
