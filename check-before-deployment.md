---
title: TiDB Environment and System Configuration Check
summary: Learn the environment check operations before deploying TiDB.
---

# TiDB Environment and System Configuration Check

This document describes the environment check operations before deploying TiDB. The following steps are ordered by priorities.

## Mount the data disk ext4 filesystem with options on the target machines that deploy TiKV

For production deployments, it is recommended to use NVMe SSD of EXT4 filesystem to store TiKV data. This configuration is the best practice, whose reliability, security, and stability have been proven in a large number of online scenarios.

Log in to the target machines using the `root` user account.

Format your data disks to the ext4 filesystem and add the `nodelalloc` and `noatime` mount options to the filesystem. It is required to add the `nodelalloc` option, or else the TiUP deployment cannot pass the precheck. The `noatime` option is optional.

> **Note:**
>
> If your data disks have been formatted to ext4 and have added the mount options, you can uninstall it by running the `umount /dev/nvme0n1p1` command, skip directly to the fifth step below to edit the `/etc/fstab` file, and add the options again to the filesystem.

Take the `/dev/nvme0n1` data disk as an example:

1. View the data disk.

    ```bash
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2. Create the partition.

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    For large NVMe devices, you can create multiple partitions:

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 2000GB
    parted -s -a optimal /dev/nvme0n1 -- mkpart primary ext4 2000GB -1
    ```

    > **Note:**
    >
    > Use the `lsblk` command to view the device number of the partition: for a NVMe disk, the generated device number is usually `nvme0n1p1`; for a regular disk (for example, `/dev/sdb`), the generated device number is usually `sdb1`.

3. Format the data disk to the ext4 filesystem.

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4. View the partition UUID of the data disk.

    In this example, the UUID of nvme0n1p1 is `c51eb23b-195c-4061-92a9-3fad812cc12f`.

    ```bash
    lsblk -f
    ```

    ```
    NAME    FSTYPE LABEL UUID                                 MOUNTPOINT
    sda
    ├─sda1  ext4         237b634b-a565-477b-8371-6dff0c41f5ab /boot
    ├─sda2  swap         f414c5c0-f823-4bb1-8fdf-e531173a72ed
    └─sda3  ext4         547909c1-398d-4696-94c6-03e43e317b60 /
    sr0
    nvme0n1
    └─nvme0n1p1 ext4         c51eb23b-195c-4061-92a9-3fad812cc12f
    ```

5. Edit the `/etc/fstab` file and add the `nodelalloc` mount options.

    ```bash
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6. Mount the data disk.

    ```bash
    mkdir /data1 && \
    systemctl daemon-reload && \
    mount -a
    ```

7. Check using the following command.

    ```bash
    mount -t ext4
    ```

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

    If the filesystem is ext4 and `nodelalloc` is included in the mount options, you have successfully mount the data disk ext4 filesystem with options on the target machines.

## Check and disable system swap

TiDB needs a sufficient amount of memory for operation. If the memory that TiDB uses gets swapped out and later gets swapped back in, this can cause latency spikes. If you want to maintain stable performance, it is recommended that you permanently disable the system swap, but it might trigger OOM issues when there is insufficient memory. If you want to avoid such OOM issues, you can just decrease the swap priority, instead of permanently disabling it.

- Enabling and using swap might introduce performance jitter issues. It is recommended that you permanently disable the operating system tier swap for low-latency and stability-critical database services. To permanently disable swap, you can use the following method:

    - During the initialization phase of the operating system, do not partition the swap partition disk separately.
    - If you have already partitioned a separate swap partition disk during the initialization phase of the operating system and enabled swap, run the following command to disable it:

        ```bash
        echo "vm.swappiness = 0">> /etc/sysctl.conf
        sysctl -p
        swapoff -a && swapon -a
        ```

- If the host memory is insufficient, disabling the system swap might be more likely to trigger OOM issues. You can run the following command to decrease the swap priority instead of disabling it permanently:

    ```bash
    echo "vm.swappiness = 0">> /etc/sysctl.conf
    sysctl -p
    ```

## Set temporary spaces for TiDB instances (Recommended)

Some operations in TiDB require writing temporary files to the server, so it is necessary to ensure that the operating system user that runs TiDB has sufficient permissions to read and write to the target directory. If you do not start the TiDB instance with the `root` privilege, you need to check the directory permissions and set them correctly.

- TiDB work area

    Operations that consume a significant amount of memory, such as hash table construction and sorting, might write temporary data to disk to reduce memory consumption and improve stability. The disk location for writing is defined by the configuration item [`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path). With the default configuration, make sure that the user that runs TiDB has read and write permissions to the temporary folder (usually `/tmp`) of the operating system.

