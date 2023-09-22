---
title: Integrate TiDB Cloud with Airbyte
summary: Learn how to use Airbyte TiDB connector.
---

# TiDB Cloudと Airbyte を統合する {#integrate-tidb-cloud-with-airbyte}

[エアバイト](https://airbyte.com/)は、抽出、読み込み、変換 (ELT) パイプラインを構築し、データ ウェアハウス、データ レイク、データベース内のデータを統合するためのオープンソース データ統合エンジンです。このドキュメントでは、Airbyte をソースまたは宛先としてTiDB Cloudに接続する方法について説明します。

## Airbyteをデプロイ {#deploy-airbyte}

わずか数ステップで Airbyte をローカルに導入できます。

1.  [ドッカー](https://www.docker.com/products/docker-desktop)ワークスペースにインストールします。

2.  Airbyte のソース コードをクローンします。

    ```shell
    git clone https://github.com/airbytehq/airbyte.git && \
    cd airbyte
    ```

3.  docker-compose で Docker イメージを実行します。

    ```shell
    docker-compose up
    ```

Airbyte バナーが表示されたら、ユーザー名 ( `airbyte` ) とパスワード ( `password` ) を使用して[http://ローカルホスト:8000](http://localhost:8000)に進み、UI にアクセスします。

    airbyte-server      |     ___    _      __          __
    airbyte-server      |    /   |  (_)____/ /_  __  __/ /____
    airbyte-server      |   / /| | / / ___/ __ \/ / / / __/ _ \
    airbyte-server      |  / ___ |/ / /  / /_/ / /_/ / /_/  __/
    airbyte-server      | /_/  |_/_/_/  /_.___/\__, /\__/\___/
    airbyte-server      |                     /____/
    airbyte-server      | --------------------------------------
    airbyte-server      |  Now ready at http://localhost:8000/
    airbyte-server      | --------------------------------------

## TiDB コネクタをセットアップする {#set-up-the-tidb-connector}

便利なことに、TiDB をソースと宛先として設定する手順は同じです。

1.  サイドバーの**「ソース」**または**「宛先」**をクリックし、TiDB タイプを選択して新しい TiDB コネクタを作成します。

2.  次のパラメータを入力します。

    -   ホスト: TiDB Cloudクラスターのエンドポイント
    -   ポート: データベースのポート
    -   データベース: データを同期するデータベース
    -   ユーザー名: データベースにアクセスするためのユーザー名
    -   パスワード: ユーザー名のパスワード

    クラスターの接続ダイアログからパラメーター値を取得できます。ダイアログを開くには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。

3.  **SSL 接続**を有効にし、 **JDBC URL Params**で TLS プロトコルを**TLSv1.2**または**TLSv1.3**に設定します。

    > 注記：
    >
    > -   TiDB Cloud はTLS 接続をサポートしています。 **TLSv1.2**および**TLSv1.3**で TLS プロトコルを選択できます (例: `enabledTLSProtocols=TLSv1.2` )。
    > -   JDBC 経由でTiDB Cloudへの TLS 接続を無効にしたい場合は、特に JDBC URL Params で useSSL を`false`に設定し、SSL 接続 (例: `useSSL=false`を閉じる必要があります。
    > -   TiDB サーバーレスは TLS 接続のみをサポートします。

4.  [ソースまたは**宛先の****セットアップ]**をクリックしてコネクタの作成を完了します。次のスクリーンショットは、ソースとしての TiDB の構成を示しています。

![TiDB source configuration](/media/tidb-cloud/integration-airbyte-parameters.jpg)

TiDB から Snowflake、CSV ファイルから TiDB など、ソースと宛先を任意に組み合わせて使用​​できます。

TiDB コネクタの詳細については、 [TiDB ソース](https://docs.airbyte.com/integrations/sources/tidb)および[TiDB の宛先](https://docs.airbyte.com/integrations/destinations/tidb)を参照してください。

## 接続をセットアップする {#set-up-the-connection}

送信元と宛先を設定したら、接続を構築して構成できます。

次の手順では、ソースと宛先の両方として TiDB を使用します。他のコネクタには異なるパラメータがある場合があります。

1.  サイドバーの**「接続」**をクリックし、 **「新しい接続」**をクリックします。

2.  以前に確立した送信元と宛先を選択します。

3.  [接続**のセットアップ]**パネルに移動し、接続の名前`${source_name} - ${destination-name}`など) を作成します。

4.  **[レプリケーション頻度]**を**[24 時間ごと]**に設定します。これは、接続が 1 日に 1 回データをレプリケートすることを意味します。

5.  **[宛先ネームスペース]**を**[カスタム形式]**に設定し、 **[ネームスペース カスタム形式]**を**テスト**して`test`データベースにすべてのデータを保存します。

6.  **同期モードを****[完全更新]**に選択します。**上書きします**。

    > **ヒント：**
    >
    > TiDB コネクタは、増分同期と完全リフレッシュ同期の両方をサポートします。
    >
    > -   増分モードでは、Airbyte は最後の同期ジョブ以降にソースに追加されたレコードのみを読み取ります。インクリメンタル モードを使用した最初の同期は、フル リフレッシュ モードと同等です。
    > -   フルリフレッシュモードでは、Airbyteは同期タスクごとにソース内のすべてのレコードを読み取り、宛先にレプリケートします。 Airbyte の**Namespace**という名前のテーブルごとに同期モードを個別に設定できます。

    ![Set up connection](/media/tidb-cloud/integration-airbyte-connection.jpg)

7.  **「正規化と変換」を****「正規化された表形式データ」**に設定してデフォルトの正規化モードを使用するか、ジョブの dbt ファイルを設定できます。正規化の詳細については、 [変換と正規化](https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt)を参照してください。

8.  **[接続のセットアップ]**をクリックします。

9.  接続が確立されたら、 **「有効」**をクリックして同期タスクをアクティブにします。 **「今すぐ同期」を**クリックしてすぐに同期することもできます。

![Sync data](/media/tidb-cloud/integration-airbyte-sync.jpg)

## 制限事項 {#limitations}

-   TiDB コネクタは、Change Data Capture (CDC) 機能をサポートしていません。
-   TiDB 宛先は、デフォルトの正規化モードで`timestamp`タイプを`varchar`タイプに変換します。これは、Airbyte が送信中にタイムスタンプ タイプを文字列に変換し、TiDB が`cast ('2020-07-28 14:50:15+1:00' as timestamp)`をサポートしていないために発生します。
-   一部の大規模な ELT ミッションでは、TiDB のパラメータを[取引制限](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions)に増やす必要があります。

## こちらも参照 {#see-also}

[Airbyte を使用してTiDB Cloudから Snowflake にデータを移行する](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/) 。
