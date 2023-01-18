---
title: Changefeed
---

# チェンジフィード {#changefeed}

TiDB Cloud changefeed は、 TiDB Cloudから他のデータ サービスにデータをストリーミングするのに役立ちます。現在、 TiDB Cloudは Apache Kafka と MySQL へのストリーミング データをサポートしています。

> **ノート：**
>
> changefeed 機能を使用するには、TiDB クラスターのバージョンが v6.4.0 以降であり、TiKV ノードのサイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。
>
> 現在、 TiDB Cloudでは、クラスターごとに最大 10 個の変更フィードしか許可されていません。
>
> [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)の場合、changefeed 機能は使用できません。

変更フィード機能にアクセスするには、 **TiDB**クラスターのクラスター概要ページに移動し、左側のナビゲーション ウィンドウで [変更フィード] をクリックします。チェンジフィード一覧が表示されます。

changefeed リストでは、次のことができます。

-   変更フィードの ID、チェックポイント、ステータスなど、作成された変更フィードの情報をビューします。
-   チェンジフィードの作成、一時停止、再開、編集、削除など、チェンジフィードを操作します。

## チェンジフィードを作成する {#create-a-changefeed}

変更フィードを作成するには、次のチュートリアルを参照してください。

-   [Apache Kafka にシンクする](/tidb-cloud/changefeed-sink-to-apache-kafka.md) (ベータ)
-   [MySQL にシンク](/tidb-cloud/changefeed-sink-to-mysql.md)

## チェンジフィードを削除する {#delete-a-changefeed}

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで [ **Changefeed** ] をクリックします。
2.  削除する対応する変更フィードを見つけて、[**アクション**] 列で [ <strong>...</strong> ] &gt; <strong>[削除</strong>] をクリックします。

## チェンジフィードを一時停止または再開する {#pause-or-resume-a-changefeed}

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで [ **Changefeed** ] をクリックします。
2.  一時停止または再開する対応する変更フィードを見つけて、[**アクション**] 列で [ <strong>...</strong> ] &gt; [<strong>一時停止/再開</strong>] をクリックします。

## チェンジフィードを編集する {#edit-a-changefeed}

> **ノート：**
>
> TiDB Cloudでは現在、一時停止状態の変更フィードのみを編集できます。

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで [ **Changefeed** ] をクリックします。

2.  一時停止する変更フィードを見つけて、[**アクション**] 列で [ <strong>...</strong> ] &gt; [<strong>一時停止</strong>] をクリックします。

3.  changefeed ステータスが`Paused`に変わったら、[ **...** ] &gt; [<strong>編集</strong>] をクリックして、対応する changefeed を編集します。

    TiDB Cloudは、デフォルトで changefeed 構成を取り込みます。次の構成を変更できます。

    -   MySQL シンク: **MySQL 接続**と<strong>テーブル フィルター</strong>。
    -   Kafka シンク: すべての構成。

4.  構成を編集したら、[ **...** ] &gt; [<strong>再開</strong>] をクリックして、対応する変更フィードを再開します。

## TiCDC RCU のクエリ {#query-ticdc-rcus}

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで [ **Changefeed** ] をクリックします。
2.  ページの左上隅に、現在の TiCDC レプリケーション キャパシティ ユニット (RCU) が表示されます。

## 変更フィードの請求 {#changefeed-billing}

TiDB Cloudでの変更フィードの課金については、 [変更フィードの請求](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md)を参照してください。
