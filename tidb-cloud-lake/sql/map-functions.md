---
title: Map 関数
summary: このセクションでは、{{{ .lake }}} の map 関数に関するリファレンス情報を提供します。Map 関数を使用すると、map データ構造（キーと値のペア）を作成、操作、およびそこから情報を抽出できます。
---

# Map 関数

このセクションでは、{{{ .lake }}} の map 関数に関するリファレンス情報を提供します。Map 関数を使用すると、map データ構造（キーと値のペア）を作成、操作、およびそこから情報を抽出できます。

## Map の作成と結合 {#map-creation-and-combination}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [MAP_CAT](/tidb-cloud-lake/sql/map-cat.md) | 複数の map を 1 つの map に結合します | `MAP_CAT({'a':1}, {'b':2})` → `{'a':1,'b':2}` |

## Map へのアクセスと情報取得 {#map-access-and-information}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [MAP_KEYS](/tidb-cloud-lake/sql/map-keys.md) | map 内のすべてのキーを配列として返します | `MAP_KEYS({'a':1,'b':2})` → `['a','b']` |
| [MAP_VALUES](/tidb-cloud-lake/sql/map-values.md) | map 内のすべての値を配列として返します | `MAP_VALUES({'a':1,'b':2})` → `[1,2]` |
| [MAP_SIZE](/tidb-cloud-lake/sql/map-size.md) | map 内のキーと値のペア数を返します | `MAP_SIZE({'a':1,'b':2,'c':3})` → `3` |
| [MAP_CONTAINS_KEY](/tidb-cloud-lake/sql/map-contains-key.md) | map に特定のキーが含まれているかどうかを確認します | `MAP_CONTAINS_KEY({'a':1,'b':2}, 'a')` → `TRUE` |

## Map の変更 {#map-modification}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [MAP_INSERT](/tidb-cloud-lake/sql/map-insert.md) | キーと値のペアを map に挿入します | `MAP_INSERT({'a':1,'b':2}, 'c', 3)` → `{'a':1,'b':2,'c':3}` |
| [MAP_DELETE](/tidb-cloud-lake/sql/map-delete.md) | キーと値のペアを map から削除します | `MAP_DELETE({'a':1,'b':2,'c':3}, 'b')` → `{'a':1,'c':3}` |

## Map の変換 {#map-transformation}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [MAP_TRANSFORM_KEYS](/tidb-cloud-lake/sql/map-transform-keys.md) | map 内の各キーに関数を適用します | `MAP_TRANSFORM_KEYS({'a':1,'b':2}, x -> UPPER(x))` → `{'A':1,'B':2}` |
| [MAP_TRANSFORM_VALUES](/tidb-cloud-lake/sql/map-transform-values.md) | map 内の各値に関数を適用します | `MAP_TRANSFORM_VALUES({'a':1,'b':2}, x -> x * 10)` → `{'a':10,'b':20}` |

## Map のフィルタリングと選択 {#map-filtering-and-selection}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [MAP_FILTER](/tidb-cloud-lake/sql/map-filter.md) | 条件式に基づいてキーと値のペアをフィルタリングします | `MAP_FILTER({'a':1,'b':2,'c':3}, (k,v) -> v > 1)` → `{'b':2,'c':3}` |
| [MAP_PICK](/tidb-cloud-lake/sql/map-pick.md) | 指定したキーのみを含む新しい map を作成します | `MAP_PICK({'a':1,'b':2,'c':3}, ['a','c'])` → `{'a':1,'c':3}` |