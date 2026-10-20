---
title: PostgreSQL データ型
summary: PostgreSQL互換の TiDB Cloud Starter でサポートされる PostgreSQL 互換データ型について説明します。
---

# PostgreSQL データ型

PostgreSQL互換の {{{ .starter }}} は、数値、テキスト、バイナリ、日付と時刻、JSON、配列、ベクトル、および全文検索のワークロード向けに、一般的な PostgreSQL データ型をサポートしています。

## サポートされるデータ型 {#supported-data-types}

以下のデータ型がサポートされています。

| データ型 | エイリアス | 説明 |
| --- | --- | --- |
| `BOOLEAN` | `BOOL` | 真偽値。 |
| `INTEGER` | `INT`, `INT4` | 4 バイトの符号付き整数。 |
| `BIGINT` | `INT8` | 8 バイトの符号付き整数。 |
| `DOUBLE PRECISION` | `FLOAT8` | 8 バイトの IEEE 754 浮動小数点数。 |
| `NUMERIC` | `NUMERIC(p,s)`, `DECIMAL` | 96 ビットの係数と最大 28 桁の小数部を持つ正確な数値。 |
| `TEXT` | - | 可変長 UTF-8 テキスト。 |
| `VARCHAR(n)` | `CHARACTER VARYING(n)` | 最大 `n` 文字の可変長テキスト。 |
| `BYTEA` | - | バイナリデータ。 |
| `TIMESTAMP` | `TIMESTAMP WITHOUT TIME ZONE` | タイムゾーンなしの日付と時刻。 |
| `TIMESTAMPTZ` | `TIMESTAMP WITH TIME ZONE` | タイムゾーンのセマンティクスを持つ日付と時刻。 |
| `DATE` | - | 暦日。 |
| `TIME` | `TIME WITHOUT TIME ZONE` | 時刻。 |
| `INTERVAL` | - | 時間間隔。 |
| `UUID` | - | 128 ビットの UUID 値。 |
| `INET` | - | IPv4 または IPv6 のホストまたはネットワークアドレス。 |
| `JSON` | - | 入力テキスト表現を保持する JSON データ。 |
| `JSONB` | - | 正規化された表現で格納される JSON データ。 |
| `SERIAL` | - | シーケンスによって支えられる自動増分の 4 バイト整数。 |
| `BIGSERIAL` | - | シーケンスによって支えられる自動増分の 8 バイト整数。 |
| `type[]` | - | サポートされるデータ型の配列。 |
| `VECTOR(n)` | - | ベクトル検索用の固定次元の密ベクトル。 |
| `TSVECTOR` | - | 全文検索ドキュメント表現。 |
| `TSQUERY` | - | 全文検索クエリ表現。 |
| `NAME` | - | システムカタログで使用される PostgreSQL 互換の識別子型。 |

以下の PostgreSQL データ型も受け付けられますが、互換性の違いがあります。

- `SMALLINT` と `INT2`: 内部的には `INTEGER` として格納されます。PostgreSQL の `SMALLINT` の範囲は適用されません。
- `REAL` と `FLOAT4`: PostgreSQL の単精度浮動小数点のセマンティクスを持たず、内部的には `DOUBLE PRECISION` として格納されます。
- `CHAR(n)` と `CHARACTER(n)`: PostgreSQL の固定長の空白埋めのセマンティクスを持たず、内部的には `VARCHAR` として格納されます。

## 数値型 {#numeric-types}

整数値には `INTEGER` または `BIGINT` を使用します。

```sql
CREATE TABLE counters (
    id BIGSERIAL PRIMARY KEY,
    count INTEGER NOT NULL,
    total BIGINT
);
```

正確な 10 進値が必要な場合は `NUMERIC` を使用します。

```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    price NUMERIC(10, 2)
);
```

PostgreSQL互換の {{{ .starter }}} は、`NUMERIC` 値を 96 ビットの係数で格納します。これにより、およそ 28～29 桁の有効 10 進数を保持できます。小数点の位置は、最大 28 桁の小数部を持てるように設定できます。

