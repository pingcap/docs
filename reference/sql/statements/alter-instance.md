---
title: ALTER INSTANCE
summary: Learn the overview of the ALTER INSTANCE usage in TiDB.
category: reference
---

# ALTER INSTANCE

The `ALTER INSTANCE` statement is used to make changes to a single TiDB instance. Currently, TiDB only supports the `RELOAD TLS` clause.

## RELOAD TLS

You can execute the `ALTER INSTANCE RELOAD TLS` statement to reload the certificate ([`ssl-cert`](/reference/configuration/tidb-server/configuration-file.md#ssl-cert)), the key ([`ssl-key`](/reference/configuration/tidb-server/configuration-file.md#ssl-key)), and the CA ([`ssl-ca`](/reference/configuration/tidb-server/configuration-file.md#ssl-ca)) from the original configuration path.

The newly loaded certificate, key, and CA take effect on the connection established after the statement is successfully executed. They have no effect on the connection established before the statement is executed.

When an error occurs during reloading, you receive an error message and continue to use the previous key and certificate by default. However, if you have added the optional `NO ROLLBACK ON ERROR`, when an error occurs during reloading, the error is not returned, and the subsequent requests are handled on condition that the TLS secure connection is disabled.

## Syntax diagram

![AlterInstanceStmt](/media/sqlgram/AlterInstanceStmt.png)

## Example

{{< copyable "sql" >}}

```sql
ALTER INSTANCE RELOAD TLS;
```

## MySQL compatibility

The `ALTER INSTANCE RELOAD TLS` statement only supports reloading from the original configuration path. It dose not support the dynamic modification of the loading path, nor does it support dynamic enablement of the TLS encrypted connection feature when TiDB is started. This feature is disabled by default when you restart TiDB.

## See also

[Enable Client TLS](/how-to/secure/enable-tls-clients.md).
