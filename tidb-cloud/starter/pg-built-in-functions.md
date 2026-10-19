---
title: PostgreSQL 組み込み関数
summary: PostgreSQL 互換の TiDB Cloud Starter でサポートされる組み込み関数について説明します。
---

# PostgreSQL 組み込み関数

PostgreSQL 互換の {{{ .starter }}} では、文字列、数値、日付と時刻、集計、ウィンドウ、JSON、配列、正規表現、シーケンス、およびシステム操作でよく使われる組み込み関数を提供しています。

## 文字列関数 {#string-functions}

以下の一般的な文字列関数がサポートされています。

| 関数 | 説明 |
| --- | --- |
| `UPPER(text)` | テキストを大文字に変換します。 |
| `LOWER(text)` | テキストを小文字に変換します。 |
| `LENGTH(text)` | 文字数を返します。 |
| `CHAR_LENGTH(text)` | 文字数を返します。 |
| `LEFT(text, n)` | 先頭から `n` 文字を返します。 |
| `RIGHT(text, n)` | 末尾から `n` 文字を返します。 |
| `TRIM(text)` | 先頭と末尾の空白または指定した文字を削除します。 |
| `BTRIM(text [, chars])` | 両端から文字を削除します。 |
| `LTRIM(text [, chars])` | 左側から文字を削除します。 |
| `RTRIM(text [, chars])` | 右側から文字を削除します。 |
| `LPAD(text, length [, fill])` | テキストの左側を埋めます。 |
| `RPAD(text, length [, fill])` | テキストの右側を埋めます。 |
| `REPEAT(text, n)` | 文字列を繰り返します。 |
| `REVERSE(text)` | 文字列を逆順にします。 |
| `INITCAP(text)` | 各単語の先頭文字を大文字に変換します。 |
| `ASCII(text)` | 先頭文字の文字コードを返します。 |
| `CHR(int)` | 文字コードに対応する文字を返します。 |
| `STRPOS(text, substring)` | 部分文字列の位置を 1 始まりで返します。 |
| `POSITION(substring IN text)` | `STRPOS` の SQL 標準形式です。 |
| `SPLIT_PART(text, delimiter, field)` | テキストを分割し、そのうち 1 つのフィールドを返します。 |
| `TRANSLATE(text, from, to)` | 個々の文字を置換します。 |
| `OVERLAY(...)` | 文字列の一部を置換します。 |
| `STARTS_WITH(text, prefix)` | テキストが指定した接頭辞で始まるかどうかを確認します。 |
| `CONCAT(...)` | 値を連結し、`NULL` 引数は無視します。 |
| `CONCAT_WS(separator, ...)` | 区切り文字を使って値を連結します。 |
| `SUBSTRING(...)` | 部分文字列を抽出します。 |
| `REPLACE(text, from, to)` | 部分文字列の出現箇所を置換します。 |
| `FORMAT(format, ...)` | PostgreSQL スタイルの書式指定子を使って文字列を整形します。 |
| `QUOTE_IDENT(text)` | 必要に応じて SQL 識別子を引用符で囲みます。 |
| `QUOTE_LITERAL(text)` | SQL リテラルを引用符で囲みます。 |
| `QUOTE_NULLABLE(text)` | SQL リテラルを引用符で囲み、入力が null の場合は文字列 `NULL` を返します。 |

例:

```sql
SELECT
    UPPER('hello') AS upper_text,
    LENGTH('PostgreSQL') AS text_length,
    CONCAT_WS('-', '2026', '09', '19') AS date_text,
    SPLIT_PART('a,b,c', ',', 2) AS second_part;
```

## 数学関数 {#mathematical-functions}

以下の一般的な数学関数がサポートされています。

