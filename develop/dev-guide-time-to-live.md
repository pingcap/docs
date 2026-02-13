---
title: Regularly Delete Expired Data Using TTL (Time to Live)
summary: Learn how to leverage TiDB's TTL feature to automatically and periodically delete expired data.
---

# Regularly Delete Expired Data Using TTL (Time to Live)

In application development, some data is only valuable for a specific period. For example, verification codes typically only need to be kept for a few minutes, short links might only be valid during an event, and access logs or intermediate calculation results often only need to be stored for a few months.

TiDB's [TTL (Time to Live)](/time-to-live.md) feature provides a row-level lifecycle control policy that helps you **automatically and periodically** delete this expired data without the need to write complex scheduled task scripts.

## Applicable Scenarios

TTL is designed to address the data cleanup problem of "data that no longer has business value after expiration" and is suitable for the following scenarios:

- Periodically deleting verification codes and short URL records
- Periodically deleting unnecessary historical orders
- Automatically deleting intermediate calculation results

> **Note:**
>
> TTL tasks are executed periodically in the background, so there is no guarantee that data will be deleted immediately after expiration.

## Quick Start

You can configure the TTL attribute directly when creating a table, or you can modify an existing table. The following sections list basic examples of using TTL to regularly delete expired data. For complete examples, TTL usage limitations, and TTL compatibility with other tools or features, please refer to [TTL (Time to Live)](/time-to-live.md).

### Creating a Table with TTL

To create a table `app_messages` for storing instant messages, and you want messages to be automatically deleted 3 months after creation, you can execute the following statement:

```sql
CREATE TABLE app_messages (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    msg_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) TTL = `created_at` + INTERVAL 3 MONTH;
```

Here, `TTL = ...` is used to define the expiration policy, `created_at` represents the creation time of the data, and `INTERVAL 3 MONTH` sets the maximum survival time of rows in the table to 3 months.

### Adding TTL to an Existing Table

If you already have a table named `app_logs` and need to add automatic cleanup functionality to it (e.g., keeping data for only 1 month), you can execute the following statement:

```sql
ALTER TABLE app_logs TTL = `created_at` + INTERVAL 1 MONTH;
```

### Adjusting the TTL Duration

To adjust the TTL duration for the table `app_logs`, you can execute the following statement:

```sql
ALTER TABLE app_logs TTL = `created_at` + INTERVAL 6 MONTH;
```

### Disabling the TTL Feature

To disable the TTL feature for the table `app_logs`, you can execute the following statement:

```sql
ALTER TABLE app_logs TTL_ENABLE = 'OFF';
```

## See Also

- [TTL (Time to Live)](/time-to-live.md)