---
title: Deploy and Maintain an Online TiDB Cluster Using TiUP No-sudo Mode
summary: Learns how to deploy and maintain an online TiDB cluster using TiUP no-sudo mode.
---

# Deploy and Maintain an Online TiDB Cluster Using TiUP No-sudo Mode

This document describes how to use the TiUP no-sudo mode to deploy a cluster.

> **Note:**
>
> For CentOS, only CentOS 8 or later versions are supported.

## Prepare the user and configure the SSH mutual trust

1. Log in to all deployment target machines in sequence, and use the `root` user to create a user named `tidb` with the following command. In no-sudo mode, there is no need to configure password-free sudo for the `tidb` user, that is, you do not need to add the `tidb` user to sudoers.
   
    ```shell
    adduser tidb
    ```
   
2. Start the `systemd` user mode for the `tidb` user on every deployment target machine. This step is required and do not skip it.

    1. Use the `tidb` user to set the `XDG_RUNTIME_DIR` environment variable.
   
        ```shell
        mkdir -p ~/.bashrc.d
        echo "export XDG_RUNTIME_DIR=/run/user/$(id -u)" > ~/.bashrc.d/systemd
        source ~/.bashrc.d/systemd
        ```
   
    2. Use `root` user to start user service.
   
        ```shell
        $ systemctl start user@1000.service # `1000` is the ID of the tidb user. You can get the user ID by executing the `id` command.
        $ systemctl status user@1000.service
        user@1000.service - User Manager for UID 1000
        Loaded: loaded (/usr/lib/systemd/system/user@.service; static; vendor preset>
        Active: active (running) since Mon 2024-01-29 03:30:51 EST; 1min 7s ago
        Main PID: 3328 (systemd)
        Status: "Startup finished in 420ms."
        Tasks: 6
        Memory: 6.1M
        CGroup: /user.slice/user-1000.slice/user@1000.service
                ├─dbus.service
                │ └─3442 /usr/bin/dbus-daemon --session --address=systemd: --nofork >
                ├─init.scope
                │ ├─3328 /usr/lib/systemd/systemd --user
                │ └─3335 (sd-pam)
                └─pulseaudio.service
                  └─3358 /usr/bin/pulseaudio --daemonize=no --log-target=journal
        ```
   
    Execute `systemctl --user` in the terminal. If no errors are reported, it indicates that it has started normally.

3. Use ssh-keygen in the central control computer to generate a key and copy the public key to other deployment machines.

## Prepare the topology file

1. Use the following command to generate topology file.

    ```shell
    tiup cluster template > topology.yaml
    ```
   
2. Edit the topology file.

    Compared with the previous mode, TiUP in no-sudo mode requires adding `systemd_mode: "user"` in the global block of `topology.yaml`. The `systemd_mode` parameter specifies whether to use systemd's user mode. If this parameter is not set, the default value is `system`, meaning sudo permissions are required. 

    Additionally, in no-sudo mode, because the non-root user `tidb` has no required permissions, `/data` cannot be used as the `deploy_dir` or `data_dir`. You must select a path accessible to non-root users. The following example uses relative paths and the final paths used are `/home/tidb/data/tidb-deploy` and `/home/tidb/data/tidb-data`. The rest is the same as the old version.

    ```yaml
    global:
      user: "tidb"
      systemd_mode: "user"
      ssh_port: 22
      deploy_dir: "data/tidb-deploy"
      data_dir: "data/tidb-data"
      arch: "amd64"
      ...
    ```
   
## Manually repair failed check items

Executing `tiup cluster check topology.yaml --user tidb` will generate some failed check items. The following is an example.

```shell
Node            Check         Result  Message
----            -----         ------  -------
192.168.124.27  thp           Fail    THP is enabled, please disable it for best performance
192.168.124.27  command       Pass    numactl: policy: default
192.168.124.27  os-version    Pass    OS is CentOS Stream 8 
192.168.124.27  network       Pass    network speed of ens160 is 10000MB
192.168.124.27  disk          Warn    mount point / does not have 'noatime' option set
192.168.124.27  disk          Fail    multiple components tikv:/home/blackcat/data/tidb-deploy/tikv-20160/data/tidb-data,tikv:/home/blackcat/data/tidb-deploy/tikv-20161/data/tidb-data are using the same partition 192.168.124.27:/ as data dir
192.168.124.27  selinux       Pass    SELinux is disabled
192.168.124.27  cpu-cores     Pass    number of CPU cores / threads: 16
192.168.124.27  cpu-governor  Warn    Unable to determine current CPU frequency governor policy
192.168.124.27  swap          Warn    swap is enabled, please disable it for best performance
192.168.124.27  memory        Pass    memory size is 9681MB
192.168.124.27  service       Fail    service firewalld is running but should be stopped
```

In no-sudo mode, the `tidb` user lacks sudo permissions, so running `tiup cluster check topology.yaml --apply --user tidb` can cause failed check items that cannot be automatically fixed due to insufficient permissions. You need to perform operations manually on the deployment machines using the `root` user.

1. Install the numactl tool.

    ```shell
    sudo yum -y install numactl
    ```
   
2. Close swap.

    ```shell
    swapoff -a || exit 0
    ```
   
3. Disable transparent huge pages.

    ```shell
    echo never > /sys/kernel/mm/transparent_hugepage/enabled
    ```

4. Start the `irqbalance` service.

    ```shell
   systemctl start irqbalance
    ```
   
5. Disable the firewall and disable firewall auto-start.

    ```shell
    systemctl stop firewalld.service
    systemctl disable firewalld.service
    ```
   
6. Modify sysctl parameters.
   
    ```shell
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_tw_recycle = 0">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    echo "vm.swappiness = 0">> /etc/sysctl.conf
    sysctl -p
    ```
   
7. Configure the user's `limits.conf` file.

    ```shell
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile          1000000
    tidb           hard    nofile          1000000
    tidb           soft    stack           32768
    tidb           hard    stack           32768
    tidb           soft    core            unlimited
    tidb           hard    core            unlimited
    EOF
    ```

## Deploy and manage the cluster

To use the `tidb` user created in the previous steps and avoid creating a new one, add `--user tidb` when running the `deploy` command.

```shell
tiup cluster deploy mycluster v8.1.0 topology.yaml --user tidb
```

Start the cluster:

```shell
tiup cluster start mycluster
```

Scale out the cluster:

```shell
tiup cluster scale-out mycluster scale.yaml --user tidb
```

Scale in the cluster:

```shell
tiup cluster scale-in mycluster -N 192.168.124.27:20160
```

Upgrade the cluster:

```shell
tiup cluster upgrade mycluster v8.2.0
```

## FAQ

### When you start user@.service, the following error occurs: `Failed to fully start up daemon: Permission denied`

This issue might be caused by the absence of `pam_systemd.so` in your `/etc/pam.d/system-auth.ued` file.

To resolve this issue, use the following command to check if the `/etc/pam.d/system-auth.ued` file contains the `pam_systemd.so` module. If not, append `session optional pam_systemd.so` to the end of the file.

```shell
grep 'pam_systemd.so' /etc/pam.d/system-auth.ued || echo 'session     optional      pam_systemd.so' >> /etc/pam.d/system-auth.ued
```
