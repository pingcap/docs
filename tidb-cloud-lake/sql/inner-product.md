---
title: INNER_PRODUCT
summary: 计算两个向量的内积（点积），用于衡量向量之间的相似性和投影关系。
---

# INNER_PRODUCT

计算两个向量的内积（点积），用于衡量向量之间的相似性和投影关系。

## 语法 {#syntax}

```sql
INNER_PRODUCT(vector1, vector2)
```

## 参数 {#arguments}

- `vector1`：第一个向量（VECTOR Data Type）
- `vector2`：第二个向量（VECTOR Data Type）

## 返回值 {#returns}

返回一个 FLOAT 值，表示两个向量的内积。

## 描述 {#description}

内积（也称为点积）用于计算两个向量中对应元素乘积之和。该函数会：

1. 验证两个输入向量的长度是否相同
2. 将两个向量中对应位置的元素相乘
3. 将所有乘积求和，得到一个标量值

其实现的数学公式为：

```
inner_product(v1, v2) = Σ(v1ᵢ * v2ᵢ)
```

其中，v1ᵢ 和 v2ᵢ 是输入向量中的元素。

内积在以下场景中是基础运算：

- 衡量向量相似性（值越大表示方向越相似）
- 计算一个向量在另一个向量上的投影
- 机器学习算法（神经网络、SVM 等）
- 涉及功和能量的物理计算

> **注意：**
>
> 此函数在 {{{ .lake }}} 内执行向量计算，不依赖外部 API。

## 示例 {#examples}

### 基本用法 {#basic-usage}

```sql
SELECT INNER_PRODUCT([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3)) AS inner_product;
```

结果：

```
┌───────────────┐
│ inner_product │
├───────────────┤
│          32.0 │
└───────────────┘
```

### 结合表数据使用 {#working-with-table-data}

创建一个包含向量数据的表：

```sql
CREATE TABLE vector_examples (
    id INT,
    vector_a VECTOR(3),
    vector_b VECTOR(3)
);

INSERT INTO vector_examples VALUES
    (1, [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]),
    (2, [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]),
    (3, [2.0, 3.0, 1.0], [1.0, 2.0, 3.0]);
```

计算内积：

```sql
SELECT
    id,
    vector_a,
    vector_b,
    INNER_PRODUCT(vector_a, vector_b) AS inner_product
FROM vector_examples;
```

结果：

```
┌────┬───────────────┬───────────────┬───────────────┐
│ id │   vector_a    │   vector_b    │ inner_product │
├────┼───────────────┼───────────────┼───────────────┤
│  1 │ [1.0,2.0,3.0] │ [4.0,5.0,6.0] │          32.0 │
│  2 │ [1.0,0.0,0.0] │ [0.0,1.0,0.0] │           0.0 │
│  3 │ [2.0,3.0,1.0] │ [1.0,2.0,3.0] │          11.0 │
└────┴───────────────┴───────────────┴───────────────┘
```

### 向量相似性分析 {#vector-similarity-analysis}

```sql
-- Calculate inner products to measure vector similarity
SELECT
    INNER_PRODUCT([1,0,0]::VECTOR(3), [1,0,0]::VECTOR(3)) AS same_direction,
    INNER_PRODUCT([1,0,0]::VECTOR(3), [0,1,0]::VECTOR(3)) AS orthogonal,
    INNER_PRODUCT([1,0,0]::VECTOR(3), [-1,0,0]::VECTOR(3)) AS opposite;
```

结果：

```
┌────────────────┬─────────────┬──────────┐
│ same_direction │ orthogonal  │ opposite │
├────────────────┼─────────────┼──────────┤
│           1.0  │         0.0 │     -1.0 │
└────────────────┴─────────────┴──────────┘
```