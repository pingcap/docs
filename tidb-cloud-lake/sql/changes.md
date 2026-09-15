---
title: CHANGES
summary: `CHANGES` 子句允许在定义的时间区间内查询表的变更跟踪元信息。请注意，时间区间必须落在数据保留时间内（默认为 24 小时）。要定义时间区间，可以使用 `AT` 关键字指定某个时间点作为区间起点，区间终点默认使用当前时间。如果希望将过去的某个时间指定为区间终点，请结合使用 `END` 关键字和 `AT` 关键字来设置该区间。
---

# CHANGES

`CHANGES` 子句允许在定义的时间区间内查询表的变更跟踪元信息。请注意，时间区间必须落在数据保留时间内（默认为 24 小时）。要定义时间区间，可以使用 `AT` 关键字指定某个时间点作为区间起点，区间终点默认使用当前时间。如果希望将过去的某个时间指定为区间终点，请结合使用 `END` 关键字和 `AT` 关键字来设置该区间。

![alt text](/media/tidb-cloud-lake/changes.png)

## 语法 {#syntax}

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

| 参数 | 描述 |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| INFORMATION | 指定要检索的变更跟踪元信息类型。可以设置为 `DEFAULT` 或 `APPEND_ONLY`。`DEFAULT` 返回所有 DML 变更，包括插入、修改和删除。设置为 `APPEND_ONLY` 时，仅返回追加的行。 |
| AT          | 指定查询变更跟踪元信息的时间区间起点。 |
| END         | 可选参数，用于指定查询变更跟踪元信息的时间区间终点。如果未提供，则默认使用当前时间作为终点。 |
| TIMESTAMP   | 指定一个特定的时间戳，作为查询变更跟踪元信息的参考点。 |
| OFFSET      | 指定一个相对于当前时间、以秒为单位的时间区间，作为查询变更跟踪元信息的参考点。其形式应为负整数，绝对值表示相差的秒数。例如，`-3600` 表示回到 1 小时前（3,600 秒）。 |
| SNAPSHOT    | 指定一个快照 ID，作为查询变更跟踪元信息的参考点。 |
| STREAM      | 指定一个 stream 名称，作为查询变更跟踪元信息的参考点。 |

## 启用变更跟踪 {#enabling-change-tracking}

`CHANGES` 子句要求表上的 Fuse 引擎选项 `change_tracking` 必须设置为 `true`。有关 `change_tracking` 选项的更多信息，请参见 [Fuse Engine 选项](/tidb-cloud-lake/sql/table-engines.md#available-engines)。

```sql title='Example:'
-- Enable change tracking for table 't'
ALTER TABLE t SET OPTIONS(change_tracking = true);
```

## 示例 {#examples}

以下示例演示了 `CHANGES` 子句的用法，可用于跟踪和查询对表所做的变更：

1. 创建一个用于存储用户资料信息的表，并启用变更跟踪。

    ```sql
    CREATE TABLE user_profiles (
        user_id INT,
        username VARCHAR(255),
        bio TEXT
    ) change_tracking = true;
    
    INSERT INTO user_profiles VALUES (1, 'john_doe', 'Software Engineer');
    INSERT INTO user_profiles VALUES (2, 'jane_smith', 'Marketing Specialist');
    ```

2. 创建一个 stream 来捕获资料更新，然后修改一个现有资料并插入一条新记录。

    ```sql
    CREATE STREAM profile_updates ON TABLE user_profiles APPEND_ONLY = TRUE;
    
    UPDATE user_profiles SET bio = 'Data Scientist' WHERE user_id = 1;
    INSERT INTO user_profiles VALUES (3, 'alex_wong', 'Data Analyst');
    ```

3. 通过该 stream 查询用户资料中的变更。

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

4. 同时使用 `AT` 和 `END` 关键字，查询某个快照与某个时间戳之间的变更。

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