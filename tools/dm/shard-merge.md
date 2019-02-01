---
title: Merging and Synchronizing Data from Sharded Tables in DM
summary: Learn how to merge and synchronize data from sharded tables in DM.
category: tools
---

# Merging and Synchronizing Data from Sharded Tables in DM

DM allows you to synchronize tables with the same structure in the upstream MySQL/MariaDB instances into one table in the downstream TiDB. It supports not only the synchronization of DML statements in the upstream, but also the coordination of synchronizing multiple upstream sharding DDL statements that alter the table structure.

In order to merge the sharded tables, you must set the parameter `is-sharding: true` in the task configuration file.

### Restrictions

DM has the following sharding DDL usage restrictions:

- In a logical sharding group (made up of all sharded tables that need to be merged and synchronized into one downstream table), all upstream sharded tables must execute the same DDL statements in the same order (the schema name and the table name can be different).
    - For example, if you add `column A` to the `table_1` before you add `column B`, then you cannot add `column B` to the `table_2` before you add `column A`. Executing the DDL statements in a different order is not supported.
- If multiple sharding groups exist in a task, you must wait for one sharding group to finish synchronizing the DDL statement, and then start to execute the DDL to other sharding groups.
    - For each sharding group, it is recommended to use one independent task to perform the synchronization.
- In a sharding group, all upstream sharded tables should execute the corresponding DDL statement.
    - For example, if DDL statements are not executed on one or more upstream sharded tables corresponding to `DM-worker-2`, then other DM-workers that have executed the DDL will pause their synchronization task and wait for `DM-worker-2` to receive the upstream DDL.
- Only after one DDL operation is completed in the whole sharding group, this group can execute the next DDL statement.
- The synchronization task of the sharding group does not support `DROP DATABASE/DROP TABLE`.
    - The upstream sharded tables will ignore the `DROP DATABASE/DROP TABLE` statement automatically.
- The synchronization task of the sharding group supports `RENAME TABLE`, but with the following limits:
    - A table can only be renamed to a new name that is not used by any other table.
    - A single `RENAME TABLE` statement can only involve a single `RENAME` operation. (Online DDL is supported in another solution) 
- At the starting point of the incremental synchronization task, the structure of each sharded table should be the same, so as to make sure that DML statements of different sharded tables can be synchronized into the downstream with a certain table structure, and the subsequent sharding DDL can be correctly matched and synchronized.
- If you need to change [table router](../features/table-route.md) rules, you have to wait for the synchronization of all sharding DDL to complete.
    - During the synchronization of the sharding DDL, it will report errors if you use `dmctl` to change `router-rules`.
- If you need to `CREATE` a new table to a sharding group that is executing the DDL, you have to make sure that the table structure is the same as the newly altered table structure.
    - For example, the original `table_1` and `table_2` has two columns (a, b) initially, and has three columns (a, b, c) after the sharding DDL, so after the synchronization the newly created table should also have three columns (a, b, c).
- As the DM-worker that has received the DDL will pause the task to wait for other DM-workers to receive their DDL, it will increase the delay of data synchronization.

### Background

Currently, DM adopts the binlog in the `ROW` format to perform the synchronization task. The binlog does not contain the table structure information. When you use the Row binlog to synchronize, if you have not synchronized the upstream tables into the same downstream table, then there only exists DDL operations of one upstream table that can update the structure of the downstream table. The Row binlog can be considered to have the nature of self-description. During the synchronization process, the DML statements can be constructed accordingly with the column values and the downstream table structure.  

However, in the process of merging and synchronizing sharded tables, if DDL statements are executed on the upstream tables to alter the table structure, then you should perform extra operations to synchronize the DDL and thus avoid the inconsistency between the DML statements produced by the column values and the actual downstream table structure.

Here is a simple example: 

![shard-ddl-example-1](../media/shard-ddl-example-1.png)

In this example, we simplify the merging process, in which there are only two MySQL instances in the upstream and each instance has only one table. Assume that when the synchronization begins, we mark the schema version of two sharded tables as `schema V1`, and mark the schema version after executing DDL statements as `schema V2`. 

