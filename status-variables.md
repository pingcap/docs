---
title: Server Status Variables
summary: Use status variables to see the system and session status
---

# Server Status Variables

Most status variables are implemented to be compatible with MySQL. These variables give information about the global status of the server and the status of the current session.

The [SHOW GLOBAL STATUS](/sql-statements/sql-statement-show-status.md) command can be used to retrieve the global status and the [SHOW SESSION STATUS](/sql-statements/sql-statement-show-status.md) command can be used to see the status of the current session.

The [FLUSH STATUS](/sql-statements/sql-statement-flush-status.md) command is also support to aid MySQL compatibility.

## Variable Reference

### Compression

- Scope: SESSION
- Type: Boolean
- Indicates if the MySQL Protocol uses compression or not.

### Compression_algorithm

- Scope: SESSION
- Type: String
- Indicates the compression algorithm that is used for the MySQL Protocol.

### Compression_level

- Scope: SESSION | GLOBAL
- Type: Integer
- The compression level that is used for the MySQL Protocol.

### Ssl_cipher

- Scope: SESSION | GLOBAL
- Type: String
- TLS Cipher that is in use.

### Ssl_cipher_list

- Scope: SESSION | GLOBAL
- Type: String
- The list of TLS Ciphers that the server supports.

### Ssl_server_not_after

- Scope: SESSION | GLOBAL
- Type: Date
- The expiration date of the X.509 certificate of the server that is used for TLS connections.

### Ssl_server_not_before

- Scope: SESSION | GLOBAL
- Type: String
- The start date of the X.509 certificate of the server that is used for TLS connections.

### Ssl_verify_mode

- Scope: SESSION | GLOBAL
- Type: Integer
- The TLS verification mode bitmask.

### Ssl_version

- Scope: SESSION | GLOBAL
- Type: String
- The version of the TLS protocol that is used

### Uptime

- Scope: SESSION | GLOBAL
- Type: Integer
- Uptime of the server in seconds.

### ddl_schema_version

- Scope: SESSION | GLOBAL
- Type: Integer
- The version of the DDL schema that is used.

### last_plan_binding_update_time <span class="version-mark">New in v5.2.0</span>

- Scope: SESSION | GLOBAL
- Type: Timestamp
- The time and date of the last plan binding update.

### server_id

- Scope: SESSION | GLOBAL
- Type: String
- UUID of the server
