---
title: ATTACH TABLE
summary: ATTACH TABLE 创建指向现有表数据的只读链接，无需复制数据。
---

# ATTACH TABLE

ATTACH TABLE 创建指向现有表数据的只读链接，无需复制数据。

## 主要特性 {#key-features}

- **零拷贝数据访问**：链接到源数据，无需进行物理数据移动
- **实时更新**：源表中的变更会立即在附加表中可见
- **只读模式**：仅支持 `SELECT` 查询（不支持 `INSERT`、`UPDATE` 或 `DELETE` 操作）
- **列级访问**：可选择仅包含特定列，以提升安全性和性能

## 语法 {#syntax}

```sql
ATTACH TABLE <target_table_name> [ ( <column_list> ) ] '<source_table_data_URI>'
CONNECTION = ( CONNECTION_NAME = '<connection_name>' )
```

### 参数 {#parameters}

- **`<target_table_name>`**：要创建的新附加表名称

- **`<column_list>`**：可选的列列表，用于指定从源表中包含哪些列
    - 省略时，将包含所有列
    - 提供列级安全性和访问控制
    - 示例：`(customer_id, product, amount)`

- **`<source_table_data_URI>`**：对象存储中源表数据的路径
    - 格式：`s3://<bucket-name>/<database_ID>/<table_ID>/`
    - 示例：`s3://lake-toronto/1/23351/`

- **`CONNECTION_NAME`**：引用通过 [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) 创建的连接

### 查找源表路径 {#finding-the-source-table-path}

使用 [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) 函数获取数据库和表 ID：

```sql
SELECT snapshot_location FROM FUSE_SNAPSHOT('default', 'employees');
-- Result contains: 1/23351/_ss/... → Path is s3://your-bucket/1/23351/
```

## 数据共享优势 {#data-sharing-benefits}

### 工作原理 {#how-it-works}

```
                对象存储 (S3, MinIO, Azure 等)
                         ┌─────────────┐
                         │   源数据     │
                         └──────┬──────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   市场团队   │         │  财务团队     │         │  销售团队    │
│    视图     │          │   视图        │           │   视图      │
└─────────────┘         └─────────────┘         └─────────────┘
```

### 主要优势 {#key-advantages}

| 传统方式 | {{{ .lake }}} ATTACH TABLE |
|---------------------|----------------------|
| 多份数据副本 | 所有人共享单一副本 |
| ETL 延迟、同步问题 | 实时，始终为最新 |
| 维护复杂 | 零维护 |
| 副本越多，安全风险越高 | 细粒度列访问 |
| 因数据移动而变慢 | 在原始数据上进行完整优化 |

### 安全性和性能 {#security-and-performance}

- **列级安全性**：团队只能看到其所需的列
- **实时更新**：源数据变更会立即在所有附加表中可见
- **强一致性**：始终看到完整的数据快照，而不是部分修改
- **完整性能**：继承源表的所有索引和优化能力

## 示例 {#examples}

### 基本用法 {#basic-usage}

```sql
-- Step 1: Create a connection to your storage
CREATE CONNECTION my_s3_connection
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your_aws_key_id>'
    SECRET_ACCESS_KEY = '<your_aws_secret_key>';

-- Step 2: Attach a table with all columns
ATTACH TABLE population_all_columns 's3://lake-doc/1/16/'
    CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```

### 出于安全考虑选择列 {#column-selection-for-security}

```sql
-- Attach only specific columns for data security
ATTACH TABLE population_selected (city, population) 's3://lake-doc/1/16/'
    CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```

### 使用 IAM Role 身份验证 {#using-iam-role-authentication}

```sql
-- Create a connection using IAM role (more secure than access keys)
CREATE CONNECTION s3_role_connection
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::123456789012:role/lake-role';

-- Attach table using the IAM role connection
ATTACH TABLE population_all_columns 's3://lake-doc/1/16/'
    CONNECTION = (CONNECTION_NAME = 's3_role_connection');
```

### 团队专用视图 {#team-specific-views}

```sql
-- Marketing: Customer behavior analysis
ATTACH TABLE marketing_view (customer_id, product, amount, order_date)
's3://your-bucket/1/23351/'
CONNECTION = (CONNECTION_NAME = 'my_s3_connection');

-- Finance: Revenue tracking (different columns)
ATTACH TABLE finance_view (order_id, amount, profit, order_date)
's3://your-bucket/1/23351/'
CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```