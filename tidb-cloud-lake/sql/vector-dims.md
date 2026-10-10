---
title: VECTOR_DIMS
summary: ベクトルの次元数（要素数）を返します。
---

# VECTOR_DIMS

ベクトルの次元数（要素数）を返します。

## 構文 {#syntax}

```sql
VECTOR_DIMS(vector)
```

## 引数 {#arguments}

- `vector`: 入力ベクトル（VECTOR データ型）

## 戻り値 {#returns}

ベクトル内の次元数（要素数）を表す INT 値を返します。

## 説明 {#description}

`VECTOR_DIMS` 関数は、ベクトルの次元数、つまりそのベクトルに含まれる要素数を返します。この関数は、次のような用途で役立ちます。

- 演算を実行する前にベクトルの次元数を検証する
- 次元情報が必要な動的ベクトル処理
- ベクトルデータのデバッグやデータ探索
- 計算時にベクトル間の互換性を確保する

> **Note:**
>
> この関数は {{{ .lake }}} 内でベクトル計算を実行し、外部 API には依存しません。

## 例 {#examples}

```sql
SELECT
    VECTOR_DIMS([1,2]::VECTOR(2)) AS dims_2d,
    VECTOR_DIMS([1,2,3]::VECTOR(3)) AS dims_3d,
    VECTOR_DIMS([1,2,3,4,5]::VECTOR(5)) AS dims_5d;
```

結果:

```
┌─────────┬─────────┬─────────┐
│ dims_2d │ dims_3d │ dims_5d │
├─────────┼─────────┼─────────┤
│       2 │       3 │       5 │
└─────────┴─────────┴─────────┘
```