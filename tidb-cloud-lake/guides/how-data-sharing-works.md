---
title: TiDB Cloud Lake 数据共享的工作原理
summary: 不同团队需要同一份数据中的不同部分。传统方案需要多次复制数据——成本高且难以维护。
---

# TiDB Cloud Lake 数据共享的工作原理

## 什么是数据共享？ {#what-is-data-sharing}

不同团队需要同一份数据中的不同部分。传统方案需要多次复制数据——成本高且难以维护。

{{{ .lake }}} 的 **[ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md)** 优雅地解决了这个问题：无需复制数据，即可为同一份数据创建多个“视图”。这得益于 {{{ .lake }}} 的 **真正的计算存储分离**——无论使用云存储还是本地对象存储，都能实现：**一次存储，随处访问**。

你可以将 ATTACH TABLE 理解为计算机中的快捷方式——它指向原始文件，而不会复制文件本身。

```
                Object Storage (S3, MinIO, Azure, etc.)
                         ┌─────────────┐
                         │ Your Data   │
                         └──────┬──────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ Marketing   │         │  Finance    │         │   Sales     │
│ Team View   │         │ Team View   │         │ Team View   │
└─────────────┘         └─────────────┘         └─────────────┘
```

## 如何使用 ATTACH TABLE {#how-to-use-attach-table}

**步骤 1：找到你的数据位置**

```sql
SELECT snapshot_location FROM FUSE_SNAPSHOT('default', 'company_sales');
-- Result: 1/23351/_ss/... → Data at s3://your-bucket/1/23351/
```

**步骤 2：创建团队专属视图**

```sql
-- Marketing: Customer behavior analysis
ATTACH TABLE marketing_view (customer_id, product, amount, order_date)
's3://your-bucket/1/23351/' CONNECTION = (ACCESS_KEY_ID = 'xxx', SECRET_ACCESS_KEY = 'yyy');

-- Finance: Revenue tracking
ATTACH TABLE finance_view (order_id, amount, profit, order_date)
's3://your-bucket/1/23351/' CONNECTION = (ACCESS_KEY_ID = 'xxx', SECRET_ACCESS_KEY = 'yyy');

-- HR: Employee info without salaries
ATTACH TABLE hr_employees (employee_id, name, department)
's3://data/1/23351/' CONNECTION = (...);

-- Development: Production structure without sensitive data
ATTACH TABLE dev_customers (customer_id, country, created_date)
's3://data/1/23351/' CONNECTION = (...);
```

**步骤 3：独立查询**

```sql
-- Marketing analyzes trends
SELECT product, COUNT(*) FROM marketing_view GROUP BY product;

-- Finance tracks profit
SELECT order_date, SUM(profit) FROM finance_view GROUP BY order_date;
```

## 主要优势 {#key-benefits}

**实时修改**：当源数据发生变化时，所有附加表都会立即看到这些变化

```sql
INSERT INTO company_sales VALUES (1001, 501, 'Laptop', 1299.99, 299.99, 'user@email.com', '2025-01-20');
SELECT COUNT(*) FROM marketing_view WHERE order_date = '2024-01-20'; -- Returns: 1
```

**列级安全性**：团队只能看到自己需要的数据——Marketing 看不到 profit，Finance 看不到客户邮箱

**强一致性**：绝不会读到部分修改，始终看到完整快照——非常适合财务报表和合规场景

**完整性能**：所有索引都会自动生效，速度与普通表相同

## 为什么这很重要 {#why-this-matters}

| 传统方式 | {{{ .lake }}} ATTACH TABLE |
|---------------------|----------------------|
| 多份数据副本 | 所有人共享单一副本 |
| ETL 延迟、同步问题 | 实时，始终最新 |
| 维护复杂 | 零维护 |
| 副本越多，安全风险越高 | 细粒度列访问 |
| 因数据移动而变慢 | 在原始数据上完整优化 |

## 底层工作原理 {#how-it-works-under-the-hood}

```
Query: SELECT product, SUM(amount) FROM marketing_view GROUP BY product

┌─────────────────────────────────────────────────────────────────┐
│                    Query Execution Flow                         │
└─────────────────────────────────────────────────────────────────┘

    User Query
        │
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 1. Read Snapshot  │───►│ s3://bucket/1/23351/_ss/            │
│    Metadata       │    │ Get current table state             │
└───────────────────┘    └─────────────────────────────────────┘
        │
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 2. Apply Column   │───►│ Filter: customer_id, product,       │
│    Filter         │    │         amount, order_date          │
└───────────────────┘    └─────────────────────────────────────┘
        │
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 3. Check Stats &  │───►│ • Segment min/max values            │
│    Indexes        │    │ • Bloom filters                     │
└───────────────────┘    │ • Aggregate indexes                 │
        │                └─────────────────────────────────────┘
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 4. Smart Data     │───►│ Skip irrelevant blocks              │
│    Fetching       │    │ Download only needed data from _b/  │
└───────────────────┘    └─────────────────────────────────────┘
        │
        ▼
┌───────────────────┐    ┌─────────────────────────────────────┐
│ 5. Local          │───►│ Full optimization & parallelism     │
│    Execution      │    │ Process with all available indexes  │
└───────────────────┘    └─────────────────────────────────────┘
        │
        ▼
    Results: Product sales summary
```

多个 {{{ .lake }}} 集群可以同时执行这一流程而无需协调——这正是真正的计算存储分离在发挥作用。

ATTACH TABLE 代表了一种根本性的转变：**从为每种使用场景复制数据，转变为一份数据配合多个视图**。无论是在云环境还是本地环境中，{{{ .lake }}} 的架构都能在保持企业级一致性和安全性的同时，实现强大而高效的数据共享。