---
title: Unique Serial Number Generation
summary: 面向开发者的唯一 ID 生成方案，用于生成自己的唯一序列号。
---

# Unique Serial Number Generation

本文介绍了唯一序列号生成方案，帮助开发者自行生成唯一 ID。

## Auto-increment column

`AUTO_INCREMENT` 是许多兼容 MySQL 协议的关系型数据库管理系统（RDBMS）中的列属性。通过 `AUTO_INCREMENT` 属性，数据库可以在无需用户干预的情况下自动为该列分配值。随着表中记录数的增加，该列的值会自动递增，并保证唯一性。在大多数场景中，`AUTO_INCREMENT` 列用作代理主键，没有实际含义。

`AUTO_INCREMENT` 列的限制在于，列必须是整数类型，且分配的值必须是整数。如果应用所需的序列号包含字母、数字或其他字符，用户很难通过 `AUTO_INCREMENT` 列获得所需的自动递增数字。

## Sequence

**Sequence** 是一种数据库对象，应用可以调用它来生成递增的序列值。应用可以灵活地使用序列值为一个或多个表赋值，也可以结合文本和数字进行更复杂的处理，从而赋予代理键一些追踪和分类的意义。

Sequence 从 TiDB v4.0 开始支持。详细信息请参考 [sequence documentation](/sql-statements/sql-statement-create-sequence.md#create-sequence)。

## Snowflake-like solutions

Snowflake 是 Twitter 提出的一种分布式 ID 生成方案。现有几种实现方式，其中较为流行的有百度的 **uid-generator** 和美团的 **leaf**。本文以 `uid-generator` 为例。

`uid-generator` 生成的 64 位 ID 结构如下：

```
| sign | delta seconds | worker node id | sequencs |
|------|---------------|----------------|----------|
| 1bit |     28bits    | 22bits         | 13bits   |
```

- sign：固定长度 1 位，固定为 `0`，表示生成的 ID 始终为正数。
- delta seconds：默认 28 位。当前时间，以相对于预设时间基准（默认为 `2016-05-20`）的秒数递增值表示。28 位支持大约 8.7 年。
- worker node id：默认 22 位。表示机器 ID，通常在应用进程启动时由集中式 ID 生成器获取。常用的集中式 ID 生成器包括自增列和 ZooKeeper。默认分配策略为“丢弃即用”，重启时会重新获取新的 worker node id。22 位支持大约 420 万台机器。
- sequence：默认 13 位。每秒的并发序列数。13 位支持每秒 8192 个并发序列。

## Number allocation solution

数字分配方案可以理解为从数据库批量获取自增 ID。该方案需要一个序列号生成表，每行代表一个序列对象。表定义示例如下：

| Field Name | Field Type | Field Description |
| -------- | ------------ | ---------------------------- |
| `SEQ_NAME` | varchar(128) | 序列名称，用于区分不同应用。 |
| `MAX_ID` | bigint | 当前已分配的最大值。 |
| `STEP` | int | 步长，表示每次分配的段长度。 |

每次，应用从配置的步长中获取一段序列号，同时更新数据库以持久化已分配的最大值。序列号的处理和分配在应用的内存中完成。当一段序列号用完后，应用会获取新的一段，从而有效减轻数据库写入压力。实际操作中，也可以调整步长以控制数据库更新的频率。

最后，注意上述两种方案生成的 ID 不够随机，不能直接作为 TiDB 表的 **primary keys**。在实际应用中，可以对生成的 ID 进行位反转，以获得更随机的新 ID。例如，位反转后，ID `00000010100101000001111010011100` 变为 `00111001011110000010100101000000`，而 `11111111111111111111111111111101` 变为 `10111111111111111111111111111111`。

## Need help?

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>