---
title: Telemetry
category: reference
---

# Telemetry

By default, TiDB, TiUP and TiDB Dashboard collect usage information and share it with PingCAP to help understand how to improve the product. For example, this usage information helps to prioritize new features.

## What gets shared?

The following sections describe the shared usage information in detail for each component. The usage details that get shared might change over time. These changes (if any) will be announced in [release notes](/releases/release-notes.md).

> **Note:**
>
> In **ALL** cases, user data stored in the TiDB cluster will **NOT** be shared. You can also refer to [PingCAP Privacy Policy](https://pingcap.com/privacy-policy).

### TiDB

When the telemetry collection feature is enabled in TiDB, the TiDB cluster collects usage details on a daily basis. These usage details include but are not limited to:

- A randomly generated telemetry ID.
- Deployment characteristics, such as the size of hardware (CPU, memory, disk), TiDB components versions, OS name.

To view the full content of the usage information shared to PingCAP, execute the following SQL statement:

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY;
```

### TiDB Dashboard

When the telemetry collection feature is enabled in TiDB Dashboard, user operations on the TiDB Dashboard web UI will be shared, including (but not limited to):

- A randomly generated telemetry ID.
- User operation information, such as the name of the TiDB Dashboard web page accessed by the user.
- Browser and OS information, such as browser name, OS name, screen resolution.

To view the full content of the usage information shared to PingCAP, use the [Network Activity Inspector of Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/network) or the [Network Monitor of Firefox Developer Tools](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor).

### TiUP

When the telemetry collection feature is enabled in TiUP, user operations with TiUP will be shared, including (but not limited to):

- A randomly generated telemetry ID.
- Execution status of TiUP commands, such as whether the execution is successful and the execution duration.
- Deployment characteristics, such as the size of hardware, TiDB components versions, deployment configuration names that have been modified.

To view the full content of the usage information shared to PingCAP, set the `TIUP_CLUSTER_DEBUG=enable` environment variable when executing the TiUP command. For example:

{{< copyable "shell-regular" >}}

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

## Disable telemetry

### Disable TiDB telemetry at deployment

When deploying TiDB clusters, configure [`enable-telemetry = false`](/tidb-configuration-file.md#enable-telemetry) to disable the TiDB telemetry collection on all TiDB instances. You can also use this setting to disable telemetry in the deployed TiDB clusters, which do not take effect until you restart the clusters.

Detailed steps to disable telemetry in different deployment tools are listed below.

<details>
  <summary>Binary deployment</summary>

Create a configuration file `tidb_config.toml` with the following content:

{{< copyable "" >}}

```toml
enable-telemetry = false
```

Specify the command line parameter `--config=tidb_config.toml` when starting TiDB to take effect.

See [TiDB Configuration Options](/command-line-flags-for-tidb-configuration.md#--config) and [TiDB Configuration File](/tidb-configuration-file.md#enable-telemetry) for details.

</details>

<details>
  <summary>TiUP Playground</summary>

Create a configuration file `tidb_config.toml` with the following content:

{{< copyable "" >}}

```toml
enable-telemetry = false
```

When starting TiUP Playground, specify the command line parameter `--db.config tidb_config.toml` to take effect, for example:

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.config tidb_config.toml
```

See [Quickly Deploy a Local TiDB Cluster](/tiup/tiup-playground.md) for details.

</details>

<details>
  <summary>TiUP Cluster deployment</summary>

Modify the deployment topology file `topology.yaml` to add or modify the following:

{{< copyable "" >}}

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

{{< copyable "sql" >}}

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

{{< copyable "" >}}

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

{{< copyable "" >}}

```toml
[dashboard]
disable-telemetry = true
```

When starting TiUP Playground, specify the command line parameter `--pd.config pd_config.toml` to take effect, for example:

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config pd_config.toml
```

See [Quickly Deploy a Local TiDB Cluster](/tiup/tiup-playground.md) for details.

</details>

<details>
  <summary>TiUP Cluster deployment</summary>

Modify the deployment topology file `topology.yaml` to add or modify the following:

{{< copyable "" >}}

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

{{< copyable "shell-regular" >}}

```shell
tiup telemetry disable
```

## Check telemetry status

For TiDB telemetry, execute the following SQL statement to check the telemetry status:

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY;
```

If the `DATA_PREVIEW` column is empty, TiDB telemetry is off. If not, TiDB telemetry is on. You can also check when the usage information was shared previously according to the `LAST_STATUS` column.

For TiUP telemetry, execute the following command to check the telemetry status:

{{< copyable "shell-regular" >}}

```shell
tiup telemetry status
```

## Compliance

In order to meet compliance requirements in different countries or regions, the usage information will be sent to servers located in different countries according to the IP address of the sender machine as follows:

- For IP addresses from mainland China, usage information will be sent and stored on cloud servers in mainland China.
- For IP addresses other than mainland China, usage information will be sent and stored on cloud servers in US.

See [PingCAP Privacy Policy](https://pingcap.com/privacy-policy) for details.
