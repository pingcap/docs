---
title: system_history.profile_history
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.764"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='PROFILE HISTORY'/>

**Query performance deep-dive analytics** - Detailed execution profiles and statistics for every SQL query. Essential for:

- **Performance Optimization**: Identify bottlenecks and optimize slow queries
- **Resource Planning**: Understand memory, CPU, and I/O usage patterns
- **Execution Analysis**: Analyze query plans and execution statistics
- **Capacity Management**: Monitor resource consumption trends over time

## Fields


| Field           | Type      | Description                                                                 |
|-----------------|-----------|-----------------------------------------------------------------------------|
| timestamp       | TIMESTAMP | The timestamp when the profile was recorded                                 |
| query_id        | VARCHAR   | The ID of the query associated with this profile                            |
| profiles        | VARIANT   | A JSON object containing detailed execution profile information             |
| statistics_desc | VARIANT   | A JSON object describing statistics format                                  |



## Examples

The `profiles` field can be used to extract specific information. For example, to get the `OutputRows` value for every physical plan, the following query can be used:
```sql
SELECT jq('[.[] | {id, output_rows: .statistics[4]}]', profiles ) AS result FROM system_history.profile_history LIMIT 1;

*************************** 1. row ***************************
result: [{"id":0,"output_rows":1},{"id":3,"output_rows":8},{"id":1,"output_rows":1},{"id":2,"output_rows":1}]
```
