---
title: SYSTEM$FUSE_AMEND
summary: 从兼容 S3 的对象存储中恢复表数据。
---

# SYSTEM$FUSE_AMEND

从兼容 S3 的对象存储中恢复表数据。

## 语法 {#syntax}

```sql
CALL SYSTEM$FUSE_AMEND('<database_name>', '<table_name>');
```

## 示例 {#examples}

此函数专为 Fail-Safe 场景设计。详情请参阅 [Fail-Safe 指南](/tidb-cloud-lake/guides/fail-safe.md)。