---
title: TiDB Environment and System Configuration Check
summary: Learn the environment check operations before deploying TiDB.
---

# TiDB 環境およびシステムコンフィグレーションのチェック {#tidb-environment-and-system-configuration-check}

本書では、TiDB 導入前の環境確認操作について説明します。次の手順は優先順位に従って並べられています。

## TiKV を展開するターゲット マシンにオプションを使用してデータ ディスク ext4 ファイル システムをマウントします。 {#mount-the-data-disk-ext4-filesystem-with-options-on-the-target-machines-that-deploy-tikv}

本番環境の場合、TiKV データの保存には EXT4 ファイルシステムの NVMe SSD を使用することをお勧めします。この構成はベスト プラクティスであり、その信頼性、セキュリティ、安定性が多数のオンライン シナリオで実証されています。

`root`ユーザー アカウントを使用してターゲット マシンにログインします。

データ ディスクを ext4 ファイル システムにフォーマットし、ファイル システムに`nodelalloc`および`noatime`マウント オプションを追加します。 `nodelalloc`オプションを追加する必要があります。追加しないと、 TiUPデプロイメントは事前チェックに合格できません。 `noatime`オプションはオプションです。

> **注記：**
>
> データ ディスクが ext4 にフォーマットされ、マウント オプションが追加されている場合は、 `umount /dev/nvme0n1p1`コマンドを実行してデータ ディスクをアンインストールし、以下の 5 番目の手順に直接進んで`/etc/fstab`ファイルを編集し、ファイル システムにオプションを再度追加します。

`/dev/nvme0n1`データ ディスクを例に挙げます。

1.  データディスクをビュー。

    ```bash
    fdisk -l
    ```

        Disk /dev/nvme0n1: 1000 GB

2.  パーティションを作成します。

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    > **注記：**
    >
    > `lsblk`コマンドを使用して、パーティションのデバイス番号を表示します。NVMe ディスクの場合、生成されるデバイス番号は通常`nvme0n1p1`です。通常のディスク (たとえば、 `/dev/sdb` ) の場合、生成されるデバイス番号は通常`sdb1`です。

3.  データディスクを ext4 ファイルシステムにフォーマットします。

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4.  データ ディスクのパーティション UUIDをビュー。

    この例では、 nvme0n1p1 の UUID は`c51eb23b-195c-4061-92a9-3fad812cc12f`です。

    ```bash
    lsblk -f
    ```

        NAME    FSTYPE LABEL UUID                                 MOUNTPOINT
        sda
        ├─sda1  ext4         237b634b-a565-477b-8371-6dff0c41f5ab /boot
        ├─sda2  swap         f414c5c0-f823-4bb1-8fdf-e531173a72ed
        └─sda3  ext4         547909c1-398d-4696-94c6-03e43e317b60 /
        sr0
        nvme0n1
        └─nvme0n1p1 ext4         c51eb23b-195c-4061-92a9-3fad812cc12f

5.  `/etc/fstab`ファイルを編集し、 `nodelalloc`マウント オプションを追加します。

    ```bash
    vi /etc/fstab
    ```

        UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2

6.  データディスクをマウントします。

    ```bash
    mkdir /data1 && \
    mount -a
    ```

7.  以下のコマンドで確認してください。

    ```bash
    mount -t ext4
    ```

        /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)

    ファイルシステムが ext4 で、マウント オプションに`nodelalloc`が含まれている場合、オプションを使用してデータ ディスク ext4 ファイル システムがターゲット マシンに正常にマウントされています。

## システムスワップをチェックして無効にする {#check-and-disable-system-swap}

TiDB の動作には十分なメモリ容量が必要です。メモリが不足している場合、スワップをバッファとして使用するとパフォーマンスが低下する可能性があります。したがって、次のコマンドを実行してシステム スワップを永久に無効にすることをお勧めします。

```bash
echo "vm.swappiness = 0">> /etc/sysctl.conf
swapoff -a && swapon -a
sysctl -p
```

> **注記：**
>
> -   `swapoff -a`実行してから`swapon -a`を実行すると、データをメモリにダンプし、スワップをクリーンアップしてスワップをリフレッシュします。スワップの変更を削除して`swapoff -a`のみを実行すると、システムの再起動後にスワップが再び有効になります。
>
> -   `sysctl -p`は、システムを再起動せずに構成を有効にすることを意味します。

## TiDB インスタンスの一時スペースを設定する (推奨) {#set-temporary-spaces-for-tidb-instances-recommended}

