---
title: 系统变量
summary: 使用 TiDB 系统变量来优化性能或修改运行行为。
---

# 系统变量 <!--Corresponding EN commit: c913fdf54451bceb35beb56879ebdfecb76d7e93-->

TiDB 系统变量的行为与 MySQL 相似，变量的作用范围可以是会话级别有效 (Session Scope) 或全局范围有效 (Global Scope)。其中：

- 对 `SESSION` 作用域变量的更改，设置后**只影响当前会话**。
- 对 `GLOBAL` 作用域变量的更改，设置后立即生效。如果该变量也有 `SESSION` 作用域，已经连接的所有会话 (包括当前会话) 将继续使用会话当前的 `SESSION` 变量值。
- 要设置变量值，可使用 [`SET` 语句](/sql-statements/sql-statement-set-variable.md)。

```sql
# 以下两个语句等价地改变一个 Session 变量
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# 以下两个语句等价地改变一个 Global 变量
SET @@global.tidb_distsql_scan_concurrency = 10;
SET GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **注意：**
>
> 部分 `GLOBAL` 作用域的变量会持久化到 TiDB 集群中。文档中的变量有一个“是否持久化到集群”的说明，可以为“是”或者“否”。
>
> - 对于持久化到集群的变量，当该全局变量被修改后，会通知所有 TiDB 服务器刷新其系统变量缓存。在集群中增加一个新的 TiDB 服务器时，或者重启现存的 TiDB 服务器时，都将自动使用该持久化变量。
> - 对于不持久化到集群的变量，对变量的修改只对当前连接的 TiDB 实例生效。如果需要保留设置过的值，需要在 `tidb.toml` 配置文件中声明。
>
> 此外，由于应用和连接器通常需要读取 MySQL 变量，为了兼容这一需求，在 TiDB 中，部分 MySQL 的变量既可读取也可设置。例如，尽管 JDBC 连接器不依赖于查询缓存 (query cache) 的行为，但仍然可以读取和设置查询缓存。

> **注意：**
>
> 变量取较大值并不总会带来更好的性能。由于大部分变量对单个连接生效，设置变量时，还应考虑正在执行语句的并发连接数量。
>
> 确定安全值时，应考虑变量的单位：
>
> * 如果单位为线程，安全值通常取决于 CPU 核的数量。
> * 如果单位为字节，安全值通常小于系统内存的总量。
> * 如果单位为时间，单位可能为秒或毫秒。
>
> 单位相同的多个变量可能会争夺同一组资源。

从 v7.4.0 开始，部分 `SESSION` 作用域的变量可以通过 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) Hint 在语句执行期间临时修改变量的值。当语句执行完成后，系统变量将在当前会话中自动恢复为原始值。通过这个 Hint 可以修改一部分与优化器、执行器相关的系统变量行为。文档中的变量有一个“是否受 Hint [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) 控制”的说明，可以为“是”或者“否”。

- 对于受 Hint SET_VAR 控制的变量，你可以在语句中使用 `/*+ SET_VAR(...) */` 修改语句执行期间变量的值。
- 对于不受 Hint SET_VAR 控制的变量，你不能在语句中使用 `/*+ SET_VAR(...) */` 修改语句执行期间变量的值。

关于 SET_VAR Hint 的更多说明，参考 [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)。

## 变量参考

### allow_auto_random_explicit_insert <span class="version-mark">从 v4.0.3 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 是否允许在 `INSERT` 语句中显式指定含有 `AUTO_RANDOM` 属性的列的值。

### authentication_ldap_sasl_auth_method_name <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`SCRAM-SHA-1`
- 可选值：`SCRAM-SHA-1`、`SCRAM-SHA-256`、`GSSAPI`
- LDAP SASL 身份验证中，验证方法的名称。

### authentication_ldap_sasl_bind_base_dn <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP SASL 身份验证中，搜索用户的范围。如果创建用户时没有通过 `AS ...` 指定 `dn`，TiDB 会自动在 LDAP Server 的该范围中根据用户名搜索用户 `dn`。例如 `dc=example,dc=org`。

### authentication_ldap_sasl_bind_root_dn <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP SASL 身份验证中，TiDB 登录 LDAP Server 搜索用户时使用的 `dn`。

### authentication_ldap_sasl_bind_root_pwd <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP SASL 身份验证中，TiDB 登录 LDAP Server 搜索用户时使用的密码。

### authentication_ldap_sasl_ca_path <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP SASL 身份验证中，TiDB 对 StartTLS 连接使用的 CA 证书的路径。

### authentication_ldap_sasl_init_pool_size <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`10`
- 范围：`[1, 32767]`
- LDAP SASL 身份验证中，TiDB 与 LDAP Server 间连接池的初始连接数。

### authentication_ldap_sasl_max_pool_size <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1000`
- 范围：`[1, 32767]`
- LDAP SASL 身份验证中，TiDB 与 LDAP Server 间连接池的最大连接数。

### authentication_ldap_sasl_server_host <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP SASL 身份验证中，LDAP Server 的主机名或地址。

### authentication_ldap_sasl_server_port <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`389`
- 范围：`[1, 65535]`
- LDAP SASL 身份验证中，LDAP Server 的 TCP/IP 端口号。

### authentication_ldap_sasl_tls <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- LDAP SASL 身份验证中，是否使用 StartTLS 对连接加密。

### authentication_ldap_simple_auth_method_name <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`SIMPLE`
- 可选值：`SIMPLE`
- LDAP simple 身份验证中，验证方法的名称。现在仅支持 `SIMPLE`。

### authentication_ldap_simple_bind_base_dn <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP simple 身份验证中，搜索用户的范围。如果创建用户时没有通过 `AS ...` 指定 `dn`，TiDB 会自动在 LDAP Server 的该范围中根据用户名搜索用户 `dn`。例如 `dc=example,dc=org`。

### authentication_ldap_simple_bind_root_dn <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP simple 身份验证中，TiDB 登录 LDAP Server 搜索用户时使用的 `dn`。

### authentication_ldap_simple_bind_root_pwd <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP simple 身份验证中，TiDB 登录 LDAP Server 搜索用户时使用的密码。

### authentication_ldap_simple_ca_path <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP simple 身份验证中，TiDB 对 StartTLS 连接使用的 CA 证书的路径。

### authentication_ldap_simple_init_pool_size <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`10`
- 范围：`[1, 32767]`
- LDAP simple 身份验证中，TiDB 与 LDAP Server 间连接池的初始连接数。

### authentication_ldap_simple_max_pool_size <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1000`
- 范围：`[1, 32767]`
- LDAP simple 身份验证中，TiDB 与 LDAP Server 间连接池的最大连接数。

### authentication_ldap_simple_server_host <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：""
- LDAP simple 身份验证中，LDAP Server 的主机名或地址。

### authentication_ldap_simple_server_port <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`389`
- 范围：`[1, 65535]`
- LDAP simple 身份验证中，LDAP Server 的 TCP/IP 端口号。

### authentication_ldap_simple_tls <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- LDAP simple 身份验证中，是否使用 StartTLS 对连接加密。

