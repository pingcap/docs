---
title: 2026-10-22 TiDB Cloud API Temporary Maintenance Notice
summary: Learn which TiDB Cloud API endpoints are temporarily unavailable during maintenance and which operations you can still perform in the TiDB Cloud console.
---

# [2026-10-22] TiDB Cloud API Temporary Maintenance Notice

Due to temporary maintenance, the TiDB Cloud API endpoints listed in this document are currently unavailable. Requests to these APIs return HTTP status code `403`. You can continue to perform the corresponding operations in the TiDB Cloud console.

## TiDB Cloud Dedicated (`dedicated.tidbapi.com`)

| Unavailable operation | Method | API path |
| --- | --- | --- |
| Delete a cluster | `DELETE` | `/v1beta1/clusters/{cluster_id}` |
| Reset the root password | `POST` | `/v1beta1/clusters/{cluster_id}:resetRootPassword` |
| Create a changefeed | `POST` | `/v1beta1/changefeeds` |
| Delete a changefeed | `DELETE` | `/v1beta1/changefeeds/{cid}` |
| Edit the downstream configuration of a changefeed | `POST` | `/v1beta1/changefeeds/{cid}:editDownstreamConfig` |
| Set event filters for a changefeed | `POST` | `/v1beta1/changefeeds/{cid}:setEventFilters` |
| Scale a changefeed | `POST` | `/v1beta1/changefeeds/{cid}:scale` |
| Resume a changefeed | `POST` | `/v1beta1/changefeeds/{cid}:resume` |
| Create a backup export | `POST` | `/v1beta1/backups/{bid}/exports` |
| Get a backup export profile | `GET` | `/v1beta1/backups/{bid}/exportProfile` |
| Create a restore task (compatibility endpoint) | `POST` | `/api/v1beta/projects/{p}/restores` |
| Create an import task | `POST` | `/v1beta1/clusters/{id}/imports` |
| Create an import task (compatibility endpoint) | `POST` | `/api/v1beta/projects/{p}/clusters/{id}/imports` |
| Upload an import file (compatibility endpoint) | `POST` | `/api/v1beta/projects/{p}/clusters/{id}/imports/upload_file` |

## TiDB Cloud Starter and Essential (`serverless.tidbapi.com`)

| Unavailable operation | Method | API path |
| --- | --- | --- |
| Delete a cluster | `DELETE` | `/v1beta1/clusters/{cluster_id}` |
| Delete clusters in batches | `POST` | `/v1beta1/clusters:batchDelete` |
| Change the root password | `PUT` | `/v1beta1/clusters/{cluster_id}/password` |
| Rotate the root password (PostgreSQL-compatible TiDB Cloud Starter) | `POST` | `/v1beta1/clusters/{cluster_id}:rotateRootPassword` |
| Redeem the root password (PostgreSQL-compatible TiDB Cloud Starter) | `POST` | `/v1beta1/clusters/{cluster_id}:redeemRootPassword` |
| Create a migration | `POST` | `/v1beta1/clusters/{id}/migrations` |
| Delete a migration | `DELETE` | `/v1beta1/clusters/{id}/migrations/{mid}` |
| Resume a migration | `POST` | `/v1beta1/clusters/{id}/migrations/{mid}:resume` |
| Create a changefeed | `POST` | `/v1beta1/clusters/{id}/changefeeds` |
| Delete a changefeed | `DELETE` | `/v1beta1/clusters/{id}/changefeeds/{cid}` |
| Edit a changefeed | `PATCH` | `/v1beta1/clusters/{id}/changefeeds/{cid}` |
| Scale a changefeed | `POST` | `/v1beta1/clusters/{id}/changefeeds/{cid}:scale` |
| Start a changefeed | `POST` | `/v1beta1/clusters/{id}/changefeeds/{cid}:start` |
| Get the cloud storage authorization configuration | `GET` | `/v1beta1/clusters/{id}/changefeeds:getCloudStorageAuthConfig` |
| Create an export | `POST` | `/v1beta1/clusters/{id}/exports` |
| Download an export | `POST` | `/v1beta1/clusters/{id}/exports/{eid}:download` |
| Download an export file | `POST` | `/v1beta1/clusters/{id}/exports/{eid}/files:download` |
| List export files | `GET` | `/v1beta1/clusters/{id}/exports/{eid}/files` |
| Create an import task | `POST` | `/v1beta1/clusters/{id}/imports` |
| Start an import upload | `POST` | `/v1beta1/clusters/{id}/imports:startUpload` |
| Complete an import upload | `POST` | `/v1beta1/clusters/{id}/imports:completeUpload` |
| Create an import task (compatibility endpoint) | `POST` | `/api/internal/projects/{p}/clusters/{id}/imports` |
| Generate an upload URL (compatibility endpoint) | `POST` | `/api/internal/projects/{p}/clusters/{id}/upload_url` |
| Create a branch | `POST` | `/v1beta1/clusters/{id}/branches` |
| Reset a branch | `POST` | `/v1beta1/clusters/{id}/branches/{bid}:reset` |
| Modify a SQL user | `PATCH` | `/v1beta1/clusters/{id}/branches/{bid}/sqlUsers/{user}` |
| Create a branch (compatibility endpoint) | `POST` | `/api/v1beta/clusters/{id}/branches` |
| Create a SQL user (compatibility endpoint) | `POST` | `/api/internal/projects/{p}/clusters/{id}/branches/{name}/users` |
| Download audit logs | `POST` | `/v1beta1/clusters/{id}/auditlogs:download` |
| Download an audit log file | `POST` | `/v1beta1/clusters/{id}/auditLog/files:download` |
| Modify the audit log configuration | `PATCH` | `/v1beta1/clusters/{id}/auditLog/config` |

## TiDB Cloud Premium and BYOC (`cloud.tidbapi.com`)

| Unavailable operation | Method | API path |
| --- | --- | --- |
| Delete an instance | `DELETE` | `/v1beta2/tidbs/{tidb_id}` |
| Reset the root password | `POST` | `/v1beta2/tidbs/{tidb_id}:resetRootPassword` |
| Delete an instance backup | `DELETE` | `/v1beta2/tidbs/{tidb_id}/backups/{backup_id}` |
| Delete a backup | `DELETE` | `/v1beta2/backups/{backup_id}` |
| Delete a resource pool (TiDB Cloud BYOC) | `DELETE` | `/v1beta2/resourcePools/{resource_pool_id}` |
| Create a migration | `POST` | `/v1beta2/tidbs/{id}/premiumMigrations` |
| Delete a migration | `DELETE` | `/v1beta2/tidbs/{id}/premiumMigrations/{mid}` |
| Resume a migration | `POST` | `/v1beta2/tidbs/{id}/premiumMigrations/{mid}:resume` |
| Create a changefeed | `POST` | `/v1beta2/changefeeds` |
| Delete a changefeed | `DELETE` | `/v1beta2/changefeeds/{cid}` |
| Edit the downstream configuration of a changefeed | `POST` | `/v1beta2/changefeeds/{cid}:editDownstreamConfig` |
| Scale a changefeed | `POST` | `/v1beta2/changefeeds/{cid}:scale` |
| Resume a changefeed | `POST` | `/v1beta2/changefeeds/{cid}:resume` |
| Create an import task | `POST` | `/v1beta2/tidbs/{id}/imports` |
