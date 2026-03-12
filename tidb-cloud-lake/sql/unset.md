---
title: UNSET
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.605"/>

Reverts one or more system settings to their global or default levels and values. For more information about the setting levels, see [Setting Levels](03-show-settings.md#setting-levels). To show all the current settings, use [SHOW SETTINGS](03-show-settings.md).

See also: [SET](02-set-global.md)

## Syntax

```sql
-- Unset one setting
UNSET [ SESSION | GLOBAL ] <setting_name> 

-- Unset multiple settings
UNSET [ SESSION | GLOBAL ] ( <setting_name>, <setting_name> ... )
```

| Parameter | Description                                                                                                                                                                                         |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SESSION   | If the setting has a global-level value, it removes the session-level override and reverts to the global setting. If the setting only has a session-level value, it reverts to the default setting. |
| GLOBAL    | Removes the global-level setting and reverts it to the default-level value.                                                                                                                         |


:::warning[CAUTION]

| Databend-Query Version | Description                                                                    |
|------------------------|--------------------------------------------------------------------------------|
| [-∞, v1.2.605)         | In default, `UNSET <setting_name>` is equal to `UNSET GLOBAL <setting_name>`.  |
| [v1.2.605, +∞]         | In default, `UNSET <setting_name>` is equal to `UNSET SESSION <setting_name>`. |

:::

## Examples

This example uses `UNSET GLOBAL` to remove the global-level setting for timezone, reverting it back to its default value and level:

```sql
SHOW SETTINGS LIKE 'timezone';

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │  value │ default │                                range                                │  level  │     description    │  type  │
├──────────┼────────┼─────────┼─────────────────────────────────────────────────────────────────────┼─────────┼────────────────────┼────────┤
│ timezone │ UTC    │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ DEFAULT │ Sets the timezone. │ String │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Sets timezone to 'Asia/Shanghai' at global level
SET GLOBAL timezone = 'Asia/Shanghai';
SHOW SETTINGS LIKE 'timezone';

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │     value     │ default │                                range                                │  level │     description    │  type  │
├──────────┼───────────────┼─────────┼─────────────────────────────────────────────────────────────────────┼────────┼────────────────────┼────────┤
│ timezone │ Asia/Shanghai │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ GLOBAL │ Sets the timezone. │ String │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Removes the global-level setting for timezone
UNSET GLOBAL timezone;
SHOW SETTINGS LIKE 'timezone';

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │  value │ default │                                range                                │  level  │     description    │  type  │
├──────────┼────────┼─────────┼─────────────────────────────────────────────────────────────────────┼─────────┼────────────────────┼────────┤
│ timezone │ UTC    │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ DEFAULT │ Sets the timezone. │ String │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example uses UNSET SESSION to remove the session-level setting for timezone, reverting it back to the global-level setting:

```sql
SHOW SETTINGS LIKE 'timezone';

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │  value │ default │                                range                                │  level  │     description    │  type  │
├──────────┼────────┼─────────┼─────────────────────────────────────────────────────────────────────┼─────────┼────────────────────┼────────┤
│ timezone │ UTC    │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ DEFAULT │ Sets the timezone. │ String │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Sets timezone to 'Asia/Shanghai' at global level
SET GLOBAL timezone = 'Asia/Shanghai';
SHOW SETTINGS LIKE 'timezone';
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │     value     │ default │                                range                                │  level │     description    │  type  │
├──────────┼───────────────┼─────────┼─────────────────────────────────────────────────────────────────────┼────────┼────────────────────┼────────┤
│ timezone │ Asia/Shanghai │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ GLOBAL │ Sets the timezone. │ String │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Set timezone to 'America/Santiago' in current session
SET timezone = 'America/Santiago';
SHOW SETTINGS LIKE 'timezone';
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │       value      │ default │                                range                                │  level  │     description    │  type  │
├──────────┼──────────────────┼─────────┼─────────────────────────────────────────────────────────────────────┼─────────┼────────────────────┼────────┤
│ timezone │ America/Santiago │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ SESSION │ Sets the timezone. │ String │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

UNSET SESSION timezone;
SHOW SETTINGS LIKE 'timezone';

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │     value     │ default │                                range                                │  level │     description    │  type  │
├──────────┼───────────────┼─────────┼─────────────────────────────────────────────────────────────────────┼────────┼────────────────────┼────────┤
│ timezone │ Asia/Shanghai │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ GLOBAL │ Sets the timezone. │ String │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example uses UNSET SESSION to remove the session-level setting for timezone, reverting it back to the session-level setting:

```sql
SHOW SETTINGS LIKE 'timezone';

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │     value     │ default │                                range                                │  level │     description    │  type  │
├──────────┼───────────────┼─────────┼─────────────────────────────────────────────────────────────────────┼────────┼────────────────────┼────────┤
│ timezone │ Asia/Shanghai │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ GLOBAL │ Sets the timezone. │ String │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

UNSET timezone;

SHOW SETTINGS LIKE 'timezone';

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name   │  value │ default │                                range                                │  level  │     description    │  type  │
├──────────┼────────┼─────────┼─────────────────────────────────────────────────────────────────────┼─────────┼────────────────────┼────────┤
│ timezone │ UTC    │ UTC     │ ["Africa/Abidjan", "Africa/Accra", "Africa/Addis_Ababa", "Africa... │ DEFAULT │ Sets the timezone. │ String │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```