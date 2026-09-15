---
title: CREATE INVERTED INDEX
summary: 在 {{{ .lake }}} 中创建一个新的倒排索引。
---

# CREATE INVERTED INDEX

在 {{{ .lake }}} 中创建一个新的倒排索引。

倒排索引通常用于 `STRING` 和 `VARIANT` 列。进行查询时，推荐优先使用 [`QUERY()`](/tidb-cloud-lake/sql/query.md) 函数，因为它支持字段感知表达式、布尔运算符和嵌套路径。你还可以将 [`score()`](/tidb-cloud-lake/sql/score.md) 与 `QUERY()` 一起使用，以返回相关性分数并对匹配的行进行排序。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] INVERTED INDEX [IF NOT EXISTS] <index>
    ON [<database>.]<table>( <column>[, <column> ...] )
    [ <IndexOptions> ]
```

| 参数                   | 描述                                                                                                                                                      |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `[ OR REPLACE ]`       | 可选参数，表示如果索引已存在，则将其替换。                                                                                                                |
| `[ IF NOT EXISTS ]`    | 可选参数，表示仅当索引尚不存在时才创建该索引。                                                                                                            |
| `<index>`              | 要创建的倒排索引名称。                                                                                                                                    |
| `[<database>.]<table>` | 包含待创建索引列的数据库和表名称。                                                                                                                        |
| `<column>`             | 要包含在索引中的列名。实际使用中，这些列通常是 `STRING` 或 `VARIANT` 列。同一张表可以创建多个索引，但每个列在不同索引之间必须唯一。                     |
| `<IndexOptions>`       | 可选的索引选项，用于指定如何构建倒排索引。                                                                                                                |

### IndexOptions {#indexoptions}

```sql
IndexOptions ::=
  TOKENIZER = 'english' | 'chinese'
  FILTERS = 'english_stop' | 'english_stemmer' | 'chinese_stop'
  INDEX_RECORD = 'position' | 'basic' | 'freq'
```

- `TOKENIZER` 指定索引时文本的分词方式。支持 `english`（默认）和 `chinese` 分词器。
- `FILTERS` 定义词项过滤规则：
    - 可以指定多个过滤器，并使用逗号分隔，例如：`FILTERS = 'english_stop,english_stemmer'`。
    - 默认会添加一个 lower case 过滤器，将单词转换为小写字母。

| FILTERS           | 描述                                                                                           |
|-------------------|------------------------------------------------------------------------------------------------|
| `english_stop`    | 移除英文停用词，例如 "a"、"an"、"and" 等。                                                      |
| `english_stemmer` | 将同一个单词的不同形式映射为一个通用词。例如，"walking" 和 "walked" 都会被映射为 "walk"。       |
| `chinese_stop`    | 移除中文停用词，目前仅支持移除中文标点符号。                                                    |

- `INDEX_RECORD` 决定索引数据中存储的内容：

| INDEX_RECORD | 默认？ | 描述                                                                                           |
|--------------|--------|------------------------------------------------------------------------------------------------|
| `position`   | 是     | 存储 DocId、词频和位置信息，占用空间最多，提供更好的评分效果，并支持短语词项。                 |
| `basic`      | 否     | 仅存储 DocId，占用空间最小，但不支持如 "brown fox" 这样的短语搜索。                            |
| `freq`       | 否     | 存储 DocId 和词频，占用空间适中，不支持短语词项，但可能提供更好的评分效果。                    |

## 示例 {#examples}

### 在单列上创建倒排索引 {#creating-an-inverted-index-on-a-single-column}

```sql
CREATE TABLE user_comments (
    id INT,
    comment_text STRING
);

CREATE INVERTED INDEX user_comments_idx ON user_comments(comment_text);
```

### 使用自定义分词器和过滤器创建倒排索引 {#creating-an-inverted-index-with-custom-tokenizer-and-filters}

```sql
CREATE TABLE product_reviews (
    id INT,
    review_text STRING
);

-- If no tokenizer is specified, the default is English.
-- Available filters include `english_stop`, `english_stemmer`, and `chinese_stop`.
CREATE INVERTED INDEX product_reviews_idx
ON product_reviews(review_text)
TOKENIZER = 'chinese'
FILTERS = 'english_stop,english_stemmer,chinese_stop'
INDEX_RECORD = 'basic';
```

### 在多列上创建倒排索引 {#creating-an-inverted-index-on-multiple-columns}

```sql
CREATE TABLE customer_feedback (
    comment_id INT,
    comment_title STRING,
    comment_body VARIANT
);

CREATE INVERTED INDEX customer_feedback_idx
ON customer_feedback(comment_title, comment_body);

SHOW CREATE TABLE customer_feedback;

*************************** 1. row ***************************
       Table: customer_feedback
Create Table: CREATE TABLE customer_feedback (
  comment_id INT NULL,
  comment_title VARCHAR NULL,
  comment_body VARIANT NULL,
  SYNC INVERTED INDEX customer_feedback_idx (comment_title, comment_body)
) ENGINE=FUSE
```

### 使用 `QUERY()` 查询单个已建立索引的列 {#querying-a-single-indexed-column-with-query}

```sql
CREATE TABLE quotes (
    id INT,
    content STRING,
    INVERTED INDEX idx_content(content)
        FILTERS = 'english_stop,english_stemmer'
);

