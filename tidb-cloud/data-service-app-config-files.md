---
title: Data App Configuration Files
summary: このドキュメントでは、 TiDB Cloudのデータ アプリの構成ファイルについて説明します。
---

# データ アプリコンフィグレーションファイル {#data-app-configuration-files}

このドキュメントでは、 TiDB Cloudの[データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)の構成ファイルについて説明します。

[データアプリをGitHubに接続しました](/tidb-cloud/data-service-manage-github-connection.md)がある場合は、次のように GitHub の指定したディレクトリでデータ アプリの構成ファイルを見つけることができます。

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

データ アプリのデータ ソースは、リンクされた TiDB クラスターから取得されます。データ ソースの構成は`data_sources/cluster.json`にあります。

    ├── <Your Data App directory>
    │   ├── data_sources
    │   │   └── cluster.json

各データ アプリに対して、1 つまたは複数の TiDB クラスターにリンクできます。

以下は`cluster.json`の構成例です。この例では、このデータ アプリには 2 つのリンクされたクラスターがあります。

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

| 分野           | タイプ | 説明                                                                                                                                                             |
| ------------ | --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cluster_id` | 整数  | TiDB クラスターの ID。クラスターの URL から取得できます。たとえば、クラスター URL が`https://tidbcloud.com/console/clusters/1234567891234567890/overview`の場合、クラスター ID は`1234567891234567890`です。 |

## データアプリの構成 {#data-app-configuration}

データ アプリのプロパティには、アプリ ID、名前、タイプが含まれます。プロパティは`dataapp_config.json`ファイルにあります。

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

| 分野            | タイプ | 説明                                                                                                                                         |
| ------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `app_id`      | 弦   | データ アプリ ID。1 `dataapp_config.json`のファイルが別のデータ アプリからコピーされ、現在のデータ アプリの ID に更新する場合を除き、このフィールドを変更しないでください。そうしないと、この変更によってトリガーされたデプロイメントは失敗します。 |
| `app_name`    | 弦   | データ アプリ名。                                                                                                                                  |
| `app_type`    | 弦   | データ アプリのタイプ。指定できるのは`"dataapi"`のみです。                                                                                                        |
| `app_version` | 弦   | データ アプリのバージョン。形式は`"<major>.<minor>.<patch>"`です。たとえば、 `"1.0.0"` 。                                                                           |
| `description` | 弦   | データ アプリの説明。                                                                                                                                |

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

各データ アプリには、1 つまたは複数のエンドポイントが存在します。データ アプリのすべてのエンドポイントの構成は、 `http_endpoints/config.json`で確認できます。

以下は`config.json`の構成例です。この例では、このデータ アプリには 2 つのエンドポイントがあります。

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

