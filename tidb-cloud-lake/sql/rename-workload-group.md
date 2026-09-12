---
title: RENAME WORKLOAD GROUP
summary: 将现有的 workload group 重命名为新名称。
---

# RENAME WORKLOAD GROUP

将现有的 workload group 重命名为新名称。

## 语法 {#syntax}

```sql
RENAME WORKLOAD GROUP <current_name> TO <new_name>
```

## 示例 {#examples}

以下示例将 `test_workload_group_1` 重命名为 `test_workload_group`：

```sql
RENAME WORKLOAD GROUP test_workload_group_1 TO test_workload_group;
```