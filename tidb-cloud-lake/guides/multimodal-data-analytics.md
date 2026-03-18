---
title: Multimodal Data Analytics
summary: CityDrive Intelligence records video of every drive. Background processing tools split the video stream into keyframe images, extracting rich multimodal information from each image and storing it by video_id. These signals include relational metadata, JSON manifests, behavior tags, vector embeddings, and GPS traces.
---

# Multimodal Data Analytics

CityDrive Intelligence records video of every drive. Background processing tools split the video stream into keyframe images, extracting rich multimodal information from each image and storing it by `video_id`. These signals include relational metadata, JSON manifests, behavior tags, vector embeddings, and GPS traces.

This guide set shows how Databend keeps all those workloads in one warehouse—no copy jobs, no extra search cluster.

| Guide | What it covers |
|-------|----------------|
| [SQL Analytics](/tidb-cloud-lake/guides/sql-analytics.md) | Base tables, filters, joins, windows, aggregating indexes |
| [JSON & Search](/tidb-cloud-lake/guides/json-search.md) | Load `frame_metadata_catalog`, run Elasticsearch `QUERY()`, link bitmap tags |
| [Vector Search](/tidb-cloud-lake/guides/vector-search-guide.md) | Persist embeddings, run cosine search, join risk metrics |
| [Geo Analytics](/tidb-cloud-lake/guides/geo-analytics.md) | Use `GEOMETRY`, distance/polygon filters, traffic-light joins |
| [Lakehouse ETL](/tidb-cloud-lake/guides/lakehouse-etl.md) | Stage once, `COPY INTO` shared tables, add streams/tasks |

Walk through them in order to see how the same identifiers flow from classic SQL to text search, vector, geo, and ETL—everything grounded in a single CityDrive scenario.
