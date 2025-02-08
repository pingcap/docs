---
title: Deploy and Maintain an Online TiDB Cluster Using TiUP No-sudo Mode
summary: Learns how to deploy and maintain an online TiDB cluster using TiUP no-sudo mode.
---

# Deploy and Maintain an Online TiDB Cluster Using TiUP No-sudo Mode


This document focuses on how to use the TiUP no-sudo Mode to deploy a cluster.

> **Note:**
>
> CentOS version limit: CentOS 8 and later versions

## Prepare user and configure SSH mutual trust
1. Log in to all deployment target machines in sequence and use the `root` user to create a normal user named `tidb` with the following command (take the `tidb` user as an example). In no-sudo mode, there is no need to configure password-free sudo for the `tidb` user, that is, there is no need to add the `tidb` user to sudoers.
   
    {{< copyable "shell-regular" >}}

    ```shell
    adduser tidb
    ```
   
2. Start systemd user mode for `tidb` user on every deployment target machine (important step)

   1. Use `tidb` user to set XDG_RUNTIME_DIR  environment variable
   
   {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p ~/.bashrc.d
    echo "export XDG_RUNTIME_DIR=/run/user/$(id -u)" > ~/.bashrc.d/systemd
    source ~/.bashrc.d/systemd
    ```
   
   2. Use `root` user to start user service
   
   {{< copyable "shell-regular" >}}
      
   ```shell
      $ systemctl start user@1000.service #1000 is the id of tidb user. You can get the user id by executing id
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
   
      Execute `systemctl --user` in the terminal and no more errors are thrown, indicating that it has started normally.

3. Use ssh-keygen in the central control computer to generate a key and copy the public key to other deployment machines.

## Prepare topology file

1. Use following command to generate topology file.

   {{< copyable "shell-regular" >}}

   ```shell
   tiup cluster template > topology.yaml
   ```
   
2. Edit the topology file.

   Compared with the previous mode, TiUP using no-sudo mode needs to add the line `systemd_mode: "user"` in the global block of topology.yaml. The `systemd_mode` parameter is used to indicate whether to use systemd user mode. If this parameter is not set, its default value is `system`, indicating that sudo permissions are required. In addition, no-sudo mode cannot use `/data` as `deploy_dir` and `data_dir` because there will be permission issues, and you need to choose a path that ordinary users can access. The example below uses relative paths and the final paths used are `/home/tidb/data/tidb-deploy` and `/home/tidb/data/tidb-data`.
   The rest is consistent with the old version.

   {{< copyable "shell-regular" >}}

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

Executing `tiup cluster check topology.yaml --user tidb` will display some failed check items, examples:

{{< copyable "shell-regular" >}}

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

Since in no-sudo mode, the `tidb` user does not have sudo permissions, executing `tiup cluster check topology.yaml --apply --user tidb` will not be able to automatically repair failed check items due to insufficient permissions. Therefore, some operations need to be performed manually on the deployment machines using the `root` user.

1. Install the numactl tool

   {{< copyable "shell-regular" >}}

    ```shell
      sudo yum -y install numactl
    ```
   
2. Close swap

   {{< copyable "shell-regular" >}}

    ```shell
       swapoff -a || exit 0
    ```
   
3. Disable transparent huge pages

    {{< copyable "shell-regular" >}}

    ```shell
       echo never > /sys/kernel/mm/transparent_hugepage/enabled
    ```

4. Start irqbalance service

   {{< copyable "shell-regular" >}}

    ```shell
       systemctl start irqbalance
   ```
   
5. Turn off the firewall and turn off firewall auto-start
   
    {{< copyable "shell-regular" >}}

    ```shell
       systemctl stop firewalld.service
       systemctl disable firewalld.service
   ```
   
6. Modify sysctl parameters
   
    {{< copyable "shell-regular" >}}

    ```shell
       echo "fs.file-max = 1000000">> /etc/sysctl.conf
       echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
       echo "net.ipv4.tcp_tw_recycle = 0">> /etc/sysctl.conf
       echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
       echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
       echo "vm.swappiness = 0">> /etc/sysctl.conf
       sysctl -p
   ```
   
7. Configure the user's limits.conf file

   {{< copyable "shell-regular" >}}

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

## Deploy cluster

In order to use the `tidb` user prepared in the above steps and avoid re-creating a new user, you need to add `--user tidb` when executing the deploy command, that is:

{{< copyable "shell-regular" >}}

```shell
  tiup cluster deploy mycluster v8.1.0 topology.yaml --user tidb
```

Start cluster

{{< copyable "shell-regular" >}}

```shell
tiup cluster start mycluster
```

Scale-out cluster

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-out mycluster scale.yaml --user tidb
```

Scale-in cluster

{{< copyable "shell-regular" >}}

```shell
tiup cluster scale-in mycluster -N 192.168.124.27:20160
```

Upgrade cluster

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade mycluster v8.2.0
```

## FAQ
1. When starting user@.service, an error occurs: Failed to fully start up daemon: Permission denied

   This may be because the `pam_systemd.so` is missing from your `/etc/pam.d/system-auth.ued` file. You can use the following command to check whether the `/etc/pam.d/system-auth.ued` file already contains the configuration of the `pam_systemd.so` module. If not, append the line `session optional pam_systemd.so` to the end of the file.

   {{< copyable "shell-regular" >}}

   ```shell
   grep 'pam_systemd.so' /etc/pam.d/system-auth.ued || echo 'session     optional      pam_systemd.so' >> /etc/pam.d/system-auth.ued
   ```
