---
title: CHAR
summary: 渡された各整数に対応する文字を返します。この関数は、各整数を対応する Unicode 文字に変換します。
---

# CHAR

渡された各整数に対応する文字を返します。この関数は、各整数を対応する Unicode 文字に変換します。

## 構文 {#syntax}

```sql
CHAR(N, ...)
CHR(N)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------------------------------------------------------|
| N         | Unicode コードポイント (0 から 2^32-1) を表す整数値 |

## 戻り値の型 {#return-type}

`STRING`

## 備考 {#remarks}

- 任意の整数型を受け付けます（自動的に Int64 にキャストされます）。
- 無効なコードポイントに対しては空文字列 (`''`) を返し、エラーをログに記録します。
- `chr` は `char` のエイリアスです。
- 入力に NULL が含まれる場合、出力は NULL になります。

## 例 {#examples}

```sql
-- Basic usage
SELECT CHAR(65, 66, 67);
┌───────┐
│ char  │
│ String│
├───────┤
│ ABC   │
└───────┘

-- Using the CHR alias
SELECT CHR(68);
┌───────┐
│ chr   │
│ String│
├───────┤
│ D     │
└───────┘

-- Creating a string from multiple code points
SELECT CHAR(77,121,83,81,76);
┌───────┐
│ char  │
│ String│
├───────┤
│ MySQL │
└───────┘

-- Auto-casting from different integer types
SELECT CHAR(CAST(65 AS UInt16));
┌───────┐
│ char  │
│ String│
├───────┤
│ A     │
└───────┘

-- NULL handling
SELECT CHAR(NULL);
┌───────┐
│ char  │
│ String│
├───────┤
│ NULL  │
└───────┘
```