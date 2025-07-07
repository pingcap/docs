---
title: PingCAP Clinic Diagnostic Data
summary: PingCAP Clinic Diagnostic Service 通过 TiUP 收集 TiDB 和 DM 集群的诊断数据。数据类型包括集群信息、TiDB、TiKV、PD、TiFlash、TiCDC、Prometheus 监控、系统变量以及节点系统信息。数据存储在 Clinic Server 中，面向国际用户和中国大陆用户。收集的数据仅用于排查集群问题。
---

# PingCAP Clinic Diagnostic Data

本文档介绍了 PingCAP Clinic Diagnostic Service（PingCAP Clinic）可以从使用 TiUP 部署的 TiDB 和 DM 集群中收集的诊断数据类型，以及每种数据类型对应的数据采集参数。当运行 [使用 Diag 客户端（Diag）收集数据的命令](/clinic/clinic-user-guide-for-tiup.md) 时，可以根据需要收集的数据类型，向命令中添加相应的参数。

PingCAP Clinic 收集的诊断数据**仅**用于排查集群问题。

部署在云端的诊断服务 Clinic Server 根据数据存储位置提供两个独立的服务：

- [面向国际用户的 Clinic Server](https://clinic.pingcap.com)：如果你将收集到的数据上传到面向国际用户的 Clinic Server，数据将存储在 PingCAP 在 AWS 美国区域部署的 Amazon S3 服务中。PingCAP 实行严格的数据访问策略，只有授权的技术支持人员可以访问这些数据。
- [面向中国大陆用户的 Clinic Server](https://clinic.pingcap.com.cn)：如果你将收集到的数据上传到面向中国大陆用户的 Clinic Server，数据将存储在 PingCAP 在中国（北京）区域部署的 Amazon S3 服务中。PingCAP 实行严格的数据访问策略，只有授权的技术支持人员可以访问这些数据。

## TiDB 集群

本节列出可以通过 [Diag](https://github.com/pingcap/diag) 从使用 TiUP 部署的 TiDB 集群中收集的诊断数据类型。

### TiDB 集群信息

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群的基本信息，包括集群ID | `cluster.json` | 默认每次运行时采集。 |
| 集群的详细信息 | `meta.yaml` | 默认每次运行时采集。 |

### TiDB 诊断数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tidb.log` | `--include=log` |
| 错误日志 | `tidb_stderr.log` | `--include=log` |
| 慢查询日志 | `tidb_slow_query.log` | `--include=log` |
| 审计日志 | `tidb-audit.log.json` | `--include=log` |
| 配置文件 | `tidb.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |

### TiKV 诊断数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tikv.log` | `--include=log` |
| 错误日志 | `tikv_stderr.log` | `--include=log` |
| 配置文件 | `tikv.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |

### PD 诊断数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `pd.log` | `--include=log` |
| 错误日志 | `pd_stderr.log` | `--include=log` |
| 配置文件 | `pd.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |
| `tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} store` 命令输出 | `store.json` | `--include=config` |
| `tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} config placement-rules show` 命令输出 | `placement-rule.json` | `--include=config` |

### TiFlash 诊断数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tiflash.log` | `--include=log` |
| 错误日志 | `tiflash_stderr.log` | `--include=log` |
| 配置文件 |  `tiflash-learner.toml`, `tiflash-preprocessed.toml`, `tiflash.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |

### TiCDC 诊断数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `ticdc.log` | `--include=log`|
| 错误日志 | `ticdc_stderr.log` | `--include=log` |
| 配置文件 | `ticdc.toml` | `--include=config` |
| 调试数据 | `info.txt`, `status.txt`, `changefeeds.txt`, `captures.txt`, `processors.txt` | `--include=debug`（Diag 默认不采集此数据类型） |

### Prometheus 监控数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有指标数据 | `{metric_name}.json` | `--include=monitor` |
| 所有告警数据 | `alerts.json` | `--include=monitor` |

### TiDB 系统变量

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| TiDB 系统变量 | `mysql.tidb.csv` | `--include=db_vars`（Diag 默认不采集此数据类型；如果需要采集，需提供数据库凭据） |
| | `global_variables.csv` | `--include=db_vars`（Diag 默认不采集此数据类型） |

### 集群节点的系统信息

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 内核日志 | `dmesg.log` | `--include=system` |
| 系统和硬件的基本信息 | `insight.json` | `--include=system` |
| `/etc/security/limits.conf` 内容 | `limits.conf` | `--include=system` |
| 内核参数列表 | `sysctl.conf` | `--include=system` |
| Socket 系统信息（`ss` 命令输出） | `ss.txt` | `--include=system` |

## DM 集群

本节列出可以通过 Diag 从使用 TiUP 部署的 DM 集群中收集的诊断数据类型。

### DM 集群信息

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群的基本信息，包括集群ID | `cluster.json`| 默认每次运行时采集。 |
| 集群的详细信息 | `meta.yaml` | 默认每次运行时采集。 |

### dm-master 诊断数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `dm-master.log` | `--include=log` |
| 错误日志 | `dm-master_stderr.log` | `--include=log` |
| 配置文件 | `dm-master.toml` | `--include=config` |

### dm-worker 诊断数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志| `dm-worker.log` | `--include=log`|
| 错误日志 | `dm-worker_stderr.log` | `--include=log` |
| 配置文件 | `dm-work.toml` | `--include=config` |

### Prometheus 监控数据

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有指标数据 | `{metric_name}.json` | `--include=monitor` |
| 所有告警数据 | `alerts.json` | `--include=monitor` |

### 集群节点的系统信息

| 数据类型 | 导出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 内核日志 | `dmesg.log` | `--include=system` |
| 系统和硬件的基本信息 | `insight.json` | `--include=system` |
| `/etc/security/limits.conf` 内容 | `limits.conf` | `--include=system` |
| 内核参数列表 | `sysctl.conf` | `--include=system` |
| Socket 系统信息（`ss` 命令输出） | `ss.txt` | `--include=system` |

### 日志文件分类

你可以使用 `--include=log.<type>` 参数指定要采集的日志类型。

日志类型：

- `std`：文件名中包含 `stderr` 的日志文件。
- `rocksdb`：以 `rocksdb` 前缀和 `.info` 后缀的日志文件。
- `slow`：慢查询日志文件。
- `unknown`：不属于上述任何类型的日志文件。
