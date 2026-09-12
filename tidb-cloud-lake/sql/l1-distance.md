---
title: L1_DISTANCE
summary: 计算两个向量之间的曼哈顿（L1）距离，即对应元素绝对差之和。
---

# L1_DISTANCE

计算两个向量之间的曼哈顿（L1）距离，即对应元素绝对差之和。

## 语法 {#syntax}

```sql
L1_DISTANCE(vector1, vector2)
```

## 参数 {#arguments}

- `vector1`：第一个向量（VECTOR 数据类型）
- `vector2`：第二个向量（VECTOR 数据类型）

## 返回值 {#returns}

返回一个 FLOAT 值，表示两个向量之间的曼哈顿（L1）距离。该值始终为非负数：

- 0：两个向量相同
- 更大的值：两个向量距离更远

## 描述 {#description}

L1 距离也称为曼哈顿距离或出租车距离，用于计算两个向量对应元素绝对差的总和。它适用于特征比较和稀疏数据分析。

公式：`L1_DISTANCE(a, b) = |a1 - b1| + |a2 - b2| + ... + |an - bn|`

## 示例 {#examples}

### 基本用法 {#basic-usage}

```sql
-- Calculate L1 distance between two vectors
SELECT L1_DISTANCE([1.0, 2.0, 3.0]::vector(3), [4.0, 5.0, 6.0]::vector(3)) AS distance;
```

结果：

```
╭──────────╮
│ distance │
├──────────┤
│        9 │
╰──────────╯
```

创建一个包含向量数据的表：

```sql
CREATE OR REPLACE TABLE vectors (
    id INT,
    vec VECTOR(3)
);

INSERT INTO vectors VALUES
    (1, [1.0000, 2.0000, 3.0000]),
    (2, [1.0000, 2.2000, 3.0000]),
    (3, [4.0000, 5.0000, 6.0000]);
```

使用 L1 距离查找最接近 [1, 2, 3] 的向量：

```sql
SELECT
    id,
    vec,
    L1_DISTANCE(vec, [1.0000, 2.0000, 3.0000]::VECTOR(3)) AS distance
FROM
    vectors
ORDER BY
    distance ASC;
```

```
╭─────────────────────────────╮
│ id │    vec    │  distance  │
├────┼───────────┼────────────┤
│  1 │ [1,2,3]   │          0 │
│  2 │ [1,2.2,3] │ 0.20000005 │
│  3 │ [4,5,6]   │          9 │
╰─────────────────────────────╯
```