| 分野                           | タイプ | 説明                                                                                                                                                                                                                                             |
| ---------------------------- | --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                       | 弦   | エンドポイント名。                                                                                                                                                                                                                                      |
| `description`                | 弦   | (オプション) エンドポイントの説明。                                                                                                                                                                                                                            |
| `method`                     | 弦   | エンドポイントの HTTP メソッド`GET`使用するとデータを取得でき、 `POST`使用するとデータを作成または挿入でき、 `PUT`使用するとデータを更新または変更でき、 `DELETE`使用するとデータを削除できます。                                                                                                                              |
| `endpoint`                   | 弦   | データ アプリ内のエンドポイントの一意のパス。パスには文字、数字、アンダースコア ( `_` )、スラッシュ ( `/` ) のみを使用できます。パスはスラッシュ ( `/` ) で始まり、文字、数字、またはアンダースコア ( `_` ) で終わる必要があります。たとえば、 `/my_endpoint/get_id`です。パスの長さは 64 文字未満にする必要があります。                                                    |
| `cluster_id`                 | 弦   | エンドポイントの TiDB クラスターの ID。TiDB クラスターの URL から取得できます。たとえば、クラスター URL が`https://tidbcloud.com/console/clusters/1234567891234567890/overview`の場合、クラスター ID は`1234567891234567890`です。                                                                   |
| `params`                     | 配列  | エンドポイントで使用されるパラメータ。パラメータを定義すると、エンドポイントを介してクエリ内のパラメータ値を動的に置き換えることができます。 `params`では、1 つまたは複数のパラメータを定義できます。パラメータごとに、 `name` 、 `type` 、 `required` 、および`default`フィールドを定義する必要があります。エンドポイントにパラメータが必要ない場合は、 `"params": []`のように`params`空のままにすることができます。 |
| `params.name`                | 弦   | パラメータの名前。名前には文字、数字、アンダースコア（ `_` ）のみを含めることができ、文字またはアンダースコア（ `_` ）で始まる必要があります。 `page`と`page_size` 、リクエスト結果のページ区切り用に予約されているため、パラメータ名として使用し**ないでください**。                                                                                            |
| `params.type`                | 弦   | パラメータのデータ型。サポートされている値は`string` 、 `number` 、 `integer` 、 `boolean` 、および`array`です。 `string`型のパラメータを使用する場合は、引用符 ( `'`または`"` ) を追加する必要はありません。たとえば、 `foo` `string`型に有効であり、 `"foo"`として処理されますが、 `"foo"` `"\"foo\""`として処理されます。                         |
| `params.required`            | 整数  | リクエストでパラメータが必須かどうかを指定します。サポートされている値は`0` (必須ではない) と`1` (必須) です。デフォルト値は`0`です。                                                                                                                                                                    |
| `params.enum`                | 弦   | (オプション) パラメータの値オプションを指定します。このフィールドは、 `params.type` `string` 、 `number` 、または`integer`に設定されている場合にのみ有効です。複数の値を指定するには、カンマ ( `,` ) で区切ります。                                                                                                          |
| `params.default`             | 弦   | パラメータのデフォルト値。値が指定したパラメータの型と一致していることを確認`ARRAY`てください。一致しない場合、エンドポイントはエラーを返します。1 型パラメータのデフォルト値は文字列であり、複数の値を区切るにはコンマ ( `,` ) を使用できます。                                                                                                              |
| `params.description`         | 弦   | パラメータの説明。                                                                                                                                                                                                                                      |
| `params.is_path_parameter`   | ブール | パラメータがパスパラメータであるかどうかを指定します。 `true`に設定されている場合、 `endpoint`フィールドに対応するパラメータプレースホルダが含まれていることを確認してください。含まれていない場合、デプロイメントが失敗します。逆に、 `endpoint`フィールドに対応するパラメータプレースホルダが含まれていても、このフィールドが`false`に設定されている場合も、デプロイメントが失敗します。                                |
| `settings.timeout`           | 整数  | エンドポイントのタイムアウト（ミリ秒単位）。デフォルトは`30000`です。 `1`から`60000`までの整数に設定できます。                                                                                                                                                                               |
| `settings.row_limit`         | 整数  | エンドポイントが操作または返すことができる行の最大数。デフォルトでは`1000`です。 `batch_operation` `0`に設定すると、 `1`から`2000`までの整数に設定できます。 `batch_operation` `1`に設定すると、 `1`から`100`までの整数に設定できます。                                                                                         |
| `settings.enable_pagination` | 整数  | リクエストによって返される結果のページ区切りを有効にするかどうかを制御します。サポートされている値は`0` (無効) と`1` (有効) です。デフォルト値は`0`です。                                                                                                                                                          |
| `settings.cache_enabled`     | 整数  | 指定された有効期間 (TTL) 内に`GET`リクエストによって返された応答をキャッシュするかどうかを制御します。サポートされている値は`0` (無効) と`1` (有効) です。デフォルト値は`0`です。                                                                                                                                        |
| `settings.cache_ttl`         | 整数  | `settings.cache_enabled` `1`に設定した場合の、キャッシュされた応答の有効期間 (TTL) の秒数。30 から 600 までの整数に設定できます。TTL 期間中に同じ`GET`要求を再度行うと、Data Service はターゲット データベースからデータを再度取得するのではなく、キャッシュされた応答を直接返すため、クエリのパフォーマンスが向上します。                                                 |
| `tag`                        | 弦   | エンドポイントのタグ。デフォルト値は`"Default"`です。                                                                                                                                                                                                               |
| `batch_operation`            | 整数  | エンドポイントがバッチ モードで動作できるようにするかどうかを制御します。サポートされている値は`0` (無効) と`1` (有効) です。 `1`に設定すると、1 回のリクエストで複数の行を操作できます。このオプションを有効にするには、リクエスト メソッドが`POST`または`PUT`あることを確認してください。                                                                                 |
| `sql_file`                   | 弦   | エンドポイントの SQL ファイル ディレクトリ。たとえば、 `"sql/GET-v1.sql"` 。                                                                                                                                                                                            |
| `type`                       | 弦   | エンドポイントのタイプ。定義済みシステム エンドポイントの場合は値は`"system-data"` 、その他のエンドポイントの場合は`"sql_endpoint"`です。                                                                                                                                                          |
| `return_type`                | 弦   | エンドポイントの応答形式`"json"`のみが可能です。                                                                                                                                                                                                                   |

### SQLファイルの構成 {#sql-file-configuration}

エンドポイントの SQL ファイルは、エンドポイントを介してデータをクエリするための SQL ステートメントを指定します。データ アプリのエンドポイント SQL ファイルは、 `http_endpoints/sql/`ディレクトリにあります。エンドポイントごとに、対応する SQL ファイルがあります。

SQL ファイル`method`名前は`<method>-<endpoint-path>.sql`形式です。3 と`<endpoint-path>` [`http_endpoints/config.json`](#endpoint-configuration)の`<method>`と`endpoint`構成と一致する必要があります。

SQL ファイルでは、テーブル結合クエリ、複雑なクエリ、集計関数などのステートメントを記述できます。以下は SQL ファイルの例です。

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

-   SQL ファイルの先頭で、SQL ステートメントにデータベースを指定する必要があります。たとえば、 `USE database_name;`です。

-   エンドポイントのパラメータを定義するには、SQL ステートメントに`${variable-name}`のような変数プレースホルダとして挿入します。

    前の例では、エンドポイントのパラメータとして`${country}`が使用されています。このパラメータを使用すると、エンドポイントの curl コマンドでクエリする国を指定できます。

    > **注記：**
    >
    > -   パラメータ名では大文字と小文字が区別されます。
    > -   パラメータはテーブル名または列名にすることはできません。
    > -   SQL ファイル内のパラメータ名は、 [`http_endpoints/config.json`](#endpoint-configuration)で構成されたパラメータ名と一致します。
