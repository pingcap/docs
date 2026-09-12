---
title: FUSE_ENCODING
summary: 返回应用于表中特定列的编码类型。它可帮助你了解数据在表中如何以原生格式被压缩和存储。
---

# FUSE_ENCODING

返回应用于表中特定列的编码类型。它可帮助你了解数据在表中如何以原生格式被压缩和存储。

## 语法 {#syntax}

```sql
FUSE_ENCODING('<database_name>', '<table_name>', '<column_name>')
```

该函数返回一个包含以下列的结果集：

| 列名              | 数据类型         | 描述                                                                                                                                     |
|-------------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| VALIDITY_SIZE     | Nullable(UInt32) | 位图值的大小，该位图用于指示列中每一行是否具有非空值。此位图用于跟踪该列数据中空值的存在或缺失。                                         |
| COMPRESSED_SIZE   | UInt32           | 列数据压缩后的大小。                                                                                                                     |
| UNCOMPRESSED_SIZE | UInt32           | 应用编码前的列数据大小。                                                                                                                 |
| LEVEL_ONE         | String           | 应用于该列的主要或初始编码。                                                                                                             |
| LEVEL_TWO         | Nullable(String) | 在初始编码之后应用于该列的次级或递归编码方法。                                                                                           |

## 示例 {#examples}

```sql
-- Create a table with an integer column 'c' and apply 'Lz4' compression
CREATE TABLE t(c INT) STORAGE_FORMAT = 'native' COMPRESSION = 'lz4';

-- Insert data into the table.
INSERT INTO t SELECT number FROM numbers(2048);

-- Analyze the encoding for column 'c' in table 't'
SELECT LEVEL_ONE, LEVEL_TWO, COUNT(*)
FROM FUSE_ENCODING('default', 't', 'c')
GROUP BY LEVEL_ONE, LEVEL_TWO;

level_one   |level_two|count(*)|
------------+---------+--------+
DeltaBitpack|         |       1|

--  Insert 2,048 rows with the value 1 into the table 't'
INSERT INTO t (c)
SELECT 1
FROM numbers(2048);

SELECT LEVEL_ONE, LEVEL_TWO, COUNT(*)
FROM FUSE_ENCODING('default', 't', 'c')
GROUP BY LEVEL_ONE, LEVEL_TWO;

level_one   |level_two|count(*)|
------------+---------+--------+
OneValue    |         |       1|
DeltaBitpack|         |       1|
```