| 関数 | 説明 |
| --- | --- |
| `ABS(x)` | 絶対値を返します。 |
| `CEIL(x)` / `CEILING(x)` | 最も近い整数に切り上げます。 |
| `FLOOR(x)` | 最も近い整数に切り下げます。 |
| `ROUND(x [, scale])` | 数値を丸めます。 |
| `TRUNC(x [, scale])` | 数値を切り捨てます。 |
| `SQRT(x)` | 平方根を返します。 |
| `CBRT(x)` | 立方根を返します。 |
| `POWER(x, y)` | `x` の `y` 乗を返します。 |
| `EXP(x)` | 指数関数の値を返します。 |
| `LN(x)` | 自然対数を返します。 |
| `LOG(x)` | 対数を返します。 |
| `MOD(x, y)` | 余りを返します。 |
| `SIGN(x)` | 数値の符号を返します。 |

例:

```sql
SELECT
    ABS(-42),
    ROUND(4.567, 2),
    SQRT(16),
    POWER(2, 8);
```

## 日付と時刻の関数 {#date-and-time-functions}

以下の一般的な日付・時刻関数および式がサポートされています。

| 関数または式 | 説明 |
| --- | --- |
| `CURRENT_DATE` | 現在の日付を返します。 |
| `CURRENT_TIME` | 現在の時刻を返します。 |
| `CURRENT_TIMESTAMP` | 現在のタイムスタンプを返します。 |
| `LOCALTIME` | 現在のローカル時刻を返します。 |
| `LOCALTIMESTAMP` | 現在のローカルタイムスタンプを返します。 |
| `NOW()` | 現在のトランザクションのタイムスタンプを返します。 |
| `DATE_TRUNC(field, value)` | 日付またはタイムスタンプを指定した単位で切り詰めます。 |
| `DATE_PART(field, value)` | 日付または時刻の 1 つのフィールドを抽出します。 |
| `EXTRACT(field FROM value)` | 日付または時刻のフィールドを抽出するための SQL 標準形式です。 |
| `AGE(timestamp [, timestamp])` | タイムスタンプ間の記号的な間隔を返します。 |
| `MAKE_DATE(year, month, day)` | 日付を構築します。 |
| `MAKE_INTERVAL(...)` | 間隔を構築します。 |

例:

```sql
SELECT
    CURRENT_DATE,
    NOW(),
    DATE_TRUNC('day', NOW()),
    EXTRACT(YEAR FROM CURRENT_DATE);
```

`INTERVAL` を使った日付・時刻の演算もサポートされています。

```sql
SELECT NOW() - INTERVAL '7 days';
```

## サンプルデータのセットアップ {#set-up-sample-data}

以降のセクションの一部の例では、サンプルテーブルをクエリします。これらの例を実行する前に、必要なテーブルを作成し、サンプルデータをテストデータベースに挿入してください。

このページのテーブル定義は、他の例で使用されているものとは異なります。テストデータベースにすでに以下の名前のテーブルが存在する場合は、このページ用に別のテストデータベースを使用してください。

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    nickname TEXT,
    active BOOLEAN,
    score INTEGER
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary NUMERIC
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    created_at TIMESTAMP
);

CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    settings JSONB
);

INSERT INTO users (id, name, nickname, active, score) VALUES
    (1, 'Alice', 'Ali', true, 100),
    (2, 'Bob', NULL, false, 0),
    (3, 'Charlie', NULL, true, 85);

INSERT INTO employees (id, name, department, salary) VALUES
    (1, 'Alice', 'Engineering', 90000),
    (2, 'Bob', 'Engineering', 85000),
    (3, 'Charlie', 'Sales', 75000);

INSERT INTO events (id, created_at) VALUES
    (1, '2026-09-01 10:00:00'),
    (2, '2026-09-02 11:00:00'),
    (3, '2026-09-03 12:00:00');

INSERT INTO profiles (id, settings) VALUES
    (1, '{"theme": "dark", "active": true}'::jsonb),
    (2, '{"theme": "light", "active": false}'::jsonb);
