---
title: EXPLAIN ANALYZE | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 EXPLAIN ANALYZE 的概述。
---

# EXPLAIN ANALYZE

`EXPLAIN ANALYZE` 语句的工作方式类似于 `EXPLAIN`，主要区别在于它会实际执行该语句。这允许你将查询计划中使用的估算值与实际执行过程中遇到的值进行比较。如果估算值与实际值差异显著，你应考虑对受影响的表执行 `ANALYZE TABLE`。

> **注意：**
>
> 当你使用 `EXPLAIN ANALYZE` 执行 DML 语句时，通常会执行数据修改。目前，**无法**显示 DML 语句的执行计划。

## 概要

```ebnf+diagram
ExplainSym ::=
    'EXPLAIN'
|   'DESCRIBE'
|    'DESC'

ExplainStmt ::=
    ExplainSym ( TableName ColumnName? | 'ANALYZE'? ExplainableStmt | 'FOR' 'CONNECTION' NUM | 'FORMAT' '=' ( stringLit | ExplainFormatType ) ( 'FOR' 'CONNECTION' NUM | ExplainableStmt ) )

ExplainableStmt ::=
    SelectStmt
|   DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
|   UnionStmt
```

## EXPLAIN ANALYZE 输出格式

不同于 `EXPLAIN`，`EXPLAIN ANALYZE` 会执行对应的 SQL 语句，记录其运行时信息，并将这些信息与执行计划一同返回。因此，你可以将 `EXPLAIN ANALYZE` 视为 `EXPLAIN` 语句的扩展。与 `EXPLAIN`（用于调试查询执行）相比，`EXPLAIN ANALYZE` 的返回结果还包括 `actRows`、`execution info`、`memory` 和 `disk` 等列的信息。这些列的详细内容如下：

| 属性名          | 描述 |
|:----------------|:---------------------------------|
| actRows       | 操作符输出的行数。 |
| execution info  | 操作符的执行信息。`time` 表示从进入操作符到离开操作符的总“墙上时间”，包括所有子操作符的总执行时间。如果操作符被父操作符多次调用（在循环中），则时间指累计时间。`loops` 表示父操作符调用当前操作符的次数。 |
| memory  | 操作符占用的内存空间。 |
| disk  | 操作符占用的磁盘空间。 |

## 示例

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```sql
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
EXPLAIN ANALYZE SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
| id          | estRows | actRows | task | access object | execution info                                                 | operator info | memory | disk |
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
| Point_Get_1 | 1.00    | 1       | root | table:t1      | time:757.205µs, loops:2, Get:{num_rpc:1, total_time:697.051µs} | handle:1      | N/A    | N/A  |
+-------------+---------+---------+------+---------------+----------------------------------------------------------------+---------------+--------+------+
1 row in set (0.01 sec)
```

```sql
EXPLAIN ANALYZE SELECT * FROM t1;
```

```sql
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| id                | estRows  | actRows | task      | access object | execution info                                                                                                                                                                                                                            | operator info                  | memory    | disk |
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
| TableReader_5     | 10000.00 | 3       | root      |               | time:278.2µs, loops:2, cop_task: {num: 1, max: 437.6µs, proc_keys: 3, copr_cache_hit_ratio: 0.00}, rpc_info:{Cop:{num_rpc:1, total_time:423.9µs}}                                                                                         | data:TableFullScan_4           | 251 Bytes | N/A  |
| └─TableFullScan_4 | 10000.00 | 3       | cop[tikv] | table:t1      | tikv_task:{time:0s, loops:1}, scan_detail: {total_process_keys: 3, total_process_keys_size: 111, total_keys: 4, rocksdb: {delete_skipped_count: 0, key_skipped_count: 3, block: {cache_hit_count: 0, read_count: 0, read_byte: 0 Bytes}}} | keep order:false, stats:pseudo | N/A       | N/A  |
+-------------------+----------+---------+-----------+---------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+-----------+------+
2 rows in set (0.00 sec)
```

## 操作符的执行信息

除了基本的 `time` 和 `loop` 执行信息外，`execution info` 还包含操作符特定的执行信息，主要包括操作符发送 RPC 请求的耗时和其他步骤的持续时间。

### Point_Get

`Point_Get` 操作符的执行信息通常包含以下内容：

