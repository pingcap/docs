---
title: CREATE FILE FORMAT
summary: 名前付きファイルフォーマットを作成します。
---

# CREATE FILE FORMAT

名前付きファイルフォーマットを作成します。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] FILE FORMAT [ IF NOT EXISTS ] <format_name> FileFormatOptions
```

`FileFormatOptions` の詳細については、[入出力ファイル形式](/tidb-cloud-lake/sql/input-output-file-formats.md) を参照してください。

## ファイルフォーマットを使用する {#use-the-file-format}

一度作成すれば、クエリとロード (load) の両方でフォーマットを再利用できます。

```sql
-- 1) Create a reusable format
CREATE OR REPLACE FILE FORMAT my_custom_csv TYPE = CSV FIELD_DELIMITER = '\t';

-- 2) Query staged files (stage table function syntax uses =>)
SELECT * FROM @mystage/data.csv (FILE_FORMAT => 'my_custom_csv') LIMIT 10;

-- 3) Load staged files with COPY INTO (copy options use =)
COPY INTO my_table
FROM @mystage/data.csv
FILE_FORMAT = (FORMAT_NAME = 'my_custom_csv');
```

なぜ演算子が異なるのでしょうか。stage テーブル関数は `=>` で記述するキー/値パラメータを受け取りますが、`COPY INTO` のオプションでは `=` による標準的な代入を使用します。

**クイックワークフロー: 同じフォーマットで作成、クエリ、ロード**

```sql
-- Create a reusable format
CREATE FILE FORMAT my_parquet TYPE = PARQUET;

-- Query staged files with the format (stage table function syntax uses =>)
SELECT * FROM @sales_stage/2024/order.parquet (FILE_FORMAT => 'my_parquet') LIMIT 10;

-- Load staged files with COPY INTO (copy options use =)
COPY INTO analytics.orders
FROM @sales_stage/2024/order.parquet
FILE_FORMAT = (FORMAT_NAME = 'my_parquet');
```

## LANCE フォーマットに関する注意 {#lance-format-note}

名前付き Lance ファイルフォーマットを作成することもできます。

```sql
CREATE FILE FORMAT my_lance TYPE = LANCE;
```

CSV、TSV、NDJSON、PARQUET とは異なり、名前付き `LANCE` フォーマットは `COPY INTO <location>` でのみ再利用できます。stage テーブルの読み取りや `COPY INTO <table>` ではサポートされません。これは、{{{ .lake}}} が単独のファイルではなく Lance データセットディレクトリを書き出すためです。

```sql
COPY INTO @ml_stage/datasets/train
FROM my_training_table
FILE_FORMAT = (FORMAT_NAME = 'my_lance')
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;
```

Lance 固有の動作と制限事項については、[入力および出力ファイルフォーマット](/tidb-cloud-lake/sql/input-output-file-formats.md#lance-options) および [`COPY INTO <location>`](/tidb-cloud-lake/sql/copy-into-location.md) を参照してください。