---
title: CREATE SNAPSHOT TAG
summary: 在 FUSE 表上创建一个具名快照标签，使你能够为表历史中的特定时间点添加书签并进行查询。
---

# CREATE SNAPSHOT TAG

在 FUSE 表上创建一个具名快照标签。快照标签会为表在某个特定时间点的状态添加书签，使你之后可以通过 [AT](/tidb-cloud-lake/sql/at.md) 子句查询该状态。

> **Note:**
>
> - 这是一个**实验性**功能。使用前请先启用：`SET enable_experimental_table_ref = 1;`。
> - 仅支持 FUSE engine 表。不支持 Memory engine 表和临时表。

## 语法 {#syntax}

```sql
ALTER TABLE [<database_name>.]<table_name> CREATE TAG <tag_name>
    [ AT (
        SNAPSHOT => '<snapshot_id>' |
        TIMESTAMP => <timestamp> |
        STREAM => <stream_name> |
        OFFSET => <time_interval> |
        TAG => <tag_name>
    ) ]
    [ RETAIN <n> { DAYS | SECONDS } ]
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| tag_name  | 标签名称。必须在表内唯一。 |
| AT        | 指定标签引用哪个快照。如果省略，则标签引用当前（最新）快照。支持与 [AT](/tidb-cloud-lake/sql/at.md) 子句相同的选项，另外还支持 `TAG`，用于从现有标签复制。 |
| RETAIN    | 设置自动过期时间。达到指定时长后，标签会在下一次执行 [VACUUM](/tidb-cloud-lake/sql/vacuum-table.md) 操作时被移除。不使用 `RETAIN` 时，标签会一直保留，直到被显式删除。 |

## 示例 {#examples}

### 为当前快照打标签 {#tag-the-current-snapshot}

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE t1(a INT, b STRING);
INSERT INTO t1 VALUES (1, 'a'), (2, 'b'), (3, 'c');

-- Create a tag at the current snapshot
ALTER TABLE t1 CREATE TAG v1_0;

-- Insert more data
INSERT INTO t1 VALUES (4, 'd'), (5, 'e');

-- Query the tagged snapshot (returns 3 rows, not 5)
SELECT * FROM t1 AT (TAG => v1_0) ORDER BY a;
```

### 基于现有引用创建标签 {#tag-from-an-existing-reference}

```sql
-- Copy from an existing tag
ALTER TABLE t1 CREATE TAG v1_0_copy AT (TAG => v1_0);

-- Tag a specific snapshot
ALTER TABLE t1 CREATE TAG before_migration
    AT (SNAPSHOT => 'aaa4857c5935401790db2c9f0f2818be');

-- Tag the state from 1 hour ago
ALTER TABLE t1 CREATE TAG hourly_checkpoint AT (OFFSET => -3600);
```

### 创建带自动过期时间的标签 {#tag-with-automatic-expiration}

```sql
-- Tag expires after 7 days
ALTER TABLE t1 CREATE TAG temp_tag RETAIN 7 DAYS;

-- Tag expires after 3600 seconds
ALTER TABLE t1 CREATE TAG debug_snapshot RETAIN 3600 SECONDS;
```