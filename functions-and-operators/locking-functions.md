---
title: Locking Functions
summary: Learn about user-level locking functions in TiDB.
---

# Locking Functions

TiDB supports most of the user-level [locking functions](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html) available in MySQL 5.7.

## Supported functions

| Name                                                                                                                 | Description                                       |
|:---------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------|
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_get-lock)    | Acquire an advisory lock                          |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_release-lock)     | Release a previously acquired lock                |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_release-all-locks)   | Release all locks held by the current session     |

## MySQL compatibility

* The maximum timeout permitted by TiDB is 1 hour. This differs from MySQL, where the timeout is unlimited.
* TiDB does not automatically detect deadlocks in user-level locks. Deadlocked sessions will timeout after a maximum of 1 hour, but can also be manually resolved by using `KILL` on one of the affected sessions. Deadlocks can also be prevented by always acquiring user-locks in the same order.

## Unsupported functions

* `IS_FREE_LOCK()`
* `IS_USED_LOCK()`
