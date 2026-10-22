---
title: 2026-10-22 TiDB Cloud API 临时维护通知
summary: 了解在维护期间哪些 TiDB Cloud API 端点暂时不可用，以及你仍可在 TiDB Cloud 控制台中执行哪些操作。
---

# [2026-10-22] TiDB Cloud API 临时维护通知 <!--Corresponding EN commit: 05c93b675ff10b9732dae65497f9e17de9d18351-->

由于临时维护，本文档中列出的 TiDB Cloud API 端点当前不可用。对这些 API 的请求会返回 HTTP 状态码 `403`。你仍然可以在 TiDB Cloud 控制台中继续执行对应操作。

## TiDB Cloud Dedicated (`dedicated.tidbapi.com`) {#tidb-cloud-dedicated-dedicated-tidbapi-com}

| 不可用操作 | 方法 | API 路径 |
| --- | --- | --- |
| 删除集群 | `DELETE` | `/v1beta1/clusters/{cluster_id}` |
| 重置 root 密码 | `POST` | `/v1beta1/clusters/{cluster_id}:resetRootPassword` |
| 创建 changefeed | `POST` | `/v1beta1/changefeeds` |
| 删除 changefeed | `DELETE` | `/v1beta1/changefeeds/{cid}` |
| 修改 changefeed 的下游配置 | `POST` | `/v1beta1/changefeeds/{cid}:editDownstreamConfig` |
| 为 changefeed 设置事件过滤器 | `POST` | `/v1beta1/changefeeds/{cid}:setEventFilters` |
| 扩展 changefeed | `POST` | `/v1beta1/changefeeds/{cid}:scale` |
| 恢复 changefeed | `POST` | `/v1beta1/changefeeds/{cid}:resume` |
| 创建备份导出 | `POST` | `/v1beta1/backups/{bid}/exports` |
| 获取备份导出配置 | `GET` | `/v1beta1/backups/{bid}/exportProfile` |
| 创建恢复任务（兼容性端点） | `POST` | `/api/v1beta/projects/{p}/restores` |
| 创建导入任务 | `POST` | `/v1beta1/clusters/{id}/imports` |
| 创建导入任务（兼容性端点） | `POST` | `/api/v1beta/projects/{p}/clusters/{id}/imports` |
| 上传导入文件（兼容性端点） | `POST` | `/api/v1beta/projects/{p}/clusters/{id}/imports/upload_file` |

## TiDB Cloud Starter and Essential (`serverless.tidbapi.com`) {#tidb-cloud-starter-and-essential-serverless-tidbapi-com}

