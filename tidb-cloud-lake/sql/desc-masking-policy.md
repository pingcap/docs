---
title: DESC MASKING POLICY
sidebar_position: 2
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.845"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='MASKING POLICY'/>

Displays detailed information about a specific masking policy in Databend.

## Syntax

```sql
DESC MASKING POLICY <policy_name>
```

## Access Control Requirements

| Privilege | Description |
|:----------|:------------|
| APPLY MASKING POLICY | Required to describe a masking policy unless you own that policy. |

Either the global `APPLY MASKING POLICY` privilege or APPLY/OWNERSHIP on the specific masking policy satisfies this requirement.

## Examples

```sql
CREATE MASKING POLICY email_mask
AS
  (val string)
  RETURNS string ->
  CASE
  WHEN current_role() IN ('MANAGERS') THEN
    val
  ELSE
    '*********'
  END
  COMMENT = 'hide_email';

DESC MASKING POLICY email_mask;

Name       |Value                                                                |
-----------+---------------------------------------------------------------------+
Name       |email_mask                                                           |
Created On |2023-08-09 02:29:16.177898 UTC                                       |
Signature  |(val STRING)                                                         |
Return Type|STRING                                                               |
Body       |CASE WHEN current_role() IN('MANAGERS') THEN VAL ELSE '*********' END|
Comment    |hide_email                                                           |
```
