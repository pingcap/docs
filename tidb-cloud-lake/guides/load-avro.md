---
title: TiDB Cloud Lake への Avro のロード
summary: Apache Avro™ はレコードデータ向けの代表的なシリアライズ形式であり、ストリーミングデータパイプラインで最初に選ばれる形式です。
---

# TiDB Cloud Lake への Avro のロード

## Avro とは {#what-is-avro}

[Apache Avro™](https://avro.apache.org/) はレコードデータ向けの代表的なシリアライズ形式であり、ストリーミングデータパイプラインで最初に選ばれる形式です。

## Avro ファイルのロード {#loading-avro-file}

AVRO ファイルをロードする一般的な構文は次のとおりです。

```sql
COPY INTO [<database>.]<table_name>
     FROM { internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
FILE_FORMAT = (TYPE = AVRO)
```

- Avro ファイル形式のオプションの詳細については、[Avro ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#avro-options) を参照してください。
- COPY INTO table オプションの詳細については、[COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md) を参照してください。

## チュートリアル: リモート HTTP URL から {{{ .lake }}} に Avro データをロードする {#tutorial-loading-avro-data-into-lake-from-remote-http-url}

このチュートリアルでは、Avro スキーマを使用して {{{ .lake }}} にテーブルを作成し、GitHub でホストされている `.avro` ファイルから HTTPS 経由で Avro データを直接ロードします。

### ステップ 1: Avro スキーマを確認する {#step-1-review-the-avro-schema}

{{{ .lake }}} にテーブルを作成する前に、まず使用する Avro スキーマを簡単に確認しましょう: [userdata.avsc](https://github.com/Teradata/kylo/blob/master/samples/sample-data/avro/userdata.avsc)。このスキーマでは、`User` という名前のレコードが定義されており、13 個のフィールドがあります。大半は string 型で、`int` 型と `float` 型も含まれています。

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "registration_dttm", "type": "string"},
    {"name": "id", "type": "int"},
    {"name": "first_name", "type": "string"},
    {"name": "last_name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "gender", "type": "string"},
    {"name": "ip_address", "type": "string"},
    {"name": "cc", "type": "string"},
    {"name": "country", "type": "string"},
    {"name": "birthdate", "type": "string"},
    {"name": "salary", "type": "float"},
    {"name": "title", "type": "string"},
    {"name": "comments", "type": "string"}
  ]
}
```

### ステップ 2: {{{ .lake }}} にテーブルを作成する {#step-2-create-a-table-in-lake}

スキーマで定義された構造に一致するテーブルを作成します。

```sql
CREATE TABLE userdata (
  registration_dttm STRING,
  id INT,
  first_name STRING,
  last_name STRING,
  email STRING,
  gender STRING,
  ip_address STRING,
  cc VARIANT,
  country STRING,
  birthdate STRING,
  salary FLOAT,
  title STRING,
  comments STRING
);
```

### ステップ 3: リモート HTTPS URL からデータをロードする {#step-3-load-data-from-a-remote-https-url}

```sql
COPY INTO userdata
FROM 'https://raw.githubusercontent.com/Teradata/kylo/master/samples/sample-data/avro/userdata1.avro'
FILE_FORMAT = (type = avro);
```

```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             File                             │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├──────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ Teradata/kylo/master/samples/sample-data/avro/userdata1.avro │        1000 │           0 │ NULL             │             NULL │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### ステップ 4: データをクエリする {#step-4-query-the-data}

これで、インポートしたデータを確認できます。

```sql
SELECT id, first_name, email, salary FROM userdata LIMIT 5;
```

```sql
┌───────────────────────────────────────────────────────────────────────────────────┐
│        id       │    first_name    │           email          │       salary      │
├─────────────────┼──────────────────┼──────────────────────────┼───────────────────┤
│               1 │ Amanda           │ ajordan0@com.com         │          49756.53 │
│               2 │ Albert           │ afreeman1@is.gd          │         150280.17 │
│               3 │ Evelyn           │ emorgan2@altervista.org  │         144972.52 │
│               4 │ Denise           │ driley3@gmpg.org         │          90263.05 │
│               5 │ Carlos           │ cburns4@miitbeian.gov.cn │              NULL │
└───────────────────────────────────────────────────────────────────────────────────┘
```