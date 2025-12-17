---
title: Changefeed
summary: TiDB Cloudチェンジフィードは、 TiDB Cloudから他のデータ サービスにデータをストリーミングするのに役立ちます。
---

# チェンジフィード {#changefeed}

TiDB Cloud changefeed は、 TiDB Cloudから他のデータサービスへのデータストリーミングをサポートします。現在、 TiDB Cloud はApache Kafka、MySQL、 TiDB Cloud 、クラウドstorageへのデータストリーミングをサポートしています。

> **注記：**
>
> -   現在、 TiDB Cloud、1アカウントあたり最大100件の変更フィードしか許可されていません。<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>。
> -   現在、 TiDB Cloud、変更フィードごとに最大 100 個のテーブル フィルター ルールのみが許可されます。
> -   クラスター[TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)および[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)では、changefeed 機能は使用できません。

## Changefeedページをビュー {#view-the-changefeed-page}

changefeed 機能にアクセスするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、<customcontent plan="dedicated">プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。</customcontent><customcontent plan="premium"> [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。</customcontent>

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲットの名前をクリックします<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>概要ページに移動し、左側のナビゲーションペインで**「データ」** &gt; **「Changefeed」**をクリックします。Changefeedページが表示されます。

**Changefeed**ページでは、変更フィードを作成したり、既存の変更フィードの一覧を表示したり、既存の変更フィードを操作したり (変更フィードのスケーリング、一時停止、再開、編集、削除など) できます。

## チェンジフィードを作成する {#create-a-changefeed}

チェンジフィードを作成するには、チュートリアルを参照してください。

-   [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
-   [MySQLに沈む](/tidb-cloud/changefeed-sink-to-mysql.md)
-   [TiDB Cloudにシンク](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)
-   [クラウドstorageに保存](/tidb-cloud/changefeed-sink-to-cloud-storage.md)

## クエリ変更フィード容量 {#query-changefeed-capacity}

<CustomContent plan="dedicated">

TiDB Cloud Dedicated では、変更フィードの TiCDC レプリケーション容量単位 (RCU) を照会できます。

1.  ターゲット TiDB クラスターの[**チェンジフィード**](#view-the-changefeed-page)ページに移動します。
2.  クエリを実行する対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[ビュー]**をクリックします。
3.  現在の TiCDC レプリケーション容量単位 (RCU) は、ページの**仕様**領域で確認できます。

</CustomContent>
<CustomContent plan="premium">

TiDB Cloud Premium では、変更フィードのTiCDC Changefeedフィード容量単位 (CCU) を照会できます。

1.  ターゲット TiDB インスタンスの[**チェンジフィード**](#view-the-changefeed-page)ページに移動します。
2.  クエリを実行する対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[ビュー]**をクリックします。
3.  現在のTiCDC Changefeed容量単位 (CCU) は、ページの**仕様**領域で確認できます。

</CustomContent>

## チェンジフィードをスケールする {#scale-a-changefeed}

<CustomContent plan="dedicated">

変更フィードをスケールアップまたはスケールダウンすることで、変更フィードの TiCDC レプリケーション容量単位 (RCU) を変更できます。

> **注記：**
>
> -   クラスターの変更フィードをスケーリングするには、このクラスターのすべての変更フィードが 2023 年 3 月 28 日以降に作成されていることを確認してください。
> -   クラスターに 2023 年 3 月 28 日より前に作成された変更フィードがある場合、このクラスターの既存の変更フィードも新しく作成された変更フィードもスケールアップまたはスケールダウンをサポートしません。

</CustomContent>
<CustomContent plan="premium">

変更フィードをスケールアップまたはスケールダウンすることで、変更フィードのTiCDC Changefeed容量単位 (CCU) を変更できます。

</CustomContent>

1.  対象のTiDBの[**チェンジフィード**](#view-the-changefeed-page)ページ目に移動します<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>。
2.  スケールする対応する変更フィードを見つけて、 **[アクション]**列で**[...]** &gt; **[スケール アップ/ダウン]**をクリックします。
3.  新しい仕様を選択します。
4.  **［送信］**をクリックします。

スケーリング プロセスが完了するまでに約 10 分 (その間、変更フィードは正常に動作します)、新しい仕様に切り替えるまでに数秒 (その間、変更フィードは一時停止され、自動的に再開されます) かかります。

## チェンジフィードを一時停止または再開する {#pause-or-resume-a-changefeed}

1.  対象のTiDBの[**チェンジフィード**](#view-the-changefeed-page)ページ目に移動します<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>。
2.  一時停止または再開する対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止/再開]**をクリックします。

## 変更フィードを編集する {#edit-a-changefeed}

> **注記：**
>
> TiDB Cloud現在、一時停止状態の変更フィードのみ編集できます。

1.  対象のTiDBの[**チェンジフィード**](#view-the-changefeed-page)ページ目に移動します<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>。

2.  一時停止する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止]**をクリックします。

3.  changefeed のステータスが`Paused`に変更されたら、 **[...]** &gt; **[編集]**をクリックして、対応する changefeed を編集します。

    TiDB Cloud はデフォルトで changefeed 設定を設定します。以下の設定を変更できます。

    -   Apache Kafka シンク: すべての構成。
    -   MySQL シンク: **MySQL 接続**、**テーブル フィルター**、および**イベント フィルター**。
    -   TiDB Cloudシンク: **TiDB Cloud接続**、**テーブル フィルター**、および**イベント フィルター**。
    -   クラウドstorageシンク:**ストレージ エンドポイント**、**テーブル フィルター**、**イベント フィルター**。

4.  設定を編集した後、 **[...]** &gt; **[再開]**をクリックして、対応する変更フィードを再開します。

## チェンジフィードを複製する {#duplicate-a-changefeed}

1.  対象のTiDBの[**チェンジフィード**](#view-the-changefeed-page)ページ目に移動します<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>。
2.  複製したい変更フィードを見つけます。 **「アクション」**列で、 **「...」** &gt; **「複製」を**クリックします。
3.  TiDB Cloud は、新しい変更フィード設定に元の設定を自動的に入力します。必要に応じて設定を確認し、変更できます。
4.  設定を確認したら、 **[送信]**をクリックして新しい変更フィードを作成し、開始します。

## 変更フィードを削除する {#delete-a-changefeed}

1.  対象のTiDBの[**チェンジフィード**](#view-the-changefeed-page)ページ目に移動します<customcontent plan="dedicated">クラスタ</customcontent><customcontent plan="premium">実例</customcontent>。
2.  削除する対応する変更フィードを見つけて、 **[アクション]**列で**[...]** &gt; **[削除]**をクリックします。

## チェンジフィード課金 {#changefeed-billing}

TiDB Cloudの変更フィードに対する課金の詳細については、 [チェンジフィード課金](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md)参照してください。

## チェンジフィードの状態 {#changefeed-states}

レプリケーションタスクの状態は、レプリケーションタスクの実行状態を表します。実行プロセス中に、レプリケーションタスクがエラーで失敗したり、手動で一時停止または再開されたりすることがあります。これらの動作により、レプリケーションタスクの状態が変化する可能性があります。

各状態は次のように説明されます。

-   `CREATING` : レプリケーション タスクを作成中です。
-   `RUNNING` : レプリケーション タスクは正常に実行され、チェックポイント ts は正常に進行します。
-   `EDITING` : レプリケーション タスクが編集中です。
-   `PAUSING` : レプリケーション タスクは一時停止されています。
-   `PAUSED` : レプリケーション タスクは一時停止されています。
-   `RESUMING` : レプリケーション タスクが再開されています。
-   `DELETING` : レプリケーション タスクが削除されています。
-   `DELETED` : レプリケーション タスクは削除されます。
-   `WARNING` : レプリケーションタスクが警告を返しました。回復可能なエラーが発生したため、レプリケーションを続行できません。この状態の変更フィードは、状態が`RUNNING`に遷移するまで再開を試行し続けます。この状態の変更フィードは[GC操作](https://docs.pingcap.com/tidb/stable/garbage-collection-overview)ブロックします。
-   `FAILED` : レプリケーションタスクが失敗しました。何らかのエラーが発生したため、レプリケーションタスクを再開できず、自動復旧もできません。増分データのガベージコレクション(GC) 前に問題が解決された場合は、失敗した変更フィードを手動で再開できます。増分データのデフォルトの Time-To-Live (TTL) 期間は 24 時間です。つまり、変更フィードが中断されてから 24 時間以内には、GC メカニズムによってデータが削除されることはありません。
