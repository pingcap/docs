---
title: System Functions
---

This page provides reference information for the system-related functions in Databend. These functions help you analyze and monitor the internal storage and performance aspects of your Databend deployment.

## Table Metadata Functions

| Function | Description | Example |
|----------|-------------|--------|
| [CLUSTERING_INFORMATION](clustering_information.md) | Returns clustering information of a table | `CLUSTERING_INFORMATION('default', 'mytable')` |

## Storage Layer Functions

| Function | Description | Example |
|----------|-------------|--------|
| [FUSE_SNAPSHOT](fuse_snapshot.md) | Returns snapshot information of a table | `FUSE_SNAPSHOT('default', 'mytable')` |
| [FUSE_SEGMENT](fuse_segment.md) | Returns segment information of a table | `FUSE_SEGMENT('default', 'mytable')` |
| [FUSE_BLOCK](fuse_block.md) | Returns block information of a table | `FUSE_BLOCK('default', 'mytable')` |
| [FUSE_COLUMN](fuse_column.md) | Returns column information of a table | `FUSE_COLUMN('default', 'mytable')` |

## Storage Optimization Functions

| Function | Description | Example |
|----------|-------------|--------|
| [FUSE_STATISTIC](fuse_statistic.md) | Returns statistics information of a table | `FUSE_STATISTIC('default', 'mytable')` |
| [FUSE_ENCODING](fuse_encoding.md) | Returns encoding information of a table | `FUSE_ENCODING('default', 'mytable')` |
| [FUSE_VIRTUAL_COLUMN](fuse_virtual_column.md) | Returns virtual column information | `FUSE_VIRTUAL_COLUMN('default', 'mytable')` |
| [FUSE_TIME_TRAVEL_SIZE](fuse_time_travel_size.md) | Returns time travel storage information | `FUSE_TIME_TRAVEL_SIZE('default', 'mytable')` |
