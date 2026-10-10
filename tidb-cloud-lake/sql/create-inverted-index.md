---
title: CREATE INVERTED INDEX
summary: "{{{ .lake }}} で新しい inverted index を作成します。"
---

# CREATE INVERTED INDEX

{{{ .lake }}} で新しい inverted index を作成します。

Inverted index は通常、`STRING` および `VARIANT` カラムに対して使用されます。クエリには、フィールドを意識した式、ブール演算子、ネストされたパスをサポートする [`QUERY()`](/tidb-cloud-lake/sql/query.md) 関数の使用を推奨します。一致した行の関連度スコアを返して順位付けするには、`QUERY()` とあわせて [`score()`](/tidb-cloud-lake/sql/score.md) を使用できます。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] INVERTED INDEX [IF NOT EXISTS] <index>
    ON [<database>.]<table>( <column>[, <column> ...] )
    [ <IndexOptions> ]
```

| パラメータ              | 説明                                                                                                                                               |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `[ OR REPLACE ]`       | 省略可能なパラメータです。インデックスがすでに存在する場合、それを置き換えることを示します。                                                                      |
| `[ IF NOT EXISTS ]`    | 省略可能なパラメータです。インデックスがまだ存在しない場合にのみ作成されることを示します。                                                           |
| `<index>`              | 作成する inverted index の名前です。                                                                                                             |
| `[<database>.]<table>` | インデックスを作成する対象カラムを含むデータベース名とテーブル名です。                                                            |
| `<column>`             | インデックスに含めるカラム名です。実際には通常 `STRING` または `VARIANT` カラムです。同じテーブルに対して複数のインデックスを作成できますが、各カラムはインデックス間で一意である必要があります。 |
| `<IndexOptions>`       | inverted index の構築方法を指定する省略可能なインデックスオプションです。                                                                                            |

### IndexOptions {#indexoptions}

```sql
IndexOptions ::=
  TOKENIZER = 'english' | 'chinese'
  FILTERS = 'english_stop' | 'english_stemmer' | 'chinese_stop'
  INDEX_RECORD = 'position' | 'basic' | 'freq'
```

- `TOKENIZER` は、インデックス作成のためにテキストをどのように分割するかを指定します。`english`（デフォルト）および `chinese` tokenizer をサポートします。
- `FILTERS` は、用語のフィルタリングルールを定義します。
    - 複数のフィルタをカンマ区切りで指定できます。例: `FILTERS = 'english_stop,english_stemmer'`。
    - 単語を小文字に変換する lower case filter はデフォルトで追加されます。

| FILTERS           | 説明                                                                                                             |
|-------------------|-----------------------------------------------------------------------------------------------------------------|
| `english_stop`    | "a"、"an"、"and" などの英語のストップワードを削除します。                                                                   |
| `english_stemmer` | 同じ単語の異なる形を 1 つの共通語にマッピングします。たとえば、"walking" と "walked" は "walk" にマッピングされます。 |
| `chinese_stop`    | 中国語のストップワードを削除します。現在は中国語の句読点の削除のみをサポートしています。                               |

- `INDEX_RECORD` は、インデックスデータに何を格納するかを決定します。

| INDEX_RECORD | デフォルト? | 説明                                                                                                             |
|--------------|----------|-----------------------------------------------------------------------------------------------------------------|
| `position`   | はい      | DocId、term frequency、positions を格納します。最も多くの領域を使用しますが、より良いスコアリングを提供し、phrase term をサポートします。 |
| `basic`      | いいえ       | DocId のみを格納します。使用領域は最小ですが、"brown fox" のようなフレーズ検索はサポートしません。                    |
| `freq`       | いいえ       | DocId と term frequency を格納します。使用領域は中程度で、phrase term はサポートしませんが、より良いスコアを提供する場合があります。    |

## 例 {#examples}

### 単一カラムに Inverted Index を作成する {#creating-an-inverted-index-on-a-single-column}

```sql
CREATE TABLE user_comments (
    id INT,
    comment_text STRING
);

