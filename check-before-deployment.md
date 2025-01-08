---
title: TiDB Environment and System Configuration Check
summary: TiDB をデプロイする前に、環境チェック操作について学習します。
---

# TiDB 環境とシステムコンフィグレーションのチェック {#tidb-environment-and-system-configuration-check}

このドキュメントでは、TiDB をデプロイする前の環境チェック操作について説明します。次の手順は優先順位に従っています。

## TiKVを展開するターゲットマシンにオプション付きでデータディスクのext4ファイルシステムをマウントする {#mount-the-data-disk-ext4-filesystem-with-options-on-the-target-machines-that-deploy-tikv}

本番環境では、TiKV データの保存に EXT4 ファイルシステムの NVMe SSD を使用することをお勧めします。この構成はベスト プラクティスであり、その信頼性、セキュリティ、安定性は多数のオンライン シナリオで実証されています。

`root`ユーザー アカウントを使用してターゲット マシンにログインします。

データ ディスクを ext4 ファイルシステムにフォーマットし、ファイルシステムに`nodelalloc`および`noatime`マウント オプションを追加します`nodelalloc`オプションを追加する必要があります。そうしないと、 TiUPデプロイメントは事前チェックに合格できません`noatime`オプションはオプションです。

> **注記：**
>
> データ ディスクが ext4 にフォーマットされ、マウント オプションが追加されている場合は、 `umount /dev/nvme0n1p1`コマンドを実行してアンインストールし、以下の 5 番目の手順に直接進んで`/etc/fstab`ファイルを編集し、オプションをファイル システムに再度追加できます。

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

    大規模な NVMe デバイスの場合は、複数のパーティションを作成できます。

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 2000GB
    parted -s -a optimal /dev/nvme0n1 -- mkpart primary ext4 2000GB -1
    ```

    > **注記：**
    >
    > パーティションのデバイス番号を表示するには、 `lsblk`コマンドを使用します。NVMe ディスクの場合、生成されるデバイス番号は通常`nvme0n1p1`です。通常のディスク (たとえば、 `/dev/sdb` ) の場合、生成されるデバイス番号は通常`sdb1`です。

3.  データ ディスクを ext4 ファイルシステムにフォーマットします。

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4.  データ ディスクのパーティション UUID をビュー。

    この例では、nvme0n1p1 の UUID は`c51eb23b-195c-4061-92a9-3fad812cc12f`です。

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

6.  データ ディスクをマウントします。

    ```bash
    mkdir /data1 && \
    systemctl daemon-reload && \
    mount -a
    ```

7.  次のコマンドを使用して確認します。

    ```bash
    mount -t ext4
    ```

        /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)

    ファイルシステムが ext4 であり、マウント オプションに`nodelalloc`が含まれている場合、ターゲット マシンにオプションを使用してデータ ディスク ext4 ファイルシステムを正常にマウントしています。

## システムスワップをチェックして無効にする {#check-and-disable-system-swap}

TiDB は、動作に十分な量のメモリを必要とします。TiDB が使用するメモリがスワップアウトされ、後でスワップインされると、レイテンシーが急上昇する可能性があります。安定したパフォーマンスを維持するには、システム スワップを永続的に無効にすることをお勧めしますが、メモリが不足すると OOM の問題が発生する可能性があります。このような OOM の問題を回避するには、永続的に無効にするのではなく、スワップの優先度を下げるだけで済みます。

-   スワップを有効にして使用すると、パフォーマンスのジッターの問題が発生する可能性があります。低レイテンシで安定性が重要なデータベース サービスでは、オペレーティング システム層のスワップを永続的に無効にすることをお勧めします。スワップを永続的に無効にするには、次の方法を使用できます。

    -   オペレーティング システムの初期化フェーズでは、スワップ パーティション ディスクを個別にパーティション分割しないでください。
    -   オペレーティング システムの初期化フェーズ中に別のスワップ パーティション ディスクを既にパーティション分割し、スワップを有効にしている場合は、次のコマンドを実行して無効にします。

        ```bash
        echo "vm.swappiness = 0">> /etc/sysctl.conf
        sysctl -p
        swapoff -a && swapon -a
        ```

-   ホストメモリが不足している場合、システム スワップを無効にすると、OOM の問題が発生する可能性が高くなります。スワップを永続的に無効にする代わりに、次のコマンドを実行してスワップの優先度を下げることができます。

    ```bash
    echo "vm.swappiness = 0">> /etc/sysctl.conf
    sysctl -p
    ```

## TiDBインスタンスの一時スペースを設定する（推奨） {#set-temporary-spaces-for-tidb-instances-recommended}

TiDB の一部の操作では、一時ファイルをサーバーに書き込む必要があるため、TiDB を実行するオペレーティング システム ユーザーに、ターゲット ディレクトリの読み取りと書き込みを行うための十分な権限があることを確認する必要があります。1 `root`で TiDB インスタンスを起動しない場合は、ディレクトリの権限を確認し、正しく設定する必要があります。

-   TiDB 作業領域

    ハッシュ テーブルの構築やソートなど、大量のメモリを消費する操作では、メモリ消費量を削減し、安定性を向上させるために、一時データをディスクに書き込むことがあります。書き込み先のディスクの場所は、構成項目[`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path)で定義されます。デフォルト構成では、TiDB を実行するユーザーに、オペレーティング システムの一時フォルダー (通常は`/tmp` ) に対する読み取りおよび書き込み権限があることを確認してください。

