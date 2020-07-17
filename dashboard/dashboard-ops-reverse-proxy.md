---
title: Use TiDB Dashboard behind a Reverse Proxy
aliases: ['/docs/dev/dashboard/dashboard-ops-reverse-proxy/']
---

# Use TiDB Dashboard behind a Reverse Proxy

You can use a reverse proxy to safely expose the TiDB Dashboard service from the internal network to the external.

## Use NGINX reverse proxy

### Step 1: Get the actual TiDB Dashboard address

When multiple PD instances are deployed in the cluster, only one of the PD instances actually runs TiDB Dashboard. Therefore, you need to ensure that the upstream of the reverse proxy points to the correct address. For details of this mechanism, see [Deployment with multiple PD instances](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances).

When you use the TiUP tool for deployment, execute the following command to get the actual TiDB Dashboard address (replace `CLUSTER_NAME` with your cluster name):

{{< copyable "shell-regular" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

The output is the actual TiDB Dashboard address. A sample is as follows:

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

### Step 2: Configure the NGINX reverse proxy

When you use [NGINX](https://nginx.org/) as the reverse proxy, take the following steps:

1. Use reverse proxy for TiDB Dashboard on the `80` port (for example). In the NGINX configuration file, add the following configuration:

    {{< copyable "" >}}

    ```nginx
    server {
        listen 80;
        location /dashboard/ {
        proxy_pass http://192.168.0.123:2379/dashboard/;
        }
    }
    ```

    Configure the URL filled in `proxy_pass` to be the actual address of the TiDB Dashboard obtained in [Step 1](#step-1-get-the-actual-tidb-dashboard-address).

   > **Warning:**
   >
   > You must keep the `/dashboard/` path in the `proxy_pass` directive to ensure that only the services under this path are reverse proxied. Otherwise, security risks will be introduced. See [Secure TiDB Dashboard](/dashboard/dashboard-ops-security.md).

2. Restart NGINX for the configuration to take effect.

3. Test whether the reverse proxy is effective: access the `/dashboard/` address on the `80` port of the machine where NGINX is located (such as `http://example.com/dashboard/`) to access TiDB Dashboard.

## Customize path prefix

TiDB Dashboard provides services by default in the `/dashboard/` path, such as `http://example.com/dashboard/`, which is the case even for reverse proxies. To configure the reverse proxy to provide the TiDB Dashboard service with a non-default path, such as `http://example.com/foo` or `http://example.com/`, take the following steps.

### Step 1: Modify PD configuration to specify the path prefix of TiDB Dashboard service

Modify the `public-path-prefix` configuration item in the `[dashboard]` category of the PD configuration to specify the path prefix of the TiDB Dashboard service. After this item is modified, restart the PD instance for the modification to take effect.

For example, if the cluster is deployed using TiUP and you want the service to run on `http://example.com/foo`, you can specify the following configuration:

{{< copyable "" >}}

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /foo
```

If you are deploying a new cluster, you can add the configuration above to the `topology.yaml` TiUP topology file and deploy the cluster. For specific instruction, see [TiUP deployment document](/production-deployment-using-tiup.md#step-3-edit-the-initialization-configuration-file).

For a deployed cluster:

1. Open the configuration file of the cluster in the edit mode (replace `CLUSTER_NAME` with the cluster name).

    {{< copyable "shell-regular" >}}

    ```bash
    tiup cluster edit-config CLUSTER_NAME
    ```

2. Modify or add configuration items under the `pd` configuration of `server_configs`. If no `server_configs` exists, add it at the top level:

    {{< copyable "" >}}

    ```yaml
    monitored:
      ...
    server_configs:
      tidb: ...
      tikv: ...
      pd:
        dashboard.public-path-prefix: /foo
      ...
    ```

    The configuration file after the modification is similar to the following file:

    {{< copyable "" >}}

    ```yaml
    monitored:
    ...
    server_configs:
      tidb: ...
      tikv: ...
      pd:
        dashboard.public-path-prefix: /foo
    ...
    ```

    Or

    {{< copyable "" >}}

    ```yaml
    monitored:
      ...
    server_configs:
      tidb: ...
      tikv: ...
      pd:
        dashboard.public-path-prefix: /foo
    ```

3. Perform a rolling restart to all PD instances for the modified configuration to take effect (replace `CLUSTER_NAME` with your cluster name):

    {{< copyable "shell-regular" >}}

   ```bash
   tiup cluster reload CLUSTER_NAME -R pd
   ```

See [Common TiUP Operations - Modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration) for details.

If you want that the TiDB Dashboard service is run in the root path (such as `http://example.com/`), use the following configuration:

{{< copyable "" >}}

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /
```

> **Warning:**
>
> After the modified and customized path prefix takes effect, you cannot directly access TiDB Dashboard. You can only access TiDB Dashboard through a reverse proxy that matches the path prefix.

### Step 2: Modify the NGINX reverse proxy configuration

Taking `http://example.com/foo` as an example, the corresponding NGINX configuration is as follows:

{{< copyable "" >}}

```nginx
server {
  listen 80;
  location /foo/ {
    proxy_pass http://192.168.0.123:2379/dashboard/;
  }
}
```

> **Warning:**
>
> Keep the `/dashboard/` path in the `proxy_pass` directive to ensure that only the services under this path are reverse proxied. Otherwise, security risks will be introduced. See [Secure TiDB Dashboard](/dashboard/dashboard-ops-security.md).

Change `http://192.168.0.123:2379/dashboard/` in the configuration to the actual address of the TiDB Dashboard obtained in [Step 1: Get the actual TiDB Dashboard address](#step-1-get-the-actual-tidb-dashboard-address).

If you want that the TiDB Dashboard service is run in the root path (such as `http://example.com/`), use the following configuration:

{{< copyable "" >}}

```nginx
server {
  listen 80;
  location / {
    proxy_pass http://192.168.0.123:2379/dashboard/;
  }
}
```

Modify the configuration and restart NGINX for the modified configuration to take effect.
