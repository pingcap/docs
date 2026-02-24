---
title: Periodically Delete Data Using TTL (Time to Live)
summary: Learn how to use the TTL feature of TiDB to automatically and periodically delete expired data.
---

# Periodically Delete Data Using TTL (Time to Live)

In application development, some data is only valuable for a limited period of time. For example, verification codes typically need to be retained for only a few minutes, short links might be valid only during a specific campaign, and access logs or intermediate computation results are often kept for just a few months.

TiDB provides the [TTL (Time to Live)](/time-to-live.md) feature, which helps you manage the lifetime of TiDB data at the row level. With TTL, you can **automatically and periodically** remove expired data without writing complex scheduled cleanup scripts.

## Use cases

TTL is designed for scenarios where data no longer has business value after a certain period of time. Typical use cases include the following:

- Periodically deleting verification codes and short URL records
- Periodically cleaning up outdated historical orders
- Automatically removing intermediate computation results

> **Note:**
>
> TTL jobs run periodically in the background. Therefore, expired data is not guaranteed to be deleted immediately after it reaches its expiration time.

## Quick start

You can configure the TTL attribute when creating a table, or add it to an existing table. The following sections provide basic examples of how to use TTL to periodically delete expired data. For complete examples, usage restrictions, and compatibility details with other tools or features, see [TTL (Time to Live)](/time-to-live.md).

### Create a table with TTL

To create a table named `app_messages` for storing instant messages and automatically delete messages three months after their creation, execute the following statement:

```sql
CREATE TABLE app_messages (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    msg_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) TTL = `created_at` + INTERVAL 3 MONTH;
```

In this example, `TTL = ...` defines the expiration policy. The `created_at` column records the creation time of each row, and `INTERVAL 3 MONTH` specifies that each row is retained for a maximum of three months.

### Configure the TTL attribute for an existing table

If you already have a table named `app_logs` and want to enable automatic cleanup (for example, retaining only one month of data), execute the following statement:

```sql
ALTER TABLE app_logs TTL = `created_at` + INTERVAL 1 MONTH;
```

### Modify the TTL period

To modify the retention period for the `app_logs` table, execute the following statement:

```sql
ALTER TABLE app_logs TTL = `created_at` + INTERVAL 6 MONTH;
```

### Disable TTL

To disable TTL for the `app_logs` table, execute the following statement:

```sql
ALTER TABLE app_logs TTL_ENABLE = 'OFF';
```

## See also

- [TTL (Time to Live)](/time-to-live.md)