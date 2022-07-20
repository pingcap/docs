---
title: Configuration Options
summary: Learn the configuration options in TiDB.
---

# Configuration / コンフィグレーションオプション {#configuration-options}

TiDBクラスタを起動すると、コマンドラインオプションまたは環境変数を使用してクラスターを構成できます。このドキュメントでは、TiDBのコマンドオプションを紹介します。デフォルトのTiDBポートは、クライアント要求用に`4000`つ、ステータスレポート用に`10080`です。

## <code>--advertise-address</code> {#code-advertise-address-code}

-   TiDBサーバーにログインするためのIPアドレス
-   デフォルト： `""`
-   このアドレスには、残りのTiDBクラスタとユーザーがアクセスできる必要があります。

## <code>--config</code> {#code-config-code}

-   構成ファイル
-   デフォルト： `""`
-   構成ファイルを指定した場合、TiDBは構成ファイルを読み取ります。対応する構成がコマンドラインオプションにも存在する場合、TiDBはコマンドラインオプションの構成を使用して、構成ファイルの構成を上書きします。詳細な構成情報については、 [TiDBConfiguration / コンフィグレーションファイルの説明](/tidb-configuration-file.md)を参照してください。

## <code>--config-check</code> {#code-config-check-code}

-   構成ファイルの有効性を確認して終了します
-   デフォルト： `false`

## <code>--config-strict</code> {#code-config-strict-code}

-   構成ファイルの有効性を強制します
-   デフォルト： `false`

## <code>--cors</code> {#code-cors-code}

-   TiDB HTTPステータスサービスのクロスオリジンリクエストシェアリング（CORS）リクエストに`Access-Control-Allow-Origin`の値を指定します
-   デフォルト： `""`

## <code>--host</code> {#code-host-code}

-   TiDBサーバーが監視するホストアドレス
-   デフォルト： `"0.0.0.0"`
-   TiDBサーバーはこのアドレスを監視します。
-   `"0.0.0.0"`アドレスは、デフォルトですべてのネットワークカードを監視します。複数のネットワークカードがある場合は、 `192.168.100.113`などのサービスを提供するネットワークカードを指定します。

## <code>--enable-binlog</code> {#code-enable-binlog-code}

-   TiDBbinlog生成を有効または無効にします
-   デフォルト： `false`

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト： `"info"`
-   `"error"` `"fatal"` `"info"` `"warn"` `"debug"`

## <code>--lease</code> {#code-lease-code}

-   スキーマリースの期間。自分が何をしているのかわからない限り、値を変更するのは**危険**です。
-   デフォルト： `45s`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト： `""`
-   このオプションが設定されていない場合、ログは「stderr」に出力されます。このオプションが設定されている場合、ログは対応するファイルに出力されます。

## <code>--log-slow-query</code> {#code-log-slow-query-code}

-   遅いクエリログのディレクトリ
-   デフォルト： `""`
-   このオプションが設定されていない場合、ログはデフォルトで`--log-file`で指定されたファイルに出力されます。

## <code>--metrics-addr</code> {#code-metrics-addr-code}

-   プロメテウスプッシュゲートウェイの住所
-   デフォルト： `""`
-   空のままにすると、Prometheusクライアントはプッシュを停止します。
-   形式は`--metrics-addr=192.168.100.115:9091`です。

## <code>--metrics-interval</code> {#code-metrics-interval-code}

-   Prometheusクライアントのプッシュ間隔（秒単位）
-   デフォルト： `15s`
-   値を0に設定すると、Prometheusクライアントはプッシュを停止します。

## <code>-P</code> {#code-p-code}

-   TiDBサービスの監視ポート
-   デフォルト： `"4000"`
-   TiDBサーバーは、このポートからのMySQLクライアント要求を受け入れます。

## <code>--path</code> {#code-path-code}

-   「unistore」などのローカルストレージエンジンのデータディレクトリへのパス
-   `--store = tikv`の場合、パスを指定する必要があります。 `--store = unistore`の場合、パスを指定しないとデフォルト値が使用されます。
-   TiKVのような分散ストレージエンジンの場合、 `--path`は実際のPDアドレスを指定します。 PDサーバーを192.168.100.113:2379、192.168.100.114:2379、および192.168.100.115:2379にデプロイするとすると、 `--path`の値は「192.168.100.113:2379,192.168.100.114:2379,192.168.100.115:2379」になります。 。
-   デフォルト： `"/tmp/tidb"`
-   `tidb-server --store=unistore --path=""`を使用して、純粋なメモリ内TiDBを有効にすることができます。

## <code>--proxy-protocol-networks</code> {#code-proxy-protocol-networks-code}

