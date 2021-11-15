---
title: Online Unsafe Recovery
summary: Learn how to use online unsafe recovery.
---

# Online Unsafe Recovery

> **Warning:**
>
> - This feature is a lossy recovery, so TiKV cannot guarantee data integrity and data indexes integrity after using the feature.
> - Online Unsafe Recovery is an experimental feature, and it is **NOT** recommended to use it in the production environment. The interface, strategy, and internal implementation of this feature might change when it becomes generally available (GA). Although this feature has been tested in some scenarios, it is not thoroughly validated and might cause system unavailability.
> - It is recommended to perform the feature-related operations with the support from the TiDB team. If any misoperation is performed, it might be hard to recover the cluster.

When permanently damaged replicas cause part of data on TiKV to be unreadable and unwritable, you can use the Online Unsafe Recovery feature to perform a lossy recovery operation.

## Feature description

In TiDB, data might be replicated in many stores at the same time according to the Placements Rules defined by users. This guarantees that data is still readable and writable even if a single or a few stores are temporarily offline or damaged. However, when most or all replicas of a Region are offline at the same time, the Region becomes temporarily unavailable, by design, to ensure data integrity.

Suppose that multiple replicas of data encounter problems like permanent damage (such as disk damage), and this issue causes stores to fail to go online. In this case, this data is temporarily unavailable. Provided that you can accept data rewind or data loss, if you want the cluster back in use under this circumstance, TiDB can theoretically re-form the majority of replicas by manually overwriting the meta information of data shards. This allows application layer services to read and write (might be stale or empty) this data.

In this case, if some stores with loss-tolerating data are permanently damaged, you can easily perform a lossy recovery operation by using online unsafe recovery. Using this feature, PD, under its global perspective, collects the meta information of data shards in all stores and generates a more real-time and more complete recovery plan. Then, PD distributes the plan to each surviving store to make the stores perform data recovery tasks. Also, after the data recovery plan is distributed, PD periodically checks the recovery progress to ensure that the current state of the cluster matches its expected state.

## User scenarios

The Online Unsafe Recovery feature is suitable for the following scenarios:

* The data for application services is unreadable and unwritable, because permanently damaged stores cause the stores to fail to restart.
* You can accept data loss and want the affected data to be readable and writable.
* You want to perform a one-stop online data recovery operation.

## Usage

### Prerequisites

Before using Online Unsafe Recovery, make sure that the following requirements are met:

* Part of data is indeed unavailable.
* The offline stores cannot be automatically recovered or restarted.

### Step 1. Disable all types of scheduling

You need to temporarily disable all types of internal scheduling, such as load balancing. After disabling them, it is recommended to wait for about 10 minutes so that the triggered scheduling can have sufficient time to complete the scheduled tasks.

> **Note:**
>
> After the scheduling is disabled, the system cannot resolve data hotspot issues. Therefore, you need to enable the scheduling as soon as possible after the recovery is completed.

1. Use pd-ctl to view the current configuration by running the [`config show`](/pd-control.md#config-show--set-option-value--placement-rules) command.
2. Use pd-ctl to disable all types of scheduling, for example:

    * [`config set region-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)
    * [`config set replica-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)
    * [`config set merge-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)

### Step 2. Remove the stores that cannot be automatically recovered

Use pd-ctl to remove the stores that cannot be automatically recovered by running the [`unsafe remove-failed-stores <store_id>[,<store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show--history) command.

> **Note:**
>
> The successful return of this command only indicates that the request is accepted, not that the recovery is completed successfully. The stores are actually recovered in the background.

### Step 3. Check the progress

When the above store removal command runs successfully, you need to use pd-ctl to check the removal progress by running the [`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules) command. When the command result shows "Last recovery has finished", the system recovery is completed.

### Step 4. Test read and write tasks

After the progress command shows that the recovery task is completed, you can try to execute some simple SQL queries like the following example or perform write tasks to ensure that the data is readable and writable.

```sql
select count(*) from table_that_suffered_from_group_majority_failure;
```

> **Note:**
>
> The situation that data can be read and written does not indicate there is no data loss.

### Step 5. Restart the scheduling

To restart the scheduling, you need to adjust the value of `config set region-schedule-limit 0`, `config set replica-schedule-limit 0`, `config set merge-schedule-limit 0` modified in step 1 to the initial values.

Then, the whole process is finished.