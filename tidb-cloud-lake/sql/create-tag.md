---
title: CREATE TAG
summary: 创建一个新标签，并可选择指定允许的值和注释。
---

# CREATE TAG

创建一个新标签。标签是租户级别的元信息对象，可分配给数据库对象以进行治理和分类。

另请参阅：[DROP TAG](/tidb-cloud-lake/sql/drop-tag.md)、[SHOW TAGS](/tidb-cloud-lake/sql/show-tags.md)、[SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

## 语法 {#syntax}

```sql
CREATE TAG [ IF NOT EXISTS ] <tag_name>
    [ ALLOWED_VALUES = ( '<value1>' [, '<value2>', ... ] ) ]
    [ COMMENT = '<string>' ]
```

| 参数 | 描述 |
|------------------|----------------------------------------------------------|
| `tag_name`       | 要创建的标签名称。 |
| `ALLOWED_VALUES` | 可选的允许值列表。设置后，在 SET TAG 中只能使用这些值。重复值会被自动移除。 |
| `COMMENT`        | 标签的可选描述。 |

## 示例 {#examples}

创建一个带有允许值和注释的标签：

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod') COMMENT = 'Environment classification';
```

创建一个接受任意值的标签：

```sql
CREATE TAG owner COMMENT = 'Data owner';
```

创建一个没有限制的标签：

```sql
CREATE TAG cost_center;
```

验证标签定义：

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