-   `Fast Online DDL`作業エリア

    変数[`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が`ON` (v6.5.0 以降のバージョンではデフォルト値) に設定されている場合、 `Fast Online DDL`が有効になり、一部の DDL 操作ではファイルシステム内の一時ファイルの読み取りと書き込みが必要になります。場所は、構成項目[`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)によって定義されます。TiDB を実行するユーザーには、オペレーティング システムのそのディレクトリに対する読み取りおよび書き込み権限があることを確認する必要があります。デフォルトのディレクトリ`/tmp/tidb`は、tmpfs (一時ファイル システム) を使用します。ディスク ディレクトリを明示的に指定することをお勧めします。次の例では、 `/data/tidb-deploy/tempdir`使用しています。

    > **注記：**
    >
    > アプリケーション内に大きなオブジェクトに対する DDL 操作が存在する場合は、 [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)用に独立した大きなファイル システムを構成することを強くお勧めします。

    ```shell
    sudo mkdir -p /data/tidb-deploy/tempdir
    ```

    `/data/tidb-deploy/tempdir`ディレクトリがすでに存在する場合は、書き込み権限が付与されていることを確認してください。

    ```shell
    sudo chmod -R 777 /data/tidb-deploy/tempdir
    ```

    > **注記：**
    >
    > ディレクトリが存在しない場合は、TiDB は起動時に自動的に作成します。ディレクトリの作成に失敗した場合、または TiDB にそのディレクトリの読み取りおよび書き込み権限がない場合は、実行時に[`Fast Online DDL`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)無効になります。

## 対象マシンのファイアウォールサービスをチェックして停止する {#check-and-stop-the-firewall-service-of-target-machines}

