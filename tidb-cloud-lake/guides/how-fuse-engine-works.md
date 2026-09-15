---
title: Fuse Engine 的工作原理
summary: Fuse Engine 是 {{{ .lake }}} 的核心存储引擎，经过优化，可在云对象存储上高效管理 PB 级数据。默认情况下，在 {{{ .lake }}} 中创建的表会自动使用该引擎（ENGINE=FUSE）。其设计灵感来自 Git，基于快照的设计支持强大的数据版本管理功能（如 Time Travel），并通过高级裁剪和索引提供高查询性能。
---

# Fuse Engine 的工作原理

## Fuse Engine {#fuse-engine}

Fuse Engine 是 {{{ .lake }}} 的核心存储引擎，经过优化，可在**云对象存储**上高效管理 **PB 级**数据。默认情况下，在 {{{ .lake }}} 中创建的表会自动使用该引擎（`ENGINE=FUSE`）。其设计灵感来自 Git，基于快照的设计支持强大的数据版本管理功能（如 Time Travel），并通过高级裁剪和索引提供**高查询性能**。

本文将介绍它的核心概念及其工作原理。

## 核心概念 {#core-concepts}

Fuse Engine 使用三种核心结构来组织数据，这与 Git 的方式类似：

* **Snapshots（类似 Git Commits）：** 不可变引用，通过指向特定的 Segments 来定义表在某一时刻的状态。支持 Time Travel。
* **Segments（类似 Git Trees）：** 由多个 Blocks 组成的集合，并带有用于快速跳过数据（裁剪）的汇总统计信息。可在多个 Snapshots 之间共享。
* **Blocks（类似 Git Blobs）：** 不可变数据文件（Parquet 格式），保存实际的行数据以及详细的列级统计信息，用于细粒度裁剪。

```
                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │               │     │ Previous:     │     │               │
     └───────┬───────┘     │ SNAPSHOT 1    │     └───────┬───────┘
             │             └───────────────┘             │
             │                     │                     │
             │                     ▼                     │
             │             ┌───────────────┐             │
             │             │  SNAPSHOT 1   │             │
             │             │               │             │
             │             └───────────────┘             │
             │                                           │
             ▼                                           ▼
     ┌───────────────┐                           ┌───────────────┐
     │   BLOCK 1     │                           │   BLOCK 2     │
     │ (cloud.txt)   │                           │(warehouse.txt)│
     └───────────────┘                           └───────────────┘
```

## 写入如何工作 {#how-writing-works}

当你向表中添加数据时，Fuse Engine 会创建一条对象链。下面我们分步骤来看这个过程：

### 第 1 步：创建表 {#step-1-create-a-table}

```sql
CREATE TABLE git(file VARCHAR, content VARCHAR);
```

此时，表已经存在，但还不包含任何数据：

```
(Empty table with no data)
```

### 第 2 步：插入第一条数据 {#step-2-insert-first-data}

```sql
INSERT INTO git VALUES('cloud.txt', '2022/05/06, Datalake, Cloud');
```

第一次插入后，Fuse Engine 会创建初始的 snapshot、segment 和 block：

```
         Table HEAD
             │
             ▼
     ┌───────────────┐
     │  SNAPSHOT 1   │
     │               │
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │  SEGMENT A    │
     │               │
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │   BLOCK 1     │
     │ (cloud.txt)   │
     └───────────────┘
```

### 第 3 步：插入更多数据 {#step-3-insert-more-data}

```sql
INSERT INTO git VALUES('warehouse.txt', '2022/05/07, Datalake, Warehouse');
```

当插入更多数据时，Fuse Engine 会创建一个新的 snapshot，它同时引用原有的 segment 和一个新的 segment：

```
                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │               │     │ Previous:     │     │               │
     └───────┬───────┘     │ SNAPSHOT 1    │     └───────┬───────┘
             │             └───────────────┘             │
             │                     │                     │
             │                     ▼                     │
             │             ┌───────────────┐             │
             │             │  SNAPSHOT 1   │             │
             │             │               │             │
             │             └───────────────┘             │
             │                                           │
             ▼                                           ▼
     ┌───────────────┐                           ┌───────────────┐
     │   BLOCK 1     │                           │   BLOCK 2     │
     │ (cloud.txt)   │                           │(warehouse.txt)│
     └───────────────┘                           └───────────────┘
```

## 读取如何工作 {#how-reading-works}

当你查询数据时，Fuse Engine 会使用智能裁剪来高效定位所需数据：

