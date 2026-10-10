---
title: SHOW TAGS
summary: 現在のテナント内のタグ定義を一覧表示します。
---

# SHOW TAGS

現在のテナント内のタグ定義を一覧表示します。`system.tags` テーブルを使用してタグ定義をクエリすることもできます。

関連情報: [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md), [DROP TAG](/tidb-cloud-lake/sql/drop-tag.md)。

## 構文 {#syntax}

```sql
SHOW TAGS [ LIKE '<pattern>' | WHERE <expr> ] [ LIMIT <n> ]
```

## 出力カラム {#output-columns}

| カラム           | 説明                                          |
|------------------|------------------------------------------------------|
| `name`           | タグ名                                             |
| `allowed_values` | 許可される値のリスト。任意の値が許可される場合は NULL |
| `comment`        | タグの説明                                      |
| `created_on`     | 作成タイムスタンプ                                   |

## 例 {#examples}

すべてのタグを表示します。

```sql
SHOW TAGS;
```

名前パターンでタグを絞り込みます。

```sql
SHOW TAGS LIKE 'env%';
```

WHERE 条件で絞り込みます。

```sql
SHOW TAGS WHERE comment IS NOT NULL;
```

結果数を制限します。

```sql
SHOW TAGS LIMIT 5;
```

system テーブルを使用した等価なクエリ:

```sql
SELECT * FROM system.tags;
```