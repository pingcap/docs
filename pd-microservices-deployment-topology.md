---
title: PD Microservice Deployment Topology
summary: Learn the deployment topology of PD microservices based on the minimal TiDB topology.
---

# PD Microservice Deployment Topology

This document describes the deployment topology of [PD microservices](/pd-microservices.md) based on the minimal TiDB topology.

## Topology information

| Instance              | Count | Physical machine configuration       | IP                                      | Configuration             |
| :-------------------- | :---  | :----------------------------------- | :-------------------------------------- | :-------------------------|
| TiDB                  | 2     | 16 VCore 32GB * 1                    | 10.0.1.1 <br/> 10.0.1.2                 | Default port <br/> Global directory configuration |
| PD                    | 3     | 4 VCore 8GB * 1                      | 10.0.1.3 <br/> 10.0.1.4 <br/> 10.0.1.5  | Default port <br/> Global directory configuration |
| TSO                   | 2     | 4 VCore 8GB * 1                      | 10.0.1.6 <br/> 10.0.1.7                 | Default port <br/> Global directory configuration |
| Scheduling            | 2     | 4 VCore 8GB * 1                      | 10.0.1.8 <br/> 10.0.1.9                 | Default port <br/> Global directory configuration |
| TiKV                  | 3     | 16 VCore 32GB 2TB (nvme ssd) * 1     | 10.0.1.10 <br/> 10.0.1.11 <br/> 10.0.1.12 | Default port <br/> Global directory configuration |
| Monitoring & Grafana  | 1     | 4 VCore 8GB * 1 500GB (ssd)          | 10.0.1.13                               | Default port <br/> Global directory configuration |

> **Note:**
>
> The IP addresses of the instances are given as examples only. In your actual deployment, replace the IP addresses with your actual IP addresses.

### Topology template

<details>
<summary>Simple template for the PD microservice topology</summary>

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"
  listen_host: 0.0.0.0
  arch: "amd64"
  pd_mode: "ms" # To enable PD microservices, you must specify this field as "ms".

monitored:
  node_exporter_port: 9200
  blackbox_exporter_port: 9215

# # Specifies the configuration of PD servers.
pd_servers:
  - host: 10.0.1.3
  - host: 10.0.1.4
  - host: 10.0.1.5

# # Specifies the configuration of TiDB servers.
tidb_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2

# # Specifies the configuration of TiKV servers.
tikv_servers:
  - host: 10.0.1.10
  - host: 10.0.1.11
  - host: 10.0.1.12

# # Specifies the configuration of TSO servers.
tso_servers:
  - host: 10.0.1.6
  - host: 10.0.1.7

# # Specifies the configuration of Scheduling servers.
scheduling_servers:
  - host: 10.0.1.8
  - host: 10.0.1.9

# # Specifies the configuration of Prometheus servers.
monitoring_servers:
  - host: 10.0.1.13

# # Specifies the configuration of Grafana servers.
grafana_servers:
  - host: 10.0.1.13
```

</details>

For detailed descriptions of the configuration items in the preceding TiDB cluster topology file, see [Topology configuration file for deploying TiDB using TiUP](/tiup/tiup-cluster-topology-reference.md).

### Key parameters

- The instance-level `host` configuration in `tso_servers` only supports IP address, not domain name.
- For detailed descriptions of TSO configuration items, see [TSO configuration file](/tso-configuration-file.md).
- The instance-level `host` configuration in `scheduling_servers` only supports IP address, not domain name.
- For detailed descriptions of Scheduling configuration items, see [Scheduling configuration file](/scheduling-configuration-file.md).

> **Note:**
>
> - You do not need to manually create the `tidb` user in the configuration file. The TiUP cluster component automatically creates the `tidb` user on the target machines. You can customize the user, or keep the user consistent with the control machine.
> - If you configure the deployment directory as a relative path, the cluster will be deployed in the home directory of the user.
