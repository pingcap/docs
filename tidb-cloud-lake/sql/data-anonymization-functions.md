---
title: 数据匿名化函数
summary: 数据匿名化是指对数据集中的个人身份识别信息（PII）进行修改或移除，以保护个人隐私。其目标是在保留数据用于分析、研究和测试的可用性的同时，将数据转换为无法追溯到特定个人的形式。
---

# 数据匿名化函数

数据匿名化是指对数据集中的个人身份识别信息（PII）进行修改或移除，以保护个人隐私。其目标是在保留数据用于分析、研究和测试的可用性的同时，将数据转换为无法追溯到特定个人的形式。

## 常见的匿名化数据类别 {#common-data-categories-for-anonymization}

有效的匿名化策略通常针对以下几类敏感数据：

* **直接标识符（PII）**：能够明确识别个人身份的信息，例如姓名全称、电子邮件地址、电话号码和政府签发的身份证件号码。
* **间接标识符（准标识符）**：与其他数据源结合后可用于识别个人的属性，例如出生日期、性别、邮政编码或职位名称。
* **敏感业务数据**：如财务事务、薪资明细或专有内部记录等机密信息，这些数据在非生产环境中也需要受到保护。

### {{{ .lake }}} 匿名化技术 {#lake-anonymization-techniques}

{{{ .lake }}} 提供了一组函数，用于实现多种匿名化技术，包括数据脱敏、假名化和合成数据生成：

- **数据脱敏**：使用 [`OBFUSCATE` 表函数](/tidb-cloud-lake/sql/obfuscate.md) 自动对列应用脱敏规则，用看似真实的人工值替换原始值。
- **假名化**：使用 [FEISTEL_OBFUSCATE](/tidb-cloud-lake/sql/feistel-obfuscate.md) 将标识符替换为确定性的替代值。这可以保留数据完整性和基数，因此适合用于保留 join key。
- **合成数据**：使用 [MARKOV_TRAIN](/tidb-cloud-lake/sql/markov-train.md) 和 [MARKOV_GENERATE](/tidb-cloud-lake/sql/markov-generate.md) 生成由机器创建的数据，这些数据在统计特征上类似于原始数据集，但与真实记录没有直接关联。

| 函数 | 描述 |
|----------|-------------|
| [MARKOV_GENERATE](/tidb-cloud-lake/sql/markov-generate.md) | 基于 Markov 模型生成匿名化字符串 |
| [FEISTEL_OBFUSCATE](/tidb-cloud-lake/sql/feistel-obfuscate.md) | 使用 Feistel 密码对数字进行混淆 |
| [OBFUSCATE](/tidb-cloud-lake/sql/obfuscate.md) | 使用内置规则进行表级脱敏 |