TiDB の一部の操作では、一時ファイルをサーバーに書き込む必要があるため、TiDB を実行するオペレーティング システム ユーザーがターゲット ディレクトリの読み取りおよび書き込みに十分な権限を持っていることを確認する必要があります。 TiDB インスタンスを`root`権限で起動しない場合は、ディレクトリの権限を確認し、正しく設定する必要があります。

-   TiDB 作業領域

    ハッシュ テーブルの構築や並べ替えなど、大量のメモリを消費する操作では、メモリ消費を削減して安定性を向上させるために、一時データがディスクに書き込まれることがあります。書き込み用のディスクの場所は構成項目[`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path)によって定義されます。デフォルト構成では、TiDB を実行するユーザーがオペレーティング システムの一時フォルダー (通常は`/tmp` ) に対する読み取りおよび書き込み権限を持っていることを確認してください。

-   `Fast Online DDL`作業領域

    変数[`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が`ON` (v6.5.0 以降のバージョンのデフォルト値) に設定されている場合、 `Fast Online DDL`が有効になり、一部の DDL 操作ではファイルシステム内の一時ファイルの読み取りおよび書き込みが必要になります。位置は構成項目[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)によって定義されます。 TiDB を実行するユーザーがオペレーティング システムのそのディレクトリに対する読み取りおよび書き込み権限を持っていることを確認する必要があります。デフォルトのディレクトリ`/tmp/tidb`例に挙げます。

    > **注記：**
    >
    > アプリケーションに大きなオブジェクトに対する DDL 操作が存在する場合は、独立した大きなファイル システムを[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)用に構成することを強くお勧めします。

    ```shell
    sudo mkdir /tmp/tidb
    ```

    `/tmp/tidb`ディレクトリがすでに存在する場合は、書き込み権限が付与されていることを確認してください。

    ```shell
    sudo chmod -R 777 /tmp/tidb
    ```

    > **注記：**
    >
    > ディレクトリが存在しない場合、TiDB は起動時に自動的に作成します。ディレクトリの作成が失敗した場合、または TiDB にそのディレクトリの読み取りおよび書き込み権限がない場合、実行時に予期しない問題が発生する可能性[`Fast Online DDL`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)あります。

## ターゲットマシンのファイアウォールサービスを確認して停止します。 {#check-and-stop-the-firewall-service-of-target-machines}

TiDB クラスターでは、読み取りおよび書き込みリクエストやデータ ハートビートなどの情報の送信を確実にするために、ノード間のアクセス ポートが開いている必要があります。一般的なオンライン シナリオでは、データベースとアプリケーション サービスの間、およびデータベース ノード間のデータ対話はすべて安全なネットワーク内で行われます。したがって、特別なセキュリティ要件がない場合は、ターゲット マシンのファイアウォールを停止することをお勧めします。それ以外の場合は、 [ポートの使用状況](/hardware-and-software-requirements.md#network-requirements)を参照して、ファイアウォール サービスの許可リストに必要なポート情報を追加します。

このセクションの残りの部分では、ターゲット マシンのファイアウォール サービスを停止する方法について説明します。

1.  ファイアウォールのステータスを確認します。 CentOS Linux リリース 7.7.1908 (コア) を例に挙げます。

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2.  ファイアウォール サービスを停止します。

    ```bash
    sudo systemctl stop firewalld.service
    ```

3.  ファイアウォールサービスの自動起動を無効にします。

    ```bash
    sudo systemctl disable firewalld.service
    ```

4.  ファイアウォールのステータスを確認します。

    ```bash
    sudo systemctl status firewalld.service
    ```

## NTPサービスを確認してインストールする {#check-and-install-the-ntp-service}

TiDB は、 ACIDモデルにおけるトランザクションの線形一貫性を保証するためにノード間のクロック同期を必要とする分散データベース システムです。

現在、クロック同期の一般的な解決策は、ネットワーク タイム プロトコル (NTP) サービスを使用することです。インターネット上で`pool.ntp.org`タイミング サービスを使用することも、オフライン環境で独自の NTP サービスを構築することもできます。

NTP サービスがインストールされているかどうか、および NTPサーバーと正常に同期しているかどうかを確認するには、次の手順を実行します。

1.  次のコマンドを実行します。 `running`が返された場合、NTP サービスは実行中です。

    ```bash
    sudo systemctl status ntpd.service
    ```

        ntpd.service - Network Time Service
        Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
        Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago

    -   `Unit ntpd.service could not be found.`が返された場合は、次のコマンドを試して、NTP とのクロック同期を実行するために`ntpd`ではなく`chronyd`を使用するようにシステムが構成されているかどうかを確認します。

        ```bash
        sudo systemctl status chronyd.service
        ```

            chronyd.service - NTP client/server
            Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
            Active: active (running) since Mon 2021-04-05 09:55:29 EDT; 3 days ago

        結果に`chronyd`も`ntpd`も設定されていないことが示された場合は、どちらもシステムにインストールされていないことを意味します。まず`chronyd`または`ntpd`インストールし、自動的に起動できることを確認する必要があります。デフォルトでは`ntpd`が使用されます。

        システムが`chronyd`を使用するように構成されている場合は、ステップ 3 に進みます。

2.  `ntpstat`コマンドを実行して、NTP サービスが NTPサーバーと同期しているかどうかを確認します。

    > **注記：**
    >
    > Ubuntu システムの場合は、 `ntpstat`パッケージをインストールする必要があります。

    ```bash
    ntpstat
    ```

    -   `synchronised to NTP server`が返された場合 (NTPサーバーと同期中)、同期プロセスは正常です。

            synchronised to NTP server (85.199.214.101) at stratum 2
            time correct to within 91 ms
            polling server every 1024 s

    -   次の状況は、NTP サービスが正常に同期していないことを示しています。

            unsynchronised

    -   次の状況は、NTP サービスが正常に実行されていないことを示しています。

            Unable to talk to NTP daemon. Is it running?

3.  `chronyc tracking`コマンドを実行して、Chrony サービスが NTPサーバーと同期しているかどうかを確認します。

    > **注記：**
    >
    > これは、NTPd の代わりに Chrony を使用するシステムにのみ適用されます。

    ```bash
    chronyc tracking
    ```

    -   コマンドが`Leap status     : Normal`を返した場合、同期プロセスは正常です。

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

    -   コマンドが次の結果を返した場合、同期でエラーが発生しています。

            Leap status    : Not synchronised

    -   コマンドが次の結果を返した場合、サービス`chronyd`は正常に実行されていません。

            506 Cannot talk to daemon

NTP サービスの同期をできるだけ早く開始するには、次のコマンドを実行します。 `pool.ntp.org` NTPサーバーに置き換えます。

```bash
sudo systemctl stop ntpd.service && \
sudo ntpdate pool.ntp.org && \
sudo systemctl start ntpd.service
```

CentOS 7 システムに NTP サービスを手動でインストールするには、次のコマンドを実行します。

```bash
sudo yum install ntp ntpdate && \
sudo systemctl start ntpd.service && \
sudo systemctl enable ntpd.service
```

## オペレーティングシステムの最適なパラメータを確認して設定します。 {#check-and-configure-the-optimal-parameters-of-the-operating-system}

本番環境の TiDB の場合、次の方法でオペレーティング システム構成を最適化することをお勧めします。

1.  THP (Transparent Huge Pages) を無効にします。データベースのメモリアクセス パターンは、連続的ではなく、まばらになる傾向があります。高レベルのメモリ断片化が深刻な場合、THP ページが割り当てられるときにレイテンシーが長くなります。
2.  storageメディアの I/O スケジューラを`noop`に設定します。高速 SSDstorageメディアの場合、カーネルの I/O スケジューリング操作によりパフォーマンスが低下する可能性があります。スケジューラを`noop`に設定すると、カーネルは他の操作を行わずに I/O リクエストをハードウェアに直接送信するため、パフォーマンスが向上します。また、noop スケジューラの方がより適切に適用できます。
3.  CPU 周波数を制御する cpufrequ モジュールには`performance`モードを選択します。動的調整を行わずに CPU 周波数をサポートされる最高の動作周波数に固定すると、パフォーマンスが最大化されます。

現在のオペレーティング システムの構成を確認し、最適なパラメータを構成するには、次の手順を実行します。

1.  次のコマンドを実行して、THP が有効か無効かを確認します。

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

        [always] madvise never

    > **注記：**
    >
    > `[always] madvise never`が出力された場合、THP が有効になります。無効にする必要があります。

2.  次のコマンドを実行して、データ ディレクトリが配置されているディスクの I/O スケジューラを確認します。 sdb ディスクと sdc ディスクの両方にデータ ディレクトリを作成すると仮定します。

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

        noop [deadline] cfq
        noop [deadline] cfq

    > **注記：**
    >
    > `noop [deadline] cfq`が出力された場合、そのディスクの I/O Scheduler は`deadline`モードです。これを`noop`に変更する必要があります。

3.  次のコマンドを実行して、ディスクの`ID_SERIAL`を確認します。

    ```bash
    udevadm info --name=/dev/sdb | grep ID_SERIAL
    ```

        E: ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81
        E: ID_SERIAL_SHORT=6d0946606d79f90025f3e09a0c1f9e81

    > **注記：**
    >
    > 複数のディスクにデータ ディレクトリが割り当てられている場合は、各ディスクの`ID_SERIAL`を記録するために上記のコマンドを数回実行する必要があります。

4.  次のコマンドを実行して、cpufreq モジュールの電源ポリシーを確認します。

    ```bash
    cpupower frequency-info --policy
    ```

        analyzing CPU 0:
        current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                      The governor "powersave" may decide which speed to use within this range.

    > **注記：**
    >
    > `The governor "powersave"`が出力された場合、cpufreq モジュールの電源ポリシーは`powersave`です。これを`performance`に変更する必要があります。仮想マシンまたはクラウド ホストを使用する場合、出力は通常`Unable to determine current policy`であり、何も変更する必要はありません。

5.  オペレーティング システムの最適なパラメータを構成します。

    -   方法 1:tuned を使用する (推奨)

        1.  `tuned-adm list`コマンドを実行して、現在のオペレーティング システムの調整されたプロファイルを確認します。

            ```bash
            tuned-adm list
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

            出力`Current active profile: balanced` 、現在のオペレーティング システムの調整されたプロファイルが`balanced`であることを意味します。現在のプロファイルに基づいてオペレーティング システムの構成を最適化することをお勧めします。

        2.  新しい調整されたプロファイルを作成します。

            ```bash
            mkdir /etc/tuned/balanced-tidb-optimal/
            vi /etc/tuned/balanced-tidb-optimal/tuned.conf
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

            出力`include=balanced` 、現在のプロファイル`balanced`にオペレーティング システムの最適化構成を追加することを意味します。

        3.  新しい調整されたプロファイルを適用します。

            ```bash
            tuned-adm profile balanced-tidb-optimal
            ```

    -   方法 2: スクリプトを使用して構成します。すでに方法 1 を使用している場合は、この方法をスキップしてください。

        1.  `grubby`コマンドを実行して、デフォルトのカーネル バージョンを確認します。

            > **注記：**
            >
            > `grubby`を実行する前に、まず`grubby`パッケージをインストールします。

            ```bash
            grubby --default-kernel
            ```

            ```bash
            /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

        2.  `grubby --update-kernel`を実行してカーネル構成を変更します。

            ```bash
            grubby --args="transparent_hugepage=never" --update-kernel /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **注記：**
            >
            > `--update-kernel`の後には、実際のデフォルトのカーネル バージョンが続きます。

        3.  `grubby --info`を実行して、変更されたデフォルトのカーネル構成を確認します。

            ```bash
            grubby --info /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **注記：**
            >
            > `--info`の後には、実際のデフォルトのカーネル バージョンが続きます。

                index=0
                kernel=/boot/vmlinuz-3.10.0-957.el7.x86_64
                args="ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet LANG=en_US.UTF-8 transparent_hugepage=never"
                root=/dev/mapper/centos-root
                initrd=/boot/initramfs-3.10.0-957.el7.x86_64.img
                title=CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)

        4.  現在のカーネル構成を変更して、THP を直ちに無効にします。

            ```bash
            echo never > /sys/kernel/mm/transparent_hugepage/enabled
            echo never > /sys/kernel/mm/transparent_hugepage/defrag
            ```

        5.  udev スクリプトで I/O スケジューラを設定します。

            ```bash
            vi /etc/udev/rules.d/60-tidb-schedulers.rules
            ```

            ```
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1fc035", ATTR{queue/scheduler}="noop"
            ACTION=="add|change", SUBSYSTEM=="block", ENV{ID_SERIAL}=="36d0946606d79f90025f3e09a0c1f9e81", ATTR{queue/scheduler}="noop"

            ```

        6.  udev スクリプトを適用します。

            ```bash
            udevadm control --reload-rules
            udevadm trigger --type=devices --action=change
            ```

        7.  CPU 電力ポリシーを構成するサービスを作成します。

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

        8.  CPU 電力ポリシー構成サービスを適用します。

            ```bash
            systemctl daemon-reload
            systemctl enable cpupower.service
            systemctl start cpupower.service
            ```

6.  次のコマンドを実行して、THP ステータスを確認します。

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

        always madvise [never]

7.  次のコマンドを実行して、データ ディレクトリが配置されているディスクの I/O スケジューラを確認します。

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

        [noop] deadline cfq
        [noop] deadline cfq

8.  次のコマンドを実行して、cpufreq モジュールの電源ポリシーを確認します。

    ```bash
    cpupower frequency-info --policy
    ```

        analyzing CPU 0:
        current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                      The governor "performance" may decide which speed to use within this range.

9.  次のコマンドを実行して`sysctl`パラメータを変更します。

    ```bash
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_tw_recycle = 0">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    sysctl -p
    ```

10. 次のコマンドを実行して、ユーザー`limits.conf`のファイルを構成します。

    ```bash
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile          1000000
    tidb           hard    nofile          1000000
    tidb           soft    stack          32768
    tidb           hard    stack          32768
    EOF
    ```

## パスワードを使用せずに SSH 相互信頼と sudo を手動で構成する {#manually-configure-the-ssh-mutual-trust-and-sudo-without-password}

このセクションでは、パスワードを使用せずに SSH 相互信頼と sudo を手動で構成する方法について説明します。導入にはTiUPを使用することをお勧めします。これにより、SSH 相互信頼が自動的に構成され、パスワードなしでログインできます。 TiUPを使用して TiDB クラスターをデプロイする場合は、このセクションを無視してください。

1.  `root`ユーザーアカウントを使用してそれぞれターゲットマシンにログインし、 `tidb`ユーザーを作成し、ログインパスワードを設定します。

    ```bash
    useradd tidb && \
    passwd tidb
    ```

2.  パスワードなしで sudo を構成するには、次のコマンドを実行し、ファイルの末尾に`tidb ALL=(ALL) NOPASSWD: ALL`を追加します。

    ```bash
    visudo
    ```

        tidb ALL=(ALL) NOPASSWD: ALL

3.  `tidb`ユーザーを使用して制御マシンにログインし、次のコマンドを実行します。 `10.0.1.1`ターゲット マシンの IP に置き換え、プロンプトに従ってターゲット マシンの`tidb`ユーザー パスワードを入力します。コマンドの実行後、SSH 相互信頼がすでに作成されています。これは他のマシンにも当てはまります。新しく作成された`tidb`ユーザーには`.ssh`ディレクトリがありません。このようなディレクトリを作成するには、RSA キーを生成するコマンドを実行します。 TiDB コンポーネントを制御マシンに展開するには、制御マシンと制御マシン自体の相互信頼を構成します。

    ```bash
    ssh-keygen -t rsa
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4.  `tidb`ユーザー アカウントを使用して制御マシンにログインし、 `ssh`使用してターゲット マシンの IP にログインします。パスワードを入力する必要がなく、正常にログインできた場合、SSH 相互信頼は正常に構成されています。

    ```bash
    ssh 10.0.1.1
    ```

        [tidb@10.0.1.1 ~]$

5.  `tidb`ユーザーを使用してターゲット マシンにログインした後、次のコマンドを実行します。パスワードを入力する必要がなく、 `root`ユーザーに切り替えることができれば、 `tidb`ユーザーのパスワードなしの sudo が正常に設定されています。

    ```bash
    sudo -su root
    ```

        [root@10.0.1.1 tidb]#

## <code>numactl</code>ツールをインストールする {#install-the-code-numactl-code-tool}

このセクションでは、NUMA ツールをインストールする方法について説明します。オンライン環境では通常、ハードウェア構成が必要以上に高くなるため、ハードウェア リソースをより適切に計画するために、TiDB または TiKV の複数のインスタンスを 1 台のマシンにデプロイできます。このようなシナリオでは、NUMA ツールを使用して、パフォーマンスの低下を引き起こす可能性のある CPU リソースの競合を防ぐことができます。

> **注記：**
>
> -   NUMA を使用したコアのバインドは、CPU リソースを分離する方法であり、高度に構成された物理マシンに複数のインスタンスをデプロイするのに適しています。
> -   `tiup cluster deploy`を使用してデプロイメントを完了した後、 `exec`コマンドを使用してクラスター レベルの管理操作を実行できます。

NUMA ツールをインストールするには、次の 2 つの方法のいずれかを実行します。

**方法 1** : ターゲット ノードにログインして NUMA をインストールします。 CentOS Linux リリース 7.7.1908 (コア) を例に挙げます。

```bash
sudo yum -y install numactl
```

**方法 2** : `tiup cluster exec`コマンドを実行して、既存のクラスターに NUMA をバッチでインストールします。

1.  [TiUPを使用した TiDBクラスタのデプロイ](/production-deployment-using-tiup.md)に従ってクラスターをデプロイします。 `tidb-test` . TiDB クラスターをインストールしている場合は、この手順をスキップできます。

    ```bash
    tiup cluster deploy tidb-test v6.1.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2.  `sudo`権限を使用して`tiup cluster exec`コマンドを実行し、 `tidb-test`クラスター内のすべてのターゲット マシンに NUMA をインストールします。

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```

    `tiup cluster exec`コマンドのヘルプ情報を取得するには、 `tiup cluster exec --help`コマンドを実行します。
