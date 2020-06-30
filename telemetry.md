---
title: Telemetry
summary: Learn the telemetry feature, how to disable and view the status of this feature.
category: reference
---

# Telemetry

By default, TiDB, TiUP and TiDB Dashboard collect usage information and share the information with PingCAP to help understand how to improve the product. For example, this usage information helps to prioritize new features.

## What gets shared?

The usage information includes the deployment characteristics of the cluster, hardware information and user performed operations. The followings describe details for each component. Note that the details that get shared may change over time. The changes will be announced in release notes if that happens.

In all cases, data stored in the cluster by users will not be shared. You may also refer to [PingCAP Privacy Policy](https://pingcap.com/privacy-policy/).

### TiDB

When TiDB telemetry collection is enabled, the TiDB cluster will collect usage details on an daily basis, including (but not limited to):

- A randomly generated telemetry ID.
- Deployment characteristics, such as the size of hardware (CPU, memory, disk), TiDB components versions, OS name, etc.

To view the full content of the usage information shared to PingCAP, execute the following SQL statement:

```sql
ADMIN SHOW TELEMETRY;
```

### TiDB Dashboard

When TiDB Dashboard telemetry collection is enabled, user operations to TiDB Dashboard web UI will be shared, including (but not limited to):

- A randomly generated telemetry ID.
- User operation information, such as the name of the TiDB Dashboard web page user accessed, etc.
- Browser and OS information, such as browser name, OS name, screen resolution, etc.

To view the full content of the usage information shared to PingCAP, use the [Network Activity Inspector of Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/network) or the [Network Monitor of Firefox Developer Tools](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor).

### TiUP

When TiUP telemetry collection is enabled, user operations to TiUP will be shared, including (but not limited to):

- A randomly generated telemetry ID.
- Command execution status, such as whether execution is successful, execution duration, etc.
- Deployment characteristics, such as the size of hardware, TiDB components versions, deployment configuration names that have been modified, etc.

To view the full content of the usage information shared to PingCAP, set `TIUP_CLUSTER_DEBUG=enable` environment variable when executing the TiUP command, for example:

```bash
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

## Opt out telemetry

### Opt out TiDB telemetry at deployment

When deploying TiDB clusters, configure [`enable-telemetry = false`](/tidb-configuration-file.md#enable-telemetry) for all TiDB instances to opt out the TiDB telemetry collection. Deployed TiDB clusters also respect this configuration item but a restart is needed to take effect.

Detailed configure steps for different deployment tools are listed below.

<details>
  <summary>Binary deployment</summary>

Create a configuration file `tidb_config.toml` with the following content:

```toml
enable-telemetry = false
```

Specify the command line parameter `--config=tidb_config.toml` when starting TiDB to take effect.

See [TiDB Configuration Options](/command-line-flags-for-tidb-configuration.md#--config) and [TiDB Configuration File](/tidb-configuration-file.md#enable-telemetry) for details.

</details>

<details>
  <summary>TiUP Playground</summary>

Create a configuration file `tidb_config.toml` with the following content:

```toml
enable-telemetry = false
```

When starting TiUP Playground, specify the command line parameter `--db.config tidb_config.toml` to take effect, for example:

```bash
tiup playground --db.config tidb_config.toml
```

See [Quickly Deploy a Local TiDB Cluster](/tiup/tiup-playground.md) for details.

</details>

<details>
  <summary>TiUP Cluster deployment</summary>

Modify the deployment topology file `topology.yaml` to add or modify the following:

```yaml
server_configs:
  tidb:
    enable-telemetry: false
```

</details>

<details>
  <summary>Ansible deployment</summary>

Locate the following contents in the configuration file `tidb-ansible/conf/tidb.yml`:

```yaml
# enable-telemetry: true
```

And change to:

```yaml
enable-telemetry: false
```

See [Deploy TiDB Using TiDB Ansible](/online-deployment-using-ansible.md) for details.

</details>

<details>
  <summary>Kubernetes deployment via TiDB Operator</summary>

Configure `spec.tidb.config.enable-telemetry: false` in `tidb-cluster.yaml` or TidbCluster Custom Resource.

See [Deploy TiDB Operator in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator) for details.

</details>

### Opt out TiDB telemetry for deployed TiDB clusters

For deployed TiDB clusters, you can also modify the system variable [`tidb_enable_telemetry`](/tidb-specific-system-variables.md#tidb_enable_telemetry) to dynamically opt out the TiDB telemetry collection:

```sql
SET GLOBAL tidb_enable_telemetry = 0;
```

Note that disabling by configuration files takes precedence over system variables. That is, when telemetry collection is disabled by configuration files, the value of the system variable will be ignored.

### Opt out TiDB Dashboard telemetry

Configure [`dashboard.disable-telemetry = true`](/pd-configuration-file.md#disable-telemetry) for all PD instances to opt out the TiDB Dashboard telemetry collection. Running clusters need to be restarted to take effect.

Detailed configure steps for different deployment tools are listed below.

<details>
  <summary>Binary deployment</summary>

Create a configuration file `pd_config.toml` with the following content:

```toml
[dashboard]
disable-telemetry = true
```

Specify the command line parameter `--config=pd_config.toml` when starting PD to take effect.

See [PD Configuration Flags](/command-line-flags-for-pd-configuration.md#--config) and [PD Configuration File](/pd-configuration-file.md#disable-telemetry) for details.

</details>

<details>
  <summary>TiUP Playground</summary>

Create a configuration file `pd_config.toml` with the following content:

```toml
[dashboard]
disable-telemetry = true
```

When starting TiUP Playground, specify the command line parameter `--pd.config pd_config.toml` to take effect, for example:

```bash
tiup playground --pd.config pd_config.toml
```

See [Quickly Deploy a Local TiDB Cluster](/tiup/tiup-playground.md) for details.

</details>

<details>
  <summary>TiUP Cluster deployment</summary>

Modify the deployment topology file `topology.yaml` to add or modify the following:

```yaml
server_configs:
  pd:
    dashboard.disable-telemetry: true
```

</details>

<details>
  <summary>Ansible deployment</summary>

Locate the following contents in the configuration file `tidb-ansible/conf/pd.yml`:

```yaml
dashboard:
  ...
  # disable-telemetry: false
```

And change to:

```yaml
dashboard:
  ...
  disable-telemetry: true
```

See [Deploy TiDB Using TiDB Ansible](/online-deployment-using-ansible.md) for details.

</details>

<details>
  <summary>Kubernetes deployment via TiDB Operator</summary>

Configure `spec.pd.config.dashboard.disable-telemetry: true` in `tidb-cluster.yaml` or TidbCluster Custom Resource.

See [Deploy TiDB Operator in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator) for details.

</details>

### Opt out TiUP telemetry

To opt out the TiUP telemetry collection, execute the following command:

```bash
tiup telemetry disable
```

## Reset telemetry ID

The usage information shared by TiDB, TiDB Dashboard and TiUP contain a randomly generated telemetry ID to distinguish different clusters or users.

### Reset TiDB telemetry ID

Execute the following SQL statement to reset and generate a new TiDB telemetry ID:

```sql
ADMIN RESET TELEMETRY_ID;
```

### Reset TiDB Dashboard telemetry ID

After accessing TiDB Dashboard, use Chrome Chrome DevTools or Firefox Developer Tools to clear the Local Storage item prefixed with `mp_` to reset and generate a new TiDB Dashboard telemetry ID:

- [View And Edit Local Storage With Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/storage/localstorage)
- [Working with Local Storage using Storage Inspector of Firefox Developer Tools](https://developer.mozilla.org/en-US/docs/Tools/Storage_Inspector/Local_Storage_Session_Storage)

### Reset TiUP telemetry ID

Execute the following command to reset and generate new TiUP telemetry ID:

```bash
tiup telemetry reset
```

## Check telemetry status

For TiDB telemetry, execute the following SQL statement to check the telemetry status:

```sql
ADMIN SHOW TELEMETRY;
```

If the `DATA_PREVIEW` column is empty, TiDB telemetry is off. If not, TiDB telemetry is on. You can also check when the usage information was shared previously according to the `LAST_STATUS` column.

For TiUP telemetry, execute the following command to check the telemetry status:

```bash
tiup telemetry status
```

## Compliance

In order to meet compliance requirements in different countries or regions, the usage information will be sent to servers located in different countries according to the IP address of the sender machine as follows:

- For IP addresses from mainland China, usage information will be sent and stored on cloud servers in mainland China.
- For IP addresses other than mainland China, usage information will be sent and stored on cloud servers in US.

See [PingCAP Privacy Policy](https://pingcap.com/privacy-policy/) for details.
