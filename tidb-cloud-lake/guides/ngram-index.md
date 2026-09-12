---
title: Ngram 索引
summary: Ngram 索引通过使用带有通配符（`%`）的 `LIKE` 运算符来加速模式匹配查询，从而无需全表扫描即可实现快速子字符串搜索。
---

# Ngram 索引

Ngram 索引通过使用带有通配符（`%`）的 `LIKE` 运算符来加速模式匹配查询，从而无需全表扫描即可实现快速子字符串搜索。

## 它解决了什么问题？ {#what-problem-does-it-solve}

在大规模数据集上，使用 `LIKE` 进行模式匹配查询会面临显著的性能挑战：

| 问题 | 影响 | Ngram Index 解决方案 |
|---------|--------|---------------------|
| **缓慢的通配符搜索** | `WHERE content LIKE '%keyword%'` 扫描整个表 | 使用 n-gram 片段预过滤数据块 |
| **全表扫描** | 每次模式搜索都会读取所有行 | 仅读取包含模式的相关数据块 |
| **搜索性能差** | 用户需要长时间等待子字符串搜索结果 | 亚秒级模式匹配响应时间 |
| **传统索引无效** | B-tree 索引无法优化中间通配符 | 字符级索引可处理任意通配符位置 |

**示例**：在 1000 万条日志记录中搜索 `'%error log%'`。如果没有 ngram 索引，需要扫描全部 1000 万行；而使用 ngram 索引时，可以立即将范围预过滤到约 1000 个相关数据块。

## Ngram 与全文索引：何时使用哪一种？ {#ngram-vs-full-text-index-when-to-use-which}

| 功能 | Ngram 索引 | 全文索引 |
|---------|-------------|-----------------|
| **主要使用场景** | 使用 `LIKE '%pattern%'` 进行模式匹配 | 使用 `MATCH()` 进行语义文本搜索 |
| **搜索类型** | 精确子字符串匹配 | 基于词的相关性搜索 |
| **查询语法** | `WHERE column LIKE '%text%'` | `WHERE MATCH(column, 'text')` |
| **高级功能** | 不区分大小写的匹配 | 模糊搜索、相关性评分、布尔运算符 |
| **性能侧重点** | 加速现有的 LIKE 查询 | 用高级搜索函数替换 LIKE |
| **最适合** | 日志分析、代码搜索、精确模式匹配 | 文档搜索、内容发现、搜索引擎 |

**在以下场景中选择 Ngram 索引：**

- 你已有 `LIKE '%pattern%'` 查询需要优化
- 需要精确的子字符串匹配（不区分大小写）
- 处理的是日志、代码或 ID 等结构化数据
- 希望在不修改查询语法的情况下提升性能

**在以下场景中选择全文索引：**

- 为文档或内容构建搜索功能
- 需要模糊搜索、相关性评分或复杂查询
- 处理自然语言文本
- 希望获得超出简单模式匹配的高级搜索能力

## Ngram 索引的工作原理 {#how-ngram-index-works}

Ngram 索引会将文本拆分为重叠的字符子串（n-gram），以便快速查找模式：

**`gram_size = 3` 示例：**

```text
Input: "The quick brown"
N-grams: "The", "he ", "e q", " qu", "qui", "uic", "ick", "ck ", "k b", " br", "bro", "row", "own"
```

**查询处理过程：**

```sql
SELECT * FROM t WHERE content LIKE '%quick br%'
```

1. 将模式 `'quick br'` 分词为 n-gram："qui"、"uic"、"ick"、"ck "、"k b"、" br"
2. 索引过滤出包含这些 n-gram 的数据块
3. 仅对预过滤后的数据块应用完整的 `LIKE` 过滤

> **注意：**
>
> - 模式长度必须至少为 `gram_size` 个字符（例如，当 `gram_size=3` 时，像 `'%yo%'` 这样的短模式不会使用索引）
> - 匹配不区分大小写（"FOO" 可匹配 "foo"、"Foo"、"fOo"）
> - 仅适用于 `LIKE` 运算符，不适用于其他模式匹配函数

## 快速开始 {#quick-setup}

