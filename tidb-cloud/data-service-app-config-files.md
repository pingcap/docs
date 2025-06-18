---
title: Data App Configuration Files
summary: このドキュメントでは、TiDB Cloudのデータ アプリの構成ファイルについて説明します。
---

# データアプリコンフィグレーションファイル {#data-app-configuration-files}

このドキュメントでは、 TiDB Cloudの[データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)の構成ファイルについて説明します。

[データアプリをGitHubに接続しました](/tidb-cloud/data-service-manage-github-connection.md)がある場合は、次のように GitHub の指定したディレクトリにデータ アプリの構成ファイルが見つかります。

    ├── <Your Data App directory>
    │   ├── data_sources
    │   │   └── cluster.json
    │   ├── dataapp_config.json
    │   ├── http_endpoints
    │   │   ├── config.json
    │   │   └── sql
    │   │       ├── <method>-<endpoint-path1>.sql
    │   │       ├── <method>-<endpoint-path2>.sql
    │   │       └── <method>-<endpoint-path3>.sql

## データソースの構成 {#data-source-configuration}

データアプリのデータソースは、リンクされたTiDBクラスタから取得されます。データソースの構成は`data_sources/cluster.json`に記載されています。

    ├── <Your Data App directory>
    │   ├── data_sources
    │   │   └── cluster.json

各データ アプリごとに、1 つまたは複数の TiDB クラスターにリンクできます。

以下は`cluster.json`の構成例です。この例では、このデータアプリには 2 つのリンクされたクラスターがあります。

```json
[
  {
    "cluster_id": <Cluster ID1>
  },
  {
    "cluster_id": <Cluster ID2>
  }
]
```

フィールドの説明は次のとおりです。

| 分野           | タイプ | 説明                                                                                                                                               |
| ------------ | --- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cluster_id` | 整数  | TiDBクラスターのIDです。クラスターのURLから取得できます。例えば、クラスターのURLが`https://tidbcloud.com/clusters/1234567891234567890/overview`の場合、クラスターIDは`1234567891234567890`です。 |

## データアプリの構成 {#data-app-configuration}

データアプリのプロパティには、アプリID、名前、タイプが含まれます。これらのプロパティは`dataapp_config.json`ファイルで確認できます。

    ├── <Your Data App directory>
    │   ├── dataapp_config.json

以下は`dataapp_config.json`の構成例です。

```json
{
  "app_id": "<Data App ID>",
  "app_name": "<Data App name>",
  "app_type": "dataapi",
  "app_version": "<Data App version>",
  "description": "<Data App description>"
}
```

各フィールドの説明は次のとおりです。

| 分野            | タイプ | 説明                                                                                                                           |
| ------------- | --- | ---------------------------------------------------------------------------------------------------------------------------- |
| `app_id`      | 弦   | データアプリID。1 `dataapp_config.json`が別のデータアプリからコピーされ、現在のデータアプリのIDに更新する場合を除き、このフィールドを変更しないでください。変更しないと、この変更によってトリガーされるデプロイが失敗します。 |
| `app_name`    | 弦   | データ アプリの名前。                                                                                                                  |
| `app_type`    | 弦   | データ アプリのタイプ。指定できるのは`"dataapi"`のみです。                                                                                          |
| `app_version` | 弦   | データアプリのバージョン（ `"<major>.<minor>.<patch>"`形式）。例： `"1.0.0"` 。                                                                  |
| `description` | 弦   | データ アプリの説明。                                                                                                                  |

## HTTPエンドポイント構成 {#http-endpoint-configuration}

データ アプリ ディレクトリでは、エンドポイント構成は`http_endpoints/config.json`に、SQL ファイルは`http_endpoints/sql/<method>-<endpoint-name>.sql`にあります。

    ├── <Your Data App directory>
    │   ├── http_endpoints
    │   │   ├── config.json
    │   │   └── sql
    │   │       ├── <method>-<endpoint-path1>.sql
    │   │       ├── <method>-<endpoint-path2>.sql
    │   │       └── <method>-<endpoint-path3>.sql

### エンドポイント構成 {#endpoint-configuration}

各データアプリには、1つまたは複数のエンドポイントが存在します。データアプリのすべてのエンドポイントの設定は、 `http_endpoints/config.json`で確認できます。

以下は`config.json`の構成例です。この例では、このデータアプリには 2 つのエンドポイントがあります。