- `Fast Online DDL` work area

    When the variable [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) is set to `ON` (the default value in v6.5.0 and later versions), `Fast Online DDL` is enabled, and some DDL operations need to read and write temporary files in filesystems. The location is defined by the configuration item [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630). You need to ensure that the user that runs TiDB has read and write permissions for that directory of the operating system. The default directory `/tmp/tidb` uses tmpfs (temporary file system). It is recommended to explicitly specify a disk directory. The following uses `/data/tidb-deploy/tempdir` as an example:

    > **Note:**
    >
    > If DDL operations on large objects exist in your application, it is highly recommended to configure an independent large file system for [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630).

    ```shell
    sudo mkdir -p /data/tidb-deploy/tempdir
    ```

    If the `/data/tidb-deploy/tempdir` directory already exists, make sure the write permission is granted.

    ```shell
    sudo chmod -R 777 /data/tidb-deploy/tempdir
    ```

    > **Note:**
    >
    > If the directory does not exist, TiDB will automatically create it upon startup. If the directory creation fails or TiDB does not have the read and write permissions for that directory, [`Fast Online DDL`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) will be disabled during runtime.

## Check the firewall service of target machines

In TiDB clusters, the access ports between nodes must be open to ensure the transmission of information such as read and write requests and data heartbeats. In common online scenarios, the data interaction between the database and the application service and between the database nodes are all made within a secure network. Therefore, if there are no special security requirements, it is recommended to stop the firewall of the target machine. Otherwise, refer to [the port usage](/hardware-and-software-requirements.md#network-requirements) and add the needed port information to the allowlist of the firewall service.

### Stop and disable firewalld

This section describes how to stop and disable the firewall service of a target machine.

1. Check the firewall status. The following example uses CentOS Linux release 7.7.1908 (Core):

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2. Stop the firewall service:

    ```bash
    sudo systemctl stop firewalld.service
    ```

3. Disable automatic startup of the firewall service:

    ```bash
    sudo systemctl disable firewalld.service
    ```

4. Check the firewall status:

    ```bash
    sudo systemctl status firewalld.service
    ```

### Change the firewall zone

Instead of disabling the firewall completely, you can use a less restrictive zone. The default `public` zone allows only specific services and ports, while the `trusted` zone allows all traffic by default.

To set the default zone to `trusted`:

```bash
firewall-cmd --set-default-zone trusted
```

To verify the default zone:

```bash
firewall-cmd --get-default-zone
# trusted
```

To list the policy for a zone:

```bash
firewall-cmd --zone=trusted --list-all
# trusted
#   target: ACCEPT
#   icmp-block-inversion: no
#   interfaces:
#   sources:
#   services:
#   ports:
#   protocols:
#   forward: yes
#   masquerade: no
#   forward-ports:
#   source-ports:
#   icmp-blocks:
#   rich rules:
```

### Configure the firewall

To configure the firewall for TiDB cluster components, use the following commands. These examples are for reference only. Adjust the zone names, ports, and services based on your specific environment.

Configure the firewall for the TiDB component:

```bash
firewall-cmd --permanent --new-service tidb
firewall-cmd --permanent --service tidb --set-description="TiDB Server"
firewall-cmd --permanent --service tidb --set-short="TiDB"
firewall-cmd --permanent --service tidb --add-port=4000/tcp
firewall-cmd --permanent --service tidb --add-port=10080/tcp
firewall-cmd --permanent --zone=public --add-service=tidb
```

Configure the firewall for the TiKV component:

```bash
firewall-cmd --permanent --new-service tikv
firewall-cmd --permanent --service tikv --set-description="TiKV Server"
firewall-cmd --permanent --service tikv --set-short="TiKV"
firewall-cmd --permanent --service tikv --add-port=20160/tcp
firewall-cmd --permanent --service tikv --add-port=20180/tcp
firewall-cmd --permanent --zone=public --add-service=tikv
```

Configure the firewall for the PD component:

```bash
firewall-cmd --permanent --new-service pd
firewall-cmd --permanent --service pd --set-description="PD Server"
firewall-cmd --permanent --service pd --set-short="PD"
firewall-cmd --permanent --service pd --add-port=2379/tcp
firewall-cmd --permanent --service pd --add-port=2380/tcp
firewall-cmd --permanent --zone=public --add-service=pd
```

Configure the firewall for Prometheus:

```bash
firewall-cmd --permanent --zone=public --add-service=prometheus
firewall-cmd --permanent --service=prometheus --add-port=12020/tcp
```

Configure the firewall for Grafana:

```bash
firewall-cmd --permanent --zone=public --add-service=grafana
```

## Check and install the NTP service

TiDB is a distributed database system that requires clock synchronization between nodes to guarantee linear consistency of transactions in the ACID model.

At present, the common solution to clock synchronization is to use the Network Time Protocol (NTP) services. You can use the `pool.ntp.org` timing service on the Internet, or build your own NTP service in an offline environment.

To check whether the NTP service is installed and whether it synchronizes with the NTP server normally, take the following steps:

1. Run the following command. If it returns `running`, then the NTP service is running.

    ```bash
    sudo systemctl status ntpd.service
    ```

    ```
    ntpd.service - Network Time Service
    Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
    Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
    ```

    - If it returns `Unit ntpd.service could not be found.`, then try the following command to see whether your system is configured to use `chronyd` instead of `ntpd` to perform clock synchronization with NTP:

        ```bash
        sudo systemctl status chronyd.service
        ```

        ```
        chronyd.service - NTP client/server
        Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
        Active: active (running) since Mon 2021-04-05 09:55:29 EDT; 3 days ago
        ```

        If the result shows that neither `chronyd` nor `ntpd` is configured, it means that neither of them is installed in your system. You should first install `chronyd` or `ntpd` and ensure that it can be automatically started. By default, `ntpd` is used.

        If your system is configured to use `chronyd`, proceed to step 3.

2. Run the `ntpstat` command to check whether the NTP service synchronizes with the NTP server.

    > **Note:**
    >
    > For the Ubuntu system, you need to install the `ntpstat` package.

    ```bash
    ntpstat
    ```

    - If it returns `synchronised to NTP server` (synchronizing with the NTP server), then the synchronization process is normal.

        ```
        synchronised to NTP server (85.199.214.101) at stratum 2
        time correct to within 91 ms
        polling server every 1024 s
        ```

    - The following situation indicates the NTP service is not synchronizing normally:

        ```
        unsynchronised
        ```

    - The following situation indicates the NTP service is not running normally:

        ```
        Unable to talk to NTP daemon. Is it running?
        ```

3. Run the `chronyc tracking` command to check whether the Chrony service synchronizes with the NTP server.

    > **Note:**
    >
    > This only applies to systems that use Chrony instead of NTPd.

    ```bash
    chronyc tracking
    ```

    - If the command returns `Leap status     : Normal`, the synchronization process is normal.

        ```
        Reference ID    : 5EC69F0A (ntp1.time.nl)
        Stratum         : 2
        Ref time (UTC)  : Thu May 20 15:19:08 2021
        System time     : 0.000022151 seconds slow of NTP time
        Last offset     : -0.000041040 seconds
        RMS offset      : 0.000053422 seconds
        Frequency       : 2.286 ppm slow
        Residual freq   : -0.000 ppm
        Skew            : 0.012 ppm
        Root delay      : 0.012706812 seconds
        Root dispersion : 0.000430042 seconds
        Update interval : 1029.8 seconds
        Leap status     : Normal
        ```

    - If the command returns the following result, an error occurs in the synchronization:

        ```
        Leap status    : Not synchronised
        ```

    - If the command returns the following result, the `chronyd` service is not running normally:

        ```
        506 Cannot talk to daemon
        ```

    - If the offset appears to be too high, you can run the `chronyc makestep` command to immediately correct the time offset. Otherwise, `chronyd` will gradually correct the time offset.

To make the NTP service start synchronizing as soon as possible, run the following command. Replace `pool.ntp.org` with your NTP server.

```bash
sudo systemctl stop ntpd.service && \
sudo ntpdate pool.ntp.org && \
sudo systemctl start ntpd.service
```

To install the NTP service manually on the CentOS 7 system, run the following command:

```bash
sudo yum install ntp ntpdate && \
sudo systemctl start ntpd.service && \
sudo systemctl enable ntpd.service
```

## Check and configure the optimal parameters of the operating system

For TiDB in the production environment, it is recommended to optimize the operating system configuration in the following ways:

- Disable [transparent huge pages (THP)](/tune-operating-system.md#memorytransparent-huge-page-thp). Database memory access is usually sparse. When higher-order memory becomes heavily fragmented, THP allocation can cause high memory allocation latency. Therefore, it is recommended to disable THP to avoid performance fluctuations.

- Set the [I/O scheduler](/tune-operating-system.md#io-scheduler) of the storage media.

    - For the high-speed SSD storage, the kernel's default I/O scheduling operations might cause performance loss. It is recommended to set the I/O Scheduler to first-in-first-out (FIFO), such as `noop` or `none`. This configuration allows the kernel to pass I/O requests directly to hardware without scheduling, thus improving performance.
    - For NVMe storage, the default I/O Scheduler is `none`, so no adjustment is needed.

- Choose the `performance` mode for [the cpufreq module](/tune-operating-system.md#cpufrequency-scaling) that controls the CPU frequency dynamically. The performance is maximized when the CPU frequency is fixed at its highest supported operating frequency without dynamic adjustment.

The steps to check and configure these parameters are as follows:

1. Execute the following command to see whether THP is enabled or disabled:

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    [always] madvise never
    ```

    > **Note:**
    >
    > If `[always] madvise never` is output, THP is enabled. You need to disable it.

2. Execute the following command to see the I/O Scheduler of the disk where the data directory is located.

    If your data directory uses an SD or VD device, run the following command to check the I/O Scheduler:

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    noop [deadline] cfq
    noop [deadline] cfq
    ```

    > **Note:**
    >
    > If `noop [deadline] cfq` is output, the I/O Scheduler for the disk is in the `deadline` mode. You need to change it to `noop`.

    If your data directory uses an NVMe device, run the following command to check the I/O Scheduler:

    ```bash
    cat /sys/block/nvme[01]*/queue/scheduler
    ```

    ```
    [none] mq-deadline kyber bfq
    [none] mq-deadline kyber bfq
    ```

    > **Note:**
    >
    > `[none] mq-deadline kyber bfq` indicates that the NVMe device uses the `none` I/O Scheduler, and no changes are needed.

3. Execute the following command to see the `ID_SERIAL` of the disk:

    ```bash
    udevadm info --name=/dev/sdb | grep ID_SERIAL
    ```

    ```
    E: ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81
    E: ID_SERIAL_SHORT=6d0946606d79f90025f3e09a0c1f9e81
    ```

    > **Note:**
    >
    > - If multiple disks are allocated with data directories, you need to execute the above command for each disk to record the `ID_SERIAL` of each disk.
    > - If your device uses the `noop` or `none` Scheduler, you do not need to record the `ID_SERIAL` or configure udev rules or the tuned profile.

4. Execute the following command to see the power policy of the cpufreq module:

    ```bash
    cpupower frequency-info --policy
    ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "powersave" may decide which speed to use within this range.
    ```

    > **Note:**
    >
    > If `The governor "powersave"` is output, the power policy of the cpufreq module is `powersave`. You need to modify it to `performance`. If you use a virtual machine or a cloud host, the output is usually `Unable to determine current policy`, and you do not need to change anything.

5. Configure optimal parameters of the operating system:

    + Method one: Use tuned (Recommended)

        1. Execute the `tuned-adm list` command to see the tuned profile of the current operating system:

            ```bash
            tuned-adm list
            ```

            ```
            Available profiles:
            - balanced                    - General non-specialized tuned profile
            - desktop                     - Optimize for the desktop use-case
            - hpc-compute                 - Optimize for HPC compute workloads
            - latency-performance         - Optimize for deterministic performance at the cost of increased power consumption
            - network-latency             - Optimize for deterministic performance at the cost of increased power consumption, focused on low latency network performance
            - network-throughput          - Optimize for streaming network throughput, generally only necessary on older CPUs or 40G+ networks
            - powersave                   - Optimize for low power consumption
            - throughput-performance      - Broadly applicable tuning that provides excellent performance across a variety of common server workloads
            - virtual-guest               - Optimize for running inside a virtual guest
            - virtual-host                - Optimize for running KVM guests
            Current active profile: balanced
            ```

            The output `Current active profile: balanced` means that the tuned profile of the current operating system is `balanced`. It is recommended to optimize the configuration of the operating system based on the current profile.

        2. Create a new tuned profile:

            ```bash
            mkdir /etc/tuned/balanced-tidb-optimal/
            vi /etc/tuned/balanced-tidb-optimal/tuned.conf
            ```

            ```
            [main]
            include=balanced

            [cpu]
            governor=performance

            [vm]
            transparent_hugepages=never

            [disk]
            devices_udev_regex=(ID_SERIAL=36d0946606d79f90025f3e09a0c1fc035)|(ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81)
            elevator=noop
            ```

            The output `include=balanced` means to add the optimization configuration of the operating system to the current `balanced` profile.

        3. Apply the new tuned profile:

            > **Note:**
            >
            > If your device uses the `noop` or `none` I/O Scheduler, skip this step. No Scheduler configuration is needed in the tuned profile.

            ```bash
            tuned-adm profile balanced-tidb-optimal
            ```

    + Method two: Configure using scripts. Skip this method if you already use method one.

        1. Execute the `grubby` command to see the default kernel version:

            > **Note:**
            >
            > Install the `grubby` package first before you execute `grubby`.

            ```bash
            grubby --default-kernel
            ```

            ```bash
            /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

        2. Execute `grubby --update-kernel` to modify the kernel configuration:

            ```bash
            grubby --args="transparent_hugepage=never" --update-kernel `grubby --default-kernel`
            ```

            > **Note:**
            >
            > You can also specify the actual version number after `--update-kernel`, for example, `--update-kernel /boot/vmlinuz-3.10.0-957.el7.x86_64` or `ALL`.

        3. Execute `grubby --info` to see the modified default kernel configuration:

            ```bash
            grubby --info /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **Note:**
            >
            > `--info` is followed by the actual default kernel version.

            ```
            index=0
            kernel=/boot/vmlinuz-3.10.0-957.el7.x86_64
            args="ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet LANG=en_US.UTF-8 transparent_hugepage=never"
            root=/dev/mapper/centos-root
            initrd=/boot/initramfs-3.10.0-957.el7.x86_64.img
            title=CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
            ```

        4. Modify the current kernel configuration to immediately disable THP:

            ```bash
            echo never > /sys/kernel/mm/transparent_hugepage/enabled
            echo never > /sys/kernel/mm/transparent_hugepage/defrag
            ```

        5. Configure the I/O Scheduler in the udev script:

            ```bash
            vi /etc/udev/rules.d/60-tidb-schedulers.rules
            ```

            ```
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1fc035", ATTR{queue/scheduler}="noop"
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1f9e81", ATTR{queue/scheduler}="noop"

            ```

        6. Apply the udev script:

            > **Note:**
            >
            > If your device uses the `noop` or `none` I/O Scheduler, skip this step. No udev rules configuration is needed.

            ```bash
            udevadm control --reload-rules
            udevadm trigger --type=devices --action=change
            ```

        7. Create a service to configure the CPU power policy:

            ```bash
            cat  >> /etc/systemd/system/cpupower.service << EOF
            [Unit]
            Description=CPU performance
            [Service]
            Type=oneshot
            ExecStart=/usr/bin/cpupower frequency-set --governor performance
            [Install]
            WantedBy=multi-user.target
            EOF
            ```

        8. Apply the CPU power policy configuration service:

            ```bash
            systemctl daemon-reload
            systemctl enable cpupower.service
            systemctl start cpupower.service
            ```

6. Execute the following command to verify the THP status:

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    always madvise [never]
    ```

7. Execute the following command to verify the I/O Scheduler of the disk where the data directory is located:

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    [noop] deadline cfq
    [noop] deadline cfq
    ```

8. Execute the following command to see the power policy of the cpufreq module:

    ```bash
    cpupower frequency-info --policy
      ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "performance" may decide which speed to use within this range.
    ```

9. Execute the following commands to modify the `sysctl` parameters:

    ```bash
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    echo "vm.min_free_kbytes = 1048576">> /etc/sysctl.conf
    sysctl -p
    ```

    > **Warning:**
    >
    > It is not recommended to increase the value of `vm.min_free_kbytes` on systems with less than 16 GiB of memory, because it might cause instability and boot failures.

    > **Note:**
    >
    > - `vm.min_free_kbytes` is a Linux kernel parameter that controls the minimum amount of free memory reserved by the system, measured in KiB.
    > - The setting of `vm.min_free_kbytes` affects the memory reclaim mechanism. Setting it too large reduces the available memory, while setting it too small might cause memory request speeds to exceed background reclaim speeds, leading to memory reclamation and consequent delays in memory allocation.
    > - It is recommended to set `vm.min_free_kbytes` to `1048576` KiB (1 GiB) at least. If [NUMA is installed](/check-before-deployment.md#install-the-numactl-tool), it is recommended to set it to `number of NUMA nodes * 1048576` KiB.
    > - For systems running Linux kernel 4.11 or earlier, it is recommended to set `net.ipv4.tcp_tw_recycle = 0`.

10. Execute the following command to configure the user's `limits.conf` file:

    ```bash
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile         1000000
    tidb           hard    nofile         1000000
    tidb           soft    stack          32768
    tidb           hard    stack          32768
    tidb           soft    core           unlimited
    tidb           hard    core           unlimited
    EOF
    ```

## Manually configure the SSH mutual trust and sudo without password

This section describes how to manually configure SSH mutual trust from the control machine to the target nodes. If you use the TiUP deployment tool, SSH mutual trust and password-free login are configured automatically, and you can skip this section.

When configuring SSH mutual trust, it is recommended to create and use the `tidb` user on all target nodes. In general, TiDB does not require that you use the same user across all nodes. However, pay attention to user consistency in the following scenarios:

- Using Backup & Restore (BR): it is strongly recommended to perform all BR and TiDB-related operations with the same user.
- Using network storage such as NFS: ensure that the user has the same UID and GID on all nodes. NFS determines file access permissions based on underlying UID and GID. If the UID or GID differs across nodes, or if the user running BR is different from the user running TiDB (especially without `sudo` privileges), permission denied errors might occur during backup or restore operations.

1. Log in to the target machine respectively using the `root` user account, create the `tidb` user and set the login password.

    ```bash
    useradd -m -d /home/tidb tidb
    passwd tidb
    ```

2. To configure sudo without password, run the following command, and add `tidb ALL=(ALL) NOPASSWD: ALL` to the end of the file:

    ```bash
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

3. Use the `tidb` user to log in to the control machine, and run the following command. Replace `10.0.1.1` with the IP of your target machine, and enter the `tidb` user password of the target machine as prompted. After the command is executed, SSH mutual trust is already created. This applies to other machines as well. Newly created `tidb` users do not have the `.ssh` directory. To create such a directory, execute the command that generates the RSA key. To deploy TiDB components on the control machine, configure mutual trust for the control machine and the control machine itself.

    ```bash
    ssh-keygen -t rsa
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4. Log in to the control machine using the `tidb` user account, and log in to the IP of the target machine using `ssh`. If you do not need to enter the password and can successfully log in, then the SSH mutual trust is successfully configured.

    ```bash
    ssh 10.0.1.1
    ```

    ```
    [tidb@10.0.1.1 ~]$
    ```

5. After you log in to the target machine using the `tidb` user, run the following command. If you do not need to enter the password and can switch to the `root` user, then sudo without password of the `tidb` user is successfully configured.

    ```bash
    sudo -su root
    ```

    ```
    [root@10.0.1.1 tidb]#
    ```

## Install the `numactl` tool

This section describes how to install the NUMA tool. In online environments, because the hardware configuration is usually higher than required, to better plan the hardware resources, multiple instances of TiDB or TiKV can be deployed on a single machine. In such scenarios, you can use NUMA tools to prevent the competition for CPU resources which might cause reduced performance.

> **Note:**
>
> - Binding cores using NUMA is a method to isolate CPU resources and is suitable for deploying multiple instances on highly configured physical machines.
> - After completing deployment using `tiup cluster deploy`, you can use the `exec` command to perform cluster level management operations.

To install the NUMA tool, take either of the following two methods:

**Method 1**: Log in to the target node to install NUMA. Take CentOS Linux release 7.7.1908 (Core) as an example.

```bash
sudo yum -y install numactl
```

**Method 2**: Install NUMA on an existing cluster in batches by running the `tiup cluster exec` command.

1. Follow [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md) to deploy a cluster `tidb-test`. If you have installed a TiDB cluster, you can skip this step.

    ```bash
    tiup cluster deploy tidb-test v6.1.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2. Run the `tiup cluster exec` command using the `sudo` privilege to install NUMA on all the target machines in the `tidb-test` cluster:

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```

    To get help information of the `tiup cluster exec` command, run the `tiup cluster exec --help` command.

## Disable SELinux

SELinux must be disabled or set to permissive mode. To check the current status, use the [getenforce(8)](https://linux.die.net/man/8/getenforce) utility.

If SELinux is not disabled, open the `/etc/selinux/config` file, locate the line starting with `SELINUX=`, and change it to `SELINUX=disabled`. After making this change, you need to reboot the system because switching from `enforcing` or `permissive` to `disabled` does not take effect without a reboot.

On some systems (such as Ubuntu), the `/etc/selinux/config` file might not exist, and the getenforce utility might not be installed. In that case, you can skip this step.
