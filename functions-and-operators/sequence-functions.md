---
title: Sequence Functions
summary: This document introduces sequence functions supported in TiDB.
---

# Sequence Functions

Sequence functions in TiDB are used to return or set values of sequence objects created using the [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) statement.

| Function name | Feature description |
| :-------------- | :------------------------------------- |
| `NEXTVAL` or `NEXT VALUE FOR` | Returns the next value of the sequence |
| `SETVAL` | Sets value of the sequence |
| `LASTVAL` | Returns the last used value of the sequence |

## MySQL compatibility

MySQL does not support the functions and statements for creating and manipulating sequences as defined in [ISO/IEC 9075-2](https://www.iso.org/standard/76584.html).
