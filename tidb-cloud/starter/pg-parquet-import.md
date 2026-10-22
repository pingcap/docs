---
title: Parquet データをインポートする
summary: PostgreSQL 互換の TiDB Cloud Starter に Parquet データをクエリおよびインポートする方法を学びます。
---

# Parquet データをインポートする

PostgreSQL 互換の {{{ .starter }}} は、Parquet データの読み取りと SQL テーブルへのインポートのために `parquet` 拡張機能をサポートしています。

> **Note:**
>
> PostgreSQL 互換の {{{ .starter }}} は現在パブリックプレビューです。

このドキュメントでは、HTTP または HTTPS URL 経由での Parquet アクセスについて説明します。ソース URL は TiDB Cloud から到達可能である必要があります。

## `parquet` 拡張機能を有効にする {#enable-the-parquet-extension}

対象のデータベースで拡張機能を有効にします。

```sql
CREATE EXTENSION IF NOT EXISTS parquet;
```

## Parquet ファイルをクエリする {#query-a-parquet-file}

スキーマ修飾された `extensions.read_parquet()` テーブル関数を使用して、Parquet ファイルを直接クエリします。

```sql
SELECT *
FROM extensions.read_parquet('https://example.com/data.parquet');
```

たとえば、行数をカウントするには次のようにします。

```sql
SELECT count(*)
FROM extensions.read_parquet('https://example.com/data.parquet');
```

> **Note:**
>
> `read_parquet()` は `extensions.read_parquet()` としてスキーマ修飾する必要があります。

## Parquet データをテーブルにインポートする {#import-parquet-data-into-a-table}

`COPY ... WITH (FORMAT parquet)` を使用して、Parquet データを既存のテーブルにインポートします。

例:

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP
);

COPY users
FROM 'https://example.com/users.parquet'
WITH (FORMAT parquet);
```

カラムは大文字と小文字を区別せずに名前で照合されます。

- 対象テーブルに一致するカラムがない Parquet カラムは無視されます。
- 一致する Parquet カラムがない対象テーブルのカラムには、対象カラムの制約に従って `NULL` が設定されます。

## 型マッピング {#type-mapping}

以下の一般的な Parquet 型は、PostgreSQL 互換の型にマッピングされます。

| Parquet 型 | PostgreSQL 型 |
| --- | --- |
| `BOOLEAN` | `BOOLEAN` |
| `INT32` | `INTEGER` |
| `INT64` | `BIGINT` |
| `FLOAT` | `DOUBLE PRECISION` |
| `DOUBLE` | `DOUBLE PRECISION` |
| UTF-8 アノテーション付き `BYTE_ARRAY` | `TEXT` |
| バイナリ `BYTE_ARRAY` | `BYTEA` |
| `INT96` タイムスタンプ | `TIMESTAMP` |
| `DATE` 論理型 | `DATE` |
| `TIME` 論理型 | サポートされていません |
| `TIMESTAMP` 論理型 | `TIMESTAMP` |
| `DECIMAL` 論理型 | `NUMERIC`、精度が最大 28 の Decimal128 に限定 |

データをインポートする前に、Parquet スキーマが対象テーブルのスキーマと互換性があることを確認してください。

## サポートされる Parquet 形式 {#supported-parquet-formats}

以下の Parquet 形式がサポートされています。

| 項目 | サポートされる値 |
| --- | --- |
| Parquet バージョン | v1 および v2 |
| 圧縮コーデック | Snappy、Gzip、Zstd、および非圧縮 |
| リモート URL スキーム | HTTP および HTTPS |

## 制限事項 {#limitations}

パブリックプレビュー期間中は、以下の制限があります。

- `COPY ... WITH (FORMAT parquet)` を実行する前に、対象テーブルが存在している必要があります。
- TiDB Cloud から到達可能な HTTP または HTTPS URL を使用してください。
- インポート前に Parquet のカラム型を確認してください。一部の互換性のない型の組み合わせは、インポート中に拒否されない場合があります。
- `extensions.read_parquet()` は `extensions` スキーマ修飾子付きで呼び出す必要があります。
- リモートリクエストには、接続タイムアウトおよびリクエストタイムアウトが適用されます。