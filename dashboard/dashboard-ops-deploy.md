---
title: Deploy TiDB Dashboard
category: how-to
---

# Deploy TiDB Dashboard

The TiDB Dashboard interface is built into the PD component of TiDB v4.0 or higher, and no additional deployment is required. You can just deploy a standard TiDB cluster and TiDB Dashboard is be integrated natively.

See to the following documents to learn how to deploy a standard TiDB cluster:

+ [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md#deploy-a-local-test-environment-using-tiup-playground)
+ [Deploy TiDB in Production Environment](/production-deployment-using-tiup.md)
+ [Kubernetes environment deployment](https://pingcap.com/docs/tidb-in-kubernetes/stable/access-dashboard/)

> **Note:**
>
> You cannot deploy TiDB Dashboard in a TiDB cluster earlier than v4.0.

## Deployment with multiple PD instances

When multiple PD instances are deployed in the cluster, only one of these instances provides the TiDB Dashboard service.

PD instances, when running for the first time, automatically negotiate with each other and choose one instance to provide the TiDB Dashboard service. After the negotiation is completed, the TiDB Dashboard service will always run on the chosen instance no matter it is restarted or scaled out, unless this instance is manually scaled in. TiDB Dashboard will not run on other PD instances. This negotiation process can be completed automatically without user intervention.

When you access a PD instance that does not provide the TiDB Dashboard service, the browser receives a redirection instruction and automatically guides you to re-access the PD instance that provides the TiDB Dashboard service, so that you can use the service normally. This process is shown in the image below.

![Process Schematic](/media/dashboard/dashboard-ops-multiple-pd.png)

> **Note:**
>
> The PD instance that provides the TiDB Dashboard service might not be consistent with the PD leader.

### Check the PD instance that actually provides the TiDB Dashboard service

If a started cluster is deployed using TiUP, you can use the `tiup cluster display` command to check which PD node provides the TiDB Dashboard service. Replace `CLUSTER_NAME` with the cluster name.

{{< copyable "shell-regular" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

A sample output is as follows:

```bash
http://192.168.0.123:2379/dashboard/
```

> **Note:**
>
> This feature is available only in the later version of the `tiup cluster` deployment tool (v1.0.3 or later). You can upgrade `tiup cluster` with the following commands:
>
> {{< copyable "shell-regular" >}}
>
> ```bash
> tiup update --self
> tiup update cluster --force
> ```

### Switch to another PD instance to provide TiDB Dashboard service

If a started cluster is deployed using TiUP, you can use the `tiup ctl pd` command to change the PD instance that provides the TiDB Dashboard service, or re-specify a PD instance to provide the TiDB Dashboard service with TiDB Dashboard disabled:

{{< copyable "shell-regular" >}}

```bash
tiup ctl pd -u http://127.0.0.1:2379 config set dashboard-address http://9.9.9.9:2379
```

In the command above:

- Replace `127.0.0.1:2379` with the IP and port of any PD instance.
- Replace `9.9.9.9:2379` with the IP and port of the new PD instance that you desire to run the TiDB Dashboard service.

After the modification above, you can use the `tiup cluster display` command to confirm whether the modification takes effect (replace `CLUSTER_NAME` with the cluster name):

{{< copyable "shell-regular" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

> **Warning:**
>
> If you change the instance to run TiDB Dashboard, the local data stored in the previous TiDB Dashboard instance will be lost, including the traffic visualization history and historical search records.

## Disable TiDB Dashboard

If a started cluster is deployed using TiUP, use the `tiup ctl pd` command to disable TiDB Dashboard on all PD instances (replace `127.0.0.1:2379` with the IP and port of any PD instance):

{{< copyable "shell-regular" >}}

```bash
tiup ctl pd -u http://127.0.0.1:2379 config set dashboard-address none
```

After disabling TiDB Dashboard, checking which PD instance provides the TiDB Dashboard service will fail:

```
Error: TiDB Dashboard is disabled
```

Visiting the TiDB Dashboard address of any PD instance via the browser will also fail:

```
Dashboard is not started.
```

## Re-enable TiDB Dashboard

If a started cluster is deployed using TiUP, use the `tiup ctl pd` command to request PD to renegotiate an instance to run TiDB Dashboard (replace `127.0.0.1:2379` with the IP and port of any PD instance) :

{{< copyable "shell-regular" >}}

```bash
tiup ctl pd -u http://127.0.0.1:2379 config set dashboard-address auto
```

After executing the command above, use the `tiup cluster display` command to view the TiDB Dashboard instance address automatically negotiated by PD (replace `CLUSTER_NAME` with the cluster name):

{{< copyable "shell-regular" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

You can also re-enable TiDB Dashboard by manually specifying which PD instance provides the TiDB Dashboard service. For specific operations, see [Switch to another PD instance to provide TiDB Dashboard service](#switch-to-another-pd-instance-to-provide-tidb-dashboard-service).

> **Warning:**
>
> If the newly enabled TiDB Dashboard instance is inconsistent with the previous instance that provides the TiDB Dashboard service, the local data stored in the previous TiDB Dashboard instance will be lost, including traffic visualization history and historical search records.

## Next

- See [Access TiDB Dashboard](/dashboard/dashboard-access.md) to learn how to access and sign into the TiDB Dashboard interface.

- See [Improve TiDB Dashboard Security](/dashboard/dashboard-ops-security.md) to learn how to enhance the security of TiDB Dashboard, such as configuring a firewall.
