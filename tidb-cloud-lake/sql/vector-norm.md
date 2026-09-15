---
title: VECTOR_NORM
summary: 计算向量的 L2 范数（欧几里得范数），它表示向量的长度或大小。
---

# VECTOR_NORM

计算向量的 L2 范数（欧几里得范数），它表示向量的长度或大小。

## 语法 {#syntax}

```sql
VECTOR_NORM(vector)
```

## 参数 {#arguments}

- `vector`：输入向量（VECTOR Data Type）

## 返回值 {#returns}

返回一个 FLOAT 值，表示向量的 L2 范数（大小）。

## 描述 {#description}

`VECTOR_NORM` 函数计算向量的 L2 范数（也称为欧几里得范数），它表示向量在欧几里得空间中的长度或大小。该函数会：

1. 将向量中的每个元素平方
2. 将所有平方值求和
3. 返回该和的平方根

实现的数学公式为：

```
vector_norm(v) = √(Σ(vᵢ²))
```

其中，vᵢ 是输入向量中的各个元素。

向量范数在以下场景中是基础概念：

- 将向量归一化为单位长度
- 在机器学习中度量向量大小
- 计算距离和相似度
- 特征缩放与预处理
- 涉及大小计算的物理学计算

> **注意：**
>
> 此函数在 {{{ .lake }}} 内执行向量计算，不依赖外部 API。

## 示例 {#examples}

```sql
-- Calculate vector magnitude (length)
SELECT
    VECTOR_NORM([3,4]::VECTOR(2)) AS norm_2d,
    VECTOR_NORM([1,2,3]::VECTOR(3)) AS norm_3d,
    VECTOR_NORM([0,0,0]::VECTOR(3)) AS zero_vector;
```

结果：

```
┌─────────┬───────────┬─────────────┐
│ norm_2d │  norm_3d  │ zero_vector │
├─────────┼───────────┼─────────────┤
│     5.0 │ 3.7416575 │         0.0 │
└─────────┴───────────┴─────────────┘
```