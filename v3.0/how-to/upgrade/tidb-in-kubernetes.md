---
title: Rolling Update TiDB in Kubernetes
category: how-to
---

# Rolling Update TiDB in Kubernetes

When you perform a rolling update for a TiDB cluster in Kubernetes, the Pod is shut down and recreated with the new image or/and configuration serially in the order of TiDB, TiKV, PD. Under the high available deployment topology (minimum requirements: PD \* 3, TiKV \* 3, TiDB \* 2), rolling updating PD and TiKV servers does not impact the running clients.

For clients that can retry stale connections, rolling updating TiDB servers does not impact the running clients neither. However, for clients that **can not** retry stale connections, rolling updating TiDB servers will close the client connections and cause the request to fail. We recommend to add connection retry ability for the clients or to perform rolling update for TiDB servers in idle time.

## Upgrade TiDB cluster version

1. Change `image` of PD, TiKV and TiDB to different image versions in `values.yaml`.
2. Run `helm upgrade` command：

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade ${releaseName} pingcap/tidb-cluster -f values.yaml --version=v1.0.0-beta.3
    ```

3. Witness the upgrade progress：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl -n ${namespace} get pod -o wide
    ```

## Change TiDB cluster Configuration

By default, the change of configuration files is not applied to the TiDB cluster automatcially. The servers load the new configuration file when being restarted.

You can enable rolling update on configuration change by setting `enableConfigMapRollout` to `true` in the `values.yaml`. The steps are as follows:

1. Set `enableConfigMapRollout` to `true` in the `values.yaml`.
2. Change the configurations in `values.yaml` as needes.
3. Run `helm upgrade` command：

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade ${releaseName} pingcap/tidb-cluster -f values.yaml --version=v1.0.0-beta.3
    ```

4. Witness the upgrade process：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl -n ${namespace} get pod -o wide
    ```

> **Note：**
>
> - Changing `enableConfigMapRollout` variable against a running cluster will trigger an rolling-update of PD, TiKV, TiDB servers even if there's no configuration change.
> - currently, changing PD's scheduler and replication configurations(the configuration key under `[scheduler]` and `[replication]` of the PD config file) after cluster creation has no effect. You have to configure these variables via `pd-ctl` after the cluster creation, see: [pd-ctl](/reference/tools/pd-control.md).
