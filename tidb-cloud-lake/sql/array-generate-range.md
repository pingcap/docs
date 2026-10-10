---
title: ARRAY_GENERATE_RANGE
summary: 開始値と終了値の間にある、等間隔の整数からなる配列を構築します。`end` 境界は排他的です。
---

# ARRAY_GENERATE_RANGE

開始値と終了値の間にある、等間隔の整数からなる配列を構築します。`end` 境界は排他的です。

## 構文 {#syntax}

```sql
ARRAY_GENERATE_RANGE(<start>, <end>[, <step>])
```

- `<start>`: 含める最初の値。
- `<end>`: 排他的な上限（または下限）。
- `<step>`: オプションの増分（デフォルトは `1`）。負のステップを指定すると降順のシーケンスを生成します。

## 戻り値の型 {#return-type}

`ARRAY`

## 例 {#examples}

```sql
SELECT ARRAY_GENERATE_RANGE(1, 5) AS seq;

┌──────────┐
│ seq      │
├──────────┤
│ [1,2,3,4]│
└──────────┘
```

```sql
SELECT ARRAY_GENERATE_RANGE(0, 6, 2) AS seq_step;

┌────────────┐
│ seq_step   │
├────────────┤
│ [0,2,4]    │
└────────────┘
```

```sql
SELECT ARRAY_GENERATE_RANGE(5, 0, -2) AS seq_down;

┌────────────┐
│ seq_down   │
├────────────┤
│ [5,3,1]    │
└────────────┘
```