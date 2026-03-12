---
title: MARKOV_TRAIN
---

Extracting patterns from datasets using Markov models

## Syntax

```sql
MARKOV_TRAIN(<string>)

MARKOV_TRAIN(<order>)(<string>)

MARKOV_TRAIN(<order>, <frequency_cutoff>, <num_buckets_cutoff>, <frequency_add>, <frequency_desaturate>) (<string>)
```

## Arguments

| Arguments | Description |
|------------------| ------------------ |
| `string` | Input |
| `order` | Order of markov model to generate strings |
| `frequency-cutoff` | Frequency cutoff for markov model: remove all buckets with count less than specified |
| `num-buckets-cutoff` | Cutoff for number of different possible continuations for a context: remove all histograms with less than specified number of buckets |
| `frequency-add` | Add a constant to every count to lower probability distribution skew |
| `frequency-desaturate` | 0..1 - move every frequency towards average to lower probability distribution skew |

## Return Type

Depending on the implementation, it is only used as a argument for [MARKOV_GENERATE](../19-data-anonymization-functions/markov_generate.md).

## Examples

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
