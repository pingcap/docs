---
title: System Variables
summary: Use system variables to optimize performance or alter running behavior.
aliases: ['/tidb/dev/tidb-specific-system-variables','/docs/dev/system-variables/','/docs/dev/reference/configuration/tidb-server/mysql-variables/', '/docs/dev/tidb-specific-system-variables/','/docs/dev/reference/configuration/tidb-server/tidb-specific-variables/']
---

# System Variables

TiDB system variables behave similar to MySQL, in that settings apply on a `SESSION` or `GLOBAL` scope:

- Changes on a `SESSION` scope will only affect the current session.
- Changes on a `GLOBAL` scope apply immediately. If this variable is also`SESSION` scoped, all sessions (including your session) will continue to use their current session value.
- Changes are made using the [`SET` statement](/sql-statements/sql-statement-set-variable.md):

```sql
# These two identical statements change a session variable
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# These two identical statements change a global variable
SET @@global.tidb_distsql_scan_concurrency = 10;
SET GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **Note:**
>
> Several `GLOBAL` variables persist to the TiDB cluster. Some variables in this document have a `Persists to cluster` setting, which can be configured to `Yes` or `No`.
>
> - For variables with the `Persists to cluster: Yes` setting, when a global variable is changed, a notification is sent to all TiDB servers to refresh their system variable cache. When you add additional TiDB servers or restart existing TiDB servers, the persisted configuration value is automatically used.
> - For variables with the `Persists to cluster: No` setting, changes only apply to the local TiDB instance that you are connected to. To retain any values set, you need to specify the variables in your `tidb.toml` configuration file.
>
> Additionally, TiDB presents several MySQL variables as both readable and settable. This is required for compatibility, because it is common for both applications and connectors to read MySQL variables. For example, JDBC connectors both read and set query cache settings, despite not relying on the behavior.

> **Note:**
>
> Larger values do not always yield better performance. It is also important to consider the number of concurrent connections that are executing statements, because most settings apply to each connection.
>
> Consider the unit of a variable when you determine safe values:
>
> * For threads, safe values are typically up to the number of CPU cores.
> * For bytes, safe values are typically less than the amount of system memory.
> * For time, pay attention that the unit might be seconds or milliseconds.
>
> Variables using the same unit might compete for the same set of resources.

Starting from v7.4.0, you can temporarily modify the value of some `SESSION` variables during statement execution using [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value). After the statement is executed, the value of the system variable in the current session is automatically changed back to the original value. This hint can be used to modify some system variables related to the optimizer and executor. Variables in this document have a `Applies to hint SET_VAR` setting, which can be configured to `Yes` or `No`.

- For variables with the `Applies to hint SET_VAR: Yes` setting, you can use the [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) hint to modify the value of the system variable in the current session during statement execution.
- For variables with the `Applies to hint SET_VAR: No` setting, you cannot use the [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) hint to modify the value of the system variable in the current session during statement execution.

For more information about the `SET_VAR` hint, see [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value).

## Variable reference

### allow_auto_random_explicit_insert <span class="version-mark">New in v4.0.3</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- Determines whether to allow explicitly specifying the values of the column with the `AUTO_RANDOM` attribute in the `INSERT` statement.

### authentication_ldap_sasl_auth_method_name <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `SCRAM-SHA-1`
- Possible values: `SCRAM-SHA-1`, `SCRAM-SHA-256`, and `GSSAPI`.
- For LDAP SASL authentication, this variable specifies the authentication method name.

### authentication_ldap_sasl_bind_base_dn <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP SASL authentication, this variable limits the search scope within the search tree. If a user is created without the `AS ...` clause, TiDB will automatically search the `dn` in LDAP server according to the user name.

### authentication_ldap_sasl_bind_root_dn <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP SASL authentication, this variable specifies the `dn` used to log in to the LDAP server to search users.

### authentication_ldap_sasl_bind_root_pwd <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP SASL authentication, this variable specifies the password used to log in to the LDAP server to search users.

### authentication_ldap_sasl_ca_path <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP SASL authentication, this variable specifies the absolute path of the certificate authority file for StartTLS connections.

### authentication_ldap_sasl_init_pool_size <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `10`
- Range: `[1, 32767]`
- For LDAP SASL authentication, this variable specifies the initial connections in the connection pool to the LDAP server.

### authentication_ldap_sasl_max_pool_size <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1000`
- Range: `[1, 32767]`
- For LDAP SASL authentication, this variable specifies the maximum connections in the connection pool to the LDAP server.

### authentication_ldap_sasl_server_host <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP SASL authentication, this variable specifies the LDAP server host name or IP address.

### authentication_ldap_sasl_server_port <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `389`
- Range: `[1, 65535]`
- For LDAP SASL authentication, this variable specifies the TCP/IP port number of the LDAP server.

### authentication_ldap_sasl_tls <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- For LDAP SASL authentication, this variable controls whether connections by the plugin to the LDAP server are protected with StartTLS.

### authentication_ldap_simple_auth_method_name <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `SIMPLE`
- Possible values: `SIMPLE`.
- For LDAP simple authentication, this variable specifies the authentication method name. The only supported value is `SIMPLE`.

### authentication_ldap_simple_bind_base_dn <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP simple authentication, this variable limits the search scope within the search tree. If a user is created without the `AS ...` clause, TiDB will automatically search the `dn` in LDAP server according to the user name.

### authentication_ldap_simple_bind_root_dn <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP simple authentication, this variable specifies the `dn` used to log in to the LDAP server to search users.

### authentication_ldap_simple_bind_root_pwd <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP simple authentication, this variable specifies the password used to log in to the LDAP server to search users.

### authentication_ldap_simple_ca_path <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP simple authentication, this variable specifies the absolute path of the certificate authority file for StartTLS connections.

### authentication_ldap_simple_init_pool_size <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `10`
- Range: `[1, 32767]`
- For LDAP simple authentication, this variable specifies the initial connections in the connection pool to the LDAP server.

### authentication_ldap_simple_max_pool_size <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1000`
- Range: `[1, 32767]`
- For LDAP simple authentication, this variable specifies the maximum connections in the connection pool to the LDAP server.

### authentication_ldap_simple_server_host <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- For LDAP simple authentication, this variable specifies the LDAP server host name or IP address.

### authentication_ldap_simple_server_port <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `389`
- Range: `[1, 65535]`
- For LDAP simple authentication, this variable specifies the TCP/IP port number of the LDAP server.

### authentication_ldap_simple_tls <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- For LDAP simple authentication, this variable controls whether connections by the plugin to the LDAP server are protected with StartTLS.

