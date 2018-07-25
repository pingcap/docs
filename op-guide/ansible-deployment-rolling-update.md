---
title: Upgrade TiDB Using TiDB-Ansible
summary: Use TiDB-Ansible to perform a rolling update for a TiDB cluster.
category: operations
---

# Upgrade TiDB Using TiDB-Ansible

When you perform a rolling update for a TiDB cluster, the service is shut down serially and is started after you update the service binary and the configuration file. If the load balancing is configured in the front-end, the rolling update of TiDB does not impact the running applications. Minimum requirements: `pd*3, tidb*2, tikv*3`.

> **Note:** If the binlog is enabled, and Pump and Drainer services are deployed in the TiDB cluster, stop the Drainer service before the rolling update. The Pump service is automatically updated in the rolling update of TiDB.

## Upgrade the component version

- To upgrade between large versions, you need to upgrade [`tidb-ansible`](https://github.com/pingcap/tidb-ansible). If you want to upgrade the version of TiDB from 1.0 to 2.0, see [TiDB 2.0 Upgrade Guide](tidb-v2-upgrade-guide.md). 

- For a minor upgrade, it is also recommended to update `tidb-ansible` for the latest configuration file templates, features, and bug fixes.

### Download the binary automatically

1. Edit the value of the `tidb_version` parameter in the `/home/tidb/tidb-ansible/inventory.ini` file, and specify the version number you need to upgrade to.

    For example, to upgrade from `v2.0.2` to `v2.0.3`:

    ```
    tidb_version = v2.0.3
    ```

2. Delete the existing `downloads` directory `/home/tidb/tidb-ansible/downloads/`.

    ```
    $ cd /home/tidb/tidb-ansible
    $ rm -rf downloads
    ```

3. Use `playbook` to download the TiDB `v2.0.3` binary and replace the existing binary in `/home/tidb/tidb-ansible/resource/bin/` with it automatically.

    ```
    $ ansible-playbook local_prepare.yml
    ```

### Download the binary manually

You can also download the binary manually. Use `wget` to download the binary and replace the existing binary in `/home/tidb/tidb-ansible/resource/bin/` with it manually.

```
wget http://download.pingcap.org/tidb-v2.0.3-linux-amd64-unportable.tar.gz
```

> **Note:** Remember to replace the version number in the download link with the one you need.

### Perform a rolling update using Ansible

- Apply a rolling update to the PD node (only upgrade the PD service)

    ```
    $ ansible-playbook rolling_update.yml --tags=pd
    ```

    When you apply a rolling update to the PD leader instance, if the number of PD instances is not less than 3, Ansible migrates the PD leader to another node before stopping this instance.

- Apply a rolling update to the TiKV node (only upgrade the TiKV service)

    ```
    $ ansible-playbook rolling_update.yml --tags=tikv
    ```

    When you apply a rolling update to the TiKV instance, Ansible migrates the Region leader to other nodes. The concrete logic is as follows: Call the PD API to add the `evict leader scheduler` -> Inspect the `leader_count` of this TiKV instance every 10 seconds -> Wait the `leader_count` to reduce to below 10, or until the times of inspecting the `leader_count` is more than 12 -> Start closing the rolling update of TiKV after two minutes of timeout -> Delete the `evict leader scheduler` after successful start. The operations are executed serially.

    If the rolling update fails in the process, log in to `pd-ctl` to execute `scheduler show` and check whether `evict-leader-scheduler` exists. If it does exist, delete it manually. Replace `{PD_IP}` and `{STORE_ID}` with your PD IP and the `store_id` of the TiKV instance:

    ```
    $ /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://{PD_IP}:2379"$ /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://{PD_IP}:2379"
    » scheduler show
    [
      "label-scheduler",
      "evict-leader-scheduler-{STORE_ID}",
      "balance-region-scheduler",
      "balance-leader-scheduler",
      "balance-hot-region-scheduler"
    ]
    » scheduler remove evict-leader-scheduler-{STORE_ID}
    ```

- Apply a rolling update to the TiDB node (only upgrade the TiDB service)

    If the binlog is enabled in the TiDB cluster, the Pump service is automatically upgraded in the rolling update of the TiDB service.

    ```
    $ ansible-playbook rolling_update.yml --tags=tidb
    ```

- Apply a rolling update to all services (upgrade PD, TiKV, and TiDB in sequence)

    If the binlog is enabled in the TiDB cluster, the Pump service is automatically upgraded in the rolling update of the TiDB service.

    ```
    $ ansible-playbook rolling_update.yml
    ```

- Apply a rolling update to the monitoring component

    ```
    $ ansible-playbook rolling_update_monitor.yml
    ```

## Modify component configuration

This section describes how to modify component configuration using Ansible.

1. Update the component configuration template.

    The component configuration template of the TiDB cluster is in the `/home/tidb/tidb-ansible/conf` folder.

    | Component | Template Name of the Configuration File |
    | :-------- | :----------: |
    | TiDB | tidb.yml  |
    | TiKV | tikv.yml  |
    | PD | pd.yml  |

    The comment status if the default configuration item, which uses the default value. To modify it, you need to cancel the comment by removing `#` and then modify the corresponding parameter value.

    The configuration template uses the yaml format, so separate the parameter name and the parameter value using `:`, and indent two spaces.

    For example, modify the value of the `high-concurrency`, `normal-concurrency` and `low-concurrency` parameters to 16 for the TiKV component:

    ```bash
    readpool:
      coprocessor:
        # Notice: if CPU_NUM > 8, the default thread pool size for coprocessors
        # will be set to CPU_NUM * 0.8.
        high-concurrency: 16
        normal-concurrency: 16
        low-concurrency: 16
    ```

2. After modifying the component configuration, you need to perform a rolling update using Ansible. See [Perform a rolling update using Ansible](#perform-a-rolling-update-using-ansible).