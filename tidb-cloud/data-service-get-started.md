---
title: Get Started with Data Service
summary: Learn how to use TiDB Cloud Data Service to access your data with HTTPS requests.
---

# データサービスを始めてみる {#get-started-with-data-service}

データ サービス (ベータ) を使用すると、カスタム API エンドポイントを使用して HTTPS リクエスト経由でTiDB Cloudデータにアクセスでき、HTTPS と互換性のあるアプリケーションやサービスとシームレスに統合できます。

> **ヒント：**
>
> TiDB Cloud は、 TiDB Serverless クラスタ用の Chat2Query API を提供します。有効にすると、 TiDB Cloud は**Chat2Query**と呼ばれるシステム データ アプリと Data Service に Chat2Data エンドポイントを自動的に作成します。このエンドポイントを呼び出して、AI に指示を提供して SQL ステートメントを生成および実行させることができます。
>
> 詳細については、 [<a href="/tidb-cloud/use-chat2query-api.md">Chat2Query API を使ってみる</a>](/tidb-cloud/use-chat2query-api.md)を参照してください。

このドキュメントでは、データ アプリの作成、開発、テスト、デプロイ、エンドポイントの呼び出しによって、 TiDB Cloud Data Service (ベータ) をすぐに開始する方法を紹介します。

## あなたが始める前に {#before-you-begin}