### auto_increment_increment

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1`
- 范围：`[1, 65535]`
- 控制 `AUTO_INCREMENT` 自增值字段的自增步长和 `AUTO_RANDOM` ID 的分配规则。该变量常与 [`auto_increment_offset`](#auto_increment_offset) 一起使用。

### auto_increment_offset

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1`
- 范围：`[1, 65535]`
- 控制 `AUTO_INCREMENT` 自增值字段的初始值和 `AUTO_RANDOM` ID 的分配规则。该变量常与 [`auto_increment_increment`](#auto_increment_increment) 一起使用。示例如下：

```sql
mysql> CREATE TABLE t1 (a int not null primary key auto_increment);
Query OK, 0 rows affected (0.10 sec)

mysql> set auto_increment_offset=1;
Query OK, 0 rows affected (0.00 sec)

mysql> set auto_increment_increment=3;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (),(),(),();
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+
| a  |
+----+
|  1 |
|  4 |
|  7 |
| 10 |
+----+
4 rows in set (0.00 sec)
```

### autocommit

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 用于设置在非显式事务时是否自动提交事务。更多信息，请参见[事务概述](/transaction-overview.md#自动提交)。

### block_encryption_mode

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`aes-128-ecb`
- 可选值：`aes-128-ecb`、`aes-192-ecb`、`aes-256-ecb`、`aes-128-cbc`、`aes-192-cbc`、`aes-256-cbc`、`aes-128-ofb`、`aes-192-ofb`、`aes-256-ofb`、`aes-128-cfb`、`aes-192-cfb`、`aes-256-cfb`
- 该变量用于设置 [`AES_ENCRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_encrypt) 和 [`AES_DECRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_decrypt) 函数的加密模式。

### character_set_client

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`utf8mb4`
- 这个变量表示从客户端发出的数据所用的字符集。有关更多 TiDB 支持的字符集和排序规则，参阅[字符集和排序规则](/character-set-and-collation.md)文档。如果需要更改字符集，建议使用 [`SET NAMES`](/sql-statements/sql-statement-set-names.md) 语句。

### character_set_connection

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`utf8mb4`
- 若没有为字符串常量指定字符集，该变量表示这些字符串常量所使用的字符集。

### character_set_database

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`utf8mb4`
- 该变量表示当前默认在用数据库的字符集，**不建议设置该变量**。选择新的默认数据库后，服务器会更改该变量的值。

### character_set_results

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`utf8mb4`
- 该变量表示数据发送至客户端时所使用的字符集。

### character_set_server

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`utf8mb4`
- 当 `CREATE SCHEMA` 中没有指定字符集时，该变量表示这些新建的表结构所使用的字符集。

### collation_connection

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`utf8mb4_bin`
- 该变量表示连接中所使用的排序规则。与 MySQL 中的 `collation_connection` 一致。

### collation_database

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`utf8mb4_bin`
- 该变量表示当前数据库默认所使用的排序规则。与 MySQL 中的 `collation_database` 一致。**不建议设置此变量**，当前使用的数据库变动时，此变量会被 TiDB 修改。

### collation_server

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`utf8mb4_bin`
- 该变量表示创建数据库时默认的排序规则。

### cte_max_recursion_depth

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`1000`
- 范围：`[0, 4294967295]`
- 这个变量用于控制公共表表达式的最大递归深度。

### datadir

> **注意：**
>
> [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 不支持该变量。

<CustomContent platform="tidb">

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：取决于组件和部署方式。
    - `/tmp/tidb`：当 [`--store`](/command-line-flags-for-tidb-configuration.md#--store) 设置为 `"unistore"` 或未设置 `--store` 时。
    - `${pd-ip}:${pd-port}`：当使用 TiKV 作为默认存储引擎（TiUP 和 TiDB Operator for Kubernetes 部署的默认值）时。
- 该变量表示数据的存储位置，可以是本地路径 `/tmp/tidb`，也可以指向 PD 服务器（如果数据存储在 TiKV 上）。格式为 `${pd-ip}:${pd-port}` 的值表示 TiDB 启动时连接的 PD 服务器。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：取决于组件和部署方式。
    - `/tmp/tidb`：当 [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store) 设置为 `"unistore"` 或未设置 `--store` 时。
    - `${pd-ip}:${pd-port}`：当使用 TiKV 作为默认存储引擎（TiUP 和 TiDB Operator for Kubernetes 部署的默认值）时。
- 该变量表示数据的存储位置，可以是本地路径 `/tmp/tidb`，也可以指向 PD 服务器（如果数据存储在 TiKV 上）。格式为 `${pd-ip}:${pd-port}` 的值表示 TiDB 启动时连接的 PD 服务器。

</CustomContent>

### ddl_slow_threshold

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`300`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 耗时超过该阈值的 DDL 操作会被记录到日志。

### default_authentication_plugin

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`mysql_native_password`
- 可选值：`mysql_native_password`、`caching_sha2_password`、`tidb_sm3_password`、`tidb_auth_token`、`authentication_ldap_sasl`、`authentication_ldap_simple`
- 该变量用于设置服务器在建立服务器-客户端连接时通告的认证方式。
- 如需使用 `tidb_sm3_password` 方式进行认证，可以通过 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3) 连接 TiDB。

<CustomContent platform="tidb">

该变量的更多可选值，参见[认证插件状态](/security-compatibility-with-mysql.md#authentication-plugin-status)。

</CustomContent>

### default_collation_for_utf8mb4 <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：GLOBAL | SESSION
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：`utf8mb4_bin`
- 可选值：`utf8mb4_bin`、`utf8mb4_general_ci`、`utf8mb4_0900_ai_ci`
- 该变量用于设置 utf8mb4 字符集的默认[排序规则](/character-set-and-collation.md)。它会影响以下语句的行为：
    - [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md) 和 [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) 语句显示的默认排序规则。
    - [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 和 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) 语句中对表或列使用 `CHARACTER SET` 语法明确指定 utf8mb4 字符集而未指定排序规则时，将使用该变量指定的排序规则。不影响未使用 `CHARACTER SET` 语法时的行为。
    - [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md) 和 [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md) 语句中使用 `CHARACTER SET` 语法明确指定 utf8mb4 字符集而未指定排序规则时，将使用该变量指定的排序规则。不影响未使用 `CHARACTER SET` 语法时的行为。
    - 任何使用 `_utf8mb4'string'` 形式的字面量在未使用 `COLLATE` 语法指定排序规则时，将使用该变量指定的排序规则。

### default_password_lifetime <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 取值范围：`[0, 65535]`
- 该变量用于设置全局自动密码过期策略，默认值为 `0`，即禁用全局自动密码过期。如果设置该变量的值为正整数 N，则表示允许的密码生存期为 N，即必须在 N 天之内更改密码。

### default_week_format

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 取值范围：`[0, 7]`
- 设置 `WEEK()` 函数使用的周格式。

### disconnect_on_expired_password <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量为只读变量，用于控制 TiDB 是否在密码过期时断开客户端连接。当设置为 `ON` 时，密码过期后客户端连接将被断开。当设置为 `OFF` 时，客户端连接将被限制在"沙箱模式"，用户只能执行密码重置操作。

<CustomContent platform="tidb">

- 如需修改密码过期后客户端连接的行为，请修改配置文件中的 [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) 配置项。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 如需修改密码过期后客户端连接的默认行为，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

### div_precision_increment <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`4`
- 范围：`[0, 30]`
- 这个变量用于控制使用运算符 `/` 执行除法操作时，结果增加的小数位数。该功能与 MySQL 保持一致。

### error_count

- 作用域：SESSION
- 默认值：`0`
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 表示上一条生成消息的 SQL 语句中的错误数。该变量为只读变量。

### foreign_key_checks

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：在 v6.6.0 之前版本中为 `OFF`，在 v6.6.0 及之后的版本中为 `ON`。
- 表示是否开启外键约束检查。

### group_concat_max_len

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1024`
- 取值范围：`[4, 18446744073709551615]`
- 表示 `GROUP_CONCAT()` 函数缓冲区的最大长度。

### have_openssl

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`DISABLED`
- 用于 MySQL 兼容性的只读变量。当服务器启用 TLS 时，服务器将其设置为 `YES`。

### have_ssl

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`DISABLED`
- 用于 MySQL 兼容性的只读变量。当服务器启用 TLS 时，服务器将其设置为 `YES`。

### hostname

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：（系统主机名）
- 这个变量为只读变量，表示 TiDB server 的主机名。

### identity <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 该变量为变量 [`last_insert_id`](#last_insert_id-从-v530-版本开始引入) 的别名。

### init_connect

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 用户首次连接到 TiDB 服务器时，`init_connect` 特性允许 TiDB 自动执行一条或多条 SQL 语句。如果你有 `CONNECTION_ADMIN` 或者 `SUPER` 权限，这些 SQL 语句将不会被自动执行。如果这些语句执行报错，你的用户连接将被终止。

### innodb_lock_wait_timeout

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`50`
- 范围：`[1, 1073741824]`
- 单位：秒
- 悲观事务语句等锁时间。

### InPacketBytes <span class="version-mark">从 v8.5.6 和 v9.0.0 版本开始引入</span>

- 这个变量只做内部统计使用，对用户不可见。

### interactive_timeout

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`28800`
- 范围：`[1, 31536000]`
- 单位：秒
- 该变量表示交互式用户会话的空闲超时时间。交互式用户会话是指使用 `CLIENT_INTERACTIVE` 选项调用 [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API 建立的会话（例如 MySQL Shell 和 MySQL Client）。该变量与 MySQL 完全兼容。

### last_insert_id <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 取值范围：`[0, 18446744073709551615]`
- 返回由 `INSERT` 语句产生的最新 `AUTO_INSCRENT` 或者 `AUTO_RANDOM` 值，与 `LAST_INSERT_ID()` 的返回的结果相同。与 MySQL 中的 `last_insert_id` 一致。

### last_plan_from_binding <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 该变量用来显示上一条执行的语句所使用的执行计划是否来自 binding 的[执行计划](/sql-plan-management.md)。

### last_plan_from_cache <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 这个变量用来显示上一个 `execute` 语句所使用的执行计划是不是直接从 plan cache 中取出来的。

### last_sql_use_alloc <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 这个变量是一个只读变量，用来显示上一个语句是否使用了缓存的 Chunk 对象 (Chunk allocation)。

### license

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`Apache License 2.0`
- 这个变量表示 TiDB 服务器的安装许可证。

### max_allowed_packet <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`67108864`
- 范围：`[1024, 1073741824]`
- 该值应为 1024 的整数倍。如果该值不能被 1024 整除，系统会发出警告并将该值向下取整。例如，当该值设为 1025 时，TiDB 中的实际值为 1024。
- 服务器和客户端在一次数据包传输中所允许的最大数据包大小。
- 在 `SESSION` 作用域下，该变量为只读。
- 该变量与 MySQL 兼容。

### OutPacketBytes <span class="version-mark">从 v8.5.6 和 v9.0.0 版本开始引入</span>

- 这个变量只做内部统计使用，对用户不可见。

### password_history <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 4294967295]`
- 该变量用于建立密码重用策略，使 TiDB 基于密码更改次数限制密码的重复使用。该变量默认值为 `0`，表示禁用基于密码更改次数的密码重用策略。当设置该变量为一个正整数 N 时，表示不允许重复使用最近 N 次使用过的密码。

### mpp_exchange_compression_mode <span class="version-mark">从 v6.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`UNSPECIFIED`
- 可选值：`NONE`，`FAST`，`HIGH_COMPRESSION`，`UNSPECIFIED`
- 该变量用于选择 MPP Exchange 算子的数据压缩模式，当 TiDB 选择版本号为 `1` 的 MPP 执行计划时生效。该变量值的含义如下：
    - `UNSPECIFIED`：表示未指定，TiDB 将自动选择压缩模式，当前 TiDB 自动选择 `FAST` 模式
    - `NONE`：不使用数据压缩
    - `FAST`：快速模式，整体性能较好，压缩比小于 `HIGH_COMPRESSION`
    - `HIGH_COMPRESSION`：高压缩比模式

### mpp_version <span class="version-mark">从 v6.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`UNSPECIFIED`
- 可选值：`UNSPECIFIED`，`0`，`1`，`2`，`3`
- 该变量用于指定不同版本的 MPP 执行计划。指定后，TiDB 会选择指定版本的 MPP 执行计划。该变量值含义如下：
    - `UNSPECIFIED`：表示未指定，此时 TiDB 自动选择最新版本 `3`。
    - `0`：兼容所有 TiDB 集群版本，MPP 版本大于 `0` 的新特性均不会生效。
    - `1`：从 v6.6.0 版本开始引入，用于开启 TiFlash 带压缩的数据交换，详情参见 [MPP Version 和 Exchange 数据压缩](/explain-mpp.md#mpp-version-和-exchange-数据压缩)。
    - `2`：从 v7.3.0 版本开始引入，用于确保在 TiFlash 执行出错的情况下，获取到准确的报错信息。
    - `3`：从 v9.0.0 版本开始引入，用于开启 TiFlash 新的字符串数据交换格式，以提高字符串的序列化和反序列化效率，从而提升查询性能。

### password_reuse_interval <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 4294967295]`
- 该变量用于建立密码重用策略，使 TiDB 基于经过时间限制密码重复使用。该变量默认值为 0，表示禁用基于密码经过时间的密码重用策略。当设置该变量为一个正整数 N 时，表示不允许重复使用最近 N 天内使用过的密码。

### max_connections

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 取值范围：`[0, 100000]`
- 该变量表示 TiDB 中同时允许的最大客户端连接数，用于资源控制。
- 默认情况下，该变量值为 `0` 表示不限制客户端连接数。当本变量的值大于 `0` 且客户端连接数到达此值时，TiDB 服务端将会拒绝新的客户端连接。

### max_execution_time

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 语句的最大执行时间。默认值为无限制（零）。

> **注意：**
>
> 在 v6.4.0 之前，`max_execution_time` 系统变量对所有类型的语句生效。从 v6.4.0 开始，该变量仅控制 `SELECT` 语句的最大执行时间。超时值的精度约为 100ms，即语句可能不会精确在你指定的毫秒数时终止。

<CustomContent platform="tidb">

对于包含 [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) hint 的 SQL 语句，该语句的最大执行时间受 hint 限制而非此变量。该 hint 还可以与 SQL binding 配合使用，详见 [SQL FAQ](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement)。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于包含 [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) hint 的 SQL 语句，该语句的最大执行时间受 hint 限制而非此变量。该 hint 还可以与 SQL binding 配合使用，详见 [SQL FAQ](https://docs.pingcap.com/tidb/stable/sql-faq)。

</CustomContent>

### max_prepared_stmt_count

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`[-1, 1048576]`
- 指定当前实例中 [`PREPARE`](/sql-statements/sql-statement-prepare.md) 语句的最大数量。
- 值为 `-1` 时表示不对实例中的 `PREPARE` 语句数量进行限制。
- 如果将变量值设为超过上限 `1048576`，则使用上限值 `1048576`：

```sql
mysql> SET GLOBAL max_prepared_stmt_count = 1048577;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------------+
| Level   | Code | Message                                                      |
+---------+------+--------------------------------------------------------------+
| Warning | 1292 | Truncated incorrect max_prepared_stmt_count value: '1048577' |
+---------+------+--------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'max_prepared_stmt_count';
+-------------------------+---------+
| Variable_name           | Value   |
+-------------------------+---------+
| max_prepared_stmt_count | 1048576 |
+-------------------------+---------+
1 row in set (0.00 sec)
```

### pd_enable_follower_handle_region <span class="version-mark">从 v7.6.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`。在 v9.0.0 之前，默认值为 `OFF`。
- 这个变量用于控制是否开启 [Active PD Follower 特性](/tune-region-performance.md#通过-active-pd-follower-提升-pd-region-信息查询服务的扩展能力)，目前该特性只适用于处理获取 Region 信息的相关请求。
    - 当该值为 `OFF` 时，TiDB 仅从 PD leader 获取 Region 信息。
    - 当该值为 `ON` 时，TiDB 在获取 Region 信息时会将请求均匀地发送到所有 PD 节点上，因此 PD follower 也可以处理 Region 信息请求，从而减轻 PD leader 的 CPU 压力。从 v9.0.0 开始，当该变量值为 `ON` 时，TiDB Lightning 的 Region 信息请求也会被均匀发送到所有 PD 节点。
- 适合开启 Active PD Follower 的场景：
    - 集群 Region 数量较多，PD leader 由于处理心跳和调度任务的开销大，导致 CPU 资源紧张。
    - 集群中 TiDB 实例数量较多，Region 信息请求并发量较大，PD leader CPU 压力大。

### plugin_dir

> **注意：**
>
> 该变量不适用于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 表示通过命令行参数指定的插件加载目录。

### plugin_load

> **注意：**
>
> 该变量不适用于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 表示 TiDB 启动时要加载的插件。这些插件通过命令行参数指定，多个插件之间用逗号分隔。

### port

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`4000`
- 范围：`[0, 65535]`
- 使用 MySQL 协议时 tidb-server 监听的端口。

### rand_seed1

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 该变量用于为 SQL 函数 `RAND()` 中使用的随机值生成器添加种子。
- 该变量的行为与 MySQL 兼容。

### rand_seed2

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 该变量用于为 SQL 函数 `RAND()` 中使用的随机值生成器添加种子。
- 该变量的行为与 MySQL 兼容。

### require_secure_transport <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **注意：**
>
> 目前 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 不支持该变量。请**不要**为 TiDB Cloud Dedicated 集群启用该变量，否则可能导致 SQL 客户端连接失败。该限制为临时控制措施，将在未来版本中解决。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `OFF`，[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 为 `ON`

<CustomContent platform="tidb">

- 该变量确保 TiDB 的所有连接均通过本地 socket 或使用 TLS。详情参见[为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量确保 TiDB 的所有连接均通过本地 socket 或使用 TLS。

</CustomContent>

- 将该变量设置为 `ON` 时，必须从启用了 TLS 的会话连接到 TiDB。这有助于防止 TLS 未正确配置时的锁定场景。
- 该设置以前是 `tidb.toml` 的配置选项 (`security.require-secure-transport`)，从 TiDB v6.1.0 起改为系统变量。
- 从 v6.5.6、v7.1.2、v7.5.1 和 v8.0.0 开始，当启用安全增强模式 (SEM) 时，禁止将该变量设置为 `ON`，以避免用户出现潜在的连接问题。

### skip_name_resolve <span class="version-mark">从 v5.2.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制 `tidb-server` 实例是否在连接握手过程中解析主机名。
- 当 DNS 不可靠时，可以开启该选项以提高网络性能。

> **注意：**
>
> 当 `skip_name_resolve=ON` 时，身份信息中包含主机名的用户将无法登录服务器。例如：
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> 在此示例中，建议将 `apphost` 替换为 IP 地址或通配符 (`%`)。

### socket

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 使用 MySQL 协议时，tidb-server 所监听的本地 unix 套接字文件。

### sql_mode

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
- 这个变量控制许多 MySQL 兼容行为。详情见 [SQL 模式](/sql-mode.md)。

### sql_require_primary_key <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否强制要求表必须具有主键。启用该变量后，尝试创建或修改没有主键的表将产生错误。
- 该功能基于 MySQL 8.0 中同名的 [`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key) 功能。
- 强烈建议在使用 TiCDC 时启用该变量，因为向 MySQL sink 同步变更需要表具有主键。

<CustomContent platform="tidb">

- 如果启用该变量且正在使用 TiDB Data Migration (DM) 迁移数据，建议在 [DM 任务配置文件](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)的 `session` 部分添加 `sql_require_ primary_key` 并设为 `OFF`，否则可能导致 DM 无法创建任务。

</CustomContent>

### sql_select_limit <span class="version-mark">从 v4.0.2 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`18446744073709551615`
- 范围：`[0, 18446744073709551615]`
- 单位：行
- `SELECT` 语句返回的最大行数。

### ssl_ca

<CustomContent platform="tidb">

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 证书颁发机构 (CA) 文件的位置（如果存在）。该变量的值由 TiDB 配置项 [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) 定义。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 证书颁发机构 (CA) 文件的位置（如果存在）。该变量的值由 TiDB 配置项 [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca) 定义。

</CustomContent>

### ssl_cert

<CustomContent platform="tidb">

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 用于 SSL/TLS 连接的证书文件的位置（如果存在）。该变量的值由 TiDB 配置项 [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) 定义。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 用于 SSL/TLS 连接的证书文件的位置（如果存在）。该变量的值由 TiDB 配置项 [`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert) 定义。

</CustomContent>

### ssl_key

<CustomContent platform="tidb">

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 用于 SSL/TLS 连接的私钥文件的位置（如果存在）。该变量的值由 TiDB 配置项 [`ssl-key`](/tidb-configuration-file.md#ssl-cert) 定义。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 用于 SSL/TLS 连接的私钥文件的位置（如果存在）。该变量的值由 TiDB 配置项 [`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key) 定义。

</CustomContent>

### system_time_zone

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：（随系统）
- 该变量显示首次引导启动 TiDB 时的系统时区。另请参阅 [`time_zone`](#time_zone)。

### tidb_adaptive_closest_read_threshold <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`4096`
- 取值范围：`[0, 9223372036854775807]`
- 单位：字节
- 这个变量用于控制当 [`replica-read`](#tidb_replica_read-从-v40-版本开始引入) 设置为 `closest-adaptive` 时，优先将读请求发送至 TiDB server 所在区域副本的阈值。当读请求预估的返回结果的大小超过此阈值时，TiDB 会将读请求优先发送至同一可用区的副本，否则会发送至 leader 副本。

### tidb_advancer_check_point_lag_limit <span class="version-mark">从 v8.5.5 和 v9.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：Duration
- 默认值：`48h0m0s`
- 范围：`[1s, 8760h0m0s]`
- 该变量用于控制日志备份任务 Checkpoint 的滞后时间限制。如果日志备份任务 Checkpoint 的滞后时间超过了限制，TiDB Advancer 会暂停该任务。

### tidb_allow_tiflash_cop <span class="version-mark">从 v7.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 当 TiDB 给 TiFlash 下推计算任务时，有三种方法（或协议）可供选择：Cop、BatchCop 和 MPP。相比于 Cop 和 BatchCop，MPP 协议更加成熟，提供更好的任务和资源管理。因此，更推荐使用 MPP 协议。

    * `0` 或 `OFF`：优化器仅生成使用 TiFlash MPP 协议的计划。
    * `1` 或 `ON`：优化器根据成本估算从 Cop、BatchCop 和 MPP 协议中选择一个用于生成执行计划。

### tidb_allow_batch_cop <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`1`
- 范围：`[0, 2]`
- 这个变量用于控制 TiDB 向 TiFlash 发送 coprocessor 请求的方式，有以下几种取值：

    * 0：从不批量发送请求
    * 1：aggregation 和 join 的请求会进行批量发送
    * 2：所有的 cop 请求都会批量发送

### tidb_allow_fallback_to_tikv <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：""
- 这个变量表示将 TiKV 作为备用存储引擎的存储引擎列表。当该列表中的存储引擎发生故障导致 SQL 语句执行失败时，TiDB 会使用 TiKV 作为存储引擎再次执行该 SQL 语句。目前支持设置该变量为 "" 或者 "tiflash"。如果设置该变量为 "tiflash"，当 TiFlash 返回超时错误（对应的错误码为 ErrTiFlashServerTimeout）时，TiDB 会使用 TiKV 作为存储引擎再次执行该 SQL 语句。

### tidb_allow_function_for_expression_index <span class="version-mark">从 v5.2.0 版本开始引入</span>

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_schema_valid, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash`
- 这个只读变量用于显示创建[表达式索引](/sql-statements/sql-statement-create-index.md#表达式索引)所允许使用的函数。

### tidb_allow_mpp <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制是否使用 TiFlash 的 MPP 模式执行查询，可以设置的值包括：
    - `0` 或 `OFF`，代表从不使用 MPP 模式。如果在 v7.3.0 及之后的版本将该变量值设置为 `0` 或 `OFF`，你需要同时开启 [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-从-v730-版本开始引入) 变量，否则可能遇到查询报错。
    - `1` 或 `ON`，代表由优化器根据代价估算选择是否使用 MPP 模式（默认）。

MPP 是 TiFlash 引擎提供的分布式计算框架，允许节点之间的数据交换并提供高性能、高吞吐的 SQL 算法。MPP 模式选择的详细说明参见[控制是否选择 MPP 模式](/tiflash/use-tiflash-mpp-mode.md#控制是否选择-mpp-模式)。

### tidb_allow_remove_auto_inc <span class="version-mark">从 v2.1.18、v3.0.4 版本开始引入</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否允许通过执行 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 语句来移除列的 `AUTO_INCREMENT` 属性。默认不允许。

### tidb_analyze_column_options <span class="version-mark">从 v8.3.0 版本开始引入</span>

> **注意：**
>
> - 该变量只在 [`tidb_analyze_version`](#tidb_analyze_version-从-v510-版本开始引入) 设置为 `2` 时生效。
> - 如果将 TiDB 集群从 v8.3.0 之前的版本升级至 v8.3.0 或更高版本，该变量会默认设置为 `ALL`，以保持原有行为。
> - 在 v8.3.0 到 v8.5.4 以及之间的版本中，对于新部署的 TiDB 集群，该变量默认设置为 `PREDICATE`。
> - 从 v8.5.5 和 v9.0.0 开始，对于新部署的 TiDB 集群，该变量默认设置为 `ALL`。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`ALL`
- 可选值：`ALL`，`PREDICATE`
- 该变量控制 `ANALYZE TABLE` 语句的行为。将其设置为 `PREDICATE` 表示仅收集 [predicate columns](/statistics.md#收集部分列的统计信息) 的统计信息；将其设置为 `ALL` 表示收集所有列的统计信息。在使用 OLAP 查询的场景中，建议将其设置为 `ALL`，否则查询性能可能会显著下降。

### tidb_analyze_distsql_scan_concurrency <span class="version-mark">从 v7.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`4`
- 范围：`[0, 4294967295]`。在 v8.2.0 之前版本中，最小值为 `1`。当设置为 `0` 时，TiDB 会根据集群规模自适应调整并发度。
- 这个变量用来设置执行 `ANALYZE` 时 `scan` 操作的并发度。

### tidb_analyze_partition_concurrency

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`2`。TiDB v7.4.0 及其之前版本默认值为 `1`。
- 范围：`[1, 128]`。在 v8.4.0 之前版本中，取值范围是 `[1, 18446744073709551615]`。
- 这个变量用于 TiDB analyze 分区表时，写入分区表统计信息的并发度。

### tidb_analyze_version <span class="version-mark">从 v5.1.0 版本开始引入</span>

> **警告：**
>
> 从 v8.5.6 开始，统计信息版本 1 (`tidb_analyze_version = 1`) 已被废弃，将在未来版本中移除。建议使用 `tidb_analyze_version = 2`。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`2`
- 范围：`[1, 2]`
- 控制 TiDB 收集统计信息的方式。
    - 对于 TiDB Self-Managed，从 v5.3.0 开始，该变量的默认值从 `1` 变更为 `2`。
    - 对于 TiDB Cloud，从 v6.5.0 开始，该变量的默认值从 `1` 变更为 `2`。
    - 如果集群从较早版本升级，升级后 `tidb_analyze_version` 的默认值不会发生变化。
- 关于该变量的详细介绍，参见[统计信息简介](/statistics.md)。

### tidb_analyze_skip_column_types <span class="version-mark">从 v7.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值："json,blob,mediumblob,longblob,mediumtext,longtext"。在 v8.2.0 之前，默认值为 "json,blob,mediumblob,longblob"。
- 可选值："json,blob,mediumblob,longblob,text,mediumtext,longtext"
- 这个变量表示在执行 `ANALYZE` 命令收集统计信息时，跳过哪些类型的列的统计信息收集。该变量仅适用于 [`tidb_analyze_version = 2`](#tidb_analyze_version-从-v510-版本开始引入) 的情况。即使使用 `ANALYZE TABLE t COLUMNS c1, ..., cn` 语法指定列，如果指定的列的类型在 `tidb_analyze_skip_column_types` 中，也不会收集该列的统计信息。

```sql
mysql> SHOW CREATE TABLE t;
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                             |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int DEFAULT NULL,
  `b` varchar(10) DEFAULT NULL,
  `c` json DEFAULT NULL,
  `d` blob DEFAULT NULL,
  `e` longblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT @@tidb_analyze_skip_column_types;
+----------------------------------+
| @@tidb_analyze_skip_column_types |
+----------------------------------+
| json,blob,mediumblob,longblob    |
+----------------------------------+
1 row in set (0.00 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.05 sec)

mysql> SELECT job_info FROM mysql.analyze_jobs ORDER BY end_time DESC LIMIT 1;
+---------------------------------------------------------------------+
| job_info                                                            |
+---------------------------------------------------------------------+
| analyze table columns a, b with 256 buckets, 500 topn, 1 samplerate |
+---------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> ANALYZE TABLE t COLUMNS a, c;
Query OK, 0 rows affected, 1 warning (0.04 sec)

mysql> SELECT job_info FROM mysql.analyze_jobs ORDER BY end_time DESC LIMIT 1;
+------------------------------------------------------------------+
| job_info                                                         |
+------------------------------------------------------------------+
| analyze table columns a with 256 buckets, 500 topn, 1 samplerate |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### tidb_auto_analyze_concurrency <span class="version-mark">从 v8.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1`
- 范围：`[1, 2147483647]`
- 这个变量用来设置 TiDB 集群中自动更新统计信息操作的并发度。在 v8.4.0 之前的版本中，该并发度固定为 `1`。你可以根据集群资源情况提高该并发度，从而加快统计信息收集任务的执行速度。

### tidb_auto_analyze_end_time

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：时间
- 默认值：`23:59 +0000`
- 这个变量用来设置一天中允许自动 ANALYZE 更新统计信息的结束时间。例如，只允许在 UTC 时间的凌晨 1:00 至 3:00 之间自动更新统计信息，可以设置如下：

    - `tidb_auto_analyze_start_time='01:00 +0000'`
    - `tidb_auto_analyze_end_time='03:00 +0000'`

- 如果参数中的时间包含时区信息，则使用该时区来解析；否则使用当前会话中 `time_zone` 指定的时区解析。例如 `01:00 +0000` 就是 UTC 时间的凌晨 1:00。

### tidb_auto_analyze_partition_batch_size <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`8192`。TiDB v7.6.0 之前，默认值为 `1`；v7.6.0 ~ v8.1.x，默认值为 `128`；从 v8.2.0 开始，默认值变更为 `8192`。
- 范围：`[1, 8192]`。对于 v8.2.0 之前的版本，范围为 `[1, 1024]`。
- 用于设置 TiDB [自动 analyze](/statistics.md#自动更新) 分区表（即自动收集分区表上的统计信息）时，每次同时 analyze 分区的个数。
- 若该变量值小于分区表的分区数，则 TiDB 会分多批自动 analyze 该分区表的所有分区。若该变量值大于等于分区表的分区数，则 TiDB 会同时 analyze 该分区表的所有分区。
- 若分区表个数远大于该变量值，且自动 analyze 花费时间较长，可调大该参数的值以减少耗时。

### tidb_auto_analyze_ratio

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：浮点数
- 默认值：`0.5`
- 范围：`(0, 1]`，v8.0.0 及之前版本范围为 `[0, 18446744073709551615]`。
- 这个变量用来设置 TiDB 在后台自动执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 更新统计信息的阈值。`0.5` 指的是当表中超过 50% 的行被修改时，触发自动 ANALYZE 更新。可以指定 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 来限制自动 ANALYZE 的时间。

> **注意：**
>
> 当系统变量 `tidb_enable_auto_analyze` 设置为 `ON` 时，TiDB 才会触发 `auto_analyze`。

### tidb_auto_analyze_start_time

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：时间
- 默认值：`00:00 +0000`
- 这个变量用来设置一天中允许自动 ANALYZE 更新统计信息的开始时间。例如，只允许在 UTC 时间的凌晨 1:00 至 3:00 之间自动更新统计信息，可以设置如下：

    - `tidb_auto_analyze_start_time='01:00 +0000'`
    - `tidb_auto_analyze_end_time='03:00 +0000'`

- 如果参数中的时间包含时区信息，则使用该时区来解析；否则使用当前会话中 `time_zone` 指定的时区解析。例如 `01:00 +0000` 就是 UTC 时间的凌晨 1:00。

### tidb_auto_build_stats_concurrency <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1`
- 范围：`[1, 256]`
- 这个变量用来设置执行统计信息自动更新的并发度。

### tidb_backoff_lock_fast

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`10`
- 范围：`[1, 2147483647]`
- 这个变量用来设置读请求遇到锁的 backoff 时间。

### tidb_backoff_weight

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`2`
- 范围：`[0, 2147483647]`
- 该变量用于增大 TiDB `backoff` 最大重试等待时间的权重，即在遇到内部网络或其他组件 (TiKV、PD) 故障时发送重试请求的最大重试等待时间。可以通过该变量来调整最大重试等待时间，最小值为 `1`。

    例如，TiDB 从 TiKV 获取 KV 的基础重试等待时间为 15 秒。当 `tidb_backoff_weight = 2` 时，获取 KV 的最大重试等待时间为：*基础时间 \* 2 = 30 秒*。

    在网络环境较差的情况下，适当增大该变量值可以有效缓解因超时导致的应用端错误。如果应用端希望更快收到错误信息，则应减小该变量值。

<CustomContent platform="tidb">

> **注意：**
>
> 该系统变量**不适用于**异步获取 TSO 请求的场景。如需调整获取 TSO 的超时时间，请配置 [`pd-server-timeout`](/tidb-configuration-file.md#pd-server-timeout) 配置项。

</CustomContent>

### tidb_batch_commit

> **警告：**
>
> **不建议**开启此变量。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制是否启用已废弃的 batch-commit 特性。当该变量开启时，事务可能会通过分组一些语句被拆分为多个事务，并被非原子地提交。不推荐使用这种方式。

### tidb_batch_delete

> **警告：**
>
> 该变量与废弃的 batch-dml 特性相关，可能会导致数据损坏。因此，不建议开启该变量来使用 batch-dml。作为替代，请使用[非事务 DML 语句](/non-transactional-dml.md)。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制是否启用已废弃的 batch-dml 特性中的 batch-delete 特性。当该变量开启时，`DELETE` 语句可能会被拆分为多个事务，并被非原子地提交。要使该特性生效，还需要开启 `tidb_enable_batch_dml` 并将 `tidb_dml_batch_size` 的值设置为正数。不推荐使用这种方式。

### tidb_batch_insert

> **警告：**
>
> 该变量与废弃的 batch-dml 特性相关，可能会导致数据损坏。因此，不建议开启该变量来使用 batch-dml。作为替代，请使用[非事务 DML 语句](/non-transactional-dml.md)。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制是否启用已废弃的 batch-dml 特性中的 batch-insert 特性。当该变量开启时，`INSERT` 语句可能会被拆分为多个事务，并被非原子地提交。要使该特性生效，还需要开启 `tidb_enable_batch_dml` 并将 `tidb_dml_batch_size` 的值设置为正数。不推荐使用这种方式。

### tidb_batch_pending_tiflash_count <span class="version-mark">从 v6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`4000`
- 范围：`[0, 4294967295]`
- 使用 `ALTER DATABASE SET TIFLASH REPLICA` 语句为 TiFlash 添加副本时，能容许的不可用表的个数上限。如果超过该上限，则会停止或者以非常慢的速度为库中的剩余表设置 TiFlash 副本。

### tidb_broadcast_join_threshold_count <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`10240`
- 范围：`[0, 9223372036854775807]`
- 单位：行
- 如果 join 的对象为子查询，优化器无法估计子查询结果集大小，在这种情况下通过结果集行数判断。如果子查询的行数估计值小于该变量，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。
- 开启 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入) 功能后，该变量将不再生效。

### tidb_broadcast_join_threshold_size <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`104857600` (100 MiB)
- 范围：`[0, 9223372036854775807]`
- 单位：字节
- 如果表大小（字节数）小于该值，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。
- 开启 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-从-v710-版本开始引入) 功能后，该变量将不再生效。

### tidb_build_stats_concurrency

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 单位：线程
- 默认值：`2`。TiDB v7.4.0 及其之前版本默认值为 `4`。
- 取值范围：`[1, 256]`
- 这个变量用来设置 ANALYZE 语句执行时并发度。
- 当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### tidb_build_sampling_stats_concurrency <span class="version-mark">从 v7.5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 单位：线程
- 默认值：`2`
- 取值范围：`[1, 256]`
- 这个变量用来设置 `ANALYZE` 过程中的采样并发度。
- 当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### tidb_capture_plan_baselines <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否开启[自动捕获绑定](/sql-plan-management.md#自动捕获绑定-baseline-capturing)功能。该功能依赖 Statement Summary，因此在使用自动绑定之前需打开 Statement Summary 开关。
- 开启该功能后会定期遍历一次 Statement Summary 中的历史 SQL 语句，并为至少出现两次的 SQL 语句自动创建绑定。

### tidb_cdc_write_source <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION
- 是否持久化到集群：否
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 15]`
- 当该变量被设置为非 0 值时，该会话中写入的数据将被视为由 TiCDC 写入。该变量只能由 TiCDC 修改，任何情况下都不要手动修改该变量。

### tidb_check_mb4_value_in_utf8

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于强制 `utf8` 字符集只存储[基本多文种平面 (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane) 中的值。如需存储 BMP 以外的字符，建议使用 `utf8mb4` 字符集。
- 在从早期 TiDB 版本升级集群时，如果之前的 `utf8` 检查较为宽松，可能需要禁用该选项。详情参见[升级后 FAQ](https://docs.pingcap.com/tidb/stable/upgrade-faq)。

### tidb_checksum_table_concurrency

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`4`
- 取值范围：`[1, 256]`
- 单位：线程
- 这个变量用来设置 [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) 语句执行时扫描索引的并发度。当这个变量被设置得更大时，会对其它的查询语句执行性能产生一定影响。

### tidb_committer_concurrency <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`128`
- 范围：`[1, 10000]`
- 在单个事务的提交阶段，用于执行提交操作相关请求的 goroutine 数量。
- 若提交的事务过大，事务提交时的流控队列等待耗时可能会过长。此时，可以通过调大该配置项来加速提交。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`performance.committer-concurrency`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### tidb_config

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 该变量为只读变量，用于获取当前 TiDB 服务器的配置信息。

### tidb_constraint_check_in_place

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量仅适用于乐观事务模型。悲观事务模式中的行为由 [`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 控制。
- 当这个变量设置为 `OFF` 时，唯一索引的重复值检查会被推迟到事务提交时才进行。这有助于提高性能，但对于某些应用，可能导致非预期的行为。详情见[约束](/constraints.md#乐观事务)。

    - 乐观事务模型下将 `tidb_constraint_check_in_place` 设置为 `OFF`：

        {{< copyable "sql" >}}

        ```sql
        create table t (i int key);
        insert into t values (1);
        begin optimistic;
        insert into t values (1);
        ```

        ```
        Query OK, 1 row affected
        ```

        {{< copyable "sql" >}}

        ```sql
        tidb> commit; -- 事务提交时才检查
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    - 乐观事务模型下将 `tidb_constraint_check_in_place` 设置为 `ON`：

        {{< copyable "sql" >}}

        ```sql
        set @@tidb_constraint_check_in_place=ON;
        begin optimistic;
        insert into t values (1);
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_constraint_check_in_place_pessimistic <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型

<CustomContent platform="tidb">

- 默认值：默认情况下，配置项 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) 为 `true`，因此该变量默认值为 `ON`。当 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) 设为 `false` 时，该变量默认值为 `OFF`。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 默认值：`ON`

</CustomContent>

- 该变量仅适用于悲观事务。乐观事务请使用 [`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place)。
- 当该变量设为 `OFF` 时，TiDB 会推迟唯一索引的唯一约束检查（推迟到下一次需要对该索引加锁的语句执行时，或推迟到事务提交时）。这有助于提高性能，但对于某些应用可能导致非预期的行为。详情参见[约束](/constraints.md#悲观事务)。
- 禁用该变量可能会导致 TiDB 在悲观事务中返回 `LazyUniquenessCheckFailure` 错误。发生此错误时，TiDB 会回滚当前事务。
- 禁用该变量时，不能在悲观事务中使用 [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)。
- 禁用该变量时，提交悲观事务可能会返回 `Write conflict` 或 `Duplicate entry` 错误。发生此类错误时，TiDB 会回滚当前事务。

    - 将 `tidb_constraint_check_in_place_pessimistic` 设为 `OFF` 并使用悲观事务：

        {{< copyable "sql" >}}

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=OFF;
        create table t (i int key);
        insert into t values (1);
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        Query OK, 1 row affected
        ```

        ```sql
        tidb> commit; -- 仅在事务提交时检查。
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    - 将 `tidb_constraint_check_in_place_pessimistic` 设为 `ON` 并使用悲观事务：

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_cost_model_version <span class="version-mark">从 v6.2.0 版本开始引入</span>

> **注意：**
>
> - 自 v6.5.0 开始，新创建的 TiDB 集群默认使用 Cost Model Version 2。如果从 v6.4.0 及之前版本的集群升级到 v6.5.0 及之后的版本，`tidb_cost_model_version` 的值不发生变化。
> - 切换代价模型版本可能会引起查询计划的变动。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`2`
- 取值范围：`[1, 2]`
- 可选值：
    - `1`：使用 Cost Model Version 1 代价模型。TiDB v6.4.0 及之前的版本默认使用 Cost Model Version 1。
    - `2`：使用 Cost Model Version 2 代价模型。TiDB v6.5.0 正式发布了代价模型 [Cost Model Version 2](/cost-model.md#cost-model-version-2)，在内部测试中比 Version 1 版本的代价模型更加准确。
- 代价模型会影响优化器对计划的选择，具体可见[代价模型](/cost-model.md)。

### tidb_current_ts

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 取值范围：`[0, 9223372036854775807]`
- 这个变量是一个只读变量，用来获取当前事务的时间戳。

### tidb_ddl_disk_quota <span class="version-mark">从 v6.3.0 版本开始引入</span>

<CustomContent platform="tidb-cloud" plan="starter,essential">

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)，该变量为只读。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="premium">

> **注意：**
>
> 对于 [{{{ .premium }}}](https://docs-preview.pingcap.com/tidbcloud/tidb-cloud-intro/#deployment-options)，该变量为只读。

</CustomContent>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`107374182400` (100 GiB)
- 范围：`[107374182400, 1125899906842624]` ([100 GiB, 1 PiB])
- 单位：字节
- 该变量仅在 [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630) 开启时生效。用于设置创建索引时回填过程中本地存储的使用限额。

### tidb_ddl_enable_fast_reorg <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **注意：**
>
> - 如果使用 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 集群，要通过该变量提高索引创建速度，需确保 TiDB 集群托管在 AWS 上且 TiDB 节点规格至少为 8 vCPU。
> - 对于 4 vCPU 的 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 集群，建议手动禁用 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)，以避免资源不足影响索引创建期间的集群稳定性。禁用该设置后，索引将通过事务方式创建，从而降低对集群的整体影响。
> - 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否开启 `ADD INDEX` 和 `CREATE INDEX` 的加速功能，以提高创建索引时回填的速度。将该变量设为 `ON` 可以为大数据量的表创建索引带来性能提升。
- 从 v7.1.0 起，索引加速操作支持断点续传。即使 TiDB owner 节点因故障重启或切换，TiDB 仍可从定期自动更新的断点恢复进度。
- 要验证已完成的 `ADD INDEX` 操作是否被加速，可执行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs) 语句查看 `JOB_TYPE` 列是否显示 `ingest`。

<CustomContent platform="tidb-cloud" plan="premium">

> **注意：**
>
> 对于 {{{ .premium }}}，该变量为只读。如需修改，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

<CustomContent platform="tidb">

> **注意：**
>
> * 索引加速功能需要一个可写且有足够可用空间的 [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)。如果 `temp-dir` 不可用，TiDB 将回退到非加速模式创建索引。建议将 `temp-dir` 放在 SSD 磁盘上。
>
> * 在将 TiDB 升级到 v6.5.0 或更高版本之前，建议检查 TiDB 的 [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) 路径是否正确挂载到 SSD 磁盘。确保运行 TiDB 的操作系统用户对该目录具有读写权限，否则 DDL 操作可能出现不可预知的问题。该路径是 TiDB 配置项，TiDB 重启后生效。因此，建议在升级前设置该配置项，以避免额外的重启。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> 目前，该功能与[在单条 `ALTER TABLE` 语句中修改多个列或索引](/sql-statements/sql-statement-alter-table.md)不完全兼容。在使用索引加速添加唯一索引时，需要避免在同一条语句中修改其他列或索引。

</CustomContent>

### tidb_stats_update_during_ddl <span class="version-mark">从 v8.5.4 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`OFF`
- 这个变量用于控制是否开启 DDL 内嵌的 Analyze 的行为。开启后，涉及新建索引的 DDL [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)，以及重组已有索引的 DDL（[`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) 和 [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)）将会在索引可见前自动执行统计信息收集。详情请参考[内嵌于 DDL 的 Analyze](/ddl_embedded_analyze.md)。

### tidb_enable_dist_task <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`ON`
- 该变量用于控制是否开启 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md)。开启后，DDL 和数据导入等 DXF 任务将由集群中多个 TiDB 节点分布式执行。
- 从 TiDB v7.1.0 起，DXF 支持分布式执行分区表的 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 语句。
- 从 TiDB v7.2.0 起，DXF 支持分布式执行 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 数据导入任务。
- 从 TiDB v8.1.0 起，该变量默认开启。如需将已启用 DXF 的集群升级到 v8.1.0 或更高版本，请在升级前禁用 DXF（将 `tidb_enable_dist_task` 设为 `OFF`），以避免升级期间的 `ADD INDEX` 操作导致数据索引不一致。升级后可手动启用 DXF。
- 该变量由 `tidb_ddl_distribute_reorg` 更名而来。

<CustomContent platform="tidb-cloud" plan="premium">

> **注意：**
>
> 对于 {{{ .premium }}}，该变量为只读。如需修改，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

### tidb_cloud_storage_uri <span class="version-mark">从 v7.4.0 版本开始引入</span>

> **注意：**
>
> 目前，[全局排序](/tidb-global-sort.md)会使用大量 TiDB 节点的计算与内存资源。对于在线增加索引等同时有用户业务在运行的场景，建议为集群添加新的 TiDB 节点，为这些 TiDB 节点设置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)，并连接到这些节点上创建任务。这样分布式框架就会将任务调度到这些节点上，将工作负载与其他 TiDB 节点隔离，以减少执行后端任务（如 `ADD INDEX` 和 `IMPORT INTO`）对用户业务的影响。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`""`
- 该变量用来指定[全局排序](/tidb-global-sort.md)中使用的 Amazon S3 云存储的 URI。在开启 [TiDB 分布式执行框架](/tidb-distributed-execution-framework.md)后，你可以配置 URI 指向具有访问存储所需权限的云存储路径，以此来实现全局排序的功能。更多详情，参考 [Amazon S3 的 URI 格式](/external-storage-uri.md#amazon-s3-uri-格式)。
- 以下语句支持全局排序功能：
    - [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 语句。
    - 用于将数据导入本地部署的 TiDB 的 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句。

### tidb_ddl_error_count_limit

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`512`
- 范围：`[0, 9223372036854775807]`
- 该变量用于设置 DDL 操作失败时的重试次数。当重试次数超过该参数值时，出错的 DDL 操作将被取消。

### tidb_ddl_flashback_concurrency <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`64`
- 范围：`[1, 256]`
- 该变量用于控制 [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) 的并发度。

### tidb_ddl_reorg_batch_size

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`256`
- 范围：`[32, 10240]`
- 单位：行
- 该变量用于设置 DDL 操作 `re-organize` 阶段的批量大小。例如，当 TiDB 执行 `ADD INDEX` 操作时，索引数据需要由 `tidb_ddl_reorg_worker_cnt`（数量）个并发 worker 进行回填，每个 worker 以批量方式回填索引数据。
    - 如果 `tidb_ddl_enable_fast_reorg` 设为 `OFF`，`ADD INDEX` 将以事务方式执行。如果在 `ADD INDEX` 执行期间目标列上有大量 `UPDATE` 和 `REPLACE` 等更新操作，批量大小越大，事务冲突的概率越大。在这种情况下，建议将批量大小设置为较小的值，最小值为 32。
    - 如果不存在事务冲突，或者 `tidb_ddl_enable_fast_reorg` 设为 `ON`，可以将批量大小设为较大的值，这样可以加快数据回填速度，但同时也会增加 TiKV 的写入压力。合适的批量大小还需参考 `tidb_ddl_reorg_worker_cnt` 的值。可以参考[在线负载与 `ADD INDEX` 操作交互测试](https://docs.pingcap.com/tidb/dev/online-workloads-and-add-index-operations)。
    - 从 v8.3.0 开始，该参数支持 SESSION 级别。在 GLOBAL 级别修改该参数不会影响正在运行的 DDL 语句，只会对新会话中提交的 DDL 生效。
    - 从 v8.5.0 开始，可以通过执行 `ADMIN ALTER DDL JOBS <job_id> BATCH_SIZE = <new_batch_size>;` 来修改正在运行的 DDL 任务的该参数。在 v8.5.5 之前的版本中，当 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 开启时，`ADD INDEX` DDL 不支持此操作。详情参见 [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)。

### tidb_ddl_reorg_priority

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`PRIORITY_LOW`
- 可选值：`PRIORITY_LOW`、`PRIORITY_NORMAL`、`PRIORITY_HIGH`
- 该变量用于设置 `re-organize` 阶段中执行 `ADD INDEX` 操作的优先级。
- 可以将该变量的值设置为 `PRIORITY_LOW`、`PRIORITY_NORMAL` 或 `PRIORITY_HIGH`。

### tidb_ddl_reorg_max_write_speed <span class="version-mark">从 v6.5.12、v7.5.5 和 v8.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：`0`
- 范围：`[0, 1PiB]`
- 该变量用于限制索引回填期间**单个 TiDB 节点到单个 TiKV 节点**的写入带宽。仅在开启索引创建加速（由 [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630) 变量控制）时生效。注意，当开启[全局排序](/tidb-global-sort.md)时，多个 TiDB 节点可同时向 TiKV 写入。当集群中数据量较大（如数十亿行）时，限制索引创建的写入带宽可有效降低对业务负载的影响。
- 默认值 `0` 表示不限制写入带宽。
- 可以指定带单位或不带单位的值。
    - 不带单位时，默认单位为字节/秒。例如，`67108864` 表示 64 MiB/秒。
    - 带单位时，支持 KiB、MiB、GiB 和 TiB。例如，`'1GiB'` 表示 1 GiB/秒，`'256MiB'` 表示 256 MiB/秒。

示例：

假设集群有 4 个 TiDB 节点和多个 TiKV 节点。在该集群中，每个 TiDB 节点都可以执行索引回填，且 Region 均匀分布在所有 TiKV 节点上。如果将 `tidb_ddl_reorg_max_write_speed` 设为 `100MiB`：

- 当全局排序未开启时，同一时间只有一个 TiDB 节点向 TiKV 写入。此时每个 TiKV 节点的最大写入带宽为 `100MiB`。
- 当全局排序开启时，所有 4 个 TiDB 节点可同时向 TiKV 写入。此时每个 TiKV 节点的最大写入带宽为 `4 * 100MiB = 400MiB`。

<CustomContent platform="tidb-cloud" plan="premium">

> **注意：**
>
> 对于 {{{ .premium }}}，该变量会自动调整为合适的值，用户不可修改。如需调整该设置，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

### tidb_ddl_reorg_worker_cnt

<CustomContent platform="tidb-cloud">

<CustomContent plan="starter,essential">

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)，该变量为只读。

</CustomContent>

<CustomContent plan="premium">

> **注意：**
>
> 对于 {{{ .premium }}}，修改该变量仅对 `MODIFY COLUMN` DDL 任务生效，不影响 `ADD INDEX` DDL 任务。

</CustomContent>

</CustomContent>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`4`
- 范围：`[1, 256]`
- 单位：线程
- 该变量用来设置 DDL 操作 `re-organize` 阶段的并发度。
- 从 v8.3.0 起，该参数支持 SESSION 级别设置。在 GLOBAL 级别修改该参数不会影响当前正在运行的 DDL 语句，仅对新会话中提交的 DDL 生效。
- 从 v8.5.0 起，可以通过执行 `ADMIN ALTER DDL JOBS <job_id> THREAD = <new_thread_count>;` 来修改正在运行的 DDL 任务的该参数。在 v8.5.5 之前的 TiDB 版本中，当 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 开启时不支持对 `ADD INDEX` DDL 执行该操作。详情参见 [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md)。

### tidb_enable_fast_create_table <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`。在 v8.5.0 之前，默认值为 `OFF`。
- 这个变量用于控制是否开启 [TiDB 加速建表](/accelerated-table-creation.md)。
- 从 TiDB v8.0.0 开始，支持使用 `tidb_enable_fast_create_table` 加速建表 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)。
- 该变量是由 v7.6.0 中引入的 [`tidb_ddl_version`](https://docs-archive.pingcap.com/zh/tidb/v7.6/system-variables#tidb_ddl_version-从-v760-版本开始引入) 更名而来。从 v8.0.0 开始，`tidb_ddl_version` 不再生效。
- 从 TiDB v8.5.0 开始，新创建的集群默认开启 TiDB 加速建表功能，即 `tidb_enable_fast_create_table` 默认值为 `ON`。如果从 v8.4.0 及之前版本的集群升级至 v8.5.0 及之后的版本，`tidb_enable_fast_create_table` 的默认值不发生变化。

### tidb_default_string_match_selectivity <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点型
- 默认值：`0.8`
- 范围：`[0, 1]`
- 这个变量用来设置过滤条件中的 `like`、`rlike`、`regexp` 函数在行数估算时的默认选择率，以及是否对这些函数启用 TopN 辅助估算。
- TiDB 总是会尝试利用统计信息对过滤条件中的 `like` 进行估算，但是当 `like` 匹配的字符串太复杂时，或者面对 `rlike` 或 `regexp` 时，往往无法充分利用统计信息，转而使用 `0.8` 作为选择率，造成行数估算的误差较大。
- 该变量可以用于修改这个行为，当变量被设为 `0` 以外的值时，会使用变量的值而不是默认的 `0.8` 作为选择率。
- 如果将该变量的值设为 `0`，TiDB 在对上述三个函数进行行数估算时，会尝试利用统计信息中的 TopN 进行求值来提高估算精度，同时也会考虑统计信息中的 NULL 数。求值操作预计会造成少量性能损耗。这个功能生效的前提是统计信息是在 [`tidb_analyze_version`](#tidb_analyze_version-从-v510-版本开始引入) 设为 `2` 时收集的。
- 当该变量的值被设为默认值以外的值的时候，会对 `not like`、`not rlike`、`not regexp` 的行数估算也进行相应的调整。

### tidb_disable_txn_auto_retry

> **警告：**
>
> 从 v8.0.0 开始，该变量已被废弃，TiDB 不再支持乐观事务的自动重试。作为替代方案，当遇到乐观事务冲突时，可以在应用层捕获错误并重试事务，或使用[悲观事务模式](/pessimistic-transaction.md)。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否禁用显式乐观事务的自动重试。默认值 `ON` 表示事务不会在 TiDB 中自动重试，`COMMIT` 语句可能返回需要在应用层处理的错误。

    设为 `OFF` 表示 TiDB 将自动重试事务，从而减少 `COMMIT` 语句的错误。进行此更改时需注意，可能会导致更新丢失。

    该变量不影响 TiDB 中自动提交的隐式事务和内部执行的事务。这些事务的最大重试次数由 `tidb_retry_limit` 的值决定。

    更多详情，参见[重试的局限](/optimistic-transaction.md#重试的局限性)。

    <CustomContent platform="tidb">

    该变量仅适用于乐观事务，不适用于悲观事务。悲观事务的重试次数由 [`max_retry_count`](/tidb-configuration-file.md#max-retry-count) 控制。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    该变量仅适用于乐观事务，不适用于悲观事务。悲观事务的重试次数为 256。

    </CustomContent>

### tidb_distsql_scan_concurrency

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`15`
- 范围：`[1, 256]`
- 单位：线程
- 这个变量用来设置 scan 操作的并发度。
- AP 类应用适合较大的值，TP 类应用适合较小的值。对于 AP 类应用，最大值建议不要超过所有 TiKV 节点的 CPU 核数。
- 若表的分区较多可以适当调小该参数（取决于扫描数据量的大小以及扫描频率），避免 TiKV 内存溢出 (OOM)。
- 对于仅包含 `LIMIT` 子句的简单查询，如果 `LIMIT` 行数小于 100000，该查询的 scan 操作被下推到 TiKV 时，会将该变量的值视为 `1` 进行处理，以提升执行效率。
- 对于查询语句 `SELECT MAX/MIN(col) FROM ...`，如果 `col` 列有索引且该索引的顺序与 `MAX(col)` 或 `MIN(col)` 函数所需的顺序一致，TiDB 会将该查询改写为 `SELECT col FROM ... LIMIT 1` 进行处理，该变量的值也将视为 `1` 进行处理。例如，对于 `SELECT MIN(col) FROM ...`，如果 `col` 列有升序排列的索引，TiDB 通过将该查询改写为 `SELECT col FROM ... LIMIT 1`，可以直接读取该索引中第一条数据，从而快速得到 `MIN(col)` 值。
- 在对 [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md) 表进行查询时，此变量可以控制解析慢日志文件的并发度。

### tidb_dml_batch_size

> **警告：**
>
> 该变量与废弃的 batch-dml 特性相关，可能会导致数据损坏。因此，不建议开启该变量来使用 batch-dml。作为替代，请使用[非事务 DML 语句](/non-transactional-dml.md)。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 单位：行
- 这个变量的值大于 `0` 时，TiDB 会将 `INSERT` 语句在更小的事务中批量提交。这样可减少内存使用，确保大批量修改时事务大小不会达到 `txn-total-size-limit` 限制。
- 只有变量值为 `0` 时才符合 ACID 要求。否则无法保证 TiDB 的原子性和隔离性要求。
- 要使该特性生效，还需要开启 `tidb_enable_batch_dml`，以及至少开启 `tidb_batch_insert` 和 `tidb_batch_delete` 中的一个。

> **注意：**
>
> 自 v7.0.0 起，`tidb_dml_batch_size` 对 [`LOAD DATA` 语句](/sql-statements/sql-statement-load-data.md)不再生效。

### tidb_dml_type <span class="version-mark">从 v8.0.0 版本开始引入</span>

> **警告：**
>
> 批量 DML 执行模式 (`tidb_dml_type = "bulk"`) 为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下被修改或删除。如果发现 bug，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues) 反馈。在当前版本中，当 TiDB 使用批量 DML 模式执行大事务时，可能会影响 TiCDC、TiFlash 以及 TiKV 的 resolved-ts 模块的内存使用和执行效率，并可能导致 OOM 问题。此外，BR 在遇到锁时可能会被阻塞并导致处理失败。因此，不建议在启用了这些组件或功能时使用该模式。

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：字符串
- 默认值：`"standard"`
- 可选值：`"standard"`、`"bulk"`
- 该变量控制 DML 语句的执行模式。
    - `"standard"` 表示标准 DML 执行模式，TiDB 事务在提交前缓存在内存中。该模式适用于存在潜在冲突的高并发事务场景，是默认推荐的执行模式。
    - `"bulk"` 表示 Pipelined DML 执行模式，适用于大量数据写入导致 TiDB 内存使用过高的场景。详情参见 [Pipelined DML](/pipelined-dml.md)。

### tidb_enable_1pc <span class="version-mark">从 v5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于指定是否对仅影响一个 Region 的事务启用一阶段提交功能。与常用的两阶段提交相比，一阶段提交可以大幅降低事务提交的延迟并提高吞吐量。

> **注意：**
>
> - 默认值 `ON` 仅适用于新创建的集群。如果集群是从早期 TiDB 版本升级的，将使用 `OFF` 值。
> - 开启该参数仅表示一阶段提交成为事务提交的一个可选模式。实际上，最合适的事务提交模式由 TiDB 决定。

### tidb_enable_analyze_snapshot <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制 `ANALYZE` 读取历史时刻的数据还是读取最新的数据。当该变量设置为 `ON` 时，`ANALYZE` 读取 `ANALYZE` 开始时刻的历史数据。当该变量设置为 `OFF` 时，`ANALYZE` 读取最新的数据。
- 在 v5.2 之前，`ANALYZE` 读取最新的数据。v5.2 至 v6.1 版本 `ANALYZE` 读取 `ANALYZE` 开始时刻的历史数据。

> **警告：**
>
> 如果 `ANALYZE` 读取 `ANALYZE` 开始时刻的历史数据，长时间的 `AUTO ANALYZE` 可能会因为历史数据被 GC 而出现 `GC life time is shorter than transaction duration` 的报错。

### tidb_enable_async_commit <span class="version-mark">从 v5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否开启异步提交 (Async Commit) 功能，使两阶段事务提交的第二阶段在后台异步执行。开启该功能可以降低事务提交的延迟。

> **注意：**
>
> - 默认值 `ON` 仅适用于新创建的集群。如果集群是从早期 TiDB 版本升级的，将使用 `OFF` 值。
> - 开启该参数仅表示 Async Commit 成为事务提交的一个可选模式。实际上，最合适的事务提交模式由 TiDB 决定。

### tidb_enable_auto_analyze <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制 TiDB 是否以后台操作自动更新表的统计信息。
- 该设置以前是 `tidb.toml` 的配置选项 (`performance.run-auto-analyze`)，从 TiDB v6.1.0 起改为系统变量。

### tidb_enable_auto_analyze_priority_queue <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量控制是否启用优先队列来调度自动收集统计信息的任务。开启该变量后，TiDB 会优先收集那些更有收集价值的表，例如新创建的索引、发生分区变更的分区表等。同时，TiDB 也会优先处理那些健康度较低的表，将它们安排在队列的前端。

### tidb_enable_auto_increment_in_generated

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否允许在创建生成列或者表达式索引时引用自增列。

### tidb_enable_batch_dml

> **警告：**
>
> 该变量与废弃的 batch-dml 特性相关，可能会导致数据损坏。因此，不建议开启该变量来使用 batch-dml。作为替代，请使用[非事务 DML 语句](/non-transactional-dml.md)。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制是否启用废弃的 batch-dml 特性。启用该变量后，部分语句可能会被拆分为多个事务执行，这是非原子性的，使用时需谨慎。使用 batch-dml 时，必须确保正在操作的数据没有并发操作。要使该变量生效，还需要为 `tidb_batch_dml_size` 指定一个正值，并启用 `tidb_batch_insert` 和 `tidb_batch_delete` 中的至少一个。

### tidb_enable_cascades_planner

> **警告：**
>
> 目前 cascades planner 为实验特性，不建议在生产环境中使用。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否开启 cascades planner。

### tidb_enable_check_constraint <span class="version-mark">从 v7.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否启用 [`CHECK` 约束](/constraints.md#check-约束)。

### tidb_enable_chunk_rpc <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来设置是否启用 Coprocessor 的 `Chunk` 数据编码格式。

### tidb_enable_clustered_index <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`ON`
- 可选值：`OFF`，`ON`，`INT_ONLY`
- 这个变量用于控制默认情况下表的主键是否使用[聚簇索引](/clustered-indexes.md)。“默认情况”即不显式指定 `CLUSTERED`/`NONCLUSTERED` 关键字的情况。可设置为 `OFF`/`ON`/`INT_ONLY`。
    - `OFF` 表示所有主键默认使用非聚簇索引。
    - `ON` 表示所有主键默认使用聚簇索引。
    - `INT_ONLY` 此时的行为受配置项 `alter-primary-key` 控制。如果该配置项取值为 `true`，则所有主键默认使用非聚簇索引；如果该配置项取值为 `false`，则由单个整数类型的列构成的主键默认使用聚簇索引，其他类型的主键默认使用非聚簇索引。

### tidb_enable_ddl <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`ON`
- 可选值：`OFF`、`ON`
- 该变量用于控制对应的 TiDB 实例是否可以成为 DDL owner。如果当前 TiDB 集群中只有一个 TiDB 实例，则无法阻止该实例成为 DDL owner，即不能将该变量设为 `OFF`。

### tidb_enable_collect_execution_info

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否在慢查询日志中记录每个算子的执行信息，以及是否记录[索引使用统计信息](/information-schema/information-schema-tidb-index-usage.md)。

### tidb_enable_column_tracking <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **警告：**
>
> 从 v8.3.0 开始，该变量被废弃，TiDB 默认收集 [predicate columns](/glossary.md#predicate-columns) 的统计信息。更多信息，参见 [`tidb_analyze_column_options`](#tidb_analyze_column_options-从-v830-版本开始引入)。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`，在 v8.3.0 之前，默认值为 `OFF`。
- 这个变量用于控制是否开启 TiDB 对 `PREDICATE COLUMNS` 的收集。关闭该变量后，之前收集的 `PREDICATE COLUMNS` 会被清除。详情见[收集部分列的统计信息](/statistics.md#收集部分列的统计信息)。

### tidb_enable_enhanced_security

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型

<CustomContent platform="tidb">

- 默认值：`OFF`
- 该变量表示所连接的 TiDB 服务器是否启用了安全增强模式 (SEM)。要修改该变量的值，需要在 TiDB 服务器配置文件中修改 `enable-sem` 的值并重启 TiDB 服务器。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 默认值：`ON`
- 该变量为只读变量。对于 TiDB Cloud，安全增强模式 (SEM) 默认启用。

</CustomContent>

- SEM 的设计灵感来源于 [Security-Enhanced Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) 等系统。它削弱了拥有 MySQL `SUPER` 权限的用户的能力，转而要求授予 `RESTRICTED` 细粒度权限作为替代。这些细粒度权限包括：
    - `RESTRICTED_TABLES_ADMIN`：向 `mysql` schema 中的系统表写入数据以及查看 `information_schema` 表中敏感列的能力。
    - `RESTRICTED_STATUS_ADMIN`：在 `SHOW STATUS` 命令中查看敏感变量的能力。
    - `RESTRICTED_VARIABLES_ADMIN`：在 `SHOW [GLOBAL] VARIABLES` 和 `SET` 中查看和设置敏感变量的能力。
    - `RESTRICTED_USER_ADMIN`：阻止其他用户修改或删除用户账号的能力。

### tidb_enable_exchange_partition

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于设置是否启用 [`exchange partitions with tables`](/partitioned-table.md#分区管理) 特性。默认值为 `ON`，即默认开启该功能。
- 该变量自 v6.3.0 开始废弃，其取值将固定为默认值 `ON`，即默认开启 `exchange partitions with tables`。

### tidb_enable_extended_stats

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 该变量指定 TiDB 是否收集[扩展统计信息](/extended-statistics.md)来指导优化器。

### tidb_enable_external_ts_read <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 当此变量设置为 `ON` 时，TiDB 会读取 [`tidb_external_ts`](#tidb_external_ts-从-v640-版本开始引入) 指定时间戳前的历史数据。

### tidb_external_ts <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 当 [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-从-v640-版本开始引入) 设置为 `ON` 时，TiDB 会依据该变量指定的时间戳读取历史数据。

### tidb_enable_fast_analyze

> **警告：**
>
> 从 v7.5.0 开始，该变量被废弃。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来控制是否启用统计信息快速分析功能。默认值 0 表示不开启。
- 快速分析功能开启后，TiDB 会随机采样约 10000 行的数据来构建统计信息。因此在数据分布不均匀或者数据量比较少的情况下，统计信息的准确度会比较低。这可能导致执行计划不优，比如选错索引。如果可以接受普通 `ANALYZE` 语句的执行时间，则推荐关闭快速分析功能。

### tidb_enable_fast_table_check <span class="version-mark">从 v7.2.0 版本开始引入</span>

> **注意：**
>
> 该功能对[多值索引](/sql-statements/sql-statement-create-index.md#多值索引)和前缀索引不生效。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制是否使用基于校验和的方式来快速检查表中数据和索引的一致性。默认值 `ON` 表示该功能默认开启。
- 开启后，TiDB 执行 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句的速度更快。

### tidb_enable_foreign_key <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：在 v6.6.0 之前版本中为 `OFF`，在 v6.6.0 及之后的版本中为 `ON`。
- 这个变量用于控制是否开启 `FOREIGN KEY` 特性。

### tidb_enable_gc_aware_memory_track

> **警告：**
>
> 该变量是 TiDB 内部调试变量，可能会在未来版本中移除。**请勿**设置该变量。

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否开启 GC-Aware 内存追踪。

### tidb_enable_global_index <span class="version-mark">从 v7.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量控制是否支持为分区表创建[全局索引](/global-indexes.md)。启用此变量后，你可以通过在索引定义中添加 `GLOBAL` 选项创建不包含分区表达式中所有列的唯一索引。
- 从 v8.4.0 开始，该变量被废弃。其值固定为默认值 `ON`，即默认启用[全局索引](/global-indexes.md)。

### tidb_enable_lazy_cursor_fetch <span class="version-mark">从 v8.3.0 版本开始引入</span>

> **警告：**
>
> 该变量控制的功能为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

<CustomContent platform="tidb">

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 可选值：`OFF`、`ON`
- 该变量用于控制 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result) 功能的行为。
    - 当开启 Cursor Fetch 且该变量设为 `OFF` 时，TiDB 在语句执行开始时读取全部数据，将数据存储在 TiDB 内存中，并根据客户端指定的 `FetchSize` 返回给客户端进行后续读取。如果结果集过大，TiDB 可能会将结果临时写入磁盘。
    - 当开启 Cursor Fetch 且该变量设为 `ON` 时，TiDB 不会一次性将全部数据读入 TiDB 节点，而是随着客户端的读取逐步将数据读入。
- 该变量控制的功能有以下限制：
    - 不支持显式事务中的语句。
    - 仅支持包含且仅包含 `TableReader`、`IndexReader`、`IndexLookUp`、`Projection` 和 `Selection` 算子的执行计划。
    - 使用 Lazy Cursor Fetch 的语句的执行信息不会出现在 [statements summary](/statement-summary-tables.md) 和[慢查询日志](/identify-slow-queries.md)中。
- 对于不支持的场景，其行为与将该变量设为 `OFF` 时相同。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 可选值：`OFF`、`ON`
- 该变量用于控制 [Cursor Fetch](/develop/dev-guide-connection-parameters.md#use-streamingresult-to-get-the-execution-result) 功能的行为。
    - 当开启 Cursor Fetch 且该变量设为 `OFF` 时，TiDB 在语句执行开始时读取全部数据，将数据存储在 TiDB 内存中，并根据客户端指定的 `FetchSize` 返回给客户端进行后续读取。如果结果集过大，TiDB 可能会将结果临时写入磁盘。
    - 当开启 Cursor Fetch 且该变量设为 `ON` 时，TiDB 不会一次性将全部数据读入 TiDB 节点，而是随着客户端的读取逐步将数据读入。
- 该变量控制的功能有以下限制：
    - 不支持显式事务中的语句。
    - 仅支持包含且仅包含 `TableReader`、`IndexReader`、`IndexLookUp`、`Projection` 和 `Selection` 算子的执行计划。
    - 使用 Lazy Cursor Fetch 的语句的执行信息不会出现在 [statements summary](/statement-summary-tables.md) 和[慢查询日志](https://docs.pingcap.com/tidb/stable/identify-slow-queries)中。
- 对于不支持的场景，其行为与将该变量设为 `OFF` 时相同。

</CustomContent>

### tidb_enable_non_prepared_plan_cache

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来控制是否开启[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)。
- 开启此功能可能会带来额外的内存和 CPU 开销，并不一定适用于所有场景，请根据具体的使用情况决定是否开启该功能。

### tidb_enable_non_prepared_plan_cache_for_dml <span class="version-mark">从 v7.1.0 版本开始引入</span>

> **警告：**
>
> 针对 DML 语句的非 Prepare 语句执行计划缓存目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来控制[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)是否支持 DML 语句。

### tidb_enable_gogc_tuner <span class="version-mark">从 v6.4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否开启 GOGC Tuner。

### tidb_enable_historical_stats

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`。在 v8.2.0 之前，默认值为 `ON`。
- 这个变量用来控制是否开启历史统计信息。默认值为 `OFF`，表示默认关闭历史统计信息。

### tidb_enable_historical_stats_for_capture

> **警告：**
>
> 当前版本中该变量控制的功能尚未完全生效，请保留默认值。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来控制 `PLAN REPLAYER CAPTURE` 抓取的内容是否默认带历史统计信息。默认值为 `OFF`，表示默认不带历史统计信息。

### tidb_enable_index_merge <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> - 当集群从 v4.0.0 以下版本升级到 v5.4.0 及以上版本时，该变量开关默认关闭，防止升级后计划发生变化导致回退。
> - 当集群从 v4.0.0 及以上版本升级到 v5.4.0 及以上版本时，该变量开关保持升级前的状态。
> - 对于 v5.4.0 及以上版本的新建集群，该变量开关默认开启。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制是否开启 index merge 功能。

### tidb_enable_index_merge_join

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 表示是否启用 `IndexMergeJoin` 算子。
- 该变量为 TiDB 内部变量，**不推荐使用**，否则可能会造成数据正确性问题。

### tidb_enable_legacy_instance_scope <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于允许使用 `SET SESSION` 对 `INSTANCE` 作用域的变量进行设置，用法同 `SET GLOBAL`。
- 为了兼容之前的 TiDB 版本，该变量值默认为 `ON`。

### tidb_enable_list_partition <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来设置是否开启 `LIST (COLUMNS) TABLE PARTITION` 特性。
- 从 v8.4.0 开始，该变量被废弃。其值将固定为默认值 `ON`，即默认启用 [List 分区](/partitioned-table.md#list-分区)。

### tidb_enable_local_txn

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于一个尚未发布的功能。**请勿修改该变量值**。

### tidb_enable_metadata_lock <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于设置是否开启[元数据锁](/metadata-lock.md)功能。注意，设置该变量时需确保集群中没有正在运行的 DDL 语句，否则数据可能出现不正确或不一致。

<CustomContent platform="tidb-cloud" plan="premium">

> **注意：**
>
> 对于 {{{ .premium }}}，该变量为只读。如需修改，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

### tidb_enable_mutation_checker <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于设置是否开启 mutation checker。mutation checker 是一项在 DML 语句执行过程中进行的数据索引一致性校验，校验报错会回滚当前语句。开启该校验会导致 CPU 使用轻微上升。详见[数据索引一致性报错](/troubleshoot-data-inconsistency-errors.md)。
- 对于新创建的 v6.0.0 及以上的集群，默认值为 `ON`。对于升级版本的集群，如果升级前是低于 v6.0.0 的版本，升级后默认值为 `OFF`。

### tidb_enable_new_cost_interface <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- TiDB v6.2.0 对代价模型的实现进行了代码层面的重构，这个变量用来控制是否使用重构后的代价模型 [Cost Model Version 2](/cost-model.md#cost-model-version-2)。
- 重构后的代价模型使用完全一样的代价公式，因此不会引起计划选择的变动，此开关默认打开。
- 从 v6.1 升级至 v6.2 的用户，此开关保持升级前的 `OFF` 状态，此时建议直接打开；对于从 v6.1 之前版本升级至 v6.2 的用户，此开关默认为 `ON`。

### tidb_enable_new_only_full_group_by_check <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制 TiDB 执行 `ONLY_FULL_GROUP_BY` 检查时的行为。有关 `ONLY_FULL_GROUP_BY` 的信息可以参考 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)。在 v6.1 中 TiDB 对该项检查做了更严格正确的处理。
- 由于可能存在版本升级造成的兼容性问题，在 v6.1 中该变量默认值是 `OFF`，即默认关闭。

### tidb_enable_noop_functions <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`OFF`
- 可选值：`ON`、`OFF`、`WARN`
- 默认情况下，用户尝试将某些语法用于尚未实现的功能时，TiDB 会报错。若将该变量值设为 `ON`，TiDB 则自动忽略此类功能不可用的情况，即不会报错。若用户无法更改 SQL 代码，可考虑将变量值设为 `ON`。
- 启用 `noop` 函数可以控制以下行为：
    * `LOCK IN SHARE MODE` 语法
    * `SQL_CALC_FOUND_ROWS` 语法
    * `START TRANSACTION READ ONLY` 和 `SET TRANSACTION READ ONLY` 语法
    * `tx_read_only`、`transaction_read_only`、`offline_mode`、`super_read_only`、`read_only` 以及 `sql_auto_is_null` 系统变量
    * `GROUP BY <expr> ASC|DESC` 语法

> **警告：**
>
> 该变量只有在默认值 `OFF` 时，才算是安全的。因为设置 `tidb_enable_noop_functions=1` 后，TiDB 会自动忽略某些语法而不报错，这可能会导致应用程序出现异常行为。例如，允许使用语法 `START TRANSACTION READ ONLY` 时，事务仍会处于读写模式。

### tidb_enable_noop_variables <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 若该变量值为 `OFF`，TiDB 具有以下行为：
    * 使用 `SET` 设置 `noop` 的系统变量时会报 `"setting *variable_name* has no effect in TiDB"` 的警告。
    * `SHOW [SESSION | GLOBAL] VARIABLES` 的结果不显示 `noop` 的系统变量。
    * 使用 `SELECT` 读取 `noop` 的系统变量时会报 `"variable *variable_name* has no effect in TiDB"` 的警告。
- 你可以通过 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;` 语句来检查 TiDB 实例是否曾设置和读取 `noop` 系统变量。

### tidb_enable_null_aware_anti_join <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：在 v7.0.0 之前版本中为 `OFF`，即默认关闭。在 v7.0.0 及之后的版本中为 `ON`，即默认开启。
- 这个变量用于控制 TiDB 对特殊集合算子 `NOT IN` 和 `!= ALL` 引导的子查询产生的 ANTI JOIN 是否采用 Null Aware Hash Join 的执行方式。
- 从旧版本升级到 v7.0.0 及之后版本，该功能自动开启，即该变量的值修改为默认值 `ON`。

### tidb_enable_outer_join_reorder <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 自 v6.1.0 起，TiDB 的 [Join Reorder 算法](/join-reorder.md)开始支持 Outer Join。该变量用于控制是否启用 Outer Join 的 Join Reorder。
- 对于从较低版本升级到当前版本的 TiDB：

    - 如果升级前 TiDB 的版本低于 v6.1.0，升级后该变量的默认值为 `ON`。
    - 如果升级前 TiDB 的版本等于或大于 v6.1.0，升级后该变量的默认值跟随升级前的设定值。

### tidb_enable_inl_join_inner_multi_pattern <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`。TiDB v8.3.0 及之前版本默认值为 `OFF`。
- 该变量用于控制当内表上有 `Selection`、`Projection` 或 `Aggregation` 算子时是否支持 Index Join。`OFF` 表示不支持。
- 如果将集群从 v7.0.0 之前版本升级至 v8.4.0 或之后的版本，该变量默认值为 `OFF`，即默认不支持 Index Join。

### tidb_enable_instance_plan_cache <span class="version-mark">从 v8.4.0 版本开始引入</span>

> **警告：**
>
> Instance Plan Cache 目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否开启 Instance Plan Cache 功能。该功能实现实例级执行计划缓存，允许同一个 TiDB 实例的所有会话共享执行计划缓存，从而提升内存利用率。开启该功能之前，建议关闭会话级别的 [Prepare 语句执行计划缓存](/sql-prepared-plan-cache.md)和[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)。

### tidb_enable_ordered_result_mode

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 指定是否对最终的输出结果进行自动排序。
- 例如，开启该变量后，TiDB 会将 `SELECT a, MAX(b) FROM t GROUP BY a` 处理为 `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`。

### tidb_enable_paging <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制是否使用分页 (paging) 方式发送 Coprocessor 请求。对于 [v5.4.0, v6.2.0) 区间的 TiDB 版本，该变量只对 `IndexLookup` 算子生效；对于 v6.2.0 以及之后的版本，该变量对全局生效。从 v6.4.0 版本开始，该变量默认值由 `OFF` 改成 `ON`。
- 适用场景：

    - 推荐在所有偏 OLTP 的场景下使用 paging。
    - 对于使用 `IndexLookUp` 和 `Limit` 并且 `Limit` 无法下推到 `IndexScan` 上的读请求，可能会出现读请求的延迟高、TiKV 的 Unified read pool CPU 使用率高的情况。在这种情况下，由于 `Limit` 算子只需要少部分数据，开启 [`tidb_enable_paging`](#tidb_enable_paging-从-v540-版本开始引入) 能够减少处理数据的数量，从而降低延迟、减少资源消耗。
    - 对于 [Dumpling](/dumpling-overview.md) 数据导出或者全表扫描这类的场景，开启 paging 后可以有效降低 TiDB 进程的内存消耗。

> **注意：**
>
> 对于偏 OLAP 的场景，并且以 TiKV 而非 TiFlash 作为存储引擎时，开启 paging 可能导致部分场景下性能回退。此时，你可以考虑通过该变量关闭 paging 或者通过系统变量 [`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-从-v620-版本开始引入) 和 [`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-从-v630-版本开始引入) 调整 paging size 的行数范围。

### tidb_enable_parallel_apply <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否开启 Apply 算子并发，并发数由 `tidb_executor_concurrency` 变量控制。Apply 算子用来处理关联子查询且默认无并发，所以执行速度较慢。打开 Apply 并发开关可增加并发度，提高执行速度。目前默认关闭。

### tidb_enable_parallel_hashagg_spill <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制 TiDB 是否支持并行 HashAgg 进行落盘。当该变量设置为 `ON` 时，在任意并发条件下，HashAgg 算子都可以根据内存使用情况自动触发数据落盘，从而兼顾性能和数据处理量。因此，不推荐将此变量修改为 `OFF`。从 v8.2.0 开始，将该变量设置为 `OFF` 时会产生警告。该变量将在未来版本中废弃。

### tidb_enable_pipelined_window_function

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量指定是否对[窗口函数](/functions-and-operators/window-functions.md)采用流水线的执行算法。

### tidb_enable_plan_cache_for_param_limit <span class="version-mark">从 v6.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制 Prepared Plan Cache 是否缓存 `LIMIT` 后面带变量 (`LIMIT ?`) 的执行计划。目前不支持缓存 `LIMIT` 后面带变量且变量值大于 10000 的执行计划。

### tidb_enable_plan_cache_for_subquery <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制 Prepared Plan Cache 是否缓存包含子查询的查询。

### tidb_enable_plan_replayer_capture

<CustomContent platform="tidb-cloud">

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否开启 `PLAN REPLAYER CAPTURE` 功能。默认值 `ON` 表示开启该功能。

</CustomContent>

<CustomContent platform="tidb">

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否开启 [`PLAN REPLAYER CAPTURE` 功能](/sql-plan-replayer.md#使用-plan-replayer-capture-抓取目标计划)。默认值 `ON` 表示开启该功能。

</CustomContent>

### tidb_enable_plan_replayer_continuous_capture <span class="version-mark">从 v7.0.0 版本开始引入</span>

<CustomContent platform="tidb-cloud">

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否开启 `PLAN REPLAYER CONTINUOUS CAPTURE` 功能。默认值 `OFF` 表示关闭该功能。

</CustomContent>

<CustomContent platform="tidb">

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否开启 [`PLAN REPLAYER CONTINUOUS CAPTURE` 功能](/sql-plan-replayer.md#使用-plan-replayer-continuous-capture)。默认值 `OFF` 表示关闭该功能。

</CustomContent>

### tidb_enable_point_get_cache

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 当 [`LOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) 的表锁类型设置为 `READ` 时，将该变量设置为 `ON` 可以缓存点查结果，减少重复查询的开销，从而提高单点查询的性能。

### tidb_enable_prepared_plan_cache <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制是否开启 [Prepared Plan Cache](/sql-prepared-plan-cache.md)。开启后，对 `Prepare`、`Execute` 请求的执行计划会进行缓存，以便在后续执行时跳过查询计划优化这个步骤，获得性能上的提升。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`prepared-plan-cache.enabled`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制是否统计 Prepared Plan Cache 中所缓存的执行计划占用的内存。具体可见 [Prepared Plan Cache 的内存管理](/sql-prepared-plan-cache.md#prepared-plan-cache-的内存管理)。

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">从 v5.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制优化器在统计信息过期时的行为。

<CustomContent platform="tidb">

- 优化器按以下方式判断表的统计信息是否过期：自上次对表执行 `ANALYZE` 获取统计信息以来，如果表中 80% 的行被修改（修改行数 / 总行数），优化器就认为该表的统计信息已过期。该比例可通过 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) 配置项修改。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 优化器按以下方式判断表的统计信息是否过期：自上次对表执行 `ANALYZE` 获取统计信息以来，如果表中 80% 的行被修改（修改行数 / 总行数），优化器就认为该表的统计信息已过期。

</CustomContent>

- 默认情况下（变量值为 `OFF`），当表的统计信息过期时，优化器仍然会使用该表的统计信息。如果将变量值设为 `ON`，优化器会认为该表的统计信息（除总行数外）不再可靠，转而使用 pseudo 统计信息。
- 如果表的数据频繁被修改且未及时执行 `ANALYZE`，为保持执行计划的稳定性，建议将该变量值设为 `OFF`。

### tidb_enable_rate_limit_action

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否为读数据算子开启动态内存控制功能。默认情况下，读数据算子启用 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 所允许的最大线程数来读取数据。当单条 SQL 语句的内存使用每次超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 时，读数据算子会停止一个线程。

<CustomContent platform="tidb">

- 当读数据算子只剩一个线程且单条 SQL 语句的内存使用持续超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 时，该 SQL 语句会触发其他内存控制行为，如[落盘](/system-variables.md#tidb_enable_tmp_storage_on_oom)。
- 当 SQL 语句仅执行读数据操作时，该变量能有效控制内存使用。如果需要计算操作（如 join 或聚合操作），内存使用可能不受 `tidb_mem_quota_query` 的控制，从而增加 OOM 风险。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 当读数据算子只剩一个线程且单条 SQL 语句的内存使用持续超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 时，该 SQL 语句会触发其他内存控制行为，如落盘。

</CustomContent>

### tidb_enable_resource_control <span class="version-mark">从 v6.6.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`ON`
- 类型：布尔型
- 该变量是[资源管控功能](/tidb-resource-control-ru-groups.md)的开关。当该变量设置为 `ON` 时，TiDB 集群可以基于资源组实现应用资源的隔离。

### tidb_enable_reuse_chunk <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 可选值：`OFF`，`ON`
- 该变量用于控制 TiDB 是否启用 Chunk 对象缓存。如果为 `ON`，则优先使用缓存中的 Chunk 对象，缓存中找不到申请的对象时才会从系统内存中申请。如果为 `OFF`，则直接从系统内存中申请 Chunk 对象。

### tidb_enable_shared_lock_promotion <span class="version-mark">从 v8.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否启用共享锁升级为排他锁的功能。TiDB 默认不支持 `SELECT LOCK IN SHARE MODE`，当该变量值为 `ON` 时，TiDB 会尝试将 `SELECT LOCK IN SHARE MODE` 语句升级为 `SELECT FOR UPDATE` 并真正加悲观锁。该变量默认值为 `OFF`，表示不启用共享锁升级为排他锁的功能。
- 无论 [`tidb_enable_noop_functions`](#tidb_enable_noop_functions-从-v40-版本开始引入) 是否开启，启用该变量都会对 `SELECT LOCK IN SHARE MODE` 语句生效。

### tidb_enable_slow_log

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否开启慢日志功能。

### tidb_enable_tmp_storage_on_oom

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 设置是否在单条 SQL 语句的内存使用超出系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 限制时为某些算子启用临时磁盘。
- 在 v6.3.0 之前这个开关可通过 TiDB 配置文件中的 `oom-use-tmp-storage` 项进行配置。在升级到 v6.3.0 及更新的版本后，集群会自动使用原 `oom-use-tmp-storage` 的值来初始化该开关，配置文件中 `oom-use-tmp-storage` 的新设置不再影响该开关。

### tidb_enable_stats_owner <span class="version-mark">从 v8.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`ON`
- 可选值：`OFF`、`ON`
- 用于设置该 TiDB 实例是否可以运行[统计信息自动更新](/statistics.md#自动更新)任务。若当前 TiDB 集群中只有一台 TiDB 实例，则不能禁止该实例运行统计信息自动更新，即不能设置为 `OFF`。

### tidb_enable_stmt_summary <span class="version-mark">从 v3.0.4 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否开启 Statement Summary 功能。开启后，SQL 的耗时等执行信息将被记录到 `information_schema.STATEMENTS_SUMMARY` 系统表中，用于定位和排查 SQL 性能问题。

### tidb_enable_strict_double_type_check <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制是否可以用 `DOUBLE` 类型的无效定义创建表。该设置的目的是提供一个从 TiDB 早期版本升级的方法，因为早期版本在验证类型方面不太严格。
- 该变量的默认值 `ON` 与 MySQL 兼容。

例如，由于无法保证浮点类型的精度，现在将 `DOUBLE(10)` 类型视为无效。将 `tidb_enable_strict_double_type_check` 更改为 `OFF` 后，将会创建表。如下所示：

```sql
CREATE TABLE t1 (id int, c double(10));
ERROR 1149 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use
SET tidb_enable_strict_double_type_check = 'OFF';
Query OK, 0 rows affected (0.00 sec)
CREATE TABLE t1 (id int, c double(10));
Query OK, 0 rows affected (0.09 sec)
```

> **注意：**
>
> 该设置仅适用于 `DOUBLE` 类型，因为 MySQL 允许为 `FLOAT` 类型指定精度。从 MySQL 8.0.17 开始已弃用此行为，不建议为 `FLOAT` 或 `DOUBLE` 类型指定精度。

### tidb_enable_table_partition

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`ON`
- 类型：枚举型
- 从 v8.4.0 开始，该变量被废弃。其值将固定为默认值 `ON`，即默认启用[分区表](/partitioned-table.md)。

### tidb_enable_telemetry <span class="version-mark">从 v4.0.2 版本开始引入</span>

> **警告：**
>
> - 在 v8.1.0 之前的版本中，TiDB 会定期向 PingCAP 上报遥测数据。
> - 从 v8.1.0 到 v8.5.1 版本，TiDB 移除了遥测功能，`tidb_enable_telemetry` 变量不再生效。该变量仅出于对早期版本的兼容性而保留。
> - 从 v8.5.3 开始，TiDB 重新引入遥测功能。但仅在本地记录遥测相关信息，不再通过网络向 PingCAP 发送数据。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`。从 v8.5.3 开始，默认值从 `OFF` 变更为 `ON`。

<CustomContent platform="tidb">

- 该变量用于控制是否在 TiDB 中开启遥测功能。从 v8.5.3 开始，该变量仅在 TiDB 实例的 [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) 配置项设为 `true` 时生效。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量不适用于 TiDB Cloud。

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制包含增删改的 SQL 语句中的读取操作能否下推到 TiFlash，比如：

    - `INSERT INTO SELECT` 语句中的 `SELECT` 查询（典型应用场景为 [TiFlash 查询结果物化](/tiflash/tiflash-results-materialization.md)）
    - `UPDATE` 和 `DELETE` 语句中的 `WHERE` 条件过滤
- 从 v7.1.0 开始，该变量废弃。当 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 时，优化器将根据 [SQL 模式](/sql-mode.md)及 TiFlash 副本的代价估算自行决定是否将查询下推至 TiFlash。需要注意的是，只有当前会话的 [SQL 模式](/sql-mode.md)为非严格模式（即 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 和 `STRICT_ALL_TABLES`）时，TiDB 才允许将包含增删改的 SQL 语句（如 `INSERT INTO SELECT`）中的读取操作下推至 TiFlash。

### tidb_enable_top_sql <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`

<CustomContent platform="tidb">

- 该变量用于控制是否开启 [Top SQL](/dashboard/top-sql.md) 功能。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于控制是否开启 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) 功能。

</CustomContent>

### tidb_enable_tso_follower_proxy <span class="version-mark">从 v5.3.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否开启 TSO Follower Proxy 功能。当值为 `OFF` 时，TiDB 仅从 PD leader 获取 TSO。当值为 `ON` 时，TiDB 会将 TSO 请求均匀分发到所有 PD 节点，PD follower 也可以处理 TSO 请求，从而降低 PD leader 的 CPU 压力。
- 适合开启 TSO Follower Proxy 的场景：
    * 由于 TSO 请求压力大，PD leader 的 CPU 达到瓶颈，导致 TSO RPC 请求延迟高。
    * TiDB 集群中有大量 TiDB 实例，且增大 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-从-v530-版本开始引入) 的值无法缓解 TSO RPC 请求延迟高的问题。

> **注意：**
>
> - 如果 TSO RPC 延迟升高的原因不是 PD leader 的 CPU 使用率瓶颈（如网络问题），开启 TSO Follower Proxy 可能会增加 TiDB 的执行延迟，并影响集群的 QPS 性能。
> - 该功能与 [`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-从-v840-版本开始引入) 不兼容。如果开启了该功能，[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-从-v840-版本开始引入) 将不生效。

### tidb_enable_unsafe_substitute <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否对生成列中表达式替换使用不安全的替换方式。默认值为 `OFF`，即默认关闭不安全的替换方式。详情见[生成列](/generated-columns.md)。

### tidb_enable_vectorized_expression <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制是否开启向量化执行。

### tidb_enable_window_function

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制是否开启[窗口函数](/functions-and-operators/window-functions.md)的支持。
- 由于窗口函数会使用一些保留关键字，可能导致原先可以正常执行的 SQL 语句在升级 TiDB 后无法被解析语法，此时可以将 `tidb_enable_window_function` 设置为 `OFF`。

### tidb_enable_row_level_checksum <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`

<CustomContent platform="tidb">

- 该变量用于控制是否开启 [TiCDC 单行数据正确性校验](/ticdc/ticdc-integrity-check.md)功能。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于控制是否开启 [TiCDC 单行数据正确性校验](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)功能。

</CustomContent>

- 可通过 [`TIDB_ROW_CHECKSUM()`](/functions-and-operators/tidb-functions.md#tidb_row_checksum) 函数获取行数据的校验值。

### tidb_enforce_mpp <span class="version-mark">从 v5.1 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`

<CustomContent platform="tidb">

- 如需修改此默认值，请修改 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 配置项的值。

</CustomContent>

- 控制是否忽略优化器的代价估算，强制使用 TiFlash 的 MPP 模式执行查询。可选值如下：
    - `0` 或 `OFF`，表示不强制使用 MPP 模式（默认值）。
    - `1` 或 `ON`，表示忽略代价估算，强制使用 MPP 模式。注意，该设置仅在 `tidb_allow_mpp=true` 时生效。

MPP 是 TiFlash 引擎提供的分布式计算框架，允许节点间进行数据交换，提供高性能、高吞吐的 SQL 算法。关于 MPP 模式的选择，请参考[控制是否选择 MPP 模式](/tiflash/use-tiflash-mpp-mode.md#控制是否选择-mpp-模式)。

### tidb_evolve_plan_baselines <span class="version-mark">从 v4.0 版本开始引入</span>

> **警告：**
>
> 该变量控制的功能为实验特性，不建议在生产环境中使用。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制是否启用自动演进绑定功能。该功能的详细介绍和使用方法可以参考[自动演进绑定](/sql-plan-management.md#自动演进绑定-baseline-evolution)。
- 为了减少自动演进对集群的影响，可以进行以下配置：

    - 设置 `tidb_evolve_plan_task_max_time`，限制每个执行计划运行的最长时间，其默认值为 600s；
    - 设置`tidb_evolve_plan_task_start_time` 和 `tidb_evolve_plan_task_end_time`，限制运行演进任务的时间窗口，默认值分别为 `00:00 +0000` 和 `23:59 +0000`。

### tidb_evolve_plan_task_end_time <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：时间
- 默认值：`23:59 +0000`
- 这个变量用来设置一天中允许自动演进的结束时间。

### tidb_evolve_plan_task_max_time <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`600`
- 范围：`[-1, 9223372036854775807]`
- 单位：秒
- 该变量用于限制自动演进功能中，每个执行计划运行的最长时间。

### tidb_evolve_plan_task_start_time <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：时间
- 默认值：`00:00 +0000`
- 这个变量用来设置一天中允许自动演进的开始时间。

### tidb_executor_concurrency <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`5`
- 范围：`[1, 256]`
- 单位：线程

该变量用来统一设置各个 SQL 算子的并发度，包括：

- `index lookup`
- `index lookup join`
- `hash join`
- `hash aggregation`（partial 和 final 阶段）
- `window`
- `projection`
- `sort`

`tidb_executor_concurrency` 整合了已有的系统变量，方便管理。这些变量所列如下：

+ `tidb_index_lookup_concurrency`
+ `tidb_index_lookup_join_concurrency`
+ `tidb_hash_join_concurrency`
+ `tidb_hashagg_partial_concurrency`
+ `tidb_hashagg_final_concurrency`
+ `tidb_projection_concurrency`
+ `tidb_window_concurrency`

v5.0 后，用户仍可以单独修改以上系统变量（会有废弃警告），且修改只影响单个算子。后续通过 `tidb_executor_concurrency` 的修改也不会影响该算子。若要通过 `tidb_executor_concurrency` 来管理所有算子的并发度，需要将以上所列变量的值设置为 `-1`。

对于从 v5.0 之前的版本升级到 v5.0 的系统，如果用户对上述所列变量的值没有做过改动（即 `tidb_hash_join_concurrency` 值为 `5`，其他值为 `4`），则会自动转为使用 `tidb_executor_concurrency` 来统一管理算子并发度。如果用户对上述变量的值做过改动，则沿用之前的变量对相应的算子做并发控制。

### tidb_expensive_query_time_threshold

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`60`
- 范围：`[10, 2147483647]`
- 单位：秒
- 该变量用于设置判断是否输出 expensive query 日志的阈值。expensive query 日志和慢查询日志的区别是：
    - 慢查询日志在语句执行完毕后输出。
    - expensive query 日志输出正在执行中且执行时间超过阈值的语句及其相关信息。

### tidb_expensive_txn_time_threshold <span class="version-mark">从 v7.2.0 版本开始引入</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`600`
- 范围：`[60, 2147483647]`
- 单位：秒
- 该变量用于控制记录 expensive 事务日志的阈值，默认为 600 秒。当事务的持续时间超过该阈值且事务既未提交也未回滚时，该事务将被视为 expensive 事务并被记录到日志。

### tidb_force_priority

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`NO_PRIORITY`
- 可选值：`NO_PRIORITY`、`LOW_PRIORITY`、`HIGH_PRIORITY`、`DELAYED`
- 该变量用于修改 TiDB 服务器上执行语句的默认优先级。使用场景如确保执行 OLAP 查询的特定用户比执行 OLTP 查询的用户获得更低的优先级。
- 默认值 `NO_PRIORITY` 表示不强制修改语句的优先级。

> **注意：**
>
> 从 v6.6.0 起，TiDB 支持[资源管控](/tidb-resource-control-ru-groups.md)。你可以使用该功能在不同的资源组中执行不同优先级的 SQL 语句。通过为这些资源组配置合适的配额和优先级，可以更好地调度不同优先级的 SQL 语句。当开启资源管控后，语句优先级将不再生效。建议使用[资源管控](/tidb-resource-control-ru-groups.md)来管理不同 SQL 语句的资源使用。

### tidb_foreign_key_check_in_shared_lock <span class="version-mark">从 v8.5.6 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制在悲观事务中，外键约束检查对父表中的行加锁时是否使用共享锁（而非排他锁）。开启后，多个并发事务可以同时对同一父表行执行外键检查而不互相阻塞，从而降低锁冲突并提升子表并发写入性能。

### tidb_gc_concurrency <span class="version-mark">从 v5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`-1` 或 `[1, 256]`
- 单位：线程
- 该变量用于控制 [GC (Garbage Collection)](/garbage-collection-overview.md) 过程中 [Resolve Locks](/garbage-collection-overview.md#resolve-locks) 步骤的并发线程数。
- 从 v8.3.0 开始，该变量还控制 GC 过程中 [Delete Ranges](/garbage-collection-overview.md#delete-ranges) 步骤的并发线程数。
- 该变量默认值为 `-1`，表示由 TiDB 根据负载自动确定合适的线程数。
- 当该变量设为 `[1, 256]` 范围内的值时：
    - Resolve Locks 直接使用该变量设定的值作为线程数。
    - Delete Range 使用该变量设定值的四分之一作为线程数。

### tidb_gc_enable <span class="version-mark">从 v5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否启用 TiKV 的垃圾回收 (GC) 机制。关闭 GC 会降低系统性能，因为旧版本的行数据将不再被清理。

### tidb_gc_life_time <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：Duration
- 默认值：`10m0s`
- 范围：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[10m0s, 8760h0m0s]`，[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 为 `[10m0s, 168h0m0s]`
- 每次 GC 保留数据的时限，使用 Go Duration 格式。GC 运行时，当前时间减去该值即为 safe point。

> **注意：**
>
> - 在频繁更新的场景下，将 `tidb_gc_life_time` 设为较大的值（如数天甚至数月）可能会导致以下潜在问题：
>     - 存储空间占用增大
>     - 大量的历史数据可能在一定程度上影响性能，尤其是范围查询，如 `select count(*) from t`
> - 如果存在运行时间超过 `tidb_gc_life_time` 的事务，在 GC 过程中会保留自该事务 `start_ts` 以来的数据，以确保该事务能继续执行。例如，如果 `tidb_gc_life_time` 配置为 10 分钟，而所有正在执行的事务中最早开始的事务已运行 15 分钟，GC 将保留最近 15 分钟的数据。

### tidb_gc_max_wait_time <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`86400`
- 范围：`[600, 31536000]`
- 单位：秒
- 该变量用于设置活跃事务阻塞 GC safe point 的最长时间。每次 GC 时，默认 safe point 不会超过正在执行的事务的开始时间。如果活跃事务的运行时间未超过该变量值，GC safe point 将一直被阻塞，直到运行时间超过该值。

### tidb_gc_run_interval <span class="version-mark">从 v5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：Duration
- 默认值：`10m0s`
- 范围：`[10m0s, 8760h0m0s]`
- 该变量用于指定 GC 的运行间隔，使用 Go Duration 格式，例如 `"1h30m"` 和 `"15m"`。

### tidb_gc_scan_lock_mode <span class="version-mark">从 v5.0 版本开始引入</span>

> **警告：**
>
> 目前 Green GC 为实验特性，不建议在生产环境中使用。

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`LEGACY`
- 可选值：`PHYSICAL`、`LEGACY`
    - `LEGACY`：使用旧的扫描方式，即关闭 Green GC。
    - `PHYSICAL`：使用物理扫描方式，即开启 Green GC。

<CustomContent platform="tidb">

- 该变量用于指定 GC 中 Resolve Locks（清理锁）步骤的扫描锁方式。当变量值设为 `LEGACY` 时，TiDB 按 Region 扫描锁。当使用 `PHYSICAL` 值时，各 TiKV 节点将绕过 Raft 层直接扫描数据，在开启 [Hibernate Region](/tikv-configuration-file.md#hibernate-regions) 功能时可有效减少 GC 唤醒所有 Region 的影响，从而提高 Resolve Locks 步骤的执行速度。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于指定 GC 中 Resolve Locks（清理锁）步骤的扫描锁方式。当变量值设为 `LEGACY` 时，TiDB 按 Region 扫描锁。当使用 `PHYSICAL` 值时，各 TiKV 节点将绕过 Raft 层直接扫描数据，可有效减少 GC 唤醒所有 Region 的影响，从而提高 Resolve Locks 步骤的执行速度。

</CustomContent>

### tidb_general_log

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`

<CustomContent platform="tidb-cloud">

- 该变量用于设置是否在日志中记录所有 SQL 语句。该功能默认关闭。在排查问题需要追踪所有 SQL 语句时，可以开启该功能。

</CustomContent>

<CustomContent platform="tidb">

- 该变量用于设置是否在[日志](/tidb-configuration-file.md#logfile)中记录所有 SQL 语句。该功能默认关闭。运维人员在排查问题需要追踪所有 SQL 语句时，可以开启该功能。

- 如果指定了 [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800) 配置项，general log 将单独写入指定文件。

- 配置项 [`log.format`](/tidb-configuration-file.md#format) 允许你配置日志消息格式，无论 general log 是写在单独文件还是与其他日志合并。

- [`tidb_redact_log`](#tidb_redact_log) 变量允许你对 general log 中记录的 SQL 语句进行脱敏。

- general log 仅记录执行成功的语句。执行失败的语句不会记录在 general log 中，而是以 `command dispatched failed` 消息记录在 TiDB 日志中。

- 要查看该功能的所有记录，你需要将 TiDB 配置项 [`log.level`](/tidb-configuration-file.md#level) 设为 `"info"` 或 `"debug"`，然后搜索 `"GENERAL_LOG"` 字符串。以下信息会被记录：
    - `time`：事件时间。
    - `conn`：当前会话的 ID。
    - `user`：当前会话用户。
    - `schemaVersion`：当前 schema 版本。
    - `txnStartTS`：当前事务开始的时间戳。
    - `forUpdateTS`：在悲观事务模式下，`forUpdateTS` 是 SQL 语句的当前时间戳。当悲观事务发生写冲突时，TiDB 会重试当前执行的 SQL 语句并更新该时间戳。你可以通过 [`max-retry-count`](/tidb-configuration-file.md#max-retry-count) 配置重试次数。在乐观事务模式下，`forUpdateTS` 等同于 `txnStartTS`。
    - `isReadConsistency`：表示当前事务隔离级别是否为 Read Committed (RC)。
    - `current_db`：当前数据库名称。
    - `txn_mode`：事务模式。可选值为 `OPTIMISTIC` 和 `PESSIMISTIC`。
    - `sql`：当前查询对应的 SQL 语句。

</CustomContent>

### tidb_non_prepared_plan_cache_size

> **警告：**
>
> 从 v7.1.0 开始，该变量被废弃。请使用 [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-从-v710-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`100`
- 范围：`[1, 100000]`
- 这个变量用来控制[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)最多能够缓存的计划数量。

### tidb_pre_split_regions <span class="version-mark">从 v8.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 15]`
- 该变量用于设置新建表默认的行分裂分片数。当设置了该变量为非 0 值后，执行 `CREATE TABLE` 语句时，TiDB 会为允许使用 `PRE_SPLIT_REGIONS` 的表（例如 `NONCLUSTERED` 表）自动设定该属性。详见 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)。该变量通常与 [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-从-v840-版本开始引入) 配合使用，用于为新建表进行分片以及 Region 预分裂。

### tidb_generate_binary_plan <span class="version-mark">从 v6.2.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制是否在慢日志和 Statement Summary 中生成二进制编码的执行计划。
- 当该变量设为 `ON` 时，可以在 TiDB Dashboard 中查看可视化的执行计划。注意，TiDB Dashboard 仅对该变量开启后生成的执行计划提供可视化展示。
- 可以通过执行 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan) 语句从二进制执行计划中解析出具体的执行计划。

### tidb_gogc_tuner_max_value <span class="version-mark">从 v7.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`500`
- 范围：`[10, 2147483647]`
- 该变量用来控制 GOGC Tuner 可调节 GOGC 的最大值。

### tidb_gogc_tuner_min_value <span class="version-mark">从 v7.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`100`
- 范围：`[10, 2147483647]`
- 该变量用来控制 GOGC Tuner 可调节 GOGC 的最小值。

### tidb_gogc_tuner_threshold <span class="version-mark">从 v6.4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`0.6`
- 范围：`[0, 0.9)`
- 该变量用于指定 GOGC 调优的最大内存阈值。当内存使用超过该阈值时，GOGC Tuner 将停止工作。

### tidb_guarantee_linearizability <span class="version-mark">从 v5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制异步提交 (Async Commit) 中计算 commit TS 的方式。默认情况下（值为 `ON`），两阶段提交会从 PD 请求一个新的 TS，并使用该 TS 来计算最终的 commit TS。在这种情况下，所有并发事务可保证线性一致性。
- 如果将该变量设为 `OFF`，则跳过从 PD 获取 TS 的过程，但代价是只能保证因果一致性而无法保证线性一致性。详情参见博客文章 [Async Commit, the Accelerator for Transaction Commit in TiDB 5.0](https://www.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/)。
- 对于只需要因果一致性的场景，可以将该变量设为 `OFF` 以提升性能。

### tidb_hash_exchange_with_new_collation

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该值表示是否在开启 new collation 的集群里生成 MPP hash partition exchange 算子。`true` 表示生成此算子，`false`表示不生成。
- 该变量为 TiDB 内部变量，**不推荐设置该变量**。

### tidb_hash_join_concurrency

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 这个变量用来设置 hash join 算法的并发度。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### tidb_hash_join_version <span class="version-mark">从 v8.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值：`optimized`。在 v9.0.0 之前，默认值为 `legacy`。
- 可选值：`legacy`、`optimized`
- 控制 TiDB 是否使用 [Hash Join 算子的优化版](/sql-statements/sql-statement-explain-analyze.md#hashjoinv2)。该变量设置为 `optimized` 时，TiDB 在执行 Hash Join 算子时将使用其优化版，以提升 Hash Join 性能。

> **注意：**
>
> 目前，仅 Inner、Outer、Semi 和 Anti Semi 类型的连接操作支持优化版的 Hash Join。对于其他类型的连接操作，即使将该变量设成 `optimized`，TiDB 也不会使用优化版的 Hash Join。

### tidb_hashagg_final_concurrency

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 这个变量用来设置并行 hash aggregation 算法 final 阶段的执行并发度。对于聚合函数参数不为 distinct 的情况，HashAgg 分为 partial 和 final 阶段分别并行执行。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### tidb_hashagg_partial_concurrency

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 这个变量用来设置并行 hash aggregation 算法 partial 阶段的执行并发度。对于聚合函数参数不为 distinct 的情况，HashAgg 分为 partial 和 final 阶段分别并行执行。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### tidb_historical_stats_duration <span class="version-mark">从 v6.6.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：Duration
- 默认值：`168h`，即 7 天
- 这个变量用来控制历史统计信息在存储中的保留时间。

### tidb_idle_transaction_timeout <span class="version-mark">从 v7.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 31536000]`
- 单位：秒
- 这个变量用来控制用户会话中事务的空闲超时。当用户会话处于事务状态且空闲时间超过该变量设定的值时，会话会被 Kill 掉。用户会话空闲是指没有正在执行的请求，处于等待请求的状态。
- 默认值 `0` 表示没有时间限制。

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置是否忽略关闭 Prepared Statement 的指令。
- 如果变量值设为 `ON`，Binary 协议的 `COM_STMT_CLOSE` 信号和文本协议的 [`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md) 语句都会被忽略。

### tidb_ignore_inlist_plan_digest <span class="version-mark">从 v7.6.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`。在 v8.5.6 之前，默认值为 `OFF`。
- 这个变量用来控制 TiDB 在生成执行计划摘要 (Plan Digest) 时，是否忽略不同查询中 `IN` 列表的元素差异。

    - 当为默认值 `ON` 时，TiDB 在生成执行计划摘要时，会忽略 `IN` 列表中的元素差异（包括元素数量的差异），并使用 `...` 代替 `IN` 列表中的元素。此时，相同类型的 `IN` 查询会生成相同的执行计划摘要。
    - 当设置为 `OFF` 时，TiDB 在生成执行计划摘要时，不会忽略 `IN` 列表中的元素差异（包括元素数量的差异）。`IN` 列表中的元素差异会导致生成的执行计划摘要不同。

### tidb_index_join_batch_size

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`25000`
- 范围：`[1, 2147483647]`
- 单位：行
- 这个变量用来设置 index lookup join 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_index_join_double_read_penalty_cost_rate <span class="version-mark">从 v6.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 默认值：`0`
- 范围：`[0, 18446744073709551615]`
- 这个变量用来设置是否给选择 index join 增加一些惩罚性的代价，以降低优化器选择 index join 操作的倾向，从而增加选择其他 join 方式的倾向，例如如选择 hash join 和 tiflash join 等。
- 优化器选择 index join 可能触发较多的回表请求，造成较多的资源开销，此时可以通过设置这个变量，来减少优化器选择 index join 的倾向。
- 这个变量只有在 [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-从-v620-版本开始引入) 设置为 `2` 时生效。

### tidb_index_lookup_concurrency

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 这个变量用来设置 index lookup 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### tidb_index_lookup_join_concurrency

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 这个变量用来设置 index lookup join 算法的并发度。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### tidb_index_lookup_pushdown_policy <span class="version-mark">从 v8.5.5 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值：`hint-only`
- 可选值：`hint-only`，`affinity-force`，`force`
- 该变量用于控制 TiDB 是否以及在什么条件下将 `IndexLookUp` 算子下推到 TiKV。可选值的含义如下：
    - `hint-only`（默认值）：仅在 SQL 中显式指定 [`INDEX_LOOKUP_PUSHDOWN`](/optimizer-hints.md#index_lookup_pushdownt1_name-idx1_name--idx2_name--从-v855-和-v900-版本开始引入) Hint 时，才将 `IndexLookUp` 算子下推到 TiKV。
    - `affinity-force`：仅对配置了 `AFFINITY` 选项的表自动启用下推。
    - `force`：对所有表开启 `IndexLookUp` 算子下推。

### tidb_index_merge_intersection_concurrency <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`-1`
- 范围：`[1, 256]`
- 这个变量用来设置索引合并进行交集操作时的最大并发度，仅在以动态裁剪模式访问分区表时有效。实际并发度为 `tidb_index_merge_intersection_concurrency` 与分区表分区数目两者中较小的值。
- 默认值 `-1` 表示使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 的值。

### tidb_index_lookup_size

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`20000`
- 范围：`[1, 2147483647]`
- 单位：行
- 这个变量用来设置 index lookup 操作的 batch 大小，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_index_serial_scan_concurrency

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`1`
- 范围：`[1, 256]`
- 单位：线程
- 这个变量用来设置顺序 scan 操作的并发度，AP 类应用适合较大的值，TP 类应用适合较小的值。

### tidb_init_chunk_size

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`32`
- 范围：`[1, 32]`
- 单位：行
- 这个变量用来设置执行过程中初始 chunk 的行数。默认值是 32，可设置的范围是 1～32。chunk 行数直接影响单个查询所需的内存。可以按照查询中所有的列的总宽度和 chunk 行数来粗略估算单个 chunk 所需内存，并结合执行器的并发数来粗略估算单个查询所需内存总量。建议单个 chunk 内存总量不要超过 16 MiB。

### tidb_instance_plan_cache_reserved_percentage <span class="version-mark">从 v8.4.0 版本开始引入</span>

> **警告：**
>
> Instance Plan Cache 目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：浮点型
- 默认值：`0.1`
- 范围：`[0, 1]`
- 这个变量用于控制内存驱逐后 [Instance Plan Cache](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入) 的空闲内存百分比。当 Instance Plan Cache 使用的内存达到 [`tidb_instance_plan_cache_max_size`](#tidb_instance_plan_cache_max_size-从-v840-版本开始引入) 设置的上限时，TiDB 会按照 Least Recently Used (LRU) 算法开始驱逐内存中的执行计划，直到空闲内存比例超过 [`tidb_instance_plan_cache_reserved_percentage`](#tidb_instance_plan_cache_reserved_percentage-从-v840-版本开始引入) 设定的值。

### tidb_instance_plan_cache_max_size <span class="version-mark">从 v8.4.0 版本开始引入</span>

> **警告：**
>
> Instance Plan Cache 目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`125829120`（即 120 MiB）
- 单位：字节
- 这个变量用于设置 [Instance Plan Cache](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入) 的最大内存使用量。

### tidb_isolation_read_engines <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`tikv,tiflash,tidb`
- 该变量用于设置 TiDB 在读取数据时可以使用的存储引擎列表。

### tidb_last_ddl_info <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION
- 默认值：""
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 该变量为只读变量，TiDB 内部使用该变量获取当前会话中上一个 DDL 操作的信息。
    - "query"：上一个 DDL 查询字符串。
    - "seq_num"：每个 DDL 操作的序列号，用于标识 DDL 操作的顺序。

### tidb_last_query_info <span class="version-mark">从 v4.0.14 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 这是一个只读变量。用于在 TiDB 内部查询上一条 DML 语句的事务信息。查询的事务信息包括：
    - `start_ts`：事务开始的时间戳。
    - `for_update_ts`：先前执行的 DML 语句的 `for_update_ts` 信息。这是 TiDB 用于测试的内部术语。通常，你可以忽略此信息。
    - `error`：错误消息（如果有）。
    - `ru_consumption`：执行语句的 [RU](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru) 消耗。

### tidb_last_txn_info <span class="version-mark">从 v4.0.9 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 此变量用于获取当前会话中最后一个事务的信息。这是一个只读变量。事务信息包括：
    - 事务的范围
    - 开始时间戳和提交时间戳
    - 事务的提交模式，可能是两阶段提交，一阶段提交，或者异步提交
    - 事务从异步提交或一阶段提交到两阶段提交的回退信息
    - 遇到的错误

### tidb_last_plan_replayer_token <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 这个变量是一个只读变量，用于获取当前会话中最后一个 `PLAN REPLAYER dump` 的结果。

### tidb_load_based_replica_read_threshold <span class="version-mark">从 v7.0.0 版本开始引入</span>

<CustomContent platform="tidb">

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值： `"1s"`
- 范围： `[0s, 1h]`
- 类型：字符串
- 该变量用于设置触发基于负载的 Follower Read 的阈值。当 leader 节点的预估排队时间超过该阈值时，TiDB 会优先从 follower 节点读取数据。格式为时间间隔，如 `"100ms"` 或 `"1s"`。更多详情，参见[排查读热点问题](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值： `"1s"`
- 范围： `[0s, 1h]`
- 类型：字符串
- 该变量用于设置触发基于负载的 Follower Read 的阈值。当 leader 节点的预估排队时间超过该阈值时，TiDB 会优先从 follower 节点读取数据。格式为时间间隔，如 `"100ms"` 或 `"1s"`。更多详情，参见[排查读热点问题](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#scatter-read-hotspots)。

</CustomContent>

### tidb_load_binding_timeout <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`200`
- 范围：`(0, 2147483647]`
- 单位：毫秒
- 这个变量用来控制加载 binding 的超时时间。当加载 binding 的执行时间超过该值时，会停止加载。

### tidb_lock_unchanged_keys <span class="version-mark">从 v7.1.1 和 v7.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量控制在以下场景是否对某些 key 加锁。设置为 `ON` 时，都加锁，设置为 `OFF` 时，都不加锁。
    - 在 `INSERT IGNORE` 语句和 `REPLACE` 语句中值重复的 key。在 v6.1.6 之前版本中，这些 key 不加锁。这个问题已在 [#42121](https://github.com/pingcap/tidb/issues/42121) 修复。
    - 在 `UPDATE` 语句中值没有改变的唯一索引 key。在 v6.5.2 之前版本中，这些 key 不加锁。这个问题已在 [#36438](https://github.com/pingcap/tidb/issues/36438) 修复。
- 为保证事务行为的一致性和合理性，不推荐修改该值。如果在升级 TiDB 后因为这两项修复导致严重的性能问题，且可以接受不加锁的行为（见上述 Issue），可以将该变量设置为 `OFF`。

### tidb_log_file_max_days <span class="version-mark">从 v5.3.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `0`
- 范围： `[0, 2147483647]`

<CustomContent platform="tidb">

- 该变量用于设置当前 TiDB 实例日志保留的最大天数。其默认值为配置文件中 [`max-days`](/tidb-configuration-file.md#max-days) 配置的值。修改该变量值仅影响当前 TiDB 实例。TiDB 重启后，变量值将被重置且不影响配置值。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于设置当前 TiDB 实例日志保留的最大天数。

</CustomContent>

### tidb_low_resolution_tso

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置是否启用低精度 TSO 特性。开启该功能之后，TiDB 使用缓存 Timestamp 来读取数据。缓存 Timestamp 默认每 2 秒更新一次。从 v8.0.0 开始，你可以通过 [`tidb_low_resolution_tso_update_interval`](#tidb_low_resolution_tso_update_interval-从-v800-版本开始引入) 配置缓存 Timestamp 的更新时间间隔。
- 主要场景是在可以容忍读到旧数据的情况下，降低小的只读事务获取 TSO 的开销。
- 从 v8.3.0 版本开始，该变量支持 GLOBAL 作用域。

### tidb_low_resolution_tso_update_interval <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`2000`
- 范围：`[10, 60000]`
- 这个变量用来设置低精度 TSO 特性中使用的缓存 Timestamp 的更新时间间隔，单位为毫秒。
- 该变量只在低精度 TSO 特性 [`tidb_low_resolution_tso`](#tidb_low_resolution_tso) 启用时有效。

### tidb_max_auto_analyze_time <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`43200`，即 12 小时
- 范围：`[0, 2147483647]`
- 单位：秒
- 这个变量用于指定自动 ANALYZE 的最大执行时间。当执行时间超出指定的时间时，自动 ANALYZE 会被终止。当该变量值为 0 时，自动 ANALYZE 没有最大执行时间的限制。

### tidb_max_bytes_before_tiflash_external_group_by <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值： `-1`
- 范围： `[-1, 9223372036854775807]`
- 该变量用于指定 TiFlash 中包含 `GROUP BY` 的 Hash Aggregation 算子的最大内存使用量，单位为字节。当内存使用超过指定值时，TiFlash 会触发 Hash Aggregation 算子落盘。当该变量值为 `-1` 时，TiDB 不会将此变量传递给 TiFlash。仅当该变量值大于等于 `0` 时，TiDB 才会将此变量传递给 TiFlash。当变量值为 `0` 时，表示内存使用不受限制，即 TiFlash Hash Aggregation 算子不会触发落盘。详情参见 [TiFlash 落盘](/tiflash/tiflash-spill-disk.md)。

<CustomContent platform="tidb">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，聚合通常会在多个 TiFlash 节点上分布式执行。该变量控制的是单个 TiFlash 节点上聚合算子的最大内存使用量。
> - 当该变量设为 `-1` 时，TiFlash 会根据自身配置项 [`max_bytes_before_external_group_by`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters) 的值来决定聚合算子的最大内存使用量。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，聚合通常会在多个 TiFlash 节点上分布式执行。该变量控制的是单个 TiFlash 节点上聚合算子的最大内存使用量。
> - 当该变量设为 `-1` 时，TiFlash 会根据自身配置项 `max_bytes_before_external_group_by` 的值来决定聚合算子的最大内存使用量。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_join <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值： `-1`
- 范围： `[-1, 9223372036854775807]`
- 该变量用于指定 TiFlash 中包含 `JOIN` 的 Hash Join 算子的最大内存使用量，单位为字节。当内存使用超过指定值时，TiFlash 会触发 Hash Join 算子落盘。当该变量值为 `-1` 时，TiDB 不会将此变量传递给 TiFlash。仅当该变量值大于等于 `0` 时，TiDB 才会将此变量传递给 TiFlash。当变量值为 `0` 时，表示内存使用不受限制，即 TiFlash Hash Join 算子不会触发落盘。详情参见 [TiFlash 落盘](/tiflash/tiflash-spill-disk.md)。

<CustomContent platform="tidb">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，join 通常会在多个 TiFlash 节点上分布式执行。该变量控制的是单个 TiFlash 节点上 join 算子的最大内存使用量。
> - 当该变量设为 `-1` 时，TiFlash 会根据自身配置项 [`max_bytes_before_external_join`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters) 的值来决定 join 算子的最大内存使用量。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，join 通常会在多个 TiFlash 节点上分布式执行。该变量控制的是单个 TiFlash 节点上 join 算子的最大内存使用量。
> - 当该变量设为 `-1` 时，TiFlash 会根据自身配置项 `max_bytes_before_external_join` 的值来决定 join 算子的最大内存使用量。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_sort <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值： `-1`
- 范围： `[-1, 9223372036854775807]`
- 该变量用于指定 TiFlash 中 TopN 和 Sort 算子的最大内存使用量，单位为字节。当内存使用超过指定值时，TiFlash 会触发 TopN 和 Sort 算子落盘。当该变量值为 `-1` 时，TiDB 不会将此变量传递给 TiFlash。仅当该变量值大于等于 `0` 时，TiDB 才会将此变量传递给 TiFlash。当变量值为 `0` 时，表示内存使用不受限制，即 TiFlash TopN 和 Sort 算子不会触发落盘。详情参见 [TiFlash 落盘](/tiflash/tiflash-spill-disk.md)。

<CustomContent platform="tidb">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，TopN 和 Sort 通常会在多个 TiFlash 节点上分布式执行。该变量控制的是单个 TiFlash 节点上 TopN 和 Sort 算子的最大内存使用量。
> - 当该变量设为 `-1` 时，TiFlash 会根据自身配置项 [`max_bytes_before_external_sort`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters) 的值来决定 TopN 和 Sort 算子的最大内存使用量。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，TopN 和 Sort 通常会在多个 TiFlash 节点上分布式执行。该变量控制的是单个 TiFlash 节点上 TopN 和 Sort 算子的最大内存使用量。
> - 当该变量设为 `-1` 时，TiFlash 会根据自身配置项 `max_bytes_before_external_sort` 的值来决定 TopN 和 Sort 算子的最大内存使用量。

</CustomContent>

### tidb_max_chunk_size

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1024`
- 范围：`[32, 2147483647]`
- 单位：行
- 这个变量用来设置执行过程中一个 chunk 最大的行数，设置过大可能引起缓存局部性的问题，建议该变量不要超过 65536。chunk 行数直接影响单个查询所需的内存。可以按照查询中所有的列的总宽度和 chunk 行数来粗略估算单个 chunk 所需内存，并结合执行器的并发数来粗略估算单个查询所需内存总量。建议单个 chunk 内存总量不要超过 16 MiB。当查询涉及数据量较大、单个 chunk 无法处理所有数据时，TiDB 会进行多次处理，每次处理时将 chunk 行数翻倍，从 [`tidb_init_chunk_size`](#tidb_init_chunk_size) 开始，直到 chunk 行数达到最大值 `tidb_max_chunk_size`。

### tidb_max_delta_schema_count

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1024`
- 范围：`[100, 16384]`
- 这个变量用来设置缓存 schema 版本信息（对应版本修改的相关 table IDs）的个数限制，可设置的范围 100 - 16384。此变量在 2.1.18 及之后版本支持。

### tidb_max_dist_task_nodes <span class="version-mark">从 v8.5.6 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`-1` 或 `[1, 128]`
- 该变量用于定义分布式框架任务可使用的 TiDB 节点数上限。默认值为 `-1`，表示启用自动模式。在自动模式下，TiDB 将按照 `min(3, tikv_nodes / 3)` 动态地计算该值，其中 `tikv_nodes` 表示集群中 TiKV 节点的数量。

> **注意：**
>
> 如果部分 TiDB 节点显式设置了 [`tidb_service_scope`](#tidb_service_scope-从-v740-版本开始引入)，则分布式执行框架仅会将任务调度到这些节点中执行。此时，即使 `tidb_max_dist_task_nodes` 设置了更大的值，实际使用的 TiDB 节点数也不会超过显式设置了 `tidb_service_scope` 的 TiDB 节点数。
>
> 例如，集群有 10 个 TiDB 节点，其中 4 个节点均设置了 `tidb_service_scope = group1`。此时即使设置 `tidb_max_dist_task_nodes = 5`，实际参与任务执行的节点数仍为 4。

### tidb_max_paging_size <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`50000`
- 范围：`[1, 9223372036854775807]`
- 单位：行
- 这个变量用来设置 coprocessor 协议中 paging size 的最大的行数。请合理设置该值，设置过小，TiDB 与 TiKV 的 RPC 交互会更频繁；设置过大，导数据和全表扫等特定场景会占用更多内存。该变量的默认值对于 OLTP 场景较友好，如果业务只使用了 TiKV 作为存储引擎，当执行偏 OLAP 的负载时，可以考虑将变量值调大，有可能获得更好的性能。

### tidb_max_tiflash_threads <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`[-1, 256]`
- 单位：线程
- TiFlash 中 request 执行的最大并发度。默认值为 `-1`，表示该系统变量无效，此时最大并发度取决于 TiFlash 配置项 `profiles.default.max_threads` 的设置。`0` 表示由 TiFlash 系统自动设置该值。

### tidb_mem_oom_action <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值： `CANCEL`
- 可选值：`CANCEL`、`LOG`

<CustomContent platform="tidb">

- 指定当单条 SQL 语句超过 `tidb_mem_quota_query` 指定的内存配额且无法落盘时，TiDB 执行的操作。详情参见 [TiDB 内存控制](/configure-memory-usage.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 指定当单条 SQL 语句超过 [`tidb_mem_quota_query`](#tidb_mem_quota_query) 指定的内存配额且无法落盘时，TiDB 执行的操作。

</CustomContent>

- 默认值为 `CANCEL`，但在 TiDB v4.0.2 及更早版本中，默认值为 `LOG`。
- 该设置以前是 `tidb.toml` 的配置选项 (`oom-action`)，从 TiDB v6.1.0 起改为系统变量。

### tidb_mem_quota_analyze <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **警告：**
>
> 目前限制 ANALYZE 的内存使用量为实验特性，在生产环境中使用时可能存在内存统计有误差的情况。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 单位：字节
- 取值范围：`[-1, 9223372036854775807]`
- 这个变量用来控制 TiDB 更新统计信息时的最大总内存占用，包括用户执行的 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 和 TiDB 后台自动执行的统计信息更新任务。当总的内存占用超过这个阈值时，用户执行的 `ANALYZE` 会被终止退出，并通过错误信息提示用户尝试更小的采样率或稍后重试。如果 TiDB 后台自动执行的统计信息更新任务因内存超限而退出，且使用的采样率高于默认值，则会使用默认采样率重试一次。当该变量值为负数或零时，TiDB 不对更新统计信息的前后台任务进行内存限制。

> **注意：**
>
> 只有在 TiDB 的启动配置文件中开启了 `run-auto-analyze` 选项，该 TiDB 集群才会触发 `auto_analyze`。

### tidb_mem_quota_apply_cache <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`33554432` (32 MiB)
- 范围：`[0, 9223372036854775807]`
- 单位：字节
- 这个变量用来设置 `Apply` 算子中局部 Cache 的内存使用阈值。
- `Apply` 算子中局部 Cache 用来加速 `Apply` 算子的计算，该变量可以设置 `Apply` Cache 的内存使用阈值。设置变量值为 `0` 可以关闭 `Apply` Cache 功能。

### tidb_mem_quota_binding_cache <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`67108864` (64 MiB)
- 范围：`[0, 2147483647]`
- 单位：字节
- 这个变量用来设置存放 `binding` 的缓存的内存使用阈值。
- 如果一个系统创建或者捕获了过多的绑定，导致绑定所使用的内存空间超过该阈值，TiDB 会在日志中增加警告日志进行提示。这种情况下，缓存无法存放所有可用的绑定，并且无法保证哪些绑定存在于缓存中，因此，可能存在一些查询无法使用可用绑定的情况。此时，可以调大该变量的值，从而保证所有可用绑定都能正常使用。修改变量值以后，需要执行命令 `admin reload bindings` 重新加载绑定，确保变更生效。

### tidb_mem_quota_query

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `1073741824` (1 GiB)
- 范围： `[-1, 9223372036854775807]`
- 单位：字节

<CustomContent platform="tidb">

- 在 TiDB v6.1.0 之前，该变量为会话级别变量，并使用 `tidb.toml` 中 `mem-quota-query` 的值作为初始值。从 v6.1.0 起，`tidb_mem_quota_query` 为 `SESSION | GLOBAL` 作用域变量。
- 在 TiDB v6.5.0 之前，该变量用于设置**单条查询**的内存配额阈值。如果查询执行期间的内存配额超过阈值，TiDB 将执行 [`tidb_mem_oom_action`](#tidb_mem_oom_action-从-v610-版本开始引入) 中定义的操作。
- 从 TiDB v6.5.0 起，该变量用于设置**单个会话**的内存配额阈值。如果会话执行期间的内存配额超过阈值，TiDB 将执行 [`tidb_mem_oom_action`](#tidb_mem_oom_action-从-v610-版本开始引入) 中定义的操作。注意，从 TiDB v6.5.0 起，会话的内存使用包括会话中事务所消耗的内存。关于 TiDB v6.5.0 及后续版本中事务内存使用的控制行为，参见 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)。
- 将变量值设为 `0` 或 `-1` 时，内存阈值为正无穷大。设置的值小于 128 时，值将默认为 `128`。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 在 TiDB v6.1.0 之前，该变量为会话级别变量。从 v6.1.0 起，`tidb_mem_quota_query` 为 `SESSION | GLOBAL` 作用域变量。
- 在 TiDB v6.5.0 之前，该变量用于设置**单条查询**的内存配额阈值。如果查询执行期间的内存配额超过阈值，TiDB 将执行 [`tidb_mem_oom_action`](#tidb_mem_oom_action-从-v610-版本开始引入) 中定义的操作。
- 从 TiDB v6.5.0 起，该变量用于设置**单个会话**的内存配额阈值。如果会话执行期间的内存配额超过阈值，TiDB 将执行 [`tidb_mem_oom_action`](#tidb_mem_oom_action-从-v610-版本开始引入) 中定义的操作。注意，从 TiDB v6.5.0 起，会话的内存使用包括会话中事务所消耗的内存。
- 将变量值设为 `0` 或 `-1` 时，内存阈值为正无穷大。设置的值小于 128 时，值将默认为 `128`。

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：浮点型
- 默认值：`0`
- 该变量表示在 TiDB memory debug 模式下，允许的内存统计误差值。
- 该变量用于 TiDB 内部测试，**不推荐修改该变量值**。

### tidb_memory_debug_mode_min_heap_inuse

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 该变量用于 TiDB 内部测试，**不推荐修改该变量值**，因为开启后会影响 TiDB 的性能。
- 配置此参数后，TiDB 会进入 memory debug 模式进行内存追踪准确度的分析。TiDB 会在后续执行 SQL 语句的过程中频繁触发 GC，并将实际内存使用和内存统计值做对比。若当前内存使用大于 `tidb_memory_debug_mode_min_heap_inuse` 且内存统计误差超过 `tidb_memory_debug_mode_alarm_ratio`，则会输出相关内存信息到日志和文件中。

### tidb_memory_usage_alarm_ratio

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：浮点型
- 默认值： `0.7`
- 范围： `[0.0, 1.0]`

<CustomContent platform="tidb">

- 该变量用于设置触发 tidb-server 内存告警的内存使用比例。默认情况下，当 TiDB 内存使用超过总内存的 70% 且满足任一[告警条件](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage)时，TiDB 将输出告警日志。
- 当该变量配置为 `0` 或 `1` 时，表示关闭内存阈值告警功能。
- 当该变量配置为大于 `0` 且小于 `1` 的值时，表示开启内存阈值告警功能。

    - 如果系统变量 [`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640) 的值为 `0`，内存告警阈值为 `tidb_memory-usage-alarm-ratio * 系统内存大小`。
    - 如果系统变量 `tidb_server_memory_limit` 的值大于 0，内存告警阈值为 `tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于设置触发 [tidb-server 内存告警](https://docs.pingcap.com/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage)的内存使用比例。
- 当该变量配置为 `0` 或 `1` 时，表示关闭内存阈值告警功能。
- 当该变量配置为大于 `0` 且小于 `1` 的值时，表示开启内存阈值告警功能。

</CustomContent>

### tidb_memory_usage_alarm_keep_record_num <span class="version-mark">从 v6.4.0 版本开始引入</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值： `5`
- 范围： `[1, 10000]`
- 当 tidb-server 内存使用超过内存告警阈值并触发告警时，TiDB 默认仅保留最近 5 次告警时生成的状态文件。可通过该变量调整该数量。

### tidb_merge_join_concurrency

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`1`
- 取值范围：`[1, 256]`
- 设置 `MergeJoin` 算子执行查询时的并发度。
- **不推荐设置该变量**，修改该变量值可能会造成数据正确性问题。

### tidb_merge_partition_stats_concurrency

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`1`
- 这个变量用于 TiDB analyze 分区表时，对分区表统计信息进行合并时的并发度。

### tidb_enable_async_merge_global_stats <span class="version-mark">从 v7.5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`。从 v7.5.0 之前版本升级到 v7.5.0 或之后版本时，默认值为 `OFF`。
- 这个变量用于设置 TiDB 使用异步方式合并统计信息，以避免 OOM 问题。

### tidb_metric_query_range_duration <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `60`
- 范围： `[10, 216000]`
- 单位：秒
- 该变量用于设置查询 `METRICS_SCHEMA` 时生成的 Prometheus 语句的范围持续时间。

### tidb_metric_query_step <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `60`
- 范围： `[10, 216000]`
- 单位：秒
- 该变量用于设置查询 `METRICS_SCHEMA` 时生成的 Prometheus 语句的步长。

### tidb_min_paging_size <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`128`
- 范围：`[1, 9223372036854775807]`
- 单位：行
- 这个变量用来设置 coprocessor 协议中 paging size 的最小的行数。请合理设置该值，设置过小，TiDB 与 TiKV 的 RPC 交互会更频繁；设置过大，IndexLookup 带 Limit 场景会出现性能下降。该变量的默认值对于 OLTP 场景较友好，如果业务只使用了 TiKV 作为存储引擎，当执行偏 OLAP 的负载时，可以考虑将变量值调大，有可能获得更好的性能。

![Paging size impact on TPCH](/media/paging-size-impact-on-tpch.png)

开启 [`tidb_enable_paging`](#tidb_enable_paging-从-v540-版本开始引入) 时，`tidb_min_paging_size` 和 [`tidb_max_paging_size`](#tidb_max_paging_size-从-v630-版本开始引入) 对 TPCH 的性能影响如上图所示，纵轴是执行时间，越小越好。

### tidb_mpp_store_fail_ttl

> **警告：**
>
> 从 v9.0.0 开始，该变量被废弃，其值将固定为 `0s`，意味着 TiDB 不再需要额外等待即可向新启动的 TiFlash 节点发送查询请求，无需再通过延迟来避免查询失败。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：Duration
- 默认值：`0s`。在 v8.5.3 及之前版本中默认值为 `60s`。
- 刚重启的 TiFlash 可能不能正常提供服务。为了防止查询失败，TiDB 会限制 tidb-server 向刚重启的 TiFlash 节点发送查询。这个变量表示刚重启的 TiFlash 不被发送请求的时间范围。

### tidb_multi_statement_mode <span class="version-mark">从 v4.0.11 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`OFF`
- 可选值：`OFF`，`ON`，`WARN`
- 该变量用于控制是否在同一个 `COM_QUERY` 调用中执行多个查询。
- 为了减少 SQL 注入攻击的影响，TiDB 目前默认不允许在同一 `COM_QUERY` 调用中执行多个查询。该变量可用作早期 TiDB 版本的升级路径选项。该变量值与是否允许多语句行为的对照表如下：

| 客户端设置         | `tidb_multi_statement_mode` 值 | 是否允许多语句 |
|------------------------|-----------------------------------|--------------------------------|
| Multiple Statements = ON  | OFF                               | 允许                            |
| Multiple Statements = ON  | ON                                | 允许                            |
| Multiple Statements = ON  | WARN                              | 允许                            |
| Multiple Statements = OFF | OFF                               | 不允许                             |
| Multiple Statements = OFF | ON                                | 允许                            |
| Multiple Statements = OFF | WARN                              | 允许 + 警告提示        |

> **注意：**
>
> 只有默认值 `OFF` 才是安全的。如果用户业务是专为早期 TiDB 版本而设计的，那么需要将该变量值设为 `ON`。如果用户业务需要多语句支持，建议用户使用客户端提供的设置，不要使用 `tidb_multi_statement_mode` 变量进行设置。

>
> * [go-sql-driver](https://github.com/go-sql-driver/mysql#multistatements) (`multiStatements`)
> * [Connector/J](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) (`allowMultiQueries`)
> * PHP [mysqli](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) (`mysqli_multi_query`)

### tidb_nontransactional_ignore_error <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置是否在非事务语句中立刻返回错误。当设为 `OFF` 时，在碰到第一个报错的 batch 时，非事务 DML 语句即中止，取消其后的所有 batch，返回错误。当设为 `ON` 时，当某个 batch 执行报错时，其后的 batch 会继续执行，直到所有 batch 执行完毕，返回结果时把这些错误合并后返回。

### tidb_opt_agg_push_down

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置优化器是否执行聚合函数下推到 Join，Projection 和 UnionAll 之前的优化操作。当查询中聚合操作执行很慢时，可以尝试设置该变量为 ON。

### tidb_opt_broadcast_cartesian_join

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`1`
- 范围：`[0, 2]`
- 表示是否允许 Broadcast Cartesian Join 算法。
- 值为 `0` 时表示不允许使用 Broadcast Cartesian Join 算法。值为 `1` 时表示根据 [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 的行数阈值确定是否允许使用 Broadcast Cartesian Join 算法。值为 `2` 时表示总是允许 Broadcast Cartesian Join 算法，即使表的大小超过了该阈值。
- 该变量是 TiDB 内部使用的变量，**不推荐**修改该变量的值。

### tidb_opt_concurrency_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 18446744073709551615]`
- 默认值：`3.0`
- 表示在 TiDB 中开启一个 Golang goroutine 的 CPU 开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### tidb_opt_copcpu_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 18446744073709551615]`
- 默认值：`3.0`
- 表示 TiKV 协处理器处理一行数据的 CPU 开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### tidb_opt_correlation_exp_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`1`
- 范围：`[0, 2147483647]`
- 当交叉估算方法不可用时，会采用启发式估算方法。这个变量用来控制启发式方法的行为。当值为 0 时不用启发式估算方法，大于 0 时，该变量值越大，启发式估算方法越倾向 index scan，越小越倾向 table scan。

### tidb_opt_correlation_threshold

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 默认值：`0.9`
- 范围：`[0, 1]`
- 这个变量用来设置优化器启用交叉估算 row count 方法的阈值。如果列和 handle 列之间的顺序相关性超过这个阈值，就会启用交叉估算方法。
- 交叉估算方法可以简单理解为，利用这个列的直方图来估算 handle 列需要扫的行数。

### tidb_opt_cpu_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`3.0`
- 表示 TiDB 处理一行数据的 CPU 开销。该变量是[代价模型](/cost-model.md)内部使用的变量，不建议修改该变量的值。

### tidb_opt_derive_topn <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 表示是否开启[从窗口函数中推导 TopN 或 Limit](/derive-topn-from-window.md) 的优化规则。

### tidb_opt_desc_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 18446744073709551615]`
- 默认值：`3.0`
- 表示降序扫描时，TiKV 在磁盘上扫描一行数据的开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### tidb_opt_disk_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 18446744073709551615]`
- 默认值：`1.5`
- 表示 TiDB 往临时磁盘读写一个字节数据的 I/O 开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### tidb_opt_distinct_agg_push_down

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置优化器是否执行带有 `Distinct` 的聚合函数（比如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。当查询中带有 `Distinct` 的聚合操作执行很慢时，可以尝试设置该变量为 `1`。

在以下示例中，`tidb_opt_distinct_agg_push_down` 开启前，TiDB 需要从 TiKV 读取所有数据，并在 TiDB 侧执行 `distinct`。`tidb_opt_distinct_agg_push_down` 开启后，`distinct a` 被下推到了 Coprocessor，在 `HashAgg_5` 里新增里一个 `group by` 列 `test.t.a`。

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```

### tidb_opt_enable_correlation_adjustment

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制优化器是否开启交叉估算。

### tidb_opt_enable_hash_join <span class="version-mark">从 v6.5.6、v7.1.2 和 v7.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 控制优化器是否会选择表的哈希连接。默认打开 (`ON`)。设置为 `OFF` 时，优化器在生成执行计划时会避免选择表的哈希连接，除非没有其他连接方式可用。
- 如果同时使用了 `tidb_opt_enable_hash_join` 和 `HASH_JOIN` Hint，则 `HASH_JOIN` Hint 优先级更高。即使 `tidb_opt_enable_hash_join` 被设置为 `OFF`，如果在查询中指定了 `HASH_JOIN` Hint，TiDB 优化器仍然会强制执行哈希连接计划。

### tidb_opt_enable_non_eval_scalar_subquery <span class="version-mark">从 v7.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来控制 `EXPLAIN` 语句是否禁止提前执行可以在优化阶段展开的常量子查询。该变量设置为 `OFF` 时，`EXPLAIN` 语句会在优化阶段提前展开子查询。该变量设置为 `ON` 时，`EXPLAIN` 语句不会在优化阶段展开子查询。更多信息请参考[禁止子查询提前展开](/explain-walkthrough.md#禁止子查询提前执行)。

### tidb_opt_enable_late_materialization <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制是否启用 [TiFlash 延迟物化](/tiflash/tiflash-late-materialization.md)功能。注意在 TiFlash [Fast Scan 模式](/tiflash/use-fastscan.md)下，延迟物化功能暂不可用。
- 当设置该变量为 `OFF` 关闭 TiFlash 延迟物化功能时，如果 `SELECT` 语句中包含过滤条件（`WHERE` 子句），TiFlash 会先扫描查询所需列的全部数据后再进行过滤。当设置该变量为 `ON` 开启 TiFlash 延迟物化功能时，TiFlash 会先扫描下推到 TableScan 算子的过滤条件相关的列数据，过滤得到符合条件的行后，再扫描这些行的其他列数据，继续后续计算，从而减少 IO 扫描和数据处理的计算量。

### tidb_opt_enable_mpp_shared_cte_execution <span class="version-mark">从 v7.2.0 版本开始引入</span>

> **警告：**
>
> 该变量控制的功能为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制非递归的[公共表表达式 (CTE)](/sql-statements/sql-statement-with.md) 是否可以在 TiFlash MPP 执行。默认情况下，未开启该变量时，CTE 在 TiDB 执行，相较于开启该功能，执行性能有较大差距。

### tidb_opt_enable_fuzzy_binding <span class="version-mark">从 v7.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制是否开启[跨数据库绑定执行计划](/sql-plan-management.md#跨数据库绑定执行计划-cross-db-binding)功能。

### tidb_opt_enable_no_decorrelate_in_select <span class="version-mark">从 v8.5.4 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制优化器是否对 `SELECT` 列表中包含子查询的所有查询应用 [`NO_DECORRELATE()`](/optimizer-hints.md#no_decorrelate) Hint。

### tidb_opt_enable_semi_join_rewrite <span class="version-mark">从 v8.5.4 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量控制优化器是否对包含子查询的所有查询应用 [`SEMI_JOIN_REWRITE()`](/optimizer-hints.md#semi_join_rewrite) Hint。

### tidb_opt_fix_control <span class="version-mark">从 v6.5.3、v7.1.0 版本开始引入</span>

<CustomContent platform="tidb">

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：字符串
- 默认值： `""`
- 该变量用于控制优化器的一些内部行为。
- 优化器的行为可能因用户场景或 SQL 语句而异。该变量对优化器提供了更细粒度的控制，有助于防止升级后因优化器行为变更导致的性能回退。
- 详细介绍参见[优化器 Fix Controls](/optimizer-fix-controls.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：字符串
- 默认值： `""`
- 该变量用于控制优化器的一些内部行为。
- 优化器的行为可能因用户场景或 SQL 语句而异。该变量对优化器提供了更细粒度的控制，有助于防止升级后因优化器行为变更导致的性能回退。
- 详细介绍参见[优化器 Fix Controls](/optimizer-fix-controls.md)。

</CustomContent>

### tidb_opt_force_inline_cte <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来控制是否强制 inline CTE。默认值为 `OFF`，即默认不强制 inline CTE。注意，此时依旧可以通过 `MERGE()` hint 来开启个别 CTE 的 inline。如果设置为 `ON`，则当前 session 中所有查询的 CTE（递归 CTE 除外）都会 inline。

### tidb_opt_advanced_join_hint <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制包括 [`HASH_JOIN()` Hint](/optimizer-hints.md#hash_joint1_name--tl_name-)、[`MERGE_JOIN()` Hint](/optimizer-hints.md#merge_joint1_name--tl_name-) 等用于控制连接算法的 Join Method Hint 是否会影响 Join Reorder 的优化过程，包括 [`LEADING()` Hint](/optimizer-hints.md#leadingt1_name--tl_name-) 的使用。默认值为 `ON`，即默认不影响。如果设置为 `OFF`，在一些同时使用 Join Method Hint 和 `LEADING()` Hint 的场景下可能会产生冲突。

> **注意：**
>
> v7.0.0 之前的版本行为和将该变量设置为 `OFF` 的行为一致。为确保向前兼容，从旧版本升级到 v7.0.0 及之后版本的集群，该变量会被设置成 `OFF`。为了获取更灵活的 Hint 行为，强烈建议在确保无性能回退的情况下，将该变量切换为 `ON`。

### tidb_opt_insubq_to_join_and_agg

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来设置是否开启优化规则：将子查询转成 join 和 aggregation。

    例如，打开这个优化规则后，会将下面子查询做如下变化：

    {{< copyable "sql" >}}

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    将子查询转成如下 join：

    {{< copyable "sql" >}}

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    如果 t1 在列 `aa` 上有 unique 且 not null 的限制，可以直接改写为如下，不需要添加 aggregation。

    {{< copyable "sql" >}}

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold

- 作用域: SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 这个变量用来控制 TiDB Join Reorder 算法的选择。当参与 Join Reorder 的节点个数大于该阈值时，TiDB 选择贪心算法，小于该阈值时 TiDB 选择动态规划 (dynamic programming) 算法。
- 目前对于 OLTP 的查询，推荐保持默认值。对于 OLAP 的查询，推荐将变量值设为 10~15 来获得 AP 场景下更好的连接顺序。

### tidb_opt_join_reorder_through_sel <span class="version-mark">从 v8.5.6 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于提升部分多表 JOIN 查询的连接顺序优化 (Join Reorder) 效果。当该变量值为 `ON` 时，在满足安全条件的前提下，优化器会将多个连续 JOIN 之间的过滤条件 (`Selection`) 一并纳入连接顺序优化的候选范围。在重建 JOIN 树时，优化器会将这些条件下推至更合适的位置，从而使更多表参与连接顺序优化。
- 如果开启后出现性能回退或执行计划不稳定，建议将该变量设置为 `OFF` 以关闭此功能。
- 对于包含非确定性函数或具有副作用的过滤条件（例如 `RAND()`），即使开启该变量，优化器也不会执行条件下推操作，以保证表达式的求值语义不变。

### tidb_opt_limit_push_down_threshold

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`100`
- 范围：`[0, 2147483647]`
- 这个变量用来设置将 Limit 和 TopN 算子下推到 TiKV 的阈值。
- 如果 Limit 或者 TopN 的取值小于等于这个阈值，则 Limit 和 TopN 算子会被强制下推到 TiKV。该变量可以解决部分由于估算误差导致 Limit 或者 TopN 无法被下推的问题。

### tidb_opt_memory_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`0.001`
- 表示 TiDB 存储一行数据的内存开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">从 v5.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 当该变量值为 `ON` 时，左连接始终使用内表作为构建端，右连接始终使用外表作为构建端。将该变量值设为 `OFF` 后，外连接可以灵活选择任意一边表作为构建端。

### tidb_opt_network_factor

- 作用域：SESSION | GLOBAL
- 是否持久化
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1.0`
- 表示传输 1 比特数据的网络净开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### tidb_opt_objective <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值：`moderate`
- 可选值：`moderate`、`determinate`
- 该变量用于设置优化器优化目标。`moderate` 与 TiDB v7.4.0 之前版本的默认行为保持一致，优化器会利用更多信息尝试生成更优的计划。`determinate` 则倾向于保守，保持执行计划稳定。
- 实时统计信息是 TiDB 在运行时根据 DML 语句自动更新的表的总行数以及修改的行数。该变量保持默认值 `moderate` 时，TiDB 会基于实时统计信息来生成执行计划。该变量设为 `determinate` 后，TiDB 在生成执行计划时将不再使用实时统计信息，这会让执行计划相对稳定。
- 对于长期稳定的 OLTP 业务，或者如果用户对系统已有的执行计划非常确定，则推荐使用 `determinate` 模式减少执行计划跳变的可能。同时还可以结合 [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) 来阻止统计信息的更新，进一步稳定执行计划。

### tidb_opt_ordering_index_selectivity_ratio <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 默认值：`-1`
- 范围：`[-1, 1]`
- 当一个索引满足 SQL 语句中的 `ORDER BY` 和 `LIMIT` 子句，但有部分过滤条件未被该索引覆盖时，该系统变量用于控制该索引的估算行数。
- 该变量适用的场景与系统变量 [`tidb_opt_ordering_index_selectivity_threshold`](#tidb_opt_ordering_index_selectivity_threshold-从-v700-版本开始引入) 相同。
- 与 `tidb_opt_ordering_index_selectivity_threshold` 的实现不同，该变量采用范围内符合条件的可能行数的比率或百分比。
- 取值为 `-1`（默认值）或小于 `0` 时，禁用此变量。取值在 `0` 到 `1` 之间时，对应 0% 到 100% 的比率（例如，`0.5` 对应 `50%`）。
- 在以下示例中，表 `t` 共有 1,000,000 行数据。示例使用相同查询，但应用了不同的 `tidb_opt_ordering_index_selectivity_ratio` 值。示例中的查询包含一个 `WHERE` 子句谓词，该谓词匹配少量行（1,000,000 中的 9,000 行）。存在一个支持 `ORDER BY a` 的索引（索引 `ia`），但是对 `b` 的过滤不在此索引中。根据实际的数据分布，满足 `WHERE` 子句和 `LIMIT 1` 的行可能在扫描非过滤索引时作为第一行访问到，也可能在几乎处理满足所有行后才找到。
- 每个示例中都使用了一个索引 hint，用于展示对 estRows 的影响。最终计划选择取决于是否存在代价更低的其他计划。
- 第一个示例使用默认值 `-1`，使用现有的估算公式。默认行为是，在找到符合条件的行之前，会扫描一小部分行进行估算。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = -1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | id                                | estRows | task      | access object         | operator info                   |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00    | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00    | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 109.20  | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 109.20  | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    ```

- 第二个示例使用 `0`，假设在找到符合条件的行之前，将扫描 0% 的行。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 0;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | id                                | estRows | task      | access object         | operator info                   |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00    | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00    | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 1.00    | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 1.00    | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    ```

- 第三个示例使用 `0.1`，假设在找到符合条件的行之前，将扫描 10% 的行。这个条件的过滤性较强，只有 1% 的行符合条件，因此最坏情况是找到这 1% 之前需要扫描 99% 的行。99% 中的 10% 大约是 9.9%，该数值会反映在 estRows 中。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 0.1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    | id                                | estRows  | task      | access object         | operator info                   |
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00     | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00     | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00     | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 99085.21 | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00     | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 99085.21 | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    ```

- 第四个示例使用 `1.0`，假设在找到符合条件的行之前，将扫描 100% 的行。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    | id                                | estRows   | task      | access object         | operator info                   |
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00      | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00      | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00      | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 990843.14 | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00      | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 990843.14 | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    ```

- 第五个示例也使用 `1.0`，但是增加了一个对 `a` 的谓词，限制了最坏情况下的扫描范围，因为 `WHERE a <= 9000` 匹配了索引，大约有 9,000 行符合条件。考虑到 `b` 上的过滤谓词不在索引中，所有大约 9,000 行在找到符合 `b <= 9000` 的行之前都会被扫描。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE a <= 9000 AND b <= 9000 ORDER BY a LIMIT 1;
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    | id                                 | estRows | task      | access object         | operator info                      |
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    | Limit_12                           | 1.00    | root      |                       | offset:0, count:1                  |
    | └─Projection_22                    | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c       |
    |   └─IndexLookUp_21                 | 1.00    | root      |                       |                                    |
    |     ├─IndexRangeScan_18(Build)     | 9074.99 | cop[tikv] | table:t, index:ia(a)  | range:[-inf,9000], keep order:true |
    |     └─Selection_20(Probe)          | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)                 |
    |       └─TableRowIDScan_19          | 9074.99 | cop[tikv] | table:t               | keep order:false                   |
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    ```

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 默认值：`0`
- 范围：`[0, 1]`
- 用于当 SQL 中存在 `ORDER BY` 和 `LIMIT` 子句且带有过滤条件时，控制优化器选择索引的行为。
- 对于此类查询，优化器会考虑选择对应的索引来满足 `ORDER BY` 和 `LIMIT` 子句（即使这个索引并不满足任何过滤条件）。但是由于数据分布的复杂性，优化器在这种场景下可能会选择不优的索引。
- 该变量表示一个阈值。当存在索引能满足过滤条件，且其选择率估算值低于该阈值时，优化器会避免选择用于满足 `ORDER BY` 和 `LIMIT` 的索引，而优先选择用于满足过滤条件的索引。
- 例如，当把该变量设为 `0` 时，优化器保持默认行为；当设为 `1` 时，优化器总是优先选择满足过滤条件的索引，避免选择满足 `ORDER BY` 和 `LIMIT` 的索引。
- 在以下示例中，`t` 表共有 1,000,000 行数据。使用 `b` 列上的索引时，其估算行数是大约 8,748 行，因此其选择率估算值大约是 0.0087。默认情况下，优化器选择了 `a` 列上的索引。而将该变量设为 `0.01` 之后，由于 `b` 列上的索引的选择率 (0.0087) 低于 0.01，优化器选择了 `b` 列上的索引。

```sql
> EXPLAIN SELECT * FROM t WHERE b <= 9000 ORDER BY a LIMIT 1;
+-----------------------------------+---------+-----------+----------------------+--------------------+
| id                                | estRows | task      | access object        | operator info      |
+-----------------------------------+---------+-----------+----------------------+--------------------+
| Limit_12                          | 1.00    | root      |                      | offset:0, count:1  |
| └─Projection_25                   | 1.00    | root      |                      | test.t.a, test.t.b |
|   └─IndexLookUp_24                | 1.00    | root      |                      |                    |
|     ├─IndexFullScan_21(Build)     | 114.30  | cop[tikv] | table:t, index:ia(a) | keep order:true    |
|     └─Selection_23(Probe)         | 1.00    | cop[tikv] |                      | le(test.t.b, 9000) |
|       └─TableRowIDScan_22         | 114.30  | cop[tikv] | table:t              | keep order:false   |
+-----------------------------------+---------+-----------+----------------------+--------------------+

> SET SESSION tidb_opt_ordering_index_selectivity_threshold = 0.01;

> EXPLAIN SELECT * FROM t WHERE b <= 9000 ORDER BY a LIMIT 1;
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
| id                               | estRows | task      | access object        | operator info                       |
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
| TopN_9                           | 1.00    | root      |                      | test.t.a, offset:0, count:1         |
| └─IndexLookUp_20                 | 1.00    | root      |                      |                                     |
|   ├─IndexRangeScan_17(Build)     | 8748.62 | cop[tikv] | table:t, index:ib(b) | range:[-inf,9000], keep order:false |
|   └─TopN_19(Probe)               | 1.00    | cop[tikv] |                      | test.t.a, offset:0, count:1         |
|     └─TableRowIDScan_18          | 8748.62 | cop[tikv] | table:t              | keep order:false                    |
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
```

### tidb_opt_partial_ordered_index_for_topn <span class="version-mark">从 v8.5.6 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值：`DISABLE`
- 可选值：`DISABLE`、`COST`
- 用于控制当查询包含 `ORDER BY ... LIMIT` 时，优化器是否可以利用索引的部分有序性 (partial order) 来优化 TopN 计算过程。当排序列与索引顺序一致时（例如排序列本身是索引列，或该列使用了前缀索引），通过索引扫描得到的数据在该列上已经具有一定的顺序（即“部分有序”）。在这种情况下，优化器可以在扫描过程中逐步构建 TopN 结果，并在满足 `LIMIT` 后提前停止扫描，从而减少排序计算开销。
- 适用场景：`ORDER BY ... LIMIT` 的排序列为较长字符串且仅建立了前缀索引时，如需减少 TopN 排序开销时，可以通过将该变量设置为 `COST` 并在查询中指定 `USE INDEX` 或 `FORCE INDEX` Hint 以应用 partial order TopN 优化。

    - 该变量默认值为 `DISABLE`，代表关闭 partial order TopN 优化。此时，优化器将直接使用常规的全局排序 TopN 方式。
   - 如需强制应用 partial order TopN 优化，请将该变量设置为 `COST` 并在查询中通过 `USE INDEX` 或 `FORCE INDEX` Hint 指定满足条件的索引。如果指定的索引不满足该优化的前置条件（例如 `ORDER BY` 与索引前缀不匹配，或者查询中存在不支持的排序形式），即使该变量设置为 `COST` 也可能无法应用该优化，执行计划会退化为常规的 TopN 方式。

    > **注意：**
    >
    > 目前优化器尚不支持根据 cost model 动态选择是否应用 partial order TopN 优化。如果只将该变量设置为 `COST` 而不指定 `USE INDEX` 或 `FORCE INDEX` Hint，优化器可能不会应用 partial order TopN 优化。如需强制应用该优化，请结合 `USE INDEX` 或 `FORCE INDEX` Hint 一起使用。

<details>
<summary>查看 partial order TopN 优化示例</summary>

创建表 `t_varchar`，并在字符串列 `name` 上定义了前缀索引 `idx_name_prefix(name(10))`：

```sql
CREATE TABLE t_varchar (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    INDEX idx_name_prefix(name(10))
);
```

- 强制应用 partial order TopN 优化（`COST` + `USE INDEX`）：

    ```sql
    > SET SESSION tidb_opt_partial_ordered_index_for_topn = 'COST';

    > EXPLAIN FORMAT='brief' SELECT /*+ use_index(t_varchar, idx_name_prefix) */ *
        FROM t_varchar ORDER BY name LIMIT 5;
    +-------------------------------------------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------+
    | id                                        | estRows | task      | access object                | operator info                                                                                |
    +-------------------------------------------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------+
    | TopN                                      | 5.00    | root      |                              | planner__core__partial_order_topn.t_varchar.name, offset:0, count:5, prefix_col:planner__core__partial_order_topn.t_varchar.name, prefix_len:10 |
    | └─IndexLookUp                             | 5.00    | root      |                              |                                                                                              |
    |   ├─Limit(Build)                          | 5.00    | cop[tikv] |                              | offset:0, count:5, prefix_col:planner__core__partial_order_topn.t_varchar.name, prefix_len:10 |
    |   │ └─IndexFullScan                       | 10000.00| cop[tikv] | table:t_varchar, index:idx_name_prefix(name) | keep order:true, stats:pseudo                                               |
    |   └─TableRowIDScan(Probe)                 | 5.00    | cop[tikv] | table:t_varchar              | keep order:false, stats:pseudo                                                               |
    +-------------------------------------------+---------+-----------+------------------------------+----------------------------------------------------------------------------------------------+
    ```

- 关闭 partial order TopN 优化（`DISABLE`）：

    ```sql
    > SET SESSION tidb_opt_partial_ordered_index_for_topn = 'DISABLE';

    > EXPLAIN FORMAT='brief' SELECT * FROM t_varchar ORDER BY name LIMIT 5;
    +---------------------------+---------+-----------+---------------------+----------------------------------------------------+
    | id                        | estRows | task      | access object       | operator info                                      |
    +---------------------------+---------+-----------+---------------------+----------------------------------------------------+
    | TopN                      | 5.00    | root      |                     | planner__core__partial_order_topn.t_varchar.name, offset:0, count:5 |
    | └─TableReader             | 5.00    | root      | data:TopN           |                                                    |
    |   └─TopN                  | 5.00    | cop[tikv] |                     | planner__core__partial_order_topn.t_varchar.name, offset:0, count:5 |
    |     └─TableFullScan       | 10000.00| cop[tikv] | table:t_varchar     | keep order:false, stats:pseudo                     |
    +---------------------------+---------+-----------+---------------------+----------------------------------------------------+
    ```

</details>

### tidb_opt_prefer_range_scan <span class="version-mark">从 v5.0 版本开始引入</span>

> **注意：**
>
> 从 v8.4.0 开始，此变量的默认值从 `OFF` 更改为 `ON`。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 该变量值为 `ON` 时，对于没有统计信息的表（伪统计信息）或空表（零统计信息），优化器将优先选择区间扫描而不是全表扫描。
- 在以下示例中，`tidb_opt_prefer_range_scan` 开启前，TiDB 优化器需要执行全表扫描。`tidb_opt_prefer_range_scan` 开启后，优化器选择了索引区间扫描。

```sql
explain select * from t where age=5;
+-------------------------+------------+-----------+---------------+-------------------+
| id                      | estRows    | task      | access object | operator info     |
+-------------------------+------------+-----------+---------------+-------------------+
| TableReader_7           | 1048576.00 | root      |               | data:Selection_6  |
| └─Selection_6           | 1048576.00 | cop[tikv] |               | eq(test.t.age, 5) |
|   └─TableFullScan_5     | 1048576.00 | cop[tikv] | table:t       | keep order:false  |
+-------------------------+------------+-----------+---------------+-------------------+
3 rows in set (0.00 sec)

set session tidb_opt_prefer_range_scan = 1;

explain select * from t where age=5;
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| id                            | estRows    | task      | access object               | operator info                 |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| IndexLookUp_7                 | 1048576.00 | root      |                             |                               |
| ├─IndexRangeScan_5(Build)     | 1048576.00 | cop[tikv] | table:t, index:idx_age(age) | range:[5,5], keep order:false |
| └─TableRowIDScan_6(Probe)     | 1048576.00 | cop[tikv] | table:t                     | keep order:false              |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
3 rows in set (0.00 sec)
```

### tidb_opt_prefix_index_single_scan <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制 TiDB 优化器是否将某些过滤条件下推到前缀索引，尽量避免不必要的回表，从而提高查询性能。
- 将该变量设置为 `ON` 时，会将过滤条件下推到前缀索引。此时，假设一张表中 `col` 列是索引前缀列，查询语句中的 `col is null` 或者 `col is not null` 条件会被归为索引上的过滤条件，而不是回表时的过滤条件，从而避免不必要的回表。

<details>
<summary>该变量的使用示例</summary>

创建一张带前缀索引的表：

```sql
CREATE TABLE t (a INT, b VARCHAR(10), c INT, INDEX idx_a_b(a, b(5)));
```

此时关闭 `tidb_opt_prefix_index_single_scan`：

```sql
SET tidb_opt_prefix_index_single_scan = 'OFF';
```

对于以下查询，执行计划使用了前缀索引 `idx_a_b` 但需要回表（出现了 `IndexLookUp` 算子）。

```sql
EXPLAIN FORMAT='brief' SELECT COUNT(1) FROM t WHERE a = 1 AND b IS NOT NULL;
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| id                            | estRows | task      | access object                | operator info                                         |
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| HashAgg                       | 1.00    | root      |                              | funcs:count(Column#8)->Column#5                       |
| └─IndexLookUp                 | 1.00    | root      |                              |                                                       |
|   ├─IndexRangeScan(Build)     | 99.90   | cop[tikv] | table:t, index:idx_a_b(a, b) | range:[1 -inf,1 +inf], keep order:false, stats:pseudo |
|   └─HashAgg(Probe)            | 1.00    | cop[tikv] |                              | funcs:count(1)->Column#8                              |
|     └─Selection               | 99.90   | cop[tikv] |                              | not(isnull(test.t.b))                                 |
|       └─TableRowIDScan        | 99.90   | cop[tikv] | table:t                      | keep order:false, stats:pseudo                        |
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
6 rows in set (0.00 sec)
```

此时打开 `tidb_opt_prefix_index_single_scan`：

```sql
SET tidb_opt_prefix_index_single_scan = 'ON';
```

开启该变量后，对于以下查询，执行计划使用了前缀索引 `idx_a_b` 且不需要回表。

```sql
EXPLAIN FORMAT='brief' SELECT COUNT(1) FROM t WHERE a = 1 AND b IS NOT NULL;
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| id                       | estRows | task      | access object                | operator info                                         |
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| StreamAgg                | 1.00    | root      |                              | funcs:count(Column#7)->Column#5                       |
| └─IndexReader            | 1.00    | root      |                              | index:StreamAgg                                       |
|   └─StreamAgg            | 1.00    | cop[tikv] |                              | funcs:count(1)->Column#7                              |
|     └─IndexRangeScan     | 99.90   | cop[tikv] | table:t, index:idx_a_b(a, b) | range:[1 -inf,1 +inf], keep order:false, stats:pseudo |
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
4 rows in set (0.00 sec)
```

</details>

### tidb_opt_projection_push_down <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`。在 v8.3.0 之前，默认值为 `OFF`。
- 指定是否允许优化器将 `Projection` 算子下推到 TiKV。开启后，优化器可能会将以下三种类型的 `Projection` 算子下推到 TiKV：
    - 算子顶层表达式全部为 [JSON 查询类函数](/functions-and-operators/json-functions/json-functions-search.md)或 [JSON 值属性类函数](/functions-and-operators/json-functions/json-functions-return.md)，例如 `SELECT JSON_EXTRACT(data, '$.name') FROM users;`。
    - 算子顶层表达式部分为 JSON 查询类函数或 JSON 值属性类函数，部分为直接的列读取，例如 `SELECT JSON_DEPTH(data), name FROM users;`。
    - 算子顶层表达式全部为直接的列读取，且输出的列数量小于输入的列数量，例如 `SELECT name FROM users;`。
- `Projection` 算子最终下推与否，还取决于优化器对查询代价的综合评估。
- 对于从 v8.3.0 以前的版本升级到 v8.3.0 或更新版本的 TiDB 集群，该变量将默认为 `OFF`。

### tidb_opt_range_max_size <span class="version-mark">从 v6.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`67108864` (64 MiB)
- 取值范围：`[0, 9223372036854775807]`
- 单位：字节
- 该变量用于指定优化器构造扫描范围的内存用量上限。当该变量为 `0` 时，表示对扫描范围没有内存限制。如果构造精确的扫描范围会超出内存用量限制，优化器会使用更宽松的扫描范围（例如 `[[NULL,+inf]]`）。如果执行计划中未使用精确的扫描范围，可以调大该变量的值让优化器构造精确的扫描范围。

该变量的使用示例如下：

<details>
<summary><code>tidb_opt_range_max_size</code> 使用示例</summary>

查看该变量的默认值，即优化器构造扫描范围最多使用 64 MiB 内存。

```sql
SELECT @@tidb_opt_range_max_size;
```

```sql
+----------------------------+
| @@tidb_opt_range_max_size |
+----------------------------+
| 67108864                   |
+----------------------------+
1 row in set (0.01 sec)
```

```sql
EXPLAIN SELECT * FROM t use index (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

在 64 MiB 的内存最大限制约束下，优化器构造出精确的扫描范围 `[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`，见如下执行计划返回结果。

```sql
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object            | operator info                                                                                                                                                               |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexLookUp_7                 | 0.90    | root      |                          |                                                                                                                                                                             |
| ├─IndexRangeScan_5(Build)     | 0.90    | cop[tikv] | table:t, index:idx(a, b) | range:[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 0.90    | cop[tikv] | table:t                  | keep order:false, stats:pseudo                                                                                                                                              |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

现将优化器构造扫描范围的内存用量上限设为 1500 字节。

```sql
SET @@tidb_opt_range_max_size = 1500;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

在 1500 字节内存的最大限制约束下，优化器构造出了更宽松的扫描范围 `[10,10], [20,20], [30,30]`，并用 warning 提示用户构造精确的扫描范围所需的内存用量超出了 `tidb_opt_range_max_size` 的限制。

```sql
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
| id                            | estRows | task      | access object            | operator info                                                   |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
| IndexLookUp_8                 | 0.09    | root      |                          |                                                                 |
| ├─Selection_7(Build)          | 0.09    | cop[tikv] |                          | in(test.t.b, 40, 50, 60)                                        |
| │ └─IndexRangeScan_5          | 30.00   | cop[tikv] | table:t, index:idx(a, b) | range:[10,10], [20,20], [30,30], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 0.09    | cop[tikv] | table:t                  | keep order:false, stats:pseudo                                  |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)
```

```sql
SHOW WARNINGS;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                     |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Memory capacity of 1500 bytes for 'tidb_opt_range_max_size' exceeded when building ranges. Less accurate ranges such as full range are chosen |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

再将优化器构造扫描范围的内存用量上限设为 100 字节。

```sql
set @@tidb_opt_range_max_size = 100;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

在 100 字节的内存最大限制约束下，优化器选择了 `IndexFullScan`，并用 warning 提示用户构造精确的扫描范围所需的内存超出了 `tidb_opt_range_max_size` 的限制。

```sql
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
| id                            | estRows  | task      | access object            | operator info                                      |
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
| IndexLookUp_8                 | 8000.00  | root      |                          |                                                    |
| ├─Selection_7(Build)          | 8000.00  | cop[tikv] |                          | in(test.t.a, 10, 20, 30), in(test.t.b, 40, 50, 60) |
| │ └─IndexFullScan_5           | 10000.00 | cop[tikv] | table:t, index:idx(a, b) | keep order:false, stats:pseudo                     |
| └─TableRowIDScan_6(Probe)     | 8000.00  | cop[tikv] | table:t                  | keep order:false, stats:pseudo                     |
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)
```

```sql
SHOW WARNINGS;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                     |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Memory capacity of 100 bytes for 'tidb_opt_range_max_size' exceeded when building ranges. Less accurate ranges such as full range are chosen |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

</details>

### tidb_opt_scan_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1.5`
- 表示升序扫描时，TiKV 在磁盘上扫描一行数据的开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### tidb_opt_seek_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`20`
- 表示 TiDB 从 TiKV 请求数据的初始开销。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

### tidb_opt_skew_distinct_agg <span class="version-mark">从 v6.2.0 版本开始引入</span>

> **注意：**
>
> 开启该变量带来的查询性能优化仅对 TiFlash 有效。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置优化器是否将带有 `DISTINCT` 的聚合函数（例如 `SELECT b, count(DISTINCT a) FROM t GROUP BY b`）改写为两层聚合函数（例如 `SELECT b, count(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`）。当聚合列有严重的数据倾斜，且 `DISTINCT` 列有很多不同的值时，这种改写能够避免查询执行过程中的数据倾斜，从而提升查询性能。

### tidb_opt_three_stage_distinct_agg <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制在 MPP 模式下是否将 `COUNT(DISTINCT)` 聚合改写为三阶段分布式执行的聚合。
- 该变量目前仅对只有一个 `COUNT(DISTINCT)` 的聚合生效。

### tidb_opt_tiflash_concurrency_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`24.0`
- 表示 TiFlash 计算的并发数。该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

## `tidb_opt_use_invisible_indexes` <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置是否允许优化器选择[不可见索引 (Invisible Index)](/sql-statements/sql-statement-create-index.md#不可见索引)。默认情况下，不可见索引由 DML 语句维护，不会被查询优化器使用。当修改变量为 `ON` 时，对该会话中的查询，优化器可以选择不可见索引进行查询优化。

### tidb_opt_use_invisible_indexes <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值： `OFF`
- 该变量用于控制当前会话中优化器是否可以选择[不可见索引](/sql-statements/sql-statement-create-index.md#不可见索引)进行查询优化。不可见索引由 DML 语句维护，但不会被查询优化器使用。在永久删除索引之前进行二次确认的场景中很有用。当变量设为 `ON` 时，优化器可在当前会话中选择不可见索引进行查询优化。

### tidb_opt_write_row_id

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值： `OFF`
- 该变量用于控制是否允许 `INSERT`、`REPLACE` 和 `UPDATE` 语句操作 `_tidb_rowid` 列。仅在使用 TiDB 工具导入数据时可使用该变量。

### tidb_opt_hash_agg_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_hash_join_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_index_join_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_index_lookup_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_index_merge_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_index_reader_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_index_scan_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_limit_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_merge_join_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_sort_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_stream_agg_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_table_full_scan_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_table_range_scan_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_table_reader_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_table_rowid_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_table_tiflash_scan_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_opt_topn_cost_factor <span class="version-mark">从 v8.5.3 和 v9.0.0 版本开始引入</span>

> **警告：**
>
> 该变量是[代价模型](/cost-model.md)内部使用的变量，**不建议**修改该变量的值。

- 作用域：SESSION | GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`1`

### tidb_optimizer_selectivity_level

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 控制优化器估算逻辑的更迭。更改该变量值后，优化器的估算逻辑会产生较大的改变。目前该变量的有效值只有 `0`，不建议设为其它值。

### tidb_partition_prune_mode <span class="version-mark">从 v5.1 版本开始引入</span>

> **警告：**
>
> 从 v8.5.0 开始，将该变量设置为 `static` 或 `static-only` 时会产生警告。该变量将在未来版本中废弃。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值：`dynamic`
- 可选值：`static`、`dynamic`、`static-only`、`dynamic-only`
- 这个变量用来设置是否开启分区表动态裁剪模式。默认值为 `dynamic`。但是注意，`dynamic` 动态裁剪模式仅在表级别汇总统计信息（即分区表的全局统计信息）收集完成的情况下生效。如果在全局统计信息未收集完成的情况下启用 `dynamic` 动态裁剪模式，TiDB 仍然会维持 `static` 静态裁剪的状态，直到全局统计信息收集完成。关于全局统计信息的更多信息，请参考[动态裁剪模式下的分区表统计信息](/statistics.md#收集动态裁剪模式下的分区表统计信息)。关于动态裁剪模式的更多信息，请参考[分区表动态裁剪模式](/partitioned-table.md#动态裁剪模式)。

### tidb_persist_analyze_options <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制是否开启 [ANALYZE 配置持久化](/statistics.md#持久化-analyze-配置)特性。

### tidb_pessimistic_txn_fair_locking <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 是否对悲观锁启用加强的悲观锁唤醒模型。该模型可严格控制悲观锁单点冲突场景下事务的唤醒顺序，避免无效唤醒，大大降低原有唤醒机制中的随机性对事务延迟带来的不确定性。如果业务场景中遇到了单点悲观锁冲突频繁的情况（如高频更新同一行数据等），并进而引起语句重试频繁、尾延迟高，甚至偶尔发生 `pessimistic lock retry limit reached` 错误，可以尝试开启该变量来解决问题。
- 对于从 v7.0.0 以前的版本升级到 v7.0.0 或更新版本的 TiDB 集群，该选项默认关闭。

> **注意：**
>
> - 视具体业务场景的不同，启用该选项可能对存在频繁锁冲突的事务造成一定程度的吞吐下降（平均延迟上升）。
> - 该选项目前仅对需要上锁单个 key 的语句有效。如果一个语句需要对多行同时上锁，则该选项不会对此类语句生效。
> - 该功能从 v6.6.0 版本引入。在 v6.6.0 版本中，该功能由变量 [`tidb_pessimistic_txn_aggressive_locking`](https://docs-archive.pingcap.com/zh/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-从-v660-版本开始引入) 控制，默认关闭。

### tidb_placement_mode <span class="version-mark">从 v6.0.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`STRICT`
- 可选值：`STRICT`、`IGNORE`
- 该变量用于控制 DDL 语句是否忽略 [SQL 中指定的放置规则](/placement-rules-in-sql.md)。当该变量值为 `IGNORE` 时，所有放置规则选项将被忽略。
- 该变量主要供逻辑备份/恢复工具使用，确保即使分配了无效的放置规则也能正常创建表。这类似于 mysqldump 在每个导出文件开头写入 `SET FOREIGN_KEY_CHECKS=0;` 的做法。

### tidb_plan_cache_invalidation_on_fresh_stats <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量用于控制当某张表上的统计信息更新后，与该表相关的 Plan Cache 是否自动失效。
- 开启此变量有助于 Plan Cache 更有效地利用可用的统计信息生成执行计划，例如：
    - 有时 Plan Cache 会在统计信息尚不可用时生成执行计划。开启此变量后，Plan Cache 会在统计信息可用时重新生成执行计划。
    - 当表上数据分布发生变化时，之前的最优执行计划可能对于现在不再是最优的。开启此变量后，Plan Cache 会在重新收集统计信息后重新生成执行计划。
- 对于从 v7.1.0 以前的版本升级到 v7.1.0 及以上版本的 TiDB 集群，该选项默认关闭 (`OFF`)。

### tidb_plan_cache_max_plan_size <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`2097152`（即 2 MiB）
- 取值范围：`[0, 9223372036854775807]`，单位为 Byte。支持带单位的内存格式 "KiB|MiB|GiB|TiB"。`0` 表示表示不设限制。
- 这个变量用来控制可以缓存的 Prepare 或非 Prepare 语句执行计划的最大大小。超过该值的执行计划将不会被缓存到 Plan Cache 中。详情请参考 [Prepare 语句执行计划缓存](/sql-prepared-plan-cache.md#prepared-plan-cache-的内存管理)和[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md#使用方法)。

### tidb_pprof_sql_cpu <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `0`
- 范围： `[0, 1]`
- 该变量用于控制是否在 profile 输出中标记对应的 SQL 语句，以便识别和排查性能问题。

### tidb_prefer_broadcast_join_by_exchange_data_size <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于设定 TiDB 选择 [MPP Hash Join 算法](/tiflash/use-tiflash-mpp-mode.md#mpp-模式的算法支持)时，是否使用最小网络交换的数据量策略。开启该变量后，TiDB 会估算 Broadcast Hash Join 和 Shuffled Hash Join 两种算法所需进行网络交换的数据量，并选择网络交换数据量较小的算法。
- 该功能开启后 [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-从-v50-版本开始引入) 和 [`tidb_broadcast_join_threshold_size`](#tidb_broadcast_join_threshold_size-从-v50-版本开始引入) 将不再生效。

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：浮点数
- 默认值：`0.1`
- 范围：`[0, 1]`
- 这个变量用来控制 Prepared Plan Cache 触发内存保护机制的阈值，具体可见 [Prepared Plan Cache 的内存管理](/sql-prepared-plan-cache.md#prepared-plan-cache-的内存管理)。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`prepared-plan-cache.memory-guard-ratio`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### tidb_prepared_plan_cache_size <span class="version-mark">从 v6.1.0 版本开始引入</span>

> **警告：**
>
> 从 v7.1.0 开始，该变量被废弃。请使用 [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-从-v710-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`100`
- 范围：`[1, 100000]`
- 这个变量用来控制单个 `SESSION` 的 Prepared Plan Cache 最多能够缓存的计划数量，具体可见 [Prepared Plan Cache 的内存管理](/sql-prepared-plan-cache.md#prepared-plan-cache-的内存管理)。
- 在 v6.1.0 之前这个开关通过 TiDB 配置文件 (`prepared-plan-cache.capacity`) 进行配置，升级到 v6.1.0 时会自动继承原有设置。

### tidb_projection_concurrency

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`[-1, 256]`
- 单位：线程
- 这个变量用来设置 `Projection` 算子的并发度。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### tidb_query_log_max_len

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`4096` (4 KiB)
- 范围：`[0, 1073741824]`
- 单位：字节
- 该变量控制 SQL 语句输出的最大长度。当一条 SQL 语句的输出长度大于 `tidb_query_log_max_len` 时，输出将会被截断。
- 在 v6.1.0 之前这个开关也可以通过 TiDB 配置文件 (`log.query-log-max-len`) 进行配置，升级到 v6.1.0 后仅可通过系统变量配置。

### tidb_rc_read_check_ts <span class="version-mark">从 v6.0.0 版本开始引入</span>

> **警告：**
>
> - 该特性与 [`replica-read`](#tidb_replica_read-从-v40-版本开始引入) 尚不兼容，开启 `tidb_rc_read_check_ts` 的读请求无法使用 [`replica-read`](#tidb_replica_read-从-v40-版本开始引入)，请勿同时开启两项特性。
> - 如果客户端使用游标操作，建议不开启 `tidb_rc_read_check_ts` 这一特性，避免前一批返回数据已经被客户端使用而语句最终会报错的情况。
> - 自 v7.0.0 版本开始，该变量对于使用 prepared statement 协议下 cursor fetch read 游标模式不再生效。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于优化时间戳的获取，适用于悲观事务 `READ-COMMITTED` 隔离级别下读写冲突较少的场景，开启此变量可以避免获取全局 timestamp 带来的延迟和开销，并优化事务内读语句延迟。
- 如果读写冲突较为严重，开启此功能会增加额外开销和延迟，造成性能回退。更详细的说明，请参考[读已提交隔离级别 (Read Committed) 文档](/transaction-isolation-levels.md#读已提交隔离级别-read-committed)。

### tidb_rc_write_check_ts <span class="version-mark">从 v6.3.0 版本开始引入</span>

> **警告：**
>
> 该特性与 [`replica-read`](#tidb_replica_read-从-v40-版本开始引入) 尚不兼容。开启本变量后，客户端发送的所有请求都将无法使用 `replica-read`，因此请勿同时开启 `tidb_rc_write_check_ts` 和 `replica-read`。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于优化时间戳的获取，适用于悲观事务 `READ-COMMITTED` 隔离级别下点写冲突较少的场景。开启此变量可以避免点写语句获取全局时间戳带来的延迟和开销。目前该变量适用的点写语句包括 `UPDATE`、`DELETE`、`SELECT ...... FOR UPDATE` 三种类型。点写语句是指将主键或者唯一键作为过滤条件且最终执行算子包含 `POINT-GET` 的写语句。
- 如果点写冲突较为严重，开启此变量会增加额外开销和延迟，造成性能回退。更详细的说明，请参考[读已提交隔离级别 (Read Committed) 文档](/transaction-isolation-levels.md#读已提交隔离级别-read-committed)。

### tidb_read_consistency <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是（注意当存在[非事务 DML 语句](/non-transactional-dml.md)时，使用 hint 修改该变量的值可能不生效）
- 类型：字符串
- 默认值：`strict`
- 此变量用于控制自动提交的读语句的读一致性。
- 如果将变量值设置为 `weak`，则直接跳过读语句遇到的锁，读的执行可能会更快，这就是弱一致性读模式。但在该模式下，事务语义（例如原子性）和分布式一致性（线性一致性）并不能得到保证。
- 如果用户场景中需要快速返回自动提交的读语句，并且可接受弱一致性的读取结果，则可以使用弱一致性读取模式。

### tidb_read_staleness <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围 `[-2147483648, 0]`
- 这个变量用于设置当前会话允许读取的历史数据范围。设置后，TiDB 会从参数允许的范围内选出一个尽可能新的时间戳，并影响后继的所有读操作。比如，如果该变量的值设置为 `-5`，TiDB 会在 5 秒时间范围内，保证 TiKV 拥有对应历史版本数据的情况下，选择尽可能新的一个时间戳。

### tidb_record_plan_in_slow_log

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值： `ON`
- 该变量用于控制是否将慢查询的执行计划记录在慢日志中。

### tidb_redact_log

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值： `OFF`
- 可选值：`OFF`、`ON`、`MARKER`
- 该变量用于控制是否在 TiDB 日志和慢日志中隐藏 SQL 语句中的用户信息。
- 默认值为 `OFF`，表示不对用户信息做任何处理。
- 当设为 `ON` 时，用户信息会被隐藏。例如，如果执行的 SQL 语句为 `INSERT INTO t VALUES (1,2)`，则在日志中记录为 `INSERT INTO t VALUES (?,?)`。
- 当设为 `MARKER` 时，用户信息会用 `‹ ›` 包裹。例如，如果执行的 SQL 语句为 `INSERT INTO t VALUES (1,2)`，则在日志中记录为 `INSERT INTO t VALUES (‹1›,‹2›)`。如果用户数据中包含 `‹` 或 `›`，`‹` 会被转义为 `‹‹`，`›` 会被转义为 `››`。基于标记后的日志，你可以决定在展示日志时是否对标记的信息进行脱敏。

### tidb_regard_null_as_point <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用来控制优化器是否可以将包含 null 的等值条件作为前缀条件来访问索引。
- 该变量默认开启。开启后，该变量可以使优化器减少需要访问的索引数据量，从而提高查询的执行速度。例如，在有多列索引 `index(a, b)` 且查询条件为 `a<=>null and b=1` 的情况下，优化器可以同时使用查询条件中的 `a<=>null` 和 `b=1` 进行索引访问。如果关闭该变量，因为 `a<=>null and b=1` 包含 null 的等值条件，优化器不会使用 `b=1` 进行索引访问。

### tidb_remove_orderby_in_subquery <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：在 v7.2.0 之前版本中为 `OFF`，在 v7.2.0 及之后版本中为 `ON`。
- 指定是否在子查询中移除 `ORDER BY` 子句。
- 在 ISO/IEC SQL 标准中，`ORDER BY` 主要用于对顶层查询结果进行排序。对于子查询中的 `ORDER BY`，SQL 标准并不要求子查询结果按 `ORDER BY` 排序。
- 如果需要对子查询结果排序，通常可以在外层查询中处理，例如使用窗口函数或在外层查询中再次使用 `ORDER BY`。这样做可以确保最终结果集的顺序。

### tidb_replica_read <span class="version-mark">从 v4.0 版本开始引入</span>

<CustomContent platform="tidb-cloud" plan="starter,essential">

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)，该变量为只读。

</CustomContent>

<CustomContent platform="tidb-cloud" plan="premium">

> **注意：**
>
> 对于 [{{{ .premium }}}](https://docs-preview.pingcap.com/tidbcloud/tidb-cloud-intro/#deployment-options)，该变量为只读。

</CustomContent>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值： `leader`
- 可选值：`leader`、`follower`、`leader-and-follower`、`prefer-leader`、`closest-replicas`、`closest-adaptive`、`learner`。`learner` 值从 v6.6.0 开始引入。
- 该变量用于控制 TiDB 的数据读取位置。从 v8.5.4 开始，该变量仅对只读 SQL 语句生效。
- 关于用法和实现的更多详情，参见 [Follower Read](/follower-read.md)。

### tidb_restricted_read_only <span class="version-mark">从 v5.2.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值： `OFF`
- `tidb_restricted_read_only` 和 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 行为类似。大多数情况下，你只需要使用 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 即可。
- 具有 `SUPER` 或 `SYSTEM_VARIABLES_ADMIN` 权限的用户可以修改该变量。但如果启用了[安全增强模式](#tidb_enable_enhanced_security)，还需要额外的 `RESTRICTED_VARIABLES_ADMIN` 权限才能读取或修改该变量。
- `tidb_restricted_read_only` 在以下情况下会影响 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)：
    - 将 `tidb_restricted_read_only` 设为 `ON` 会将 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 更新为 `ON`。
    - 将 `tidb_restricted_read_only` 设为 `OFF` 不会改变 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)。
    - 如果 `tidb_restricted_read_only` 为 `ON`，[`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 不能被设置为 `OFF`。
- 对于 TiDB 的 DBaaS 提供商，如果 TiDB 集群是另一个数据库的下游数据库，为了使 TiDB 集群变为只读，你可能需要在启用[安全增强模式](#tidb_enable_enhanced_security)的情况下使用 `tidb_restricted_read_only`，从而防止客户通过 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 将集群变为可写。为此，你需要启用[安全增强模式](#tidb_enable_enhanced_security)，使用具有 `SYSTEM_VARIABLES_ADMIN` 和 `RESTRICTED_VARIABLES_ADMIN` 权限的管理员用户来控制 `tidb_restricted_read_only`，并让你的数据库用户使用具有 `SUPER` 权限的 root 用户仅控制 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)。
- 该变量控制整个集群的只读状态。当变量为 `ON` 时，整个集群中所有 TiDB 服务器都处于只读模式。此时，TiDB 仅执行不修改数据的语句，如 `SELECT`、`USE` 和 `SHOW`。对于 `INSERT` 和 `UPDATE` 等其他语句，TiDB 在只读模式下将拒绝执行。
- 使用该变量开启只读模式仅保证整个集群最终进入只读状态。如果你在 TiDB 集群中修改了该变量的值但变更尚未传播到其他 TiDB 服务器，则未更新的 TiDB 服务器仍**未**处于只读模式。
- TiDB 在执行 SQL 语句之前会检查只读标志。从 v6.2.0 起，在 SQL 语句提交之前也会检查该标志。这有助于防止服务器已设为只读模式后，长时间运行的[自动提交](/transaction-overview.md#autocommit)语句仍修改数据的情况。
- 当该变量开启时，TiDB 对未提交的事务按如下方式处理：
    - 对于未提交的只读事务，可以正常提交。
    - 对于未提交的非只读事务，在这些事务中执行写操作的 SQL 语句将被拒绝。
    - 对于未提交的数据已修改的只读事务，这些事务的提交将被拒绝。
- 开启只读模式后，所有用户（包括具有 `SUPER` 权限的用户）都不能执行可能写入数据的 SQL 语句，除非该用户被显式授予 `RESTRICTED_REPLICA_WRITER_ADMIN` 权限。

### tidb_request_source_type <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值：`""`
- 可选值：`"ddl"`、`"stats"`、`"br"`、`"lightning"`、`"background"`
- 显式指定当前会话的任务类型，用于[资源管控](/tidb-resource-control-ru-groups.md)识别并控制。如 `SET @@tidb_request_source_type = "background"`。

### tidb_resource_control_strict_mode <span class="version-mark">从 v8.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 该变量是 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) 和优化器 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) Hint 权限控制的开关。当此变量设置为 `ON` 时，你需要有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 或者 `RESOURCE_GROUP_USER` 权限才能使用这两种方式修改当前会话或当前语句绑定的资源组；当此变量设置为 `OFF` 时，则无需上述权限，其行为与不支持此变量的 TiDB 之前版本相同。
- 从旧版本升级到 v8.2.0 及之后版本时，该功能默认关闭，此时该变量默认值为 `OFF`。

### tidb_retry_limit

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`10`
- 范围：`[-1, 9223372036854775807]`
- 这个变量用来设置乐观事务的最大重试次数。一个事务执行中遇到可重试的错误（例如事务冲突、事务提交过慢或表结构变更）时，会根据该变量的设置进行重试。注意当 `tidb_retry_limit = 0` 时，也会禁用自动重试。该变量仅适用于乐观事务，不适用于悲观事务。

### tidb_row_format_version

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `2`
- 范围： `[1, 2]`
- 该变量控制表中新保存数据的格式版本。在 TiDB v4.0 中，默认使用[新存储行格式](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2018-07-19-row-format.md)版本 `2` 保存新数据。
- 如果从 v4.0.0 之前的 TiDB 版本升级到 v4.0.0 或更高版本，格式版本不会改变，TiDB 将继续使用旧版本 `1` 的格式向表中写入数据，即**只有新创建的集群才默认使用新的数据格式**。
- 注意，修改该变量不会影响已保存的旧数据，仅对修改后新写入的数据应用对应的版本格式。

### tidb_runtime_filter_mode <span class="version-mark">从 v7.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值：`OFF`
- 可选值：`OFF`，`LOCAL`
- 控制 Runtime Filter 的模式，即**生成 Filter 算子**和**接收 Filter 算子**之间的关系。当前可设置为两种模式：`OFF`、`LOCAL`。`OFF` 代表关闭 Runtime Filter，`LOCAL` 代表开启 `LOCAL` 模式的 Runtime Filter。详细说明见 [Runtime Filter Mode](/runtime-filter.md#runtime-filter-mode)。

### tidb_runtime_filter_type <span class="version-mark">从 v7.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值：`IN`
- 可选值：`IN`
- 控制 Runtime Filter 的类型，即生成的 Filter 算子使用的谓词类型。当前仅支持 `IN`，所以无需更改此设置。详细说明见 [Runtime Filter Type](/runtime-filter.md#runtime-filter-type)。

### tidb_scatter_region

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`""`
- 可选值：`""`、`table`、`global`
- 如果在建表时设置了 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS` 参数，系统会在表创建成功后自动将其拆分为指定数量的 Region。该变量用于控制这些拆分 Region 的打散策略。TiDB 会根据所选的打散策略处理 Region。需要注意的是，由于建表操作需要等待打散过程完成后才返回成功状态，开启该变量可能会显著增加 `CREATE TABLE` 语句的执行时间，与未开启时相比可能慢数倍。各可选值的说明如下：
    - `""`：默认值，表示建表后不打散表的 Region。
    - `table`：表示如果建表时设置了 `PRE_SPLIT_REGIONS` 或 `SHARD_ROW_ID_BITS` 属性，在预拆分多个 Region 的场景下，这些表的 Region 将按表的粒度进行打散。但如果建表时未设置上述属性，在快速创建大量表的场景下，这些表的 Region 会集中在少数 TiKV 节点上，导致 Region 分布不均。
    - `global`：表示 TiDB 根据整个集群的数据分布来打散新创建表的 Region。特别是在快速创建大量表的场景下，使用 `global` 选项有助于防止 Region 过度集中在少数 TiKV 节点上，确保 Region 在集群中更均衡地分布。

### tidb_schema_cache_size <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`536870912` (512 MiB)
- 取值范围：`0` 或 `[67108864, 9223372036854775807]`
- 对 TiDB v8.4.0 以前的版本，该变量默认值为 `0`。
- 从 TiDB v8.4.0 开始，默认值为 `536870912`（即 512 MiB）。从低版本升级到 v8.4.0 及更高版本后仍然会使用旧值。
- 这个变量用来控制 TiDB schema 信息缓存的大小。单位为 byte。设置为 `0` 表示不打开缓存限制功能。如需开启，则需要将该变量的值设置在 `[67108864, 9223372036854775807]` 范围内，TiDB 将使用该变量的值做为可用的内存上限，并使用 Least Recently Used (LRU) 算法缓存所需的表，有效降低 schema 信息占用的内存。
- 当集群中存在较多分区表，或需要频繁对分区表执行 DDL 操作（如 `TRUNCATE`、`DROP` 分区等）时，建议将该参数取值设置为 `0`。

### tidb_schema_version_cache_limit <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`16`
- 取值范围：`[2, 255]`
- 该变量用于限制 TiDB 实例可以缓存多少个历史版本的表结构信息。默认值为 `16`，即默认缓存 16 个历史版本的表结构信息。
- 一般不需要修改该变量。当使用 [Stale Read](/stale-read.md) 功能且 DDL 执行非常频繁时，会导致表结构信息的版本号变更非常频繁，进而导致 Stale Read 在获取 Snapshot 的表结构信息时，可能会因为未命中表结构信息的缓存而需要消耗大量时间重新构建该信息。此时可以适当调大 `tidb_schema_version_cache_limit` 的值（例如 `32` ）来避免表结构信息的缓存不命中的问题。
- 修改该变量会使 TiDB 的内存占用轻微上升。使用时请注意 TiDB 的内存占用，避免出现 OOM 问题。

### tidb_server_memory_limit <span class="version-mark">从 v6.4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`80%`
- 范围：
    - 可以设置为百分比格式，表示内存使用占总内存的百分比，取值范围为 `[1%, 99%]`。
    - 也可以设置为内存大小，取值范围为 `0` 和 `[536870912, 9223372036854775807]`（单位为字节），支持 "KiB|MiB|GiB|TiB" 单位格式。`0` 表示不限制内存。
    - 如果该变量设为小于 512 MiB 但不为 `0` 的内存大小，TiDB 将使用 512 MiB 作为实际大小。
- 该变量用于指定 TiDB 实例的内存限制。当 TiDB 的内存使用达到该限制时，TiDB 会取消当前正在运行的内存使用最高的 SQL 语句。SQL 语句被成功取消后，TiDB 会尝试调用 Golang GC 立即回收内存，以尽快缓解内存压力。
- 只有内存使用超过 [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-从-v640-版本开始引入) 限制的 SQL 语句才会被优先选为待取消的 SQL 语句。
- 目前，TiDB 每次只取消一条 SQL 语句。当 TiDB 完全取消一条 SQL 语句并回收资源后，如果内存使用仍大于该变量设置的限制，TiDB 将开始下一次取消操作。

### tidb_server_memory_limit_gc_trigger <span class="version-mark">从 v6.4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`70%`
- 范围：`[50%, 99%]`
- TiDB 尝试触发 GC 的阈值。当 TiDB 的内存使用达到 `tidb_server_memory_limit` \* `tidb_server_memory_limit_gc_trigger` 的值时，TiDB 会主动触发一次 Golang GC 操作。一分钟内最多只会触发一次 GC 操作。

### tidb_server_memory_limit_sess_min_size <span class="version-mark">从 v6.4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`134217728`（即 128 MiB）
- 范围：`[128, 9223372036854775807]`，单位为字节，也支持 "KiB|MiB|GiB|TiB" 单位格式。
- 开启内存限制后，TiDB 会终止当前实例上内存使用最高的 SQL 语句。该变量用于指定待终止 SQL 语句的最小内存使用量。如果 TiDB 实例超出内存限制是由于大量低内存使用的会话导致的，可以适当调小该变量的值以允许更多会话被取消。

### tidb_service_scope <span class="version-mark">从 v7.4.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值： ""
- 可选值：长度不超过 64 个字符的字符串。有效字符包括数字 `0-9`、字母 `a-zA-Z`、下划线 `_` 和连字符 `-`。从 v8.5.6 开始，该变量值不区分大小写。TiDB 会将输入值转换为小写进行存储和比较。
- 该变量为实例级别的系统变量。你可以使用它来控制 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md) 下各 TiDB 节点的服务范围。DXF 根据该变量的值来决定哪些 TiDB 节点可被调度执行分布式任务。具体规则参见[任务调度](/tidb-distributed-execution-framework.md#任务调度)。

### tidb_session_alias <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：SESSION
- 是否持久化到集群：否
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：字符串
- 默认值：""
- 用来自定义当前会话相关日志中 `session_alias` 列的值，方便故障定位时识别该会话。此设置会对语句执行过程中涉及的多个节点的日志生效（包括 TiKV）。此变量限制长度最大为 64 个字符，超出的部分将会被自动截断。如果变量值的末尾存在空格，也会被自动去除。

### tidb_session_plan_cache_size <span class="version-mark">从 v7.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`100`
- 范围：`[1, 100000]`
- 这个变量用来控制 Plan Cache 最多能够缓存的计划数量。其中，[Prepare 语句执行计划缓存](/sql-prepared-plan-cache.md)和[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)共用一个缓存。
- 从旧版本升级到 v7.1.0 及之后的版本，`tidb_session_plan_cache_size` 的值与 [`tidb_prepared_plan_cache_size`](#tidb_prepared_plan_cache_size-从-v610-版本开始引入) 保持一致。

### tidb_shard_allocate_step <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`9223372036854775807`
- 范围：`[1, 9223372036854775807]`
- 该变量设置为 [`AUTO_RANDOM`](/auto-random.md) 或 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 属性列分配的最大连续 ID 数。通常，`AUTO_RANDOM` ID 或带有 `SHARD_ROW_ID_BITS` 属性的行 ID 在一个事务中是增量和连续的。你可以使用该变量来解决大事务场景下的热点问题。

### tidb_shard_row_id_bits <span class="version-mark">从 v8.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 15]`
- 该变量用于设置新建表默认的行 ID 的分片数。当设置了该变量为非 0 值后，执行 `CREATE TABLE` 语句时，TiDB 会为允许使用 `SHARD_ROW_ID_BITS` 的表（例如 `NONCLUSTERED` 表）自动设定该属性。详见 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)。

### tidb_simplified_metrics

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 开启该变量后，TiDB 将不再收集或记录 Grafana 面板中未使用的监控指标。

### tidb_skip_ascii_check <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置是否校验 ASCII 字符的合法性。
- 校验 ASCII 字符会损耗些许性能。当你确认输入的字符串为有效的 ASCII 字符时，可以将其设置为 `ON`。

### tidb_skip_isolation_level_check

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 开启这个开关之后，如果对 `tx_isolation` 赋值一个 TiDB 不支持的隔离级别，不会报错，有助于兼容其他设置了（但不依赖于）不同隔离级别的应用。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_missing_partition_stats <span class="version-mark">从 v7.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 分区表在开启[动态裁剪模式](/partitioned-table.md#动态裁剪模式)时，TiDB 会汇总各个分区的统计信息生成全局统计信息。这个变量用于控制当分区统计信息缺失时生成全局统计信息的行为。

    - 当开启该变量时，TiDB 生成全局统计信息时会跳过缺失的分区统计信息，不影响全局统计信息的生成。
    - 当关闭该变量时，遇到缺失的分区统计信息，TiDB 会停止生成全局统计信息。

### tidb_skip_utf8_check

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用来设置是否校验 UTF-8 字符的合法性。
- 校验 UTF-8 字符会损耗些许性能。当你确认输入的字符串为有效的 UTF-8 字符时，可以将其设置为 `ON`。

> **注意：**
>
> 跳过字符检查可能会使 TiDB 检测不到应用写入的非法 UTF-8 字符，进一步导致执行 `ANALYZE` 时解码错误，以及引入其他未知的编码问题。如果应用不能保证写入字符串的合法性，不建议跳过该检查。

### tidb_slow_log_max_per_sec <span class="version-mark">从 v8.5.6 和 v9.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`0`
- 类型：整数型
- 范围：`[0, 1000000]`
- 控制每个 TiDB 节点每秒打印的慢查询日志的数量上限。
    - 当值为 `0` （默认值）时，表示不限制每秒打印的慢查询日志数量。
    - 当值大于 `0` 时，TiDB 每秒最多打印指定数量的慢查询日志，超过部分将被丢弃，不会写入慢查询日志文件。
- 该变量常与 [`tidb_slow_log_rules`](#tidb_slow_log_rules-从-v856-和-v900-版本开始引入) 结合使用，以防止在高负载情况下产生过多的慢查询日志。

### tidb_slow_log_rules <span class="version-mark">从 v8.5.6 和 v9.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 类型：字符串
- 用于定义慢查询日志的触发规则，支持基于多维度指标的组合条件，实现更加灵活和精细化的日志记录控制。
- 关于该系统变量的详细使用方法，请参考 [`tidb_slow_log_rules` 使用方法](/identify-slow-queries.md#tidb_slow_log_rules-使用方法)。

> **Tip:**
>
> 建议在启用 `tidb_slow_log_rules` 后，同时配置 [`tidb_slow_log_max_per_sec`](#tidb_slow_log_max_per_sec-从-v856-和-v900-版本开始引入)，以限制慢查询日志打印频率，防止基于规则的慢查询日志触发过于频繁。

### tidb_slow_log_threshold

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅作用于当前连接的 TiDB 实例。
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `300`
- 范围： `[-1, 9223372036854775807]`
- 单位：毫秒
- 该变量用于输出慢日志的耗时阈值，默认值为 300 毫秒。当查询耗时大于该值时，该查询被视为慢查询，其日志将输出到慢查询日志。注意，当 [`log.level`](https://docs.pingcap.com/tidb/dev/tidb-configuration-file#level) 的输出级别为 `"debug"` 时，无论该变量如何设置，所有查询都将记录到慢查询日志。

### tidb_slow_query_file

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值： ""
- 查询 `INFORMATION_SCHEMA.SLOW_QUERY` 时，仅解析配置文件中 `slow-query-file` 设置的慢查询日志文件名，默认的慢查询日志名为 "tidb-slow.log"。如需解析其他日志，可以将 `tidb_slow_query_file` 会话变量设置为指定的文件路径，然后查询 `INFORMATION_SCHEMA.SLOW_QUERY` 即可按设置的文件路径解析慢查询日志。

<CustomContent platform="tidb">

详情参见[慢查询日志](/identify-slow-queries.md)。

</CustomContent>

### tidb_slow_txn_log_threshold <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：无符号整数型
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 单位：毫秒
- 用于设置慢事务日志阈值。当事务执行时间超过该阈值时，TiDB 会在日志中记录该事务的详细信息。设置为 `0` 时，表示关闭该功能。

### tidb_snapshot

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 这个变量用来设置当前会话期待读取的历史数据所处时刻。比如当设置为 `"2017-11-11 20:20:20"` 时或者一个 TSO 数字 "400036290571534337"，当前会话将能读取到该时刻的数据。

### tidb_source_id <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `1`
- 范围： `[1, 15]`

<CustomContent platform="tidb">

- 该变量用于在[双向复制](/ticdc/ticdc-bidirectional-replication.md)集群中配置不同的集群 ID。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于在[双向复制](https://docs.pingcap.com/tidb/stable/ticdc-bidirectional-replication)集群中配置不同的集群 ID。

</CustomContent>

### tidb_stats_cache_mem_quota <span class="version-mark">从 v6.1.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 单位：字节
- 默认值：`0`，表示统计信息缓存的内存使用上限为 TiDB 实例总内存的 20%。在 v8.5.1 之前，`0` 表示该上限为 TiDB 实例总内存的 50%。
- 范围：`[0, 1099511627776]`
- 这个变量用于控制 TiDB 统计信息缓存的内存使用上限。

### tidb_stats_load_pseudo_timeout <span class="version-mark">从 v5.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制统计信息同步加载超时后，SQL 是执行失败（`OFF`），还是退回使用 pseudo 的统计信息（`ON`）。

### tidb_stats_load_sync_wait <span class="version-mark">从 v5.4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`100`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 该变量用于控制是否开启统计信息的同步加载功能。值为 `0` 表示关闭该功能。如需开启，可以将该变量设置为 SQL 优化等待同步加载完整列统计信息的最大超时时间（单位为毫秒）。详情参见[统计信息的加载](/statistics.md#统计信息的加载)。

### tidb_stmt_summary_enable_persistent <span class="version-mark">从 v6.6.0 版本开始引入</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> Statements summary 持久化为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值： `OFF`
- 该变量为只读变量，用于控制是否开启 [statements summary 持久化](/statement-summary-tables.md#持久化-statements-summary)。

<CustomContent platform="tidb">

- 该变量的值与配置项 [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_filename <span class="version-mark">从 v6.6.0 版本开始引入</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> Statements summary 持久化为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：字符串
- 默认值： `"tidb-statements.log"`
- 该变量为只读变量，用于指定开启 [statements summary 持久化](/statement-summary-tables.md#持久化-statements-summary)时持久化数据写入的文件。

<CustomContent platform="tidb">

- 该变量的值与配置项 [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_file_max_backups <span class="version-mark">从 v6.6.0 版本开始引入</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> Statements summary 持久化为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `0`
- 该变量为只读变量，用于指定开启 [statements summary 持久化](/statement-summary-tables.md#持久化-statements-summary)时可持久化的数据文件的最大数量。

<CustomContent platform="tidb">

- 该变量的值与配置项 [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_file_max_days <span class="version-mark">从 v6.6.0 版本开始引入</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> Statements summary 持久化为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `3`
- 单位：天
- 该变量为只读变量，用于指定开启 [statements summary 持久化](/statement-summary-tables.md#持久化-statements-summary)时持久化数据文件的最大保留天数。

<CustomContent platform="tidb">

- 该变量的值与配置项 [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_file_max_size <span class="version-mark">从 v6.6.0 版本开始引入</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> Statements summary 持久化为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

- 作用域：GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `64`
- 单位：MiB
- 该变量为只读变量，用于指定开启 [statements summary 持久化](/statement-summary-tables.md#持久化-statements-summary)时单个持久化数据文件的最大大小。

<CustomContent platform="tidb">

- 该变量的值与配置项 [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_history_size <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`24`
- 范围：`[0, 255]`
- 该变量用于设置 [Statement Summary 表](/statement-summary-tables.md)的历史容量。

### tidb_stmt_summary_internal_query <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 该变量用于控制是否在 [Statement Summary 表](/statement-summary-tables.md)中包含 TiDB 内部 SQL 的信息。

### tidb_stmt_summary_max_sql_length <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `4096`
- 范围： `[0, 2147483647]`
- 单位：字节

<CustomContent platform="tidb">

- 该变量用于控制 [statement summary 表](/statement-summary-tables.md)和 [TiDB Dashboard](/dashboard/dashboard-intro.md) 中 SQL 字符串的长度。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于控制 [statement summary 表](/statement-summary-tables.md)中 SQL 字符串的长度。

</CustomContent>

### tidb_stmt_summary_max_stmt_count <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `3000`
- 范围： `[1, 32767]`
- 该变量用于限制 [`statements_summary`](/statement-summary-tables.md#statements_summary) 和 [`statements_summary_history`](/statement-summary-tables.md#statements_summary_history) 表在内存中可存储的 SQL digest 的总数。

<CustomContent platform="tidb">

> **注意：**
>
> 当 [`tidb_stmt_summary_enable_persistent`](/statement-summary-tables.md#持久化-statements-summary) 开启时，`tidb_stmt_summary_max_stmt_count` 仅限制 [`statements_summary`](/statement-summary-tables.md#statements_summary) 表在内存中可存储的 SQL digest 数量。

</CustomContent>

### tidb_stmt_summary_refresh_interval <span class="version-mark">从 v4.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1800`
- 范围：`[1, 2147483647]`
- 单位：秒
- 该变量用于设置 [Statement Summary 表](/statement-summary-tables.md)的刷新时间。

### tidb_store_batch_size

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`4`
- 范围：`[0, 25000]`
- 设置 `IndexLookUp` 算子回表时多个 Coprocessor Task 的 batch 大小。`0` 代表不使用 batch。当 `IndexLookUp` 算子的回表 Task 数量特别多，出现极长的慢查询时，可以适当调大该参数以加速查询。

### tidb_store_limit <span class="version-mark">从 v3.0.4 和 v4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 这个变量用于限制 TiDB 同时向 TiKV 发送的请求的最大数量，0 表示没有限制。

### tidb_streamagg_concurrency

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1`
- 设置 `StreamAgg` 算子执行查询时的并发度。
- **不推荐设置该变量**，修改该变量值可能会造成数据正确性问题。

### tidb_super_read_only <span class="version-mark">从 v5.3.1 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值: `OFF`。
- `tidb_super_read_only` 用于实现对 MySQL 变量 `super_read_only` 的替代。然而，由于 TiDB 是一个分布式数据库，开启 `tidb_super_read_only` 后数据库各个 TiDB 服务器进入只读模式的时刻不是强一致的，而是最终一致的。
- 拥有 `SUPER` 或 `SYSTEM_VARIABLES_ADMIN` 权限的用户可以修改该变量。
- 该变量可以控制整个集群的只读状态。开启后（即该值为 `ON`），整个集群中的 TiDB 服务器都将进入只读状态，只有 `SELECT`、`USE`、`SHOW` 等不会修改数据的语句才能被执行，其他如 `INSERT`、`UPDATE` 等语句会被拒绝执行。
- 该变量开启只读模式只保证整个集群最终进入只读模式，当变量修改状态还没被同步到其他 TiDB 服务器时，尚未同步的 TiDB 仍然停留在非只读模式。
- 在执行 SQL 语句之前，TiDB 会检查集群的只读标志。从 v6.2.0 起，在提交 SQL 语句之前，TiDB 也会检查该标志，从而防止在服务器被置于只读模式后某些长期运行的 [auto commit](/transaction-overview.md#自动提交) 语句可能修改数据的情况。
- 在变量开启时，对于尚未提交的事务：
    - 如果有尚未提交的只读事务，可正常提交该事务。
    - 如果尚未提交的事务为非只读事务，在事务内执行写入的 SQL 语句会被拒绝。
    - 如果尚未提交的事务已经有数据改动，其提交也会被拒绝。
- 当集群开启只读模式后，所有用户（包括 `SUPER` 用户）都无法执行可能写入数据的 SQL 语句，除非该用户被显式地授予了 `RESTRICTED_REPLICA_WRITER_ADMIN` 权限。
- 当系统变量 [`tidb_restricted_read_only`](#tidb_restricted_read_only-从-v520-版本开始引入) 为 `ON` 时，`tidb_super_read_only` 的值会受到 [`tidb_restricted_read_only`](#tidb_restricted_read_only-从-v520-版本开始引入) 的影响。详情请参见[`tidb_restricted_read_only`](#tidb_restricted_read_only-从-v520-版本开始引入) 中的描述。

### tidb_sysdate_is_now <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`OFF`
- 这个变量用于控制 `SYSDATE` 函数能否替换为 `NOW` 函数，其效果与 MYSQL 中的 [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now) 一致。

### tidb_sysproc_scan_concurrency <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`1`
- 范围：`[0, 4294967295]`。v7.5.0 及更早版本的最大值为 `256`。v8.2.0 之前最小值为 `1`。设为 `0` 时，系统会根据集群规模自适应调整并发度。
- 该变量用于设置 TiDB 执行内部 SQL 语句（例如统计信息的自动更新）时扫描操作的并发度。

### tidb_table_cache_lease <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`3`
- 范围：`[1, 10]`
- 单位：秒
- 这个变量用来控制[缓存表](/cached-tables.md)的 lease 时间，默认值是 3 秒。该变量值的大小会影响缓存表的修改。在缓存表上执行修改操作后，最长可能出现 `tidb_table_cache_lease` 变量值时长的等待。如果业务表为只读表，或者能接受很高的写入延迟，则可以将该变量值调大，从而增加缓存的有效时间，减少 lease 续租的频率。

### tidb_tmp_table_max_size <span class="version-mark">从 v5.3 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`67108864`
- 范围：`[1048576, 137438953472]`
- 单位：字节
- 这个变量用于限制单个[临时表](/temporary-tables.md)的最大大小，临时表超出该大小后报错。

### tidb_top_sql_max_meta_count <span class="version-mark">从 v6.0.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `5000`
- 范围： `[1, 10000]`

<CustomContent platform="tidb">

- 该变量用于控制 [Top SQL](/dashboard/top-sql.md) 每分钟收集的 SQL 语句类型的最大数量。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于控制 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) 每分钟收集的 SQL 语句类型的最大数量。

</CustomContent>

### tidb_top_sql_max_time_series_count <span class="version-mark">从 v6.0.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

> **注意：**
>
> 目前，TiDB Dashboard 的 Top SQL 页面仅显示负载贡献最大的前 5 种 SQL 查询类型，与 `tidb_top_sql_max_time_series_count` 的配置无关。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `100`
- 范围： `[1, 5000]`

<CustomContent platform="tidb">

- 该变量用于控制 [Top SQL](/dashboard/top-sql.md) 每分钟可记录的负载贡献最大（即 top N）的 SQL 语句数量。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于控制 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) 每分钟可记录的负载贡献最大（即 top N）的 SQL 语句数量。

</CustomContent>

### tidb_track_aggregate_memory_usage

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 本变量控制 TiDB 是否跟踪聚合函数的内存使用情况。

> **警告：**
>
> 如果禁用该变量，TiDB 可能无法准确跟踪内存使用情况，并且无法控制对应 SQL 语句的内存使用。

### tidb_tso_client_batch_max_wait_time <span class="version-mark">从 v5.3.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：浮点型
- 默认值：`0`
- 范围：`[0, 10]`
- 单位：毫秒
- 该变量用于设置 TiDB 从 PD 请求 TSO 时批量操作的最大等待时间。默认值为 `0`，表示不额外等待。
- 每次从 PD 获取 TSO 请求时，TiDB 使用的 PD Client 会尽可能多地收集同一时间收到的 TSO 请求，然后将收集到的请求批量合并为一个 RPC 请求发送给 PD，以减轻 PD 的压力。
- 将该变量设为大于 `0` 的值后，TiDB 会在每次批量合并结束前等待该值对应的最大时长，以收集更多的 TSO 请求并提高批量操作的效果。
- 适合增大该变量值的场景：
    * 由于 TSO 请求压力大，PD leader 的 CPU 达到瓶颈，导致 TSO RPC 请求延迟高。
    * 集群中 TiDB 实例数量不多，但每个 TiDB 实例的并发度较高。
- 建议将该变量设置为尽可能小的值。

> **注意：**
>
> - 如果 TSO RPC 延迟升高的原因不是 PD leader 的 CPU 使用率瓶颈（如网络问题），增大 `tidb_tso_client_batch_max_wait_time` 的值可能会增加 TiDB 的执行延迟，并影响集群的 QPS 性能。
> - 该功能与 [`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-从-v840-版本开始引入) 不兼容。如果该变量设为非零值，[`tidb_tso_client_rpc_mode`](#tidb_tso_client_rpc_mode-从-v840-版本开始引入) 将不生效。

### tidb_tso_client_rpc_mode <span class="version-mark">从 v8.4.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`DEFAULT`
- 可选值：`DEFAULT`、`PARALLEL`、`PARALLEL-FAST`
- 这个变量用来设置 TiDB 向 PD 发送 TSO RPC 请求时使用的模式。这里的模式将用于控制 TSO RPC 请求是否并行，调节获取 TS 时消耗在请求攒批阶段的时间，从而在某些场景中减少执行查询时等待 TS 阶段的时间。

    - `DEFAULT`：默认模式。TiDB 会将一段时间内当前节点的所有取 TS 操作攒批到一个 TSO RPC 请求中发送给 PD 批量获取 TS，因而每次取 TS 操作的耗时由等待攒批的时间和进行 RPC 请求的时间组成。在默认模式下，不同的 TSO RPC 请求之间是串行进行的，每个取 TS 操作的平均耗时是实际 TSO RPC 耗时的 1.5 倍左右。
    - `PARALLEL`：并行模式。在该模式下，TiDB 会尝试将每次攒批的时间缩短到默认模式的 1/2 左右，并尽可能保持两个 TSO RPC 请求同时进行。这样，每个取 TS 的操作的平均耗时理论上最多能缩短到实际 TSO RPC 耗时的 1.25 倍左右，即默认模式的 83% 左右。但是，攒批的效果会降低，TSO RPC 请求的数量会上升到默认模式的两倍左右。
    - `PARALLEL-FAST`：快速并行模式。与 `PARALLEL` 模式类似，在该模式下，TiDB 会尝试将每次攒批的时间缩短到默认模式 1/4 左右，并尽可能保持 4 个 TSO RPC 请求同时进行。这样，每个取 TS 操作的平均耗时理论上最多能缩短到实际 TSO RPC 耗时的 1.125 倍左右，即默认模式的 75% 左右。但是，攒批的效果会进一步降低，TSO RPC 请求的数量会上升到默认模式的 4 倍左右。

- 当满足以下条件时，可以考虑将该变量设置为 `PARALLEL` 或 `PARALLEL-FAST` 来获得一定的性能提升：

    - TSO 等待时间在 SQL 查询的整体耗时中占比显著。
    - PD 的 TSO 分配未达到瓶颈。
    - PD 和 TiDB 节点的 CPU 资源比较充足。
    - TiDB 到 PD 的网络延迟显著高于 PD 进行 TSO 分配的耗时，即 TSO RPC 请求的耗时主要由网络延迟构成。
        - TSO RPC 请求的耗时可以通过 Grafana 的 TiDB 面板中 PD Client 分类下的 **PD TSO RPC Duration** 查看。
        - PD 进行 TSO 分配的耗时可以通过 Grafana 的 PD 面板中 TiDB 分类下的 **PD server TSO handle duration** 查看。
    - 可以接受 TiDB 到 PD 的 TSO RPC 请求的数量增加 2 倍（对于 `PARALLEL` 模式）或 4 倍（对于 `PARALLEL-FAST`）所带来的额外网络流量。

> **注意：**
>
> - `PARALLEL` 和 `PARALLEL-FAST` 这两种模式与 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-从-v530-版本开始引入) 和 [`tidb_enable_tso_follower_proxy`](#tidb_enable_tso_follower_proxy-从-v530-版本开始引入) 不兼容。如果 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-从-v530-版本开始引入) 被设为非零值或者 [`tidb_enable_tso_follower_proxy`](#tidb_enable_tso_follower_proxy-从-v530-版本开始引入) 被启用，则 `tidb_tso_client_rpc_mode` 的设置不会生效，并按照 `DEFAULT` 模式执行。
> - `PARALLEL` 和 `PARALLEL-FAST` 主要用于降低 TiDB 取 TS 操作的平均耗时。对于某些延迟波动较大的情况，如长尾、尖刺问题，这两种模式可能无法带来显著性能改善。

### tidb_cb_pd_metadata_error_rate_threshold_ratio <span class="version-mark">从 v8.5.5 和 v9.0.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`0`
- 取值范围：`[0, 1]`
- 该变量用于控制 TiDB 何时触发熔断器。设置为 `0`（默认值）表示禁用熔断器。设置为 `0.01` 到 `1` 之间的值时，表示启用熔断器，当发送到 PD 的特定请求的错误率达到或超过该阈值时，熔断器会被触发。

### tidb_ttl_delete_rate_limit <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 该变量用于限制每个 TiDB 节点上 TTL 任务中 `DELETE` 语句的速率。该值表示单个节点在 TTL 任务中每秒允许执行的 `DELETE` 语句的最大数量。当该变量设为 `0` 时，不做任何限制。详情参见 [Time to Live](/time-to-live.md)。

### tidb_ttl_delete_batch_size <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`100`
- 范围：`[1, 10240]`
- 该变量用于设置 TTL 任务中单个 `DELETE` 事务中可删除的最大行数。详情参见 [Time to Live](/time-to-live.md)。

### tidb_ttl_delete_worker_count <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`4`
- 范围：`[1, 256]`
- 该变量用于设置每个 TiDB 节点上 TTL 任务的最大并发度。详情参见 [Time to Live](/time-to-live.md)。

### tidb_ttl_job_enable <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`ON`
- 类型：布尔型
- 该变量用于控制是否启用 TTL 任务。如果设为 `OFF`，所有设置了 TTL 属性的表将自动停止清理过期数据。详情参见 [Time to Live](/time-to-live.md)。

### tidb_ttl_scan_batch_size <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`500`
- 范围：`[1, 10240]`
- 该变量用于设置 TTL 任务中用于扫描过期数据的每条 `SELECT` 语句的 `LIMIT` 值。详情参见 [Time to Live](/time-to-live.md)。

### tidb_ttl_scan_worker_count <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`4`
- 范围：`[1, 256]`
- 该变量用于设置每个 TiDB 节点上 TTL 扫描任务的最大并发度。详情参见 [Time to Live](/time-to-live.md)。

### tidb_ttl_job_schedule_window_start_time <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：Time
- 是否持久化到集群：是
- 默认值：`00:00 +0000`
- 该变量用于控制后台 TTL 任务调度窗口的开始时间。修改该变量值时请注意，过小的窗口可能导致过期数据清理失败。详情参见 [Time to Live](/time-to-live.md)。

### tidb_ttl_job_schedule_window_end_time <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：Time
- 是否持久化到集群：是
- 默认值：`23:59 +0000`
- 该变量用于控制后台 TTL 任务调度窗口的结束时间。修改该变量值时请注意，过小的窗口可能导致过期数据清理失败。详情参见 [Time to Live](/time-to-live.md)。

### tidb_ttl_running_tasks <span class="version-mark">从 v7.0.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`-1` 和 `[1, 256]`
- 该变量用于指定整个集群中正在运行的 TTL 任务的最大数量。`-1` 表示 TTL 任务数量等于 TiKV 节点数。详情参见 [Time to Live](/time-to-live.md)。

### tidb_txn_assertion_level <span class="version-mark">从 v6.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`FAST`
- 可选值：`OFF`，`FAST`，`STRICT`
- 这个变量用于设置 assertion 级别。assertion 是一项在事务提交过程中进行的数据索引一致性校验，它对正在写入的 key 是否存在进行检查。如果不符则说明数据索引不一致，会导致事务 abort。详见[数据索引一致性报错](/troubleshoot-data-inconsistency-errors.md)。
- 对于新创建的 v6.0.0 及以上的集群，默认值为 `FAST`。对于升级版本的集群，如果升级前是低于 v6.0.0 的版本，升级后默认值为 `OFF`。

    - `OFF`: 关闭该检查。
    - `FAST`: 开启大多数检查项，对性能几乎无影响。
    - `STRICT`: 开启全部检查项，当系统负载较高时，对悲观事务的性能有较小影响。

### tidb_txn_commit_batch_size <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `16384`
- 范围： `[1, 1073741824]`
- 单位：字节

<CustomContent platform="tidb">

- 该变量用于控制 TiDB 向 TiKV 发送事务提交请求的批量大小。如果应用负载中大多数事务的写入操作较多，将该变量调大可以提高批处理性能。但是，如果该变量值设置过大，超过了 TiKV 的 [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) 限制，提交可能会失败。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于控制 TiDB 向 TiKV 发送事务提交请求的批量大小。如果应用负载中大多数事务的写入操作较多，将该变量调大可以提高批处理性能。但是，如果该变量值设置过大，超过了 TiKV 的单条日志最大大小限制（默认为 8 MiB），提交可能会失败。

</CustomContent>

### tidb_txn_entry_size_limit <span class="version-mark">从 v7.6.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `0`
- 范围： `[0, 125829120]`
- 单位：字节

<CustomContent platform="tidb">

- 该变量用于动态修改 TiDB 配置项 [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)。它限制 TiDB 中单行数据的大小，等价于该配置项。该变量的默认值为 `0`，表示 TiDB 默认使用配置项 `txn-entry-size-limit` 的值。当该变量设为非零值时，`txn-entry-size-limit` 也会被设为相同的值。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 该变量用于动态修改 TiDB 配置项 [`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)。它限制 TiDB 中单行数据的大小，等价于该配置项。该变量的默认值为 `0`，表示 TiDB 默认使用配置项 `txn-entry-size-limit` 的值。当该变量设为非零值时，`txn-entry-size-limit` 也会被设为相同的值。

</CustomContent>

> **注意：**
>
> 在 SESSION 作用域下修改该变量仅影响当前用户会话，不影响 TiDB 内部会话。如果 TiDB 内部事务的 entry 大小超过配置项的限制，可能导致事务失败。因此，若需动态增大该限制，建议在 GLOBAL 作用域下修改该变量。

### tidb_txn_mode

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`pessimistic`
- 可选值：`pessimistic`、`optimistic`
- 该变量用于设置事务模式。TiDB 3.0 支持悲观事务。从 TiDB 3.0.8 开始，默认启用[悲观事务模式](/pessimistic-transaction.md)。
- 如果从 v3.0.7 或更早版本升级到 v3.0.8 或更高版本，默认事务模式不会改变。**只有新创建的集群才默认使用悲观事务模式**。
- 如果将该变量设为 "optimistic" 或 ""，TiDB 将使用[乐观事务模式](/optimistic-transaction.md)。

### tidb_use_plan_baselines <span class="version-mark">从 v4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制是否开启执行计划绑定功能，默认打开，可通过赋值 `OFF` 来关闭。关于执行计划绑定功能的使用可以参考[执行计划绑定文档](/sql-plan-management.md#创建绑定)。

### tidb_wait_split_region_finish

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 打散 Region 通常需要较长时间，由 PD 调度和 TiKV 负载决定。该变量用于设置执行 `SPLIT REGION` 语句时是否在所有 Region 完全打散后才将结果返回给客户端：
    - `ON` 要求 `SPLIT REGIONS` 语句等待所有 Region 打散完成。
    - `OFF` 允许 `SPLIT REGIONS` 语句在所有 Region 打散完成之前返回。
- 注意，在打散 Region 期间，正在被打散的 Region 的读写性能可能会受到影响。在批量写入或数据导入场景中，建议在 Region 打散完成后再导入数据。

### tidb_wait_split_region_timeout

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`300`
- 范围：`[1, 2147483647]`
- 单位：秒
- 该变量用于设置执行 `SPLIT REGION` 语句的超时时间。如果语句在指定时间内未执行完毕，将返回超时错误。

### tidb_window_concurrency <span class="version-mark">从 v4.0 版本开始引入</span>

> **警告：**
>
> 从 v5.0 版本开始，该变量被废弃。请使用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-从-v50-版本开始引入) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 这个变量用于设置 window 算子的并行度。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### tiflash_fastscan <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`OFF`
- 类型：布尔型
- 如果开启 [FastScan 功能](/tiflash/use-fastscan.md)（设置为 `ON` 时），TiFlash 可以提供更高效的查询性能，但不保证查询结果的精度和数据一致性。

### tiflash_fine_grained_shuffle_batch_size <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 默认值：`8192`
- 范围：`[1, 18446744073709551615]`
- 细粒度 shuffle 功能开启时，下推到 TiFlash 的窗口函数可以并行执行。该变量控制发送端发送数据的攒批大小。
- 对性能影响：如果该值设置过小，例如极端值 1，会导致每个 Block 都进行一次网络传输。如果设置过大，例如极端值整个表的行数，会导致接收端大部分时间都在等待数据，无法流水线计算。可以观察 TiFlash 接收端收到的行数分布情况，如果大部分线程接收的行数很少，例如只有几百行，可以增加该值以达到减少网络开销的目的。

### tiflash_fine_grained_shuffle_stream_count <span class="version-mark">从 v6.2.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：整数型
- 默认值：`0`
- 范围：`[-1, 1024]`
- 当窗口函数下推到 TiFlash 执行时，可以通过该变量控制窗口函数执行的并行度。不同取值含义：

    * -1: 表示不使用细粒度 shuffle 功能，下推到 TiFlash 的窗口函数以单线程方式执行
    * 0: 表示使用细粒度 shuffle 功能。如果 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-从-v610-版本开始引入) 有效（大于 0），则 `tiflash_fine_grained_shuffle_stream_count` 会自动取值为 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-从-v610-版本开始引入)，否则会根据 TiFlash 计算节点的 CPU 资源自动推算。最终在 TiFlash 上窗口函数的实际并发度为：min(`tiflash_fine_grained_shuffle_stream_count`，TiFlash 节点物理线程数)
    * 大于 0: 表示使用细粒度 shuffle 功能，下推到 TiFlash 的窗口函数会以多线程方式执行，并发度为： min(`tiflash_fine_grained_shuffle_stream_count`, TiFlash 节点物理线程数)
- 理论上窗口函数的性能会随着该值的增加线性提升。但是如果设置的值超过实际的物理线程数，反而会导致性能下降。

### tiflash_mem_quota_query_per_node <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[-1, 9223372036854775807]`
- 用于设置单个查询在单个 TiFlash 节点上的内存使用上限，超过该限制时 TiFlash 会报错并终止该查询。`-1` 或者 `0` 表示无限制。当该变量的值大于 `0` 且 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-从-v740-版本开始引入) 也设置为有效值时，TiFlash 将启用[查询级别的落盘机制](/tiflash/tiflash-spill-disk.md#查询级别的落盘)。

### tiflash_query_spill_ratio <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：浮点数
- 默认值：`0.7`
- 范围：`[0, 0.85]`
- 用于控制 TiFlash [查询级别的落盘](/tiflash/tiflash-spill-disk.md#查询级别的落盘)机制的阈值：`0` 表示关闭查询级别的自动落盘机制；大于 `0` 时，如果查询使用的内存超过 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入) * `tiflash_query_spill_ratio`，TiFlash 会触发查询级别的落盘，即将查询中支持落盘的算子的数据按需进行落盘。

> **注意：**
>
> - 该变量只在 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入) 大于 `0` 时生效，即如果 [tiflash_mem_quota_query_per_node](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入) 为 `0` 或 `-1`，即使 `tiflash_query_spill_ratio` 大于 `0` 也不会启用查询级别的落盘机制。
> - 当 TiFlash 查询级别的落盘机制开启时，TiFlash 单个算子的落盘阈值会自动失效，即如果 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-从-v740-版本开始引入) 和 `tiflash_query_spill_ratio` 均大于 0， [tidb_max_bytes_before_tiflash_external_sort](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-从-v700-版本开始引入)、[tidb_max_bytes_before_tiflash_external_group_by](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-从-v700-版本开始引入)、[tidb_max_bytes_before_tiflash_external_join](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-从-v700-版本开始引入) 这三个变量会自动失效，等效于被设置为 `0`。

### tiflash_replica_read <span class="version-mark">从 v7.3.0 版本开始引入</span>

> **注意：**
>
> 该变量不适用于 TiDB Cloud。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值： `all_replicas`
- 可选值：`all_replicas`、`closest_adaptive`、`closest_replicas`
- 该变量用于设置当查询需要 TiFlash 引擎时选择 TiFlash 副本的策略。
    - `all_replicas` 表示使用所有可用的 TiFlash 副本进行分析计算。
    - `closest_adaptive` 表示优先使用与发起查询的 TiDB 节点在同一 zone 的 TiFlash 副本。如果该 zone 的副本不包含所有所需数据，则查询会涉及其他 zone 的 TiFlash 副本及其对应的 TiFlash 节点。
    - `closest_replicas` 表示仅使用与发起查询的 TiDB 节点在同一 zone 的 TiFlash 副本。如果该 zone 的副本不包含所有所需数据，查询将返回错误。

<CustomContent platform="tidb">

> **注意：**
>
> - 如果 TiDB 节点未配置 [zone 属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)且 `tiflash_replica_read` 未设为 `all_replicas`，TiFlash 将忽略副本选择策略，使用所有 TiFlash 副本进行查询，并返回 `The variable tiflash_replica_read is ignored.` 警告。
> - 如果 TiFlash 节点未配置 [zone 属性](/schedule-replicas-by-topology-labels.md#configure-labels-for-tikv-and-tiflash)，则该节点被视为不属于任何 zone。

</CustomContent>

### tiflash_hashagg_preaggregation_mode <span class="version-mark">从 v8.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：是
- 类型：枚举型
- 默认值：`force_preagg`
- 可选值：`force_preagg`、`force_streaming`、`auto`
- 该变量用于控制下推到 TiFlash 的两阶段或三阶段 HashAgg 在第一阶段采用哪种预聚合策略：
    - `force_preagg`：TiFlash 在第一阶段的 HashAgg 中强制进行预聚合操作，与 v8.3.0 之前版本的行为一致
    - `force_streaming`：TiFlash 直接将数据发送到下一阶段的 HashAgg，不进行预聚合操作
    - `auto`：TiFlash 根据当前工作负载的聚合度自动选择是否进行预聚合操作

### tikv_client_read_timeout <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 该变量用于设置查询语句中 TiDB 发送 TiKV RPC 读请求的超时时间。当 TiDB 集群在网络不稳定或 TiKV 的 I/O 延迟抖动严重的环境下，且用户对查询 SQL 的延迟比较敏感时，可以通过设置 `tikv_client_read_timeout` 调小 TiKV RPC 读请求的超时时间，这样当某个 TiKV 节点出现 I/O 延迟抖动时，TiDB 侧可以快速超时并重新发送 TiKV RPC 请求给下一个 TiKV Region Peer 所在的 TiKV 节点。如果所有 TiKV Region Peer 都请求超时，则会用默认的超时时间（通常是 40 秒）进行新一轮的重试。
- 你也可以在查询语句中使用 Optimizer Hint `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */` 来设置 TiDB 发送 TiKV RPC 读请求的超时时间。当同时设置了 Optimizer Hint 和该系统变量时，Optimizer Hint 的优先级更高。
- 默认值 `0` 表示使用默认的超时时间（通常是 40 秒）。

> **注意：**
>
> - 一个普通查询通常耗时几毫秒，但偶尔可能会出现某个 TiKV 节点的网络不稳定或 I/O 抖动，导致查询耗时超过 1 秒甚至 10 秒。此时，你可以尝试在查询语句中使用 Optimizer Hint `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=100) */` 将 TiKV RPC 读请求超时设置为 100 毫秒，这样即使遇到某个 TiKV 节点查询慢，也可以快速超时然后重新发送 RPC 请求给下一个 TiKV Region Peer 所在的 TiKV 节点。由于两个 TiKV 节点同时出现 I/O 抖动的概率较低，所以该查询语句的耗时通常可以预期在几毫秒到 110 毫秒之间。
> - 不建议将 `tikv_client_read_timeout` 的值设置的太小（例如，1 毫秒），否则 TiDB 集群在负载压力较大时会很容易导致请求超时，然后重试会进一步增加 TiDB 集群的压力。
> - 如需为不同类型的查询语句设置不同的超时时间，建议使用 Optimizer Hint。

### time_zone

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`SYSTEM`
- 数据库所使用的时区。这个变量值可以写成时区偏移的形式，如 '-8:00'，也可以写成一个命名时区，如 'America/Los_Angeles'。
- 默认值 `SYSTEM` 表示时区应当与系统主机的时区相同。系统的时区可通过 [`system_time_zone`](#system_time_zone) 获取。

### timestamp

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：浮点数
- 默认值：`0`
- 取值范围：`[0, 2147483647]`
- 一个 Unix 时间戳。变量值非空时，表示 `CURRENT_TIMESTAMP()`、`NOW()` 等函数的时间戳。该变量通常用于数据恢复或数据复制。

### transaction_isolation

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值：`REPEATABLE-READ`
- 可选值：`READ-UNCOMMITTED`，`READ-COMMITTED`，`REPEATABLE-READ`，`SERIALIZABLE`
- 这个变量用于设置事务隔离级别。TiDB 为了兼容 MySQL，支持可重复读 (`REPEATABLE-READ`)，但实际的隔离级别是快照隔离。详情见[事务隔离级别](/transaction-isolation-levels.md)。

### tx_isolation

这个变量是 `transaction_isolation` 的别名。

### tx_isolation_one_shot

> **注意：**
>
> 该变量仅用于 TiDB 内部实现，不推荐设置该变量。

在 TiDB 内部实现中，TiDB 解释器会将 `SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]` 语句转化为 `SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`。

### tx_read_ts

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 在 Stale Read 场景下，该会话变量用于帮助记录 Stable Read TS 值。
- 该变量仅用于 TiDB 内部实现，**不推荐设置该变量**。

### txn_scope

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`global`
- 可选值：`global` 和 `local`
- 该变量用于设置当前会话事务是全局事务还是局部事务。
- 该变量仅用于 TiDB 内部操作，**不推荐设置该变量**。

### validate_password.check_user_name <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`ON`
- 类型：布尔型
- 该变量是密码复杂度策略检查中的一个检查项，用于进行密码与用户名匹配检查。只有 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启时，该变量才生效。
- 当该变量生效且为 `ON` 时，如果设置账户密码，TiDB 会将密码与当前会话账户的用户名部分（不包含主机名部分）进行比较，如果匹配则拒绝该密码。
- 该变量独立于 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入)，即不受密码复杂度检测强度的控制。

### validate_password.dictionary <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：""
- 类型：字符串
- 该变量是密码复杂度策略检查中的一个检查项，用于进行密码与字典字符串匹配检查。只有当 [`validate_password.enable`](/system-variables.md#validate_passwordenable-从-v650-版本开始引入) 开启且 [validate_password.policy](/system-variables.md#validate_passwordpolicy-从-v650-版本开始引入) 设置为 `2` (STRONG) 时，该变量才生效。
- 该变量是一个长字符串，长度不超过 1024，字符串内容可包含一个或多个在密码中不允许出现的单词，每个单词之间采用英文分号（`;`）分隔。
- 默认情况下，该变量为空值，不执行字典检查。要进行字典检查，该变量值必须包含待匹配的单词。配置了该变量后，在设置账户密码时，TiDB 会将长度为 4 到 100 的密码的每个子字符串与该变量中配置的单词进行比较。任何匹配都会导致密码被拒绝。比较不区分大小写。

### validate_password.enable <span class="version-mark">从 v6.5.0 版本开始引入</span>

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)，该变量始终开启。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`OFF`
- 类型：布尔型
- 该变量用于控制是否进行密码复杂度检查。如果该变量设为 `ON`，TiDB 将在设置密码时进行密码复杂度检查。

### validate_password.length <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `8`
- 范围：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[0, 2147483647]`，[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 为 `[8, 2147483647]`
- 该变量是密码复杂度检查中的一项检查项，用于检查密码长度是否足够。默认最小密码长度为 `8`。该变量仅在 [`validate_password.enable`](#validate_passwordenable-从-v650-版本开始引入) 开启时生效。
- 该变量的值不能小于表达式：`validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`。
- 如果你修改了 `validate_password.number_count`、`validate_password.special_char_count` 或 `validate_password.mixed_case_count` 的值，使得该表达式的值大于 `validate_password.length`，则 `validate_password.length` 的值会自动调整为与表达式值一致。

### validate_password.mixed_case_count <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `1`
- 范围：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[0, 2147483647]`，[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 为 `[1, 2147483647]`
- 该变量是密码复杂度检查中的一项检查项，用于检查密码中是否包含足够数量的大小写字母。该变量仅在 [`validate_password.enable`](#validate_passwordenable-new-in-v650) 开启且 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) 设为 `1` (MEDIUM) 或更高时生效。
- 密码中大写字母和小写字母的数量都不能少于 `validate_password.mixed_case_count` 的值。例如，当变量设为 `1` 时，密码必须至少包含一个大写字母和一个小写字母。

### validate_password.number_count <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `1`
- 范围：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[0, 2147483647]`，[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 为 `[1, 2147483647]`
- 该变量是密码复杂度检查中的一项检查项，用于检查密码中是否包含足够数量的数字。该变量仅在 [`validate_password.enable`](#password_reuse_interval-new-in-v650) 开启且 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) 设为 `1` (MEDIUM) 或更高时生效。

### validate_password.policy <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：枚举型
- 默认值： `1`
- 可选值：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `0`、`1`、`2`；[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 为 `1`、`2`
- 该变量用于控制密码复杂度检查的策略。该变量仅在 [`validate_password.enable`](#password_reuse_interval-new-in-v650) 开启时生效。该变量的值决定了除 `validate_password.check_user_name` 外的其他 `validate-password` 变量是否在密码复杂度检查中生效。
- 该变量的值可以为 `0`、`1` 或 `2`（分别对应 LOW、MEDIUM 或 STRONG）。不同策略级别有不同的检查项：
    - 0 或 LOW：密码长度。
    - 1 或 MEDIUM：密码长度、大小写字母、数字和特殊字符。
    - 2 或 STRONG：密码长度、大小写字母、数字、特殊字符和字典匹配。

### validate_password.special_char_count <span class="version-mark">从 v6.5.0 版本开始引入</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值： `1`
- 范围：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[0, 2147483647]`，[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 为 `[1, 2147483647]`
- 该变量是密码复杂度检查中的一项检查项，用于检查密码中是否包含足够数量的特殊字符。该变量仅在 [`validate_password.enable`](#password_reuse_interval-new-in-v650) 开启且 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) 设为 `1` (MEDIUM) 或更高时生效。

### version

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`8.0.11-TiDB-(tidb version)`
- 这个变量的值是 MySQL 的版本和 TiDB 的版本，例如 '8.0.11-TiDB-v8.5.0'。

### version_comment

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：(string)
- 这个变量的值是 TiDB 版本号的其他信息，例如 'TiDB Server (Apache License 2.0) Community Edition, MySQL 8.0 compatible'。

### version_compile_machine

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：(string)
- 这个变量值是运行 TiDB 的 CPU 架构的名称。

### version_compile_os

- 作用域：NONE
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：(string)
- 这个变量值是 TiDB 所在操作系统的名称。

### wait_timeout

> **注意：**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 实例，该变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：整数型
- 默认值：`28800`
- 范围：`[0, 31536000]`
- 单位：秒
- 该变量用于控制用户会话的空闲超时时间。值为零表示不限制。

### warning_count

- 作用域：SESSION
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 默认值：`0`
- 这个只读变量表示之前执行语句中出现的警告数。

### windowing_use_high_precision

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否受 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value) 控制：否
- 类型：布尔型
- 默认值：`ON`
- 这个变量用于控制计算[窗口函数](/functions-and-operators/window-functions.md)时是否采用高精度模式。
