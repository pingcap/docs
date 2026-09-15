---
title: DROP WORKLOAD GROUP
summary: 删除指定的 workload group。
---

# DROP WORKLOAD GROUP

删除指定的 workload group。

## 语法 {#syntax}

```sql
DROP WORKLOAD GROUP [IF EXISTS] <workload_group_name>
```

## 示例 {#examples}

以下示例删除 `test_workload_group` workload group：

```sql
DROP WORKLOAD GROUP test_workload_group;
```