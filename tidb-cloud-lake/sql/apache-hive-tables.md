---
title: Apache Hive Tables
summary: "{{{ .lake }}} 可以直接查询由 Apache Hive 编目管理的数据，而无需复制数据。将 Hive Metastore 注册为 {{{ .lake }}} catalog，指向存放表数据的对象存储，然后即可像查询原生 {{{ .lake }}} 对象一样查询这些表。"
---

# Apache Hive Tables

{{{ .lake }}} 可以直接查询由 Apache Hive 编目管理的数据，而无需复制数据。将 Hive Metastore 注册为 {{{ .lake }}} catalog，指向存放表数据的对象存储，然后即可像查询原生 {{{ .lake }}} 对象一样查询这些表。

## 快速开始 {#quick-start}

1. **注册 Hive Metastore**

   ```sql
   CREATE CATALOG hive_prod
   TYPE = HIVE
   CONNECTION = (
     METASTORE_ADDRESS = '127.0.0.1:9083'
     URL = 's3://lakehouse/'
     ACCESS_KEY_ID = '<your_key_id>'
     SECRET_ACCESS_KEY = '<your_secret_key>'
   );
   ```

2. **浏览 catalog**

   ```sql
   USE CATALOG hive_prod;
   SHOW DATABASES;
   SHOW TABLES FROM tpch;
   ```

3. **查询 Hive 表**

   ```sql
   SELECT l_orderkey, SUM(l_extendedprice) AS revenue
   FROM tpch.lineitem
   GROUP BY l_orderkey
   ORDER BY revenue DESC
   LIMIT 10;
   ```

## 保持元信息最新 {#keep-metadata-fresh}

Hive schema 或 partition 可能会在 {{{ .lake }}} 之外发生变化。出现这种情况时，请刷新 {{{ .lake }}} 的缓存元信息：

```sql
ALTER TABLE tpch.lineitem REFRESH CACHE;
```

## 数据类型映射 {#data-type-mapping}

查询运行时，{{{ .lake }}} 会自动将 Hive 原语类型转换为最接近的原生类型：

| Hive 类型 | {{{ .lake }}} 类型 |
| --------- | ------------- |
| `BOOLEAN` | [BOOLEAN](/tidb-cloud-lake/sql/boolean.md) |
| `TINYINT`, `SMALLINT`, `INT`, `BIGINT` | [整数型类型](/tidb-cloud-lake/sql/numeric.md#integer-data-types) |
| `FLOAT`, `DOUBLE` | [浮点类型](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) |
| `DECIMAL(p,s)` | [DECIMAL](/tidb-cloud-lake/sql/decimal.md) |
| `STRING`, `VARCHAR`, `CHAR` | [STRING](/tidb-cloud-lake/sql/string.md) |
| `DATE`, `TIMESTAMP` | [DATETIME](/tidb-cloud-lake/sql/datetime.md) |
| `ARRAY<type>` | [ARRAY](/tidb-cloud-lake/sql/array.md) |
| `MAP<key,value>` | [MAP](/tidb-cloud-lake/sql/map.md) |

`STRUCT` 等嵌套结构会通过 [VARIANT](/tidb-cloud-lake/sql/variant.md) 类型呈现。

## 注意事项和限制 {#notes-and-limitations}

- 在 {{{ .lake }}} 中，Hive catalog 为**只读**（写入必须通过兼容 Hive 的引擎完成）。
- 需要能够访问底层对象存储；请使用[连接参数](/tidb-cloud-lake/sql/connection-parameters.md)配置凭证。
- 每当表布局发生变化（例如新增 partition）时，请使用 `ALTER TABLE ... REFRESH CACHE` 以保持查询结果为最新。