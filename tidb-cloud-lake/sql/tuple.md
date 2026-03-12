---
title: Tuple
description: Tuple is a collection of ordered, immutable types.
sidebar_position: 9
---

## Overview

`TUPLE(T1, T2, …)` stores a fixed ordered list of values with declared element types. Each tuple value can hold heterogeneous data (for example, `TUPLE(DATETIME, STRING)`) and behaves like a compact struct. Because tuples are immutable, insert the entire tuple value whenever you need to change its contents.

## Examples

### Create and Insert

```sql
CREATE TABLE events_tuple (
  event_info TUPLE(DATETIME, STRING)
);

INSERT INTO events_tuple VALUES
  (('2023-02-14 08:00:00', 'Valentine''s Day')),
  (('2023-03-17 19:30:00', 'Game Night'));

SELECT event_info FROM events_tuple;
```

Result:
```
┌──────────────────────────────────────────────────────┐
│ event_info                                           │
├──────────────────────────────────────────────────────┤
│ ["2023-02-14T08:00:00","Valentine's Day"]            │
│ ["2023-03-17T19:30:00","Game Night"]                 │
└──────────────────────────────────────────────────────┘
```

### Access Elements

Tuple fields use 1-based ordinal access (`tuple_column.1`) or aliases when you name the elements.

```sql
-- Ordinal access
SELECT
  event_info.1 AS event_time,
  event_info.2 AS description
FROM events_tuple;
```

Result:
```
┌──────────────────────────┬──────────────────┐
│ event_time               │ description      │
├──────────────────────────┼──────────────────┤
│ 2023-02-14T08:00:00      │ Valentine's Day  │
│ 2023-03-17T19:30:00      │ Game Night       │
└──────────────────────────┴──────────────────┘
```

Tuples are handy when you need to pass grouped values through SQL expressions without introducing additional table columns.