CREATE INVERTED INDEX user_comments_idx ON user_comments(comment_text);
```

### カスタム Tokenizer と Filters を使用して Inverted Index を作成する {#creating-an-inverted-index-with-custom-tokenizer-and-filters}

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

### 複数カラムに Inverted Index を作成する {#creating-an-inverted-index-on-multiple-columns}

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

### `QUERY()` を使用して単一のインデックス付きカラムをクエリする {#querying-a-single-indexed-column-with-query}

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

`QUERY()` を使用してインデックス付きカラムを検索し、`score()` で関連度スコアを返します。

```sql
SELECT id, score(), content
FROM quotes
WHERE QUERY('content:word')
ORDER BY score() DESC;
```

結果:

```text
╭──────────────────────────────────────────────────────╮
│ id │  score()  │               content               │
├────┼───────────┼─────────────────────────────────────┤
│  2 │ 0.8025914 │ A picture is worth a thousand words │
│  3 │ 0.7438652 │ Actions speak louder than words     │
╰──────────────────────────────────────────────────────╯
```

あいまい検索を実行することもできます。

```sql
SELECT id, score(), content
FROM quotes
WHERE QUERY('content:box', 'fuzziness=1');
```

結果:

```text
╭────────────────────────────────────────────────────────────╮
│ id │ score() │                   content                   │
├────┼─────────┼─────────────────────────────────────────────┤
│  1 │     1.0 │ The quick brown fox jumps over the lazy dog │
╰────────────────────────────────────────────────────────────╯
```

### `QUERY()` を使用した複数のインデックス付きカラムのクエリ {#querying-multiple-indexed-columns-with-query}

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

フィールドを意識したブール検索には `QUERY()` を使用します。

```sql
SELECT id, score(), title
FROM books
WHERE QUERY('title:设计 OR title:实现')
ORDER BY score() DESC;
```

結果:

```text
╭───────────────────────────────────╮
│ id │  score()  │       title      │
├────┼───────────┼──────────────────┤
│  3 │ 1.8571336 │ Vue.js设计与实现 │
│  4 │ 0.6785374 │ 前端架構设计     │
╰───────────────────────────────────╯
```

複数のフィールドをまとめて検索することもできます。

```sql
SELECT id, score(), title
FROM books
WHERE QUERY('title:ChatGPT OR description:OpenAI')
ORDER BY score() DESC;
```

結果:

```text
╭───────────────────────────────────╮
│ id │  score()  │       title      │
├────┼───────────┼──────────────────┤
│  1 │ 2.5784383 │ 这就是ChatGPT    │
╰───────────────────────────────────╯
```

### `QUERY()` を使用した `VARIANT` カラムのクエリ {#querying-a-variant-column-with-query}

`VARIANT` カラムもサポートされています。これは、ネストされた JSON ライクなドキュメントを事前にフラット化せずに検索したい場合に便利です。

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

`VARIANT` ドキュメント内のネストされたパスをクエリします。

```sql
SELECT id, body
FROM media_assets
WHERE QUERY('body.videoInfo.extraData.name:codecA AND body.videoInfo.extraData.type:jpg')
ORDER BY id;
```

結果:

```text
╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ id │                                             body                                            │
├────┼─────────────────────────────────────────────────────────────────────────────────────────────┤
│  2 │ {"videoInfo":{"extraData":[{"name":"codecA","type":"jpg"},{"name":"codecA","type":"mp4"}]}} │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```

また、引用符付きの用語は、スペースを含む値に対しても機能します。

```sql
SELECT id, body
FROM media_assets
WHERE QUERY('body.videoInfo.extraData.name:"codec foo" AND body.videoInfo.extraData.type:mp4')
ORDER BY id;
```

結果:

```text
╭──────────────────────────────────────────────────────────────────────╮
│ id │                               body                              │
├────┼─────────────────────────────────────────────────────────────────┤
│  4 │ {"videoInfo":{"extraData":[{"name":"codec foo","type":"mp4"}]}} │
╰──────────────────────────────────────────────────────────────────────╯
```