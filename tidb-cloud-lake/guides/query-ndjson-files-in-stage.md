---
title: stage 内の NDJSON ファイルをクエリする
summary: "{{{ .lake }}} では、stage に保存された NDJSON ファイルを、データをテーブルにロードする前に直接クエリできます。この方法は、データ探索、ETL 処理、アドホック分析のシナリオで特に有用です。"
---

# stage 内の NDJSON ファイルをクエリする

{{{ .lake }}} では、stage に保存された NDJSON ファイルを、データをテーブルにロードする前に直接クエリできます。この方法は、データ探索、ETL 処理、アドホック分析のシナリオで特に有用です。

## NDJSON とは何ですか？ {#what-is-ndjson}

NDJSON (Newline Delimited JSON) は、各行に完全で有効な JSON オブジェクトが 1 つ含まれる JSON ベースのファイル形式です。この形式は、ストリーミングデータ処理やビッグデータ分析に特に適しています。

**NDJSON ファイル内容の例:**

```json
{"id": 1, "title": "Database Fundamentals", "author": "John Doe", "price": 45.50, "category": "Technology"}
{"id": 2, "title": "Machine Learning in Practice", "author": "Jane Smith", "price": 68.00, "category": "AI"}
{"id": 3, "title": "Web Development Guide", "author": "Mike Johnson", "price": 52.30, "category": "Frontend"}
```

**NDJSON の利点:**

- **ストリーム向き**: ファイル全体をメモリにロードせずに、行単位で解析できます
- **ビッグデータ互換**: ログファイル、データエクスポート、ETL パイプラインで広く使用されています
- **処理が容易**: 各行が独立した JSON オブジェクトであるため、並列処理が可能です

## 構文 {#syntax}

- [行を Variants としてクエリ](/tidb-cloud-lake/guides/query-stage.md#query-rows-as-variants)
- [メタデータのクエリ](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## チュートリアル {#tutorial}

### Step 1. 外部 stage を作成する {#step-1-create-an-external-stage}

NDJSON ファイルが保存されている独自の S3 バケットと認証情報を使用して、外部 stage を作成します。

```sql
CREATE STAGE ndjson_query_stage
URL = 's3://load/ndjson/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. カスタム NDJSON ファイル形式を作成する {#step-2-create-custom-ndjson-file-format}

```sql
CREATE FILE FORMAT ndjson_query_format
    TYPE = NDJSON,
    COMPRESSION = AUTO;
```

- NDJSON ファイル形式のその他のオプションについては、[NDJSON ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#ndjson-options) を参照してください

### Step 3. NDJSON ファイルをクエリする {#step-3-query-ndjson-files}

これで、stage から NDJSON ファイルを直接クエリできます。この例では、各 JSON オブジェクトから `title` フィールドと `author` フィールドを抽出します。

```sql
SELECT $1:title, $1:author
FROM @ndjson_query_stage
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson'
);
```

**説明:**

- `$1:title` と `$1:author`: JSON オブジェクトから特定のフィールドを抽出します。`$1` は JSON オブジェクト全体を variant として表し、`:field_name` で個々のフィールドにアクセスします
- `@ndjson_query_stage`: Step 1 で作成した外部 stage を参照します
- `FILE_FORMAT => 'ndjson_query_format'`: Step 2 で定義したカスタムファイル形式を使用します
- `PATTERN => '.*[.]ndjson'`: `.ndjson` で終わるすべてのファイルに一致する正規表現パターンです

### 圧縮ファイルをクエリする {#querying-compressed-files}

NDJSON ファイルが gzip で圧縮されている場合は、圧縮ファイルに一致するようにパターンを変更します。

```sql
SELECT $1:title, $1:author
FROM @ndjson_query_stage
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson[.]gz'
);
```

**主な違い:** `.*[.]ndjson[.]gz` パターンは、`.ndjson.gz` で終わるファイルに一致します。ファイル形式の `COMPRESSION = AUTO` 設定により、{{{ .lake }}} はクエリ実行中に gzip ファイルを自動的に展開します。

## 関連ドキュメント {#related-documentation}

- [NDJSON ファイルをロードする](/tidb-cloud-lake/guides/load-ndjson.md) - NDJSON データをテーブルにロードする方法
- [NDJSON ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#ndjson-options) - NDJSON 形式の完全な設定
- [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) - 外部 stage と内部 stage の管理