---
title: String
description: Basic String data type.
sidebar_position: 3
---

## String Data Types

In Databend, strings can be stored in the `VARCHAR` field, the storage size is variable.

| Name    | Aliases | Storage Size |
|---------|---------|--------------|
| VARCHAR | STRING  | variable     |

## Functions

See [String Functions](/sql/sql-functions/string-functions).


## Example

```sql
CREATE TABLE string_table(text VARCHAR);
```

```
DESC string_table;
```
Result:
```
┌──────────────────────────────────────────────┐
│  Field │   Type  │  Null  │ Default │  Extra │
├────────┼─────────┼────────┼─────────┼────────┤
│ text   │ VARCHAR │ YES    │ NULL    │        │
└──────────────────────────────────────────────┘
```

```sql
INSERT INTO string_table VALUES('databend');
```

```
SELECT * FROM string_table;
```
Result:
```
┌──────────────────┐
│       text       │
├──────────────────┤
│ databend         │
└──────────────────┘
```
