---
title: UUID Best Practices
summary: Learn best practice and strategy for using UUID's with TiDB.
---

# UUID Best Practices

## The usecase for UUID

There are several benefits to using a `UUID` as a primary key, instead of an `AUTO_INCREMENT` integer value:

- UUIDs are designed to be globally unique, and can be generated on multiple systems without risking conflicts. In some cases, this means that the number of network trips to TiDB can be reduced, leading to improved performance.
- UUIDs are supported by most programming languages and database systems.
- When used as part of URLs, a UUID is not vulnerable to enumeration attacks. i.e. with an `auto_increment` number, it is possible to guess the other invoice ids or user ids.

## Using UUID's with TiDB

In TiDB you can generate UUID's with [`UUID()`](/functions-and-operators/miscellaneous-functions.md) and use `UUID_TO_BIN()` and `BIN_TO_UUID()` to convert from a text format to a binary format and back.

## Best practices

### Store as binary

The textual UUID format looks like this: `ab06f63e-8fe7-11ec-a514-5405db7aad56`, this is a string of 36 characters. By using `UUID_TO_BIN()` the textual format can be converted into a binary format of 16 bytes. This allows you to store this in `BINARY(16)` column. When retrieving you can use the `BIN_TO_UUID()` function to get back to the textual format.

### UUID format binary order and a clustered PK

The `UUID_TO_BIN()` function can be used with one argument, the UUID or with two arguments where the second argument is a `swap_flag`. It is recommended to not set the `swap_flag` with TiDB to avoid [hotspots](/best-practices/high-concurrency-best-practices.md).

To avoid hotspots it is recommended to explicitly set [the `CLUSTERED` option](/clustered-indexes.md) for UUID based primary keys to avoid hotspots.

To demonstrate the effect of the `swap_flag`, here are two tables with an identical structure. The difference is that the data inserted into `uuid_demo_1` uses `UUID_TO_BIN(?, 0)` and `uuid_demo_2` uses `UUID_TO_BIN(?, 1)`.

In the screenshot of the [Key Visualizer](/dashboard/dashboard-key-visualizer.md) below you can see that writes are concentrated in a single region of the `uuid_demo_2` table that has the order of the fields swapped in the binary format.

![Key Visualizer](/media/best-practices/uuid_keyviz.png)

```sql
CREATE TABLE `uuid_demo_1` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

```sql
CREATE TABLE `uuid_demo_2` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

## MySQL Compatibility

UUID's can be used in MySQL as well. The `BIN_TO_UUID()` and `UUID_TO_BIN()` functions were introduced in MySQL 8.0. The `UUID()` function is available in older MySQL versions as well.