```

テーブルを使う例を実行する前に、このセットアップを一度実行してください。リテラル値を使用する例では、セットアップは不要です。

## 集計関数 {#aggregate-functions}

以下の一般的な集計関数がサポートされています。

| 関数 | 説明 |
| --- | --- |
| `COUNT(*)` | 行数をカウントします。 |
| `COUNT(expression)` | null でない値をカウントします。 |
| `COUNT(DISTINCT expression)` | 重複しない null でない値をカウントします。 |
| `SUM(expression)` | 合計を返します。 |
| `AVG(expression)` | 平均を返します。 |
| `MIN(expression)` | 最小値を返します。 |
| `MAX(expression)` | 最大値を返します。 |
| `STRING_AGG(expression, delimiter)` | 区切り文字を使用して値を連結します。 |
| `ARRAY_AGG(expression)` | 値を配列に集約します。 |
| `JSON_AGG(expression)` | 値を JSON 配列に集約します。 |
| `JSONB_AGG(expression)` | 値を JSONB 配列に集約します。 |
| `JSON_OBJECT_AGG(key, value)` | キー/値のペアを JSON オブジェクトに集約します。 |
| `JSONB_OBJECT_AGG(key, value)` | キー/値のペアを JSONB オブジェクトに集約します。 |
| `BOOL_AND(expression)` | null でないすべての入力が true の場合に true を返します。 |
| `BOOL_OR(expression)` | null でないいずれかの入力が true の場合に true を返します。 |

例:

```sql
SELECT
    department,
    COUNT(*) AS employee_count,
    AVG(salary) AS average_salary,
    MAX(salary) AS maximum_salary
FROM employees
GROUP BY department;
```

集計 `FILTER` がサポートされています。

```sql
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE active = true) AS active_count
FROM users;
```

## ウィンドウ関数 {#window-functions}

PostgreSQL 互換の {{{ .starter }}} は、一般的なランキングおよび値アクセスのウィンドウ関数をサポートしています。

### ランキング関数 {#ranking-functions}

- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `NTILE()`
- `PERCENT_RANK()`
- `CUME_DIST()`

例:

```sql
SELECT
    name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS salary_rank
FROM employees;
```

### 値アクセス関数 {#value-access-functions}

- `LAG()`
- `LEAD()`
- `FIRST_VALUE()`
- `LAST_VALUE()`
- `NTH_VALUE()`

例:

```sql
SELECT
    id,
    created_at,
    LAG(created_at) OVER (ORDER BY created_at) AS previous_created_at
FROM events;
```

### ウィンドウ関数としての集計関数 {#aggregate-functions-as-window-functions}

以下の集計関数は `OVER` 句とともに使用できます。

- `SUM`
- `AVG`
- `COUNT`
- `MIN`
- `MAX`
- `STRING_AGG`

例:

```sql
SELECT
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS department_average
FROM employees;
```

その他の集計関数はウィンドウ関数として使用できません。

## JSON および JSONB 関数 {#json-and-jsonb-functions}

以下の一般的な JSON および JSONB 関数がサポートされています。

| 関数 | 説明 |
| --- | --- |
| `JSON_TYPEOF(json)` | 最上位の JSON 値の型を返します。 |
| `JSONB_TYPEOF(jsonb)` | 最上位の JSONB 値の型を返します。 |
| `JSON_BUILD_OBJECT(...)` | キー/値のペアから JSON オブジェクトを構築します。 |
| `JSONB_BUILD_OBJECT(...)` | キー/値のペアから JSONB オブジェクトを構築します。 |
| `JSON_BUILD_ARRAY(...)` | JSON 配列を構築します。 |
| `JSONB_BUILD_ARRAY(...)` | JSONB 配列を構築します。 |
| `JSON_ARRAY_LENGTH(json)` | JSON 配列の長さを返します。 |
| `JSONB_ARRAY_LENGTH(jsonb)` | JSONB 配列の長さを返します。 |
| `JSON_ARRAY_ELEMENTS(json)` | JSON 配列を行に展開します。 |
| `JSONB_ARRAY_ELEMENTS(jsonb)` | JSONB 配列を行に展開します。 |
| `JSON_OBJECT_KEYS(json)` | オブジェクトのキーを返します。 |
| `JSONB_OBJECT_KEYS(jsonb)` | オブジェクトのキーを返します。 |
| `JSONB_EACH(jsonb)` | JSONB オブジェクトをキー/値の行に展開します。 |
| `JSONB_SET(jsonb, path, value [, create_missing])` | パス上の JSONB 値を置き換えるか挿入します。 |

例:

```sql
SELECT
    JSONB_TYPEOF('{"a":1}'::jsonb),
    JSONB_BUILD_OBJECT('name', 'Alice', 'active', true),
    JSONB_ARRAY_LENGTH('[1,2,3]'::jsonb);