より大きい精度またはスケールを宣言した場合でも、以下の制限が適用されます。

- `NUMERIC(38,0)` では 38 桁の整数を格納できません。サポートされる最大の整数は `79228162514264337593543950335` であり、これより大きい整数は格納できません。
- 宣言したスケールが 28 を超えても、28 桁を超える小数部は保持されません。たとえば、`NUMERIC(60,35)` カラムに `0.12345678901234567890123456789012345` を格納すると、`0.1234567890123456789012345679` に丸められます。

PostgreSQL からデータを移行する前に、数値がサポート範囲内にあることを確認してください。

浮動小数点値には `DOUBLE PRECISION` を使用します。

```sql
CREATE TABLE measurements (
    id BIGSERIAL PRIMARY KEY,
    value DOUBLE PRECISION
);
```

## 文字型とバイナリ型 {#character-and-binary-types}

可変長テキストには `TEXT` を使用します。

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    title TEXT,
    body TEXT
);
```

最大文字数を制限したい場合は `VARCHAR(n)` を使用します。

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL
);
```

バイナリデータを格納するには `BYTEA` を使用します。

```sql
CREATE TABLE files (
    id BIGSERIAL PRIMARY KEY,
    content BYTEA
);
```

## 日付と時刻の型 {#date-and-time-types}

PostgreSQL互換の {{{ .starter }}} は、`DATE`、`TIME`、`TIMESTAMP`、`TIMESTAMPTZ`、および `INTERVAL` をサポートしています。

例:

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_date DATE,
    start_time TIME,
    created_at TIMESTAMP,
    published_at TIMESTAMPTZ,
    duration INTERVAL
);
```

必要に応じて PostgreSQL の型付きリテラルを使用します。

```sql
SELECT
    DATE '2026-09-19',
    TIME '15:30:00',
    TIMESTAMP '2026-09-19 15:30:00',
    TIMESTAMPTZ '2026-09-19 15:30:00+00',
    INTERVAL '2 hours';
```

### タイムスタンプ精度 {#timestamp-precision}

タイムスタンプはマイクロ秒精度で格納されます。

型構文では 0 から 6 までの精度パラメータを受け付けますが、格納される小数秒は切り捨てられません。

たとえば、`TIMESTAMP(3)` でも小数部 6 桁を保持できます。

## 時間間隔の演算 {#interval-operations}

時間間隔は、月ベースの成分と月未満の成分を別々に保持するため、カレンダーを考慮した日付演算が可能です。

時間間隔に対して加算、減算、乗算、除算を実行できます。

```sql
SELECT
    INTERVAL '1 day' * 2 AS two_days,
    2 * INTERVAL '1 day' AS two_days_again,
    INTERVAL '1 day' / 2 AS half_day,
    INTERVAL '1 day' + INTERVAL '1 hour' AS day_and_hour,
    INTERVAL '3 days' - INTERVAL '1 day' AS two_days,
    INTERVAL '0 day' - INTERVAL '1 day' AS negative_day,
    NOW() - 7 * INTERVAL '1 day' AS one_week_ago;
```

## UUID {#uuid}

128 ビットの UUID 値を格納するには `UUID` を使用します。

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id BIGINT NOT NULL
);
```

## INET {#inet}

IPv4 または IPv6 のホストアドレスやネットワークアドレスを格納するには、`INET` を使用します。

```sql
CREATE TABLE access_log (
    id BIGSERIAL PRIMARY KEY,
    client_ip INET
);
```

例:

```sql
INSERT INTO access_log (client_ip)
VALUES
    ('192.168.1.10'),
    ('10.0.0.0/8'),
    ('::1');
```

