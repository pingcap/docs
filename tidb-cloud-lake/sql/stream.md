---
title: Stream
summary: 本页按功能组织，全面概述了 {{{ .lake }}} 中的 stream 操作，便于快速查阅。
---

# Stream

本页按功能组织，全面概述了 {{{ .lake }}} 中的 stream 操作，便于快速查阅。

## Stream 管理 {#stream-management}

| Command | 描述 |
|---------|-------------|
| [CREATE STREAM](/tidb-cloud-lake/sql/create-stream.md) | 创建一个新的 stream 以跟踪表中的变更 |
| [DROP STREAM](/tidb-cloud-lake/sql/drop-stream.md) | 删除一个 stream |

## Stream 信息 {#stream-information}

| Command | 描述 |
|---------|-------------|
| [DESC STREAM](/tidb-cloud-lake/sql/desc-stream.md) | 显示 stream 的详细信息 |
| [SHOW STREAMS](/tidb-cloud-lake/sql/show-streams.md) | 列出当前或指定数据库中的所有 streams |

## 相关主题 {#related-topics}

- [通过 Streams 跟踪和转换数据](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md)

> **注意：**
>
> {{{ .lake }}} 中的 streams 用于跟踪和捕获表的变更，从而支持持续的数据管道和实时数据处理。