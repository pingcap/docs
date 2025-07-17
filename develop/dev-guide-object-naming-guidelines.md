---
title: Object Naming Convention
summary: 了解 TiDB 中的对象命名规范。
---

# Object Naming Convention

本文档介绍了数据库对象的命名规则，包括数据库、表、索引和用户。

## General rules

- 建议使用有意义的英文单词，单词之间用下划线分隔。
- 名称中只使用字母、数字和下划线。
- 避免使用 TiDB 的保留字，例如 `group` 和 `order`，作为列名。
- 建议所有数据库对象均使用小写字母。

## Database naming convention

建议根据业务、产品或其他指标区分数据库名称，数据库名长度不超过 20 个字符。例如，可以将临时库命名为 `tmp_crm`，测试库命名为 `test_crm`。

## Table naming convention

- 对于同一业务或模块的表，使用相同的前缀，并尽可能使表名具有自解释性。
- 单词之间用下划线分隔。建议表名不超过 32 个字符。
- 建议为表的用途添加注释，以便更好理解。例如：
    - 临时表：`tmp_t_crm_relation_0425`
    - 备份表：`bak_t_crm_relation_20170425`
    - 业务操作的临时表：`tmp_st_{business code}_{creator abbreviation}_{date}`
    - 账户期间的记录表：`t_crm_ec_record_YYYY{MM}{dd}`
- 对不同业务模块的表创建单独的数据库，并相应添加注释。

## Column naming convention

- 列名应反映列的实际含义或其缩写。
- 建议在具有相同含义的表之间使用相同的列名。
- 建议为列添加注释，并为枚举类型指定命名值，例如 "0: offline, 1: online"。
- 建议将布尔类型的列命名为 `is_{description}`。例如，表示会员是否启用的列可以命名为 `is_enabled`。
- 不建议列名超过 30 个字符，列数应少于 60 个。
- 避免使用 TiDB 的保留字作为列名，例如 `order`、`from` 和 `desc`。要检查某个关键词是否为保留字，请参见 [TiDB keywords](/keywords.md)。

## Index naming convention

- 主键索引：`pk_{table_name_abbreviation}_{field_name_abbreviation}`
- 唯一索引：`uk_{table_name_abbreviation}_{field_name_abbreviation}`
- 普通索引：`idx_{table_name_abbreviation}_{field_name_abbreviation}`
- 多词列名：使用有意义的缩写

## Need help?

<CustomContent platform="tidb">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](https://tidb.support.pingcap.com/).

</CustomContent>