-   [PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を使用してTiDBに接続できるプロキシサーバーのIPアドレスのリスト。
-   デフォルト： `""`
-   通常、リバースプロキシの背後でTiDBにアクセスすると、TiDBはリバースプロキシサーバーのIPアドレスをクライアントのIPアドレスとして使用します。 PROXYプロトコルを有効にすることにより、HAProxyなどのこのプロトコルをサポートするリバースプロキシは、実際のクライアントIPアドレスをTiDBに渡すことができます。
-   このフラグを設定した後、TiDBは、設定された送信元IPアドレスがPROXYプロトコルを使用してTiDBに接続できるようにします。 PROXY以外のプロトコルが使用されている場合、この接続は拒否されます。このフラグを空のままにすると、PROXYプロトコルを使用してIPアドレスをTiDBに接続できなくなります。値は、IPアドレス（192.168.1.50）またはCIDR（192.168.1.0/24）で、区切り文字として`,`を使用できます。 `*`は任意のIPアドレスを意味します。

> **警告：**
>
> `*`は、任意のIPアドレスのクライアントがそのIPアドレスを報告できるようにすることでセキュリティリスクをもたらす可能性があるため、注意して使用してください。さらに、 `*`を使用すると、TiDBに直接接続する内部コンポーネント（TiDBダッシュボードなど）が使用できなくなる可能性もあります。

## <code>--proxy-protocol-header-timeout</code> {#code-proxy-protocol-header-timeout-code}

-   PROXYプロトコルヘッダー読み取りのタイムアウト
-   デフォルト： `5` （秒）

    > **ノート：**
    >
    > 値を`0`に設定しないでください。特別な状況を除いて、デフォルト値を使用してください。

## <code>--report-status</code> {#code-report-status-code}

-   ステータスレポートとpprofツールを有効（ `true` ）または無効（ `false` ）にします
-   デフォルト： `true`
-   `true`に設定すると、このパラメーターはメトリックとpprofを有効にします。 `false`に設定すると、このパラメーターはメトリックとpprofを無効にします。

## <code>--run-ddl</code> {#code-run-ddl-code}

-   `tidb-server`がDDLステートメントを実行するかどうかを確認し、クラスタで`tidb-server`の数が2を超える場合に設定します
-   デフォルト： `true`
-   値は（true）または（false）になります。 （true）は、 `tidb-server`がDDL自体を実行することを示します。 （false）は、 `tidb-server`がDDL自体を実行しないことを示します。

## <code>--socket string</code> {#code-socket-string-code}

-   TiDBサービスは、外部接続にunixソケットファイルを使用します。
-   デフォルト： `""`
-   `/tmp/tidb.sock`を使用してUNIXソケットファイルを開きます。

## <code>--status</code> {#code-status-code}

-   TiDBサーバーのステータスレポートポート
-   デフォルト： `"10080"`
-   このポートは、サーバーの内部データを取得するために使用されます。データには[プロメテウスメトリクス](https://prometheus.io/)と[pprof](https://golang.org/pkg/net/http/pprof/)が含まれます。
-   Prometheusメトリックには`"http://host:status_port/metrics"`でアクセスできます。
-   pprofデータには`"http://host:status_port/debug/pprof"`でアクセスできます。

## <code>--status-host</code> {#code-status-host-code}

-   TiDBサービスのステータスを監視するために使用される`HOST`
-   デフォルト： `0.0.0.0`

## <code>--store</code> {#code-store-code}

-   最下層でTiDBが使用するストレージエンジンを指定します
-   デフォルト： `"unistore"`
-   「unistore」または「tikv」を選択できます。 （「unistore」はローカルストレージエンジン、「tikv」は分散ストレージエンジンです）

## <code>--token-limit</code> {#code-token-limit-code}

-   TiDBで同時に実行できるセッションの数。交通管制に使用されます。
-   デフォルト： `1000`
-   同時セッションの数が`token-limit`より大きい場合、要求はブロックされ、終了した操作がトークンを解放するのを待機します。

## <code>-V</code> {#code-v-code}

-   TiDBのバージョンを出力します
-   デフォルト： `""`

## <code>--plugin-dir</code> {#code-plugin-dir-code}

-   プラグインのストレージディレクトリ。
-   デフォルト： `"/data/deploy/plugin"`

## <code>--plugin-load</code> {#code-plugin-load-code}

-   ロードするプラグインの名前。それぞれがコンマで区切られています。
-   デフォルト： `""`

## <code>--affinity-cpus</code> {#code-affinity-cpus-code}

-   TiDBサーバーのCPUアフィニティをコンマで区切って設定します。たとえば、「1,2,3」。
-   デフォルト： `""`

## <code>--repair-mode</code> {#code-repair-mode-code}

-   データ修復シナリオでのみ使用される修復モードを有効にするかどうかを決定します。
-   デフォルト： `false`

## <code>--repair-list</code> {#code-repair-list-code}

-   修復モードで修復されるテーブルの名前。
-   デフォルト： `""`
