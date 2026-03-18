---
title: SET
summary: Changes the value of a system setting for the current session. To show all the current settings, use SHOW SETTINGS.
---

# SET

Changes the value of a system setting for the current session. To show all the current settings, use [SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md).

See also:
- [SETTINGS Clause](/tidb-cloud-lake/sql/settings-clause.md)
- [SET_VAR](/tidb-cloud-lake/sql/set-var.md)
- [UNSET](/tidb-cloud-lake/sql/unset.md)

## Syntax

```sql
SET [ SESSION | GLOBAL ] <setting_name> = <new_value>
```

| Parameter | Description                                                                                                                                                                                     |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SESSION   | Applies the setting change at the session level. If omitted, it applies to the session level by default.                                                                                        |
| GLOBAL    | Applies the setting change at the global level, rather than just the current session. For more information about the setting levels, see  [Setting Levels](/tidb-cloud-lake/sql/show-settings.md#setting-levels). |

## Examples

The following example sets the `max_memory_usage` setting to `4 GB`:

```sql
SET max_memory_usage = 1024*1024*1024*4;
```

The following example sets the `max_threads` setting to `4`:

```sql
SET max_threads = 4;
```

The following example sets the `max_threads` setting to `4` and changes it to be a global-level setting:

```sql
SET GLOBAL max_threads = 4;
```
