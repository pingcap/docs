---
title: 计算集群 (Warehouse)
summary: {{{ .lake }}} 的计算集群相关 SQL 命令。
---

# 计算集群 (Warehouse)

{{{ .lake }}} 的计算集群相关 SQL 命令。

## 通用规则 {#general-rules}

- **计算集群命名**：长度为 3–63 个字符，只能包含 `A-Z`、`a-z`、`0-9` 和 `-`。
- **字符串和标识符**：不含空格的裸标识符可以省略引号；否则请使用单引号括起来。语法允许使用关键字或数字/布尔字面量作为名称，但仍会进行运行时校验。
- **数值参数**：`nullable_unsigned_number` / `nullable_signed_number` 接受整数型或 `NULL`。提供 `NULL` 会将该值重置（例如，`AUTO_SUSPEND = NULL` 等同于 `0`）。
- **时间参数**：`QUERY_HISTORY` 使用 `YYYY-MM-DD HH:MM:SS`（UTC 或显式时区）。如果缺少小数秒，则按整秒解释。
- **布尔参数**：仅接受 `TRUE`/`FALSE`。
- **`WITH` 关键字**：可以出现在整个选项列表之前，也可以出现在每个选项之前。选项之间以空白字符分隔；逗号不属于语法的一部分。

## 计算集群管理 {#warehouse-management}

标签是键值对，用于帮助对计算集群进行分类和组织，类似于 AWS resource tags。常见用途包括：

- **成本分摊**：按团队、项目或成本中心跟踪计算集群成本
- **环境标识**：将计算集群标记为 dev、staging 或 production
- **团队归属**：标识哪个团队拥有或管理某个计算集群
- **自定义元信息**：为组织管理目的添加任意元信息

标签键和值都是任意字符串（如果包含空格或特殊字符，则需要用引号括起来）。标签可以：

- 在创建计算集群时通过 `WITH TAG (key = 'value', ...)` 添加
- 之后通过 `ALTER WAREHOUSE ... SET TAG key = 'value'` 修改或新增
- 通过 `ALTER WAREHOUSE ... UNSET TAG key` 删除

标签会在 API 响应中返回，也可以通过 `SHOW WAREHOUSES` 查看。

**标签限制：**

- 每个计算集群最多 10 个标签
- 标签名称（key）最大长度：128 个字符
- 标签值最大长度：256 个字符

## 支持的语句 {#supported-statements}

| 语句 | 用途 | 说明 |
| ------------------ | ---------------------------- | ---------------------------------------------------------- |
| `CREATE WAREHOUSE` | 创建计算集群 | 支持 `IF NOT EXISTS` 和选项列表 |
| `ALTER WAREHOUSE`  | 暂停/恢复/修改/重命名 | `SUSPEND`/`RESUME`、`SET <options>` 或 `RENAME TO <name>` |
| `DROP WAREHOUSE`   | 删除计算集群 | 可选 `IF EXISTS` |
| `USE WAREHOUSE`    | 绑定当前会话 | 仅校验是否存在 |
| `SHOW WAREHOUSES`  | 列出计算集群 | 可选 `LIKE` 过滤 |
| `QUERY_HISTORY`    | 查看查询日志 | 按计算集群、时间范围、限制条数过滤 |

## 计算集群 SQL 命令 {#warehouse-sql-commands}

| 命令                                 | 描述                                       |
| --------------------------------------- | ------------------------------------------------- |
| [CREATE WAREHOUSE](/tidb-cloud-lake/sql/create-warehouse.md) | 创建新的计算集群 |
| [USE WAREHOUSE](/tidb-cloud-lake/sql/use-warehouse.md)       | 为会话设置当前计算集群 |
| [SHOW WAREHOUSES](/tidb-cloud-lake/sql/show-warehouses.md)   | 列出所有计算集群，并支持可选过滤 |
| [ALTER WAREHOUSE](/tidb-cloud-lake/sql/alter-warehouse.md)   | 暂停、恢复或修改计算集群设置 |
| [ALTER WAREHOUSE ASSIGN NODES](/tidb-cloud-lake/sql/alter-warehouse-assign-nodes.md) | 为计算集群分配节点 |
| [ALTER WAREHOUSE UNASSIGN NODES](/tidb-cloud-lake/sql/alter-warehouse-unassign-nodes.md) | 从计算集群中移除已分配的节点 |
| [DROP WAREHOUSE](/tidb-cloud-lake/sql/drop-warehouse.md)     | 删除计算集群 |
| [QUERY_HISTORY](/tidb-cloud-lake/sql/query-history.md)       | 查看某个计算集群的查询日志 |

> **注意：**
>
> 计算集群表示在 {{{ .lake }}} 中用于运行查询的计算资源。