---
title: system.copy_history
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.823"/>

Contains information about copy history.

## Syntax

```sql
SELECT * FROM copy_history('<table_name>');
```

- `table_name`: The table name.

```sql
select * from copy_history('my_table');

╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                          file_name                          │ content_length │        last_modified       │       etag       │
│                            String                           │     UInt64     │     Nullable(Timestamp)    │ Nullable(String) │
├─────────────────────────────────────────────────────────────┼────────────────┼────────────────────────────┼──────────────────┤
│ data_0199db4c843a70b2b81f115f01c8de97_0000_00000000.parquet │          10531 │ 2025-10-13 02:00:49.083208 │ NULL             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Note that, the results of `system.copy_history` is respected by settings `load_file_metadata_expire_hours` which is 24 hours by default.

