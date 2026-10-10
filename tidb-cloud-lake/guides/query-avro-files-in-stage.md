---
title: stage 内の Avro ファイルのクエリ
summary: "{{{ .lake }}} は、stage から直接 Avro ファイルをクエリするための包括的なサポートを提供します。これにより、データを最初にテーブルへロードすることなく、柔軟にデータの探索や変換を行えます。"
---

# stage 内の Avro ファイルのクエリ

## 構文 {#syntax}

- [行を Variants としてクエリ](/tidb-cloud-lake/guides/query-stage.md#query-rows-as-variants)
- [メタデータのクエリ](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## Avro クエリ機能の概要 {#avro-querying-features-overview}

{{{ .lake }}} は、stage から直接 Avro ファイルをクエリするための包括的なサポートを提供します。これにより、データを最初にテーブルへロードすることなく、柔軟にデータの探索や変換を行えます。

* **Variant 表現**: Avro ファイル内の各行は variant として扱われ、`$1` で参照されます。これにより、Avro データ内のネストされた構造へ柔軟にアクセスできます。
* **型マッピング**: 各 Avro 型は、{{{ .lake }}} 内の対応する variant 型にマッピングされます。
* **メタデータアクセス**: `METADATA$FILENAME` や `METADATA$FILE_ROW_NUMBER` のようなメタデータカラムにアクセスして、ソースファイルや行に関する追加のコンテキストを取得できます。

## チュートリアル {#tutorial}

このチュートリアルでは、stage に保存された Avro ファイルをクエリする方法を示します。

### ステップ 1. Avro ファイルを準備する {#step-1-prepare-an-avro-file}

次のスキーマを持つ `user` という名前の Avro ファイルを考えます。

```json
{
  "type": "record",
  "name": "user",
  "fields": [
    {
      "name": "id",
      "type": "long"
    },
    {
      "name": "name",
      "type": "string"
    }
  ]
}
```

### ステップ 2. 外部 stage を作成する {#step-2-create-an-external-stage}

Avro ファイルが保存されている独自の S3 バケットと認証情報を使用して、外部 stage を作成します。

```sql
CREATE STAGE avro_query_stage
URL = 's3://load/avro/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### ステップ 3. Avro ファイルをクエリする {#step-3-query-avro-files}

#### 基本的なクエリ {#basic-query}

stage から直接 Avro ファイルをクエリします。

```sql
SELECT
    CAST($1:id AS INT) AS id,
    $1:name AS name
FROM @avro_query_stage
(
    FILE_FORMAT => 'AVRO',
    PATTERN => '.*[.]avro'
);
```

### メタデータ付きでクエリする {#query-with-metadata}

`METADATA$FILENAME` や `METADATA$FILE_ROW_NUMBER` のようなメタデータカラムを含めて、stage から直接 Avro ファイルをクエリします。

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    CAST($1:id AS INT) AS id,
    $1:name AS name
FROM @avro_query_stage
(
    FILE_FORMAT => 'AVRO',
    PATTERN => '.*[.]avro'
);
```

## Variant への型マッピング {#type-mapping-to-variant}

{{{ .lake }}} の Variant は JSONB として保存されます。ほとんどの Avro 型はそのままマッピングされますが、いくつか特別な考慮事項があります。

* **時刻型**: `TimeMillis` と `TimeMicros` は、JSONB にネイティブな Time 型がないため、`INT64` にマッピングされます。これらの値を処理する際は、元の型を認識しておく必要があります。
* **Decimal 型**: Decimal は `DECIMAL128` または `DECIMAL256` としてロードされます。精度がサポートされる上限を超える場合、エラーが発生することがあります。
* **Enum 型**: Avro の `ENUM` 型は、{{{ .lake }}} では `STRING` 値にマッピングされます。