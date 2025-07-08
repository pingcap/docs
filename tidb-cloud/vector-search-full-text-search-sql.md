---
title: Full-Text Search with SQL
summary: Full-text search lets you retrieve documents for exact keywords. In Retrieval-Augmented Generation (RAG) scenarios, you can use full-text search together with vector search to improve the retrieval quality.
aliases: ['/tidb/stable/vector-search-full-text-search-sql']
---

# 使用 SQL 进行全文搜索

与 [Vector Search](/tidb-cloud/vector-search-overview.md)，专注于语义相似性的搜索不同，全文搜索允许你根据精确关键词检索文档。在 Retrieval-Augmented Generation (RAG) 场景中，你可以将全文搜索与向量搜索结合使用，以提升检索质量。

TiDB 中的全文搜索功能提供了以下能力：

- **直接查询文本数据**：你可以直接搜索任何字符串列，无需进行嵌入处理。

- **支持多语言**：无需指定语言即可实现高质量搜索。TiDB 中的文本分析器支持多种语言的文档混合在同一表中，并会自动为每个文档选择最佳的分析器。

- **按相关性排序**：搜索结果可以使用广泛采用的 [BM25 排名](https://en.wikipedia.org/wiki/Okapi_BM25) 算法按相关性排序。

- **完全兼容 SQL**：所有 SQL 功能，如预过滤、后过滤、分组和连接，都可以与全文搜索结合使用。

> **Tip:**
>
> 关于 Python 的使用方法，参见 [Full-Text Search with Python](/tidb-cloud/vector-search-full-text-search-python.md)。
>
> 若要在你的 AI 应用中同时使用全文搜索和向量搜索，参见 [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)。

## 入门指南

全文搜索仍处于早期阶段，我们正在不断向更多客户推广。目前，全文搜索仅在以下产品选项和区域提供：

- TiDB Cloud Serverless：`Frankfurt (eu-central-1)` 和 `Singapore (ap-southeast-1)`

在使用全文搜索之前，请确保你的 TiDB Cloud Serverless 集群创建在支持的区域内。如果还没有，可以按照 [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) 创建。

执行全文搜索的步骤如下：

1. [**创建全文索引**](#create-a-full-text-index)：创建带有全文索引的表，或在现有表上添加全文索引。

2. [**插入文本数据**](#insert-text-data)：向表中插入文本数据。

3. [**执行全文搜索**](#perform-a-full-text-search)：使用文本查询和全文搜索函数进行搜索。

### 创建全文索引

要执行全文搜索，必须创建全文索引，因为它提供了高效搜索和排名所需的数据结构。全文索引可以在新表上创建，也可以添加到已有表中。

创建带有全文索引的表：

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT,
    FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

或者在已有表上添加全文索引：

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT
);

-- 你可以在插入数据后再创建全文索引。
-- 即使表中已有数据，也可以创建全文索引。

ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL ADD_COLUMNAR_REPLICA_ON_DEMAND;
```

`WITH PARSER <PARSER_NAME>` 子句支持的分析器有：

- `STANDARD`：速度快，适用于英文内容，按空格和标点符号拆分词语。

- `MULTILINGUAL`：支持多种语言，包括英文、中文、日语和韩语。

### 插入文本数据

向带有全文索引的表中插入数据，方式与普通表相同。

例如，可以执行以下 SQL 语句，插入多语言文本。TiDB 中的多语言分析器会自动处理文本。

```sql
INSERT INTO stock_items VALUES (1, "イヤホン bluetooth ワイヤレスイヤホン ");
INSERT INTO stock_items VALUES (2, "完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0 ");
INSERT INTO stock_items VALUES (3, "ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD ");
INSERT INTO stock_items VALUES (4, "楽器用 オンイヤーヘッドホン 密閉型【国内正規品】");
INSERT INTO stock_items VALUES (5, "ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセリング");
INSERT INTO stock_items VALUES (6, "Lightweight Bluetooth Earbuds with 48 Hours Playtime");
INSERT INTO stock_items VALUES (7, "True Wireless Noise Cancelling Earbuds - Compatible with Apple & Android, Built-in Microphone");
INSERT INTO stock_items VALUES (8, "In-Ear Earbud Headphones with Mic, Black");
INSERT INTO stock_items VALUES (9, "Wired Headphones, HD Bass Driven Audio, Lightweight Aluminum Wired in Ear Earbud Headphones");
INSERT INTO stock_items VALUES (10, "LED Light Bar, Music Sync RGB Light Bar, USB Ambient Lamp");
INSERT INTO stock_items VALUES (11, "无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）");
INSERT INTO stock_items VALUES (12, "专业版USB7.1声道游戏耳机电竞耳麦头戴式电脑网课办公麦克风带线控");
INSERT INTO stock_items VALUES (13, "投影仪家用智能投影机便携卧室手机投影");
INSERT INTO stock_items VALUES (14, "无线蓝牙耳机超长续航42小时快速充电 流光金属耳机");
INSERT INTO stock_items VALUES (15, "皎月银 国家补贴 心率血氧监测 蓝牙通话 智能手表 男女表");
```

### 执行全文搜索

可以使用 `FTS_MATCH_WORD()` 函数进行全文搜索。

**示例：搜索最相关的 10 条文档**

```sql
SELECT * FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title)
    ORDER BY fts_match_word("bluetoothイヤホン", title)
    DESC LIMIT 10;

-- 结果按相关性排序，最相关的文档排在前面。

+------+-----------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                     |
+------+-----------------------------------------------------------------------------------------------------------+
|    1 | イヤホン bluetooth ワイヤレスイヤホン                                                                         |
|    6 | Lightweight Bluetooth Earbuds with 48 Hours Playtime                                                      |
|    2 | 完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0                                                           |
|    3 | ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD                                               |
|    5 | ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル                                            |
+------+-----------------------------------------------------------------------------------------------------------+

-- 试试用另一种语言搜索：
SELECT * FROM stock_items
    WHERE fts_match_word("蓝牙耳机", title)
    ORDER BY fts_match_word("蓝牙耳机", title)
    DESC LIMIT 10;

-- 结果按相关性排序，最相关的文档排在前面。

+------+---------------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                         |
+------+---------------------------------------------------------------------------------------------------------------+
|   14 | 无线蓝牙耳机超长续航42小时快速充电 流光金属耳机                                                                      |
|   11 | 无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）                                                |
|   15 | 皎月银 国家补贴 心率血氧监测 蓝牙通话 智能手表 男女表                                                                 |
+------+---------------------------------------------------------------------------------------------------------------+
```

**示例：统计匹配用户查询的文档数量**

```sql
SELECT COUNT(*) FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title);

+----------+
| COUNT(*) |
+----------+
|        5 |
+----------+
```

## 高级示例：将搜索结果与其他表连接

你可以将全文搜索与其他 SQL 功能（如连接和子查询）结合使用。

假设你有 `users` 表和 `tickets` 表，想根据用户姓名的全文搜索结果找到对应的工单：

```sql
CREATE TABLE users(
    id INT,
    name TEXT,
    FULLTEXT INDEX (name) WITH PARSER STANDARD
);

INSERT INTO users VALUES (1, "Alice Smith");
INSERT INTO users VALUES (2, "Bob Johnson");

CREATE TABLE tickets(
    id INT,
    title TEXT,
    author_id INT
);

INSERT INTO tickets VALUES (1, "Ticket 1", 1);
INSERT INTO tickets VALUES (2, "Ticket 2", 1);
INSERT INTO tickets VALUES (3, "Ticket 3", 2);
```

你可以用子查询找到匹配的用户 ID，然后在外层查询中使用这些 ID 来检索和连接相关的工单信息：

```sql
SELECT t.title AS TICKET_TITLE, u.id AS AUTHOR_ID, u.name AS AUTHOR_NAME FROM tickets t
LEFT JOIN users u ON t.author_id = u.id
WHERE t.author_id IN
(
    SELECT id FROM users
    WHERE fts_match_word("Alice", name)
);

+--------------+-----------+--------------+
| TICKET_TITLE | AUTHOR_ID | AUTHOR_NAME  |
+--------------+-----------+--------------+
| Ticket 1     |         1 | Alice Smith  |
| Ticket 2     |         1 | Alice Smith  |
+--------------+-----------+--------------+
```

## 相关链接

- [Hybrid Search](/tidb-cloud/vector-search-hybrid-search.md)

## 反馈与帮助

全文搜索仍处于早期阶段，访问权限有限。如果你希望在尚未支持的区域试用全文搜索，或有反馈或需要帮助，欢迎联系我们：

<CustomContent platform="tidb">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [加入我们的 Discord](https://discord.gg/zcqexutz2R)
- [访问我们的支持门户](https://tidb.support.pingcap.com/)

</CustomContent>