---
title: 从操作错误中恢复
summary: 本指南提供了在 {{{ .lake }}} 中从常见操作错误中恢复的分步说明。
---

# 从操作错误中恢复

本指南提供了在 {{{ .lake }}} 中从常见操作错误中恢复的分步说明。

## 简介 {#introduction}

{{{ .lake }}} 可以帮助你从以下常见操作错误中恢复：

- **意外删除数据库**
- **意外删除表**
- **错误的数据修改（UPDATE/DELETE 操作）**
- **意外截断表**
- **数据加载错误**
- **Schema Evolution 回滚**（还原表结构变更）
- **已删除的列或约束**

这些恢复能力由 {{{ .lake }}} 的 FUSE 引擎提供支持。该引擎采用类似 Git 的存储设计，可维护数据在不同时间点的快照。

## 恢复场景与解决方案 {#recovery-scenarios-and-solutions}

### 场景：意外删除数据库 {#scenario-accidentally-dropped-database}

如果你意外删除了数据库，可以使用 `UNDROP DATABASE` 命令将其恢复：

1. 确认已删除的数据库：

    ```sql
   SHOW DROP DATABASES LIKE '%sales_data%';
    ```

2. 恢复已删除的数据库：

   ```sql
   UNDROP DATABASE sales_data;
   ```

3. 验证数据库是否已恢复：

   ```sql
   SHOW DATABASES;
   ```

4. 恢复所有权（如有需要）：

   ```sql
   GRANT OWNERSHIP on sales_data.* to ROLE <role_name>;
   ```

> **重要：**
>
> 只能在保留时间内恢复已删除的数据库（默认值为 24 小时）。

更多详情，请参见 [UNDROP DATABASE](/tidb-cloud-lake/sql/undrop-database.md) 和 [SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md)。

### 场景：意外删除表 {#scenario-accidentally-dropped-table}

如果你意外删除了表，可以使用 `UNDROP TABLE` 命令将其恢复：

1. 确认已删除的表：

   ```sql
   SHOW DROP TABLES LIKE '%order%';
   ```

2. 恢复已删除的表：

   ```sql
   UNDROP TABLE sales_data.orders;
   ```

3. 验证表是否已恢复：

   ```sql
   SHOW TABLES FROM sales_data;
   ```

4. 恢复所有权（如有需要）：

   ```sql
   GRANT OWNERSHIP on sales_data.orders to ROLE <role_name>;
   ```

> **重要：**
>
> 只能在保留时间内恢复已删除的表（默认值为 24 小时）。

更多详情，请参见 [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) 和 [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md)。

### 场景：错误的数据修改或删除 {#scenario-incorrect-data-updates-or-deletions}

如果你意外修改或删除了表中的数据，可以使用 `FLASHBACK TABLE` 命令将其恢复到之前的状态：

1. 找出错误操作发生前的快照 ID 或时间戳：

    ```sql
    SELECT * FROM fuse_snapshot('sales_data', 'orders');
    ```

    ```text
    snapshot_id: c5c538d6b8bc42f483eefbddd000af7d
    snapshot_location: 29356/44446/_ss/c5c538d6b8bc42f483eefbddd000af7d_v2.json
    format_version: 2
    previous_snapshot_id: NULL
    [... ...]
    timestamp: 2023-04-19 04:20:25.062854
    ```

2. 将表恢复到之前的状态：

    ```sql
    -- Using snapshot ID
    ALTER TABLE sales_data.orders FLASHBACK TO (SNAPSHOT => 'c5c538d6b8bc42f483eefbddd000af7d');

    -- Or using timestamp
    ALTER TABLE sales_data.orders FLASHBACK TO (TIMESTAMP => '2023-04-19 04:20:25.062854'::TIMESTAMP);
    ```

3. 验证数据是否已恢复：

    ```sql
    SELECT * FROM sales_data.orders LIMIT 3;
    ```

> **重要：**
>
> 仅可对现有表执行 Flashback 操作，且必须在保留时间内进行。

更多详情，请参见 [FLASHBACK TABLE](/tidb-cloud-lake/sql/flashback-table.md)。

### 场景：Schema Evolution 回滚 {#scenario-schema-evolution-rollbacks}

如果你对表结构进行了不需要的更改，可以回退到之前的 schema：

1. 创建表并添加一些数据：

    ```sql
    CREATE OR REPLACE TABLE customers (id INT, name VARCHAR, email VARCHAR);
    INSERT INTO customers VALUES (1, 'John', 'john@example.com');
    ```

2. 进行 schema 更改：

    ```sql
    ALTER TABLE customers ADD COLUMN phone VARCHAR;
    DESC customers;
    ```

    输出：

    ```text
    ┌─────────┬─────────┬──────┬─────────┬─────────┐
    │ Field   │ Type    │ Null │ Default │ Extra   │
    ├─────────┼─────────┼──────┼─────────┼─────────┤
    │ id      │ INT     │ YES  │ NULL    │         │
    │ name    │ VARCHAR │ YES  │ NULL    │         │
    │ email   │ VARCHAR │ YES  │ NULL    │         │
    │ phone   │ VARCHAR │ YES  │ NULL    │         │
    └─────────┴─────────┴──────┴─────────┴─────────┘
    ```

3. 查找 schema 更改之前的 snapshot ID：

    ```sql
    SELECT * FROM fuse_snapshot('default', 'customers');
    ```

    输出：

    ```text
    snapshot_id: 01963cefafbb785ea393501d2e84a425  timestamp: 2025-04-16 04:51:03.227000  previous_snapshot_id: 01963ce9cc29735b87886a08d3ca7e2f
    snapshot_id: 01963ce9cc29735b87886a08d3ca7e2f  timestamp: 2025-04-16 04:44:37.289000  previous_snapshot_id: NULL
    ```

4. 回退到之前的 schema（使用较早的 snapshot）：

    ```sql
    ALTER TABLE customers FLASHBACK TO (SNAPSHOT => '01963ce9cc29735b87886a08d3ca7e2f');
    ```

5. 验证 schema 已恢复：

    ```sql
    DESC customers;
    ```

    输出：

    ```text
    ┌─────────┬─────────┬──────┬─────────┬─────────┐
    │ Field   │ Type    │ Null │ Default │ Extra   │
    ├─────────┼─────────┼──────┼─────────┼─────────┤
    │ id      │ INT     │ YES  │ NULL    │         │
    │ name    │ VARCHAR │ YES  │ NULL    │         │
    │ email   │ VARCHAR │ YES  │ NULL    │         │
    └─────────┴─────────┴──────┴─────────┴─────────┘
    ```

## 重要注意事项和限制 {#important-considerations-and-limitations}

- **时间限制**：恢复仅在保留时间内有效（默认：24 小时）。
- **名称冲突**：如果已存在同名对象，则无法执行 undrop——请先[重命名数据库](/tidb-cloud-lake/sql/alter-database.md)或[重命名表](/tidb-cloud-lake/sql/rename-table.md)。
- **所有权**：所有权不会自动恢复，需要在恢复后手动授予。
- **临时表**：Flashback 不适用于 transient tables（不会存储快照）。

**紧急情况**：遇到严重数据丢失？请立即联系 {{{ .lake }}} Support 寻求帮助。