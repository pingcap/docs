---
title: SHOW WAREHOUSES
summary: 現在のテナントから参照可能なすべての Warehouse を一覧表示します。
---

# SHOW WAREHOUSES

現在のテナントから参照可能なすべての Warehouse を一覧表示します。

## 構文 {#syntax}

```sql
SHOW WAREHOUSES [ LIKE '<pattern>' ] [ <pattern_without_like> ]
```

| パラメーター | 説明 |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `LIKE '<pattern>'`       | 任意。SQL の `LIKE` セマンティクスを使用して Warehouse 名をフィルタリングします（`%` は任意の文字列、`_` は任意の 1 文字に一致します）。 |
| `<pattern_without_like>` | 任意。`LIKE` を省略してリテラルが続く場合、そのリテラルは `LIKE '<literal>'` として扱われます。 |

## 出力カラム {#output-columns}

| カラム              | 説明 |
| ------------------- | ----------------------------------------- |
| `name`              | Warehouse 名                            |
| `state`             | 現在の状態（例: Running、Suspended）  |
| `size`              | Warehouse のサイズ                            |
| `auto_suspend`      | 自動サスペンドまでのタイムアウト（秒）           |
| `auto_resume`       | 自動再開が有効かどうか            |
| `min_cluster_count` | オートスケーリング時の最小クラスター数    |
| `max_cluster_count` | オートスケーリング時の最大クラスター数    |
| `role`              | Warehouse のロール                            |
| `comment`           | ユーザー定義のコメント                      |
| `tags`              | JSON 形式の文字列として表された Warehouse タグ |
| `created_by`        | 作成者                                   |
| `created_on`        | 作成日時                        |

## 例 {#examples}

すべての Warehouse を一覧表示します。

```sql
SHOW WAREHOUSES;
```

パターンに一致する Warehouse を一覧表示します。

```sql
SHOW WAREHOUSES LIKE '%prod%';
```

`LIKE` を使わずにリテラルを使用します。

```sql
SHOW WAREHOUSES 'nightly-etl';
```