```

### JSON 演算子 {#json-operators}

以下を含む、一般的な PostgreSQL の JSON および JSONB 演算子がサポートされています。

| 演算子 | 説明 |
| --- | --- |
| `->` | キーまたは配列インデックスで JSON 値を取得します。 |
| `->>` | JSON 値をテキストとして取得します。 |
| `#>` | パスで JSON 値を取得します。 |
| `#>>` | パスで JSON 値をテキストとして取得します。 |
| `@>` | JSONB の包含関係を確認します。 |
| `<@` | JSONB が別の値に含まれているかどうかを確認します。 |
| `?` | キーが存在するかどうかを確認します。 |
| `?|` | 指定したキーのいずれかが存在するかどうかを確認します。 |
| `?&` | 指定したすべてのキーが存在するかどうかを確認します。 |

例:

```sql
SELECT settings->>'theme'
FROM profiles
WHERE settings @> '{"active":true}';
```

## 配列関数 {#array-functions}

以下の一般的な配列関数がサポートされています。

| 関数 | 説明 |
| --- | --- |
| `ARRAY_LENGTH(array, dimension)` | 配列の次元の長さを返します。 |
| `ARRAY_UPPER(array, dimension)` | 次元の上限を返します。 |
| `ARRAY_LOWER(array, dimension)` | 次元の下限を返します。 |
| `ARRAY_APPEND(array, element)` | 要素を末尾に追加します。 |
| `ARRAY_PREPEND(element, array)` | 要素を先頭に追加します。 |
| `ARRAY_CAT(array1, array2)` | 配列を連結します。 |
| `ARRAY_POSITION(array, element)` | 最初に一致した位置を返します。 |
| `ARRAY_POSITIONS(array, element)` | 一致したすべての位置を返します。 |
| `ARRAY_REMOVE(array, element)` | 一致した要素を削除します。 |
| `ARRAY_REPLACE(array, from, to)` | 一致した要素を置き換えます。 |
| `ARRAY_TO_STRING(array, delimiter [, null_string])` | 配列をテキストに変換します。 |
| `STRING_TO_ARRAY(text, delimiter [, null_string])` | テキストを分割して配列にします。 |
| `UNNEST(array)` | 配列を行に展開します。 |
| `GENERATE_SUBSCRIPTS(array, dimension)` | 有効な配列インデックスを生成します。 |

例:

```sql
SELECT
    ARRAY_LENGTH(ARRAY['a', 'b', 'c'], 1),
    ARRAY_APPEND(ARRAY['a', 'b'], 'c'),
    ARRAY_POSITION(ARRAY['a', 'b', 'c'], 'b');
```

## 正規表現の関数と演算子 {#regular-expression-functions-and-operators}

以下の正規表現関数がサポートされています。

| 関数 | 説明 |
| --- | --- |
| `REGEXP_REPLACE(text, pattern, replacement [, flags])` | 正規表現に一致するテキストを置換します。 |
| `REGEXP_SPLIT_TO_ARRAY(text, pattern [, flags])` | 正規表現を使用してテキストを分割します。 |
| `REGEXP_SPLIT_TO_TABLE(text, pattern [, flags])` | テキストを複数の行に分割します。 |

例:

```sql
SELECT REGEXP_REPLACE(
    'foo   bar',
    '\s+',
    ' ',
    'g'
);
```

以下の正規表現演算子がサポートされています。

| 演算子 | 説明 |
| --- | --- |
| `~` | 大文字と小文字を区別する一致です。 |
| `~*` | 大文字と小文字を区別しない一致です。 |
| `!~` | 大文字と小文字を区別する非一致です。 |
| `!~*` | 大文字と小文字を区別しない非一致です。 |

例:

```sql
SELECT 'PostgreSQL' ~* 'postgres';
```

