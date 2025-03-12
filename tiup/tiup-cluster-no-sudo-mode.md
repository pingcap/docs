---
title: Deploy and Maintain an Online TiDB Cluster Using TiUP No-sudo Mode
summary: TiUP no-sudo モードを使用してオンライン TiDB クラスターをデプロイおよび保守する方法を学習します。
---

# TiUP No-sudo モードを使用してオンライン TiDBクラスタをデプロイおよび管理 {#deploy-and-maintain-an-online-tidb-cluster-using-tiup-no-sudo-mode}

このドキュメントでは、 TiUP no-sudo モードを使用してクラスターをデプロイする方法について説明します。

> **注記：**
>
> CentOS の場合、CentOS 8 以降のバージョンのみがサポートされます。

## ユーザーを準備し、SSH相互信頼を構成する {#prepare-the-user-and-configure-the-ssh-mutual-trust}

1.  `tidb`ユーザーを例に挙げます。すべてのターゲット マシンにログインし、次のコマンドで`root`ユーザーを使用して`tidb`という名前のユーザーを作成します。no-sudo モードでは、 `tidb`ユーザーに対してパスワードなしの sudo を構成する必要はありません。つまり、 `tidb`ユーザーを`sudoers`ファイルに追加する必要はありません。

    ```shell
    adduser tidb
    ```

