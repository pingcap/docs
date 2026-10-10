---
title: Spatial Index
summary: Spatial インデックスは、`GEOMETRY` カラムに対する空間述語フィルタリングを高速化します。
---

# Spatial Index

{{{ .lake }}} の Spatial インデックスは、`GEOMETRY` カラムに対する空間述語フィルタリングを高速化します。これらは Fuse テーブル向けに設計されており、オプティマイザが正確な空間関数を評価する前にブロックをプルーニングするのに役立ちます。

> **Tip:**
>
> Spatial インデックスは、インデックス作成後に書き込まれたデータに対して自動的に管理されます。すでにデータを含むテーブルにインデックスを作成し、既存の行をバックフィルする必要がある場合は、`REFRESH SPATIAL INDEX` を使用してください。

## Spatial インデックスの管理 {#spatial-index-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE SPATIAL INDEX](/tidb-cloud-lake/sql/create-spatial-index.md) | 1 つ以上の `GEOMETRY` カラムに新しい Spatial インデックスを作成します |
| [REFRESH SPATIAL INDEX](/tidb-cloud-lake/sql/refresh-spatial-index.md) | インデックス作成前から存在していた行の Spatial インデックスデータをバックフィルします |
| [DROP SPATIAL INDEX](/tidb-cloud-lake/sql/drop-spatial-index.md) | テーブルから Spatial インデックスを削除します |

## サポートされる述語 {#supported-predicates}

{{{ .lake }}} は、以下の空間述語を使用して構築されたクエリを Spatial インデックスで高速化できます。

- `ST_CONTAINS`
- `ST_INTERSECTS`
- `ST_WITHIN`
- `ST_DWITHIN`

## 制限事項 {#limitations}

- Spatial インデックスは Fuse テーブルでサポートされます。
- インデックス対象のカラムは `GEOMETRY` 型である必要があります。
- `GEOGRAPHY` カラムはサポートされません。

## 関連トピック {#related-topics}

- [Geospatial Functions](/tidb-cloud-lake/sql/geospatial-functions.md)