---
title: system_history.log_history
summary: 注意：此表包含原始日志数据，并作为其他专用历史表的数据来源。其他表会基于这些数据提供结构化的、面向特定查询的视图。
---

# system_history.log_history

**系统操作审计轨迹** - 来自所有 {{{ .lake }}} 节点和组件的原始日志仓库。它是运维智能分析的基础：

- **系统监控**：跟踪系统健康状态、性能和资源使用情况
- **故障排查**：通过详细的错误日志和系统事件调试问题
- **运维分析**：分析系统行为模式和趋势
- **根因分析**：调查系统故障和性能瓶颈

> **注意：** 此表包含原始日志数据，并作为其他专用历史表的数据来源。其他表会基于这些数据提供结构化的、面向特定查询的视图。

## 字段 {#fields}

| 字段         | 类型      | 描述                                             |
|--------------|-----------|--------------------------------------------------|
| timestamp    | TIMESTAMP | 记录该日志条目时的时间戳                         |
| path         | VARCHAR   | 日志的源文件路径和行号                           |
| target       | VARCHAR   | 日志对应的目标模块或组件                         |
| log_level    | VARCHAR   | 日志等级（例如 `INFO`、`ERROR`）                 |
| cluster_id   | VARCHAR   | 集群的标识符                                     |
| node_id      | VARCHAR   | 节点的标识符                                     |
| warehouse_id | VARCHAR   | 计算集群的标识符                                 |
| query_id     | VARCHAR   | 与该日志关联的查询 ID                            |
| message      | VARCHAR   | 日志消息内容                                     |
| fields       | VARIANT   | 附加字段（以 JSON 对象形式存储）                 |
| batch_number | BIGINT    | 内部使用，无特殊含义                             |

注意：`message` 字段存储纯文本日志，而 `fields` 字段存储 JSON 格式的日志。

例如，一条日志记录的 `fields` 字段可能如下所示：

```
fields: {"node_id":"8R5ZMF8q0HHE6x9H7U1gr4","query_id":"72d2319a-b6d6-4b1d-8694-670137a40d87","session_id":"189fd3e2-e6ac-48c3-97ef-73094c141312","sql":"select * from system_history.log_history"}
```

另一条日志记录的 `message` 字段可能如下所示：

```
message: [HTTP-QUERY] Preparing to plan SQL query
```