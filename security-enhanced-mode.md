# TiDB Security Enhanced Mode (SEM)

## Overview and Purpose

Security Enhanced Mode (SEM) provides a mandatory access control layer that operates on top of TiDB's standard privilege system. Its primary purpose is to limit the capabilities of all users, including the `root` user.

This feature is especially critical in Database-as-a-Service (DBaaS) environments. Service providers can offer tenants `root` access to their databases—ensuring compatibility with applications—while simultaneously preventing them from executing commands that could compromise the underlying cluster's security, stability, or data isolation.

You can enable SEM in two ways: a default mode with a predefined set of restrictions, or a custom mode that uses a configuration file for a highly detailed security policy.

## Enabling and Configuring SEM

You enable SEM by setting `security.enable-sem = true` in your TiDB server's configuration file (`tidb.toml`). The specific behavior of SEM depends on whether you also provide a configuration file.

You can verify which mode is active by checking the `tidb_enable_enhanced_security` system variable.

```sql
SHOW VARIABLES LIKE 'tidb_enable_enhanced_security';
```

### Mode 1: Default Restrictions

This mode provides a baseline set of security enhancements that primarily reduce the broad power of the `SUPER` privilege, replacing it with fine-grained privileges.

  * Activation: Set `enable-sem = true` in `tidb.toml` without setting the `sem-config` path.
  * System Variable: `tidb_enable_enhanced_security` will be `ON`.

In this mode, TiDB enforces the following restrictions:

| Restricted Action                                                                                             | Required Privilege for Exemption |
| :------------------------------------------------------------------------------------------------------------ | :------------------------------- |
| Writing data to system tables in the `mysql` schema and viewing sensitive columns in `information_schema` tables. | `RESTRICTED_TABLES_ADMIN`        |
| Viewing sensitive variables in `SHOW STATUS`.                                                                 | `RESTRICTED_STATUS_ADMIN`        |
| Viewing and setting sensitive system variables.                                                               | `RESTRICTED_VARIABLES_ADMIN`     |
| Dropping or modifying a user account that holds the `RESTRICTED_USER_ADMIN` privilege.                        | `RESTRICTED_USER_ADMIN`          |

### Mode 2: Custom Restrictions via Configuration File

This mode enables a fully customizable security policy defined in a JSON file. It offers granular control over tables, variables, privileges, and SQL commands.

  * Activation: Set both `enable-sem = true` and `sem-config = '/path/to/your/sem-policy.json'` in `tidb.toml`.
  * System Variable: `tidb_enable_enhanced_security` will be `CONFIG`.

You must restart your TiDB cluster for any configuration changes to take effect.

## Custom Policy Feature Reference (Mode 2)

The following sections detail the features available when using a custom configuration file (Mode 2).

### Restricting Access to Tables and Databases

This feature prevents access to specified databases or individual tables.

  * Configuration:
      * `restricted_databases`: An array of database names. All tables within these databases become inaccessible.
      * `restricted_tables`: An array of objects specifying a `schema` and `name`. The optional `"hidden": true` flag makes the table invisible.
  * Exemption Privilege: `RESTRICTED_TABLES_ADMIN`
  * Configuration Example:
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_databases": ["mysql"],
      "restricted_tables": [{"schema": "information_schema", "name": "columns", "hidden": true}]
    }
    ```
    As a restricted user (e.g., `root`):
    ```
    mysql> select * from information_schema.columns;
    ERROR 1142 (42000): SELECT command denied to user 'root'@'%' for table 'columns'
    mysql> use mysql;
    ERROR 1044 (42000): Access denied for user 'root'@'%' to database 'mysql'
    ```

### Restricting System Variables

This feature controls interaction with system variables by hiding them, making them read-only, or masking their values.

  * Configuration: The `restricted_variables` key contains an array of variable objects with a control flag:
      * `"hidden": true`: The variable is inaccessible.
      * `"readonly": true`: The variable can be read but not modified.
      * `"value": "string"`: Overrides the variable's return value. Note: This option is only supported for local read-only variables.
  * Exemption Privilege: `RESTRICTED_VARIABLES_ADMIN`
  * Configuration Example:
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_variables": [
        {"name": "tidb_config", "hidden": true},
        {"name": "hostname", "hidden": false, "value": "testhostname"}
      ]
    }
    ```
    As a restricted user (e.g., `root`):
    ```
    mysql> SELECT @@tidb_config;
    ERROR 1227 (42000): Access denied; you need (at least one of) the RESTRICTED_VARIABLES_ADMIN privilege(s) for this operation
    mysql> SELECT @@hostname;
    +--------------+
    | @@hostname   |
    +--------------+
    | testhostname |
    +--------------+
    1 row in set (0.00 sec)
    ```