INSERT INTO quotes VALUES
  (1, 'The quick brown fox jumps over the lazy dog'),
  (2, 'A picture is worth a thousand words'),
  (3, 'Actions speak louder than words'),
  (4, 'Time flies like an arrow; fruit flies like a banana');
```

使用 `QUERY()` 搜索已建立索引的列，并通过 `score()` 返回相关性分数：

```sql
SELECT id, score(), content
FROM quotes
WHERE QUERY('content:word')
ORDER BY score() DESC;
```

结果：

```text
╭──────────────────────────────────────────────────────╮
│ id │  score()  │               content               │
├────┼───────────┼─────────────────────────────────────┤
│  2 │ 0.8025914 │ A picture is worth a thousand words │
│  3 │ 0.7438652 │ Actions speak louder than words     │
╰──────────────────────────────────────────────────────╯
```

你也可以执行模糊搜索：

```sql
SELECT id, score(), content
FROM quotes
WHERE QUERY('content:box', 'fuzziness=1');
```

结果：

```text
╭────────────────────────────────────────────────────────────╮
│ id │ score() │                   content                   │
├────┼─────────┼─────────────────────────────────────────────┤
│  1 │     1.0 │ The quick brown fox jumps over the lazy dog │
╰────────────────────────────────────────────────────────────╯
```

### 使用 `QUERY()` 查询多个已建立索引的列 {#querying-multiple-indexed-columns-with-query}

```sql
CREATE TABLE books (
    id INT,
    title STRING,
    author STRING,
    description STRING
);

CREATE INVERTED INDEX idx_books
ON books(title, author, description)
TOKENIZER = 'chinese'
FILTERS = 'english_stop,english_stemmer,chinese_stop';

INSERT INTO books VALUES
  (1, '这就是ChatGPT', '斯蒂芬·沃尔弗拉姆', 'ChatGPT 是 OpenAI 开发的人工智能聊天机器人程序。'),
  (2, 'Python深度学习（第2版）', '弗朗索瓦·肖莱', '本书通过 Python 代码讲解深度学习的核心思想。'),
  (3, 'Vue.js设计与实现', '霍春阳', '本书从规范和源码出发，讲解 Vue.js 框架设计与实现细节。'),
  (4, '前端架构设计', '迈卡·高保特', '本书探讨前端架构原则、工作流程和工程实践。');
```

使用 `QUERY()` 执行带字段感知的布尔搜索：

```sql
SELECT id, score(), title
FROM books
WHERE QUERY('title:设计 OR title:实现')
ORDER BY score() DESC;
```

结果：

```text
╭───────────────────────────────────╮
│ id │  score()  │       title      │
├────┼───────────┼──────────────────┤
│  3 │ 1.8571336 │ Vue.js设计与实现 │
│  4 │ 0.6785374 │ 前端架构设计     │
╰───────────────────────────────────╯
```

你也可以同时搜索多个字段：

```sql
SELECT id, score(), title
FROM books
WHERE QUERY('title:ChatGPT OR description:OpenAI')
ORDER BY score() DESC;
```

结果：

```text
╭───────────────────────────────────╮
│ id │  score()  │       title      │
├────┼───────────┼──────────────────┤
│  1 │ 2.5784383 │ 这就是ChatGPT    │
╰───────────────────────────────────╯
```

### 使用 `QUERY()` 查询 `VARIANT` 列 {#querying-a-variant-column-with-query}

也支持 `VARIANT` 列。当你希望搜索嵌套的类 JSON 文档而不先将其扁平化时，这会非常有用。

```sql
CREATE TABLE media_assets (
    id INT,
    body VARIANT,
    INVERTED INDEX idx_body(body)
);

INSERT INTO media_assets VALUES
  (1, '{"videoInfo":{"extraData":[{"name":"codecA","type":"mp4"},{"name":"codecB","type":"jpg"}]}}'),
  (2, '{"videoInfo":{"extraData":[{"name":"codecA","type":"jpg"},{"name":"codecA","type":"mp4"}]}}'),
  (3, '{"videoInfo":{"extraData":[{"name":"codecA","attributes":{"type":"jpg"}},{"name":"codecB","attributes":{"type":"mp4"}}]}}'),
  (4, '{"videoInfo":{"extraData":[{"name":"codec foo","type":"mp4"}]}}');
```

查询 `VARIANT` 文档中的嵌套路径：

```sql
SELECT id, body
FROM media_assets
WHERE QUERY('body.videoInfo.extraData.name:codecA AND body.videoInfo.extraData.type:jpg')
ORDER BY id;
```

结果：

```text
╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ id │                                             body                                            │
├────┼─────────────────────────────────────────────────────────────────────────────────────────────┤
│  2 │ {"videoInfo":{"extraData":[{"name":"codecA","type":"jpg"},{"name":"codecA","type":"mp4"}]}} │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```

对于包含空格的值，也可以使用带引号的词项：

```sql
SELECT id, body
FROM media_assets
WHERE QUERY('body.videoInfo.extraData.name:"codec foo" AND body.videoInfo.extraData.type:mp4')
ORDER BY id;
```

结果：

```text
╭──────────────────────────────────────────────────────────────────────╮
│ id │                               body                              │
├────┼─────────────────────────────────────────────────────────────────┤
│  4 │ {"videoInfo":{"extraData":[{"name":"codec foo","type":"mp4"}]}} │
╰──────────────────────────────────────────────────────────────────────╯
```