---
title: DROP SNAPSHOT TAG
summary: 从 FUSE 表中删除一个已命名的快照标签；如果没有其他标签或保留策略对其进行保护，则该标签引用的快照可以被垃圾回收。
---

# DROP SNAPSHOT TAG

从 FUSE 表中删除一个已命名的快照标签。删除后，如果没有其他标签或保留策略对其进行保护，则该标签引用的快照将可以被垃圾回收。

> **Note:**
>
> - 这是一个**实验性**功能。使用前请先启用：`SET enable_experimental_table_ref = 1;`。
> - 仅支持 FUSE 引擎表。

## 语法 {#syntax}

```sql
ALTER TABLE [<database_name>.]<table_name> DROP TAG <tag_name>
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| tag_name  | 要删除的快照标签名称。如果该标签不存在，则会返回错误。 |

## 示例 {#examples}

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE t1(a INT, b STRING);
INSERT INTO t1 VALUES (1, 'a'), (2, 'b');

-- Create and then drop a tag
ALTER TABLE t1 CREATE TAG v1_0;
ALTER TABLE t1 DROP TAG v1_0;

-- Querying a dropped tag returns an error
SELECT * FROM t1 AT (TAG => v1_0);
-- Error: tag 'v1_0' not found
```