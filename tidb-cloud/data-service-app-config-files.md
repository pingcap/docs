---
title: Data App Configuration Files
summary: このドキュメントでは、TiDB Cloudのデータ アプリの構成ファイルについて説明します。
---

# データアプリコンフィグレーションファイル {#data-app-configuration-files}

このドキュメントでは、TiDB Cloudの[データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)の構成ファイルについて説明します。

データ[データアプリをGitHubに接続しました](/tidb-cloud/data-service-manage-github-connection.md)た場合は、次のように GitHub の指定したディレクトリでデータアプリの構成ファイルを見つけることができます。

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

## データソース構成 {#data-source-configuration}

データアプリのデータソースは、リンクされた TiDB クラスターから取得されます。データソースの設定は`data_sources/cluster.json`で確認できます。

    ├── <Your Data App directory>
    │   ├── data_sources
    │   │   └── cluster.json

各データアプリは、1つまたは複数のTiDBクラスターにリンクできます。

以下は`cluster.json`の構成例です。この例では、このデータアプリにリンクされたクラスターが 2 つあります。

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

当該フィールドの説明は以下のとおりです。

| 分野           | タイプ | 説明                                                                                                                                                                                          |
| ------------ | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cluster_id` | 整数  | TiDB Cloud StarterインスタンスのIDです。インスタンスのURLから取得できます。たとえば、インスタンスのURLが`https://tidbcloud.com/tidbs/1234567891234567890/overview?orgId=<organization-id>`の場合、インスタンスIDは`1234567891234567890`になります。 |

## データアプリの設定 {#data-app-configuration}

データアプリのプロパティには、アプリID、名前、およびタイプが含まれます。これらのプロパティは`dataapp_config.json`ファイルで確認できます。

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

各項目の説明は以下のとおりです。

| 分野            | タイプ | 説明                                                                                                                                    |
| ------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `app_id`      | 弦   | データアプリID。 `dataapp_config.json`ファイルが別のデータアプリからコピーされたもので、現在のデータアプリのIDに更新したい場合を除き、このフィールドは変更しないでください。そうでない場合、この変更によってトリガーされるデプロイは失敗します。 |
| `app_name`    | 弦   | データアプリの名前。                                                                                                                            |
| `app_type`    | 弦   | データアプリのタイプは、 `"dataapi"`のみとなります。                                                                                                      |
| `app_version` | 弦   | データアプリのバージョンは、 `"<major>.<minor>.<patch>"`形式です。たとえば、 `"1.0.0"` 。                                                                      |
| `description` | 弦   | データアプリの説明。                                                                                                                            |

## HTTPエンドポイント構成 {#http-endpoint-configuration}

データアプリのディレクトリには、 `http_endpoints/config.json`にエンドポイント構成があり、 `http_endpoints/sql/<method>-<endpoint-name>.sql`に SQL ファイルが見つかります。

    ├── <Your Data App directory>
    │   ├── http_endpoints
    │   │   ├── config.json
    │   │   └── sql
    │   │       ├── <method>-<endpoint-path1>.sql
    │   │       ├── <method>-<endpoint-path2>.sql
    │   │       └── <method>-<endpoint-path3>.sql

### エンドポイント構成 {#endpoint-configuration}

各データアプリには、1つまたは複数のエンドポイントが存在する可能性があります。データアプリのすべてのエンドポイントの設定は`http_endpoints/config.json`で確認できます。

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

各項目の説明は以下のとおりです。

