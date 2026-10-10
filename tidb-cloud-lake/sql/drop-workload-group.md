---
title: DROP WORKLOAD GROUP
summary: 指定したワークロードグループを削除します。
---

# DROP WORKLOAD GROUP

指定したワークロードグループを削除します。

## 構文 {#syntax}

```sql
DROP WORKLOAD GROUP [IF EXISTS] <workload_group_name>
```

## 例 {#examples}

次の例では、`test_workload_group` ワークロードグループを削除します。

```sql
DROP WORKLOAD GROUP test_workload_group;
```