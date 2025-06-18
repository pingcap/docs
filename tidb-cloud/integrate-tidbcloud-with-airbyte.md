---
title: Integrate TiDB Cloud with Airbyte
summary: Airbyte TiDB コネクタの使用方法を学びます。
---

# TiDB CloudとAirbyteを統合する {#integrate-tidb-cloud-with-airbyte}

Airbyte [エアバイト](https://airbyte.com/) 、抽出、ロード、変換（ELT）パイプラインを構築し、データウェアハウス、データレイク、データベース内のデータを統合するためのオープンソースのデータ統合エンジンです。このドキュメントでは、AirbyteをTiDB Cloudにソースまたはデスティネーションとして接続する方法について説明します。

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

Airbyteのバナーが表示されたら、ユーザー名( `airbyte` )とパスワード( `password` )を使用して[http://localhost:8000](http://localhost:8000)に進み、UIにアクセスできます。

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

    パラメータ値は、クラスターの接続ダイアログから取得できます。ダイアログを開くには、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットクラスターの名前をクリックして概要ページに移動し、右上隅の**「接続」**をクリックします。

3.  **SSL 接続**を有効にし、 **JDBC URL パラメータ**で TLS プロトコルを**TLSv1.2**または**TLSv1.3**に設定します。

    > 注記：
    >
    > -   TiDB CloudはTLS接続をサポートしています。TLSv1.2**と****TLSv1.3**の中から、例えば`enabledTLSProtocols=TLSv1.2` TLSプロトコルを選択できます。
    > -   JDBC 経由でTiDB Cloudへの TLS 接続を無効にする場合は、JDBC URL パラメータで useSSL を`false`に設定し、SSL 接続を閉じる必要があります (例: `useSSL=false` )。
    > -   TiDB Cloud Serverless は TLS 接続のみをサポートします。

4.  「ソースまたは**宛先の****設定」**をクリックしてコネクタの作成を完了します。次のスクリーンショットは、ソースとしてTiDBを設定した場合の設定を示しています。

![TiDB source configuration](/media/tidb-cloud/integration-airbyte-parameters.jpg)

TiDB から Snowflake、CSV ファイルから TiDB など、ソースと宛先の任意の組み合わせを使用できます。

TiDB コネクタの詳細については、 [TiDBソース](https://docs.airbyte.com/integrations/sources/tidb)および[TiDB 宛先](https://docs.airbyte.com/integrations/destinations/tidb)参照してください。

## 接続を設定する {#set-up-the-connection}

ソースと宛先を設定したら、接続を構築して構成できます。

以下の手順では、ソースと宛先の両方にTiDBを使用します。他のコネクタではパラメータが異なる場合があります。

1.  サイドバーの**「接続」**をクリックし、 **「新しい接続」**をクリックします。

2.  以前に設定したソースと宛先を選択します。

3.  [接続**の設定]**パネルに移動して、接続の名前 (例: `${source_name} - ${destination-name}` ) を作成します。

4.  **レプリケーション頻度を****24 時間ごと**に設定します。これは、接続が 1 日に 1 回データを複製することを意味します。

5.  **宛先名前空間を****カスタム形式**に設定し、**名前空間カスタム形式**を**テスト**に設定して、すべてのデータを`test`データベースに保存します。

6.  **同期モード**を**「完全更新 | 上書き」**に選択します。

    > **ヒント：**
    >
    > TiDB コネクタは[増分同期と完全更新同期](https://airbyte.com/blog/understanding-data-replication-modes)両方をサポートします。
    >
    > -   増分モードでは、Airbyteは前回の同期ジョブ以降にソースに追加されたレコードのみを読み取ります。増分モードでの最初の同期は、完全更新モードと同等です。
    > -   フルリフレッシュモードでは、Airbyteは同期タスクごとにソース内のすべてのレコードを読み取り、同期先に複製します。同期モードは、Airbyte内の**Namespace**という名前のテーブルごとに個別に設定できます。

    ![Set up connection](/media/tidb-cloud/integration-airbyte-connection.jpg)

7.  デフォルトの正規化モードを使用するには、 **「正規化と変換」**を**「正規化された表形式データ」**に設定するか、ジョブのdbtファイルを設定すると便利です。正規化の詳細については、 [変換と正規化](https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt)を参照してください。

8.  **[接続の設定]を**クリックします。

9.  接続が確立されたら、 **「有効」**をクリックして同期タスクを有効にします。 **「今すぐ同期」**をクリックしてすぐに同期することもできます。

![Sync data](/media/tidb-cloud/integration-airbyte-sync.jpg)

## 制限事項 {#limitations}

-   TiDBコネクタは、TiCDCが提供する変更データキャプチャ（CDC）機能を使用できません。増分同期はカーソルメカニズムに基づいて実行されます。
-   TiDBの宛先は、デフォルトの正規化モードでは`timestamp`型を`varchar`型に変換します。これは、Airbyteが送信時にタイムスタンプ型を文字列に変換するのに対し、TiDBが`cast ('2020-07-28 14:50:15+1:00' as timestamp)`をサポートしていないために発生します。
-   一部の大規模な ELT ミッションでは、TiDB のパラメータを[取引制限](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions)増やす必要があります。

## 参照 {#see-also}

[Airbyte を使用してTiDB Cloudから Snowflake にデータを移行する](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/) 。
