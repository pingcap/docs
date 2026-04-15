---
title: Integrate TiDB Cloud with Airbyte
summary: Airbyte TiDBコネクタの使い方を学びましょう。
---

# TiDB CloudとAirbyteを統合する {#integrate-tidb-cloud-with-airbyte}

[エアバイト](https://airbyte.com/)データウェアハウス、データレイク、データベース内のデータを統合し、抽出、ロード、変換（ELT）パイプラインを構築するためのオープンソースのデータ統合エンジンです。このドキュメントでは、エアバイトをソースまたは宛先としてTiDB Cloudに接続する方法について説明します。

## Airbyteをデプロイ {#deploy-airbyte}

Airbyteは、わずか数ステップでローカル環境にデプロイできます。

1.  ワークスペースに[ドッカー](https://www.docker.com/products/docker-desktop)をインストールします。

2.  Airbyteのソースコードをクローンする。

    ```shell
    git clone https://github.com/airbytehq/airbyte.git && \
    cd airbyte
    ```

3.  docker-composeを使用してDockerイメージを実行します。

    ```shell
    docker-compose up
    ```

Airbyteのバナーが表示されたら、ユーザー名（ `airbyte` ）とパスワード（`password`）を使用して[http://localhost:8000](http://localhost:8000) `password`アクセスし、UIにアクセスできます。

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

便利なことに、TiDBをソースと宛先に設定する手順は同じです。

1.  サイドバーの**「ソース」**または**「宛先」**をクリックし、TiDBタイプを選択して新しいTiDBコネクタを作成します。

2.  以下のパラメータを入力してください。

    -   ホスト: <CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent>のエンドポイント<CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>
    -   ポート: データベースのポート番号
    -   データベース：データを同期したいデータベース
    -   ユーザー名：データベースにアクセスするためのユーザー名
    -   パスワード：ユーザー名のパスワード

    TiDB Cloudコンソールの接続ダイアログからパラメーター値を取得できます。ダイアログを開くには、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットの<CustomContent plan="starter">TiDB Cloud Starterインスタンス</CustomContent><CustomContent plan="essential">TiDB Cloud Essentialインスタンス</CustomContent><CustomContent plan="premium">TiDB Cloud Premiumインスタンス</CustomContent><CustomContent plan="dedicated">TiDB Cloud Dedicatedクラスター</CustomContent>クラスターの名前をクリックして概要ページに移動し、右上隅の**Connect**をクリックします。

3.  **SSL接続**を有効にし、 **JDBC URLパラメータ**でTLSプロトコルを**TLSv1.2**または**TLSv1.3**に設定します。

    > **注記：**
    >
    > -   TiDB Cloud はTLS 接続をサポートしています。TLSv1.2 および**TLSv1.3**から TLS プロトコルを選択できます。たとえば、 `enabledTLSProtocols=TLSv1.2` **。**
    > -   JDBC を介してTiDB Cloudへの TLS 接続を無効にする場合は、JDBC URL パラメータで useSSL を`false`に設定し、SSL 接続を閉じる必要があります。たとえば、 `useSSL=false`のように設定します。
    > -   TiDB Cloud StarterとTiDB Cloud EssentialはTLS接続のみをサポートしています。

4.  コネクタの作成を完了するには、「ソースまたは**宛先の****設定」**をクリックします。次のスクリーンショットは、ソースとしてTiDBを設定した例です。

![TiDB source configuration](/media/tidb-cloud/integration-airbyte-parameters.jpg)

TiDBからSnowflakeへの転送や、CSVファイルからTiDBへの転送など、ソースと宛先を自由に組み合わせて使用​​できます。

TiDB コネクタの詳細については、 [TiDBソース](https://docs.airbyte.com/integrations/sources/tidb)と[TiDB宛先](https://docs.airbyte.com/integrations/destinations/tidb)参照してください。

## 接続を設定する {#set-up-the-connection}

送信元と送信先を設定したら、接続を構築して構成できます。

以下の手順では、TiDBをソースと宛先の両方として使用します。他のコネクタでは、パラメータが異なる場合があります。

1.  サイドバーの**「接続」**をクリックし、次に**「新しい接続」**をクリックします。

2.  事前に設定した送信元と送信先を選択してください。

3.  接続**設定**パネルに移動し、 `${source_name} - ${destination-name}`などの接続名を作成します。

4.  **レプリケーション頻度を****「24時間ごと**」に設定すると、接続は1日に1回データを複製します。

5.  **宛先名前空間を****カスタム形式**に設定し、**名前空間カスタム形式**を**テスト**に設定して、すべてのデータを`test`データベースに保存します。

6.  **同期モード**を**「完全更新」または「上書き」**に選択してください。

    > **ヒント：**
    >
    > TiDB コネクタは[増分更新と完全更新の同期](https://airbyte.com/blog/understanding-data-replication-modes)をサポートします。
    >
    > -   インクリメンタルモードでは、Airbyteは前回の同期ジョブ以降にソースに追加されたレコードのみを読み取ります。インクリメンタルモードを使用した最初の同期は、フルリフレッシュモードと同等です。
    > -   フルリフレッシュモードでは、Airbyteはソース内のすべてのレコードを読み取り、同期タスクごとに宛先に複製します。Airbyteの**「名前空間」**という名前のテーブルごとに、同期モードを個別に設定できます。

    ![Set up connection](/media/tidb-cloud/integration-airbyte-connection.jpg)

7.  デフォルトの正規化モードを使用するには、 **「正規化と変換」**を「正規化**された表形式データ」**に設定してください。または、ジョブに使用するdbtファイルを設定することもできます。正規化の詳細については、 [変換と正規化](https://docs.airbyte.com/operator-guides/transformation-and-normalization/transformations-with-dbt)を参照してください。

8.  **「接続設定」**をクリックしてください。

9.  接続が確立されたら、 **「有効」**をクリックして同期タスクをアクティブ化します。また、 **「今すぐ同期」**をクリックすると、すぐに同期を開始できます。

![Sync data](/media/tidb-cloud/integration-airbyte-sync.jpg)

## 制限事項 {#limitations}

-   TiDBコネクタは、TiCDCが提供する変更データキャプチャ（CDC）機能を使用できません。増分同期はカーソル機構に基づいて実行されます。
-   TiDB の宛先では、デフォルトの正規化モードで`timestamp`型が`varchar`型に変換されます。これは、Airbyte が送信中にタイムスタンプ型を文字列に変換し、TiDB が`cast ('2020-07-28 14:50:15+1:00' as timestamp)`をサポートしていないためです。
-   一部の大規模な ELT ミッションでは、TiDB の[取引制限](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions)のパラメーターを増やす必要があります。

## 関連項目 {#see-also}

[Airbyteを使用してTiDB CloudからSnowflakeへデータを移行する](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/)。
