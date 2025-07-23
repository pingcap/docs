---
title: 排查数据与索引不一致问题
summary: 了解如何处理由数据与索引一致性检查报告的错误。
---

# 排查数据与索引不一致问题

TiDB 在执行事务或 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句时，会检查数据与索引之间的一致性。如果检查发现某个记录的键值与对应的索引键值不一致，即存储行数据的键值对与存储其索引的键值对不一致（例如，索引多余或缺失），TiDB 会报告数据不一致错误，并在错误日志中打印相关错误信息。

<CustomContent platform="tidb">

本文档描述了数据不一致错误的含义，并提供了一些绕过一致性检查的方法。如果发生数据一致性错误，你可以 [获取支持](/support.md) 来自 PingCAP 或社区。

</CustomContent>

<CustomContent platform="tidb-cloud">

本文档描述了数据不一致错误的含义，并提供了一些绕过一致性检查的方法。如果发生数据一致性错误，你可以 [联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

## 错误说明

当数据与索引不一致时，你可以检查 TiDB 的错误信息，以了解行数据与索引数据之间哪个项不一致，或者查看相关的错误日志以进行进一步排查。

### 事务执行过程中报告的错误

本节列出在 TiDB 执行事务时报告的数据不一致错误，并用示例说明这些错误的含义。

#### Error 8133

`ERROR 8133 (HY000): data inconsistency in table: t, index: k2, index-count:1 != record-count:0`

该错误表示在表 `t` 的 `k2` 索引中，索引的数量为 1，而行记录的数量为 0，两者不一致。

#### Error 8138

`ERROR 8138 (HY000): writing inconsistent data in table: t, expected-values:{KindString green} != record-values:{KindString GREEN}`

该错误表示事务试图写入一行不正确的值。写入的数据中，编码后的行数据与编码前的原始数据不匹配。

#### Error 8139

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

该错误表示待写入的数据的句柄（即行数据的键）不一致。对于表 `t` 中的索引 `i1`，事务要写入的行在索引键值对中的句柄为 4，而在行记录的键值对中的句柄为 3。此行的数据将不会被写入。

#### Error 8140

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

该错误表示事务要写入的一行数据与索引中的数据不匹配。对于表 `t` 中的索引 `i2`，事务要写入的行在索引键值对中的数据为 `hellp`，在行记录的键值对中的数据为 `hello`，两者不一致，行数据不会被写入。

#### Error 8141

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

该错误表示在提交事务时断言失败。假设数据和索引是一致的，TiDB 断言键 `7480000000000000405f720133000000000000000000f8` 不存在。当事务提交时，TiDB 发现该键确实存在，由写入该键的事务的 `start ts` 为 `430590532931551233`。TiDB 会将该键的多版本并发控制（MVCC）历史打印到日志中。

### 管理检查中报告的错误

本节列出在执行 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句时可能出现的 数据不一致错误，并用示例说明这些错误的含义。

#### Error 8003

`ERROR 8003 (HY000): table count 3 != index(idx) count 2`

该错误表示执行 [`ADMIN CHECK`] 语句的表有 3 个行键值对，但索引只有 2 个。

#### Error 8134

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

该错误表示在表 `t` 的索引 `c2` 中，列 `c2` 的值存在不一致，具体为：

- 在句柄为 `2` 的行的索引键值对中，列 `c2` 的值为 `13`。
- 在行记录的键值对中，列 `c2` 的值为 `12`。

#### Error 8223

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

该错误表示 `index-values` 为空，而 `record-values` 不为空，意味着该行没有对应的索引。

## 解决方案

<CustomContent platform="tidb">

如果你遇到数据不一致错误，**不要自己处理**，应立即 [获取支持](/support.md) 来自 PingCAP 进行排查。如果你的应用需要紧急跳过此类错误，可以使用以下方法绕过检查。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你遇到数据不一致错误，**不要自己处理**，应立即 [联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 进行排查。如果你的应用需要紧急跳过此类错误，可以使用以下方法绕过检查。

</CustomContent>

### 重写 SQL

如果数据不一致错误只在某个特定的 SQL 语句中发生，可以通过用不同的执行操作符重写 SQL 语句为等价的形式，绕过此错误。

### 禁用错误检查

对于在事务执行过程中报告的以下错误，你可以绕过相应的检查：

- 要绕过错误 8138、8139 和 8140 的检查，配置 `set @@tidb_enable_mutation_checker=0`。
- 要绕过错误 8141 的检查，配置 `set @@tidb_txn_assertion_level=OFF`。

> **Note:**
>
> 禁用 `tidb_enable_mutation_checker` 和 `tidb_txn_assertion_level` 会绕过所有 SQL 语句的相应检查。

对于在事务执行过程中报告的其他错误，以及在 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句执行期间报告的所有错误，你不能绕过对应的检查，因为数据已经不一致。