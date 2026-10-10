---
title: クエリ構文
summary: このページでは、{{{ .lake }}} におけるクエリ構文のリファレンス情報を提供します。各コンポーネントは個別に使用することも、組み合わせて強力なクエリを構築することもできます。
---

# クエリ構文

このページでは、{{{ .lake }}} におけるクエリ構文のリファレンス情報を提供します。各コンポーネントは個別に使用することも、組み合わせて強力なクエリを構築することもできます。

## 主要なクエリコンポーネント {#core-query-components}

| コンポーネント | 説明 |
|-----------|-------------|
| **[SELECT](/tidb-cloud-lake/sql/select.md)** | テーブルからデータを取得します。すべてのクエリの基盤です |
| **[FROM / JOIN](/tidb-cloud-lake/sql/join.md)** | データソースを指定し、複数のテーブルを結合します |
| **[WHERE](/tidb-cloud-lake/sql/select.md#where-clause)** | 条件に基づいて行をフィルタリングします |
| **[GROUP BY](/tidb-cloud-lake/sql/group-by.md)** | 行をグループ化し、集計（SUM、COUNT、AVG など）を実行します |
| **[HAVING](/tidb-cloud-lake/sql/group-by.md)** | グループ化された結果をフィルタリングします |
| **[ORDER BY](/tidb-cloud-lake/sql/select.md#order-by-clause)** | クエリ結果を並べ替えます |
| **[LIMIT / TOP](/tidb-cloud-lake/sql/top.md)** | 返される行数を制限します |

## 高度な機能 {#advanced-features}

| コンポーネント | 説明 |
|-----------|-------------|
| **[WITH (CTE)](/tidb-cloud-lake/sql/clause.md)** | 複雑なロジックのために再利用可能なクエリブロックを定義します |
| **[PIVOT](/tidb-cloud-lake/sql/pivot.md)** | 行をカラムに変換します（ワイド形式） |
| **[UNPIVOT](/tidb-cloud-lake/sql/unpivot.md)** | カラムを行に変換します（ロング形式） |
| **[QUALIFY](/tidb-cloud-lake/sql/qualify.md)** | ウィンドウ関数の計算後に行をフィルタリングします |
| **[VALUES](/tidb-cloud-lake/sql/values.md)** | インラインの一時データセットを作成します |

## Time Travel と Streaming {#time-travel-streaming}

| コンポーネント | 説明 |
|-----------|-------------|
| **[AT](/tidb-cloud-lake/sql/at.md)** | 特定の時点のデータをクエリします |
| **[CHANGES](/tidb-cloud-lake/sql/changes.md)** | 挿入、更新、削除を追跡します |
| **[WITH CONSUME](/tidb-cloud-lake/sql/with-consume.md)** | オフセット管理を使用してストリーミングデータを処理します |
| **[WITH STREAM HINTS](/tidb-cloud-lake/sql/stream-hints.md)** | ストリーム処理の動作を最適化します |

## クエリ実行 {#query-execution}

| コンポーネント | 説明 |
|-----------|-------------|
| **[Settings](/tidb-cloud-lake/sql/settings-clause.md)** | クエリの最適化および実行パラメータを設定します |

## クエリ構造 {#query-structure}

一般的な {{{ .lake }}} クエリは、次の構造に従います。

```sql
[WITH cte_expressions]
SELECT [TOP n] columns
FROM table
[JOIN other_tables]
[WHERE conditions]
[GROUP BY columns]
[HAVING group_conditions]
[QUALIFY window_conditions]
[ORDER BY columns]
[LIMIT n]
```