| 分野                           | タイプ  | 説明                                                                                                                                                                                                                                                                                            |
| ---------------------------- | ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                       | 弦    | エンドポイント名。                                                                                                                                                                                                                                                                                     |
| `description`                | 弦    | （オプション）エンドポイントの説明。                                                                                                                                                                                                                                                                            |
| `method`                     | 弦    | エンドポイントの HTTP メソッド。 `GET`を使用してデータを取得し、 `POST`を使用してデータを作成または挿入し、 `PUT`を使用してデータを更新または変更し、 `DELETE`を使用してデータを削除できます。                                                                                                                                                                              |
| `endpoint`                   | 弦    | データ アプリ内のエンドポイントの一意のパス。パスには、文字、数字、アンダースコア ( `_` )、およびスラッシュ ( `/` ) のみを使用できます。パスはスラッシュ ( `/` ) で始まり、文字、数字、またはアンダースコア ( `_` ) で終わる必要があります。例: `/my_endpoint/get_id` 。パスの長さは 64 文字未満である必要があります。                                                                                                   |
| `cluster_id`                 | 弦    | エンドポイントのTiDB Cloud Starterインスタンスの ID です。インスタンスの URL から取得できます。たとえば、インスタンスの URL が`https://tidbcloud.com/tidbs/1234567891234567890/overview?orgId=<organization-id>`の場合、インスタンス ID は`1234567891234567890`です。                                                                                      |
| `params`                     | 配列   | エンドポイントで使用されるパラメーター。パラメーターを定義することで、エンドポイントを介してクエリ内のパラメーター値を動的に置き換えることができます。 `params`では、1 つまたは複数のパラメーターを定義できます。各パラメーターについて、 `name` 、 `type` 、 `required` 、および`default`フィールドを定義する必要があります。エンドポイントにパラメーターが必要ない場合は`params` }} のように { `"params": []` PLACEHOLDER-5-PLACEHOLDER-E}} を空のままにすることができます。 |
| `params.name`                | 弦    | パラメータ名。名前には文字、数字、アンダースコアのみを使用できます（ `_` ）。また、文字またはアンダースコアで始まる必要があります（ `_` ）。 `page`および`page_size`はリクエスト結果のページネーション用に**予約されて**いるため、パラメータ名として使用しないでください。                                                                                                                                         |
| `params.type`                | 弦    | パラメーターのデータ型。サポートされている値は`string` 、 `number` 、 `integer` 、 `boolean` 、および`array` 。 `string`型のパラメーターを使用する場合は、引用符（ `'`または`"` ）を追加する必要はありません。例えば、 `foo` `string`タイプに対して有効であり、 `"foo"`として処理されますが、 `"foo"`は`"\"foo\""`として処理されます。                                                                     |
| `params.required`            | 整数   | リクエストでパラメータが必須かどうかを指定します。サポートされている値は、 `0` (必須ではない) と`1` (必須) です。デフォルト値は`0`です。                                                                                                                                                                                                                 |
| `params.enum`                | 弦    | （オプション）パラメーターの値オプションを指定します。このフィールドは、 `params.type`が`string` 、 `number` 、または`integer`に設定されている場合にのみ有効です。複数の値を指定する場合は、カンマで区切ります（ `,` ）。                                                                                                                                                          |
| `params.default`             | 弦    | パラメーターのデフォルト値です。指定したパラメーターの型と値が一致していることを確認してください。一致しない場合、エンドポイントはエラーを返します。 `ARRAY`型のパラメーターのデフォルト値は文字列で、複数の値を区切るにはカンマ ( `,` ) を使用できます。                                                                                                                                                         |
| `params.description`         | 弦    | パラメータの説明。                                                                                                                                                                                                                                                                                     |
| `params.is_path_parameter`   | ブール値 | パラメータがパス パラメータであるかどうかを指定します。 `true`に設定されている場合、 `endpoint`フィールドに該当するパラメータ プレースホルダーが含まれていることを確認してください。含まれていない場合、デプロイが失敗します。逆に、 `endpoint`フィールドに該当するパラメータ プレースホルダーが含まれているにもかかわらず、このフィールドが`false`に設定されている場合も、デプロイが失敗します。                                                                          |
| `settings.timeout`           | 整数   | エンドポイントのタイムアウト時間（ミリ秒単位）。デフォルトでは`30000`です。 `1`から`60000`までの整数値を設定できます。                                                                                                                                                                                                                          |
| `settings.row_limit`         | 整数   | エンドポイントが操作または返すことができる行の最大数。デフォルトでは`1000`です。 `batch_operation`が`0`に設定されている場合、 `1`から`2000`までの整数に設定できます。 `batch_operation`が`1`に設定されている場合、 `1` `100`までの整数に設定できます。                                                                                                                                 |
| `settings.enable_pagination` | 整数   | リクエストによって返される結果のページネーションを有効にするかどうかを制御します。サポートされている値は、 `0` (無効) と`1` (有効) です。デフォルト値は`0`です。                                                                                                                                                                                                     |
| `settings.cache_enabled`     | 整数   | `GET`リクエストによって返されたレスポンスを、指定された有効期限 (TTL) 期間内にキャッシュするかどうかを制御します。サポートされている値は、 `0` (無効) と`1` (有効) です。デフォルト値は`0`です。                                                                                                                                                                               |
| `settings.cache_ttl`         | 整数   | `settings.cache_enabled`を`1`に設定した場合のキャッシュされた応答の有効期間 (TTL) を秒単位で指定します。30 ～ 600 の整数値を設定できます。TTL 期間中に同じ`GET`リクエストを再度行うと、データ サービスは対象データベースからデータを再度取得する代わりに、キャッシュされた応答を直接返します。これにより、クエリのパフォーマンスが向上します。                                                                                             |
| `tag`                        | 弦    | エンドポイントのタグ。デフォルト値は`"Default"`です。                                                                                                                                                                                                                                                              |
| `batch_operation`            | 整数   | エンドポイントをバッチモードで動作させるかどうかを制御します。サポートされている値は`0` (無効) と`1` (有効) です。 `1`に設定すると、1 つのリクエストで複数の行を操作できます。このオプションを有効にするには、リクエストメソッドが`POST`または`PUT`であることを確認してください。                                                                                                                                      |
| `sql_file`                   | 弦    | エンドポイントの SQL ファイルディレクトリ。例: `"sql/GET-v1.sql"` 。                                                                                                                                                                                                                                               |
| `type`                       | 弦    | エンドポイントのタイプ。定義済みのシステムエンドポイントの場合は`"system-data"` 、その他のエンドポイントの場合は`"sql_endpoint"`となります。                                                                                                                                                                                                        |
| `return_type`                | 弦    | エンドポイントの応答形式は`"json"`のみです。                                                                                                                                                                                                                                                                    |