- `Get:{num_rpc:1, total_time:697.051µs}`：向 TiKV 发送的 `Get` RPC 请求次数（`num_rpc`）和所有 RPC 请求的总耗时（`total_time`）。
- `ResolveLock:{num_rpc:1, total_time:12.117495ms}`：如果 TiDB 在读取数据时遇到锁，则必须先解决锁，通常发生在读写冲突场景中。此信息表示解决锁的耗时。
- `regionMiss_backoff:{num:11, total_time:2010 ms},tikvRPC_backoff:{num:11, total_time:10691 ms}`：当 RPC 请求失败时，TiDB 会等待退避时间后重试。退避统计包括退避类型（如 `regionMiss` 和 `tikvRPC`）、总等待时间（`total_time`）和退避总次数（`num`）。

### Batch_Point_Get

`Batch_Point_Get` 操作符的执行信息与 `Point_Get` 类似，但 `Batch_Point_Get` 通常会向 TiKV 发送 `BatchGet` RPC 请求以读取数据。

`BatchGet:{num_rpc:2, total_time:83.13µs}`：向 TiKV 发送的 `BatchGet` 类型 RPC 请求次数（`num_rpc`）和所有 RPC 请求的总耗时（`total_time`）。

### TableReader

`TableReader` 操作符的执行信息通常如下：

```
cop_task: {num: 6, max: 1.07587ms, min: 844.312µs, avg: 919.601µs, p95: 1.07587ms, max_proc_keys: 16, p95_proc_keys: 16, tot_proc: 1ms, tot_wait: 1ms, copr_cache_hit_ratio: 0.00}, rpc_info:{Cop:{num_rpc:6, total_time:5.313996ms}}
```

- `cop_task`：包含 `cop` 任务的执行信息。例如：
    - `num`：cop 任务的数量。
    - `max`、`min`、`avg`、`p95`：执行 cop 任务所耗时间的最大值、最小值、平均值和 P95。
    - `max_proc_keys` 和 `p95_proc_keys`：所有 cop 任务中扫描的最大和 P95 的键值数。如果最大值与 P95 之间差异较大，可能意味着数据分布不均。
    - `copr_cache_hit_ratio`：Coprocessor 缓存的命中率。
- `rpc_info`：向 TiKV 发送的 RPC 请求的总次数和总耗时，按请求类型统计。
- `backoff`：包含不同类型的退避和总等待时间。

### Insert

`Insert` 操作符的执行信息通常如下：

```
prepare:109.616µs, check_insert:{total_time:1.431678ms, mem_insert_time:667.878µs, prefetch:763.8µs, rpc:{BatchGet:{num_rpc:1, total_time:699.166µs},Get:{num_rpc:1, total_time:378.276µs }}}
```

- `prepare`：准备写入的耗时，包括表达式、默认值和自增值的计算。
- `check_insert`：通常出现在 `insert ignore` 和 `insert on duplicate` 语句中，包括冲突检测和将数据写入 TiDB 事务缓存的耗时。注意，此时间不包括事务提交的耗时。包含：
    - `total_time`：`check_insert` 步骤的总耗时。
    - `mem_insert_time`：将数据写入 TiDB 事务缓存的耗时。
    - `prefetch`：从 TiKV 获取待冲突检测数据的时间，此步骤会发送 `Batch_Get` RPC 请求。
    - `rpc`：向 TiKV 发送 RPC 请求的总耗时，通常包括 `BatchGet` 和 `Get` 两种请求类型，其中：
        - `BatchGet` RPC 请求在 `prefetch` 步骤中发送。
        - `Get` RPC 请求在执行 `insert on duplicate` 语句的 `duplicate update` 时发送。
- `backoff`：包含不同类型的退避和总等待时间。

### IndexJoin

`IndexJoin` 操作符有 1 个外部工作线程和 N 个内部工作线程用于并发执行。连接结果保持外表的顺序。详细执行流程如下：

1. 外部工作线程读取 N 行外部行，然后将其封装成任务，发送到结果通道和内部工作线程通道。
2. 内部工作线程接收任务，从任务中构建键范围，并根据键范围获取内部行，然后构建内部行的哈希表。
3. 主 `IndexJoin` 线程从结果通道接收任务，等待内部工作线程完成任务处理。
4. 主 `IndexJoin` 线程通过查找内部行的哈希表，将每个外部行与内部行进行连接。

`IndexJoin` 操作符的执行信息如下：

```
inner:{total:4.297515932s, concurrency:5, task:17, construct:97.96291ms, fetch:4.164310088s, build:35.219574ms}, probe:53.574945ms
```

- `Inner`：内部工作线程的执行信息：
    - `total`：内部工作线程的总耗时。
    - `concurrency`：内部工作线程数。
    - `task`：内部工作线程处理的任务总数。
    - `construct`：内部工作线程读取对应内部表行之前的准备时间。
    - `fetch`：内部工作线程读取内部表行的总耗时。
    - `build`：内部工作线程构建对应内部表行哈希表的总耗时。
