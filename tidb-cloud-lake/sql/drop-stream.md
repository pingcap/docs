---
title: DROP STREAM
summary: Deletes an existing stream.
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.223"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='STREAM'/>

Deletes an existing stream.

## Syntax

```sql
DROP STREAM [ IF EXISTS ] [ <database_name>. ]<stream_name>
```

## Examples

```sql
DROP STREAM books_stream_2023;
```