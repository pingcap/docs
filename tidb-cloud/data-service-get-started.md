---
title: Get Started with Data Service
summary: Learn how to use TiDB Cloud Data Service to access your data with HTTPS requests.
---

# データ サービスを開始する {#get-started-with-data-service}

データ サービス (ベータ版) を使用すると、カスタム API エンドポイントを使用して HTTPS 要求経由でTiDB Cloudデータにアクセスでき、HTTPS と互換性のある任意のアプリケーションまたはサービスとシームレスに統合できます。

> **ヒント：**
>
> TiDB Cloud は、Serverless Tierクラスター用の Chat2Query API を提供します。有効にすると、 TiDB Cloud は、 **Chat2Query**と呼ばれるシステム データ アプリと Data Service の Chat2Data エンドポイントを自動的に作成します。このエンドポイントを呼び出して、命令を提供することで AI に SQL ステートメントを生成および実行させることができます。
>
> 詳細については、 [Chat2Query API の使用を開始する](/tidb-cloud/use-chat2query-api.md)を参照してください。

このドキュメントでは、データ アプリを作成し、エンドポイントを開発、テスト、デプロイ、および呼び出すことにより、 TiDB Cloud Data Service (ベータ) をすばやく開始する方法を紹介します。

## あなたが始める前に {#before-you-begin}

Data App を作成する前に、 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターを作成したことを確認してください。持っていない場合は、 [クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)の手順に従って作成します。

## 手順 1. データ アプリを作成する {#step-1-create-a-data-app}

データ アプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのグループです。データ アプリを作成するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  左側のナビゲーション ペインで、<mdsvgicon name="icon-left-data-service">**データ サービス**。</mdsvgicon>

3.  **Get started by creating your first data application**ページで、名前を入力し、Data App がアクセスするクラスターを選択します。

