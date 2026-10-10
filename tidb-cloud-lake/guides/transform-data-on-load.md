---
title: ロード時のデータ変換
summary: "{{{ .lake }}} の `COPY INTO` コマンドでは、ロード処理中にデータ変換を実行できます。これにより、基本的な変換を取り込んで ETL パイプラインを簡素化し、一時テーブルが不要になります。"
---

# ロード時のデータ変換

{{{ .lake }}} の `COPY INTO` コマンドでは、ロード処理中にデータ変換を実行できます。これにより、基本的な変換を取り込んで ETL パイプラインを簡素化し、一時テーブルが不要になります。

構文については、[クエリと変換]( /tidb-cloud-lake/guides/query-stage.md) を参照してください。

実行できる主な変換は次のとおりです。

- **データカラムの一部をロードする**: 特定のカラムだけを選択してインポートします。
- **カラムの並べ替え**: ロード時にカラム順を変更します。
- **データ型の変換**: 一貫性と互換性を確保します。
- **算術演算の実行**: 新しい派生データを生成します。
- **追加カラムを持つテーブルへのデータロード**: 既存の構造にデータをマッピングして挿入します。

## チュートリアル {#tutorials}

以下のチュートリアルでは、ロード時のデータ変換を紹介します。各例では、stage 上のファイルからロードする方法を示します。

### 始める前に {#before-you-begin}

stage を作成し、サンプルの Parquet ファイルを生成します。

```sql
CREATE STAGE my_parquet_stage;
COPY INTO @my_parquet_stage
FROM (
    SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS id,
           'Name_' || CAST(number AS VARCHAR) AS name,
           20 + MOD(number, 23) AS age,
           DATE_ADD('day', MOD(number, 60), '2022-01-01') AS onboarded
    FROM numbers(10)
)
FILE_FORMAT = (TYPE = PARQUET);
```

stage 上のサンプルファイルをクエリします。

```sql
SELECT * FROM @my_parquet_stage;
```

結果:

```
┌───────────────────────────────────────┐
│   id   │  name  │   age  │  onboarded │
├────────┼────────┼────────┼────────────┤
│      1 │ Name_0 │     20 │ 2022-01-01 │
│      2 │ Name_5 │     25 │ 2022-01-06 │
│      3 │ Name_1 │     21 │ 2022-01-02 │
│      4 │ Name_6 │     26 │ 2022-01-07 │
│      5 │ Name_7 │     27 │ 2022-01-08 │
│      6 │ Name_2 │     22 │ 2022-01-03 │
│      7 │ Name_8 │     28 │ 2022-01-09 │
│      8 │ Name_3 │     23 │ 2022-01-04 │
│      9 │ Name_4 │     24 │ 2022-01-05 │
│     10 │ Name_9 │     29 │ 2022-01-10 │
└───────────────────────────────────────┘
```

### チュートリアル 1 - データカラムの一部をロードする {#tutorial-1-loading-a-subset-of-data-columns}

ソースファイルより少ないカラム数のテーブルにデータをロードします（例: `age` を除外）。

```sql
CREATE TABLE employees_no_age (
  id INT,
  name VARCHAR,
  onboarded timestamp
);

COPY INTO employees_no_age
FROM (
    SELECT t.id,
           t.name,
           t.onboarded
    FROM @my_parquet_stage t
)
FILE_FORMAT = (TYPE = PARQUET)
PATTERN = '.*parquet';

SELECT * FROM employees_no_age;
```

結果（先頭 3 行）:

```
┌──────────────────────────────────────────────────────────┐
│        id       │       name       │      onboarded      │
├─────────────────┼──────────────────┼─────────────────────┤
│               1 │ Name_0           │ 2022-01-01 00:00:00 │
│               2 │ Name_5           │ 2022-01-06 00:00:00 │
│               3 │ Name_1           │ 2022-01-02 00:00:00 │
└──────────────────────────────────────────────────────────┘
```

### チュートリアル 2 - ロード時にカラムを並べ替える {#tutorial-2-reordering-columns-during-load}

カラム順が異なるテーブルにデータをロードします（例: `name` の前に `age` を配置）。

