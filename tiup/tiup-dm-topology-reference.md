---
title: Topology Configuration File for DM Cluster Deployment using TiUP
---

# Topology Configuration File for DM Cluster Deployment using TiUP

To deploy or scale a TiDB Data Migration (DM) cluster, you need to provide a topology file to describe the cluster topology. Similarly, to modify the cluster topology, you need to modify the topology file. The difference is that you can only modify a part of the fields in the topology file.

Here is an [example topology file](https://github.com/pingcap/tiup/blob/master/embed/templates/examples/dm/topology.example.yaml) for your reference.

## File Structure

The topology file of a DM cluster might contain the following blocks:

- [global](/tiup/tiup-dm-topology-reference.md#global): the global configuration of the cluster. Some of the configuration items use the default values on the cluster, and you can configure them separately in each instance.
- [server_configs](/tiup/tiup-dm-topology-reference.md#server_configs): the global configuration of the components. You can configure each component separately. If an instance has a configuration item with the same name, the items configured in the instance will take effect.
- [master_servers](/tiup/tiup-dm-topology-reference.md#master_servers): the configuration of DM master instance. The block is used to specify the machines to which the master service of the DM component is deployed.
- [worker_servers](/tiup/tiup-dm-topology-reference.md#worker_servers): the configuration of DM worker instance. The block is used to specify the machines to which the worker service of the DM component is deployed.
- [monitoring_servers](/tiup/tiup-cluster-topology-reference.md#monitoring_servers): specifies the machines to which the Prometheus instances are deployed. TiUP supports the deployment of multiple Prometheus instances, but only the first instance is actually in use.
- [grafana_servers](/tiup/tiup-cluster-topology-reference.md#grafana_servers): the configuration of Grafana instances. The block is used to specify the machines to which the Grafana instances are deployed.
- [alertmanager_servers](/tiup/tiup-cluster-topology-reference.md#alertmanager_servers): the configuration of the Alertemanager instances. The block is used to specify the machines to which the Alertmanager instances are deployed.

### `global`

The `global` block corresponds to the global configuration of the cluster and contains the following fields:

- `user`: the user to start the deployed cluster. The default value is "tidb". If the user specified in the `<user>` field does not exist on the target machine, TiUP will automatically try to create the user.
- `group`: the user group to which a user belongs when the user is automatically created. The default value is the same as the `<user>` field. If the specified group does not exist, it will be created automatically.
- `ssh_port`: the SSH port to connect to the target machine for operations. The default value is "22".
- `deploy_dir`: the deployment directory for each component. The default value is "deploy". The application rules are as follows:
    - If the absolute path `deploy_dir` is configured at the instance level, the actual deployment directory is the `deploy_dir` configured for the instance.
    - For each instance, if `deploy_dir` is not configured, the default value is the relative path `<component-name>-<component-port>`.
    - If `global.deploy_dir` is set to an absolute path, the component is deployed to `<global.deploy_dir>/<instance.deploy_dir>` directory.
    - If `global.deploy_dir` is set to a relative path, the component is deployed to `/home/<global.user>/<global.deploy_dir>/<instance.deploy_dir>` directory.
- `data_dir`: the data directory. The default value is "data". The application rules are as follows.
    - If the absolute path `data_dir` is configured at the instance level, the actual data directory is the `data_dir` configured for the instance.
    - For each instance, if `data_dir` is not configured, the default value is `<global.data_dir>`.
    - If `data_dir` is set to a relative path, the component data is stored in `<deploy_dir>/<data_dir>`. For the calculation rules of `<deploy_dir>`, see the application rules of the `deploy_dir` field.
- `log_dir`: the data directory. The default value is "log". The application rules are as follows.
    - If the absolute path of `log_dir` is configured at the instance level, the actual log directory is the `log_dir` configured for the instance.
    - For each instance, if `log_dir` is not configured by the user, the default value is `<global.log_dir>`.
    - If `log_dir` is a relative path, the component logs will be stored in `<deploy_dir>/<log_dir>`. For the calculation rules of `<deploy_dir>`, see the application rules of the `deploy_dir` field.
- `os`: the operating system of the target machine. The field controls which operating system to adapt to for the components pushed to the target machine. The default value is "linux".
- `arch`: the CPU architecture of the target machine. The field controls which platform to adapt to for the binary packages pushed to the target machine. The supported values are "amd64" and "arm64". The default value is "amd64".
- `resource_control`: runtime resource control. All configurations under this field will be written to the `service` file of systemd. By default, the runtime resource is unlimited. The supported resources for control are as follows:
    - `memory_limit`: limits the maximum memory at runtime. For example, "2G" means that the maximum memory of 2 GB can be used.
    - `cpu_quota`: limits the maximum CPU usage at runtime. For example, "200%".
    - `io_read_bandwidth_max`: limits the maximum bandwidth for read disk IO. For example, "/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M".
    - `io_write_bandwidth_max`: limits the maximum bandwidth of write disk IO. For example, "/dev/disk/by-path/pci-0000:00:1f.2-scsi-0:0:0:0:0 100M".
    - `limit_core`: controls the size of core dump.

A `global` configuration example:

```yaml
global:
  user: "tidb"
  resource_control:
    memory_limit: "2G"
```

In the example, the configuration specifies that the `tidb` user is used to start the cluster, and that each component is limited to a maximum of 2GB of memory when it is running.

### `server_configs`

`server_configs` is used to configure the service and generate the configuration file for each component. Similar to the `global` block, the configurations in the `server_configs` block can be overridden by the configurations with the same names in the instance. The block mainly contains the following fields:

- `master`: configuration related to the DM master service. For all the supported configuration items, see [DM-master Configuration File](https://docs.pingcap.com/zh/tidb-data-migration/stable/dm-master-configuration-file).
- `worker`: configuration related to the DM worker service, For all the supported configuration items, see [DM-worker Configuration File](https://docs.pingcap.com/zh/tidb-data-migration/stable/dm-worker-configuration-file).

A `server_configs` configuration example:

```yaml
server_configs:
  master:
    log-level: info
    rpc-timeout: "30s"
    rpc-rate-limit: 10.0
    rpc-rate-burst: 40
  worker:
    log-level: info
```

## `master_servers`

`master_servers` specifies the machines to which the master node of the DM component is deployed. You can also specify the service configuration on each machine. `master_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` block is used.
- `name`: specifies the name of the DM master instance. The name must be unique for different instances. Otherwise, the cluster cannot be deployed.
- `port`: specifies the port on which DM master provides services. The default values is "8261".
- `peer_port`: specifies the port that DM masters use to communicate with each other. The default value is "8291".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` block.
- `data_dir`: specifies the data directory. If the field is not specified, or specified as a relative directory, the data directory is generated according to the `data_dir` configuration in the `global` block.
- `log_dir`: specifies the log directory. If the field not specified, or specified as a relative directory, the log directory is generated according to the `log_dir` configuration in the `global` block.
- `numa_node`: assigns the NUMA policy to the instance. If the field is specified, make sure that [numactl](https://linux.die.net/man/8/numactl) is installed on the target machine, then [numactl](https://linux.die.net/man/8/numactl) will assign the cpubind and membind policies. The field value type is `STRING`. The field value is the NUMA node ID, for example, "0,1".
- `config`: the configuration rules of this field are the same as that of `master` in the `server_configs` block. If `config` is specified, the configuration of `config` will be merged with the configuration of `master` in `server_configs` (if the two fields overlap, the configuration of this field takes effect), and then the configuration file is generated and distributed to the machine specified in the `host` field.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` block.
- `arch`: the architecture of the machine specified by the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` block.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` block (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` block.
- `v1_source_path`: when upgrading from v1.0.x, you can specify the directory where the configuration file of the V1 source is located in this field.

In the `master_servers` block, the following fields cannot be modified after the deployment is completed: 

- `host`
- `name`
- `port`
- `peer_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`
- `v1_source_path`

A `master_servers` configuration example:

```yaml
master_servers:
  - host: 10.0.1.11
    name: master1
    ssh_port: 22
    port: 8261
    peer_port: 8291
    deploy_dir: "/dm-deploy/dm-master-8261"
    data_dir: "/dm-data/dm-master-8261"
    log_dir: "/dm-deploy/dm-master-8261/log"
    numa_node: "0,1"
    # The following configs are used to overwrite the `server_configs.master` values.
    config:
      log-level: info
      rpc-timeout: "30s"
      rpc-rate-limit: 10.0
      rpc-rate-burst: 40
  - host: 10.0.1.18
    name: master2
  - host: 10.0.1.19
    name: master3
```

## `worker_servers`

`worker_servers` specifies the machines to which the master node of the DM component is deployed. You can also specify the service configuration on each machine. `worker_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` block is used.
- `name`: specifies the name of the DM worker instance. The name must be unique for different instances. Otherwise, the cluster cannot be deployed.
- `port`: specifies the port on which DM worker provides services. The default values is "8262".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` block.
- `data_dir`: specifies the data directory. If the field is not specified, or specified as a relative directory, the data directory is generated according to the `data_dir` configuration in the `global` block.
- `log_dir`: specifies the log directory. If the field not specified, or specified as a relative directory, the log directory is generated according to the `log_dir` configuration in the `global` block.
- `numa_node`: assigns the NUMA policy to the instance. If the field is specified, make sure that [numactl](https://linux.die.net/man/8/numactl) is installed on the target machine, then [numactl](https://linux.die.net/man/8/numactl) will assign the cpubind and membind policies. The field value type is `STRING`. The field value is the NUMA node ID, for example, "0,1".
- `config`: the configuration rules of this field are the same as that of `worker` in the `server_configs` block. If `config` is specified, the configuration of `config` will be merged with the configuration of `worker` in `server_configs` (if the two fields overlap, the configuration of this field takes effect), and then the configuration file is generated and distributed to the machine specified in the `host` field.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` block.
- `arch`: the architecture of the machine specified by the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` block.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` block (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` block.

In the `worker_servers` block, the following fields cannot be modified after the deployment is completed: 

- `host`
- `name`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

A `worker_servers` configuration example:

```yaml
worker_servers:
  - host: 10.0.1.12
    ssh_port: 22
    port: 8262
    deploy_dir: "/dm-deploy/dm-worker-8262"
    log_dir: "/dm-deploy/dm-worker-8262/log"
    numa_node: "0,1"
    # config is used to overwrite the `server_configs.worker` values
    config:
      log-level: info
  - host: 10.0.1.19
```

### `monitoring_servers`

`monitoring_servers` specifies the machines to which the Prometheus service is deployed. You can also specify the service configuration on the machine. `monitoring_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` block is used.
- `port`: specifies the port on which Prometheus provides services. The default values is "9090".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` block.
- `data_dir`: specifies the data directory. If the field is not specified, or specified as a relative directory, the data directory is generated according to the `data_dir` configuration in the `global` block.
- `log_dir`: specifies the log directory. If the field not specified, or specified as a relative directory, the log directory is generated according to the `log_dir` configuration in the `global` block.
- `numa_node`: assigns the NUMA policy to the instance. If the field is specified, make sure that [numactl](https://linux.die.net/man/8/numactl) is installed on the target machine, then [numactl](https://linux.die.net/man/8/numactl) will assign the cpubind and membind policies. The field value type is `STRING`. The field value is the NUMA node ID, for example, "0,1".
- `storage_retention`: specifies the retention time of the Prometheus monitoring data. The default value is "15d".
- `rule_dir`: specifies a local directory where the complete `*.rules.yml` files are located. The files in the specified directory will be sent to the target machine as the Prometheus rules during the initialization phase of the cluster configuration.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` block.
- `arch`: the architecture of the machine specified by the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` block.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` block (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` block.

In the `monitoring_servers` block, the following fields cannot be modified after the deployment is completed: 

- `host`
- `port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

A `monitoring_servers` configuration example:

```yaml
monitoring_servers:
  - host: 10.0.1.11
    rule_dir: /local/rule/dir
```

### ``grafana_servers``

`grafana_servers` specifies the machines to which the Grafana service is deployed. You can also specify the service configuration on the machine. `grafana_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` block is used.
- `port`: specifies the port on which Grafana provides services. The default values is "3000".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` block.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` block.
- `arch`: the architecture of the machine specified by the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` block.
- `username`: specifies the username of the Grafana login screen.
- `password`: specifies the corresponding password of Grafana.
- `dashboard_dir`: specifies a local directory where the complete `dashboard(*.json)` files are located. The files in the specified directory will be sent to the target machine as Grafana dashboards during the initialization phase of the cluster configuration.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` block (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` block.

> **Note:**
>
> If the `dashboard_dir` field of `grafana_servers` is configured, after executing the `tiup cluster rename` command to rename the cluster, you need to do the following:
>
> 1. In the local `dashboards` directory, update the value of the `datasource` field to the new cluster name (the `datasource` is named according to the cluster name).
> 2. Execute the `tiup cluster reload -R grafana` command.

In `grafana_servers`, the following fields cannot be modified after the deployment is completed:

- `host`
- `port`
- `deploy_dir`
- `arch`
- `os`

A `grafana_servers` configuration example：

```yaml
grafana_servers:
  - host: 10.0.1.11
    dashboard_dir: /local/dashboard/dir
```

### `alertmanager_servers`

`alertmanager_servers` specifies the machines to which the Alertmanager service is deployed. You can also specify the service configuration on each machine. `alertmanager_servers` is an array. Each array element contains the following fields:

- `host`: specifies the machine to deploy to. The field value is an IP address and is mandatory.
- `ssh_port`: specifies the SSH port to connect to the target machine for operations. If the field is not specified, the `ssh_port` in the `global` block is used.
- `web_port`: specify the port on which Alertmanager provides webpage services. The default value is "9093".
- `cluster_port`: Specify the port on which Alertmanger communicates with Alertmanagers. The default value is "9094".
- `deploy_dir`: specifies the deployment directory. If the field is not specified, or specified as a relative directory, the deployment directory is generated according to the `deploy_dir` configuration in the `global` block.
- `data_dir`: specifies the data directory. If the field is not specified, or specified as a relative directory, the data directory is generated according to the `data_dir` configuration in the `global` block.
- `log_dir`: specifies the log directory. If the field not specified, or specified as a relative directory, the log directory is generated according to the `log_dir` configuration in the `global` block.
- `numa_node`: assigns the NUMA policy to the instance. If the field is specified, make sure that [numactl](https://linux.die.net/man/8/numactl) is installed on the target machine, then [numactl](https://linux.die.net/man/8/numactl) will assign the cpubind and membind policies. The field value type is `STRING`. The field value is the NUMA node ID, for example, "0,1".
- `config_file`: specifies a local file. The specified file will be sent to the target machine as the configuration for Alertmanager during the initialization phase of the cluster configuration.
- `os`: the operating system of the machine specified in the `host` field. If the field is not specified, the default value is the `os` value configured in the `global` block.
- `arch`: the architecture of the machine specified by the `host` field. If the field is not specified, the default value is the `arch` value configured in the `global` block.
- `resource_control`: resource control on this service. If this field is specified, the configuration of this field will be merged with the configuration of `resource_control` in the `global` block (if the two fields overlap, the configuration of this field takes effect), and then the configuration file of systemd is generated and distributed to the machine specified in the `host` field. The configuration rules of this field are the same as that of `resource_control` in the `global` block.

In `alertmanager_servers`, the following fields cannot be modified after the deployment is completed:

- `host`
- `web_port`
- `cluster_port`
- `deploy_dir`
- `data_dir`
- `log_dir`
- `arch`
- `os`

An `alertmanager_servers` configuration example：

```yaml
alertmanager_servers:
  - host: 10.0.1.11
    config_file: /local/config/file
  - host: 10.0.1.12
    config_file: /local/config/file
```
