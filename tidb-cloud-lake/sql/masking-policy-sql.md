---
title: 脱敏策略
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中脱敏策略的相关操作，便于参考。
---

# 脱敏策略

本页按功能分类，全面概述了 {{{ .lake }}} 中脱敏策略的相关操作，便于参考。

## 脱敏策略管理 {#masking-policy-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md) | 创建新的脱敏策略，用于数据混淆 |
| [DESCRIBE MASKING POLICY](/tidb-cloud-lake/sql/desc-masking-policy.md) | 显示特定脱敏策略的详细信息 |
| [DROP MASKING POLICY](/tidb-cloud-lake/sql/drop-masking-policy.md) | 删除脱敏策略 |

## 相关主题 {#related-topics}

- [脱敏策略](/tidb-cloud-lake/guides/masking-policy.md)

> **注意：**
>
> {{{ .lake }}} 中的脱敏策略允许你在缺少适当权限的用户查询数据时，通过动态转换或混淆数据来保护敏感信息。