### auto_increment_increment

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- Range: `[1, 65535]`
- Controls the step size of `AUTO_INCREMENT` values to be allocated to a column, and allocation rules for `AUTO_RANDOM` IDs. It is often used in combination with [`auto_increment_offset`](#auto_increment_offset).

### auto_increment_offset

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- Range: `[1, 65535]`
- Controls the initial offset of `AUTO_INCREMENT` values to be allocated to a column, and allocation rules for `AUTO_RANDOM` IDs. This setting is often used in combination with [`auto_increment_increment`](#auto_increment_increment). For example:

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

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- Controls whether statements should automatically commit when not in an explicit transaction. See [Transaction Overview](/transaction-overview.md#autocommit) for more information.

### block_encryption_mode

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `aes-128-ecb`
- Value options: `aes-128-ecb`, `aes-192-ecb`, `aes-256-ecb`, `aes-128-cbc`, `aes-192-cbc`, `aes-256-cbc`, `aes-128-ofb`, `aes-192-ofb`, `aes-256-ofb`, `aes-128-cfb`, `aes-192-cfb`, `aes-256-cfb`
- This variable sets the encryption mode for the built-in functions `AES_ENCRYPT()` and `AES_DECRYPT()`.

### character_set_client

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `utf8mb4`
- The character set for data sent from the client. See [Character Set and Collation](/character-set-and-collation.md) for details on the use of character sets and collations in TiDB. It is recommended to use [`SET NAMES`](/sql-statements/sql-statement-set-names.md) to change the character set when needed.

### character_set_connection

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `utf8mb4`
- The character set for string literals that do not have a specified character set.

### character_set_database

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `utf8mb4`
- This variable indicates the character set of the default database in use. **It is NOT recommended to set this variable**. When a new default database is selected, the server changes the variable value.

### character_set_results

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `utf8mb4`
- The character set that is used when data is sent to the client.

### character_set_server

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `utf8mb4`
- The default character set for the server.

### collation_connection

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `utf8mb4_bin`
- This variable indicates the collation used in the current connection. It is consistent with the MySQL variable `collation_connection`.

### collation_database

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `utf8mb4_bin`
- This variable indicates the default collation of the database in use. **It is NOT recommended to set this variable**. When a new database is selected, TiDB changes this variable value.

### collation_server

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `utf8mb4_bin`
- The default collation used when the database is created.

### cte_max_recursion_depth

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `1000`
- Range: `[0, 4294967295]`
- Controls the maximum recursion depth in Common Table Expressions.

### datadir

> **Note:**
>
> This variable is not supported on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

<CustomContent platform="tidb">

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: it depends on the component and the deployment method.
    - `/tmp/tidb`: when you set `"unistore"` for [`--store`](/command-line-flags-for-tidb-configuration.md#--store) or if you don't set `--store`.
    - `${pd-ip}:${pd-port}`: when you use TiKV, which is the default storage engine for TiUP and TiDB Operator for Kubernetes deployments.
- This variable indicates the location where data is stored. This location can be a local path `/tmp/tidb`, or point to a PD server if the data is stored on TiKV. A value in the format of `${pd-ip}:${pd-port}` indicates the PD server that TiDB connects to on startup.

</CustomContent>

<CustomContent platform="tidb-cloud">

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: it depends on the component and the deployment method.
    - `/tmp/tidb`: when you set `"unistore"` for [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store) or if you don't set `--store`.
    - `${pd-ip}:${pd-port}`: when you use TiKV, which is the default storage engine for TiUP and TiDB Operator for Kubernetes deployments.
- This variable indicates the location where data is stored. This location can be a local path `/tmp/tidb`, or point to a PD server if the data is stored on TiKV. A value in the format of `${pd-ip}:${pd-port}` indicates the PD server that TiDB connects to on startup.

</CustomContent>

### ddl_slow_threshold

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `300`
- Range: `[0, 2147483647]`
- Unit: Milliseconds
- Log DDL operations whose execution time exceeds the threshold value.

### default_authentication_plugin

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `mysql_native_password`
- Possible values: `mysql_native_password`, `caching_sha2_password`, `tidb_sm3_password`, `tidb_auth_token`, `authentication_ldap_sasl`, and `authentication_ldap_simple`.
- This variable sets the authentication method that the server advertises when the server-client connection is being established.
- To authenticate using the `tidb_sm3_password` method, you can connect to TiDB using [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3).

<CustomContent platform="tidb">

For more possible values of this variable, see [Authentication plugin status](/security-compatibility-with-mysql.md#authentication-plugin-status).

</CustomContent>

### default_collation_for_utf8mb4 <span class="version-mark">New in v7.4.0</span>

- Scope: GLOBAL | SESSION
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: `utf8mb4_bin`
- Value options: `utf8mb4_bin`, `utf8mb4_general_ci`, `utf8mb4_0900_ai_ci`
- This variable is used to set the default [collation](/character-set-and-collation.md) for the `utf8mb4` character set. It affects the behavior of the following statements:
    - The default collation displayed in the [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md) and [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) statements.
    - If [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) and [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) statements contain the `CHARACTER SET utf8mb4` clause against a table or a column without specifying a collation, the collation specified by this variable is used. This does not affect the behavior when `CHARACTER SET` clause is not used.
    - If [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md) and [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md) statements contain `CHARACTER SET utf8mb4` clause without specifying a collation, the collation specified by this variable is used. This does not affect the behavior when `CHARACTER SET` clause is not used.
    - If the `COLLATE` clause is not used, any literal string in the format of `_utf8mb4'string'` uses the collation specified by this variable.

### default_password_lifetime <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 65535]`
- Sets the global policy for automatic password expiration. The default value `0` indicates that the password never expires. If this system variable is set to a positive integer `N`, it means that the password lifetime is `N` days, and you must change your password within `N` days.

### default_week_format

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 7]`
- Sets the week format used by the `WEEK()` function.

### disconnect_on_expired_password <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is read-only. It indicates whether TiDB disconnects the client connection when the password is expired. If the variable is set to `ON`, the client connection is disconnected when the password is expired. If the variable is set to `OFF`, the client connection is restricted to the "sandbox mode" and the user can only execute the password reset operation.

<CustomContent platform="tidb">

- If you need to change the behavior of the client connection for the expired password, modify the [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) configuration item in the configuration file.

</CustomContent>

<CustomContent platform="tidb-cloud">

- If you need to change the default behavior of the client connection for the expired password, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

</CustomContent>

### div_precision_increment <span class="version-mark">New in v8.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `4`
- Range: `[0, 30]`
- This variable specifies the number of digits by which to increase the scale of the result of a division operation performed using the `/` operator. This variable is the same as MySQL.

### error_count

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- A read-only variable that indicates the number of errors that resulted from the last statement that generated messages.

### foreign_key_checks

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: Before v6.6.0, the default value is `OFF`. Starting from v6.6.0, the default value is `ON`.
- This variable controls whether to enable foreign key constraint checking.

### group_concat_max_len

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1024`
- Range: `[4, 18446744073709551615]`
- The maximum buffer size for items in the `GROUP_CONCAT()` function.

### have_openssl

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `DISABLED`
- A read-only variable for MySQL compatibility. Set to `YES` by the server when the server has TLS enabled.

### have_ssl

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `DISABLED`
- A read-only variable for MySQL compatibility. Set to `YES` by the server when the server has TLS enabled.

### hostname

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: (system hostname)
- The hostname of the TiDB server as a read-only variable.

### identity <span class="version-mark">New in v5.3.0</span>

This variable is an alias for [`last_insert_id`](#last_insert_id).

### init_connect

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- The `init_connect` feature permits a SQL statement to be automatically executed when you first connect to a TiDB server. If you have the `CONNECTION_ADMIN` or `SUPER` privileges, this `init_connect` statement will not be executed. If the `init_connect` statement results in an error, your user connection will be terminated.

### innodb_lock_wait_timeout

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `50`
- Range: `[1, 3600]`
- Unit: Seconds
- The lock wait timeout for pessimistic transactions (default).

### interactive_timeout

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `28800`
- Range: `[1, 31536000]`
- Unit: Seconds
- This variable represents the idle timeout of the interactive user session. Interactive user session refers to the session established by calling [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API using the `CLIENT_INTERACTIVE` option (for example, MySQL Shell and MySQL Client). This variable is fully compatible with MySQL.

### last_insert_id

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 18446744073709551615]`
- This variable returns the last `AUTO_INCREMENT` or `AUTO_RANDOM` value generated by an insert statement.
- The value of `last_insert_id` is the same as the value returned by the function `LAST_INSERT_ID()`.

### last_plan_from_binding <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to show whether the execution plan used in the previous statement was influenced by a [plan binding](/sql-plan-management.md)

### last_plan_from_cache <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to show whether the execution plan used in the previous `execute` statement is taken directly from the plan cache.

### last_sql_use_alloc <span class="version-mark">New in v6.4.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `OFF`
- This variable is read-only. It is used to show whether the previous statement uses a cached chunk object (chunk allocation).

### license

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `Apache License 2.0`
- This variable indicates the license of your TiDB server installation.

### log_bin

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable indicates whether [TiDB Binlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview) is used.

### max_allowed_packet <span class="version-mark">New in v6.1.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `67108864`
- Range: `[1024, 1073741824]`
- The value should be an integer multiple of 1024. If the value is not divisible by 1024, a warning will be prompted and the value will be rounded down. For example, when the value is set to 1025, the actual value in TiDB is 1024.
- The maximum packet size allowed by the server and the client in one transmission of packets.
- In the `SESSION` scope, this variable is read-only.
- This variable is compatible with MySQL.

### password_history <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 4294967295]`
- This variable is used to establish a password reuse policy that allows TiDB to limit password reuse based on the number of password changes. The default value `0` means disabling the password reuse policy based on the number of password changes. When this variable is set to a positive integer `N`, the reuse of the last `N` passwords is not allowed.

### mpp_exchange_compression_mode <span class="version-mark">New in v6.6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `UNSPECIFIED`
- Value options: `NONE`, `FAST`, `HIGH_COMPRESSION`, `UNSPECIFIED`
- This variable is used to specify the data compression mode of the MPP Exchange operator. This variable takes effect when TiDB selects the MPP execution plan with the version number `1`. The meanings of the variable values are as follows:
    - `UNSPECIFIED`: means unspecified. TiDB will automatically select the compression mode. Currently, TiDB automatically selects the `FAST` mode.
    - `NONE`: no data compression is used.
    - `FAST`: fast mode. The overall performance is good and the compression ratio is less than `HIGH_COMPRESSION`.
    - `HIGH_COMPRESSION`: the high compression ratio mode.

### mpp_version <span class="version-mark">New in v6.6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `UNSPECIFIED`
- Value options: `UNSPECIFIED`, `0`, `1`
- This variable is used to specify different versions of the MPP execution plan. After a version is specified, TiDB selects the specified version of the MPP execution plan. The meanings of the variable values are as follows:
    - `UNSPECIFIED`: means unspecified. TiDB automatically selects the latest version `1`.
    - `0`: compatible with all TiDB cluster versions. Features with the MPP version greater than `0` do not take effect in this mode.
    - `1`: new in v6.6.0, used to enable data exchange with compression on TiFlash. For details, see [MPP version and exchange data compression](/explain-mpp.md#mpp-version-and-exchange-data-compression).

### password_reuse_interval <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 4294967295]`
- This variable is used to establish a password reuse policy that allows TiDB to limit password reuse based on time elapsed. The default value `0` means disabling the password reuse policy based on time elapsed. When this variable is set to a positive integer `N`, the reuse of any password used in the last `N` days is not allowed.

### max_connections

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 100000]`
- The maximum number of concurrent connections permitted for a single TiDB instance. This variable can be used for resources control.
- The default value `0` means no limit. When the value of this variable is larger than `0`, and the number of connections reaches the value, the TiDB server rejects new connections from clients.

### max_execution_time

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- Unit: Milliseconds
- The maximum execution time of a statement. The default value is unlimited (zero).

> **Note:**
>
> The `max_execution_time` system variable currently only controls the maximum execution time for read-only SQL statements. The precision of the timeout value is roughly 100ms. This means the statement might not be terminated in accurate milliseconds as you specify.

<CustomContent platform="tidb">

For a SQL statement with the [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) hint, the maximum execution time of this statement is limited by the hint instead of this variable. The hint can also be used with SQL bindings as described [in the SQL FAQ](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement).

</CustomContent>

<CustomContent platform="tidb-cloud">

For a SQL statement with the [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) hint, the maximum execution time of this statement is limited by the hint instead of this variable. The hint can also be used with SQL bindings as described [in the SQL FAQ](https://docs.pingcap.com/tidb/stable/sql-faq).

</CustomContent>

### max_prepared_stmt_count

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[-1, 1048576]`
- Specifies the maximum number of [`PREPARE`](/sql-statements/sql-statement-prepare.md) statements in the current TiDB instance.
- The value of `-1` means no limit on the maximum number of `PREPARE` statements in the current TiDB instance.
- If you set the variable to a value that exceeds the upper limit `1048576`, `1048576` is used instead:

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

### pd_enable_follower_handle_region <span class="version-mark">New in v7.6.0</span>

> **Warning:**
>
> The [Active PD Follower](https://docs.pingcap.com/tidb/dev/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service) feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the Active PD Follower feature (currently only applicable to requests for Region information). When the value is `OFF`, TiDB only obtains Region information from the PD leader. When the value is `ON`, TiDB evenly distributes requests for Region information to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.
- Scenarios for enabling Active PD Follower:
    * In a cluster with a large number of Regions, the PD leader experiences high CPU pressure due to the increased overhead of handling heartbeats and scheduling tasks.
    * In a TiDB cluster with many TiDB instances, the PD leader experiences high CPU pressure due to a high concurrency of requests for Region information.

### plugin_dir

> **Note:**
>
> This variable is not supported on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- Indicates the directory to load plugins as specified by a command-line flag.

### plugin_load

> **Note:**
>
> This variable is not supported on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- Indicates the plugins to load when TiDB is started. These plugins are specified by a command-line flag and separated by commas.

### port

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `4000`
- Range: `[0, 65535]`
- The port that the `tidb-server` is listening on when speaking the MySQL protocol.

### rand_seed1

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- This variable is used to seed the random value generator used in the `RAND()` SQL function.
- The behavior of this variable is MySQL compatible.

### rand_seed2

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- This variable is used to seed the random value generator used in the `RAND()` SQL function.
- The behavior of this variable is MySQL compatible.

### require_secure_transport <span class="version-mark">New in v6.1.0</span>

> **Note:**
>
> Currently, this variable is not supported on [TiDB Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated). DO **NOT** enable this variable for TiDB Dedicated clusters. Otherwise, you might get SQL client connection failures. This restriction is a temporary control measure and will be resolved in a future release.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF` for TiDB Self-Hosted and [TiDB Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated), `ON` for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)

<CustomContent platform="tidb">

- This variable ensures that all connections to TiDB are either on a local socket, or using TLS. See [Enable TLS between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md) for additional details.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable ensures that all connections to TiDB are either on a local socket, or using TLS.

</CustomContent>

- Setting this variable to `ON` requires you to connect to TiDB from a session that has TLS enabled. This helps prevent lock-out scenarios when TLS is not configured correctly.
- This setting was previously a `tidb.toml` option (`security.require-secure-transport`), but changed to a system variable starting from TiDB v6.1.0.
- Starting from v6.5.6, v7.1.2, v7.5.1, and v8.0.0, when Security Enhanced Mode (SEM) is enabled, setting this variable to `ON` is prohibited to avoid potential connectivity issues for users.

### skip_name_resolve <span class="version-mark">New in v5.2.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether the `tidb-server` instance resolves hostnames as a part of the connection handshake.
- When the DNS is unreliable, you can enable this option to improve network performance.

> **Note:**
>
> When `skip_name_resolve=ON`, users with a hostname in their identity will no longer be able to log into the server. For example:
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> In this example, it is recommended to replace `apphost` with an IP address or the wildcard (`%`).

### socket

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- The local unix socket file that the `tidb-server` is listening on when speaking the MySQL protocol.

### sql_log_bin

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- Indicates whether to write changes to [TiDB Binlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview) or not.

> **Note:**
>
> It is not recommended to set `sql_log_bin` as a global variable because the future versions of TiDB might only allow setting this as a session variable.

### sql_mode

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
- This variable controls a number of MySQL compatibility behaviors. See [SQL Mode](/sql-mode.md) for more information.

### sql_require_primary_key <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enforce the requirement that a table has a primary key. After this variable is enabled, attempting to create or alter a table without a primary key will produce an error.
- This feature is based on the similarly named [`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key) in MySQL 8.0.
- It is strongly recommended to enable this variable when using TiCDC. This is because replicating changes to a MySQL sink requires that tables have a primary key.

<CustomContent platform="tidb">

- If you enable this variable and are using TiDB Data Migration (DM) to migrate data, it is recommended that you add `sql_require_ primary_key` to the `session` part in the [DM Task Configuration File](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) and set it to `OFF`. Otherwise, it will cause DM to fail to create tasks.

</CustomContent>

### sql_select_limit <span class="version-mark">New in v4.0.2</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `18446744073709551615`
- Range: `[0, 18446744073709551615]`
- Unit: Rows
- The maximum number of rows returned by the `SELECT` statements.

### ssl_ca

<CustomContent platform="tidb">

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- The location of the certificate authority file (if there is one). The value of this variable is defined by the TiDB configuration item [`ssl-ca`](/tidb-configuration-file.md#ssl-ca).

</CustomContent>

<CustomContent platform="tidb-cloud">

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- The location of the certificate authority file (if there is one). The value of this variable is defined by the TiDB configuration item [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca).

</CustomContent>

### ssl_cert

<CustomContent platform="tidb">

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- The location of the certificate file (if there is a file) that is used for SSL/TLS connections. The value of this variable is defined by the TiDB configuration item [`ssl-cert`](/tidb-configuration-file.md#ssl-cert).

</CustomContent>

<CustomContent platform="tidb-cloud">

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- The location of the certificate file (if there is a file) that is used for SSL/TLS connections. The value of this variable is defined by the TiDB configuration item [`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert).

</CustomContent>

### ssl_key

<CustomContent platform="tidb">

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- The location of the private key file (if there is one) that is used for SSL/TLS connections. The value of this variable is defined by TiDB configuration item [`ssl-key`](/tidb-configuration-file.md#ssl-cert).

</CustomContent>

<CustomContent platform="tidb-cloud">

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- The location of the private key file (if there is one) that is used for SSL/TLS connections. The value of this variable is defined by TiDB configuration item [`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key).

</CustomContent>

### system_time_zone

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: (system dependent)
- This variable shows the system time zone from when TiDB was first bootstrapped. See also [`time_zone`](#time_zone).

### tidb_adaptive_closest_read_threshold <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `4096`
- Range: `[0, 9223372036854775807]`
- Unit: Bytes
- This variable is used to control the threshold at which the TiDB server prefers to send read requests to a replica in the same availability zone as the TiDB server when [`tidb_replica_read`](#tidb_replica_read-new-in-v40) is set to `closest-adaptive`. If the estimated result is higher than or equal to this threshold, TiDB prefers to send read requests to a replica in the same availability zone. Otherwise, TiDB sends read requests to the leader replica.

### tidb_allow_tiflash_cop <span class="version-mark">New in v7.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- When TiDB pushes computation tasks down to TiFlash, there are three methods (or protocols) to choose from: Cop, BatchCop, and MPP. Compared to Cop and BatchCop, the MPP protocol is more mature and offers better task and resource management. Therefore, it is recommended to use the MPP protocol.
    - `0` or `OFF`: the optimizer only generates plans using the TiFlash MPP protocol.
    - `1` or `ON`: the optimizer determines whether to use the Cop, BatchCop, or MPP protocol to generate execution plans based on the cost estimation.

### tidb_allow_batch_cop <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `1`
- Range: `[0, 2]`
- This variable is used to control how TiDB sends a coprocessor request to TiFlash. It has the following values:

    * `0`: Never send requests in batches
    * `1`: Aggregation and join requests are sent in batches
    * `2`: All coprocessor requests are sent in batches

### tidb_allow_fallback_to_tikv <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: ""
- This variable is used to specify a list of storage engines that might fall back to TiKV. If the execution of a SQL statement fails due to a failure of the specified storage engine in the list, TiDB retries executing this SQL statement with TiKV. This variable can be set to "" or "tiflash". When this variable is set to "tiflash", if TiFlash returns a timeout error (error code: ErrTiFlashServerTimeout), TiDB retries executing this SQL statement with TiKV.

### tidb_allow_function_for_expression_index <span class="version-mark">New in v5.2.0</span>

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `json_array`, `json_array_append`, `json_array_insert`, `json_contains`, `json_contains_path`, `json_depth`, `json_extract`, `json_insert`, `json_keys`, `json_length`, `json_merge_patch`, `json_merge_preserve`, `json_object`, `json_pretty`, `json_quote`, `json_remove`, `json_replace`, `json_search`, `json_set`, `json_storage_size`, `json_type`, `json_unquote`, `json_valid`, `lower`, `md5`, `reverse`, `tidb_shard`, `upper`, `vitess_hash`
- This variable is used to show the functions that are allowed to be used for creating expression indexes.

### tidb_allow_mpp <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- Controls whether to use the MPP mode of TiFlash to execute queries. The value options are as follows:
    - `0` or `OFF`, which means that the MPP mode will not be used. For v7.3.0 or a later version, if you set the value of this variable to `0` or `OFF`, you also need to enable the [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730) variable. Otherwise, queries might return errors.
    - `1` or `ON`, which means that the optimizer determines whether to use the MPP mode based on the cost estimation (by default).

MPP is a distributed computing framework provided by the TiFlash engine, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. For details about the selection of the MPP mode, refer to [Control whether to select the MPP mode](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode).

### tidb_allow_remove_auto_inc <span class="version-mark">New in v2.1.18 and v3.0.4</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether the `AUTO_INCREMENT` property of a column is allowed to be removed by executing `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` statements. It is not allowed by default.

### tidb_analyze_distsql_scan_concurrency <span class="version-mark">New in v7.6.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `4`
- Range: `[1, 4294967295]`
- This variable is used to set the concurrency of the `scan` operation when executing the `ANALYZE` operation.

### tidb_analyze_partition_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `2`. The default value is `1` for v7.4.0 and earlier versions.
- This variable specifies the concurrency of reading and writing statistics for a partitioned table when TiDB analyzes the partitioned table.

### tidb_analyze_version <span class="version-mark">New in v5.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `2`
- Range: `[1, 2]`
- Controls how TiDB collects statistics.
    - For TiDB Self-Hosted, the default value of this variable changes from `1` to `2` starting from v5.3.0.
    - For TiDB Cloud, the default value of this variable changes from `1` to `2` starting from v6.5.0.
    - If your cluster is upgraded from an earlier version, the default value of `tidb_analyze_version` does not change after the upgrade.
- For detailed introduction about this variable, see [Introduction to Statistics](/statistics.md).

### tidb_analyze_skip_column_types <span class="version-mark">New in v7.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: "json,blob,mediumblob,longblob"
- Possible values: "json,blob,mediumblob,longblob,text,mediumtext,longtext"
- This variable controls which types of columns are skipped for statistics collection when executing the `ANALYZE` command to collect statistics. The variable is only applicable for `tidb_analyze_version = 2`. Even if you specify a column using `ANALYZE TABLE t COLUMNS c1, ... , cn`, no statistics will be collected for the specified column if its type is in `tidb_analyze_skip_column_types`.

```
mysql> SHOW CREATE TABLE t;
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                             |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int(11) DEFAULT NULL,
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

### tidb_auto_analyze_end_time

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Time
- Default value: `23:59 +0000`
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1 AM and 3 AM in UTC time, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_auto_analyze_partition_batch_size <span class="version-mark">New in v6.4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `128`. Before v7.6.0, the default value is `1`.
- Range: `[1, 1024]`
- This variable specifies the number of partitions that TiDB [automatically analyzes](/statistics.md#automatic-update) when analyzing a partitioned table (which means automatically collecting statistics on a partitioned table).
- If the value of this variable is smaller than the number of partitions, TiDB automatically analyzes all partitions of the partitioned table in multiple batches. If the value of this variable is greater than or equal to the number of partitions, TiDB analyzes all partitions of the partitioned table at the same time.
- If the number of partitions of a partitioned table is far greater than this variable value and the auto-analyze takes a long time, you can increase the value of this variable to reduce the time consumption.

### tidb_auto_analyze_ratio

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Float
- Default value: `0.5`
- Range: `(0, 1]`. The range for v8.0.0 and earlier versions is `[0, 18446744073709551615]`.
- This variable is used to set the threshold when TiDB automatically executes [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) in a background thread to update table statistics. For example, a value of 0.5 means that auto-analyze is triggered when greater than 50% of the rows in a table have been modified. Auto-analyze can be restricted to only execute during certain hours of the day by specifying `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`.

> **Note:**
>
> This feature requires the system variable `tidb_enable_auto_analyze` set to `ON`.

### tidb_auto_analyze_start_time

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Time
- Default value: `00:00 +0000`
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1 AM and 3 AM in UTC time, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_auto_build_stats_concurrency <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- Range: `[1, 256]`
- This variable is used to set the concurrency of executing the automatic update of statistics.

### tidb_backoff_lock_fast

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `10`
- Range: `[1, 2147483647]`
- This variable is used to set the `backoff` time when the read request meets a lock.

### tidb_backoff_weight

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `2`
- Range: `[0, 2147483647]`
- This variable is used to increase the weight of the maximum time of TiDB `backoff`, that is, the maximum retry time for sending a retry request when an internal network or other component (TiKV, PD) failure is encountered. This variable can be used to adjust the maximum retry time and the minimum value is 1.

    For example, the base timeout for TiDB to take TSO from PD is 15 seconds. When `tidb_backoff_weight = 2`, the maximum timeout for taking TSO is: *base time \* 2 = 30 seconds*.

    In the case of a poor network environment, appropriately increasing the value of this variable can effectively alleviate error reporting to the application end caused by timeout. If the application end wants to receive the error information more quickly, minimize the value of this variable.

### tidb_batch_commit

> **Warning:**
>
> It is **NOT** recommended to enable this variable.

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- The variable is used to control whether to enable the deprecated batch-commit feature. When this variable is enabled, a transaction might be split into multiple transactions by grouping a few statements and committed non-atomically, which is not recommended.

### tidb_batch_delete

> **Warning:**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [non-transactional DML](/non-transactional-dml.md).

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the batch-delete feature, which is a part of the deprecated batch-dml feature. When this variable is enabled, `DELETE` statements might be split into multiple transactions and committed non-atomically. To make it work, you also need to enable `tidb_enable_batch_dml` and set a positive value for `tidb_dml_batch_size`, which is not recommended.

### tidb_batch_insert

> **Warning:**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [non-transactional DML](/non-transactional-dml.md).

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the batch-insert feature, which is a part of the deprecated batch-dml feature. When this variable is enabled, `INSERT` statements might be split into multiple transactions and committed non-atomically. To make it work, you also need to enable `tidb_enable_batch_dml` and set a positive value for `tidb_dml_batch_size`, which is not recommended.

### tidb_batch_pending_tiflash_count <span class="version-mark">New in v6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `4000`
- Range: `[0, 4294967295]`
- Specifies the maximum number of permitted unavailable tables when you use `ALTER DATABASE SET TIFLASH REPLICA` to add TiFlash replicas. If the number of unavailable tables exceeds this limit, the operation will be stopped or setting TiFlash replicas for the remaining tables will be very slow.

### tidb_broadcast_join_threshold_count <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `10240`
- Range: `[0, 9223372036854775807]`
- Unit: Rows
- If the objects of the join operation belong to a subquery, the optimizer cannot estimate the size of the subquery result set. In this situation, the size is determined by the number of rows in the result set. If the estimated number of rows in the subquery is less than the value of this variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used.
- This variable will not take effect after [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) is enabled.

### tidb_broadcast_join_threshold_size <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `104857600` (100 MiB)
- Range: `[0, 9223372036854775807]`
- Unit: Bytes
- If the table size is less than the value of the variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used.
- This variable will not take effect after [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) is enabled.

### tidb_build_stats_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `2`. The default value is `4` for v7.4.0 and earlier versions.
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of executing the `ANALYZE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_build_sampling_stats_concurrency <span class="version-mark">New in v7.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Unit: Threads
- Default value：`2`
- Range: `[1, 256]`
- This variable is used to set the sampling concurrency in the `ANALYZE` process.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_capture_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the [baseline capturing](/sql-plan-management.md#baseline-capturing) feature. This feature depends on the statement summary, so you need to enable the statement summary before you use baseline capturing.
- After this feature is enabled, the historical SQL statements in the statement summary are traversed periodically, and bindings are automatically created for SQL statements that appear at least twice.

### tidb_cdc_write_source <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION
- Persists to cluster: No
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 15]`
- When this variable is set to a value other than 0, data written in this session is considered to be written by TiCDC. This variable can only be modified by TiCDC. Do not manually modify this variable in any case.

### tidb_check_mb4_value_in_utf8

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to enforce that the `utf8` character set only stores values from the [Basic Multilingual Plane (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane). To store characters outside the BMP, it is recommended to use the `utf8mb4` character set.
- You might need to disable this option when upgrading your cluster from an earlier version of TiDB where the `utf8` checking was more relaxed. For details, see [FAQs After Upgrade](https://docs.pingcap.com/tidb/stable/upgrade-faq).

### tidb_checksum_table_concurrency

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `4`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the scan index concurrency of executing the [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_committer_concurrency <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `128`
- Range: `[1, 10000]`
- The number of goroutines for requests related to executing commit in the commit phase of the single transaction.
- If the transaction to commit is too large, the waiting time for the flow control queue when the transaction is committed might be too long. In this situation, you can increase the configuration value to speed up the commit.
- This setting was previously a `tidb.toml` option (`performance.committer-concurrency`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_config

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- This variable is read-only. It is used to obtain the configuration information of the current TiDB server.

### tidb_constraint_check_in_place

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable only applies to optimistic transactions. For pessimistic transactions, use [`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-new-in-v630) instead.
- When this variable is set to `OFF`, checking for duplicate values in unique indexes is deferred until the transaction commits. This helps improve performance but might be an unexpected behavior for some applications. See [Constraints](/constraints.md#optimistic-transactions) for details.

    - When setting `tidb_constraint_check_in_place` to `OFF` and using optimistic transactions:

        ```sql
        tidb> create table t (i int key);
        tidb> insert into t values (1);
        tidb> begin optimistic;
        tidb> insert into t values (1);
        Query OK, 1 row affected
        tidb> commit; -- Check only when a transaction is committed.
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    - When setting `tidb_constraint_check_in_place` to `ON` and using optimistic transactions:

        ```sql
        tidb> set @@tidb_constraint_check_in_place=ON;
        tidb> begin optimistic;
        tidb> insert into t values (1);
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_constraint_check_in_place_pessimistic <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean

<CustomContent platform="tidb">

- Default value: By default, the [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) configuration item is `true` so the default value of this variable is `ON`. When [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) is set to `false`, the default value of this variable is `OFF`.

</CustomContent>

<CustomContent platform="tidb-cloud">

- Default value: `ON`

</CustomContent>

- This variable only applies to pessimistic transactions. For optimistic transactions, use [`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place) instead.
- When this variable is set to `OFF`, TiDB defers the unique constraint check of a unique index (to the next time when executing a statement that requires a lock to the index or to the time when committing the transaction). This helps improve performance but might be an unexpected behavior for some applications. See [Constraints](/constraints.md#pessimistic-transactions) for details.
- Disabling this variable might cause TiDB to return a `LazyUniquenessCheckFailure` error in pessimistic transactions. When this error occurs, TiDB rolls back the current transaction.
- When this variable is disabled, you cannot use [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md) in pessimistic transactions.
- When this variable is disabled, committing a pessimistic transaction might return a `Write conflict` or `Duplicate entry` error. When such an error occurs, TiDB rolls back the current transaction.

    - When setting `tidb_constraint_check_in_place_pessimistic` to `OFF` and using pessimistic transactions:

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
        tidb> commit; -- Check only when a transaction is committed.
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    - When setting `tidb_constraint_check_in_place_pessimistic` to `ON` and using pessimistic transactions:

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_cost_model_version <span class="version-mark">New in v6.2.0</span>

> **Note:**
>
> - Since TiDB v6.5.0, the newly created cluster uses Cost Model Version 2 by default. If you upgrade from a TiDB version earlier than v6.5.0 to v6.5.0 or later, the `tidb_cost_model_version` value does not change.
> - Switching the version of the cost model might cause changes to query plans.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `2`
- Value options:
    - `1`: enables the Cost Model Version 1, which is used by default in TiDB v6.4.0 and earlier versions.
    - `2`: enables the [Cost Model Version 2](/cost-model.md#cost-model-version-2), which is generally available in TiDB v6.5.0 and is more accurate than the version 1 in internal tests.
- The version of cost model affects the plan decision of optimizer. For more details, see [Cost Model](/cost-model.md).

### tidb_current_ts

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 9223372036854775807]`
- This variable is read-only. It is used to obtain the timestamp of the current transaction.

### tidb_ddl_disk_quota <span class="version-mark">New in v6.3.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `107374182400` (100 GiB)
- Range: `[107374182400, 1125899906842624]` ([100 GiB, 1 PiB])
- Unit: Bytes
- This variable only takes effect when [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630) is enabled. It sets the usage limit of local storage during backfilling when creating an index.

### tidb_ddl_enable_fast_reorg <span class="version-mark">New in v6.3.0</span>

> **Note:**
>
> - If you are using a [TiDB Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated) cluster, to improve the speed for index creation using this variable, make sure that your TiDB cluster is hosted on AWS and your TiDB node size is at least 8 vCPU.
> - For [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters, this variable is read-only.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the acceleration of `ADD INDEX` and `CREATE INDEX` to improve the speed of backfilling for index creation. Setting this variable value to `ON` can bring performance improvement for index creation on tables with a large amount of data.
- Starting from v7.1.0, the index acceleration operation supports checkpoints. Even if the TiDB owner node is restarted or changed due to failures, TiDB can still recover progress from checkpoints that are automatically updated on a regular basis.
- To verify whether a completed `ADD INDEX` operation is accelerated, you can execute the [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs) statement to see whether `ingest` is displayed in the `JOB_TYPE` column.

<CustomContent platform="tidb">

> **Note:**
>
> * Index acceleration requires a [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) that is writable and has enough free space. If the `temp-dir` is unusable, TiDB falls back to non-accelerated index building. It is recommended to put the `temp-dir` on a SSD disk.
>
> * Before you upgrade TiDB to v6.5.0 or later, it is recommended that you check whether the [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) path of TiDB is correctly mounted to an SSD disk. Make sure that the operating system user that runs TiDB has the read and write permissions for this directory. Otherwise, The DDL operations might experience unpredictable issues. This path is a TiDB configuration item, which takes effect after TiDB is restarted. Therefore, setting this configuration item before upgrading can avoid another restart.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Warning:**
>
> Currently, this feature is not fully compatible with [altering multiple columns or indexes in a single `ALTER TABLE` statement](/sql-statements/sql-statement-alter-table.md). When adding a unique index with the index acceleration, you need to avoid altering other columns or indexes in the same statement.

</CustomContent>

### tidb_enable_dist_task <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- This variable is used to control whether to enable the [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md). After the framework is enabled, the DXF tasks such as DDL and import will be distributedly executed and completed by multiple TiDB nodes in the cluster.
- Starting from TiDB v7.1.0, the DXF supports distributedly executing the [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) statement for partitioned tables.
- Starting from TiDB v7.2.0, the DXF supports distributedly executing the [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) statement for import jobs.
- Starting from TiDB v8.1.0, this variable is enabled by default. If you want to upgrade a cluster with the DXF enabled to v8.1.0 or later, disable the DXF (by setting `tidb_enable_dist_task` to `OFF`) before the upgrade, which avoids `ADD INDEX` operations during the upgrade causing data index inconsistency. After the upgrade, you can manually enable the DXF.
- This variable is renamed from `tidb_ddl_distribute_reorg`.

### tidb_cloud_storage_uri <span class="version-mark">New in v7.4.0</span>

> **Note:**
>
> Currently, the [Global Sort](/tidb-global-sort.md) process consumes a large amount of computing and memory resources of TiDB nodes. In scenarios such as adding indexes online while user business applications are running, it is recommended to add new TiDB nodes to the cluster, configure the [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) variable for these nodes, and connect to these nodes to create tasks. In this way, the distributed framework schedules tasks to these nodes, isolating the workload from other TiDB nodes to reduce the impact of executing backend tasks such as `ADD INDEX` and `IMPORT INTO` on user business applications.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `""`
- This variable is used to specify the Amazon S3 cloud storage URI to enable [Global Sort](/tidb-global-sort.md). After enabling the [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md), you can use the Global Sort feature by configuring the URI and pointing it to an appropriate cloud storage path with the necessary permissions to access the storage. For more details, see [Amazon S3 URI format](/external-storage-uri.md#amazon-s3-uri-format).
- The following statements can use the Global Sort feature.
    - The [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) statement.
    - The [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) statement for import jobs.

### tidb_ddl_error_count_limit

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `512`
- Range: `[0, 9223372036854775807]`
- This variable is used to set the number of retries when the DDL operation fails. When the number of retries exceeds the parameter value, the wrong DDL operation is canceled.

### tidb_ddl_flashback_concurrency <span class="version-mark">New in v6.3.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `64`
- Range: `[1, 256]`
- This variable controls the concurrency of [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md).

### tidb_ddl_reorg_batch_size

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `256`
- Range: `[32, 10240]`
- Unit: Rows
- This variable is used to set the batch size during the `re-organize` phase of the DDL operation. For example, when TiDB executes the `ADD INDEX` operation, the index data needs to backfilled by `tidb_ddl_reorg_worker_cnt` (the number) concurrent workers. Each worker backfills the index data in batches.
    - If many updating operations such as `UPDATE` and `REPLACE` exist during the `ADD INDEX` operation, a larger batch size indicates a larger probability of transaction conflicts. In this case, you need to adjust the batch size to a smaller value. The minimum value is 32.
    - If the transaction conflict does not exist, you can set the batch size to a large value (consider the worker count. See [Interaction Test on Online Workloads and `ADD INDEX` Operations](https://docs.pingcap.com/tidb/stable/online-workloads-and-add-index-operations) for reference). This can increase the speed of the backfilling data, but the write pressure on TiKV also becomes higher.

### tidb_ddl_reorg_priority

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `PRIORITY_LOW`
- Value options: `PRIORITY_LOW`, `PRIORITY_NORMAL`, `PRIORITY_HIGH`
- This variable is used to set the priority of executing the `ADD INDEX` operation in the `re-organize` phase.
- You can set the value of this variable to `PRIORITY_LOW`, `PRIORITY_NORMAL` or `PRIORITY_HIGH`.

### tidb_ddl_reorg_worker_cnt

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `4`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the DDL operation in the `re-organize` phase.

### `tidb_enable_fast_create_table` <span class="version-mark">New in v8.0.0</span>

> **Warning:**
>
> This variable is currently an experimental feature and it is not recommended to use in a production environment. This feature might change or be removed without prior notice. If you find a bug, please give feedback by raising an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable [TiDB Accelerated Table Creation](/accelerated-table-creation.md).
- Starting from v8.0.0, TiDB supports accelerating table creation by the [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) statement using `tidb_enable_fast_create_table`.
- This variable is renamed from the variable [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760) that is introduced in v7.6.0. Starting from v8.0.0, `tidb_ddl_version` no longer takes effect.

### tidb_default_string_match_selectivity <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Default value: `0.8`
- Range: `[0, 1]`
- This variable is used to set the default selectivity of `like`, `rlike`, and `regexp` functions in the filter condition when estimating the number of rows. This variable also controls whether to enable TopN to help estimate these functions.
- TiDB tries to estimate `like` in the filter condition using statistics. But when `like` matches a complex string, or when using `rlike` or `regexp`, TiDB often fails to fully use statistics, and the default value `0.8` is set as the selectivity rate instead, resulting in inaccurate estimation.
- This variable is used to change the preceding behavior. If the variable is set to a value other than `0`, the selectivity rate is the specified variable value instead of `0.8`.
- If the variable is set to `0`, TiDB tries to evaluate using TopN in statistics to improve the accuracy and consider the NULL number in statistics when estimating the preceding three functions. The prerequisite is that statistics are collected when [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510) is set to `2`. Such evaluation might slightly affect the performance.
- If the variable is set to a value other than the `0.8`, TiDB adjusts the estimation for `not like`, `not rlike`, and `not regexp` accordingly.

### tidb_disable_txn_auto_retry

> **Warning:**
>
> Starting from v8.0.0, this variable is deprecated, and TiDB no longer supports automatic retries of optimistic transactions. As an alternative, when encountering optimistic transaction conflicts, you can capture the error and retry transactions in your application, or use the [Pessimistic transaction mode](/pessimistic-transaction.md) instead.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to set whether to disable the automatic retry of explicit optimistic transactions. The default value of `ON` means that transactions will not automatically retry in TiDB and `COMMIT` statements might return errors that need to be handled in the application layer.

    Setting the value to `OFF` means that TiDB will automatically retry transactions, resulting in fewer errors from `COMMIT` statements. Be careful when making this change, because it might result in lost updates.

    This variable does not affect automatically committed implicit transactions and internally executed transactions in TiDB. The maximum retry count of these transactions is determined by the value of `tidb_retry_limit`.

    For more details, see [limits of retry](/optimistic-transaction.md#limits-of-retry).

    <CustomContent platform="tidb">

    This variable only applies to optimistic transactions, not to pessimistic transactions. The number of retries for pessimistic transactions is controlled by [`max_retry_count`](/tidb-configuration-file.md#max-retry-count).

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    This variable only applies to optimistic transactions, not to pessimistic transactions. The number of retries for pessimistic transactions is 256.

    </CustomContent>

### tidb_distsql_scan_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `15`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.
- For OLAP scenarios, the maximum value should not exceed the number of CPU cores of all the TiKV nodes.
- If a table has a lot of partitions, you can reduce the variable value appropriately (determined by the size of the data to be scanned and the frequency of the scan) to avoid TiKV becoming out of memory (OOM).

### tidb_dml_batch_size

> **Warning:**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [non-transactional DML](/non-transactional-dml.md).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- Unit: Rows
- When this value is greater than `0`, TiDB will batch commit statements such as `INSERT` into smaller transactions. This reduces memory usage and helps ensure that the `txn-total-size-limit` is not reached by bulk modifications.
- Only the value `0` provides ACID compliance. Setting this to any other value will break the atomicity and isolation guarantees of TiDB.
- To make this variable work, you also need to enable `tidb_enable_batch_dml` and at least one of `tidb_batch_insert` and `tidb_batch_delete`.

> **Note:**
>
> Starting from v7.0.0, `tidb_dml_batch_size` no longer takes effect on the [`LOAD DATA` statement](/sql-statements/sql-statement-load-data.md).

### tidb_dml_type <span class="version-mark">New in v8.0.0</span>

> **Warning:**
>
> The bulk DML execution mode (`tidb_dml_type = "bulk"`) is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues). In the current version, when TiDB performs large transactions using the bulk DML mode, it might affect the memory usage and execution efficiency of TiCDC, TiFlash, and the resolved-ts module of TiKV, and might cause OOM issues. Additionally, BR might be blocked and fail to process when encountering locks. Therefore, it is not recommended to use this mode when these components or features are enabled.

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: String
- Default value: `"standard"`
- Value options: `"standard"`, `"bulk"`
- This variable controls the execution mode of DML statements.
    - `"standard"` indicates the standard DML execution mode, where TiDB transactions are cached in memory before being committed. This mode is suitable for high-concurrency transaction scenarios with potential conflicts and is the default recommended execution mode.
    - `"bulk"` indicates the bulk DML execution mode, which is suitable for scenarios where a large amount of data is written, causing excessive memory usage in TiDB.
        - During the execution of TiDB transactions, the data is not fully cached in the TiDB memory, but is continuously written to TiKV to reduce memory usage and smooth the write pressure.
        - Only `INSERT`, `UPDATE`, `REPLACE`, and `DELETE` statements are affected by the `"bulk"` mode. Due to the pipelined execution in `"bulk"` mode, the usage of `INSERT IGNORE ... ON DUPLICATE UPDATE ...` might result in a `Duplicate entry` error when updates cause conflicts. In contrast, in `"standard"` mode, because the `IGNORE` keyword is set, this error would be ignored and not be returned to the user.
        - `"bulk"` mode is only suitable for scenarios where a large amount of **data is written without conflicts**. This mode is not efficient for handling write conflicts, as write-write conflicts might cause large transactions to fail and be rolled back.
        - `"bulk"` mode only takes effect on statements with auto-commit enabled, and requires the [`pessimistic-auto-commit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#pessimistic-auto-commit-new-in-v600) configuration item to be set to `false`.
        - When using the `"bulk"` mode to execute statements, ensure that the [metadata lock](/metadata-lock.md) remains enabled during the execution process.
        - `"bulk"` mode cannot be used on [temporary tables](/temporary-tables.md) and [cached tables](/cached-tables.md).
        - `"bulk"` mode cannot be used on tables containing foreign keys and tables referenced by foreign keys when the foreign key constraint check is enabled (`foreign_key_checks = ON`).
        - In situations that the environment does not support or is incompatible with the `"bulk"` mode, TiDB falls back to the `"standard"` mode and returns a warning message. To verify if the `"bulk"` mode is used, you can check the `pipelined` field using [`tidb_last_txn_info`](#tidb_last_txn_info-new-in-v409). A `true` value indicates that the `"bulk"` mode is used.
        - When executing large transactions in the `"bulk"` mode, the transaction duration might be long. For transactions in this mode, the maximum TTL of the transaction lock is the greater value between [`max-txn-ttl`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#max-txn-ttl) and 24 hours. Additionally, if the transaction execution time exceeds the value set by [`tidb_gc_max_wait_time`](#tidb_gc_max_wait_time-new-in-v610), the GC might force a rollback of the transaction, leading to its failure.
        - This mode is implemented by the Pipelined DML feature. For detailed design and GitHub issues, see [Pipelined DML](https://github.com/pingcap/tidb/blob/master/docs/design/2024-01-09-pipelined-DML.md) and [#50215](https://github.com/pingcap/tidb/issues/50215).

### tidb_enable_1pc <span class="version-mark">New in v5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to specify whether to enable the one-phase commit feature for transactions that only affect one Region. Compared with the often-used two-phase commit, one-phase commit can greatly reduce the latency of transaction commit and increase the throughput.

> **Note:**
>
> - The default value of `ON` only applies to new clusters. if your cluster was upgraded from an earlier version of TiDB, the value `OFF` will be used instead.
> - If you have enabled TiDB Binlog, enabling this variable cannot improve the performance. To improve the performance, it is recommended to use [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) instead.
> - Enabling this parameter only means that one-phase commit becomes an optional mode of transaction commit. In fact, the most suitable mode of transaction commit is determined by TiDB.

### tidb_enable_analyze_snapshot <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to read historical data or the latest data when performing `ANALYZE`. If this variable is set to `ON`, `ANALYZE` reads the historical data available at the time of `ANALYZE`. If this variable is set to `OFF`, `ANALYZE` reads the latest data.
- Before v5.2, `ANALYZE` reads the latest data. From v5.2 to v6.1, `ANALYZE` reads the historical data available at the time of `ANALYZE`.

> **Warning:**
>
> If `ANALYZE` reads the historical data available at the time of `ANALYZE`, the long duration of `AUTO ANALYZE` might cause the `GC life time is shorter than transaction duration` error because the historical data is garbage-collected.

### tidb_enable_async_commit <span class="version-mark">New in v5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the async commit feature for the second phase of the two-phase transaction commit to perform asynchronously in the background. Enabling this feature can reduce the latency of transaction commit.

> **Note:**
>
> - The default value of `ON` only applies to new clusters. if your cluster was upgraded from an earlier version of TiDB, the value `OFF` will be used instead.
> - If you have enabled TiDB Binlog, enabling this variable cannot improve the performance. To improve the performance, it is recommended to use [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) instead.
> - Enabling this parameter only means that Async Commit becomes an optional mode of transaction commit. In fact, the most suitable mode of transaction commit is determined by TiDB.

### tidb_enable_auto_analyze <span class="version-mark">New in v6.1.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- Determines whether TiDB automatically updates table statistics as a background operation.
- This setting was previously a `tidb.toml` option (`performance.run-auto-analyze`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_enable_auto_analyze_priority_queue <span class="version-mark">New in v8.0.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the priority queue to schedule the tasks of automatically collecting statistics. When this variable is enabled, TiDB prioritizes collecting statistics for tables that are more valuable to collect, such as newly created indexes and partitioned tables with partition changes. Additionally, TiDB prioritizes tables with lower health scores, placing them at the front of the queue.

### tidb_enable_auto_increment_in_generated

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to determine whether to include the `AUTO_INCREMENT` columns when creating a generated column or an expression index.

### tidb_enable_batch_dml

> **Warning:**
>
> This variable is associated with the deprecated batch-dml feature, which might cause data corruption. Therefore, it is not recommended to enable this variable for batch-dml. Instead, use [non-transactional DML](/non-transactional-dml.md).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the deprecated batch-dml feature. When it is enabled, certain statements might be split into multiple transactions, which is non-atomic and should be used with care. When using batch-dml, you must ensure that there are no concurrent operations on the data you are operating on. To make it work, you must also specify a positive value for `tidb_batch_dml_size` and enable at least one of `tidb_batch_insert` and `tidb_batch_delete`.

### tidb_enable_cascades_planner

> **Warning:**
>
> Currently, cascades planner is an experimental feature. It is not recommended that you use it in production environments.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the cascades planner.

### tidb_enable_check_constraint <span class="version-mark">New in v7.2.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the [`CHECK` constraint](/constraints.md#check) feature.

### tidb_enable_chunk_rpc <span class="version-mark">New in v4.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the `Chunk` data encoding format in Coprocessor.

### tidb_enable_clustered_index <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `ON`
- Possible values: `OFF`, `ON`, `INT_ONLY`
- This variable is used to control whether to create the primary key as a [clustered index](/clustered-indexes.md) by default. "By default" here means that the statement does not explicitly specify the keyword `CLUSTERED`/`NONCLUSTERED`. Supported values are `OFF`, `ON`, and `INT_ONLY`:
    - `OFF` indicates that primary keys are created as non-clustered indexes by default.
    - `ON` indicates that primary keys are created as clustered indexes by default.
    - `INT_ONLY` indicates that the behavior is controlled by the configuration item `alter-primary-key`. If `alter-primary-key` is set to `true`, all primary keys are created as non-clustered indexes by default. If it is set to `false`, only the primary keys which consist of an integer column are created as clustered indexes.

### tidb_enable_ddl <span class="version-mark">New in v6.3.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- Possible values: `OFF`, `ON`
- This variable controls whether the corresponding TiDB instance can become a DDL owner or not. If there is only one TiDB instance in the current TiDB cluster, you cannot prevent it from becoming a DDL owner, which means you cannot set it to `OFF`.

### tidb_enable_collect_execution_info

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to record the execution information of each operator in the slow query log and whether to record the [usage statistics of indexes](/information-schema/information-schema-tidb-index-usage.md).

### tidb_enable_column_tracking <span class="version-mark">New in v5.4.0</span>

> **Warning:**
>
> Currently, collecting statistics on `PREDICATE COLUMNS` is an experimental feature. It is not recommended that you use it in production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable TiDB to collect `PREDICATE COLUMNS`. After enabling the collection, if you disable it, the information of previously collected `PREDICATE COLUMNS` is cleared. For details, see [Collect statistics on some columns](/statistics.md#collect-statistics-on-some-columns).

### tidb_enable_enhanced_security

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean

<CustomContent platform="tidb">

- Default value: `OFF`
- This variable indicates whether the TiDB server you are connected to has the Security Enhanced Mode (SEM) enabled. To change its value, you need to modify the value of `enable-sem` in your TiDB server configuration file and restart the TiDB server.

</CustomContent>

<CustomContent platform="tidb-cloud">

- Default value: `ON`
- This variable is read-only. For TiDB Cloud, the Security Enhanced Mode (SEM) is enabled by default.

</CustomContent>

- SEM is inspired by the design of systems such as [Security-Enhanced Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux). It reduces the abilities of users with the MySQL `SUPER` privilege and instead requires `RESTRICTED` fine-grained privileges to be granted as a replacement. These fine-grained privileges include:
    - `RESTRICTED_TABLES_ADMIN`: The ability to write data to system tables in the `mysql` schema and to see sensitive columns on `information_schema` tables.
    - `RESTRICTED_STATUS_ADMIN`: The ability to see sensitive variables in the command `SHOW STATUS`.
    - `RESTRICTED_VARIABLES_ADMIN`: The ability to see and set sensitive variables in `SHOW [GLOBAL] VARIABLES` and `SET`.
    - `RESTRICTED_USER_ADMIN`: The ability to prevent other users from making changes or dropping a user account.

### tidb_enable_exchange_partition

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the [`exchange partitions with tables`](/partitioned-table.md#partition-management) feature. The default value is `ON`, that is, `exchange partitions with tables` is enabled by default.
- This variable is deprecated since v6.3.0. Its value will be fixed to the default value `ON`, that is, `exchange partitions with tables` is enabled by default.

### tidb_enable_extended_stats

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable indicates whether TiDB can collect the extended statistic to guide the optimizer. See [Introduction to Extended Statistics](/extended-statistics.md) for more information.

### tidb_enable_external_ts_read <span class="version-mark">New in v6.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- If this variable is set to `ON`, TiDB reads data with the timestamp specified by [`tidb_external_ts`](#tidb_external_ts-new-in-v640).

### tidb_external_ts <span class="version-mark">New in v6.4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- If [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-new-in-v640) is set to `ON`, TiDB reads data with the timestamp specified by this variable.

### tidb_enable_fast_analyze

> **Warning:**
>
> Starting from v7.5.0, this variable is deprecated.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to enable the statistics `Fast Analyze` feature.
- If the statistics `Fast Analyze` feature is enabled, TiDB randomly samples about 10,000 rows of data as statistics. When the data is distributed unevenly or the data size is small, the statistics accuracy is low. This might lead to a non-optimal execution plan, for example, selecting a wrong index. If the execution time of the regular `Analyze` statement is acceptable, it is recommended to disable the `Fast Analyze` feature.

### tidb_enable_fast_table_check <span class="version-mark">New in v7.2.0</span>

> **Note:**
>
> This variable does not work for [multi-valued indexes](/sql-statements/sql-statement-create-index.md#multi-valued-indexes) and prefix indexes.

- Scope: SESSION | GLOBAL
- Persists to the cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to use a checksum-based approach to quickly check the integrity of data and indexes in a table. The default value `ON` means this feature is enabled by default.
- When this variable is enabled, TiDB can execute the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement in a faster way.

### tidb_enable_foreign_key <span class="version-mark">New in v6.3.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: Before v6.6.0, the default value is `OFF`. Starting from v6.6.0, the default value is `ON`.
- This variable controls whether to enable the `FOREIGN KEY` feature.

### tidb_enable_gc_aware_memory_track

> **Warning:**
>
> This variable is an internal variable for debugging in TiDB. It might be removed in a future release. **Do not** set this variable.

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable GC-Aware memory track.

### tidb_enable_global_index <span class="version-mark">New in v7.6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- Possible values: `OFF`, `ON`
- This variable controls whether to support creating `Global indexes` for partitioned tables. `Global index` is currently in the development stage. **It is not recommended to modify the value of this system variable**.

### tidb_enable_non_prepared_plan_cache

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) feature.
- Enabling this feature might incur additional memory and CPU overhead and might not be suitable for all situations. Please determine whether to enable this feature according to your actual scenario.

### tidb_enable_non_prepared_plan_cache_for_dml <span class="version-mark">New in v7.1.0</span>

> **Warning:**
>
> The non-prepared execution plan cache for DML statements is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`.
- This variable controls whether to enable the [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) feature for DML statements.

### tidb_enable_gogc_tuner <span class="version-mark">New in v6.4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable GOGC Tuner.

### tidb_enable_historical_stats

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable historical statistics. The default value changes from `OFF` to `ON`, which means that historical statistics are enabled by default.

### tidb_enable_historical_stats_for_capture

> **Warning:**
>
> The feature controlled by this variable is not fully functional in the current TiDB version. Do not change the default value.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether the information captured by `PLAN REPLAYER CAPTURE` includes historical statistics by default. The default value `OFF` means that historical statistics are not included by default.

### tidb_enable_index_merge <span class="version-mark">New in v4.0</span>

> **Note:**
>
> - After upgrading a TiDB cluster from versions earlier than v4.0.0 to v5.4.0 or later, this variable is disabled by default to prevent performance regression due to changes of execution plans.
>
> - After upgrading a TiDB cluster from v4.0.0 or later to v5.4.0 or later, this variable remains the setting before the upgrade.
>
> - Since v5.4.0, for a newly deployed TiDB cluster, this variable is enabled by default.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the index merge feature.

### tidb_enable_index_merge_join

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- Specifies whether to enable the `IndexMergeJoin` operator.
- This variable is used only for the internal operation of TiDB. It is **NOT recommended** to adjust it. Otherwise, data correctness might be affected.

### tidb_enable_legacy_instance_scope <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable permits `INSTANCE` scoped variables to be set using the `SET SESSION` as well as `SET GLOBAL` syntax.
- This option is enabled by default for compatibility with earlier versions of TiDB.

### tidb_enable_list_partition <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to set whether to enable the `LIST (COLUMNS) TABLE PARTITION` feature.

### tidb_enable_local_txn

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used for an unreleased feature. **Do not change the variable value**.

### tidb_enable_metadata_lock <span class="version-mark">New in v6.3.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to set whether to enable the [Metadata lock](/metadata-lock.md) feature. Note that when setting this variable, you need to make sure that there are no running DDL statements in the cluster. Otherwise, the data might be incorrect or inconsistent.

### tidb_enable_mutation_checker <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable TiDB mutation checker, which is a tool used to check consistency between data and indexes during the execution of DML statements. If the checker returns an error for a statement, TiDB rolls back the execution of the statement. Enabling this variable causes a slight increase in CPU usage. For more information, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md).
- For new clusters of v6.0.0 or later versions, the default value is `ON`. For existing clusters that upgrade from versions earlier than v6.0.0, the default value is `OFF`.

### tidb_enable_new_cost_interface <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- TiDB v6.2.0 refactors the implementation of previous cost model. This variable controls whether to enable the refactored Cost Model implementation.
- This variable is enabled by default because the refactored Cost Model uses the same cost formula as before, which does not change the plan decision.
- If your cluster is upgraded from v6.1 to v6.2, this variable remains `OFF`, and it is recommended to enable it manually. If your cluster is upgraded from a version earlier than v6.1, this variable sets to `ON` by default.

### tidb_enable_new_only_full_group_by_check <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls the behavior when TiDB performs the `ONLY_FULL_GROUP_BY` check. For detailed information about `ONLY_FULL_GROUP_BY`, see the [MySQL documentation](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by). In v6.1.0, TiDB handles this check more strictly and correctly.
- To avoid potential compatibility issues caused by version upgrades, the default value of this variable is `OFF` in v6.1.0.

### tidb_enable_noop_functions <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `OFF`
- Possible values: `OFF`, `ON`, `WARN`
- By default, TiDB returns an error when you attempt to use the syntax for functionality that is not yet implemented. When the variable value is set to `ON`, TiDB silently ignores such cases of unavailable functionality, which is helpful if you cannot make changes to the SQL code.
- Enabling `noop` functions controls the following behaviors:
    * `LOCK IN SHARE MODE` syntax
    * `SQL_CALC_FOUND_ROWS` syntax
    * `START TRANSACTION READ ONLY` and `SET TRANSACTION READ ONLY` syntax
    * The `tx_read_only`, `transaction_read_only`, `offline_mode`, `super_read_only`, `read_only` and `sql_auto_is_null` system variables
    * `GROUP BY <expr> ASC|DESC` syntax

> **Warning:**
>
> Only the default value of `OFF` can be considered safe. Setting `tidb_enable_noop_functions=1` might lead to unexpected behaviors in your application, because it permits TiDB to ignore certain syntax without providing an error. For example, the syntax `START TRANSACTION READ ONLY` is permitted, but the transaction remains in read-write mode.

### tidb_enable_noop_variables <span class="version-mark">New in v6.2.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- If you set the variable value to `OFF`, TiDB behaves as follows:
    * When you use `SET` to set a `noop` variable, TiDB returns the `"setting *variable_name* has no effect in TiDB"` warning.
    * The result of `SHOW [SESSION | GLOBAL] VARIABLES` does not include `noop` variables.
    * When you use `SELECT` to read a `noop` variable, TiDB returns the `"variable *variable_name* has no effect in TiDB"` warning.
- To check whether a TiDB instance has set and read the `noop` variable, you can use the `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;` statement.

### tidb_enable_null_aware_anti_join <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: Before v7.0.0, the default value is `OFF`. Starting from v7.0.0, the default value is `ON`.
- Type: Boolean
- This variable controls whether TiDB applies Null Aware Hash Join when ANTI JOIN is generated by subqueries led by special set operators `NOT IN` and `!= ALL`.
- When you upgrade from an earlier version to a v7.0.0 or later cluster, the feature is automatically enabled, meaning that this variable is set to `ON`.

### tidb_enable_outer_join_reorder <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- Since v6.1.0, the [Join Reorder](/join-reorder.md) algorithm of TiDB supports Outer Join. This variable controls whether TiDB enables the Join Reorder's support for Outer Join.
- If your cluster is upgraded from an earlier version of TiDB, note the following:

    - If the TiDB version before the upgrade is earlier than v6.1.0, the default value of this variable after the upgrade is `ON`.
    - If the TiDB version before the upgrade is v6.1.0 or later, the default value of the variable after the upgrade follows the value before the upgrade.

### `tidb_enable_inl_join_inner_multi_pattern` <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether Index Join is supported when the inner table has `Selection` or `Projection` operators on it. The default value `OFF` means that Index Join is not supported in this scenario.

### tidb_enable_ordered_result_mode

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- Specifies whether to sort the final output result automatically.
- For example, with this variable enabled, TiDB processes `SELECT a, MAX(b) FROM t GROUP BY a` as `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`.

### tidb_enable_paging <span class="version-mark">New in v5.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- This variable controls whether to use the method of paging to send coprocessor requests. For TiDB versions in [v5.4.0, v6.2.0), this variable only takes effect on the `IndexLookup` operator; for v6.2.0 and later, this variable takes effect globally. Starting from v6.4.0, the default value of this variable is changed from `OFF` to `ON`.
- User scenarios:

    - In all OLTP scenarios, it is recommended to use the method of paging.
    - For read queries that use `IndexLookup` and `Limit` and that `Limit` cannot be pushed down to `IndexScan`, there might be high latency for the read queries and high usage for TiKV `Unified read pool CPU`. In such cases, because the `Limit` operator only requires a small set of data, if you set [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540) to `ON`, TiDB processes less data, which reduces query latency and resource consumption.
    - In scenarios such as data export using [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) and full table scan, enabling paging can effectively reduce the memory consumption of TiDB processes.

> **Note:**
>
> In OLAP scenarios where TiKV is used as the storage engine instead of TiFlash, enabling paging might cause performance regression in some cases. If the regression occurs, consider using this variable to disable paging, or using the [`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-new-in-v620) and [`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-new-in-v630) variables to adjust the range of rows for paging size.

### tidb_enable_parallel_apply <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable concurrency for the `Apply` operator. The number of concurrencies is controlled by the `tidb_executor_concurrency` variable. The `Apply` operator processes correlated subqueries and has no concurrency by default, so the execution speed is slow. Setting this variable value to `1` can increase concurrency and speed up execution. Currently, concurrency for `Apply` is disabled by default.

### tidb_enable_parallel_hashagg_spill <span class="version-mark">New in v8.0.0</span>

> **Warning:**
>
> Currently, the feature controlled by this variable is experimental. It is not recommended that you use it in production environments. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether TiDB supports disk spill for the parallel HashAgg algorithm. When it is `ON`, disk spill can be triggered for the parallel HashAgg algorithm. This variable will be deprecated after this feature is generally available in a future release.

### tidb_enable_pipelined_window_function

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable specifies whether to use the pipeline execution algorithm for window functions.

### tidb_enable_plan_cache_for_param_limit <span class="version-mark">New in v6.6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether Prepared Plan Cache caches execution plans with a variable as the `LIMIT` parameter (`LIMIT ?`). The default value is `ON`, which means Prepared Plan Cache supports caching such execution plans. Note that Prepared Plan Cache does not support caching execution plans with a variable that is greater than 10000.

### tidb_enable_plan_cache_for_subquery <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether Prepared Plan Cache caches queries that contain subqueries.

### tidb_enable_plan_replayer_capture

<CustomContent platform="tidb-cloud">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the `PLAN REPLAYER CAPTURE` feature. The default value `OFF` means to disable the `PLAN REPLAYER CAPTURE` feature.

</CustomContent>

<CustomContent platform="tidb">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the [`PLAN REPLAYER CAPTURE` feature](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans). The default value `ON` means to enable the `PLAN REPLAYER CAPTURE` feature.

</CustomContent>

### tidb_enable_plan_replayer_continuous_capture <span class="version-mark">New in v7.0.0</span>

<CustomContent platform="tidb-cloud">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the `PLAN REPLAYER CONTINUOUS CAPTURE` feature. The default value `OFF` means to disable the feature.

</CustomContent>

<CustomContent platform="tidb">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the [`PLAN REPLAYER CONTINUOUS CAPTURE` feature](/sql-plan-replayer.md#use-plan-replayer-continuous-capture). The default value `OFF` means to disable the feature.

</CustomContent>

### tidb_enable_prepared_plan_cache <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- Determines whether to enable [Prepared Plan Cache](/sql-prepared-plan-cache.md). When it is enabled, the execution plans of `Prepare` and `Execute` are cached so that the subsequent executions skip optimizing the execution plans, which brings performance improvement.
- This setting was previously a `tidb.toml` option (`prepared-plan-cache.enabled`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">New in v6.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- This variable controls whether to count the memory consumed by the execution plans cached in the Prepared Plan Cache. For details, see [Memory management of Prepared Plan Cache](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache).

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">New in v5.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls the behavior of the optimizer on using statistics of a table when the statistics are outdated.

<CustomContent platform="tidb">

- The optimizer determines whether the statistics of a table is outdated in this way: since the last time `ANALYZE` is executed on a table to get the statistics, if 80% of the table rows are modified (the modified row count divided by the total row count), the optimizer determines that the statistics of this table is outdated. You can change this ratio using the [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) configuration.

</CustomContent>

<CustomContent platform="tidb-cloud">

- The optimizer determines whether the statistics of a table is outdated in this way: since the last time `ANALYZE` is executed on a table to get the statistics, if 80% of the table rows are modified (the modified row count divided by the total row count), the optimizer determines that the statistics of this table is outdated.

</CustomContent>

- By default (with the variable value `OFF`), when the statistics of a table is outdated, the optimizer still keeps using the statistics of the table. If you set the variable value to `ON`, the optimizer determines that the statistics of the table is no longer reliable except for the total row count. Then, the optimizer uses the pseudo statistics.
- If the data on a table is frequently modified without executing `ANALYZE` on this table in time, to keep the execution plan stable, it is recommended to set the variable value to `OFF`.

### tidb_enable_rate_limit_action

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the dynamic memory control feature for the operator that reads data. By default, this operator enables the maximum number of threads that [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) allows to read data. When the memory usage of a single SQL statement exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) each time, the operator that reads data stops one thread.

<CustomContent platform="tidb">

- When the operator that reads data has only one thread left and the memory usage of a single SQL statement constantly exceeds [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), this SQL statement triggers other memory control behaviors, such as [spilling data to disk](/system-variables.md#tidb_enable_tmp_storage_on_oom).
- This variable controls memory usage effectively when an SQL statement only reads data. If computing operations (such as join or aggregation operations) are required, memory usage might not be under the control of `tidb_mem_quota_query`, which increases the risk of OOM.

</CustomContent>

<CustomContent platform="tidb-cloud">

- When the operator that reads data has only one thread left and the memory usage of a single SQL statement continues to exceed [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), this SQL statement triggers other memory control behaviors, such as spilling data to disk.

</CustomContent>

### tidb_enable_resource_control <span class="version-mark">New in v6.6.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- Type: Boolean
- This variable is a switch for [the resource control feature](/tidb-resource-control.md). When this variable is set to `ON`, the TiDB cluster can isolate application resources based on resource groups.

### tidb_enable_reuse_chunk <span class="version-mark">New in v6.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- Value options: `OFF`, `ON`
- This variable controls whether TiDB enables chunk objects cache. If the value is `ON`, TiDB prefers to use the cached chunk object and only requests from the system if the requested object is not in the cache. If the value is `OFF`, TiDB requests chunk objects from the system directly.

### tidb_enable_slow_log

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the slow log feature.

### tidb_enable_tmp_storage_on_oom

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- Value options: `OFF`, `ON`
- Controls whether to enable the temporary storage for some operators when a single SQL statement exceeds the memory quota specified by the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query).
- Before v6.3.0, you can enable or disable this feature by using the TiDB configuration item `oom-use-tmp-storage`. After upgrading the cluster to v6.3.0 or a later version, the TiDB cluster will initialize this variable using the value of `oom-use-tmp-storage` automatically. After that, changing the value of `oom-use-tmp-storage` **does not** take effect anymore.

### tidb_enable_stmt_summary <span class="version-mark">New in v3.0.4</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the statement summary feature. If enabled, SQL execution information like time consumption is recorded to the `information_schema.STATEMENTS_SUMMARY` system table to identify and troubleshoot SQL performance issues.

### tidb_enable_strict_double_type_check <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control if tables can be created with invalid definitions of type `DOUBLE`. This setting is intended to provide an upgrade path from earlier versions of TiDB, which were less strict in validating types.
- The default value of `ON` is compatible with MySQL.

For example, the type `DOUBLE(10)` is now considered invalid because the precision of floating point types is not guaranteed. After changing `tidb_enable_strict_double_type_check` to `OFF`, the table is created:

```sql
mysql> CREATE TABLE t1 (id int, c double(10));
ERROR 1149 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use

mysql> SET tidb_enable_strict_double_type_check = 'OFF';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE t1 (id int, c double(10));
Query OK, 0 rows affected (0.09 sec)
```

> **Note:**
>
> This setting only applies to the type `DOUBLE` since MySQL permits precision for `FLOAT` types. This behavior is deprecated starting with MySQL 8.0.17, and it is not recommended to specify precision for either `FLOAT` or `DOUBLE` types.

### tidb_enable_table_partition

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `ON`
- Possible values: `OFF`, `ON`, `AUTO`
- This variable is used to set whether to enable the `TABLE PARTITION` feature:
    - `ON` indicates enabling Range partitioning, Hash partitioning, and Range column partitioning with one single column.
    - `AUTO` functions the same way as `ON` does.
    - `OFF` indicates disabling the `TABLE PARTITION` feature. In this case, the syntax that creates a partition table can be executed, but the table created is not a partitioned one.

### tidb_enable_telemetry <span class="version-mark">New in v4.0.2</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`

<CustomContent platform="tidb">

- This variable is used to dynamically control whether the telemetry collection in TiDB is enabled. In the current version, the telemetry is disabled by default. If the [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) TiDB configuration item is set to `false` on all TiDB instances, the telemetry collection is always disabled and this system variable will not take effect. See [Telemetry](/telemetry.md) for details.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to dynamically control whether the telemetry collection in TiDB is enabled.

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether read operations in SQL statements containing `INSERT`, `DELETE`, and `UPDATE` can be pushed down to TiFlash. For example:

    - `SELECT` queries in `INSERT INTO SELECT` statements (typical usage scenario: [TiFlash query result materialization](/tiflash/tiflash-results-materialization.md))
    - `WHERE` condition filtering in `UPDATE` and `DELETE` statements
- Starting from v7.1.0, this variable is deprecated. When [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50), the optimizer intelligently decides whether to push a query down to TiFlash based on the [SQL mode](/sql-mode.md) and the cost estimates of the TiFlash replica. Note that TiDB allows read operations in SQL statements containing `INSERT`, `DELETE`, and `UPDATE` (such as `INSERT INTO SELECT`) to be pushed down to TiFlash only when the [SQL Mode](/sql-mode.md) of the current session is not strict, which means that the `sql_mode` value does not contain `STRICT_TRANS_TABLES` and `STRICT_ALL_TABLES`.

### tidb_enable_top_sql <span class="version-mark">New in v5.4.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`

<CustomContent platform="tidb">

- This variable is used to control whether to enable the [Top SQL](/dashboard/top-sql.md) feature.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to control whether to enable the [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) feature.

</CustomContent>

### tidb_enable_tso_follower_proxy <span class="version-mark">New in v5.3.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the TSO Follower Proxy feature. When the value is `OFF`, TiDB only gets TSO from the PD leader. When the value is `ON`, TiDB evenly distributes requests for TSO to all PD servers, and PD followers can also handle TSO requests, thereby reducing the CPU pressure on the PD leader.
- Scenarios for enabling TSO Follower Proxy:
    * Due to the high pressure of TSO requests, the CPU of the PD leader reaches a bottleneck, which causes high latency of TSO RPC requests.
    * The TiDB cluster has many TiDB instances, and increasing the value of [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530) cannot alleviate the high latency issue of TSO RPC requests.

> **Note:**
>
> Suppose that the TSO RPC latency increases for reasons other than a CPU usage bottleneck of the PD leader (such as network issues). In this case, enabling the TSO Follower Proxy might increase the execution latency in TiDB and affect the QPS performance of the cluster.

### tidb_enable_unsafe_substitute <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to replace expressions with generated columns in an unsafe way. The default value is `OFF`, which means that unsafe replacement is disabled by default. For more details, see [Generated Columns](/generated-columns.md).

### tidb_enable_vectorized_expression <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable vectorized execution.

### tidb_enable_window_function

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the support for window functions. Note that window functions may use reserved keywords. This might cause SQL statements that could be executed normally cannot be parsed after upgrading TiDB. In this case, you can set `tidb_enable_window_function` to `OFF`.

### `tidb_enable_row_level_checksum` <span class="version-mark">New in v7.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`

<CustomContent platform="tidb">

- This variable is used to control whether to enable the [TiCDC data integrity validation for single-row data](/ticdc/ticdc-integrity-check.md) feature.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to control whether to enable the [TiCDC data integrity validation for single-row data](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check) feature.

</CustomContent>

- You can use the [`TIDB_ROW_CHECKSUM()`](/functions-and-operators/tidb-functions.md#tidb_row_checksum) function to get the checksum value of a row.

### tidb_enforce_mpp <span class="version-mark">New in v5.1</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`

<CustomContent platform="tidb">

- To change this default value, modify the [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) configuration value.

</CustomContent>

- Controls whether to ignore the optimizer's cost estimation and to forcibly use TiFlash's MPP mode for query execution. The value options are as follows:
    - `0` or `OFF`, which means that the MPP mode is not forcibly used (by default).
    - `1` or `ON`, which means that the cost estimation is ignored and the MPP mode is forcibly used. Note that this setting only takes effect when `tidb_allow_mpp=true`.

MPP is a distributed computing framework provided by the TiFlash engine, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. For details about the selection of the MPP mode, refer to [Control whether to select the MPP mode](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode).

### tidb_evolve_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to enable the baseline evolution feature. For detailed introduction or usage , see [Baseline Evolution](/sql-plan-management.md#baseline-evolution).
- To reduce the impact of baseline evolution on the cluster, use the following configurations:
    - Set `tidb_evolve_plan_task_max_time` to limit the maximum execution time of each execution plan. The default value is 600s.
    - Set `tidb_evolve_plan_task_start_time` and `tidb_evolve_plan_task_end_time` to limit the time window. The default values are respectively `00:00 +0000` and `23:59 +0000`.

### tidb_evolve_plan_task_end_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Time
- Default value: `23:59 +0000`
- This variable is used to set the end time of baseline evolution in a day.

### tidb_evolve_plan_task_max_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `600`
- Range: `[-1, 9223372036854775807]`
- Unit: Seconds
- This variable is used to limit the maximum execution time of each execution plan in the baseline evolution feature.

### tidb_evolve_plan_task_start_time <span class="version-mark">New in v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Time
- Default value: `00:00 +0000`
- This variable is used to set the start time of baseline evolution in a day.

### tidb_executor_concurrency <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `5`
- Range: `[1, 256]`
- Unit: Threads

This variable is used to set the concurrency of the following SQL operators (to one value):

- `index lookup`
- `index lookup join`
- `hash join`
- `hash aggregation` (the `partial` and `final` phases)
- `window`
- `projection`

`tidb_executor_concurrency` incorporates the following existing system variables as a whole for easier management:

+ `tidb_index_lookup_concurrency`
+ `tidb_index_lookup_join_concurrency`
+ `tidb_hash_join_concurrency`
+ `tidb_hashagg_partial_concurrency`
+ `tidb_hashagg_final_concurrency`
+ `tidb_projection_concurrency`
+ `tidb_window_concurrency`

Since v5.0, you can still separately modify the system variables listed above (with a deprecation warning returned) and your modification only affects the corresponding single operators. After that, if you use `tidb_executor_concurrency` to modify the operator concurrency, the separately modified operators will not be affected. If you want to use `tidb_executor_concurrency` to modify the concurrency of all operators, you can set the values of all variables listed above to `-1`.

For a system upgraded to v5.0 from an earlier version, if you have not modified any value of the variables listed above (which means that the `tidb_hash_join_concurrency` value is `5` and the values of the rest are `4`), the operator concurrency previously managed by these variables will automatically be managed by `tidb_executor_concurrency`. If you have modified any of these variables, the concurrency of the corresponding operators will still be controlled by the modified variables.

### tidb_expensive_query_time_threshold

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `60`
- Range: `[10, 2147483647]`
- Unit: Seconds
- This variable is used to set the threshold value that determines whether to print expensive query logs. The difference between expensive query logs and slow query logs is:
    - Slow logs are printed after the statement is executed.
    - Expensive query logs print the statements that are being executed, with execution time exceeding the threshold value, and their related information.

### tidb_expensive_txn_time_threshold <span class="version-mark">New in v7.2.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `600`
- Range: `[60, 2147483647]`
- Unit: Seconds
- This variable controls the threshold for logging expensive transactions, which is 600 seconds by default. When the duration of a transaction exceeds the threshold, and the transaction is neither committed nor rolled back, it is considered an expensive transaction and will be logged.

### tidb_force_priority

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `NO_PRIORITY`
- Possible values: `NO_PRIORITY`, `LOW_PRIORITY`, `HIGH_PRIORITY`, `DELAYED`
- This variable is used to change the default priority for statements executed on a TiDB server. A use case is to ensure that a particular user that is performing OLAP queries receives lower priority than users performing OLTP queries.
- The default value `NO_PRIORITY` means that the priority for statements is not forced to change.

> **Note:**
>
> Starting from v6.6.0, TiDB supports [Resource Control](/tidb-resource-control.md). You can use this feature to execute SQL statements with different priorities in different resource groups. By configuring proper quotas and priorities for these resource groups, you can gain better scheduling control for SQL statements with different priorities. When resource control is enabled, statement priority will no longer take effect. It is recommended that you use [Resource Control](/tidb-resource-control.md) to manage resource usage for different SQL statements.

### tidb_gc_concurrency <span class="version-mark">New in v5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- Specifies the number of threads in the [Resolve Locks](/garbage-collection-overview.md#resolve-locks) step of GC. A value of `-1` means that TiDB will automatically decide the number of garbage collection threads to use.

### tidb_gc_enable <span class="version-mark">New in v5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- Enables garbage collection for TiKV. Disabling garbage collection will reduce system performance, as old versions of rows will no longer be purged.

### tidb_gc_life_time <span class="version-mark">New in v5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Duration
- Default value: `10m0s`
- Range: `[10m0s, 8760h0m0s]`
- The time limit during which data is retained for each GC, in the format of Go Duration. When a GC happens, the current time minus this value is the safe point.

> **Note:**
>
> - In scenarios of frequent updates, a large value (days or even months) for `tidb_gc_life_time` may cause potential issues, such as:
>     - Larger storage use
>     - A large amount of history data may affect performance to a certain degree, especially for range queries such as `select count(*) from t`
> - If there is any transaction that has been running longer than `tidb_gc_life_time`, during GC, the data since `start_ts` is retained for this transaction to continue execution. For example, if `tidb_gc_life_time` is configured to 10 minutes, among all transactions being executed, the transaction that starts earliest has been running for 15 minutes, GC will retain data of the recent 15 minutes.

### tidb_gc_max_wait_time <span class="version-mark">New in v6.1.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `86400`
- Range: `[600, 31536000]`
- Unit: Seconds
- This variable is used to set the maximum time that active transactions block the GC safe point. During each time of GC, the safe point does not exceed the start time of the ongoing transactions by default. If the runtime of active transactions does not exceed this variable value, the GC safe point will be blocked until the runtime exceeds this value.

### tidb_gc_run_interval <span class="version-mark">New in v5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Duration
- Default value: `10m0s`
- Range: `[10m0s, 8760h0m0s]`
- Specifies the GC interval, in the format of Go Duration, for example, `"1h30m"`, and `"15m"`

### tidb_gc_scan_lock_mode <span class="version-mark">New in v5.0</span>

> **Warning:**
>
> Currently, Green GC is an experimental feature. It is not recommended that you use it in production environments.

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `LEGACY`
- Possible values: `PHYSICAL`, `LEGACY`
    - `LEGACY`: Uses the old way of scanning, that is, disable Green GC.
    - `PHYSICAL`: Uses the physical scanning method, that is, enable Green GC.

<CustomContent platform="tidb">

- This variable specifies the way of scanning locks in the Resolve Locks step of GC. When the variable value is set to `LEGACY`, TiDB scans locks by Regions. When the value `PHYSICAL` is used, it enables each TiKV node to bypass the Raft layer and directly scan data, which can effectively mitigate the impact of GC wakening up all Regions when the [Hibernate Region](/tikv-configuration-file.md#hibernate-regions) feature is enabled, thus improving the execution speed in the Resolve Locks step.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable specifies the way of scanning locks in the Resolve Locks step of GC. When the variable value is set to `LEGACY`, TiDB scans locks by Regions. When the value `PHYSICAL` is used, it enables each TiKV node to bypass the Raft layer and directly scan data, which can effectively mitigate the impact of GC wakening up all Regions, thus improving the execution speed in the Resolve Locks step.

</CustomContent>

### tidb_general_log

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`

<CustomContent platform="tidb-cloud">

- This variable is used to set whether to record all SQL statements in the log. This feature is disabled by default. If you need to trace all SQL statements when locating issues, enable this feature.

</CustomContent>

<CustomContent platform="tidb">

- This variable is used to set whether to record all SQL statements in the [log](/tidb-configuration-file.md#logfile). This feature is disabled by default. If maintenance personnel needs to trace all SQL statements when locating issues, they can enable this feature.

- To see all records of this feature in the log, you need to set the TiDB configuration item [`log.level`](/tidb-configuration-file.md#level) to `"info"` or `"debug"` and then query the `"GENERAL_LOG"` string. The following information is recorded:
    - `conn`: The ID of the current session.
    - `user`: The current session user.
    - `schemaVersion`: The current schema version.
    - `txnStartTS`: The timestamp at which the current transaction starts.
    - `forUpdateTS`: In the pessimistic transactional mode, `forUpdateTS` is the current timestamp of the SQL statement. When a write conflict occurs in the pessimistic transaction, TiDB retries the SQL statement currently being executed and updates this timestamp. You can configure the number of retries via [`max-retry-count`](/tidb-configuration-file.md#max-retry-count). In the optimistic transactional model, `forUpdateTS` is equivalent to `txnStartTS`.
    - `isReadConsistency`: Indicates whether the current transactional isolation level is Read Committed (RC).
    - `current_db`: The name of the current database.
    - `txn_mode`: The transactional mode. Value options are `OPTIMISTIC` and `PESSIMISTIC`.
    - `sql`: The SQL statement corresponding to the current query.

</CustomContent>

### tidb_non_prepared_plan_cache_size

> **Warning:**
>
> Starting from v7.1.0, this variable is deprecated. Instead, use [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `100`
- Range: `[1, 100000]`
- This variable controls the maximum number of execution plans that can be cached by [Non-prepared plan cache](/sql-non-prepared-plan-cache.md).

### tidb_generate_binary_plan <span class="version-mark">New in v6.2.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to generate binary-encoded execution plans in slow logs and statement summaries.
- When this variable is set to `ON`, you can view visual execution plans in TiDB Dashboard. Note that TiDB Dashboard only provides visual display for execution plans generated after this variable is enabled.
- You can execute the `SELECT tidb_decode_binary_plan('xxx...')` statement to parse the specific plan from a binary plan.

### tidb_gogc_tuner_max_value <span class="version-mark">New in v7.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `500`
- Range: `[10, 2147483647]`
- The variable is used to control the maximum value of GOGC that the GOGC Tuner can adjust.

### tidb_gogc_tuner_min_value <span class="version-mark">New in v7.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `100`
- Range: `[10, 2147483647]`
- The variable is used to control the minimum value of GOGC that the GOGC Tuner can adjust.

### tidb_gogc_tuner_threshold <span class="version-mark">New in v6.4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `0.6`
- Range: `[0, 0.9)`
- This variable specifies the maximum memory threshold for tuning GOGC. When the memory exceeds this threshold, GOGC Tuner stops working.

### tidb_guarantee_linearizability <span class="version-mark">New in v5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls the way commit TS is calculated for async commit. By default (with the `ON` value), the two-phase commit requests a new TS from the PD server and uses the TS to calculate the final commit TS. In this situation, linearizability is guaranteed for all the concurrent transactions.
- If you set this variable to `OFF`, the process of fetching TS from the PD server is skipped, with the cost that only causal consistency is guaranteed but not linearizability. For more details, see the blog post [Async Commit, the Accelerator for Transaction Commit in TiDB 5.0](https://en.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/).
- For scenarios that require only causal consistency, you can set this variable to `OFF` to improve performance.

### tidb_hash_exchange_with_new_collation

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether the MPP hash partition exchange operator is generated in a cluster with new collation enabled. `true` means to generate the operator, and `false` means not to generate it.
- This variable is used for the internal operation of TiDB. It is **NOT recommended** to set this variable.

### tidb_hash_join_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `hash join` algorithm.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_hashagg_final_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `final` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_hashagg_partial_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `partial` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_historical_stats_duration <span class="version-mark">New in v6.6.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Duration
- Default value: `168h`, which means 7 days
- This variable controls the duration that the historical statistics are retained in the storage.

### tidb_idle_transaction_timeout <span class="version-mark">New in v7.6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 31536000]`
- Unit: Seconds
- This variable controls the idle timeout for transactions in a user session. When a user session is in a transactional state and remains idle for a duration exceeding the value of this variable, TiDB will terminate the session. An idle user session means that there are no active requests and the session is waiting for new requests.
- The default value `0` means unlimited.

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to ignore the commands for closing prepared statement cache.
- When this variable is set to `ON`, the `COM_STMT_CLOSE` command of the Binary protocol and the [`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md) statement of the text protocol are ignored. For details, see [Ignore the `COM_STMT_CLOSE` command and the `DEALLOCATE PREPARE` statement](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement).

### tidb_index_join_batch_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `25000`
- Range: `[1, 2147483647]`
- Unit: Rows
- This variable is used to set the batch size of the `index lookup join` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_join_double_read_penalty_cost_rate <span class="version-mark">New in v6.6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Default value: `0`
- Range: `[0, 18446744073709551615]`
- This variable determines whether to apply a penalty cost to the selection of index join, which reduces the likelihood of the optimizer selecting index join, and increases the likelihood of selecting alternative join methods such as hash join and tiflash join.
- When index join is selected, many table lookup requests are triggered, which consumes too many resources. You can use this variable to reduce the likelihood of the optimizer selecting index join.
- This variable takes effect only when the [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620) variable is set to `2`.

### tidb_index_lookup_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_index_lookup_join_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `index lookup join` algorithm.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_index_merge_intersection_concurrency <span class="version-mark">New in v6.5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `-1`
- Range: `[1, 256]`
- This variable sets the maximum concurrency for the intersection operations that index merge performs. It is effective only when TiDB accesses partitioned tables in the dynamic pruning mode. The actual concurrency is the smaller value of `tidb_index_merge_intersection_concurrency` and the number of partitions of the partitioned table.
- The default value `-1` means that the value of `tidb_executor_concurrency` is used.

### tidb_index_lookup_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `20000`
- Range: `[1, 2147483647]`
- Unit: Rows
- This variable is used to set the batch size of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_serial_scan_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `serial scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_init_chunk_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `32`
- Range: `[1, 32]`
- Unit: Rows
- This variable is used to set the number of rows for the initial chunk during the execution process. The number of rows for a chunk directly affects the amount of memory required for a single query. You can roughly estimate the memory needed for a single chunk by considering the total width of all columns in the query and the number of rows for the chunk. Combining this with the concurrency of the executor, you can make a rough estimation of the total memory required for a single query. It is recommended that the total memory for a single chunk does not exceed 16 MiB.

### tidb_isolation_read_engines <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `tikv,tiflash,tidb`
- This variable is used to set the storage engine list that TiDB can use when reading data.

### tidb_last_ddl_info <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- Type: String
- This is a read-only variable. It is internally used in TiDB to get the information of the last DDL operation within the current session.
    - "query": The last DDL query string.
    - "seq_num": The sequence number for each DDL operation. It is used to identify the order of DDL operations.

### tidb_last_query_info <span class="version-mark">New in v4.0.14</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- This is a read-only variable. It is internally used in TiDB to query the transaction information of the last DML statement. The information includes:
    - `txn_scope`: The scope of the transaction, which can be `global` or `local`.
    - `start_ts`: The start timestamp of the transaction.
    - `for_update_ts`: The `for_update_ts` of the previously executed DML statement. This is an internal term of TiDB used for tests. Usually, you can ignore this information.
    - `error`: The error message, if any.
    - `ru_consumption`: Consumed [RU](/tidb-resource-control.md#what-is-request-unit-ru) for executing the statement.

### tidb_last_txn_info <span class="version-mark">New in v4.0.9</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- This variable is used to get the last transaction information within the current session. It is a read-only variable. The transaction information includes:
    - The transaction scope.
    - The start and commit TS.
    - The transaction commit mode, which might be a two-phase, one-phase, or async commit.
    - The information of transaction fallback from async commit or one-phase commit to two-phase commit.
    - The error encountered.

### tidb_last_plan_replayer_token <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- This variable is read-only and is used to obtain the result of the last `PLAN REPLAYER DUMP` execution in the current session.

### tidb_load_based_replica_read_threshold <span class="version-mark">New in v7.0.0</span>

<CustomContent platform="tidb">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `"1s"`
- Range: `[0s, 1h]`
- Type: String
- This variable is used to set the threshold for triggering load-based replica read. When the estimated queue time of the leader node exceeds the threshold, TiDB prioritizes reading data from the follower node. The format is a time duration, such as `"100ms"` or `"1s"`. For more details, see [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots).

</CustomContent>

<CustomContent platform="tidb-cloud">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `"1s"`
- Range: `[0s, 1h]`
- Type: String
- This variable is used to set the threshold for triggering load-based replica read. When the estimated queue time of the leader node exceeds the threshold, TiDB prioritizes reading data from the follower node. The format is a time duration, such as `"100ms"` or `"1s"`. For more details, see [Troubleshoot Hotspot Issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#scatter-read-hotspots).

</CustomContent>

### `tidb_load_binding_timeout` <span class="version-mark">New in v8.0.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `200`
- Range: `(0, 2147483647]`
- Unit: Milliseconds
- This variable is used to control the timeout of loading bindings. If the execution time of loading bindings exceeds this value, the loading will stop.

### `tidb_lock_unchanged_keys` <span class="version-mark">New in v7.1.1 and v7.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to lock specific keys in the following scenarios. When the value is set to `ON`, these keys are locked. When the value is set to `OFF`, these keys are not locked.
    - Duplicate keys in `INSERT IGNORE` and `REPLACE` statements. Before v6.1.6, these keys were not locked. This issue has been fixed in [#42121](https://github.com/pingcap/tidb/issues/42121).
    - Unique keys in `UPDATE` statements when the values of the keys are not changed. Before v6.5.2, these keys were not locked. This issue has been fixed in [#36438](https://github.com/pingcap/tidb/issues/36438).
- To maintain the consistency and rationality of the transaction, it is not recommended to change this value. If upgrading TiDB causes severe performance issues due to these two fixes, and the behavior without locks is acceptable (see the preceding issues), you can set this variable to `OFF`.

### tidb_log_file_max_days <span class="version-mark">New in v5.3.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`

<CustomContent platform="tidb">

- This variable is used to set the maximum days that the log is retained on the current TiDB instance. Its value defaults to the value of the [`max-days`](/tidb-configuration-file.md#max-days) configuration in the configuration file. Changing the variable value only affects the current TiDB instance. After TiDB is restarted, the variable value is reset and the configuration value is not affected.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to set the maximum days that the log is retained on the current TiDB instance.

</CustomContent>

### tidb_low_resolution_tso

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to enable the low-precision TSO feature. After this feature is enabled, TiDB uses the cached timestamp to read data. The cached timestamp is updated every 2 seconds by default. Starting from v8.0.0, you can configure the update interval by [`tidb_low_resolution_tso_update_interval`](#tidb_low_resolution_tso_update_interval-new-in-v800).
- The main applicable scenario is to reduce the overhead of acquiring TSO for small read-only transactions when reading old data is acceptable.

### `tidb_low_resolution_tso_update_interval` <span class="version-mark">New in v8.0.0</span>

- Scope：GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type：Integer
- Default value：`2000`
- Range：`[10, 60000]`
- Unit: Milliseconds
- This variable is used to set the update interval of the cached timestamp used in the low-precision TSO feature, in milliseconds.
- This variable is only available when [`tidb_low_resolution_tso`](#tidb_low_resolution_tso) is enabled.

### tidb_max_auto_analyze_time <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `43200`
- Range: `[0, 2147483647]`
- Unit: Seconds
- This variable is used to specify the maximum execution time of automatic `ANALYZE` tasks. When the execution time of an automatic `ANALYZE` task exceeds the specified time, the task will be terminated. When the value of this variable is `0`, there is no limit to the maximum execution time of automatic `ANALYZE` tasks.

### tidb_max_bytes_before_tiflash_external_group_by <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `-1`
- Range: `[-1, 9223372036854775807]`
- This variable is used to specify the maximum memory usage of the Hash Aggregation operator with `GROUP BY` in TiFlash, in bytes. When the memory usage exceeds the specified value, TiFlash triggers the Hash Aggregation operator to spill to disk. When the value of this variable is `-1`, TiDB does not pass this variable to TiFlash. Only when the value of this variable is greater than or equal to `0`, TiDB passes this variable to TiFlash. When the value of this variable is `0`, it means that the memory usage is unlimited, that is, TiFlash Hash Aggregation operator will not trigger spilling. For details, see [TiFlash Spill to Disk](/tiflash/tiflash-spill-disk.md).

<CustomContent platform="tidb">

> **Note:**
>
> - If a TiDB cluster has multiple TiFlash nodes, aggregation is usually distributedly executed on multiple TiFlash nodes. This variable controls the maximum memory usage of the aggregation operator on a single TiFlash node.
> - When this variable is set to `-1`, TiFlash determines the maximum memory usage of the aggregation operator based on the value of its own configuration item [`max_bytes_before_external_group_by`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - If a TiDB cluster has multiple TiFlash nodes, aggregation is usually distributedly executed on multiple TiFlash nodes. This variable controls the maximum memory usage of the aggregation operator on a single TiFlash node.
> - When this variable is set to `-1`, TiFlash determines the maximum memory usage of the aggregation operator based on the value of its own configuration item `max_bytes_before_external_group_by`.

</CustomContent>

### tidb_max_bytes_before_tiflash_external_join <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `-1`
- Range: `[-1, 9223372036854775807]`
- This variable is used to specify the maximum memory usage of the Hash Join operator with `JOIN` in TiFlash, in bytes. When the memory usage exceeds the specified value, TiFlash triggers the Hash Join operator to spill to disk. When the value of this variable is `-1`, TiDB does not pass this variable to TiFlash. Only when the value of this variable is greater than or equal to `0`, TiDB passes this variable to TiFlash. When the value of this variable is `0`, it means that the memory usage is unlimited, that is, TiFlash Hash Join operator will not trigger spilling. For details, see [TiFlash Spill to Disk](/tiflash/tiflash-spill-disk.md).

<CustomContent platform="tidb">

> **Note:**
>
> - If a TiDB cluster has multiple TiFlash nodes, join is usually distributedly executed on multiple TiFlash nodes. This variable controls the maximum memory usage of the join operator on a single TiFlash node.
> - When this variable is set to `-1`, TiFlash determines the maximum memory usage of the join operator based on the value of its own configuration item [`max_bytes_before_external_join`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - If a TiDB cluster has multiple TiFlash nodes, join is usually distributedly executed on multiple TiFlash nodes. This variable controls the maximum memory usage of the join operator on a single TiFlash node.
> - When this variable is set to `-1`, TiFlash determines the maximum memory usage of the join operator based on the value of its own configuration item `max_bytes_before_external_join`.

</CustomContent>

### tidb_max_bytes_before_tiflash_external_sort <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `-1`
- Range: `[-1, 9223372036854775807]`
- This variable is used to specify the maximum memory usage of the TopN and Sort operators in TiFlash, in bytes. When the memory usage exceeds the specified value, TiFlash triggers the TopN and Sort operators to spill to disk. When the value of this variable is `-1`, TiDB does not pass this variable to TiFlash. Only when the value of this variable is greater than or equal to `0`, TiDB passes this variable to TiFlash. When the value of this variable is `0`, it means that the memory usage is unlimited, that is, TiFlash TopN and Sort operators will not trigger spilling. For details, see [TiFlash Spill to Disk](/tiflash/tiflash-spill-disk.md).

<CustomContent platform="tidb">

> **Note:**
>
> - If a TiDB cluster has multiple TiFlash nodes, TopN and Sort are usually distributedly executed on multiple TiFlash nodes. This variable controls the maximum memory usage of the TopN and Sort operators on a single TiFlash node.
> - When this variable is set to `-1`, TiFlash determines the maximum memory usage of the TopN and Sort operators based on the value of its own configuration item [`max_bytes_before_external_sort`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - If a TiDB cluster has multiple TiFlash nodes, TopN and Sort are usually distributedly executed on multiple TiFlash nodes. This variable controls the maximum memory usage of the TopN and Sort operators on a single TiFlash node.
> - When this variable is set to `-1`, TiFlash determines the maximum memory usage of the TopN and Sort operators based on the value of its own configuration item `max_bytes_before_external_sort`.

</CustomContent>

### tidb_max_chunk_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1024`
- Range: `[32, 2147483647]`
- Unit: Rows
- This variable is used to set the maximum number of rows in a chunk during the execution process. Setting to too large of a value may cause cache locality issues. The recommended value for this variable is no larger than 65536. The number of rows for a chunk directly affects the amount of memory required for a single query. You can roughly estimate the memory needed for a single chunk by considering the total width of all columns in the query and the number of rows for the chunk. Combining this with the concurrency of the executor, you can make a rough estimation of the total memory required for a single query. It is recommended that the total memory for a single chunk does not exceed 16 MiB. When the query involves a large amount of data and a single chunk is insufficient to handle all the data, TiDB processes it multiple times, doubling the chunk size with each processing iteration, starting from [`tidb_init_chunk_size`](#tidb_init_chunk_size) until the chunk size reaches the value of `tidb_max_chunk_size`.

### tidb_max_delta_schema_count <span class="version-mark">New in v2.1.18 and v3.0.5</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1024`
- Range: `[100, 16384]`
- This variable is used to set the maximum number of schema versions (the table IDs modified for corresponding versions) allowed to be cached. The value range is 100 ~ 16384.

### tidb_max_paging_size <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `50000`
- Range: `[1, 9223372036854775807]`
- Unit: Rows
- This variable is used to set the maximum number of rows during the coprocessor paging request process. Setting it to too small a value increases the RPC count between TiDB and TiKV, while setting it to too large a value results in excessive memory usage in some cases, such as loading data and full table scan. The default value of this variable brings better performance in OLTP scenarios than in OLAP scenarios. If the application only uses TiKV as the storage engine, consider increasing the value of this variable when executing OLAP workload queries, which might bring you better performance.

### tidb_max_tiflash_threads <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[-1, 256]`
- Unit: Threads
- This variable is used to set the maximum concurrency for TiFlash to execute a request. The default value is `-1`, indicating that this system variable is invalid and the maximum concurrency depends on the setting of the TiFlash configuration `profiles.default.max_threads`. When the value is `0`, the maximum number of threads is automatically configured by TiFlash.

### tidb_mem_oom_action <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `CANCEL`
- Possible values: `CANCEL`, `LOG`

<CustomContent platform="tidb">

- Specifies what operation TiDB performs when a single SQL statement exceeds the memory quota specified by `tidb_mem_quota_query` and cannot be spilled over to disk. See [TiDB Memory Control](/configure-memory-usage.md) for details.

</CustomContent>

<CustomContent platform="tidb-cloud">

- Specifies what operation TiDB performs when a single SQL statement exceeds the memory quota specified by [`tidb_mem_quota_query`](#tidb_mem_quota_query) and cannot be spilled over to disk.

</CustomContent>

- The default value is `CANCEL`, but in TiDB v4.0.2 and earlier versions, the default value is `LOG`.
- This setting was previously a `tidb.toml` option (`oom-action`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_mem_quota_analyze <span class="version-mark">New in v6.1.0</span>

> **Warning:**
>
> Currently, the `ANALYZE` memory quota is an experimental feature, and the memory statistics might be inaccurate in production environments.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[-1, 9223372036854775807]`
- Unit: Bytes
- This variable controls the maximum memory usage of TiDB updating statistics. Such a memory usage occurs when you manually execute [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) and when TiDB automatically analyzes tasks in the background. When the total memory usage exceeds this threshold, user-executed `ANALYZE` will exit, and an error message is reported that reminds you to try a lower sampling rate or retry later. If the automatic task in the TiDB background exits because the memory threshold is exceeded, and the sampling rate used is higher than the default value, TiDB will retry the update using the default sampling rate. When this variable value is negative or zero, TiDB does not limit the memory usage of both the manual and automatic update tasks.

> **Note:**
>
> `auto_analyze` will be triggered in a TiDB cluster only when `run-auto-analyze` is enabled in the TiDB startup configuration file.

### tidb_mem_quota_apply_cache <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `33554432` (32 MiB)
- Range: `[0, 9223372036854775807]`
- Unit: Bytes
- This variable is used to set the memory usage threshold of the local cache in the `Apply` operator.
- The local cache in the `Apply` operator is used to speed up the computation of the `Apply` operator. You can set the variable to `0` to disable the `Apply` cache feature.

### tidb_mem_quota_binding_cache <span class="version-mark">New in v6.0.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `67108864`
- Range: `[0, 2147483647]`
- Unit: Bytes
- This variable is used to set the threshold of the memory used for caching bindings.
- If a system creates or captures excessive bindings, resulting in overuse of memory space, TiDB returns a warning in the log. In this case, the cache cannot hold all available bindings or determine which bindings to store. For this reason, some queries might miss their bindings. To address this problem, you can increase the value of this variable, which increases the memory used for caching bindings. After modifying this parameter, you need to run `admin reload bindings` to reload bindings and validate the modification.

### tidb_mem_quota_query

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1073741824` (1 GiB)
- Range: `[-1, 9223372036854775807]`
- Unit: Bytes

<CustomContent platform="tidb">

- For versions earlier than TiDB v6.1.0, this is a session scope variable and uses the value of `mem-quota-query` from `tidb.toml` as an initial value. Starting from v6.1.0, `tidb_mem_quota_query` is a `SESSION | GLOBAL` scope variable.
- For versions earlier than TiDB v6.5.0, this variable is used to set the threshold value of memory quota for **a query**. If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation defined by [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610).
- For TiDB v6.5.0 and later versions, this variable is used to set the threshold value of memory quota for **a session**. If the memory quota of a session during execution exceeds the threshold value, TiDB performs the operation defined by [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610). Note that starting from TiDB v6.5.0, the memory usage of a session contains the memory consumed by the transactions in the session. For the control behavior of transaction memory usage in TiDB v6.5.0 and later versions, see [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit).
- When you set the variable value to `0` or `-1`, the memory threshold is positive infinity. When you set a value smaller than 128, the value will be defaulted to `128`.

</CustomContent>

<CustomContent platform="tidb-cloud">

- For versions earlier than TiDB v6.1.0, this is a session scope variable. Starting from v6.1.0, `tidb_mem_quota_query` is a `SESSION | GLOBAL` scope variable.
- For versions earlier than TiDB v6.5.0, this variable is used to set the threshold value of memory quota for **a query**. If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation defined by [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610).
- For TiDB v6.5.0 and later versions, this variable is used to set the threshold value of memory quota for **a session**. If the memory quota of a session during execution exceeds the threshold value, TiDB performs the operation defined by [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610). Note that starting from TiDB v6.5.0, the memory usage of a session contains the memory consumed by the transactions in the session.
- When you set the variable value to `0` or `-1`, the memory threshold is positive infinity. When you set a value smaller than 128, the value will be defaulted to `128`.

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Float
- Default value: `0`
- This variable represents the memory statistics error value allowed in the TiDB memory debug mode.
- This variable is used for the internal testing of TiDB. It is **NOT recommended** to set this variable.

### tidb_memory_debug_mode_min_heap_inuse

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- This variable is used for the internal testing of TiDB. It is **NOT recommended** to set this variable. Enabling this variable will affect the performance of TiDB.
- After configuring this parameter, TiDB will enter the memory debug mode to analyze the accuracy of memory tracking. TiDB will frequently trigger GC during the execution of subsequent SQL statements, and compare the actual memory usage and memory statistics. If the current memory usage is greater than `tidb_memory_debug_mode_min_heap_inuse` and the memory statistics error exceeds `tidb_memory_debug_mode_alarm_ratio`, TiDB will output the relevant memory information to the log and file.

### tidb_memory_usage_alarm_ratio

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Float
- Default value: `0.7`
- Range: `[0.0, 1.0]`

<CustomContent platform="tidb">

- This variable sets the memory usage ratio that triggers the tidb-server memory alarm. By default, TiDB prints an alarm log when TiDB memory usage exceeds 70% of its total memory and any of the [alarm conditions](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage) is met.
- When this variable is configured to `0` or `1`, it means the memory threshold alarm feature is disabled.
- When this variable is configured to a value greater than `0` and less than `1`, it means that the memory threshold alarm feature is enabled.

    - If the value of the system variable [`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640) is `0`, the memory alarm threshold is `tidb_memory-usage-alarm-ratio * system memory size`.
    - If the value of the system variable `tidb_server_memory_limit` is set to greater than 0, the memory alarm threshold is `tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable sets the memory usage ratio that triggers the [tidb-server memory alarm](https://docs.pingcap.com/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage).
- When this variable is configured to `0` or `1`, it means the memory threshold alarm feature is disabled.
- When this variable is configured to a value greater than `0` and less than `1`, it means that the memory threshold alarm feature is enabled.

</CustomContent>

### tidb_memory_usage_alarm_keep_record_num <span class="version-mark">New in v6.4.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `5`
- Range: `[1, 10000]`
- When the tidb-server memory usage exceeds the memory alarm threshold and triggers an alarm, TiDB only retains the status files generated during the recent 5 alarms by default. You can adjust this number with this variable.

### tidb_merge_join_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Range: `[1, 256]`
- Default value: `1`
- This variable sets the concurrency of the `MergeJoin` operator when a query is executed.
- It is **NOT recommended** to set this variable. Modifying the value of this variable might cause data correctness issues.

### tidb_merge_partition_stats_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `1`
- This variable specifies the concurrency of merging statistics for a partitioned table when TiDB analyzes the partitioned table.

### tidb_enable_async_merge_global_stats <span class="version-mark">New in v7.5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`. When you upgrade TiDB from a version earlier than v7.5.0 to v7.5.0 or a later version, the default value is `OFF`.
- This variable is used for TiDB to merge global statistics asynchronously to avoid OOM issues.

### tidb_metric_query_range_duration <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `60`
- Range: `[10, 216000]`
- Unit: Seconds
- This variable is used to set the range duration of the Prometheus statement generated when querying `METRICS_SCHEMA`.

### tidb_metric_query_step <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `60`
- Range: `[10, 216000]`
- Unit: Seconds
- This variable is used to set the step of the Prometheus statement generated when querying `METRICS_SCHEMA`.

### tidb_min_paging_size <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `128`
- Range: `[1, 9223372036854775807]`
- Unit: Rows
- This variable is used to set the minimum number of rows during the coprocessor paging request process. Setting it to a too small value increases the RPC request count between TiDB and TiKV, while setting it to a too large value might cause a performance decrease when executing queries using IndexLookup with Limit. The default value of this variable brings better performance in OLTP scenarios than in OLAP scenarios. If the application only uses TiKV as the storage engine, consider increasing the value of this variable when executing OLAP workload queries, which might bring you better performance.

![Paging size impact on TPCH](/media/paging-size-impact-on-tpch.png)

As shown in this diagram, when [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540) is enabled, the performance of TPCH is affected by the settings of `tidb_min_paging_size` and [`tidb_max_paging_size`](#tidb_max_paging_size-new-in-v630). The vertical axis is the execution time, and it is the smaller the better.

### tidb_mpp_store_fail_ttl

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Duration
- Default value: `60s`
- The newly started TiFlash node does not provide services. To prevent queries from failing, TiDB limits the tidb-server sending queries to the newly started TiFlash node. This variable indicates the time range in which the newly started TiFlash node is not sent requests.

### tidb_multi_statement_mode <span class="version-mark">New in v4.0.11</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `OFF`
- Possible values: `OFF`, `ON`, `WARN`
- This variable controls whether to allow multiple queries to be executed in the same `COM_QUERY` call.
- To reduce the impact of SQL injection attacks, TiDB now prevents multiple queries from being executed in the same `COM_QUERY` call by default. This variable is intended to be used as part of an upgrade path from earlier versions of TiDB. The following behaviors apply:

| Client setting            | `tidb_multi_statement_mode` value | Multiple statements permitted? |
| ------------------------- | --------------------------------- | ------------------------------ |
| Multiple Statements = ON  | OFF                               | Yes                            |
| Multiple Statements = ON  | ON                                | Yes                            |
| Multiple Statements = ON  | WARN                              | Yes                            |
| Multiple Statements = OFF | OFF                               | No                             |
| Multiple Statements = OFF | ON                                | Yes                            |
| Multiple Statements = OFF | WARN                              | Yes (+warning returned)        |

> **Note:**
>
> Only the default value of `OFF` can be considered safe. Setting `tidb_multi_statement_mode=ON` might be required if your application was specifically designed for an earlier version of TiDB. If your application requires multiple statement support, it is recommended to use the setting provided by your client library instead of the `tidb_multi_statement_mode` option. For example:
>
> * [go-sql-driver](https://github.com/go-sql-driver/mysql#multistatements) (`multiStatements`)
> * [Connector/J](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) (`allowMultiQueries`)
> * PHP [mysqli](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) (`mysqli_multi_query`)

### tidb_nontransactional_ignore_error <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable specifies whether to return an error immediately when the error occurs in a non-transactional DML statement.
- When the value is set to `OFF`, the non-transactional DML statement stops immediately at the first error and returns the error. All the following batches are canceled.
- When the value is set to `ON` and an error occurs in a batch, the following batches will continue to be executed until all batches are executed. All errors occurred during the execution process are returned together in the result.

### tidb_opt_agg_push_down

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before Join, Projection, and UnionAll.
- When the aggregate operation is slow in query, you can set the variable value to ON.

### tidb_opt_broadcast_cartesian_join

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `1`
- Range: `[0, 2]`
- Indicates whether to allow the Broadcast Cartesian Join.
- `0` means that the Broadcast Cartesian Join is not allowed. `1` means that it is allowed based on [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50). `2` means that it is always allowed even if the table size exceeds the threshold.
- This variable is internally used in TiDB, and it is **NOT** recommended to modify its value.

### tidb_opt_concurrency_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 18446744073709551615]`
- Default value: `3.0`
- Indicates the CPU cost of starting a Golang goroutine in TiDB. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_copcpu_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 18446744073709551615]`
- Default value: `3.0`
- Indicates the CPU cost for TiKV Coprocessor to process one row. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_correlation_exp_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `1`
- Range: `[0, 2147483647]`
- When the method that estimates the number of rows based on column order correlation is not available, the heuristic estimation method is used. This variable is used to control the behavior of the heuristic method.
    - When the value is 0, the heuristic method is not used.
    - When the value is greater than 0:
        - A larger value indicates that an index scan will probably be used in the heuristic method.
        - A smaller value indicates that a table scan will probably be used in the heuristic method.

### tidb_opt_correlation_threshold

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Default value: `0.9`
- Range: `[0, 1]`
- This variable is used to set the threshold value that determines whether to enable estimating the row count by using column order correlation. If the order correlation between the current column and the `handle` column exceeds the threshold value, this method is enabled.

### tidb_opt_cpu_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `3.0`
- Indicates the CPU cost for TiDB to process one row. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### `tidb_opt_derive_topn` <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- Controls whether to enable the optimization rule of [Deriving TopN or Limit from window functions](/derive-topn-from-window.md).

### tidb_opt_desc_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 18446744073709551615]`
- Default value: `3.0`
- Indicates the cost for TiKV to scan one row from the disk in descending order. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_disk_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 18446744073709551615]`
- Default value: `1.5`
- Indicates the I/O cost for TiDB to read or write one byte of data from or to the temporary disk. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_distinct_agg_push_down

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function with `distinct` (such as `select count(distinct a) from t`) to Coprocessor.
- When the aggregate function with the `distinct` operation is slow in the query, you can set the variable value to `1`.

In the following example, before `tidb_opt_distinct_agg_push_down` is enabled, TiDB needs to read all data from TiKV and execute `distinct` on the TiDB side. After `tidb_opt_distinct_agg_push_down` is enabled, `distinct a` is pushed down to Coprocessor, and a `group by` column `test.t.a` is added to `HashAgg_5`.

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

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether the optimizer estimates the number of rows based on column order correlation

### tidb_opt_enable_hash_join <span class="version-mark">New in v6.5.6, v7.1.2, and v7.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether the optimizer selects hash joins for tables. The value is `ON` by default. If it is set to `OFF`, the optimizer avoids selecting hash joins when generating execution plans, unless no other join algorithm is available.
- If both the system variable `tidb_opt_enable_hash_join` and the `HASH_JOIN` hint are configured, the `HASH_JOIN` hint takes precedence. Even if `tidb_opt_enable_hash_join` is set to `OFF`, when you specify a `HASH_JOIN` hint in a query, the TiDB optimizer still enforces a hash join plan.

### tidb_opt_enable_non_eval_scalar_subquery <span class="version-mark">New in v7.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether the `EXPLAIN` statement disables the execution of constant subqueries that can be expanded at the optimization stage. When this variable is set to `OFF`, the `EXPLAIN` statement expands the subquery in advance at the optimization stage. When this variable is set to `ON`, the `EXPLAIN` statement does not expand the subquery at the optimization stage. For more information, see [Disable subquery expansion](/explain-walkthrough.md#disable-the-early-execution-of-subqueries).

### tidb_opt_enable_late_materialization <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the [TiFlash late materialization](/tiflash/tiflash-late-materialization.md) feature. Note that TiFlash late materialization does not take effect in the [fast scan mode](/tiflash/use-fastscan.md).
- When this variable is set to `OFF` to disable the TiFlash late materialization feature, to process a `SELECT` statement with filter conditions (`WHERE` clause), TiFlash scans all the data of the required columns before filtering. When this variable is set to `ON` to enable the TiFlash late materialization feature, TiFlash can first scan the column data related to the filter conditions that are pushed down to the TableScan operator, filter the rows that meet the conditions, and then scan the data of other columns of these rows for further calculations, thereby reducing IO scans and computations of data processing.

### tidb_opt_enable_mpp_shared_cte_execution <span class="version-mark">New in v7.2.0</span>

> **Warning:**
>
> The feature controlled by this variable is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether the non-recursive [Common Table Expressions (CTE)](/sql-statements/sql-statement-with.md) can be executed on TiFlash MPP. By default, when this variable is disabled, CTE is executed on TiDB, which has a large performance gap compared with enabling this feature.

### tidb_opt_enable_fuzzy_binding <span class="version-mark">New in v7.6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether to enable the [Cross-database binding](/sql-plan-management.md#cross-database-binding) feature.

### tidb_opt_fix_control <span class="version-mark">New in v6.5.3 and v7.1.0</span>

<CustomContent platform="tidb">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: String
- Default value: `""`
- This variable is used to control some internal behaviors of the optimizer.
- The optimizer's behavior might vary depending on user scenarios or SQL statements. This variable provides a more fine-grained control over the optimizer and helps to prevent performance regression after upgrading caused by behavior changes in the optimizer.
- For a more detailed introduction, see [Optimizer Fix Controls](/optimizer-fix-controls.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: String
- Default value: `""`
- This variable is used to control some internal behaviors of the optimizer.
- The optimizer's behavior might vary depending on user scenarios or SQL statements. This variable provides a more fine-grained control over the optimizer and helps to prevent performance regression after upgrading caused by behavior changes in the optimizer.
- For a more detailed introduction, see [Optimizer Fix Controls](https://docs.pingcap.com/tidb/v7.2/optimizer-fix-controls).

</CustomContent>

### tidb_opt_force_inline_cte <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether common table expressions (CTEs) in the entire session are inlined or not. The default value is `OFF`, which means that inlining CTE is not enforced by default. However, you can still inline CTE by specifying the `MERGE()` hint. If the variable is set to `ON`, all CTEs (except recursive CTE) in this session are forced to be inlined.

### tidb_opt_advanced_join_hint <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether the Join Method hint, such as [`HASH_JOIN()` hint](/optimizer-hints.md#hash_joint1_name--tl_name-) and [`MERGE_JOIN()` hint](/optimizer-hints.md#merge_joint1_name--tl_name-), affects the Join Reorder optimization process, including the use of [`LEADING()` hint](/optimizer-hints.md#leadingt1_name--tl_name-). The default value is `ON`, which means that it does not affect. If it is set to `OFF`, there might be conflicts in some scenarios where both Join Method hint and `LEADING()` hint are used at the same time.

> **Note:**
>
> The behavior of versions earlier than v7.0.0 is consistent with that of setting this variable to `OFF`. To ensure forward compatibility, when you upgrade from an earlier version to a v7.0.0 or later cluster, this variable is set to `OFF`. To obtain more flexible hint behavior, it is strongly recommended to switch this variable to `ON` under the condition that there is no performance regression.

### tidb_opt_insubq_to_join_and_agg

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- This variable is used to set whether to enable the optimization rule that converts a subquery to join and aggregation.
- For example, after you enable this optimization rule, the subquery is converted as follows:

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    The subquery is converted to join as follows:

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    If `t1` is limited to be `unique` and `not null` in the `aa` column. You can use the following statement, without aggregation.

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- This variable is used to control the selection of the TiDB Join Reorder algorithm. When the number of nodes participating in Join Reorder is greater than this threshold, TiDB selects the greedy algorithm, and when it is less than this threshold, TiDB selects the dynamic programming algorithm.
- Currently, for OLTP queries, it is recommended to keep the default value. For OLAP queries, it is recommended to set the variable value to 10~15 to get better connection orders in OLAP scenarios.

### tidb_opt_limit_push_down_threshold

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `100`
- Range: `[0, 2147483647]`
- This variable is used to set the threshold that determines whether to push the Limit or TopN operator down to TiKV.
- If the value of the Limit or TopN operator is smaller than or equal to this threshold, these operators are forcibly pushed down to TiKV. This variable resolves the issue that the Limit or TopN operator cannot be pushed down to TiKV partly due to wrong estimation.

### tidb_opt_memory_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `0.001`
- Indicates the memory cost for TiDB to store one row. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">New in v5.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- When the variable value is `ON`, the left join operator always uses inner table as the build side and the right join operator always uses outer table as the build side. If you set the value to `OFF`, the outer join operator can use either side of the tables as the build side.

### tidb_opt_network_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `1.0`
- Indicates the net cost of transferring 1 byte of data through the network. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_objective <span class="version-mark">New in v7.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Enumeration
- Default value: `moderate`
- Possible values: `moderate`, `determinate`
- This variable controls the objective of the optimizer. `moderate` maintains the default behavior in versions prior to TiDB v7.4.0, where the optimizer tries to use more information to generate better execution plans. `determinate` mode tends to be more conservative and makes the execution plan more stable.
- The real-time statistics are the total number of rows and the number of modified rows that are automatically updated based on DML statements. When this variable is set to `moderate` (default), TiDB generates the execution plan based on real-time statistics. When this variable is set to `determinate`, TiDB does not use real-time statistics for generating the execution plan, which will make execution plans more stable.
- For long-term stable OLTP workload, or if the user is affirmative on the existing execution plans, it is recommended to use the `determinate` mode to reduce the possibility of unexpected execution plan changes. Additionally, you can use the [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) to prevent the statistics from being modified and further stabilize the execution plan.

### tidb_opt_ordering_index_selectivity_ratio <span class="version-mark">New in v8.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Default value: `-1`
- Range: `[-1, 1]`
- This variable controls the estimated number of rows for an index that matches the SQL statement `ORDER BY` when there are `ORDER BY` and `LIMIT` clauses in a SQL statement, but does not cover some filter conditions.
- This addresses the same query patterns as the system variable [tidb_opt_ordering_index_selectivity_threshold](#tidb_opt_ordering_index_selectivity_threshold-new-in-v700).
- It differs in implementation by applying a ratio or percentage of the possible range that the qualified rows will be found.
- A value of `-1` (default) or less than `0` disables this ratio. Any value between `0` and `1` applies a ratio of 0% to 100% (for example, `0.5` corresponds to `50%`).
- In the following examples, the table `t` has a total of 1,000,000 rows. The same query is used, but different values for `tidb_opt_ordering_index_selectivity_ratio` are used. The query in the example contains a `WHERE` clause predicate that qualifies a small percentage of rows (9,000 out of 1,000,000). There is an index that supports the `ORDER BY a` (index `ia`), but the filter on `b` is not included in this index. Depending on the actual data distribution, the rows matching the `WHERE` clause and `LIMIT 1` might be found as the first row accessed when scanning the non-filtering index, or at worst, after nearly all the rows have been processed.
- Each example uses an index hint to demonstrate the impact on estRows. The final plan selection depends on the availability and cost of other plans.
- The first example uses the default value `-1`, which uses the existing estimation formula. By default, a small percentage of rows are scanned for estimation before the qualified rows are found.

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

- The second example uses `0`, which assumes that 0% of rows will be scanned before the qualified rows are found. 

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

- The third example uses `0.1`, which assumes that 10% of rows will be scanned before the qualified rows are found. This condition is highly selective, with only 1% of rows meeting the condition. Therefore, in the worst-case scenario, it might be necessary to scan 99% of rows before finding the 1% that qualify. 10% of that 99% is approximately 9.9%, which is reflected in the estRows.

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

- The fourth example uses `1.0`, which assumes that 100% of rows will be scanned before the qualified rows are found.

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

- The fifth example also uses `1.0`, but adds a predicate on `a`, limiting the scan range in the worst-case scenario. This is because `WHERE a <= 9000` matches the index, with approximately 9,000 rows would qualify. Given that the filter predicate on `b` is not in the index, all the approximately 9,000 rows are considered to be scanned before finding a row that matches `b <= 9000`.

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

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Default value: `0`
- Range: `[0, 1]`
- This variable is used to control how the optimizer selects an index when there are `ORDER BY` and `LIMIT` clauses with filter conditions in a SQL statement.
- For such queries, the optimizer considers selecting the corresponding index to satisfy the `ORDER BY` and `LIMIT` clauses (even if this index does not satisfy any filter conditions). However, due to the complexity of data distribution, the optimizer might select a suboptimal index in this scenario.
- This variable represents a threshold. When an index exists that can satisfy filtering conditions and its selectivity estimate is lower than this threshold, the optimizer will avoid selecting an index used to satisfy `ORDER BY` and `LIMIT`. Instead, it prioritizes an index that satisfies the filtering conditions.
- For example, when the variable is set to `0`, the optimizer maintains its default behavior; when it is set to `1`, the optimizer always prioritizes selecting indexes that satisfy the filter conditions and avoids selecting indexes that satisfy both `ORDER BY` and `LIMIT` clauses.
- In the following example, table `t` has a total of 1,000,000 rows. When using an index on column `b`, its estimated row count is approximately 8,748, so its selectivity estimate value is about 0.0087. By default, the optimizer selects an index on column `a`. However, after setting this variable to 0.01, since the selectivity of an index on column `b` (0.0087) is less than 0.01, the optimizer selects an index on column `b`.

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

### tidb_opt_prefer_range_scan <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- After you set the value of this variable to `ON`, the optimizer always prefers range scans over full table scans.
- In the following example, before you enable `tidb_opt_prefer_range_scan`, the TiDB optimizer performs a full table scan. After you enable `tidb_opt_prefer_range_scan`, the optimizer selects an index range scan.

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

### tidb_opt_prefix_index_single_scan <span class="version-mark">New in v6.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `ON`
- This variable controls whether the TiDB optimizer pushes down some filter conditions to the prefix index to avoid unnecessary table lookup and to improve query performance.
- When this variable value is set to `ON`, some filter conditions are pushed down to the prefix index. Suppose that the `col` column is the index prefix column in a table. The `col is null` or `col is not null` condition in the query is handled as a filter condition on the index instead of a filter condition for the table lookup, so that unnecessary table lookup is avoided.

<details>
<summary>Usage example of <code>tidb_opt_prefix_index_single_scan</code></summary>

Create a table with a prefix index:

```sql
CREATE TABLE t (a INT, b VARCHAR(10), c INT, INDEX idx_a_b(a, b(5)));
```

Disable `tidb_opt_prefix_index_single_scan`:

```sql
SET tidb_opt_prefix_index_single_scan = 'OFF';
```

For the following query, the execution plan uses the prefix index `idx_a_b` but requires a table lookup (the `IndexLookUp` operator appears).

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

Enable `tidb_opt_prefix_index_single_scan`:

```sql
SET tidb_opt_prefix_index_single_scan = 'ON';
```

After enabling this variable, for the following query, the execution plan uses the prefix index `idx_a_b` but does not require a table lookup.

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

### tidb_opt_projection_push_down <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- Specifies whether to allow the optimizer to push `Projection` down to the TiKV or TiFlash coprocessor.

### tidb_opt_range_max_size <span class="version-mark">New in v6.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `67108864` (64 MiB)
- Scope: `[0, 9223372036854775807]`
- Unit: Bytes
- This variable is used to set the upper limit of memory usage for the optimizer to build scan ranges. When the variable value is `0`, there is no memory limit for building scan ranges. If building exact scan ranges consumes memory that exceeds the limit, the optimizer uses more relaxed scan ranges (such as `[[NULL,+inf]]`). If the execution plan does not use exact scan ranges, you can increase the value of this variable to let the optimizer build exact scan ranges.

The usage example of this variable is as follows:

<details>
<summary><code>tidb_opt_range_max_size</code> usage examples</summary>

View the default value of this variable. From the result, you can see that the optimizer uses up to 64 MiB of memory to build scan ranges.

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

In the 64 MiB memory upper limit, the optimizer builds the following exact scan ranges `[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`, as shown in the following execution plan result.

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

Now set the upper limit of memory usage for the optimizer to build scan ranges to 1500 bytes.

```sql
SET @@tidb_opt_range_max_size = 1500;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

In the 1500-byte memory limit, the optimizer builds more relaxed scan ranges `[10,10], [20,20], [30,30]`, and uses a warning to inform the user that the memory usage required to build exact scan ranges exceeds the limit of `tidb_opt_range_max_size`.

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

Then set the upper limit of memory usage to 100 bytes:

```sql
set @@tidb_opt_range_max_size = 100;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

In the 100-byte memory limit, the optimizer chooses `IndexFullScan`, and uses a warning to inform the user that the memory required to build exact scan ranges exceeds the limit of `tidb_opt_range_max_size`.

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

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `1.5`
- Indicates the cost for TiKV to scan one row of data from the disk in ascending order. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_seek_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `20`
- Indicates the start-up cost for TiDB to request data from TiKV. This variable is internally used in the [Cost Model](/cost-model.md), and it is **NOT** recommended to modify its value.

### tidb_opt_skew_distinct_agg <span class="version-mark">New in v6.2.0</span>

> **Note:**
>
> The query performance optimization by enabling this variable is effective **only for TiFlash**.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable sets whether the optimizer rewrites the aggregate functions with `DISTINCT` to the two-level aggregate functions, such as rewriting `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b` to `SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`. When the aggregation column has serious skew and the `DISTINCT` column has many different values, this rewriting can avoid the data skew in the query execution and improve the query performance.

### tidb_opt_three_stage_distinct_agg <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `ON`
- This variable specifies whether to rewrite a `COUNT(DISTINCT)` aggregation into a three-stage aggregation in MPP mode.
- This variable currently applies to an aggregation that only contains one `COUNT(DISTINCT)`.

### tidb_opt_tiflash_concurrency_factor

- Scope: SESSION | GLOBAL
- Persists to cluster: YES
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Float
- Range: `[0, 2147483647]`
- Default value: `24.0`
- Indicates the concurrency number of TiFlash computation. This variable is internally used in the Cost Model, and it is NOT recommended to modify its value.

### tidb_opt_use_invisible_indexes <span class="version-mark">New in v8.0.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable controls whether the optimizer can select [invisible indexes](/sql-statements/sql-statement-create-index.md#invisible-index) for query optimization in the current session. Invisible indexes are maintained by DML statements, but will not be used by the query optimizer. This is useful in scenarios where you want to double-check before removing an index permanently. When the variable is set to `ON`, the optimizer can select invisible indexes for query optimization in the session.

### tidb_opt_write_row_id

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to allow `INSERT`, `REPLACE`, and `UPDATE` statements to operate on the `_tidb_rowid` column. This variable can be used only when you import data using TiDB tools.

### tidb_optimizer_selectivity_level

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- This variable controls the iteration of the optimizer's estimation logic. After changing the value of this variable, the estimation logic of the optimizer will change greatly. Currently, `0` is the only valid value. It is not recommended to set it to other values.

### tidb_partition_prune_mode <span class="version-mark">New in v5.1</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Enumeration
- Default value: `dynamic`
- Possible values: `static`, `dynamic`, `static-only`, `dynamic-only`
- Specifies whether to use `dynamic` or `static` mode for partitioned tables. Note that dynamic partitioning is effective only after full table-level statistics, or GlobalStats, are collected. Before GlobalStats are collected, TiDB will use the `static` mode instead. For detailed information about GlobalStats, see [Collect statistics of partitioned tables in dynamic pruning mode](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode). For details about the dynamic pruning mode, see [Dynamic Pruning Mode for Partitioned Tables](/partitioned-table.md#dynamic-pruning-mode).

### tidb_persist_analyze_options <span class="version-mark">New in v5.4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to enable the [ANALYZE configuration persistence](/statistics.md#persist-analyze-configurations) feature.

### tidb_pessimistic_txn_fair_locking <span class="version-mark">New in v7.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- Determines whether to use enhanced pessimistic locking wake-up model for pessimistic transactions. This model strictly controls the wake-up order of pessimistic transactions in the pessimistic locking single-point conflict scenarios to avoid unnecessary wake-ups. It greatly reduces the uncertainty brought by the randomness of the existing wake-up mechanism. If you encounter frequent single-point pessimistic locking conflicts in your business scenario (such as frequent updates to the same row of data), and thus cause frequent statement retries, high tail latency, or even occasional `pessimistic lock retry limit reached` errors, you can try to enable this variable to solve the problem.
- This variable is disabled by default for TiDB clusters that are upgraded from versions earlier than v7.0.0 to v7.0.0 or later versions.

> **Note:**
>
> - Depending on the specific business scenario, enabling this option might cause a certain degree of throughput reduction (average latency increase) for transactions with frequent lock conflicts.
> - This option only takes effect on statements that need to lock a single key. If a statement needs to lock multiple rows at the same time, this option will not take effect on such statements.
> - This feature is introduced in v6.6.0 by the [`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660) variable, which is disabled by default.

### tidb_placement_mode <span class="version-mark">New in v6.0.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `STRICT`
- Possible values: `STRICT`, `IGNORE`
- This variable controls whether DDL statements ignore the [placement rules specified in SQL](/placement-rules-in-sql.md). When the variable value is `IGNORE`, all placement rule options are ignored.
- It is intended to be used by logical dump/restore tools to ensure that tables can always be created even if invalid placement rules are assigned. This is similar to how mysqldump writes `SET FOREIGN_KEY_CHECKS=0;` to the start of every dump file.

### `tidb_plan_cache_invalidation_on_fresh_stats` <span class="version-mark">New in v7.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to invalidate the plan cache automatically when statistics on related tables are updated.
- After enabling this variable, plan cache can make use of statistics more sufficiently to generate execution plans. For example:
    - If execution plans are generated before statistics are available, plan cache re-generates execution plans once the statistics are available.
    - If the data distribution of a table changes, causing the previously optimal execution plan to become non-optimal, plan cache re-generates execution plans after the statistics are re-collected.
- This variable is disabled by default for TiDB clusters that are upgraded from a version earlier than v7.1.0 to v7.1.0 or later.

### `tidb_plan_cache_max_plan_size` <span class="version-mark">New in v7.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `2097152` (which is 2 MiB)
- Range: `[0, 9223372036854775807]`, in bytes. The memory format with the units "KiB|MiB|GiB|TiB" is also supported. `0` means no limit.
- This variable controls the maximum size of a plan that can be cached in prepared or non-prepared plan cache. If the size of a plan exceeds this value, the plan will not be cached. For more details, see [Memory management of prepared plan cache](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache) and [Non-prepared plan cache](/sql-plan-management.md#usage).

### tidb_pprof_sql_cpu <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 1]`
- This variable is used to control whether to mark the corresponding SQL statement in the profile output to identify and troubleshoot performance issues.

### tidb_prefer_broadcast_join_by_exchange_data_size <span class="version-mark">New in v7.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `OFF`
- This variable controls whether to use the algorithm with the minimum overhead of network transmission when TiDB selects the [MPP Hash Join algorithm](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode). If this variable is enabled, TiDB estimates the size of the data to be exchanged in the network using `Broadcast Hash Join` and `Shuffled Hash Join` respectively, and then chooses the one with the smaller size.
- [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) and [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) will not take effect after this variable is enabled.

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Float
- Default value: `0.1`
- Range: `[0, 1]`
- The threshold at which the prepared plan cache triggers a memory protection mechanism. For details, see [Memory management of Prepared Plan Cache](/sql-prepared-plan-cache.md).
- This setting was previously a `tidb.toml` option (`prepared-plan-cache.memory-guard-ratio`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_prepared_plan_cache_size <span class="version-mark">New in v6.1.0</span>

> **Warning:**
>
> Starting from v7.1.0, this variable is deprecated. Instead, use [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `100`
- Range: `[1, 100000]`
- The maximum number of plans that can be cached in a session. For details, see [Memory management of Prepared Plan Cache](/sql-prepared-plan-cache.md).
- This setting was previously a `tidb.toml` option (`prepared-plan-cache.capacity`), but changed to a system variable starting from TiDB v6.1.0.

### tidb_projection_concurrency

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[-1, 256]`
- Unit: Threads
- This variable is used to set the concurrency of the `Projection` operator.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tidb_query_log_max_len

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `4096` (4 KiB)
- Range: `[0, 1073741824]`
- Unit: Bytes
- The maximum length of the SQL statement output. When the output length of a statement is larger than the `tidb_query_log_max_len` value, the statement is truncated to output.
- This setting was previously also available as a `tidb.toml` option (`log.query-log-max-len`), but is only a system variable starting from TiDB v6.1.0.

### tidb_rc_read_check_ts <span class="version-mark">New in v6.0.0</span>

> **Warning:**
>
> - This feature is incompatible with [`replica-read`](#tidb_replica_read-new-in-v40). Do not enable `tidb_rc_read_check_ts` and `replica-read` at the same time.
> - If your client uses a cursor, it is not recommended to enable `tidb_rc_read_check_ts` in case that the previous batch of returned data has already been used by the client and the statement eventually fails.
> - Starting from v7.0.0, this variable is no longer valid for the cursor fetch read mode that uses the prepared statement protocol.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to optimize the timestamp acquisition, which is suitable for scenarios with read-committed isolation level where read-write conflicts are rare. Enabling this variable can avoid the latency and cost of getting the global timestamp, and can optimize the transaction-level read latency.
- If read-write conflicts are severe, enabling this feature will increase the cost and latency of getting the global timestamp, and might cause performance regression. For details, see [Read Committed isolation level](/transaction-isolation-levels.md#read-committed-isolation-level).

### tidb_rc_write_check_ts <span class="version-mark">New in v6.3.0</span>

> **Warning:**
>
> This feature is currently incompatible with [`replica-read`](#tidb_replica_read-new-in-v40). After this variable is enabled, all requests sent by the client cannot use `replica-read`. Therefore, do not enable `tidb_rc_write_check_ts` and `replica-read` at the same time.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to optimize the acquisition of timestamps and is suitable for scenarios with few point-write conflicts in `READ-COMMITTED` isolation level of pessimistic transactions. Enabling this variable can avoid the latency and overhead brought by obtaining the global timestamps during the execution of point-write statements. Currently, this variable is applicable to three types of point-write statements: `UPDATE`, `DELETE`, and `SELECT ...... FOR UPDATE`. A point-write statement refers to a write statement that uses the primary key or unique key as a filter condition and the final execution operator contains `POINT-GET`.
- If the point-write conflicts are severe, enabling this variable will increase extra overhead and latency, resulting in performance regression. For details, see [Read Committed isolation level](/transaction-isolation-levels.md#read-committed-isolation-level).

### tidb_read_consistency <span class="version-mark">New in v5.4.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: String
- Default value: `strict`
- This variable is used to control the read consistency for an auto-commit read statement.
- If the variable value is set to `weak`, the locks encountered by the read statement are skipped directly and the read execution might be faster, which is the weak consistency read mode. However, the transaction semantics (such as atomicity) and distributed consistency (such as linearizability) are not guaranteed.
- For user scenarios where the auto-commit read needs to return fast and weak consistency read results are acceptable, you can use the weak consistency read mode.

### tidb_read_staleness <span class="version-mark">New in v5.4.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `0`
- Range: `[-2147483648, 0]`
- This variable is used to set the time range of historical data that TiDB can read in the current session. After setting the value, TiDB selects a timestamp as new as possible from the range allowed by this variable, and all subsequent read operations are performed against this timestamp. For example, if the value of this variable is set to `-5`, on the condition that TiKV has the corresponding historical version's data, TiDB selects a timestamp as new as possible within a 5-second time range.

### tidb_record_plan_in_slow_log

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to include the execution plan of slow queries in the slow log.

### tidb_redact_log

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `OFF`
- Possible values: `OFF`, `ON`, `MARKER`
- This variable controls whether to hide the user information in the SQL statement being recorded into the TiDB log and slow log.
- The default value is `OFF`, which means that the user information is not processed in any way.
- When you set the variable to `ON`, the user information is hidden. For example, if the executed SQL statement is `INSERT INTO t VALUES (1,2)`, the statement is recorded as `INSERT INTO t VALUES (?,?)` in the log.
- When you set the variable to `MARKER`, the user information is wrapped in `‹ ›`. For example, if the executed SQL statement is `INSERT INTO t VALUES (1,2)`, the statement is recorded as `INSERT INTO t VALUES (‹1›,‹2›)` in the log. If the input has `‹`, it is escaped as `‹‹`, and `›` is escaped as `››`. Based on the marked logs, you can decide whether to desensitize the marked information when the logs are displayed.

### tidb_regard_null_as_point <span class="version-mark">New in v5.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether the optimizer can use a query condition including null equivalence as a prefix condition for index access.
- This variable is enabled by default. When it is enabled, the optimizer can reduce the volume of index data to be accessed, which accelerates query execution. For example, if a query involves multiple-column indexes `index(a, b)` and the query condition contains `a<=>null and b=1`, the optimizer can use both `a<=>null` and `b=1` in the query condition for index access. If the variable is disabled, because `a<=>null and b=1` includes the null equivalence condition, the optimizer does not use `b=1` for index access.

### tidb_remove_orderby_in_subquery <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: Before v7.2.0, the default value is `OFF`. Starting from v7.2.0, the default value is `ON`.
- Specifies whether to remove `ORDER BY` clause in a subquery.

### tidb_replica_read <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Enumeration
- Default value: `leader`
- Possible values: `leader`, `follower`, `leader-and-follower`, `prefer-leader`, `closest-replicas`, `closest-adaptive`, and `learner`. The `learner` value is introduced in v6.6.0.
- This variable is used to control where TiDB reads data.
- For more details about usage and implementation, see [Follower read](/follower-read.md).

### tidb_restricted_read_only <span class="version-mark">New in v5.2.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- `tidb_restricted_read_only` and [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) behave similarly. In most cases, you should use [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) only.
- Users with the `SUPER` or `SYSTEM_VARIABLES_ADMIN` privilege can modify this variable. However, if the [Security Enhanced Mode](#tidb_enable_enhanced_security) is enabled, the additional `RESTRICTED_VARIABLES_ADMIN` privilege is required to read or modify this variable.
- `tidb_restricted_read_only` affects [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) in the following cases:
    - Setting `tidb_restricted_read_only` to `ON` will update [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) to `ON`.
    - Setting `tidb_restricted_read_only` to `OFF` leaves [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) unchanged.
    - If `tidb_restricted_read_only` is `ON`, [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) cannot be set to `OFF`.
- For DBaaS providers of TiDB, if a TiDB cluster is a downstream database of another database, to make the TiDB cluster read-only, you might need to use `tidb_restricted_read_only` with [Security Enhanced Mode](#tidb_enable_enhanced_security) enabled, which prevents your customers from using [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) to make the cluster writable. To achieve this, you need to enable [Security Enhanced Mode](#tidb_enable_enhanced_security), use an admin user with the `SYSTEM_VARIABLES_ADMIN` and `RESTRICTED_VARIABLES_ADMIN` privileges to control `tidb_restricted_read_only`, and let your database users use the root user with the `SUPER` privilege to control [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) only.
- This variable controls the read-only status of the entire cluster. When the variable is `ON`, all TiDB servers in the entire cluster are in the read-only mode. In this case, TiDB only executes the statements that do not modify data, such as `SELECT`, `USE`, and `SHOW`. For other statements such as `INSERT` and `UPDATE`, TiDB rejects executing those statements in the read-only mode.
- Enabling the read-only mode using this variable only ensures that the entire cluster finally enters the read-only status. If you have changed the value of this variable in a TiDB cluster but the change has not yet propagated to other TiDB servers, the un-updated TiDB servers are still **not** in the read-only mode.
- TiDB checks the read-only flag before SQL statements are executed. Since v6.2.0, the flag is also checked before SQL statements are committed. This helps prevent the case where long-running [auto commit](/transaction-overview.md#autocommit) statements might modify data after the server has been placed in read-only mode.
- When this variable is enabled, TiDB handles the uncommitted transactions in the following ways:
    - For uncommitted read-only transactions, you can commit the transactions normally.
    - For uncommitted transactions that are not read-only, SQL statements that perform write operations in these transactions are rejected.
    - For uncommitted read-only transactions with modified data, the commit of these transactions is rejected.
- After the read-only mode is enabled, all users (including the users with the `SUPER` privilege) cannot execute the SQL statements that might write data unless the user is explicitly granted the `RESTRICTED_REPLICA_WRITER_ADMIN` privilege.

### tidb_request_source_type <span class="version-mark">New in v7.4.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: `""`
- Possible values: `"ddl"`, `"stats"`, `"br"`, `"lightning"`, `"background"`
- This variable is used to explicitly specify the task type for the current session, which is identified and controlled by [Resource Control](/tidb-resource-control.md). For example: `SET @@tidb_request_source_type = "background"`.

### tidb_retry_limit

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `10`
- Range: `[-1, 9223372036854775807]`
- This variable is used to set the maximum number of the retries for optimistic transactions. When a transaction encounters retryable errors (such as transaction conflicts, very slow transaction commit, or table schema changes), this transaction is re-executed according to this variable. Note that setting `tidb_retry_limit` to `0` disables the automatic retry. This variable only applies to optimistic transactions, not to pessimistic transactions.

### tidb_row_format_version

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `2`
- Range: `[1, 2]`
- Controls the format version of the newly saved data in the table. In TiDB v4.0, the [new storage row format](https://github.com/pingcap/tidb/blob/master/docs/design/2018-07-19-row-format.md) version `2` is used by default to save new data.
- If you upgrade from a TiDB version earlier than v4.0.0 to v4.0.0 or later versions, the format version is not changed, and TiDB continues to use the old format of version `1` to write data to the table, which means that **only newly created clusters use the new data format by default**.
- Note that modifying this variable does not affect the old data that has been saved, but applies the corresponding version format only to the newly written data after modifying this variable.

### tidb_runtime_filter_mode <span class="version-mark">New in v7.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Enumeration
- Default value: `OFF`
- Possible values: `OFF`, `LOCAL`
- Controls the mode of Runtime Filter, that is, the relationship between the **Filter Sender operator** and **Filter Receiver operator**. There are two modes: `OFF` and `LOCAL`. `OFF` means disabling Runtime Filter. `LOCAL` means enabling Runtime Filter in the local mode. For more information, see [Runtime Filter mode](/runtime-filter.md#runtime-filter-mode).

### tidb_runtime_filter_type <span class="version-mark">New in v7.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Enumeration
- Default value: `IN`
- Possible values: `IN`
- Controls the type of predicate used by the generated Filter operator. Currently, only one type is supported: `IN`. For more information, see [Runtime Filter type](/runtime-filter.md#runtime-filter-type).

### tidb_scatter_region

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- By default, Regions are split for a new table when it is being created in TiDB. After this variable is enabled, the newly split Regions are scattered immediately during the execution of the `CREATE TABLE` statement. This applies to the scenario where data need to be written in batches right after the tables are created in batches, because the newly split Regions can be scattered in TiKV beforehand and do not have to wait to be scheduled by PD. To ensure the continuous stability of writing data in batches, the `CREATE TABLE` statement returns success only after the Regions are successfully scattered. This makes the statement's execution time multiple times longer than that when you disable this variable.
- Note that if `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` have been set when a table is created, the specified number of Regions are evenly split after the table creation.

### tidb_schema_cache_size <span class="version-mark">New in v8.0.0</span>

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 9223372036854775807]`
- This variable controls the size of the schema cache in TiDB. The unit is byte. The default value is `0`, which means that the cache limit feature is not enabled. When this feature is enabled, TiDB uses the value you set as the maximum available memory limit, and uses the Least Recently Used (LRU) algorithm to cache the required tables, effectively reducing the memory occupied by the schema information.

### tidb_schema_version_cache_limit <span class="version-mark">New in v7.4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `16`
- Range: `[2, 255]`
- This variable limits how many historical schema versions can be cached in a TiDB instance. The default value is `16`, which means that TiDB caches 16 historical schema versions by default.
- Generally, you do not need to modify this variable. When the [Stale Read](/stale-read.md) feature is used and DDL operations are executed very frequently, it will cause the schema version to change very frequently. Consequently, when Stale Read tries to obtain schema information from a snapshot, it might take a lot of time to rebuild the information due to schema cache misses. In this case, you can increase the value of `tidb_schema_version_cache_limit` (for example, `32`) to avoid the problem of schema cache misses.
- Modifying this variable causes the memory usage of TiDB to increase slightly. Monitor the memory usage of TiDB to avoid OOM problems.

### tidb_server_memory_limit <span class="version-mark">New in v6.4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `80%`
- Range:
    - You can set the value in the percentage format, which means the percentage of the memory usage relative to the total memory. The value range is `[1%, 99%]`.
    - You can also set the value in memory size. The value range is `0` and `[536870912, 9223372036854775807]` in bytes. The memory format with the units "KiB|MiB|GiB|TiB" is supported. `0` means no memory limit.
    - If this variable is set to a memory size that is less than 512 MiB but not `0`, TiDB uses 512 MiB as the actual size.
- This variable specifies the memory limit for a TiDB instance. When the memory usage of TiDB reaches the limit, TiDB cancels the currently running SQL statement with the highest memory usage. After the SQL statement is successfully canceled, TiDB tries to call Golang GC to immediately reclaim memory to relieve memory stress as soon as possible.
- Only the SQL statements with more memory usage than the [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640) limit are selected as the SQL statements to be canceled first.
- Currently, TiDB cancels only one SQL statement at a time. After TiDB completely cancels a SQL statement and recovers resources, if the memory usage is still greater than the limit set by this variable, TiDB starts the next cancel operation.

### tidb_server_memory_limit_gc_trigger <span class="version-mark">New in v6.4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `70%`
- Range: `[50%, 99%]`
- The threshold at which TiDB tries to trigger GC. When the memory usage of TiDB reaches the value of `tidb_server_memory_limit` \* the value of `tidb_server_memory_limit_gc_trigger`, TiDB will actively trigger a Golang GC operation. Only one GC operation will be triggered in one minute.

### tidb_server_memory_limit_sess_min_size <span class="version-mark">New in v6.4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `134217728` (which is 128 MiB)
- Range: `[128, 9223372036854775807]`, in bytes. The memory format with the units "KiB|MiB|GiB|TiB" is also supported.
- After you enable the memory limit, TiDB will terminate the SQL statement with the highest memory usage on the current instance. This variable specifies the minimum memory usage of the SQL statement to be terminated. If the memory usage of a TiDB instance that exceeds the limit is caused by too many sessions with low memory usage, you can properly lower the value of this variable to allow more sessions to be canceled.

### tidb_service_scope <span class="version-mark">New in v7.4.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: ""
- Optional value: a string with a length of up to 64 characters. Valid characters include digits `0-9`, letters `a-zA-Z`, underscores `_`, and hyphens `-`.
- This variable is an instance-level system variable. You can use it to control the service scope of each TiDB node under the [TiDB Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md). The DXF determines which TiDB nodes can be scheduled to execute distributed tasks based on the value of this variable. For specific rules, see [Task scheduling](/tidb-distributed-execution-framework.md#task-scheduling).

### tidb_session_alias <span class="version-mark">New in v7.4.0</span>

- Scope: SESSION
- Persists to cluster: No
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: ""
- You can use this variable to customize the value of the `session_alias` column in the logs related to the current session, which helps identify the session in troubleshooting. This setting affects the logs of multiple nodes involved in the statement execution (including TiKV). The maximum length of this variable is limited to 64 characters, and any characters exceeding the length will be truncated automatically. Spaces at the end of the value will also be removed automatically.

### tidb_session_plan_cache_size <span class="version-mark">New in v7.1.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `100`
- Range: `[1, 100000]`
- This variable controls the maximum number of plans that can be cached. [Prepared plan cache](/sql-prepared-plan-cache.md) and [non-prepared plan cache](/sql-non-prepared-plan-cache.md) share the same cache.
- When you upgrade from an earlier version to a v7.1.0 or later version, this variable remains the same value as [`tidb_prepared_plan_cache_size`](#tidb_prepared_plan_cache_size-new-in-v610)

### tidb_shard_allocate_step <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `9223372036854775807`
- Range: `[1, 9223372036854775807]`
- This variable controls the maximum number of continuous IDs to be allocated for the [`AUTO_RANDOM`](/auto-random.md) or [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) attribute. Generally, `AUTO_RANDOM` IDs or the `SHARD_ROW_ID_BITS` annotated row IDs are incremental and continuous in one transaction. You can use this variable to solve the hotspot issue in large transaction scenarios.

### tidb_simplified_metrics

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- When this variable is enabled, TiDB does not collect or record the metrics that are not used in the Grafana panels.

### tidb_skip_ascii_check <span class="version-mark">New in v5.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to skip ASCII validation.
- Validating ASCII characters affects the performance. When you are sure that the input characters are valid ASCII characters, you can set the variable value to `ON`.

### tidb_skip_isolation_level_check

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- After this switch is enabled, if an isolation level unsupported by TiDB is assigned to `tx_isolation`, no error is reported. This helps improve compatibility with applications that set (but do not depend on) a different isolation level.

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_missing_partition_stats <span class="version-mark">New in v7.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- When accessing a partitioned table in [dynamic pruning mode](/partitioned-table.md#dynamic-pruning-mode), TiDB aggregates the statistics of each partition to generate GlobalStats. This variable controls the generation of GlobalStats when partition statistics are missing.

    - If this variable is `ON`, TiDB skips missing partition statistics when generating GlobalStats so the generation of GlobalStats is not affected.
    - If this variable is `OFF`, TiDB stops generating GlobalStats when it detects any missing partition statistics.

### tidb_skip_utf8_check

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to set whether to skip UTF-8 validation.
- Validating UTF-8 characters affects the performance. When you are sure that the input characters are valid UTF-8 characters, you can set the variable value to `ON`.

> **Note:**
>
> If the character check is skipped, TiDB might fail to detect illegal UTF-8 characters written by the application, cause decoding errors when `ANALYZE` is executed, and introduce other unknown encoding issues. If your application cannot guarantee the validity of the written string, it is not recommended to skip the character check.

### tidb_slow_log_threshold

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: No, only applicable to the current TiDB instance that you are connecting to.
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `300`
- Range: `[-1, 9223372036854775807]`
- Unit: Milliseconds
- This variable is used to output the threshold value of the time consumed by the slow log. When the time consumed by a query is larger than this value, this query is considered as a slow log and its log is output to the slow query log.

### tidb_slow_query_file

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- When `INFORMATION_SCHEMA.SLOW_QUERY` is queried, only the slow query log name set by `slow-query-file` in the configuration file is parsed. The default slow query log name is "tidb-slow.log". To parse other logs, set the `tidb_slow_query_file` session variable to a specific file path, and then query `INFORMATION_SCHEMA.SLOW_QUERY` to parse the slow query log based on the set file path.

<CustomContent platform="tidb">

For details, see [Identify Slow Queries](/identify-slow-queries.md).

</CustomContent>

### tidb_snapshot

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- This variable is used to set the time point at which the data is read by the session. For example, when you set the variable to "2017-11-11 20:20:20" or a TSO number like "400036290571534337", the current session reads the data of this moment.

### tidb_source_id <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- Range: `[1, 15]`

<CustomContent platform="tidb">

- This variable is used to configure the different cluster IDs in a [bi-directional replication](/ticdc/ticdc-bidirectional-replication.md) cluster.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to configure the different cluster IDs in a [bi-directional replication](https://docs.pingcap.com/tidb/stable/ticdc-bidirectional-replication) cluster.

</CustomContent>

### tidb_stats_cache_mem_quota <span class="version-mark">New in v6.1.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Unit: Byte
- Default value: `0`, which means that the memory quota is automatically set to half of the total memory size of the TiDB instance.
- Range: `[0, 1099511627776]`
- This variable sets the memory quota for the TiDB statistics cache.

### tidb_stats_load_pseudo_timeout <span class="version-mark">New in v5.4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls how TiDB behaves when the waiting time of SQL optimization reaches the timeout to synchronously load complete column statistics. The default value `ON` means that the SQL optimization gets back to using pseudo statistics after the timeout. If this variable to `OFF`, SQL execution fails after the timeout.

### tidb_stats_load_sync_wait <span class="version-mark">New in v5.4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `100`
- Range: `[0, 2147483647]`
- Unit: Milliseconds
- This variable controls whether to enable the synchronously loading statistics feature. The value `0` means that the feature is disabled. To enable the feature, you can set this variable to a timeout (in milliseconds) that SQL optimization can wait for at most to synchronously load complete column statistics. For details, see [Load statistics](/statistics.md#load-statistics).

### tidb_stmt_summary_enable_persistent <span class="version-mark">New in v6.6.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is read-only. It controls whether to enable [statements summary persistence](/statement-summary-tables.md#persist-statements-summary).

<CustomContent platform="tidb">

- The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660).

</CustomContent>

### tidb_stmt_summary_filename <span class="version-mark">New in v6.6.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: String
- Default value: `"tidb-statements.log"`
- This variable is read-only. It specifies the file to which persistent data is written when [statements summary persistence](/statement-summary-tables.md#persist-statements-summary) is enabled.

<CustomContent platform="tidb">

- The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660).

</CustomContent>

### tidb_stmt_summary_file_max_backups <span class="version-mark">New in v6.6.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- This variable is read-only. It specifies the maximum number of data files that can be persisted when [statements summary persistence](/statement-summary-tables.md#persist-statements-summary) is enabled.

<CustomContent platform="tidb">

- The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660).

</CustomContent>

### tidb_stmt_summary_file_max_days <span class="version-mark">New in v6.6.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `3`
- Unit: day
- This variable is read-only. It specifies the maximum number of days to keep persistent data files when [statements summary persistence](/statement-summary-tables.md#persist-statements-summary) is enabled.

<CustomContent platform="tidb">

- The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660).

</CustomContent>

### tidb_stmt_summary_file_max_size <span class="version-mark">New in v6.6.0</span>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

</CustomContent>

> **Warning:**
>
> Statements summary persistence is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

- Scope: GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `64`
- Unit: MiB
- This variable is read-only. It specifies the maximum size of a persistent data file when [statements summary persistence](/statement-summary-tables.md#persist-statements-summary) is enabled.

<CustomContent platform="tidb">

- The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660).

</CustomContent>

### tidb_stmt_summary_history_size <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `24`
- Range: `[0, 255]`
- This variable is used to set the history capacity of [statement summary tables](/statement-summary-tables.md).

### tidb_stmt_summary_internal_query <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether to include the SQL information of TiDB in [statement summary tables](/statement-summary-tables.md).

### tidb_stmt_summary_max_sql_length <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `4096`
- Range: `[0, 2147483647]`
- Unit: Bytes

<CustomContent platform="tidb">

- This variable is used to control the length of the SQL string in [statement summary tables](/statement-summary-tables.md) and the [TiDB Dashboard](/dashboard/dashboard-intro.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to control the length of the SQL string in [statement summary tables](/statement-summary-tables.md).

</CustomContent>

### tidb_stmt_summary_max_stmt_count <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `3000`
- Range: `[1, 32767]`
- This variable is used to set the maximum number of statements that [statement summary tables](/statement-summary-tables.md) store in memory.

### tidb_stmt_summary_refresh_interval <span class="version-mark">New in v4.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1800`
- Range: `[1, 2147483647]`
- Unit: Seconds
- This variable is used to set the refresh time of [statement summary tables](/statement-summary-tables.md).

### tidb_store_batch_size

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `4`
- Range: `[0, 25000]`
- This variable is used to control the batch size of the Coprocessor Tasks of the `IndexLookUp` operator. `0` means to disable batch. When the number of tasks is relatively large and slow queries occur, you can increase this variable to optimize the query.

### tidb_store_limit <span class="version-mark">New in v3.0.4 and v4.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 9223372036854775807]`
- This variable is used to limit the maximum number of requests TiDB can send to TiKV at the same time. 0 means no limit.

### tidb_streamagg_concurrency

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- This variable sets the concurrency of the `StreamAgg` operator when queries are executed.
- It is **NOT recommended** to set this variable. Modifying the variable value might cause data correctness issues.

### tidb_super_read_only <span class="version-mark">New in v5.3.1</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- `tidb_super_read_only` aims to be implemented as a replacement of the MySQL variable `super_read_only`. However, because TiDB is a distributed database, `tidb_super_read_only` does not make the database read-only immediately after execution, but eventually.
- Users with the `SUPER` or `SYSTEM_VARIABLES_ADMIN` privilege can modify this variable.
- This variable controls the read-only status of the entire cluster. When the variable is `ON`, all TiDB servers in the entire cluster are in the read-only mode. In this case, TiDB only executes the statements that do not modify data, such as `SELECT`, `USE`, and `SHOW`. For other statements such as `INSERT` and `UPDATE`, TiDB rejects executing those statements in the read-only mode.
- Enabling the read-only mode using this variable only ensures that the entire cluster finally enters the read-only status. If you have changed the value of this variable in a TiDB cluster but the change has not yet propagated to other TiDB servers, the un-updated TiDB servers are still **not** in the read-only mode.
- TiDB checks the read-only flag before SQL statements are executed. Since v6.2.0, the flag is also checked before SQL statements are committed. This helps prevent the case where long-running [auto commit](/transaction-overview.md#autocommit) statements might modify data after the server has been placed in read-only mode.
- When this variable is enabled, TiDB handles the uncommitted transactions in the following ways:
    - For uncommitted read-only transactions, you can commit the transactions normally.
    - For uncommitted transactions that are not read-only, SQL statements that perform write operations in these transactions are rejected.
    - For uncommitted read-only transactions with modified data, the commit of these transactions is rejected.
- After the read-only mode is enabled, all users (including the users with the `SUPER` privilege) cannot execute the SQL statements that might write data unless the user is explicitly granted the `RESTRICTED_REPLICA_WRITER_ADMIN` privilege.
- When the [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520) system variable is set to `ON`, `tidb_super_read_only` is affected by [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520) in some cases. For detailed impact, see the description of [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520).

### tidb_sysdate_is_now <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `OFF`
- This variable is used to control whether the `SYSDATE` function can be replaced by the `NOW` function. This configuration item has the same effect as the MySQL option [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now).

### tidb_sysproc_scan_concurrency <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- Range: `[1, 4294967295]`. The maximum value for v7.5.0 and earlier versions is `256`.
- This variable is used to set the concurrency of scan operations performed when TiDB executes internal SQL statements (such as an automatic update of statistics).

### tidb_table_cache_lease <span class="version-mark">New in v6.0.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `3`
- Range: `[1, 10]`
- Unit: Seconds
- This variable is used to control the lease time of [cached tables](/cached-tables.md) with a default value of `3`. The value of this variable affects the modification to cached tables. After a modification is made to cached tables, the longest waiting time might be `tidb_table_cache_lease` seconds. If the table is read-only or can accept a high write latency, you can increase the value of this variable to increase the valid time for caching tables and to reduce the frequency of lease renewal.

### tidb_tmp_table_max_size <span class="version-mark">New in v5.3.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `67108864`
- Range: `[1048576, 137438953472]`
- Unit: Bytes
- This variable is used to set the maximum size of a single [temporary table](/temporary-tables.md). Any temporary table with a size larger than this variable value causes error.

### tidb_top_sql_max_meta_count <span class="version-mark">New in v6.0.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `5000`
- Range: `[1, 10000]`

<CustomContent platform="tidb">

- This variable is used to control the maximum number of SQL statement types collected by [Top SQL](/dashboard/top-sql.md) per minute.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to control the maximum number of SQL statement types collected by [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) per minute.

</CustomContent>

### tidb_top_sql_max_time_series_count <span class="version-mark">New in v6.0.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

> **Note:**
>
> Currently, the Top SQL page in TiDB Dashboard only displays the top 5 types of SQL queries that contribute the most to the load, which is irrelevant with the configuration of `tidb_top_sql_max_time_series_count`.

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `100`
- Range: `[1, 5000]`

<CustomContent platform="tidb">

- This variable is used to control how many SQL statements that contribute the most to the load (that is, top N) can be recorded by [Top SQL](/dashboard/top-sql.md) per minute.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to control how many SQL statements that contribute the most to the load (that is, top N) can be recorded by [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) per minute.

</CustomContent>

### tidb_track_aggregate_memory_usage

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether TiDB tracks the memory usage of aggregate functions.

> **Warning:**
>
> If you disable this variable, TiDB might not accurately track the memory usage and cannot control the memory usage of the corresponding SQL statements.

### tidb_tso_client_batch_max_wait_time <span class="version-mark">New in v5.3.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Float
- Default value: `0`
- Range: `[0, 10]`
- Unit: Milliseconds
- This variable is used to set the maximum waiting time for a batch operation when TiDB requests TSO from PD. The default value is `0`, which means no extra waiting time.
- When obtaining TSO requests from PD each time, PD Client, used by TiDB, collects as many TSO requests received at the same time as possible. Then, PD Client merges the collected requests in batch into one RPC request and sends the request to PD. This helps reduce the pressure on PD.
- After setting this variable to a value greater than `0`, TiDB waits for the maximum duration of this value before the end of each batch merge. This is to collect more TSO requests and improve the effect of batch operations.
- Scenarios for increasing the value of this variable:
    * Due to the high pressure of TSO requests, the CPU of the PD leader reaches a bottleneck, which causes high latency of TSO RPC requests.
    * There are not many TiDB instances in the cluster, but every TiDB instance is in high concurrency.
- It is recommended to set this variable to a value as small as possible.

> **Note:**
>
> Suppose that the TSO RPC latency increases for reasons other than a CPU usage bottleneck of the PD leader (such as network issues). In this case, increasing the value of `tidb_tso_client_batch_max_wait_time` might increase the execution latency in TiDB and affect the QPS performance of the cluster.

### tidb_ttl_delete_rate_limit <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `0`
- Range: `[0, 9223372036854775807]`
- This variable is used to limit the rate of `DELETE` statements in TTL jobs on each TiDB node. The value represents the maximum number of `DELETE` statements allowed per second in a single node in a TTL job. When this variable is set to `0`, no limit is applied. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_ttl_delete_batch_size <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `100`
- Range: `[1, 10240]`
- This variable is used to set the maximum number of rows that can be deleted in a single `DELETE` transaction in a TTL job. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_ttl_delete_worker_count <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `4`
- Range: `[1, 256]`
- This variable is used to set the maximum concurrency of TTL jobs on each TiDB node. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_ttl_job_enable <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- Type: Boolean
- This variable is used to control whether TTL jobs are enabled. If it is set to `OFF`, all tables with TTL attributes automatically stop cleaning up expired data. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_ttl_scan_batch_size <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `500`
- Range: `[1, 10240]`
- This variable is used to set the `LIMIT` value of each `SELECT` statement used to scan expired data in a TTL job. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_ttl_scan_worker_count <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `4`
- Range: `[1, 256]`
- This variable is used to set the maximum concurrency of TTL scan jobs on each TiDB node. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_ttl_job_schedule_window_start_time <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Time
- Persists to cluster: Yes
- Default value: `00:00 +0000`
- This variable is used to control the start time of the scheduling window of TTL jobs in the background. When you modify the value of this variable, be cautious that a small window might cause the cleanup of expired data to fail. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_ttl_job_schedule_window_end_time <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Time
- Persists to cluster: Yes
- Default value: `23:59 +0000`
- This variable is used to control the end time of the scheduling window of TTL jobs in the background. When you modify the value of this variable, be cautious that a small window might cause the cleanup of expired data to fail. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_ttl_running_tasks <span class="version-mark">New in v7.0.0</span>

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `-1` and `[1, 256]`
- Specifies the maximum number of running TTL tasks in the entire cluster. `-1` means the number of TTL tasks is equivalent to the number of TiKV nodes. For more information, refer to [Time to Live](/time-to-live.md).

### tidb_txn_assertion_level <span class="version-mark">New in v6.0.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `FAST`
- Possible values: `OFF`, `FAST`, `STRICT`
- This variable is used to control the assertion level. Assertion is a consistency check between data and indexes, which checks whether a key being written exists in the transaction commit process. For more information, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md).

    - `OFF`: Disable this check.
    - `FAST`: Enable most of the check items, with almost no impact on performance.
    - `STRICT`: Enable all check items, with a minor impact on pessimistic transaction performance when the system workload is high.

- For new clusters of v6.0.0 or later versions, the default value is `FAST`. For existing clusters that upgrade from versions earlier than v6.0.0, the default value is `OFF`.

### tidb_txn_commit_batch_size <span class="version-mark">New in v6.2.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `16384`
- Range: `[1, 1073741824]`
- Unit: Bytes

<CustomContent platform="tidb">

- This variable is used to control the batch size of transaction commit requests that TiDB sends to TiKV. If most of the transactions in the application workload have a large number of write operations, adjusting this variable to a larger value can improve the performance of batch processing. However, if this variable is set to too large a value and exceeds the limit of TiKV's [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size), the commits might fail.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to control the batch size of transaction commit requests that TiDB sends to TiKV. If most of the transactions in the application workload have a large number of write operations, adjusting this variable to a larger value can improve the performance of batch processing. However, if this variable is set to too large a value and exceeds the limit of TiKV's maximum size of a single log (which is 8 MiB by default), the commits might fail.

</CustomContent>

### tidb_txn_entry_size_limit <span class="version-mark">New in v7.6.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 125829120]`
- Unit: Bytes

<CustomContent platform="tidb">

- This variable is used to dynamically modify the TiDB configuration item [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50). It limits the size of a single row of data in TiDB, which is equivalent to the configuration item. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, `txn-entry-size-limit` is also set to the same value.

</CustomContent>

<CustomContent platform="tidb-cloud">

- This variable is used to dynamically modify the TiDB configuration item [`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50). It limits the size of a single row of data in TiDB, which is equivalent to the configuration item. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, `txn-entry-size-limit` is also set to the same value.

</CustomContent>

> **Note:**
>
> Modifying this variable with the SESSION scope only affects the current user session, not the internal TiDB session. This might lead to transaction failure if the entry size of an internal TiDB transaction exceeds the limit of the configuration item. Therefore, to dynamically increase the limit, it is recommended that you modify the variable with the GLOBAL scope.

### tidb_txn_mode

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `pessimistic`
- Possible values: `pessimistic`, `optimistic`
- This variable is used to set the transaction mode. TiDB 3.0 supports the pessimistic transactions. Since TiDB 3.0.8, the [pessimistic transaction mode](/pessimistic-transaction.md) is enabled by default.
- If you upgrade TiDB from v3.0.7 or earlier versions to v3.0.8 or later versions, the default transaction mode does not change. **Only the newly created clusters use the pessimistic transaction mode by default**.
- If this variable is set to "optimistic" or "", TiDB uses the [optimistic transaction mode](/optimistic-transaction.md).

### tidb_use_plan_baselines <span class="version-mark">New in v4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable is used to control whether to enable the execution plan binding feature. It is enabled by default, and can be disabled by assigning the `OFF` value. For the use of the execution plan binding, see [Execution Plan Binding](/sql-plan-management.md#create-a-binding).

### tidb_wait_split_region_finish

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- It usually takes a long time to scatter Regions, which is determined by PD scheduling and TiKV loads. This variable is used to set whether to return the result to the client after all Regions are scattered completely when the `SPLIT REGION` statement is being executed:
    - `ON` requires that the `SPLIT REGIONS` statement waits until all Regions are scattered.
    - `OFF` permits the `SPLIT REGIONS` statement to return before finishing scattering all Regions.
- Note that when scattering Regions, the write and read performances for the Region that is being scattered might be affected. In batch-write or data importing scenarios, it is recommended to import data after Regions scattering is finished.

### tidb_wait_split_region_timeout

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `300`
- Range: `[1, 2147483647]`
- Unit: Seconds
- This variable is used to set the timeout for executing the `SPLIT REGION` statement. If a statement is not executed completely within the specified time value, a timeout error is returned.

### tidb_window_concurrency <span class="version-mark">New in v4.0</span>

> **Warning:**
>
> Since v5.0, this variable is deprecated. Instead, use [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) for setting.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `-1`
- Range: `[1, 256]`
- Unit: Threads
- This variable is used to set the concurrency degree of the window operator.
- A value of `-1` means that the value of `tidb_executor_concurrency` will be used instead.

### tiflash_fastscan <span class="version-mark">New in v6.3.0</span>

- Scope: SESSION | GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `OFF`
- Type: Boolean
- If [FastScan](/tiflash/use-fastscan.md) is enabled (set to `ON`), TiFlash provides more efficient query performance, but does not guarantee the accuracy of the query results or data consistency.

### tiflash_fine_grained_shuffle_batch_size <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `8192`
- Range: `[1, 18446744073709551615]`
- When Fine Grained Shuffle is enabled, the window function pushed down to TiFlash can be executed in parallel. This variable controls the batch size of the data sent by the sender.
- Impact on performance: set a reasonable size according to your business requirements. Improper setting affects the performance. If the value is set too small, for example `1`, it causes one network transfer per Block. If the value is set too large, for example, the total number of rows of the table, it causes the receiving end to spend most of the time waiting for data, and the piplelined computation cannot work. To set a proper value, you can observe the distribution of the number of rows received by the TiFlash receiver. If most threads receive only a few rows, for example a few hundred, you can increase this value to reduce the network overhead.

### tiflash_fine_grained_shuffle_stream_count <span class="version-mark">New in v6.2.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Integer
- Default value: `0`
- Range: `[-1, 1024]`
- When the window function is pushed down to TiFlash for execution, you can use this variable to control the concurrency level of the window function execution. The possible values are as follows:

    * -1: the Fine Grained Shuffle feature is disabled. The window function pushed down to TiFlash is executed in a single thread.
    * 0: the Fine Grained Shuffle feature is enabled. If [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610) is set to a valid value (greater than 0), then `tiflash_fine_grained_shuffle_stream_count` is set to the value of [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610). Otherwise, it is automatically estimated based on the CPU resources of the TiFlash compute node. The actual concurrency level of the window function on TiFlash is: min(`tiflash_fine_grained_shuffle_stream_count`, the number of physical threads on TiFlash nodes).
    * Integer greater than 0: the Fine Grained Shuffle feature is enabled. The window function pushed down to TiFlash is executed in multiple threads. The concurrency level is: min(`tiflash_fine_grained_shuffle_stream_count`, the number of physical threads on TiFlash nodes).
- Theoretically, the performance of the window function increases linearly with this value. However, if the value exceeds the actual number of physical threads, it instead leads to performance degradation.

### tiflash_mem_quota_query_per_node <span class="version-mark">New in v7.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[-1, 9223372036854775807]`
- This variable limits the maximum memory usage for a query on a TiFlash node. When the memory usage of a query exceeds this limit, TiFlash returns an error and terminates the query. Setting this variable to `-1` or `0` means no limit. When this variable is set to a value greater than `0` and [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) is set to a valid value, TiFlash enables [query-level spilling](/tiflash/tiflash-spill-disk.md#query-level-spilling).

### tiflash_query_spill_ratio <span class="version-mark">New in v7.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Float
- Default value: `0.7`
- Range: `[0, 0.85]`
- This variable controls the threshold for TiFlash [query-level spilling](/tiflash/tiflash-spill-disk.md#query-level-spilling). `0` means disabling the automatic query-level spilling. When this variable is greater than `0` and the memory usage of a query exceeds [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) * `tiflash_query_spill_ratio`, TiFlash triggers query-level spilling, which spills data of supported operators in the query as needed.

> **Note:**
>
> - This variable only takes effect when [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) is greater than `0`. In other words, if [tiflash_mem_quota_query_per_node](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) is `0` or `-1`, query-level spilling will not be enabled even if `tiflash_query_spill_ratio` is greater than `0`.
> - When TiFlash query-level spilling is enabled, the spilling thresholds for individual TiFlash operators automatically become invalidated. In other words, if both [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) and `tiflash_query_spill_ratio` are greater than 0, the three variables [tidb_max_bytes_before_tiflash_external_sort](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700), [tidb_max_bytes_before_tiflash_external_group_by](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700), and [tidb_max_bytes_before_tiflash_external_join](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700) become invalidated automatically, equivalent to setting them to `0`.

### tiflash_replica_read <span class="version-mark">New in v7.3.0</span>

> **Note:**
>
> This TiDB variable is not applicable to TiDB Cloud.

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `all_replicas`
- Value options: `all_replicas`, `closest_adaptive`, or `closest_replicas`
- This variable is used to set the strategy for selecting TiFlash replicas when a query requires the TiFlash engine.
    - `all_replicas` means using all available TiFlash replicas for analytical computing.
    - `closest_adaptive` means preferring to use TiFlash replicas in the same zone as the TiDB node initiating the query. If replicas in this zone do not contain all the required data, the query will involve TiFlash replicas from other zones along with their corresponding TiFlash nodes.
    - `closest_replicas` means using only TiFlash replicas in the same zone as the TiDB node initiating the query. If replicas in this zone do not contain all the required data, the query will return an error.

<CustomContent platform="tidb">

> **Note:**
>
> - If TiDB nodes do not have [zone attributes](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb) configured and `tiflash_replica_read` is not set to `all_replicas`, TiFlash ignores the replica selection strategy. Instead, it uses all TiFlash replicas for queries and returns the `The variable tiflash_replica_read is ignored.` warning.
> - If TiFlash nodes do not have [zone attributes](/schedule-replicas-by-topology-labels.md#configure-labels-for-tikv-and-tiflash) configured, they are treated as nodes not belonging to any zone.

</CustomContent>

### tikv_client_read_timeout <span class="version-mark">New in v7.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `0`
- Range: `[0, 2147483647]`
- Unit: Millisecond
- You can use `tikv_client_read_timeout` to set the timeout for TiDB to send a TiKV RPC read request in a query. When a TiDB cluster is in an environment with unstable network or serious TiKV I/O latency jitter, and your application is sensitive to the latency of the SQL queries, you can set `tikv_client_read_timeout` to reduce the timeout of the TiKV RPC read requests. In this case, when a TiKV node has I/O latency jitter, TiDB can time out quickly and re-send the RPC request to the TiKV node where the next TiKV Region Peer is located. If the requests of all TiKV Region Peers time out, TiDB will retry with the default timeout (usually 40 seconds).
- You can also use the optimizer hint `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */` in a query to set the timeout for TiDB to send a TiKV RPC read request. If both the optimizer hint and this system variable are set, the optimizer hint takes higher priority.
- The default value `0` indicates that the default timeout (usually 40 seconds) is used.

> **Note:**
>
> - Normally, a regular query takes a few milliseconds, but occasionally when a TiKV node is in unstable network or gets I/O jitter, the query can take more than 1 second or even 10 seconds. In this case, you can set the TiKV RPC read request timeout to 100 milliseconds for a specific query by using the optimizer hint `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=100) */`. In this way, even if the response of a TiKV node is slow, TiDB can quickly time out and then re-send the RPC request to the TiKV node where the next TiKV Region Peer is located. Because the probability of two TiKV nodes getting I/O jitter simultaneously is low, the query can be completed usually within a few milliseconds to 110 milliseconds.
> - Do not set too small values (for example, 1 millisecond) for `tikv_client_read_timeout`. Otherwise, the requests might time out easily when the workload of a TiDB cluster is high, and subsequent retries will further increase the load on the TiDB cluster.
> - If you need to set different timeout values for different types of queries, it is recommended to use optimizer hints.

### time_zone

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `SYSTEM`
- This variable returns the current time zone. Values can be specified as either an offset such as '-8:00' or a named zone 'America/Los_Angeles'.
- The value `SYSTEM` means that the time zone should be the same as the system host, which is available via the [`system_time_zone`](#system_time_zone) variable.

### timestamp

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Float
- Default value: `0`
- Range: `[0, 2147483647]`
- A non-empty value of this variable indicates the UNIX epoch that is used as the timestamp for `CURRENT_TIMESTAMP()`, `NOW()`, and other functions. This variable might be used in data restore or replication.

### transaction_isolation

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `REPEATABLE-READ`
- Possible values: `READ-UNCOMMITTED`, `READ-COMMITTED`, `REPEATABLE-READ`, `SERIALIZABLE`
- This variable sets the transaction isolation. TiDB advertises `REPEATABLE-READ` for compatibility with MySQL, but the actual isolation level is Snapshot Isolation. See [transaction isolation levels](/transaction-isolation-levels.md) for further details.

### tx_isolation

This variable is an alias for `transaction_isolation`.

### tx_isolation_one_shot

> **Note:**
>
> This variable is internally used in TiDB. You are not expected to use it.

Internally, the TiDB parser transforms the `SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]` statements to `SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`.

### tx_read_ts

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: ""
- In the Stale Read scenarios, this session variable is used to help record the Stable Read timestamp value.
- This variable is used for the internal operation of TiDB. It is **NOT recommended** to set this variable.

### txn_scope

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `global`
- Value options: `global` and `local`
- This variable is used to set whether the current session transaction is a global transaction or a local transaction.
- This variable is used for the internal operation of TiDB. It is **NOT recommended** to set this variable.

### validate_password.check_user_name <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `ON`
- Type: Boolean
- This variable is a check item in the password complexity check. It checks whether the password matches the username. This variable takes effect only when [`validate_password.enable`](#validate_passwordenable-new-in-v650) is enabled.
- When this variable is effective and set to `ON`, if you set a password, TiDB compares the password with the username (excluding the hostname). If the password matches the username, the password is rejected.
- This variable is independent of [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) and not affected by the password complexity check level.

### validate_password.dictionary <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `""`
- Type: String
- This variable is a check item in the password complexity check. It checks whether the password matches the dictionary. This variable takes effect only when [`validate_password.enable`](#validate_passwordenable-new-in-v650) is enabled and [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) is set to `2` (STRONG).
- This variable is a string not longer than 1024 characters. It contains a list of words that cannot exist in the password. Each word is separated by semicolon (`;`).
- This variable is set to an empty string by default, which means no dictionary check is performed. To perform the dictionary check, you need to include the words to be matched in the string. If this variable is configured, when you set a password, TiDB compares each substring (length in 4 to 100 characters) of the password with the words in the dictionary. If any substring of the password matches a word in the dictionary, the password is rejected. The comparison is case-insensitive.

### validate_password.enable <span class="version-mark">New in v6.5.0</span>

> **Note:**
>
> This variable is always enabled for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `OFF`
- Type: Boolean
- This variable controls whether to perform password complexity check. If this variable is set to `ON`, TiDB performs the password complexity check when you set a password.

### validate_password.length <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `8`
- Range: `[0, 2147483647]` for TiDB Self-Hosted and [TiDB Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated), `[8, 2147483647]` for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)
- This variable is a check item in the password complexity check. It checks whether the password length is sufficient. By default, the minimum password length is `8`. This variable takes effect only when [`validate_password.enable`](#validate_passwordenable-new-in-v650) is enabled.
- The value of this variable must not be smaller than the expression: `validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`.
- If you change the value of `validate_password.number_count`, `validate_password.special_char_count`, or `validate_password.mixed_case_count` such that the expression value is larger than `validate_password.length`, the value of `validate_password.length` is automatically changed to match the expression value.

### validate_password.mixed_case_count <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- Range: `[0, 2147483647]` for TiDB Self-Hosted and [TiDB Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated), `[1, 2147483647]` for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)
- This variable is a check item in the password complexity check. It checks whether the password contains sufficient uppercase and lowercase letters. This variable takes effect only when [`validate_password.enable`](#validate_passwordenable-new-in-v650) is enabled and [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger.
- Neither the number of uppercase letters nor the number of lowercase letters in the password can be fewer than the value of `validate_password.mixed_case_count`. For example, when the variable is set to `1`, the password must contain at least one uppercase letter and one lowercase letter.

### validate_password.number_count <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- Range: `[0, 2147483647]` for TiDB Self-Hosted and [TiDB Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated), `[1, 2147483647]` for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)
- This variable is a check item in the password complexity check. It checks whether the password contains sufficient numbers. This variable takes effect only when [`validate_password.enable`](#password_reuse_interval-new-in-v650) is enabled and [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger.

### validate_password.policy <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Enumeration
- Default value: `1`
- Value options: `0`, `1`, and `2` for TiDB Self-Hosted and [TiDB Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated); `1` and `2` for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)
- This variable controls the policy for the password complexity check. This variable takes effect only when [`validate_password.enable`](#password_reuse_interval-new-in-v650) is enabled. The value of this variable determines whether other `validate-password` variables take effect in the password complexity check, except for `validate_password.check_user_name`.
- This value of this variable can be `0`, `1`, or `2` (corresponds to LOW, MEDIUM, or STRONG). Different policy levels have different checks:
    - 0 or LOW: password length.
    - 1 or MEDIUM: password length, uppercase and lowercase letters, numbers, and special characters.
    - 2 or STRONG: password length, uppercase and lowercase letters, numbers, special characters, and dictionary match.

### validate_password.special_char_count <span class="version-mark">New in v6.5.0</span>

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `1`
- Range: `[0, 2147483647]` for TiDB Self-Hosted and [TiDB Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-dedicated), `[1, 2147483647]` for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)
- This variable is a check item in the password complexity check. It checks whether the password contains sufficient special characters. This variable takes effect only when [`validate_password.enable`](#password_reuse_interval-new-in-v650) is enabled and [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) is set to `1` (MEDIUM) or larger.

### version

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `8.0.11-TiDB-`(tidb version)
- This variable returns the MySQL version, followed by the TiDB version. For example '8.0.11-TiDB-v8.1.0'.

### version_comment

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: (string)
- This variable returns additional details about the TiDB version. For example, 'TiDB Server (Apache License 2.0) Community Edition, MySQL 8.0 compatible'.

### version_compile_machine

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: (string)
- This variable returns the name of the CPU architecture on which TiDB is running.

### version_compile_os

- Scope: NONE
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: (string)
- This variable returns the name of the OS on which TiDB is running.

### wait_timeout

> **Note:**
>
> This variable is read-only for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer
- Default value: `28800`
- Range: `[0, 31536000]`
- Unit: Seconds
- This variable controls the idle timeout of user sessions. A zero-value means unlimited.

### warning_count

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Default value: `0`
- This read-only variable indicates the number of warnings that occurred in the statement that was previously executed.

### windowing_use_high_precision

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Boolean
- Default value: `ON`
- This variable controls whether to use the high precision mode when computing the window functions.
