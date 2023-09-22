---
title: Get Started with Chat2Query API
summary: Learn how to use TiDB Cloud Chat2Query API to generate and execute SQL statements using AI by providing instructions.
---

# Chat2Query API を使ってみる {#get-started-with-chat2query-api}

TiDB Cloud は、指示を提供することで AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェイスである Chat2Query API を提供します。その後、API はクエリ結果を返します。

Chat2Query API には HTTPS 経由でのみアクセスできるため、ネットワーク上で送信されるすべてのデータは TLS を使用して暗号化されます。

> **注記：**
>
> Chat2Query APIは[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスタで利用可能です。 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターで Chat2Query API を使用するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## あなたが始める前に {#before-you-begin}

Chat2Query API を使用する前に、TiDB クラスターを作成し、 [SQLクエリを生成するAI](/tidb-cloud/explore-data-with-chat2query.md)有効にしていることを確認してください。 TiDB クラスターがない場合は、 [TiDB サーバーレスクラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)または[TiDB 専用クラスターの作成](/tidb-cloud/create-tidb-cluster.md)の手順に従って作成します。

## ステップ 1. Chat2Query API を有効にする {#step-1-enable-the-chat2query-api}

Chat2Query API を有効にするには、次の手順を実行します。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅の をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  クラスター名をクリックし、左側のナビゲーション ウィンドウで**[Chat2Query]**をクリックします。

3.  Chat2Query の右上隅で**[...]**をクリックし、 **[設定]**を選択します。

4.  **DataAPI を**有効にすると、Chat2Query データ アプリが作成されます。

    > **注記：**
    >
    > 1 つの TiDB クラスターで DataAPI を有効にすると、同じプロジェクト内のすべての TiDB クラスターで Chat2Query API を使用できるようになります。

5.  メッセージ内の**「Data Service」**リンクをクリックして、Chat2Query API にアクセスします。

    **Chat2Query System** [データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)とその**Chat2Data** [終点](/tidb-cloud/tidb-cloud-glossary.md#endpoint)左側のペインに表示されていることがわかります。

## ステップ 2. API キーを作成する {#step-2-create-an-api-key}

エンドポイントを呼び出す前に、API キーを作成する必要があります。 Chat2Query データ アプリの API キーを作成するには、次の手順を実行します。

1.  [**データサービス**](https://tidbcloud.com/console/data-service)の左側のペインで、 **Chat2Query システム**の名前をクリックして詳細を表示します。

2.  **「認証」**領域で、 **「API キーの作成」を**クリックします。

3.  **[API キーの作成]**ダイアログ ボックスで、説明を入力し、API キーのロールを選択します。

    このロールは、API キーがデータ アプリにリンクされたクラスターに対してデータの読み取りまたは書き込みを行えるかどうかを制御するために使用されます。 `ReadOnly`または`ReadAndWrite`役割を選択できます。

    -   `ReadOnly` : API キーは`SELECT` 、 `SHOW` 、 `USE` 、 `DESC` 、 `EXPLAIN`ステートメントなどのデータの読み取りのみを許可します。
    -   `ReadAndWrite` : API キーによるデータの読み取りと書き込みを許可します。この API キーを使用して、DML ステートメントや DDL ステートメントなどのすべての SQL ステートメントを実行できます。

4.  **「次へ」**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密キーをコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密キーを再度取得することはできなくなります。

5.  **「完了」**をクリックします。

## ステップ 3. Chat2Data エンドポイントを呼び出す {#step-3-call-the-chat2data-endpoint}

[**データサービス**](https://tidbcloud.com/console/data-service)ページの左側のペインで、 **[Chat2Query]** &gt; **[/chat2data]**をクリックしてエンドポイントの詳細を表示します。 Chat2Data の**プロパティが**表示されます。

-   **エンドポイント パス**: (読み取り専用) Chat2Data エンドポイントのパス`/chat2data` 。

-   **エンドポイント URL** : (読み取り専用) Chat2Data エンドポイントの URL。エンドポイントを呼び出すために使用されます。たとえば、 `https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data` 。

-   **Request Method** : (読み取り専用) Chat2Data エンドポイントの HTTP メソッド`POST` 。

-   **Timeout(ms)** : Chat2Data エンドポイントのタイムアウト (ミリ秒単位)。

-   **Max Rows** : Chat2Data エンドポイントが返す最大行数。

TiDB Cloudは、エンドポイントの呼び出しに役立つコード サンプルを生成します。例を取得してコードを実行するには、次の手順を実行します。

1.  現在の**Chat2Data**ページで、 **[エンドポイント URL]**の右側にある**[コード例]**をクリックします。 **[コード例]**ダイアログ ボックスが表示されます。
2.  ダイアログ ボックスで、エンドポイントの呼び出しに使用するクラスターとデータベースを選択し、コード例をコピーします。
3.  コード例をアプリケーションに貼り付けて実行します。

    -   `<Public Key>`と`<Private Key>`プレースホルダーを API キーに置き換えます。
    -   `<your instruction>`プレースホルダーを、AI に SQL ステートメントを生成して実行させる命令に置き換えます。
    -   `<your table name, optional>`プレースホルダーを、クエリするテーブル名に置き換えます。テーブル名を指定しない場合、AI はデータベース内のすべてのテーブルをクエリします。

> **注記：**
>
> 各 Chat2Query データ アプリには、1 日あたり 100 リクエストのレート制限があります。レート制限を超えると、API は`429`エラーを返します。さらに割り当てが必要な場合は、サポート チームに[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)お問い合わせください。

次のコード例は、 `sample_data.github_events`テーブルから最も人気のある GitHub リポジトリを検索するために使用されます。

```bash
curl --digest --user '<Public Key>:<Private Key>' \
  --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data' \
  --header 'content-type: application/json' \
  --data-raw '{
      "cluster_id": "12345678912345678960",
      "database": "sample_data",
      "tables": ["github_events"],
      "instruction": "Find the most popular repo from GitHub events"
      }'
```

前述の例では、リクエスト本文は次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。 TiDB クラスターの一意の識別子。
-   `database` :*文字列*。データベースの名前。
-   `tables` :*配列*。 (オプション) クエリ対象のテーブル名のリスト。
-   `instruction` :*文字列*。必要なクエリを説明する自然言語命令。

応答は次のとおりです。

```json
{
    "type": "chat2data_endpoint",
    "data": {
        "columns": [
            {
                "col": "repo_name",
                "data_type": "VARCHAR",
                "nullable": false
            },
            {
                "col": "count",
                "data_type": "BIGINT",
                "nullable": false
            }
        ],
        "rows": [
            {
                "count": "2390",
                "repo_name": "pytorch/pytorch"
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
            "limit": 50,
            "sql": "SELECT sample_data.github_events.`repo_name`, COUNT(*) AS count FROM sample_data.github_events GROUP BY sample_data.github_events.`repo_name` ORDER BY count DESC LIMIT 1;",
            "ai_latency": "30ms"
        }
    }
```

API 呼び出しが成功しなかった場合は、 `200`以外のステータス コードが返されます。以下は`500`ステータス コードの例です。

```json
{
    "type": "chat2data_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 500,
            "message": "internal error! defaultPermissionHelper: rpc error: code = DeadlineExceeded desc = context deadline exceeded",
            "start_ms": "",
            "end_ms": "",
            "latency": "",
            "row_count": 0,
            "row_affect": 0,
            "limit": 0
        }
    }
}
```

## もっと詳しく知る {#learn-more}

-   [APIキーを管理する](/tidb-cloud/data-service-api-key.md)
-   [データサービスのレスポンスコードとステータスコード](/tidb-cloud/data-service-response-and-status-code.md)
