---
title: Data App Configuration Files
summary: This document describes the configuration files of Data App in TiDB Cloud.
---

# データアプリコンフィグレーションファイル {#data-app-configuration-files}

このドキュメントでは、 TiDB Cloud[データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)構成ファイルについて説明します。

[データ アプリを GitHub に接続しました](/tidb-cloud/data-service-manage-github-connection.md)がある場合は、次のように GitHub 上の指定したディレクトリでデータ アプリの構成ファイルを見つけることができます。

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

データ アプリのデータ ソースは、リンクされた TiDB クラスターから取得されます。データ ソース構成は`data_sources/cluster.json`にあります。

    ├── <Your Data App directory>
    │   ├── data_sources
    │   │   └── cluster.json

データ アプリごとに、1 つまたは複数の TiDB クラスターにリンクできます。

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

| 分野            | タイプ | 説明                                                                                                                              |
| ------------- | --- | ------------------------------------------------------------------------------------------------------------------------------- |
| `app_id`      | 弦   | データアプリID。ファイルが`dataapp_config.json`のデータ アプリからコピーされ、現在のデータ アプリの ID に更新する場合を除き、このフィールドは変更しないでください。そうしないと、この変更によってトリガーされる展開は失敗します。 |
| `app_name`    | 弦   | データアプリ名。                                                                                                                        |
| `app_type`    | 弦   | データ アプリのタイプ。 `"dataapi"`のみにすることができます。                                                                                           |
| `app_version` | 弦   | Data App のバージョン`"<major>.<minor>.<patch>"`形式です。たとえば、 `"1.0.0"` 。                                                                |
| `description` | 弦   | データアプリの説明。                                                                                                                      |

## HTTPエンドポイント構成 {#http-endpoint-configuration}

Data App ディレクトリでは、エンドポイント構成が`http_endpoints/config.json`に、SQL ファイルが`http_endpoints/sql/<method>-<endpoint-name>.sql`にあります。

    ├── <Your Data App directory>
    │   ├── http_endpoints
    │   │   ├── config.json
    │   │   └── sql
    │   │       ├── <method>-<endpoint-path1>.sql
    │   │       ├── <method>-<endpoint-path2>.sql
    │   │       └── <method>-<endpoint-path3>.sql

### エンドポイント構成 {#endpoint-configuration}

データ アプリごとに、1 つまたは複数のエンドポイントが存在する可能性があります。データ アプリのすべてのエンドポイントの構成は`http_endpoints/config.json`で確認できます。

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
        "description": "<Parameter description>"
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

