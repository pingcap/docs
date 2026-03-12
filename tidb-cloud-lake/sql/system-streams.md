---
title: system.streams
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.223"/>

Provides information about streams in the system. Each row in this table corresponds to a stream, and the columns contain details such as the stream's mode, comment (if any), associated table name, table ID, table version, snapshot location, invalid reason (if applicable), and owner. 

```sql title="Example:"
SELECT * FROM system.streams;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ catalog │   database  │  name  │ stream_id │         created_on         │         updated_on         │     mode    │      comment     │   table_name  │ table_id │ table_version │                   snapshot_location                   │ invalid_reason │       owner      │
├─────────┼─────────────┼────────┼───────────┼────────────────────────────┼────────────────────────────┼─────────────┼──────────────────┼───────────────┼──────────┼───────────────┼───────────────────────────────────────────────────────┼────────────────┼──────────────────┤
│ default │ test_stream │ s      │      3290 │ 2023-11-28 16:27:16.404667 │ 2023-11-28 16:37:15.761127 │ append_only │                  │ test_stream.t │     3272 │          3342 │ 3264/3272/_ss/f143831d621c4c7a80f782a5f2ee2338_v4.mpk │                │ NULL             │
│ default │ test_stream │ s1     │      3300 │ 2023-11-28 16:28:12.381539 │ 2023-11-28 16:28:12.381539 │ append_only │                  │ test_stream.t │     3272 │          3298 │ 3264/3272/_ss/6e6a0a94b2a344e3b7eeff16fe6996dc_v4.mpk │                │ NULL             │
│ default │ test_stream │ s2     │      3318 │ 2023-11-28 16:33:17.195153 │ 2023-11-28 16:33:17.195154 │ append_only │ this is a stream │ test_stream.t │     3272 │          3282 │ 3264/3272/_ss/a746f1cdbea84a3a91510a7118475b7d_v4.mpk │                │ NULL             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```