---
title: FUSE_ENCODING
summary: テーブル内の特定のカラムに適用されているエンコーディングの種類を返します。これにより、データがテーブル内でどのように圧縮され、ネイティブ形式で保存されているかを理解できます。
---

# FUSE_ENCODING

テーブル内の特定のカラムに適用されているエンコーディングの種類を返します。これにより、データがテーブル内でどのように圧縮され、ネイティブ形式で保存されているかを理解できます。

## 構文 {#syntax}

```sql
FUSE_ENCODING('<database_name>', '<table_name>', '<column_name>')
```

この関数は、次のカラムを持つ結果セットを返します。

| カラム            | データ型          | 説明                                                                                                                                                                                     |
|-------------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| VALIDITY_SIZE     | Nullable(UInt32) | カラム内の各行が非 null 値を持つかどうかを示すビットマップ値のサイズです。このビットマップは、カラムデータ内における null 値の有無を追跡するために使用されます。 |
| COMPRESSED_SIZE   | UInt32           | 圧縮後のカラムデータのサイズです。                                                                                                                                                       |
| UNCOMPRESSED_SIZE | UInt32           | エンコーディングを適用する前のカラムデータのサイズです。                                                                                                                                 |
| LEVEL_ONE         | String           | カラムに適用される主要な、または最初のエンコーディングです。                                                                                                                            |
| LEVEL_TWO         | Nullable(String) | 最初のエンコーディングの後にカラムへ適用される、二次的または再帰的なエンコーディング方式です。                                                                                          |

## 例 {#examples}

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