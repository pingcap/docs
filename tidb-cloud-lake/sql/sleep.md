---
title: SLEEP
summary: 各データブロックで `seconds` 秒スリープします。
---

# SLEEP

各データブロックで `seconds` 秒スリープします。

> **Note:**
>
> スリープが必要なテストでのみ使用されます。

## 構文 {#syntax}

```sql
SLEEP(seconds)
```

## 引数 {#arguments}

| 引数 | 説明 |
| ----------- | ----------- |
| seconds  | 任意の非負の数値または浮動小数点数の定数カラムである必要があります。｜

## 戻り値の型 {#return-type}

UInt8

## 例 {#examples}

```sql
SELECT sleep(2);
+----------+
| sleep(2) |
+----------+
|        0 |
+----------+
```