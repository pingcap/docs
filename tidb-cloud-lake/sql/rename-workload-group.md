---
title: RENAME WORKLOAD GROUP
summary: 既存の workload group の名前を新しい名前に変更します。
---

# RENAME WORKLOAD GROUP

既存の workload group の名前を新しい名前に変更します。

## 構文 {#syntax}

```sql
RENAME WORKLOAD GROUP <current_name> TO <new_name>
```

## 例 {#examples}

この例では、`test_workload_group_1` の名前を `test_workload_group` に変更します。

```sql
RENAME WORKLOAD GROUP test_workload_group_1 TO test_workload_group;
```