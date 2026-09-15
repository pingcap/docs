---
title: 多模态数据分析
summary: CityDrive Intelligence 记录每一次驾驶的视频。后台处理工具将视频流切分为关键帧图像，从每张图像中提取丰富的多模态信息，并按 `video_id` 存储。这些信号包括关系型元信息、JSON 清单、行为标签、向量嵌入和 GPS 轨迹。
---

# 多模态数据分析

CityDrive Intelligence 记录每一次驾驶的视频。后台处理工具将视频流切分为关键帧图像，从每张图像中提取丰富的多模态信息，并按 `video_id` 存储。这些信号包括关系型元信息、JSON 清单、行为标签、向量嵌入和 GPS 轨迹。

本指南系列展示了 {{{ .lake }}} 如何将所有这些工作负载保留在同一个计算集群中——无需复制作业，也无需额外的搜索集群。

| 指南 | 涵盖内容 |
|-------|----------------|
| [SQL 分析](/tidb-cloud-lake/guides/sql-analytics.md) | 基础表、过滤、连接、窗口、聚合索引 |
| [JSON & Search](/tidb-cloud-lake/guides/json-search.md) | 加载 `frame_metadata_catalog`，运行 Elasticsearch `QUERY()`，关联位图标签 |
| [向量搜索](/tidb-cloud-lake/guides/vector-search-guide.md) | 持久化嵌入，运行余弦搜索，连接风险指标 |
| [地理空间分析](/tidb-cloud-lake/guides/geo-analytics.md) | 使用 `GEOMETRY`、距离/多边形过滤、交通灯连接 |
| [Lakehouse ETL](/tidb-cloud-lake/guides/lakehouse-etl.md) | 一次 stage，使用 `COPY INTO` 导入共享表，添加 streams/tasks |

按顺序阅读这些指南，可以了解相同的标识符如何从经典 SQL 流转到文本搜索、向量、地理空间和 ETL——所有内容都基于同一个 CityDrive 场景。