```json
[
  {
    "name": "<Endpoint name1>",
    "description": "<Endpoint description1>",
    "method": "<HTTP method1>",
    "endpoint": "<Endpoint path1>",
    "data_source": {
      "cluster_id": <Cluster ID1>
    },
    "params": [],
    "settings": {
      "timeout": <Endpoint timeout>,
      "row_limit": <Maximum rows>,
      "enable_pagination": <0 | 1>,
      "cache_enabled": <0 | 1>,
      "cache_ttl": <time-to-live period>
    },
    "tag": "Default",
    "batch_operation": <0 | 1>,
    "sql_file": "<SQL file directory1>",
    "type": "sql_endpoint",
    "return_type": "json"
  },
  {
    "name": "<Endpoint name2>",
    "description": "<Endpoint description2>",
    "method": "<HTTP method2>",
    "endpoint": "<Endpoint path2>",
    "data_source": {
      "cluster_id": <Cluster ID2>
    },
    "params": [
      {
        "name": "<Parameter name>",
        "type": "<Parameter type>",
        "required": <0 | 1>,
        "default": "<Parameter default value>",
        "description": "<Parameter description>",
        "is_path_parameter": <true | false>
      }
    ],
    "settings": {
      "timeout": <Endpoint timeout>,
      "row_limit": <Maximum rows>,
      "enable_pagination": <0 | 1>,
      "cache_enabled": <0 | 1>,
      "cache_ttl": <time-to-live period>
    },
    "tag": "Default",
    "batch_operation": <0 | 1>,
    "sql_file": "<SQL file directory2>",
    "type": "sql_endpoint",
    "return_type": "json"
  }
]
```

各フィールドの説明は次のとおりです。

| 分野                           | タイプ  | 説明                                                                                                                                                                                                                |
| ---------------------------- | ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                       | 弦    | エンドポイント名。                                                                                                                                                                                                         |
| `description`                | 弦    | (オプション) エンドポイントの説明。                                                                                                                                                                                               |
| `method`                     | 弦    | エンドポイントのHTTPメソッド`GET`データの取得、 `POST`データの作成または挿入、 `PUT`データの更新または変更、 `DELETE`データの削除に使用できます。                                                                                                                          |
| `endpoint`                   | 弦    | データアプリ内のエンドポイントの一意のパス。パスには文字、数字、アンダースコア（ `_` ）、スラッシュ（ `/` ）のみを使用できます。パスはスラッシュ（ `/` ）で始まり、文字、数字、またはアンダースコア（ `_` ）で終わる必要があります。例： `/my_endpoint/get_id` 。パスの長さは64文字未満である必要があります。                                     |
| `cluster_id`                 | 弦    | エンドポイントのTiDBクラスターのIDです。TiDBクラスターのURLから取得できます。例えば、クラスターURLが`https://tidbcloud.com/clusters/1234567891234567890/overview`の場合、クラスターIDは`1234567891234567890`です。                                                       |
| `params`                     | 配列   | エンドポイントで使用されるパラメータ。パラメータを定義することで、エンドポイントを介したクエリ内のパラメータ値を動的に置き換えることができます。1 では、 `params` `type` `name` `required`を定義する必要があります。エンドポイントにパラメータが不要な場合は、 `params`空白のままにすることができます（例： `default` `"params": []` 。           |
| `params.name`                | 弦    | パラメータ名。名前には文字、数字、アンダースコア（ `_` ）のみを使用でき、文字またはアンダースコア（ `_` ）で始まる必要があります。7と`page_size` `page`結果のページ区切り用に予約されているため、パラメータ名として使用し**ないでください**。                                                                           |
| `params.type`                | 弦    | パラメータのデータ型。サポートされる値は`string` 、 `number` 、 `integer` 、 `boolean` 、 `array`です。11 型のパラメータを使用する場合は、引用符（ `'`または`"` ）を追加する必要はありません。例えば、 `string`型`string`は`foo`が有効であり、 `"foo"`として処理されますが、 `"foo"` `"\"foo\""`として処理されます。 |
| `params.required`            | 整数   | リクエストにおいてパラメータが必須かどうかを指定します。サポートされている値は`0` （必須ではない）と`1` （必須）です。デフォルト値は`0`です。                                                                                                                                      |
| `params.enum`                | 弦    | （オプション）パラメータの値オプションを指定します。このフィールドは、 `params.type` `string` 、 `number` 、または`integer`に設定されている場合にのみ有効です。複数の値を指定するには、カンマ（ `,` ）で区切ります。                                                                                |
| `params.default`             | 弦    | パラメータのデフォルト値です。値が指定したパラメータの型と一致していることを確認してください。一致していない場合、エンドポイントはエラーを返します。1 型`ARRAY`パラメータのデフォルト値は文字列で、複数の値を指定する場合はカンマ ( `,` ) で区切ることができます。                                                                        |
| `params.description`         | 弦    | パラメータの説明。                                                                                                                                                                                                         |
| `params.is_path_parameter`   | ブール値 | パラメータがパスパラメータかどうかを指定します`true`に設定されている場合、 `endpoint`フィールドに対応するパラメータプレースホルダが含まれていることを確認してください。含まれていない場合、デプロイに失敗します。逆に、 `endpoint`フィールドに対応するパラメータプレースホルダが含まれているにもかかわらず、このフィールドが`false`に設定されている場合も、デプロイに失敗します。        |
| `settings.timeout`           | 整数   | エンドポイントのタイムアウト（ミリ秒単位）。デフォルトは`30000`です`1`から`60000`までの整数に設定できます。                                                                                                                                                    |
| `settings.row_limit`         | 整数   | エンドポイントが操作または返すことができる行の最大数。デフォルトは`1000`です。3 `batch_operation` `0`に設定すると、 `1`から`2000`までの整数を設定できます。11 `batch_operation` `1`に設定すると、 `1`から`100`までの整数を設定できます。                                                          |
| `settings.enable_pagination` | 整数   | リクエストによって返される結果のページ区切りを有効にするかどうかを制御します。サポートされる値は`0` (無効) と`1` (有効) です。デフォルト値は`0`です。                                                                                                                               |
| `settings.cache_enabled`     | 整数   | `GET`リクエストで返されたレスポンスを、指定された有効期限（TTL）内にキャッシュするかどうかを制御します。サポートされている値は`0` （無効）と`1` （有効）です。デフォルト値は`0`です。                                                                                                              |
| `settings.cache_ttl`         | 整数   | `settings.cache_enabled` `1`に設定した場合の、キャッシュされたレスポンスの有効期間（TTL）（秒単位）。30 から 600 までの整数に設定できます。TTL 期間中に同じリクエストを`GET`再度送信した場合、Data Service はターゲットデータベースからデータを再度取得するのではなく、キャッシュされたレスポンスを直接返すため、クエリのパフォーマンスが向上します。         |
| `tag`                        | 弦    | エンドポイントのタグ。デフォルト値は`"Default"`です。                                                                                                                                                                                  |
| `batch_operation`            | 整数   | エンドポイントをバッチモードで操作できるようにするかどうかを制御します。サポートされる値は`0` (無効) と`1` (有効) です。 `1`に設定すると、1 回のリクエストで複数の行を操作できます。このオプションを有効にするには、リクエストメソッドが`POST`または`PUT`であることを確認してください。                                                       |
| `sql_file`                   | 弦    | エンドポイントのSQLファイルディレクトリ。例： `"sql/GET-v1.sql"` 。                                                                                                                                                                     |
| `type`                       | 弦    | エンドポイントのタイプ。定義済みシステムエンドポイントの場合は値は`"system-data"` 、その他のエンドポイントの場合は`"sql_endpoint"` 。                                                                                                                               |
| `return_type`                | 弦    | エンドポイントの応答形式`"json"`のみが可能です。                                                                                                                                                                                      |