```
Query: SELECT * FROM git WHERE file = 'cloud.txt';

                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │    CHECK      │     │               │     │    CHECK      │
     └───────┬───────┘     └───────────────┘     └───────────────┘
             │                                          ✗
             │                                    (Skip - doesn't contain
             │                                     'cloud.txt')
             ▼
     ┌───────────────┐
     │   BLOCK 1     │
     │    CHECK      │
     └───────┬───────┘
             │
             │ ✓ (Contains 'cloud.txt')
             ▼
        Read this block
```

### 智能裁剪过程 {#smart-pruning-process}

```
┌─────────────────────────────────────────┐
│ Query: WHERE file = 'cloud.txt'         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check SEGMENT A                         │
│ Min file value: 'cloud.txt'             │
│ Max file value: 'cloud.txt'             │
│                                         │
│ Result: ✓ Might contain 'cloud.txt'     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check SEGMENT B                         │
│ Min file value: 'warehouse.txt'         │
│ Max file value: 'warehouse.txt'         │
│                                         │
│ Result: ✗ Cannot contain 'cloud.txt'    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check BLOCK 1 in SEGMENT A              │
│ Min file value: 'cloud.txt'             │
│ Max file value: 'cloud.txt'             │
│                                         │
│ Result: ✓ Contains 'cloud.txt'          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Read only BLOCK 1                       │
└─────────────────────────────────────────┘
```

## 基于快照的功能 {#snapshot-based-features}

Fuse Engine 的快照架构支持强大的数据管理能力：

### Time Travel {#time-travel}

查询任意时间点的数据状态。支持数据分支、打标签和治理，并提供完整的审计跟踪与错误恢复能力。

### 零拷贝 Schema Evolution {#zero-copy-schema-evolution}

在**不重写任何底层数据文件**的情况下，修改表结构（添加列、删除列、重命名、修改类型）。

- 这些变更都是仅修改元信息的操作，并记录在新的快照中。
- 该过程是即时的，无需停机，并且避免了高成本的数据迁移任务。旧数据仍可使用其原始 schema 进行访问。

## 用于查询加速的高级索引（Fuse Engine） {#advanced-indexing-for-query-acceleration-fuse-engine}

除了基于统计信息的基本 block/segment pruning 之外，Fuse Engine 还提供了专用的二级索引，以进一步加速特定的查询模式：

| 索引类型          | 简要描述                                         | 可加速的查询类似...                         | 示例查询片段                   |
| :------------------ | :-------------------------------------------------------- | :-------------------------------------------------- | :-------------------------------------- |
| **聚合索引** | 为指定分组预计算聚合结果       | 更快的 `COUNT`、`SUM`、`AVG`... + `GROUP BY`          | `SELECT COUNT(*)... GROUP BY city`      |
| **全文索引** | 用于文本内快速关键字搜索的倒排索引        | 使用 `MATCH` 的文本搜索（例如日志）              | `WHERE MATCH(log_entry, 'error')`     |
| **JSON 索引**      | 为 JSON 文档中的特定路径/键建立索引       | 按特定 JSON 路径/值进行过滤             | `WHERE event_data:user.id = 123`      |
| **布隆过滤器索引** | 使用概率性检查快速跳过不匹配的 block | 快速点查询（`=`）和 `IN` 列表过滤      | `WHERE user_id = 'xyz'` |

## 对比：{{{ .lake }}} Fuse Engine 与 Apache Iceberg {#comparison-lake-fuse-engine-vs-apache-iceberg}

_**注意：** 此对比专门聚焦于**表格式特性**。作为 {{{ .lake }}} 的原生表格式，Fuse 会持续演进，以提升**易用性和性能**。表中展示的是当前特性；后续可能会发生变化。_

| 功能                 | Apache Iceberg                     | {{{ .lake }}} Fuse Engine                 |
| :---------------------- | :--------------------------------- | :----------------------------------- |
| **元信息结构**  | Manifest Lists -> Manifest Files -> Data Files | **快照** -> Segments -> Blocks   |
| **统计级别**   | 文件级（+Partition）            | **多级别**（快照、Segment、Block）→ 更精细的 pruning |
| **裁剪能力**       | 良好（文件/Partition 统计信息）      | **优秀**（多级统计信息 + 二级索引） |
| **Schema Evolution**    | 支持（元信息变更）        | **零拷贝**（仅元信息，即时） |
| **数据聚簇**     | 排序（写入时）     | **自动**优化（后台） |
| **流式支持**   | 基础流式摄取          | **高级增量**（Insert/Update 跟踪） |