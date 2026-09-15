---
title: 全文索引
summary: 全文索引（倒排索引）通过将词项映射到文档，在大型文档集合中自动实现极速文本搜索，无需缓慢的全表扫描。
---

# 全文索引

> **注意：**
>
> 想要查看可动手实践的演练？参见 [JSON 与搜索指南](/tidb-cloud-lake/guides/json-search.md)。

## 全文索引：自动实现极速文本搜索 {#full-text-index-automatic-lightning-fast-text-search}

全文索引（倒排索引）通过将词项映射到文档，在大型文档集合中自动实现极速文本搜索，无需缓慢的全表扫描。

## 它解决了什么问题？ {#what-problem-does-it-solve}

大型数据集上的文本搜索操作面临显著的性能挑战：

| 问题 | 影响 | 全文索引解决方案 |
|---------|--------|-------------------------|
| **缓慢的 LIKE 查询** | `WHERE content LIKE '%keyword%'` 扫描整个表 | 直接查找词项，跳过无关文档 |
| **全表扫描** | 每次文本搜索都会读取所有行 | 只读包含搜索词项的文档 |
| **糟糕的搜索体验** | 用户需要等待数秒/数分钟才能获得搜索结果 | 亚秒级搜索响应时间 |
| **搜索能力有限** | 仅支持基本模式匹配 | 高级功能：模糊搜索、相关性评分 |
| **高资源占用** | 文本搜索消耗过多的 CPU/内存 | 索引搜索仅需极少资源 |

**示例**：在 1000 万条日志中搜索 "kubernetes error"。如果没有全文索引，则需要扫描全部 1000 万行。使用全文索引后，可以直接找到约 1000 个匹配文档，几乎瞬间返回结果。

## 工作原理 {#how-it-works}

全文索引会创建从词项到文档的倒排映射：

| 术语 | 文档 ID |
|------|-------------|
| "kubernetes" | 101, 205, 1847 |
| "error" | 101, 892, 1847 |
| "pod" | 205, 1847, 2901 |

当搜索 "kubernetes error" 时，索引会找到同时包含这两个词项的文档（101、1847），而无需扫描整张表。

## 快速设置 {#quick-setup}

```sql
-- Create table with text content
CREATE TABLE logs(id INT, message TEXT, timestamp TIMESTAMP);

-- Create full-text index - automatically indexes new data
CREATE INVERTED INDEX logs_message_idx ON logs(message);

-- One-time refresh needed only for existing data before index creation
REFRESH INVERTED INDEX logs_message_idx ON logs;

-- Search using MATCH function - fully automatic optimization
SELECT * FROM logs WHERE MATCH(message, 'error kubernetes');
```

**自动索引管理**：

- **New Data**：插入时会自动建立索引，无需手动操作
- **Existing Data**：仅对创建索引前已存在的数据需要执行一次刷新
- **Ongoing Maintenance**：{{{ .lake }}} 会自动维护最佳搜索性能

## 搜索函数 {#search-functions}

| 函数 | 用途 | 示例 |
|----------|---------|---------|
| `MATCH(column, 'terms')` | 基本文本搜索 | `MATCH(content, 'database performance')` |
| `QUERY('column:terms')` | 高级查询语法 | `QUERY('title:"full text" AND content:search')` |
| `SCORE()` | 相关性评分 | `SELECT *, SCORE() FROM docs WHERE MATCH(...)` |

## 高级搜索功能 {#advanced-search-features}

### 模糊搜索 {#fuzzy-search}

```sql
-- Find documents even with typos (fuzziness=1 allows 1 character difference)
SELECT * FROM logs WHERE MATCH(message, 'kubernetes', 'fuzziness=1');
```

### 相关性评分 {#relevance-scoring}

```sql
-- Get results with relevance scores, filter by minimum score
SELECT id, message, SCORE() as relevance
FROM logs
WHERE MATCH(message, 'critical error') AND SCORE() > 0.5
ORDER BY SCORE() DESC;
```

### 复杂查询 {#complex-queries}

```sql
-- Advanced query syntax with boolean operators
SELECT * FROM docs WHERE QUERY('title:"user guide" AND content:(tutorial OR example)');
```

## 完整示例 {#complete-example}

本示例演示了如何在 Kubernetes 日志数据上创建全文搜索索引，并使用多种函数进行搜索：

