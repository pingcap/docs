---
title: UNPIVOT
summary: UNPIVOT 操作通过将列转换为行来轮转表。
---

# UNPIVOT

`UNPIVOT` 操作通过将列转换为行来轮转表。

它是一种关系运算符，接受两个列（来自表或子查询）以及一个列列表，并为列表中指定的每一列生成一行。在查询中，它位于表名或子查询之后，在 `FROM` 子句中指定。

**另请参阅：** [PIVOT](/tidb-cloud-lake/sql/pivot.md)

## 语法 {#syntax}

```sql
SELECT ...
FROM ...
    UNPIVOT ( <value_column>
    FOR <name_column> IN ( <column_list> ) )

[ ... ]
```

其中：

* `<value_column>`：用于存储从 `<column_list>` 中列提取出的值的列。
* `<name_column>`：用于存储提取这些值所对应列名的列。
* `<column_list>`：要执行 unpivot 的列列表，以逗号分隔。你也可以选择使用 AS 或直接使用字符串字面量为列名提供别名。

## 示例 {#examples}

下面将各个月份的独立列进行 unpivot，为每位员工按月份返回单个销售额值：

### 创建并插入数据 {#creating-and-inserting-data}

```sql
-- Create the unpivoted_monthly_sales table
CREATE TABLE unpivoted_monthly_sales(
  empid INT,
  jan INT,
  feb INT,
  mar INT,
  apr INT
);

-- Insert sales data
INSERT INTO unpivoted_monthly_sales VALUES
  (1, 10400,  8000, 11000, 18000),
  (2, 39500, 90700, 12000,  5300);
```

### 使用 UNPIVOT {#using-unpivot}

```sql
SELECT *
FROM unpivoted_monthly_sales
    UNPIVOT (amount
    FOR month IN (jan as 'Jan', feb AS 'Feb', mar 'MARCH', apr));
```

输出：

```sql
┌──────────────────────────────────────────────────────┐
│      empid      │       month      │      amount     │
├─────────────────┼──────────────────┼─────────────────┤
│               1 │ Jan              │           10400 │
│               1 │ Feb              │            8000 │
│               1 │ MARCH            │           11000 │
│               1 │ apr              │           18000 │
│               2 │ Jan              │           39500 │
│               2 │ Feb              │           90700 │
│               2 │ MARCH            │           12000 │
│               2 │ apr              │            5300 │
└──────────────────────────────────────────────────────┘

```