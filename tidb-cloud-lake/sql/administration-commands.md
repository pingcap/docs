---
title: 管理命令
summary: 本页提供 {{{ .lake }}} 中系统管理命令的参考信息。
---

# 管理命令

本页提供 {{{ .lake }}} 中系统管理命令的参考信息。

## 系统监控 {#system-monitoring}

| 命令 | 描述 |
|---------|-------------|
| **[SHOW PROCESSLIST](/tidb-cloud-lake/sql/show-processlist.md)** | 显示活动查询和连接 |
| **[SHOW METRICS](/tidb-cloud-lake/sql/show-metrics.md)** | 查看系统性能指标 |
| **[KILL](/tidb-cloud-lake/sql/kill.md)** | 终止正在运行的查询或连接 |
| **[RUST BACKTRACE](/tidb-cloud-lake/sql/system-enable-disable-exception-backtrace.md)** | 调试 Rust 堆栈跟踪 |

## 访问控制 {#access-control}

| 命令 | 描述 |
|---------|-------------|
| **[FLUSH PRIVILEGES](/tidb-cloud-lake/guides/privileges.md)** | 强制每个查询节点重新加载角色和权限元信息 |

## 配置管理 {#configuration-management}

| 命令 | 描述 |
|---------|-------------|
| **[SET](/tidb-cloud-lake/sql/set.md)** | 设置全局配置参数 |
| **[UNSET](/tidb-cloud-lake/sql/unset.md)** | 移除配置设置 |
| **[SET VARIABLE](/tidb-cloud-lake/sql/set-var.md)** | 管理用户定义变量 |
| **[SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md)** | 显示当前系统设置 |

## 函数管理 {#function-management}

| 命令 | 描述 |
|---------|-------------|
| **[SHOW FUNCTIONS](/tidb-cloud-lake/sql/show-functions.md)** | 列出内置函数 |
| **[SHOW USER FUNCTIONS](/tidb-cloud-lake/sql/show-user-functions.md)** | 列出用户定义函数 |
| **[SHOW TABLE FUNCTIONS](/tidb-cloud-lake/sql/show-table-functions.md)** | 列出表值函数 |

## 存储维护 {#storage-maintenance}

| 命令 | 描述 |
|---------|-------------|
| **[VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md)** | 回收表占用的存储空间 |
| **[VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md)** | 清理已删除表的数据 |
| **[VACUUM TEMP FILES](/tidb-cloud-lake/sql/vacuum-temporary-files.md)** | 移除临时文件 |
| **[VACUUM VIRTUAL COLUMN](/tidb-cloud-lake/sql/vacuum-virtual-column.md)** | 移除过时的虚拟列文件 |
| **[SHOW INDEXES](/tidb-cloud-lake/sql/show-indexes.md)** | 显示表索引 |

## 动态执行 {#dynamic-execution}

| 命令 | 描述 |
|---------|-------------|
| **[EXECUTE IMMEDIATE](/tidb-cloud-lake/sql/execute-immediate.md)** | 执行动态构造的 SQL 语句 |