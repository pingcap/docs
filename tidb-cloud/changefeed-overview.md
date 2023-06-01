---
title: Changefeed
---

# チェンジフィード {#changefeed}

TiDB Cloudチェンジフィードは、 TiDB Cloudから他のデータ サービスにデータをストリーミングするのに役立ちます。現在、 TiDB Cloud は、 Apache Kafka および MySQL へのストリーミング データをサポートしています。

> **ノート：**
>
> チェンジフィード機能を使用するには、TiDB クラスターのバージョンが v6.4.0 以降であり、TiKV ノードのサイズが少なくとも 8 vCPU および 16 GiB であることを確認してください。
>
> 現在、 TiDB Cloudクラスターごとに最大 10 個の変更フィードのみが許可されます。
>
> [<a href="/tidb-cloud/select-cluster-tier.md#serverless-tier-beta">Serverless Tierクラスター</a>](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)の場合、チェンジフィード機能は使用できません。

チェンジフィード機能にアクセスするには、TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[チェンジフィード]**をクリックします。チェンジフィード一覧が表示されます。

変更フィード リストでは、次のことができます。

-   変更フィードの ID、チェックポイント、ステータスなど、作成された変更フィードの情報をビュー。
-   変更フィードの作成、一時停止、再開、編集、削除など、変更フィードを操作します。

## 変更フィードを作成する {#create-a-changefeed}

チェンジフィードを作成するには、次のチュートリアルを参照してください。

-   [<a href="/tidb-cloud/changefeed-sink-to-apache-kafka.md">Apache Kafka にシンクする</a>](/tidb-cloud/changefeed-sink-to-apache-kafka.md) (ベータ版)
-   [<a href="/tidb-cloud/changefeed-sink-to-mysql.md">MySQL にシンクする</a>](/tidb-cloud/changefeed-sink-to-mysql.md)

## 変更フィードを削除する {#delete-a-changefeed}

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。
2.  削除する対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[削除]**をクリックします。

## チェンジフィードを一時停止または再開する {#pause-or-resume-a-changefeed}

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。
2.  一時停止または再開する対応する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止/再開]**をクリックします。

## 変更フィードを編集する {#edit-a-changefeed}

> **ノート：**
>
> TiDB Cloud現在、一時停止ステータスでのみ変更フィードの編集が可能です。

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。

2.  一時停止する変更フィードを見つけて、 **[アクション]**列の**[...]** &gt; **[一時停止]**をクリックします。

3.  チェンジフィードのステータスが`Paused`に変わったら、 **[...]** &gt; **[編集] を**クリックして、対応するチェンジフィードを編集します。

    TiDB Cloud は、デフォルトで変更フィード構成を設定します。次の構成を変更できます。

    -   MySQL シンク: **MySQL 接続**と**テーブル フィルター**。
    -   Kafka シンク: すべての構成。

4.  構成を編集した後、 **[...]** &gt; **[再開]**をクリックして、対応する変更フィードを再開します。

## TiCDC RCU のクエリ {#query-ticdc-rcus}

1.  ターゲット TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[Changefeed]**をクリックします。
2.  ページの左上隅に現在の TiCDC レプリケーション キャパシティ ユニット (RCU) が表示されます。

## 変更フィードの請求 {#changefeed-billing}

TiDB Cloudでの変更フィードの請求については、 [<a href="/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md">変更フィードの請求</a>](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md)を参照してください。