### Restricting Privileges and User Management

This feature prevents powerful privileges from being granted and protects administrative accounts from being altered or dropped.

  * Configuration: The `restricted_privileges` key contains an array of privilege names. Once listed, a privilege cannot be granted. Listing `RESTRICTED_USER_ADMIN` itself protects users who hold that privilege.
  * Exemption Privilege: `RESTRICTED_PRIV_ADMIN`
  * Configuration Example:
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_privileges": ["FILE"]
    }
    ```
    As a restricted user (e.g., `root`):
    ```
    mysql> GRANT FILE ON *.* TO 'some_user'@'%';
    ERROR 1227 (42000): Access denied; you need (at least one of) the RESTRICTED_PRIV_ADMIN privilege(s) for this operation
    -- Assuming 'sem_admin' has the RESTRICTED_USER_ADMIN privilege, attempt to drop the user
    mysql> DROP USER 'sem_admin'@'%';
    ERROR 1227 (42000): Access denied; you need (at least one of) the RESTRICTED_USER_ADMIN privilege(s) for this operation
    ```

### Restricting Status Variables

This feature filters sensitive operational data from the output of `SHOW STATUS`.

  * Configuration:
      * `restricted_status_variables`: An array of status variable names to hide from `SHOW STATUS`.
  * Exemption Privilege: `RESTRICTED_STATUS_ADMIN`
  * Configuration Example:
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_status_variables": ["tidb_gc_leader_desc"]
    }
    ```
    As a restricted user (e.g., `root`):
    ```
    mysql> SHOW STATUS LIKE 'tidb_gc_leader_desc';
    Empty set (0.01 sec)
    ```

### Restricting SQL Commands

This feature blocks the execution of specific SQL statements or entire classes of commands.

  * Configuration:
      * `restricted_sql`: An object containing two arrays:
          * `sql`: A list of specific SQL commands to block (e.g., `BACKUP`, `RESTORE`).
          * `rule`: A list of predefined rule names that block specific classes of statements. Supported rules are:
              * `time_to_live`: Blocks DDL statements related to Table TTL.
              * `alter_table_attributes`: Blocks the `ALTER TABLE ... ATTRIBUTES="..."` statement.
              * `import_with_external_id`: Blocks `IMPORT INTO` statements that use an S3 `EXTERNAL_ID`.
              * `select_into_file`: Blocks `SELECT ... INTO OUTFILE` statements.
              * `import_from_local`: Blocks `LOAD DATA LOCAL INFILE` and `IMPORT INTO` from a local file path.
  * Exemption Privilege: `RESTRICTED_SQL_ADMIN`
  * Configuration Example:
    ```json
    {
      "version": "1", "tidb_version": "9.0.0",
      "restricted_sql": {
        "rule": ["time_to_live"],
        "sql": ["BACKUP"]
      }
    }
    ```
    As a restricted user (e.g., `root`):
    ```
    mysql> BACKUP DATABASE `test` TO 's3://bucket/backup';
    ERROR 8132 (HY000): Feature 'BACKUP DATABASE `test` TO 's3://bucket/backup'' is not supported when security enhanced mode is enabled
    mysql> CREATE TABLE test.t1 (id INT, created_at TIMESTAMP) TTL = `created_at` + INTERVAL 1 DAY;
    ERROR 8132 (HY000): Feature 'CREATE TABLE test.t1 (id INT, created_at TIMESTAMP) TTL = `created_at` + INTERVAL 1 DAY' is not supported when security enhanced mode is enabled
    ```