データ アプリを作成する前に、 [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverless</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターを作成していることを確認してください。お持ちでない場合は、 [<a href="/tidb-cloud/create-tidb-cluster.md">クラスターを作成する</a>](/tidb-cloud/create-tidb-cluster.md)の手順に従って作成してください。

## ステップ 1. データ アプリを作成する {#step-1-create-a-data-app}

データ アプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのグループです。データ アプリを作成するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com">TiDB Cloudコンソール</a>](https://tidbcloud.com)にログインします。

2.  左側のナビゲーション ウィンドウで、<mdsvgicon name="icon-left-data-service">**データサービス**。</mdsvgicon>

3.  **[最初のデータ アプリケーションの作成を開始します]**ページで、名前を入力し、データ アプリがアクセスするクラスターを選択します。

4.  (オプション) データ アプリのエンドポイントを優先する GitHub リポジトリとブランチに自動的にデプロイするには、 **[GitHub に接続]**を有効にして、次の手順を実行します。

    1.  **[GitHub にインストール] を**クリックし、画面上の指示に従って**TiDB Cloud Data Service**をアプリケーションとしてターゲット リポジトリにインストールします。

    2.  **「承認」**をクリックして、GitHub 上のアプリケーションへのアクセスを承認します。

    3.  データ アプリの構成ファイルを保存するターゲット リポジトリ、ブランチ、ディレクトリを指定します。

    > **ノート：**
    >
    > -   ディレクトリはスラッシュ ( `/` ) で始まる必要があります。たとえば、 `/mydata` 。指定したディレクトリがターゲット リポジトリおよびブランチに存在しない場合は、自動的に作成されます。
    > -   リポジトリ、ブランチ、ディレクトリの組み合わせによって構成ファイルのパスが識別されます。このパスはデータ アプリ間で一意である必要があります。指定したパスがすでに別のデータ アプリで使用されている場合は、代わりに新しいパスを指定する必要があります。そうしないと、現在のデータ アプリのTiDB Cloudコンソールで構成されたエンドポイントによって、指定したパス内のファイルが上書きされます。

5.  **[データ アプリの作成]**をクリックします。 [<a href="https://tidbcloud.com/console/data-service">**データサービス**</a>](https://tidbcloud.com/console/data-service)詳細ページが表示されます。

6.  データ アプリを GitHub に接続するように構成している場合は、指定した GitHub ディレクトリを確認してください。 [<a href="/tidb-cloud/data-service-app-config-files.md">データアプリ構成ファイル</a>](/tidb-cloud/data-service-app-config-files.md) `tidb-cloud-data-service`までにディレクトリにコミットされていることがわかります。これは、データ アプリが GitHub に正常に接続されていることを意味します。

    新しいデータ アプリでは、**自動同期とデプロイメント**および**ドラフトのレビュー**がデフォルトで有効になっているため、 TiDB Cloudコンソールと GitHub の間でデータ アプリの変更を簡単に同期し、デプロイメント前に変更をレビューできます。 GitHub 統合の詳細については、 [<a href="/tidb-cloud/data-service-manage-github-connection.md">データ アプリの変更を GitHub で自動的にデプロイ</a>](/tidb-cloud/data-service-manage-github-connection.md)を参照してください。

## ステップ 2. エンドポイントを開発する {#step-2-develop-an-endpoint}

エンドポイントは、SQL ステートメントを実行するためにカスタマイズできる Web API です。

データ アプリを作成すると、デフォルトの`untitled endpoint`自動的に作成されます。デフォルトのエンドポイントを使用してTiDB Cloudクラスターにアクセスできます。

新しいエンドポイントを作成する場合は、新しく作成したデータ アプリを見つけて、アプリ名の右側にある**[+****エンドポイントの作成]**をクリックします。

### プロパティの構成 {#configure-properties}

右側のペインで、 **「プロパティ」**タブをクリックし、次のようなエンドポイントのプロパティを設定します。

-   **エンドポイント パス**: ユーザーがアクセスするために使用するエンドポイントの一意のパス。

    -   パスはデータ アプリ内で一意である必要があります。
    -   パスには文字、数字、アンダースコア ( `_` )、およびスラッシュ ( `/` ) のみを使用できます。パスはスラッシュ ( `/` ) で始まり、文字、数字、またはアンダースコア ( `_` ) で終わる必要があります。たとえば、 `/my_endpoint/get_id` 。
    -   パスの長さは 64 文字未満である必要があります。

-   **エンドポイント URL** : (読み取り専用) URL は、対応するクラスターが配置されているリージョン、データ アプリのサービス URL、およびエンドポイントのパスに基づいて自動的に生成されます。たとえば、エンドポイントのパスが`/my_endpoint/get_id`の場合、エンドポイント URL は`https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`です。

-   **リクエストメソッド**: エンドポイントの HTTP メソッド。次のメソッドがサポートされています。

    -   `GET` : このメソッドを使用して、 `SELECT`ステートメントなどのデータをクエリします。
    -   `POST` : このメソッドは、 `INSERT`ステートメントなどのデータを挿入するために使用します。

-   **Timeout(ms)** : エンドポイントのタイムアウト。範囲は`1` ～ `30000`です。デフォルト値は`5000`ミリ秒です。詳細については、 [<a href="/tidb-cloud/data-service-manage-endpoint.md#configure-properties">プロパティの構成</a>](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)を参照してください。

-   **Max Rows** : エンドポイントが返す最大行数。範囲は`1` ～ `2000`です。デフォルト値は`50`行です。詳細については、 [<a href="/tidb-cloud/data-service-manage-endpoint.md#configure-properties">プロパティの構成</a>](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)を参照してください。

### SQL ステートメントを作成する {#write-sql-statements}

SQL エディター (**データ サービス**ページの中央のペイン) でエンドポイントの SQL ステートメントをカスタマイズできます。

1.  クラスターを選択します。

    > **ノート：**
    >
    > データ アプリにリンクされているクラスターのみがドロップダウン リストに表示されます。リンクされたクラスターを管理するには、 [<a href="/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources">リンクされたクラスターを管理する</a>](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)を参照してください。

    SQL エディターの上部で、SQL ステートメントを実行するクラスターをドロップダウン リストから選択します。その後、右側のペインの**[スキーマ]**タブで、このクラスターのすべてのデータベースを表示できます。

2.  SQL ステートメントを作成します。

    データをクエリまたは変更する前に、まず SQL ステートメントでデータベースを指定する必要があります。たとえば、 `USE database_name;` 。

    SQL エディターでは、テーブル結合クエリ、複雑なクエリ、集計関数のステートメントを作成できます。 `--`に続けて指示を入力するだけで、AI に SQL ステートメントを自動的に生成させることもできます。

    パラメーターを定義するには、SQL ステートメントに`${ID}`のような変数プレースホルダーとして挿入します。たとえば、 `SELECT * FROM table_name WHERE id = ${ID}` 。次に、右側のペインの**「Params」**タブをクリックして、パラメータ定義とテスト値を変更できます。

    > **ノート：**
    >
    > -   パラメータ名では大文字と小文字が区別されます。
    > -   このパラメーターをテーブル名または列名として使用することはできません。

    -   **「定義」**セクションでは、クライアントがエンドポイントを呼び出すときにパラメーターが必要かどうか、データ型 ( `STRING` 、 `NUMBER` 、または`BOOLEAN` )、およびパラメーターのデフォルト値を指定できます。 `STRING`型パラメータを使用する場合は、引用符 ( `'`または`"` ) を追加する必要はありません。たとえば、 `foo` `STRING`タイプに対して有効であり、 `"foo"`として処理されますが、 `"foo"`は`"\"foo\""`として処理されます。
    -   **「テスト値」**セクションでは、パラメーターのテスト値を設定できます。テスト値は、SQL ステートメントを実行するとき、またはエンドポイントをテストするときに使用されます。テスト値を設定しない場合は、デフォルト値が使用されます。
    -   詳細については、 [<a href="/tidb-cloud/data-service-manage-endpoint.md#configure-parameters">パラメータを設定する</a>](/tidb-cloud/data-service-manage-endpoint.md#configure-parameters)を参照してください。

3.  SQL ステートメントを実行します。

    SQL ステートメントにパラメータを挿入した場合は、右側のペインの**[パラメータ]**タブでパラメータのテスト値またはデフォルト値を設定していることを確認してください。それ以外の場合は、エラーが返されます。

    SQL ステートメントを実行するには、カーソルで SQL の行を選択し、 **「実行」** &gt; **「カーソル位置で実行」**をクリックします。

    SQL エディターですべての SQL ステートメントを実行するには、 **「実行」**をクリックします。この場合、最後の SQL 結果のみが返されます。

    ステートメントを実行すると、ページ下部の**[結果]**タブにクエリ結果がすぐに表示されます。

## ステップ 3. エンドポイントをテストする (オプション) {#step-3-test-the-endpoint-optional}

エンドポイントを構成した後、展開する前にエンドポイントをテストして、期待どおりに動作するかどうかを確認できます。

エンドポイントをテストするには、右上隅の**「テスト」**をクリックするか、 **F5**を押します。

その後、ページの下部にある**[HTTP 応答]**タブで応答を確認できます。応答の詳細については、 [<a href="/tidb-cloud/data-service-manage-endpoint.md#response">エンドポイントの応答</a>](/tidb-cloud/data-service-manage-endpoint.md#response)を参照してください。

## ステップ 4. エンドポイントをデプロイ {#step-4-deploy-the-endpoint}

エンドポイントをデプロイするには、次の手順を実行します。

1.  エンドポイントの詳細ページで、右上隅にある**「デプロイ」**をクリックします。

2.  **「デプロイ」**をクリックしてデプロイメントを確認します。**エンドポイントが正常にデプロイされる**と、「エンドポイントがデプロイされました」というプロンプトが表示されます。

    エンドポイントの詳細ページの右側のペインで、 **「デプロイメント」**タブをクリックすると、デプロイされた履歴を表示できます。

## ステップ 5. エンドポイントを呼び出す {#step-5-call-the-endpoint}

HTTPS リクエストを送信することでエンドポイントを呼び出すことができます。エンドポイントを呼び出す前に、まずデータ アプリの API キーを取得する必要があります。

### 1. APIキーを作成する {#1-create-an-api-key}

1.  [<a href="https://tidbcloud.com/console/data-service">**データサービス**</a>](https://tidbcloud.com/console/data-service)ページの左側のペインで、データ アプリの名前をクリックして詳細を表示します。

2.  **「API キー」**領域で、 **「API キーの作成」を**クリックします。

3.  **[API キーの作成]**ダイアログ ボックスで、説明を入力し、API キーのロールを選択します。

    このロールは、API キーがデータ アプリにリンクされたクラスターに対してデータの読み取りまたは書き込みを行えるかどうかを制御するために使用されます。 `ReadOnly`または`ReadAndWrite`役割を選択できます。

    -   `ReadOnly` : API キーは`SELECT` 、 `SHOW` 、 `USE` 、 `DESC` 、 `EXPLAIN`ステートメントなどのデータの読み取りのみを許可します。
    -   `ReadAndWrite` : API キーによるデータの読み取りと書き込みを許可します。この API キーを使用して、DML ステートメントや DDL ステートメントなどのすべての SQL ステートメントを実行できます。

4.  **「次へ」**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密キーをコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密キーを再度取得することはできなくなります。

5.  **「完了」**をクリックします。

### 2. コード例を取得する {#2-get-the-code-example}

TiDB Cloudは、エンドポイントの呼び出しに役立つコード サンプルを生成します。コード例を取得するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/console/data-service">**データサービス**</a>](https://tidbcloud.com/console/data-service)ページの左側のペインで、エンドポイントの名前をクリックし、右上隅にある**[...]** &gt; **[コード例]**をクリックします。 **[コード例]**ダイアログ ボックスが表示されます。

2.  ダイアログ ボックスで、エンドポイントの呼び出しに使用するクラスターとデータベースを選択し、コード例をコピーします。

    Curl コード例の例は次のとおりです。

    <SimpleTab>
     <div label="Test Environment">

    エンドポイントのドラフト バージョンを呼び出すには、 `endpoint-type: draft`ヘッダーを追加する必要があります。

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
      --header 'endpoint-type: draft'
    ```

    </div>

    <div label="Online Environment">

    オンライン環境でコード例を確認する前に、まずエンドポイントをデプロイする必要があります。

    現在のオンライン バージョンのエンドポイントを呼び出すには、次のコマンドを使用します。

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>'
    ```

    </div>
     </SimpleTab>

    > **ノート：**
    >
    > -   リージョン ドメイン`<region>.data.tidbcloud.com`をリクエストすると、TiDB クラスターが配置されているリージョンのエンドポイントに直接アクセスできます。
    > -   あるいは、リージョンを指定せずにグローバル ドメイン`data.tidbcloud.com`をリクエストすることもできます。この方法で、 TiDB Cloudはリクエストを内部的にターゲット リージョンにリダイレクトしますが、これにより追加のレイテンシーが発生する可能性があります。この方法を選択した場合は、エンドポイントを呼び出すときに必ず`--location-trusted`オプションをcurl コマンドに追加してください。

### 3. コード例を使用する {#3-use-the-code-example}

コード例をアプリケーションに貼り付けて実行します。その後、エンドポイントの応答を取得できます。

-   `<Public Key>`と`<Private Key>`プレースホルダーを API キーに置き換える必要があります。
-   エンドポイントにパラメーターが含まれている場合は、エンドポイントを呼び出すときにパラメーター値を指定します。

エンドポイントを呼び出した後、JSON 形式で応答を確認できます。以下は例です。

```json
{
  "type": "sql_endpoint",
  "data": {
    "columns": [
      {
        "col": "id",
        "data_type": "BIGINT",
        "nullable": false
      },
      {
        "col": "type",
        "data_type": "VARCHAR",
        "nullable": false
      }
    ],
    "rows": [
      {
        "id": "20008295419",
        "type": "CreateEvent"
      }
    ],
    "result": {
      "code": 200,
      "message": "Query OK!",
      "start_ms": 1678965476709,
      "end_ms": 1678965476839,
      "latency": "130ms",
      "row_count": 1,
      "row_affect": 0,
      "limit": 50
    }
  }
}
```

応答の詳細については、 [<a href="/tidb-cloud/data-service-manage-endpoint.md#response">エンドポイントの応答</a>](/tidb-cloud/data-service-manage-endpoint.md#response)を参照してください。

## もっと詳しく知る {#learn-more}

-   [<a href="/tidb-cloud/data-service-overview.md">データサービスの概要</a>](/tidb-cloud/data-service-overview.md)
-   [<a href="/tidb-cloud/use-chat2query-api.md">Chat2Query API を使ってみる</a>](/tidb-cloud/use-chat2query-api.md)
-   [<a href="/tidb-cloud/data-service-manage-data-app.md">データアプリを管理する</a>](/tidb-cloud/data-service-manage-data-app.md)
-   [<a href="/tidb-cloud/data-service-manage-endpoint.md">エンドポイントの管理</a>](/tidb-cloud/data-service-manage-endpoint.md)
