---
title: TiDB Environment and System Configuration Check
summary: Learn the environment check operations before deploying TiDB.
---

# TiDB環境とシステムConfiguration / コンフィグレーションのチェック {#tidb-environment-and-system-configuration-check}

このドキュメントでは、TiDBをデプロイする前の環境チェック操作について説明します。次の手順は優先順位順に並べられています。

## TiKVをデプロイするターゲットマシンにオプションを使用してデータディスクext4ファイルシステムをマウントします {#mount-the-data-disk-ext4-filesystem-with-options-on-the-target-machines-that-deploy-tikv}

実稼働環境では、EXT4ファイルシステムのNVMeSSDを使用してTiKVデータを保存することをお勧めします。この構成はベストプラクティスであり、その信頼性、セキュリティ、および安定性は、多数のオンラインシナリオで証明されています。

`root`ユーザーアカウントを使用してターゲットマシンにログインします。

データディスクをext4ファイルシステムにフォーマットし、ファイルシステムに`nodelalloc`および`noatime`マウントオプションを追加します。 `nodelalloc`オプションを追加する必要があります。そうしないと、TiUPデプロイメントは事前チェックに合格できません。 `noatime`オプションはオプションです。

> **ノート：**
>
> データディスクがext4にフォーマットされ、マウントオプションが追加されている場合は、 `umount /dev/nvme0n1p1`コマンドを実行してアンインストールし、以下の5番目の手順に直接スキップして`/etc/fstab`ファイルを編集し、ファイルシステムにオプションを再度追加できます。

例として`/dev/nvme0n1`のデータディスクを取り上げます。

1.  データディスクをビューします。

    {{< copyable "" >}}

    ```bash
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2.  パーティションを作成します。

    {{< copyable "" >}}

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    > **ノート：**
    >
    > `lsblk`コマンドを使用して、パーティションのデバイス番号を表示します。NVMeディスクの場合、生成されるデバイス番号は通常`nvme0n1p1`です。通常のディスク（たとえば、 `/dev/sdb` ）の場合、生成されるデバイス番号は通常`sdb1`です。

3.  データディスクをext4ファイルシステムにフォーマットします。

    {{< copyable "" >}}

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4.  データディスクのパーティションUUIDをビューします。

    この例では、nvme0n1p1のUUIDは`c51eb23b-195c-4061-92a9-3fad812cc12f`です。

    {{< copyable "" >}}

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

5.  `/etc/fstab`のファイルを編集し、 `nodelalloc`のマウントオプションを追加します。

    {{< copyable "" >}}

    ```bash
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6.  データディスクをマウントします。

    {{< copyable "" >}}

    ```bash
    mkdir /data1 && \
    mount -a
    ```

7.  次のコマンドで確認してください。

    {{< copyable "" >}}

    ```bash
    mount -t ext4
    ```

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

    ファイルシステムがext4であり、マウントオプションに`nodelalloc`が含まれている場合、ターゲットマシンにオプションを使用してデータディスクext4ファイルシステムを正常にマウントできています。

## システムスワップを確認して無効にする {#check-and-disable-system-swap}

TiDBは、動作のために十分なメモリスペースを必要とします。メモリが不足している場合、スワップをバッファとして使用すると、パフォーマンスが低下する可能性があります。したがって、次のコマンドを実行して、システムスワップを永続的に無効にすることをお勧めします。

{{< copyable "" >}}

```bash
echo "vm.swappiness = 0">> /etc/sysctl.conf
swapoff -a && swapon -a
sysctl -p
```

> **ノート：**
>
> -   `swapoff -a`を実行してから`swapon -a`を実行すると、データをメモリにダンプしてスワップをクリーンアップすることにより、スワップを更新します。スワップピネスの変更を削除して`swapoff -a`だけ実行すると、システムを再起動した後にスワップが再度有効になります。
>
> -   `sysctl -p`は、システムを再起動せずに構成を有効にすることです。

## ターゲットマシンのファイアウォールサービスを確認して停止します {#check-and-stop-the-firewall-service-of-target-machines}