TiDB クラスターでは、読み取りおよび書き込み要求やデータ ハートビートなどの情報の伝送を確実にするために、ノード間のアクセス ポートが開いている必要があります。一般的なオンライン シナリオでは、データベースとアプリケーション サービス間、およびデータベース ノード間のデータ インタラクションはすべて、安全なネットワーク内で行われます。したがって、特別なセキュリティ要件がない場合は、ターゲット マシンのファイアウォールを停止することをお勧めします。それ以外の場合は、 [ポートの使用](/hardware-and-software-requirements.md#network-requirements)を参照して、必要なポート情報をファイアウォール サービスの許可リストに追加します。

このセクションの残りの部分では、ターゲット マシンのファイアウォール サービスを停止する方法について説明します。

1.  ファイアウォールの状態を確認します。CentOS Linux リリース 7.7.1908 (Core) を例に挙げます。

    ```shell
    sudo firewall-cmd --state
    sudo systemctl status firewalld.service
    ```

2.  ファイアウォール サービスを停止します。

    ```bash
    sudo systemctl stop firewalld.service
    ```

3.  ファイアウォール サービスの自動起動を無効にします。

    ```bash
    sudo systemctl disable firewalld.service
    ```

4.  ファイアウォールの状態を確認します。

    ```bash
    sudo systemctl status firewalld.service
    ```

## NTPサービスを確認してインストールする {#check-and-install-the-ntp-service}

TiDB は、 ACIDモデルでのトランザクションの線形一貫性を保証するためにノード間のクロック同期を必要とする分散データベース システムです。

現在、クロック同期の一般的なソリューションは、ネットワーク タイム プロトコル (NTP) サービスを使用することです。インターネット上の`pool.ntp.org`タイミング サービスを使用することも、オフライン環境で独自の NTP サービスを構築することもできます。

NTP サービスがインストールされ、NTPサーバーと正常に同期しているかどうかを確認するには、次の手順を実行します。

1.  次のコマンドを実行します。 `running`が返された場合、NTP サービスは実行されています。

    ```bash
    sudo systemctl status ntpd.service
    ```

        ntpd.service - Network Time Service
        Loaded: loaded (/usr/lib/systemd/system/ntpd.service; disabled; vendor preset: disabled)
        Active: active (running) since 一 2017-12-18 13:13:19 CST; 3s ago

    -   `Unit ntpd.service could not be found.`が返された場合は、次のコマンドを試して、システムが NTP とのクロック同期を実行するために`ntpd`ではなく`chronyd`使用するように設定されているかどうかを確認します。

        ```bash
        sudo systemctl status chronyd.service
        ```

            chronyd.service - NTP client/server
            Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
            Active: active (running) since Mon 2021-04-05 09:55:29 EDT; 3 days ago

        結果に`chronyd`も`ntpd`も設定されていないと表示された場合は、どちらもシステムにインストールされていないことを意味します。まず`chronyd`または`ntpd`インストールし、自動的に起動できることを確認してください。デフォルトでは`ntpd`が使用されます。

        システムが`chronyd`使用するように構成されている場合は、手順 3 に進みます。

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
    > これは、NTPd ではなく Chrony を使用するシステムにのみ適用されます。

    ```bash
    chronyc tracking
    ```

    -   コマンドが`Leap status     : Normal`返す場合、同期プロセスは正常です。

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

    -   コマンドが次の結果を返す場合、同期でエラーが発生しています。

            Leap status    : Not synchronised

    -   コマンドが次の結果を返す場合、 `chronyd`サービスは正常に実行されていません。

            506 Cannot talk to daemon

NTP サービスの同期をできるだけ早く開始するには、次のコマンドを実行します。1 `pool.ntp.org` NTPサーバーに置き換えます。

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

## オペレーティングシステムの最適なパラメータを確認して構成する {#check-and-configure-the-optimal-parameters-of-the-operating-system}

本番環境の TiDB の場合、次の方法でオペレーティング システム構成を最適化することをお勧めします。

1.  THP (Transparent Huge Pages) を無効にします。データベースのメモリアクセス パターンは、連続的ではなく、散在的になる傾向があります。高レベルのメモリの断片化が深刻な場合、THP ページが割り当てられると、レイテンシーが高くなります。

2.  storageメディアの I/O スケジューラを設定します。

    -   高速 SSDstorageの場合、カーネルのデフォルトの I/O スケジューリング操作によってパフォーマンスが低下する可能性があります。I/O スケジューラを`noop`や`none`などの先入れ先出し (FIFO) に設定することをお勧めします。この構成により、カーネルはスケジュールなしで I/O 要求を直接ハードウェアに渡すことができるため、パフォーマンスが向上します。
    -   NVMestorageの場合、デフォルトの I/O スケジューラは`none`なので、調整は必要ありません。

3.  CPU 周波数を制御する cpufrequ モジュールの`performance`モードを選択します。CPU 周波数が動的な調整なしでサポートされている最高の動作周波数に固定されている場合、パフォーマンスが最大化されます。

現在のオペレーティング システムの構成を確認し、最適なパラメータを構成するには、次の手順を実行します。

1.  THP が有効か無効かを確認するには、次のコマンドを実行します。

    ```bash
    cat /sys/kernel/mm/transparent_hugepage/enabled
    ```

        [always] madvise never

    > **注記：**
    >
    > `[always] madvise never`が出力された場合、THP が有効になっています。無効にする必要があります。

2.  次のコマンドを実行して、データ ディレクトリが配置されているディスクの I/O スケジューラを確認します。

    データ ディレクトリで SD または VD デバイスを使用している場合は、次のコマンドを実行して I/O スケジューラを確認します。

    ```bash
    cat /sys/block/sd[bc]/queue/scheduler
    ```

        noop [deadline] cfq
        noop [deadline] cfq

    > **注記：**
    >
    > `noop [deadline] cfq`出力された場合、ディスクの I/O スケジューラは`deadline`モードになっています。これを`noop`に変更する必要があります。

    データ ディレクトリで NVMe デバイスを使用している場合は、次のコマンドを実行して I/O スケジューラを確認します。

    ```bash
    cat /sys/block/nvme[01]*/queue/scheduler
    ```

        [none] mq-deadline kyber bfq
        [none] mq-deadline kyber bfq

    > **注記：**
    >
    > `[none] mq-deadline kyber bfq` NVMe デバイスが`none` I/O スケジューラを使用し、変更する必要がないことを示します。

3.  ディスクの`ID_SERIAL`表示するには、次のコマンドを実行します。

    ```bash
    udevadm info --name=/dev/sdb | grep ID_SERIAL
    ```

        E: ID_SERIAL=36d0946606d79f90025f3e09a0c1f9e81
        E: ID_SERIAL_SHORT=6d0946606d79f90025f3e09a0c1f9e81

    > **注記：**
    >
    > -   複数のディスクにデータ ディレクトリが割り当てられている場合は、各ディスクの`ID_SERIAL`記録するために、各ディスクに対して上記のコマンドを実行する必要があります。
    > -   デバイスが`noop`または`none`スケジューラを使用している場合は、 `ID_SERIAL`を記録したり、udev ルールや調整されたプロファイルを構成したりする必要はありません。

4.  cpufreq モジュールの電源ポリシーを確認するには、次のコマンドを実行します。

    ```bash
    cpupower frequency-info --policy
    ```

        analyzing CPU 0:
        current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                      The governor "powersave" may decide which speed to use within this range.

    > **注記：**
    >
    > `The governor "powersave"`が出力された場合、 cpufreq モジュールの電源ポリシーは`powersave`です。これを`performance`に変更する必要があります。仮想マシンまたはクラウドホストを使用する場合、出力は通常`Unable to determine current policy`であり、何も変更する必要はありません。

5.  オペレーティング システムの最適なパラメータを構成します。

    -   方法 1: チューニングを使用する (推奨)

        1.  現在のオペレーティング システムの調整されたプロファイルを表示するには、 `tuned-adm list`コマンドを実行します。

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

            出力`Current active profile: balanced`は、現在のオペレーティング システムの調整済みプロファイルが`balanced`であることを意味します。現在のプロファイルに基づいて、オペレーティング システムの構成を最適化することをお勧めします。

        2.  新しい調整済みプロファイルを作成します。

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

            出力`include=balanced`は、オペレーティング システムの最適化構成を現在の`balanced`プロファイルに追加することを意味します。

        3.  新しく調整されたプロファイルを適用します。

            > **注記：**
            >
            > デバイスが`noop`または`none` I/O スケジューラを使用している場合は、この手順をスキップしてください。調整されたプロファイルではスケジューラの構成は必要ありません。

            ```bash
            tuned-adm profile balanced-tidb-optimal
            ```

    -   方法 2: スクリプトを使用して構成します。すでに方法 1 を使用している場合は、この方法をスキップしてください。

        1.  デフォルトのカーネル バージョンを確認するには、 `grubby`コマンドを実行します。

            > **注記：**
            >
            > `grubby`実行する前に、まず`grubby`パッケージをインストールします。

            ```bash
            grubby --default-kernel
            ```

            ```bash
            /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

        2.  カーネル構成を変更するには、 `grubby --update-kernel`実行します。

            ```bash
            grubby --args="transparent_hugepage=never" --update-kernel `grubby --default-kernel`
            ```

            > **注記：**
            >
            > `--update-kernel`後に実際のバージョン番号を指定することもできます (例: `--update-kernel /boot/vmlinuz-3.10.0-957.el7.x86_64` )。

        3.  変更されたデフォルトのカーネル構成を確認するには、 `grubby --info`実行します。

            ```bash
            grubby --info /boot/vmlinuz-3.10.0-957.el7.x86_64
            ```

            > **注記：**
            >
            > `--info`後には実際のデフォルトのカーネル バージョンが続きます。

                index=0
                kernel=/boot/vmlinuz-3.10.0-957.el7.x86_64
                args="ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet LANG=en_US.UTF-8 transparent_hugepage=never"
                root=/dev/mapper/centos-root
                initrd=/boot/initramfs-3.10.0-957.el7.x86_64.img
                title=CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)

        4.  THP を直ちに無効にするには、現在のカーネル構成を変更します。

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

            > **注記：**
            >
            > デバイスが`noop`または`none` I/O スケジューラを使用している場合は、この手順をスキップしてください。udev ルールの構成は必要ありません。

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

        8.  CPU 電源ポリシー構成サービスを適用します。

            ```bash
            systemctl daemon-reload
            systemctl enable cpupower.service
            systemctl start cpupower.service
            ```

6.  THP ステータスを確認するには、次のコマンドを実行します。

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

8.  cpufreq モジュールの電源ポリシーを確認するには、次のコマンドを実行します。

    ```bash
    cpupower frequency-info --policy
    ```

        analyzing CPU 0:
        current policy: frequency should be within 1.20 GHz and 3.10 GHz.
                      The governor "performance" may decide which speed to use within this range.

9.  `sysctl`パラメータを変更するには、次のコマンドを実行します。

    ```bash
    echo "fs.file-max = 1000000">> /etc/sysctl.conf
    echo "net.core.somaxconn = 32768">> /etc/sysctl.conf
    echo "net.ipv4.tcp_tw_recycle = 0">> /etc/sysctl.conf
    echo "net.ipv4.tcp_syncookies = 0">> /etc/sysctl.conf
    echo "vm.overcommit_memory = 1">> /etc/sysctl.conf
    echo "vm.min_free_kbytes = 1048576">> /etc/sysctl.conf
    sysctl -p
    ```

    > **注記：**
    >
    > -   `vm.min_free_kbytes`は、システムによって予約される空きメモリの最小量 (KiB 単位) を制御する Linux カーネル パラメータです。
    > -   `vm.min_free_kbytes`に設定すると、メモリ再利用メカニズムに影響します。設定が大きすぎると使用可能なメモリが減少し、設定が小さすぎるとメモリ要求速度がバックグラウンド再利用速度を超え、メモリ再利用が発生してメモリ割り当てが遅れる可能性があります。
    > -   少なくとも`vm.min_free_kbytes` ～ `1048576` KiB (1 GiB) に設定することをお勧めします。 [NUMAがインストールされている](/check-before-deployment.md#install-the-numactl-tool)場合は`number of NUMA nodes * 1048576` KiB に設定することをお勧めします。
    > -   メモリサイズが 16 GiB 未満のサーバーの場合は、デフォルト値の`vm.min_free_kbytes`変更せずに維持することをお勧めします。
    > -   `tcp_tw_recycle` Linux カーネル 4.12 で削除されました。それ以降のカーネル バージョンを使用している場合は、この設定をスキップしてください。

10. ユーザーの`limits.conf`ファイルを構成するには、次のコマンドを実行します。

    ```bash
    cat << EOF >>/etc/security/limits.conf
    tidb           soft    nofile          1000000
    tidb           hard    nofile          1000000
    tidb           soft    stack          32768
    tidb           hard    stack          32768
    EOF
    ```

## SSH相互信頼とパスワードなしのsudoを手動で設定する {#manually-configure-the-ssh-mutual-trust-and-sudo-without-password}

このセクションでは、SSH 相互信頼とパスワードなしの sudo を手動で構成する方法について説明します。デプロイメントには、SSH 相互信頼とパスワードなしのログインを自動的に構成するTiUP を使用することをお勧めします。TiUPを使用して TiDB クラスターをデプロイする場合は、このセクションを無視してください。

1.  それぞれ`root`ユーザー アカウントを使用してターゲット マシンにログインし、 `tidb`ユーザーを作成してログイン パスワードを設定します。

    ```bash
    useradd tidb && \
    passwd tidb
    ```

2.  パスワードなしで sudo を設定するには、次のコマンドを実行し、ファイルの末尾に`tidb ALL=(ALL) NOPASSWD: ALL`を追加します。

    ```bash
    visudo
    ```

        tidb ALL=(ALL) NOPASSWD: ALL

3.  `tidb`ユーザーを使用してコントロール マシンにログインし、次のコマンドを実行します。3 `10.0.1.1`ターゲット マシンの IP に置き換え、プロンプトに従ってターゲット マシンの`tidb`ユーザー パスワードを入力します。コマンドの実行後、SSH 相互信頼がすでに作成されています。これは他のマシンにも適用されます。新しく作成された`tidb`ユーザーには`.ssh`ディレクトリがありません。このようなディレクトリを作成するには、RSA キーを生成するコマンドを実行します。コントロール マシンに TiDB コンポーネントを展開するには、コントロール マシンとコントロール マシン自体の相互信頼を構成します。

    ```bash
    ssh-keygen -t rsa
    ssh-copy-id -i ~/.ssh/id_rsa.pub 10.0.1.1
    ```

4.  `tidb`ユーザーアカウントを使用してコントロールマシンにログインし、 `ssh`使用してターゲットマシンの IP にログインします。パスワードを入力する必要がなく、正常にログインできる場合は、SSH 相互信頼が正常に構成されています。

    ```bash
    ssh 10.0.1.1
    ```

        [tidb@10.0.1.1 ~]$

5.  `tidb`ユーザーを使用してターゲット マシンにログインした後、次のコマンドを実行します。パスワードを入力する必要がなく、 `root`ユーザーに切り替えることができれば、 `tidb`ユーザーのパスワードなしの sudo が正常に構成されています。

    ```bash
    sudo -su root
    ```

        [root@10.0.1.1 tidb]#

## <code>numactl</code>ツールをインストールする {#install-the-code-numactl-code-tool}

このセクションでは、NUMA ツールのインストール方法について説明します。オンライン環境では、ハードウェア構成が通常必要以上に高いため、ハードウェア リソースをより適切に計画するために、TiDB または TiKV の複数のインスタンスを 1 台のマシンに展開できます。このようなシナリオでは、NUMA ツールを使用して、パフォーマンスの低下を引き起こす可能性のある CPU リソースの競合を防ぐことができます。

> **注記：**
>
> -   NUMA を使用してコアをバインドすることは、CPU リソースを分離する方法であり、高度に構成された物理マシンに複数のインスタンスを展開するのに適しています。
> -   `tiup cluster deploy`使用してデプロイを完了したら、 `exec`コマンドを使用してクラスター レベルの管理操作を実行できます。

NUMA ツールをインストールするには、次の 2 つの方法のいずれかを実行します。

**方法 1** : ターゲット ノードにログインして NUMA をインストールします。CentOS Linux リリース 7.7.1908 (Core) を例に挙げます。

```bash
sudo yum -y install numactl
```

**方法 2** : `tiup cluster exec`コマンドを実行して、既存のクラスターに NUMA をバッチでインストールします。

1.  [TiUP を使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってクラスター`tidb-test`を展開します。TiDB クラスターをインストールしている場合は、この手順をスキップできます。

    ```bash
    tiup cluster deploy tidb-test v6.1.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2.  `sudo`権限を使用して`tiup cluster exec`コマンドを実行し、 `tidb-test`クラスター内のすべてのターゲット マシンに NUMA をインストールします。

    ```bash
    tiup cluster exec tidb-test --sudo --command "yum -y install numactl"
    ```

    `tiup cluster exec`コマンドのヘルプ情報を取得するには、 `tiup cluster exec --help`コマンドを実行します。

## SELinuxを無効にする {#disable-selinux}

[強制取得(8)](https://linux.die.net/man/8/getenforce)ユーティリティを使用して、SELinux が無効になっているか、または permissive に設定されているかを確認します。強制モードの SELinux は、デプロイメントの失敗を引き起こす可能性があります。SELinux を無効にする手順については、オペレーティング システムのドキュメントを参照してください。
