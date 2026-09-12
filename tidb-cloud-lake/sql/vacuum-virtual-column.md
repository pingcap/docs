---
title: VACUUM VIRTUAL COLUMN
summary: 删除表中已过时的虚拟列文件。
---

# VACUUM VIRTUAL COLUMN

删除表中已过时的虚拟列文件。

> **Note:**
>
> 此命令需要 virtual column 企业版功能。

## 语法 {#syntax}

```sql
VACUUM VIRTUAL COLUMN FROM [ <catalog_name>. ][ <database_name>. ]<table_name>
```

## 输出 {#output}

返回已删除的文件数量。