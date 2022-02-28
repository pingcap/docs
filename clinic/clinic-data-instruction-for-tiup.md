---
title: TiDB Clinic Diagnostic Data
summary: Learn what diagnostic data can be collected by the TiDB Clinic Diagnostic Service from the clusters deployed using TiUP.
---

# TiDB Clinic Diagnostic Data

This document provides the scope of diagnostic data that can be collected by TiDB Clinic Diagnostic Service (TiDB Clinic) from the clusters deployed using TiUP. Also, the document lists the parameters for data collection corresponding to each data type. When running a command to collect data using the Clinic Diag tool (Diag), you can add the required parameters to the command according to the scope of the data to be collected.

The diagnostic data collected by TiDB Clinic is **only** used for troubleshooting cluster problems.

The Clinic Server is set up on the PingCAP intranet (in China). If you upload the collected diagnostic data to the Clinic Server for PingCAP technical support staff to troubleshoot cluster problems remotely, the uploaded data is stored in the AWS S3 China (Beijing) Region server set up by PingCAP. PingCAP strictly controls permissions for data access and only allows authorized in-house technical support staff to access the uploaded data.

After a technical support case is closed, PingCAP permanently deletes or anonymizes the corresponding data within 90 days.

## Data collection scope of TiDB clusters

This section lists the types of diagnostic data that can be collected by Diag from the TiDB clusters deployed using TiUP.

### Basic information of the cluster

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Basic information of the cluster, including the cluster ID | `cluster.json` | The data is collected every time by default. |
| Detailed information of the cluster | `meta.yaml` | The data is collected every time by default. |

### TiDB diagnostic data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Log | `tidb.log` | `--include=log` |
| Error log | `tidb_stderr.log` | `--include=log` |
| Slow log | `tidb_slow_query.log` | `--include=log` |
| Configuration file | `tidb.toml` | `--include=config` |
| Realtime configuration | `config.json` | `--include=config` |

### TiKV diagnostic data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Log | `tikv.log` | `--include=log` |
| Error log | `tikv_stderr.log` | `--include=log` |
| Configuration file | `tikv.toml` | `--include=config` |
| Realtime configuration | `config.json` | `--include=config` |

### PD diagnostic data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Log | `pd.log` | `--include=log` |
| Error log | `pd_stderr.log` | `--include=log` |
| Configuration file | `pd.toml` | `--include=config` |
| Realtime configuration | `config.json` | `--include=config` |
| Outputs of the command `tiup ctl pd -u http://${pd IP}:${PORT} store` | `store.json` | `--include=config` |
| Outputs of the command `tiup ctl pd -u http://${pd IP}:${PORT} config placement-rules show` | `placement-rule.json` | `--include=config` |

### TiFlash diagnostic data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Log | `tiflash.log` | `--include=log` |
| Error log | `tiflash_stderr.log` | `--include=log` |
| Configuration file |  `tiflash-learner.toml`，`tiflash-preprocessed.toml`，`tiflash.toml` | `--include=config` |
| Realtime configuration | `config.json` | `--include=config` |

### TiCDC diagnostic data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Log | `ticdc.log` | `--include=log`|
| Error log | `ticdc_stderr.log` | `--include=log` |
| Configuration file | `ticdc.toml` | `--include=config` |

### Prometheus monitoring data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| All metrics data | `{metric_name}.json` | `--include=monitor` |
| All alerts data | `alerts.json` | `--include=monitor` |

### TiDB system variable

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Get TiDB system variables ( iag does not collect this data type by default; if you need to collect this data type, database credential is required) | `mysql.tidb.csv` | `--include=db_vars` |
| | `global_variables.csv` | `--include=db_vars` |

### System information of the cluster

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Kernel log | `dmesg.log` | `--include=system` |
| Basic information of the system and the hardware | `insight.json` | `--include=system` |
| Contents in the `/etc/security/limits.conf` | `limits.conf` | `--include=system` |
| List of kernel parameters | `sysctl.conf` | `--include=system` |
| Socket system information, outputs of the ss command | `ss.txt` | `--include=system` |

## Data collection scope of DM clusters

This section lists the detailed diagnostic data collected by Diag from a DM cluster deployed using TiUP.

### Basic information of the cluster

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Basic information of the cluster, including the cluster ID  | `cluster.json`| The data is collected per run by default. |
| Detailed information of the cluster | `meta.yaml` | The data is collected per run by default. |

### dm-master diagnostic data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Log | `m-master.log` | `--include=log` |
| Error log | `dm-master_stderr.log` | `--include=log` |
| Configuration file | `dm-master.toml` | `--include=config` |

### dm-worker diagnostic data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Log| `dm-worker.log` | `--include=log`|
| Error log | `dm-worker_stderr.log` | `--include=log` |
| Configuration file | `dm-work.toml` | `--include=config` |

### Prometheus monitoring data

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| All metrics data | `{metric_name}.json` | `--include=monitor` |
| Alert list | `alerts.json` | `--include=monitor` |

### System information of the cluster

| Data type | Exported file | Parameter for data collection by TiDB Clinic |
| :------ | :------ |:-------- |
| Kernel log | `dmesg.log` | `--include=system` |
| Basic information of the system and the hardware | `insight.json` | `--include=system` |
| Contents in the `/etc/security/limits.conf` system | `limits.conf` | `--include=system` |
| List of kernel parameters | `sysctl.conf` | `--include=system` |
| Socket system information, outputs of the ss command | `ss.txt` | `--include=system` |