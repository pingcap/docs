---
title: SYSTEM$FUSE_AMEND
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.609"/>

Recovers table data from S3-compatible object storage.

## Syntax

```sql
CALL SYSTEM$FUSE_AMEND('<database_name>', '<table_name>');
```

## Examples

This function is designed for fail-safe scenarios. See the [Fail-Safe Guide](/guides/security/fail-safe) for details.