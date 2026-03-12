---
title: How Databend Data Sharing Works
---

## What is Data Sharing?

Different teams need different parts of the same data. Traditional solutions copy data multiple times - expensive and hard to maintain.

Databend's **[ATTACH TABLE](/sql/sql-commands/ddl/table/attach-table)** solves this elegantly: create multiple "views" of the same data without copying it. This leverages Databend's **true compute-storage separation** - whether using cloud storage or on-premise object storage: **store once, access everywhere**.

Think of ATTACH TABLE like computer shortcuts - they point to the original file without duplicating it.

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

## How to Use ATTACH TABLE

**Step 1: Find your data location**
```sql
SELECT snapshot_location FROM FUSE_SNAPSHOT('default', 'company_sales');
-- Result: 1/23351/_ss/... → Data at s3://your-bucket/1/23351/
```

**Step 2: Create team-specific views**
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

**Step 3: Query independently**
```sql
-- Marketing analyzes trends
SELECT product, COUNT(*) FROM marketing_view GROUP BY product;

-- Finance tracks profit
SELECT order_date, SUM(profit) FROM finance_view GROUP BY order_date;
```

## Key Benefits

**Real-Time Updates**: When source data changes, all attached tables see it instantly
```sql
INSERT INTO company_sales VALUES (1001, 501, 'Laptop', 1299.99, 299.99, 'user@email.com', '2025-01-20');
SELECT COUNT(*) FROM marketing_view WHERE order_date = '2024-01-20'; -- Returns: 1
```

**Column-Level Security**: Teams only see what they need - Marketing can't see profit, Finance can't see customer emails

**Strong Consistency**: Never read partial updates, always see complete snapshots - perfect for financial reporting and compliance

**Full Performance**: All indexes work automatically, same speed as regular tables

## Why This Matters

| Traditional Approach | Databend ATTACH TABLE |
|---------------------|----------------------|
| Multiple data copies | Single copy shared by all |
| ETL delays, sync issues | Real-time, always current |
| Complex maintenance | Zero maintenance |
| More copies = more security risk | Fine-grained column access |
| Slower due to data movement | Full optimization on original data |

## How It Works Under the Hood

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

Multiple Databend clusters can execute this flow simultaneously without coordination - true compute-storage separation in action.

ATTACH TABLE represents a fundamental shift: **from copying data for each use case to one copy with many views**. Whether in cloud or on-premise environments, Databend's architecture enables powerful, efficient data sharing while maintaining enterprise-grade consistency and security.
