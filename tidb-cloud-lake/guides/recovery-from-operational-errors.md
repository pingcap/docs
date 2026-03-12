---
title: Recovery from Operational Errors
---
import IndexOverviewList from '@site/src/components/IndexOverviewList';

# Recovery from Operational Errors

This guide provides step-by-step instructions for recovering from common operational errors in Databend.

## Introduction

Databend can help you recover from these common operational errors:
- **Accidentally dropped databases**
- **Accidentally dropped tables**
- **Incorrect data modifications (UPDATE/DELETE operations)**
- **Accidentally truncated tables**
- **Data loading mistakes**
- **Schema evolution rollbacks** (reverting table structure changes)
- **Dropped columns or constraints**

These recovery capabilities are powered by Databend's FUSE engine with its Git-like storage design, which maintains snapshots of your data at different points in time.

## Recovery Scenarios and Solutions

### Scenario: Accidentally Dropped Database

If you've accidentally dropped a database, you can restore it using the `UNDROP DATABASE` command:

1. Identify the dropped database:

    ```sql
   SHOW DROP DATABASES LIKE '%sales_data%';
    ```

2. Restore the dropped database:

   ```sql
   UNDROP DATABASE sales_data;
   ```

3. Verify the database has been restored:

   ```sql
   SHOW DATABASES;
   ```

4. Restore ownership (if needed):

   ```sql
   GRANT OWNERSHIP on sales_data.* to ROLE <role_name>;
   ```

**Important**: A dropped database can only be restored within the retention period (default is 24 hours).

For more details, see [UNDROP DATABASE](/sql/sql-commands/ddl/database/undrop-database) and [SHOW DROP DATABASES](/sql/sql-commands/ddl/database/show-drop-databases).

### Scenario: Accidentally Dropped Table

If you've accidentally dropped a table, you can restore it using the `UNDROP TABLE` command:

1. Identify the dropped table:

   ```sql
   SHOW DROP TABLES LIKE '%order%';
   ```

2. Restore the dropped table:

   ```sql
   UNDROP TABLE sales_data.orders;
   ```

3. Verify the table has been restored:

   ```sql
   SHOW TABLES FROM sales_data;
   ```

4. Restore ownership (if needed):

   ```sql
   GRANT OWNERSHIP on sales_data.orders to ROLE <role_name>;
   ```

**Important**: A dropped table can only be restored within the retention period (default is 24 hours).

For more details, see [UNDROP TABLE](/sql/sql-commands/ddl/table/ddl-undrop-table) and [SHOW DROP TABLES](/sql/sql-commands/ddl/table/show-drop-tables).

### Scenario: Incorrect Data Updates or Deletions

If you've accidentally modified or deleted data in a table, you can restore it to a previous state using the `FLASHBACK TABLE` command:

1. Identify the snapshot ID or timestamp before the incorrect operation:

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

2. Restore the table to the previous state:

```sql
   -- Using snapshot ID
ALTER TABLE sales_data.orders FLASHBACK TO (SNAPSHOT => 'c5c538d6b8bc42f483eefbddd000af7d');

-- Or using timestamp
ALTER TABLE sales_data.orders FLASHBACK TO (TIMESTAMP => '2023-04-19 04:20:25.062854'::TIMESTAMP);
```

3. Verify the data has been restored:

```sql
SELECT * FROM sales_data.orders LIMIT 3;
```

**Important**: Flashback operations are only possible for existing tables and within the retention period.

For more details, see [FLASHBACK TABLE](/sql/sql-commands/ddl/table/flashback-table).

### Scenario: Schema Evolution Rollbacks
If you've made unwanted changes to a table's structure, you can revert to the previous schema:

1. Create a table and add some data:

```sql
CREATE OR REPLACE TABLE customers (id INT, name VARCHAR, email VARCHAR);
INSERT INTO customers VALUES (1, 'John', 'john@example.com');
```

2. Make schema changes:
```sql
ALTER TABLE customers ADD COLUMN phone VARCHAR;
DESC customers;
```

Output:
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

3. Find the snapshot ID from before the schema change:
```sql
SELECT * FROM fuse_snapshot('default', 'customers');
```

Output:
```text
snapshot_id: 01963cefafbb785ea393501d2e84a425  timestamp: 2025-04-16 04:51:03.227000  previous_snapshot_id: 01963ce9cc29735b87886a08d3ca7e2f
snapshot_id: 01963ce9cc29735b87886a08d3ca7e2f  timestamp: 2025-04-16 04:44:37.289000  previous_snapshot_id: NULL
```

4. Revert to the previous schema (using the earlier snapshot):
```sql
ALTER TABLE customers FLASHBACK TO (SNAPSHOT => '01963ce9cc29735b87886a08d3ca7e2f');
```

5. Verify the schema has been restored:
```sql 
DESC customers;
```
Output:
```text
┌─────────┬─────────┬──────┬─────────┬─────────┐
│ Field   │ Type    │ Null │ Default │ Extra   │
├─────────┼─────────┼──────┼─────────┼─────────┤
│ id      │ INT     │ YES  │ NULL    │         │
│ name    │ VARCHAR │ YES  │ NULL    │         │
│ email   │ VARCHAR │ YES  │ NULL    │         │
└─────────┴─────────┴──────┴─────────┴─────────┘
```


## Important Considerations and Limitations

- **Time Constraints**: Recovery only works within the retention period (default: 24 hours).
- **Name Conflicts**: Cannot undrop if an object with the same name exists — [rename database](/sql/sql-commands/ddl/database/ddl-alter-database) or [rename table](/sql/sql-commands/ddl/table/ddl-rename-table) first.
- **Ownership**: Ownership isn't automatically restored—manually grant it after recovery.
- **Transient Tables**: Flashback doesn't work for transient tables (no snapshots stored).

**For Emergency Situations**: Facing critical data loss? Contact Databend Support immediately for help.
[Contact Databend Support](https://www.databend.com/contact-us/)
