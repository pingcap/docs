---
title: L2_DISTANCE
summary: 计算两个向量之间的欧几里得（L2）距离，用于衡量它们在向量空间中的直线距离。
---

# L2_DISTANCE

计算两个向量之间的欧几里得（L2）距离，用于衡量它们在向量空间中的直线距离。

## 语法 {#syntax}

```sql
L2_DISTANCE(vector1, vector2)
```

## 参数 {#arguments}

- `vector1`：第一个向量（VECTOR 数据类型）
- `vector2`：第二个向量（VECTOR 数据类型）

## 返回值 {#returns}

返回一个 FLOAT 值，表示两个向量之间的欧几里得（L2）距离。该值始终为非负数：

- 0：向量相同
- 更大的值：向量之间距离更远

## 描述 {#description}

L2 距离也称为欧几里得距离，用于衡量欧几里得空间中两点之间的直线距离。它是向量相似度搜索和机器学习应用中最常用的指标之一。

该函数会：

1. 验证两个输入向量的长度是否相同
2. 计算对应元素差值平方的总和
3. 返回该总和的平方根

实现的数学公式为：

```
L2_distance(v1, v2) = √(Σ(v1ᵢ - v2ᵢ)²)
```

其中，v1ᵢ 和 v2ᵢ 是输入向量中的元素。

> **注意：**
>
> - 此函数在 {{{ .lake }}} 内执行向量计算，不依赖外部 API。

## 示例 {#examples}

### 基本用法 {#basic-usage}

```sql
-- Calculate L2 distance between two vectors
SELECT L2_DISTANCE([1.0, 2.0, 3.0]::vector(3), [4.0, 5.0, 6.0]::vector(3)) AS distance;
```

结果：

```
╭──────────╮
│ distance │
├──────────┤
│ 5.196152 │
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

使用 L2 距离查找最接近 [1, 2, 3] 的向量：

```sql
SELECT
    id,
    vec,
    L2_DISTANCE(vec, [1.0000, 2.0000, 3.0000]::VECTOR(3)) AS distance
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
│  3 │ [4,5,6]   │   5.196152 │
╰─────────────────────────────╯
```