- `probe`：主线程与内部表行哈希表进行连接的总耗时。

### IndexHashJoin

`IndexHashJoin` 操作符的执行过程类似于 `IndexJoin`，但输出顺序不一定与外表保持一致。`IndexHashJoin` 也有 1 个外部工作线程和 N 个内部工作线程并行执行，详细流程如下：

1. 外部工作线程读取 N 行外部行，构建任务，并发送到内部工作线程通道。
2. 内部工作线程接收任务，依次执行以下三步：
   a. 从外部行构建哈希表
   b. 从外部行构建键范围并获取内部行
   c. 探测哈希表，将连接结果发送到结果通道。注意：步骤 a 和 b 是并发运行的。
3. `IndexHashJoin` 的主线程从结果通道接收连接结果。

`IndexHashJoin` 的执行信息如下：

```sql
inner:{total:4.429220003s, concurrency:5, task:17, construct:96.207725ms, fetch:4.239324006s, build:24.567801ms, join:93.607362ms}
```

- `Inner`：内部工作线程的执行信息：
    - `total`：总耗时。
    - `concurrency`：内部工作线程数。
    - `task`：处理的任务总数。
    - `construct`：读取内部表行之前的准备时间。
    - `fetch`：读取内部表行的总耗时。
    - `build`：构建内部表哈希表的总耗时。
    - `join`：与内部表行和外部表哈希表进行连接的总耗时。

### HashJoin

`HashJoin` 操作符有内部工作线程、外部工作线程和 N 个连接工作线程。详细执行流程如下：

1. 内部工作线程读取内部表行，构建哈希表。
2. 外部工作线程读取外部表行，然后封装成任务，发送到连接工作线程。
3. 连接工作线程等待第 1 步中哈希表的构建完成。
4. 连接工作线程使用任务中的外部表行和哈希表进行连接操作，然后将连接结果发送到结果通道。
5. `HashJoin` 的主线程从结果通道接收连接结果。

`HashJoin` 的执行信息如下：

```
build_hash_table:{total:146.071334ms, fetch:110.338509ms, build:35.732825ms}, probe:{concurrency:5, total:857.162518ms, max:171.48271ms, probe:125.341665ms, fetch:731.820853ms}
```

- `build_hash_table`：读取内部表数据并构建哈希表的执行信息：
    - `total`：总耗时。
    - `fetch`：读取内部表数据的总耗时。
    - `build`：构建哈希表的总耗时。
- `probe`：连接工作线程的执行信息：
    - `concurrency`：连接工作线程数。
    - `total`：所有连接工作线程的总耗时。
    - `max`：单个连接工作线程的最长执行时间。
    - `probe`：连接外部表行与哈希表的总耗时。
    - `fetch`：连接工作线程等待读取外部表行数据的总耗时。

### TableFullScan (TiFlash)

在 TiFlash 节点上执行的 `TableFullScan` 操作符包含以下执行信息：

```sql
tiflash_scan: {
  dtfile: {
    total_scanned_packs: 2, 
    total_skipped_packs: 1, 
    total_scanned_rows: 16000, 
    total_skipped_rows: 8192, 
    total_rough_set_index_load_time: 2ms, 
    total_read_time: 20ms
  }, 
  total_create_snapshot_time: 1ms
}
```

+ `dtfile`：在表扫描过程中与 DTFile（DeltaTree 文件）相关的信息，反映 TiFlash 稳定层的数据扫描状态。
    - `total_scanned_packs`：已扫描的包总数。包是 TiFlash DTFile 中的最小读取单位，默认每 8192 行组成一个包。
    - `total_skipped_packs`：被跳过的包总数。当 `WHERE` 条件命中粗集索引或匹配主键范围过滤时，会跳过不相关的包。
    - `total_scanned_rows`：已扫描的行总数。如果存在多个版本的更新或删除（MVCC），每个版本都单独计数。
    - `total_skipped_rows`：被跳过的行总数。
    - `total_rs_index_load_time`：读取 DTFile 粗集索引的总耗时。
    - `total_read_time`：读取 DTFile 数据的总耗时。
+ `total_create_snapshot_time`：在表扫描过程中创建快照的总耗时。

### lock_keys 执行信息

当在悲观事务中执行 DML 语句时，操作符的执行信息可能还会包含 `lock_keys` 的执行信息，例如：

```
lock_keys: {time:94.096168ms, region:6, keys:8, lock_rpc:274.503214ms, rpc_count:6}
```

