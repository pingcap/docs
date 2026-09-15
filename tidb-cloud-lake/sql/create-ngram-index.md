---
title: CREATE NGRAM INDEX
summary: 在表的列上创建 Ngram 索引。
---

# CREATE NGRAM INDEX

在表的列上创建 Ngram 索引。

## 语法 {#syntax}

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

- `gram_size`（默认为 3）指定在为列文本建立索引时，每个基于字符的子字符串（n-gram）的长度。例如，当 `gram_size = 3` 时，文本 `"hello world"` 会被切分为如下重叠的子字符串：

  ```text
  "hel", "ell", "llo", "lo ", "o w", " wo", "wor", "orl", "rld"
  ```

- `bloom_size` 指定用于加速每个数据块内字符串匹配的布隆过滤器位图大小（以字节为单位）。它控制索引准确性与内存使用之间的权衡：

    - 较大的 `bloom_size` 会减少字符串查找中的误报，从而提高查询精度，但会占用更多内存。
    - 较小的 `bloom_size` 可以节省内存，但可能会增加误报。
    - 如果未显式设置，默认值为每个已索引列、每个数据块 1,048,576 字节（1m）。有效范围为 512 字节到 10,485,760 字节（10m）。

## 示例 {#examples}

### 创建带有 NGRAM 索引的表 {#creating-a-table-with-ngram-index}

```sql
CREATE TABLE articles (
    id INT,
    title VARCHAR,
    content STRING,
    NGRAM INDEX idx_content (content)
);
```

### 在现有表上创建 NGRAM 索引 {#creating-an-ngram-index-on-an-existing-table}

```sql
CREATE TABLE products (
    id INT,
    name VARCHAR,
    description STRING
);

CREATE NGRAM INDEX idx_description
ON products(description);
```

### 查看索引 {#viewing-indexes}

```sql
SHOW INDEXES;
```

结果：

```
┌─────────────────┬───────┬──────────┬─────────────────────────┬──────────────────────────┐
│ name            │ type  │ original │ definition              │ created_on               │
├─────────────────┼───────┼──────────┼─────────────────────────┼──────────────────────────┤
│ idx_content     │ NGRAM │          │ articles(content)       │ 2025-05-13 01:22:34.123  │
│ idx_description │ NGRAM │          │ products(description)   │ 2025-05-13 01:23:45.678  │
└─────────────────┴───────┴──────────┴─────────────────────────┴──────────────────────────┘
```

### 使用 NGRAM 索引 {#using-ngram-index}

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

结果：

```
┌────┬─────────────────────┐
│ id │ text                │
├────┼─────────────────────┤
│  1 │ apple banana cherry │
│  2 │ banana date fig     │
└────┴─────────────────────┘
```

### 删除 NGRAM 索引 {#dropping-an-ngram-index}

```sql
DROP NGRAM INDEX idx_text ON phrases;
```