---
title: Notifications in the TiDB Cloud Console
summary: 通知の種類、目的、表示方法など、 TiDB Cloudコンソールの通知について説明します。
---

# TiDB Cloudコンソールの通知 {#notifications-in-the-tidb-cloud-console}

[TiDB Cloudコンソール](https://tidbcloud.com/)は、重要な更新、システム メッセージ、製品の変更、請求の通知、その他の関連情報について通知を提供します。これらの通知により、コンソールを離れることなく最新情報を入手し、必要なアクションを実行できます。

## 通知の種類 {#notification-types}

TiDB Cloudコンソールでは、次のようなさまざまな種類の通知を受け取る場合があります。

-   **情報通知**

    機能の使用に関するヒント、アプリケーションの変更、今後のイベントのリマインダーなど、役立つ更新情報を提供します。

-   **実用的な通知**

    クレジットカードの追加など、特定のアクションを実行するように促します。

-   **アラート通知**

    システム エラー、セキュリティ警告、重要な更新など、すぐに対処する必要がある重大な問題や緊急イベントを通知します。

-   **請求通知**

    クレジットや割引の更新など、請求関連のアクティビティに関する更新情報を配信します。

-   **フィードバック通知**

    最近のやり取りを評価したり、アンケートに回答したりするなど、機能の使用経験に関するフィードバックをリクエストします。

## 通知リスト {#notifications-list}

次の表は、 TiDB Cloudで利用可能な通知と、そのトリガー イベントおよび受信者を示しています。

| 通知                             | トリガーイベント                                                                                      | 通知受信者                                                                                             |
| ------------------------------ | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| TiDB Cloudサーバーレス クラスターの作成      | [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターが作成されます。     | プロジェクトメンバー全員                                                                                      |
| TiDB Cloud Serverless クラスターの削除 | TiDB Cloud Serverless クラスターが削除されます。                                                           | プロジェクトメンバー全員                                                                                      |
| TiDB Cloud専用クラスターの作成           | [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターが作成されます。          | プロジェクトメンバー全員                                                                                      |
| TiDB Cloud専用クラスタの削除            | TiDB Cloud Dedicated クラスターが削除されます。                                                            | プロジェクトメンバー全員                                                                                      |
| 組織予算しきい値アラート                   | 組織[予算のしきい値](/tidb-cloud/tidb-cloud-budget.md)に到達しました。                                         | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer`                 |
| プロジェクト予算しきい値アラート               | プロジェクト[予算のしきい値](/tidb-cloud/tidb-cloud-budget.md)に到達しました。                                     | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer` `Project Owner` |
| サーバーレス クラスターの支出制限しきい値アラート      | 組織内のTiDB Cloud Serverless クラスターの数が[支出限度額](/tidb-cloud/manage-serverless-spend-limit.md)達しました。 | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer` `Project Owner` |
| クレジットの更新                       | 組織の[クレジット](/tidb-cloud/tidb-cloud-billing.md#credits)適用済み、完全に使用済み、再利用済み、または期限切れです。            | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer`                 |
| 割引の更新                          | 組織の[割引](/tidb-cloud/tidb-cloud-billing.md#discounts)適用、再利用、または期限切れです。                         | `Organization Owner` `Organization Billing Manager` `Organization Billing Viewer`                 |
| マーケットプレイスの更新                   | 組織は、クラウド プロバイダー マーケットプレイスを通じてサブスクリプションまたはサブスクリプション解除を行っています。                                  | 組織メンバー全員                                                                                          |
| サポートプランの更新                     | 組織のサポート プラン サブスクリプションが変更されます。                                                                 | 組織メンバー全員                                                                                          |

## 通知をビュー {#view-notifications}

新しい通知がある場合、青い点が<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9.354 21c.705.622 1.632 1 2.646 1s1.94-.378 2.646-1M18 8A6 6 0 1 0 6 8c0 3.09-.78 5.206-1.65 6.605-.735 1.18-1.102 1.771-1.089 1.936.015.182.054.252.2.36.133.099.732.099 1.928.099H18.61c1.196 0 1.795 0 1.927-.098.147-.11.186-.179.2-.361.014-.165-.353-.755-1.088-1.936C18.78 13.206 18 11.09 18 8Z" stroke-width="inherit"></path></svg> TiDB Cloudコンソールの右下隅にあるアイコンをクリックします。 <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9.354 21c.705.622 1.632 1 2.646 1s1.94-.378 2.646-1M18 8A6 6 0 1 0 6 8c0 3.09-.78 5.206-1.65 6.605-.735 1.18-1.102 1.771-1.089 1.936.015.182.054.252.2.36.133.099.732.099 1.928.099H18.61c1.196 0 1.795 0 1.927-.098.147-.11.186-.179.2-.361.014-.165-.353-.755-1.088-1.936C18.78 13.206 18 11.09 18 8Z" stroke-width="inherit"></path></svg>通知を表示します。

または、<mdsvgicon name="icon-top-account-settings"> TiDB Cloudコンソールの左下隅にある をクリックし、 **[通知] を**クリックしてすべての通知のリストを表示します。特定の通知をクリックすると、詳細が表示されます。</mdsvgicon>