| 不可用操作 | 方法 | API 路径 |
| --- | --- | --- |
| 删除集群 | `DELETE` | `/v1beta1/clusters/{cluster_id}` |
| 批量删除集群 | `POST` | `/v1beta1/clusters:batchDelete` |
| 更改 root 密码 | `PUT` | `/v1beta1/clusters/{cluster_id}/password` |
| 轮转 root 密码（兼容 PostgreSQL 的 TiDB Cloud Starter） | `POST` | `/v1beta1/clusters/{cluster_id}:rotateRootPassword` |
| 兑换 root 密码（兼容 PostgreSQL 的 TiDB Cloud Starter） | `POST` | `/v1beta1/clusters/{cluster_id}:redeemRootPassword` |
| 创建迁移 | `POST` | `/v1beta1/clusters/{id}/migrations` |
| 删除迁移 | `DELETE` | `/v1beta1/clusters/{id}/migrations/{mid}` |
| 恢复迁移 | `POST` | `/v1beta1/clusters/{id}/migrations/{mid}:resume` |
| 创建 changefeed | `POST` | `/v1beta1/clusters/{id}/changefeeds` |
| 删除 changefeed | `DELETE` | `/v1beta1/clusters/{id}/changefeeds/{cid}` |
| 修改 changefeed | `PATCH` | `/v1beta1/clusters/{id}/changefeeds/{cid}` |
| 扩展 changefeed | `POST` | `/v1beta1/clusters/{id}/changefeeds/{cid}:scale` |
| 启动 changefeed | `POST` | `/v1beta1/clusters/{id}/changefeeds/{cid}:start` |
| 获取云存储授权配置 | `GET` | `/v1beta1/clusters/{id}/changefeeds:getCloudStorageAuthConfig` |
| 创建导出 | `POST` | `/v1beta1/clusters/{id}/exports` |
| 下载导出 | `POST` | `/v1beta1/clusters/{id}/exports/{eid}:download` |
| 下载导出文件 | `POST` | `/v1beta1/clusters/{id}/exports/{eid}/files:download` |
| 列出导出文件 | `GET` | `/v1beta1/clusters/{id}/exports/{eid}/files` |
| 创建导入任务 | `POST` | `/v1beta1/clusters/{id}/imports` |
| 开始导入上传 | `POST` | `/v1beta1/clusters/{id}/imports:startUpload` |
| 完成导入上传 | `POST` | `/v1beta1/clusters/{id}/imports:completeUpload` |
| 创建导入任务（兼容性端点） | `POST` | `/api/internal/projects/{p}/clusters/{id}/imports` |
| 生成上传 URL（兼容性端点） | `POST` | `/api/internal/projects/{p}/clusters/{id}/upload_url` |
| 创建分支 | `POST` | `/v1beta1/clusters/{id}/branches` |
| 重置分支 | `POST` | `/v1beta1/clusters/{id}/branches/{bid}:reset` |
| 修改 SQL 用户 | `PATCH` | `/v1beta1/clusters/{id}/branches/{bid}/sqlUsers/{user}` |
| 创建分支（兼容性端点） | `POST` | `/api/v1beta/clusters/{id}/branches` |
| 创建 SQL 用户（兼容性端点） | `POST` | `/api/internal/projects/{p}/clusters/{id}/branches/{name}/users` |
| 下载审计日志 | `POST` | `/v1beta1/clusters/{id}/auditlogs:download` |
| 下载审计日志文件 | `POST` | `/v1beta1/clusters/{id}/auditLog/files:download` |
| 修改审计日志配置 | `PATCH` | `/v1beta1/clusters/{id}/auditLog/config` |

## TiDB Cloud Premium and BYOC (`cloud.tidbapi.com`) {#tidb-cloud-premium-and-byoc-cloud-tidbapi-com}

| 不可用操作 | 方法 | API 路径 |
| --- | --- | --- |
| 删除实例 | `DELETE` | `/v1beta2/tidbs/{tidb_id}` |
| 重置 root 密码 | `POST` | `/v1beta2/tidbs/{tidb_id}:resetRootPassword` |
| 删除实例备份 | `DELETE` | `/v1beta2/tidbs/{tidb_id}/backups/{backup_id}` |
| 删除备份 | `DELETE` | `/v1beta2/backups/{backup_id}` |
| 删除资源池（TiDB Cloud BYOC） | `DELETE` | `/v1beta2/resourcePools/{resource_pool_id}` |
| 创建迁移 | `POST` | `/v1beta2/tidbs/{id}/premiumMigrations` |
| 删除迁移 | `DELETE` | `/v1beta2/tidbs/{id}/premiumMigrations/{mid}` |
| 恢复迁移 | `POST` | `/v1beta2/tidbs/{id}/premiumMigrations/{mid}:resume` |
| 创建 changefeed | `POST` | `/v1beta2/changefeeds` |
| 删除 changefeed | `DELETE` | `/v1beta2/changefeeds/{cid}` |
| 修改 changefeed 的下游配置 | `POST` | `/v1beta2/changefeeds/{cid}:editDownstreamConfig` |
| 扩展 changefeed | `POST` | `/v1beta2/changefeeds/{cid}:scale` |
| 恢复 changefeed | `POST` | `/v1beta2/changefeeds/{cid}:resume` |
| 创建导入任务 | `POST` | `/v1beta2/tidbs/{id}/imports` |