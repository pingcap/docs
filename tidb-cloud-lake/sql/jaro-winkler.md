---
title: JARO_WINKLER
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.675"/>

Calculates the [Jaro-Winkler distance](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) between two strings. It is commonly used for measuring the similarity between strings, with values ranging from 0.0 (completely dissimilar) to 1.0 (identical strings). 

## Syntax

```sql
JARO_WINKLER(<string1>, <string2>)
```

## Return Type

The JARO_WINKLER function returns a FLOAT64 value representing the similarity between the two input strings. The return value follows these rules:

- Similarity Range: The result ranges from 0.0 (completely dissimilar) to 1.0 (identical).

    ```sql title='Examples:'
    SELECT JARO_WINKLER('databend', 'Databend') AS similarity;

    ┌────────────────────┐
    │     similarity     │
    ├────────────────────┤
    │ 0.9166666666666666 │
    └────────────────────┘

    SELECT JARO_WINKLER('databend', 'database') AS similarity;

    ┌────────────┐
    │ similarity │
    ├────────────┤
    │        0.9 │
    └────────────┘
    ```
- NULL Handling: If either string1 or string2 is NULL, the result is NULL.

    ```sql title='Examples:'
    SELECT JARO_WINKLER('databend', NULL) AS similarity;

    ┌────────────┐
    │ similarity │
    ├────────────┤
    │ NULL       │
    └────────────┘
    ```
- Empty Strings:
    - Comparing two empty strings returns 1.0.

    ```sql title='Examples:'
    SELECT JARO_WINKLER('', '') AS similarity;

    ┌────────────┐
    │ similarity │
    ├────────────┤
    │          1 │
    └────────────┘
    ```
    - Comparing an empty string with a non-empty string returns 0.0.

    ```sql title='Examples:'
    SELECT JARO_WINKLER('databend', '') AS similarity;

    ┌────────────┐
    │ similarity │
    ├────────────┤
    │          0 │
    └────────────┘
    ```