---
title: FUSE_TAG
summary: 返回表的快照标签。有关快照标签的更多信息，请参见 Snapshot Tags。
---

# FUSE_TAG

返回表的快照标签。有关快照标签的更多信息，请参见 [快照标签](/tidb-cloud-lake/sql/table-versioning.md#snapshot-tags)。

## 语法 {#syntax}

```sql
FUSE_TAG('<database_name>', '<table_name>')
```

## 输出列 {#output-columns}

| 列名                | 类型               | 描述                                                                 |
|---------------------|--------------------|-----------------------------------------------------------------------------|
| name                | STRING             | 标签名称                                                                    |
| snapshot_location   | STRING             | 该标签指向的快照文件                                             |
| expire_at           | TIMESTAMP (nullable) | 过期时间戳；在 CREATE SNAPSHOT TAG 中使用 `RETAIN` 时设置    |

## 示例 {#examples}

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE mytable(a INT, b INT);

INSERT INTO mytable VALUES(1, 1),(2, 2);

-- Create a snapshot tag
ALTER TABLE mytable CREATE TAG v1;

INSERT INTO mytable VALUES(3, 3);

-- Create another tag with expiration
ALTER TABLE mytable CREATE TAG temp RETAIN 2 DAYS;

SELECT * FROM FUSE_TAG('default', 'mytable');

---
| name | snapshot_location                                          | expire_at                  |
|------|------------------------------------------------------------|----------------------------|
| v1   | 1/319/_ss/a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4_v4.mpk        | NULL                       |
| temp | 1/319/_ss/f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3_v4.mpk        | 2025-06-15 10:30:00.000000 |
```