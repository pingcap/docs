---
title: クエリと変換
summary: "{{{ .lake }}} は、データを最初にテーブルへロードせずに、stage 上のファイルを直接クエリできます。任意の stage タイプ（user、internal、external）のファイル、またはオブジェクトストレージや HTTPS URL を直接クエリできます。ロードの前後におけるデータの確認、検証、変換に最適です。"
---

# クエリと変換

{{{ .lake }}} は、データを最初にテーブルへロード (load) せずに、stage 上のファイルを直接クエリできます。任意の stage タイプ（user、internal、external）のファイル、またはオブジェクトストレージや HTTPS URL を直接クエリできます。ロードの前後におけるデータの確認、検証、変換に最適です。

## 構文 {#syntax}

query only

```sql
SELECT {
    [<alias>.]<column> [, [<alias>.]<column> ...] -- Query columns by name
  | [<alias>.]$<col_position> [, [<alias>.]$<col_position> ...] -- Query columns by position
  | [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] -- Query rows as Variants
}
FROM {@<stage_name>[/<path>] | '<uri>'}  -- stage table function
  [( -- stage table function parameters
    [<connection_parameters>],
    [ PATTERN => '<regex_pattern>'],
    [ FILE_FORMAT => 'CSV | TSV | NDJSON | PARQUET | ORC | Avro | <custom_format_name>'],
    [ FILES => ( '<file_name>' [ , '<file_name>' ... ])],
    [ CASE_SENSITIVE => true | false ]
  )]
  [<alias>]
```

copy with transform

```sql
COPY INTO [<database_name>.]<table_name> [ ( <col_name> [ , <col_name> ... ] ) ]
     FROM (
        SELECT {
            [<alias>.]<column> [, [<alias>.]<column> ...] -- Query columns by name
            | [<alias>.]$<col_position> [, [<alias>.]$<col_position> ...] -- Query columns by position
            | [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] -- Query rows as Variants
            } ]
        FROM {@<stage_name>[/<path>] | '<uri>'}
    )
[ FILES = ( '<file_name>' [ , '<file_name>' ] [ , ... ] ) ]
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO } [ formatTypeOptions ]
       ) ]
[ copyOptions ]
```

> **Note:**
>
> 2 つの構文を比較すると、次のとおりです。
>
> - 同じ `Select List`
> - 同じ `FROM {@<stage_name>[/<path>] | '<uri>'}`
> - 異なるパラメータ:
>     - query では `table function parameters`、つまり `(<key> => <value>, ...)` を使用します
>     - transform では [Copy into table](/tidb-cloud-lake/sql/copy-into-table.md) の末尾にある Options を使用します

## FROM 句 {#from-clause}

FROM 句は `Table Function` と似た構文を使用します。通常のテーブルと同様に、他のテーブルと join する際にはテーブル `alias` を使用できます。

table function parameters:

| パラメータ | 説明 |
|-------------------------|---------------------------------------------------------|
| `FILE_FORMAT`           | ファイル形式のタイプ (CSV, TSV, NDJSON, PARQUET, ORC, Avro) |
| `PATTERN`               | ファイルを絞り込むための正規表現パターン |
| `FILES`                 | クエリ対象とするファイルの明示的なリスト |
| `CASE_SENSITIVE`        | カラム名の大文字・小文字の区別 (Parquet のみ) |
| `connection_parameters` | 外部ストレージ接続の詳細 |

## ファイルデータのクエリ {#query-file-data}

select list は 3 つの構文をサポートしており、使用できるのはそのうち 1 つだけです。混在させることはできません。

### 行を Variants としてクエリ {#query-rows-as-variants}

- サポートされるファイル形式: NDJSON, AVRO, Parquet, ORC

> **Note:**
>
> 現在、Parquet と ORC では、`Query rows as Variants` は `Query columns by name` より低速であり、この 2 つの方法を混在して使用することはできません。

syntax:

```sql
SELECT [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] <FROM Clause>
```

- 例: `SELECT $1:id, $1:name FROM ...`
- テーブルスキーマ: ($1: Variant)。つまり、Variant Object Type の単一カラムで、各 Variant が行全体を表します
- 注意:
    - `$1:column` のようなパス式の型も Variant です。式で使用したり、宛先テーブルのカラムへロードしたりする際にはネイティブ型へ自動キャストできますが、型固有の操作では、意味をより明確にするために事前に手動でキャストしたい場合があります（例: `CAST($1:id AS INT)`）。

### 名前でカラムをクエリ {#query-columns-by-name}

- サポートされるファイル形式: NDJSON, AVRO, Parquet, ORC

```sql
SELECT [<alias>.]<column> [, [<alias>.]<column>  ...] <FROM Clause>
```

- 例: `SELECT id, name FROM ...`
- テーブルスキーマ: Parquet または ORC ファイルスキーマからマッピングされたカラム
- 注意:
    - すべてのファイルは同じ Parquet/ORC スキーマを持っている必要があります。そうでない場合はエラーが返されます

### 位置でカラムをクエリ {#query-columns-by-position}

- サポートされるファイル形式: CSV, TSV

```sql
SELECT [<alias>.]$<col_position>[, [<alias>.]$<col_position>,  ...] <FROM Clause>
```

- 例: `SELECT $1, $2 FROM ...`
- テーブルスキーマ: 型 `VARCHAR NULL` のカラム
- 注意
    - `<col_position>` は 1 から始まります

## メタデータのクエリ {#query-metadata}

クエリにはファイルメタデータを含めることもできます。これは、データリネージの追跡やデバッグに役立ちます。

```sql
SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER, $1, <FROM Clause>
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson'
);
```

サポートされるファイル形式では、次のファイルレベルのメタデータフィールドを利用できます。

| ファイルメタデータ | 型 | 説明 |
| -------------------------- | ------- |--------------------------------------------------|
| `METADATA$FILENAME`        | VARCHAR | 行が読み取られたファイルのパス |
| `METADATA$FILE_ROW_NUMBER` | INT     | ファイル内の行番号 (0 から開始) |

**ユースケース:**

- **データリネージ**: 各レコードに寄与したソースファイルを追跡する
- **デバッグ**: ファイル名と行番号で問題のあるレコードを特定する
- **増分処理**: 特定のファイル、またはファイル内の特定範囲のみを処理する

## ファイル形式別チュートリアル {#tutorials-by-file-formats}

- [Parquet ファイルのクエリ](/tidb-cloud-lake/guides/query-parquet-files-in-stage.md)
- [ORC ファイルのクエリ](/tidb-cloud-lake/guides/query-staged-orc-files-in-stage.md)
- [NDJSON ファイルのクエリ](/tidb-cloud-lake/guides/query-ndjson-files-in-stage.md)
- [Avro ファイルのクエリ](/tidb-cloud-lake/guides/query-avro-files-in-stage.md)
- [CSV ファイルのクエリ](/tidb-cloud-lake/guides/query-csv-files-in-stage.md)
- [TSV ファイルのクエリ](/tidb-cloud-lake/guides/query-tsv-files-in-stage.md)

## Schema Evolution {#schema-evolution}

- [Schema Evolution](/tidb-cloud-lake/guides/schema-evolution.md): スキーマが変化する Parquet ファイルをロードする際に、新しいカラムをテーブルへ自動的に追加します。