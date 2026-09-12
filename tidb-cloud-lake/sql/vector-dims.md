---
title: VECTOR_DIMS
summary: 返回向量的维度（元素个数）。
---

# VECTOR_DIMS

返回向量的维度（元素个数）。

## 语法 {#syntax}

```sql
VECTOR_DIMS(vector)
```

## 参数 {#arguments}

- `vector`：输入向量（VECTOR Data Type）

## 返回值 {#returns}

返回一个 `INT` 值，表示向量中的维度数（元素个数）。

## 描述 {#description}

`VECTOR_DIMS` 函数返回向量的维度，即其包含的元素个数。此函数适用于以下场景：

- 在执行操作前验证向量维度
- 需要维度信息的动态向量处理
- 使用向量数据进行调试和数据探索
- 确保计算中向量之间的兼容性

> **注意：**
>
> 此函数在 {{{ .lake }}} 内执行向量计算，不依赖外部 API。

## 示例 {#examples}

```sql
SELECT
    VECTOR_DIMS([1,2]::VECTOR(2)) AS dims_2d,
    VECTOR_DIMS([1,2,3]::VECTOR(3)) AS dims_3d,
    VECTOR_DIMS([1,2,3,4,5]::VECTOR(5)) AS dims_5d;
```

结果：

```
┌─────────┬─────────┬─────────┐
│ dims_2d │ dims_3d │ dims_5d │
├─────────┼─────────┼─────────┤
│       2 │       3 │       5 │
└─────────┴─────────┴─────────┘
```