TiDBクラスターでは、読み取りおよび書き込み要求やデータハートビートなどの情報を確実に送信するために、ノード間のアクセスポートを開く必要があります。一般的なオンラインシナリオでは、データベースとアプリケーションサービス間、およびデータベースノード間のデータ相互作用はすべて安全なネットワーク内で行われます。したがって、特別なセキュリティ要件がない場合は、ターゲットマシンのファイアウォールを停止することをお勧めします。それ以外の場合は、 [ポートの使用法](/hardware-and-software-requirements.md#network-requirements)を参照して、必要なポート情報をファイアウォールサービスの許可リストに追加します。

このセクションの残りの部分では、ターゲットマシンのファイアウォールサービスを停止する方法について説明します。

1.  ファイアウォールの状態を確認してください。例として、CentOS Linuxリリース7.7.1908（コア）を取り上げます。

    {{< copyable "" >}}

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2.  ファイアウォールサービスを停止します。

    {{< copyable "" >}}

    ```bash
    sudo systemctl stop firewalld.service
    ```

3.  ファイアウォールサービスの自動開始を無効にします。

    {{< copyable "" >}}

    ```bash
    sudo systemctl disable firewalld.service
    ```

4.  ファイアウォールの状態を確認してください。

    {{< copyable "" >}}

    ```bash
    sudo systemctl status firewalld.service
    ```

## NTPサービスを確認してインストールします {#check-and-install-the-ntp-service}

TiDBは、ACIDモデルのトランザクションの線形整合性を保証するために、ノード間のクロック同期を必要とする分散データベースシステムです。

現在、クロック同期の一般的な解決策は、ネットワークタイムプロトコル（NTP）サービスを使用することです。インターネットで`pool.ntp.org`タイミングサービスを使用することも、オフライン環境で独自のNTPサービスを構築することもできます。

NTPサービスがインストールされているかどうか、およびNTPサーバーと正常に同期しているかどうかを確認するには、次の手順を実行します。

1.  次のコマンドを実行します。 `running`が返される場合は、NTPサービスが実行されています。

    {{< copyable "" >}}

    ```bash
    sudo systemctl status ntpd.service
    ```

    ```
    ntpd.service - Network Time Service
    Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
    Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago
    ```

    -   `Unit ntpd.service could not be found.`が返された場合は、次のコマンドを試して、システムがNTPとのクロック同期を実行するために`ntpd`ではなく`chronyd`を使用するように構成されているかどうかを確認します。

        {{< copyable "" >}}

        ```bash
        sudo systemctl status chronyd.service
        ```

        ```
        chronyd.service - NTP client/server
        Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
        Active: active (running) since Mon 2021-04-05 09:55:29 EDT; 3 days ago
        ```

        結果が`chronyd`も`ntpd`も構成されていないことを示している場合は、どちらもシステムにインストールされていないことを意味します。最初に`chronyd`または`ntpd`をインストールし、自動的に開始できることを確認する必要があります。デフォルトでは、 `ntpd`が使用されます。

        システムが`chronyd`を使用するように構成されている場合は、ステップ3に進みます。

2.  `ntpstat`コマンドを実行して、NTPサービスがNTPサーバーと同期しているかどうかを確認します。

    > **ノート：**
    >
    > Ubuntuシステムの場合、 `ntpstat`パッケージをインストールする必要があります。

    {{< copyable "" >}}

    ```bash
    ntpstat
    ```

    -   `synchronised to NTP server` （NTPサーバーとの同期）を返す場合、同期プロセスは正常です。

        ```
        synchronised to NTP server (85.199.214.101) at stratum 2
        time correct to within 91 ms
        polling server every 1024 s
        ```

    -   次の状況は、NTPサービスが正常に同期していないことを示しています。

        ```
        unsynchronised
        ```

    -   次の状況は、NTPサービスが正常に実行されていないことを示しています。

        ```
        Unable to talk to NTP daemon. Is it running?
        ```

3.  `chronyc tracking`コマンドを実行して、ChronyサービスがNTPサーバーと同期するかどうかを確認します。

    > **ノート：**
    >
    > これは、NTPdの代わりにChronyを使用するシステムにのみ適用されます。

    {{< copyable "" >}}

    ```bash
    chronyc tracking
    ```

    -   コマンドが`Leap status     : Normal`を返す場合、同期プロセスは正常です。

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

    -   コマンドが次の結果を返す場合、同期でエラーが発生します。

        ```
        Leap status    : Not synchronised
        ```

    -   コマンドが次の結果を返す場合、 `chronyd`サービスは正常に実行されていません。

        ```
        506 Cannot talk to daemon
        ```

NTPサービスの同期をできるだけ早く開始するには、次のコマンドを実行します。 `pool.ntp.org`をNTPサーバーに置き換えます。

{{< copyable "" >}}

```bash
sudo systemctl stop ntpd.service && \
sudo ntpdate pool.ntp.org && \
sudo systemctl start ntpd.service
```

CentOS 7システムにNTPサービスを手動でインストールするには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
sudo yum install ntp ntpdate && \
sudo systemctl start ntpd.service && \
sudo systemctl enable ntpd.service
```

## オペレーティングシステムの最適なパラメータを確認して構成します {#check-and-configure-the-optimal-parameters-of-the-operating-system}

実稼働環境のTiDBの場合、次の方法でオペレーティングシステム構成を最適化することをお勧めします。

1.  THP（Transparent Huge Pages）を無効にします。データベースのメモリアクセスパターンは、連続的ではなくまばらになる傾向があります。高レベルのメモリの断片化が深刻な場合、THPページが割り当てられるときに待ち時間が長くなります。
2.  ストレージメディアのI/Oスケジューラを`noop`に設定します。高速SSDストレージメディアの場合、カーネルのI/Oスケジューリング操作によってパフォーマンスが低下する可能性があります。スケジューラを`noop`に設定すると、カーネルが他の操作なしでI / O要求をハードウェアに直接送信するため、パフォーマンスが向上します。また、noopスケジューラの方が適しています。
3.  CPU周波数を制御するcpufrequモジュールの`performance`モードを選択します。 CPU周波数が動的調整なしでサポートされている最高の動作周波数に固定されている場合、パフォーマンスは最大になります。

次の手順を実行して、現在のオペレーティングシステムの構成を確認し、最適なパラメーターを構成します。

1.  次のコマンドを実行して、THPが有効か無効かを確認します。

    {{< copyable "" >}}

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    [always] madvise never
    ```

    > **ノート：**
    >
    > `[always] madvise never`が出力される場合、THPが有効になります。無効にする必要があります。

2.  次のコマンドを実行して、データディレクトリが配置されているディスクのI/Oスケジューラを確認します。 sdbディスクとsdcディスクの両方にデータディレクトリを作成するとします。

    {{< copyable "" >}}

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    noop [deadline] cfq
    noop [deadline] cfq
    ```

    > **ノート：**
    >
    > `noop [deadline] cfq`が出力された場合、ディスクのI/Oスケジューラは`deadline`モードになります。 `noop`に変更する必要があります。

3.  次のコマンドを実行して、ディスクの`ID_SERIAL`を確認します。

    {{< copyable "" >}}

    ```bash
    udevadm info --name=/dev/sdb | grep ID_SERIAL
    ```

    ```
    E: ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81
    E: ID_SERIAL_SHORT=6d0946606d79f90025f3e09a0c1f9e81
    ```

    > **ノート：**
    >
    > 複数のディスクにデータディレクトリが割り当てられている場合は、上記のコマンドを数回実行して、各ディスクの`ID_SERIAL`を記録する必要があります。

4.  次のコマンドを実行して、cpufreqモジュールの電源ポリシーを確認します。

    {{< copyable "" >}}

    ```bash
    cpupower frequency-info --policy
    ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "powersave" may decide which speed to use within this range.
    ```

    > **ノート：**
    >
    > `The governor "powersave"`が出力される場合、cpufreqモジュールの電源ポリシーは`powersave`です。 `performance`に変更する必要があります。仮想マシンまたはクラウドホストを使用する場合、出力は通常`Unable to determine current policy`であり、何も変更する必要はありません。

5.  オペレーティングシステムの最適なパラメータを構成します。

    -   方法1：調整済みを使用する（推奨）

        1.  `tuned-adm list`コマンドを実行して、現在のオペレーティングシステムの調整済みプロファイルを確認します。

            {{< copyable "" >}}

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

            出力`Current active profile: balanced`は、現在のオペレーティングシステムの調整されたプロファイルが`balanced`であることを意味します。現在のプロファイルに基づいて、オペレーティングシステムの構成を最適化することをお勧めします。

        2.  新しい調整済みプロファイルを作成します。

            {{< copyable "" >}}

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

            出力`include=balanced`は、オペレーティングシステムの最適化構成を現在の`balanced`プロファイルに追加することを意味します。

        3.  新しい調整済みプロファイルを適用します。

            {{< copyable "" >}}

            ```bash
            tuned-adm profile balanced-tidb-optimal
            ```

    -   方法2：スクリプトを使用して構成します。すでに方法1を使用している場合は、この方法をスキップしてください。

        1.  `grubby`コマンドを実行して、デフォルトのカーネルバージョンを確認します。

            > **ノート：**
            >
            > `grubby`を実行する前に、最初に`grubby`のパッケージをインストールします。

            {{< copyable "" >}}

            ```bash
            grubby --default-kernel
            ```

            ```bash
            /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

        2.  `grubby --update-kernel`を実行して、カーネル構成を変更します。

            {{< copyable "" >}}

            ```bash
            grubby --args="transparent_hugepage=never" --update-kernel /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **ノート：**
            >
            > `--update-kernel`の後に、実際のデフォルトのカーネルバージョンが続きます。

        3.  `grubby --info`を実行して、変更されたデフォルトのカーネル構成を確認します。

            {{< copyable "" >}}

            ```bash
            grubby --info /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **ノート：**
            >
            > `--info`の後に、実際のデフォルトのカーネルバージョンが続きます。

            ```
            index=0
            kernel=/boot/vmlinuz-3.10.0-957.el7.x86_64
            args="ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet LANG=en_US.UTF-8 transparent_hugepage=never"
            root=/dev/mapper/centos-root
            initrd=/boot/initramfs-3.10.0-957.el7.x86_64.img
            title=CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
            ```

        4.  現在のカーネル構成を変更して、THPをすぐに無効にします。

            {{< copyable "" >}}

            ```bash
            echo never > /sys/kernel/mm/transparent_hugepage/enabled
            echo never > /sys/kernel/mm/transparent_hugepage/defrag
            ```

        5.  udevスクリプトでI/Oスケジューラを構成します。

            {{< copyable "" >}}

            ```bash
            vi /etc/udev/rules.d/60-tidb-schedulers.rules
            ```

            ```
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1fc035", ATTR{queue/scheduler}="noop"
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1f9e81", ATTR{queue/scheduler}="noop"

            ```

        6.  udevスクリプトを適用します。

            {{< copyable "" >}}

            ```bash
            udevadm control --reload-rules
            udevadm trigger --type=devices --action=change
            ```

        7.  CPU電源ポリシーを構成するサービスを作成します。

            {{< copyable "" >}}

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

        8.  CPU電源ポリシー構成サービスを適用します。

            {{< copyable "" >}}

            ```bash
            systemctl daemon-reload
            systemctl enable cpupower.service
            systemctl start cpupower.service
            ```

6.  次のコマンドを実行して、THPステータスを確認します。

    {{< copyable "" >}}

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

    ```
    always madvise [never]
    ```

7.  次のコマンドを実行して、データディレクトリが配置されているディスクのI/Oスケジューラを確認します。

    {{< copyable "" >}}

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

    ```
    [noop] deadline cfq
    [noop] deadline cfq
    ```

8.  次のコマンドを実行して、cpufreqモジュールの電源ポリシーを確認します。

    {{< copyable "" >}}

    ```bash
    cpupower frequency-info --policy
    ```

    ```
    analyzing CPU 0:
    current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                  The governor "performance" may decide which speed to use within this range.
    ```

9.  次のコマンドを実行して、 `sysctl`つのパラメーターを変更します。

    {{< copyable "" >}}

    ```bash
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_tw_recycle = 0">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    sysctl -p
    ```

10. 次のコマンドを実行して、ユーザーの`limits.conf`ファイルを構成します。

    {{< copyable "" >}}

    ```bash
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile          1000000
    tidb           hard    nofile          1000000
    tidb           soft    stack          32768
    tidb           hard    stack          32768
    EOF
    ```

## パスワードなしでSSH相互信頼とsudoを手動で構成する {#manually-configure-the-ssh-mutual-trust-and-sudo-without-password}

このセクションでは、パスワードなしでSSH相互信頼とsudoを手動で構成する方法について説明します。展開にはTiUPを使用することをお勧めします。これにより、SSH相互信頼が自動的に構成され、パスワードなしでログインできます。 TiUPを使用してTiDBクラスターをデプロイする場合は、このセクションを無視してください。

1.  `root`ユーザーアカウントを使用してそれぞれターゲットマシンにログインし、 `tidb`ユーザーを作成して、ログインパスワードを設定します。

    {{< copyable "" >}}

    ```bash
    useradd tidb && \
    passwd tidb
    ```

2.  パスワードなしでsudoを設定するには、次のコマンドを実行し、ファイルの最後に`tidb ALL=(ALL) NOPASSWD: ALL`を追加します。

    {{< copyable "" >}}

    ```bash
    visudo
    ```

    ```
    tidb ALL=(ALL) NOPASSWD: ALL
    ```

3.  `tidb`人のユーザーを使用して制御マシンにログインし、次のコマンドを実行します。 `10.0.1.1`をターゲットマシンのIPに置き換え、プロンプトに従ってターゲットマシンの`tidb`ユーザーパスワードを入力します。コマンドの実行後、SSH相互信頼はすでに作成されています。これは他のマシンにも当てはまります。新しく作成された`tidb`人のユーザーには`.ssh`ディレクトリがありません。このようなディレクトリを作成するには、RSAキーを生成するコマンドを実行します。制御マシンにTiDBコンポーネントを展開するには、制御マシンと制御マシン自体の相互信頼を構成します。

    {{< copyable "" >}}

    ```bash
    ssh-keygen -t rsa
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4.  `tidb`ユーザーアカウントを使用してコントロールマシンにログインし、 `ssh`を使用してターゲットマシンのIPにログインします。パスワードを入力する必要がなく、正常にログインできる場合は、SSH相互信頼が正常に構成されています。

    {{< copyable "" >}}

    ```bash
    ssh 10.0.1.1
    ```

    ```
    [tidb@10.0.1.1 ~]$
    ```

5.  `tidb`ユーザーを使用してターゲットマシンにログインした後、次のコマンドを実行します。パスワードを入力する必要がなく、 `root`ユーザーに切り替えることができる場合は、 `tidb`ユーザーのパスワードなしのsudoが正常に構成されています。

    {{< copyable "" >}}

    ```bash
    sudo -su root
    ```

    ```
    [root@10.0.1.1 tidb]#
    ```

## <code>numactl</code>ツールをインストールします {#install-the-code-numactl-code-tool}

このセクションでは、NUMAツールをインストールする方法について説明します。オンライン環境では、ハードウェア構成は通常必要以上に高いため、ハードウェアリソースをより適切に計画するために、TiDBまたはTiKVの複数のインスタンスを単一のマシンに展開できます。このようなシナリオでは、NUMAツールを使用して、パフォーマンスの低下を引き起こす可能性のあるCPUリソースの競合を防ぐことができます。

> **ノート：**
>
> -   NUMAを使用したコアのバインドは、CPUリソースを分離する方法であり、高度に構成された物理マシンに複数のインスタンスをデプロイするのに適しています。
> -   `tiup cluster deploy`を使用して展開を完了した後、 `exec`コマンドを使用してクラスタレベルの管理操作を実行できます。

NUMAツールをインストールするには、次の2つの方法のいずれかを実行します。

**方法1** ：ターゲットノードにログインしてNUMAをインストールします。例として、CentOS Linuxリリース7.7.1908（コア）を取り上げます。

```bash
sudo yum -y install numactl
```

**方法2** ： `tiup cluster exec`コマンドを実行して、NUMAを既存のクラスタにバッチでインストールします。

1.  [TiUPを使用してTiDBクラスターをデプロイする](/production-deployment-using-tiup.md)に従って、クラスタ`tidb-test`をデプロイします。 TiDBクラスタをインストールしている場合は、この手順をスキップできます。

    ```bash
    tiup cluster deploy tidb-test v6.1.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2.  `sudo`特権を使用して`tiup cluster exec`コマンドを実行し、 `tidb-test`クラスタのすべてのターゲットマシンにNUMAをインストールします。

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```

    `tiup cluster exec`コマンドのヘルプ情報を取得するには、 `tiup cluster exec --help`コマンドを実行します。
