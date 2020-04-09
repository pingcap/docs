---
title: Upgrade TiFlash Nodes
summary: Learn how to upgrade TiFlash nodes.
category: reference
---

# Upgrade TiFlash Nodes

To upgrade TiFlash nodes, take the following steps:

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
