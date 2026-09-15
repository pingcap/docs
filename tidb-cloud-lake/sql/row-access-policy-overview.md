---
title: 行访问策略概览
summary: "按功能组织的 {{{ .lake }}} 中行访问策略操作综合概览，便于参考。"
---

# 行访问策略概览

本页提供 {{{ .lake }}} 中行访问策略操作的综合概览，并按功能进行组织，便于参考。

## 行访问策略管理 {#row-access-policy-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE ROW ACCESS POLICY](/tidb-cloud-lake/sql/create-row-access-policy.md) | 创建行级过滤策略 |
| [DESCRIBE ROW ACCESS POLICY](/tidb-cloud-lake/sql/desc-row-access-policy.md) | 显示行访问策略的详细信息 |
| [DROP ROW ACCESS POLICY](/tidb-cloud-lake/sql/drop-row-access-policy.md) | 删除行访问策略 |

## 相关主题 {#related-topics}

- [行访问策略](/tidb-cloud-lake/guides/row-access-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#row-access-policy-operations)
- [POLICY_REFERENCES](/tidb-cloud-lake/sql/policy-references.md)

> **注意：**
>
> 行访问策略会在查询时过滤行。受保护的表仅返回策略表达式计算结果为 `TRUE` 的行。