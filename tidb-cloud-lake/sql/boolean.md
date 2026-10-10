---
title: Boolean
summary: 基本的な論理データ型。
---

# Boolean

## 概要 {#overview}

`BOOLEAN`（別名 `BOOL`）は `TRUE` または `FALSE` を表し、常に 1 バイトのストレージを使用します。数値入力および文字列入力は、可能な場合は自動的に boolean 値に変換されます。

| 入力タイプ | TRUE に変換 | FALSE に変換 | 注記 |
|------------|-----------------|-------------------|-------|
| 数値    | 0 以外の任意の値     | 0                 | 負の数は TRUE に変換されます。 |
| 文字列     | `TRUE`           | `FALSE`           | 大文字と小文字は区別されません。その他のテキストはキャストに失敗します。 |

## 例 {#examples}

```sql
SELECT
  0::BOOLEAN            AS zero_is_false,
  42::BOOLEAN           AS nonzero_is_true,
  'True'::BOOLEAN       AS string_true,
  'false'::BOOLEAN      AS string_false;
```

結果:

```
┌───────────────┬──────────────────┬───────────────┬────────────────┐
│ zero_is_false │ nonzero_is_true  │ string_true   │ string_false   │
├───────────────┼──────────────────┼───────────────┼────────────────┤
│ false         │ true             │ true          │ false          │
└───────────────┴──────────────────┴───────────────┴────────────────┘
```

```sql
-- Casting unsupported text raises an error.
SELECT 'yes'::BOOLEAN;
```

結果:

```
ERROR 1105 (HY000): QueryFailed: [1006]cannot parse to type `BOOLEAN` while evaluating function `to_boolean('yes')` in expr `CAST('yes' AS Boolean)`
```