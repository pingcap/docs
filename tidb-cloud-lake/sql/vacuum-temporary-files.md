---
title: VACUUM TEMPORARY FILES
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.348"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='VACUUM TEMPORARY FILES'/>

Removes temporary files created by Databend, such as spill files.

See also: [system.temp_files](../../00-sql-reference/31-system-tables/system-temp-files.md)

## Syntax

```sql
VACUUM TEMPORARY FILES [ LIMIT <limit> ]
```

| Parameter | Description                                          |
|-----------|------------------------------------------------------|
| LIMIT     | The maximum number of temporary files to be removed. |

## Output

Returns the number of deleted temporary files.

## Example

```sql
SELECT * FROM system.temp_files;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ file_type │                          file_name                          │ file_content_length │ file_last_modified_time │
├───────────┼─────────────────────────────────────────────────────────────┼─────────────────────┼─────────────────────────┤
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/0tUE8EqsxxjO4ftZA8Zni6 │           591239232 │ 2024-11-19 03:06:03     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/440NKJwbRrW8HCFfQuNmb4 │           607193920 │ 2024-11-19 03:05:18     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/5oQxtCB58oRhTA7EgO3027 │           787631104 │ 2024-11-19 03:04:34     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/7nBLkWobl4jaDQtROAIow1 │           596923264 │ 2024-11-19 03:06:04     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/Dx1xSJ5kv5vZyoWdmSpe32 │           780189824 │ 2024-11-19 03:04:34     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/KSHXnVch2KUbHCqE0rgpx7 │           741196608 │ 2024-11-19 03:05:21     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/O3TvRQja41NrpME8qXjJE3 │           792868608 │ 2024-11-19 03:06:06     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/OMXTEzXmvR5Zw3jk2BVlR5 │           661675392 │ 2024-11-19 03:05:19     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/PkSYoCjNxwDqCwP3k0axs1 │           797124864 │ 2024-11-19 03:04:33     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/Sdr4ew2l60k90e7zZs3mF  │           797046144 │ 2024-11-19 03:05:21     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/TPMpuE1ypRSwRiSx2bRhh6 │           531469504 │ 2024-11-19 03:06:03     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/VdzW61PcSugFIGyCR4B6P6 │           736063616 │ 2024-11-19 03:04:34     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/WcTI2vVUfyzy8XUyjQAhc2 │           791146496 │ 2024-11-19 03:04:34     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/Y6cCfDUkIkeD7Mnm0Zut67 │           738694976 │ 2024-11-19 03:06:05     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/eNACGmJy00y8Pr1xSPCT25 │           790728256 │ 2024-11-19 03:05:21     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/fojFryduQMoru0kAwnzys5 │           795929344 │ 2024-11-19 03:05:20     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/iWcusSG1zW0pnbo76j0vr7 │           797382080 │ 2024-11-19 03:06:04     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/klWl0CxOZQ08IHymUdeHr  │           796787712 │ 2024-11-19 03:04:34     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/kyX7EzdFBOVEBDNwKtexC6 │           743725184 │ 2024-11-19 03:05:20     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/qDOtHrPpdpPPxqqb2Ybht7 │           794764672 │ 2024-11-19 03:04:34     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/qp7GnofqSBZXnJrFuuxqa6 │           797497664 │ 2024-11-19 03:06:02     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/w2qbixYObBOaMlgk7IQms1 │           716091520 │ 2024-11-19 03:06:05     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/xO0ozrAKnq0naJ85BO53I4 │           779609664 │ 2024-11-19 03:04:34     │
│ Spill     │ 1e9411e1-3c2f-48ee-9712-9d3ce396d1b3/xpejvCn9HNGJOc0szcC5b4 │           793506112 │ 2024-11-19 03:05:21     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/2Gk62gm2GgFSLjTIGJbWv6 │           796510336 │ 2024-11-19 03:01:55     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/2iq9gvwTVgpyp4CSQhimY3 │           613255680 │ 2024-11-19 03:01:52     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/6gwj6vG0FDPLbBPIfcBDK  │           750276224 │ 2024-11-19 03:02:36     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/FXMxh0kA9W6QM5gmJizr92 │           640907328 │ 2024-11-19 03:02:35     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/JQgHSgRphfQNtty8iZYGV5 │           592456704 │ 2024-11-19 03:02:35     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/KZh2d7Av3UgfFu63dLKyh7 │           639652608 │ 2024-11-19 03:01:53     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/L2NiIGBOUUsWHwqhqYVni5 │           767536768 │ 2024-11-19 03:01:07     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/MG1fGMXMqlX9x1iQhUHQr4 │           750610560 │ 2024-11-19 03:01:54     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/ObfLpkM6boMbeZHvckEGy3 │           796252032 │ 2024-11-19 03:02:36     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/QuP4XULWwFtw1eWN9wYPf4 │           664751936 │ 2024-11-19 03:02:35     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/Qy1i0PXzXMmJQ5DYWqfhN5 │           789342016 │ 2024-11-19 03:01:08     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/UblG5Do43sJ4eRrr7Jh2O5 │           796920768 │ 2024-11-19 03:01:07     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/UvmDHe3hIAO1uGubX0O8K3 │           789434112 │ 2024-11-19 03:01:55     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/UxEvvrlyQdZws1Ou8Qhy62 │           595680768 │ 2024-11-19 03:02:34     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/ZrbdJT9xOcsHjExj6wCum3 │           796707456 │ 2024-11-19 03:01:53     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/e2sY1RKXFsHtNFx4PkFxT1 │           753388160 │ 2024-11-19 03:01:54     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/fnQanOb1s6OmwJtooi35K5 │           796730688 │ 2024-11-19 03:01:08     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/hHSrrfmMjtnPP4gbKBuTc2 │           764452672 │ 2024-11-19 03:01:07     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/pZ06OYSniDzOLp8vTtruQ6 │           796523712 │ 2024-11-19 03:02:37     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/rPdRFZz6g3NlhIlbnk5b16 │           790081408 │ 2024-11-19 03:01:07     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/sxOeDcjyKRrahkCHtAbeG2 │           605099776 │ 2024-11-19 03:01:52     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/v1PU6oEHSSEieXL7mceqz5 │           682199616 │ 2024-11-19 03:02:36     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/xRRUU3sKkjyFAKv4LDuUt2 │           786471232 │ 2024-11-19 03:01:08     │
│ Spill     │ 71c1bdcd-8ebb-45c1-98af-2700df2f9e10/ys9yCVJNSRBY73ce46bCA6 │           747938176 │ 2024-11-19 03:01:07     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

VACUUM TEMPORARY FILES;

┌────────┐
│  Files │
├────────┤
│     48 │
└────────┘
```