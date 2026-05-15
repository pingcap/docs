---
title: The GB18030 Character Set
summary: Learn the details of TiDB's support for the GB18030 character set.
---

# The GB18030 Character Set <span class="version-mark">New in v9.0.0</span>

Starting from v9.0.0, TiDB supports the GB18030-2022 character set. This document describes TiDB's support for and compatibility with the GB18030 character set.

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gb18030';
```

```
+---------+---------------------------------+--------------------+--------+
| Charset | Description                     | Default collation  | Maxlen |
+---------+---------------------------------+--------------------+--------+
| gb18030 | China National Standard GB18030 | gb18030_chinese_ci |      4 |
+---------+---------------------------------+--------------------+--------+
1 row in set (0.01 sec)
```

```sql
SHOW COLLATION WHERE CHARSET = 'gb18030';
```

```
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| gb18030_bin        | gb18030 | 249 |         | Yes      |       1 | PAD SPACE     |
| gb18030_chinese_ci | gb18030 | 248 | Yes     | Yes      |       1 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
2 rows in set (0.001 sec)
```

## MySQL compatibility

This section describes the compatibility of the GB18030 character set in TiDB with MySQL.

### Collation compatibility

In MySQL, the default collation for the GB18030 character set is `gb18030_chinese_ci`. In TiDB, the default collation for GB18030 depends on the configuration parameter [`new_collations_enabled_on_first_bootstrap`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file/#new_collations_enabled_on_first_bootstrap):

- By default, `new_collations_enabled_on_first_bootstrap` is set to `true`, which means enabling the [new collation framework](/character-set-and-collation.md#new-framework-for-collations). In this case, the default collation for GB18030 is `gb18030_chinese_ci`.
- If `new_collations_enabled_on_first_bootstrap` is set to `false`, the new framework for collations is disabled, and the default collation for GB18030 is `gb18030_bin`.

Additionally, the `gb18030_bin` supported by TiDB differs from MySQL's `gb18030_bin` collation. TiDB converts GB18030 to `utf8mb4` and then performs binary sorting.

After enabling the new framework for collations, if you check the collations for the GB18030 character set, you can see that TiDB's default collation for GB18030 is switched to `gb18030_chinese_ci`:

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gb18030';
```

```
+---------+---------------------------------+--------------------+--------+
| Charset | Description                     | Default collation  | Maxlen |
+---------+---------------------------------+--------------------+--------+
| gb18030 | China National Standard GB18030 | gb18030_chinese_ci |      4 |
+---------+---------------------------------+--------------------+--------+
1 row in set (0.01 sec)
```

```sql
SHOW COLLATION WHERE CHARSET = 'gb18030';
```

```
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| gb18030_bin        | gb18030 | 249 |         | Yes      |       1 | PAD SPACE     |
| gb18030_chinese_ci | gb18030 | 248 | Yes     | Yes      |       1 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
2 rows in set (0.00 sec)
```

### Character compatibility

- TiDB supports GB18030-2022 characters, while MySQL supports GB18030-2005 characters. As a result, the encoding and decoding results for certain characters differ between the two systems.

- For invalid GB18030 characters, such as `0xFE39FE39`, MySQL allows writing them to the database in hexadecimal form and stores them as `?`. In TiDB, reading or writing invalid GB18030 characters in strict mode returns an error; in non-strict mode, TiDB allows reading or writing invalid GB18030 characters but returns a warning.

### Others

- Currently, TiDB does not support using the `ALTER TABLE` statement to convert other character sets to `gb18030`, or to convert from `gb18030` to another character set.

- TiDB does not support using the `_gb18030` character set introducer. For example:

    ```sql
    CREATE TABLE t(a CHAR(10) CHARSET BINARY);
    Query OK, 0 rows affected (0.00 sec)
    INSERT INTO t VALUES (_gb18030'啊');
    ERROR 1115 (42000): Unsupported character introducer: 'gb18030'
    ```

- For binary characters in `ENUM` and `SET` types, TiDB currently treats them as using the `utf8mb4` character set.

## Component compatibility

- TiFlash, TiDB Data Migration (DM), and TiCDC currently do not support the GB18030 character set.

- Before v9.0.0, Dumpling does not support exporting tables with `charset=GB18030`, and TiDB Lightning does not support importing tables with `charset=GB18030`.

- Before v9.0.0, TiDB Backup & Restore (BR) does not support backing up or restoring tables with `charset=GB18030`. In addition, no version of BR supports restoring tables with `charset=GB18030` to TiDB clusters earlier than v9.0.0.

## See also

* [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
* [Character Set and Collation](/character-set-and-collation.md)