4.  **[データ アプリの作成]**をクリックします。 [**データサービス**](https://tidbcloud.com/console/data-service)詳細ページが表示されます。

## ステップ 2. エンドポイントを開発する {#step-2-develop-an-endpoint}

エンドポイントは、SQL ステートメントを実行するためにカスタマイズできる Web API です。

Data App を作成すると、デフォルトの`untitled endpoint`自動的に作成されます。デフォルトのエンドポイントを使用して、 TiDB Cloudクラスターにアクセスできます。

新しいエンドポイントを作成する場合は、新しく作成されたデータ アプリを見つけて、左側のペインの上部にある**[+**<strong>エンドポイントの作成]</strong>をクリックします。

### プロパティの構成 {#configure-properties}

右側のペインで**[プロパティ]**タブをクリックし、次のようなエンドポイントのプロパティを設定します。

-   **エンドポイント パス**: ユーザーがアクセスするために使用するエンドポイントの一意のパス。

    -   パスはデータ アプリ内で一意である必要があります。
    -   パスには文字、数字、アンダースコア ( `_` )、およびスラッシュ ( `/` ) のみを使用でき、スラッシュ ( `/` ) で始まる必要があります。たとえば、 `/my_endpoint/get_id`です。
    -   パスの長さは 64 文字未満にする必要があります。

-   **エンドポイント URL** : (読み取り専用) URL は、データ アプリのサービス URL とエンドポイントのパスに基づいて自動的に生成されます。たとえば、エンドポイントのパスが`/my_endpoint/get_id`の場合、エンドポイント URL は`https://data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`です。

-   **Request Method** : エンドポイントの HTTP メソッド。次の方法がサポートされています。

    -   `GET` : このメソッドを使用して、 `SELECT`ステートメントなどのデータをクエリします。
    -   `POST` : このメソッドを使用して、 `INSERT`ステートメントなどのデータを挿入します。

-   **Timeout(ms)** : エンドポイントのタイムアウト。範囲は`1` ～ `30000`です。デフォルト値は`5000`ミリ秒です。詳細については、 [プロパティの構成](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)を参照してください。

-   **Max Rows** : エンドポイントが返す最大行数。範囲は`1` ～ `2000`です。デフォルト値は`50`行です。詳細については、 [プロパティの構成](/tidb-cloud/data-service-manage-endpoint.md#configure-properties)を参照してください。

### SQL ステートメントを作成する {#write-sql-statements}

**Data Service**ページの中央ペインにある SQL エディターで、エンドポイントの SQL ステートメントをカスタマイズできます。

1.  クラスターを選択します。

    > **ノート：**
    >
    > ドロップダウン リストには、データ アプリにリンクされているクラスターのみが表示されます。リンクされたクラスターを管理するには、 [リンクされたクラスターを管理する](/tidb-cloud/data-service-manage-data-app.md#manage-linked-clusters)を参照してください。

    SQL エディターの上部で、SQL ステートメントを実行するクラスターをドロップダウン リストから選択します。次に、右側のペインの**[スキーマ]**タブで、このクラスターのすべてのデータベースを表示できます。

2.  SQL ステートメントを記述します。

    データを照会または変更する前に、まず SQL ステートメントでデータベースを指定する必要があります。たとえば、 `USE database_name;`です。

    SQL エディターでは、テーブル結合クエリ、複雑なクエリ、集計関数のステートメントを記述できます。 `--`入力してから命令を入力するだけで、AI に SQL ステートメントを自動的に生成させることもできます。

    パラメーターを定義するには、SQL ステートメントに`${ID}`のような変数プレースホルダーとして挿入できます。たとえば、 `SELECT * FROM table_name WHERE id = ${ID}`です。次に、右側のペインの**[Params]**タブをクリックして、パラメーターの定義とテスト値を変更できます。

    > **ノート：**
    >
    > -   パラメータ名は大文字と小文字が区別されます。
    > -   このパラメーターは、テーブル名または列名として使用できません。

    -   **[定義]**セクションでは、クライアントがエンドポイントを呼び出すときにパラメーターが必要かどうか、データ型 ( `STRING` 、 `NUMBER` 、または`BOOLEAN` )、およびパラメーターの既定値を指定できます。 `STRING`タイプのパラメーターを使用する場合、引用符 ( `'`または`"` ) を追加する必要はありません。たとえば、 `foo` `STRING`タイプに有効であり、 `"foo"`として処理されますが、 `"foo"`は`"\"foo\""`として処理されます。
    -   **[テスト値]**セクションでは、パラメーターのテスト値を設定できます。テスト値は、SQL ステートメントを実行するとき、またはエンドポイントをテストするときに使用されます。テスト値を設定しない場合、デフォルト値が使用されます。
    -   詳細については、 [パラメータの構成](/tidb-cloud/data-service-manage-endpoint.md#configure-parameters)を参照してください。

3.  SQL ステートメントを実行します。

    SQL ステートメントにパラメーターを挿入した場合は、右側のペインの**[パラメーター]**タブでパラメーターのテスト値またはデフォルト値を設定したことを確認してください。それ以外の場合は、エラーが返されます。

    SQL ステートメントを実行するには、カーソルで SQL の行を選択し、 **[実行]** &gt; <strong>[カーソル位置で実行]</strong>をクリックします。

    SQL エディターですべての SQL ステートメントを実行するには、 **[実行]**をクリックします。この場合、最後の SQL 結果のみが返されます。

    ステートメントを実行すると、ページの下部にある**[結果]**タブにクエリの結果がすぐに表示されます。

## ステップ 3. エンドポイントをテストする (オプション) {#step-3-test-the-endpoint-optional}

エンドポイントを構成した後、展開する前にエンドポイントをテストして、期待どおりに動作するかどうかを確認できます。

エンドポイントをテストするには、右上隅の**[テスト]**をクリックするか、 <strong>F5</strong>を押します。

次に、ページの下部にある**[HTTP 応答]**タブで応答を確認できます。応答の詳細については、 [エンドポイントの応答](/tidb-cloud/data-service-manage-endpoint.md#response)参照してください。

## ステップ 4. エンドポイントをデプロイ {#step-4-deploy-the-endpoint}

エンドポイントをデプロイするには、次の手順を実行します。

1.  エンドポイントの詳細ページで、右上隅にある**[デプロイ]**をクリックします。

2.  **[デプロイ]**をクリックして、展開を確認します。<strong>エンドポイントが正常にデプロイされる</strong>と、「エンドポイントがデプロイされました」というプロンプトが表示されます。

    エンドポイントの詳細ページの右側のペインで、 **[展開]**タブをクリックして、展開された履歴を表示できます。

## ステップ 5. エンドポイントを呼び出す {#step-5-call-the-endpoint}

HTTPS リクエストを送信して、エンドポイントを呼び出すことができます。エンドポイントを呼び出す前に、まずデータ アプリの API キーを取得する必要があります。

### 1.API キーを作成する {#1-create-an-api-key}

1.  [**データサービス**](https://tidbcloud.com/console/data-service)ページの左側のペインで、データ アプリの名前をクリックして詳細を表示します。

2.  **[API キー]**領域で、 <strong>[API キーの作成]</strong>をクリックします。

3.  **[API キーの作成]**ダイアログ ボックスで、説明を入力し、API キーのロールを選択します。

    ロールは、API キーが Data App にリンクされたクラスターにデータを読み書きできるかどうかを制御するために使用されます。 `ReadOnly`または`ReadAndWrite`役割を選択できます。

    -   `ReadOnly` : API キーが`SELECT` 、 `SHOW` 、 `USE` 、 `DESC` 、および`EXPLAIN`ステートメントなどのデータを読み取ることのみを許可します。
    -   `ReadAndWrite` : API キーによるデータの読み取りと書き込みを許可します。この API キーを使用して、DML ステートメントや DDL ステートメントなど、すべての SQL ステートメントを実行できます。

4.  **[次へ]**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密鍵をコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密鍵を再度取得することはできなくなります。

5.  **[完了]**をクリックします。

### 2. コード例を入手する {#2-get-the-code-example}

TiDB Cloud は、エンドポイントを呼び出すのに役立つコード例を生成します。コード例を取得するには、次の手順を実行します。

1.  [**データサービス**](https://tidbcloud.com/console/data-service)ページの左側のペインで、エンドポイントの名前をクリックし、右上隅にある**[...]** &gt; <strong>[コード例]</strong>をクリックします。 <strong>[コード例]</strong>ダイアログ ボックスが表示されます。

2.  ダイアログ ボックスで、エンドポイントの呼び出しに使用するクラスターとデータベースを選択し、コード例をコピーします。

    curl コード例の例は次のとおりです。

    <SimpleTab>
     <div label="Test Environment">

    エンドポイントのドラフト バージョンを呼び出すには、 `endpoint-type: draft`ヘッダーを追加する必要があります。

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
      --header 'endpoint-type: draft'
    ```

    </div>

    <div label="Online Environment">

    オンライン環境でコード例を確認する前に、まずエンドポイントを展開する必要があります。

    エンドポイントの現在のオンライン バージョンを呼び出すには、次のコマンドを使用します。

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>'
    ```

    </div>
     </SimpleTab>

### 3. コード例を使用する {#3-use-the-code-example}

コード例をアプリケーションに貼り付けて実行します。その後、エンドポイントの応答を取得できます。

-   `<Public Key>`と`<Private Key>`プレースホルダーを API キーに置き換える必要があります。
-   エンドポイントにパラメーターが含まれている場合は、エンドポイントを呼び出すときにパラメーター値を指定します。

エンドポイントを呼び出した後、JSON 形式で応答を確認できます。次に例を示します。

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

応答の詳細については、 [エンドポイントの応答](/tidb-cloud/data-service-manage-endpoint.md#response)を参照してください。

## もっと詳しく知る {#learn-more}

-   [データ サービスの概要](/tidb-cloud/data-service-overview.md)
-   [Chat2Query API を使ってみる](/tidb-cloud/use-chat2query-api.md)
-   [データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)
-   [エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)
