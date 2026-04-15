---
title: Changefeed
summary: TiDB Cloud changefeed を使用すると、TiDB Cloudから他のデータサービスにデータをストリーミングできます。
---

# 変更フィード {#changefeed}

TiDB Cloud changefeed を使用すると、 TiDB Cloudから他のデータサービスへデータをストリーミングできます。現在、 TiDB Cloud はApache Kafka、MySQL、 TiDB Cloud 、およびクラウドstorageへのデータストリーミングをサポートしています。

> **注記：**
>
> -   現在、 TiDB Cloudでは、 <CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>ごとに最大 100 件の変更フィードのみが許可されます。
> -   現在、 TiDB Cloud、変更フィードごとに最大100個のテーブルフィルタルールしか設定できません。
> -   [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)インスタンスでは、変更フィード機能は利用できません。
> -   [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンスの場合、変更フィード機能はベータ版です。詳細については、 [変更フィード（ベータ版）](/tidb-cloud/essential-changefeed-overview.md)を参照してください。

## Changefeedページをビュー {#view-the-changefeed-page}

変更フィード機能にアクセスするには、以下の手順に従ってください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>インスタンスの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[データ]** &gt; **[変更フィード]**をクリックします。チェンジフィードページが表示されます。

**変更フィード**ページでは、変更フィードの作成、既存の変更フィードの一覧表示、および既存の変更フィードの操作（変更フィードの拡大縮小、一時停止、再開、編集、削除など）を行うことができます。

## 変更フィードを作成する {#create-a-changefeed}

変更フィードを作成するには、チュートリアルを参照してください。

-   [Apache Kafkaへのシンク](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
-   [MySQLにシンクする](/tidb-cloud/changefeed-sink-to-mysql.md)
-   [TiDB Cloudにシンクする](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)
-   [クラウドstorageにシンクする](/tidb-cloud/changefeed-sink-to-cloud-storage.md)

## クエリ変更フィード容量 {#query-changefeed-capacity}

<CustomContent plan="dedicated">

TiDB Cloud Dedicatedでは、変更フィードの TiCDC レプリケーション容量ユニット (RCU) を照会できます。

1.  ターゲットのTiDB Cloud Dedicatedクラスターの[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  クエリを実行したい対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[ビュー]**をクリックします。
3.  現在のTiCDCレプリケーション容量ユニット（RCU）は、ページの**仕様**欄で確認できます。

</CustomContent>
<CustomContent plan="premium">

TiDB Cloud Premiumでは、チェンジフィードのTiCDC Changefeed容量ユニット（CCU）を照会できます。

1.  ターゲットのTiDB Cloud Premium インスタンスの[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  クエリを実行したい対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[ビュー]**をクリックします。
3.  TiCDC Changefeedの現在の容量ユニット（CCU）は、ページの**仕様**欄で確認できます。

</CustomContent>

## 変更フィードを拡張する {#scale-a-changefeed}

<CustomContent plan="dedicated">

変更フィードのスケールアップまたはスケールダウンを行うことで、変更フィードの TiCDC レプリケーション容量ユニット (RCU) を変更できます。

> **注記：**
>
> -   TiDB Cloud Dedicatedクラスターの変更フィードをスケーリングするには、このクラスターのすべての変更フィードが 2023 年 3 月 28 日以降に作成されていることを確認してください。
> -   TiDB Cloud Dedicatedクラスターに 2023 年 3 月 28 日より前に作成された変更フィードがある場合、このクラスターの既存の変更フィードも新しく作成された変更フィードもスケールアップまたはスケールダウンをサポートしません。

</CustomContent>
<CustomContent plan="premium">

チェンジフィードのTiCDC Changefeed容量ユニット（CCU）は、チェンジフィードのスケールアップまたはスケールダウンによって変更できます。

</CustomContent>

1.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>の[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  拡大縮小したい対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[拡大/縮小]**をクリックします。
3.  新しい仕様を選択してください。
4.  **「送信」**をクリックしてください。

スケーリング処理の完了には約10分かかります（この間、changefeedは通常通り動作します）。新しい仕様への切り替えには数秒かかります（この間、changefeedは一時停止され、自動的に再開されます）。

## 変更フィードを一時停止または再開する {#pause-or-resume-a-changefeed}

1.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>の[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  一時停止または再開したい該当する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止/再開]**をクリックします。

## 変更フィードを編集する {#edit-a-changefeed}

> **注記：**
>
> TiDB Cloud現在、一時停止状態の変更フィードの編集のみが許可されています。

1.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>の[**変更フィード**](#view-the-changefeed-page)ページに移動します。

2.  一時停止したい変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止]**をクリックします。

3.  変更フィードのステータスが`Paused`に変更されたら、 **[...]** &gt; **[編集]**をクリックして、対応する変更フィードを編集します。

    TiDB Cloudはデフォルトで変更フィードの設定を自動的に行います。以下の設定を変更できます。

    -   Apache Kafkaシンク：すべての設定。
    -   MySQLシンク： **MySQL接続**、**テーブルフィルタ**、および**イベントフィルタ**。
    -   TiDB Cloudシンク: **TiDB Cloud接続**、**テーブルフィルタ**、および**イベントフィルタ**。
    -   クラウドstorageシンク：**ストレージエンドポイント**、**テーブルフィルタ**、および**イベントフィルタ**。

4.  設定を編集した後、 **[...]** &gt; **[再開]**をクリックして、対応する変更フィードを再開します。

## 変更フィードを複製する {#duplicate-a-changefeed}

1.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>の[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  複製したい変更フィードを探します。**アクション**列で、 **...** &gt;**複製を**クリックします。
3.  TiDB Cloudは、新しい変更フィード設定に元の設定を自動的に反映します。必要に応じて設定を確認および変更できます。
4.  設定を確認後、 **「送信」**をクリックして新しい変更フィードを作成して開始します。

## 変更フィードを削除する {#delete-a-changefeed}

1.  ターゲットの<CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent>の[**変更フィード**](#view-the-changefeed-page)ページに移動します。
2.  削除したい該当する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[削除]**をクリックします。

## Changefeedの請求 {#changefeed-billing}

TiDB Cloudでの変更フィードの請求については、[Changefeedの請求](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md)参照してください。

## Changefeedの状態 {#changefeed-states}

レプリケーションタスクの状態は、その実行中の状態を表します。実行中に、レプリケーションタスクはエラーで失敗したり、手動で一時停止または再開されたりすることがあります。これらの動作によって、レプリケーションタスクの状態が変化する可能性があります。

各州は以下のように説明されます。

-   `CREATING` : レプリケーションタスクが作成されています。
-   `RUNNING` : レプリケーション タスクは正常に実行され、チェックポイント ts も正常に進行します。
-   `EDITING` : レプリケーションタスクが編集されています。
-   `PAUSING` : レプリケーション タスクが一時停止されています。
-   `PAUSED` : レプリケーション タスクが一時停止されました。
-   `RESUMING` : レプリケーションタスクが再開されます。
-   `DELETING` : レプリケーション タスクが削除されています。
-   `DELETED` : レプリケーション タスクが削除されました。
-   `WARNING` : レプリケーション タスクが警告を返します。回復可能なエラーのため、レプリケーションを続行できません。この状態の変更フィードは、状態が`RUNNING`に遷移するまで再開を試み続けます。この状態の変更フィードは[GCオペレーション](https://docs.pingcap.com/tidb/stable/garbage-collection-overview)ブロックします 。
-   `FAILED` : レプリケーション タスクが失敗しました。エラーが発生したため、レプリケーション タスクを再開できず、自動的に復旧することもできません。増分データのガベージコレクション(GC) の前に問題が解決された場合は、失敗した変更フィードを手動で再開できます。増分データのデフォルトの有効期間 (TTL) は 24 時間です。つまり、変更フィードが中断されてから 24 時間以内に GC メカニズムによってデータが削除されることはありません。