等価比較と順序比較がサポートされています。一部の PostgreSQL ネットワーク演算子および関数はサポートされていません。[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。

## JSON と JSONB {#json-and-jsonb}

元の JSON テキスト表現を保持することが重要な場合は、`JSON` を使用します。正規化された表現や JSON の包含などの操作には、`JSONB` を使用します。

例:

```sql
CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    settings JSONB
);

INSERT INTO profiles (settings)
VALUES ('{"theme":"dark","notifications":true}');

SELECT *
FROM profiles
WHERE settings @> '{"theme":"dark"}';
```

## 配列 {#arrays}

配列を定義するには、`type[]` を使用します。

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    tags TEXT[]
);
```

配列の値を挿入してアクセスします。

```sql
INSERT INTO articles (tags)
VALUES (ARRAY['database', 'cloud', 'postgresql']);

SELECT tags[1]
FROM articles;
```

## ベクトル型と全文検索型 {#vector-and-full-text-search-types}

ベクトル検索には `VECTOR(n)` を使用できます。

```sql
CREATE TABLE embeddings (
    id BIGSERIAL PRIMARY KEY,
    embedding VECTOR(3)
);
```

ベクトル演算子と HNSW インデックスについては、[ベクトル検索](/tidb-cloud/starter/pg-vector-search.md) を参照してください。

PostgreSQL 互換の全文検索には、`TSVECTOR` と `TSQUERY` を使用できます。

```sql
SELECT
    to_tsvector('simple', 'PostgreSQL full text search')
    @@ plainto_tsquery('simple', 'PostgreSQL');
```

詳細は、[全文検索](/tidb-cloud/starter/pg-full-text-search.md) を参照してください。

## 暗黙的な型変換 {#type-coercion}

PostgreSQL 互換の {{{ .starter }}} は、一般的な SQL コンテキストで PostgreSQL スタイルの暗黙的な型変換をサポートしています。

### `UNION`、`CASE`、`COALESCE`、`VALUES` {#union-case-coalesce-and-values}

テキストが別の型付きの値と組み合わされると、式はテキスト型に解決されることがあります。

例:

```sql
SELECT 1
UNION
SELECT 'a';
```

### 比較 {#comparisons}

テキストリテラルが型付きの値と比較される場合、可能であれば、そのテキストリテラルはもう一方のオペランドの型に暗黙的に変換されます。

例:

```sql
CREATE TABLE example (
    id INTEGER PRIMARY KEY
);

SELECT *
FROM example
WHERE id = '42';
```

この例では、`'42'` は `INTEGER` に暗黙的に変換されます。

### 数値型の昇格 {#numeric-type-promotion}

数値型が組み合わされると、結果は次の一般的な優先順位に従って昇格されます。

```text
INTEGER -> BIGINT -> DOUBLE PRECISION -> NUMERIC
```

PostgreSQL とは異なり、`DOUBLE PRECISION` と `NUMERIC` を組み合わせると、結果は `NUMERIC` になります。例:

```sql
SELECT pg_typeof(1::double precision + 2::numeric);
```

このクエリは `numeric` を返します。

アプリケーションで `DOUBLE PRECISION` の結果が必要な場合は、`NUMERIC` オペランドを明示的に `DOUBLE PRECISION` にキャストしてください。

### 時間型の昇格 {#temporal-type-promotion}

一般的な時間型の式は、次のように昇格されます。

| 式の型 | 結果の型 |
| --- | --- |
| `DATE` と `TIMESTAMP` | `TIMESTAMP` |
| `TIMESTAMP` と `TIMESTAMPTZ` | `TIMESTAMPTZ` |
| `DATE` と `TIMESTAMPTZ` | `TIMESTAMPTZ` |

## 型キャスト {#type-casts}

PostgreSQL のキャスト構文は、次のいずれかを使用します。

```sql
SELECT CAST('42' AS INTEGER);
SELECT '42'::INTEGER;
```

明示的なキャストは、代入キャストや暗黙的なキャストよりも許容範囲が広くなります。たとえば、明示的なキャストでは、`INSERT` や `UPDATE` の代入では拒否される一部の変換を実行できます。