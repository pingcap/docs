---
title: 使用 UUID 作为主键的最佳实践
summary: UUIDs（通用唯一标识符）在作为主键时，具有减少网络请求次数、支持大部分编程语言和数据库、以及防止枚举攻击等优点。建议将 UUID 以二进制格式存储在 `BINARY(16)` 列中。同时，建议避免在 TiDB 中设置 `swap_flag` 以防热点。UUIDs 也兼容 MySQL。
---

# 使用 UUID 作为主键的最佳实践

UUIDs（通用唯一标识符）是在分布式数据库中替代自增整数作为主键的常用方案。本文档概述了在 TiDB 中使用 UUID 的优势，并提供了高效存储和索引的最佳实践。

## UUID 概述

作为主键时，UUID 相较于 [`AUTO_INCREMENT`](/auto-increment.md) 整数具有以下优势：

- UUID 可以在多个系统上生成，而不必担心冲突。在某些情况下，这可以减少对 TiDB 的网络请求次数，从而提升性能。
- UUID 被大多数编程语言和数据库系统支持。
- 作为 URL 的一部分时，UUID 不易受到枚举攻击。相比之下，使用 `AUTO_INCREMENT` 数字时，可能会猜测出发票编号或用户编号。

## 最佳实践

本节介绍在 TiDB 中存储和索引 UUID 的最佳实践。

### 以二进制存储

文本格式的 UUID 如：`ab06f63e-8fe7-11ec-a514-5405db7aad56`，是一个 36 字符的字符串。通过使用 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md#uuid_to_bin)，可以将文本格式转换为 16 字节的二进制格式。这允许你将其存储在 [`BINARY(16)`](/data-type-string.md#binary-type) 列中。在检索 UUID 时，可以使用 [`BIN_TO_UUID()`](/functions-and-operators/miscellaneous-functions.md#bin_to_uuid) 函数还原为文本格式。

### UUID 格式的二进制排序和聚簇主键

`UUID_TO_BIN()` 函数可以接受一个参数，即 UUID，或者两个参数，其中第二个参数是 `swap_flag`。

<CustomContent platform="tidb">

建议不要在 TiDB 中设置 `swap_flag`，以避免 [hotspots](/best-practices/high-concurrency-best-practices.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

建议不要在 TiDB 中设置 `swap_flag`，以避免热点。

</CustomContent>

你也可以显式为基于 UUID 的主键设置 [`CLUSTERED` 选项](/clustered-indexes.md)，以避免热点。

为了演示 `swap_flag` 的效果，以下是两个结构相同的表。区别在于插入到 `uuid_demo_1` 的数据使用了 `UUID_TO_BIN(?, 0)`，而 `uuid_demo_2` 使用了 `UUID_TO_BIN(?, 1)`。

<CustomContent platform="tidb">

在下面的 [Key Visualizer](/dashboard/dashboard-key-visualizer.md) 截图中，你可以看到写入集中在 `uuid_demo_2` 表的某一单一区域，该表的字段顺序在二进制格式中被交换。

</CustomContent>

<CustomContent platform="tidb-cloud">

在下面的 [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer) 截图中，你可以看到写入集中在 `uuid_demo_2` 表的某一单一区域，该表的字段顺序在二进制格式中被交换。

</CustomContent>

![Key Visualizer](/media/best-practices/uuid_keyviz.png)

```sql
CREATE TABLE `uuid_demo_1` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

```sql
CREATE TABLE `uuid_demo_2` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

## MySQL 兼容性

UUIDs 也可以在 MySQL 中使用。`BIN_TO_UUID()` 和 `UUID_TO_BIN()` 函数在 MySQL 8.0 版本中引入，`UUID()` 函数在早期版本的 MySQL 中也可用。