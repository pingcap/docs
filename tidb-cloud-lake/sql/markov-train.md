---
title: MARKOV_TRAIN
summary: 使用 Markov 模型从数据集中提取模式。
---

# MARKOV_TRAIN

使用 Markov 模型从数据集中提取模式

## 语法 {#syntax}

```sql
MARKOV_TRAIN(<string>)

MARKOV_TRAIN(<order>)(<string>)

MARKOV_TRAIN(<order>, <frequency_cutoff>, <num_buckets_cutoff>, <frequency_add>, <frequency_desaturate>) (<string>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|------------------| ------------------ |
| `string` | 输入 |
| `order` | 用于生成字符串的 Markov 模型阶数 |
| `frequency-cutoff` | Markov 模型的频率截断：移除所有计数小于指定值的存储桶 |
| `num-buckets-cutoff` | 上下文可用的不同后续项数量的截断值：移除所有存储桶数量小于指定值的直方图 |
| `frequency-add` | 为每个计数增加一个常数，以降低概率分布偏斜 |
| `frequency-desaturate` | 0..1 - 将每个频率向平均值移动，以降低概率分布偏斜 |

## 返回类型 {#return-type}

根据具体实现，它仅用作 [MARKOV_GENERATE](/tidb-cloud-lake/sql/markov-generate.md) 的参数。

## 示例 {#examples}

```sql
create table model as
select markov_train(concat('bar', number::string)) as bar from numbers(100);

select markov_generate(bar,'{"order":5,"sliding_window_size":8}', 151, (number+100000)::string) as generate
from numbers(5), model;
+-----------+
| generate  |
+-----------+
│ bar95     │
│ bar64     │
│ bar85     │
│ bar56     │
│ bar95     │
+-----------+
```