Now suppose that in the synchronization process, the binlog data received from the two upstream sharded tables has the following time sequence:
1. When the synchronization begins, the syncer unit in DM-worker can only receive the DML events of `schema V1` from the two sharded tables. 
2. At `t1`, the sharding DDL events from the instance 1 are received. 
3. From `t2` on, the syncer unit receives the DML of `schema V2` from the instance 1; but from the instance 2, it still receives the DML of `schema V1`. 
4. At `t3`, the sharding DDL events from the instance 2 are received. 
5. From `t4` on, the syncer unit receives the DML of `schema V2` from the instance 2 as well. 

Suppose that we do no operation to the DDL of the sharded tables during the synchronization process. After DDL statements of the instance 1 are synchronized to the downstream, the downstream table structure will be altered into `schema V2`. But for the instance 2, the syncer unit in DM-worker is still receiving DML events of `schema V1` from `t1` to `t2`. Therefore, in the process of synchronizing the DML of `schema V1` to the downstream, the inconsistency between the DML and the table structure might lead to errors and failure to synchronize the data. 

### Principles

To show you how DM synchronizes the DDL statements in the process of merging tables, here is an example:

![shard-ddl-flow](../media/shard-ddl-flow.png)

In this example, `DM-worker-1` synchronizes the data from MySQL instance 1 and `DM-worker-2` synchronizes the data from MySQL instance 2. `DM-master` coordinates the DDL synchronization among multiple DM-workers. After `DM-worker-1` receives the DDL, the simplified processes of synchronizing the DDL are as follows:

1. `DM-worker-1` receives the DDL from MySQL instance 1 at `t1`, pauses the data synchronization of the corresponding DDL and DML, and sends the DDL information to `DM-master`. 
2. `DM-master` decides if the synchronization of this DDL needs to be coordinated based on the received DDL information, creates a lock for the DDL, sends the DDL lock information back to `DM-worker-1` and marks `DM-worker-1` as the owner of this lock at the same time. 
3. `DM-worker-2` continues synchronizing the DML until it receives the DDL from MySQL instance 2 at `t3`, pauses the data synchronization of the DDL, and sends the DDL information to `DM-master`.
4. `DM-master` decides if the lock of this DDL exists based on the received DDL information, and sends the lock information directly to `DM-worker-2`.
5. Based on the information such as the configuration information when the task begins, the information of sharded tables in the upstream MySQL instance and the deployment topology information, `DM-master` decides if it has received the DDL of all upstream sharded tables to be merged, and asks the owner of the DDL lock (`DM-worker-1`) to execute the DDL to downstream.
6. `DM-worker-1` verifies the DDL execution request based on the DDL lock information received at step 2; executes the DDL to the downstream, and sends the results to `DM-master`; If the execution is successful, `DM-worker-1` continues synchronizing the subsequent (from the binlog at `t2`) DML.
7. `DM-master` receives the response from the lock owner that the DDL is successfully executed, and asks all other DM-workers (`DM-worker-2`) that are waiting for the DDL lock to ignore the DDL and then continue to synchronize the subsequent (from the binlog at `t4`) DML. 

We can conclude some characteristics of how DM coordinates the sharding DDL synchronization among multiple DM-workers: 

- Based on the task configuration and DM cluster deployment topology information, we build a logical sharding group in `DM-master` that coordinates DDL synchronization of each group member (that is, the DM-worker who handles each sub-task into which the synchronization task is divided).
- After receiving the DDL from the binlog event, each DM-worker sends the DDL information to `DM-master`. 
- `DM-master` creates/updates the DDL lock based on the DDL information from each DM-worker and the sharding group information.
- If all members of the sharding group receive a specific DDL, this indicates that all DML statements before the DDL execution on the upstream sharded tables have been synchronized; that the DDL can be executed and the subsequent DML can be synchronized. 
- After being converted by the [table router](../features/table-route.md), the DDL of the upstream sharded tables should be consistent with the DDL to be executed in the downstream. Therefore, this DDL only needs to be executed once by the DDL owner and all other DM-workers can ignore this DDL.

In the above example, there is only one sharded table to be merged in the upstream MySQL instance that each DM-worker corresponds to. But in actual scenarios, there might be multiple sharded tables in multiple sharded schemas to be merged in one MySQL instance. And when this happens, it becomes more complex to coordinate the sharding DDL synchronization.

