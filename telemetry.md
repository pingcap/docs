---
title: Telemetry
summary: Learn the telemetry feature, how to disable the feature and view its status.
aliases: ['/docs/dev/telemetry/','/tidb/dev/sql-statement-admin-show-telemetry']
---

# Telemetry

When the telemetry feature is enabled, TiUP collects usage information and shares the information with PingCAP to help understand how to improve the product.

> **Note:**
>
> - Starting from TiUP v1.11.3, the telemetry feature in TiUP is disabled by default, which means TiUP usage information is not collected by default. If you upgrade from a TiUP version earlier than v1.11.3 to v1.11.3 or a later version, the telemetry feature keeps the same status as before the upgrade.
> - For versions from v8.1.0 to v8.5.1, the telemetry feature in TiDB and TiDB Dashboard is removed.
> - Starting from v8.5.3, TiDB reintroduces the telemetry feature. However, it only logs telemetry-related information locally and no longer sends data to PingCAP over the network.

## What is shared when telemetry is enabled?

The following sections describe the shared usage information in detail for TiUP. The usage details that get shared might change over time. These changes (if any) will be announced in [release notes](/releases/_index.md).

> **Note:**
>
> In **ALL** cases, user data stored in the TiDB cluster will **NOT** be shared. You can also refer to [PingCAP Privacy Policy](https://pingcap.com/privacy-policy).

When the telemetry collection feature is enabled in TiUP, usage details of TiUP will be shared, including (but not limited to):

- A randomly generated telemetry ID.
- Execution status of TiUP commands, such as whether the execution is successful and the execution duration.
- Deployment characteristics, such as the size of hardware, TiDB components versions, and deployment configuration names that have been modified.

To view the full content of the usage information shared to PingCAP, set the `TIUP_CLUSTER_DEBUG=enable` environment variable when executing the TiUP command. For example:

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

## Enable telemetry

To enable the TiUP telemetry collection, execute the following command:

```shell
tiup telemetry enable
```

## Disable telemetry

To disable the TiUP telemetry collection, execute the following command:

```shell
tiup telemetry disable
```

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
