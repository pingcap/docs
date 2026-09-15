---
title: SET
summary: 更改当前会话的系统设置值。要显示所有当前设置，请使用 SHOW SETTINGS。
---

# SET

更改当前会话的系统设置值。要显示所有当前设置，请使用 [SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md)。

另请参阅：

- [SETTINGS 子句](/tidb-cloud-lake/sql/settings-clause.md)
- [SET_VAR](/tidb-cloud-lake/sql/set-var.md)
- [UNSET](/tidb-cloud-lake/sql/unset.md)

## 语法 {#syntax}

```sql
SET [ SESSION | GLOBAL ] <setting_name> = <new_value>
```

| 参数 | 描述 |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SESSION   | 在会话级别应用设置更改。如果省略，则默认在会话级别应用。 |
| GLOBAL    | 在全局级别应用设置更改，而不仅限于当前会话。有关设置级别的更多信息，请参阅 [设置级别](/tidb-cloud-lake/sql/show-settings.md#setting-levels)。 |

## 示例 {#examples}

以下示例将 `max_memory_usage` 设置为 `4 GB`：

```sql
SET max_memory_usage = 1024*1024*1024*4;
```

以下示例将 `max_threads` 设置为 `4`：

```sql
SET max_threads = 4;
```

以下示例将 `max_threads` 设置为 `4`，并将其更改为全局级别设置：

```sql
SET GLOBAL max_threads = 4;
```