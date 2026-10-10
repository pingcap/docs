---
title: Bitmap
summary: BITMAP は符号なし 64 ビット整数のメンバーシップ情報を格納し、高速な集合演算（count、union、intersection など）をサポートします。SELECT 文ではバイナリ blob として表示されるため、値を解釈するには Bitmap Functions を使用してください。
---

# Bitmap

> **Note:**
>
> v1.1.45 で導入されました。

## 概要 {#overview}

`BITMAP` は符号なし 64 ビット整数のメンバーシップ情報を格納し、高速な集合演算（count、union、intersection など）をサポートします。SELECT 文ではバイナリ blob として表示されるため、値を解釈するには [Bitmap Functions](/tidb-cloud-lake/sql/bitmap-functions.md) を使用してください。

## 例 {#examples}

### Bitmap の構築 {#build-bitmaps}

`TO_BITMAP` は、カンマ区切りの文字列、または `UINT64` 値（単一要素として扱われます）のいずれかを受け取ります。`TO_STRING` は bitmap を読みやすいテキストに再シリアライズします。

```sql
SELECT
  TO_BITMAP('1,2,3')                     AS str_input,
  TO_STRING(TO_BITMAP('1,2,3'))          AS round_tripped,
  TO_STRING(TO_BITMAP(123))              AS from_uint64;
```

結果:

```
┌────────────────────────────────┬──────────────────────────────────┬────────────────┐
│ str_input                      │ round_tripped                    │ from_uint64    │
├────────────────────────────────┼──────────────────────────────────┼────────────────┤
│ <bitmap binary>                │ 1,2,3                            │ 123            │
└────────────────────────────────┴──────────────────────────────────┴────────────────┘
```

### Bitmap の永続化 {#persist-bitmaps}

配列をテーブルに挿入する前に bitmap に変換するには、`BUILD_BITMAP` を使用します。その後、`BITMAP_COUNT` などの集約関数を使うことで、格納された値を高速に読み取れます。

```sql
CREATE TABLE user_visits (
  user_id INT,
  page_visits BITMAP
);

INSERT INTO user_visits VALUES
  (1, BUILD_BITMAP([2, 5, 8, 10])),
  (2, BUILD_BITMAP([3, 7, 9])),
  (3, BUILD_BITMAP([1, 4, 6, 10]));

SELECT
  user_id,
  BITMAP_COUNT(page_visits) AS distinct_pages,
  BITMAP_HAS_ALL(page_visits, BUILD_BITMAP([10])) AS saw_page_10
FROM user_visits;
```

結果:

```
┌────────┬────────────────┬─────────────┐
│ user_id │ distinct_pages │ saw_page_10 │
├────────┼────────────────┼─────────────┤
│      1 │              4 │        true │
│      2 │              3 │       false │
│      3 │              4 │        true │
└────────┴────────────────┴─────────────┘
```