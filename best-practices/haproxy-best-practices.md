---
title: Best Practices for Using HAProxy in TiDB
summary: This document describes best practices for configuration and usage of HAProxy in TiDB.
---

# TiDB で HAProxy を使用するためのベスト プラクティス {#best-practices-for-using-haproxy-in-tidb}

このドキュメントでは、TiDB の[HAプロキシ](https://github.com/haproxy/haproxy)の構成と使用に関するベスト プラクティスについて説明します。 HAProxy は、TCP ベースのアプリケーションの負荷分散を提供します。 TiDB クライアントからは、HAProxy によって提供されるフローティング仮想 IP アドレスに接続するだけでデータを操作できます。これは、TiDBサーバーレイヤーでの負荷分散の実現に役立ちます。

![HAProxy Best Practices in TiDB](/media/haproxy.jpg)

> **注記：**
>
> TiDB のすべてのバージョンで動作する HAProxy の最小バージョンは v1.5 です。 v1.5 と v2.1 の間では、 `mysql-check`に`post-41`オプションを設定する必要があります。 HAProxy v2.2 以降を使用することをお勧めします。

## HAProxyの概要 {#haproxy-overview}

HAProxy は、C 言語で書かれた無料のオープンソース ソフトウェアで、TCP および HTTP ベースのアプリケーションに高可用性ロード バランサーとプロキシサーバーを提供します。 HAProxy は CPU とメモリを高速かつ効率的に使用できるため、現在、GitHub、Bitbucket、Stack Overflow、Reddit、Tumblr、Twitter、Tuenti、AWS (アマゾン ウェブ サービス) などの多くの有名な Web サイトで広く使用されています。

HAProxy は、Linux カーネルの中心的な貢献者である Willy Tarreau によって 2000 年に作成されました。彼は現在もプロジェクトのメンテナンスを担当しており、オープンソース コミュニティで無料のソフトウェア アップデートを提供しています。このガイドでは、HAProxy [2.6](https://www.haproxy.com/blog/announcing-haproxy-2-6/)が使用されます。最新の安定バージョンを使用することをお勧めします。詳細は[HAProxy のリリースされたバージョン](http://www.haproxy.org/)参照してください。

## 基本的な機能 {#basic-features}

-   [高可用性](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.4) : HAProxy は、正常なシャットダウンとシームレスなスイッチオーバーをサポートする高可用性を提供します。
-   [ロードバランシング](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html#4.2-balance) : TCP (レイヤー4 とも呼ばれる) と HTTP (レイヤー7 とも呼ばれる) という 2 つの主要なプロキシ モードがサポートされています。ラウンドロビン、leastconn、ランダムなど、9 つ以上の負荷分散アルゴリズムがサポートされています。
-   [健康診断](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html#5.2-check) : HAProxy はサーバーの HTTP または TCP モードのステータスを定期的にチェックします。
-   [スティッキーセッション](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.6) : HAProxy は、アプリケーションがスティッキー セッションをサポートしていない間、クライアントを特定のサーバーに固定できます。
-   [SSL](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.2) : HTTPS 通信と解決がサポートされます。
-   [モニタリングと統計](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.3) : Web ページを通じて、サービスの状態とトラフィック フローをリアルタイムで監視できます。

## あなたが始める前に {#before-you-begin}

HAProxy を展開する前に、ハードウェアとソフトウェアの要件を満たしていることを確認してください。

### ハードウェア要件 {#hardware-requirements}

サーバーについては、次のハードウェア要件を満たすことをお勧めします。負荷分散環境に応じてサーバーのスペックを向上させることもできます。

| ハードウェアリソース        | 最小仕様           |
| :---------------- | :------------- |
| CPU               | 2コア、3.5GHz     |
| メモリ               | 16ギガバイト        |
| ストレージ             | 50GB(SATA)     |
| ネットワークインターフェースカード | 10Gネットワ​​ークカード |

### ソフトウェア要件 {#software-requirements}

次のオペレーティング システムを使用して、必要な依存関係がインストールされていることを確認できます。 yum を使用して HAProxy をインストールする場合、依存関係も一緒にインストールされるため、再度個別にインストールする必要はありません。

#### オペレーティングシステム {#operating-systems}

| Linuxディストリビューション      | バージョン         |
| :-------------------- | :------------ |
| レッドハット エンタープライズ リナックス | 7または8         |
| CentOS                | 7または8         |
| Oracle エンタープライズ Linux | 7または8         |
| Ubuntu LTS            | 18.04以降のバージョン |

> **注記：**
>
> -   サポートされているその他のオペレーティング システムの詳細については、 [HAProxy ドキュメント](https://github.com/haproxy/haproxy/blob/master/INSTALL)を参照してください。

#### 依存関係 {#dependencies}

-   エペルリリース
-   gcc
-   systemd-開発

上記の依存関係をインストールするには、次のコマンドを実行します。

```bash
yum -y install epel-release gcc systemd-devel
```

## HAProxyのデプロイ {#deploy-haproxy}

HAProxy を使用すると、負荷分散されたデータベース環境を簡単に構成およびセットアップできます。このセクションでは、一般的な展開操作について説明します。実際のシナリオに基づいて[設定ファイル](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html)をカスタマイズできます。

### HAProxy をインストールする {#install-haproxy}

1.  HAProxy 2.6.2 ソース コードのパッケージをダウンロードします。

    ```bash
    wget https://www.haproxy.org/download/2.6/src/haproxy-2.6.2.tar.gz
    ```

2.  パッケージを抽出します。

    ```bash
    tar zxf haproxy-2.6.2.tar.gz
    ```

3.  ソース コードからアプリケーションをコンパイルします。

    ```bash
    cd haproxy-2.6.2
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

#### HAProxy コマンド {#haproxy-commands}

次のコマンドを実行して、キーワードのリストとその基本的な使用法を出力します。

```bash
haproxy --help
```

| オプション                           | 説明                                                                                                                                                        |
| :------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-v`                            | バージョンとビルド日を報告します。                                                                                                                                         |
| `-vv`                           | バージョン、ビルド オプション、ライブラリのバージョン、および使用可能なポーラーを表示します。                                                                                                           |
| `-d`                            | デバッグモードを有効にします。                                                                                                                                           |
| `-db`                           | バックグラウンドモードとマルチプロセスモードを無効にします。                                                                                                                            |
| `-dM [<byte>]`                  | メモリポイズニングを強制します。つまり、malloc() または pool_alloc2() で割り当てられたすべてのメモリ領域は、呼び出し元に渡される前に`<byte>`で埋められます。                                                            |
| `-V`                            | 詳細モードを有効にします (静音モードを無効にします)。                                                                                                                              |
| `-D`                            | デーモンとして起動します。                                                                                                                                             |
| `-C <dir>`                      | 設定ファイルをロードする前にディレクトリ`<dir>`に変更します。                                                                                                                        |
| `-W`                            | マスターワーカーモード。                                                                                                                                              |
| `-q`                            | 「静か」モードを設定します。これにより、構成解析中および起動中に一部のメッセージが無効になります。                                                                                                         |
| `-c`                            | 構成ファイルのチェックのみを実行し、バインドを試行する前に終了します。                                                                                                                       |
| `-n <limit>`                    | プロセスごとの接続制限を`<limit>`に制限します。                                                                                                                              |
| `-m <limit>`                    | すべてのプロセスで割り当て可能なメモリの合計を`<limit>` MB に制限します。                                                                                                               |
| `-N <limit>`                    | デフォルトのプロキシごとの maxconn を、組み込みのデフォルト値 (通常は 2000) ではなく`<limit>`に設定します。                                                                                       |
| `-L <name>`                     | ローカル ピア名を`<name>`に変更します。これはデフォルトでローカル ホスト名になります。                                                                                                          |
| `-p <file>`                     | 起動時にすべてのプロセスの PID を`<file>`に書き込みます。                                                                                                                       |
| `-de`                           | epoll(7) の使用を無効にします。 epoll(7) は、Linux 2.6 および一部のカスタム Linux 2.4 システムでのみ使用できます。                                                                             |
| `-dp`                           | poll(2) の使用を無効にします。代わりに select(2) が使用される場合があります。                                                                                                          |
| `-dS`                           | 古いカーネルでは壊れている splice(2) の使用を無効にします。                                                                                                                       |
| `-dR`                           | SO_REUSEPORT の使用を無効にします。                                                                                                                                  |
| `-dr`                           | サーバーアドレス解決の失敗を無視します。                                                                                                                                      |
| `-dV`                           | サーバー側で SSL 検証を無効にします。                                                                                                                                     |
| `-sf <pidlist>`                 | 起動後に pidlist 内の PID に「終了」信号を送信します。このシグナルを受信したプロセスは、すべてのセッションが終了するまで待ってから終了します。このオプションは最後に指定し、その後に任意の数の PID を指定する必要があります。厳密に言えば、SIGTTOU と SIGUSR1 が送信されます。 |
| `-st <pidlist>`                 | 起動後に pidlist 内の PID に「終了」信号を送信します。このシグナルを受信したプロセスは直ちに終了し、アクティブなセッションをすべて閉じます。このオプションは最後に指定し、その後に任意の数の PID を指定する必要があります。技術的に言えば、SIGTTOU と SIGTERM が送信されます。 |
| `-x <unix_socket>`              | 指定されたソケットに接続し、古いプロセスからリスニングしているすべてのソケットを取得します。その後、これらのソケットは新しいソケットをバインドする代わりに使用されます。                                                                      |
| `-S <bind>[,<bind_options>...]` | マスター/ワーカー モードでは、マスター CLI を作成します。この CLI により、すべてのワーカーの CLI へのアクセスが可能になります。デバッグに便利で、終了プロセスにアクセスする便利な方法です。                                                    |

HAProxy コマンド ライン オプションの詳細については、 [HAProxy管理ガイド](http://cbonte.github.io/haproxy-dconv/2.6/management.html)および[HAProxyの一般コマンドマニュアル](https://manpages.debian.org/buster-backports/haproxy/haproxy.1.en.html)を参照してください。

### HAProxy の構成 {#configure-haproxy}

yum を使用して HAProxy をインストールすると、構成テンプレートが生成されます。シナリオに応じて、次の構成項目をカスタマイズすることもできます。

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

`SHOW PROCESSLIST`を使用して送信元 IP アドレスを確認するには、TiDB に接続するように[プロキシプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を設定する必要があります。

```yaml
   server tidb-1 10.9.18.229:4000 send-proxy check inter 2000 rise 2 fall 3       
   server tidb-2 10.9.39.208:4000 send-proxy check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 send-proxy check inter 2000 rise 2 fall 3
```

> **注記：**
>
> PROXY プロトコルを使用する前に、TiDBサーバーの構成ファイルで[`proxy-protocol.networks`](/tidb-configuration-file.md#networks)を構成する必要があります。

### HAProxyを開始する {#start-haproxy}

HAProxy を開始するには、 `haproxy`を実行します。デフォルトでは`/etc/haproxy/haproxy.cfg`が読み取られます (推奨)。

```bash
haproxy -f /etc/haproxy/haproxy.cfg
```

### HAProxy を停止する {#stop-haproxy}

HAProxy を停止するには、 `kill -9`コマンドを使用します。

1.  次のコマンドを実行します。

    ```bash
    ps -ef | grep haproxy
    ```

2.  HAProxy のプロセスを終了します。

    ```bash
    kill -9 ${haproxy.pid}
    ```