```sql
-- Create table with text content
CREATE TABLE logs(id INT, message STRING);

-- Create ngram index with 3-character segments
CREATE NGRAM INDEX logs_message_idx ON logs(message) gram_size = 3;

-- Insert data (automatically indexed)
INSERT INTO logs VALUES (1, 'Application error occurred');

-- Search using LIKE - automatically optimized
SELECT * FROM logs WHERE message LIKE '%error%';
```

## 完整示例 {#complete-example}

以下示例演示了如何为日志分析创建 ngram 索引，并验证其带来的性能收益：

```sql
-- Create table for application logs
CREATE TABLE t_articles (
    id INT,
    content STRING
);

-- Create ngram index with 3-character segments
CREATE NGRAM INDEX ngram_idx_content
ON t_articles(content)
gram_size = 3;

-- Verify index creation
SHOW INDEXES;
```

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        name       │  type  │ original │            definition            │         created_on         │      updated_on     │
├───────────────────┼────────┼──────────┼──────────────────────────────────┼────────────────────────────┼─────────────────────┤
│ ngram_idx_content │ NGRAM  │          │ t_articles(content)gram_size='3' │ 2025-05-13 01:02:58.598409 │ NULL                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```sql
-- Insert test data: 995 irrelevant rows + 5 target rows
INSERT INTO t_articles
SELECT number, CONCAT('Random text number ', number)
FROM numbers(995);

INSERT INTO t_articles VALUES
    (1001, 'The silence was deep and complete'),
    (1002, 'They walked in silence through the woods'),
    (1003, 'Silence fell over the room'),
    (1004, 'A moment of silence was observed'),
    (1005, 'In silence, they understood each other');

-- Search with pattern matching
SELECT id, content FROM t_articles WHERE content LIKE '%silence%';

-- Verify index usage
EXPLAIN SELECT id, content FROM t_articles WHERE content LIKE '%silence%';
```

**性能结果：**

```sql
-[ EXPLAIN ]-----------------------------------
TableScan
├── table: default.default.t_articles
├── output columns: [id (#0), content (#1)]
├── read rows: 5
├── read size: < 1 KiB
├── partitions total: 2
├── partitions scanned: 1
├── pruning stats: [segments: <range pruning: 2 to 2>, blocks: <range pruning: 2 to 2, bloom pruning: 2 to 1>]
├── push downs: [filters: [is_true(like(t_articles.content (#1), '%silence%'))], limit: NONE]
└── estimated rows: 15.62
```

**关键性能指标：** `bloom pruning: 2 to 1` 表明 ngram 索引在扫描前成功过滤掉了 50% 的数据块。

## 最佳实践 {#best-practices}

| 实践 | 收益 |
|----------|---------|
| **选择合适的 gram_size** | `gram_size=3` 适用于大多数情况；对于更长的模式使用更大的值 |
| **为经常搜索的列建立索引** | 重点关注用于 `LIKE '%pattern%'` 查询的列 |
| **监控索引使用情况** | 使用 `EXPLAIN` 验证 `bloom pruning` 统计信息 |
| **考虑模式长度** | 确保搜索模式的长度至少为 `gram_size` 个字符 |

## 常用命令 {#essential-commands}

完整命令参考请参见 [Ngram 索引](/tidb-cloud-lake/sql/ngram-index-sql.md)。

| 命令                                                  | 用途                                      |
|----------------------------------------------------------|----------------------------------------------|
| `CREATE NGRAM INDEX name ON table(column) gram_size = N` | 创建具有 N 字符分段的 ngram 索引             |
| `SHOW INDEXES`                                           | 列出所有索引，包括 ngram 索引                |
| `REFRESH NGRAM INDEX name ON table`                      | 刷新 ngram 索引                              |
| `DROP NGRAM INDEX name ON table`                         | 删除 ngram 索引                              |

**何时使用 Ngram 索引**

**适用场景：**

- 日志分析和监控系统
- 代码搜索和模式匹配
- 商品目录搜索
- 任何频繁使用 `LIKE '%pattern%'` 查询的应用

**不推荐的场景：**

- 短模式搜索（少于 `gram_size` 个字符）
- 精确字符串匹配（应改用等值比较）
- 复杂文本搜索需求（应改用全文索引）

---

*Ngram 索引对于需要在大型文本数据集上使用 `LIKE` 查询进行快速模式匹配的应用来说至关重要。*
