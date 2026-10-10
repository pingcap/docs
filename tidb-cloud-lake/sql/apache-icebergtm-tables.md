---
title: Apache Iceberg™ Tables
summary: TiDB Cloud Lake を Apache Iceberg カタログに接続し、Iceberg テーブルをクエリまたは書き込む方法を学びます。
---

# Apache Iceberg™ Tables

{{{ .lake }}} は [Apache Iceberg™](https://iceberg.apache.org/) カタログに接続できるため、Fuse テーブルにデータをロードせずに Iceberg テーブルをクエリできます。接続先のカタログが書き込み操作をサポートしている場合は、Iceberg テーブルを作成して書き込むこともできます。

## Iceberg を使用する場合 {#when-to-use-iceberg}

次のような場合は Iceberg を使用します。

- データがすでに Iceberg カタログで管理されている。
- 複数のクエリエンジンで同じテーブルメタデータとオブジェクトストレージを共有する必要がある。
- schema evolution や snapshot などの Iceberg の機能が必要である。
- {{{ .lake }}} から Iceberg テーブルをクエリまたは書き込みたい。

## Iceberg カタログを作成する {#create-an-iceberg-catalog}

Iceberg データベースおよびテーブルにアクセスする前に、カタログを作成します。

### 構文 {#syntax}

```sql
CREATE CATALOG <catalog_name>
TYPE = ICEBERG
CONNECTION = (
    TYPE = '<catalog_type>'
    [ ADDRESS = '<catalog_address>' ]
    [ WAREHOUSE = '<warehouse_location>' ]
    [ "<connection_parameter>" = '<connection_parameter_value>' ]
    ...
);
```

### パラメータ {#parameters}

| パラメータ | 必須 | 説明 |
| --- | --- | --- |
| `<catalog_name>` | はい | {{{ .lake }}} 内のカタログ名。 |
| `TYPE` | はい | カタログエンジン。この値を `ICEBERG` に設定します。 |
| `CONNECTION` | はい | Iceberg カタログおよびそのストレージの接続プロパティ。 |
| `TYPE` inside `CONNECTION` | はい | Iceberg カタログタイプ: `rest`、`glue`、`storage`、または `hive`。 |
| `ADDRESS` | カタログタイプによる | カタログサービスのエンドポイント、または Hive Metastore のアドレス。 |
| `WAREHOUSE` | カタログタイプによる | カタログで使用される Warehouse の場所。 |
| `<connection_parameter>` | カタログタイプによる | カタログ、認証、およびオブジェクトストレージのプロパティ。 |

以下の接続パラメータは、S3 互換ストレージで使用できます。

| 接続パラメータ | 説明 |
| --- | --- |
| `s3.endpoint` | S3 互換サービスのエンドポイント。 |
| `s3.access-key-id` | S3 access key ID。 |
| `s3.secret-access-key` | S3 secret access key。 |
| `s3.session-token` | 一時クレデンシャルとともに使用するセッショントークン。 |
| `s3.region` | S3 リージョン。 |
| `client.region` | クライアントで使用されるリージョン。この値は `s3.region` より優先されます。 |
| `s3.path-style-access` | path-style の S3 アクセスを使用するかどうか。 |
| `s3.sse.type` | サーバー側暗号化のタイプ。 |
| `s3.sse.key` | KMS key ID、または顧客提供の暗号化キー。 |
| `s3.sse.md5` | 顧客提供の暗号化キーに対する MD5 チェックサム。 |
| `client.assume-role.arn` | 引き受ける IAM ロールの ARN。 |
| `client.assume-role.external-id` | IAM ロールを引き受ける際に使用する external ID。 |
| `client.assume-role.session-name` | IAM ロールを引き受ける際に使用するセッション名。 |
| `s3.allow-anonymous` | パブリックストレージへの匿名アクセスを許可するかどうか。 |
| `s3.disable-ec2-metadata` | EC2 インスタンスメタデータからのクレデンシャルを無効にするかどうか。 |
| `s3.disable-config-load` | ローカル設定ソースからのクレデンシャルおよび設定の読み込みを無効にするかどうか。 |

## サポートされるカタログタイプ {#supported-catalog-types}

{{{ .lake }}} は、以下の Iceberg カタログタイプをサポートしています。

| カタログタイプ | `TYPE` 値 | 接続要件 |
| --- | --- | --- |
| REST | `rest` | REST カタログアドレス、Warehouse の場所、およびストレージプロパティ。 |
| AWS Glue | `glue` | Glue リージョンと認証プロパティに加え、S3 ストレージプロパティ。 |
| Storage (Amazon S3 Tables) | `storage` | テーブルバケット ARN と AWS クライアント認証プロパティ。 |
| Hive Metastore | `hive` | Hive Metastore アドレス、Warehouse の場所、およびストレージプロパティ。 |

Storage カタログは、以下の AWS クライアントプロパティをサポートします。

| 接続パラメータ | 説明 |
| --- | --- |
| `table_bucket_arn` | Amazon S3 Tables のテーブルバケットの ARN。 |
| `profile_name` | AWS プロファイル名。 |
| `region_name` | AWS リージョン。 |
| `aws_access_key_id` | AWS access key ID。 |
| `aws_secret_access_key` | AWS secret access key。 |
| `aws_session_token` | 一時クレデンシャルとともに使用する AWS セッショントークン。 |

## Iceberg カタログを管理およびクエリする {#manage-and-query-iceberg-catalogs}

カタログを確認および選択するには、以下のステートメントを使用します。

```sql
SHOW CREATE CATALOG <catalog_name>;
```

```sql
SHOW CATALOGS [ LIKE '<pattern>' | WHERE <expression> ];
```

```sql
USE CATALOG <catalog_name>;
```

詳細は、[SHOW CREATE CATALOG](/tidb-cloud-lake/sql/show-create-catalog.md) および [SHOW CATALOGS](/tidb-cloud-lake/sql/show-catalogs.md) を参照してください。

カタログを選択した後は、標準 SQL を使用してそのテーブルをクエリします。

```sql
SELECT <select_list>
FROM [ <catalog_name>. ]<database_name>.<table_name>
[ WHERE <condition> ];
```

## データ型マッピング {#data-type-mapping}

以下の表は、Iceberg 型から {{{ .lake }}} 型へのサポートされるマッピングを示しています。ここに記載されていない Iceberg 型はサポートされません。

| Apache Iceberg™ | {{{ .lake }}} |
| --- | --- |
| BOOLEAN | [BOOLEAN](/tidb-cloud-lake/sql/boolean.md) |
| INT | [INT32](/tidb-cloud-lake/sql/numeric.md#integer-data-types) |
| LONG | [INT64](/tidb-cloud-lake/sql/numeric.md#integer-data-types) |
| DATE | [DATE](/tidb-cloud-lake/sql/date-time.md) |
| TIMESTAMP / TIMESTAMPZ | [TIMESTAMP](/tidb-cloud-lake/sql/date-time.md) |
| FLOAT | [FLOAT](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) |
| DOUBLE | [DOUBLE](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) |
| STRING / BINARY | [STRING](/tidb-cloud-lake/sql/string.md) |
| DECIMAL | [DECIMAL](/tidb-cloud-lake/sql/decimal.md) |
| LIST | [ARRAY](/tidb-cloud-lake/sql/array.md) |
| MAP | [MAP](/tidb-cloud-lake/sql/map.md) |
| STRUCT | [TUPLE](/tidb-cloud-lake/sql/tuple.md) |

## キャッシュされたメタデータを更新する {#refresh-cached-metadata}

{{{ .lake }}} は、最初のクエリ後に Iceberg カタログのメタデータをキャッシュします。メタデータキャッシュの有効期間はデフォルトで 10 分で、非同期に更新されます。

キャッシュされたメタデータをすぐに更新する必要がある場合は、以下のステートメントを使用します。

```sql
USE CATALOG <catalog_name>;
ALTER DATABASE <database_name> REFRESH CACHE;
ALTER TABLE <database_name>.<table_name> REFRESH CACHE;
```

{{{ .lake }}} は、Iceberg カタログから読み取ったテーブルデータのキャッシュもサポートしています。

## Iceberg テーブルに書き込む {#write-to-iceberg-tables}

書き込み操作をサポートするカタログでは、Iceberg テーブルを作成して書き込むことができます。

### テーブルを作成する {#create-a-table}

```sql
CREATE TABLE [ <database_name>. ]<table_name> (
    <column_name> <data_type> [ , ... ]
)
ENGINE = ICEBERG
[ PARTITION BY ( <column_name> [ , ... ] ) ];
```

| パラメータ | 説明 |
| --- | --- |
| `ENGINE = ICEBERG` | テーブルを Iceberg 形式で保存します。 |
| `PARTITION BY` | 1 つ以上のパーティションカラムを定義します。 |

Iceberg テーブルへの書き込み時には、以下の {{{ .lake }}} データ型がサポートされます。

| {{{ .lake }}} 型 | Apache Iceberg™ 型 |
| --- | --- |
| BOOLEAN | ブール値 |
| INT | 整数 |
| BIGINT | 長整数 |
| FLOAT | 浮動小数点数 |
| DOUBLE | 倍精度浮動小数点数 |
| STRING | 文字列 |
| DATE | 日付 |
| TIMESTAMP | タイムスタンプ |

### データを挿入する {#insert-data}

`INSERT INTO` を使用して Iceberg テーブルに行を書き込みます。

```sql
INSERT INTO [ <database_name>. ]<table_name>
[ ( <column_name> [ , ... ] ) ]
VALUES ( <value> [ , ... ] ) [ , ... ];
```

パーティションテーブルと非パーティションテーブルの両方で、単一行および複数行の挿入をサポートしています。パーティションテーブルの場合、{{{ .lake }}} は行を対応するパーティションにルーティングします。

## Iceberg テーブル関数 {#iceberg-table-functions}

Iceberg メタデータを調査するには、次のテーブル関数を使用します。

- [ICEBERG_MANIFEST](/tidb-cloud-lake/sql/iceberg-manifest.md)
- [ICEBERG_SNAPSHOT](/tidb-cloud-lake/sql/iceberg-snapshot.md)