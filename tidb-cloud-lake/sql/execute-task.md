---
title: EXECUTE TASK
summary: `EXECUTE TASK` 语句用于手动执行一个现有任务。
---

# EXECUTE TASK

`EXECUTE TASK` 语句用于手动执行一个现有任务。

**NOTICE:** 此功能仅在 {{{ .lake }}} 中开箱即用。

## 语法 {#syntax}

```sql
EXECUTE TASK  <name>
```

| 参数                             | 描述                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| name                             | 任务的名称。这是一个必填字段。                                                               |

## 使用说明 {#usage-notes}

- 该 SQL 命令只能执行独立任务或 DAG 中的根任务。如果输入的是子任务，该命令会返回用户错误。

## 使用示例 {#usage-examples}

```sql
EXECUTE TASK  mytask;
```

该命令会执行名为 mytask 的任务。