## UUID、エンコーディング、およびハッシュ関数 {#uuid-encoding-and-hashing-functions}

一般的な UUID、エンコーディング、およびハッシュ関数には、次のものがあります。

| 関数 | 説明 |
| --- | --- |
| `GEN_RANDOM_UUID()` | ランダムな UUID を生成します。 |
| `MD5(text)` | MD5 ハッシュを 16 進数テキストとして返します。 |
| `ENCODE(bytea, format)` | バイナリデータをエンコードします。 |
| `DECODE(text, format)` | テキストをバイナリデータにデコードします。 |

追加の `uuid-ossp` 互換 UUID 関数が組み込まれており、`CREATE EXTENSION "uuid-ossp"` を使用して拡張メタデータを登録できます。

## シーケンス関数 {#sequence-functions}

以下のシーケンス関数がサポートされています。

| 関数 | 説明 |
| --- | --- |
| `NEXTVAL(sequence)` | シーケンスを進め、新しい値を返します。 |
| `CURRVAL(sequence)` | 現在のセッションで、そのシーケンスに対して `NEXTVAL` が最後に返した値を返します。 |
| `SETVAL(sequence, value [, called])` | 現在のシーケンス値を設定します。 |
| `LASTVAL()` | 現在のセッションで `NEXTVAL` が最後に返した値を返します。 |

例:

```sql
CREATE SEQUENCE order_seq START WITH 1000;

SELECT nextval('order_seq');
SELECT currval('order_seq');
SELECT setval('order_seq', 2000);
```

`NEXTVAL` などのシーケンス操作は非トランザクション的です。

## 条件式 {#conditional-expressions}

以下の PostgreSQL 条件式がサポートされています。

- `CASE`
- `COALESCE`
- `NULLIF`
- `GREATEST`
- `LEAST`

例:

```sql
SELECT
    COALESCE(nickname, name) AS display_name,
    NULLIF(score, 0) AS nonzero_score
FROM users;
```

## システム関数と互換関数 {#system-and-compatibility-functions}

一般的な PostgreSQL 互換システム関数には、次のものがあります。

| 関数または式 | 説明 |
| --- | --- |
| `CURRENT_USER` | 現在のロール名を返します。 |
| `SESSION_USER` | セッションユーザーを返します。 |
| `CURRENT_DATABASE()` | 現在のデータベースを返します。 |
| `CURRENT_SCHEMA()` | 現在のスキーマを返します。 |
| `CURRENT_SCHEMAS(boolean)` | 現在の検索パス内のスキーマを返します。 |
| `VERSION()` | PostgreSQL 互換のサーバーバージョン情報を返します。 |
| `PG_TYPEOF(value)` | 値のデータ型を返します。 |
| `PG_BACKEND_PID()` | PostgreSQL 互換のバックエンドプロセス識別子を返します。 |
| `CURRENT_SETTING(name)` | セッションパラメータ値を返します。 |

例:

```sql
SELECT
    CURRENT_USER,
    CURRENT_DATABASE(),
    CURRENT_SCHEMA(),
    PG_TYPEOF(42);
```

## 集合を返す関数 {#set-returning-functions}

一部の関数は複数の行を返します。

`FROM` 句で `GENERATE_SERIES()` を使用します。

```sql
SELECT value
FROM generate_series(1, 5) AS t(value);
```

`UNNEST()` を使用すると配列を展開できます。

```sql
SELECT value
FROM unnest(ARRAY['a', 'b', 'c']) AS t(value);
```

一部のスカラー関数および集合を返す関数では、関数呼び出し位置が PostgreSQL と異なる場合があります。移植性を高めるため、前述の例のように、集合を返す関数は `FROM` 句で使用してください。

## 拡張機能固有の関数 {#extension-specific-functions}

以下の機能により、追加の SQL 関数が提供されます。

- ベクトル検索と埋め込み
- 全文検索
- HTTP リクエスト
- Parquet インポート
- UUID 生成

詳細は、[PostgreSQL 拡張機能](/tidb-cloud/starter/pg-extensions-overview.md) を参照してください。