### SQLファイル構成 {#sql-file-configuration}

エンドポイントの SQL ファイルには、エンドポイントを介してデータを照会するための SQL ステートメントが指定されています。データ アプリのエンドポイント SQL ファイルは`http_endpoints/sql/`ディレクトリにあります。各エンドポイントには、対応する SQL ファイルが必要です。

SQL ファイルの名前は`<method>-<endpoint-path>.sql`形式です。ここで、 `<method>`と`<endpoint-path>`は[`http_endpoints/config.json`](#endpoint-configuration)の`method`と`endpoint`の設定と一致する必要があります。

SQLファイルには、テーブル結合クエリ、複雑なクエリ、集計関数などのステートメントを記述できます。以下はSQLファイルの例です。

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

SQLファイルを作成する際は、以下の点に注意してください。

-   SQL ファイルの先頭で、SQL ステートメント内のデータベースを指定する必要があります。たとえば、 `USE database_name;`のようになります。

-   エンドポイントのパラメータを定義するには、 `${variable-name}`のような変数プレースホルダーとして SQL ステートメントに挿入します。

    上記の例では、 `${country}`がエンドポイントのパラメータとして使用されています。このパラメータを使用すると、エンドポイントの curl コマンドでクエリ対象の国を指定できます。

    > **注記：**
    >
    > -   パラメータ名は大文字と小文字を区別します。
    > -   パラメータには、テーブル名または列名を指定することはできません。
    > -   SQL ファイル内のパラメータ名は[`http_endpoints/config.json`](#endpoint-configuration)で設定されているパラメータ名と一致します。
