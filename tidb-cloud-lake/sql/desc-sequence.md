---
title: DESC SEQUENCE
sidebar_position: 4
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.742"/>

Describes the properties of a sequence.

## Syntax

```sql
DESC SEQUENCE <sequence_name>
```

| Parameter      | Description                                                                                                                 |
|----------------|-----------------------------------------------------------------------------------------------------------------------------|
| sequence_name  | The name of the sequence to describe. This will display all properties of the sequence including start value, interval, current value, creation timestamp, last update timestamp, and any comment. |

## Examples

```sql
-- Create a sequence
CREATE SEQUENCE seq;

-- Use the sequence in an INSERT statement
CREATE TABLE tmp(a int, b uint64, c int);
INSERT INTO tmp select 10,nextval(seq),20 from numbers(3);

-- Describe the sequence
DESC SEQUENCE seq;

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  name  │  start │ interval │ current │         created_on         │         updated_on         │      comment     │
├────────┼────────┼──────────┼─────────┼────────────────────────────┼────────────────────────────┼──────────────────┤
│ seq    │      1 │        1 │       4 │ 2025-05-20 02:48:49.749338 │ 2025-05-20 02:49:14.302917 │ NULL             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