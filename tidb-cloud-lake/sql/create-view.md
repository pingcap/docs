---
title: CREATE VIEW
summary: 基于查询创建一个新的视图；逻辑视图不存储任何物理数据，当我们访问逻辑视图时，它会将 sql 转换为子查询格式来完成查询。
---

# CREATE VIEW

基于查询创建一个新的视图；逻辑视图不存储任何物理数据，当我们访问逻辑视图时，它会将 sql 转换为子查询格式来完成查询。

例如，如果你创建了一个逻辑视图：

```sql
CREATE VIEW view_t1 AS SELECT a, b FROM t1;
```

然后执行如下查询：

```sql
SELECT a FROM view_t1;
```

其结果等价于下面的查询：

```sql
SELECT a FROM (SELECT a, b FROM t1);
```

因此，如果你删除了该视图所依赖的表，就会报错，提示原始表不存在。此时，你可能需要删除旧视图并重新创建所需的新视图。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] VIEW [ IF NOT EXISTS ] [ db. ]view_name [ (<column>, ...) ] AS SELECT query
```

## 访问控制要求 {#access-control-requirements}

要访问视图，用户只需要拥有该视图本身的 SELECT 权限。

不需要对视图的底层表单独授予权限。该机制简化了访问控制并增强了数据安全性。

## 示例 {#examples}

```sql
CREATE VIEW tmp_view(c1, c2) AS SELECT number % 3 AS a, avg(number) FROM numbers(1000) GROUP BY a ORDER BY a;

SELECT * FROM tmp_view;
+------+-------+
| c1   | c2    |
+------+-------+
|    0 | 499.5 |
|    1 | 499.0 |
|    2 | 500.0 |
+------+-------+
```