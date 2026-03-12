---
title: CHANGES
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.410"/>

The CHANGES clause allows querying the change tracking metadata for a table within a defined time interval. Please note that the time interval must fall within the data retention period (defaulted to 24 hours). To define a time interval, use the `AT` keyword to specify a time point as the start of the interval, with the current time being applied as the default end of the interval. If you wish to specify a past time as the end of the interval, use the `END` keyword in conjunction with the `AT` keyword to set the interval.

![alt text](/img/sql/changes.png)

## Syntax

```sql
SELECT ...
FROM ...
   CHANGES ( INFORMATION => { DEFAULT | APPEND_ONLY } )
   AT ( { TIMESTAMP => <timestamp> |
          OFFSET => <time_interval> |
          SNAPSHOT => '<snapshot_id>' |
          STREAM => <stream_name> } )

    [ END ( { TIMESTAMP => <timestamp> |
             OFFSET => <time_interval> |
             SNAPSHOT => '<snapshot_id>' } ) ]
```

| Parameter   | Description                                                                                                                                                                                                                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| INFORMATION | Specifies the type of change tracking metadata to be retrieved. Can be set to either `DEFAULT` or `APPEND_ONLY`. `DEFAULT` returns all DML changes, including inserts, updates, and deletes. When set to `APPEND_ONLY`, only appended rows are returned.                                                                              |
| AT          | Specifies the starting point of the time interval for querying change tracking metadata.                                                                                                                                                                                                                                              |
| END         | Optional parameter specifying the end point of the time interval for querying change tracking metadata. If not provided, the current time is used as the default end point.                                                                                                                                                           |
| TIMESTAMP   | Specifies a specific timestamp as the reference point for querying change tracking metadata.                                                                                                                                                                                                                                          |
| OFFSET      | Specifies a time interval in seconds relative to the current time as the reference point for querying change tracking metadata. It should be in the form of a negative integer, where the absolute value represents the time difference in seconds. For example, `-3600` represents traveling back in time by 1 hour (3,600 seconds). |
| SNAPSHOT    | Specifies a snapshot ID as the reference point for querying change tracking metadata.                                                                                                                                                                                                                                                 |
| STREAM      | Specifies a stream name as the reference point for querying change tracking metadata.                                                                                                                                                                                                                                                 |

## Enabling Change Tracking

The CHANGES clause requires that the Fuse engine option `change_tracking` must be set to `true` on the table. For more information about the `change_tracking` option, see [Fuse Engine Options](/sql/sql-reference/table-engines/fuse#options).

```sql title='Example:'
-- Enable change tracking for table 't'
ALTER TABLE t SET OPTIONS(change_tracking = true);
```

## Examples

This example demonstrates the use of the CHANGES clause, allowing for the tracking and querying of changes made to a table:

1. Create a table to store user profile information and enable change tracking.

```sql
CREATE TABLE user_profiles (
    user_id INT,
    username VARCHAR(255),
    bio TEXT
) change_tracking = true;


INSERT INTO user_profiles VALUES (1, 'john_doe', 'Software Engineer');
INSERT INTO user_profiles VALUES (2, 'jane_smith', 'Marketing Specialist');
```

2. Create a stream to capture profile updates, then update an exiting profile and insert a new one.

```sql
CREATE STREAM profile_updates ON TABLE user_profiles APPEND_ONLY = TRUE;


UPDATE user_profiles SET bio = 'Data Scientist' WHERE user_id = 1;
INSERT INTO user_profiles VALUES (3, 'alex_wong', 'Data Analyst');
```

3. Query changes in user profiles by the stream.

```sql
-- Return all changes in user profiles captured in the stream
SELECT *
FROM user_profiles
CHANGES (INFORMATION => DEFAULT)
AT (STREAM => profile_updates);

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     user_id     │     username     │        bio        │   change$action  │              change$row_id             │ change$is_update │
├─────────────────┼──────────────────┼───────────────────┼──────────────────┼────────────────────────────────────────┼──────────────────┤
│               1 │ john_doe         │ Data Scientist    │ INSERT           │ 69cffb02264144c384d56f7b6cedee41000000 │ true             │
│               3 │ alex_wong        │ Data Analyst      │ INSERT           │ 59f315c8655c49eab35ba1959e269430000000 │ false            │
│               1 │ john_doe         │ Software Engineer │ DELETE           │ 69cffb02264144c384d56f7b6cedee41000000 │ true             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Return appended rows in user profiles captured in the stream
SELECT *
FROM user_profiles
CHANGES (INFORMATION => APPEND_ONLY)
AT (STREAM => profile_updates);

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     user_id     │     username     │        bio       │ change$action │ change$is_update │              change$row_id             │
├─────────────────┼──────────────────┼──────────────────┼───────────────┼──────────────────┼────────────────────────────────────────┤
│               3 │ alex_wong        │ Data Analyst     │ INSERT        │ false            │ 59f315c8655c49eab35ba1959e269430000000 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

4. Query changes between a snapshot and a timestamp with both the `AT` and `END` keywords.

```sql
-- Step 6: Take a snapshot of the user profile data.
SELECT snapshot_id, timestamp
FROM FUSE_SNAPSHOT('default', 'user_profiles');

┌───────────────────────────────────────────────────────────────┐
│            snapshot_id           │          timestamp         │
├──────────────────────────────────┼────────────────────────────┤
│ 6a11c94433714970895edd38577ac8b0 │ 2024-04-10 02:51:39.422832 │
│ 53dc4750af92423da91c50dcee547cfb │ 2024-04-10 02:51:39.399568 │
│ 910af7424f764891b0c6fa60aa99fc3a │ 2024-04-10 02:50:14.522416 │
│ 1225000916f44819a0d23178b2d0d1af │ 2024-04-10 02:50:14.500417 │
└───────────────────────────────────────────────────────────────┘

SELECT *
FROM user_profiles
CHANGES (INFORMATION => DEFAULT)
AT (SNAPSHOT => '1225000916f44819a0d23178b2d0d1af')
END (TIMESTAMP => '2024-04-10 02:51:39.399568'::TIMESTAMP);

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     user_id     │     username     │          bio         │   change$action  │              change$row_id             │ change$is_update │
├─────────────────┼──────────────────┼──────────────────────┼──────────────────┼────────────────────────────────────────┼──────────────────┤
│               1 │ john_doe         │ Data Scientist       │ INSERT           │ 69cffb02264144c384d56f7b6cedee41000000 │ true             │
│               1 │ john_doe         │ Software Engineer    │ DELETE           │ 69cffb02264144c384d56f7b6cedee41000000 │ true             │
│               2 │ jane_smith       │ Marketing Specialist │ INSERT           │ 3db484ac18174223851dc9de22f6bfec000000 │ false            │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