```sql
CREATE TABLE employees_new_order (
  id INT,
  age INT,
  name VARCHAR,
  onboarded timestamp
);

COPY INTO employees_new_order
FROM (
    SELECT
        t.id,
        t.age,
        t.name,
        t.onboarded
    FROM @my_parquet_stage t
)
FILE_FORMAT = (TYPE = PARQUET)
PATTERN = '.*parquet';

SELECT * FROM employees_new_order;
```

結果（先頭 3 行）:

```
┌────────────────────────────────────────────────────────────────────────────┐
│        id       │       age       │       name       │      onboarded      │
├─────────────────┼─────────────────┼──────────────────┼─────────────────────┤
│               1 │              20 │ Name_0           │ 2022-01-01 00:00:00 │
│               2 │              25 │ Name_5           │ 2022-01-06 00:00:00 │
│               3 │              21 │ Name_1           │ 2022-01-02 00:00:00 │
└────────────────────────────────────────────────────────────────────────────┘
```

### チュートリアル 3 - ロード時にデータ型を変換する {#tutorial-3-converting-datatypes-during-load}

データをロードしながら、カラムのデータ型を変換します（例: `onboarded` を `DATE` に変換）。

```sql
CREATE TABLE employees_date (
  id INT,
  name VARCHAR,
  age INT,
  onboarded date
);

COPY INTO employees_date
FROM (
    SELECT
        t.id,
        t.name,
        t.age,
        to_date(t.onboarded)
    FROM @my_parquet_stage t
)
FILE_FORMAT = (TYPE = PARQUET)
PATTERN = '.*parquet';

SELECT * FROM employees_date;
```

結果（先頭 3 行）:

```
┌───────────────────────────────────────────────────────────────────────┐
│        id       │       name       │       age       │    onboarded   │
├─────────────────┼──────────────────┼─────────────────┼────────────────┤
│               1 │ Name_0           │              20 │ 2022-01-01     │
│               2 │ Name_5           │              25 │ 2022-01-06     │
│               3 │ Name_1           │              21 │ 2022-01-02     │
└───────────────────────────────────────────────────────────────────────┘
```

### Tutorial 4 - ロード中に算術演算を実行する {#tutorial-4-performing-arithmetic-operations-during-load}

データをロードし、算術演算を実行します（例: `age` を 1 増やす）。

```sql
CREATE TABLE employees_new_age (
  id INT,
  name VARCHAR,
  age INT,
  onboarded timestamp
);

COPY INTO employees_new_age
FROM (
    SELECT
        t.id,
        t.name,
        t.age + 1,
        t.onboarded
    FROM @my_parquet_stage t
)
FILE_FORMAT = (TYPE = PARQUET)
PATTERN = '.*parquet';

SELECT * FROM employees_new_age;
```

結果（先頭 3 行）:

```
┌────────────────────────────────────────────────────────────────────────────┐
│        id       │       name       │       age       │      onboarded      │
├─────────────────┼──────────────────┼─────────────────┼─────────────────────┤
│               1 │ Name_0           │              21 │ 2022-01-01 00:00:00 │
│               2 │ Name_5           │              26 │ 2022-01-06 00:00:00 │
│               3 │ Name_1           │              22 │ 2022-01-02 00:00:00 │
└────────────────────────────────────────────────────────────────────────────┘
```

### Tutorial 5 - 追加カラムを持つテーブルへのロード {#tutorial-5-loading-to-a-table-with-additional-columns}

ソースファイルよりも多くのカラムを持つテーブルにデータをロードします。

```sql
CREATE TABLE employees_plus (
  id INT,
  name VARCHAR,
  age INT,
  onboarded timestamp,
  lastday timestamp
);

COPY INTO employees_plus (id, name, age, onboarded)
FROM (
    SELECT
        t.id,
        t.name,
        t.age,
        t.onboarded
    FROM @my_parquet_stage t
)
FILE_FORMAT = (TYPE = PARQUET)
PATTERN = '.*parquet';

SELECT * FROM employees_plus;
```

結果（先頭 3 行）:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│        id       │       name       │       age       │      onboarded      │       lastday       │
├─────────────────┼──────────────────┼─────────────────┼─────────────────────┼─────────────────────┤
│               1 │ Name_0           │              20 │ 2022-01-01 00:00:00 │ NULL                │
│               2 │ Name_5           │              25 │ 2022-01-06 00:00:00 │ NULL                │
│               3 │ Name_1           │              21 │ 2022-01-02 00:00:00 │ NULL                │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```