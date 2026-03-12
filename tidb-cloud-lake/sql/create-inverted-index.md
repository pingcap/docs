---
title: CREATE INVERTED INDEX
sidebar_position: 1
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.405"/>

Creates a new inverted index in Databend.

## Syntax

```sql
CREATE [ OR REPLACE ] INVERTED INDEX [IF NOT EXISTS] <index>
    ON [<database>.]<table>( <column>[, <column> ...] )
    [ <IndexOptions> ]
```

| Parameter              | Description                                                                                                                                               |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `[ OR REPLACE ]`       | Optional parameter indicating that if the index already exists, it will be replaced.                                                                      |
| `[ IF NOT EXISTS ]`    | Optional parameter indicating that the index will only be created if it does not already exist.                                                           |
| `<index>`              | The name of the inverted index to be created.                                                                                                             |
| `[<database>.]<table>` | The name of the database and table containing the columns for which the index will be created.                                                            |
| `<column>`             | The name of the column(s) to be included in the index. Multiple indexes can be created for the same table, but each column must be unique across indexes. |
| `<IndexOptions>`       | Optional index options specifying how the inverted index is built.                                                                                            |

### IndexOptions

```sql
IndexOptions ::=
  TOKENIZER = 'english' | 'chinese'
  FILTERS = 'english_stop' | 'english_stemmer' | 'chinese_stop'
  INDEX_RECORD = 'position' | 'basic' | 'freq' 
```

- `TOKENIZER` specifies how text is segmented for indexing. It supports `english` (default) and `chinese` tokenizers.

- `FILTERS` defines rules for term filtering:

  - Multiple filters can be specified, separated by commas, e.g., `FILTERS = 'english_stop,english_stemmer'`. 
  - A lower case filter is added by default to convert words to lowercase letters.

| FILTERS           | Description                                                                                                             |
|-------------------|-------------------------------------------------------------------------------------------------------------------------|
| `english_stop`    | Removes English stop words like "a", "an", "and" etc.                                                                   |
| `english_stemmer` | Maps different forms of the same word to one common word. For example, "walking" and "walked" will be mapped to "walk". |
| `chinese_stop`    | Removes Chinese stop words, currently only supports removal of Chinese punctuation marks.                               |

- `INDEX_RECORD` determines what is to be stored for the index data:

| INDEX_RECORD | Default? | Description                                                                                                             |
|--------------|----------|-------------------------------------------------------------------------------------------------------------------------|
| `position`   | Yes      | Stores DocId, term frequency, and positions, occupies the most space, offers better scoring, and supports phrase terms. |
| `basic`      | No       | Stores only the DocId, occupies minimal space, but doesn't support phrase searches like "brown fox".                    |
| `freq`       | No       | Stores DocId and term frequency, occupies medium space, doesn't support phrase terms, but may provide better scores.    |

## Examples

```sql
-- Create an inverted index for the 'comment_text' column in the table 'user_comments'
CREATE INVERTED INDEX user_comments_idx ON user_comments(comment_text);

-- Create an inverted index with a Chinese tokenizer
-- If no tokenizer is specified, the default is English
-- Filters are `english_stop`, `english_stemmer` and `chinese_stop`
-- Index_record in `basic`.
CREATE INVERTED INDEX product_reviews_idx ON product_reviews(review_text) TOKENIZER = 'chinese' FILTERS = 'english_stop,english_stemmer,chinese_stop' INDEX_RECORD='basic';

-- Create an inverted index for the 'comment_title' and 'comment_body' columns in the table 'user_comments'
-- The output of SHOW CREATE TABLE includes information about the created inverted index
CREATE INVERTED INDEX customer_feedback_idx ON customer_feedback(comment_title, comment_body);

SHOW CREATE TABLE customer_feedback;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│       Table       │                                                                                       Create Table                                                                                      │
├───────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ customer_feedback │ CREATE TABLE customer_feedback (\n  comment_title VARCHAR NULL,\n  comment_body VARCHAR NULL,\n  SYNC INVERTED INDEX customer_feedback_idx (comment_title, comment_body)\n) ENGINE=FUSE │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
