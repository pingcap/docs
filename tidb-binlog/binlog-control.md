---
title: binlogctl
summary: Learns how to use `binlogctl`.
category: reference
---

# binlogctl

[Binlog Control](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl) (`binlogctl` for short) is a command line tool for TiDB Binlog. You can use `binlogctl` to manage TiDB Binlog clusters.

You can use `binlogctl` to:

* Check the state of Pump or Drainer
* Pause or close Pump or Drainer
* Handle the abnormal state of Pump or Drainer

The following are its usage scenarios:

* An error occurs during data replication or you need to check the running state of Pump or Drainer.
* You need to pause or close Pump or Drainer when maintaining the cluster.
* A Pump or Drainer process exits abnormally, while the node state is not updated or is unexpected. This affects the data replication task.

## Download `binlogctl`

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz &&
wget https://download.pingcap.org/tidb-{version}-linux-amd64.sha256
```

To check the file integrity, execute the following command. If the result is OK, the file is correct.

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-{version}-linux-amd64.sha256
```

For TiDB v2.1.0 GA or later versions, `binlogctl` is integrated into the TiDB download package. For earlier versions, you need to download binlogctl separately:

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz &&
wget https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256
```

To check the file integrity, execute the following command. If the result is OK, the file is correct.

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
```

## Descriptions

Command line parameters:

```
Usage of binlogctl:
-V
    Outputs the binlogctl version information
-cmd string
    The command mode, including "generate_meta" (deprecated), "pumps", "drainers", "update-pump" ,"update-drainer", "pause-pump", "pause-drainer", "offline-pump", and "offline-drainer"
-data-dir string
    The file path where the checkpoint file of Drainer is stored ("binlog_position" by default) (deprecated)
-node-id string
    The ID of Pump or Drainer
-pd-urls string
    The address of PD. If multiple addresses exist, use "," to separate each ("http://127.0.0.1:2379" by default)
-ssl-ca string
    The file path of SSL CAs
-ssl-cert string
    The file path of the X509 certificate file in the PEM format
-ssl-key string
    The file path of the X509 key file in the PEM format
-time-zone string
    If a time zone is set, the corresponding time of the obtained `TSO` is printed in the "generate_meta" mode. For example, "Asia/Shanghai" is the CST time zone and "Local" is the local time zone
-show-offline-nodes
    Used with the `-cmd pumps` or `-cmd drainers` command. The two commands do not show the offline node by default unless this parameter is explicitly specified
```

Command examples:

- Check the state of all the Pump or Drainer nodes.

    Set `cmd` to `pumps` or `drainers`. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pumps
    ```

    ```
    [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=pump] [node="{NodeID: 1.1.1.1:8250, Addr: pump:8250, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd drainers
    ```

    ```
    [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=drainer] [node="{NodeID: 1.1.1.1:8249, Addr: 1.1.1.1:8249, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]
    ```

- Pause or close Pump or Drainer.

    You can use the following commands to pause or close services:

    | Command             | Description           | Example                                                                                             |
    | :--------------- | :------------- | :------------------------------------------------------------------------------------------------|
    | pause-pump      | Pause Pump      | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-pump -node-id ip-127-0-0-1:8250`       |
    | pause-drainer   | Pause Drainer   | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-drainer -node-id ip-127-0-0-1:8249`    |
    | offline-pump    | Close Pump      | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-pump -node-id ip-127-0-0-1:8250`     |
    | offline-drainer | Close Drainer   | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-drainer -node-id ip-127-0-0-1:8249`  |

    `binlogctl` sends the HTTP request to the Pump or Drainer node. After receiving the request, the node executes the exiting procedures accordingly.

- Modify the state of a Pump or Drainer node in abnormal states.

    When a Pump or Drainer node runs normally or when it is paused or closed in the normal process, it is in the normal state. In abnormal states, the Pump or Drainer node cannot correctly maintain its state. This affects data replication tasks. In this case, use `binlogctl` to repair the state information.

    To update the state of a Pump or Drainer node, set `cmd` to `update-pump` or `update-drainer`. The state can be `paused` or `offline`. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd update-pump -node-id ip-127-0-0-1:8250 -state paused
    ```

    > **Note:**
    >
    > When a Pump or Drainer node runs normally, it regularly updates its state to PD. The above command directly modifies the Pump or Drainer state saved in PD; therefore, do not use the command when the Pump or Drainer node runs normally. For more information, refer to [TiDB Binlog FAQ](/tidb-binlog/tidb-binlog-faq.md).
