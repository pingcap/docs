---
title: Best Practices for Using HAProxy in TiDB
summary: This document describes best practices for configuration and usage of HAProxy in TiDB.
---

# TiDBでHAProxyを使用するためのベストプラクティス {#best-practices-for-using-haproxy-in-tidb}

このドキュメントでは、TiDBでの[HAProxy](https://github.com/haproxy/haproxy)の構成と使用に関するベストプラクティスについて説明します。 HAProxyは、TCPベースのアプリケーションに負荷分散を提供します。 TiDBクライアントから、HAProxyによって提供されるフローティング仮想IPアドレスに接続するだけでデータを操作できます。これは、TiDBサーバー層での負荷分散を実現するのに役立ちます。

![HAProxy Best Practices in TiDB](/media/haproxy.jpg)

## HAProxyの概要 {#haproxy-overview}

HAProxyは、C言語で記述された無料のオープンソースソフトウェアであり、TCPおよびHTTPベースのアプリケーションに高可用性ロードバランサーとプロキシサーバーを提供します。 CPUとメモリを高速かつ効率的に使用するため、HAProxyは現在、GitHub、Bitbucket、Stack Overflow、Reddit、Tumblr、Twitter、Tuenti、AWS（Amazon Web Services）などの多くの有名なWebサイトで広く使用されています。

HAProxyは、2000年にLinuxカーネルのコアコントリビューターであるWilly Tarreauによって作成されました。彼は、プロジェクトのメンテナンスを引き続き担当し、オープンソースコミュニティで無料のソフトウェアアップデートを提供しています。このガイドでは、 [2.5.0](https://www.haproxy.com/blog/announcing-haproxy-2-5/)を使用します。最新の安定バージョンを使用することをお勧めします。詳細については、 [HAProxyのリリースバージョン](http://www.haproxy.org/)を参照してください。

## 基本的な機能 {#basic-features}

-   [高可用性](http://cbonte.github.io/haproxy-dconv/2.5/intro.html#3.3.4) ：HAProxyは、正常なシャットダウンとシームレスなスイッチオーバーをサポートする高可用性を提供します。
-   [負荷分散](http://cbonte.github.io/haproxy-dconv/2.5/configuration.html#4.2-balance) ：2つの主要なプロキシモードがサポートされています。TCP（レイヤー4とも呼ばれます）とHTTP（レイヤー7とも呼ばれます）。ラウンドロビン、最小接続、ランダムなど、9つ以上の負荷分散アルゴリズムがサポートされています。
-   [健康診断](http://cbonte.github.io/haproxy-dconv/2.5/configuration.html#5.2-check) ：HAProxyは、サーバーのHTTPまたはTCPモードのステータスを定期的にチェックします。
-   [スティッキーセッション](http://cbonte.github.io/haproxy-dconv/2.5/intro.html#3.3.6) ：HAProxyは、アプリケーションがスティッキーセッションをサポートしていない間、クライアントを特定のサーバーに固定できます。
-   [SSL](http://cbonte.github.io/haproxy-dconv/2.5/intro.html#3.3.2) ：HTTPS通信と解決がサポートされています。
-   [監視と統計](http://cbonte.github.io/haproxy-dconv/2.5/intro.html#3.3.3) ：Webページを通じて、サービスの状態とトラフィックフローをリアルタイムで監視できます。

## あなたが始める前に {#before-you-begin}

HAProxyをデプロイする前に、ハードウェアとソフトウェアの要件を満たしていることを確認してください。

### ハードウェア要件 {#hardware-requirements}

サーバーについては、次のハードウェア要件を満たすことをお勧めします。負荷分散環境に応じてサーバーの仕様を改善することもできます。

| ハードウェアリソース        | 最小仕様         |
| :---------------- | :----------- |
| CPU               | 2コア、3.5 GHz  |
| メモリー              | 16ギガバイト      |
| 保管所               | 50 GB（SATA）  |
| ネットワークインターフェースカード | 10Gネットワークカード |

### ソフトウェア要件 {#software-requirements}

次のオペレーティングシステムを使用して、必要な依存関係がインストールされていることを確認できます。 yumを使用してHAProxyをインストールする場合、依存関係はそれと一緒にインストールされるため、個別に再度インストールする必要はありません。

#### オペレーティングシステム {#operating-systems}

| Linuxディストリビューション         | バージョン         |
| :----------------------- | :------------ |
| Red Hat Enterprise Linux | 7または8         |
| CentOS                   | 7または8         |
| Oracle Enterprise Linux  | 7または8         |
| Ubuntu LTS               | 18.04以降のバージョン |

> **ノート：**
>
> -   サポートされている他のオペレーティングシステムの詳細については、 [HAProxyドキュメント](https://github.com/haproxy/haproxy/blob/master/INSTALL)を参照してください。

#### 依存関係 {#dependencies}

-   epel-リリース
-   gcc
-   systemd-devel

上記の依存関係をインストールするには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
yum -y install epel-release gcc systemd-devel
```

## HAProxyをデプロイ {#deploy-haproxy}

HAProxyを使用して、負荷分散されたデータベース環境を簡単に構成およびセットアップできます。このセクションでは、一般的な展開操作について説明します。実際のシナリオに基づいて[構成ファイル](http://cbonte.github.io/haproxy-dconv/2.5/configuration.html)をカスタマイズできます。

### HAProxyをインストールする {#install-haproxy}

1.  HAProxy2.5.0ソースコードのパッケージをダウンロードします。

    {{< copyable "" >}}

    ```bash
    wget https://github.com/haproxy/haproxy/archive/refs/tags/v2.5.0.zip
    ```

2.  パッケージを解凍します。

    {{< copyable "" >}}

    ```bash
    unzip v2.5.0.zip
    ```

3.  ソースコードからアプリケーションをコンパイルします。

    {{< copyable "" >}}

    ```bash
    cd haproxy-2.5.0
    make clean
    make -j 8 TARGET=linux-glibc USE_THREAD=1
    make PREFIX=${/app/haproxy} SBINDIR=${/app/haproxy/bin} install  # Replace `${/app/haproxy}` and `${/app/haproxy/bin}` with your custom directories.
    ```

4.  プロファイルを再構成します。

    {{< copyable "" >}}

    ```bash
    echo 'export PATH=/app/haproxy:$PATH' >> /etc/profile
    ```

5.  インストールが成功したかどうかを確認します。

    {{< copyable "" >}}

    ```bash
    which haproxy
    ```

#### HAProxyコマンド {#haproxy-commands}

次のコマンドを実行して、キーワードとその基本的な使用法のリストを印刷します。

{{< copyable "" >}}

```bash
haproxy --help
```

| オプション                           | 説明                                                                                                                                                   |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-v`                            | バージョンとビルド日を報告します。                                                                                                                                    |
| `-vv`                           | バージョン、ビルドオプション、ライブラリバージョン、および使用可能なポーラーを表示します。                                                                                                        |
| `-d`                            | デバッグモードを有効にします。                                                                                                                                      |
| `-db`                           | バックグラウンドモードとマルチプロセスモードを無効にします。                                                                                                                       |
| `-dM [<byte>]`                  | メモリポイズニングを強制します。つまり、malloc（）またはpool_alloc2（）で割り当てられたすべてのメモリ領域は、呼び出し元に渡される前に`<byte>`で埋められます。                                                          |
| `-V`                            | 詳細モードを有効にします（クワイエットモードを無効にします）。                                                                                                                      |
| `-D`                            | デーモンとして起動します。                                                                                                                                        |
| `-C <dir>`                      | 構成ファイルをロードする前に、ディレクトリー`<dir>`に変更します。                                                                                                                 |
| `-W`                            | マスターワーカーモード。                                                                                                                                         |
| `-q`                            | 「クワイエット」モードを設定します。これにより、構成の解析中および起動中に一部のメッセージが無効になります。                                                                                               |
| `-c`                            | バインドを試みる前に、構成ファイルのチェックのみを実行して終了します。                                                                                                                  |
| `-n <limit>`                    | プロセスごとの接続制限を`<limit>`に制限します。                                                                                                                         |
| `-m <limit>`                    | 割り当て可能なメモリの合計を、すべてのプロセスで`<limit>`メガバイトに制限します。                                                                                                        |
| `-N <limit>`                    | 組み込みのデフォルト値（通常は2000）ではなく、デフォルトのプロキシごとのmaxconnを`<limit>`に設定します。                                                                                       |
| `-L <name>`                     | ローカルピア名を`<name>`に変更します。これは、デフォルトでローカルホスト名になります。                                                                                                      |
| `-p <file>`                     | 起動時にすべてのプロセスのPIDを`<file>`に書き込みます。                                                                                                                    |
| `-de`                           | epoll（7）の使用を無効にします。 epoll（7）は、Linux2.6および一部のカスタムLinux2.4システムでのみ使用できます。                                                                               |
| `-dp`                           | poll（2）の使用を無効にします。代わりにselect（2）が使用される場合があります。                                                                                                        |
| `-dS`                           | 古いカーネルでは壊れているsplice（2）の使用を無効にします。                                                                                                                    |
| `-dR`                           | SO_REUSEPORTの使用を無効にします。                                                                                                                              |
| `-dr`                           | サーバーアドレス解決の失敗を無視します。                                                                                                                                 |
| `-dV`                           | サーバー側でSSL検証を無効にします。                                                                                                                                  |
| `-sf <pidlist>`                 | 起動後、pidlistのPIDに「終了」信号を送信します。このシグナルを受信するプロセスは、すべてのセッションが終了するのを待ってから終了します。このオプションは最後に指定する必要があり、その後に任意の数のPIDを指定する必要があります。技術的には、SIGTTOUとSIGUSR1が送信されます。 |
| `-st <pidlist>`                 | 起動後、pidlistのPIDに「終了」信号を送信します。このシグナルを受信したプロセスはすぐに終了し、アクティブなすべてのセッションを閉じます。このオプションは最後に指定する必要があり、その後に任意の数のPIDを指定する必要があります。技術的には、SIGTTOUとSIGTERMが送信されます。 |
| `-x <unix_socket>`              | 指定されたソケットに接続し、古いプロセスからすべてのリスニングソケットを取得します。次に、これらのソケットは、新しいソケットをバインドする代わりに使用されます。                                                                     |
| `-S <bind>[,<bind_options>...]` | マスターワーカーモードで、マスターCLIを作成します。このCLIにより、すべてのワーカーのCLIにアクセスできます。デバッグに役立ちます。これは、離脱プロセスにアクセスするための便利な方法です。                                                    |

HAProxyコマンドラインオプションの詳細については、 [HAProxyの管理ガイド](http://cbonte.github.io/haproxy-dconv/2.5/management.html)および[HAProxyの一般的なコマンドマニュアル](https://manpages.debian.org/buster-backports/haproxy/haproxy.1.en.html)を参照してください。

### HAProxyを構成する {#configure-haproxy}

yumを使用してHAProxyをインストールすると、構成テンプレートが生成されます。シナリオに応じて、以下の構成項目をカスタマイズすることもできます。

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

### HAProxyを起動します {#start-haproxy}

HAProxyを起動するには、 `haproxy`を実行します。デフォルトでは`/etc/haproxy/haproxy.cfg`が読み取られます（推奨）。

{{< copyable "" >}}

```bash
haproxy -f /etc/haproxy/haproxy.cfg
```

### HAProxyを停止します {#stop-haproxy}

HAProxyを停止するには、 `kill -9`コマンドを使用します。

1.  次のコマンドを実行します。

    {{< copyable "" >}}

    ```bash
    ps -ef | grep haproxy
    ```

2.  HAProxyのプロセスを終了します。

    {{< copyable "" >}}

    ```bash
    kill -9 ${haproxy.pid}
    ```
