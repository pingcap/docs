---
title: Upgrade TiFlash Nodes
summary: Learn how to upgrade TiFlash nodes.
category: reference
---

# Upgrade TiFlash Nodes

To upgrade TiFlash nodes, take the following steps:

1. Download the new TiFlash binary to the Control Machine by either of the following two methods:

    - Download the latest TiDB Ansible, or update the TiDB Ansible git repository by running the `git pull` command. Then run the `ansible-playbook local_prepare.yml` command.
    - Manually download TiFlash binary and overwrite to `resource/bin/tiflash`.

2. Rolling upgrade TiFlash:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update.yml --tags tiflash
    ```

3. Rolling upgrade the TiDB monitoring component:

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update_monitor.yml
    ```