### SQLファイルの構成 {#sql-file-configuration}

エンドポイントのSQLファイルは、エンドポイントを介してデータをクエリするためのSQL文を指定します。データアプリのエンドポイントSQLファイルは、 `http_endpoints/sql/`ディレクトリにあります。エンドポイントごとに、対応するSQLファイルが存在します。

SQL ファイルの名前は`<method>-<endpoint-path>.sql`形式です。3 と`<endpoint-path>` `<method>` [`http_endpoints/config.json`](#endpoint-configuration) `method`と`endpoint`構成と一致する必要があります。

SQLファイルでは、テーブル結合クエリ、複雑なクエリ、集計関数などのステートメントを記述できます。以下はSQLファイルの例です。

```sql
/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries in the TiDB Cloud console.
Declare a parameter like "Where id = ${arg}".
*/
USE sample_data;
SELECT
  rank,
  company_name,
FROM
  global_fortune_500_2018_2022
WHERE
  country = ${country};
```

SQL ファイルを書き込むときは、次の点に注意してください。

-   SQLファイルの先頭で、SQL文にデータベースを指定する必要があります。例： `USE database_name;` 。

-   エンドポイントのパラメータを定義するには、それを`${variable-name}`ような変数プレースホルダとして SQL ステートメントに挿入します。

    上記の例では、エンドポイントのパラメータとして`${country}`使用されています。このパラメータを使用することで、エンドポイントの curl コマンドでクエリする国を指定できます。

    > **注記：**
    >
    > -   パラメータ名では大文字と小文字が区別されます。
    > -   パラメータにはテーブル名または列名は指定できません。
    > -   SQL ファイル内のパラメータ名は、 [`http_endpoints/config.json`](#endpoint-configuration)で構成されたパラメータ名と一致します。