Suppose that there are two sharded tables `table_1` and `table_2` to be merged in one MySQL instance:

![shard-ddl-example-2](../media/shard-ddl-example-2.png)

Because data comes from the same MySQL instance, all the data is obtained from the same binlog flow. In this case, the time sequence is as follows:

1.  The syncer unit in DM-worker receives the DML of `schema V1` from both sharded tables when the synchronization begins. 
2. At `t1`, it receives the DDL of `table_1`.
3. From `t2` to `t3`, the received data includes the DML of `schema V2` from `table_1` and the DML of `schema V1` from `table_2`.
4. At `t3`, it receives the DDL of `table_2`.
5. From `t4` on, it receives the DML of `schema V2` from both tables.

If we do no special operations to the DDL during the data synchronization, when the DDL of `table_1` is synchronized to the downstream and alters the downstream table structure, the DML of `schema V1` from `table_2` will not be synchronized normally. Therefore, within a single DM-worker, we have created a logical sharding group which is similar to that within `DM-master`, except that members of this group are the different sharded tables in the same upstream MySQL instance.  

But when a DM-worker coordinates the synchronization of the sharding group within itself, it is not entirely same as that performed by `DM-master`. The reasons are:

- When the DM-worker receives the DDL of `table_1`, it can not pause the synchronization and needs to continue parsing binlog to get the subsequent DDL of `table_2`, that is, it needs to continue parsing from `t2` to `t3`. 
- During the binlog parsing from `t2` to `t3`, the DML of `schema V2` from `table_1` cannot be synchronized to the downstream until the sharding DDL is synchronized and successfully executed. 

In DM, a simplified synchronization process of the sharding DDL within the DM worker is as below:

1. When receiving the DDL of `table_1` at `t1`, the DM-worker records the DDL information and the current position of the binlog.
2. Continue parsing the binlog from `t2` to `t3`.
3. Ignore the DML of `schema V2` if it belongs to `table_1`. Synchronize the DML of `schema V1` to the downstream if it belongs to `table_2`.
4. When receiving the DDL of `table_2` at `t3`, the DM-worker records the DDL information and the current position of the binlog.
5. Based on the information of the synchronization task configurations and the upstream schemas and tables, the DM-worker confirms if the DDL of all sharded tables in the MySQL instance have been received. If all DDL statements have been received, synchronize them to the downstream, and execute them to alter the downstream table structures.
6. Set the starting point of parsing the new binlog flow to be the position saved at step 1.
7. Resume parsing the binlog from `t2` to `t3`.
8. Synchronize the DML of `schema V2` to the downstream if it belongs to `table_1`. Ignore the DML of `schema V1` if it belongs to `table_2`.
9. After parsing the binlog position saved at step 4, the DM-worker knows that all DML statements that have been ignored in step 3 have been synchronized to the downstream again.
10. Resume the synchronization from the binlog position at `t4`.

You can conclude from the above analysis that DM mainly uses two-level sharding groups for coordination and control when handling synchronization of the sharding DDL. Here is the simplified process:

1. Each DM-worker independently coordinates the DDL synchronization for the corresponding sharding group made of multiple sharded tables within the upstream MySQL instance.
2. After the DM-worker receives the DDL statements of all sharding tables, it sends the DDL information to `DM-master`.
3. `DM-master` coordinates the DDL synchronization of the sharding group made of the DM-workers based on the received DDL information.
4. After receiving the DDL information from all DM-workers, `DM-master` asks the DDL lock owner (a specific DM-worker) to execute the DDL.
5. The DDL lock owner executes the DDL and returns the result to `DM-master`. Then the owner restarts the synchronization of the previously ignored DML during the internal coordination of DDL synchronization.
6. After `DM-master` confirms that the owner has successfully executed the DDL, it asks all other DM-workers to continue with the synchronization.
7. All other DM-workers separately restart the synchronization of the previously ignored DML during the internal coordination of DDL synchronization.
8. After finishing re-synchronizing the ignored DML, all DM-workers resumes the normal synchronization process.
