---
title: Upgrade TiFlash Nodes
summary: Learn how to upgrade TiFlash nodes.
category: reference
---

# Upgrade TiFlash Nodes

Currently, TiFlash does not support upgrading using `tiup cluster upgrade`. To upgrade TiFlash, take the following steps:

1. Refer to [Scale in a TiFlash node](/how-to/scale/with-tiup.md#sclale-in-a-tiflash-node), and scale in all the nodes in TiFlash.

2. Run the upgrade command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster upgrade test v4.0.0-rc
    ```

3. Run the scale-out command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster scale-out test scale-out.yaml
    ```

4. View the cluster status:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

5. Access the monitoring platform using your browser, and view the status of the cluster.
