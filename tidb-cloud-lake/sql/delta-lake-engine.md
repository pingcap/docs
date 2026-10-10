---
title: Delta Lake Engine
summary: "{{{ .lake }}} の Delta Lake engine を使用すると、オブジェクトストレージに保存された Delta Lake テーブル内のデータをシームレスにクエリおよび分析できます。{{{ .lake }}} で Delta Lake engine を使用してテーブルを作成する際には、Delta Lake テーブルのデータファイルが保存されている場所を指定します。この設定により、{{{ .lake }}} 内からテーブルに直接アクセスし、シームレスにクエリを実行できます。"
---

# Delta Lake Engine

{{{ .lake }}} の [Delta Lake](https://delta.io/) engine を使用すると、オブジェクトストレージに保存された Delta Lake テーブル内のデータをシームレスにクエリおよび分析できます。{{{ .lake }}} で Delta Lake engine を使用してテーブルを作成する際には、Delta Lake テーブルのデータファイルが保存されている場所を指定します。この設定により、{{{ .lake }}} 内からテーブルに直接アクセスし、シームレスにクエリを実行できます。

- {{{ .lake }}} の Delta Lake engine は現在、読み取り専用の操作のみをサポートしています。これは、Delta Lake テーブルからのデータのクエリはサポートされますが、テーブルへの書き込みはサポートされないことを意味します。
- Delta Lake engine を使用して作成されたテーブルのスキーマは、作成時に設定されます。元の Delta Lake テーブルのスキーマに変更があった場合は、同期を確実にするために、{{{ .lake }}} 内の対応するテーブルを再作成する必要があります。
- {{{ .lake }}} の Delta Lake engine は、公式の [delta-rs](https://github.com/delta-io/delta-rs) ライブラリに基づいて構築されています。Deletion Vector、Change Data Feed、Generated Columns、Identity Columns など、delta-protocol で定義されている一部の機能は、現在この engine ではサポートされていない点に注意してください。

## 構文 {#syntax}

```sql
CREATE TABLE <table_name>
ENGINE = Delta
LOCATION = 's3://<path_to_table>'
CONNECTION_NAME = '<connection_name>'
```

Delta Lake engine を使用してテーブルを作成する前に、S3 ストレージへの接続を確立するために使用する connection オブジェクトを作成する必要があります。{{{ .lake }}} で connection を作成するには、[CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) コマンドを使用します。

## 例 {#examples}

```sql
--Set up connection
CREATE CONNECTION my_s3_conn
STORAGE_TYPE = 's3'
ACCESS_KEY_ID ='your-ak' SECRET_ACCESS_KEY ='your-sk';

-- Create table with Delta Lake engine
CREATE TABLE test_delta
ENGINE = Delta
LOCATION = 's3://testbucket/admin/data/delta/delta-table/'
CONNECTION_NAME = 'my_s3_conn';
```