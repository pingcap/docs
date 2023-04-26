---
title: Integrate TiDB Cloud with Airbyte
summary: Learn how to use Airbyte TiDB connector.
---

# TiDB Cloudと Airbyte を統合する {#integrate-tidb-cloud-with-airbyte}

[エアバイト](https://airbyte.com/)は、抽出、読み込み、変換 (ELT) パイプラインを構築し、データ ウェアハウス、データ レイク、およびデータベース内のデータを統合するオープンソースのデータ統合エンジンです。このドキュメントでは、Airbyte をソースまたは宛先としてTiDB Cloudに接続する方法について説明します。

## エアバイトをデプロイ {#deploy-airbyte}

ほんの数ステップで Airbyte をローカルに展開できます。

1.  ワークスペースに[ドッカー](https://www.docker.com/products/docker-desktop)をインストールします。

2.  Airbyte のソース コードを複製します。

    ```shell
    git clone https://github.com/airbytehq/airbyte.git && \
    cd airbyte
    ```

3.  docker-compose で Docker イメージを実行します。

    ```shell
    docker-compose up
    ```

Airbyte バナーが表示されたら、ユーザー名 ( `airbyte` ) とパスワード ( `password` ) を使用して[http://localhost:8000](http://localhost:8000)に移動し、UI にアクセスできます。

```
airbyte-server      |     ___    _      __          __
airbyte-server      |    /   |  (_)____/ /_  __  __/ /____
airbyte-server      |   / /| | / / ___/ __ \/ / / / __/ _ \
airbyte-server      |  / ___ |/ / /  / /_/ / /_/ / /_/  __/
airbyte-server      | /_/  |_/_/_/  /_.___/\__, /\__/\___/
airbyte-server      |                     /____/
airbyte-server      | --------------------------------------
airbyte-server      |  Now ready at http://localhost:8000/
airbyte-server      | --------------------------------------
```

## TiDB コネクタをセットアップする {#set-up-the-tidb-connector}

便利なことに、TiDB をソースと宛先として設定する手順は同じです。

1.  サイドバーの**[ソース]**または<strong>[宛先]</strong>をクリックし、TiDB タイプを選択して新しい TiDB コネクタを作成します。

2.  次のパラメータを入力します。接続文字列から接続情報を取得するには、 [標準接続で接続](/tidb-cloud/connect-via-standard-connection.md)を参照してください。

    -   ホスト: TiDB Cloudクラスターのエンドポイント
    -   ポート: データベースのポート
    -   データベース: データを同期するデータベース
    -   ユーザー名: データベースにアクセスするためのユーザー名
    -   パスワード: ユーザー名のパスワード

3.  **SSL 接続**を有効にし、 <strong>JDBC URL Params</strong>で TLS プロトコルを<strong>TLSv1.2</strong>または<strong>TLSv1.3</strong>に設定します。

    > ノート：
    >
    > -   TiDB Cloud はTLS 接続をサポートしています。 **TLSv1.2**および<strong>TLSv1.3</strong>で TLS プロトコルを選択できます (例: `enabledTLSProtocols=TLSv1.2` )。
    > -   JDBC 経由でTiDB Cloudへの TLS 接続を無効にする場合は、特に JDBC URL Params で useSSL を`false`に設定し、SSL 接続を閉じる必要があります (例: `useSSL=false` )。
    > -   TiDBServerless TierはTLS 接続のみをサポートします。

4.  [ソースまたは**宛先の**<strong>セットアップ]</strong>をクリックして、コネクタの作成を完了します。次のスクリーンショットは、ソースとしての TiDB の構成を示しています。

![TiDB source configuration](/media/tidb-cloud/integration-airbyte-parameters.jpg)

TiDB から Snowflake、CSV ファイルから TiDB など、ソースと宛先の任意の組み合わせを使用できます。

TiDB コネクタの詳細については、 [TiDB ソース](https://docs.airbyte.com/integrations/sources/tidb)および[TiDB 宛先](https://docs.airbyte.com/integrations/destinations/tidb)を参照してください。

## 接続を設定する {#set-up-the-connection}

ソースと宛先を設定したら、接続を構築して構成できます。

次の手順では、TiDB をソースと宛先の両方として使用します。他のコネクタには異なるパラメータがある場合があります。

1.  サイドバーの**[接続]**をクリックし、 <strong>[新しい接続]</strong>をクリックします。

2.  以前に確立されたソースと宛先を選択します。

3.  [接続**のセットアップ]**パネルに移動し、 `${source_name} - ${destination-name}`などの接続の名前を作成します。

4.  **[レプリケーションの頻度]**を<strong>[24 時間ごと]</strong>に設定します。これは、接続が 1 日に 1 回データをレプリケートすることを意味します。

5.  **Destination Namespace を**<strong>Custom format</strong>に設定し、 <strong>Namespace Custom Format を</strong><strong>test</strong>に設定して、すべてのデータを`test`データベースに保存します。

6.  **同期モード**を<strong>フル リフレッシュ |</strong>に選択します。<strong>上書きします</strong>。

    > **ヒント：**
    >
    > TiDB コネクタは、増分同期と完全更新同期の両方をサポートしています。
    >
    > -   増分モードでは、Airbyte は最後の同期ジョブ以降にソースに追加されたレコードのみを読み取ります。増分モードを使用した最初の同期は、完全更新モードと同等です。
    > -   フル リフレッシュ モードでは、Airbyte はすべての同期タスクでソースのすべてのレコードを読み取り、宛先にレプリケートします。 Airbyte の**Namespace**という名前のテーブルごとに同期モードを個別に設定できます。

    ![Set up connection](/media/tidb-cloud/integration-airbyte-connection.jpg)

7.  **[正規化と変換] を**<strong>[正規化された表形式データ]</strong>に設定して、既定の正規化モードを使用するか、ジョブの dbt ファイルを設定できます。正規化の詳細については、 [変換と正規化](https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt)を参照してください。

8.  **[接続のセットアップ]**をクリックします。

9.  接続が確立されたら、 **[ENABLED]**をクリックして同期タスクを有効にします。 <strong>[今すぐ同期] を</strong>クリックして、すぐに同期することもできます。

![Sync data](/media/tidb-cloud/integration-airbyte-sync.jpg)

## 制限事項 {#limitations}

-   TiDB コネクタは、変更データ キャプチャ (CDC) 機能をサポートしていません。
-   TiDB 宛先は、デフォルトの正規化モードで`timestamp`タイプを`varchar`タイプに変換します。これは、Airbyte が送信中にタイムスタンプ タイプを文字列に変換し、TiDB が`cast ('2020-07-28 14:50:15+1:00' as timestamp)`をサポートしていないために発生します。
-   一部の大規模な ELT ミッションでは、TiDB でパラメーターを[取引制限](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions)に増やす必要があります。

## こちらもご覧ください {#see-also}

[Airbyte を使用してTiDB Cloudから Snowflake にデータを移行する](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/) .
