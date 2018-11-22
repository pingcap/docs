---
title: Handling the Sharding DDL Lock Manually
summary: Learn to manually unlock the sharding DDL lock.
category: tools
---

# Handling the Sharding DDL Lock Manually

This document shows how to manually unlock the sharding DDL lock in different cases.

Generally, the sharding DDL lock synchronization of DM can be completed automatically. But when some abnormality happens, you need to use `unlock-ddl-lock`/`break-ddl-lock` to unlock the abnormal DDL lock manually.

The possible causes of an abnormality include:

- Some DM-workers go offline
- Some DM-worker restarts (or is unreachable temporarily)
- DM-master restarts

> **Note:** You can use `unlock-ddl-lock`/`break-ddl-lock` only when you are definitely clear about the possible impacts brought by this command and you can accept the impacts.

## Case one: some DM-workers go offline

Before DM-master tries to automatically unlock the sharding DDL lock, all the DM-workers need to receive the sharding DDL event. If the sharding DDL operation is already in the synchronization process, and some DM-workers have gone offline and are not to be restarted, the sharding DDL lock cannot be automatically synchronized and unlocked since not all the DM-workers can receive the DDL event.

If you do not need to make some DM-workers offline in the synchronization process of the sharding DDL operation, a better policy is to use `stop-task` to stop the running task first, then make some DM-workers offline, and finally use `start-task` and the **new task configuration** that does not contain the already offline DM-worker to restart the task.

If the owner has finished the DDL operation but other DM-workers have not skipped this DDL operation, the owner has gone offline. For the solution, see [Case two: some DM-worker restarts](#case-two-some-dm-worker-restarts-or-is-unreachable-temporarily).

### Manual solution

1. Run `show-ddl-locks` to obtain the information of the sharding DDL lock that is currently pending synchronization. 

2. Run the `unlock-ddl-lock` command to specify the information of the lock to be unlocked manually.

    - If the owner of this lock is offline, you can configure the `--owner` parameter to specify another DM-worker as the new owner to execute the DDL operation.

3. Run `show-ddl-locks` to check whether this lock has been successfully unlocked.

### Impact

After you have manually unlocked the lock, the lock might not be automatically synchronized when the next sharding DDL event is received, because the configuration information of this task still includes offline DM-workers.

Therefore, after you have manually unlocked the DM-workers, you need to use `stop-task`/`start-task` and the updated task configuration that does not include offline DM-workers to restart the task.

> **Note:** If the DM-workers that went offline go online after you run `unlock-ddl-lock`, it means: These DM-workers will synchronize the unlocked DDL operation again. (Other DM-workers that were not offline have synchronized the DDL operation.)
The DDL operation of these DM-workers will try to match the subsequent synchronized DDL operations of other DM-workers. A match error of synchronizing sharding DDL operations of different DM-workers might occur.

## Case two: some DM-worker restarts (or is unreachable temporarily)

The unlocking operation process of a DM calling multiple DM-workers to execute/skip the sharding DDL operation and update the checkpoint is not atomic. Therefore, a possible case is that after the owner finishes the DDL operation, an non-owner restarts before other DM-workers skip this DDL operation. At this time, the lock information on other DM-masters has been removed but the DM-worker that performs the restart operation has not skipped the DDL operation or updated the checkpoint.

After the DDL task in restarted and `start-task` is performed, the DM-worker that performs the restart operation tries to synchronize this sharding DDL operation. But as other DM-workers have finished synchronizing the DDL operation, the restarted DM-worker cannot synchronize or skip this DDL operation.

### Manual solution

1. Run `query-status` to check the information of the sharding DDL operation that the restarted DM-worker is currently blocking. 

2. Run `break-ddl-lock` to specify the DM-worker that is to break the lock forcefully.
    
    - Configure `skip` to specify the sharding DDL operation to be skipped.

3. Run `query-status` to check whether the lock has been successfully broken.

### Impact

No bad impact. After you have manually broken the lock, the subsequent sharding DDL operation can be automatically synchronized normally.

## Case three: DM-master restarts

After a DM-worker sends the sharding DDL information to DM-master, this DM-worker will hang up, wait for the message from DM-master, and then decide whether to execute or skip this DDL operation.

Because the state of DM-master is not persistent, the lock information that a DM-worker sends to DM-master will be lost if DM-master restarts.

Therefore, DM-master cannot dispatch a DM-worker to execute/skip the DDL operation after DM-master restarts due to lock information loss.

### Manual solution

1. Run `show-ddl-locks` to verify whether the sharding DDL lock information is lost.
2. Run `query-status` to verify whether the DM-worker is blocked as it is waiting for synchronization of the sharding DDL lock.
3. Run `pause-task` to pause the blocked task.
4. Run `resume-task` to resume the blocked task and restart synchronizing the sharding DDL lock.

### Impact

No bad impact. After you have manually paused and resumed the task, the DM-worker resumes synchronizing the sharding DDL lock and sends the lost lock information to DM-master. The subsequent sharding DDL operation can be synchronized normally.

## Parameter description of related commands

### `show-ddl-locks`

- `task-name`: 
    
    - Non-flag parameter, string, optional
    - If not set, no specific task is to be queried; if set, only this task is to be queried.

- `worker`:
    
    - Flag parameter, string array, `--worker`, optional
    - Can be specified repeatedly multiple times.
    - If set, only the DDL lock information that is related to these DM-workers is to be queried.

#### `unlock-ddl-lock`

- `lock-ID`: 

    - Non-flag parameter, string, required
    - Specifies the lock ID of the DDL operation to be unlocked (this ID can be obtained by `show-ddl-locks`)

- `owner`: 
    
    - Flag parameter, string, `--owner`, optional
    - If set, this value should correspond to a DM-worker that executes the DDL operation of the lock instead of the default owner.

- `force-remove`: 
    
    - Flag parameter, boolean, `--force-remove`, optional
    - If set, the lock information is removed even though the owner fails to execute the DDL operation. The owner cannot retry or perform other operations.

- `worker`: 
    
    - Flag parameter, string array, `--worker`, optional
    - Can be specified repeatedly multiple times.
    - If not set, all the DM-workers to receive the lock event execute/skip the DDL operation. If set, only the specified DM-workers execute/skip the DDL operation.

#### `break-ddl-lock`

- `task-name`: 
    
    - Non-flag parameter, string, required
    - Specifies the name for the task that contains the lock to be broken.

- `worker`: 

    - Flag parameter, string, `--worker`, required
    - Only one should be specified.
    - Specifies the DM-worker to break the lock.

- `remove-id`: 

    - Flag parameter, string, `--remove-id`, required
    - If set, the value should be the ID of a DDL lock. Then the information about the DDL lock recorded in the DM-worker is removed.
    
- `exec`: 

    - Flag parameter, boolean, `--exec`, optional
    - If set, a specific DM-worker executes the DDL operation corresponding to the lock.
    - Cannot be specified simultaneously with the `skip` parameter.

- `skip`: 
    
    - Flag parameter, boolean, `--skip`, optional
    - If set, a specific DM-worker skips the DDL operation of the lock.
    - Cannot be specified simultaneously with the `skip` parameter.
