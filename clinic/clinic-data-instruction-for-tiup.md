---
title: Clinic Diagnostic Data
summary: Introduces in detail what diagnostic data can be collected by the Clinic diagnostic service in the clusters deployed using TiUP.
---

# Clinic Diagnostic Data

This document provides the range of the diagnostic data can be collected by the Clinic diagnostic service in the clusters deployed using TiUP. Also, the document lists the parameters for data collection corresponding to each data module. That is, when running a command to collect data using the Clinic Diag tool (Diag), you can add the required parameters to that command according to the range of the data to be collected.

The diagnostic data collected by the Clinic diagnosis service is **only** used for troubleshooting.

The Clinic Server is located on the PingCAP intranet (in China). When you uploaded the collected diagnostic data to the Clinic Server for PingCAP developers to troubleshoot remotely, the data is stored in the AWS S3 China (Beijing) Region server set up by PingCAP. PingCAP strictly controls permissions for data access, and only authorized in-house developers can get access to the uploaded data.

After a technical support case is closed, PingCAP permanently deletes or anonymizes the corresponding data within 90 days.

## Data collection range of TiDB clutsers

This section lists the detailed diagnostic data collected by Diag in a TiDB cluster deployed using TiUP.

### Basic information of the cluster

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Basic information of the cluster, including the cluster ID | `cluster.json` | The data is collected everytime by default. |
| Detailed information of the cluster | `meta.yaml` | The data is collected everytime by default. |

### TiDB diagnostic data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Log | `tidb.log` | `--include=log` |
| Error log | `tidb_stderr.log` | `--include=log` |
| Slow log | `tidb_slow_query.log` | `--include=log` |
| Configuration file | `tidb.toml` | `--include=config` |
| Dynamic configuration | `config.json` | `--include=config` |

### TiKV diagnostic data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Log | `tikv.log` | `--include=log` |
| Error log | `tikv_stderr.log` | `--include=log` |
| Configuration file | `tikv.toml` | `--include=config` |
| Dynamic configuration | `config.json` | `--include=config` |

### PD diagnostic data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Log | `pd.log` | `--include=log` |
| Error log | `pd_stderr.log` | `--include=log` |
| Configuration file | `pd.toml` | `--include=config` |
| Dynamic configuration | `config.json` | `--include=config` |
| Outputs of the command `tiup ctl pd -u http://${pd IP}:${PORT} store` | `store.json` | `--include=config` |
| Outputs of the command `tiup ctl pd -u http://${pd IP}:${PORT} config placement-rules show` | `placement-rule.json` | `--include=config` |

### TiFlash diagnostic data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Log | `tiflash.log` | `--include=log` |
| Error log | `tiflash_stderr.log` | `--include=log` |
| Configuration file |  `tiflash-learner.toml`，`tiflash-preprocessed.toml`，`tiflash.toml` | `--include=config` |
| Dynamic configuration | `config.json` | `--include=config` |

### TiCDC diagnostic data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Log | `ticdc.log` | `--include=log`|
| Error log | `ticdc_stderr.log` | `--include=log` |
| Configuration file | `ticdc.toml` | `--include=config` |

### Prometheus monitoring data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| All metric data | `{metric_name}.json` | `--include=monitor` |
| Alert list | `alerts.json` | `--include=monitor` |

### TiDB system variable

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Get TiDB system variables (do not collect this data by default; if you need to collect the data, additional database account is required) | `mysql.tidb.csv` | `--include=db_vars` |
| | `global_variables.csv` | `--include=db_vars` |

### System information of the cluster

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Kernel log | `dmesg.log` | `--include=system` |
| Basic information of the system and the hardware | `insight.json` | `--include=system` |
| Contents in the `/etc/security/limits.conf` system  | `limits.conf` | `--include=system` |
| List of kernel parameters | `sysctl.conf` | `--include=system` |
| Socket system information, outputs of the ss command | `ss.txt` | `--include=system` |

## Data collection range of DM clusters

This section lists the detailed diagnostic data collected by Diag in a DM cluster deployed using TiUP.

### Basic information of the cluster

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Basic information of the cluster, including the cluster ID  | `cluster.json`| The data is collected everytime by default. |
| Detailed information of the cluster | `meta.yaml` | The data is collected everytime by default.  |

### dm-master diagnostic data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Log | `m-master.log` | `--include=log` |
| Error log | `dm-master_stderr.log` | `--include=log` |
| Configuration file | `dm-master.toml` | `--include=config` |

### dm-worker diagnostic data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Log| `dm-worker.log` | `--include=log`|
| Error log | `dm-worker_stderr.log` | `--include=log` |
| Configuration file | `dm-work.toml` | `--include=config` |

### Prometheus monitoring data

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| All metric data | `{metric_name}.json` | `--include=monitor` |
| Alert list | `alerts.json` | `--include=monitor` |

### System information of the cluster

| Data type | Exported file | Parameter for Clinic's data collection |
| :------ | :------ |:-------- |
| Kernel log | `dmesg.log` | `--include=system` |
| Basic information of the system and the hardware | `insight.json` | `--include=system` |
| Contents in the `/etc/security/limits.conf` system | `limits.conf` | `--include=system` |
| List of kernel parameters | `sysctl.conf` | `--include=system` |
| Socket system information, outputs of the ss command | `ss.txt` | `--include=system` |