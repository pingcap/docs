---
title: Troubleshoot Inconsistencies Between Data and Index
summary: Learn how to deal with errors reported by the data index consistency check, which can be performed automatically or manually.
---

# Troubleshoot Inconsistencies Between Data and Index

TiDB checks consistency between data and index during executing a transaction or executing the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) command. If the check finds that record key-value and index key-value are inconsistent, that is, the key-value pair storing row data and the key-value pair storing its corresponding index are inconsistent (for example, more indexes or missing indexes), TiDB reports the data index consistency error and prints the related errors in the log file.

This document explains the errors of data index consistency and provides some ways to bypass the check. When a data index consistency error occurs, contact PingCAP technical support to fix or troubleshoot.

## Example error explanation

When data index inconsistency occurs, you can check TiDB error messages to see the specific inconsistent item of row data and index data, or check the related error logs for further investigation.

### Errors reported during transaction execution

This section lists the data index inconsistency errors reported when TiDB executes transactions and explains the meaning of these errors with examples.

#### Error 8133

`ERROR 8133 (HY000): data inconsistency in table: t, index: k2, index-count:1 != record-count:0`

This error indicates that for the `k2` index in table `t`, the number of indexes in the table is 1 and the number of row records is 0. The number is inconsistent.

#### Error 8138

`ERROR 8138 (HY000): writing inconsistent data in table: t, expected-values:{KindString green} != record-values:{KindString GREEN}`

This error indicates that the transaction was attempting to write an incorrect row value. For the data to be written, due to issues in the encoding and decoding process, the encoded row data does not match the original data before encoding.

#### Error 8139

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

This error indicates that the handle (that is, the key of the row data) value of the data to be written is inconsistent. For the `i1` index in the table `t`, the row to be written by the transaction has a handle of 4 in the index key-value pair and a handle of 3 in the row record key-value pair. The data of this row will not be written.

#### Error 8140

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

This error indicates that the data of a row to be written by the transaction does not match the value of the index. For the `i2` index in the table `t`, a row to be written by the transaction has data in the index key-value pair as `hellp` and data in the row record key-value pair as `hello`. The data of this row will not be written.

#### Error 8141

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

This error indicates that the assertion failed when a transaction was committed. Assuming that the data index is consistent, TiDB asserted that the key `7480000000000000405f720133000000000000000000f8` did not exist. When the transaction was committed, TiDB found the key did exist, written by the transaction with `start ts` as `430590532931551233`. TiDB will print the MVCC (Multi-Version Concurrency Control) history of this key to the log.

### Errors reported in admin check

This section lists the data index inconsistency errors that might occur in TiDB when you execute the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement, with examples provided to explain the error meanings.

#### Error 8003

`ERROR 8003 (HY000): table count 3 != index(idx) count 2`

This error indicates that the table on which the `ADMIN CHECK` statement is executed has 3 row key-value pairs but only 2 index key-value pairs.

#### Error 8134

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

This error indicates that for the `c2` index in table `t`, the handle value of a row is 13 in the index key-value pair but is 12 in the row record key-value pair, which results in data inconsistency.

#### Error 8223

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

This error indicates that `index-value` is null and `record-values` is not null, meaning that the record does not have the corresponding index but has the corresponding row, which results in data inconsistency.

## Reasons and solutions

When a data index consistency error occurs, the reasons can be as follows:

- The data indexes in the existing data are consistent. The current version of TiDB has a bug. An ongoing transaction is about to write inconsistent data into the existing data, so the transaction is aborted.
- The data indexes in the existing data are inconsistent. The inconsistent data could be from an error or a dangerous operation in the past or caused by a TiDB bug.
- The data indexes are consistent but the detection algorithm has a bug that causes a false alarm.

If you receive a data index consistency error, contact PingCAP technical support immediately to fix or troubleshoot it instead of dealing with the error by yourself. If PingCAP technical support confirms that the error is a false alarm, or your application needs to skip such errors urgently, you can use the following methods to bypass the check.

### Disable error check

For some errors reported in transaction execution, you can bypass the corresponding check as follows:

- To bypass the check of errors 8138, 8139, and 8140, configure `set @@tidb_enable_mutation_checker=0`.
- To bypass the check of error 8141, configure `set @@tidb_txn_assertion_level=OFF`.

For other errors reported in transaction execution and all errors reported during the execution of the `ADMIN CHECK [TABLE|INDEX]` statements, you cannot bypass the corresponding check, because the data inconsistency has already occurred.

### Rewrite SQL

Disabling `tidb_enable_mutation_checker` and `tidb_txn_assertion_level` mentioned in the previous section bypasses the corresponding check of all SQL statements. If only a particular SQL is misreported, you can try bypassing the error by rewriting the SQL to another equivalent form using different execution operators.