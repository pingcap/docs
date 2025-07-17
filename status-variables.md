---
title: Server Status Variables
summary: 使用状态变量查看系统和会话状态
---

# Server Status Variables

服务器状态变量提供关于 TiDB 服务器的全局状态信息以及当前会话的状态。大部分这些变量设计为与 MySQL 兼容。

你可以使用 [SHOW GLOBAL STATUS](/sql-statements/sql-statement-show-status.md) 命令获取全局状态，使用 [SHOW SESSION STATUS](/sql-statements/sql-statement-show-status.md) 命令获取当前会话的状态。

此外，为了 MySQL 兼容性，还支持 [FLUSH STATUS](/sql-statements/sql-statement-flush-status.md) 命令。

## 变量参考

### Compression

- Scope: SESSION
- Type: Boolean
- 表示是否启用 MySQL Protocol 的压缩。

### Compression_algorithm

- Scope: SESSION
- Type: String
- 表示用于 MySQL Protocol 的压缩算法。

### Compression_level

- Scope: SESSION
- Type: Integer
- 表示用于 MySQL Protocol 的压缩级别。

### Ssl_cipher

- Scope: SESSION | GLOBAL
- Type: String
- 当前使用的 TLS 密码套件。

### Ssl_cipher_list

- Scope: SESSION | GLOBAL
- Type: String
- 服务器支持的 TLS 密码套件列表。

### Ssl_server_not_after

- Scope: SESSION | GLOBAL
- Type: Date
- 用于 TLS 连接的 X.509 证书的到期日期。

### Ssl_server_not_before

- Scope: SESSION | GLOBAL
- Type: String
- 用于 TLS 连接的 X.509 证书的起始日期。

### Ssl_verify_mode

- Scope: SESSION | GLOBAL
- Type: Integer
- TLS 验证模式的位掩码。

### Ssl_version

- Scope: SESSION | GLOBAL
- Type: String
- 使用的 TLS 协议版本。

### Uptime

- Scope: SESSION | GLOBAL
- Type: Integer
- 服务器的运行时间（秒）。

### ddl_schema_version

- Scope: SESSION | GLOBAL
- Type: Integer
- 使用的 DDL 架构版本。

### last_plan_binding_update_time <span class="version-mark">New in v5.2.0</span>

- Scope: SESSION
- Type: Timestamp
- 上次计划绑定更新的时间和日期。

### server_id

- Scope: SESSION | GLOBAL
- Type: String
- 服务器的 UUID。

### tidb_gc_last_run_time

- Scope: SESSION | GLOBAL
- Type: String
- [GC](/garbage-collection-overview.md) 上次运行的时间戳。

### tidb_gc_leader_desc

- Scope: SESSION | GLOBAL
- Type: String
- [GC](/garbage-collection-overview.md) 领导者的信息，包括主机名和进程 ID (pid)。

### tidb_gc_leader_lease

- Scope: SESSION | GLOBAL
- Type: String
- [GC](/garbage-collection-overview.md) 租约的时间戳。

### tidb_gc_leader_uuid

- Scope: SESSION | GLOBAL
- Type: String
- [GC](/garbage-collection-overview.md) 领导者的 UUID。

### tidb_gc_safe_point

- Scope: SESSION | GLOBAL
- Type: String
- [GC](/garbage-collection-overview.md) 安全点的时间戳。