| 分野                           | タイプ | 説明                                                                                                                                                                                                                                                  |
| ---------------------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                       | 弦   | エンドポイント名。                                                                                                                                                                                                                                           |
| `description`                | 弦   | (オプション) エンドポイントの説明。                                                                                                                                                                                                                                 |
| `method`                     | 弦   | エンドポイントのHTTPメソッド。 `GET`を使用してデータを取得し、 `POST`を使用してデータを作成または挿入し、 `PUT`使用してデータを更新または変更し、 `DELETE`を使用してデータを削除できます。                                                                                                                                       |
| `endpoint`                   | 弦   | データ アプリ内のエンドポイントの一意のパス。パスには文字、数字、アンダースコア ( `_` )、およびスラッシュ ( `/` ) のみを使用できます。パスはスラッシュ ( `/` ) で始まり、文字、数字、またはアンダースコア ( `_` ) で終わる必要があります。たとえば、 `/my_endpoint/get_id` 。パスの長さは 64 文字未満である必要があります。                                                       |
| `cluster_id`                 | 弦   | エンドポイントの TiDB クラスターの ID。 TiDB クラスターの URL から取得できます。たとえば、クラスター URL が`https://tidbcloud.com/console/clusters/1234567891234567890/overview`の場合、クラスター ID は`1234567891234567890`です。                                                                       |
| `params`                     | 配列  | エンドポイントで使用されるパラメータ。パラメーターを定義すると、エンドポイントを通じてクエリ内のパラメーター値を動的に置き換えることができます。 `params`では、1 つまたは複数のパラメーターを定義できます。パラメーターごとに、その`name` 、 `type` 、 `required` 、および`default`フィールドを定義する必要があります。エンドポイントにパラメータが必要ない場合。 `params` `"params": []`のように空のままにすることができます。 |
| `params.name`                | 弦   | パラメータの名前。名前には文字、数字、アンダースコア ( `_` ) のみを含めることができ、文字またはアンダースコア ( `_` ) で始める必要があります。 `page`と`page_size`はパラメータ名として使用し**ないでください**。これらはリクエスト結果のページネーション用に予約されています。                                                                                         |
| `params.type`                | 弦   | パラメータのデータ型。サポートされている値は`string` 、 `number` 、 `integer` 、および`boolean`です。 `string`型パラメータを使用する場合は、引用符 ( `'`または`"` ) を追加する必要はありません。たとえば、 `foo` `string`タイプに対して有効であり、 `"foo"`として処理されますが、 `"foo"`は`"\"foo\""`として処理されます。                                    |
| `params.required`            | 整数  | リクエストにパラメータが必須かどうかを指定します。サポートされている値は`0` (不要) と`1` (必須) です。デフォルト値は`0`です。                                                                                                                                                                             |
| `params.default`             | 弦   | パラメータのデフォルト値。値が指定したパラメータのタイプと一致していることを確認してください。それ以外の場合、エンドポイントはエラーを返します。                                                                                                                                                                            |
| `params.description`         | 弦   | パラメータの説明。                                                                                                                                                                                                                                           |
| `settings.timeout`           | 整数  | エンドポイントのタイムアウト (ミリ秒単位)。デフォルトでは`30000`です。 `1` ～ `30000`の整数に設定できます。                                                                                                                                                                                   |
| `settings.row_limit`         | 整数  | エンドポイントが操作または返すことができる最大行数。デフォルトでは`1000`です。 `batch_operation`を`0`に設定した場合、 `1`から`2000`までの整数を設定できます。 `batch_operation` `1`に設定した場合、 `1`から`100`までの整数を設定できます。                                                                                             |
| `settings.enable_pagination` | 整数  | リクエストによって返された結果のページネーションを有効にするかどうかを制御します。サポートされている値は`0` (無効) と`1` (有効) です。デフォルト値は`0`です。                                                                                                                                                             |
| `settings.cache_enabled`     | 整数  | 指定された存続時間 (TTL) 期間内に`GET`によって返された応答をキャッシュするかどうかを制御します。サポートされている値は`0` (無効) と`1` (有効) です。デフォルト値は`0`です。                                                                                                                                                |
| `settings.cache_ttl`         | 整数  | `settings.cache_enabled`を`1`に設定した場合の、キャッシュされた応答の存続時間 (TTL) 期間 (秒単位)。 30 ～ 600 の整数に設定できます。TTL 期間中に同じ`GET`リクエストを再度実行すると、Data Service はターゲット データベースからデータを再度フェッチするのではなく、キャッシュされた応答を直接返します。これにより、クエリのパフォーマンスが向上します。                                      |
| `tag`                        | 弦   | エンドポイントのタグ。デフォルト値は`"Default"`です。                                                                                                                                                                                                                    |
| `batch_operation`            | 整数  | エンドポイントがバッチ モードで動作できるようにするかどうかを制御します。サポートされている値は`0` (無効) と`1` (有効) です。 `1`に設定すると、1 つのリクエストで複数の行を操作できます。このオプションを有効にするには、リクエスト メソッドが`POST` 、 `PUT` 、または`DELETE`であることを確認してください。                                                                        |
| `sql_file`                   | 弦   | エンドポイントの SQL ファイル ディレクトリ。たとえば、 `"sql/GET-v1.sql"` 。                                                                                                                                                                                                 |
| `type`                       | 弦   | エンドポイントのタイプ。 `"sql_endpoint"`のみにすることができます。                                                                                                                                                                                                          |
| `return_type`                | 弦   | エンドポイントの応答形式。 `"json"`のみです。                                                                                                                                                                                                                         |

### SQLファイルの構成 {#sql-file-configuration}

エンドポイントの SQL ファイルは、エンドポイントを介してデータをクエリするための SQL ステートメントを指定します。データ アプリのエンドポイント SQL ファイルは`http_endpoints/sql/`ディレクトリにあります。各エンドポイントには、対応する SQL ファイルが必要です。

SQL ファイルの名前は`<method>-<endpoint-path>.sql`形式であり、 `<method>`と`<endpoint-path>`は[`http_endpoints/config.json`](#endpoint-configuration)の`method`と`endpoint`構成と一致する必要があります。

SQL ファイルでは、テーブル結合クエリ、複雑なクエリ、集計関数のステートメントを作成できます。以下は SQL ファイルの例です。

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

SQL ファイルを作成するときは、次の点に注意してください。

-   SQL ファイルの先頭で、SQL ステートメントでデータベースを指定する必要があります。たとえば、 `USE database_name;` 。

-   エンドポイントのパラメーターを定義するには、それを`${variable-name}`のような変数プレースホルダーとして SQL ステートメントに挿入します。

    前の例では、エンドポイントのパラメータとして`${country}`が使用されています。このパラメータを使用すると、エンドポイントのcurlコマンドでクエリを実行する国を指定できます。

    > **注記：**
    >
    > -   パラメータ名では大文字と小文字が区別されます。
    > -   パラメータにテーブル名や列名を指定することはできません。
    > -   SQL ファイル内のパラメータ名は、 [`http_endpoints/config.json`](#endpoint-configuration)で設定したパラメータ名と一致します。
