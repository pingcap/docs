---
title: Use Clinic
summary: Introduces in detail how to troubleshoot cluster problems remotely and perform a quick check of the cluster status locally with the Clinic diagnosis service on a cluster deployed using TiUP.
---

# Use Clinic

For TiDB clusters and DM clusters deployed using TiUP, the Clinic diagnosis service (Clinic) can troubleshoot cluster problems remotely and perform a quick check of the cluster status locally with the Clinic diagnostic tool Diag (Diag) and the Clinic Server cloud service (Clinic Server).

The Clinic diagnostic service is currently in the Beta testing stage.

> **Note:**
>
> - Clinic temporarily **does not support** collecting data in the clusters with TLS encryption enabled and the clusters deployed using TiDB Ansible.

## Usage scenarios

- [Troubleshoot cluster problems remotely](#troubleshoot-cluster-problems-remotely):

    - When your cluster has some problems, and you need the PingCAP technical support, you can perform the following operations to assist technical support: collect diagnostic data with Diag, upload the data to Clinic Server, and provide the data link to technical support staff.

    > **Note:**
    >
    > - Clinic is currently in the Beta testing stage, so only the invited users can use the service. If you need to upload data to Clinic Server using Diag, you should get a trial account from the PingCAP technical support staff you contacted before.
    > - In the Clinic Beta version, external users cannot use the features of the Clinic server. After you upload the collected data to the Clinic Server and get the data link, only authorized PingCAP technical support staff can access the link and view the data.

    - When your cluster has some problems, but you cannot analyze them immediately, you can use Diag to collect data and save it for later analysis.

- [Perform a quick check for the cluster status locally](#perform-a-quick-check-for-the-cluster-status-locally):

    Even if your cluster can run normally, it is necessary to periodically check the cluster for potential stability risks. You can check the potential health risks of the cluster using the Clinic local quick check feature. Clinic Beta version mainly provides a rationality check for cluster configuration items to discover unreasonable configurations and provide modification suggestions.

## Prerequisites

If you have installed TiUP on the control machine, run the following command to install Diag with one click:

{{< copyable "shell-regular" >}}

```bash
tiup install diag
```

If you have installed Diag locally, you can also use the following command to upgrade Diag to the latest version with one click:

{{< copyable "shell-regular" >}}

```bash
tiup update diag
```

> **Note:**
>
> - For offline clusters, you need to deploy Diag offline. For details, refer to [Deploy TiUP offline: Method 2](production-deployment-using-tiup.md#method-2-deploy-tiup-offline).
> - Diag is **only** included in the TiDB Server offline mirror package of v5.4.0 and later versions.

## Troubleshoot cluster problems remotely

Diag can quickly collect the diagnostic data in the TiDB cluster, including monitoring data and configuration information.

### Step 1. Check the data needs to be collected

For a detailed list of data that can be collected by Diag, see [Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md). You are recommended to collect complete monitoring data, configuration information, and other data to help improve the efficiency of the later diagnosis.

### Step 2. Collect data

With Diag, you can collect data in the TiDB clusters and the DM clusters deployed using TiUP.

#### Collect data in TiDB clusters

1. Run the command to collect data using Diag.

    For example, to collect the diagnostic data from 4 hours ago to 2 hours ago at the current time, run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    Description of the parameters for data collection:

    - `-f/--from`: Specifies the start point of the data collection time. If you did not specify this parameter, the starting point is 2 hours before the current time by default. To modify the time zone, use the syntax `-f="12:30 +0800"`. If you did not specify the time zone information in this parameter, such as `+0800`, the time zone is UTC by default.
    - `-t/--to`: Specifies the end point of the data collection time. If you did not specify this parameter, the end point is the current moment by default. To modify the time zone, use the syntax `-f="12:30 +0800"`. If you did not specify the time zone information in this parameter, such as `+0800`, the time zone is UTC by default.

    Parameter usage tips:

    In addition to specifying the data collection time, you can use Diag to specify more parameters. To see all parameters, use the `tiup diag collect -h` command.

    - `-l`: The bandwidth limit for transferring files, the unit is Kbit/s, and the default value is `100000` (the `-l` parameter of scp).
    - `-N/--node`: Supports collecting the data only in the specified node, the format is `ip:port`.
    - `--include`: Only collects specific types of data, optional values are `system`, `monitor`, `log`, `config`, `db_vars`.
    - `--exclude`: Does not collect specific types of data, optional values are `system`, `monitor`, `log`, `config`, `db_vars`.

    After running the command, Diag does not start collecting data immediately. Diag asks you whether to collect data while providing the estimated data size and the path stored data in the result. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    Estimated size of data to collect:
    Host               Size       Target
    ----               ----       ------
    172.16.7.129:9090  43.57 MB   1775 metrics, compressed
    172.16.7.87        0 B        /tidb-deploy/tidb-4000/log/tidb_stderr.log
    ... ...
    172.16.7.179       325 B      /tidb-deploy/tikv-20160/conf/tikv.toml
    Total              2.01 GB    (inaccurate)
    These data will be stored in /home/qiaodan/diag-fNTnz5MGhr6
    Do you want to continue? [y/N]: (default=N)
    ```

2. To confirm that you want to start collecting data, enter `Y`.

    Collecting data takes a certain amount of time. The required time is related to the amount of data to be collected. For example, in a test environment, collecting 1 GB of data takes about 10 minutes.

    After the collection is complete, Diag provides the folder path where the collected data is located. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
    ```

#### Collect data in DM clusters

1. Run the command to collect data using Diag.

    For example, to collect the diagnostic data from 4 hours ago to 2 hours ago at the current time, run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collectdm ${cluster-name} -f="-4h" -t="-2h"
    ```

    For the parameters used in the above commands or other parameters used when using Diag, refer to [Collect data in DM clusters](#collect-data-in-tidb-clusters).

    After running the command, Diag does not start collecting data immediately. Diag asks you whether to collect data while providing the estimated data size and the path stored data in the result.

2. To confirm that you want to start collecting data, enter `Y`.

    Collecting data takes a certain amount of time. The required time is related to the amount of data to be collected. For example, in a test environment, collecting 1 GB of data takes about 10 minutes.

    After the collection is complete, Diag provides the folder path where the collected data is located. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    Collected data are stored in /home/qiaodan/diag-fNTnz5MGhr6
    ```

### Step 3. View data locally (optional)

The collected data is stored in separate subdirectories based on its data source. These subdirectories are named after the machine name and port number. The storage locations of the configuration, logs, and other files of each node are the same as the relative path stored in the real server:

- Basic information of the system and the hardware: In `insight.json`
- Contents in the system `/etc/security/limits.conf`: In `limits.conf`
- List of kernel parameters: In `sysctl.conf`
- Kernel logs: In `dmesg.log`
- Network connection when collecting data: In `ss.txt`
- Configuration data: in the `config.json` directory of every node
- Meta-information for the cluster itself: In `meta.yaml` (this file is located at the top level of the directory that stored collected data)
- Monitoring data: In the `/monitor` file directory. The monitoring data compressed by default and cannot be viewed directly. To directly view the JSON file that has the monitoring data directly, disable compression with the `--compress-metrics=false` parameter when collecting data.

### Upload data

To provide the cluster diagnostic data to PingCAP technical support staff, you need to upload the data to Clinic Server first, and then send the data link to the staff. Clinic Server is a cloud service for Clinic that stores and shares the diagnostic data securely.

Depending on the network connection of the cluster, you can choose one of the following methods to upload data:

- Methods 1: If the network where the cluster is located can directly connect to the Clinic Server, you can [directly upload data using the upload command](#method-1-upload-directly).
- Methods 2: If the network where the cluster is located cannot directly connect to the Clinic Server, you need to [pack the data and then upload it](#method-2-pack-and-upload-data).

#### Method 1: Upload directly

When the network where the cluster is located can directly connect to the Clinic Server, you can directly upload the folder with collected data obtained in [Step 2: Collect data](#step-2-collect-data) using the following command:

{{< copyable "shell-regular" >}}

```bash
 tiup diag upload ${filepath} -u=username -p='password'
 ```

> **Note:**
>
> Clinic is currently in the Beta testing stage, so only the invited users can use the service. You need to get a trial account from the PingCAP technical support staff you contacted before.

The output can be as follows:

{{< copyable "shell-regular" >}}

```bash
[root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag upload /home/qiaodan/diag-fNTnz5MGhr6
Enter Username: username
Enter Password: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
Completed!
Download URL: "https://clinic.pingcap.com:4433/diag/files?uuid=XXXX"
```

After the upload is complete, you need to send the data access link of `Download URL` to the PingCAP technical support staff you contacted before.

> **Note:**
>
> In the Beta version of the Clinic diagnostic service, external users cannot use the features of the Clinic server. The data access link is only open for the PingCAP technical support staff.

#### Method 2: Pack and upload data

If your cluster is deployed offline, you need to pack the data on your intranet and upload it to the Clinic Server using a network-connected device, because the network where the cluster is located cannot directly connect to the Clinic Server. The detailed operations are as follows:

1.Compress and encrypt the data package collected in [Step 2: Collect data](#step-2-collect-data).

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag package ${filepath}
    ```

    When packaging, Diag encrypts and compresses the data at the same time. In the test environment, 800 MB of data was compressed to 57 MB. The output can be as follows:

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/qiaodan/diag-fNTnz5MGhr6.diag
    ```

    After the data is packaged through the `package` command above, the data is in the `.diag` format. This file can only be decrypted and viewed after uploading it to the Clinic Server. If you need to directly forward the collected data instead of viewing it in the Clinic Server, you can compress the data and forward it by yourself.

2. Upload the package using the Clinic Server connectable network.

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag upload ${filepath} -u=username -p='password'
    ```

    > **Note:**
    >
    > Clinic is currently in the Beta testing stage, so only the invited users can use the service. You need to get a trial account from the PingCAP technical support staff you contacted before.

    The output can be as follows:

    {{< copyable "shell-regular" >}}

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 qiaodan]# tiup diag upload /home/qiaodan/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag upload /home/qiaodan/diag-fNTnz5MGhr6
    Enter Username: username
    Enter Password: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
    Completed!
    Download URL: "https://clinic.pingcap.com:4433/diag/files?uuid=XXXX"
    ```

    After the upload is complete, you need to send the data access link of `Download URL` to the PingCAP technical support staff you contacted before.

    > **Note:**
    >
    > In the Beta version of the Clinic diagnostic service, external users cannot use the features of the Clinic server. The data access link is only open for the PingCAP technical support staff.

## Perform a quick check for the cluster status locally

You can have a quick check for the cluster status locally using Diag. Even if your cluster can run normally, it is necessary to periodically check the cluster for potential stability risks. Clinic in Beta version mainly provides a rationality check for cluster configuration items to discover unreasonable configurations and provide modification suggestions.

1. Collect configuration data

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect ${cluster-name} --include="config"
    ```

    The configuration file data is relatively small. After the collection, the data is stored in the current path by default. In the test environment, for a cluster with 18 nodes, the size of configuration file data is less than 10 KB.

2. Diagnose configuration data

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag check ${subdir-in-output-data}
    ```

    `${subdir-in-output-data}` in the above command is the path stored the collected data, and this path has the `meta.yaml` file.

3. View the diagnostic result

    The diagnostic result is returned on the command line. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.5.1/diag check diag-fNTnz5MGhr6

    # Diagnostic result
    lili 2022-01-24T09:33:57+08:00

    ## 1. Cluster Information
    - Cluster ID: 7047403704292855808
    - Cluster Name: lili
    - Cluster Version: v5.3.0

    ## 2. Sample Information
    - Sample ID: fNTnz5MGhr6
    - Sampling Date: 2022-01-24T09:33:57+08:00
    - Sample Content:: [system monitor log config]

    ## 3. Diagnostic, including potential configuration problems
    In this inspection, 22 rules were executed.
    The results of **1** rules were abnormal and needed to be further discussed with support team.
    The following is the details of the abnormalities.

    ### Diagnostic result Summary
    The configuration rules are all derived from PingCAP’s OnCall Service.
    If the results of the configuration rules are found to be abnormal, they may cause the cluster to fail.
    There were **1** abnormal results.

    #### Path to save the diagnostic result file
    Rule Name: tidb-max-days
    - RuleID: 100
    - Variation: TidbConfig.log.file.max-days
    - For more information, please visit: https://s.tidb.io/msmo6awg
    - Check Result:
      TidbConfig_172.16.7.87:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.86:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.179:4000   TidbConfig.log.file.max-days:0   warning

    Result report and record are saved at diag-fNTnz5MGhr6/report-220125153215
    ```

    In the diagnostic result information (last part) of the above result example, for each configuration problem found, Diag provides a corresponding knowledge base link to view detailed configuration suggestions. In the example above, the relevant link is `https://s.tidb.io/msmo6awg`.

## FAQ

1. If the data upload fails, can I re-upload it?

    Yes. Data upload supports breakpoint upload. If the upload fails, you can upload it again directly.

2. After uploading data, I cannot open the returned data access link. What should I do?

    Clinic is currently in the Beta version, and external users cannot visit the data access link. Only authorized PingCAP technical support staff can access the link and view the data.

3. How long will the data uploaded to the Clinic Server be kept?

    After a technical support case is closed, PingCAP permanently deletes or anonymizes the corresponding data within 90 days.