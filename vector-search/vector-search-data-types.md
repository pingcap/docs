---
title: Vector Data Types
summary: 了解 TiDB 中的 Vector 数据类型。
---

# Vector Data Types

向量是浮点数的序列，例如 `[0.3, 0.5, -0.1, ...]`。TiDB 提供了专门优化的 Vector 数据类型，旨在高效存储和查询广泛应用于 AI 领域的向量嵌入。

<CustomContent platform="tidb">

> **Warning:**
>
> 该功能处于实验阶段。不建议在生产环境中使用。此功能可能会在不提前通知的情况下进行更改。如发现 bug，可以在 [issue](https://github.com/pingcap/tidb/issues) 上向 GitHub 报告。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 该功能处于测试版，可能会在不提前通知的情况下进行更改。如发现 bug，可以在 [issue](https://github.com/pingcap/tidb/issues) 上向 GitHub 报告。

</CustomContent>

> **Note:**
>
> Vector 数据类型在 TiDB Self-Managed、[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 上均可使用。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 及以上（建议使用 v8.5.0 及以上）。

目前可用的 Vector 数据类型如下：

- `VECTOR`：任意维度的单精度浮点数序列。
- `VECTOR(D)`：固定维度 `D` 的单精度浮点数序列。

使用向量数据类型相较于 [`JSON`](/data-type-json.md) 类型具有以下优势：

- 向量索引支持：可以构建 [向量搜索索引](/vector-search/vector-search-index.md) 来加快向量搜索速度。
- 维度强制：可以指定维度，禁止插入不同维度的向量。
- 优化存储格式：向量数据类型针对向量数据进行了优化，提供比 `JSON` 类型更好的空间效率和性能。

## 语法

你可以使用以下语法的字符串来表示一个 Vector 值：

```sql
'[<float>, <float>, ...]'
```

示例：

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR(3)
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]');

INSERT INTO vector_table VALUES (2, NULL);
```

插入格式不正确的向量值会导致错误：

```sql
[tidb]> INSERT INTO vector_table VALUES (3, '[5, ]');
ERROR 1105 (HY000): Invalid vector text: [5, ]
```

在以下示例中，由于在创建表时对 `embedding` 列强制维度为 `3`，插入不同维度的向量会导致错误：

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

关于向量数据类型的函数和操作符，请参见 [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)。

关于构建和使用向量搜索索引的更多信息，请参见 [Vector Search Index](/vector-search/vector-search-index.md)。

## 存储不同维度的向量

你可以通过省略 `VECTOR` 类型中的维度参数，在同一列中存储不同维度的向量：

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 维向量，OK
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 维向量，OK
```

但请注意，不能为此列构建 [向量搜索索引](/vector-search/vector-search-index.md)，因为只能在维度相同的向量之间计算距离。

## 比较

你可以使用 [comparison operators](/functions-and-operators/operators.md)（如 `=`, `!=`, `<`, `>`, `<=`, 和 `>=`）对向量数据类型进行比较。关于向量数据类型的完整比较操作符和函数列表，请参见 [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)。

向量数据类型的比较是逐元素数值比较。例如：

- `[1] < [12]`
- `[1,2,3] < [1,2,5]`
- `[1,2,3] = [1,2,3]`
- `[2,2,3] > [1,2,3]`

不同维度的两个向量采用字典序比较，规则如下：

- 从第一个元素开始逐个元素比较，每个元素按数值比较。
- 第一个不匹配的元素决定哪个向量在字典序上 _更小_ 或 _更大_。
- 如果一个向量是另一个向量的前缀，则较短的向量在字典序上 _更小_。例如，`[1,2,3] < [1,2,3,0]`。
- 长度相同且元素相同的两个向量在字典序上 _相等_。
- 空向量在字典序上 _小于_ 任何非空向量。例如，`[] < [1]`。
- 两个空向量在字典序上 _相等_。

在比较向量常量时，建议先进行 [显式类型转换](#cast)，避免基于字符串值的比较：

```sql
-- 由于给定的是字符串，TiDB 会比较字符串：
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- 显式转换为向量后按向量比较：
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

## 算术操作

向量数据类型支持 `+`（加法）和 `-`（减法）算术操作。但不同维度的向量之间的算术运算不支持，执行会报错。

示例：

```sql
[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]');
+---------------------------------------------+
| VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]') |
+---------------------------------------------+
| [9]                                         |
+---------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]');
+-----------------------------------------------------+
| VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]') |
+-----------------------------------------------------+
| [1,1,1]                                             |
+-----------------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[1,2,3]');
ERROR 1105 (HY000): vectors have different dimensions: 1 and 3
```

## 类型转换

### Vector ⇔ String 之间的转换

使用以下函数可以在 Vector 和 String 之间进行转换：

- `CAST(... AS VECTOR)`：字符串 ⇒ 向量
- `CAST(... AS CHAR)`：向量 ⇒ 字符串
- `VEC_FROM_TEXT`：字符串 ⇒ 向量
- `VEC_AS_TEXT`：向量 ⇒ 字符串

为了提升易用性，如果调用只支持向量数据类型的函数（如向量相关的距离函数），你也可以直接传入符合格式的字符串，TiDB 会自动进行隐式类型转换。

```sql
-- VEC_DIMS 函数只接受 VECTOR 参数，因此可以直接传入字符串进行隐式转换。
[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

-- 也可以显式将字符串转换为向量，再传入 VEC_DIMS：
[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

-- 也可以使用 CAST(... AS VECTOR) 进行显式转换：
[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

在使用支持多类型的操作符或函数时，必须先显式将字符串类型转换为向量类型，然后再传入字符串，否则 TiDB 不会进行隐式转换。例如，在进行比较操作前，必须显式将字符串转换为向量，否则会按字符串值进行比较，而非数值向量。

```sql
-- 由于给定的是字符串，TiDB 会比较字符串：
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- 显式转换为向量后按向量比较：
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

你也可以显式将向量转换为字符串，例如使用 `VEC_AS_TEXT()` 函数：

```sql
-- 字符串先隐式转换为向量，然后再显式转换为字符串，返回标准格式的字符串：
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

关于其他的类型转换函数，请参见 [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)。

### Vector ⇔ 其他数据类型之间的转换

目前，不支持直接在 Vector 和其他数据类型（如 `JSON`）之间进行转换。可以在 SQL 语句中使用 String 作为中间类型进行转换。

注意，存储在表中的向量数据类型列不能通过 `ALTER TABLE ... MODIFY COLUMN ...` 转换为其他数据类型。

## 限制

关于向量数据类型的限制，请参见 [Vector search limitations](/vector-search/vector-search-limitations.md) 和 [Vector index restrictions](/vector-search/vector-search-index.md#restrictions)。

## MySQL 兼容性

向量数据类型为 TiDB 特有，不支持在 MySQL 中使用。

## 相关链接

- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Vector Search Index](/vector-search/vector-search-index.md)
- [Improve Vector Search Performance](/vector-search/vector-search-improve-performance.md)