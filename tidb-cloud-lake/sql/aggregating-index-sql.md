---
title: 集計インデックス
summary: このページでは、{{{ .lake }}} における集計インデックスの操作について、参照しやすいよう機能別に整理して包括的に説明します。
---

# 集計インデックス

このページでは、{{{ .lake }}} における集計インデックスの操作について、参照しやすいよう機能別に整理して包括的に説明します。

## 集計インデックスの管理 {#aggregating-index-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE AGGREGATING INDEX](/tidb-cloud-lake/sql/create-aggregating-index.md) | テーブルの新しい集計インデックスを作成します |
| [DROP AGGREGATING INDEX](/tidb-cloud-lake/sql/drop-aggregating-index.md) | 集計インデックスを削除します |
| [REFRESH AGGREGATING INDEX](/tidb-cloud-lake/sql/refresh-aggregating-index.md) | 最新のデータで集計インデックスを更新します |

## 関連トピック {#related-topics}

- [集計インデックス](/tidb-cloud-lake/guides/aggregating-index.md)

> **Note:**
>
> {{{ .lake }}} の集計インデックスは、集計クエリの結果を事前に計算して保存することで、集計クエリのパフォーマンスを向上させるために使用されます。