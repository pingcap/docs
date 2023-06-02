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
    "cluster_id": ${CLUSTER_ID}
  },
  {
    "cluster_id": ${CLUSTER_ID}
  },
  {
    "cluster_id":${CLUSTER_ID}
  }
]
```


| Field  | Type  | Description  |
|---------|---------|---------|
| `${CLUSTER_ID}`     |    Number     | The ID of the cluster. You can get it from the URL of your TiDB cluster. For example, if your cluster URL is https://tidbcloud.com/console/clusters/1379111944646164111/overview, the cluster ID is `1379111944646164111`. |

## dataapp_config.json

## http_endpoints

### config.json

### sql