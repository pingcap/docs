---
title: Backup and Restore
category: advanced
---

# Backup and Restore

## About

This document describes how to backup and restore the data of TiDB. Currently, this document only covers full backup and restoration.

Here we assume that the TiDB service information is as follows:

|Name|Address|Port|User|Password|
|:----:|:-------:|:----:|:----:|:------:|
|TiDB|127.0.0.1|4000|root|*|

Use the following tools for data backup and restoration:

- `mydumper`: to export data from TiDB
- `loader`: to import data into TiDB

### Download TiDB Toolset (Linux)

```bash
# Download the tool package.
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256

# Check the file integrity. If the result is OK, the file is correct.
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256

# Extract the package.
tar -xzf tidb-enterprise-tools-latest-linux-amd64.tar.gz
cd tidb-enterprise-tools-latest-linux-amd64
```

## Full Backup and Restoration Using `mydumper`/`loader`

The `mydumper` is a powerful data backup tool. See more about [`mydumper`](https://github.com/maxbube/mydumper). 

To backup data, use `mydumper` to export data from TiDB. To restore data, use `loader` to import data into TiDB.

> **Note:** You can use the official `mysqldump` tool of MySQL to backup and restore data in TiDB, but its performance is worse than `mydumper`/`loader`. It will take up much time to backup and restore a large amount of data. Therefore, the tool `mysqldump` is not recommended.

### Best Practices of Full Backup and Restoration Using `mydumper`/`loader` 

To quickly backup and restore data (especially large amounts of data), refer to the following recommendations:

- Keep the size of the data file exported using `mydumper` as small as possible. It is recommended to keep it within 64M. You can set the parameter `-F` to 64.
- You can adjust the `loader` parameter `-t` based on the number of TiKV instances and the load. For example, you can set the parameter to `3 *(1~n)` in the case of 3 TiKV scenarios. When the TiKV load is too high, and a large number of `backoffer.maxSleep 15000ms is exceeded` show in `loader` and TiDB log, adjust it to a smaller value appropriately. When the TiKV load is not too high, adjust it to a higher value appropriately.

#### An Example of Restoring Data and Related Configuration 

- The total amount of data exported using `mydumper` is 214G. Single table 8 columns, 2 billion rows of data.
- Cluster topology:
  - TiKV * 12
  - TiDB * 4
  - PD * 3
- Set the `mydumper` parameter `-F` to 16, and `loader` parameter `-t` to 64.

Result: It takes about 11 hours to import, with 19.4G/hour.

### Backup Data from TiDB

Use `mydumper` to backup data from TiDB.

```bash
./bin/mydumper -h 127.0.0.1 -P 4000 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

The `-B test` indicates that the operation is on the database `test`. The `-T t1,t2` indicates that only the two tables `t1` and `t2` are exported.  

The `-t 16` indicates using 16 threads to export data. The actual `table` is divided into `chunk`s, and the `-F 64` indicates that the size of `chunk` is 64MB.  

The `--skip-tz-utc` indicates ignoring the difference of time zone settings between TiDB and the machine that is exporting data. Automatic conversion is prohibited.    

### Restore Data into TiDB

To restore data into TiDB, use `loader` to import the previously exported data. Refer to [Loader instructions](../tools/loader.md) for the download and specific use of `loader`.   

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

After the data is exported successfully, enter TiDB using the MySQL official client and check:

```sql
mysql -h127.0.0.1 -P4000 -uroot

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| t2             |
+----------------+

mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
+----+------+

mysql> select * from t2;
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
```
