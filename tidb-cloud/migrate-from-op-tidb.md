---
title: Migrate from On-Premise TiDB to TiDB Cloud
summary: Learn how to migrate data from on-premise TiDB to TiDB Cloud.
---

# Migrate from On-Premise TiDB to TiDB Cloud

本文主要针对 OP(On Premise) 环境自建 TiDB 集群，通过 dumpling + TiCDC 工具，将数据全量导入TiDB Cloud (AWS) 的场景。
整体方案：
  - 环境搭建及工具准备
  - 存量数据迁移：OP TiDB ( dumpling ) -- S3 -- (Import) TiDB Cloud 
  - 增量数据迁移：OP TiDB  -- (TiCDC) -- TiDB Cloud 
  - 数据验证