```sql
-- Create a table with a computed column
CREATE TABLE k8s_logs (
    event_id INT,
    event_data VARIANT,
    event_timestamp TIMESTAMP,
    event_message VARCHAR AS (event_data['message']::VARCHAR) STORED
);

-- Create an inverted index on the "event_message" column
CREATE INVERTED INDEX event_message_fulltext ON k8s_logs(event_message);

-- Insert comprehensive sample data
INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (1,
    PARSE_JSON('{
        "message": "Pod scheduled",
        "object_type": "Pod",
        "name": "frontend-1",
        "namespace": "production",
        "node": "node-01",
        "status": "Scheduled"
    }'),
    '2024-04-08T08:00:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (2,
    PARSE_JSON('{
        "message": "Deployment scaled",
        "object_type": "Deployment",
        "name": "backend",
        "namespace": "development",
        "replicas": 3
    }'),
    '2024-04-08T09:15:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (3,
    PARSE_JSON('{
        "message": "Node condition changed",
        "object_type": "Node",
        "name": "node-02",
        "condition": "Ready",
        "status": "True"
    }'),
    '2024-04-08T10:30:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (4,
    PARSE_JSON('{
        "message": "ConfigMap updated",
        "object_type": "ConfigMap",
        "name": "app-config",
        "namespace": "default",
        "change": "data update"
    }'),
    '2024-04-08T11:45:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (5,
    PARSE_JSON('{
        "message": "PersistentVolume claim created",
        "object_type": "PVC",
        "name": "storage-claim",
        "namespace": "storage",
        "status": "Bound",
        "volume": "pv-logs"
    }'),
    '2024-04-08T12:00:00Z');

-- Basic search for events containing "PersistentVolume"
SELECT
  event_id,
  event_message
FROM
  k8s_logs
WHERE
  MATCH(event_message, 'PersistentVolume');

-[ RECORD 1 ]-----------------------------------
     event_id: 5
event_message: PersistentVolume claim created

-- Verify index usage with EXPLAIN
EXPLAIN SELECT event_id, event_message FROM k8s_logs WHERE MATCH(event_message, 'PersistentVolume');

-[ EXPLAIN ]-----------------------------------
Filter
├── output columns: [k8s_logs.event_id (#0), k8s_logs.event_message (#3)]
├── filters: [k8s_logs._search_matched (#4)]
├── estimated rows: 5.00
└── TableScan
    ├── table: default.default.k8s_logs
    ├── output columns: [event_id (#0), event_message (#3), _search_matched (#4)]
    ├── read rows: 1
    ├── read size: < 1 KiB
    ├── partitions total: 5
    ├── partitions scanned: 1
    ├── pruning stats: [segments: <range pruning: 5 to 5>, blocks: <range pruning: 5 to 5, inverted pruning: 5 to 1>]
    ├── push downs: [filters: [k8s_logs._search_matched (#4)], limit: NONE]
    └── estimated rows: 5.00

-- Advanced search with relevance scoring
SELECT
  event_id,
  event_message,
  event_timestamp,
  SCORE()
FROM
  k8s_logs
WHERE
  SCORE() > 0.5
  AND QUERY('event_message:"PersistentVolume claim created"');

-[ RECORD 1 ]-----------------------------------
       event_id: 5
  event_message: PersistentVolume claim created
event_timestamp: 2024-04-08 12:00:00
        score(): 0.86304635

-- Fuzzy search example (handles typos)
SELECT
    event_id, event_message, event_timestamp
FROM
    k8s_logs
WHERE
    match('event_message', 'PersistentVolume claim create', 'fuzziness=1');

-[ RECORD 1 ]-----------------------------------
       event_id: 5
  event_message: PersistentVolume claim created
event_timestamp: 2024-04-08 12:00:00
```

**示例要点：**

- `inverted pruning: 5 to 1` 表示索引将扫描的块数从 5 个减少到 1 个
- 相关性评分有助于根据匹配质量对结果进行排序
- 模糊搜索即使在存在拼写错误时也能找到结果（`create` 与 `created`）

## 最佳实践 {#best-practices}

| 做法 | 好处 |
|----------|---------|
| **为经常搜索的列建立索引** | 为搜索查询中常用的列建立索引 |
| **使用 MATCH 代替 LIKE** | 利用索引自动带来的性能优势 |
| **监控索引使用情况** | 使用 EXPLAIN 验证索引是否被使用 |
| **考虑多个索引** | 不同列可以分别拥有独立的索引 |

## 关键命令 {#essential-commands}

| 命令 | 用途 | 何时使用 |
|---------|---------|-------------|
| `CREATE INVERTED INDEX name ON table(column)` | 创建新的全文索引 | 初始设置时使用 - 对新数据自动生效 |
| `REFRESH INVERTED INDEX name ON table` | 为现有数据建立索引 | 仅对索引创建前已存在的数据执行一次 |
| `DROP INVERTED INDEX name ON table` | 删除索引 | 当不再需要该索引时使用 |

## 重要说明 {#important-notes}

**适合使用全文索引的场景：**

- 大型文本数据集（文档、日志、评论）
- 频繁执行文本搜索操作
- 需要高级搜索功能（模糊搜索、评分）
- 对性能要求较高的搜索应用

**不适合使用的场景：**

- 小型文本数据集
- 仅需要精确字符串匹配
- 很少执行搜索操作

## 索引限制 {#index-limitations}

- 每一列只能属于一个倒排索引
- 在数据插入后需要刷新索引（如果数据在索引创建前已存在）
- 索引数据会占用额外的存储空间

---

*全文索引对于需要在大型文档集合上实现快速、复杂文本搜索能力的应用至关重要。*
