---
title: Best Practices for Using HAProxy in TiDB
summary: This document describes best practices for configuration and usage of HAProxy in TiDB.
---

# TiDB で HAProxy を使用するためのベスト プラクティス {#best-practices-for-using-haproxy-in-tidb}

このドキュメントでは、TiDB での[HAProxy](https://github.com/haproxy/haproxy)の構成と使用に関するベスト プラクティスについて説明します。 HAProxy は、TCP ベースのアプリケーションの負荷分散を提供します。 TiDB クライアントからは、HAProxy が提供するフローティング仮想 IP アドレスに接続するだけでデータを操作できるため、TiDBサーバーレイヤーでの負荷分散に役立ちます。

![HAProxy Best Practices in TiDB](/media/haproxy.jpg)

> **ノート：**
>
> TiDB のすべてのバージョンで動作する HAProxy の最小バージョンは v1.5 です。 v1.5 と v2.1 の間では、 `post-41`オプションを`mysql-check`に設定する必要があります。 HAProxy v2.2 以降を使用することをお勧めします。

## HAProxy の概要 {#haproxy-overview}

HAProxy は、C 言語で記述された無料のオープンソース ソフトウェアで、TCP および HTTP ベースのアプリケーションに高可用性のロード バランサーとプロキシサーバーを提供します。 CPU とメモリを高速かつ効率的に使用するため、HAProxy は現在、GitHub、Bitbucket、Stack Overflow、Reddit、Tumblr、Twitter、Tuenti、AWS (Amazon Web Services) など、多くの有名な Web サイトで広く使用されています。

HAProxy は 2000 年に Linux カーネルの中心的貢献者である Willy Tarreau によって書かれました。Willy Tarreau は今でもプロジェクトの保守を担当しており、オープンソース コミュニティで無料のソフトウェア アップデートを提供しています。このガイドでは、HAProxy [2.6](https://www.haproxy.com/blog/announcing-haproxy-2-6/)を使用します。最新の安定版を使用することをお勧めします。詳細は[HAProxy のリリース バージョン](http://www.haproxy.org/)参照してください。

## 基本的な機能 {#basic-features}

-   [高可用性](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.4) : HAProxy は、グレースフル シャットダウンとシームレスな切り替えをサポートする高可用性を提供します。
-   [負荷分散](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html#4.2-balance) : 2 つの主要なプロキシ モードがサポートされています。レイヤー4 とも呼ばれる TCP と、レイヤー7 とも呼ばれる HTTP です。roundrobin、leastconn、random など、9 つ以上の負荷分散アルゴリズムがサポートされています。
-   [健康診断](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html#5.2-check) : HAProxy はサーバーの HTTP または TCP モードのステータスを定期的にチェックします。
-   [スティッキー セッション](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.6) : HAProxy は、アプリケーションがスティッキー セッションをサポートしていない間、クライアントを特定のサーバーに固定できます。
-   [SSL](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.2) : HTTPS 通信と解決がサポートされます。
-   [モニタリングと統計](http://cbonte.github.io/haproxy-dconv/2.6/intro.html#3.3.3) : Web ページを通じて、サービスの状態とトラフィック フローをリアルタイムで監視できます。

## あなたが始める前に {#before-you-begin}

HAProxy をデプロイする前に、ハードウェアとソフトウェアの要件を満たしていることを確認してください。

### ハードウェア要件 {#hardware-requirements}

サーバーについては、次のハードウェア要件を満たすことをお勧めします。負荷分散環境に合わせてサーバーのスペックを向上させることもできます。

| ハードウェア リソース       | 最小仕様           |
| :---------------- | :------------- |
| CPU               | 2コア、3.5GHz     |
| メモリー              | 16ギガバイト        |
| 保管所               | 50GB (SATA)    |
| ネットワークインターフェースカード | 10G ネットワーク カード |

### ソフトウェア要件 {#software-requirements}

次のオペレーティング システムを使用して、必要な依存関係がインストールされていることを確認できます。 yum を使用して HAProxy をインストールすると、依存関係が一緒にインストールされるため、個別に再度インストールする必要はありません。

#### オペレーティングシステム {#operating-systems}

| Linux ディストリビューション     | バージョン          |
| :-------------------- | :------------- |
| レッドハット エンタープライズ リナックス | 7または8          |
| CentOS                | 7または8          |
| オラクル エンタープライズ Linux   | 7または8          |
| Ubuntu LTS            | 18.04 以降のバージョン |

> **ノート：**
>
> -   サポートされているその他のオペレーティング システムの詳細については、 [HAProxy ドキュメント](https://github.com/haproxy/haproxy/blob/master/INSTALL)を参照してください。

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

HAProxy を使用すると、負荷分散されたデータベース環境を簡単に構成およびセットアップできます。このセクションでは、一般的な展開操作について説明します。実際のシナリオに基づいて[構成ファイル](http://cbonte.github.io/haproxy-dconv/2.6/configuration.html)をカスタマイズできます。

### HAProxy をインストールする {#install-haproxy}

1.  HAProxy 2.6.2 ソース コードのパッケージをダウンロードします。

    {{< copyable "" >}}

    ```bash
    wget https://www.haproxy.org/download/2.6/src/haproxy-2.6.2.tar.gz
    ```

2.  パッケージを抽出します。

    {{< copyable "" >}}

    ```bash
    tar zxf haproxy-2.6.2.tar.gz
    ```

3.  ソース コードからアプリケーションをコンパイルします。

    {{< copyable "" >}}

    ```bash
    cd haproxy-2.6.2
    make clean
    make -j 8 TARGET=linux-glibc USE_THREAD=1
    make PREFIX=${/app/haproxy} SBINDIR=${/app/haproxy/bin} install  # Replace `${/app/haproxy}` and `${/app/haproxy/bin}` with your custom directories.
    ```

4.  プロファイルを再構成します。

    {{< copyable "" >}}

    ```bash
    echo 'export PATH=/app/haproxy/bin:$PATH' >> /etc/profile
    . /etc/profile
    ```

5.  インストールが成功したかどうかを確認します。

    {{< copyable "" >}}

    ```bash
    which haproxy
    ```

#### HAProxy コマンド {#haproxy-commands}

次のコマンドを実行して、キーワードのリストとその基本的な使用方法を出力します。

{{< copyable "" >}}

```bash
haproxy --help
```

| オプション                           | 説明                                                                                                                                                              |
| :------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-v`                            | バージョンとビルド日を報告します。                                                                                                                                               |
| `-vv`                           | バージョン、ビルド オプション、ライブラリ バージョン、使用可能なポーラーを表示します。                                                                                                                    |
| `-d`                            | デバッグ モードを有効にします。                                                                                                                                                |
| `-db`                           | バックグラウンド モードとマルチプロセス モードを無効にします。                                                                                                                                |
| `-dM [<byte>]`                  | メモリポイズニングを強制します。つまり、malloc() または pool_alloc2() で割り当てられたすべてのメモリ領域が、呼び出し元に渡される前に`<byte>`で埋められます。                                                                  |
| `-V`                            | verbose モードを有効にします (quiet モードを無効にします)。                                                                                                                          |
| `-D`                            | デーモンとして起動します。                                                                                                                                                   |
| `-C <dir>`                      | 構成ファイルをロードする前にディレクトリ`<dir>`に変更します。                                                                                                                              |
| `-W`                            | マスターワーカーモード。                                                                                                                                                    |
| `-q`                            | 「quiet」モードを設定します。これにより、構成の解析中および起動中の一部のメッセージが無効になります。                                                                                                           |
| `-c`                            | 構成ファイルのチェックのみを実行し、バインドを試行する前に終了します。                                                                                                                             |
| `-n <limit>`                    | プロセスごとの接続制限を`<limit>`に制限します。                                                                                                                                    |
| `-m <limit>`                    | すべてのプロセスで割り当て可能なメモリの合計を`<limit>`メガバイトに制限します。                                                                                                                    |
| `-N <limit>`                    | デフォルトのプロキシごとの maxconn を、組み込みのデフォルト値 (通常は 2000) ではなく`<limit>`に設定します。                                                                                             |
| `-L <name>`                     | ローカル ピア名を`<name>`に変更します。デフォルトはローカル ホスト名です。                                                                                                                      |
| `-p <file>`                     | 起動時にすべてのプロセスの PID を`<file>`に書き込みます。                                                                                                                             |
| `-de`                           | epoll(7) の使用を無効にします。 epoll(7) は、Linux 2.6 および一部のカスタム Linux 2.4 システムでのみ使用できます。                                                                                   |
| `-dp`                           | poll(2) の使用を無効にします。代わりに select(2) を使用できます。                                                                                                                      |
| `-dS`                           | 古いカーネルでは機能しない splice(2) の使用を無効にします。                                                                                                                             |
| `-dR`                           | SO_REUSEPORT の使用を無効にします。                                                                                                                                        |
| `-dr`                           | サーバーアドレス解決の失敗を無視します。                                                                                                                                            |
| `-dV`                           | サーバー側で SSL 検証を無効にします。                                                                                                                                           |
| `-sf <pidlist>`                 | 始動後に pidlist 内の PID に「終了」シグナルを送信します。このシグナルを受信したプロセスは、終了する前にすべてのセッションが終了するのを待ちます。このオプションは最後に指定し、その後に任意の数の PID を指定する必要があります。技術的に言えば、SIGTTOU と SIGUSR1 が送信されます。    |
| `-st <pidlist>`                 | 始動後に pidlist 内の PID に「終了」シグナルを送信します。このシグナルを受信したプロセスはただちに終了し、すべてのアクティブなセッションが閉じられます。このオプションは最後に指定し、その後に任意の数の PID を指定する必要があります。技術的に言えば、SIGTTOU と SIGTERM が送信されます。 |
| `-x <unix_socket>`              | 指定されたソケットに接続し、古いプロセスからリッスンしているすべてのソケットを取得します。次に、新しいソケットをバインドする代わりに、これらのソケットが使用されます。                                                                             |
| `-S <bind>[,<bind_options>...]` | マスター ワーカー モードで、マスター CLI を作成します。この CLI を使用すると、すべてのワーカーの CLI にアクセスできます。デバッグに便利で、終了プロセスにアクセスする便利な方法です。                                                             |

HAProxy コマンド ライン オプションの詳細については、 [HAProxy管理ガイド](http://cbonte.github.io/haproxy-dconv/2.6/management.html)および[HAProxy の一般的なコマンド マニュアル](https://manpages.debian.org/buster-backports/haproxy/haproxy.1.en.html)を参照してください。

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

`SHOW PROCESSLIST`を使用して送信元 IP アドレスを確認するには、TiDB に接続するように[プロキシ プロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を構成する必要があります。

```yaml
   server tidb-1 10.9.18.229:4000 send-proxy check inter 2000 rise 2 fall 3       
   server tidb-2 10.9.39.208:4000 send-proxy check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 send-proxy check inter 2000 rise 2 fall 3
```

> **ノート：**
>
> PROXY プロトコルを使用する前に、TiDBサーバーの構成ファイルで[`proxy-protocol.networks`](/tidb-configuration-file.md#networks)を構成する必要があります。

### HAProxy を開始する {#start-haproxy}

HAProxy を開始するには、 `haproxy`を実行します。デフォルトでは`/etc/haproxy/haproxy.cfg`が読み取られます (推奨)。

{{< copyable "" >}}

```bash
haproxy -f /etc/haproxy/haproxy.cfg
```

### HAProxy を停止する {#stop-haproxy}

HAProxy を停止するには、 `kill -9`コマンドを使用します。

1.  次のコマンドを実行します。

    {{< copyable "" >}}

    ```bash
    ps -ef | grep haproxy
    ```

2.  HAProxy のプロセスを終了します。

    {{< copyable "" >}}

    ```bash
    kill -9 ${haproxy.pid}
    ```
