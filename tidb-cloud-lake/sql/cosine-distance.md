---
title: COSINE_DISTANCE
summary: 在 {{{ .lake }}} 中使用 cosine_distance 函数衡量相似性。
---

# COSINE_DISTANCE

计算两个向量之间的余弦距离，用于衡量它们有多不相似。

## 语法 {#syntax}

```sql
COSINE_DISTANCE(vector1, vector2)
```

## 参数 {#arguments}

- `vector1`: 第一个向量（VECTOR 数据类型）
- `vector2`: 第二个向量（VECTOR 数据类型）

## 返回值 {#returns}

返回一个介于 0 和 1 之间的 FLOAT 值：

- 0：向量相同（完全相似）
- 1：向量正交（完全不相似）

## 描述 {#description}

余弦距离基于两个向量之间的夹角来衡量它们的不相似程度，而与它们的大小无关。该函数会：

1. 验证两个输入向量的长度是否相同
2. 计算两个向量对应元素乘积之和（点积）
3. 计算每个向量平方和的平方根（向量模长）
4. 返回 `1 - (dot_product / (magnitude1 * magnitude2))`

实现的数学公式为：

```
cosine_distance(v1, v2) = 1 - (Σ(v1ᵢ * v2ᵢ) / (√Σ(v1ᵢ²) * √Σ(v2ᵢ²)))
```

其中，v1ᵢ 和 v2ᵢ 是输入向量中的元素。

> **注意：**
>
> 此函数在 {{{ .lake }}} 内部执行向量计算，不依赖外部 API。

## 示例 {#examples}

### 基本用法 {#basic-usage}

```sql
-- Calculate cosine distance between two vectors
SELECT COSINE_DISTANCE([1.0, 2.0, 3.0]::vector(3), [4.0, 5.0, 6.0]::vector(3)) AS distance;
```

结果：

```
╭─────────────╮
│   distance  │
├─────────────┤
│ 0.025368214 │
╰─────────────╯
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

查找与 [1, 2, 3] 最相似的向量：

```sql
SELECT
    id,
    vec,
    COSINE_DISTANCE(vec, [1.0000, 2.0000, 3.0000]::VECTOR(3)) AS distance
FROM
    vectors
ORDER BY
    distance ASC;
```

```
╭────────────────────────────────────╮
│ id │    vec    │      distance     │
├────┼───────────┼───────────────────┤
│  1 │ [1,2,3]   │ 0.000000059604645 │
│  2 │ [1,2.2,3] │     0.00096315145 │
│  3 │ [4,5,6]   │       0.025368214 │
╰────────────────────────────────────╯
```