---
title: CREATE NGRAM INDEX
summary: テーブルのカラムに Ngram インデックスを作成します。
---

# CREATE NGRAM INDEX

テーブルのカラムに Ngram インデックスを作成します。

## 構文 {#syntax}

```sql
-- Create an Ngram index on an existing table
CREATE [OR REPLACE] NGRAM INDEX [IF NOT EXISTS] <index_name>
ON [<database>.]<table_name>(<column>)
[gram_size = <number>] [bloom_size = <number>]

-- Create an Ngram index when creating a table
CREATE [OR REPLACE] TABLE <table_name> (
    <column_definitions>,
    NGRAM INDEX <index_name> (<column>)
        [gram_size = <number>] [bloom_size = <number>]
)...
```

- `gram_size`（デフォルトは 3）は、カラムのテキストをインデックス化する際に、文字ベースの各部分文字列（n-gram）の長さを指定します。たとえば、`gram_size = 3` の場合、テキスト `"hello world"` は次のような重なり合う部分文字列に分割されます。

  ```text
  "hel", "ell", "llo", "lo ", "o w", " wo", "wor", "orl", "rld"
  ```

- `bloom_size` は、各データブロック内で文字列マッチングを高速化するために使用されるブルームフィルターのビットマップサイズをバイト単位で指定します。これは、インデックスの精度とメモリ使用量のトレードオフを制御します。

    - `bloom_size` を大きくすると、文字列検索時の偽陽性が減少し、より多くのメモリを消費する代わりにクエリ精度が向上します。
    - `bloom_size` を小さくすると、メモリを節約できますが、偽陽性が増える可能性があります。
    - 明示的に設定しない場合、デフォルトはインデックス付きカラムごと・ブロックごとに 1,048,576 バイト（1m）です。有効範囲は 512 バイトから 10,485,760 バイト（10m）です。

## 例 {#examples}

### NGRAM インデックス付きテーブルの作成 {#creating-a-table-with-ngram-index}

```sql
CREATE TABLE articles (
    id INT,
    title VARCHAR,
    content STRING,
    NGRAM INDEX idx_content (content)
);
```

### 既存テーブルに NGRAM インデックスを作成する {#creating-an-ngram-index-on-an-existing-table}

```sql
CREATE TABLE products (
    id INT,
    name VARCHAR,
    description STRING
);

CREATE NGRAM INDEX idx_description
ON products(description);
```

### インデックスの表示 {#viewing-indexes}

```sql
SHOW INDEXES;
```

結果:

```
┌─────────────────┬───────┬──────────┬─────────────────────────┬──────────────────────────┐
│ name            │ type  │ original │ definition              │ created_on               │
├─────────────────┼───────┼──────────┼─────────────────────────┼──────────────────────────┤
│ idx_content     │ NGRAM │          │ articles(content)       │ 2025-05-13 01:22:34.123  │
│ idx_description │ NGRAM │          │ products(description)   │ 2025-05-13 01:23:45.678  │
└─────────────────┴───────┴──────────┴─────────────────────────┴──────────────────────────┘
```

### NGRAM インデックスの使用 {#using-ngram-index}

```sql
-- Create a table with NGRAM index
CREATE TABLE phrases (
    id INT,
    text STRING,
    NGRAM INDEX idx_text (text)
);

-- Insert sample data
INSERT INTO phrases VALUES
(1, 'apple banana cherry'),
(2, 'banana date fig'),
(3, 'cherry elderberry fig'),
(4, 'date grape kiwi');

-- Query using fuzzy matching with the NGRAM index
SELECT * FROM phrases WHERE text LIKE '%banana%';
```

結果:

```
┌────┬─────────────────────┐
│ id │ text                │
├────┼─────────────────────┤
│  1 │ apple banana cherry │
│  2 │ banana date fig     │
└────┴─────────────────────┘
```

### NGRAM インデックスの削除 {#dropping-an-ngram-index}

```sql
DROP NGRAM INDEX idx_text ON phrases;
```