2.  各ターゲット マシンで`tidb`ユーザーに対して`systemd user`モードを開始します。この手順は必須なので、スキップしないでください。

    1.  `tidb`ユーザーを使用して`XDG_RUNTIME_DIR`環境変数を設定します。

        ```shell
        sudo -iu tidb  # Switch to the tidb user
        mkdir -p ~/.bashrc.d
        echo "export XDG_RUNTIME_DIR=/run/user/$(id -u)" > ~/.bashrc.d/systemd
        source ~/.bashrc.d/systemd
        ```

    2.  `root`ユーザーを使用してユーザー サービスを開始します。

        ```shell
        $ uid=$(id -u tidb) # Get the ID of the tidb user
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

    3.  `systemctl --user`実行します。エラーが発生しない場合は、 `systemd user`モードが正常に開始されたことを示します。

3.  `root`ユーザーを使用して次のコマンドを実行し、 systemd ユーザー`tidb`の lingering を有効にします。

    ```shell
    loginctl enable-linger tidb
    loginctl show-user -p Linger tidb # This should show: Linger=yes
    ```

    参考として、systemd のドキュメント[systemd ユーザーインスタンスの自動起動](https://wiki.archlinux.org/title/Systemd/User#Automatic_start-up_of_systemd_user_instances)読んでみてください。

4.  制御マシンで`ssh-keygen`使用してキーを生成します。

    ```shell
    ssh-keygen
    ```

5.  SSH 信頼を確立するには、公開キーをクラスター内の他のマシンにコピーします。

    -   `tidb`ユーザーにパスワードを設定している場合は、 `ssh-copy-id`コマンドを使用して公開キーをターゲット マシンにコピーできます。

        ```shell
        ssh-copy-id tidb@host
        ```

        `host`ターゲット マシンのホスト名に置き換え、クラスター内の他の各マシンでこのコマンドを実行する必要があります。

    -   別の方法で公開鍵をコピーする場合は、コピー後に`/home/tidb/.ssh/authorized_keys`ファイルの権限を必ず確認してください。

        ```shell
        chown -R tidb:tidb /home/tidb/.ssh/authorized_keys
        chmod 600 /home/tidb/.ssh/authorized_keys
        ```

## トポロジファイルを準備する {#prepare-the-topology-file}

1.  次のコマンドを実行してトポロジ ファイルを生成します。

    ```shell
    tiup cluster template > topology.yaml
    ```

2.  トポロジファイルを編集します。

    通常モードと比較して、 TiUP をno-sudo モードで使用する場合は、 `topology.yaml`ファイルの`global`モジュールに`systemd_mode: "user"`行目を追加する必要があります。7 パラメータ`systemd_mode` 、 `systemd user`モードを使用するかどうかを設定するために使用されます。このパラメータが設定されていない場合、デフォルト値は`system`であり、sudo 権限が必要であることを意味します。

    さらに、no-sudo モードでは、非ルート`tidb`ユーザーに`/data`ディレクトリを`deploy_dir`または`data_dir`として使用する権限がないため、非ルート ユーザーがアクセスできるパスを選択する必要があります。次の例では相対パスを使用しており、実際に使用されるパスは`/home/tidb/data/tidb-deploy`と`/home/tidb/data/tidb-data`です。トポロジ ファイルの残りの部分は、通常モードの場合と同じです。別のオプションとして、ルート ユーザーを使用してディレクトリを作成し、 `chown`を使用して所有権を`tidb:tidb`に変更することもできます。

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

## 失敗したチェック項目を手動で修復する {#manually-repair-failed-check-items}

> **注記：**
>
> 最小インストールを使用する場合は、 `tar`パッケージがインストールされていることを確認してください。そうでない場合、 `tiup cluster check`コマンドは失敗します。

`tiup cluster check topology.yaml --user tidb`実行すると、失敗したチェック項目がいくつか生成される場合があります。以下は例です。

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

no-sudo モードでは、 `tidb`ユーザーには sudo 権限がありません。そのため、 `tiup cluster check topology.yaml --apply --user tidb`実行しても失敗したチェック項目を自動的に修正することはできません。ターゲット マシンで`root`ユーザーを使用して手動で修正する必要があります。

詳細については、 [TiDB 環境とシステムコンフィグレーションのチェック](/check-before-deployment.md)参照してください。ドキュメントの手順[SSH相互信頼とパスワードなしのsudoを手動で設定する](/check-before-deployment.md#manually-configure-the-ssh-mutual-trust-and-sudo-without-password)スキップする必要があることに注意してください。

## クラスターのデプロイと管理 {#deploy-and-manage-the-cluster}

前の手順で作成した`tidb`ユーザーを使用し、新しいユーザーを作成しないようにするには、次の`deploy`コマンドを実行するときに`--user tidb`追加します。

```shell
tiup cluster deploy mycluster v8.5.0 topology.yaml --user tidb
```

> **注記：**
>
> 上記のコマンドの`v8.5.0` 、デプロイする TiDB バージョンに置き換え、 `mycluster`クラスターに付ける名前に置き換える必要があります。

クラスターを起動します。

```shell
tiup cluster start mycluster
```

クラスターをスケールアウトします。

```shell
tiup cluster scale-out mycluster scale.yaml --user tidb
```

クラスターのスケールイン:

```shell
tiup cluster scale-in mycluster -N 192.168.124.27:20160
```

クラスターをアップグレードします。

```shell
tiup cluster upgrade mycluster v8.2.0
```

## FAQ {#faq}

### &lt;user@.service&gt; の起動時に<code>Trying to run as user instance, but $XDG_RUNTIME_DIR is not set.</code>エラーが発生します。 {#the-code-trying-to-run-as-user-instance-but-xdg-runtime-dir-is-not-set-code-error-occurs-when-starting-x3c-user-service}

この問題は、 `/etc/pam.d/system-auth.ued`ファイルに`pam_systemd.so`存在しないために発生する可能性があります。

この問題を解決するには、次のコマンドを使用して、 `/etc/pam.d/system-auth.ued`ファイルに`pam_systemd.so`モジュールが含まれているかどうかを確認します。含まれていない場合は、ファイルの末尾に`session optional pam_systemd.so`追加します。

```shell
grep 'pam_systemd.so' /etc/pam.d/system-auth.ued || echo 'session     optional      pam_systemd.so' >> /etc/pam.d/system-auth.ued
```
