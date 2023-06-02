---
title: Data App Configuration Files
summary: This document describes the configuration files of Data Service in TiDB Cloud.
---

# Data App Configuration Files

This document describes the configuration files of Data Service in TiDB Cloud.

If you have connected your Data App to GitHub, you can find the configuration files of your Data App in your specified directory on GitHub. For more information, see [Deploy Automatically with GitHub](/tidb-cloud/data-service-manage-github-integration.md).

```
├── app
│   ├── data_sources
│   │   └── cluster.json
│   ├── dataapp_config.json
│   ├── http_endpoints
│   │   ├── config.json
│   │   └── sql
│   │       ├── <method>-<endpoint-name1>.sql
│   │       ├── <method>-<endpoint-name2>.sql
│   │       └── <method>-<endpoint-name3>.sql
```

## Data source configuration

The data source of a Data App is the linked clusters for this App. You can configure the data source in `cluster.json`.

```
├── app
│   ├── data_sources
│   │   └── cluster.json
```

The following is an example configuration of `cluster.json`.

```json
[
  {
    "cluster_id": <cluster ID>
  },
  {
    "cluster_id": <cluster ID>
  },
  {
    "cluster_id": <cluster ID>
  }
]
```


| Field  | Type  | Description  |
|---------|---------|---------|
| `<cluster ID>`     |    Number     |    The ID of the cluster. You can get it from the browser URL of your TiDB cluster.|

## dataapp_config.json

## http_endpoints

### config.json

### sql