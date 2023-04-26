---
title: Get Started with Chat2Query API
summary: Learn how to use TiDB Cloud Chat2Query API to generate and execute SQL statements using AI by providing instructions.
---

# Chat2Query API を使ってみる {#get-started-with-chat2query-api}

TiDB Cloud は、命令を提供することで AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェイスである Chat2Query API を提供します。次に、API がクエリ結果を返します。

Chat2Query API は HTTPS 経由でのみアクセスできるため、ネットワーク経由で送信されるすべてのデータは TLS を使用して暗号化されます。

> **ノート：**
>
> Chat2Query API は[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターでのみ使用できます。

## あなたが始める前に {#before-you-begin}

Chat2Query API を使用する前に、 [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターを作成し、 [AI による SQL クエリの生成](/tidb-cloud/explore-data-with-chat2query.md)有効にしていることを確認してください。 Serverless Tierクラスターがない場合は、 [クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)の手順に従って作成します。

## ステップ 1.Chat2Query API を有効にする {#step-1-enable-the-chat2query-api}

Chat2Query API を有効にするには、次の手順を実行します。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

2.  クラスター名をクリックし、左側のナビゲーション ペインで**[Chat2Query]**をクリックします。

3.  Chat2Query の右上隅にある**[...]**をクリックし、 <strong>[設定]</strong>を選択します。

4.  **DataAPI を**有効にすると、Chat2Query データ アプリが作成されます。

    > **ノート：**
    >
    > 1 つのServerless Tierクラスターで DataAPI を有効にすると、同じプロジェクト内のすべてのServerless Tierクラスターで Chat2Query API を使用できるようになります。

5.  メッセージ内の**Data Service**リンクをクリックして、Chat2Query API にアクセスします。

    **Chat2Query システム**[データ アプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)とその<strong>Chat2Data</strong> [終点](/tidb-cloud/tidb-cloud-glossary.md#endpoint)左側のペインに表示されていることがわかります。

## ステップ 2. API キーを作成する {#step-2-create-an-api-key}

エンドポイントを呼び出す前に、API キーを作成する必要があります。 Chat2Query データ アプリの API キーを作成するには、次の手順を実行します。

1.  [**データサービス**](https://tidbcloud.com/console/data-service)の左側のペインで、 **Chat2Query システム**の名前をクリックして詳細を表示します。

2.  **[API キー]**領域で、 <strong>[API キーの作成]</strong>をクリックします。

3.  **[API キーの作成]**ダイアログ ボックスで、説明を入力し、API キーのロールを選択します。

    ロールは、API キーが Data App にリンクされたクラスターにデータを読み書きできるかどうかを制御するために使用されます。 `ReadOnly`または`ReadAndWrite`役割を選択できます。

    -   `ReadOnly` : API キーが`SELECT` 、 `SHOW` 、 `USE` 、 `DESC` 、および`EXPLAIN`ステートメントなどのデータを読み取ることのみを許可します。
    -   `ReadAndWrite` : API キーによるデータの読み取りと書き込みを許可します。この API キーを使用して、DML ステートメントや DDL ステートメントなど、すべての SQL ステートメントを実行できます。

4.  **[次へ]**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密鍵をコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密鍵を再度取得することはできなくなります。

5.  **[完了]**をクリックします。

## ステップ 3. Chat2Data エンドポイントを呼び出す {#step-3-call-the-chat2data-endpoint}

[**データサービス**](https://tidbcloud.com/console/data-service)ページの左側のペインで、 **Chat2Query** &gt; <strong>/chat2data</strong>をクリックして、エンドポイントの詳細を表示します。 Chat2Data の<strong>プロパティが</strong>表示されます。

-   **Endpoint Path** : (読み取り専用) `/chat2data`である Chat2Data エンドポイントのパス。

-   **エンドポイント URL** : (読み取り専用) エンドポイントの呼び出しに使用される Chat2Data エンドポイントの URL。たとえば、 `https://data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data`です。

-   **Request Method** : (読み取り専用) Chat2Data エンドポイントの HTTP メソッド。これは`POST`です。

-   **Timeout(ms)** : Chat2Data エンドポイントのタイムアウト。

    -   デフォルト値: `30000`
    -   最大値: `60000`
    -   最小値: `1`
    -   単位：ミリ秒

-   **Max Rows** : Chat2Data エンドポイントが返す最大行数。

    -   デフォルト値: `50`
    -   最大値: `2000`
    -   最小値: `1`

TiDB Cloud は、エンドポイントを呼び出すのに役立つコード例を生成します。サンプルを取得してコードを実行するには、次の手順を実行します。

1.  現在の**Chat2Data**ページで、 <strong>[エンドポイント URL]</strong>の右側にある<strong>[コード例]</strong>をクリックします。 <strong>[コード例]</strong>ダイアログ ボックスが表示されます。
2.  ダイアログ ボックスで、エンドポイントの呼び出しに使用するクラスターとデータベースを選択し、コード例をコピーします。
3.  コード例をアプリケーションに貼り付けて実行します。

    -   `<Public Key>`と`<Private Key>`プレースホルダーを API キーに置き換えます。
    -   `<your instruction>`プレースホルダーを、AI が生成して SQL ステートメントを実行する命令に置き換えます。
    -   `<your table name, optional>`プレースホルダーをクエリするテーブル名に置き換えます。テーブル名を指定しない場合、AI はデータベース内のすべてのテーブルを照会します。

> **ノート：**
>
> 各 Chat2Query データ アプリには、1 日あたり 100 リクエストのレート制限があります。レート制限を超えると、API は`429`エラーを返します。さらに割り当てが必要な場合は、サポート チームに[リクエストを提出する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)してください。

次のコード例は、 `sample_data.github_events`テーブルから最も人気のある GitHub リポジトリを見つけるために使用されます。

```bash
curl --digest --user '<Public Key>:<Private Key>' \
  --request POST 'https://data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data' \
  --header 'content-type: application/json' \
  --data-raw '{
      "cluster_id": "12345678912345678960",
      "database": "sample_data",
      "tables": ["github_events"],
      "instruction": "Find the most popular repo from GitHub events"
      }'
```

前の例では、要求本文は次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。 TiDB クラスターの一意の識別子。
-   `database` :*文字列*。データベースの名前。
-   `tables` :*配列*。 (オプション) 照会するテーブル名のリスト。
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

API 呼び出しが成功しない場合は、 `200`以外のステータス コードが返されます。以下は、 `500`ステータス コードの例です。

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

-   [API キーを管理する](/tidb-cloud/data-service-api-key.md)
-   [データ サービスの応答コードとステータス コード](/tidb-cloud/data-service-response-and-status-code.md)
