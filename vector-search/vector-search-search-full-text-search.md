---
title: Full Text Search
summary: Full-text search allows you to retrieve documents for exact keywords. In RAG (Retrieval-Augmented Generation) scenarios, you can use full-text search along with vector search together to improve the retrieval quality.
---

# Full-Text Search

Unlike Vector Search, which focuses on semantic similarity, full-text search allows you to retrieve documents for exact keywords. In RAG (Retrieval-Augmented Generation) scenarios, you can use full-text search along with vector search together to improve the retrieval quality.

The full-text search feature in TiDB provides the following capabilities:

- **Operate on Text Data**: You can search over any string columns directly without embedding process.

- **Support Hybrid-Language**: No need to specify the language for high quality search. TiDB's text analyzer supports documents of multiple languages mixed in the same table and chooses the best analyzer for each document.

- **Order by Relevance**: The search result can be ordered by relevance using the widely used [BM25 ranking](https://en.wikipedia.org/wiki/Okapi_BM25) algorithm.

- **Support Full SQL Features**: All SQL features, like pre-filtering, post-filtering, grouping, joining, etc, can be used with full-text search.

> **Tip:**
>
> This document covers details about the full-text search feature itself using SQL. For guidelines of using full-text search and vector search together in your AI application, you may further refer to [Hybrid Search](/vector-search/vector-search-search-hybrid-search.md).

## Getting Started using SQL

Full-Text search is still in early stage and we are continously rolling out to more customers. Full-Text Search is currently only available for the following service and regions:

- TiDB Serverless (Europe Region)

Make sure you have a TiDB Serverless cluster in the supported regions above, then follow these steps:

1. [**Create Full-Text Index**](#create-full-text-index): Create a table with a full-text index, or add a full-text index to an existing table.

2. [**Insert Text Data**](#insert-text-data): Insert text data into the table.

3. [**Perform Full-Text Search**](#perform-full-text-search): Perform a full-text search using text queries and full-text search functions.

## Create Full-Text Index

A full-text index is required to perform full-text search, as it provides the necessary data structure for efficient searching and ranking. Full-text indexes can be created on new tables or added to existing tables.

Create a table with a full-text index:

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT,
    FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

Or add a full-text index to an existing table:

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT
);

-- You may insert some data here.
-- The Full-Text index can be created even if data is already in the table.

ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL;
```

## Insert Text Data

Inserting data into a table with a full-text index is identical to inserting data into any other tables.

In this example we will insert data in multiple languages, like Japanese, English, and Chinese. This can be naturally handled by TiDB's multilingual text analyzer:

```sql
INSERT INTO stock_items VALUES (1, "イヤホン bluetooth ワイヤレスイヤホン ");
INSERT INTO stock_items VALUES (2, "完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0 ");
INSERT INTO stock_items VALUES (3, "ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD ");
INSERT INTO stock_items VALUES (4, "楽器用 オンイヤーヘッドホン 密閉型【国内正規品】");
INSERT INTO stock_items VALUES (5, "ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル");
INSERT INTO stock_items VALUES (6, "Lightweight Bluetooth Earbuds with 48 Hours Playtime");
INSERT INTO stock_items VALUES (7, "True Wireless Noise Cancelling Earbuds - Compatible with Apple & Android, Built-in Microphone");
INSERT INTO stock_items VALUES (8, "In-Ear Earbud Headphones with Mic, Black");
INSERT INTO stock_items VALUES (9, "Wired Headphones, HD Bass Driven Audio, Lightweight Aluminum Wired in Ear Earbud Headphones");
INSERT INTO stock_items VALUES (10, "LED Light Bar, Music Sync RGB Light Bar, USB Ambient Lamp");
INSERT INTO stock_items VALUES (11, "无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）");
INSERT INTO stock_items VALUES (12, "专业版USB7.1声道游戏耳机电竞耳麦头戴式电脑网课办公麦克风带线控");
INSERT INTO stock_items VALUES (13, "投影仪家用智能投影机便携卧室手机投影");
INSERT INTO stock_items VALUES (14, "无线蓝牙耳机超长续航42小时快速充电 流光金属耳机");
INSERT INTO stock_items VALUES (15, "皎月银 国家补贴 澎湃OS 2 心率血氧监测 蓝牙通话 智能手表 男女表");
```

## Perform Full-Text Search

Use the `FTS_MATCH_WORD()` function to perform a full-text search.

**Search for most relevant 10 documents:**

```sql
SELECT * FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title)
    ORDER BY fts_match_word("bluetoothイヤホン", title)
    DESC LIMIT 10;

-- Results are ordered by relevance, with the most relevant documents appearing first.

+------+-----------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                     |
+------+-----------------------------------------------------------------------------------------------------------+
|    1 | イヤホン bluetooth ワイヤレスイヤホン                                                                     |
|    6 | Lightweight Bluetooth Earbuds with 48 Hours Playtime                                                      |
|    2 | 完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0                                                   |
|    3 | ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD                                         |
|    5 | ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル                                 |
+------+-----------------------------------------------------------------------------------------------------------+

-- Try with another language:
SELECT * FROM stock_items
    WHERE fts_match_word("蓝牙耳机", title)
    ORDER BY fts_match_word("蓝牙耳机", title)
    DESC LIMIT 10;

-- Results are ordered by relevance, with the most relevant documents appearing first.

+------+---------------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                         |
+------+---------------------------------------------------------------------------------------------------------------+
|   14 | 无线蓝牙耳机超长续航42小时快速充电 流光金属耳机                                                               |
|   11 | 无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）                                    |
|   15 | 皎月银 国家补贴 澎湃OS 2 心率血氧监测 蓝牙通话 智能手表 男女表                                                |
+------+---------------------------------------------------------------------------------------------------------------+
```

**Count the number of documents matching the user query:**

```sql
SELECT COUNT(*) FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title);

+----------+
| COUNT(*) |
+----------+
|        5 |
+----------+
```

## Feedbacks & Help

Full-text search is still in early stage with limited accessibility. If you would like to try full-text search in a region that is not available yet, or you have feedbacks or need help, feel free to reach out to us:

<CustomContent platform="tidb">

- [Join our Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)

</CustomContent>

## See also

- [Hybrid Search](/vector-search/vector-search-search-hybrid-search.md)