- `time`：执行 `lock_keys` 操作的总耗时。
- `region`：涉及的 Region 数量。
- `keys`：需要加锁的 Key 数量。
- `lock_rpc`：向 TiKV 发送 `Lock` 类型 RPC 请求的总耗时。由于可以并行发送多个 RPC 请求，实际总 RPC 时间可能大于 `lock_keys` 的总耗时。
- `rpc_count`：发送的 `Lock` 类型 RPC 请求总数。

### commit_txn 执行信息

当在自动提交（`autocommit=1`）事务中执行写操作的 DML 语句时，写操作的执行信息还会包含事务提交的耗时信息，例如：

```
commit_txn: {prewrite:48.564544ms, wait_prewrite_binlog:47.821579, get_commit_ts:4.277455ms, commit:50.431774ms, region_num:7, write_keys:16, write_byte:536}
```

- `prewrite`：事务的 2PC 提交中的 `prewrite` 阶段耗时。
- `wait_prewrite_binlog`：等待写入预写二进制日志的耗时。
- `get_commit_ts`：获取事务提交时间戳的耗时。
- `commit`：事务 2PC 提交中的 `commit` 阶段耗时。
- `write_keys`：事务中写入的总 Key 数。
- `write_byte`：事务中写入的总字节数（单位：字节）。

### RU（Request Unit）消耗

[Request Unit (RU)](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) 是系统资源的统一抽象单位，由 TiDB 资源控制定义。顶层操作符的 `execution info` 展示了该 SQL 语句的整体 RU 消耗。

```
RU:273.842670
```

> **注意：**
>
> 该值显示此次执行实际消耗的 RU 数量。由于缓存（例如 [coprocessor cache](/coprocessor-cache.md)）的影响，同一 SQL 语句每次执行可能会消耗不同的 RU 数量。

你可以通过 `EXPLAIN ANALYZE` 中的其他值，特别是 `execution info` 列，计算 RU。例如：

```json
'executeInfo':
   time:2.55ms, 
   loops:2, 
   RU:0.329460, 
   Get:{
       num_rpc:1,
       total_time:2.13ms
   }, 
   total_process_time: 231.5µs,
   total_wait_time: 732.9µs, 
   tikv_wall_time: 995.8µs,
   scan_detail: {
      total_process_keys: 1, 
      total_process_keys_size: 150, 
      total_keys: 1, 
      get_snapshot_time: 691.7µs,
      rocksdb: {
          block: {
              cache_hit_count: 2,
              read_count: 1,
              read_byte: 8.19 KB,
              read_time: 10.3µs
          }
      }
  },
```

基础成本定义在 [`tikv/pd` 源码](https://github.com/tikv/pd/blob/aeb259335644d65a97285d7e62b38e7e43c6ddca/client/resource_group/controller/config.go#L58C19-L67)，计算在 [`model.go`](https://github.com/tikv/pd/blob/54219d649fb4c8834cd94362a63988f3c074d33e/client/resource_group/controller/model.go#L107) 文件中。

如果你使用 TiDB v7.1，计算方式为 `pd/pd-client/model.go` 中的 `BeforeKVRequest()` 和 `AfterKVRequest()` 之和，即：

```
在处理键值请求之前：
      consumption.RRU += float64(kc.ReadBaseCost) -> kv.ReadBaseCost * rpc_nums

在处理键值请求之后：
      consumption.RRU += float64(kc.ReadBytesCost) * readBytes -> kc.ReadBytesCost * total_process_keys_size
      consumption.RRU += float64(kc.CPUMsCost) * kvCPUMs -> kc.CPUMsCost * total_process_time
```

对于写入和批量获取，计算类似，但基础成本不同。

### 其他常用执行信息

Coprocessor 操作符通常包含两部分执行时间信息：`cop_task` 和 `tikv_task`。`cop_task` 是 TiDB 记录的时间，从请求发出到收到响应的时间；`tikv_task` 是 TiKV Coprocessor 自身记录的时间。如果两者差异较大，可能意味着等待响应的时间过长，或者 gRPC 或网络的耗时较长。

## MySQL 兼容性

`EXPLAIN ANALYZE` 是 MySQL 8.0 的特性，但在 TiDB 中，输出格式和潜在的执行计划与 MySQL 孙差异很大。

## 相关链接

* [Understanding the Query Execution Plan](/explain-overview.md)
* [EXPLAIN](/sql-statements/sql-statement-explain.md)
* [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md)
* [TRACE](/sql-statements/sql-statement-trace.md)