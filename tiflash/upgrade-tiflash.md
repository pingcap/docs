---
title: Upgrade TiFlash Nodes
summary: Learn how to upgrade TiFlash nodes.
category: reference
aliases: ['/docs/v3.1/tiflash/upgrade-tiflash/','/docs/v3.1/reference/tiflash/upgrade/']
---

# Upgrade TiFlash Nodes

> **Note:**
>
> To upgrade TiFlash from the Pre-RC version to a later version, contact [PingCAP](mailto:info@pingcap.com) for more information and help.

Before the upgrade, make sure that the cluster is started. To upgrade TiFlash nodes, take the following steps:

1. Back up the `tidb-ansible` folder:

    {{< copyable "shell-regular" >}}

    ```shell
    mv tidb-ansible tidb-ansible-bak
    ```

2. Download tidb-ansible that corresponds to the tag of TiDB v3.1:

    {{< copyable "shell-regular" >}}

    ```shell
    git clone -b $tag https://github.com/pingcap/tidb-ansible.git
    ```

3. Download binary:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook local_prepare.yml
    ```

4. Edit the `inventory.ini` file.

5. Rolling upgrade TiFlash:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update.yml --tags tiflash
    ```

6. Rolling upgrade the TiDB monitoring component:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update_monitor.yml
    ```
