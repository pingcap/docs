---
title: stage 内のステージ済み ORC ファイルをクエリする
summary: このチュートリアルでは、ORC 形式の Iris データセットをダウンロードし、Amazon S3 バケットにアップロードし、external stage を作成して、ORC ファイルから直接データをクエリする手順を説明します。
---

# stage 内のステージ済み ORC ファイルをクエリする

## 構文 {#syntax}

- [行を Variants としてクエリ](/tidb-cloud-lake/guides/query-stage.md#query-rows-as-variants)
- [名前でカラムをクエリ](/tidb-cloud-lake/guides/query-stage.md#query-columns-by-name)
- [メタデータのクエリ](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## チュートリアル {#tutorial}

このチュートリアルでは、ORC 形式の Iris データセットをダウンロードし、Amazon S3 バケットにアップロードし、external stage を作成して、ORC ファイルから直接データをクエリする手順を説明します。

## ステップ 1: Iris データセットをダウンロードする {#step-1-download-iris-dataset}

<https://github.com/tensorflow/io/raw/master/tests/test_orc/iris.orc> から iris データセットをダウンロードし、その後 Amazon S3 バケットにアップロードします。

iris データセットには、それぞれ 50 個のインスタンスを持つ 3 つのクラスが含まれており、各クラスはアイリス植物の種類を表します。4 つの属性があります: (1) sepal length、(2) sepal width、(3) petal length、(4) petal width。最後のカラムにはクラスラベルが含まれます。

## ステップ 2: External Stage を作成する {#step-2-create-external-stage}

iris データセットファイルが保存されている Amazon S3 バケットを使用して external stage を作成します。

```sql
CREATE STAGE orc_query_stage
    URL = 's3://lake-doc'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-key>'
    );
```

## ステップ 3: ORC ファイルをクエリする {#step-3-query-orc-file}

カラムを指定してクエリします。

```sql
SELECT *
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'
);

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│    sepal_length   │    sepal_width    │    petal_length   │    petal_width    │      species     │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────┤
│               5.1 │               3.5 │               1.4 │               0.2 │ setosa           │
│                 · │                 · │                 · │                 · │ ·                │
│               5.9 │                 3 │               5.1 │               1.8 │ virginica        │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

パス式を使用してクエリします。

```sql
SELECT $1
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'

);
```

リモート ORC ファイルを直接クエリすることもできます。

```sql
SELECT
  *
FROM
  'https://github.com/tensorflow/io/raw/master/tests/test_orc/iris.orc' (file_format => 'orc');
```

## ステップ 4: メタデータ付きでクエリする {#step-4-query-with-metadata}

`METADATA$FILENAME` や `METADATA$FILE_ROW_NUMBER` などのメタデータカラムを含めて、stage から ORC ファイルを直接クエリします。

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    *
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'
);
```