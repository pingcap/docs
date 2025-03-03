---
title: Deploy and Maintain an Online TiDB Cluster Using TiUP No-sudo Mode
summary: Learn how to deploy and maintain an online TiDB cluster using the TiUP no-sudo mode.
---

# Deploy and Maintain an Online TiDB Cluster Using TiUP No-sudo Mode

This document describes how to use the TiUP no-sudo mode to deploy a cluster.

> **Note:**
>
> For CentOS, only CentOS 8 or later versions are supported.

## Prepare the user and configure the SSH mutual trust

1. Take the `tidb` user as an example. Log in to all the target machines and create a user named `tidb` using the `root` user with the following command. In no-sudo mode, configuring passwordless sudo for the `tidb` user is unnecessary, that is, you do not need to add the `tidb` user to the `sudoers` file.
   
    ```shell
    adduser tidb
    ```
   
2. Start the `systemd user` mode for the `tidb` user on each target machine. This step is required and do not skip it.

    1. Use the `tidb` user to set the `XDG_RUNTIME_DIR` environment variable.
   
        ```shell
        sudo -iu tidb  # This is to switch to the tidb user
        mkdir -p ~/.bashrc.d
        echo "export XDG_RUNTIME_DIR=/run/user/$(id -u)" > ~/.bashrc.d/systemd
        source ~/.bashrc.d/systemd
        ```
   
    2. Use the `root` user to start the user service.
   
        ```shell
        $ uid=$(id -u tidb) # Get the id of the tidb user
        $ systemctl start user@${uid}.service
        $ systemctl status user@${uid}.service
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
       
    3. Execute `systemctl --user`. If no errors occur, it indicates that the `systemd user` mode has started successfully.

3. Use the `root` user to execute the following command to enable lingering for the systemd user `tidb`.

    ```shell
    loginctl enable-linger tidb
    ```

    You can read the systemd documentation for reference, [Automatic start-up of systemd user instances](https://wiki.archlinux.org/title/Systemd/User#Automatic_start-up_of_systemd_user_instances).

4. Generate a key using `ssh-keygen` on the control machine, and copy the public key to the other deployment machines to establish SSH trust. If you have set a password for the tidb user user you can use `ssh-copy-id` to copy the public key to the target machine. If you use any other method make user to check the permissions of the `/home/tidb/.ssh/authorized_keys` file.

    ```shell
    ssh-keygen
    ssh-copy-id tidb@host
    ```

    Replace `host` with the hostname of the target machine and run the `ssh-copy-id` command for every machine in the cluster.

    ```
    chown -R tidb:tidb /home/tidb/.ssh/authorized_keys
    chmod 600 /home/tidb/.ssh/authorized_keys
    ```

## Prepare the topology file

1. Execute the following command to generate the topology file.

    ```shell
    tiup cluster template > topology.yaml
    ```
   
2. Edit the topology file.

    Compared with the regular mode, when using TiUP in no-sudo mode, you need to add a line `systemd_mode: "user"` in the `global` module of the `topology.yaml` file. The `systemd_mode` parameter is used to set whether to use the `systemd user` mode. If this parameter is not set, the default value is `system`, meaning sudo permissions are required.

    Additionally, in no-sudo mode, because the non-root `tidb` user does not have permission to use the `/data` directory as `deploy_dir` or `data_dir`, you must select a path accessible to non-root users. The following example uses relative paths and the final paths used are `/home/tidb/data/tidb-deploy` and `/home/tidb/data/tidb-data`. The rest of the topology file remains the same as in the regular mode.

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


> **Note:**
>
> If you use a minimal install, please make sure the `tar` package is installed. Otherwise the `tiup cluster check` command will fail.

Executing `tiup cluster check topology.yaml --user tidb` can generate some failed check items. The following is an example.

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

In no-sudo mode, the `tidb` user does not have sudo permissions. As a result, running `tiup cluster check topology.yaml --apply --user tidb` cannot automatically fix the failed check items. You need to manually perform the following steps using the `root` user on the target machines.


See [Check before deployment](/check-before-deployment.md) for how to correct these.

## Deploy and manage the cluster

To use the `tidb` user created in preceding steps and avoid creating a new one, add `--user tidb` when running the following `deploy` command:

```shell
tiup cluster deploy mycluster v8.1.0 topology.yaml --user tidb
```

> **Note:**
>
> You have to replace v8.1.0 in the command above with the TiDB version that you want to deploy.

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

### The `Trying to run as user instance, but $XDG_RUNTIME_DIR is not set.` error occurs when starting user@.service

This issue might be caused by the absence of `pam_systemd.so` in your `/etc/pam.d/system-auth.ued` file.

To resolve this issue, use the following command to check whether the `/etc/pam.d/system-auth.ued` file contains the `pam_systemd.so` module. If not, append `session optional pam_systemd.so` to the end of the file.

```shell
grep 'pam_systemd.so' /etc/pam.d/system-auth.ued || echo 'session     optional      pam_systemd.so' >> /etc/pam.d/system-auth.ued
```
