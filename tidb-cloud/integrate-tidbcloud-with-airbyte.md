---
title: Integrate TiDB Cloud with Airbyte
summary: Airbyte TiDB コネクタの使用方法を学びます。
---

# TiDB Cloudを Airbyte と統合する {#integrate-tidb-cloud-with-airbyte}

[エアバイト](https://airbyte.com/)は、抽出、ロード、変換 (ELT) パイプラインを構築し、データ ウェアハウス、データ レイク、データベース内のデータを統合するためのオープン ソースのデータ統合エンジンです。このドキュメントでは、Airbyte をソースまたは宛先としてTiDB Cloudに接続する方法について説明します。

## Airbyteをデプロイ {#deploy-airbyte}

わずか数ステップで Airbyte をローカルに展開できます。

1.  ワークスペースに[ドッカー](https://www.docker.com/products/docker-desktop)インストールします。

2.  Airbyte ソース コードを複製します。

    ```shell
    git clone https://github.com/airbytehq/airbyte.git && \
    cd airbyte
    ```

3.  docker-compose で Docker イメージを実行します。

    ```shell
    docker-compose up
    ```

Airbyte バナーが表示されたら、ユーザー名 ( `airbyte` ) とパスワード ( `password` ) を使用して[http://ローカルホスト:8000](http://localhost:8000)に移動し、UI にアクセスできます。

    airbyte-server      |     ___    _      __          __
    airbyte-server      |    /   |  (_)____/ /_  __  __/ /____
    airbyte-server      |   / /| | / / ___/ __ \/ / / / __/ _ \
    airbyte-server      |  / ___ |/ / /  / /_/ / /_/ / /_/  __/
    airbyte-server      | /_/  |_/_/_/  /_.___/\__, /\__/\___/
    airbyte-server      |                     /____/
    airbyte-server      | --------------------------------------
    airbyte-server      |  Now ready at http://localhost:8000/
    airbyte-server      | --------------------------------------

## TiDBコネクタを設定する {#set-up-the-tidb-connector}

便利なことに、TiDB をソースと宛先として設定する手順は同じです。

1.  サイドバーの**「ソース」**または**「宛先」**をクリックし、TiDB タイプを選択して新しい TiDB コネクタを作成します。

2.  次のパラメータを入力してください。

    -   ホスト: TiDB Cloudクラスターのエンドポイント
    -   ポート: データベースのポート
    -   データベース: データを同期するデータベース
    -   ユーザー名: データベースにアクセスするためのユーザー名
    -   パスワード: ユーザー名のパスワード

    パラメータ値は、クラスターの接続ダイアログから取得できます。ダイアログを開くには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。

3.  **SSL 接続を**有効にし、 **JDBC URL パラメータ**で TLS プロトコルを**TLSv1.2**または**TLSv1.3**に設定します。

    > 注記：
    >
    > -   TiDB Cloud はTLS 接続をサポートしています。TLSv1.2 および**TLSv1.3**で TLS プロトコルを選択できます**(**例: `enabledTLSProtocols=TLSv1.2` )。
    > -   JDBC 経由でTiDB Cloudへの TLS 接続を無効にする場合は、JDBC URL Params で useSSL を`false`に設定し、SSL 接続を閉じる必要があります (例: `useSSL=false` )。
    > -   TiDB Serverless は TLS 接続のみをサポートします。

4.  コネクタの作成を完了するには、[ソースまたは**宛先****の設定] を**クリックします。次のスクリーンショットは、ソースとしての TiDB の構成を示しています。

![TiDB source configuration](/media/tidb-cloud/integration-airbyte-parameters.jpg)

TiDB から Snowflake、CSV ファイルから TiDB など、ソースと宛先の任意の組み合わせを使用できます。

TiDB コネクタの詳細については、 [TiDB ソース](https://docs.airbyte.com/integrations/sources/tidb)および[TiDB 宛先](https://docs.airbyte.com/integrations/destinations/tidb)を参照してください。

## 接続を設定する {#set-up-the-connection}

ソースと宛先を設定したら、接続を構築して構成できます。

次の手順では、ソースと宛先の両方として TiDB を使用します。他のコネクタではパラメータが異なる場合があります。

1.  サイドバーの**「接続」**をクリックし、 **「新しい接続」**をクリックします。

2.  以前に確立したソースと宛先を選択します。

3.  [接続**の設定**] パネルに移動し、接続の名前 (例: `${source_name} - ${destination-name}` ) を作成します。

4.  **レプリケーション頻度を****24 時間ごと**に設定します。これは、接続が 1 日に 1 回データを複製することを意味します。

5.  **宛先名前空間を****カスタム形式**に設定し、**名前空間カスタム形式**を**テスト**に設定して、すべてのデータを`test`データベースに保存します。

6.  **同期モードを****「完全更新 | 上書き」**に選択します。

    > **ヒント：**
    >
    > TiDB コネクタは、増分更新同期と完全更新同期の両方をサポートします。
    >
    > -   増分モードでは、Airbyte は最後の同期ジョブ以降にソースに追加されたレコードのみを読み取ります。増分モードを使用した最初の同期は、完全更新モードと同等です。
    > -   フル リフレッシュ モードでは、Airbyte はソース内のすべてのレコードを読み取り、同期タスクごとに宛先に複製します。Airbyte の**Namespace**という名前のテーブルごとに同期モードを個別に設定できます。

    ![Set up connection](/media/tidb-cloud/integration-airbyte-connection.jpg)

7.  デフォルトの正規化モードを使用するには、 **「正規化と変換」**を**「正規化された表形式データ**」に設定するか、ジョブの dbt ファイルを設定することができます。正規化の詳細については、 [変換と正規化](https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt)を参照してください。

8.  **[接続の設定]を**クリックします。

9.  接続が確立されたら、 **[有効]**をクリックして同期タスクをアクティブにします。 **[今すぐ同期] を**クリックしてすぐに同期することもできます。

![Sync data](/media/tidb-cloud/integration-airbyte-sync.jpg)

## 制限事項 {#limitations}

-   TiDB コネクタは、変更データ キャプチャ (CDC) 機能をサポートしていません。
-   TiDB の宛先は、デフォルトの正規化モードで`timestamp`型を`varchar`型に変換します。これは、Airbyte が送信中にタイムスタンプ型を文字列に変換し、TiDB が`cast ('2020-07-28 14:50:15+1:00' as timestamp)`サポートしていないために発生します。
-   一部の大規模な ELT ミッションでは、TiDB のパラメータを[取引制限](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions)増やす必要があります。

## 参照 {#see-also}

[Airbyte を使用してTiDB Cloudから Snowflake にデータを移行する](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/) 。
