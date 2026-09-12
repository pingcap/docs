---
title: DML（数据操作语言）命令
summary: 本页提供 {{{ .lake }}} 中 DML（数据操作语言）命令的参考信息。
---

# DML（数据操作语言）命令

本页提供 {{{ .lake }}} 中 DML（数据操作语言）命令的参考信息。

## 数据修改 {#data-modification}

| 命令 | 描述 |
|---------|-------------|
| **[INSERT](/tidb-cloud-lake/sql/insert.md)** | 向表中添加新行 |
| **[INSERT MULTI](/tidb-cloud-lake/sql/insert-multi-table.md)** | 在一条语句中向多个表插入数据 |
| **[UPDATE](/tidb-cloud-lake/sql/update.md)** | 修改表中的现有行 |
| **[DELETE](/tidb-cloud-lake/sql/delete.md)** | 从表中删除行 |
| **[REPLACE](/tidb-cloud-lake/sql/replace.md)** | 插入新行或修改现有行 |
| **[MERGE](/tidb-cloud-lake/sql/merge.md)** | 根据条件执行 upsert 操作 |

## 数据加载与导出 {#data-loading-export}

| 命令 | 描述 |
|---------|-------------|
| **[COPY INTO Table](/tidb-cloud-lake/sql/copy-into-table.md)** | 将文件中的数据加载到表中 |
| **[COPY INTO Location](/tidb-cloud-lake/sql/copy-into-location.md)** | 将表数据导出到文件 |