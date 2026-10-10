---
title: CREATE TAG
summary: オプションの許可値とコメントを指定して新しいタグを作成します。
---

# CREATE TAG

新しいタグを作成します。タグはテナントレベルのメタデータオブジェクトであり、ガバナンスや分類のためにデータベースオブジェクトへ割り当てることができます。

関連情報: [DROP TAG](/tidb-cloud-lake/sql/drop-tag.md)、[SHOW TAGS](/tidb-cloud-lake/sql/show-tags.md)、[SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

## 構文 {#syntax}

```sql
CREATE TAG [ IF NOT EXISTS ] <tag_name>
    [ ALLOWED_VALUES = ( '<value1>' [, '<value2>', ... ] ) ]
    [ COMMENT = '<string>' ]
```

| Parameter        | 説明 |
|------------------|----------------------------------------------------------|
| `tag_name`       | 作成するタグの名前。                                                                                            |
| `ALLOWED_VALUES` | オプションの許可値リスト。設定すると、SET TAG ではこれらの値のみを使用できます。重複する値は自動的に削除されます。 |
| `COMMENT`        | タグのオプションの説明。                                                                                     |

## 例 {#examples}

許可値とコメントを指定してタグを作成します。

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod') COMMENT = 'Environment classification';
```

任意の値を受け入れるタグを作成します。

```sql
CREATE TAG owner COMMENT = 'Data owner';
```

制限のないタグを作成します。

```sql
CREATE TAG cost_center;
```

タグ定義を確認します。

```sql
SELECT name, allowed_values, comment FROM system.tags ORDER BY name;

┌──────────────────────────────────────────────────────────────────────┐
│      name      │       allowed_values       │         comment        │
├────────────────┼────────────────────────────┼────────────────────────┤
│ cost_center    │ NULL                       │                        │
│ env            │ ['dev', 'staging', 'prod'] │ Environment classific… │
│ owner          │ NULL                       │ Data owner             │
└──────────────────────────────────────────────────────────────────────┘
```