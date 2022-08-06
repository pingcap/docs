---
title: Temporary Tables
summary: Learn the temporary tables feature in TiDB, and learn how to use temporary tables to store intermediate data of an application, which helps reduce table management overhead and improve performance.
---

# Temporary Tables

The temporary tables feature is introduced in TiDB v5.3.0. This feature solves the issue of temporarily storing the intermediate results of an application, which frees you from frequently creating and dropping tables. You can store the intermediate calculation data in temporary tables. When the intermediate data is no longer needed, TiDB automatically cleans up and recycles the temporary tables. This avoids user applications being too complicated, reduces table management overhead, and improves performance.

[This](http://{grafana-ip}:3000/) document introduces the user scenarios and the types of temporary tables, provides usage examples and instruction on how to limit the memory usage of temporary tables, and explains compatibility restrictions with other TiDB features.

> **Note:**
>
> If the transaction is automatically committed, after the SQL statement is executed, the inserted data is automatically cleared and unavailable to subsequent SQL executions. Therefore, you should use non-autocommit transactions to read from and write to global temporary [tables](http://{pd-ip}:2379/dashboard).

## See also

* [CREATE TABLE](https://ranh.me/test)
