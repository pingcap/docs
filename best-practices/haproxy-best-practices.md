---
title: Best Practices for Using HAProxy in TiDB
summary: HAProxyは、TCPおよびHTTPベースのアプリケーション向けの無料のオープンソースロードバランサおよびプロキシサーバーです。高可用性、負荷分散、ヘルスチェック、スティッキーセッション、SSLサポート、監視機能を提供します。HAProxyを導入するには、ハードウェアとソフトウェアの要件を満たしていることを確認の上、インストールと設定を行ってください。最適な結果を得るには、最新の安定バージョンをご使用ください。
aliases: ['/ja/tidb/stable/haproxy-best-practices/','/ja/tidb/dev/haproxy-best-practices/']
---

# TiDB で HAProxy を使用するためのベストプラクティス {#best-practices-for-using-haproxy-in-tidb}

このドキュメントでは、TiDBにおける[HAプロキシ](https://github.com/haproxy/haproxy)の設定と使用に関するベストプラクティスについて説明します。HAProxyは、TCPベースのアプリケーションの負荷分散を提供します。TiDBクライアントからは、HAProxyが提供するフローティング仮想IPアドレスに接続するだけでデータを操作できるため、TiDBサーバーレイヤーでの負荷分散を実現できます。

![HAProxy Best Practices in TiDB](/media/haproxy.jpg)

> **注記：**
>
> TiDBのすべてのバージョンで動作するHAProxyの最小バージョンはv1.5です。v1.5とv2.1の間では、 `mysql-check`の`post-41`オプションを設定する必要があります。HAProxy v2.2以降の使用をお勧めします。

## HAProxyの概要 {#haproxy-overview}

HAProxyは、C言語で書かれた無料のオープンソースソフトウェアで、TCPおよびHTTPベースのアプリケーション向けの高可用性ロードバランサおよびプロキシサーバーを提供します。CPUとメモリを高速かつ効率的に使用できるため、GitHub、Bitbucket、Stack Overflow、Reddit、Tumblr、Twitter、Tuenti、AWS（Amazon Web Services）など、多くの著名なウェブサイトで広く利用されています。

HAProxyは、LinuxカーネルのコアコントリビューターであるWilly Tarreauによって2000年に作成されました。彼は現在もプロジェクトのメンテナンスを担当し、オープンソースコミュニティに無料のソフトウェアアップデートを提供しています。このガイドでは、HAProxy [2.6](https://www.haproxy.com/blog/announcing-haproxy-2-6/)使用しています。最新の安定版の使用を推奨します。詳細は[HAProxyのリリースバージョン](http://www.haproxy.org/)ご覧ください。

## 基本機能 {#basic-features}

-   [高可用性](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.4) : HAProxy は、正常なシャットダウンとシームレスな切り替えをサポートする高可用性を提供します。
-   [負荷分散](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html#4.2-balance) : 2 つの主要なプロキシ モード (レイヤー4 とも呼ばれる TCP とレイヤー7 とも呼ばれる HTTP) がサポートされています。ラウンドロビン、Leastconn、ランダムなど、9 種類以上の負荷分散アルゴリズムがサポートされています。
-   [健康チェック](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html#5.2-check) : HAProxy はサーバーの HTTP または TCP モードのステータスを定期的にチェックします。
-   [スティッキーセッション](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.6) : アプリケーションがスティッキーセッションをサポートしていない間、HAProxy はクライアントを特定のサーバーに固定することができます。
-   [SSL](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.2) : HTTPS 通信と解決がサポートされます。
-   [監視と統計](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.3) ：Web ページを通じて、サービスの状態とトラフィック フローをリアルタイムで監視できます。

## 始める前に {#before-you-begin}

HAProxy をデプロイする前に、ハードウェアとソフトウェアの要件を満たしていることを確認してください。

### ハードウェア要件 {#hardware-requirements}

[HAProxyドキュメント](https://www.haproxy.com/documentation/haproxy-enterprise/getting-started/installation/linux/)によると、HAProxyの最小ハードウェア構成は以下の表の通りです。Sysbench `oltp_read_write`ワークロードでは、この構成での最大QPSは約50Kです。負荷分散環境に応じてサーバー構成を増やすことができます。

| ハードウェアリソース        | 最小仕様           |
| :---------------- | :------------- |
| CPU               | 2コア、3.5GHz     |
| メモリ               | 4ギガバイト         |
| ストレージ             | 50 GB (SATA)   |
| ネットワークインターフェースカード | 10Gネットワ​​ークカード |

### ソフトウェア要件 {#software-requirements}

以下のオペレーティングシステムをご使用いただけます。必要な依存関係がインストールされていることを確認してください。yum を使用して HAProxy をインストールすると、依存関係も一緒にインストールされるため、別途インストールする必要はありません。

#### オペレーティングシステム {#operating-systems}

| Linuxディストリビューション      | バージョン         |
| :-------------------- | :------------ |
| レッドハットエンタープライズリナックス   | 7または8         |
| セントOS                 | 7または8         |
| Oracle エンタープライズ Linux | 7または8         |
| Ubuntu LTS            | 18.04以降のバージョン |

> **注記：**
>
> -   サポートされているその他のオペレーティング システムの詳細については、 [HAProxyドキュメント](https://github.com/haproxy/haproxy/blob/master/INSTALL)参照してください。

#### 依存関係 {#dependencies}

-   エペルリリース
-   gcc
-   systemd-devel

上記の依存関係をインストールするには、次のコマンドを実行します。

```bash
yum -y install epel-release gcc systemd-devel
```

## HAProxyをデプロイ {#deploy-haproxy}

HAProxyを使用すると、負荷分散されたデータベース環境を簡単に構成・セットアップできます。このセクションでは、一般的なデプロイメント操作について説明します。実際のシナリオに合わせて[設定ファイル](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html)カスタマイズできます。

### HAProxyをインストールする {#install-haproxy}

1.  HAProxy 2.6.21 ソースコードのパッケージをダウンロードします。

    ```bash
    wget https://www.haproxy.org/download/2.6/src/haproxy-2.6.21.tar.gz
    ```

2.  パッケージを抽出します。

    ```bash
    tar zxf haproxy-2.6.21.tar.gz
    ```

3.  ソース コードからアプリケーションをコンパイルします。

    ```bash
    cd haproxy-2.6.21
    make clean
    make -j 8 TARGET=linux-glibc USE_THREAD=1
    make PREFIX=${/app/haproxy} SBINDIR=${/app/haproxy/bin} install  # Replace `${/app/haproxy}` and `${/app/haproxy/bin}` with your custom directories.
    ```

4.  プロファイルを再構成します。

    ```bash
    echo 'export PATH=/app/haproxy/bin:$PATH' >> /etc/profile
    . /etc/profile
    ```

5.  インストールが成功したかどうかを確認します。

    ```bash
    which haproxy
    ```

#### HAProxyコマンド {#haproxy-commands}

キーワードとその基本的な使用法のリストを印刷するには、次のコマンドを実行します。

```bash
haproxy --help
```

| オプション                           | 説明                                                                                                                                                              |
| :------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-v`                            | バージョンとビルドの日付を報告します。                                                                                                                                             |
| `-vv`                           | バージョン、ビルド オプション、ライブラリ バージョン、使用可能なポーラーを表示します。                                                                                                                    |
| `-d`                            | デバッグ モードを有効にします。                                                                                                                                                |
| `-db`                           | バックグラウンド モードとマルチプロセス モードを無効にします。                                                                                                                                |
| `-dM [<byte>]`                  | メモリポイズニングを強制します。つまり、malloc() または pool_alloc2() で割り当てられたすべてのメモリ領域は、呼び出し元に渡される前に`<byte>`で埋められます。                                                                  |
| `-V`                            | 詳細モードを有効にします (静音モードを無効にします)。                                                                                                                                    |
| `-D`                            | デーモンとして起動します。                                                                                                                                                   |
| `-C <dir>`                      | 設定ファイルを読み込む前にディレクトリ`<dir>`に変更します。                                                                                                                               |
| `-W`                            | マスターワーカーモード。                                                                                                                                                    |
| `-q`                            | 「quiet」モードを設定します。これにより、構成の解析中および起動中に一部のメッセージが無効になります。                                                                                                           |
| `-c`                            | バインドを試みる前に、構成ファイルのチェックのみを実行して終了します。                                                                                                                             |
| `-n <limit>`                    | プロセスごとの接続制限を`<limit>`に制限します。                                                                                                                                    |
| `-m <limit>`                    | すべてのプロセスにわたって割り当て可能なメモリのメモリを`<limit>`メガバイトに制限します。                                                                                                               |
| `-N <limit>`                    | 組み込みのデフォルト値 (通常は 2000) ではなく、プロキシごとのデフォルトの maxconn を`<limit>`に設定します。                                                                                             |
| `-L <name>`                     | ローカル ピア名を`<name>`に変更します。これはデフォルトでローカル ホスト名になります。                                                                                                                |
| `-p <file>`                     | 起動時にすべてのプロセスの PID を`<file>`に書き込みます。                                                                                                                             |
| `-de`                           | epoll(7)の使用を無効にします。epoll(7)はLinux 2.6および一部のカスタムLinux 2.4システムでのみ利用可能です。                                                                                          |
| `-dp`                           | poll(2) の使用を無効にします。代わりに select(2) が使用される場合があります。                                                                                                                |
| `-dS`                           | 古いカーネルでは壊れているsplice(2)の使用を無効にします。                                                                                                                               |
| `-dR`                           | SO_REUSEPORT の使用を無効にします。                                                                                                                                        |
| `-dr`                           | サーバーのアドレス解決の失敗を無視します。                                                                                                                                           |
| `-dV`                           | サーバー側での SSL 検証を無効にします。                                                                                                                                          |
| `-sf <pidlist>`                 | 起動後、pidlist で指定されたPIDに「finish」シグナルを送信します。このシグナルを受信したプロセスは、すべてのセッションが終了するまで待機してから終了します。このオプションは最後に指定する必要があり、その後に任意の数のPIDが続きます。厳密には、SIGTTOUとSIGUSR1が送信されます。       |
| `-st <pidlist>`                 | 起動後、pidlist で指定されたPIDに「terminate」シグナルを送信します。このシグナルを受信したプロセスは即座に終了し、すべてのアクティブなセッションが閉じられます。このオプションは最後に指定する必要があり、その後に任意の数のPIDが続きます。厳密に言えば、SIGTTOUとSIGTERMが送信されます。 |
| `-x <unix_socket>`              | 指定されたソケットに接続し、古いプロセスからすべてのリスニングソケットを取得します。その後、新しいソケットをバインドする代わりに、これらのソケットを使用します。                                                                                |
| `-S <bind>[,<bind_options>...]` | マスターワーカーモードでは、マスターCLIを作成します。このCLIは、すべてのワーカーのCLIへのアクセスを可能にします。デバッグに役立ち、離脱中のプロセスにアクセスする便利な方法です。                                                                   |

HAProxy コマンドライン オプションの詳細については、 [HAProxyの管理ガイド](http://cbonte.github.io/haproxy-dconv/2.6/management.html)と[HAProxyの一般コマンドマニュアル](https://manpages.debian.org/buster-backports/haproxy/haproxy.1.en.html)を参照してください。

### HAProxyを設定する {#configure-haproxy}

yum を使用して HAProxy をインストールすると、設定テンプレートが生成されます。シナリオに応じて、以下の設定項目をカスタマイズすることもできます。

```yaml
global                                     # Global configuration.
   log         127.0.0.1 local2            # Global syslog servers (up to two).
   chroot      /var/lib/haproxy            # Changes the current directory and sets superuser privileges for the startup process to improve security.
   pidfile     /var/run/haproxy.pid        # Writes the PIDs of HAProxy processes into this file.
   maxconn     4096                        # The maximum number of concurrent connections for a single HAProxy process. It is equivalent to the command-line argument "-n".
   nbthread    48                          # The maximum number of threads. (The upper limit is equal to the number of CPUs)
   user        haproxy                     # Same with the UID parameter.
   group       haproxy                     # Same with the GID parameter. A dedicated user group is recommended.
   daemon                                  # Makes the process fork into background. It is equivalent to the command line "-D" argument. It can be disabled by the command line "-db" argument.
   stats socket /var/lib/haproxy/stats     # The directory where statistics output is saved.

defaults                                   # Default configuration.
   log global                              # Inherits the settings of the global configuration.
   retries 2                               # The maximum number of retries to connect to an upstream server. If the number of connection attempts exceeds the value, the backend server is considered unavailable.
   timeout connect  2s                     # The maximum time to wait for a connection attempt to a backend server to succeed. It should be set to a shorter time if the server is located on the same LAN as HAProxy.
   timeout client 30000s                   # The maximum inactivity time on the client side.
   timeout server 30000s                   # The maximum inactivity time on the server side.

listen admin_stats                         # The name of the Stats page reporting information from frontend and backend. You can customize the name according to your needs.
   bind 0.0.0.0:8080                       # The listening port.
   mode http                               # The monitoring mode.
   option httplog                          # Enables HTTP logging.
   maxconn 10                              # The maximum number of concurrent connections.
   stats refresh 30s                       # Automatically refreshes the Stats page every 30 seconds.
   stats uri /haproxy                      # The URL of the Stats page.
   stats realm HAProxy                     # The authentication realm of the Stats page.
   stats auth admin:pingcap123             # User name and password in the Stats page. You can have multiple user names.
   stats hide-version                      # Hides the version information of HAProxy on the Stats page.
   stats admin if TRUE                     # Manually enables or disables the backend server (supported in HAProxy 1.4.9 or later versions).

listen tidb-cluster                        # Database load balancing.
   bind 0.0.0.0:3390                       # The Floating IP address and listening port.
   mode tcp                                # HAProxy uses layer 4, the transport layer.
   balance leastconn                       # The server with the smallest number of connections receives the connection. "leastconn" is recommended where long sessions are expected, such as LDAP, SQL and TSE, rather than protocols using short sessions, such as HTTP. The algorithm is dynamic, which means that server weights might be adjusted on the fly for slow starts for instance.
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

`SHOW PROCESSLIST`使用して送信元 IP アドレスを確認するには、 [PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を TiDB に接続するように設定する必要があります。

```yaml
   server tidb-1 10.9.18.229:4000 send-proxy check inter 2000 rise 2 fall 3       
   server tidb-2 10.9.39.208:4000 send-proxy check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 send-proxy check inter 2000 rise 2 fall 3
```

> **注記：**
>
> PROXY プロトコルを使用する前に、TiDBサーバーの構成ファイルで[`proxy-protocol.networks`](/tidb-configuration-file.md#networks)構成する必要があります。

### HAProxyを起動する {#start-haproxy}

HAProxy を起動するには、 `haproxy`を実行します。デフォルトでは`/etc/haproxy/haproxy.cfg`が読み込まれます (推奨)。

```bash
haproxy -f /etc/haproxy/haproxy.cfg
```

### HAProxyを停止する {#stop-haproxy}

HAProxy を停止するには、 `kill -9`コマンドを使用します。

1.  次のコマンドを実行します。

    ```bash
    ps -ef | grep haproxy
    ```

2.  HAProxy のプロセスを終了します。

    ```bash
    kill -9 ${haproxy.pid}
    ```
