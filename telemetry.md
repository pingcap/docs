---
title: Telemetry
summary: Learn the telemetry feature, how to disable the feature and view its status.
aliases: ['/docs/dev/telemetry/','/tidb/dev/sql-statement-admin-show-telemetry']
---

# Telemetry

When the telemetry feature is enabled, TiUP and TiSpark collect usage information and share the information with PingCAP to help understand how to improve the product.

> **Note:**
>
> - Starting from TiUP v1.11.3, the telemetry feature in TiUP is disabled by default, which means TiUP usage information is not collected by default. If you upgrade from a TiUP version earlier than v1.11.3 to v1.11.3 or a later version, the telemetry feature keeps the same status as before the upgrade.
> - Starting from TiSpark v3.0.3, the telemetry feature in TiSpark is disabled by default, which means TiSpark usage information is not collected by default.
> - Starting from v8.1.0, the telemetry feature in TiDB and TiDB Dashboard is removed.

## What is shared when telemetry is enabled?

The following sections describe the shared usage information in detail for TiUP and TiSpark. The usage details that get shared might change over time. These changes (if any) will be announced in [release notes](/releases/release-notes.md).

> **Note:**
>
> In **ALL** cases, user data stored in the TiDB cluster will **NOT** be shared. You can also refer to [PingCAP Privacy Policy](https://pingcap.com/privacy-policy).

### TiUP

When the telemetry collection feature is enabled in TiUP, usage details of TiUP will be shared, including (but not limited to):

- A randomly generated telemetry ID.
- Execution status of TiUP commands, such as whether the execution is successful and the execution duration.
- Deployment characteristics, such as the size of hardware, TiDB components versions, and deployment configuration names that have been modified.

To view the full content of the usage information shared to PingCAP, set the `TIUP_CLUSTER_DEBUG=enable` environment variable when executing the TiUP command. For example:

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

### TiSpark

> **Note:**
>
> Starting from v3.0.3, the telemetry collection is disabled by default in TiSpark, and usage information is not collected and shared with PingCAP.

When the telemetry collection feature is enabled for TiSpark, the Spark module will share the usage details of TiSpark, including (but not limited to):

- A randomly generated telemetry ID.
- Some configuration information of TiSpark, such as the read engine and whether streaming read is enabled.
- Cluster deployment information, such as the machine hardware information, OS information, and component version number of the node where TiSpark is located.

You can view TiSpark usage information that is collected in Spark logs. You can set the Spark log level to INFO or lower, for example:

```shell
grep "Telemetry report" {spark.log} | tail -n 1
```

## Enable telemetry

### Enable TiUP telemetry

To enable the TiUP telemetry collection, execute the following command:

```shell
tiup telemetry enable
```

### Enable TiSpark telemetry

To enable the TiSpark telemetry collection, configure `spark.tispark.telemetry.enable = true` in the TiSpark configuration file.

## Disable telemetry

### Disable TiUP telemetry

To disable the TiUP telemetry collection, execute the following command:

```shell
tiup telemetry disable
```

### Disable TiSpark telemetry

To disable the TiSpark telemetry collection, configure `spark.tispark.telemetry.enable = false` in the TiSpark configuration file.

## Check telemetry status

For TiUP telemetry, execute the following command to check the telemetry status:

```shell
tiup telemetry status
```

## Compliance

To meet compliance requirements in different countries or regions, the usage information is sent to servers located in different countries according to the IP address of the sender machine:

- For IP addresses from the Chinese mainland, usage information is sent to and stored on cloud servers in the Chinese mainland.
- For IP addresses from outside of the Chinese mainland, usage information is sent to and stored on cloud servers in the US.

See [PingCAP Privacy Policy](https://www.pingcap.com/privacy-policy/) for details.
