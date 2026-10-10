---
title: JARO_WINKLER
summary: 2 つの文字列間の Jaro-Winkler 距離を計算します。これは文字列間の類似度を測定するためによく使用され、値の範囲は 0.0（完全に異なる）から 1.0（同一の文字列）です。
---

# JARO_WINKLER

2 つの文字列間の [Jaro-Winkler distance](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) を計算します。これは文字列間の類似度を測定するためによく使用され、値の範囲は 0.0（完全に異なる）から 1.0（同一の文字列）です。

## 構文 {#syntax}

```sql
JARO_WINKLER(<string1>, <string2>)
```

## 戻り値の型 {#return-type}

`JARO_WINKLER` 関数は、2 つの入力文字列間の類似度を表す `FLOAT64` 値を返します。戻り値は次のルールに従います。

- 類似度の範囲: 結果は 0.0（完全に異なる）から 1.0（同一）までの範囲です。

    ```sql title='Examples:'
    SELECT JARO_WINKLER('datalake', 'Datalake') AS similarity;

    ┌────────────────────┐
    │     similarity     │
    ├────────────────────┤
    │ 0.9166666666666666 │
    └────────────────────┘

    SELECT JARO_WINKLER('datalake', 'database') AS similarity;

    ┌────────────┐
    │ similarity │
    ├────────────┤
    │        0.9 │
    └────────────┘
    ```

- NULL の処理: string1 または string2 のいずれかが NULL の場合、結果は NULL です。

    ```sql title='Examples:'
    SELECT JARO_WINKLER('datalake', NULL) AS similarity;

    ┌────────────┐
    │ similarity │
    ├────────────┤
    │ NULL       │
    └────────────┘
    ```

- 空文字列:
    - 2 つの空文字列を比較すると 1.0 を返します。

    ```sql title='Examples:'
    SELECT JARO_WINKLER('', '') AS similarity;

    ┌────────────┐
    │ similarity │
    ├────────────┤
    │          1 │
    └────────────┘
    ```

    - 空文字列と空でない文字列を比較すると 0.0 を返します。

    ```sql title='Examples:'
    SELECT JARO_WINKLER('datalake', '') AS similarity;

    ┌────────────┐
    │ similarity │
    ├────────────┤
    │          0 │
    └────────────┘
    ```