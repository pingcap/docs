---
title: MARKOV_TRAIN
summary: マルコフモデルを使用してデータセットからパターンを抽出します。
---

# MARKOV_TRAIN

マルコフモデルを使用してデータセットからパターンを抽出します

## 構文 {#syntax}

```sql
MARKOV_TRAIN(<string>)

MARKOV_TRAIN(<order>)(<string>)

MARKOV_TRAIN(<order>, <frequency_cutoff>, <num_buckets_cutoff>, <frequency_add>, <frequency_desaturate>) (<string>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|------------------| ------------------ |
| `string` | 入力 |
| `order` | 文字列生成に使用するマルコフモデルの次数 |
| `frequency-cutoff` | マルコフモデルの頻度カットオフ: 指定した値未満のカウントを持つすべてのバケットを削除します |
| `num-buckets-cutoff` | コンテキストに対する異なる継続候補数のカットオフ: 指定した数未満のバケットを持つすべてのヒストグラムを削除します |
| `frequency-add` | 確率分布の偏りを抑えるため、すべてのカウントに定数を加算します |
| `frequency-desaturate` | 0..1 - 確率分布の偏りを抑えるため、すべての頻度を平均値に近づけます |

## 戻り値の型 {#return-type}

実装によって異なりますが、これは [MARKOV_GENERATE](/tidb-cloud-lake/sql/markov-generate.md) の引数としてのみ使用されます。

## 例 {#examples}

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